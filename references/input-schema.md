# Deterministic review input

Create a UTF-8 JSON file with this structure before running `scripts/score_review.py`.

```json
{
  "scope_name": "Business or circle name",
  "scope_type": "business",
  "plan_type": "SP+BP",
  "version": "v0.3",
  "owner": "owner name",
  "decision_body": "named decision body",
  "review_date": "YYYY-MM-DD",
  "review_mode": "peer_review",
  "source_packs": {
    "business_product": {"status": "complete", "owner": "business owner", "as_of": "YYYY-MM-DD"},
    "finance": {"status": "complete", "owner": "finance partner", "as_of": "YYYY-MM-DD"}
  },
  "boundary_pack": {
    "status": "complete",
    "owner": "portfolio owner",
    "as_of": "YYYY-MM-DD",
    "conflicts": []
  },
  "business_profile": {
    "business_type": "consumer_product",
    "stage": "growth",
    "primary_constraint": "channel",
    "classification_evidence": "demand and economics are evidenced, repeatability is not mature",
    "classification_confidence": "Medium"
  },
  "periods": {
    "sp": "<SP start>—<SP end>",
    "bp": "<BP start>—<BP end>",
    "budget": "<budget period>"
  },
  "hard_gates": {
    "redlines": {"status": "pass", "evidence": "source or finding"},
    "unique_value": {"status": "pass", "evidence": "source or finding"},
    "strategic_choice": {"status": "pass", "evidence": "source or finding"},
    "evidence": {"status": "pass", "evidence": "source or finding"},
    "commercial_closure": {"status": "pass", "evidence": "source or finding"},
    "budget_traceability": {"status": "pass", "evidence": "source or finding"},
    "accountability": {"status": "pass", "evidence": "source or finding"}
  },
  "dimension_scores": {
    "soul_alignment": 8,
    "unique_value_trust": 7,
    "facts_swot_tows": 6,
    "ansoff_curves": 8,
    "wtp_htw_control": 7,
    "sp_bp_milestones": 8,
    "financial_quality": 7,
    "evidence_budget_gates": 6,
    "ai_org_accountability": 7
  },
  "baseline_metrics": [
    {
      "name": "revenue",
      "definition": "recognized revenue under the named finance definition",
      "baseline_period": "<baseline period>",
      "baseline_value": 100,
      "source": "finance ledger or approved source",
      "owner": "finance partner",
      "target_period": "<target period>",
      "target_value": 130,
      "gap": 30,
      "driver": "price-volume-mix and channel efficiency",
      "decision_impact": "release next budget only after baseline is verified",
      "due_date": "YYYY-MM-DD"
    }
  ],
  "opportunities": [
    {
      "name": "US channel expansion",
      "ansoff": "market_development",
      "curve": 1,
      "evidence_level": "E2",
      "unique_value_evidence": "pilot user and payment evidence",
      "control_point": "owned listing and service loop",
      "evidence_purchase": "limited pilot with payment and margin evidence",
      "irreversible_investment": false,
      "budget_release_condition": "local GTM, margin, service and trust reach E3",
      "stop_condition": "pilot conversion or margin misses threshold by date",
      "owner": "owner name",
      "decision_authority": "named decision authority",
      "sp_milestone": "<SP milestone>",
      "bp_milestone": "<BP milestone>",
      "review_date": "YYYY-MM-DD"
    }
  ],
  "review_findings": [
    {"priority": "P1", "finding": "claim", "action": "exact revision"}
  ]
}
```

Rules:

- Hard-gate status must be `pass`, `fail`, or `unknown`.
- `review_mode` must be `self_check`, `peer_review`, or `portfolio`.
- Dimension scores must include all nine keys and remain between 0 and 10.
- `business_type` must be `consumer_product`, `commercial_b2b`, `odm`, `platform_function`, or `company_portfolio`.
- `stage` must be `survival`, `turnaround`, `growth`, `scale`, `incubation`, or `transformation`.
- Product/business and finance source packs must be tracked separately as `complete`, `partial`, or `missing`.
- The Agent must supply `classification_evidence` and `classification_confidence`; owners supply facts, not framework labels.
- Baseline metrics must state definition, baseline period/value, source, owner, target period/value, and due date. Use `null` plus source `GAP` when unavailable; the formal verdict will be capped at `暂停`.
- Baseline metrics should also state `gap`, `driver`, and `decision_impact`; missing critical fields are a formal-review gap.
- Opportunities/initiatives must contain one to three items.
- Each opportunity should state its control point, evidence purchase, decision authority, and review date. Missing release/stop/owner/milestone fields cap the verdict at `暂停`.
- `evidence_level` must be `E0` through `E4`.
- `ansoff` must be `market_penetration`, `market_development`, `product_development`, or `diversification`. Platform/function initiatives may use `platform_enablement`.
- `curve` must be 1, 2, or 3.
- Use the same structure for human and Agent reviews.
- Do not fabricate this JSON from an incomplete draft. If source packs, baselines, hard gates, or opportunity fields are incomplete, use preliminary mode and report `暂不评分（资料不完整）`.
