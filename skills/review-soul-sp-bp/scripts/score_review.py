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
    "smart_hardware_product",
    "ai_hardware_product",
    "commercial_hardware",
    "odm_hardware",
    "hardware_platform_function",
    "hardware_portfolio",
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
VALID_METRIC_SUBJECTS = {
    "recognized_revenue",
    "sell_out",
    "sell_in",
    "bookings",
    "backlog",
    "gross_profit",
    "gross_margin",
    "operating_profit",
    "net_profit",
    "cash",
    "collection",
    "inventory",
    "unit_efficiency",
    "quality",
    "trust",
    "delivery",
    "cycle_time",
    "adoption",
    "reuse",
    "downstream_value",
    "risk_avoided",
    "capacity",
    "ai_package_human_package",
    "bom_cost",
    "yield",
    "warranty_return",
    "service_sla",
    "model_quality",
    "ota_reliability",
    "privacy_security",
}
VALID_RESULT_CLASSES = {
    "business_result",
    "economics",
    "cash",
    "trust_quality",
    "cycle",
    "adoption",
    "downstream_value",
    "capacity",
    "risk",
}
LEADING_RESULT_SUBJECTS = {"sell_in", "bookings", "backlog"}
REQUIRED_RESULT_CLASSES = {
    "consumer_product": {"business_result", "economics", "cash", "trust_quality"},
    "commercial_b2b": {"business_result", "economics", "cash", "trust_quality"},
    "odm": {"business_result", "economics", "cash", "trust_quality"},
    "company_portfolio": {"business_result", "economics", "cash", "trust_quality"},
    "smart_hardware_product": {"business_result", "economics", "cash", "trust_quality"},
    "ai_hardware_product": {"business_result", "economics", "cash", "trust_quality"},
    "commercial_hardware": {"business_result", "economics", "cash", "trust_quality"},
    "odm_hardware": {"business_result", "economics", "cash", "trust_quality"},
    "hardware_portfolio": {"business_result", "economics", "cash", "trust_quality"},
    "platform_function": {"cycle", "adoption", "downstream_value", "trust_quality"},
    "hardware_platform_function": {"cycle", "adoption", "downstream_value", "trust_quality"},
}
REQUIRED_HARDWARE_PROFILE_FIELDS = (
    "device_scope",
    "user_scenario",
    "device_ai_service_loop",
    "manufacturing_or_delivery_stage",
    "trust_safety_boundary",
)
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

    findings: list[str] = []
    critical_baseline_gap = False
    gate_rows: list[dict[str, Any]] = []
    evidence_ledger = data.get("evidence_ledger")
    ledger_ids = set()
    if isinstance(evidence_ledger, list):
        ledger_ids = {
            str(item.get("id")).strip()
            for item in evidence_ledger
            if isinstance(item, dict) and str(item.get("id", "")).strip()
        }
        if not ledger_ids:
            critical_baseline_gap = True
            findings.append("evidence_ledger must contain at least one identified source")
    else:
        critical_baseline_gap = True
        findings.append("evidence_ledger is missing")
    for gate in GATES:
        item = gates.get(gate)
        if not isinstance(item, dict):
            raise InputError(f"hard_gates.{gate} must be an object")
        status = item.get("status")
        if status not in VALID_STATUSES:
            raise InputError(f"hard_gates.{gate}.status must be pass, fail, or unknown")
        evidence_refs = item.get("evidence_refs", [])
        if status == "pass":
            if not isinstance(evidence_refs, list) or not evidence_refs:
                critical_baseline_gap = True
                findings.append(f"hard gate {gate}: evidence_refs are required for pass")
            elif ledger_ids and any(str(ref).strip() not in ledger_ids for ref in evidence_refs):
                critical_baseline_gap = True
                findings.append(f"hard gate {gate}: an evidence_ref is not in evidence_ledger")
        gate_rows.append(
            {
                "gate": gate,
                "status": status,
                "evidence": str(item.get("evidence", "")),
                "evidence_refs": [str(ref) for ref in evidence_refs] if isinstance(evidence_refs, list) else [],
            }
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

    goal_pack = data.get("goal_pack")
    if not isinstance(goal_pack, dict):
        critical_baseline_gap = True
        findings.append("goal_pack is missing")
        goal_pack = {}
    else:
        if goal_pack.get("status") != "complete":
            critical_baseline_gap = True
            findings.append("goal_pack is not complete")
        for field in ("source", "owner", "as_of"):
            if not str(goal_pack.get(field, "")).strip():
                critical_baseline_gap = True
                findings.append(f"goal_pack.{field} is missing")

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

    hardware_profile = data.get("hardware_profile")
    if not isinstance(hardware_profile, dict):
        critical_baseline_gap = True
        findings.append("hardware_profile is missing")
        hardware_profile = {}
    else:
        for field in REQUIRED_HARDWARE_PROFILE_FIELDS:
            if not str(hardware_profile.get(field, "")).strip():
                critical_baseline_gap = True
                findings.append(f"hardware_profile.{field} is missing")

    baseline_metrics = data.get("baseline_metrics")
    baseline_count = 0
    metric_subjects: set[str] = set()
    result_classes: set[str] = set()
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
            "metric_subject",
            "result_class",
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
        subject = str(metric.get("metric_subject", "")).strip()
        result_class = str(metric.get("result_class", "")).strip()
        if subject and subject not in VALID_METRIC_SUBJECTS:
            critical_baseline_gap = True
            findings.append(f"baseline metric {index}: invalid metric_subject '{subject}'")
        if result_class and result_class not in VALID_RESULT_CLASSES:
            critical_baseline_gap = True
            findings.append(f"baseline metric {index}: invalid result_class '{result_class}'")
        if subject:
            metric_subjects.add(subject)
        if result_class:
            result_classes.add(result_class)
        if result_class == "business_result" and subject in LEADING_RESULT_SUBJECTS:
            findings.append(
                f"baseline metric {index}: {subject} is a leading indicator, not a verified business result"
            )

    business_type = profile.get("business_type", "")
    required_classes = REQUIRED_RESULT_CLASSES.get(business_type, set())
    missing_classes = sorted(required_classes - result_classes)
    if missing_classes:
        critical_baseline_gap = True
        findings.append("baseline metric coverage missing: " + ", ".join(missing_classes))
    if business_type in {
        "consumer_product",
        "commercial_b2b",
        "odm",
        "company_portfolio",
        "smart_hardware_product",
        "ai_hardware_product",
        "commercial_hardware",
        "odm_hardware",
        "hardware_portfolio",
    } and not ({"recognized_revenue", "sell_out"} & metric_subjects):
        critical_baseline_gap = True
        findings.append("baseline metric coverage missing: recognized_revenue or sell_out")
    if business_type in {"platform_function", "hardware_platform_function"} and "downstream_value" not in metric_subjects:
        critical_baseline_gap = True
        findings.append("platform baseline metric coverage missing: downstream_value")

    causal_bridges = data.get("causal_bridges")
    causal_opportunities: set[str] = set()
    if not isinstance(causal_bridges, list) or not causal_bridges:
        critical_baseline_gap = True
        findings.append("causal_bridges must contain at least one structured causal link")
        causal_bridges = []
    for index, bridge in enumerate(causal_bridges, start=1):
        if not isinstance(bridge, dict):
            critical_baseline_gap = True
            findings.append(f"causal_bridges[{index - 1}] must be an object")
            continue
        required_bridge_fields = (
            "opportunity",
            "action",
            "result_metric",
            "baseline",
            "target",
            "owner",
            "source",
        )
        missing = [field for field in required_bridge_fields if not str(bridge.get(field, "")).strip()]
        if missing:
            critical_baseline_gap = True
            findings.append(f"causal bridge {index}: missing {', '.join(missing)}")
        opportunity_name = str(bridge.get("opportunity", "")).strip()
        if opportunity_name:
            causal_opportunities.add(opportunity_name)
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
            conflicts = boundary_pack.get("conflicts", [])
            if not isinstance(conflicts, list):
                boundary_gap = True
                findings.append("boundary_pack.conflicts must be a list")
                conflicts = []
            for index, conflict in enumerate(conflicts, start=1):
                if not isinstance(conflict, dict):
                    boundary_gap = True
                    findings.append(f"boundary conflict {index}: must be an object")
                    continue
                required_conflict_fields = ("type", "status", "owner", "resolver", "due_date", "result_impact")
                missing = [field for field in required_conflict_fields if not str(conflict.get(field, "")).strip()]
                if missing:
                    boundary_gap = True
                    findings.append(f"boundary conflict {index}: missing {', '.join(missing)}")
                status = str(conflict.get("status", "")).strip().lower()
                if status not in {"resolved", "closed", "accepted"}:
                    boundary_gap = True
                    findings.append(f"boundary conflict {index}: unresolved")
        circle_packs = data.get("circle_packs")
        if not isinstance(circle_packs, list) or len(circle_packs) < 2:
            boundary_gap = True
            findings.append("circle_packs must contain at least two independent circle packs in portfolio mode")
        else:
            for index, circle_pack in enumerate(circle_packs, start=1):
                if not isinstance(circle_pack, dict):
                    boundary_gap = True
                    findings.append(f"circle_packs[{index - 1}] must be an object")
                    continue
                for field in ("scope_name", "status", "owner", "as_of"):
                    if not str(circle_pack.get(field, "")).strip():
                        boundary_gap = True
                        findings.append(f"circle_packs[{index}].{field} is missing")
                if circle_pack.get("status") != "complete":
                    boundary_gap = True
                    findings.append(f"circle_packs[{index}] is not complete")
    critical_opportunity_gap = False
    budget_lines = data.get("budget_lines")
    budget_line_names: set[str] = set()
    if not isinstance(budget_lines, list) or not budget_lines:
        critical_opportunity_gap = True
        findings.append("budget_lines must contain at least one row from goal.md")
        budget_lines = []
    for index, line in enumerate(budget_lines, start=1):
        if not isinstance(line, dict):
            critical_opportunity_gap = True
            findings.append(f"budget_lines[{index - 1}] must be an object")
            continue
        required_budget_fields = (
            "budget_line",
            "sp_opportunity",
            "bp_milestone",
            "budget_period",
            "amount",
            "currency",
            "evidence_purchase",
            "release_condition",
            "stop_condition",
            "owner",
            "authority",
            "review_date",
        )
        missing = [field for field in required_budget_fields if line.get(field) is None or not str(line.get(field, "")).strip()]
        if missing:
            critical_opportunity_gap = True
            findings.append(f"budget line {index}: missing {', '.join(missing)}")
        amount = line.get("amount")
        if not isinstance(amount, (int, float)) or amount < 0:
            critical_opportunity_gap = True
            findings.append(f"budget line {index}: amount must be a non-negative number")
        opportunity_name = str(line.get("sp_opportunity", "")).strip()
        if opportunity_name:
            budget_line_names.add(opportunity_name)
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

    opportunity_names = {row["name"] for row in opportunity_rows}
    missing_causal = sorted(opportunity_names - causal_opportunities)
    if missing_causal:
        critical_baseline_gap = True
        findings.append("causal bridge missing for: " + ", ".join(missing_causal))
    missing_budget = sorted(opportunity_names - budget_line_names)
    if missing_budget:
        critical_opportunity_gap = True
        findings.append("budget line missing for: " + ", ".join(missing_budget))
    unknown_budget_opportunities = sorted(budget_line_names - opportunity_names)
    if unknown_budget_opportunities:
        critical_opportunity_gap = True
        findings.append("budget line references unknown opportunity: " + ", ".join(unknown_budget_opportunities))

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
        "goal_pack": goal_pack,
        "boundary_pack": boundary_pack,
        "business_profile": profile,
        "hardware_profile": hardware_profile,
        "baseline_metric_count": baseline_count,
        "budget_line_count": len(budget_lines),
        "metric_subjects": sorted(metric_subjects),
        "result_classes": sorted(result_classes),
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
        f"- Budget lines: {result['budget_line_count']}",
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
