# Deterministic review input

Create a UTF-8 JSON file with this structure before running `scripts/score_review.py`.

The JSON is the review record, not the source of truth. `goal.md` supplies the approved periods, goals, thresholds, budget lines, and owners; the evidence ledger supplies the facts that support hard-gate claims.

```json
{
  "scope_name": "Example AI hardware line",
  "scope_type": "business",
  "plan_type": "SP+BP",
  "version": "v1",
  "owner": "owner name",
  "decision_body": "named decision body",
  "review_date": "YYYY-MM-DD",
  "review_mode": "peer_review",
  "source_packs": {
    "business_product": {"status": "complete", "owner": "business owner", "as_of": "YYYY-MM-DD"},
    "finance": {"status": "complete", "owner": "finance partner", "as_of": "YYYY-MM-DD"}
  },
  "goal_pack": {
    "status": "complete",
    "source": "goal.md v1",
    "owner": "strategy/finance owner",
    "as_of": "YYYY-MM-DD"
  },
  "hardware_profile": {
    "device_scope": "connected device with embedded AI and service layer",
    "user_scenario": "specific home or professional scenario",
    "device_ai_service_loop": "device input -> model decision -> safe action -> human feedback",
    "manufacturing_or_delivery_stage": "pilot with production and service readiness evidence",
    "trust_safety_boundary": "privacy, security, certification, and human-override boundary"
  },
  "boundary_pack": {
    "status": "complete",
    "owner": "portfolio owner",
    "as_of": "YYYY-MM-DD",
    "conflicts": []
  },
  "circle_packs": [],
  "evidence_ledger": [
    {"id": "EVID-001", "fact_type": "recognized revenue", "source": "approved finance source", "as_of": "YYYY-MM-DD"},
    {"id": "EVID-002", "fact_type": "user and payment evidence", "source": "approved product source", "as_of": "YYYY-MM-DD"}
  ],
  "business_profile": {
    "business_type": "ai_hardware_product",
    "stage": "growth",
    "primary_constraint": "delivery and service capacity",
    "classification_evidence": "demand and economics are evidenced, repeatability is not mature",
    "classification_confidence": "Medium"
  },
  "periods": {
    "sp": "<SP start>—<SP end>",
    "bp": "<BP start>—<BP end>",
    "budget": "<budget period>"
  },
  "hard_gates": {
    "redlines": {"status": "pass", "evidence": "red-line review complete", "evidence_refs": ["EVID-002"]},
    "unique_value": {"status": "pass", "evidence": "user-perceived differentiated value", "evidence_refs": ["EVID-002"]},
    "strategic_choice": {"status": "pass", "evidence": "choice, sacrifice, and control point are explicit", "evidence_refs": ["EVID-002"]},
    "evidence": {"status": "pass", "evidence": "claims map to source ledger", "evidence_refs": ["EVID-001", "EVID-002"]},
    "commercial_closure": {"status": "pass", "evidence": "result, economics, cash, trust, and delivery bridge", "evidence_refs": ["EVID-001"]},
    "budget_traceability": {"status": "pass", "evidence": "goal line maps to SP, BP, and evidence purchase", "evidence_refs": ["EVID-001"]},
    "accountability": {"status": "pass", "evidence": "owner, authority, and review date are named", "evidence_refs": ["EVID-001"]}
  },
  "dimension_scores": {
    "soul_alignment": 8,
    "unique_value_trust": 7,
    "facts_swot_tows": 8,
    "ansoff_curves": 8,
    "wtp_htw_control": 8,
    "sp_bp_milestones": 8,
    "financial_quality": 7,
    "evidence_budget_gates": 8,
    "ai_org_accountability": 7
  },
  "baseline_metrics": [
    {
      "name": "recognized revenue",
      "definition": "recognized revenue under the named finance definition",
      "metric_subject": "recognized_revenue",
      "result_class": "business_result",
      "baseline_period": "<baseline period>",
      "baseline_value": 100,
      "source": "approved finance source",
      "owner": "finance partner",
      "target_period": "<target period>",
      "target_value": 130,
      "gap": 30,
      "driver": "price-volume-mix and adoption",
      "decision_impact": "release only after baseline and causal bridge are verified",
      "due_date": "YYYY-MM-DD"
    },
    {
      "name": "gross margin",
      "definition": "gross profit divided by recognized revenue, including agreed hardware and service cost",
      "metric_subject": "gross_margin",
      "result_class": "economics",
      "baseline_period": "<baseline period>",
      "baseline_value": 0.35,
      "source": "approved finance source",
      "owner": "finance partner",
      "target_period": "<target period>",
      "target_value": 0.4,
      "gap": 0.05,
      "driver": "BOM, yield, price, service, and mix",
      "decision_impact": "no scale before healthy economics are verified",
      "due_date": "YYYY-MM-DD"
    },
    {
      "name": "cash collection",
      "definition": "cash collected from the scoped business result",
      "metric_subject": "cash",
      "result_class": "cash",
      "baseline_period": "<baseline period>",
      "baseline_value": 80,
      "source": "approved finance source",
      "owner": "finance partner",
      "target_period": "<target period>",
      "target_value": 100,
      "gap": 20,
      "driver": "collection, inventory, and channel terms",
      "decision_impact": "protect working capital before expansion",
      "due_date": "YYYY-MM-DD"
    },
    {
      "name": "quality and trust",
      "definition": "agreed defect, failure, privacy/security, warranty, and service indicators",
      "metric_subject": "quality",
      "result_class": "trust_quality",
      "baseline_period": "<baseline period>",
      "baseline_value": 0.98,
      "source": "approved quality/service source",
      "owner": "quality/service owner",
      "target_period": "<target period>",
      "target_value": 0.995,
      "gap": 0.015,
      "driver": "firmware, test coverage, service readiness, and incident response",
      "decision_impact": "stop exposure or release if red-line indicators miss threshold",
      "due_date": "YYYY-MM-DD"
    }
  ],
  "causal_bridges": [
    {
      "opportunity": "validated growth lane",
      "action": "pilot the device-plus-AI closed loop in the named scenario",
      "result_metric": "recognized revenue, gross margin, cash, adoption, and quality",
      "baseline": "baseline metric IDs and values",
      "target": "goal.md target and milestone",
      "owner": "business owner",
      "source": "approved product and finance sources"
    }
  ],
  "budget_lines": [
    {
      "budget_line": "validation package 1",
      "sp_opportunity": "validated growth lane",
      "bp_milestone": "<BP milestone>",
      "budget_period": "<budget period>",
      "amount": 100,
      "currency": "<currency>",
      "evidence_purchase": "smallest pilot that verifies adoption, margin, service, and trust",
      "release_condition": "goal.md E3-equivalent condition is met",
      "stop_condition": "conversion, margin, quality, cash, or trust misses threshold by review date",
      "owner": "business owner",
      "authority": "named release authority",
      "review_date": "YYYY-MM-DD"
    }
  ],
  "review_findings": [
    {"priority": "P1", "finding": "claim", "action": "exact revision"}
  ]
}
```

Rules:

- Hard-gate status must be `pass`, `fail`, or `unknown`. A `pass` must include `evidence_refs` that exist in `evidence_ledger`; free-text evidence alone is not enough.
- `review_mode` must be `self_check`, `peer_review`, or `portfolio`.
- Dimension scores must include all nine keys and remain between 0 and 10.
- `goal_pack` must point to an approved/populated `goal.md`; without it, use preliminary mode.
- `business_type` must be one of `consumer_product`, `commercial_b2b`, `odm`, `platform_function`, `company_portfolio`, `smart_hardware_product`, `ai_hardware_product`, `commercial_hardware`, `odm_hardware`, `hardware_platform_function`, or `hardware_portfolio`.
- `hardware_profile` must describe device scope, user scenario, device/AI/service loop, manufacturing or delivery stage, and trust/safety boundary.
- `stage` must be `survival`, `turnaround`, `growth`, `scale`, `incubation`, or `transformation`.
- Product/business and finance source packs must be tracked separately as `complete`, `partial`, or `missing`.
- Baseline metrics must state `metric_subject` and `result_class` in addition to definition, baseline period/value, source, owner, target period/value, gap, driver, decision impact, and due date.
- Commercial hardware baselines must cover a verified business result (`recognized_revenue` or `sell_out`), economics, cash, and trust/quality. SI, bookings, or backlog alone are leading indicators.
- Platform/function baselines must cover cycle, adoption, downstream value, and trust/quality; direct revenue is not mandatory.
- Every opportunity needs a structured causal bridge and a line-level `budget_lines` row from `goal.md`.
- `budget_lines.amount` must be numeric and non-negative; every line needs currency, release/stop conditions, owner, authority, and review date.
- In portfolio mode, `circle_packs` must contain at least two complete independent circle packs. Every boundary conflict needs type, status, owner, resolver, due date, and result impact; unresolved conflicts force `暂停` and invalidate the score.
- Opportunities/initiatives must contain one to three items, with `evidence_level` `E0` through `E4`, a valid Ansoff quadrant, curve 1/2/3, control point, evidence purchase, decision authority, milestones, and review date.
- Do not fabricate this JSON from an incomplete draft. If goal packs, source packs, baselines, evidence refs, hard gates, causal bridges, budget lines, or opportunity fields are incomplete, use preliminary mode and report `暂不评分（资料不完整）`.
