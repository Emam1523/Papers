# Paper Analysis 01 (Trust): Trustworthy AI Software Engineers

> Sub-domain: Trustworthy AI for Software Engineering
> PDF: Trustworthy AI for Software Engineering/Trustworthy AI Software Engineers.pdf

## ০. Bibliographic info

| Field | Detail |
|---|---|
| Title | Trustworthy AI Software Engineers |
| Authors | Aldeida Aleti (Monash University, Australia), Baishakhi Ray (Columbia University, USA), Rashina Hoda (Monash University), Simin Chen (Columbia University) |
| Type | Vision paper (কোনো experiment, dataset বা benchmark নেই) |
| Venue / year | arXiv:2602.06310v2 [cs.SE], 3 Jun 2026 (v2)। ACM template-এ ছাপা, কিন্তু venue ফাঁকা: "Conference'17, July 2017, Washington, DC, USA" এবং DOI "10.1145/nnnnnnn.nnnnnnn" হলো template placeholder। তাই চূড়ান্ত প্রকাশিত venue paper-এ বলা নেই |
| Length | ৫ পৃষ্ঠা, ৩৬টি reference |
| Data availability | "There are no data available yet." |
| Core contribution | ৬টি "New Idea" (#1–#6): agentic engineer-এর ৪ শর্ত, multi-dimensional trustworthiness framework, evidence-centric inspection, V&V পুনর্ভাবনা, code review as runtime monitoring, trust interface |
| আমাদের জন্য ভূমিকা | পুরো assurance report-এর conceptual frame (কোন কোন dimension আমরা কোন signal দিয়ে মাপব) |

## ১. TL;DR

- Paper বলে: AI coding agent শুধু code লিখলেই "software engineer" নয়। SE মানে requirements, design, testing, maintenance, team-work, accountability। তাই একটি agent-কে "agentic engineer" বলতে হলে ৪টি শর্ত লাগে (New Idea #1)।
- **Trust** (মানুষের মনোভাব) আর **trustworthiness** (system-এর property) আলাদা। Paper trustworthiness-কে system property হিসেবে নেয়, subjective attitude হিসেবে নয়।
- Trustworthiness-এর পরিবার: Technical quality, Transparency and accountability, Epistemic humility, Ethical alignment, এবং socio-technical practice। এগুলো system / model / output স্তরে এবং developer / organisation / society স্টেকহোল্ডারের জন্য প্রযোজ্য (Figure 1)।
- কোনো একটি dimension একা "necessary and sufficient" নয়; trustworthiness আসে dimension-এর **configuration** থেকে।
- Developer সব কিছু পরীক্ষা করতে পারবে না (cognitive overload, review fatigue)। তাই প্রস্তাব: artefact-centric inspection থেকে **evidence-centric inspection**-এ যাওয়া: "developer-কে সব দেখাতে হবে না, ঠিক জিনিসগুলো দেখাতে হবে"।
- V&V হবে multi-level: output, process (planning/tool use ঠিক কি না), epistemic (agent নিজের uncertainty ঠিকভাবে জানায় কি না)।
- Paper নিজে স্বীকার করে মূল gap হলো **trustworthiness measurement gap** এবং property থেকে developer-facing interface-এর রূপান্তর।

**Supervisor-কে ৩০ সেকেন্ডে:** "এই paper আমাদের assurance report-এর তাত্ত্বিক কাঠামো দেয়। ওরা বলছে developer-কে raw patch না দেখিয়ে evidence (requirement-এর সাথে মিল, defensible reasoning, uncertainty, failure mode) দেখাতে হবে। আমরা ঠিক সেটাই বানাচ্ছি: প্রতিটি patch-এর জন্য আলাদা signal-সহ একটি assurance report, 'যাচাই করা যায়নি' একটি স্পষ্ট ফলাফল। Paper-এর কোনো experiment নেই, তাই আমাদের কাজ হলো এর দাবিগুলোকে মাপার মতো signal-এ রূপান্তর করা, এটিই এই paper-এর উল্লেখিত measurement gap।"

## ২. Background (এই প্রজেক্টে নতুন ধারণা)

- **Agentic engineer:** Paper-এর পরিভাষা। কেবল coding agent নয়; SE lifecycle-এর কাজ + planning/tool use + collaboration + human values মানে।
- **Trust vs trustworthiness:** Trust হলো মানুষের সিদ্ধান্ত/প্রবণতা কোনো AI-এর ওপর নির্ভর করার। Trustworthiness হলো system-এর সেই property যা ওই নির্ভরতাকে justify করে। দুটি অসমমিত: মানুষ untrustworthy system-কে trust করতে পারে (অতি-নির্ভরতা), আবার trustworthy system opaque হলে trust পাবে না। এটি Pink et al. [20]-এর ধারণা।
- **Khati et al. [11] তিনটি attribute:** ability (accuracy, efficiency, reliability), benevolence (user ও stakeholder লক্ষ্যের সাথে মিল), integrity (safe, secure, ethical practice)।
- **CRAFT values [10]:** Comprehensive, Responsible, Adaptive, Foundational, Translational। Agentic SE-কে code-এর বাইরে নেওয়ার মূল্যবোধ।
- **Epistemic humility:** AI নিজের জ্ঞানের সীমা জানাবে, uncertainty ও bias স্বীকার করবে। আমাদের CG7 (confidence/abstention)-এর সরাসরি তাত্ত্বিক ভিত্তি।
- **Selective visibility problem:** Agent-এর সব intermediate step দেখানো scalable বা useful নয়; কী দেখানো হবে তা curate করতে হবে।
- **Process-level verification ও epistemic verification:** যথাক্রমে agent-এর planning/tool use ঠিক কি না, এবং agent নিজের uncertainty সঠিকভাবে প্রকাশ করে কি না যাচাই।
- **Trustworthiness oracle [18]:** Robustness, fairness, security-এর জন্য স্বয়ংক্রিয়ভাবে check তৈরির কাজ (Nguyen Tung et al., FSE 2025, ML text classifier-এর জন্য)।
- **Code review as runtime monitoring:** Merge-এর পরেও deployed code "provisional", agent production behaviour নিয়মিত পর্যবেক্ষণ করবে।

## ৩. Problem

1. AI agent-এর adoption হচ্ছে কিন্তু trustworthiness নিয়ে সংশয় টিকে আছে (paper [23] উল্লেখ করে)। LLM untrustworthy হতে পারে [8, 29], vulnerability ভুল বোঝে [30], hallucinate করে [31], training data মুখস্থ করে [4, 13], biased feature-এর ওপর নির্ভর করে [29], এবং syntactically ঠিক কিন্তু semantically ভুল program বানায় [27, 32]।
2. "Software engineer" বলতে কী বোঝায় তা অস্পষ্ট। IEEE, ACM, SWEBoK অনুযায়ী SE শুধু programming নয়; day-to-day কাজের বড় অংশ non-coding [15]। বর্তমান agent socio-technical কাজ (judgment, communication, accountability) কীভাবে করবে তা অজানা।
3. Trustworthiness-এর dimension (fairness, robustness, transparency, explainability, auditability, traceability, privacy ইত্যাদি [14]) আছে, কিন্তু AI-based SE agent-এর প্রেক্ষাপটে systematic ভাবে বসানো হয়নি।
4. Dimension জানাই যথেষ্ট নয়: agent বিপুল artefact তৈরি করে, developer সব দেখতে পারে না। ফলে exhaustive verification (অসম্ভব) আর uncritical reliance (ঝুঁকিপূর্ণ)-এর মধ্যে সমঝোতা দরকার।
5. Code review pre-merge inspection হিসেবে bottleneck হয়ে যাচ্ছে।

## ৪. Goal ও Research Questions

Paper RQ হিসেবে তিনটি "fundamental question" তোলে (empirical RQ নয়):

| # | প্রশ্ন (paper-এর ভাষায়) | উত্তরের জায়গা |
|---|---|---|
| Q1 | What is an agentic engineer? | Section 2, New Idea #1 |
| Q2 | What characteristics should agentic engineers possess in order to be considered trustworthy? | Section 3, New Idea #2, Figure 1 |
| Q3 | What should developers verify and validate when working with agentic software engineers? | Section 4, New Idea #3–#6 |

লক্ষ্য: AI-কে "replace" করার productivity narrative থেকে সরে "trustworthy human-AI SE team"-এর নীতিভিত্তিক ধারণায় যাওয়া।

## ৫. Methodology (এই paper-এর ক্ষেত্রে: argument-এর ধাপ)

Paper-এ কোনো experimental method নেই। এটি conceptual/position paper; তাই এখানে যুক্তির ধাপগুলো ক্রমানুসারে দেওয়া হলো।

**ধাপ ১: Agentic engineer সংজ্ঞা (New Idea #1).** একটি AI agent তখনই agentic engineer, যদি ৪টি শর্ত পূরণ করে:

1. **Breadth:** coding-এর বাইরে বিভিন্ন SE task সামলায়: evolving problem statement, requirements, constraints, ethics, design, testing, operations, অসম্পূর্ণ তথ্যে iterative refinement [7]।
2. **Agency:** planning ও tool use দেখায়, শুধু code-কেন্দ্রিক নয় [10, 25]।
3. **Collaboration:** human workflow-এ coordination, feedback, negotiation সহ মিশে যায় [1, 10, 17]।
4. **Values:** human values, constraints, ethical responsibility মানে; সিদ্ধান্তের justification দেয়; accountability ও oversight সমর্থন করে (ethics-by-design, sustainability) [10, 17]।

Paper বলে এটি "autonomous coding"-এর চেয়ে উঁচু মান। এটি "working definition"।

**ধাপ ২: Trust ≠ trustworthiness।** Trustworthiness system property। Trust গতিশীল: অর্জন, হারানো, পুনঃ-calibrate করা যায়, কখনো হঠাৎ [20, 24, 34]। Developer trust-ই adoption-এর মূল বাধা [22]। Developer-দের default trust position আলাদা [26]। তাই trustworthiness এক-বারের জিনিস নয়; sustained, recalibrated সম্পর্ক ও mutual trust লাগে।

**ধাপ ৩: Multi-dimensional framework (New Idea #2).** Dimension-গুলো SE quality model (SWEBoK), trustworthy AI literature [23] ও [18]-এর ওপর ভিত্তি করে। তিনটি স্তর: system, model, output। তিন ধরনের stakeholder: developer, organisation, society। সময়সীমা: short ও long term। মূল যুক্তি: কোনো একক dimension necessary-and-sufficient নয়; configuration-ই justify করে।

Dimension-এর বিবরণ (Section 3 থেকে):

| পরিবার | অন্তর্ভুক্ত dimension | paper-এর সংজ্ঞা |
|---|---|---|
| Technical quality | correctness | output কার্যকরী requirement মেটায় কি না |
| Technical quality | reliability | সময়ের সাথে ধারাবাহিকভাবে গ্রহণযোগ্য ফল দেওয়ার ক্ষমতা |
| Technical quality | performance ও robustness | response time, efficiency, scalability, DoS-জাতীয় আচরণে resilience; invalid বা stress input-এ সঠিক আচরণ |
| Technical quality | security | vulnerability ও misuse প্রতিরোধ |
| Technical quality | cost | developer time, computational resource, financial expense, environmental impact; নির্ভুল হলেও অতি ধীর, ভঙ্গুর বা ব্যয়বহুল হলে untrustworthy |
| Transparency and accountability | transparency ও explainability, traceability, auditability, reproducibility, accountability | stakeholder কীভাবে ও কেন সিদ্ধান্ত হলো বুঝতে পারে; output-কে input, model, process-এর সাথে জোড়া যায়; একই শর্তে একই ফল; দায়িত্ব স্পষ্ট ও প্রয়োগযোগ্য |
| Epistemic humility | uncertainty জানানো, সীমা স্বীকার, bias সচেতনতা | নইলে overconfidence ও misplaced trust |
| Ethical alignment | fairness, bias mitigation, privacy, regulatory compliance, safety, sustainability | human values [21]-এর সাথে সামঞ্জস্য |
| Socio-technical practice | collaboration, team culture, developer experience, societal impact, cultural sensitivity, sustainability | team ও সমাজে responsible participant হিসেবে দেখা |

আমার পর্যবেক্ষণ: Figure 1 একটি ছবি; PDF text থেকে তার ভেতরের লেবেল সরাসরি পাওয়া যায়নি। উপরের table paper-এর Section 3 গদ্য থেকে বানানো। Figure 1-এর সঠিক গ্রুপিং supervisor-কে দেখানোর আগে মূল PDF-এ মিলিয়ে নেওয়া দরকার।

**ধাপ ৪: Selective visibility ও evidence-centric inspection (New Idea #3).** Agent বহু-ধাপে কাজ করে (planning, tool use, intermediate decision, refinement)। সব ধাপ দেখানো scalable নয়। তাই developer-কে দেখাতে হবে ঠিক সিগন্যালগুলো:

- output requirement ও constraint-এর সাথে মেলে কি না,
- মূল সিদ্ধান্ত defensible reasoning-এর ওপর দাঁড়িয়ে আছে কি না,
- uncertainty, assumption, সম্ভাব্য failure mode স্পষ্টভাবে জানানো হয়েছে কি না।

Paper-এর বক্তব্য (সংক্ষেপে): trustworthiness শুধু system কী তৈরি করে তার property নয়, কী প্রকাশ করতে বেছে নেয় তারও।

**ধাপ ৫: V&V পুনর্ভাবনা (New Idea #4).** Verification (সঠিকভাবে বানানো?) ও validation (সঠিক জিনিস বানানো?) বাড়ানো হয় process-level verification (planning/tool use উপযুক্ত?), epistemic verification (নিজের uncertainty সঠিক?) এবং validation-এর ক্ষেত্রে evolving requirement-এর সাথে আচরণের সামঞ্জস্য। Testing ও static analysis দরকার, কিন্তু একা যথেষ্ট নয়, কারণ ওরা কেবল final artefact-এ কাজ করে। সম্ভাব্য কৌশল: agent activity-কে সংক্ষিপ্ত meaningful সারাংশে distil করা, traceability, uncertainty/alternative/known limitation প্রকাশ, automated trustworthiness oracle [18]।

**ধাপ ৬: Code review as runtime monitoring (New Idea #5).** Deployed code "provisional"। Agent production-এ execution trace, resource usage, security signal, expected behaviour থেকে বিচ্যুতি পর্যবেক্ষণ করে। Review হয় temporally distributed, adaptive; development ও deployment-এর সীমা মুছে যায়।

**ধাপ ৭: Trust interface (New Idea #6).** Property থেকে developer-facing interface-এ রূপান্তর: কী তথ্য, কখন, কীভাবে দেখানো হবে যা developer-এর workflow ও cognitive সীমার সাথে মেলে। নইলে exhaustive verification বনাম uncritical reliance-এর সংকট।

## ৬. Math (formalisation)

Paper-এ কোনো formula, metric বা equation নেই। নিচের সবকিছু **আমার হিসাব / আমার formalisation** (paper-এর দাবি নয়); উদ্দেশ্য হলো paper-এর ধারণাকে আমাদের signal-এর সাথে মাপার মতো করে লেখা।

**৬.১ Configuration view (paper: "configurations of dimensions").** ধরি $D = \{d_1, \ldots, d_k\}$ dimension-এর সেট এবং কোনো context $c$ (task, stakeholder, সময়সীমা)-এ প্রতিটি dimension-এর জন্য একটি signal $s_i(x, c)$ আছে, $x$ হলো একটি agent output (যেমন একটি patch)। Paper বলে কোনো একক $d_i$ necessary-and-sufficient নয়। তাই আমরা কোনো weighted sum নিই না; report হলো ভেক্টর

$$
\mathbf{R}(x, c) = \left( s_1(x, c), \; s_2(x, c), \; \ldots, \; s_k(x, c) \right)
$$

এখানে $s_i$ নিজেই একটি তিন-মানের ফল হতে পারে: পাস, ফেল, বা যাচাই করা যায়নি (CG11, CG22)। এটি context-sensitive: একই $x$ আলাদা $c$-তে আলাদা নির্ভরতা justify করতে পারে।

**৬.২ Evidence-centric inspection-কে budget সমস্যা হিসেবে।** ধরি agent প্রতিটি output-এর সাথে $m$ টি সম্ভাব্য evidence item $E = \{e_1, \ldots, e_m\}$ তৈরি করতে পারে। Developer-এর মনোযোগ budget $B$। প্রতিটি item $e_j$-এর পরীক্ষার খরচ $\text{cost}(e_j)$ এবং তথ্যমূল্য $v(e_j)$। তাহলে "selective visibility" হলো

$$
\max_{S \subseteq E} \sum_{e_j \in S} v(e_j) \quad \text{such that} \quad \sum_{e_j \in S} \text{cost}(e_j) \leq B
$$

$v(e_j)$-কে আমরা মাপতে পারি: যদি $e_j$ পরীক্ষা করলে developer-এর সিদ্ধান্ত (গ্রহণ বা প্রত্যাখ্যান) বদলায় এবং সেই বদলটি সঠিক হয়, তাহলে মান বেশি। এটি paper-এর "see the right things" বাক্যের formal রূপ। Paper নিজে এ ধরনের কিছু বলে না।

**৬.৩ Epistemic humility = calibration।** Agent বা judge confidence $p$ দেয়। Calibration error (Expected Calibration Error, ECE):

$$
\text{ECE} = \sum_{b=1}^{M} \frac{n_b}{N} \left| \text{acc}(b) - \text{conf}(b) \right|
$$

- $M$ = confidence bin সংখ্যা, $N$ = মোট নমুনা, $n_b$ = bin $b$-তে নমুনা, $\text{acc}(b)$ = bin-এর প্রকৃত সঠিকতার হার, $\text{conf}(b)$ = bin-এর গড় confidence।
- ECE শূন্য মানে "যখন ৮০% confident, তখন ৮০% ক্ষেত্রে সঠিক"। এটি epistemic verification (New Idea #4)-এর একটি সম্ভাব্য মাপকাঠি। Paper ECE উল্লেখ করেনি; এটি আমাদের প্রস্তাব।
- Abstention-এর জন্য: coverage $\kappa$ = যত অংশে system উত্তর দেয়; selective accuracy = সেই অংশে নির্ভুলতা। Risk-coverage curve দিয়ে "যাচাই করা যায়নি" ফলাফলের মূল্য দেখানো যায় (CG7)।

**৬.৪ Reliability (paper: সময়ের সাথে ধারাবাহিকতা)।** একই task-এ $k$ বার চালালে সব বার সফল হওয়ার সম্ভাবনা, $\text{pass}^k = p^k$ (যদি প্রতিটি run স্বাধীন ও সফলতার সম্ভাবনা $p$)। এটি আমাদের run consistency (CG4)-এর সাথে মেলে।

**Worked example (আমার হিসাব; সংখ্যাগুলো আমাদের আগের sub-domain থেকে, এই paper থেকে নয়)।** Paper বলে correctness একা trustworthiness নয়। দুটি আগের ফলাফলে তা মাপা যায়:

- CWEval (Sub-domain 6): GPT-4o func@1 = 80.81 এবং func-sec@1 = 50.21। পার্থক্য = $80.81 - 50.21 = 30.60$ percentage point। অনুপাত $50.21 / 80.81 = 0.621$ (প্রায়)। অর্থাৎ শুধু "correctness" signal-এর ভিত্তিতে নির্ভর করলে সঠিক-ও-নিরাপদ ফলের মাত্র প্রায় ৬২.১% মেলে; বাকি প্রায় ৩৭.৯% ক্ষেত্রে অতি-নির্ভরতা (misplaced trust)।
- SecureVibeBench: Claude Code 48.6% correct বনাম 17.1% C-SEC। অনুপাত $17.1 / 48.6 = 0.352$ (প্রায়)। অর্থাৎ correct দাবি করা ক্ষেত্রের প্রায় ৬৪.৮% ($1 - 0.352 = 0.648$) correct-and-secure নয়।

দুটি উদাহরণই paper-এর "no single dimension is sufficient" দাবির সংখ্যাগত সমর্থন, কিন্তু এগুলো এই paper-এর ফল নয়।

## ৭. Setup

| Item | Detail |
|---|---|
| Experiment | নেই |
| Dataset / benchmark | নেই; paper: "There are no data available yet" |
| Model / agent | নেই। উল্লেখিত agent শুধু উদাহরণ: Claude Code [2], Codex [19], Kiro [12], AutoCodeRover [35], SWE-agent [33], RepairAgent [3], RovoDev [28] |
| Method | Literature-grounded conceptual argument: IEEE/ACM/SWEBoK সংজ্ঞা, Khati et al. [11], CRAFT [10], trust literature [20, 24, 34], trustworthy AI survey [14, 23] |
| Validation | নেই (কোনো user study, case study বা expert survey নেই) |
| মূল উৎস-নির্ভরতা | Hoda [10] (সহলেখক), Roychoudhury et al. [22, 23] (সহলেখক Ray), Nguyen Tung et al. [18] (সহলেখক Aleti) |

আমার পর্যবেক্ষণ: তিনটি মূল ধারণা (CRAFT, Agentic AI software engineer, trustworthiness oracle) লেখকদের নিজেদের পূর্বের কাজের ওপর দাঁড়িয়ে; স্বাধীন সমর্থন নেই।

## ৮. Results (argument-এর ফলাফল; কোনো সংখ্যাগত ফল নেই)

কোনো table বা figure-এ পরিমাপ নেই। Paper-এ একমাত্র Figure 1 (multidimensional view)। নিচে paper-এর "ফল" অর্থাৎ ছয়টি New Idea এবং আমাদের প্রকল্পের সাথে সরাসরি রূপান্তর।

**৮.১ Paper-এর ছয় দাবি**

| ID | দাবি | Paper-এ কোথায় |
|---|---|---|
| NI1 | Agentic engineer = ৪ শর্ত (breadth, agency, collaboration, values) | Section 2 |
| NI2 | Multi-dimensional trustworthiness framework (system/model/output স্তর; developer/organisation/society) | Section 3, Figure 1 |
| NI3 | Artefact-centric থেকে evidence-centric inspection | Section 4 |
| NI4 | V&V multi-level: output, process, epistemic | Section 4 |
| NI5 | Code review = continuous runtime monitoring | Section 4 |
| NI6 | Trustworthiness property থেকে trust interface | Section 4 |

**৮.২ Trust dimension থেকে আমাদের signal ও CG-এর ম্যাপ (আমার ম্যাপিং)**

| Paper-এর dimension | আমাদের assurance signal | সংশ্লিষ্ট CG |
|---|---|---|
| Correctness | F2P/P2P test, regression run, patch-targeted test, distinguishing test | CG1, CG2, CG3, CG13, CG14 |
| Correctness (static) | rubric-driven reasoning judge + learned classifier (দুটি আলাদা signal) | CG10, CG16, CG17, CG22 |
| Reliability | pass^k, run-to-run variance, environment health | CG4, CG8, CG15 |
| Performance / robustness | invalid input ও stress test, timeout; patch-এর ভেতরে performance regression check | CG3, CG13 |
| Security | functional+security joint verdict (before/after delta), scanner agreement | CG5, CG20, CG21 |
| Cost | token, wall-clock, USD per task (report-এ আলাদা কলাম) | CG8 (G3, ১৩ দেখো) |
| Transparency / explainability | judge-এর rubric-ভিত্তিক ব্যাখ্যা; patch-issue-requirement traceability | CG16, CG17 |
| Traceability / auditability / reproducibility | tool ও model version-সহ verdict; fixed seed ও environment hash | CG11, CG15 |
| Accountability | কে কোন signal-এ সম্মতি দিল তার log; agent-কে "author oracle" না ধরা | CG19 |
| Epistemic humility | confidence, abstention, "could not verify" outcome; task-unclear detection | CG7 |
| Ethical alignment / values | leakage ও gaming check, persuasion/prompt-injection robustness; secrets/privacy scan | CG12, CG18, CG6 |
| Socio-technical / collaboration | (আমাদের সীমার বাইরে; future work) | — |

**৮.৩ Paper-এর দাবি বনাম আমাদের আগের সংখ্যাগত প্রমাণ (আগের sub-domain থেকে; এই paper-এর নয়)**

| Paper-এর দাবি | আমাদের আগের প্রমাণ | Sub-domain |
|---|---|---|
| "No single dimension sufficient" | GPT-4o func@1 80.81 বনাম func-sec@1 50.21 (CWEval) | ৬ |
| Reliability আলাদা dimension | SWE-agent pass@1 17.94 বনাম pass@6 32.67 | ১ |
| Correctness সব নয় | AutoCodeRover: 51/78 = 65.4% plausible patch সঠিক | ১ |
| Epistemic humility দরকার | Agentless Lite-S audit: ১০% ক্ষেত্রে তথ্য অপর্যাপ্ত (abstention দরকার) | ১ |
| Judge-এর transparency | Human rubric Fleiss kappa 0.31 → shared rubric 0.66 | ৫ |
| Trust interface দরকার | HITL LLM judge: recall 0.93, precision 0.65 (মানব পর্যালোচনা প্রয়োজন) | ৫ |
| Security signal-এর নিজের নির্ভরযোগ্যতা | ~৫০% Semgrep alert মিথ্যা (SecureVibeBench) | ৬ |

## ৯. Key findings (paper-এর মূল সিদ্ধান্ত)

1. **Agentic engineer ≠ coding agent।** ৪টি শর্ত (breadth, agency, collaboration, values) না মিটলে "software engineer" বলা যাবে না।
2. **Trustworthiness একটি system property, trust নয়।** দুটি অসমমিত; অতি-নির্ভরতা ও অপর্যাপ্ত-নির্ভরতা দুটিই ক্ষতিকর।
3. **Trust গতিশীল:** অর্জন, হারানো, recalibrate করা যায়। তাই এককালীন সার্টিফিকেশন নয়, continuous assessment।
4. **কোনো একক dimension যথেষ্ট নয়:** configuration-based, context-dependent।
5. **Developer-এর জন্য evidence > artefact:** "সব দেখো" নয়, "সঠিক জিনিস দেখো"। Trustworthiness হলো system যা প্রকাশ করতে বেছে নেয় তারও property।
6. **V&V তিন স্তরে:** output, process (planning/tool use), epistemic (uncertainty)। Testing ও static analysis একা অপর্যাপ্ত।
7. **Code review runtime-এ চলে যাবে:** deployed code "provisional"; development ও deployment-এর সীমা ঝাপসা।
8. **Measurement gap:** property জানা আছে, কিন্তু developer-facing interface ও পরিমাপ নেই। এটিই paper-এর শেষ আহ্বান।

## ১০. Alternatives-এর চেয়ে ভালো কোথায়

| তুলনা | Paper-এর অবস্থান |
|---|---|
| বনাম "autonomous coding" দৃষ্টিভঙ্গি | উচ্চতর মান: SE lifecycle, collaboration, accountability অন্তর্ভুক্ত |
| বনাম Khati et al. [11] (ability, benevolence, integrity) | Khati coding model-এর জন্য; এই paper agent-এর planning, tool use, collaboration, decision process-ও ধরে |
| বনাম সাধারণ trustworthy AI [14] | সাধারণ নীতিগুলোকে AI SE agent-এ বসায় এবং SE quality model (SWEBoK)-এর সাথে জোড়ে |
| বনাম একক metric (accuracy) | Configuration view; correctness একা নয় |
| বনাম exhaustive review | Evidence-centric, selective visibility; review fatigue এড়ায় |
| বনাম pre-merge review | Runtime monitoring সহ continuous review |

আমার পর্যবেক্ষণ: এই তুলনাগুলো কেবল যুক্তিভিত্তিক; কোনো empirical তুলনা নেই, তাই "ভালো" কথাটি এখানে "বেশি সম্পূর্ণ" অর্থে।

## ১১. কখন কাজ করে / কখন ব্যর্থ

**কাজ করার সম্ভাব্য ক্ষেত্র (paper-এর যুক্তি অনুসারে):** বড় আকারের agent output, যেখানে exhaustive review অসম্ভব; high-stakes ও জটিল প্রেক্ষাপট (epistemic humility-র জন্য paper "complex or high-stakes settings" উল্লেখ করে); মানব-AI team।

**ব্যর্থ হতে পারে (আমার পর্যবেক্ষণ, paper আংশিক স্বীকার করে):**

- Agent যা "প্রকাশ করতে বেছে নেয়" সেটিই যদি সাজানো বা অসত্য হয়: Turpin et al. [29]-এর unfaithful chain-of-thought ফল দেখায় ব্যাখ্যা বিশ্বাসযোগ্য না-ও হতে পারে। তখন "evidence" নিজেই gaming-এর শিকার (CG12)।
- যখন uncertainty ভুল calibrate করা (overconfident), epistemic humility ফাঁপা।
- Developer-দের default trust position ভিন্ন [26]; একই evidence আলাদা ভাবে কাজ করবে।
- Process-level verification-এর ground truth নেই: "planning ঠিক কি না" কে ঠিক করবে?
- Paper-এ কোনো validation না থাকায় কোন dimension বাস্তবে সিদ্ধান্ত বদলায় তা অজানা।

## ১২. Limitations

**Paper নিজে যা বলে:**

- "There are no data available yet."
- Measurement gap স্বীকার; empirical ও design-oriented গবেষণার ডাক।
- Property থেকে interface-এ রূপান্তর "significantly less attention" পেয়েছে।
- Trustworthiness এককালীন নয়; context-sensitive।

**আমার পর্যবেক্ষণ:**

1. কোনো empirical validation, user study, বা case study নেই; ৬টি "New Idea" কেবল দাবি।
2. Dimension-গুলো পরিমাপের সংজ্ঞা দেয়নি (যেমন "epistemic humility কীভাবে মাপব?")।
3. Dimension-এর মধ্যে দ্বন্দ্ব ও trade-off (যেমন cost বনাম correctness, transparency বনাম privacy) আলোচিত নয়।
4. Gaming ও adversarial ঝুঁকি (agent evidence সাজাতে পারে) প্রায় অনুপস্থিত; METR-এর ফল (context.md: ≥16% সফল long-task run ছিল cheat) এর সাথে সরাসরি সম্পর্কিত।
5. "Evidence"-এর কোনো ধরন-তালিকা বা ন্যূনতম সেট দেওয়া নেই।
6. Process-level verification-এর oracle অনির্ধারিত।
7. Code review as runtime monitoring-এর কোনো ঝুঁকি বিশ্লেষণ নেই (false alarm, monitor-এর নিজের trustworthiness)।
8. Security ও correctness-এর আগের empirical ফল (যেমন plausible ≠ correct) paper-এ উল্লেখ নেই, তাই দাবিগুলো সংখ্যাগতভাবে সমর্থিত নয়।
9. ACM template placeholder (Conference'17, DOI nnnnnnn) থেকে বোঝা যায় এটি এখনো চূড়ান্ত venue-এ প্রকাশিত নয়, বা v2 ক্যামেরা-রেডি নয়।
10. সহলেখকদের নিজ-উদ্ধৃতি বেশি (Hoda [10], Roychoudhury et al. [22, 23], Nguyen Tung et al. [18])।

## ১৩. Research gaps

| G-id | Gap | Evidence | Related CG / folder |
|---|---|---|---|
| G1 | Trustworthiness dimension-এর কোনো operational metric নেই (measurement gap) | Section 5: "trustworthiness measurement gap"; Section 4: "significantly less attention" | নতুন CG23 (প্রস্তাব); সব sub-domain |
| G2 | "Evidence" কোন item, কত সংখ্যায়, কে বাছবে তা অজানা; budget-সীমিত inspection-এর মূল্য মাপা হয়নি | New Idea #3, #6; কোনো experiment নেই | নতুন CG24 (প্রস্তাব); 05_Patch_Validation |
| G3 | Cost একটি trust dimension কিন্তু assurance report-এ cost-aware trade-off নেই | Section 3 cost অনুচ্ছেদ; context.md cost: Opus 5.5 13.20 USD বনাম GPT-6.1 Sol 1.72 USD (Vals, I) | CG8 |
| G4 | Epistemic verification: agent-এর confidence calibrated কি না কেউ মাপেনি | New Idea #4 | CG7 |
| G5 | Process-level verification-এর ground truth ও oracle নেই | New Idea #4 | CG19 |
| G6 | Evidence ও trust interface নিজে gaming/persuasion-এর শিকার হতে পারে | Paper-এ আলোচনা নেই; [29] unfaithful CoT | CG12, CG18 |
| G7 | Runtime monitoring-এর নিজের নির্ভরযোগ্যতা ও false alarm হার | New Idea #5 | CG11, CG21 |
| G8 | Developer trust calibration-এর (অতি/অপর্যাপ্ত নির্ভরতা) human-subject প্রমাণ নেই | Section 3, [26] | CG7 (human study; SPL3 সীমার বাইরে হতে পারে) |
| G9 | Dimension-এর মধ্যে trade-off ও তাদের configuration-এর নিয়ম অনির্ধারিত | "configurations of dimensions" | CG10 |

**CG তালিকার জন্য নতুন প্রস্তাব:** CG23 = trustworthiness-এর dimension-ভিত্তিক operational metric-এর অভাব (প্রতিটি dimension-এর জন্য signal, uncertainty ও version-bound verdict)। CG24 = inspection-budget-সীমিত অবস্থায় কোন evidence সিদ্ধান্ত বদলায় তা অজানা।

## ১৪. Improvement ideas

1. **Dimension-to-signal table:** ৮.২-এর ম্যাপকে চূড়ান্ত report schema-য় রূপ দেওয়া; প্রতিটি dimension-এর জন্য ঠিক একটি primary signal, tool ও model version, uncertainty।
2. **Tri-state verdict:** প্রতিটি signal পাস / ফেল / যাচাই করা যায়নি (abstain)। "যাচাই করা যায়নি" ছাড়া epistemic humility বাস্তবায়ন অসম্ভব।
3. **Evidence value experiment:** Developer (বা LLM-simulated reviewer)-কে বিভিন্ন evidence সেট দেখিয়ে সিদ্ধান্তের সঠিকতা মাপা: raw patch বনাম patch+signal report।
4. **Calibration audit:** Judge ও agent-এর confidence-এর ECE ও risk-coverage curve (৬.৩)।
5. **Process-level check:** Agent trajectory থেকে সংক্ষিপ্ত "decision summary" বানিয়ে তার সঠিকতা যাচাই; তার সাথে trajectory-তে .git/network ব্যবহার বা test-edit সনাক্তকরণ (leakage ও gaming)।
6. **Cost column:** প্রতিটি patch report-এ token, সময়, USD খরচ।
7. **Runtime monitoring সরলীকরণ:** শুধু post-merge test rerun ও regression delta, SPL3 সীমার জন্য।
8. **Trust-interface prototype:** এক-পৃষ্ঠার JSON/Markdown report যেখানে ৫–৭টি signal ও তাদের অনিশ্চয়তা দেখানো হয়।

## ১৫. Publication potential (SPL3-feasible)

- **সবচেয়ে বাস্তব:** একটি "from framework to measurement" workshop বা short paper: Aleti et al.-এর dimension-গুলোকে ১০–১২টি পরিমাপযোগ্য signal-এ রূপান্তর করে আমাদের assurance report prototype-এর ফল দেখানো। Paper নিজেই বলছে এটি অনুপস্থিত, তাই novelty যুক্তিযুক্ত।
- সম্ভাব্য venue ধরন: SE-এর trustworthy-AI বা LLM-for-SE workshop (নির্দিষ্ট venue নাম এই paper থেকে বলা যায় না)।
- ঝুঁকি: ছাত্র-প্রকল্পের সীমিত compute; তাই fresh SWE-rebench-এর ছোট উপসেট এবং আগের paper-এর পাবলিক patch ব্যবহার করা উচিত।
- Human-subject trust study বাস্তবসম্মত নয়; বদলে LLM-simulated reviewer বা অল্প-সংখ্যক expert rater।

## ১৬. SPL3 implementation

**Assurance report schema (প্রস্তাব, আমার ডিজাইন):**

| Signal ID | Paper dimension | কীভাবে মাপব | Output |
|---|---|---|---|
| S1 | Correctness | repo test (F2P/P2P) + patch-targeted test | pass / fail / unverifiable |
| S2 | Correctness (oracle strength) | mutation বা distinguishing test audit | strong / weak / unknown |
| S3 | Static plausibility | rubric-driven reasoning judge | verdict + confidence |
| S4 | Static plausibility (দ্বিতীয় স্বাধীন) | learned classifier | score + ECE |
| S5 | Reliability | pass^k, k run | rate ± interval |
| S6 | Security | scanner delta (before/after) + test | delta + scanner agreement |
| S7 | Epistemic | confidence calibration; abstain rule | ECE, coverage |
| S8 | Integrity/gaming | .git/network leakage, test edit, hidden-test reasoning check | clean / flagged |
| S9 | Traceability | patch, issue, test link; model/tool version | complete / partial |
| S10 | Cost | token, সময়, USD | number |
| S11 | Robustness of judge | persuasion/prompt-injection comment in patch | stable / flipped |

**ধাপ:**

1. ২০–৩০ SWE-rebench fresh task বেছে নিই; ২–৩টি agent থেকে patch সংগ্রহ।
2. S1–S11 চালাই; প্রতিটি signal আলাদা রাখি (কোনো weighted score নয়)।
3. Evidence-centric report ও raw-patch-only baseline তুলনা: reviewer (LLM-simulated + ২–৩ জন মানুষ) সঠিক গ্রহণ/প্রত্যাখ্যানে কতটা ভালো (McNemar paired test)।
4. Metric: recall ও specificity উভয়, R@P=0.8, ECE, abstention coverage।
5. Ablation: কোন signal বাদ দিলে সিদ্ধান্তের সঠিকতা সবচেয়ে কমে (৬.২-এর $v(e_j)$-এর অভিজ্ঞতামূলক মাপ)।

## ১৭. আগের sub-domain-এর সাথে সম্পর্ক

| Sub-domain | সংযোগ |
|---|---|
| ১ AI Coding Agents | SWE-agent pass@1 বনাম pass@6 (reliability), AutoCodeRover 51/78 plausible ≠ correct (correctness dimension একা অপর্যাপ্ত), Agentless-এর audit (epistemic humility ও task-unclear) |
| ২ APR | VRpilot ও RePaCA: static ও compiler signal; "plausible ≠ correct" এই paper-এর "correctness একা নয়"-এর উদাহরণ |
| ৩ Evaluation | SWE-rebench, SWE-Bench Pro: reproducibility, run-to-run variance, benchmark contamination (reliability, auditability) |
| ৪ Test generation | Oracle strength (CG13) = trustworthy test evidence |
| ৫ Patch Validation | HITL LLM-as-a-Judge: human rubric ও judge-এর error direction; "evidence-centric inspection"-এর সরাসরি বাস্তবায়ন |
| ৬ Security | CWEval ও SecureVibeBench: security dimension; scanner reliability (CG21) |

এই paper কোনো sub-domain-এর technical কাজকে প্রতিস্থাপন করে না; এটি সবকটিকে একটি common vocabulary দেয়: correctness, reliability, security, transparency, epistemic humility, accountability।

## ১৮. Supervisor Q&A

1. **প্রশ্ন: Paper-এ কোনো experiment নেই; আমরা এটি কেন গুরুত্ব দিচ্ছি?** উত্তর: এটি vision paper। আমাদের জন্য এটি framework: assurance report-এ কোন dimension থাকা উচিত তার তাত্ত্বিক ভিত্তি। এর নিজের স্বীকৃত "measurement gap"-ই আমাদের কাজের ক্ষেত্র।
2. **প্রশ্ন: Trust আর trustworthiness-এর পার্থক্য আমাদের জন্য কেন গুরুত্বপূর্ণ?** উত্তর: আমরা একটি system-এর property মাপছি (patch বা agent কতটা নির্ভরযোগ্য), developer-এর মনোভাব নয়। তাই আমাদের মাপকাঠি objective signal, survey নয়।
3. **প্রশ্ন: Paper বলে "no single dimension suffices"। আমাদের সংখ্যায় প্রমাণ?** উত্তর: CWEval-এ GPT-4o func@1 80.81 বনাম func-sec@1 50.21; AutoCodeRover-এ plausible patch-এর ৬৫.৪% সঠিক। (আগের sub-domain-এর সংখ্যা, এই paper-এর নয়।)
4. **প্রশ্ন: Evidence-centric inspection কীভাবে আমাদের design-এ আসে?** উত্তর: Report-এ raw patch-এর বদলে আলাদা signal (S1–S11), প্রতিটির অনিশ্চয়তা ও version, এবং "যাচাই করা যায়নি" আউটপুট। Weighted score নয়, কারণ gaming ঝুঁকি (CG12)।
5. **প্রশ্ন: Evidence নিজেই যদি ভুল বা সাজানো হয়?** উত্তর: এটি paper-এ আলোচিত নয়; আমাদের গ্যাপ G6। আমরা judge-এর persuasion test (S11) ও gaming check (S8) রাখব; agent-এর নিজের ব্যাখ্যাকে ground truth ধরব না (CG19)।
6. **প্রশ্ন: Epistemic humility আমরা কীভাবে মাপব?** উত্তর: Confidence-এর ECE এবং abstention-এর risk-coverage curve; paper কোনো metric দেয়নি, তাই এটি আমাদের প্রস্তাব (৬.৩)।
7. **প্রশ্ন: Paper-এর কোন দাবি সবচেয়ে দুর্বল মনে হয়?** উত্তর: Code review as runtime monitoring: কোনো ঝুঁকি বিশ্লেষণ বা উদাহরণ নেই; monitor-এর নিজের নির্ভরযোগ্যতা অনির্ধারিত। আমরা এটি SPL3-এর সীমার বাইরে রাখছি।
8. **প্রশ্ন: Venue কী?** উত্তর: arXiv:2602.06310v2 (3 Jun 2026)। ACM template-এর venue ও DOI placeholder (Conference'17, nnnnnnn); তাই চূড়ান্ত venue জানা নেই।

## ১৯. Glossary

| Term | অর্থ |
|---|---|
| Agentic engineer | ৪ শর্ত-পূরণকারী AI agent (breadth, agency, collaboration, values) |
| Trust | মানুষের নির্ভরতার সিদ্ধান্ত/প্রবণতা |
| Trustworthiness | system-এর সেই property যা নির্ভরতাকে justify করে |
| Evidence-centric inspection | final output নয়, তার পেছনের justification ও signal পরীক্ষা |
| Selective visibility | কী প্রকাশ হবে তা বেছে নেওয়ার সমস্যা |
| Process-level verification | agent-এর planning ও tool use ঠিক কি না |
| Epistemic verification | agent নিজের uncertainty ঠিক জানায় কি না |
| Epistemic humility | সীমা ও অনিশ্চয়তা স্বীকার |
| Traceability | output-কে input, model, process-এর সাথে জোড়া |
| Trust interface | trustworthiness property-কে developer-facing রূপে দেখানো |
| Trustworthiness oracle | trustworthiness property-র জন্য স্বয়ংক্রিয় check |
| CRAFT | Comprehensive, Responsible, Adaptive, Foundational, Translational |
| ECE | Expected Calibration Error |

## ২০. Summary card

| Item | Detail |
|---|---|
| Paper | Trustworthy AI Software Engineers (Aleti, Ray, Hoda, Chen), arXiv:2602.06310v2, 3 Jun 2026 |
| ধরন | Vision paper; ৫ পৃষ্ঠা; ৩৬ reference; কোনো data নেই |
| মূল ধারণা | Agentic engineer (৪ শর্ত); trustworthiness = system property; configuration of dimensions; evidence-centric inspection; multi-level V&V |
| ছয় New Idea | NI1 সংজ্ঞা, NI2 framework, NI3 evidence-centric, NI4 V&V, NI5 runtime review, NI6 trust interface |
| শক্তি | স্পষ্ট conceptual frame; trust বনাম trustworthiness পার্থক্য; "see the right things" |
| দুর্বলতা | কোনো validation নেই; metric নেই; gaming ও trade-off আলোচিত নয় |
| আমাদের ব্যবহার | Assurance report-এর dimension কাঠামো; ৮.২ ম্যাপ (dimension, signal, CG) |
| নতুন gap | CG23 (operational trust metric-এর অভাব), CG24 (evidence value অজানা) |

## ২১. বর্তমান (2026) প্রেক্ষাপট

### ২১.১ তখন বনাম এখন

| বিষয় | Paper-এর অবস্থান (v2, 3 Jun 2026) | বর্তমান তথ্য (context.md) |
|---|---|---|
| Agent উদাহরণ | Claude Code, Codex, Kiro, AutoCodeRover, SWE-agent, RepairAgent, RovoDev | Claude Opus 5.5 (2026-09-22), Sonnet 5.5, GPT-6 family, Gemini 4 Argon, Kimi K3.1 Pro, GLM-5.x, DeepSeek V4; harness: mini-SWE-agent (এসব তথ্য context.md-তে আছে, এই paper-এ নেই) |
| Correctness benchmark | কোনো benchmark নেই | SWE-bench Verified saturated: Vals.ai 97.0% (I); OpenAI ব্যবহার বন্ধ করেছে, audited উপসেটের ≥59.4% flawed test (S) |
| Reliability | জেনেরিক দাবি | SWE-rebench pass@1 বনাম pass@5 ফারাক ১২–১৮ pts (I); ২৯টির মধ্যে ০টি adjacent top-30 জোড়া আলাদা করা যায় (I) |
| Security | জেনেরিক দাবি | SusVibes: FuncPass 62–84% বনাম SecPass 7.8–17.3% (I, Opus 4.6/GPT-5.4 যুগ) |
| Integrity/gaming | আলোচিত নয় | METR: ≥16% সফল long-task run cheat (I, আগের প্রজন্ম); Opus 5.5 card-এ hidden tests reasoning ও git concealment কিছু পরিবেশে (V) |
| Judge | আলোচিত নয় | Plain-LLM judge ComPass 62.14% (S); "over-fix" flag-এ ৫–১০% precision (S); Opus 5.5/GPT-6 patch-এর judge study নেই |
| Cost | cost একটি dimension | Vals Terminal-Bench 4.0 (I): Opus 5.5 13.20 USD, Kimi K3.1 Pro 4.57, GPT-6.1 Sol 1.72 |

### ২১.২ এখনো সত্য / পুরোনো

**এখনো সত্য:**

- "কোনো একক dimension যথেষ্ট নয়": SusVibes-এর FuncPass 62–84% বনাম SecPass 7.8–17.3% সরাসরি সমর্থন (I)।
- Reliability আলাদা dimension: pass@1 বনাম pass@5 ফারাক ১২–১৮ pts।
- Gaming ও integrity বাস্তব সমস্যা (METR, system card), যা paper আলোচনা করেনি।
- Developer review একটি bottleneck এবং industry rubric/LLM-judged mergeability-র দিকে যাচ্ছে (FrontierCode)।

**পুরোনো বা অসম্পূর্ণ:**

- Paper-এ উল্লেখিত agent-গুলো (AutoCodeRover, SWE-agent) এখন পূর্ববর্তী প্রজন্ম।
- Paper কোনো সংখ্যা ব্যবহার করে না, তাই সংখ্যা পুরোনো হয়নি; কিন্তু দাবিগুলোর সংখ্যাগত যাচাই বর্তমান model-এর জন্য নেই।

### ২১.৩ আজকের উন্মুক্ত gap

| Gap | বর্তমান অবস্থা | Related |
|---|---|---|
| Trust dimension-এর operational metric | কোনো standard নেই; বর্তমান model-এর তথ্য পাওয়া যায়নি | G1 / CG23 |
| Epistemic humility (calibration) | বর্তমান model-এর তথ্য পাওয়া যায়নি (calibration বা abstention ফল নেই) | G4 / CG7 |
| Evidence-centric report-এর ব্যবহারযোগ্যতা | কোনো human-subject বা industry-validated ফল পাওয়া যায়নি | G2 / CG24 |
| Judge-এর নির্ভরযোগ্যতা বর্তমান patch-এ | Opus 5.5/GPT-6 patch-এ judge study নেই | CG17, CG18 |
| Security signal | SusVibes/BaxBench-এ current-model data নেই | CG20, CG21 |
| Gaming-এর বিরুদ্ধে evidence | Opus 5.5 card-এ hidden-test reasoning (V); স্বাধীন নিয়মিত ডেটা নেই | CG12 |

### ২১.৪ বর্তমান model-সহ SPL3 idea (cost-aware)

- **Idea:** আমাদের assurance report (S1–S11)-কে ২০–৩০টি fresh SWE-rebench task-এ চালানো, patch আসবে একটি সস্তা ও একটি দামী current model থেকে।
- **Cost-সচেতন পরিকল্পনা (context.md-র Vals সংখ্যা):** per-task খরচ Opus 5.5 13.20 USD, Kimi K3.1 Pro 4.57, GPT-6.1 Sol 1.72। আমার হিসাব (শুধু agent-run খরচ, প্রতি একক run-এ; Terminal-Bench খরচ SWE-rebench task-এ হুবহু প্রযোজ্য নাও হতে পারে): ৩০ task × 1.72 = 51.60 USD (Sol) বনাম ৩০ × 13.20 = 396.00 USD (Opus 5.5)। তাই প্রধান patch-সংগ্রহ Sol বা Kimi দিয়ে, Opus শুধু ছোট উপসেটে। k-run বাড়ালে খরচও k গুণ।
- **Judge:** reasoning judge শুধু static signal (S3) হিসেবে; ঝুঁকি: over-fix flag-এ ৫–১০% precision (S) ও persuasion; তাই recall ও specificity উভয়ই মাপতে হবে।
- **Gaming check (S8):** .git/network ব্লক করা (SWE-Bench Pro Verified-এ GLM-5.2 78.80% → 57.32%, I), trajectory-তে test-edit/hidden-test সন্ধান।
- ফলাফল ব্যাখ্যা: vendor (V) ও independent (I) সংখ্যা আলাদা লেবেলে রাখা; ছোট নমুনায় confidence interval ও paired test।

### ২১.৫ ৩টি Q&A

1. **প্রশ্ন: এই paper-এর framework কি বর্তমান model-এও প্রযোজ্য?** উত্তর: Framework সাধারণ (model-নির্ভর নয়), তাই প্রযোজ্য। কিন্তু current-model-এ প্রতিটি dimension কতটা পূরণ হয় তার স্বাধীন ডেটা অনেক ক্ষেত্রে পাওয়া যায়নি (calibration, judge, SusVibes current model)।
2. **প্রশ্ন: Vendor-reported সংখ্যা কি trustworthiness-এর প্রমাণ?** উত্তর: না। যেমন SWE-Bench Pro-তে Opus 5.5 89.9% (V) বনাম Scale board top 61.50 ± 3.10 (I)। Paper-এর transparency/auditability dimension ঠিক এই ফারাকের কথাই বলে: যাচাইযোগ্য, version-bound verdict দরকার।
3. **প্রশ্ন: Cost কি trustworthiness dimension হিসেবে আমরা report-এ রাখব?** উত্তর: হ্যাঁ; paper cost-কে স্পষ্ট dimension বলে। Vals Terminal-Bench 4.0-এ Opus 5.5 13.20 USD বনাম GPT-6.1 Sol 1.72 USD প্রতি task; তাই report-এ cost একটি আলাদা কলাম, score-এর সাথে মেশানো নয়।
