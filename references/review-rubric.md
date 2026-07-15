# Review rubric

Hard gates override the weighted score.

## Seven hard gates

Use `pass`, `fail`, or `unknown` and cite evidence.

| Gate | Pass condition | Failure consequence |
|---|---|---|
| redlines | safety, integrity, privacy, quality, compliance clear | fail → `终止`; unknown → `暂停` |
| unique_value | differentiated and user-perceived value has evidence | fail → `终止`; unknown → `暂停` |
| strategic_choice | ≤3 opportunities, choice, sacrifice, control point, and portfolio/circle boundary integrity | fail/unknown → `暂停` |
| evidence | claims sourced; E-level and gaps explicit | fail/unknown → `暂停` |
| commercial_closure | growth, margin, cash, trust, delivery form a plausible loop | disproven → `终止`; unknown → `暂停` |
| budget_traceability | SP/BP/budget/evidence/release/stop map is complete | fail/unknown → `暂停` |
| accountability | owner, authority, review date, verification explicit | fail/unknown → `暂停` |

An early opportunity may pass the `evidence` gate at E0-E2 if its uncertainty is honestly labeled and the requested action is only a bounded validation. It cannot receive full or irreversible budget.

Baseline integrity is a mandatory sub-gate of `evidence` and `commercial_closure`. A formal approval cannot receive `通过` when critical metric definitions, comparable baselines, sources, or owners remain missing.

For low-price, ODM, or channel-specific plans, commercial closure requires full-cost economics: dedicated people, quality/testing, warranty/service, returns, inventory, collection, marketing, incentives, brand externality, and shared-capability cost. A positive narrow marginal contribution does not pass the gate.

## Weighted score

Do not use this section in preliminary mode. A numerical score is valid only when both source packs are complete, critical baselines are present, no hard gate is `unknown`, and opportunity ownership/release/stop fields are complete. Otherwise output `暂不评分（资料不完整）`.

Score each dimension from 0 to 10.

| Key | Dimension | Weight |
|---|---|---:|
| soul_alignment | SOUL alignment, red lines, and long-term value | 12 |
| unique_value_trust | distinctive value, premium logic, and trust | 10 |
| facts_swot_tows | factual quality and SWOT/TOWS option logic | 10 |
| ansoff_curves | Ansoff risk and growth-curve migration | 10 |
| wtp_htw_control | Where to Play, How to Win, sacrifice, control point | 14 |
| sp_bp_milestones | SP/BP alignment, half-year milestones, metrics | 12 |
| financial_quality | growth, healthy margin, cash, unit efficiency, delivery | 14 |
| evidence_budget_gates | E0-E4, evidence purchase, release and stop rules | 12 |
| ai_org_accountability | AI Native leverage, organization, owner, review | 6 |

Total: `Σ(score × weight / 10)`.

## Verdict algorithm

Apply in order:

1. If `redlines`, `unique_value`, or disproven `commercial_closure` is `fail` → `终止`.
2. If another hard gate is `fail` or any hard gate is `unknown` → `暂停`.
3. Otherwise use score: `≥80 通过`, `65-79.9 验证`, `<65 暂停`.
4. If any E0-E2 opportunity requests irreversible investment, cap the result at `验证`; if release/stop/owner is missing, return `暂停`.
5. If any opportunity lacks a budget release condition, stop condition, owner, or SP/BP milestone, cap the result at `暂停`.

Verdict and score are separate: a preliminary review may still recommend `暂停` or `终止` through hard-gate logic while numerical scoring remains invalid.

No average can repair a hard-gate failure.

## Confidence

- High: all critical claims sourced; no unknown hard gate; baselines consistent.
- Medium: decision is possible but non-critical gaps remain.
- Low: source access, baseline, or causal assumptions materially limit the review.

## Priority labels

- P0: red line, wrong decision/budget gate, or fatal commercial contradiction.
- P1: must fix before formal SP/BP approval.
- P2: improves clarity, measurement, or execution after the decision is sound.
