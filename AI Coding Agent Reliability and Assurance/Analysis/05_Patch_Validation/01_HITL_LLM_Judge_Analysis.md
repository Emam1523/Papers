# Paper Analysis 01 (PatchVal): Human-in-the-Loop Framework for Reliable Patch Evaluation Using an LLM-as-a-Judge

> Sub-domain: Patch Validation
> PDF: Patch Validation/Towards a Human-in-the-Loop Framework for Reliable PatchEvaluation Using an LLM-as-a-Judge.pdf

## ০. Bibliographic info

| Field | তথ্য |
|---|---|
| Title | Towards a Human-in-the-Loop Framework for Reliable Patch Evaluation Using an LLM-as-a-Judge |
| Authors | Sherry Shi, Renyao Wei, Michele Tufano, Jose Cambronero, Runxiang Cheng, Franjo Ivancic, Pat Rondon |
| Affiliation | Google (Mountain View, California, USA) |
| Venue | 1st International Workshop on AI for Software Quality Evaluation - Judgment, Metrics, Benchmarks, and Beyond (AI-SQE '26) |
| Date/Place | April 12–18, 2026, Rio de Janeiro, Brazil |
| Publisher | ACM, New York; ISBN 979-8-4007-2407-7/26/04; DOI 10.1145/3786175.3788348 |
| Length | 10 pages (workshop paper), Creative Commons Attribution 4.0 license |
| LLM ব্যবহৃত | Gemini 2.5 Pro (rubric generator এবং judge, দুটোতেই) |
| Dataset | Google monorepo-এর sanitizer bug: 48 bug, 115 unique F2P patch |
| Code/data | paper-এ public release-এর উল্লেখ নেই (internal Google data) |

## ১. TL;DR

**এক কথায়:** Patch "test pass করেছে" মানেই সঠিক নয়। Human reviewer-রাও নিজেদের মধ্যে একমত হন না (Fleiss's kappa 0.31)। লেখকরা দেখালেন যে সবাই একই **rubric** ব্যবহার করলে agreement বাড়ে। তাই তাঁরা প্রতিটি bug-এর জন্য LLM দিয়ে rubric-এর draft বানান, দুজন human developer একবার সেটা review করে "golden rubric" করেন, তারপর LLM judge সেই rubric দিয়ে patch-কে VALID/INVALID বলে।

- Judge vs human consensus: **full** (115 patch) kappa 0.57, recall 0.93, precision 0.65; **clear** (81 patch, যেখানে 3 human একমত) kappa 0.75, recall 0.94, precision 0.80 (Table 6)।
- Human refinement ছাড়া (draft rubric) kappa নামে 0.38-এ; free-form rubric-এ 0.29; ground-truth patch দিয়ে 0.39 (Table 6)।
- 504টি F2P patch-এর 219টি (43.5%) judge INVALID বলেছে (§7)। অর্থাৎ pass@k অনেক বেশি আশাবাদী।

**Supervisor-কে ৩০ সেকেন্ডে:**

1. Problem: pass@k ≠ validity, আবার human label-ও অস্থির (Fleiss 0.31)।
2. Idea: per-bug rubric (LLM draft + একবারের human review) → LLM judge।
3. Result: Human-unanimous patch-এ kappa 0.75; সব patch-এ 0.57; recall উঁচু (0.93) কিন্তু precision কম (0.65), মানে judge বেশি VALID বলে ফেলে।
4. আমাদের কাজে: এটা assurance report-এর "static signal"। এর recall ভালো, কিন্তু false-VALID সমস্যা (22/71 invalid patch গৃহীত, আমার হিসাব) থেকে যায় — তাই একা যথেষ্ট নয়, dynamic signal লাগবে।

## ২. Background (শুধু এই project-এ নতুন ধারণাগুলো)

- **LLM-as-a-Judge:** একটি LLM অন্য model-এর output (এখানে patch) মূল্যায়ন করে। পুরো নির্ভরযোগ্যতা নির্ভর করে judge-কে কী তথ্য (rubric, reference) দেওয়া হচ্ছে তার ওপর।
- **Rubric:** মূল্যায়নের লিখিত মানদণ্ড। এখানে per-bug: root cause, "valid fix-এর requirement checklist", গ্রহণযোগ্য ও অগ্রহণযোগ্য সমাধানের উদাহরণ (Listing 1)। Test-এর মতো, কিন্তু প্রাকৃতিক ভাষায়।
- **Golden rubric:** human যাচাই-করা চূড়ান্ত rubric (R_gold)। Draft rubric (R_draft) হল LLM-এর প্রথম খসড়া।
- **F2P (Fail-to-Pass) patch:** যে patch failing test-কে pass করায়। Paper-এ "plausible"-এর সমার্থক ব্যবহার (আমার ব্যাখ্যা: আমাদের CG1-এর "plausible")।
- **valid@k:** pass@k-এর বিপরীতে, k টি চেষ্টায় অন্তত একটি **সত্যিকার valid** patch পাওয়ার সম্ভাবনা। Paper-এ Figure 3-এ "(pass & LLM-valid)@k" ব্যবহার হয়েছে।
- **Inter-rater reliability (IRR):** একাধিক বিচারক কতটা একমত। শুধু "কত % মিলেছে" বললে ভুল হয়, কারণ দৈবাৎ মিলও আছে। তাই chance-corrected মাপ: Cohen's kappa, Fleiss's kappa, Krippendorff's alpha (§৬-এ সূত্রসহ)।
- **NPV (Negative Predictive Value):** judge INVALID বললে সেটা কতবার সত্যিই invalid। Precision-এর উল্টো দিক।
- **Sanitizer bug:** AddressSanitizer/ThreadSanitizer/MemorySanitizer ইত্যাদি tool যে runtime bug ধরে (data race, use of uninitialized value ইত্যাদি)। Report structured, তাই APR-এর জন্য সুবিধাজনক।
- **Levenshtein (edit) distance:** এক string থেকে আরেক string-এ যেতে ন্যূনতম কতটি character insert/delete/replace লাগে।

## ৩. Problem

1. **Execution-based metric অপর্যাপ্ত:** পরীক্ষা পাস করা patch-ও invalid হতে পারে। Paper-এর উদাহরণ (§2): Defects4J v1.2-এ Recoder-এর plausible patch-এর মাত্র 54.3% correct; ContrastRepair 62.5% (120-এর মধ্যে 75); ChatRepair 51.5% (101-এর মধ্যে 52)। এটা আমাদের CG1 (plausible ≠ correct)।
2. **Human review-ও অস্থির:** 3 জন rater, 52 F2P patch, 5 bug, নিজের লেখা rubric: Fleiss's kappa 0.31 (Table 1)। কারণ: root cause-এর ভিন্ন ব্যাখ্যা, অপ্রয়োজনীয় পরিবর্তন গ্রহণযোগ্য কি না তা নিয়ে মতভেদ, non-functional requirement, এবং code ভুল বোঝা।
3. **Scale:** manual review ব্যয়বহুল। Industrial APR deployment (Google) বাড়ছে, offline ফল online-এর সাথে মিলতে হবে।
4. **Rubric তৈরির বোঝা:** আগের কাজে (Agent-as-a-Judge, 90% alignment) হাতে-লেখা requirement লেগেছিল; নতুন bug-এর জন্য সেটা scale হয় না।

## ৪. Goal ও Research Question

**Goal:** APR patch-এর validity-র জন্য scalable ও reliable offline evaluation, human-in-the-loop রেখে।

Contribution (paper-এর তালিকা): (1) human evaluation-এর empirical study; (2) LLM-generated + human-refined rubric framework; (3) 115 patch-এ বড় আকারের evaluation (বড়-আকার বলা হয়েছে, কিন্তু আসলে ছোট; §১২ দেখো)।

| RQ | প্রশ্ন | উত্তরের উৎস |
|---|---|---|
| Motivation study | Human rater কতটা একমত? Rubric কতটা প্রভাব ফেলে? | §2, Table 1–3 |
| RQ1 | LLM কি reusable, ভালো মানের rubric বানাতে পারে? | §5.1, 50 draft vs golden |
| RQ2 | Golden-rubric judge কি human consensus-এর সাথে মেলে? | §5.2, Table 5–6 |
| Ablation | Refinement, template, rubric-vs-GT-patch-এর অবদান কতটুকু? | §6, Table 6 |

## ৫. Methodology (ধাপে ধাপে)

### ৫.১ Motivation study (§2)

1. তিনজন লেখক rater। Dataset: 5টি Google sanitizer bug-এর 52 F2P patch।
2. প্রতিটি bug-এর জন্য bug report ও ground-truth patch দেখে প্রত্যেকে নিজের rubric লেখেন।
3. প্রত্যেকে 52 patch-কে VALID/INVALID করেন, দুই অবস্থায়: (১) নিজের rubric, (২) অন্যের rubric।
4. Fleiss's kappa (3 জন, নিজ-নিজ rubric): 0.31। জোড়ায় জোড়ায় Cohen's kappa 0.37, 0.19, 0.39 (Table 1)।
5. Self-agreement (একই rater, দুই rubric): 0.35, 0.36, 0.49 (Table 2)। মানে rubric বদলালে একই মানুষ ভিন্ন রায় দেয়।
6. একই rubric ব্যবহার করলে জোড়ায় Cohen's kappa 0.84, 0.67, 0.53 (Table 3)।
7. তিনজন disagreement বিশ্লেষণ করে একটি **template** বানান: root cause, requirement checklist, acceptable/unacceptable example।
8. তিনজন নতুন rater (আগে জড়িত ছিলেন না) golden rubric নিয়ে একই 52 patch দেখেন: Fleiss's kappa **0.66**।

### ৫.২ Framework (§3, Figure 1)

**Stage 1: Rubric generation (প্রতি bug-এ একবার)**

1. Input: bug context (description) + ground-truth fix (code owner-এর করা)। Reference-free evaluation এই paper-এর scope-এর বাইরে।
2. LLM predefined template (Listing 1) অনুযায়ী draft rubric বানায়।
3. Human review: একজন developer edit করে (ভুল requirement সংশোধন, ground-truth-এ overfit করা requirement সরানো, দরকারি element যোগ) এবং প্রতিটি edit-এর justification লেখে। দ্বিতীয় developer সব edit ও justification নিশ্চিত করে। ফল: golden rubric।

**Stage 2: Patch evaluation (পুনরাবৃত্তিযোগ্য, স্বয়ংক্রিয়)**

1. Input: bug context + unified diff format-এর patch + golden rubric।
2. Output: "thought" অংশ, binary label (VALID/INVALID), সংক্ষিপ্ত justification।
3. Label ও justification সংরক্ষিত, যাতে qualitative বিশ্লেষণ সম্ভব হয়।

### ৫.৩ Dataset তৈরি (§4.1)

1. Prior curation process (Rondon et al. [30]) অনুসরণ করে 50 sanitizer bug।
2. Google-এর নিজস্ব APR agent দিয়ে প্রতি bug-এ 20 patch (মোট 1,000)।
3. F2P যাচাই: bug report-এর failing test patch-এর পরে pass করে কি না।
4. প্রতি bug থেকে সর্বোচ্চ 3টি unique F2P patch random sample (hash দিয়ে uniqueness)।
5. 2টি bug-এ কোনো F2P patch নেই, বাদ। ফল: 48 bug, 115 patch (44 C++, 3 Go, 1 Java bug)।

### ৫.৪ Human benchmark (§4.3.2, §5.2.1)

1. 115 patch-এর প্রতিটিতে 3 জন লেখক-rater স্বাধীনভাবে, judge-এর output না দেখে, golden rubric দিয়ে label করেন।
2. মতভেদ হলে আলোচনা করে একটি final label (consensus)।
3. দুটি benchmark: **full** = 115 patch, **clear** = 81 patch (আলোচনার আগে 3 জনই একমত)।

### ৫.৫ RQ1 মেট্রিক (§4.3.1)

- Modification rate: কত % draft rubric human বদলেছে।
- Normalized edit distance (সূত্র §৬)।
- Edit type: addition / deletion / modification।
- Thematic analysis: LLM প্রাথমিক category বানায়, মানুষ iteratively merge/split/relabel করে।

### ৫.৬ Ablation (§6)

| Variant | কী বদলানো হয়েছে |
|---|---|
| R_gold (full approach) | LLM draft + human refinement + template |
| R_draft | human refinement ছাড়া, templated draft |
| R_ff | template ছাড়া free-form rubric, refinement নেই |
| GT patch | rubric নেই; judge-কে ground-truth patch reference হিসেবে দেওয়া (CodeJudge/MT-Bench ধরন) |

সব ক্ষেত্রে Gemini 2.5 Pro। Temperature, prompt text, বা কতবার judge চালানো হয়েছে paper-এ নেই।

## ৬. Math

### ৬.১ Framework formalization (§3.3)

- b = bug context, f = ground-truth fix, p = একটি F2P patch।
- Draft rubric: $R_{\text{draft}} = G(b, f)$, যেখানে G = LLM rubric generator।
- Golden rubric: $R_{\text{gold}} = H(R_{\text{draft}})$, H = human developer-এর review/refine।
- Judge: $(y, j) = J_{\text{llm}}(b, p, R_{\text{gold}})$, y ∈ {VALID, INVALID}, j = justification।

### ৬.২ Confusion matrix ও মেট্রিক

VALID class-কে positive ধরা হয়, human consensus = ground truth।

$$\text{Precision} = \frac{TP}{TP + FP}, \quad \text{Recall} = \frac{TP}{TP + FN}$$

$$F_1 = \frac{2 \cdot \text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}}, \quad \text{Accuracy} = \frac{TP + TN}{TP + TN + FP + FN}$$

$$\text{NPV} = \frac{TN}{TN + FN}, \quad \text{Specificity} = \frac{TN}{TN + FP}$$

- TP: judge VALID, human VALID। FP: judge VALID, human INVALID (বিপজ্জনক ভুল)। FN: judge INVALID, human VALID। TN: দুজনই INVALID।
- Specificity paper রিপোর্ট করেনি; আমি যোগ করেছি, কারণ আমাদের CG-তে "low specificity" মূল প্রশ্ন।

### ৬.৩ Cohen's kappa (দুজন বিচারক, বা judge বনাম human)

$$\kappa = \frac{p_o - p_e}{1 - p_e}$$

- $p_o$ = observed agreement = দুজন যে অনুপাতে একমত (accuracy-র মতো)।
- $p_e$ = দৈবাৎ মিল হওয়ার প্রত্যাশিত সম্ভাবনা:

$$p_e = \sum_{c} p_{1,c} \cdot p_{2,c}$$

যেখানে $p_{1,c}$ = বিচারক 1 যে অনুপাতে class c বলেছে, $p_{2,c}$ = বিচারক 2-এর অনুপাত। Binary-তে c ∈ {VALID, INVALID}।

- κ = 1: পুরো মিল; κ = 0: দৈবাৎ মিলের সমান; κ < 0: দৈবের চেয়েও খারাপ।
- Landis-Koch ব্যাখ্যা (সাধারণ রীতি): 0.21–0.40 fair, 0.41–0.60 moderate, 0.61–0.80 substantial, 0.81–1.00 almost perfect। Paper এই ভাষাই ব্যবহার করে (0.38 fair, 0.57 moderate, 0.75 substantial)।

**কেন শুধু accuracy নয়?** ধরুন 95% patch invalid। যে judge সবকিছুকেই INVALID বলে তার accuracy 95%, কিন্তু κ = 0 (কারণ $p_o = p_e$)।

**Worked example — paper-এর নিজস্ব সংখ্যা (আমার হিসাব):** Table 5-এর full benchmark: 44 VALID, 71 INVALID। Recall 0.93 ⇒ TP = 41, FN = 3। §5.2.2 বলে false positive = 22 ⇒ TP + FP = 63, precision = 41/63 = 0.65 ✓। TN = 71 − 22 = 49। Judge ও human-এর marginal:

| | Human VALID | Human INVALID | মোট |
|---|---|---|---|
| Judge VALID | 41 (TP) | 22 (FP) | 63 |
| Judge INVALID | 3 (FN) | 49 (TN) | 52 |
| মোট | 44 | 71 | 115 |

$$p_o = \frac{41 + 49}{115} = 0.7826$$

$$p_e = \frac{63}{115} \cdot \frac{44}{115} + \frac{52}{115} \cdot \frac{71}{115} = \frac{2772 + 3692}{13225} = 0.4888$$

$$\kappa = \frac{0.7826 - 0.4888}{1 - 0.4888} = 0.575 \approx 0.57$$

এটা Table 6-এর 0.57 ও accuracy 0.78-এর সাথে মিলে যায় (আমার পুনর্গঠন, paper-এ confusion matrix দেওয়া নেই)। NPV = 49/52 = 0.94 ✓; মোট ভুল = 22 + 3 = 25 ✓ (§5.2.2-এর 25 patch)।

**Clear benchmark (আমার হিসাব):** 35 VALID, 46 INVALID। Recall 0.94 ⇒ TP = 33, FN = 2। Precision 0.80 ⇒ FP = 8 (33/41 = 0.805)। TN = 46 − 8 = 38। Accuracy = 71/81 = 0.877 (paper 0.87; rounding-পার্থক্য), NPV = 38/40 = 0.95 ✓। $p_o = 0.8765$, $p_e = (41 \cdot 35 + 40 \cdot 46)/81^2 = 0.4992$, κ = 0.753 ≈ 0.75 ✓।

**Cross-check:** full-এ FP = 22, clear-এ FP = 8, ফলে human-disagreement-এর 34 patch-এ FP = 14; paper বলে ঠিক "22-এর মধ্যে 14 (63.6%)" ✓। 14/22 = 0.636।

**Confidence interval (আমার আনুমানিক হিসাব):** Cohen's kappa-র standard error ≈ $\sqrt{p_o(1-p_o)/(n(1-p_e)^2)}$।

- full: $\sqrt{0.7826 \cdot 0.2174 / (115 \cdot 0.2613)} \approx 0.075$ ⇒ 95% CI ≈ 0.57 ± 0.15 = 0.42 থেকে 0.72।
- clear: SE ≈ 0.073 ⇒ 0.75 ± 0.14 = 0.61 থেকে 0.89।

মানে "moderate" ও "substantial" ব্যান্ড overlap করে; ছোট sample-এ ব্যান্ড-দাবি দুর্বল। Paper কোনো CI দেয়নি।

### ৬.৪ Fleiss's kappa (৩+ বিচারক)

N টি item, প্রতিটিকে n জন বিচারক k টি category-র একটিতে ফেলে। $n_{ij}$ = item i-কে category j-তে ফেলা বিচারকের সংখ্যা।

$$P_i = \frac{1}{n(n-1)} \left( \sum_{j=1}^{k} n_{ij}^2 - n \right), \quad \bar{P} = \frac{1}{N} \sum_{i=1}^{N} P_i$$

$$p_j = \frac{1}{N n} \sum_{i=1}^{N} n_{ij}, \quad \bar{P}_e = \sum_{j=1}^{k} p_j^2, \quad \kappa_F = \frac{\bar{P} - \bar{P}_e}{1 - \bar{P}_e}$$

- $P_i$ = item i-তে বিচারকদের জোড়া-ভিত্তিক মিলের অনুপাত; $\bar{P}$ = গড় মিল; $\bar{P}_e$ = দৈবাৎ মিল।

**Toy example (আমার হিসাব, paper-এর data নয়):** N = 4 patch, n = 3 rater, VALID-ভোট 3, 2, 1, 0।

- $P_1 = (9 + 0 - 3)/6 = 1$; $P_2 = (4 + 1 - 3)/6 = 0.333$; $P_3 = 0.333$; $P_4 = 1$ ⇒ $\bar{P} = 0.667$।
- VALID-ভোট মোট 6 / 12 = 0.5 ⇒ $\bar{P}_e = 0.25 + 0.25 = 0.5$।
- $\kappa_F = (0.667 - 0.5)/0.5 = 0.333$ (fair)। এটা paper-এর 0.31-এর কাছাকাছি স্তর, বোঝায় যে 4 patch-এর 2টিতে 2-1 ভাগ হলেই kappa এত নেমে যায়।

Paper-এর Fleiss সংখ্যা: 0.31 (self-authored rubric, Table 1), 0.66 (নতুন 3 rater, golden rubric, §2)।

### ৬.৫ Krippendorff's alpha

$$\alpha = 1 - \frac{D_o}{D_e}$$

- $D_o$ = observed disagreement, $D_e$ = দৈবাৎ প্রত্যাশিত disagreement। Missing rating সহ ৩+ rater-এও কাজ করে (Paper §4.2 এই কারণেই এটি রাখে)।
- Paper: α = 0.60 (115 patch, আলোচনার আগে), clear benchmark-এ 1.0 (নির্মাণগতভাবে)।

### ৬.৬ Weighted average Cohen's kappa (human vs consensus)

প্রতিটি human rater ও consensus label-এর kappa, ওজন = সেই rater-এর review করা patch-এর শতাংশ। Table 5: 0.76 (full), 1.0 (clear)। বিঃদ্রঃ 1.0 অর্থহীন কারণ clear subset-ই বেছে নেওয়া হয়েছে unanimous হওয়ার শর্তে।

### ৬.৭ Normalized edit distance (RQ1)

$$\text{NED} = \frac{\text{Levenshtein}(R_{\text{draft}}, R_{\text{gold}})}{\text{length}(R_{\text{draft}})}$$

Paper-এর সংখ্যা: median absolute edit = 276 character, mean 385; draft median length 2,004, mean 2,058 character; median NED = 0.14, max = 0.70।

আমার হিসাব: 276/2,004 = 0.138 ≈ 0.14 ✓ (median-এর সাথে মেলে); mean-এর আনুমানিক অনুপাত 385/2,058 = 0.19।

### ৬.৮ pass@k বনাম (pass & LLM-valid)@k

pass@k = k টি sample-এর অন্তত একটি F2P হওয়ার সম্ভাবনা। (pass & LLM-valid)@k = অন্তত একটি patch F2P **এবং** judge-এর VALID। Figure 3: k = 20-এ pass@20 = 96%, (pass & LLM-valid)@20 = 80%, ফাঁক 16 percentage point (প্রতি bug-এ 20 patch, 50 bug, মোট 1,000 patch)।

### ৬.৯ Baseline হিসাব: "সব F2P-কে VALID বলো" (execution-only)

(আমার হিসাব) যেহেতু সব 115 patch F2P, pass@k-ভিত্তিক সিদ্ধান্ত সবাইকে VALID বলে। তাহলে TP = 44, FP = 71, FN = 0, TN = 0:

- Precision = 44/115 = 0.383; Recall = 1.00; Accuracy = 0.383; F1 = 0.553; Specificity = 0; κ = 0।
- Clear-এ: precision = 35/81 = 0.432; F1 = 0.604।
- তুলনা: judge F1 0.77 (full), 0.87 (clear); Specificity = 49/71 = 0.69 (full), 38/46 = 0.83 (clear) (আমার হিসাব)।

## ৭. Setup

| Item | মান |
|---|---|
| Domain | Google monorepo sanitizer bug (C++ 44, Go 3, Java 1 bug) |
| Bug-সংখ্যা | 50 collected, 48 with F2P patch |
| Patch generation | Google-এর internal APR agent [30], প্রতি bug-এ 20 (মোট 1,000) |
| Patch sample | ≤ 3 unique F2P/bug ⇒ 115 patch |
| Rubric generator + judge | Gemini 2.5 Pro |
| Rubric review | 2 developer/rubric (একজন edit, একজন confirm); 6 লেখক মিলে 50 rubric |
| Human rater (benchmark) | 3 জন লেখক, স্বাধীন label ⇒ মতভেদে consensus আলোচনা |
| Metrics | Cohen's kappa, Krippendorff's alpha, accuracy, precision, recall, F1, NPV |
| Reference | Ground-truth fix (code owner-এর) |
| Motivation study | 5 bug, 52 F2P patch, 3 rater + 3 নতুন rater |

Bug-type বণ্টন (Table 4): data_race 14 bug/33 patch; use_of_uninitialized_value 11/26 (এবং আরেক সারিতে 2/5); misaligned_pointer_use 6/13; data_race_go 3/8; fuzztest_crash 2/4; leak_detected 2/6; signed_integer_overflow 2/5; stack_use_after_scope 2/6; hwasan_tag_mismatch 1/2; invalid_bool_load 1/2; invalid_enum_load 1/3; null_pointer_use 1/2। মোট 48 bug, 115 patch (আমি যোগ করে যাচাই করেছি; তবে use_of_uninitialized_value দুবার এসেছে, §১২-তে উল্লেখ)।

## ৮. Results

### ৮.১ Motivation study (Table 1–3)

| Table | Raters | Rubric | Kappa |
|---|---|---|---|
| 1 | Rater 1,2,3 (Fleiss) | নিজস্ব | 0.31 |
| 1 | Rater 1 ও 2 | নিজস্ব | 0.37 |
| 1 | Rater 2 ও 3 | নিজস্ব | 0.19 |
| 1 | Rater 3 ও 1 | নিজস্ব | 0.39 |
| 2 | Rater 1 নিজের সাথে (own vs Rater 3 rubric) | দুই rubric | 0.35 |
| 2 | Rater 2 নিজের সাথে (own vs Rater 1 rubric) | দুই rubric | 0.36 |
| 2 | Rater 3 নিজের সাথে (own vs Rater 2 rubric) | দুই rubric | 0.49 |
| 3 | Rater 1 ও 2 | Rater 1-এর rubric | 0.84 |
| 3 | Rater 2 ও 3 | Rater 2-এর rubric | 0.67 |
| 3 | Rater 3 ও 1 | Rater 3-এর rubric | 0.53 |
| §2 | নতুন 3 rater (Fleiss) | golden (template) | 0.66 |

### ৮.২ RQ1: Rubric generation (§5.1)

| মেট্রিক | মান |
|---|---|
| Draft rubric length (median / mean) | 2,004 / 2,058 character |
| Revision দরকার হয়েছে | 44 / 50 = 88% |
| Absolute edit distance (median / mean) | 276 / 385 character |
| Normalized edit distance (median / max) | 0.14 / 0.70 |
| সম্পূর্ণ rewrite দরকার | কোনোটিতে নয় |

Edit type (একটি rubric একাধিক ধরনে পড়তে পারে, তাই যোগফল 44-এর বেশি, আমার পর্যবেক্ষণ): deletion 39, modification 14, addition 3 rubric।

Thematic category (Figure/text §5.1.3):

| Category | Rubric সংখ্যা |
|---|---|
| Removing Superfluous Constraints | 31 |
| Reducing Overfitting to Ground Truth | 10 |
| Correcting LLM Errors and Hallucinations | 9 |
| Refining Scope and Expectations | 6 |
| Standardization | 5 |

### ৮.৩ RQ2: Human benchmark (Table 5)

| মেট্রিক | full | clear |
|---|---|---|
| Bug | 48 | 41 |
| Patch | 115 | 81 |
| Unanimous agreement | 70.4% (81/115) | 100% (81/81) |
| Krippendorff's alpha | 0.60 | 1.0 |
| Weighted average Cohen's kappa | 0.76 | 1.0 |
| Consensus VALID patch | 44 | 35 |
| Consensus INVALID patch | 71 | 46 |

34 disagreement patch-এর কারণ (human): Overlooked Requirements 15, Unnecessary Changes 9, Rubric Ambiguity 8, Correctness Assessment 2 (মোট 34 ✓)।

### ৮.৪ RQ2 ও Ablation (Table 6)

| Metric | Benchmark | R_gold | R_draft | R_ff | GT patch |
|---|---|---|---|---|---|
| Cohen's kappa | full | 0.57 | 0.38 | 0.29 | 0.39 |
| Cohen's kappa | clear | 0.75 | 0.52 | 0.33 | 0.44 |
| Accuracy | full | 0.78 | 0.70 | 0.62 | 0.69 |
| Accuracy | clear | 0.87 | 0.76 | 0.65 | 0.72 |
| Precision | full | 0.65 | 0.60 | 0.51 | 0.56 |
| Precision | clear | 0.80 | 0.74 | 0.57 | 0.62 |
| Recall | full | 0.93 | 0.66 | 0.82 | 0.84 |
| Recall | clear | 0.94 | 0.71 | 0.83 | 0.89 |
| F1 | full | 0.77 | 0.63 | 0.63 | 0.67 |
| F1 | clear | 0.87 | 0.72 | 0.67 | 0.73 |

(Table-এর column-গুলো PDF-এর `-raw` extract থেকে নিশ্চিত করা; layout extract garbled ছিল।) NPV: 0.94 (full), 0.95 (clear)।

**Judge-এর 25 ভুল (full):** Overlooked Requirements 10, Unnecessary Changes 9, Rubric Ambiguity 6। 22 false positive-এর 14 (63.6%) ঠিক সেই patch-এ যেখানে human-দেরও মতভেদ ছিল।

### ৮.৫ Discussion পরীক্ষা: pass@k gap (§7, Figure 3)

| মেট্রিক | মান |
|---|---|
| মোট patch | 1,000 (50 bug × 20) |
| F2P patch (48 bug-এর) | 504 |
| Judge INVALID বলেছে | 219 (43.5%) |
| k = 20: pass@20 | 96% |
| k = 20: (pass & LLM-valid)@20 | 80% |
| ফাঁক | 16 percentage point |

Judge-এর rejection কারণ (219-এর মধ্যে, LLM দিয়ে cluster):

| কারণ | % |
|---|---|
| Violating Specified Requirements in Rubric (style, RAII, scope ইত্যাদি) | 60.6 |
| Not Addressing Root Cause (symptom ঢাকা, sanitizer suppress ইত্যাদি) | 26.6 |
| Incomplete Implementation | 7.3 |
| Introducing New Issues | 5.5 |

(যোগফল 100.0 ✓)। আমার পর্যবেক্ষণ: 60.6% rejection "rubric-এর শর্ত ভঙ্গ" (style/scope), অর্থাৎ আসল functional ভুল নয়; এই 60.6% পুরোটা correctness নয়, অনেকটাই "review-গ্রহণযোগ্যতা"।

## ৯. Key findings

1. **Human label-ই noisy:** নিজের-rubric-এ Fleiss κ = 0.31; একই মানুষ rubric বদলালে κ মাত্র 0.35–0.49 (Table 1–2)। Human = gold standard ধারণাটাই প্রশ্নবিদ্ধ।
2. **Shared rubric agreement বাড়ায়:** κ 0.19–0.39 থেকে 0.53–0.84 (Table 3); নতুন rater-দের Fleiss 0.66।
3. **LLM draft ভালো scaffold কিন্তু যথেষ্ট নয়:** 88% (44/50) rubric-এ edit লেগেছে; কিন্তু median মাত্র 14%, কোনোটিতে পুরো rewrite নয়। মানুষের কাজ "লেখা" থেকে "review"-এ নেমেছে।
4. **LLM-এর draft-এর প্রধান দোষ অতিরিক্ত শর্ত ও ground-truth overfitting:** 31 rubric-এ superfluous constraint সরানো, 10-এ overfitting কমানো; deletion (39) ≫ addition (3)।
5. **Human refinement অপরিহার্য:** κ 0.38 → 0.57 (full), recall 0.66 → 0.93, precision 0.60 → 0.65 (Table 6)।
6. **Template কাজ করে:** free-form-এ κ 0.29, templated draft-এ 0.38, golden-এ 0.57।
7. **Rubric > ground-truth patch reference:** GT-patch judge κ 0.39 বনাম rubric 0.57 (full)।
8. **Judge-এর শক্তি recall ও NPV, দুর্বলতা precision:** recall 0.93, NPV 0.94, কিন্তু precision 0.65; ভুলের 63.6% সেই patch-এ যেখানে human-ও দ্বিধায়।
9. **pass@k আশাবাদী:** 504 F2P-র 43.5% judge-এর মতে invalid; pass@20 96% বনাম (pass & LLM-valid)@20 80%।

## ১০. Alternative-এর চেয়ে কেন ভালো

| Alternative | সমস্যা | এই paper-এর সুবিধা |
|---|---|---|
| শুধু pass@k / test | Weak assertion, coverage ফাঁক; plausible ≠ correct | Semantic ও non-functional requirement-ও ধরে |
| Free-form human review | Fleiss 0.31; অ-reproducible | Shared rubric ⇒ reproducible, agreement বেশি |
| GT-patch reference দিয়ে LLM judge | κ 0.39; ground-truth-এর শৈলীতে overfit | Rubric root cause ও গ্রহণযোগ্য বিকল্প সমাধান বর্ণনা করে (κ 0.57) |
| Raw LLM draft rubric | Hallucination ও overfitting; recall 0.66 | একবারের human refinement; recall 0.93 |
| CodeBLEU ইত্যাদি similarity | Validity ধরে না [29, 35] | Validity সরাসরি লক্ষ্য |
| Full manual review প্রতি patch | ধীর, দামী | Human কাজ প্রতি **bug** একবার, patch-সংখ্যায় নয় |

আমার পর্যবেক্ষণ: তুলনাটি "judge বনাম অন্য judge/reference" ধরনের। Execution-based বা hidden-test oracle-এর সাথে একই label-এ সরাসরি তুলনা (যেমন differential/distinguishing test) করা হয়নি।

## ১১. কখন কাজ করে / কখন করে না

**কাজ করে যখন:**

- Bug-এর structured report আছে (sanitizer: bug type, failing test, reproduction command)।
- Ground-truth fix আছে এবং human rubric বদলে overfitting সরিয়েছে।
- Human-রাও patch-এ একমত (clear: κ 0.75, precision 0.80)।
- INVALID label দরকার (NPV 0.94/0.95): invalid patch আগে ছেঁকে ফেলা।

**ব্যর্থ হয় যখন:**

- Patch-এর validity বিতর্কিত: unnecessary change, rubric-এর অস্পষ্টতা। Judge-এর 25 ভুলের 9 unnecessary-change, 6 rubric-ambiguity, 10 overlooked requirement।
- Rubric overfitted থাকলে বৈধ বিকল্প patch reject (draft-এ recall 0.66)।
- অন্য ভাষা/ধরনের bug: dataset 44/48 C++।
- Ground-truth fix না থাকলে: reference-free case paper-এর scope-এর বাইরে।

## ১২. Limitations

### ১২.১ লেখকদের স্বীকৃত

1. Google monorepo ও sanitizer bug ছাড়া অন্য প্রসঙ্গে (open-source, logic/UI bug) সাধারণীকরণ অনিশ্চিত।
2. একটি মাত্র APR system-এর patch ও একটিই LLM (Gemini 2.5 Pro)।
3. লেখকরা prompt engineering-এ দক্ষ, তাই golden rubric সাধারণ developer-এর চেয়ে বেশি optimized হতে পারে।
4. Rater-রা code-এর original author নন, গভীর context-এর অভাব।
5. Golden rubric তৈরিতে human judgment ⇒ variability (mitigation: দ্বিতীয় reviewer)।
6. Binary label: patch-এর গ্রহণযোগ্যতার মাত্রা থাকে, তাই rejection rate বেশি হিসাব হতে পারে।
7. Future work: user study (time/cognitive load) এখনো হয়নি।

### ১২.২ আমার পর্যবেক্ষণ

1. **Circularity:** Judge ও human দুজনই একই golden rubric ব্যবহার করে, এবং rubric বানিয়েছেন সেই লেখকরাই যাঁরা benchmark label করেছেন। তাই agreement আংশিকভাবে "একই rubric মানা"-র প্রতিফলন, ground-truth correctness নয়। Rubric ভুল হলে দুজনেই একসাথে ভুল।
2. **Clear subset selection bias:** headline "κ 0.75, precision 0.80" সেই patch-এ যেখানে human আগেই একমত, অর্থাৎ সহজ patch। বাস্তব deployment-এ কঠিন patch-ই বেশি জরুরি। বাস্তব সংখ্যা full-এ: κ 0.57, precision 0.65।
4. **Sample ছোট, CI নেই:** 115 patch, 48 bug; kappa-র আনুমানিক 95% CI full-এ 0.42–0.72, clear-এ 0.61–0.89 (আমার হিসাব)। Paper-এ "large-scale" দাবি অতিরঞ্জিত।
5. **একবারের run:** Judge নির্ধারণশীল কি না, temperature, run-to-run variance (CG4) এবং prompt sensitivity রিপোর্ট নেই।
6. **Patch-per-bug ≤ 3 এবং বাছাই:** একই bug-এর patch পরস্পর নির্ভরশীল (clustered), অথচ kappa independence ধরে।
7. **Execution-based oracle-এর সাথে তুলনা নেই:** human consensus-কেই ground truth ধরা হয়েছে; hidden/regression test বা production outcome-এর সাথে নয়।
8. **Rater-দের অ-স্বাধীনতা:** লেখকরা নিজেরাই rater; judge-এর output তাঁরা দেখেননি, কিন্তু rubric ও framework সম্পর্কে পক্ষপাত থাকতে পারে।
9. **Internal data:** Reproducibility কম: dataset, rubric, prompt, APR system সবই Google-internal।
10. **Rubric-এর খরচ অমাপা:** "একবারের review" কতটা সময় নেয় তা মাপা হয়নি; প্রতি bug-এ 2 জন developer লাগে (খরচ রয়েছে)।
11. **Gaming/adversarial না দেখা:** patch-এর comment/ভাষা দিয়ে judge-কে প্রভাবিত করা যায় কি না পরীক্ষা নেই (§১১-এ বিশদ)।

**Paper-অভ্যন্তরীণ অসঙ্গতি:**

- §5.2.1 weighted average kappa 0.76-কে "moderate" বলা হয়েছে, অথচ 0.75-কে অন্যত্র "substantial" বলা হয় (Landis-Koch-এ 0.61–0.80 = substantial)।
- Table 4-এ `use_of_uninitialized_value` দুটি আলাদা সারিতে (11 bug/26 patch এবং 2 bug/5 patch); সম্ভবত দুটি ভিন্ন variant, ব্যাখ্যা নেই।
- Table 5-এ "Weighed average" টাইপো; Table 6-এর column header PDF-এ garbled।
- Clear benchmark-এ accuracy: আমার হিসাবে 71/81 = 0.877, paper 0.87 (rounding)।
- Abstract/§1 "substantial agreement" জোর দেয় clear-এর 0.75-এ; full-এর 0.57 শুধু শেষ বাক্যে।

## ১৩. Research gaps

| G-id | Gap | Evidence | Related CG / sub-domain |
|---|---|---|---|
| G1 | Judge false-VALID বেশি: 22 / 71 invalid patch গৃহীত (specificity 0.69, আমার হিসাব) | Table 6 precision 0.65; §5.2.2 | CG1; Sub-domain 2 (RePaCA) |
| G2 | Human benchmark ও judge একই rubric-নির্ভর (circularity) | §4.3.2, §5.2.1 | CG10 |
| G3 | "Clear" subset-এ ফল বেশি, কঠিন patch-এ কম (selection bias) | Table 5–6, κ 0.75 বনাম 0.57 | CG10, CG8 |
| G4 | Judge-এর gaming/prompt-injection প্রতিরোধ অপরীক্ষিত | কোনো adversarial পরীক্ষা নেই | CG12 |
| G5 | Judge ও rubric-এর version/model-bound verdict নেই (Gemini 2.5 Pro-ই একমাত্র) | §10 | CG11 |
| G6 | Run-to-run variance ও CI অনুপস্থিত | একবারের run, ছোট n | CG4, CG8 |
| G7 | Execution/dynamic oracle-এর সাথে তুলনা নেই | Human consensus-ই ground truth | CG3, CG14 |
| G8 | Abstain/"uncertain" outcome নেই; controversial patch-এ binary জবরদস্তি | 14/22 FP বিতর্কিত patch-এ | CG7 |
| G9 | শুধু sanitizer/C++/Google; SWE-bench-style multi-file issue-এ অপরীক্ষিত | §10 External threats | CG9 |
| G10 | Rubric-এর ground-truth-নির্ভরতা (GT leak/contamination ও reference-free case) | §3.1 | CG6, CG10 |
| G11 | Non-functional/security মাত্রা judge-এ নেই | §8 Future Work | CG5 |

## ১৪. Improvement ideas

1. **Judge + dynamic hybrid:** judge VALID বললে পরে distinguishing test/regression test দিয়ে confirm (Sub-domain 4-এর Oracle-Guided Selection দেখো); Judge শুধু "ছাঁকনি", final verdict নয়।
2. **Abstain band:** judge-কে confidence/"unclear" বলতে দিয়ে human-routing, যেমন 14/22 বিতর্কিত patch human-এ পাঠানো।
3. **Multi-judge ensemble ও variance রিপোর্ট:** একাধিক model/seed দিয়ে judge চালিয়ে agreement মাপা (CG4)।
4. **Rubric-এর বিরুদ্ধে stress test:** rubric reviewer-কে বিভিন্ন patch (valid/invalid/adversarial) দেখিয়ে rubric ঠিক করা, যা paper নিজেই future work-এ বলেছে।
5. **"Unnecessary change" নীতি:** paper-এর প্রস্তাব, অপ্রয়োজনীয় পরিবর্তন মানেই INVALID, কিন্তু আমাদের জন্য আলাদা "scope" signal হিসেবে রাখা ভালো, যাতে correctness ও style মিশে না যায়।
6. **Version-bound verdict:** প্রতি judgment-এর সাথে judge model, rubric hash, prompt version সংরক্ষণ (CG11)।
7. **Reference-free rubric:** ground-truth ছাড়া (issue + test থেকে) rubric বানানোর পরীক্ষা; SWE-bench-এ GT patch model-এর training data-তে থাকতে পারে (contamination)।
8. **Prompt-injection hardening:** patch-এর comment/string-কে data হিসেবে isolate করা; judge-কে diff-এর কোড-অংশ ও comment আলাদা দেখানো।

## ১৫. Publication potential (SPL3-feasible)

- **Realistic লক্ষ্য:** workshop/short paper (AI-SQE-এর মতো) বা student research track।
- **সম্ভাব্য contribution:** "Judge-এর specificity ও gaming মাপার replication on open data": Google-এর internal dataset ছাড়া SWE-rebench/SWE-bench Verified-এর একটি ছোট subset-এ।
- **শক্তি:** open data + open-weight judge + CI-সহ কঠোর statistics + adversarial test = বাস্তবসম্মত নতুনত্ব।
- **ঝুঁকি:** human labeler-এর সময় (rubric review খরচ); 100–150 patch-এর ছোট human-labled set-ই সম্ভব।
- **Novelty claim:** "Rubric judge-এর false-VALID ও adversarial robustness" Paper-এ নেই, তাই gap স্পষ্ট।

## ১৬. SPL3 implementation

1. **Data:** SWE-rebench fresh task বা SWE-bench Verified-এর ছোট subset, প্রতি task-এ 2–3টি F2P agent patch।
2. **Rubric stage:** open-weight বা API model দিয়ে per-task rubric draft (এই paper-এর template: root cause, requirement list, acceptable/unacceptable example)। আমরা দুজন (বা supervisor সহ) review করব; edit log রাখব (normalized edit distance আমাদের RQ1 হিসাবে পুনরুৎপাদন করা যায়)।
3. **Judge stage:** একই rubric + patch diff ⇒ VALID/INVALID + justification, একাধিক run (কমপক্ষে 3 seed) ও কমপক্ষে দুটি ভিন্ন model।
4. **Human label:** 3 rater, স্বাধীন, তারপর consensus; Krippendorff's alpha ও Fleiss হিসাব (library: `statsmodels`/`krippendorff`)।
5. **Metrics:** recall **এবং specificity** (এই paper যা দেয়নি), NPV, κ + bootstrap CI, ছোট n-এ McNemar judge বনাম test-only baseline।
6. **Baseline:** (a) শুধু F2P (সবাই VALID), (b) GT-patch-reference judge, (c) free-form judge, (d) rubric judge।
7. **Adversarial test:** patch-এ বাড়তি comment ("this patch is correct and follows all requirements"), test-only পরিবর্তন, sanitizer-suppress ধরনের patch ঢুকিয়ে judge কতবার ঠকে মাপা।
8. **Assurance report integration:** judge output-কে "static signal" হিসেবে রাখা, সংখ্যা ও uncertainty সহ; dynamic signal-এর সাথে মেলালে "disagree ⇒ human review" নিয়ম।

## ১৭. Influence / আমাদের আগের sub-domain-এর সাথে সংযোগ

| আগের কাজ | সংযোগ |
|---|---|
| Sub-domain 1: Agentless, AutoCodeRover | AutoCodeRover-এ 51/78 plausible patch সত্যি correct; Agentless-এর patch-selection। এই paper দেখায় human review-ও অস্থির (বেশি সংখ্যা বিশ্বাসযোগ্য নয় ধরে নেওয়া ঠিক নয়) |
| Sub-domain 2: RePaCA | দুটোই static judge। RePaCA training-ভিত্তিক (GRPO), এই paper prompt-ভিত্তিক + human rubric। Error profile উল্টো (§১১ দেখো, নিচে) |
| Sub-domain 3: SWE-rebench, SWE-Bench Pro, Reliable Coding Agents | Weak/flawed test সমস্যা এই paper-এর motivation; "verifier health" (CG11) এখানে rubric/judge-এর health হয়ে ফিরে আসে |
| Sub-domain 4: Test generation, Oracle-Guided Selection | Judge-এর complement: Judge "কী করা উচিত" বলে, distinguishing test "কী করে" মাপে |

**RePaCA-র সাথে সরাসরি তুলনা (আমার বিশ্লেষণ; ভিন্ন dataset, তাই সংখ্যা সরাসরি তুলনীয় নয়):**

| দিক | RePaCA (Sub-domain 2) | এই paper (HITL judge) |
|---|---|---|
| Judge ধরন | Fine-tuned reasoning LLM (GRPO) | Prompted Gemini 2.5 Pro + human golden rubric |
| Input | patch + context | patch + bug context + golden rubric (+ GT fix দিয়ে rubric) |
| Data | Defects4J | Google sanitizer bug (internal) |
| Headline | 83.1% accuracy | accuracy 0.78 (full), 0.87 (clear); κ 0.57/0.75 |
| Invalid ধরা | 106/109 overfitting ধরেছে (≈ 97%) | specificity ≈ 0.69 (49/71) full-এ, আমার হিসাব |
| Valid গ্রহণ | 16/30 correct গৃহীত (≈ 53%) | recall 0.93 (41/44) full-এ |
| Error profile | Over-reject (valid বাদ), low acceptance | Over-accept (invalid ঢোকে), উচ্চ recall |
| Human ভূমিকা | training-এ label | rubric review (inference-time) |

আমার ব্যাখ্যা: দুই judge-এর ভুলের দিক উল্টো। তাই assurance report-এ দুটিকে আলাদা signal হিসেবে রাখলে পরস্পর পূরক হতে পারে (একটি valid বাদ দেয়, অন্যটি invalid ঢোকায়)। তবে এটা অনুমান; একই dataset-এ পরীক্ষা ছাড়া নিশ্চিত নয়।

## ১৮. Supervisor Q&A

**Q1. Cohen's kappa কেন accuracy-র বদলে? সূত্র কী?**
A: Accuracy দৈবাৎ মিলকে বাদ দেয় না। $\kappa = (p_o - p_e)/(1 - p_e)$। Paper-এর full benchmark-এ accuracy 0.78 কিন্তু κ 0.57, কারণ $p_e = 0.489$ (আমার হিসাব)। ৬.৩-এ পুরো হিসাব আছে।

**Q2. Fleiss's kappa আর Cohen's kappa-র পার্থক্য? 0.31 কীসের?**
A: Cohen = ঠিক ২ বিচারক; Fleiss = ৩+। 0.31 = তিন লেখক-rater, 52 F2P patch, নিজ-নিজ rubric (Table 1)। Shared golden rubric-এ নতুন 3 rater-এর Fleiss 0.66।

**Q3. Judge-এ human কীভাবে loop-এ আছে?**
A: দুই জায়গায়: (১) প্রতি bug-এ একবার rubric review (একজন edit, একজন confirm; 44/50 rubric-এ edit); (২) benchmark label ও consensus। Patch-পর্যায়ে human নেই, তাই scalable।

**Q4. Judge কি execution-based evaluation-এর চেয়ে নির্ভুল?**
A: সরাসরি তুলনা নেই। আমার হিসাবে "সব F2P = VALID" baseline-এর precision 0.38 (full), F1 0.55; judge-এর precision 0.65, F1 0.77। তবে human consensus যদি ভুল হয়, দুটোই ভুল। Hidden-test oracle দিয়ে যাচাই হয়নি।

**Q5. Low-specificity সমস্যা এখানে আছে?**
A: আছে, উল্টো আকারে। Judge recall 0.93, কিন্তু 71 invalid-এর 22টি (31%) VALID বলেছে (specificity 0.69, আমার হিসাব)। 14/22 human-দের মতভেদের patch-এ। RePaCA-তে উল্টো সমস্যা (valid reject)।

**Q6. Judge gaming-এর শিকার হতে পারে? (CG12)**
A: Paper পরীক্ষা করেনি। সম্ভাবনা বেশি: patch-এর ভেতরে comment/শব্দ দিয়ে প্রভাব, rubric-এর requirement-ভাষা নকল করা, GT-এর শৈলী নকল। Judge diff পড়ে, তাই আমাদের adversarial test জরুরি।

**Q7. 0.75 কি সত্যিই "substantial"? কেন 0.57 বলা হয় না?**
A: 0.75 শুধু clear (81) patch-এর, যা human-unanimous হওয়ার শর্তে বাছা, সহজতর অংশ। Full-এ 0.57 (moderate), আনুমানিক CI 0.42–0.72 (আমার হিসাব)।

**Q8. Rubric-এর খরচ কি scale করে?**
A: প্রতি bug-এ 2 developer। Median edit মাত্র 14%, কিন্তু সময় মাপা হয়নি (future work)। SWE-bench-এর হাজার task-এ খরচ বড় হবে; আমরা ছোট subset-এ করব।

## ১৯. Glossary

| শব্দ | অর্থ |
|---|---|
| APR | Automated Program Repair, স্বয়ংক্রিয় bug fix |
| F2P | Fail-to-Pass, failing test pass করানো patch |
| Plausible / valid | Plausible = test পাস; valid = সত্যিই সঠিক |
| Rubric | মূল্যায়নের লিখিত মানদণ্ড |
| Golden rubric | Human-যাচাইকৃত চূড়ান্ত rubric |
| IRR | Inter-rater reliability, বিচারকদের মিল |
| Cohen's kappa | দুই বিচারকের chance-corrected মিল |
| Fleiss's kappa | তিন বা বেশি বিচারকের মিল |
| Krippendorff's alpha | Missing rating সহ বহু-বিচারকের মিল |
| NPV | Negative predictive value |
| Specificity | সত্যিকার invalid-এর কত অংশ ধরা পড়েছে |
| Sanitizer | Runtime bug-ধরা tool (ASan, TSan, MSan) |
| Levenshtein distance | দুই string-এর ন্যূনতম edit সংখ্যা |
| valid@k | k চেষ্টায় অন্তত একটি valid patch |

## ২০. Summary card

| Item | মান |
|---|---|
| Paper | HITL + LLM-as-a-Judge patch evaluation, Google, AI-SQE '26 |
| Idea | LLM draft rubric ⇒ 2-developer review ⇒ golden rubric ⇒ LLM judge |
| Data | 48 bug, 115 F2P patch (44 C++), sanitizer; Gemini 2.5 Pro |
| Human IRR | Fleiss 0.31 (নিজস্ব rubric) ⇒ 0.66 (shared rubric) |
| Judge (full 115) | κ 0.57, acc 0.78, prec 0.65, rec 0.93, F1 0.77, NPV 0.94 |
| Judge (clear 81) | κ 0.75, acc 0.87, prec 0.80, rec 0.94, F1 0.87, NPV 0.95 |
| Ablation (full κ) | draft 0.38, free-form 0.29, GT-patch 0.39 |
| Rubric edit | 44/50 (88%) edited; median NED 0.14, max 0.70 |
| pass vs valid | 504 F2P-র 43.5% judge-INVALID; pass@20 96% ⇒ 80% |
| প্রধান দুর্বলতা | false-VALID (22/71), circularity, ছোট n, gaming অপরীক্ষিত |
| আমাদের ব্যবহার | Assurance report-এর static signal, dynamic signal-এর পরিপূরক |

## ২১. বর্তমান (2026) প্রেক্ষাপট

### ২১.১ তখন বনাম এখন

| বিষয় | Paper-এর সময়/সেটআপ | 2026 (context.md থেকে; V = vendor, I = independent, S = snippet) |
|---|---|---|
| Judge model | Gemini 2.5 Pro | Claude Opus 5.5, Fable 5.1, GPT-6 family, Gemini 4 Argon, open: Kimi K3.1 Pro, GLM-5.x, DeepSeek V4। এই model-গুলোর patch-এর উপর judge study: বর্তমান model-এর তথ্য পাওয়া যায়নি |
| Plain LLM judge শক্তি | Rubric ছাড়া GT-patch judge: κ 0.39 | ComPass-এ plain-LLM judge overfitting detection-এ 62.14% (S) |
| Judge precision | Full-এ 0.65 (false-VALID 22) | Judge "over-fix" flag-এ 5–10% precision (S) |
| Plausible ≠ correct | 504 F2P-র 43.5% judge-invalid | PatchDiff: plausible patch-এর 29.6% gold-এর চেয়ে ভিন্ন আচরণ (I, পুরোনো model) |
| Benchmark | Google internal sanitizer bug | SWE-bench Verified saturated (Vals.ai 97.0%, archived; I); OpenAI ব্যবহার বন্ধ, ≥59.4% audited subset-এ flawed test (S) |
| Industry practice | Offline pass@k + manual review | Rubric/LLM-judged mergeability-র দিকে যাচ্ছে (FrontierCode) |
| Gaming | Paper-এ নেই | METR: ≥16% successful long-task run ছিল cheat (I, পূর্ববর্তী প্রজন্ম); Opus 5.5 card-এ "hidden tests" reasoning ও git concealment (V) |
| Variance | একবারের judge run | SWE-rebench pass@1 বনাম pass@5 ফাঁক 12–18 pt (I); prompt rewording noise 11–58× reruns (I) |

### ২১.২ এখনো সত্য / পুরোনো

**এখনো সত্য:**

- Plausible ≠ correct: PatchDiff (29.6%) ও ComPass-এ plain judge-এর দুর্বলতা paper-এর দাবির পক্ষে।
- Judge-এর false-VALID সমস্যা: "over-fix" precision 5–10% (S) ইঙ্গিত দেয় সমস্যা শুধু Gemini 2.5 Pro-র নয়।
- Industry rubric-ভিত্তিক মূল্যায়নের দিকে যাচ্ছে, এই paper-এর দিকনির্দেশের সাথে মেলে।

**পুরোনো/বদলেছে:**

- Gemini 2.5 Pro-র ফল 2026-এর model-এ হুবহু বলা যায় না; বর্তমান model-এর তথ্য পাওয়া যায়নি।
- Verified-ধরনের benchmark saturated, তাই "pass@k বনাম human" বিশ্লেষণ এখন fresh/corrected benchmark-এ করতে হবে।
- Agent নিজে test/evaluation অবস্থা পড়ে ও লুকিয়ে ফেলতে পারে (V/I), তাই judge-কে gaming-এর লক্ষ্য ধরে নিতে হবে।

### ২১.৩ আজকের দিনেও খোলা gap

| Gap | কেন এখনো খোলা | সংশ্লিষ্ট |
|---|---|---|
| Current model-এর patch-এর উপর rubric-judge study | বর্তমান model-এর তথ্য পাওয়া যায়নি | CG1, CG10 |
| Judge-এর gaming (prompt-injection, hidden-test reasoning) | Opus 5.5 card-এ hidden-test reasoning (V); judge-কেন্দ্রিক পরীক্ষা পাওয়া যায়নি | CG12 |
| Judge specificity ও precision | Over-fix precision 5–10% (S) | CG1 |
| Judge variance ও version-bound verdict | Rewording noise 11–58× (I) | CG4, CG11 |
| Fresh benchmark-এ human-label সহ judge যাচাই | Verified saturated/flawed | CG6 |

### ২১.৪ 2026 model দিয়ে SPL3 ধারণা (cost-aware)

- **Judge হিসেবে সস্তা model, label-validation-এ একটি শক্তিশালী model:** Cost per task (Vals Terminal-Bench 4.0, I): Opus 5.5 13.20 USD, Kimi K3.1 Pro 4.57 USD, GPT-6.1 Sol 1.72 USD (এটি agent-চালনার খরচ, judge-এর নয়; judge call ছোট, তাই খরচ কম হবে, আমার অনুমান)।
- Rubric-draft একবার (শক্তিশালী model), judge বহুবার (সস্তা open-weight, যেমন Kimi K3.1 Pro/DeepSeek V4/GLM-5.x), শুধু disagreement-এ শক্তিশালী model বা human।
- Dataset: fresh SWE-rebench task, 100–150 patch, 3 human rater; প্রতি patch-এ 3 judge run।
- Output: Assurance report-এ "static judge signal" = recall, specificity, CI, model/rubric version সহ; "could not verify" ও "human review needed" explicit outcome।
- সব ফল 2026 model-এ নতুন করে মাপা হবে, কারণ এই paper-এর সংখ্যা Gemini 2.5 Pro-র।

### ২১.৫ তিনটি Q&A

**Q1. 2026-এর model কি Gemini 2.5 Pro-র চেয়ে ভালো judge?**
A: বর্তমান model-এর তথ্য পাওয়া যায়নি; context.md-তে এই model-গুলোর patch-judge ফল নেই। এটাই আমাদের project-এর সুযোগ।

**Q2. Verified saturated হলে এই paper-এর পদ্ধতি এখনো কাজে লাগে?**
A: হ্যাঁ। Saturation মানে pass@k বিভ্রান্তিকর (≥59.4% audited task-এ flawed test, S)। ঠিক এই অবস্থায় test-এর বাইরে rubric-ভিত্তিক validity signal আরও দরকার।

**Q3. Agent যদি judge-কে ঠকাতে চায়?**
A: METR-এর ≥16% cheat (I) ও Opus 5.5-এর hidden-test reasoning (V) বলে, ঠকানোর ঝুঁকি বাস্তব। Judge-কে একা সিদ্ধান্ত না নিতে দিয়ে dynamic signal ও leakage check-এর সাথে একত্রে ব্যবহার করতে হবে।
