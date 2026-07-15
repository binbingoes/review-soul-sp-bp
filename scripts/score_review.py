#!/usr/bin/env python3
"""Deterministically validate and score a SOUL SP/BP review card."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


WEIGHTS = {
    "soul_alignment": 12,
    "unique_value_trust": 10,
    "facts_swot_tows": 10,
    "ansoff_curves": 10,
    "wtp_htw_control": 14,
    "sp_bp_milestones": 12,
    "financial_quality": 14,
    "evidence_budget_gates": 12,
    "ai_org_accountability": 6,
}

GATES = (
    "redlines",
    "unique_value",
    "strategic_choice",
    "evidence",
    "commercial_closure",
    "budget_traceability",
    "accountability",
)

TERMINATE_GATES = {"redlines", "unique_value", "commercial_closure"}
VALID_STATUSES = {"pass", "fail", "unknown"}
VALID_EVIDENCE = {"E0", "E1", "E2", "E3", "E4"}
VALID_ANSOFF = {
    "market_penetration",
    "market_development",
    "product_development",
    "diversification",
    "platform_enablement",
}
VALID_BUSINESS_TYPES = {
    "consumer_product",
    "commercial_b2b",
    "odm",
    "platform_function",
    "company_portfolio",
}
VALID_STAGES = {
    "survival",
    "turnaround",
    "growth",
    "scale",
    "incubation",
    "transformation",
}
VALID_PACK_STATUSES = {"complete", "partial", "missing"}
VALID_REVIEW_MODES = {"self_check", "peer_review", "portfolio"}
REQUIRED_PERIOD_KEYS = ("sp", "bp", "budget")
VERDICT_ORDER = {"终止": 0, "暂停": 1, "验证": 2, "通过": 3}


class InputError(ValueError):
    pass


def load_input(path: str) -> dict[str, Any]:
    if path == "-":
        return json.load(sys.stdin)
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def require_mapping(data: dict[str, Any], key: str) -> dict[str, Any]:
    value = data.get(key)
    if not isinstance(value, dict):
        raise InputError(f"{key} must be an object")
    return value


def validate_and_score(data: dict[str, Any]) -> dict[str, Any]:
    gates = require_mapping(data, "hard_gates")
    scores = require_mapping(data, "dimension_scores")
    periods = require_mapping(data, "periods")
    opportunities = data.get("opportunities")
    if not isinstance(opportunities, list) or not 1 <= len(opportunities) <= 3:
        raise InputError("opportunities must contain 1 to 3 items")

    review_mode = data.get("review_mode", "peer_review")
    if review_mode not in VALID_REVIEW_MODES:
        raise InputError("review_mode must be self_check, peer_review, or portfolio")

    gate_rows: list[dict[str, str]] = []
    for gate in GATES:
        item = gates.get(gate)
        if not isinstance(item, dict):
            raise InputError(f"hard_gates.{gate} must be an object")
        status = item.get("status")
        if status not in VALID_STATUSES:
            raise InputError(f"hard_gates.{gate}.status must be pass, fail, or unknown")
        gate_rows.append(
            {"gate": gate, "status": status, "evidence": str(item.get("evidence", ""))}
        )

    weighted_score = 0.0
    score_rows: list[dict[str, Any]] = []
    for key, weight in WEIGHTS.items():
        if key not in scores:
            raise InputError(f"dimension_scores.{key} is required")
        value = scores[key]
        if not isinstance(value, (int, float)) or not 0 <= value <= 10:
            raise InputError(f"dimension_scores.{key} must be a number from 0 to 10")
        contribution = float(value) * weight / 10
        weighted_score += contribution
        score_rows.append(
            {"dimension": key, "score": float(value), "weight": weight, "points": contribution}
        )

    # Avoid binary floating-point drift at exact rubric thresholds such as 80.0.
    weighted_score = round(weighted_score, 10)

    findings: list[str] = []
    critical_baseline_gap = False
    source_packs = data.get("source_packs")
    if not isinstance(source_packs, dict):
        critical_baseline_gap = True
        findings.append("source_packs is missing")
        source_packs = {}
    for pack_name in ("business_product", "finance"):
        pack = source_packs.get(pack_name)
        if not isinstance(pack, dict):
            critical_baseline_gap = True
            findings.append(f"source_packs.{pack_name} is missing")
            continue
        status = pack.get("status")
        if status not in VALID_PACK_STATUSES:
            critical_baseline_gap = True
            findings.append(f"source_packs.{pack_name}.status is missing or invalid")
        elif status != "complete":
            critical_baseline_gap = True
            findings.append(f"source_packs.{pack_name} is {status}")
        for field in ("owner", "as_of"):
            if not str(pack.get(field, "")).strip():
                critical_baseline_gap = True
                findings.append(f"source_packs.{pack_name}.{field} is missing")

    profile = data.get("business_profile")
    if not isinstance(profile, dict):
        critical_baseline_gap = True
        profile = {}
        findings.append("business_profile is missing")
    else:
        business_type = profile.get("business_type")
        stage = profile.get("stage")
        if business_type not in VALID_BUSINESS_TYPES:
            critical_baseline_gap = True
            findings.append("business_profile.business_type is missing or invalid")
        if stage not in VALID_STAGES:
            critical_baseline_gap = True
            findings.append("business_profile.stage is missing or invalid")
        for field in ("classification_evidence", "classification_confidence"):
            if not str(profile.get(field, "")).strip():
                critical_baseline_gap = True
                findings.append(f"business_profile.{field} is missing")

    baseline_metrics = data.get("baseline_metrics")
    baseline_count = 0
    if not isinstance(baseline_metrics, list) or not baseline_metrics:
        critical_baseline_gap = True
        findings.append("baseline_metrics must contain at least one operating baseline")
        baseline_metrics = []
    for index, metric in enumerate(baseline_metrics, start=1):
        if not isinstance(metric, dict):
            critical_baseline_gap = True
            findings.append(f"baseline_metrics[{index - 1}] must be an object")
            continue
        baseline_count += 1
        required_metric_fields = (
            "name",
            "definition",
            "baseline_period",
            "source",
            "owner",
            "target_period",
            "gap",
            "driver",
            "decision_impact",
            "due_date",
        )
        missing_metric_fields = [
            field for field in required_metric_fields if not str(metric.get(field, "")).strip()
        ]
        if missing_metric_fields:
            critical_baseline_gap = True
            findings.append(
                f"baseline metric {index}: missing {', '.join(missing_metric_fields)}"
            )
        if metric.get("baseline_value") is None or str(metric.get("source", "")).upper() == "GAP":
            critical_baseline_gap = True
            findings.append(f"baseline metric {index}: baseline value remains GAP")
        if "target_value" not in metric or metric.get("target_value") is None:
            critical_baseline_gap = True
            findings.append(f"baseline metric {index}: target_value is missing")
    boundary_pack = data.get("boundary_pack")
    boundary_gap = False
    if review_mode == "portfolio":
        if not isinstance(boundary_pack, dict):
            boundary_gap = True
            findings.append("boundary_pack is required in portfolio mode")
        else:
            if boundary_pack.get("status") != "complete":
                boundary_gap = True
                findings.append("boundary_pack is not complete")
            for field in ("owner", "as_of"):
                if not str(boundary_pack.get(field, "")).strip():
                    boundary_gap = True
                    findings.append(f"boundary_pack.{field} is missing")
    # Periods are organization-specific. Validate presence, but never impose
    # a private company's dates on a public skill distribution.
    period_mismatch = False
    for key in REQUIRED_PERIOD_KEYS:
        actual = periods.get(key)
        if not str(actual or "").strip():
            critical_baseline_gap = True
            findings.append(f"period missing: {key}")

    opportunity_rows: list[dict[str, Any]] = []
    has_early_evidence = False
    critical_opportunity_gap = False
    irreversible_before_e3 = False
    for index, opportunity in enumerate(opportunities, start=1):
        if not isinstance(opportunity, dict):
            raise InputError(f"opportunities[{index - 1}] must be an object")
        name = str(opportunity.get("name", "")).strip()
        if not name:
            raise InputError(f"opportunities[{index - 1}].name is required")
        evidence_level = opportunity.get("evidence_level")
        if evidence_level not in VALID_EVIDENCE:
            raise InputError(f"{name}: evidence_level must be E0 through E4")
        ansoff = opportunity.get("ansoff")
        if ansoff not in VALID_ANSOFF:
            raise InputError(f"{name}: invalid ansoff classification")
        curve = opportunity.get("curve")
        if curve not in {1, 2, 3}:
            raise InputError(f"{name}: curve must be 1, 2, or 3")

        level_number = int(evidence_level[1])
        if level_number < 3:
            has_early_evidence = True
        irreversible = bool(opportunity.get("irreversible_investment", False))
        if irreversible and level_number < 3:
            irreversible_before_e3 = True
            findings.append(f"{name}: irreversible investment requested at {evidence_level}, below E3")

        required_text = (
            "unique_value_evidence",
            "control_point",
            "evidence_purchase",
            "budget_release_condition",
            "stop_condition",
            "owner",
            "decision_authority",
            "sp_milestone",
            "bp_milestone",
            "review_date",
        )
        missing = [field for field in required_text if not str(opportunity.get(field, "")).strip()]
        if missing:
            critical_opportunity_gap = True
            findings.append(f"{name}: missing {', '.join(missing)}")

        opportunity_rows.append(
            {
                "name": name,
                "ansoff": ansoff,
                "curve": curve,
                "evidence_level": evidence_level,
                "irreversible_investment": irreversible,
            }
        )

    failed_terminate = [row["gate"] for row in gate_rows if row["status"] == "fail" and row["gate"] in TERMINATE_GATES]
    failed_pause = [row["gate"] for row in gate_rows if row["status"] == "fail" and row["gate"] not in TERMINATE_GATES]
    unknown = [row["gate"] for row in gate_rows if row["status"] == "unknown"]

    if failed_terminate:
        verdict = "终止"
        findings.append("termination hard gate failed: " + ", ".join(failed_terminate))
    elif failed_pause or unknown or critical_opportunity_gap or critical_baseline_gap or boundary_gap:
        verdict = "暂停"
        if failed_pause:
            findings.append("pause hard gate failed: " + ", ".join(failed_pause))
        if unknown:
            findings.append("unknown hard gate: " + ", ".join(unknown))
        if boundary_gap:
            findings.append("portfolio boundary pack is incomplete")
    elif weighted_score >= 80:
        verdict = "通过"
    elif weighted_score >= 65:
        verdict = "验证"
    else:
        verdict = "暂停"

    if verdict == "通过" and (has_early_evidence or irreversible_before_e3):
        verdict = "验证"
        findings.append("verdict capped at 验证 because at least one opportunity is below E3")
    if irreversible_before_e3 and critical_opportunity_gap:
        verdict = "暂停"

    confidence = "High"
    if unknown or critical_opportunity_gap or critical_baseline_gap or findings:
        confidence = "Medium"
    if unknown or len(findings) >= 3:
        confidence = "Low"

    score_valid = (
        not critical_baseline_gap
        and not critical_opportunity_gap
        and not boundary_gap
        and not unknown
        and not period_mismatch
    )
    return {
        "scope_name": data.get("scope_name", ""),
        "version": data.get("version", ""),
        "owner": data.get("owner", ""),
        "review_mode": review_mode,
        "source_packs": source_packs,
        "boundary_pack": boundary_pack,
        "business_profile": profile,
        "baseline_metric_count": baseline_count,
        "verdict": verdict,
        "score_valid": score_valid,
        "weighted_score": round(weighted_score, 1) if score_valid else None,
        "confidence": confidence,
        "hard_gates": gate_rows,
        "dimension_scores": score_rows,
        "opportunities": opportunity_rows,
        "findings": findings,
    }


def markdown_report(result: dict[str, Any]) -> str:
    lines = [
        "# SOUL SP/BP review result",
        "",
        f"- Scope: {result['scope_name']}",
        f"- Version: {result['version']}",
        f"- Owner: {result['owner']}",
        f"- Review mode: {result['review_mode']}",
        f"- Business type: {result['business_profile'].get('business_type', '')}",
        f"- Stage: {result['business_profile'].get('stage', '')}",
        f"- Baseline metrics: {result['baseline_metric_count']}",
        f"- Verdict: **{result['verdict']}**",
        (
            f"- Weighted score: **{result['weighted_score']}/100**"
            if result["score_valid"]
            else "- Weighted score: **暂不评分（资料不完整）**"
        ),
        f"- Confidence: **{result['confidence']}**",
        "",
        "## Hard gates",
        "",
        "| Gate | Status | Evidence |",
        "|---|---|---|",
    ]
    for row in result["hard_gates"]:
        lines.append(f"| {row['gate']} | {row['status']} | {row['evidence']} |")
    lines.extend(["", "## Opportunities", "", "| Name | Ansoff | Curve | Evidence | Irreversible |", "|---|---|---:|---|---|"])
    for row in result["opportunities"]:
        lines.append(
            f"| {row['name']} | {row['ansoff']} | {row['curve']} | {row['evidence_level']} | {row['irreversible_investment']} |"
        )
    lines.extend(["", "## Findings", ""])
    if result["findings"]:
        lines.extend(f"- {finding}" for finding in result["findings"])
    else:
        lines.append("- No deterministic validation gaps found.")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="JSON review card path, or - for stdin")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    args = parser.parse_args()
    try:
        result = validate_and_score(load_input(args.input))
    except (OSError, json.JSONDecodeError, InputError) as exc:
        print(f"input_error: {exc}", file=sys.stderr)
        return 2
    if args.format == "json":
        json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
        print()
    else:
        print(markdown_report(result), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
