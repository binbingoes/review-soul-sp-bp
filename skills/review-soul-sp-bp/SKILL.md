---
name: review-soul-sp-bp
description: "Review and self-check smart-hardware and AI-hardware company, business-line, product-line, platform, or functional SP/BP plans against an approved SOUL template plus goal.md, adaptive operating baselines, SWOT/TOWS, Ansoff matrix, growth curves, Where to Play/How to Win, E0-E4 evidence maturity, hardware economics, trust, AI Native leverage, and staged gates. Use when executives, circle leads, product owners, finance teams, or agents ask to 检查SP、检查BP、SPBP自检、智能硬件战略评审、AI硬件规划、硬件产品线审阅、跨圈组合审阅、预算评审、经营指标基线、财务基线、SP牵引指标、业务规划体检、产品线规划复盘、SOUL原则检查, or need a consistent human/agent verdict of 通过、验证、暂停、终止."
---

# Review SOUL SP/BP

## Public distribution

This repository is a public, smart-hardware-focused implementation. It does not contain any organization’s private SOUL text, targets, tokens, document links, or current budget commitments. Supply the approved SOUL and the organization’s populated `goal.md`; the bundled SOUL and goal files are templates and must not be treated as live facts.

Install from GitHub with:

```bash
npx skills add binbingoes/review-soul-sp-bp
```

For a global install, add `-g`; to select the skill explicitly, add `--skill review-soul-sp-bp`.

## Data boundary: SOUL versus goal.md

- `references/soul-decision-kernel.md` contains only stable SOUL language and qualitative SP strategic pull. It must not be used as the source of BP periods, budget amounts, quotas, or current financial targets.
- `goal.md` contains the time-sensitive quantitative layer: SP traction goals, BP results, budget lines, evidence thresholds, owners, release conditions, and stop conditions.
- If SOUL and `goal.md` disagree, expose the conflict. Do not silently copy BP/budget data into SOUL or treat a goal as a timeless principle.

## Audience and review modes

Support three equivalent modes with the same evidence contract:

1. **Author self-check:** the circle or plan owner supplies a self-check pack. Do not accept its verdict as evidence; independently test facts, conflicts, and gates.
2. **Peer/reviewer check:** a peer, executive, finance partner, or Agent reviews the plan and returns exact revision actions.
3. **Portfolio check:** review several circles or business lines separately first, then reconcile shared products, channels, customers, resources, and financial targets. Never merge conflicting numbers or assign the same result to multiple circles without an ownership rule.

The portable output must state source versions, coverage, review mode, confidence, verdict, unresolved gaps, and next decision authority. If an original source is unavailable, mark it `GAP`; do not imply full coverage.

Turn an SP, BP, or budget draft for a smart-hardware or AI-hardware business into an evidence-based decision review. Apply hard gates before scoring so revenue ambition, presentation quality, or seniority cannot offset red lines, missing unique value, or an untraceable goal/budget chain.

## Resource routing

Read only what the review needs, in this order:

- Read [references/soul-decision-kernel.md](references/soul-decision-kernel.md) for stable SOUL language, qualitative SP pull, hardware trust principles, and evidence vocabulary. It contains no BP/budget targets.
- Read [goal.md](goal.md) for the approved SP/BP periods, quantitative goals, metric definitions, budget lines, evidence thresholds, owners, release conditions, and stop conditions. If it is missing or unpopulated, use preliminary mode.
- Read [references/strategy-frameworks.md](references/strategy-frameworks.md) when analyzing SWOT/TOWS, Ansoff, growth curves, or Where to Play/How to Win.
- Read [references/finance-pull.md](references/finance-pull.md) for finance evidence intake questions and definitions. It is not a goal source.
- Read [references/baseline-intake.md](references/baseline-intake.md) when the plan lacks operating metrics, comparable baselines, or causal targets. Select questions by business type, stage, Ansoff quadrant, and growth curve.
- Read [references/review-rubric.md](references/review-rubric.md) before scoring or assigning a verdict.
- Read [references/input-schema.md](references/input-schema.md) before running the deterministic scorer.
- Use [references/output-template.md](references/output-template.md) for the final report.

## Workflow

### Step 1: Lock scope and source priority

Identify:

1. review scope: company, business line, product line, platform, or function;
2. artifact type: SP, BP, budget, or combined pack;
3. version, owner, decision body, and review date;
4. planning periods: the SP cycle, BP cycle, and current budget period stated in the approved `goal.md`;
5. latest SOUL source and `goal.md` version.

For a multi-circle or multi-channel review, also identify the **boundary pack**: circle/series ownership, user and scenario boundary, price band, channel role, shared capability, cannibalization rule, and the decision authority for overlap. A missing boundary pack is a strategic-choice gap, not a formatting issue.

Use sources in this priority order:

1. the latest explicit instruction from the user or decision owner;
2. the latest approved SOUL and `goal.md`;
3. the bundled templates;
4. the plan under review.

If versions conflict, expose the conflict. Do not silently choose an older target.

Label every important statement:

- `FACT` — source-backed observation or number;
- `JUDGMENT` — management choice or target;
- `ASSUMPTION` — plausible but unverified causal belief;
- `GAP` — missing information required for a decision.

If a live document is inaccessible, ask for an export or pasted text. Continue with available material, lower confidence, and keep missing content as `GAP`.

Do not silently carry a current rule backward into an older plan. Record SOUL revision and `goal.md` effective period/revision before judging a historical plan.

### Step 2: Collect evidence packs, then classify

Do not ask the product/business owner or finance owner to choose a stage, Ansoff quadrant, or growth curve. Ask them for evidence in their own domain; the Agent makes the classification and shows its reasoning.

Collect three separate packs:

1. **Product/business pack:** own historical performance; users and problems; product, channel, region, and price-band results; market change; competitor and alternative evidence; capabilities and constraints; proposed opportunities and explicit sacrifices.
2. **Finance pack:** comparable revenue, gross profit/margin, operating profit, cash, inventory/collection, unit efficiency, investment, AI package/human package, definitions, sources, and forecast/budget baselines.
3. **Goal pack:** populated `goal.md`, source version, SP/BP/budget periods, quantitative goals, metric definitions, thresholds, owners, and review dates.

For a portfolio or cross-circle review, collect a fourth **boundary pack** containing:

- who owns each product, customer, channel, price band, and result;
- overlaps between circles or series and the proposed resolution;
- channel requests versus strategic choices;
- shared platform, GTM, marketing, service, and delivery capacity;
- cannibalization, price integrity, and resource-allocation rules.

Read [references/baseline-intake.md](references/baseline-intake.md). Ask no more than six first-round questions to each owner. Do not send the full question bank.

After receiving both packs, the Agent must:

1. reconcile definitions, periods, and sources;
2. classify business type, stage, primary constraint, Ansoff quadrant, and growth curve;
3. cite the facts supporting each classification and state confidence;
4. mark an ambiguous classification `provisional` and ask only for the missing factual distinction;
5. show conflicts between business and finance inputs side by side; never average conflicting facts or silently choose one owner.

For every requested metric require:

- definition and calculation;
- comparable baseline period and value;
- source and data owner;
- SP/BP target period and value;
- gap, causal driver, responsible owner, and next update date.

Before calculating completion, reconcile the metric subject. At minimum distinguish circle revenue, regional/full-market revenue, sell-in/SI, sell-out/SO, recognized management revenue, operating profit, net profit variants, contribution margin, and cash. A shipment, order, or channel commitment is not a business result unless the plan defines how sell-out, collection, margin, quality, and trust are verified.

Use the baseline periods and target milestones defined in `goal.md`; if they are absent, record `GAP` rather than inventing a cycle.

If finance cannot provide a number, record `GAP`, owner, and due date. A plan with a critical missing baseline may receive a preliminary review, but cannot receive `通过`.

🔴 **CHECKPOINT — baseline:** Before scoring financial quality, show the selected metric dimensions, definitions, baselines, and unresolved gaps to the plan owner or named finance authority. Do not infer a baseline from an aspirational target.

### Smart-hardware focus

For every device or AI-hardware opportunity, check the complete system rather than the device claim alone:

- user scenario, device interaction, embedded model, cloud/service dependency, installation, and after-sales loop;
- BOM, tooling, yield, test, certification, firmware/OTA, warranty, returns, inventory, logistics, and service economics;
- activation, adoption, model quality, failure/defect, privacy/security, recommendation, trust, and service-SLA evidence;
- channel price integrity, lifecycle, cannibalization, and one-owner-per-result rules.

### Step 3: Normalize the plan

Extract no more than three strategic opportunities or platform initiatives. For each one record:

- target user/customer and problem;
- unique value evidence;
- SWOT facts and TOWS option;
- market-driven or technology-driven;
- Ansoff quadrant;
- first, second, or third growth curve;
- Where to Play, How to Win, and core control point;
- E0-E4 evidence level;
- SP and BP half-year milestones;
- revenue or downstream value, healthy gross margin, cash, trust, unit-efficiency, hardware reliability, and capability assumptions;
- SP/BP/budget goal references from `goal.md`, including release condition, stop condition, owner, and review date;
- explicit choice and explicit sacrifice.

Treat channel or customer requests as evidence inputs, not automatic priorities. For every request, record the requesting party, reachable user problem, incremental value, full-cost economics, strategic fit, and what the plan will not do. If a product/price/channel boundary overlaps another circle, create a conflict row and pause the affected strategic conclusion until the named authority resolves it.

Treat a platform or function initiative as an opportunity. Evaluate cycle time, quality, reuse, adoption, downstream economic value, and risk avoided instead of demanding direct revenue.

### Step 4: Run hard gates in fixed order

Run these gates before scoring:

1. **Red lines:** safety, integrity, privacy, quality, and compliance.
2. **Unique value:** horizontal difference, vertical progress, user perception, and payment/trust evidence.
3. **Strategic choice:** no more than three opportunities; clear choice, sacrifice, and control point.
4. **Evidence:** facts are sourced; E0-E4 is explicit; authority, consensus, and sunk cost are not treated as evidence.
5. **Commercial closure:** growth, healthy gross margin, cash, trust, and delivery can form a viable loop.
6. **Budget traceability:** every budget maps to an SP opportunity, BP milestone, evidence purchase, release condition, and stop condition.
7. **Accountability:** result owner, decision body, exception owner, review date, and result verification are explicit.

The strategic-choice gate also checks portfolio integrity: one owner per result, no ungoverned circle or series overlap, no channel-exclusive promise without lifecycle and price rules, and no double counting of shared revenue or capability benefits.

Apply the override rules in [references/review-rubric.md](references/review-rubric.md). A hard-gate failure cannot be repaired by a higher total score.

### Step 5: Apply the strategy frameworks

Use the fixed chain:

`SOUL SP pull → goal.md → SWOT/TOWS → Ansoff → growth curve → E0-E4 → staged gates → review and reallocation`

Reject framework theater:

- SWOT without sources is a list of opinions, not analysis.
- Ansoff classification without a higher evidence bar for farther moves is only labeling.
- A second or third curve without migration milestones is a slogan.
- Where to Play without a sacrifice is not a choice.
- How to Win without a control point, owner, or metric is not a strategy.
- A channel request list without a choice, sacrifice, and economics is not a GTM strategy.
- A product matrix with overlapping price bands and no user/value boundary is not portfolio strategy.

### Step 6: Check SP, BP, and budget traceability

For SP, require every milestone in `goal.md`, target portfolio, growth-curve migration, required capabilities, choices, exits, and multi-year assumptions.

For BP, require every BP milestone in `goal.md`, key actions, evidence upgrades, financial, hardware reliability, and trust metrics, resource ceilings, and correction against SP.

For the current budget, require the line-level evidence purchase, amount, release condition, stop condition, owner, authority, and review date from `goal.md`. Do not approve irreversible investment before the goal file’s E3-equivalent gate. Allocate third-curve work as a limited, time-boxed option until evidence supports expansion.

For low-price, ODM, or channel-specific plans, require a full-cost view: product cost, dedicated people, quality/testing, warranty/service, returns, inventory, collection, marketing, channel incentives, brand externality, and shared-capability cost. Do not approve a plan because a narrow marginal-contribution view is positive.

Check company-level portfolio defaults only on the configurable strategic growth and investment budget:

- market-driven / technology-driven: `80/20`;
- first / second / third curve: `70/20/10`;
- exclude safety/compliance, basic operations, and rigid commitments from the denominator.

Do not force every unit to mechanically match company-level ratios. Require any exception to state reason, owner, validity period, and review date.

### Step 7: Score and determine the verdict

Choose review mode before scoring.

Use **preliminary mode** if the business/product, finance, or goal pack is missing/partial, a critical operating baseline is missing, any hard gate is `unknown`, or opportunity ownership/release/stop fields are incomplete. In preliminary mode:

- do not output a numerical score or nine-dimension score table;
- do not run the scorer with invented placeholder scores;
- return `暂不评分（资料不完整）`;
- keep the report to five sections and at most two main tables;
- ask only for the missing evidence that can change the next decision.

Use preliminary mode as well when a multi-circle review has no independent circle pack, when a source is inaccessible, or when definitions conflict. State which circle, metric, or decision is uncovered; do not imply full portfolio coverage.

Use **formal mode** only when all three packs, comparable baselines, seven hard gates, opportunity cards, owners, and review dates are complete. Score the nine dimensions in [references/review-rubric.md](references/review-rubric.md), create the structured card in [references/input-schema.md](references/input-schema.md), and run the deterministic scorer.

Run:

```bash
python scripts/score_review.py review.json --format markdown
```

If Python is unavailable, calculate the weighted score manually and apply the same override rules. Never change a hard-gate result to fit the score.

Use only these verdicts:

- `通过` — evidence and operating closure support the approved scale;
- `验证` — direction is plausible, but only validation budget is justified;
- `暂停` — critical evidence, capability, traceability, or ownership is missing;
- `终止` — a red line is hit, unique value is absent, or commercial closure is disproven.

### Step 8: Return a revision-ready report

Use the matching preliminary or formal format in [references/output-template.md](references/output-template.md). Lead with:

1. verdict, weighted score, and confidence;
2. hard-gate results;
3. the three most important defects;
4. exact actions to keep, add, delete, validate, or stop;
5. the questions that require the named strategy, product, finance, delivery, red-line, or final decision authority to decide.

Keep management language direct. Do not rewrite the entire plan unless asked. Point to the exact claim, table, milestone, or budget line that must change.

For an author self-check, return two layers: (1) the plan participant's claimed status, and (2) the Agent's independent status. Never let consensus, sponsorship, or prior spend substitute for evidence.

Do not invent a submission date, threshold, score, evidence level, Ansoff quadrant, or curve. Use `GAP` or `provisional` until the responsible source supplies the deciding fact.

Scope red-line stops precisely. Stop real-data collection, user exposure, launch, or budget release when those actions create the risk. Do not automatically stop safe offline design, fictional-data testing, or remediation work unless the red-line owner requires it.

🔴 **CHECKPOINT — formal decision:** Before changing a live SP/BP, releasing budget, stopping a project, or creating a people consequence, present the review record to the named decision authority. An Agent may recommend `终止`; it may not silently make the formal company decision.

## Failure recovery

| Trigger | First response | If still unresolved |
|---|---|---|
| Source document cannot be read | Request export or pasted content; review visible sections | Mark unavailable sections `GAP`, lower confidence, and do not claim a full review |
| Baseline numbers have conflicting definitions | Put definitions and sources side by side | Return `暂停` for the affected financial conclusion until the named finance authority fixes the baseline |
| Finance or goal file has not produced the baseline | Ask the selected hardware/type/stage/quadrant questions and assign each gap an owner and date | Return a preliminary review only; cap the formal result at `暂停` |
| The plan has more than three opportunities | Ask the owner to rank and remove | Review the top three only and list the rest as explicit sacrifices or backlog |
| A functional plan has no direct revenue | Switch to cycle, quality, reuse, adoption, downstream economics, and risk avoided | Pause only if it still cannot name a supported SP opportunity or measurable downstream result |
| A target is unsupported but directionally useful | Label it `JUDGMENT` or `ASSUMPTION` | Convert it into a dated validation milestone; never present it as `FACT` |
| E0-E2 work requests irreversible investment | Reduce to validation budget and add an E3 gate | If the owner refuses a gate or stop condition, return `暂停` |
| The scorer rejects the input | Fix missing fields or invalid 0-10 scores | Use the manual rubric and disclose that deterministic validation did not pass |

## Anti-pattern blacklist

Do not:

- reward polished slides, high revenue targets, or executive sponsorship as evidence;
- accept six priorities disguised as three themes;
- let SWOT adjectives stand without facts, sources, dates, and implications;
- classify an opportunity with Ansoff or a growth curve but ignore the resulting evidence and budget threshold;
- approve growth that lacks healthy gross margin, cash discipline, trust, or delivery capacity;
- treat AI spend as progress without an adopted workflow, measurable leverage, and result accountability;
- penalize a platform for lacking direct revenue when downstream value is measurable;
- approve full budget because money was already spent;
- invent missing market, competitor, user, margin, cash, or adoption data;
- output a numerical score when source packs, baselines, hard gates, or required fields are incomplete;
- invent dates or thresholds because a current-cycle snapshot contains a nearby deadline;
- hide contradictions by averaging scores;
- output only a score without exact revision actions and decision questions;
- treat a channel, customer, or executive request as a strategy without user, economics, and sacrifice evidence;
- double count the same revenue, SKU, channel, customer, or shared platform result across circles;
- approve a low-price product from contribution margin that excludes dedicated people, quality, service, inventory, cash, or brand cost;
- leave overlapping product-series price bands unresolved while releasing channel or tooling budget;
- publish internal targets, named cases, or confidential financial data outside the authorized audience.

## Completion gate

Call the review complete only when:

- source version, scope, owner, and periods are explicit;
- the approved SOUL source and populated `goal.md` version are explicit;
- business type, stage, quadrant/curve, metric definitions, baselines, sources, owners, and target periods are explicit;
- no more than three opportunities or initiatives are reviewed;
- all seven hard gates have evidence and a status;
- cross-circle boundaries, ownership, overlaps, and double-counting rules are explicit when applicable;
- every opportunity has Ansoff, curve, E-level, WTP/HTW, control point, milestones, and a budget gate;
- SP, BP, and budget traceability is visible;
- financial, unit-efficiency, trust, and AI Native assumptions are separated from facts;
- the deterministic scorer passes or manual fallback is disclosed;
- verdict, confidence, top gaps, revision actions, authority, and next review date are present.
- numerical scoring appears only in formal mode after the scorer confirms input completeness.
