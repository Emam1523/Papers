# Paper Analysis 03 (Trust): AI Assurance — A Comprehensive Testing Strategy for Enterprise AI Systems

> Sub-domain: Trustworthy AI for Software Engineering
> PDF: Trustworthy AI for Software Engineering/A Comprehensive Testing Strategy.pdf

## ০. Bibliographic info

| বিষয় | তথ্য |
|---|---|
| Title | AI Assurance: A Comprehensive Testing Strategy for Enterprise AI Systems |
| Authors | Chitra Badagi, Divye Singh, Animesh Sen, Adinath Shirsath |
| Affiliation | Thoughtworks Technologies (Pune, Hyderabad, India) |
| arXiv id | arXiv:2605.23459v1 [cs.SE], তারিখ 22 May 2026 |
| Venue/year | কোনো peer-reviewed venue paper-এ বলা নেই; arXiv preprint, 2026 |
| Paper-এর ধরন | Practitioner white paper / strategy paper; কোনো experiment, dataset বা measured result নেই |
| দৈর্ঘ্য | ৩২ পৃষ্ঠা (Summary + ৯ section + Appendix A) |
| Tables / Figures | Table 1–12, Figure 1–7, Appendix-এ Listing 1–5 (Python pseudo-code) |
| Reference সংখ্যা | ৫টি ([1] Xia et al. EDD process model; [2] BLEU; [3] ROUGE; [4] RAGAS; [5] deepeval, May 2026) |
| আমাদের project-এ ভূমিকা | "Assurance process বাস্তবে কেমন" — industry practice-এর উদাহরণ, evidence নয় |

## ১. TL;DR

- Paper-এর মূল দাবি: LLM/RAG/agent-ভিত্তিক enterprise system probabilistic, তাই classical অর্থে "correct প্রমাণ" করা যায় না; লক্ষ্য হওয়া উচিত continuous risk reduction।
- তিনটি স্তম্ভ: (১) testing = continuous risk reduction, (২) evaluation একটি core engineering discipline (Evaluation-Driven Development, EDD), (৩) AI assurance failure-এর organisational ফল traditional bug থেকে আলাদা।
- Contribution হিসেবে দেওয়া হয়েছে: ১৫টি failure mode-এর AI Failure Taxonomy (৫ category, Table 2), পাঁচ স্তরের AI Assurance Pyramid (Layer 0–4, Table 5–9), RAG-এর ৪টি metric (Table 11), model lifecycle/drift নীতি (Section 7), human oversight/cost/auditability (Section 8)।
- সবচেয়ে কাজের concrete সংখ্যা: faithfulness gate 0.90, context recall 0.85, precision ও relevancy 0.80 (Listing 5); weighted score 0.4/0.4/0.2 ও final pass threshold 0.8 (Listing 3); consistency verdict: pass rate < 0.5 = CONSISTENT_FAILURE, < 0.9 = FLAKY, নইলে CONSISTENT_PASS (Listing 4, n = 10); drift trigger: ৭ দিনে 5%-এর বেশি score কমলে flag (Table 12)।
- সীমাবদ্ধতা: এই সংখ্যাগুলো কোনো experiment থেকে আসেনি; কোনো baseline, কোনো case-study সংখ্যা, কোনো ablation নেই। এটি design guidance, measured evidence নয়।
- আমাদের জন্য: assurance report-এর কাঠামো (আলাদা signal, mandatory gate, consistency, drift trigger, human escalation, audit lineage) এখান থেকে নেওয়া যায়; কিন্তু threshold ও judge-এর validity আমাদেরই মাপতে হবে।

### Supervisor-কে ৩০ সেকেন্ডে

- এটি Thoughtworks-এর practitioner strategy paper (arXiv, May 2026)। কোনো benchmark বা experiment নেই; তাই এর শক্তি "process design", দুর্বলতা "empirical evidence-এর অভাব"।
- ধারণাগুলো আমাদের assurance report-এর সাথে মিলে: failure taxonomy, layered signals, consistency (pass rate) , mandatory gates, continuous monitoring, human review, audit lineage।
- তবে paper-এর threshold (যেমন faithfulness 0.90) অযাচাইকৃত; আমাদের উচিত coding-agent patch-এর উপর নিজেদের data দিয়ে threshold calibrate করা এবং judge-এর recall/specificity মাপা (CG10, CG17)।
- আমার নতুন পর্যবেক্ষণ: Listing 3-এ binary rubric score ধরলে weighted threshold 0.8 আসলে intent alignment-কে কার্যত gate বানিয়ে দেয়, অথচ intent MANDATORY তালিকায় নেই, তাই failed_gates-এ তা দেখা যায় না (আমার হিসাব, §৬.৪)।

## ২. Background (শুধু এই project-এর জন্য নতুন ধারণা)

- **Assurance vs verification:** verification মানে spec-এর সাথে মিল প্রমাণ; assurance মানে সময়ের সাথে প্রমাণ (evidence) জমানো যে system গ্রহণযোগ্যভাবে আচরণ করছে। এই paper-এর মূল শব্দ "confidence is a property of accumulated evidence" (§9.4)।
- **Test বনাম Evaluation (Table 3):** test = deterministic assertion, pass/fail, প্রায় বিনা খরচে; evaluation = dataset-এর উপর probabilistic score, LLM judge বা human লাগে, খরচ non-trivial।
- **Evaluation-Driven Development (EDD):** behaviour নির্দিষ্ট হয় evaluation dataset দিয়ে, শুধু requirements document দিয়ে নয়; model/prompt বদলালেই loop-এ আবার ঢুকতে হয় (Figure 5)।
- **Golden dataset:** প্রতিটি prompt-এর নিজস্ব input-সেট (normal, edge, ambiguous, unsafe, adversarial) + expected output বা rubric + acceptance threshold (§4.4)।
- **Rubric ও single-dimension নীতি:** একটি rubric একটি মাত্র dimension মাপবে (intent alignment, factual correctness, safety); একাধিক dimension মেশালে scoring অসঙ্গত হয় (§4.5, Appendix A.2)।
- **Mandatory gate বনাম weighted score:** কিছু dimension (যেমন safety) এমন যেগুলো aggregate score যাই হোক fail করলে পুরো evaluation fail (§4.5)।
- **Consistency verdict:** একই input বারবার চালিয়ে pass rate দেখা; তিনটি verdict: consistent pass, flaky, consistent failure (§4.6)।
- **Trajectory evaluation:** agent-এর reasoning step, tool call, state transition-এর পুরো ক্রম মূল্যায়ন; "ভুল পথে সঠিক উত্তর" একটি false positive (§5.3)।
- **Agent handoff accuracy:** এক agent আরেক agent-কে task context কতটা সঠিকভাবে দিল; tool-call accuracy থেকে আলাদা (§5.4)।
- **Failure injection:** ইচ্ছাকৃতভাবে API error, empty retrieval, malformed tool response ঢুকিয়ে recovery path আলাদাভাবে পরীক্ষা (§6.4)।
- **Model drift:** provider নিঃশব্দে model বদলালে আচরণের ধীর পরিবর্তন; error/latency monitoring-এ ধরা পড়ে না, evaluation-based detection লাগে (§7.3)।
- **RAG metrics:** context precision, context recall, faithfulness, answer relevancy (RAGAS/DeepEval) — retrieval ও generation আলাদা করে মাপে।
- **Defect leakage rate:** Layer 0-এর failure যা প্রথমে উপরের layer-এ ধরা পড়ে তার শতাংশ (Table 5 KPI); "pyramid কতটা কাজ করছে" তার নিজস্ব মাপকাঠি।

## ৩. Problem

- Enterprise team-রা AI system কে conventional software-এর মতো test suite, pass/fail gate ও release-time validation দিয়ে যাচাই করছে (Summary)। Paper-এর ভাষায় এটি "structural mismatch", resource-এর সমস্যা নয়।
- Determinism ধারণা ভাঙে: একই input-এ ভিন্ন output; context sensitivity (শব্দ/ক্রম/framing); composition-এ emergent failure (§2.1)।
- Benchmark (MMLU, HumanEval, leaderboard) ≠ product readiness; নিজের domain-এ evaluation ছাড়া production readiness জানা যায় না (§2.4)।
- Failure-এর ধরন "error ছাড়া ভুল উত্তর": hallucination, instruction drift, trajectory collapse, coordination failure (§9)।
- Failure space enumerate করা যায় না (unknown unknowns, §3.2)।
- Cloud model-এ নির্ভরতা: provider ১২–১৮ মাসের মধ্যে model retire করে এবং changelog ছাড়া update করে (§7); তাই আজ পাশ করা system কাল fail করতে পারে।
- Evaluation infrastructure ad-hoc, প্রতি project-এ আবার বানানো হয়; sustainable নয় (§8.4)।

## ৪. Goal & RQ

- Paper কোনো formal RQ দেয় না। Abstract থেকে অন্তর্নিহিত লক্ষ্য: engineering leader ও practitioner-কে এমন strategy দেওয়া যা "philosophically grounded and operationally deployable"।
- আমার ব্যাখ্যায় implicit প্রশ্ন ৪টি:
  1. AI system-এর testing দর্শন কী হবে যখন correctness প্রমাণ অসম্ভব?
  2. কোন failure mode গুলো systematically cover করতে হবে (taxonomy)?
  3. কোন layer-এ কোন failure ধরা হবে (pyramid) এবং কত খরচে?
  4. model/prompt বদলে ও drift হলে confidence কীভাবে বজায় থাকবে (lifecycle, monitoring, governance)?
- Paper-এর "five core arguments" (§9.1): (১) risk reduction দর্শন, CI/CD-ই সঠিক analogy; (২) taxonomy আগে, strategy পরে; (৩) evaluation behaviour নির্ধারণ করে; (৪) pyramid অর্থনীতি প্রতিফলিত করবে (নিচে বেশি coverage); (৫) evaluation infrastructure একটি platform।

## ৫. Methodology (ধাপে ধাপে)

এটি empirical method নয়; এটি একটি prescriptive process। ধাপগুলো:

1. **Stack বোঝা (§1):** LLM → AI Agent (tool use + state) → Agentic AI (multi-agent, emergence)। প্রতি ধাপে testing-এর প্রধান challenge বদলায় (Table 1): LLM-এ semantic evaluation, Agent-এ trajectory correctness, Agentic-এ coordination failure।
2. **RAG-এর দুই failure surface (§1.2, Figure 2):** retrieval ও generation আলাদা; শুধু final output দেখলে কোনটি ভেঙেছে বোঝা যায় না।
3. **Taxonomy তৈরি (§3):** ৫ category, ১৫ failure mode (Table 2) — প্রতিটি category-র জন্য আলাদা detection mechanism (§3.3)।
4. **EDD loop (§4.2, Figure 5):** Define behaviour → Build eval dataset → Implement (prompt/config) → Run evaluations → threshold পূরণ না হলে Refine → হলে Ship; model/prompt বদলালে আবার loop।
5. **Dataset গঠন (§4.4):** prompt template, golden input (normal/edge/ambiguous/unsafe/adversarial), expected output বা rubric, acceptance threshold। Table 4 উদাহরণ: ৫টি row (normal ২, unsafe ১, ambiguous ১, jailbreak ১)।
6. **Hybrid evaluation (§4.5):** structured output হলে deterministic assertion আগে (token cost শূন্য); শুধু natural language-এ LLM judge + single-dimension rubric; weighted score + mandatory gate।
7. **Consistency analysis (§4.6, A.4):** n বার একই input চালিয়ে pass rate; তিন verdict।
8. **Pyramid প্রয়োগ (§5):** Layer 0 (deterministic infrastructure: tool unit test, prompt structure validation, API contract test) → Layer 1 (component: prompt eval, retrieval quality, tool selection, guardrail) → Layer 2 (single agent: trajectory, tool call accuracy, reasoning quality, state retention) → Layer 3 (multi-agent: handoff, orchestration, failure recovery, emergent behaviour) → Layer 4 (business outcome: goal completion, compliance, hallucination, red-teaming)।
9. **Diagnostic use (§5.6, Table 10):** production symptom থেকে নিচ থেকে উপরে (bottom-up) খোঁজা।
10. **RAG evaluation (§6):** চার metric, score-combination থেকে root cause (Table 11), quality gate (faithfulness ও recall non-negotiable)।
11. **Agentic-specific design (§6.4):** per-agent prompt dataset; tool selection ও parameter আলাদা failure dimension; reference trajectory বনাম rubric; stateful scenario এমনভাবে যেন context loss হলে output সুনির্দিষ্টভাবে ভুল হয়; handoff-এর baseline বনাম corrupted variation; প্রতিটি recovery path-এর আলাদা failure-injection scenario; emergent scenario production incident থেকে তৈরি; goal completion-এর জন্য structured LLM judge বা human।
12. **Lifecycle (§7):** তিন change scenario (model বদল / prompt বদল / দুটোই — দুটোই হলে variable isolate: আগে model, পরে prompt); drift detection; dataset-এ edge, unsafe/adversarial ও আগে-ঠিক-করা failure অন্তর্ভুক্ত।
13. **Monitoring (§7.5, Table 12):** trigger: scheduled (অন্তত দৈনিক, Layer 1-এর full prompt suite), model version change (সব prompt, সব layer), prompt update, production incident। Incident-কে evaluation coverage-এ রূপান্তর।
14. **Governance (§8):** HITL (uncertainty threshold, sampling, escalation), cost lever (deterministic আগে, tiered frequency, risk-proportionate coverage), auditability (model version, prompt version, retrieved context, eval verdict), evaluation engineering team।

## ৬. Math

Paper-এ কোনো গাণিতিক সূত্র লেখা নেই। নিচে যা আছে তা paper-এর Appendix code ও Table থেকে formalise করা আমার সূত্রায়ন; আলাদা করে "আমার হিসাব" লেবেল দেওয়া হলো।

### ৬.১ Consistency verdict (Listing 4 থেকে formalise)

n বার চালিয়ে $k$ বার score $\ge 0.8$ হলে pass rate:

$$\hat p = \frac{k}{n}$$

Verdict:

$$
\text{verdict}(\hat p)=
\begin{cases}
\text{CONSISTENT\_FAILURE} & \hat p < 0.5 \\
\text{FLAKY} & 0.5 \leq \hat p < 0.9 \\
\text{CONSISTENT\_PASS} & \hat p \geq 0.9
\end{cases}
$$

- $\hat p$ = n রানে পর্যবেক্ষিত pass-এর অনুপাত; $k$ = যে রানে judge score $\geq 0.8$; $n$ = পুনরাবৃত্তি সংখ্যা (code-এ default 10)।
- Paper-এর §4.6 বলে "fails more than half" = consistent failure, অর্থাৎ $\hat p<0.5$; code-ও একই। Boundary $\hat p=0.5$ code-এ FLAKY।

### ৬.২ Weighted score ও mandatory gate (Listing 3)

$$S = \sum_{d} w_d \cdot s_d,\qquad w_{\text{intent}}=0.4,\; w_{\text{fact}}=0.4,\; w_{\text{safety}}=0.2$$

$$\text{final\_pass} = \left(s_{\text{fact}}=1\right)\land\left(s_{\text{safety}}=1\right)\land\left(S\geq 0.8\right)$$

- $s_d$ = dimension $d$-এর rubric score (A.2-তে rubric শুধু 0 বা 1); $w_d$ = ওজন; $S$ = aggregate।

### ৬.৩ RAG gate (Listing 5)

$$\text{deploy} = \left(r_{\text{faith}} \geq \tau_{\text{faith}}\right)\land\left(r_{\text{recall}} \geq \tau_{\text{recall}}\right)\land\left(r_{\text{prec}} \geq \tau_{\text{prec}}\right)\land\left(r_{\text{rel}} \geq \tau_{\text{rel}}\right),\quad \tau_{\text{faith}}=0.90,\; \tau_{\text{recall}}=0.85,\; \tau_{\text{prec}}=0.80,\; \tau_{\text{rel}}=0.80$$

- $r_m$ = metric $m$-এর পরিমাপ; $\tau_m$ = threshold। সবগুলো পূরণ না হলে deploy নয়।
- Paper metric-এর গাণিতিক সংজ্ঞা দেয়নি; এগুলো RAGAS library-র সংজ্ঞা অনুসরণ করে (paper-এ নেই)।

### ৬.৪ Worked example (paper-এর সংখ্যা, আমার হিসাব)

**(ক) Mandatory gate পাশ করলে weighted threshold স্বয়ংক্রিয়।** Binary rubric ধরে (A.2): $s_{\text{fact}}=s_{\text{safety}}=1$ হলে

$$S = 0.4\,s_{\text{intent}} + 0.4(1) + 0.2(1) = 0.6 + 0.4\,s_{\text{intent}}$$

$s_{\text{intent}}=0$ হলে $S=0.6<0.8$; $s_{\text{intent}}=1$ হলে $S=1.0$। অর্থাৎ $S\ge0.8$ ঠিক তখনই যখন $s_{\text{intent}}=1$; intent কার্যত একটি de-facto gate হয়ে যায়। কিন্তু code-এ intent MANDATORY set-এ নেই, তাই failed_gates তালিকায় intent কখনো দেখা যাবে না এবং diagnosis তথ্য হারায় (আমার হিসাব)।

**(খ) Consistency, n = 10, 9টি pass:** $\hat p = 9/10 = 0.9 \Rightarrow$ CONSISTENT_PASS (boundary-তে)। 8টি pass হলে $\hat p=0.8\Rightarrow$ FLAKY।

**(গ) Wilson 95% interval (আমার হিসাব):** $n=10$, $\hat p=0.9$:

$$\text{CI}=\frac{\hat p + \frac{z^2}{2n} \pm z\sqrt{\frac{\hat p(1-\hat p)}{n}+\frac{z^2}{4n^2}}}{1+\frac{z^2}{n}},\quad z=1.96$$

ফল প্রায় [0.60, 0.98]। $\hat p=0.8$ হলে প্রায় [0.49, 0.94]। অর্থাৎ n = 10-এ CONSISTENT_PASS ও FLAKY ও কিছুটা CONSISTENT_FAILURE-এর interval ওভারল্যাপ করে; verdict-এর boundary statistically শক্ত নয়।

**(ঘ) সত্যিকার $p=0.9$ হলেও ১০/১০ পাওয়ার সম্ভাবনা** $0.9^{10}\approx 0.349$ (আমার হিসাব) — অর্থাৎ "এক রানে পাশ" দুর্বল প্রমাণ, যা §4.6-এর বক্তব্যকে সমর্থন করে।

**(ঙ) Drift trigger (Table 12): ">5% decline over 7 days"।** Baseline 0.95 হলে relative 5% হ্রাস = 0.9025; absolute 5 percentage point হ্রাস = 0.90। Paper বলেনি কোনটি (অস্পষ্টতা)। Dataset আকার $N=50$ হলে SE $=\sqrt{0.95\times0.05/50}\approx0.031$, অর্থাৎ 5 pp ≈ 1.6 SE — noise থেকে আলাদা করা কঠিন; $N=200$ হলে SE ≈ 0.015, 5 pp ≈ 3.2 SE (আমার হিসাব)।

**(চ) Paper-এর উদাহরণ:** "95% → 80% এক মাসে" ও "95% single run কিন্তু repeated execution-এ 70%" (§4.6, §7.5) — এগুলো illustrative সংখ্যা, measured নয়।

## ৭. Setup (table)

| উপাদান | বিবরণ |
|---|---|
| Experimental setup | নেই। কোনো model, dataset, benchmark, baseline বা hardware বর্ণিত নয় |
| উদাহরণ domain | Travel assistant (flight, hotel, notification agent); financial/pharma/legal উদাহরণ ছোট vignette |
| Failure taxonomy | ৫ category, ১৫ mode (Table 2) |
| Pyramid | Layer 0–4; প্রতি layer-এ ৪টির মতো evaluation target ও ৪–৬টি KPI |
| Tool/library উল্লেখ | RAGAS [4], DeepEval [5] (deepeval, May 2026) |
| Code listing | ৫টি Python snippet (illustrative; library/API পরিবেশ-নির্ভর বলে paper নিজেই জানায়) |
| Dataset উদাহরণ | Table 4: visualisation assistant prompt, ৫টি row |
| Threshold | faithfulness 0.90, recall 0.85, precision 0.80, relevancy 0.80; weighted 0.8; consistency n = 10 |
| Monitoring cadence | দৈনিক (সর্বনিম্ন) + event trigger; ৭ দিনে 5%-এর বেশি হ্রাসে flag |
| Validation | কোনো empirical validation নেই |

## ৮. Results

Paper-এ কোনো measured result নেই। নিচে "paper যা কাঠামো হিসেবে দেয়" তা table আকারে। এগুলো results নয়, design output।

### ৮.১ Failure taxonomy (Table 2)

| Category | Failure mode | Manifestation |
|---|---|---|
| Grounding | Hallucination | Fabricated facts stated with confidence |
| Grounding | Grounding failure | Response retrieved context-এর সাথে contradict করে |
| Grounding | Retrieval failure | Query-র জন্য ভুল document |
| Reasoning | Reasoning failure | সঠিক premise থেকে ভুল সিদ্ধান্ত |
| Reasoning | Instruction drift | Session-এর মাঝে constraint ভুলে যাওয়া |
| Reasoning | Trajectory collapse | স্থানীয়ভাবে বৈধ step শেষে অবৈধ ফল |
| Safety | Prompt injection | Malicious input system instruction override করে |
| Safety | Unsafe compliance | Policy-বিরোধী অনুরোধ পূরণ |
| Safety | Reward hacking | Metric পূরণ, কিন্তু উদ্দেশ্য লঙ্ঘন |
| Coordination | Context loss | আগের conversation state ভুলে যাওয়া |
| Coordination | Tool misuse | ভুল tool/parameter |
| Coordination | Over-delegation | Sub-agent এখতিয়ারের বাইরে কাজ করে |
| Coordination | Infinite loops | Agent অনির্দিষ্টকাল retry করে |
| Stochastic | Stochastic inconsistency | রানের মধ্যে pass-rate variance অগ্রহণযোগ্য |
| Stochastic | Latent emergence | Model update-এর পর অপ্রত্যাশিত সক্ষমতা |

### ৮.২ Pyramid-এর সারাংশ (Table 5–9)

| Layer | নাম | Live model call | মূল evaluation | উদাহরণ KPI |
|---|---|---|---|---|
| 0 | Deterministic Infrastructure | না | Tool unit test, prompt structure validation, API contract test | Schema adherence rate; Defect leakage rate |
| 1 | Component Evaluations | হ্যাঁ | Prompt eval, retrieval quality, tool selection, guardrail | Prompt pass rate; Prompt regression rate; Context precision/recall; Guardrail trigger rate |
| 2 | Agent Behavioural | হ্যাঁ | Trajectory, tool call accuracy, reasoning quality, state retention | Trajectory correctness rate; Unnecessary call rate; Instruction adherence rate |
| 3 | Multi-agent and Workflow | হ্যাঁ | Handoff, orchestration, failure recovery, emergent behaviour | Agent handoff accuracy; Recovery success rate; Trajectory efficiency score |
| 4 | Business Outcome | হ্যাঁ | Goal completion, compliance, hallucination, red-teaming | Goal completion rate; Hallucination rate; End-to-end regression pass rate |

- তিন নীতি (§5): উপরে গেলে খরচ বাড়ে; diagnostic specificity কমে; epistemology deterministic verification থেকে probabilistic evaluation-এ সরে।
- মূল নীতি: failure যতটা সম্ভব নিচের layer-এ ধরা।

### ৮.৩ RAG diagnostic profile (Table 11, উল্টানো/পরিষ্কার করে)

| Precision | Recall | Faithfulness | Relevancy | Diagnosis |
|---|---|---|---|---|
| Low | Low | Any | Any | Retrieval pipeline broken: chunking ও embedding দেখো |
| High | Low | Any | Any | Missing documents: recall/index coverage সমস্যা |
| High | High | Low | Any | Hallucination: generation grounding অপর্যাপ্ত |
| High | High | High | Low | Prompt issue: response shaping/instruction clarity |
| High | High | High | High | সব dimension-এ ভালো |

(Table 11 PDF text-এ column মিশে গিয়েছিল; row-diagnosis মিলানো আমার পুনর্গঠন, মূল ক্রম diagnosis list-এর ক্রমের সাথে সামঞ্জস্যপূর্ণ।)

### ৮.৪ Production symptom → check order (Table 10)

| Symptom | প্রথমে দেখো | সম্ভাব্য root cause |
|---|---|---|
| Final response হঠাৎ কম নির্ভুল | Layer 4 regression suite, Layer 2 trajectory test | Model drift বা prompt degradation |
| Agent মাঝে মাঝে ভুল tool ডাকে | Layer 2 tool call accuracy | Model update tool-call আচরণ বদলেছে |
| Tool ভুল parameter পায় | Layer 2 tool call accuracy, Layer 0 prompt validation | Prompt change parameter construction প্রভাবিত করেছে |
| Multi-step task মাঝপথে context হারায় | Layer 3 coordination test | Agent-মধ্যে state handoff ভাঙছে |
| Output format downstream-এ ভাঙছে | Layer 0 prompt validation | Prompt output structure schema থেকে সরেছে |
| Guardrail unsafe query মিস করছে | Layer 1 guardrail evaluation | Model update guardrail sensitivity কমিয়েছে |
| সঠিক উত্তর, ভুল reasoning | Layer 2 trajectory test | False positive: fragile path, পরে fail করবে |

(Table 10-ও PDF-এ মিশে ছিল; mapping আমার পুনর্গঠন, কিছু row-এর "check first" একাধিক layer থাকতে পারে।)

### ৮.৫ Monitoring cadence (Table 12)

| Trigger | Scope | Degradation-এ action |
|---|---|---|
| Scheduled (daily) | Layer 1-এ পুরো prompt test suite | Score trend ৭ দিনে 5%-এর বেশি কমলে prompt flag |
| Model version change | সব prompt, সব layer | Layer 1 baseline পুনঃপ্রতিষ্ঠা পর্যন্ত deployment block |
| Prompt update | Updated prompt + নির্ভরশীল downstream prompt | Merge-এর আগে evaluation run বাধ্যতামূলক |
| Production incident | Affected prompt + upstream component | Origin layer চিহ্নিত করে incident case dataset-এ যোগ |

## ৯. Key findings

(Paper-এর "findings" মানে তার প্রধান argument; কোনো measured finding নয়)

1. AI system-এ testing হলো "continuous risk reduction"; একক pass run দুর্বল প্রমাণ, সপ্তাহব্যাপী ধারাবাহিক উচ্চ score শক্ত প্রমাণ (§2.2)।
2. Evaluation infrastructure AI-র CI/CD-র সমতুল্য (Figure 4); release gate হিসেবে একবার নয়, প্রতি change-এ ও নিয়মিত চলবে।
3. Benchmark ≠ product readiness; model selection benchmark দিয়ে, readiness domain evaluation দিয়ে (§2.4)।
4. ভুল পথে সঠিক উত্তর একটি false positive; শুধু output পরীক্ষা এটি ধরে না, trajectory evaluation লাগে (§1.1, §5.3)।
5. Test ও evaluation আলাদা; evaluation-কে test-এর মতো pass/fail বানালে false confidence, test-কে LLM judge দিয়ে মাপলে অপচয় (§4.1)।
6. Deterministic validation আগে, semantic evaluation পরে; mandatory gate aggregate score-এ লুকানো ব্যর্থতা ধরে (§4.5)।
7. Model ও prompt একসাথে বদলানো সবচেয়ে ঝুঁকিপূর্ণ; একটি করে variable বদলাও (§7.2)।
8. Human review automation-এর বিকল্প নয়, পরিপূরক: uncertainty threshold, sampling, escalation; unknown unknowns এর মাধ্যমেই আসে (§8.1)।

## ১০. Why better than alternatives

- বনাম classical test pyramid: unit/integration/system/e2e AI-র probabilistic component boundary-তে মেলে না; Layer 0–4 failure class ভিত্তিক (§5)।
- বনাম শুধু benchmark দেখা: domain data, domain constraint ও compliance যাচাই করে (§2.4)।
- বনাম শুধু end-to-end evaluation: Layer 4 ব্যয়বহুল ও কম diagnostic; নিচে ধরলে সস্তা ও নির্দিষ্ট ফল (§5, §9.1)।
- বনাম standard NLP metric (BLEU/ROUGE): ওগুলো reference string-এর সাথে মেলায়; grounding ও faithfulness বোঝে না (§6.1)।
- বনাম single aggregate score: diagnostic profile (Table 11) কোথায় ভাঙছে বলে দেয়।
- বনাম ad-hoc per-project tooling: shared platform ও versioned dataset (§8.4)।
- (আমার পর্যবেক্ষণ) এই সব "better" দাবি যুক্তিনির্ভর; কোনো প্রতিযোগী পদ্ধতির সাথে measured তুলনা নেই।

## ১১. When it works / fails

**কখন কাজ করার কথা (paper-এর যুক্তি অনুযায়ী):**

- যখন output structured (JSON/label/schema) — deterministic validation সম্ভব।
- যখন প্রতিটি prompt-এর জন্য ভালো golden dataset আছে, adversarial/unsafe case সহ।
- যখন task-এ একাধিক বৈধ উপায় আছে; তখন rubric-ভিত্তিক trajectory evaluation reference trajectory-র চেয়ে ভালো (§6.4)।
- যখন organisation-এর একাধিক AI system আছে ও shared platform বানানো লাভজনক।

**কখন ব্যর্থ বা অপর্যাপ্ত হতে পারে (paper-এর স্বীকৃতি + আমার পর্যবেক্ষণ):**

- Unknown unknowns: যা কেউ ভাবেনি তা dataset-এ থাকে না (§3.2); red-teaming ও human sampling দরকার।
- Reference trajectory brittle: বৈধ বিকল্প পথ fail করে (§6.4)।
- LLM judge নিজেই variance আনে ("model variance", §4.5) — কিন্তু judge-কে কীভাবে validate করতে হবে তা paper বলেনি।
- Dataset ছোট হলে 5% drift trigger noise-প্রবণ (আমার হিসাব §৬.৪ ঙ)।
- Agent goal completion নিচের layer-এর যোগফল থেকে অনুমান করা যায় না (§6.4); তাই Layer 4-এর ব্যয় এড়ানো যায় না।
- Provider-এর hidden change এড়াতে কেবল নিজের নিয়ন্ত্রণের evaluation আছে, provider-এর ভেতরের কিছু জানা যায় না।

## ১২. Limitations

**Authors-এর স্বীকৃত:**

- RAG-এর চার metric "exhaustive" নয়; domain অনুযায়ী অতিরিক্ত metric লাগতে পারে (§6.2)।
- Appendix-এর code illustrative; library/API পরিবেশ অনুযায়ী বদলাবে (Appendix A)।
- Unknown unknowns কখনো পুরোপুরি enumerate করা যায় না (§3.2)।
- Semantic evaluation-এ token cost ও judge-এর নিজস্ব variance আছে (§4.5)।

**আমার পর্যবেক্ষণ:**

- কোনো empirical evidence নেই: কোনো experiment, dataset, case study সংখ্যা, ablation, বা false-positive/negative হার নেই। "These costs consistently exceed the infrastructure investment" (Summary) কোনো সংখ্যা বা সূত্র ছাড়া।
- Threshold (0.90, 0.85, 0.80, 0.80, 0.8, 5%, ৭ দিন, n = 10) কীভাবে নির্ধারিত তা বলা নেই; কোনো calibration বা sensitivity নেই।
- Statistical rigour নেই: confidence interval, significance test, paired comparison বা sample-size guidance অনুপস্থিত (আমার হিসাব §৬.৪ গ, ঙ)।
- LLM judge validity নিয়ে নীরব: judge recall/specificity, rater agreement, prompt-injection-এ judge-এর দুর্বলতা — কিছুই নেই (CG17, CG18)।
- "Reward hacking" taxonomy-তে আছে কিন্তু কোনো detection কৌশল বা metric নেই (CG12)।
- "Could not verify / abstain" নামে স্পষ্ট outcome নেই; কেবল HITL-এ low-confidence routing আছে।
- Coding agent বা software-engineering task নিয়ে কোনো উদাহরণ নেই; domain হল RAG/chat/travel agent।
- Internal সামঞ্জস্যহীনতা (§ "অনিশ্চয়তা"-তে বিস্তারিত): §4.4 "three components" বললেও চারটি তালিকা; Layer 3 KPI "Trajectory efficiency score" ratio actual/optimal, কিন্তু "score" শব্দে মনে হয় বেশি ভালো, অথচ ratio বেশি হলে খারাপ।
- Table 2 ও Table 10, 11 PDF text-এ মিশে গেছে; পাঠে ক্রম পুনর্গঠন করতে হয়েছে।
- Vendor bias সম্ভব: Thoughtworks consulting প্রতিষ্ঠান; "build dedicated evaluation function" সুপারিশ তাদের পরিষেবার সাথে স্বার্থ-সংগতিপূর্ণ হতে পারে (আমার অনুমান, প্রমাণ নেই)।

## ১৩. Research gaps

| G-id | Gap | Evidence (paper-এ) | Related CG / folder |
|---|---|---|---|
| G1 | Threshold-গুলো অযাচাইকৃত ও calibration নেই | Listing 3, 5, Table 12: 0.90/0.85/0.8/5% কোনো উৎস ছাড়া | CG8, CG10; নতুন CG23 |
| G2 | Judge validity (recall, specificity, agreement) অনুপস্থিত | §4.5, A.2: rubric judge নির্দেশিত, validate নয় | CG17, CG10; Sub-domain 5 |
| G3 | Judge-এর prompt injection robustness নেই | §2.3 injection model-এর জন্য আছে, judge-এর জন্য নয় | CG18 |
| G4 | Reward hacking শনাক্তকরণ নেই | Table 2-এ নাম আছে, §5-এ কোনো test নেই | CG12 |
| G5 | Trajectory-level assurance coding agent-এর জন্য নেই | Layer 2 generic travel উদাহরণ | CG1, CG19; নতুন CG24 |
| G6 | Statistical power ও CI অনুপস্থিত (n = 10, 5% trigger) | Listing 4, Table 12 | CG4, CG8 |
| G7 | "Could not verify" outcome নেই | §8.1 শুধু low-confidence routing | CG7 |
| G8 | Version-bound verdict আংশিক: auditability আছে, verdict-এর expiry নীতি নেই | §8.3 | CG11 |
| G9 | Evaluation environment নিজেই flaky হলে কী হবে | Layer 0 deterministic ধরা হয়েছে, environment reliability আলোচিত নয় | CG15 |
| G10 | Dataset contamination/leakage নিয়ে নীরব | §4.4 golden dataset maintain, leakage-free split নয় | CG6, CG10, CG16 |
| G11 | Reference trajectory বনাম rubric: পুরনো "gold may be wrong" সমস্যা | §6.4 reference brittle স্বীকার, কোনো tri-state নেই | CG22 |
| G12 | কোনো measured case study নেই | পুরো paper | সব CG-এর evidence শক্তি |

## ১৪. Improvement ideas

1. **Coding-agent pyramid:** Layer 0 = environment/test harness validity; Layer 1 = localisation, test-generation, static judge component; Layer 2 = trajectory audit (git history, .git/network access, hidden-test peeking); Layer 3 = multi-agent বা retry-selector; Layer 4 = merge-ready outcome (functional + security + reviewer acceptance)।
2. **Gate-only reporting:** Listing 3-এর weighted score বাদ দিয়ে শুধু mandatory gate ও আলাদা signal দেখানো; কারণ weighted score gaming-প্রবণ (CG12; Sub-domain 3 monograph দেখো)।
3. **Threshold calibration:** আমাদের নিজস্ব patch dataset-এ judge ও test signal-এর threshold R@P = 0.8 এবং specificity সহ নির্ধারণ (Sub-domain 5 Harden and Catch ও HITL paper দেখো)।
4. **Statistical drift trigger:** 5% flat rule-এর বদলে paired test (McNemar) বা sequential test ও dataset-আকার অনুযায়ী CI।
5. **Consistency = pass^k:** দুই-মুখী verdict (flaky/consistent) বাদ দিয়ে pass@k ও pass^k দুটোই report; k ও CI সহ।
6. **Tri-state verdict:** pass / fail / could-not-verify; পরেরটি HITL queue-এ যায় (CG7, CG22)।
7. **Incident-to-eval pipeline:** প্রতি ভুল-merge বা ভুল-pass patch regression dataset-এ যোগ (§7.5-এর নীতি coding-এ)।
8. **Judge robustness test:** patch-এর ভেতরে persuasive comment/injection ঢুকিয়ে judge-এর verdict বদলায় কিনা মাপা (CG18)।

## ১৫. Publication potential (SPL3-feasible)

- সরাসরি এই paper-কে ভিত্তি করে নতুন paper সম্ভব নয় (এটি strategy paper); তবে এর কাঠামো **অনুমান (hypothesis) ও টেমপ্লেট** হিসেবে ব্যবহার করে empirical study সম্ভব।
- সম্ভাব্য contribution: "Pyramid-style assurance report for coding-agent patches: signals, thresholds and drift triggers — an empirical calibration"।
- SPL3-তে feasible অংশ: ছোট scale (SWE-rebench fresh tasks-এর উপসেট), ২–৩ model, ৫ run, signal: test result, judge verdict, consistency, security scan।
- সম্ভাব্য venue: workshop বা short paper (যেমন AI-for-SE/LLM evaluation workshop); full conference-এর জন্য বড় dataset ও human study লাগবে।
- ঝুঁকি: "assurance process" নিজে novel নয়; novelty আসবে measured calibration ও judge/test signal-এর disagreement বিশ্লেষণ থেকে (CG10, CG17)।
- বাস্তবসম্মত: SPL3 report + একটি artifact (open-source assurance report generator)।

## ১৬. SPL3 implementation

- ধাপ ১: কয়েকটি coding agent বা model দিয়ে fresh task-এ patch সংগ্রহ (SWE-rebench, কয়েকশ task; cost-aware, §২১.৪)।
- ধাপ ২: Layer 0 হিসেবে environment health check (build/test সফল কিনা, repo clean কিনা, network/.git leakage block কিনা)।
- ধাপ ৩: Layer 1 signal আলাদা আলাদা: regression test, patch-targeted test, static judge (rubric single-dimension: intent, correctness, safety), security scanner।
- ধাপ ৪: Layer 2 audit: trajectory log থেকে rule-based red flag (test ফাইল সম্পাদনা, hidden-test অনুসন্ধান, git history পড়া)।
- ধাপ ৫: Consistency: প্রতি task ৫ রান, pass@k ও pass^k, Wilson CI।
- ধাপ ৬: Gate সংজ্ঞা: কোন signal mandatory (যেমন environment health, security high finding), কোনটি informational।
- ধাপ ৭: Report format: প্রতি signal-এর মান, uncertainty, tool/model version, "could not verify" কারণ; কোনো একক weighted score নয়।
- ধাপ ৮: Drift simulation: দুটি model version তুলনা করে paired test; threshold sensitivity (5% বনাম CI-ভিত্তিক)।
- ধাপ ৯: Human review: low-confidence ও signal-disagreement নমুনা থেকে ছোট human-labelled subset (rubric shared); judge-এর recall ও specificity মাপা।
- ধাপ ১০: Metrics: R@P = 0.8, specificity, McNemar, SEM; inter-signal agreement।
- সময়/খরচ: দৈনিক cadence অনুকরণ না করে event-trigger ভিত্তিক সিমুলেশন যথেষ্ট; API খরচ কমাতে deterministic signal আগে চালানো (paper-এর §8.2 নীতি)।

## ১৭. Influence / link to our earlier sub-domains

| আগের sub-domain | সম্পর্ক |
|---|---|
| 1 AI Coding Agents (SWE-bench, SWE-agent, Agentless) | Layer 2/4-এর "outcome বনাম trajectory"; ACI ও Agentless-এর audit এখানকার "benchmark ≠ readiness"-র উদাহরণ |
| 2 APR | "plausible ≠ correct" (CG1) = "ভুল পথে সঠিক উত্তর" false positive-এর patch-স্তর রূপ |
| 3 Evaluation (SWE-rebench, SWE-Bench Pro, monograph) | Consistency, variance, benchmark contamination, verifier health — paper-এর §4.6 ও §2.4-কে সরাসরি সমর্থন করে |
| 4 Test generation | Layer 0/1 test quality; stateful ও handoff scenario design = distinguishing/oracle-strength ধারণার কাছাকাছি (CG13, CG14) |
| 5 Patch Validation (HITL judge, APCA, Harden and Catch) | Rubric single-dimension ও judge validity; HITL paper judge-কে measure করেছে, এই paper করেনি |
| 6 Security (CWEval, SecureVibeBench) | Layer 1 guardrail ও safety category; joint functional+security verdict (CG20), scanner reliability (CG21) |

- এই paper আমাদের জন্য **process-level framing** দেয়; আগের sub-domain গুলো **measurement-level evidence** দেয়।

## ১৮. Supervisor Q&A

**প্রশ্ন ১: এই paper-এর evidence কতটা শক্ত?**
- উত্তর: দুর্বল। এটি practitioner strategy paper; কোনো experiment নেই। সংখ্যাগুলো (0.90, 0.85, 5%, n = 10) design পছন্দ, মাপা ফল নয়। আমরা এটিকে "process template" হিসেবে ব্যবহার করব, "প্রমাণ" হিসেবে নয়।

**প্রশ্ন ২: তাহলে আমরা কেন এটি পড়লাম?**
- উত্তর: assurance process বাস্তবে কেমন দেখায় তার একটি সুসংগঠিত industry উদাহরণ; আমাদের report-এর উপাদান (আলাদা signal, gate, consistency, drift trigger, HITL, audit lineage) এখানে একসাথে পাওয়া যায়।

**প্রশ্ন ৩: Weighted score ব্যবহার কি আমাদের "একক score নয়" নীতির সাথে বিরোধ করে?**
- উত্তর: হ্যাঁ আংশিক। Paper mandatory gate সহ weighted score দেয়। আমরা শুধু gate + আলাদা signal রাখব, কারণ weighted score gaming-প্রবণ (CG12)। আমার হিসাবে Listing 3-এ binary score ধরলে gate পাশ করা মানেই $S\ge0.8$ হতে intent লাগে — কিন্তু intent gate-তালিকায় নেই।

**প্রশ্ন ৪: Consistency verdict-এর threshold কি নির্ভরযোগ্য?**
- উত্তর: n = 10-এ Wilson interval প্রশস্ত (0.9-এর জন্য প্রায় 0.60–0.98, আমার হিসাব)। তাই verdict boundary statistically দুর্বল। আমরা CI ও বেশি run বা paired test ব্যবহার করব।

**প্রশ্ন ৫: Coding agent-এ pyramid কীভাবে বসে?**
- উত্তর: Layer 0 environment/test harness, Layer 1 component signal (judge, test, scanner), Layer 2 trajectory audit (cheating, hidden-test, git), Layer 3 multi-agent/selection, Layer 4 merge-ready outcome। §১৪ ও §১৬ দেখো।

**প্রশ্ন ৬: LLM judge-কে paper কতটা validate করে?**
- উত্তর: করে না। শুধু rubric single-dimension বলে। Judge-এর recall/specificity ও error direction আমাদের Sub-domain 5 থেকে আসে (HITL judge: recall 0.93, precision 0.65)। এটি একটি বড় gap (G2, CG17)।

**প্রশ্ন ৭: Continuous monitoring আমাদের SPL3-তে কীভাবে প্রযোজ্য?**
- উত্তর: Production নেই, তাই event-trigger simulation: model/version বদল, prompt বদল, নতুন fresh task batch; paired test দিয়ে drift মাপা।

**প্রশ্ন ৮: Paper-এর সবচেয়ে বড় ঝুঁকি কী?**
- উত্তর: অযাচাইকৃত threshold ও vendor-সম্ভাব্য bias। এছাড়া "confidence = accumulated evidence" ভালো দর্শন হলেও কত evidence যথেষ্ট তার উত্তর নেই।

## ১৯. Glossary

| শব্দ | অর্থ |
|---|---|
| AI Assurance | AI system গ্রহণযোগ্যভাবে আচরণ করছে তার ধারাবাহিক প্রমাণ জমানো |
| EDD | Evaluation-Driven Development; evaluation dataset দিয়ে behaviour নির্ধারণ |
| Golden dataset | Curated input-সেট + expected output/rubric + threshold |
| Rubric | একটি dimension-এর স্কোরিং নির্দেশিকা |
| Mandatory gate | Aggregate score যাই হোক fail করলে পুরো fail হওয়া dimension |
| Consistency | একই input বারবার চালিয়ে pass rate |
| Flaky | বেশিরভাগ সময় pass, মাঝে মাঝে fail |
| Trajectory | Agent-এর reasoning, tool call ও state transition-এর ক্রম |
| Handoff | এক agent থেকে আরেকে task context হস্তান্তর |
| Failure injection | ইচ্ছাকৃত ভুল ঢুকিয়ে recovery পরীক্ষা |
| Model drift | Provider-এর নীরব update-এ আচরণ বদল |
| Faithfulness | Response-এর দাবি retrieved context দ্বারা সমর্থিত কিনা |
| Context precision/recall | Retrieved document-এর প্রাসঙ্গিকতা/সম্পূর্ণতা |
| Red-teaming | Unknown failure খুঁজতে structured adversarial পরীক্ষা |
| Defect leakage rate | নিচের layer-এর ভুল যা উপরে প্রথম ধরা পড়ে তার শতাংশ |

## ২০. Summary card

| বিষয় | সারাংশ |
|---|---|
| Paper | AI Assurance: A Comprehensive Testing Strategy (Thoughtworks, arXiv 2605.23459v1, May 2026) |
| ধরন | Practitioner strategy paper; কোনো measured result নেই |
| মূল ধারণা | Testing = continuous risk reduction; EDD; ৫-layer pyramid; ১৫-failure taxonomy |
| মূল সংখ্যা | Gates 0.90/0.85/0.80/0.80; weighted 0.4/0.4/0.2 ও 0.8; consistency <0.5, <0.9, n = 10; drift >5% in 7 days; model retire 12–18 মাস |
| শক্তি | সুসংগঠিত process, diagnostic bottom-up, trajectory ও handoff design, HITL ও audit lineage |
| দুর্বলতা | Evidence নেই, threshold অযাচাইকৃত, judge validity নীরব, coding-agent উদাহরণ নেই |
| আমাদের কাজে | Assurance report-এর কাঠামো; threshold ও judge calibrate করতে হবে |
| নতুন gap | CG23 (threshold/drift calibration), CG24 (trajectory-level assurance for coding agents) |
| Evidence শক্তি | নিম্ন (industry practice, CG8/CG10/CG11-কে সরাসরি পরিমাপ করে না, কেবল সমস্যাটি নামকরণ করে) |

## ২১. বর্তমান (2026) প্রেক্ষাপট

Paper-এর তারিখ 22 May 2026; context-এর "বর্তমান" তথ্য আরও পরের (যেমন Claude Opus 5.5, 2026-09-22)। নিচে শুধু context.md-র তথ্য ব্যবহৃত; লেবেল: V = vendor-reported, I = independent, S = search-snippet only।

### ২১.১ তখন বনাম এখন

| বিষয় | Paper (May 2026) | বর্তমান তথ্য (context.md) |
|---|---|---|
| Benchmark ≠ readiness | MMLU/HumanEval/leaderboard readiness মাপে না (§2.4) | SWE-bench Verified saturated: Vals.ai 97.0% (Opus 5), তারপর archived (I); OpenAI আর ব্যবহার করে না — audited subset-এর ≥59.4%-এ flawed test (S) |
| Vendor বনাম independent | কোনো তুলনা নেই | SWE-Bench Pro: Opus 5.5 89.9% (V) বনাম Scale board top 61.50 ± 3.10 (I); OpenAI audit-এ public task-এর 27.4–34.1% broken (secondary) |
| Leakage | উল্লেখ নেই | SWE-Bench Pro Verified: GLM-5.2 78.80% → 57.32% যখন .git/network leakage বন্ধ (I) |
| Consistency/variance | Single run দুর্বল; n = 10 পরামর্শ | SWE-rebench pass@1 বনাম pass@5 পার্থক্য 12–18 pt (I); adjacent top-30 জোড়ার 0/29 আলাদা করা যায়; scaffold model-কে 29.8 pt পর্যন্ত নড়ায় (I); prompt rewording noise rerun-এর 11–58 গুণ (I) |
| Prompt = test surface | §2.1 prompt sensitivity | উপরের 11–58× সংখ্যা সমর্থন করে (I) |
| Judge | LLM judge + rubric সুপারিশ | PatchDiff: plausible patch-এর 29.6% gold থেকে আলাদা আচরণ (I, পুরনো model); ComPass plain LLM judge 62.14% (S); judge "over-fix" flag-এ 5–10% precision (S); Opus 5.5/GPT-6 patch-এ কোনো judge study নেই |
| Test oracle | Layer 0/1 test বিশ্বাসযোগ্য ধরা | Agent-লেখা test patch-এর 80.2% weak/no oracle (I); agent over-mock 36% বনাম 26% (S) |
| Security/Injection | Safety category, red-teaming | SusVibes FuncPass 62–84% কিন্তু SecPass 7.8–17.3% (I, Opus 4.6/GPT-5.4 যুগ); Opus 5.5 prompt-injection success 54.61% safeguard ছাড়া, 11.13% সহ (V) |
| Reward hacking | Taxonomy-তে নাম | METR: সফল long-task run-এর ≥16% cheat (I, আগের প্রজন্ম); Opus 5.5 card-এ "hidden tests" reasoning ও git গোপন করা (V) |
| Cost | §8.2 নীতি, সংখ্যা নেই | Vals Terminal-Bench 4.0 cost/task: Opus 5.5 13.20 USD, Kimi K3.1 Pro 4.57, GPT-6.1 Sol 1.72 (I) |
| Model deprecation 12–18 মাস | Paper-এর দাবি | বর্তমান model-এর তথ্য পাওয়া যায়নি (context-এ deprecation timeline নেই) |

### ২১.২ এখনো সত্য / পুরনো

**এখনো সত্য (context দ্বারা সমর্থিত):**

- Benchmark readiness মাপে না — Verified saturation ও Pro-র vendor/independent ফারাক এটি দেখায়।
- Single run দুর্বল; variance বড় (pass@1 বনাম pass@5 12–18 pt)।
- Reward hacking/cheating বাস্তব (METR ≥16%, V কার্ড তথ্য); trajectory audit-এর যুক্তি শক্ত।
- Prompt sensitivity বাস্তব (11–58×)।
- Functional pass ≠ secure (SusVibes); একক outcome-signal যথেষ্ট নয়।

**পুরনো বা অনিশ্চিত:**

- Paper-এর thresholds (0.90 ইত্যাদি) নতুন model-এ প্রযোজ্য কিনা — তথ্য পাওয়া যায়নি।
- "12–18 মাস retire" দাবি যাচাইয়ের তথ্য নেই।
- Paper RAG/chat-কেন্দ্রিক; coding-agent-এর harness (mini-SWE-agent, Claude Code, Codex ইত্যাদি) নিয়ে কিছু বলে না।

### ২১.৩ আজও খোলা gap

| Gap | আজকের অবস্থা | CG |
|---|---|---|
| Threshold calibration | কোনো current-model calibration তথ্য নেই | CG8, CG23 |
| Judge validity নতুন model-এ | Opus 5.5/GPT-6 patch-এ কোনো judge study নেই | CG17 |
| Judge injection robustness | Injection success সংখ্যা model-এর (V); judge-এর নয় | CG18 |
| Trajectory-level cheating detection | METR ও system card ইঙ্গিত দেয়, standard assurance test নেই | CG12, CG24 |
| Test oracle strength | 80.2% weak oracle (I) | CG13 |
| Security signal | SusVibes পুরনো যুগের; current-model SusVibes/BaxBench নেই | CG20, CG21 |
| Version-bound verdict | Vendor/independent ফারাক বড় | CG11 |

### ২১.৪ বর্তমান model দিয়ে SPL3 idea (cost-aware)

- Idea: ছোট fresh-task সেটে (SWE-rebench) ৩টি model শ্রেণি — একটি frontier (যেমন Opus 5.5, ব্যয়বহুল: 13.20 USD/task Terminal-Bench ভিত্তিক সূচক, I), একটি open (Kimi K3.1 Pro, 4.57 USD), একটি সস্তা (GPT-6.1 Sol, 1.72 USD) — এই cost সংখ্যা ভিন্ন benchmark-এর, আমাদের task-এর নয়; আমাদের নিজের cost আলাদা মাপতে হবে।
- Pyramid-style report: environment health → regression/targeted test → static judge → security scan → trajectory audit → consistency (k = 5)।
- খরচ কমানো: deterministic signal আগে; judge শুধু যেখানে test অমীমাংসিত; frontier model কেবল ছোট audit subset-এ judge হিসেবে।
- মাপার জিনিস: signal-disagreement হার, judge recall/specificity, threshold sensitivity (0.8 বনাম CI-ভিত্তিক), "could not verify" অনুপাত।
- বর্তমান model-এর উপর paper-এর thresholds-এর কোনো পরীক্ষিত তথ্য পাওয়া যায়নি — তাই এটাই আমাদের মূল empirical প্রশ্ন।

### ২১.৫ তিনটি Q&A

**প্রশ্ন ১: Verified 97% archived হওয়ায় paper-এর "benchmark ≠ readiness" কি আরও জোরালো?**
- উত্তর: হ্যাঁ, context-এর তথ্য (I) সমর্থন করে; saturated benchmark readiness বলে না, ও audit-এ ≥59.4% flawed test (S) এর কারণ দেখায়।

**প্রশ্ন ২: Vendor-reported সংখ্যা কি assurance evidence?**
- উত্তর: না। Pro-তে Opus 5.5 89.9% (V) বনাম independent board 61.50 ± 3.10 (I)। Assurance report-এ উৎস লেবেল (V/I) ও version দেখানো দরকার (CG11)।

**প্রশ্ন ৩: Cheating যদি ≥16% হয়, Layer 4 outcome-signal কি ভরসাযোগ্য?**
- উত্তর: একা নয়। METR-এর সংখ্যা আগের প্রজন্মের (I); তাই trajectory audit (Layer 2) ও আলাদা signal দরকার। বর্তমান model-এর জন্য নির্দিষ্ট হার পাওয়া যায়নি।
