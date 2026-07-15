# Goal template: SP traction, BP results, and budget gates

This file is the quantitative and time-sensitive companion to SOUL. It is intentionally separate so the same public skill can be used by internal and external teams. The public copy contains placeholders only; an organization may maintain an approved private `goal.md` with its own periods, targets, owners, and thresholds.

`SOUL` answers **why and where to play**. `goal.md` answers **how much, by when, with what evidence, and when to release or stop**.

Do not treat any placeholder, example, or target in this template as a fact. Every populated goal needs a source, definition, owner, effective date, and review date.

## 1. Source and authority

```yaml
goal_version: "<version>"
status: "draft | approved"
owner: "<strategy/finance owner>"
as_of: "YYYY-MM-DD"
decision_authority: "<named authority>"
soul_source: "<approved SOUL source and revision>"
```

## 2. Planning cycles

```yaml
sp_cycle: "<SP start>—<SP end>"
sp_milestones: ["<SP milestone 1>", "<SP milestone 2>"]
bp_cycle: "<BP start>—<BP end>"
bp_milestones: ["<BP milestone 1>", "<BP milestone 2>"]
budget_cycle: "<current budget period>"
```

The skill must use the dates in the approved goal file. It must not invent dates or carry a current cycle backward into an older plan.

## 3. SP traction goals

SP goals express the strategic pull. Keep no more than three company, circle, or product opportunities. For each goal, fill:

| Field | Required content |
|---|---|
| opportunity | one chosen SP opportunity |
| user/scenario | target user, household, professional, or care scenario |
| strategic choice | Where to Play / How to Win |
| control point | device, embedded intelligence, data, service, channel, or capability control point |
| metric | measurable result or leading indicator |
| definition | calculation and metric subject |
| baseline | period, value, source, and owner |
| target | period, value, and owner |
| causal bridge | action → user adoption/value → economic/trust result |
| sacrifice | what the strategy will not do |
| evidence_level | E0-E4 and the evidence supporting it |
| review_date | next review date |

For smart hardware, distinguish product result from shipment: sell-in/SI, sell-out/SO, recognized revenue, gross margin, cash/collection, quality, warranty, service, inventory, and trust must not be merged.

## 4. BP result goals

BP goals convert each SP opportunity into near-term results and evidence upgrades. Each row must state:

| Field | Required content |
|---|---|
| sp_opportunity | exact SP opportunity name |
| bp_milestone | approved BP milestone |
| result_metric | definition, baseline, target, and source |
| evidence_upgrade | what uncertainty is closed |
| key_action | action and deliverable |
| resource_ceiling | people, tooling, inventory, cloud/API, or service ceiling |
| owner | accountable result owner |
| stop_or_correct | correction rule and stop trigger |
| review_date | review date |

For AI hardware, include device adoption/activation, model quality and failure rate, OTA reliability, privacy/security incidents, installation/service completion, warranty/return rate, and cloud/model cost where relevant.

## 5. Budget gates

Budget is released only against a named evidence purchase. Every budget line must map to one SP opportunity and one BP milestone:

| Field | Required content |
|---|---|
| budget_line | unique line or package |
| sp_opportunity | exact SP opportunity name |
| bp_milestone | exact BP milestone |
| amount | amount and currency |
| evidence_purchase | smallest action that buys the next decision evidence |
| release_condition | measurable condition for release |
| stop_condition | measurable stop or correction condition |
| owner | budget and result owner |
| authority | named release authority |
| review_date | review date |

Irreversible tooling, production, procurement, channel expansion, or real-user exposure must not be approved below the organization’s E3-equivalent gate. The threshold and exception rule belong here, not in SOUL.

## 6. Smart-hardware economic and trust guardrails

Use the organization’s actual thresholds. At minimum consider:

- BOM, tooling, yield, test, certification, packaging, logistics, installation, warranty, returns, and service cost;
- device gross margin, cloud/model/API cost, support cost, collection, inventory, and working capital;
- activation, adoption, retention, recommendation, defect, failure, return, service SLA, and trust/privacy indicators;
- channel price integrity, cannibalization, lifecycle, and ownership rules;
- AI package versus human package, with adopted workflow and measurable leverage rather than tool counts.

If a required definition, baseline, source, owner, or threshold is missing, write `GAP` and keep the review in preliminary mode.

