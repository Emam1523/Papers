# Paper Analysis 03 (Eval): Engineering Reliable Coding Agents — Evaluating and Operating the System Around the Model

> **Sub-domain:** Coding-Agent Evaluation & Reliability
> **Analysis করেছে:** SPL3 — AI Coding Agent Reliability and Assurance
> **Paper file:** `Coding-Agent Evaluation & Reliability/Engineering Reliable Coding Agents.pdf`
> **বিশেষ নোট:** এটা সাধারণ paper নয় — প্রায় 133,000 শব্দের (PDF-এ 313 পৃষ্ঠা) একটা **technical review + engineering monograph**। তাই পুরোটা line-by-line পড়া হয়নি; কোন অংশ গভীরভাবে পড়া হয়েছে আর কোনটা skim করা হয়েছে তা Section ৫.৯-এ লেখা আছে।

---

## ০. Paper-এর পরিচয় (Bibliographic Info)

| বিষয় | তথ্য |
|---|---|
| **Title** | Engineering Reliable Coding Agents: Evaluating and Operating the System Around the Model |
| **Author** | Stephanie Jarmak (একক লেখক) |
| **Institution / affiliation** | PDF-এ আলাদা করে institution লেখা নেই। Data availability অংশে লেখক নিজেই বলেছেন যে Chapter 12-এর benchmark (CodeScaleBench) তিনি এমন একটা vendor-এ বানিয়েছেন ও চালান, যার retrieval product benchmark-এর একটা arm সরবরাহ করে (repository: `github.com/sourcegraph/CodeScaleBench`) |
| **Venue** | arXiv preprint — arXiv:2608.13867v1 [cs.SE], 14 August 2026; Version 1.0.0 (peer-reviewed নয়) |
| **Paper type** | **Structured multivocal review + engineering monograph** — নতুন algorithm বা benchmark নয়; বরং evidence-graded practice catalog, একটা system-level framework, লেখকের নিজের system থেকে মাপা কিছু ফলাফল, আর runnable protocol |
| **আকার** | 6টা Part, 20টা chapter, 313 PDF page, 249টা reference |
| **Evidence corpus** | 164 scholarly works, 100 practitioner records, 29 benchmark records, 17 author-system case records |
| **Artifacts** | 206টা reliability record-এর catalog (193 gated practice, যার 56টা গভীরভাবে developed; আর 13টা research lead), machine-readable evidence ledger, chapter crosswalk, benchmark catalog, ছয়টা runnable protocol, পাঁচটা reusable agent skill, blinded external-grading packet — সব `github.com/sjarmak/engineering-reliable-coding-agents`-এ (লেখকের দাবি; আমি repository খুলে যাচাই করিনি) |
| **আমাদের domain-এ গুরুত্ব** | ⭐⭐⭐⭐⭐ — আমাদের domain-এর নামটাই ("Reliability and Assurance") এই monograph-এর মূল বিষয়। CG4 (run-to-run reliability), CG6 (benchmark quality), CG8 (evaluation rigor) ও CG10 (assurance tool-এর নিজের validity)-এর জন্য এটা এখন পর্যন্ত সবচেয়ে বিস্তারিত উৎস |

---

## ১. এক লাইনে Paper (TL;DR)

**Coding agent-কে আমরা "model" হিসেবে মাপি কিন্তু "system" হিসেবে চালাই; তাই অনেক failure যেটাকে model-এর দোষ মনে হয় তা আসলে harness, execution environment, retrieval, state, permission, verifier বা review-এর দোষ — আর evaluation থেকে operation পর্যন্ত পুরো ব্যাপারটা একটা dependency chain, যেখানে আগের (upstream) স্তরের দুর্বলতা পরের (downstream) স্তরের কোনো machinery দিয়ে সারানো যায় না (repair asymmetry)।**

### Supervisor-কে ৩০ সেকেন্ডে কীভাবে বলবো
> "Sir, এটা একটা বড় review-monograph। লেখক 164টা scholarly paper, 100টা practitioner record আর নিজের চালানো system-এর measurement মিলিয়ে দেখিয়েছেন যে coding agent-এর reliability শুধু model-এর ব্যাপার না — benchmark-এর test দুর্বল হলে, একবার run করলে, verifier ভুল artifact-এ চললে, বা retrieval stale হলে ভালো score-ও বিভ্রান্তিকর। যেমন 60,000 SWE-bench Verified trajectory-তে একই setup-এ single-run score 2.2 থেকে 6.0 percentage point পর্যন্ত ওঠানামা করেছে, অথচ অনেক paper 2–3 point উন্নতিকে 'improvement' বলে। লেখক এগুলোকে একটা ছয়-স্তরের dependency chain হিসেবে সাজিয়েছেন — measurement, grading, containment/recovery, retrieval/context, review, allocation — আর 206টা evidence-graded practice দিয়েছেন। আমাদের 'assurance layer' direction-এর জন্য এটা সরাসরি কাজে লাগে: paired comparison, pass^k, judge calibration, আর verdict-কে নির্দিষ্ট artifact version-এর সাথে বেঁধে রাখার নিয়ম।"

---

## ২. Background — এই paper বুঝতে যা আগে জানা দরকার

Monograph-টা অনেক field একসাথে ছুঁয়েছে (statistics, software testing, distributed systems, security, information retrieval, HCI)। নিচে প্রতিটা নতুন concept সহজভাবে ব্যাখ্যা করা হলো।

### ২.১ Model বনাম System; Harness ও Scaffold
- **Model:** LLM নিজে — text নেয়, text দেয়।
- **Coding agent system:** model + তার চারপাশের সব কিছু — কোন tool ব্যবহার করতে পারবে, কোন file দেখবে, কোথায় code চালাবে, কে verify করবে, কে approve করবে।
- **Evaluation harness:** লেখকের glossary অনুযায়ী — যে code, configuration, tool, permission, prompt, task version ও grader মিলে একটা system-কে "recorded outcome"-এ রূপান্তর করে। SWE-bench-এর harness যেমন repository checkout করে, agent চালায়, patch apply করে, test চালিয়ে score দেয়।
- **Scaffold:** model-এর চারপাশের agent-logic (planner, retry loop, memory, tool-calling loop)। লেখক দেখান scaffold-এর development-ও একধরনের "training" — বারবার একই evaluation set-এ tune করলে set-টা scaffold-এর training data হয়ে যায় (Chapter 2-এর "iteration holdout")।

**উদাহরণ:** Paper 02-এর SWE-agent আসলে একটা scaffold (ACI); Paper 04-এর Agentless আরেকটা scaffold। একই model দুই scaffold-এ ভিন্ন score পায় — এটাই "system around the model"।

### ২.২ Multivocal Literature Review ও Grey Literature
- **Systematic Literature Review (SLR):** নির্দিষ্ট search string, database, inclusion/exclusion criteria দিয়ে শুধু peer-reviewed paper নিয়ে review।
- **Grey literature:** যা প্রচলিত academic venue-তে প্রকাশিত নয় — company engineering blog, incident report, podcast, newsletter, Reddit post, product documentation।
- **Multivocal Literature Review (MLR):** scholarly + grey literature দুটোই একসাথে review করা (Garousi, Felderer ও Mäntylä 2019-এর SE guideline)। কারণ: production incident ও operational mechanism অনেক সময় শুধু blog-এ লেখা থাকে।
- এই monograph Kitchenham et al. (2022)-এর সতর্কতাও মেনেছে: পরিবর্তনশীল social-media post-কে "primary study" ধরা হয়নি; practitioner record সাধারণত শুধু **corroborating** (সমর্থনকারী) হিসেবে গণ্য।
- **Independence key:** একই incident নিয়ে দশটা blog লিখলে সেটা দশটা আলাদা প্রমাণ নয় — একটা key দিয়ে group করে একবারই গোনা হয়।

### ২.৩ Evidence Grading (প্রমাণের মান নির্ধারণ)
এই monograph প্রতিটা **নির্দিষ্ট দাবি (scoped claim)**-কে চার ভাগে রেখেছে — পুরো paper বা venue-কে নয়:

| Group | সংজ্ঞা (লেখকের) | সহজ উদাহরণ |
|---|---|---|
| **Strong** | দাবির উপর সরাসরি controlled comparison, validated benchmark result, বা সমান নির্দিষ্ট measurement | 60,000 trajectory-র variance study |
| **Directional** | mechanism, threat model বা effect-এর দিক সমর্থন করে, কিন্তু পুরো recommendation, magnitude বা transfer প্রমাণ করে না | Distributed-systems paper থেকে agent-এ ধার করা mechanism |
| **Corroborating** | case report, practitioner account — সম্ভাব্যতা দেখায়, কত ঘন ঘন হয় (prevalence) তা নয় | "Agent 9 সেকেন্ডে production database মুছে দিলো" blog |
| **Null or conflicting** | প্রত্যাশিত effect পাওয়া যায়নি বা অন্য দাবিকে সীমিত করে | Context file A/B test-এ উল্টো ফল |

নিয়ম: কয়েকটা directional source একমত হলেও composite recommendation "strong" হয় না; সন্দেহ হলে নিচের grade।

### ২.৪ Run-to-Run Variance ও Nondeterminism
- একই agent, একই task, একই configuration — আবার চালালে ভিন্ন ফল। কারণ: sampling, infrastructure nondeterminism (GPU floating-point, batching), tool timing, network।
- **Temperature 0 মানেই deterministic নয়:** Bjarnason et al. (2026) 60,000 SWE-bench Verified trajectory-তে দেখিয়েছেন temperature 0-তেও standard deviation 1.5 percentage point-এর বেশি; trajectory প্রথম কয়েক শতাংশ token-এর মধ্যেই আলাদা হয়ে যায়।
- লেখকের মূল বাক্য: **"One run is one draw"** — একটা run মানে একটা random draw।

### ২.৫ Statistical Power, Minimum Detectable Effect, Paired Design
- **Power:** সত্যিই একটা নির্দিষ্ট পার্থক্য থাকলে experiment সেটা ধরতে পারবে — তার সম্ভাবনা।
- **Minimum Detectable Effect (MDE):** নির্দিষ্ট sample size, variance আর error rate-এ experiment সবচেয়ে ছোট যে পার্থক্য নির্ভরযোগ্যভাবে ধরতে পারে।
- **Paired design:** দুটো system একই item-এ চালিয়ে item-by-item পার্থক্য দেখা। সহজ task-এ দুজনেই পাস, কঠিনে দুজনেই ফেল — এই "shared difficulty" বিয়োগ করলে noise কমে।
- **McNemar's test:** pass/fail ধরনের paired data-র জন্য — শুধু discordant pair (একজন পাস, অন্যজন ফেল) দেখে।
- **Bootstrap:** data থেকে বারবার resample করে uncertainty বের করা; paired-এ পুরো pair একসাথে resample করতে হয়।
- **Welch's t-test:** দুই group-এর variance সমান না ধরে t-test।
- **Retrospective power:** ফল দেখার পরে power হিসাব — লেখকের মতে circular, অর্থহীন।

### ২.৬ pass@1, pass@k, pass^k
| Metric | প্রশ্ন | কখন উপযুক্ত |
|---|---|---|
| **pass@1** | একবারের চেষ্টায় কত task solve হয়? | একটাই সুযোগ |
| **pass@k** | k বার চেষ্টা করলে **অন্তত একবার** সফল হওয়ার সম্ভাবনা | মানুষ বা selector অনেকগুলো থেকে বাছাই করতে পারে |
| **pass^k** | k বার চেষ্টা করলে **প্রতিবার** সফল হওয়ার সম্ভাবনা | Unsupervised কাজ — একবার fail মানেই সমস্যা |

pass^k ধারণাটা tau-bench (Yao et al. 2024) থেকে; monograph-এর মূল বার্তা: **একই k trial দুটো ভিন্ন operational প্রশ্নের উত্তর দেয়; deployment-এর failure semantics অনুযায়ী metric বাছাই করতে হবে।** (সূত্র Section ৬-এ)

### ২.৭ Contamination, Solution Leakage, Weak Oracle, Construct Validity
- **Contamination:** evaluation material model আগেই training-এ দেখেছে।
- **Solution leakage:** task-এর issue text বা comment-এই উত্তর লেখা আছে (run-এর সময় model দেখতে পায়)।
- **Weak oracle:** test এত দুর্বল যে ভুল patch-ও পাস করে। লেখকের গুরুত্বপূর্ণ পর্যবেক্ষণ: তিনটার মধ্যে **শুধু weak oracle-ই ভুল patch-কে পাস করায়**; প্রথম দুটো সঠিক patch দেয় কিন্তু "স্বাধীন problem-solving" দাবিটা নষ্ট করে।
- **Temporal holdout:** model-এর training cutoff-এর পরে প্রকাশিত task দিয়েই শুধু evaluate করা।
- **Construct validity:** instrument আসলে যা মাপছে বলে দাবি করে তাই মাপছে কিনা (Bean et al. 2025, 445 benchmark-এর systematic review)।

### ২.৮ Execution-based Evaluation ও Sandbox
- **Execution-based evaluation:** patch পড়ে নয়, চালিয়ে (compile, test, build) সিদ্ধান্ত নেওয়া।
- **Sandbox:** আলাদা, সীমাবদ্ধ পরিবেশ (container/VM) — নির্দিষ্ট CPU, memory, সময়, network বন্ধ, প্রতিবার পরিষ্কার snapshot থেকে শুরু, শেষে ফেলে দেওয়া।
- লেখকের নিয়ম: **environment failure ≠ candidate failure।** Docker image pull না হলে patch-কে "ভুল" বললে evaluation দূষিত হয়; "পাস" বললে release দূষিত হয়। সঠিক ফল: **infrastructure error** (block করো, retry করো, কিন্তু credit বা blame দিও না)।

### ২.৯ LLM-as-a-Judge, Inter-rater Reliability, Cohen's Kappa
- **LLM-as-a-judge:** একটা model দিয়ে অন্য system-এর output grade করা।
- **Inter-rater reliability:** একাধিক মানুষ একই item-এ কতটা একই label দেয়।
- **Cohen's kappa (κ):** দুজন rater-এর agreement থেকে "শুধু chance-এ মিলে যাওয়া" অংশ বাদ দিয়ে মাপা। **Fleiss' kappa:** দুইয়ের বেশি rater।
- লেখকের মূল বাক্য: **"Agreement is a calibration result, not a correctness verdict"** — দুটো grader যারা সবকিছুকে PASS বলে, তাদের agreement 100% কিন্তু উপকারিতা শূন্য।

### ২.১০ Proxy Metric Gaming (Goodhart's law) ও Reward Hacking
- **Proxy:** আসল লক্ষ্য (সঠিক, নিরাপদ code) মাপা কঠিন বলে মাপা যায় এমন একটা signal (test pass rate) ব্যবহার করা।
- **Goodhart's law (সাধারণ ধারণা):** একটা measure-কে target বানালে সেটা আর ভালো measure থাকে না।
- **Reward hacking:** agent proxy বাড়ানোর shortcut খুঁজে নেয় (test-কে hard-code করা, exception চাপা দেওয়া)।
- Monograph Skalse et al. (2022)-এর theorem উল্লেখ করে: একটা নির্দিষ্ট linear setting-এ দুটো non-constant reward পরস্পরের "unhackable" হতে পারে না — অর্থাৎ নিখুঁত metric design দিয়ে এই সমস্যা থেকে সর্বজনীন মুক্তি নেই।

### ২.১১ Execution State, Durable Execution ও Distributed-Systems Concept
Monograph-এর Part III-তে লেখক "software factory"-কে একটা **distributed system** হিসেবে দেখেন। নিচের ধারণাগুলো সেখান থেকে:

| ধারণা | সহজ মানে | Agent-এ উদাহরণ |
|---|---|---|
| **Execution state** | একটা run চলাকালীন plan, progress, tool result, event — যা run-এর অবস্থা বোঝায় | 14 ধাপের কাজের 9 নম্বর ধাপে আছে |
| **Durable execution** | process মরে গেলেও state টিকে থাকে, recorded progress থেকে আবার শুরু করা যায় | Workflow engine (যেমন Temporal-ধরনের) step result লিখে রাখে |
| **Logical work বনাম attempt** | "bug-টা একবার fix করো" হলো logical work; প্রতিটা চেষ্টা একটা attempt | Retry মানে নতুন attempt, নতুন কাজ নয় |
| **Retry ও at-least-once delivery** | completion record না পেলে runtime আবার পাঠায় — তাই একটা step একাধিকবার চলতে পারে | Merge request পাঠিয়ে worker মারা গেলে আবার merge request |
| **Idempotency** | একই operation একাধিকবার করলে ফল একবার করার মতোই থাকে | Idempotency key দিয়ে দ্বিতীয় PR তৈরি আটকানো |
| **Exactly-once (সীমিত অর্থে)** | runtime-এর ভেতরে result একবার record হয়; কিন্তু বাইরের effect-এর জন্য boundary-তে আলাদা contract লাগে | লেখক: "Execution is at least once" |
| **Lease / heartbeat** | কে এখন কাজটা করছে, সে বেঁচে আছে কিনা — allocation প্রশ্ন | Lease শেষ হলেও পুরনো worker চলতে পারে |
| **Fencing / ownership epoch** | প্রতিবার authority বদলালে generation number বাড়ে; পুরনো generation-এর write boundary-তে বাতিল | Google Chubby-র sequencer (Burrows 2006) |
| **Failure domain / failure isolation** | যেসব resource একসাথে নষ্ট হতে পারে; isolation মানে recovery path-কে আলাদা domain-এ রাখা | একই credential দিয়ে production DB ও backup মুছে যাওয়া |
| **Reconciliation** | internal record বিশ্বাস না করে বাইরের আসল state পড়ে সিদ্ধান্ত নেওয়া | PR খোলা হয়েছিল কিনা code host-এ দেখা |
| **Unknown state** | effect হয়েছে কিনা নিরাপদে বলা যায় না — তখন অনুমান না করে মানুষের কাছে escalate | "Guessing in either direction is unsafe" |
| **Backpressure, jitter, admission control** | load বেশি হলে নতুন কাজ সীমিত করা; retry-গুলো একসাথে না পাঠিয়ে random delay | Retry storm ঠেকানো (Chapter 19) |

### ২.১২ Permissions, Sandboxing ও Prompt Injection
- **Least privilege:** কাজের জন্য যতটুকু দরকার শুধু ততটুকু অনুমতি, শুধু ততক্ষণ। লেখকের default: **ordinary identity read-only**; write-এর জন্য নির্দিষ্ট, সীমিত, মেয়াদি escalation।
- **Blast radius:** একটা ভুল বা compromise নতুন authorization ছাড়াই যতদূর পৌঁছাতে পারে। লেখকের মূল বাক্য: **"Authority, not instruction, defines blast radius"** — prompt-এ "delete করো না" লিখলে ক্ষমতা কমে না।
- **Indirect prompt injection:** agent যে data পড়ে (web page, issue, log) তার ভেতরে লুকানো নির্দেশ। Greshake et al. (2023), AgentDojo (Debenedetti et al. 2024)।

### ২.১৩ Observability, Telemetry ও Trace
- **Observability:** system-এর ভেতরে কী হচ্ছে তা বাইরে থেকে বোঝার ক্ষমতা; **telemetry** হলো সেই data (log, metric, trace)।
- **Transcript বনাম typed event stream:** transcript শুধু কথোপকথন; typed event stream প্রতিটা event-কে type দেয় — `tool_call_dispatched`, `tool_result_persisted` ইত্যাদি — যাতে বোঝা যায় কোন effect সত্যিই হয়েছে।
- **OpenTelemetry GenAI semantic conventions:** trace-এর একটা shared vocabulary (লেখক বলেন এটা portability-তে সাহায্য করে কিনা পরীক্ষিত নয়)।
- **Replay:** recorded event থেকে run আবার গঠন করা, শুধু পরিবর্তিত step থেকে নতুন করে চালানো।
- **Fault injection:** ইচ্ছা করে worker kill করে দেখা recovery দাবি অনুযায়ী কাজ করে কিনা।

### ২.১৪ Retrieval ও Memory (Agent-এর জন্য)
- **Repository retrieval:** বড় codebase থেকে প্রাসঙ্গিক file/symbol খুঁজে context-এ দেওয়া (SWE-bench-এর BM25 এর একটা সরল রূপ)।
- **Precision@k / Recall@k:** প্রথম k ফলাফলের কত অংশ প্রাসঙ্গিক / প্রয়োজনীয় item-এর কত অংশ প্রথম k-তে এসেছে।
- **Reciprocal-rank fusion (RRF):** BM25 ও embedding-এর মতো ভিন্ন channel-এর ranked list rank দিয়ে মেলানো (score scale আলাদা হলেও কাজ করে)।
- **Localization funnel:** repository → file → symbol → edit location — ধাপে ধাপে সংকুচিত করা (Agentless-এর hierarchical localization-এর মতো)।
- **Freshness / staleness:** retrieved evidence যে repository revision থেকে এসেছে, agent যে revision edit করছে তা একই কিনা।
- **Agent memory:** session-এর বাইরে টিকে থাকা তথ্য। **Compaction:** বড় history-কে ছোট summary-তে বদলানো — source না রাখলে lossy।
- **Advertised বনাম effective context length:** model 128K token নিতে পারে বলে মানেই 128K-তে ভালো কাজ করে না।

### ২.১৫ Human Review, Overreliance, Provenance, Effective Gate
- **Overreliance:** মানুষ ভুল AI output গ্রহণ করে। Vasconcelos et al. (2023): verification সস্তা হলে overreliance কমে।
- **Provenance:** একটা artifact কোথা থেকে, কে, কোন version থেকে বানিয়েছে তার রেকর্ড।
- **Effective gate বনাম compliance theater:** একটা approval gate তখনই কার্যকর যখন reject করলে আসলেই execution বদলায়; না হলে সেটা শুধু "assent" রেকর্ড করে।

### ২.১৬ Agent Skills
- সাধারণভাবে, **agent skill** হলো একটা packaged নির্দেশনা-সেট (প্রায়ই একটা instruction file + script/checklist) যা একটা coding agent নির্দিষ্ট ধরনের কাজের সময় load করে অনুসরণ করে — অনেকটা "reusable SOP"।
- এই monograph পাঁচটা skill প্যাকেজ করেছে: **evaluation design, end-to-end test design, failure-mode capture, focused execution, verified long-running implementation** — প্রতিটার সাথে practice-level evidence map। লেখক স্পষ্ট বলেছেন এগুলো **implementation artifact, নতুন evidence নয়**।

### ২.১৭ Flaky Test ও Verifier Health
- **Flaky test:** code না বদলালেও কখনো পাস, কখনো ফেল।
- লেখক verification-এ দুটো আলাদা failure domain দেখান: **(ক) verifier infrastructure health** — verifier আদৌ ঠিক artifact-এ চলেছে কিনা; **(খ) oracle adequacy** — চললেও ভুল ধরতে পারে কিনা।

### ২.১৮ Pareto Frontier (Cost–Accuracy)
একটা configuration অন্যটাকে **dominate** করে যদি accuracy কমপক্ষে সমান আর cost বেশি নয়, এবং অন্তত একটায় কঠোরভাবে ভালো। যারা dominated নয় তাদের নিয়ে Pareto frontier। (সূত্র Section ৬-এ)

---

## ৩. Problem Statement — কী সমস্যা ছিল?

### ৩.১ মূল সমস্যা
1. **Model হিসেবে মাপা, system হিসেবে চালানো:** leaderboard-এ এক সারিতে একটা score থাকে, কিন্তু সেই score-এর পেছনের execution history (কতবার চালানো, কোন harness, কোন permission) হারিয়ে যায়।
2. **ভুল জায়গায় দোষ:** লেখকের দাবি — অনেক "model failure" আসলে অন্য layer থেকে আসে: দুর্বল test, stale retrieval, flaky verifier, worker মরে গিয়ে duplicate PR।
3. **একটা layer-এ উন্নতি end-to-end-এ পৌঁছায় না:** লেখকের নিজের benchmark-এ retrieval precision@10 তিনগুণের বেশি বেড়েছে, কিন্তু end-to-end reward বেড়েছে মাত্র +0.0349।
4. **Statistical দুর্বলতা:** একটা run থেকে সিদ্ধান্ত, paired design নেই, power analysis নেই।
5. **Benchmark নিজেই অবিশ্বস্ত:** SWE-bench Verified-এর audit-এ 138টা task-এর 59.4%-এ flawed test; SWE-Bench Pro-র প্রায় 30% task broken।
6. **Agent-এর self-report বিশ্বাসযোগ্য নয়:** একটা model প্রতিটা trial-এ "done" বলেছে কিন্তু external oracle-এ মাত্র 44% resolved।
7. **Evidence অসম:** operational দিক থেকে সবচেয়ে জরুরি practice (যেমন blast radius containment)-এর পেছনে controlled study প্রায় নেই।

### ৩.২ কেন এটা গুরুত্বপূর্ণ?
Agent এখন production-এ PR খোলে, database migration করে, deploy করে। তখন প্রশ্ন শুধু "কত % task solve হলো" নয় — "এই নির্দিষ্ট পরিবর্তনটা কি বিশ্বাসযোগ্য, আবার চালালে একই হবে কি, ব্যর্থ হলে কি নিরাপদে ফেরা যাবে?" লেখক বলেন: **"Downstream confidence cannot repair evidence lost upstream."**

---

## ৪. Goal ও Research Questions

**Goal:** coding-agent system-কে নির্ভরযোগ্যভাবে **evaluate** ও **operate** করার জন্য একটা system-level, evidence-graded, runnable methodology দেওয়া — যা model পরিবর্তন হলেও টিকে থাকবে।

Monograph-এ RQ আকারে লেখা নেই; পড়ে আমি এই implicit প্রশ্নগুলো পেয়েছি (**আমার পর্যবেক্ষণ**):
- **RQ1:** একটা published agent score কোন দাবি সমর্থন করে, আর সেই দাবি কোন শর্তের উপর নির্ভরশীল? (Part I)
- **RQ2:** Run-to-run variance-এর মধ্যে দুটো system-এর পার্থক্য বিশ্বাসযোগ্যভাবে কীভাবে মাপা যায়? (Chapter 1–2)
- **RQ3:** Test/grader-এর verdict কখন "সঠিকতা"-র প্রমাণ, কখন শুধু agreement বা proxy? (Part II)
- **RQ4:** Worker মরে গেলে, retry হলে, বা concurrent worker থাকলে কোন record ও contract reliability রক্ষা করে? (Part III)
- **RQ5:** কোন evidence agent-এর কাছে পৌঁছালো, তা current কিনা — এটা কীভাবে মাপা যায়? (Part IV)
- **RQ6:** Human review কোথায় বসালে আসলেই outcome বদলাতে পারে? (Part V)
- **RQ7:** Multi-agent topology ও model routing কখন একক agent-এর চেয়ে ভালো — কোন evidence দিয়ে promote করা উচিত? (Part VI, research agenda)

---

## ৫. Methodology — Review Protocol ও Framework কীভাবে বানানো হয়েছে

### ৫.১ Paper-এর ধরন বোঝা
এটা empirical paper-এর মতো "একটা experiment → একটা result" নয়। তিনটা স্তর একসাথে আছে:
1. **Structured multivocal review** — literature থেকে bounded claim বের করে grade করা।
2. **Engineering synthesis** — সেই claim থেকে practice ও framework (dependency chain, factory contracts) বানানো।
3. **Author-system case** — লেখকের নিজের চালানো system থেকে measurement ও failure case, যেগুলো **independent evidence হিসেবে গোনা হয়নি**।

### ৫.২ Source Assembly — Search Lane

| Lane | কী করা হয়েছে | সংখ্যা |
|---|---|---|
| **Base review** | সাতটা topic thread: benchmark validity, failure taxonomy, evaluation statistics, oversight & accountability, context & retrieval, durable execution, scheduling & repository scoping | 118 scholarly works |
| **Bounded update audit** | July 27 – August 5 (+ August 6-এর targeted check)-এর record screen | 39 screened → 11 admitted, 1 আগে থেকেই ছিল, 27 deferred/excluded |
| **SE coverage probe** | OpenAlex metadata দিয়ে 8টা topic × ICSE, FSE, ASE, ISSTA, EMSE, TSE, TOSEM, CSCW | 148 unique candidate → 9 methodologically material work admitted (যেমন SEGRESS guideline, ABC framework, construct validity) |
| **Distributed-systems synthesis** | citation-driven targeted selection (distributed systems, cluster scheduling, build systems + 3টা agent preprint) | 21 scholarly + 7 practitioner |
| **অন্যান্য targeted** | repository-scale framing-এর জন্য 1 scholarly + 1 practitioner; cutoff-এর পরের 1টা factory case; inference serving-এর 4টা systems paper | — |
| **Benchmark collection** | দুটো inventory merge, identity দিয়ে deduplicate, JSON Schema দিয়ে validate | 29 benchmark record (3টা repeated record বাদ) |
| **মোট** | — | **164 scholarly, 100 practitioner, 29 benchmark, 17 author-system case** |

**আমার হিসাব (scholarly যোগফল যাচাই):** 118 + 11 + 9 + 21 + 1 + 4 = 164 ✓। (practitioner-এর 100-এর পুরো ভাঙন main text-এ নেই।)

**Search instrument:**
- **Scholarly:** SciX (NASA-supported, Smithsonian Astrophysical Observatory পরিচালিত) + লেখকের local layer "SciX Agent" — 32.4 million record-এর SciX/arXiv corpus, 299.3 million citation link, 14.9 million record-এর full text; INDUS dense retrieval + BM25 lexical retrieval, reciprocal-rank fusion দিয়ে মেলানো।
- **Practitioner:** লেখক-পরিচালিত "Code Intelligence Digest" — July 26 cutoff-এ 162,350 normalized record, 149 source label, 43,953 record-এ full text।
- **গুরুত্বপূর্ণ নিয়ম:** এই retrieval tool-গুলো শুধু কোনটা আগে পড়া হবে তা ঠিক করেছে; **evidence grade দেয়নি**। Retrieval rank screening-এর ক্রম ঠিক করেছে, screening-এর পরে কোনো বাড়তি গুরুত্ব পায়নি।

**যা execute করা হয়নি (লেখক নিজেই disclose করেছেন):**

| Provider | অবস্থা | কারণ |
|---|---|---|
| ACM Digital Library | Not performed | Automated client-এ HTTP 403; policy automated agent নিষেধ করে |
| IEEE Xplore | Not performed | Credential "provider-inactive" response |
| Scopus | Not performed | API key ও institutional token নেই |
| DBLP title census (বিকল্প) | Performed | 8 topic × 8 venue stream (2018–2026) = 64 cell → 55 unique publication, যার 50টা আগের reference set ও OpenAlex probe-এ ছিল না; 34টা retained candidate August 6-এর পরে পাওয়া, পরের edition-এ deferred |
| 40-DOI SciX sample | Performed | 40টার মধ্যে মাত্র 8টা exact DOI match (সবগুলো TSE); TSE-এর 26টা candidate-ই SciX-এ ছিল, অন্য venue-র 32টা ছিল না |

লেখকের সতর্কতা: এই probe দিয়ে corpus recall estimate করা যায় না; search **structured, not exhaustive**।

### ৫.৩ Curation Workflow (নির্দিষ্ট ক্রম)
1. প্রতিটা thread-এর প্রশ্ন নির্ধারণ
2. Candidate retrieve
3. Record identity resolve
4. In-scope claim আছে কিনা screen
5. Bounded claim ও তার শর্ত extract
6. Evidence group assign
7. Assignment-কে challenge
8. Candidate practice derive
9. Chapter-এর জন্য practice select
10. শেষে citation audit

**Automation বনাম মানুষ (Table 1-এর সারাংশ):**

| ধাপ | Mode | মানুষের সিদ্ধান্ত |
|---|---|---|
| Retrieval ও ranking | Automated + assisted | Thread-এর প্রশ্ন ও search boundary লেখক ঠিক করেছেন, admitted source নিজে পড়েছেন |
| Identity resolution, duplicate check | Automated check + human resolution | Ambiguous identity ও independence key লেখক ঠিক করেছেন |
| Bounded-claim extraction | Assisted | Source মিলিয়ে claim সংশোধন |
| প্রাথমিক evidence-group প্রস্তাব | Assisted | চূড়ান্ত label লেখকের |
| Challenge pass | Assisted | Automated pass composite claim, contrary finding, duplicate support flag করেছে; লেখক আবার পড়ে সিদ্ধান্ত নিয়েছেন |
| Practice admission, chapter selection, prose | Human | লেখক |
| Schema, checksum, identifier gate | Automated verification | Fail করলে release block |

### ৫.৪ Inclusion ও Evidence Grading
- **Inclusion:** source-এ অন্তত একটা measured result, reproducible mechanism, operational incident, benchmark property বা concrete practice থাকতে হবে।
- **Exclusion:** identity unresolved, কোনো claim নেই, scope-এর কোনো সিদ্ধান্তের সাথে সম্পর্ক নেই, বা ভালো source-এর সম্পূর্ণ duplicate।
- **Source inclusion ও practice admission আলাদা সিদ্ধান্ত** — একটা source থাকতে পারে কিন্তু তার প্রস্তাবিত practice বাতিল হতে পারে।
- **Grading audit:** যে 10টা practice-এর একমাত্র supporting synthesis "strong" ছিল + 2টা restored item পরীক্ষা করা হয়েছে → **6টা grade কমানো হয়েছে** (source আসলে hazard বা adjacent result দেখিয়েছিল, remedy নয়), **6টা রাখা হয়েছে**।
- **Inter-rater reliability নেই:** লেখক নিজেই বলেছেন এটা blinded multi-reviewer grading নয়। 20টা practice-এর deterministic random sample, label লুকিয়ে, Cohen's/Fleiss' kappa হিসাবের script সহ একটা packet release করা হয়েছে — কিন্তু **এই edition-এ কোনো external grader-এর ফল বা kappa value নেই**।

### ৫.৫ Practice Derivation ও Chapter Selection

| ধাপ | সংখ্যা |
|---|---|
| Candidate practice (ছয়টা extraction shard থেকে) | 244 |
| Admission gate পার হয়েছে | 214 (30 rejected) |
| Hardening (overlapping operation — যোগ-বিয়োগ করে মেলানো যায় না বলে লেখক সতর্ক করেছেন) | 26 removed, 13 demoted, 8 split, 3 added, 1 provenance repair-এর পর reinstated |
| চূড়ান্ত record | **206** = 193 gated practice + 13 research lead (ERCA-193 থেকে ERCA-205) |
| Main chapter-এ developed | **56** |
| Companion-এ compact entry | 137 gated + 13 lead = 150 |
| "Limited-support" চিহ্নিত companion entry | 29 |

**Admission gate:** একটা record পাস করে যদি অন্তত (ক) একটা scholarly item, বা (খ) resolvable scholarly identity-সহ একটা non-author synthesis, বা (গ) আলাদা independence key-সহ দুটো practitioner item থাকে।

**Developed set বাছাই:** তিনটা আলাদা ranking — (১) একটা bounded case দিয়ে শেখানো যায় কিনা, (২) engineering সিদ্ধান্তে কতটা প্রভাব ফেলে, (৩) 14টা mechanism cluster-এর coverage। অন্তত দুটো ranking-এ এলে developed set-এর base।

**গুরুত্বপূর্ণ সংখ্যা:** consequence ranking-এ 52টা practice-এর উপর urgency rank আর "অন্তত একটা strong evidence আছে কিনা"-এর Spearman correlation = **−0.004** → evidence strength আর operational urgency প্রায় সম্পর্কহীন। লেখক তাই স্পষ্ট বলেন chapter set একটা **"authorial engineering judgment, not an evidence-derived consensus"**।

### ৫.৬ Author-System Case-এর Treatment
- লেখকের নিজের system (CodeProbe, CodeScaleBench, memory system, trace-diagnostics corpus, fleet ledger ইত্যাদি) থেকে পাওয়া ফল সবসময় **illustration বা local measurement** — independent external evidence হিসেবে গোনা হয়নি, একা কোনো general recommendation সমর্থন করে না।
- প্রতিটা chapter-এর শেষে "Sources and evidence" অংশে এগুলো "Not an evidence item" লেবেলে আলাদা।

### ৫.৭ Framework Construction

#### ৫.৭.১ Reliability Dependency Chain (ছয় স্তর)

| ক্রম | Layer | Part | এই layer যা দেয় (output) | এই layer ভাঙলে নিচে কী হয় |
|---|---|---|---|---|
| 1 | Measurement | I (Ch 1–3) | credible comparison | দুর্বল measurement → আত্মবিশ্বাসী কিন্তু ভুল grade |
| 2 | Grading | II (Ch 4–6) | defensible verdict | দুর্বল grade → unsafe কাজ গৃহীত |
| 3 | Containment ও recovery | III (Ch 7–11) | bounded, recoverable record | অসম্পূর্ণ recovery record → retrieval-এ "সম্পূর্ণ" হিসেবে ঢোকে |
| 4 | Retrieval ও context | IV (Ch 12–15) | current, usable evidence | context নেই → review অকার্যকর মনে হয় |
| 5 | Review ও accountability | V (Ch 16–17) | challengeable decision | invalid review signal → ভুল configuration-এ বেশি কাজ যায় |
| 6 | Allocation ও cost | VI (Ch 18–19) | measured commitment | future work আবার measurement layer-এ ফেরে |

**Repair asymmetry (লেখকের ভাষায়):** পরের machinery যোগ করা আগের instrument সারানোর চেয়ে সহজ, অথচ সেই machinery-কে আগের (ত্রুটিপূর্ণ) instrument দিয়েই মাপা হয়। উদাহরণ (Chapter 20):
- বেশি sample → production কাজ বাদ দেওয়া task distribution সারায় না।
- বেশি judge → expert-রা অসংগতভাবে প্রয়োগ করা rubric সারায় না।
- বেশি agent → empty result-কে authoritative ধরা retrieval boundary সারায় না।
- বেশি context → governing specification হারানো run সারায় না।
- ভালো scheduling → কোন attempt publish করতে পারবে তা চিনতে না পারা ledger সারায় না।
- বেশি observability → identity record না করা external effect সারায় না।

#### ৫.৭.২ Software Factory Model ও Identity (Chapter 7)

| Identity | মানে |
|---|---|
| `work_id` | স্থায়ী logical work — যে intent একবারই ঘটা উচিত |
| `input_state_id` | attempt যে repository/branch/revision দেখে plan ও execute করেছে |
| `ownership_epoch` | ঐ কাজের উপর write authority-র monotonic generation |
| `attempt_id` | একটা নির্দিষ্ট work ও epoch-এর অধীনে একটা execution attempt |
| `artifact_version` | attempt-এর তৈরি নির্দিষ্ট code বা state |
| `verification_id` | একটা verification execution — artifact, verifier version, environment, input সহ |
| `effect_id` | একটা logical বাহ্যিক mutation; boundary-তে idempotency key এর রূপ হতে পারে |

**ছয়টা contract family (I1–I11):**

| Family | Contract | সহজ মানে |
|---|---|---|
| Work continuity ও retry identity | I1, I4 | গৃহীত কাজ চুপচাপ হারাবে না; retry = একই work_id-এর নতুন attempt_id |
| Generation-scoped authority | I2, I3 | শুধু current epoch mutation commit করতে পারে; stale completion logical state এগোতে পারে না |
| External-effect safety | I5 | বাহ্যিক effect redelivery-তে নিরাপদ, নয়তো স্পষ্টভাবে "uncertain" |
| Record ও evidence consistency | I6, I7, I8 | বিরোধী record → reconciliation; evidence version-bound; verifier failure ≠ software failure |
| Visible liveness ও safe recovery | I9, I10 | admissible কাজ অদৃশ্যভাবে আটকে থাকবে না; recovery path-ও production code |
| Causal attribution | I11 | গুরুত্বপূর্ণ transition কার, কোন attempt, কোন state, কোন authority — সব attributable |

লেখকের মূল কথা: **"None of these contracts mention model quality."** Agent-এর "done" শুধু attempt-কে `outcome_ready` পর্যন্ত নিতে পারে; logical work complete করতে পারে শুধু independently observed evidence।

#### ৫.৭.৩ Chapter-এর গঠন (প্রতিটা chapter একই ছাঁচে)
1. **Evidence profile:** কতগুলো strong / directional / corroborating / null item, কোন ERCA record-এর বিপরীতে।
2. **Chapter claim:** এক বাক্যের দাবি (যেমন "One run is one draw")।
3. একটা concrete situation (প্রায়ই লেখকের নিজের ভুল measurement) → mechanism → evidence কী প্রমাণ করে ও করে না → boundary condition → runnable procedure।
4. **Sources and evidence:** প্রতিটা citation-এর evidence group ও claim।

#### ৫.৭.৪ Minimum Pass (Section 0.5) — ছয় ধাপ
1. একটা aggregate score-ভিত্তিক সিদ্ধান্ত আবার খোলো; সবচেয়ে সস্তা credible baseline ও candidate একই task version-এ, প্রথমে প্রতি item-এ 3 বার চালাও, per-item outcome রাখো।
2. Success, reliability, cost, latency, model, harness, prompt, permission, pricing snapshot আলাদা করে রেকর্ড করো।
3. সাধারণ identity দিয়ে একটা অনুমোদিত ও একটা নিষিদ্ধ action চালাও (primary বনাম recovery resource-এর boundary সহ)।
4. সাম্প্রতিক একটা completion claim repository/system state থেকে যাচাই করো, executable check আবার চালাও।
5. 20টা failed বা unverifiable run পড়ো, যেখানে সম্ভব first upstream failure label করো।
6. পরের promotion run-এর আগে success floor, cost ceiling, task ও baseline version, fault-containment guard লিখে রাখো।

### ৫.৮ কী Execute করা হয়েছে, কী হয়নি — এক নজরে

| বিষয় | অবস্থা |
|---|---|
| Base review, update audit, SE coverage probe, DBLP census | ✅ করা হয়েছে |
| ACM DL, IEEE Xplore, Scopus search | ❌ করা হয়নি (disclosed) |
| প্রতিটা interactive query-র byte-for-byte log | ❌ নেই — retained record ও reconstruction আলাদা করে রাখা |
| Evidence grading-এর external IRR | ❌ নেই — packet release করা, ফল নেই |
| Author-system measurement (CodeScaleBench, CodeProbe ইত্যাদি) | ✅ করা হয়েছে, কিন্তু illustration হিসেবে |
| Practice-গুলোর controlled effect পরীক্ষা | ❌ বেশিরভাগ practice-এর জন্য নয় — অনেক জায়গায় "local test চালাও" বলা |

### ৫.৯ এই Analysis-এর Coverage (আমি কী পড়েছি)

| অংশ | পড়ার গভীরতা |
|---|---|
| Abstract, পুরো Table of Contents, List of Figures/Tables | সম্পূর্ণ |
| Introduction (0.1–0.10): problem, dependency chain, পুরো method section, contributions, minimum pass, organization | সম্পূর্ণ |
| Chapter 1 (variance, power, paired comparison) | সম্পূর্ণ, sources সহ |
| Chapter 2 (baseline, ablation, cost) | প্রায় সম্পূর্ণ |
| Chapter 3 (contamination, oracle strength, workload validity) | সম্পূর্ণ, sources সহ |
| Chapter 4 (execution-based evaluation, pass^k release test) | সম্পূর্ণ, sources সহ |
| Chapter 5 (grader calibration, kappa) | 5.1–5.3 গভীরভাবে; 5.4–5.5 skim |
| Chapter 6 (proxy gaming, verifier health) | 6.1, 6.3, 6.4, 6.5 গভীরভাবে; 6.2 আংশিক |
| Chapter 7 (software factory, contracts) | প্রায় সম্পূর্ণ |
| Chapter 8 (isolation, injection, independent verification) | 8.1–8.3 গভীরভাবে; 8.4 skim |
| Chapter 9 (durable state, idempotency) | 9.1 শুরু, 9.3, 9.5 গভীরভাবে; 9.2, 9.4 skim |
| Chapter 10 (trace, fault injection) | 10.1–10.2, 10.4–10.6 গভীরভাবে; 10.3, 10.7–10.9 skim |
| Chapter 11 (failure taxonomy) | 11.1 গভীরভাবে; বাকি skim |
| Chapter 12 (retrieval measurement) | 12.0–12.2 গভীরভাবে; 12.3–12.5 skim |
| Chapter 13 (localization, freshness) | opening, 13.1 শুরু, 13.3-এর freshness experiment গভীরভাবে |
| Chapter 14–15 (context budget, memory) | opening ও প্রথম section; বাকি skim |
| Chapter 16–17 (human review, accountability) | opening পড়া; বাকি skim |
| Chapter 18–19 (topology, scheduling — research agenda) | opening ও প্রথম section; বাকি skim |
| Chapter 20 (evidence chain, Table 20.1) | সম্পূর্ণ |
| Appendix A (206 record-এর catalog) | Script দিয়ে parse করে গোনা (206 = 56 developed + 137 companion + 13 lead; 29 limited-support) ও সব developed record-এর নাম দেখা; প্রতিটা entry-র বিস্তারিত companion-এ, PDF-এ নেই |
| Glossary, Data and materials availability | সম্পূর্ণ |
| References (249টা) | শুধু প্রয়োজনমতো দেখা |

---

## ৬. Mathematical Formulation — সূত্র ও ব্যাখ্যা

Monograph-এ কিছু সূত্র সরাসরি আছে (paired difference, kappa, inflation gap, eligibility, RRF, retry probability), আর কিছু শুধু কথায় বলা। নিচে প্রতিটা সূত্রের পাশে লেখা আছে সেটা **paper-এর** নাকি **আমার যোগ করা standard সূত্র/হিসাব**।

### ৬.১ একটা Run = একটা Random Draw (Repeated-run Statistics)
ধরি একটা configuration-কে $R$ বার চালানো হলো, $r$-তম run-এর score $S_r$:
$$
\bar{S} = \frac{1}{R}\sum_{r=1}^{R} S_r, \qquad s = \sqrt{\frac{1}{R-1}\sum_{r=1}^{R}\left(S_r - \bar{S}\right)^2}, \qquad \text{SEM} = \frac{s}{\sqrt{R}}
$$
| Symbol | মানে |
|---|---|
| $R$ | কতবার একই configuration চালানো হলো |
| $S_r$ | $r$-তম run-এর aggregate score (যেমন % resolved) |
| $\bar{S}$ | গড় score |
| $s$ | run-গুলোর মধ্যে standard deviation (spread) |
| SEM | গড়ের standard error — $R$ বাড়লে কমে |

(এগুলো standard সূত্র; monograph বলে "report every run-level score, along with the mean and standard deviation"।)

**Paper-এর সংখ্যা:** 60,000 SWE-bench Verified trajectory-তে single-run pass@1-এর spread 2.2 থেকে 6.0 percentage point; temperature 0-তেও SD > 1.5 pp।

**আমার হিসাব (intuition):** SD = 1.5 pp হলে, দুটো আলাদা single run-এর পার্থক্যের SD হবে প্রায় $\sqrt{2}\times 1.5 \approx 2.1$ pp (দুটো run independent ধরে)। তাই একই system-কে দুবার চালালেই 2 pp "উন্নতি" দেখা যাওয়া খুবই স্বাভাবিক — যে কারণে লেখক বলেন 2–3 pp-এর দাবি এই variance envelope-এর ভেতরে পড়ে।

### ৬.২ Paired Difference (Chapter 1 — paper-এর সূত্র)
Item $i$-এ system A ও B-এর score $x_i$, $y_i$:
$$
d_i = x_i - y_i, \qquad \bar{d} = \frac{1}{n}\sum_{i=1}^{n} d_i, \qquad SE(\bar{d}) = \frac{s_d}{\sqrt{n}}
$$
$$
\text{Var}(\bar{d}) = \frac{s_x^2 + s_y^2 - 2\,\text{Cov}(x, y)}{n}
$$
| Symbol | মানে |
|---|---|
| $d_i$ | item $i$-এ দুই system-এর score-এর পার্থক্য |
| $\bar{d}$ | গড় পার্থক্য |
| $s_d$ | $d_i$-গুলোর standard deviation |
| $s_x^2,\, s_y^2$ | দুই system-এর item-level variance |
| $\text{Cov}(x,y)$ | দুই system-এর item score একসাথে কতটা ওঠানামা করে |

**Intuition:** সহজ task-এ দুজনেই পাস, কঠিনে দুজনেই ফেল → Cov ধনাত্মক → $-2\,\text{Cov}$ পদটা variance কমায়। Independent analysis এই পদ বাদ দেয়, ফলে "সহজ বনাম কঠিন" variation দুবার গোনে — uncertainty অকারণে বড় দেখায়।

Paired t statistic:
$$
t = \frac{\bar{d}}{SE(\bar{d})}, \qquad \text{df} = n - 1
$$

**Worked example (paper-এর CodeProbe rerun):** প্রথম single run-এ পার্থক্য +0.054 (একটা task-এ +0.300)। প্রতি configuration 3 বার চালানোর পর: $\bar{d} = +0.0035$, 95% CI = [−0.0005, +0.0074], $n = 5$ task (paired unit), df = 4, $t = 2.41$, critical value 2.776 → **significant নয়**। যে task-এ +0.300 দেখা গিয়েছিল, সেখানে দুটো configuration-ই প্রতিবার 0.800 পেয়েছে — পার্থক্য 0.000।

**আমার হিসাব (সংখ্যাগুলো পরস্পর সংগত কিনা যাচাই):**
- CI-এর মাঝখান = $(-0.0005 + 0.0074)/2 = 0.00345 \approx 0.0035$ ✓
- CI-এর অর্ধেক প্রস্থ = $(0.0074 - (-0.0005))/2 = 0.00395$
- $SE = 0.00395 / 2.776 \approx 0.00142$
- $t = 0.0035 / 0.00142 \approx 2.46$ — paper-এর 2.41-এর খুব কাছে (পার্থক্যটা rounding-এর কারণে বলে মনে হয়)।

### ৬.৩ Statistical Power ও Minimum Detectable Effect (MDE)
Monograph power-এর ধারণা কথায় দিয়েছে; normal approximation-এ standard সূত্রটা (**আমার যোগ করা**):
$$
\text{MDE} \approx \left(z_{1-\alpha/2} + z_{1-\beta}\right) \cdot SE
$$
| Symbol | মানে |
|---|---|
| $\alpha$ | false-positive rate (যেমন 0.05) → $z_{0.975} = 1.96$ |
| $1-\beta$ | power (যেমন 0.80) → $z_{0.80} = 0.84$ |
| $SE$ | পার্থক্যের standard error |

**আমার হিসাব (worked example):** ধরি SWE-bench Lite-এর 300 task, দুটো system-এর resolve rate প্রায় 0.30, আর ধরে নিই তারা independent (paired correlation বাদ):
- একটা proportion-এর $SE = \sqrt{0.30 \times 0.70 / 300} \approx 0.0265$
- পার্থক্যের $SE \approx \sqrt{2} \times 0.0265 \approx 0.0374$
- $\text{MDE} \approx (1.96 + 0.84) \times 0.0374 \approx 0.105$ → **প্রায় 10.5 percentage point**

অর্থাৎ একবার-একবার চালিয়ে 300 task-এ 3–4 pp পার্থক্য নির্ভরযোগ্যভাবে আলাদা করা যায় না। Paired design (positive covariance) আর repeated run এই MDE কমায় — monograph-এর মূল যুক্তি এটাই।

**Paper-এর সংখ্যা:** Miller (2024)-এর worked example-এ প্রতি প্রশ্নে বেশি response sample করে MDE **13.2% থেকে 7.5%**-এ নেমেছে; Colas et al. (2018) variance estimate-এর জন্য **অন্তত 20টা pilot run** সুপারিশ করেছেন; 10-এর কম run-এ bootstrap-এর আসল false-positive rate প্রায় 10% (nominal 5% হলেও)।

### ৬.৪ pass@k, pass^k ও Retry Probability
**Paper-এর সূত্র (Chapter 2, independence ধরে):** একবারে পাস হওয়ার সম্ভাবনা $p$ হলে দুটো independent চেষ্টায় অন্তত একবার পাস:
$$
P(\text{at least one pass in 2}) = 1 - (1-p)^2
$$
সাধারণভাবে (**আমার যোগ করা**, independence ধরে):
$$
\text{pass@}k = 1 - (1-p)^k, \qquad \text{pass}^k = p^k
$$
Repeated trial থেকে estimator — $n$ trial-এর মধ্যে $c$টা সফল (pass@k-এর estimator Chen et al. 2021-এর; pass^k-এর estimator tau-bench-এ ব্যবহৃত combinatorial রূপ — monograph এগুলো "appropriate combinatorial estimator" বলে উল্লেখ করেছে কিন্তু সূত্র দেয়নি):
$$
\hat{P}_{@k} = 1 - \frac{\binom{n-c}{k}}{\binom{n}{k}}, \qquad \hat{P}^{k} = \frac{\binom{c}{k}}{\binom{n}{k}}
$$
| Symbol | মানে |
|---|---|
| $n$ | একটা task-এ মোট trial |
| $c$ | সফল trial |
| $k$ | metric-এর k (release policy থেকে ঠিক হয়) |

**Worked example (আমার হিসাব):**
- একটা task-এ $n = 3$ trial, $c = 2$ সফল: pass@1 = 2/3 ≈ 0.667; pass@3 = 1 (কারণ অন্তত একটা সফল); pass^2 = $\binom{2}{2}/\binom{3}{2} = 1/3$; pass^3 = 0।
- $p = 0.3$ হলে: pass@2 = $1 - 0.7^2 = 0.51$ (architecture না বদলে শুধু আরেকবার চেষ্টাতেই 30% থেকে 51%) কিন্তু pass^2 = $0.09$।
- **আগের sub-domain-এর সাথে সংযোগ:** SWE-agent (Paper 02) Lite-এ 6 run-এর গড় 17.94% কিন্তু pass@6 = 32.67% — এই gap-ই দেখায় যে অনেক task "কখনো পারে, কখনো পারে না"; pass^6 নিশ্চয়ই 17.94%-এর চেয়ে অনেক কম হবে (সঠিক সংখ্যা ঐ paper-এ নেই)।

**Release gate-এ multiplicity (আমার formalization; লেখক কথায় বলেছেন "chance grows with both the set size and k"):** প্রতিটা verdict-এ evaluator noise-এর কারণে ভুল fail-এর সম্ভাবনা $\epsilon$, golden set-এ $N$টা case, প্রতিটা $k$ বার:
$$
P(\text{false block}) = 1 - (1-\epsilon)^{N k}
$$
**আমার হিসাব:** $\epsilon = 0.01$, $N = 10$, $k = 3$ → $1 - 0.99^{30} \approx 0.26$। অর্থাৎ নিখুঁত candidate-ও প্রায় 26% সময় strict all-pass gate-এ আটকে যাবে — তাই flaky verifier ঠিক না করে k বাড়ানো বিপজ্জনক।

### ৬.৫ Cohen's Kappa (Chapter 5 — paper-এর সূত্র ও উদাহরণ)
$$
\kappa = \frac{p_o - p_e}{1 - p_e}
$$
| Symbol | মানে |
|---|---|
| $p_o$ | observed agreement — কত শতাংশ item-এ দুজন একই label দিয়েছে |
| $p_e$ | expected agreement — শুধু দুজনের label frequency থেকে chance-এ যতটা মিলতো |

**Worked example (paper-এর):** 100 item; cell = 85 (দুজনেই PASS), 5, 5, 5 (দুজনেই FAIL)। প্রত্যেকে 90 PASS, 10 FAIL।
- $p_o = (85 + 5)/100 = 0.90$
- $p_e = 0.90 \times 0.90 + 0.10 \times 0.10 = 0.81 + 0.01 = 0.82$
- $\kappa = (0.90 - 0.82)/(1 - 0.82) = 0.08/0.18 \approx 0.44$ → শুধু **moderate**
- দুজনেই সবকিছু PASS দিলে $p_o = p_e = 1$ → $\kappa = 0/0$ → **undefined, perfect নয়**।

**Paper-এর অন্য সংখ্যা:** Cemri et al. (2025) ছয়জন annotator দিয়ে rubric বারবার ঠিক করে Cohen's kappa 0.88-এ পৌঁছানোর পরে automated annotator test করেছেন; Panthi ও Abdelfattah (2026)-এ পাঁচজন মানুষের Fleiss' kappa 0.83, একজন মানুষ + চারটা model-এর panel 0.79, প্রতিটা model বনাম মানুষ Cohen's kappa 0.77–0.87 (115-case validation set), তারপর 1,902টা contested case-এ পাঁচ-model majority vote।

### ৬.৬ Class-specific Error Rate ও Stratified Reweighting (Chapter 5)
Defect = positive class:
$$
\text{TPR} = \frac{TP}{TP + FN}, \qquad \text{FPR} = \frac{FP}{FP + TN}, \qquad \text{TNR} = 1 - \text{FPR}
$$
**Worked example (paper-এর):** validation set-এ 40 defect, 80 non-defect; grader 32টা defect flag করে → TPR = 32/40 = 80%; 12টা non-defect-ও flag করে → FPR = 12/80 = 15%, TNR = 85%। অর্থাৎ 8টা defect মিস, 12টা ভালো output অকারণে review-এ।

**"TPR at fixed FPR":** reviewer যদি সর্বোচ্চ 5% false alarm সহ্য করতে পারে, threshold এমনভাবে বাছাই করো যাতে FPR ≈ 5%, তারপর সেই threshold-এ TPR report করো।

**Stratified sample থেকে deployment-এর aggregate (আমার formalization):**
$$
\hat{R}_{\text{deploy}} = \sum_{s} \pi_s \, \hat{R}_s
$$
$\pi_s$ = deployment-এ stratum $s$-এর অনুপাত, $\hat{R}_s$ = সেই stratum-এ মাপা rate।

**Paper-এর উদাহরণ:** 1,000 item-এর stream-এ 950 routine, 30 borderline, 20 clear defect। Natural sample-এ 100টার মধ্যে মাত্র প্রায় 2টা defect → একটা মিস করলেই detection rate 50 percentage point বদলায়। Stratified sample (40, 40, 40) এই সমস্যা কমায়, কিন্তু aggregate-এর জন্য $\pi = (0.95, 0.03, 0.02)$ দিয়ে reweight করতে হবে।

### ৬.৭ McNemar's Test (Chapter 1 ও 13)
Paired binary outcome-এ $b$ = A পাস/B ফেল, $c$ = A ফেল/B পাস:
$$
\chi^2 = \frac{(b - c)^2}{b + c}, \qquad p_{\text{exact}} = 2\sum_{i=0}^{\min(b,c)}\binom{b+c}{i}\,0.5^{\,b+c}
$$
**Worked example (paper-এর data, p-value আমি নিজে হিসাব করে মিলিয়েছি):** Weng et al. (2026) — 17টা উদাহরণে helper function-এর signature বদলানো। Stale-only retrieval-এ Qwen2.5-Coder-7B-Instruct 15টা incompatible output দিয়েছে, current-only retrieval-এ 0টা। তাহলে $b = 15$, $c = 0$:
$$
p_{\text{exact}} = 2 \times 0.5^{15} = 2/32768 \approx 6.1 \times 10^{-5}
$$
gpt-4.1-mini-তে $b = 13$, $c = 0$: $p = 2 \times 0.5^{13} \approx 2.44 \times 10^{-4}$। দুটোই paper-এর রিপোর্ট করা মান (6.1 × 10⁻⁵ ও 2.4 × 10⁻⁴)-এর সাথে মেলে ✓। (Paper-এর ব্যাখ্যা: এটা curated sample-এর ভেতরে পার্থক্য প্রমাণ করে, অন্য repository-তে effect size নয়।)

### ৬.৮ Contamination: Inflation Gap ও Temporal Eligibility (Chapter 3 — paper-এর সূত্র)
$$
G(m) = S(m,\, \text{public}) - S(m,\, \text{matched control})
$$
$$
\text{eligible}(t, m) = 1 \quad \text{যদি } T_{\text{pub}}(t) > T_{\text{cut}}(m)
$$
| Symbol | মানে |
|---|---|
| $G(m)$ | model $m$-এর inflation gap |
| $S(m, \cdot)$ | public suite ও matched private control-এ score |
| $T_{\text{pub}}(t)$ | task $t$-এর material প্রথম কখন public হয়েছে (benchmark-এ ঢোকার তারিখ নয়) |
| $T_{\text{cut}}(m)$ | model-এর ঘোষিত training cutoff |

**গুরুত্বপূর্ণ:** gap প্রতিটা model-এর জন্য আলাদা মাপতে হবে; একটা গড় "correction factor" সব model-এ বসানো ভুল (GSM1k-এ model-level gap আর verbatim reproduction-এর Spearman $\rho = 0.36$, $p = 0.03$)।

**Survival fraction (আমার formalization; লেখক বলেন "publish how many old passes survived"):**
$$
SF = \frac{N_{\text{still pass under stronger oracle}}}{N_{\text{old pass}}}
$$
**আমার হিসাব (paper-এর সংখ্যা দিয়ে):**
- SWE-Bench+ (একটা agent-model pair): resolve rate 12.47% → 3.97% → $SF \approx 3.97/12.47 \approx 0.318$, অর্থাৎ প্রায় 32% "success" টিকেছে।
- SWE-ABS: top score 78.80% → 62.20% → 16.6 pp কমেছে, আপেক্ষিক পতন $16.6/78.80 \approx 21.1\%$।
- SWE-bench Verified audit: 138টার 59.4% ≈ 82টা flawed task → $82/500 = 16.4\%$ পুরো subset-এর ✓ (paper-এর সংখ্যার সাথে মেলে)।

### ৬.৯ Retrieval Metrics ও Reciprocal-Rank Fusion (Chapter 12)
$$
\text{Precision@}k = \frac{\text{প্রথম } k \text{-তে প্রাসঙ্গিক item}}{k}, \qquad \text{Recall@}k = \frac{\text{প্রথম } k \text{-তে পাওয়া প্রয়োজনীয় item}}{\text{মোট প্রয়োজনীয় item}}
$$
$$
\text{RRF}(d) = \sum_{j=1}^{J} \frac{1}{c + r_j(d)}
$$
| Symbol | মানে |
|---|---|
| $J$ | retrieval channel সংখ্যা (যেমন BM25, embedding) |
| $r_j(d)$ | channel $j$-এ document $d$-এর rank (1 = প্রথম) |
| $c$ | fixed damping constant (paper মান বলেনি; literature-এ প্রায়ই 60 ব্যবহার হয় — **আমার নোট**) |

**আমার হিসাব (RRF উদাহরণ, $c = 60$):** file A BM25-এ rank 1, embedding-এ rank 10 → $1/61 + 1/70 \approx 0.0164 + 0.0143 = 0.0307$। file B দুটোতেই rank 4 → $2/64 = 0.0313$। দুই channel-এ ধারাবাহিকভাবে ভালো B সামান্য এগিয়ে — raw score যোগ না করে rank দিয়ে মেলানোর সুবিধা।

**Worked example (paper-এর CodeScaleBench সংখ্যা):** Precision@10: 0.095 → 0.313 (প্রায় 3.3 গুণ, **আমার হিসাব**); Recall@10: 0.120 → 0.272 (প্রায় 2.27 গুণ); অন্তত একটা প্রয়োজনীয় file পাওয়া task: 0.33 → 0.56। কিন্তু 370 paired task-এ end-to-end reward মাত্র **+0.0349** (bootstrap 95% CI [+0.0130, +0.0579])। লেখক নিজেই বলেছেন এই CI task-গুলোকে independent ধরেছে, অথচ task-গুলো 46টা anchor repository ও 20টা suite-এ grouped — তাই CI সম্ভবত uncertainty কম দেখাচ্ছে (cluster bootstrap লাগবে)।

### ৬.১০ Pareto Dominance (Chapter 2)
Configuration $a$ configuration $b$-কে dominate করে যদি:
$$
A_a \geq A_b \;\land\; C_a \leq C_b \;\land\; \left(A_a > A_b \lor C_a < C_b\right)
$$
$A$ = accuracy, $C$ = inference cost per task। লেখকের নিয়ম: score-per-dollar একটা ratio-তে নামিয়ে আনলে minimum accuracy-র নিচের সস্তা configuration-ও ভালো দেখাতে পারে — তাই দুটো axis আলাদা রেখে frontier আঁকো, তারপর constraint (minimum accuracy, cost ceiling) বসাও।

**আগের sub-domain-এর সাথে সংযোগ (আমার পর্যবেক্ষণ):** Sub-domain 1-এর Lite table-এ (Agentless paper-এর Table 1) Agentless (32.00%, 0.70 USD) AutoCodeRover (19.00%, 0.45 USD)-কে dominate করে না (cost বেশি), কিন্তু SWE-agent GPT-4 (18.00%, 2.51 USD)-কে dominate করে।

### ৬.১১ Dependency Chain ও Repair Asymmetry — একটা সরল Formal Model (আমার formalization)
লেখক এটা কথায় বলেছেন, সূত্রে নয়। Supervisor-কে বোঝানোর জন্য একটা সরল model:

ধরি layer $i$ ($i = 1, \ldots, 6$)-এর output "valid" হওয়ার সম্ভাবনা $v_i$, আর layer $j$-এর একটা conclusion valid হতে হলে তার আগের সব layer valid থাকতে হবে (সরলতার জন্য independent ধরে):
$$
V_j = \prod_{i=1}^{j} v_i
$$
**Repair asymmetry:** layer $j$-এ যত machinery যোগ করা হোক, তা শুধু $v_j$ (বা তার পরের) বাড়াতে পারে; $v_1, \ldots, v_{j-1}$ বদলায় না। তাই
$$
V_j \leq \min_{i \leq j} v_i
$$
**আমার হিসাব:** প্রতিটা layer-এ $v_i = 0.9$ হলে $V_6 = 0.9^6 \approx 0.53$। যদি measurement layer $v_1 = 0.6$ (যেমন single run, unpaired), তবে পরের পাঁচটা layer নিখুঁত (1.0) হলেও $V_6 \leq 0.6$। এটাই "More judges do not repair a rubric…" কথাটার গাণিতিক রূপ।

**সীমাবদ্ধতা:** বাস্তবে layer-গুলো independent নয়, আর "valid" binary নয় — এটা শুধু intuition-এর জন্য।

### ৬.১২ Idempotency ও External-Effect Invariant (Chapter 9–10)
**Idempotency (standard সংজ্ঞা; লেখকের ভাষায় "repeating it converges on the same observable state as applying it once"):**
$$
f(f(x)) = f(x)
$$
**No-duplicate invariant (আমার formalization; contract I5):** প্রতিটা logical effect identity $e$-এর জন্য
$$
N_{\text{effect}}(e) \leq 1 \quad \forall e
$$
— নয়তো স্পষ্টভাবে `unknown_external_state`।

**পাঁচটা kill point (paper-এর):** (1) dispatch-এর আগে; (2) dispatch-এর পরে কিন্তু external commitment-এর আগে; (3) commitment-এর পরে কিন্তু local acknowledgment-এর আগে; (4) acknowledgment-এর পরে কিন্তু durable state transition-এর আগে; (5) durable state transition-এর পরে। সবচেয়ে বিপজ্জনক "execute-then-log gap" হলো (3)–(4)।

### ৬.১৩ অন্যান্য সংখ্যাগত সম্পর্ক
- **Spearman correlation:** $\rho = 1 - \dfrac{6\sum d_i^2}{n(n^2-1)}$ (standard)। Paper: 52টা practice-এ urgency rank বনাম strong-evidence indicator-এর $\rho = -0.004$ — প্রায় শূন্য।
- **Context restart rule (Table 20.1, লেখকের personal default):** local sweep-এ weakest required task যে সবচেয়ে ছোট context length-এ উল্লেখযোগ্যভাবে খারাপ হয়, তার 60%-এ restart/consolidate। **আমার হিসাব:** degradation 64,000 token-এ হলে restart ≈ 38,400 token-এ।
- **Flaky CI (Ge ও Zhang 2026):** 3.2% build rerun হয়েছে, তার 67.73% flaky। **আমার হিসাব:** $0.032 \times 0.6773 \approx 0.0217$ → মোট build-এর প্রায় 2.2% ছিল "rerun হয়েছে এবং flaky" — এটা মোট flaky হারের একটা নিম্নসীমা মাত্র (যেগুলো rerun হয়নি তাদের কথা জানা নেই); লেখকও সতর্ক করেছেন এটা "two-thirds of all builds" নয়।
- **Netflix (practitioner, corroborating):** transient failure-এ deployment হারানো প্রায় 4% → 0.0001%। **আমার হিসাব:** প্রায় 40,000 গুণ কম — কিন্তু adopting team-এর নিজের মাপা, audit হয়নি, আর একসাথে অনেক কিছু বদলেছে।

---

## ৭. Experimental Setup (Monograph-এর জন্য: Evidence ও Measurement-এর উৎস)

### ৭.১ Evidence Corpus

| উৎস | সংখ্যা | কীভাবে ব্যবহৃত |
|---|---|---|
| Scholarly works | 164 | Bounded claim, evidence group সহ |
| Practitioner records | 100 | বেশিরভাগ corroborating |
| Benchmark records | 29 | Benchmark catalog (JSON Schema validated) |
| Author-system case records | 17 | Illustration / local measurement |
| Reference list | 249 | — |
| Cutoff | July 26, 2026 (consolidation); August 6, 2026 (update audit) | পরের material পরের edition-এ |

### ৭.২ Evidence-এর বণ্টন (প্রতিটা chapter-এর evidence profile থেকে)

| Ch | বিষয় | Strong | Directional | Corrob. | Null | Developed practice |
|---|---|---|---|---|---|---|
| 1 | Variance, power, paired | 10 | 1 | 0 | 0 | 3 |
| 2 | Baseline, ablation, cost | 1 | 5 | 0 | 0 | 2 |
| 3 | Contamination, oracle, workload | 7 | 8 | 1 | 0 | 4 |
| 4 | Execution gate, pass^k | 3 | 4 | 0 | 0 | 3 |
| 5 | Grader calibration | 5 | 7 | 0 | 0 | 2 |
| 6 | Proxy gaming, verifier | 3 | 3 | 0 | 0 | 3 |
| 7 | Software factory | 0 | 4 | 3 | 0 | 0 |
| 8 | Isolation, injection | 0 | 4 | 3 | 0 | 3 |
| 9 | Durable state, idempotency | 0 | 12 | 3 | 1 | 3 |
| 10 | Trace, fault injection | 1 | 9 | 0 | 0 | 2 |
| 11 | Failure taxonomy | 2 | 4 | 1 | 0 | 3 |
| 12 | Retrieval measurement | 6 | 8 | 1 | 0 | 3 |
| 13 | Localization, freshness | 6 | 5 | 1 | 0 | 3 |
| 14 | Context budget | 6 | 2 | 0 | 2 | 4 |
| 15 | Memory, compaction | 2 | 4 | 1 | 0 | 3 |
| 16 | Verification interface, escalation | 3 | 4 | 0 | 0 | 3 |
| 17 | Autonomy, provenance, gates | 2 | 5 | 0 | 0 | 4 |
| 18 | Topology | 6 | 16 | 1 | 0 | 4 |
| 19 | Fleet scheduling, routing | 2 | 17 | 2 | 0 | 4 |
| | **মোট (আমার যোগফল)** | **65** | **122** | **18** | **3** | **56** |

**আমার পর্যবেক্ষণ:**
- Profile-গুলো যোগ করলে 208টা item, যার 65টা (প্রায় 31%) strong। (এক item একাধিক chapter-এ গোনা হতে পারে, তাই এটা "unique source" সংখ্যা নয়।)
- লেখক বলেছেন Part I-এ strong item 56%, Part III-এ মাত্র 10%। শুধু profile-এর সংখ্যা দিয়ে আমার হিসাবে Part I ≈ 18/33 ≈ 55%, Part III ≈ 3/47 ≈ 6% — Part III-এ পার্থক্যের সম্ভাব্য কারণ: Chapter 8-এর দুটো strong item (AgentS4D, Perry et al.) companion record-এর বিপরীতে গোনা, যা যোগ করলে 5/49 ≈ 10% হয়।
- **সবচেয়ে strong অংশ:** evaluation statistics (Ch 1) ও benchmark validity (Ch 3) — ঠিক আমাদের CG4, CG6, CG8-এর জায়গা।
- **সবচেয়ে দুর্বল অংশ:** containment, durable execution (Ch 7–9) — কোনো strong item নেই।

### ৭.৩ লেখকের নিজের System (Author-system cases)

| System | কী | Monograph-এ কোথায় |
|---|---|---|
| **CodeProbe** (public repository) | Repository-র merged PR থেকে evaluation task mine করে; instruction আর ground-truth commit আলাদা রাখে; PR-এ touched test-কে verification command হিসেবে ব্যবহার; container ছাড়া চলে না, network বন্ধ | Ch 1, 2, 3, 4, 6, 8, 18 |
| **CodeScaleBench** (public, Apache-2.0) | 370 paired task, 20 suite (150 software-lifecycle + 220 organization-scale), 46 anchor repository (মোট 56 distinct), 9টা primary language; Chromium (~35M line), Firefox (~20M), LLVM (~15M), Android frameworks (~12M), Linux kernel, JDK, LibreOffice; দুই arm-এর পার্থক্য শুধু code access (local file tool বনাম retrieval server) | Ch 12, 20 |
| Enterprise data-access agent benchmark | Filesystem ownership দিয়ে write boundary; null "echo" agent দিয়ে verifier audit | Ch 2, 3, 8 |
| Memory system | Stable identity বনাম token similarity retrieval; schema বদলালে derived layer rebuild | Ch 6, 13, 15 |
| Trace-diagnostics corpus | 199টা trace, 1,705টা visible thinking block (private, redistribute করা হয়নি) | Ch 14 |
| Fleet ledger | 11 সপ্তাহ, 1,286 work item, 22 execution pool (private) | Ch 19 |
| Agent-workflow / orchestration system | "Works correctly" ধরনের acceptance criterion reject; failed worktree রাখা; branch guard | Ch 4, 8 |
| Human-approval queue | Audit-এ fail-open path পাওয়া গেছে | Ch 17 |
| Migration-evaluation framework | দুটো judge-কে Cohen's kappa দিয়ে gate (শুধু replay fixture-এ) | Ch 5 |
| Search-visibility measurement project | Model update-কে deployment হিসেবে ধরে fixed prompt corpus replay | Ch 4 |

---

## ৮. Results — মূল ফলাফল

### ৮.১ Review-এর Quantitative Output
| Output | সংখ্যা |
|---|---|
| Reliability record | 206 (193 gated + 13 lead) |
| Developed in depth | 56 |
| Companion compact entry | 137 (+ 13 lead) |
| Limited-support note | 29 |
| Chapter crosswalk | 193 gated record → chapter; 13 lead chapter-assignment ছাড়া |
| Grade audit | 10 practice + 2 restored → 6 নামানো, 6 রাখা |
| Urgency বনাম strong evidence (52 practice) | Spearman −0.004 |

**Catalog-এর chapter-ভিত্তিক বণ্টন (Appendix A parse করে আমার গোনা; lead সহ):** Ch1: 13, Ch2: 8, Ch3: 22, Ch4: 7, Ch5: 4, Ch6: 10, Ch7: 0, Ch8: 9, Ch9: 17, Ch10: 13, Ch11: 10, Ch12: 8, Ch13: 11, Ch14: 10, Ch15: 9, Ch16: 11, Ch17: 17, Ch18: 10, Ch19: 17 → মোট 206 ✓। **Chapter 3 (benchmark validity)-এ সবচেয়ে বেশি record (22)** — এটা আমাদের CG6-এর জন্য গুরুত্বপূর্ণ।

### ৮.২ External Evidence-এর মূল সংখ্যা (Monograph যেভাবে রিপোর্ট করেছে)

**Measurement ও statistics:**
| Finding | সংখ্যা | Evidence group |
|---|---|---|
| Single-run variance (Bjarnason et al. 2026) | 60,000 SWE-bench Verified trajectory; pass@1 spread 2.2–6.0 pp; temperature 0-তেও SD > 1.5 pp | Strong |
| একই system-এর দুটো single score তুলনা (Reimers ও Gurevych 2018) | 26% পর্যন্ত comparison-এ ভুয়া "significant" (p < 0.05) | Strong |
| Nuisance randomize (Bouthillier et al. 2021) | সব source আলাদাভাবে control করার প্রায় সমান estimator, ~51 গুণ কম compute | Strong |
| Prompt format sensitivity (Sclar et al. 2023) | 53 task-এ median 7.5 pp spread, সর্বোচ্চ 76 pp | Strong |
| Seed (Dodge et al. 2020) | একই hyperparameter-এ 2,100 fine-tuning trial-এ seed-ভেদে বড় পার্থক্য | Strong |
| Skill ablation (Tank ও Nama 2026) | প্রায় 6,000 run; ভালো skill জেতে মূলত কম regression ঘটিয়ে | Strong (সংকীর্ণ দাবিতে) |
| Cheap baseline (Kapoor et al. 2024) | HumanEval-এ retry জটিল architecture-এর সমান, অনেক কম খরচে | Directional |

**Benchmark validity ও oracle strength:**
| Finding | সংখ্যা | Evidence group |
|---|---|---|
| SWE-bench Verified audit (OpenAI 2026) | 500 task, 93 professional developer screen করেছিলেন; পরে 138টা audited task-এর 59.4% flawed test (≈82, পুরো subset-এর 16.4%); শুধু task ID দিলেই কিছু frontier model solution detail হুবহু reproduce করেছে | Corroborating |
| SWE-Bench Pro (OpenAI 2026) | audit-এ প্রায় 30% task broken → July 2026-এ recommendation প্রত্যাহার | Corroborating |
| Public-private gap (Prathifkumar et al. 2025) | SWE-bench Verified-এ control-এর তুলনায় প্রায় 3 গুণ overall ও 6 গুণ file-localization সুবিধা | Directional |
| Retroactive twins (Haimes et al. 2024) | 20 model-এ public score twin-এর চেয়ে 16 pp পর্যন্ত বেশি (QA benchmark) | Strong |
| GSM1k (Zhang et al. 2024) | 8 pp পর্যন্ত accuracy drop; $\rho = 0.36$, $p = 0.03$ | Strong |
| HackDetect (Shao et al. 2026) | 15 benchmark-এর 2,385 trace; Frontier Science trace-এর 67.0% ও AutoLab task-এর 66.7%-এ exposure বা reward hacking; inflation 0.45–1.00 (Mislead-gap scale) | Strong (audited protocol-এ) |
| EvalPlus (Liu et al. 2023) | Test 80 গুণ বাড়িয়ে 26 model-এ pass@k আপেক্ষিকভাবে প্রায় 19–29% কমেছে, ranking বদলেছে | Strong |
| UTBoost (Yu et al. 2025) | 36টা under-tested task, 345টা patch ভুলভাবে "passing"; Lite-এ 40.9% ও Verified-এ 24.4% entry সংশোধিত; 29টা ranking বদলেছে | Strong |
| PAIChecker (Wang, Xu ও He 2026) | SWE-bench Verified-এ 13.6% instance-এ PR-issue misalignment; detector accuracy 92.12% (SWE-Gym), 91.67% (SWE-bench Multilingual) | Strong |
| Ye et al. (2019) | 14টা repair system-এর 638টা patch; random test-ভিত্তিক oracle automatic patch assessment 190% উন্নত | Strong |
| SWE-ABS (Yu et al. 2026) | আগে পাস করা patch-এর 19.71% বাতিল; top score 78.80% → 62.20% | Strong |
| SWE-Bench+ (Aleithan et al. 2024) | একটা agent-model pair-এর apparent success-এর 32.67% solution leakage, 31.08% weak test; resolution 12.47% → 3.97% | Directional |
| Temporal split (LiveCodeBench, Jain et al. 2024) | Cutoff-এর পরের problem-এ কিছু model family-র performance উল্লেখযোগ্যভাবে কম | Strong |
| SWE-bench-Live, SWE-rebench, SWE-MERA | Live/decontaminated pipeline সম্ভব; frozen ও fresh distribution ভিন্ন ফল দেয় | Directional |

**আমার পর্যবেক্ষণ:** SWE-Bench+-এর 12.47% সংখ্যাটা আমাদের Paper 02 (SWE-agent + GPT-4 Turbo, full SWE-bench 12.47%)-এর সাথে হুবহু মেলে — তাই সম্ভবত ঐ pair-ই audit করা হয়েছিল (monograph শুধু "one agent and model pair" বলেছে; নিশ্চিত হতে SWE-Bench+ paper দেখতে হবে)। অর্থাৎ Sub-domain 1-এর SWE-agent-এর headline score-এর প্রায় দুই-তৃতীয়াংশ stronger audit-এ টেকেনি।

**Grading, execution ও self-report:**
| Finding | সংখ্যা | Evidence group |
|---|---|---|
| Silent semantic failure (Mehta 2026) | 4 model, 50 task, 1,750 trajectory; একটা model 100% trial-এ submit করেছে কিন্তু external oracle-এ মাত্র 44% resolved | Directional |
| Self-verdict gate (Park ও Choi 2026) | 54 cycle-এ agent প্রতিবার উন্নতি দাবি করেছে, অথচ 56% delta শূন্য বা ঋণাত্মক; self-verdict gate সব cycle accept করে best state 19% নষ্ট করেছে | Strong |
| Intrinsic self-correction (Huang et al. 2023) | External feedback ছাড়া self-correction প্রায়ই ব্যর্থ, কখনো খারাপ করে | Strong |
| Flaky CI (Ge ও Zhang 2026) | 1,960 Java project; 3.2% build rerun, তার 67.73% flaky; 1,055 project-এ অন্তত একটা | Directional (preprint) |
| CoT monitoring (Baker et al. 2025) | Reasoning trace দেখে reward hacking ধরা action-only-এর চেয়ে অনেক ভালো; দুর্বল model শক্তিশালী model monitor করতে পেরেছে; কিন্তু monitor-এর বিরুদ্ধে RL চাপ দিলে agent hack লুকাতে শিখেছে | Strong |

**Containment ও operation:**
| Finding | সংখ্যা | Evidence group |
|---|---|---|
| Risk-injected workspace (Zhou et al. 2026) | 328 task, 20 harness-model combination, 6,560 trial; 68.0% run-এ unsafe signal, 66.22% একসাথে unsafe ও complete | Strong |
| Real sessions (Tang et al. 2026) | 1,639 repository-র 20,574 session; misalignment episode-এর 90.5% irreversible ক্ষতি না করে effort ও trust খরচ করেছে; visible resolution-এর 91.49%-এ user-এর explicit correction লেগেছে | Directional |
| Production DB deletion (practitioner) | 9 সেকেন্ডে production database মুছে, একই credential দিয়ে backup-ও | Corroborating |
| Netflix durable workflow | ~4% → 0.0001% | Corroborating |
| Failure attribution (Zhang et al. 2025) | 127 multi-agent system; সেরা method দায়ী agent 53.5%, decisive step মাত্র 14.2% | Strong |
| Failure as process (Zhao et al. 2026) | 3,843 trajectory, 1,794 complete valid run, 63,000+ step | Directional (preprint) |

**Retrieval ও context:**
| Finding | সংখ্যা | Evidence group |
|---|---|---|
| Agent Retrieval Bench (Qin ও Xie 2026) | 25 repository-তে 427 sample; agent trajectory 27–35% sample-এ সব gold file মিস করেছে | Strong |
| Stale retrieval (Weng et al. 2026) | 17 উদাহরণ; stale-only-তে 15 ও 13 incompatible, current-only-তে 0; current যোগ করলে incompatible হার 47–65 pp কমে | Strong (ছোট diagnostic) |
| RULER (Hsieh et al. 2024) | 17 model-এর মোটামুটি অর্ধেক 32K token-এ সন্তোষজনক | Strong |
| LongSWE-Bench (Rando et al. 2025) | Claude 3.5 Sonnet 32K-এ 29% → 256K-এ 3%; LongCodeQA-তে Qwen2.5-14B 512K-এ 70.2% → 1M-এ 40.0% | Strong |
| Leng et al. (2024) | 20 model; বেশিরভাগ frontier model-এ accuracy প্রায় 64K-এ saturate | Strong |
| SWE-QA topology (Oskooei et al. 2026) | Semantic search 65.2% বনাম planner-subagent 46.2%, অর্ধেকের কম খরচে; handoff loss subagent failure-এর 41.8% | Strong |

### ৮.৩ লেখকের নিজের Measurement ও Failure Case

| # | Case | ফল | শিক্ষা |
|---|---|---|---|
| 1 | CodeProbe single run বনাম 3× rerun | +0.054 → +0.0035, CI [−0.0005, +0.0074], t = 2.41 < 2.776 | একটা run একটা draw |
| 2 | CodeProbe end-to-end | Plain baseline tool-augmented arm-কে score ও score-per-dollar দুটোতেই হারিয়েছে | Baseline না থাকলে tool-কে ভুল credit দেওয়া হতো |
| 3 | Enterprise benchmark task | 41 turn চলেছে কিন্তু tested tool একবারও call হয়নি | Static check-এ "perfect" task tool comparison-এর জন্য অকেজো |
| 4 | CodeProbe recall reward | পুরো repository return করলে "perfect" 1.0; পরদিন withdraw, F1 default | Proxy gaming বাস্তব |
| 5 | Null "echo" agent | কিছু verifier শুধু instruction repeat করা output-কেও credit দিয়েছে; একটা full marks দিয়েছে কারণ checker prompt-এর শব্দই খুঁজছিল | শূন্য-ক্ষমতার adversary সস্তায় verifier defect ধরে |
| 6 | Merge fault demonstration | Naive pipeline দ্বিতীয়বার merge request পাঠিয়ে "success" রিপোর্ট করেছে; guarded variant একটা merge, একটা escalation, workflow failed | Uncertainty রেখে fail করা বেশি reliable |
| 7 | CodeScaleBench retrieval | P@10 0.095 → 0.313; R@10 0.120 → 0.272; hit 0.33 → 0.56; reward +0.0349 (n = 370) | Layer-এ উন্নতি end-to-end-এ পৌঁছায় না; CI cluster-aware হয়নি |
| 8 | Memory system (4 seed) | Stable identity retrieval 1.0, token-similarity 0.0 (superseded value ফেরত) | ভালো rank ≠ current |
| 9 | Trace diagnostics | 199 trace-এর 1,705 thinking block-এ system prompt-এর নির্দেশ 0 বার | Context window-এ থাকা ≠ সক্রিয় থাকা |
| 10 | CodeProbe preamble patch | Cost 28% কম, reward +0.0048 (t = 0.27); সময় 40% কমার prediction-এর বদলে 3.9% বেড়েছে | Prompt patch ভুল variable বদলেছে; harness coupling-ই আসল কারণ |
| 11 | Fleet replay | 11 সপ্তাহ, 1,286 item, 22 pool; FCFS 6.84 ঘণ্টা বনাম অন্য তিন policy 6.70 ঘণ্টা; আগে ঠিক করা 15% promotion requirement → কোনোটা ship হয়নি | আগে লেখা decision rule জটিলতা ঠেকায় |
| 12 | Human-approval queue | কিছু script missing component-এ fail-open; validation ছাড়া execution | Gate থাকা ≠ gate কার্যকর |
| 13 | Orchestration worktree | Controller ভুল base revision দিয়েছিল; mechanical branch guard একটা commit আটকেছে | Agent-কে না জিজ্ঞেস করে repository state দেখো |
| 14 | Research pipeline reference audit | Generated reference list-এ fabricated, mis-cited, untraceable source | Certainty ≠ existence |
| 15 | Context-assembly practice ranking | 10টা practice তিনভাবে rank করে মাত্র 1টায় তিনটা ranking একমত | Field এখনো converge করেনি |

### ৮.৪ Catalog Structure ও প্রতিনিধিত্বমূলক Developed Practice

| Chapter | উদাহরণ developed practice (ERCA ID) |
|---|---|
| 1 | Never report a single run (020); Compare systems with paired tests matched to the metric (024); Power-analyze the eval before running (025) |
| 2 | Evaluate jointly on cost and accuracy, with trivial baselines (012); Run ablation and no-tool controls (114) |
| 3 | Strengthen weak test oracles before trusting pass rates (001); Pair public score with matched private control (003); Post-cutoff temporal holdouts (004); Evaluate on your own workload (066) |
| 4 | Gate self-correction on external feedback (061); Ground evaluation in execution (094); Replay a golden set every release, scored pass^k (095) |
| 5 | Calibrate LLM judges against expert labels before scaling (096); Never treat consensus as verification (111) |
| 6 | Never gate on a single proxy (038); Watch for proxy/true-signal divergence (039); Monitor the CoT, never train against the monitor (042) |
| 8 | Contain agent blast radius (068); Never trust "done": verify workspace state (069); Defend against prompt injection in depth (105) |
| 9 | Make every retried step idempotent (124); Durable workflow engine (128); Externalize agent state (130) |
| 10 | Structured, replayable trace (097); Benchmark recovery with fault injection (127) |
| 11 | Derive failure taxonomy from own traces (045); Do not delegate attribution to a model (046); Traces for human audit (047) |
| 12–13 | Score retrieval separately (076); Hybrid multi-channel retrieval (083); AST chunking (085); Freshness gate (078); Localization funnel (084); Typed knowledge graph (174) |
| 14–15 | Budget context to measured length (072); Consolidate spec and restart (088); Persist large outputs as files (143); A/B-test context files (178); Raw traces as ground truth (116) |
| 16–17 | Verification surfaces cheaper than blind acceptance (153); Widen autonomy per action track record (145); Audit every human gate (154); Label AI-generated code (165) |
| 18–19 | Default to single agent (093); Match topology to task (107); Route to cheapest sufficient model (187); Replay traces under competing policies (191) |

### ৮.৫ লেখকের Personal Default (Table 20.1 — "transferred effect estimate নয়")

| সিদ্ধান্ত | Starting point |
|---|---|
| Repeated evaluation | Screening-এ প্রতি item-এ k = 3 paired run; শুধু screen থেকে promote নয়; release comparison pilot ও decision-relevant effect থেকে size |
| Reliability reporting | pass@k ও pass^k দুটোই, k পাশে লিখে; k = 3 দিয়ে শুরু |
| Human-label agreement | Kappa < 0.60 → rubric debug trigger; > 0.60 correctness gate নয় |
| Promotion threshold | আগে থেকে: 3 pp absolute success gain (cost না বাড়িয়ে) অথবা 10% cost reduction (success না কমিয়ে) |
| Failure review | Model/apparatus/policy বদলের পর 20টা stratified failure পড়া; "abstain" category রাখা |
| Context restart | Shortest degradation length-এর 60%-এ |
| Freshness | Code retrieval-এ exact repository-revision identity; source revision অজানা index reject |

**"Floor পর্যন্ত টিকে থাকা উচিত" এমন চারটা জিনিস:** (1) executable acceptance check; (2) ordinary ও recovery authority আলাদা; (3) task, input state, configuration, attempt ও accepted artifact-এর versioned identity; (4) সবচেয়ে সস্তা credible baseline-এর বিপরীতে paired comparison।

---

## ৯. Key Findings / Insights (Supervisor-কে বলার মতো ৮টা পয়েন্ট)

1. **একটা run একটা draw:** SWE-bench Verified-class task-এ single-run variance (2.2–6.0 pp) অনেক published "improvement"-এর সমান; temperature 0 সমাধান নয়।
2. **Pairing ও power বাধ্যতামূলক:** একই item-এ দুই system, per-item record, ফল দেখার আগে threshold — নয়তো "no verdict"।
3. **Test pass ≠ correct:** UTBoost, SWE-ABS, SWE-Bench+, EvalPlus — সব audit-এ শক্ত oracle দিলে score ও ranking বদলায়; passing patch একটা "hypothesis about correctness"।
4. **Agent-এর "done" একটা claim, প্রমাণ নয়:** 100% submit বনাম 44% resolved; self-verdict gate 54 cycle-এর সবকটা accept করেছে।
5. **Agreement ≠ correctness:** judge-কে expert label, kappa, class-specific error ও fixed-FPR-এ TPR দিয়ে calibrate করতে হবে; consensus vote verification নয়।
6. **Verifier-এর নিজেরও দুটো failure domain:** infrastructure health (flaky, wrong revision) ও oracle adequacy; verdict-কে artifact version, verifier version ও environment-এর সাথে বাঁধতে হবে; "indeterminate" একটা বৈধ status।
7. **Layer-এ উন্নতি end-to-end-এ নাও পৌঁছাতে পারে:** retrieval precision তিনগুণ, reward +0.0349 — তাই stage-level measurement দরকার।
8. **Evidence strength ও urgency সম্পর্কহীন (ρ = −0.004):** containment-এর মতো জরুরি control-এর পেছনে controlled study নেই; লেখক mechanism-ভিত্তিক, locally testable justification দেন।

---

## ১০. কেন এই কাজ অন্যগুলোর থেকে ভালো / আলাদা?

| বৈশিষ্ট্য | Benchmark paper (যেমন SWE-bench) | Agent system paper (SWE-agent, Agentless) | সাধারণ SLR / APR survey | **এই monograph** |
|---|---|---|---|---|
| মূল একক | Model/agent-এর score | একটা scaffold-এর score | Literature-এর taxonomy | **পুরো system ও তার evidence chain** |
| Grey literature | না | না | সাধারণত না | **হ্যাঁ, independence key সহ** |
| Evidence grading | প্রযোজ্য নয় | প্রযোজ্য নয় | কখনো quality score | **প্রতিটা scoped claim-এ চার-স্তর grade + challenge audit** |
| Statistical rigor guidance | কম (একবার run) | কম–মাঝারি | কম | **বিস্তারিত: pairing, power, McNemar, cluster resampling** |
| Operation (retry, recovery, permission) | না | না | না | **হ্যাঁ, distributed-systems contract সহ** |
| Runnable artifact | Dataset, harness | Code | সাধারণত না | **Protocol, skill, catalog, ledger, schema** |
| নিজের সীমা disclose | আংশিক | আংশিক | আংশিক | **খুব বিস্তারিত (search lane না চলা, IRR নেই)** |

**মূল শক্তি:**
1. **System-level দৃষ্টিভঙ্গি:** model-এর বাইরে harness, verifier, state, permission-কে প্রথম-শ্রেণির reliability বিষয় হিসেবে ধরা।
2. **Claim-level honesty:** প্রতিটা সংখ্যার পাশে evidence group; author-system ফলকে evidence থেকে আলাদা।
3. **Actionability:** প্রতিটা chapter-এর শেষে চালানো যায় এমন procedure।
4. **Stable identifier (ERCA-NNN):** manuscript, ledger, protocol, skill — সব এক ID-তে যুক্ত; পরের edition-এও ID বদলাবে না।
5. **Transparency:** কোন database search চলেনি, কোন অংশে strong evidence নেই — সব লেখা।

---

## ১১. কোন পরিস্থিতিতে এই Monograph ভালো কাজ করে, কোথায় করে না

### ✅ ভালো কাজ করে যখন:
- **Evaluation design করতে চাও:** কতবার চালাবো, কোন test, কীভাবে দুটো system তুলনা — Part I–II সরাসরি ব্যবহারযোগ্য।
- **Public benchmark score বিচার করতে চাও:** Section 3.5-এর চারটা প্রশ্ন।
- **Production-এ agent চালাও:** বড় organization, অনেক repository, scarce reviewer, durable external effect।
- **Assurance/verification tool বানাতে চাও:** verdict record, judge calibration, proxy independence।

### ❌ সীমিত যখন:
- **কোন model ভালো** জানতে চাও — লেখক ইচ্ছা করে model comparison বাদ দিয়েছেন।
- **Prompt বা tool-schema design** শিখতে চাও — scope-এর বাইরে।
- **ছোট single-repository project:** লেখক নিজেই বলেছেন অনেক practice বড় scale-এর জন্য; নিচে transfer "assumption to test"।
- **Numeric threshold চাও:** বেশিরভাগ জায়গায় কোনো universal value নেই; Table 20.1-ও personal default।
- **Part VI (topology, scheduling):** এটা research agenda — প্রতিষ্ঠিত guidance নয়।
- **Patch-এর security/code quality analysis:** containment (permission) নিয়ে অনেক কথা, কিন্তু agent-এর লেখা code-এ নতুন vulnerability ঢুকছে কিনা তা মাপার পদ্ধতি এই monograph-এর কেন্দ্রে নেই (Perry et al. 2023 শুধু উল্লেখ)।

---

## ১২. Limitations — দুর্বলতা

### ১২.১ Author যা নিজে স্বীকার করেছেন
1. **Structured, not exhaustive:** ACM DL, IEEE Xplore, Scopus search চালানো হয়নি; DBLP census শুধু title-ভিত্তিক।
2. **Evidence অসম:** কিছু topic-এ শুধু case-level support; recent capability measurement দ্রুত পুরনো হয়; practitioner report-এ selection, survivorship ও reporting bias।
3. **Grading-এ independent calibration নেই:** লেখক একা চূড়ান্ত grade দিয়েছেন; automated challenge pass আছে, কিন্তু blinded multi-reviewer grading নেই; IRR packet release করা হলেও ফল নেই। লেখক নিজেই এটাকে Chapter 5-এর পরামর্শের সাথে "asymmetry" বলেছেন।
4. **Query log পুরোপুরি replay করা যায় না:** কিছু interactive search reconstructed।
5. **Author-system case independent evidence নয়।**
6. **Chapter selection authorial judgment** (Spearman −0.004)।
7. **Part VI মূলত transfer:** telescope/cluster scheduling থেকে ধার করা; settled guidance নয়।
8. **Workload-নির্ভরতা:** empirical ফল workload ও system configuration-নির্ভর।
9. **CodeScaleBench-এর CI cluster structure মানেনি** — uncertainty কম দেখাতে পারে।

### ১২.২ আমার Critical Analysis (Professor-level observation)
1. **একক লেখক, preprint, peer review নেই:** 313 পৃষ্ঠার এত বড় দাবি-সমষ্টি একজনের — selection, grading, synthesis সব একজনের হাতে। লেখকের নিজের Chapter 5-এর মানদণ্ডে এই grading-ই এখনো "uncalibrated instrument"।
2. **Conflict of interest-এর সম্ভাবনা:** CodeScaleBench লেখক এমন vendor-এ বানিয়েছেন যার retrieval product একটা arm — লেখক নিজেই এটা disclose করে ফলকে "illustration" বলেছেন, যা প্রশংসনীয়; তবু retrieval chapter পড়ার সময় এটা মনে রাখা দরকার।
3. **খুব নতুন ও অনেক preprint source-এর উপর নির্ভরতা:** অনেক strong item 2026-এর arXiv preprint (যেমন Park ও Choi, Shao et al., Wang et al., Tank ও Nama)। "Strong" grade এখানে study design-এর উপর, peer review-এর উপর নয় — পরে এগুলোর কোনোটা সংশোধিত বা প্রত্যাহার হতে পারে। আমি cited কাজগুলো আলাদাভাবে যাচাই করিনি।
4. **Vendor blog-এর উপর নির্ভর headline:** SWE-bench Verified ও SWE-Bench Pro-র সমস্যার সংখ্যা (59.4%, ~30%) OpenAI-এর নিজের post থেকে — লেখক এগুলোকে ঠিকভাবেই "corroborating" রেখেছেন, কিন্তু opening narrative-এ এগুলো অনেক গুরুত্ব পেয়েছে।
5. **Evidence profile-এর সংখ্যা চেক করা কঠিন:** "Part I-এ 56% strong" আর chapter profile যোগ করে আমার ~55% প্রায় মেলে, কিন্তু Part III-এর "10%" মেলাতে companion-counted item যোগ করতে হয় — counting নিয়ম main text-এ স্পষ্ট নয়।
6. **ছোটখাটো অসংগতি:** "Monitorability tax" Chapter 6-এ মানে monitor-এর বিরুদ্ধে optimize না করার জন্য ছেড়ে দেওয়া gain; কিন্তু Glossary-তে মানে জটিল architecture diagnosable করার বাড়তি instrumentation কাজ — দুটো আলাদা সংজ্ঞা।
7. **Patch-level correctness assessment কম:** monograph oracle strengthening ও judge calibration নিয়ে অনেক বলে, কিন্তু APR-এর APCA (যেমন RePaCA-ধরনের static correctness classifier) বা patch overfitting detector-কে আলাদা করে বিশ্লেষণ করেনি — আমাদের CG1/CG9-এর মূল প্রশ্নটা এখানে সরাসরি নেই।
8. **Security of generated code প্রায় অনুপস্থিত:** blast radius, injection, permission আছে; কিন্তু "agent-এর patch নিজে vulnerable কিনা" (CWE, SAST) — এটা scope-এ নেই। আমাদের CG5-এর জন্য অন্য sub-domain লাগবে।
9. **Practicality vs. student scale:** অনেক practice (durable workflow engine, fleet scheduling) বড় organization-এর জন্য; SPL3 scale-এ Part I–II আর Ch 6, 8, 12–13 বেশি প্রাসঙ্গিক।
10. **Long-term validity প্রশ্ন:** লেখক নিজে বলেন numeric ফল দ্রুত পুরনো হবে; তাঁর দাবি "structural claims" টিকবে — এটা যুক্তিসঙ্গত, কিন্তু এখনো empirically পরীক্ষিত নয়।

---

## ১৩. Research Gaps — কোথায় কাজ করার সুযোগ আছে

### ১৩.১ Monograph থেকে পাওয়া Gap (আমাদের sub-domain folder-এর সাথে যুক্ত)

| # | Gap | Monograph-এর প্রমাণ | কোন sub-domain folder-এ আরও পড়তে হবে | গুরুত্ব |
|---|---|---|---|---|
| E1 | **Patch-level oracle strengthening-কে assurance layer-এ নেওয়া** — stored patch-এ stronger test চালিয়ে survival fraction | UTBoost, SWE-ABS, EvalPlus, SWE-Bench+ (Ch 3) | Patch Validation; LLM Test Generation | ⭐⭐⭐⭐⭐ |
| E2 | **Version-bound verification record ও infrastructure-vs-semantic separation** (accepted / rejected / indeterminate) | Ch 6.4, contract I7–I8, Ge ও Zhang flaky CI | Patch Validation; AI Coding Agents | ⭐⭐⭐⭐⭐ |
| E3 | **Repeated-run reliability (pass^k) agent patch-এর জন্য** — কেউ SWE-bench-ধরনের agent-এ pass^k নিয়মিত report করে না | Ch 1, Ch 4 (tau-bench), Table 20.1 | Coding-Agent Evaluation & Reliability (এই folder) | ⭐⭐⭐⭐ |
| E4 | **LLM judge-কে patch correctness-এ calibrate করা** (kappa, TPR at fixed FPR, stratified validation) | Ch 5 | Patch Validation (HITL LLM-as-a-Judge paper); Trustworthy AI for SE | ⭐⭐⭐⭐⭐ |
| E5 | **Assurance signal-এর বিরুদ্ধে optimization pressure** — agent retry বা best-of-n যদি assurance verdict দেখে, তবে detector gaming | Ch 6 (Skalse, Baker, best-of-n against monitor) | Trustworthy AI for SE; Patch Validation | ⭐⭐⭐⭐ |
| E6 | **Agent self-report বনাম workspace verification** (submission ≠ resolution) | Mehta, Park ও Choi, Tang et al. (Ch 4, 8) | AI Coding Agents; Trustworthy AI for SE | ⭐⭐⭐⭐ |
| E7 | **Cluster-aware statistics** (repository/suite-level resampling) | CodeScaleBench CI সমস্যা (Ch 12, 20) | Coding-Agent Evaluation & Reliability | ⭐⭐⭐ |
| E8 | **Stage-level retrieval measurement ও freshness** | Ch 12–13 | AI Coding Agents (localization) | ⭐⭐⭐ |
| E9 | **Generated patch-এর security** — monograph-এ প্রায় অনুপস্থিত | Perry et al. (Ch 8) শুধু উল্লেখ | Security of AI-Generated Code | ⭐⭐⭐⭐ |
| E10 | **Patch overfitting detector (APCA) agent patch-এ** — monograph-এ আলোচনা নেই | — (অনুপস্থিতিই gap) | Automated Program Repair; Patch Validation | ⭐⭐⭐⭐⭐ |
| E11 | **Evidence grading-এর IRR** — monograph-এর নিজের packet চালানো | Section 0.3.3 | Trustworthy AI for SE (meta-research) | ⭐⭐ |
| E12 | **Recovery benchmark** (published fault menu, named kill placement) — লেখক নিজে বলেছেন এমন study দরকার | Ch 10, 20.2 | Coding-Agent Evaluation & Reliability | ⭐⭐ (SPL3-এর জন্য বড়) |

### ১৩.২ ১৩টা Research Lead — আমাদের Direction-এর সাথে Overlap ও SPL3 Feasibility

(Lead মানে লেখকের ভাষায় "preserved for investigation, not recommendation" — gated practice নয়।)

| ID | Lead | Ch | আমাদের assurance layer-এর সাথে overlap | SPL3-এ করা সম্ভব? |
|---|---|---|---|---|
| ERCA-193 | Fence stale worker authority at the mutation boundary | 18 | কম — multi-worker orchestration-এর বিষয় | ❌ scope-এর বাইরে |
| ERCA-194 | Separate logical work identity from attempt identity | 9 | **মাঝারি** — প্রতিটা agent run-কে attempt হিসেবে record করলে consistency check ও pass^k সহজ | ✅ data model হিসেবে সহজ |
| ERCA-195 | Reconcile unknown external effects instead of assuming | 9 | কম | ❌ |
| ERCA-196 | Test the controller under stale and missed state | 10 | কম–মাঝারি (stale state ধারণা freshness-এর সাথে যুক্ত) | ⚠️ ছোট demo সম্ভব |
| ERCA-197 | Place fault injections at named commit barriers | 10 | মাঝারি — assurance pipeline নিজে crash-safe কিনা পরীক্ষা | ⚠️ ছোট demo সম্ভব |
| ERCA-198 | Test the recovery action itself | 10 | কম | ❌ |
| ERCA-199 | Budget retries as load | 19 | কম | ❌ |
| ERCA-200 | Jitter recovery redelivery | 19 | কম | ❌ |
| ERCA-201 | Reserve or prioritize capacity for recovery work | 19 | কম | ❌ |
| ERCA-202 | Separate global capacity from local dispatch | 19 | কম | ❌ |
| ERCA-203 | **Version verifier results** | 9 | **উচ্চ** — assurance verdict-কে (artifact version, verifier version, environment)-এর সাথে বাঁধা; আমাদের layer-এর মূল record format হতে পারে | ✅ সরাসরি |
| ERCA-204 | Measure recovery under live load | 10 | কম | ❌ |
| ERCA-205 | Detect retry storms and recovery starvation | 19 | কম | ❌ |

**আমার পর্যবেক্ষণ:** 13টা lead-এর বেশিরভাগই distributed-systems/fleet operation-এর — আমাদের direction-এর সাথে সরাসরি মেলে শুধু **ERCA-203**, আংশিকভাবে **ERCA-194** ও **ERCA-197**। আমাদের জন্য বেশি গুরুত্বপূর্ণ আসলে gated practice-গুলো: ERCA-001 (strengthen weak oracles), 095 (golden set pass^k), 094 (ground in execution), 096 (calibrate judges), 111 (consensus ≠ verification), 038/039 (proxy), 069 (never trust "done"), 020/024/025 (statistics)।

---

## ১৪. কী করলে আরও ভালো হবে — Improvement Ideas

1. **External grading packet চালানো ও kappa report করা** — monograph-এর সবচেয়ে বড় methodological ফাঁক বন্ধ হবে।
2. **ACM/IEEE/Scopus lane চালানো** — SE venue coverage পূর্ণ করা।
3. **Patch correctness assessment-এর একটা chapter যোগ করা** — APR-এর overfitting literature (APCA, test-free classifier) কে oracle strengthening-এর পাশে রাখা।
4. **Generated-code security-কে grading layer-এর অংশ করা** — SAST signal কে "layered independent signal" হিসেবে।
5. **CodeScaleBench-এ cluster/hierarchical bootstrap** দিয়ে CI পুনঃহিসাব।
6. **Recovery benchmark** (লেখকের নিজের প্রস্তাব) — published fault menu, named kill point, recurring failure।
7. **Glossary ও chapter-এর সংজ্ঞা মেলানো** (যেমন monitorability tax)।
8. **(আমার প্রস্তাব) pass^k-এর একটা ছোট public dataset** — কয়েকটা open agent-কে SWE-bench Lite subset-এ k বার চালিয়ে per-task outcome publish করা; এটা monograph-এর Table 20.1-এর নিয়মের প্রথম বাস্তব প্রয়োগ হতে পারে।

---

## ১৫. কোন Gap-এ Research করলে ভালো Result ও Publication আসতে পারে

> ⚠️ তিনটা sub-domain-এর পরের প্রাথমিক মত। বাকি sub-domain (LLM Test Generation, Patch Validation, Security, Trustworthy AI) পড়ার পর চূড়ান্ত করবো।

| Gap | SPL3-তে করা সম্ভব? | Novelty | Publication সম্ভাবনা |
|---|---|---|---|
| **E1 + E10: Agent patch-এ oracle strengthening + overfitting detection, survival fraction report** | ✅ হ্যাঁ — SWE-bench Lite/Verified-এর ছোট subset, public patch | উচ্চ | ⭐⭐⭐⭐⭐ |
| **E2 + ERCA-203: Version-bound assurance record (accepted / rejected / indeterminate) + flaky detection** | ✅ হ্যাঁ — tool-engineering contribution | মাঝারি-উচ্চ (agent patch-এ এভাবে কেউ করেছে কিনা যাচাই করতে হবে) | ⭐⭐⭐⭐ (tool/demo track) |
| **E4: Patch-correctness LLM judge-এর calibration study** (kappa, TPR at fixed FPR) | ✅ হ্যাঁ — ছোট labelled set (যেমন AutoCodeRover-এর 78টা যাচাই করা patch, যদি label পাওয়া যায়) | উচ্চ | ⭐⭐⭐⭐ |
| **E3: pass^k-ভিত্তিক agent patch reliability** | ⚠️ সম্ভব কিন্তু API খরচ বেশি (k × task) | মাঝারি-উচ্চ | ⭐⭐⭐ |
| **E5: Assurance detector-এর বিরুদ্ধে best-of-n gaming পরীক্ষা** | ⚠️ ছোট আকারে সম্ভব | উচ্চ | ⭐⭐⭐⭐ |
| E12: Recovery benchmark | ❌ SPL3-এর জন্য বড় | উচ্চ | ⭐⭐⭐ |

**সম্ভাব্য venue (general guidance, যাচাই সাপেক্ষে):**
- **Conference:** ICSE, FSE, ASE, ISSTA (top SE); তাদের workshop ও tool/demo track (যেমন LLM4Code-ধরনের workshop) — student-এর শুরু করার জন্য সহজ।
- **Journal:** ACM TOSEM, IEEE TSE, Empirical Software Engineering, JSS, IST।
- **নোট:** Monograph-এর SEGRESS ও construct-validity রেফারেন্সগুলো আমাদের নিজের methodology section লিখতে কাজে লাগবে।

---

## ১৬. SPL3 Implementation Perspective — Software-এ কীভাবে আনবো

### ১৬.১ Monograph থেকে কী Reuse করা যায় (লেখকের দাবি অনুযায়ী artifact; আমি repository খুলে দেখিনি — license ও availability যাচাই করতে হবে)

| Artifact | কী | আমাদের কাজে ব্যবহার |
|---|---|---|
| `protocols/evaluation-comparison.md` | Paired comparison, repeat, pass condition, retained file | Assurance layer-এর evaluation (CG8, CG10) |
| `protocols/minimum-reliability-pass.md` | Section 0.5-এর ছয় ধাপ checklist | Project-এর শুরুতে baseline audit |
| `protocols/failure-trace-review.md` | Blinded failure review | Agent failure taxonomy বানাতে |
| `protocols/authority-boundary-test.md` | Permitted/prohibited action test | Agent sandbox config যাচাই |
| `protocols/recovery-fault-injection.md` | Kill-point sweep | (ঐচ্ছিক) আমাদের pipeline-এর crash safety |
| `protocols/allocation-policy-replay.md` | Scheduling replay | প্রাসঙ্গিক নয় |
| `protocols/factory-contracts.yaml` | I1–I11 machine-testable form | Record schema design-এর reference |
| Skill: **evaluation design** | Evaluation পরিকল্পনা | Experiment design |
| Skill: **end-to-end test design** | Test design | Extra test generation component |
| Skill: **failure-mode capture** | Failure ধরা ও রেকর্ড | Failure taxonomy |
| Skill: **focused execution**, **verified long-running implementation** | Agent কাজের নিয়ম | নিজের development-এ coding agent ব্যবহার করলে |
| **CodeProbe** (public) | Merged PR থেকে task mining | নিজের repository থেকে ছোট golden set |
| **CodeScaleBench** (Apache-2.0, GitHub + HuggingFace) | 370 paired task, বড় repository | খুব ভারী — শুধু reference বা ছোট subset |

(Data availability অংশে "six named runnable protocols" বলা আছে; উপরের ছয়টা `.md` file-ই সম্ভবত সেই ছয়টা — এটা **আমার অনুমান**, repository দেখে নিশ্চিত হতে হবে।)

### ১৬.২ Assurance Layer — Monograph অনুযায়ী Update করা Module Design

| Module | কাজ | Monograph-এর ভিত্তি | CG |
|---|---|---|---|
| 1. Task & attempt store | প্রতিটা task-এর `task_id`, `input_state_id` (repo commit), প্রতিটা agent run-এর `attempt_id`, `artifact_version` (patch hash) | Ch 7 identity, ERCA-194 | CG4, CG8 |
| 2. Sandboxed execution gate | Docker-এ clean snapshot, network বন্ধ, timeout, structured result parse; infrastructure error আলাদা | Ch 4 (094) | CG3, CG8 |
| 3. Verification record | `verification_id`, artifact version, verifier version, environment, raw result, status = accepted / rejected / indeterminate; flaky হলে নতুন verification_id | Ch 6.4, ERCA-203, I7–I8 | নতুন CG11 |
| 4. Oracle strengthening | Generated extra test + adversarial wrong-patch (hard-coded fixture, exception চাপা দেওয়া) দিয়ে survival fraction | Ch 3.3 (001) | CG1, CG3 |
| 5. Static judge (APCA / LLM-as-judge) | RePaCA-ধরনের reasoning judge — expert label দিয়ে kappa, TPR at fixed FPR | Ch 5 (096, 111), Sub-domain 2 | CG1, CG9, CG10 |
| 6. Security scan | Bandit/Semgrep — আলাদা, independent signal হিসেবে | Ch 6 (layered signals) | CG5 |
| 7. Repeated-run module | প্রতি task k = 3; pass@k ও pass^k দুটোই | Ch 1, 4 (020, 095) | CG4 |
| 8. Statistics module | Paired McNemar, paired/cluster bootstrap, MDE, kappa, class-specific rate | Ch 1, 5 (024, 025) | CG8, CG10 |
| 9. Report (multi-signal, scalar নয়) | প্রতিটা signal আলাদা দেখানো; disagreement highlight | Ch 6 (038) | CG7 |

### ১৬.৩ Verification Record-এর একটা উদাহরণ (আমার design, monograph-এর field অনুসারে)
```yaml
verification_id: ver-0007
task_id: django__django-11099
input_state_id: <base commit sha>
attempt_id: agentless-run2-attempt1
artifact_version: sha256:<patch hash>
verifier: swebench-harness
verifier_version: <harness version>
environment_id: <docker image digest>
signals:
  f2p_p2p_tests: pass
  extra_generated_tests: fail (2 of 15)
  static_judge: overfitting (confidence 0.71)
  security_scan: no new finding
status: rejected   # accepted / rejected / indeterminate
raw_result_ref: runs/ver-0007/log.txt
```

### ১৬.৪ Practical সতর্কতা
- **Windows-এ WSL2 + Docker** লাগবে (SWE-bench harness)।
- **খরচ:** k = 3 মানে API খরচ তিনগুণ — প্রথমে public patch (Agentless, AutoCodeRover) দিয়ে offline কাজ; repeated run শুধু ছোট subset-এ।
- **Assurance verdict agent-কে feedback দিলে** সেটা best-of-n selection-এ পরিণত হয় (Ch 6) — evaluation-এর সময় verdict feedback loop থেকে আলাদা রাখতে হবে, অথবা এটাকেই experiment-এর variable বানাতে হবে।
- **নিজের detector-এর evaluation-এ leakage-মুক্ত split** (Sub-domain 2-এর শিক্ষা) আর pre-registered threshold (Ch 4, Table 20.1)।
- Promotion/claim-এর threshold **ফল দেখার আগে** লিখে রাখা।

---

## ১৭. প্রভাব ও আগের Sub-domain-এর সাথে সংযোগ (Context)

### ১৭.১ আগের Paper-গুলোর সাথে সরাসরি যোগসূত্র
- **SWE-bench (Paper 01):** monograph একে executable repository repair-এর directional উৎস হিসেবে ব্যবহার করে, আর দেখায় Verified subset-ও পরে ত্রুটিপূর্ণ পাওয়া গেছে (59.4% of 138 audited)। আমাদের SWE-bench analysis-এর G1 (weak test) ও G5 (reliability) gap এখানে বিস্তারিত প্রমাণ পায়।
- **SWE-agent (Paper 02):** SWE-Bench+-এর 12.47% → 3.97% audit সম্ভবত ঐ pair-এর (আমার পর্যবেক্ষণ)।
- **Agentless (Paper 04):** Chapter 13-এ Xia et al. (2024)-কে staged localization funnel-এর উদাহরণ হিসেবে উল্লেখ — fixed pipeline সে সময়ের autonomous agent-কে হারিয়েছে, যদিও পরে শক্তিশালী model-এ অন্যরা এগিয়ে গেছে।
- **SWE-rebench (এই folder-এর আরেকটা paper):** Badertdinov et al. (2025) — directional evidence হিসেবে live/decontaminated pipeline-এর উদাহরণ।
- **Sub-domain 2 (APR):** Ye et al. (2019)-এর 638 patch, 190% উন্নতি — APR-এর পুরনো oracle সমস্যা monograph-ও স্বীকার করে: "shipped tests are not equivalent to a specification"।

### ১৭.২ CG1–CG10-এ Monograph-এর অবদান

| CG | Gap | Monograph কী বলে | অবস্থা |
|---|---|---|---|
| CG1 | Plausible patch-এর correctness | Passing patch = "hypothesis about correctness"; UTBoost (345 ভুল pass), SWE-ABS (19.71% বাতিল), SWE-Bench+ (12.47% → 3.97%), EvalPlus | **অনেক শক্ত হলো** — repository-scale প্রমাণসহ |
| CG2 | Candidate selection / re-ranking | সরাসরি কম; তবে সতর্কতা: selector যদি verdict-এর বিরুদ্ধে best-of-n করে, proxy gaming হয় | **Refine** — re-ranking signal-কে independent রাখতে হবে |
| CG3 | Generated test ও validation-এর মান | Weak oracle, adversarial wrong-patch construction, faulty feedback "directed failure mode" তৈরি করে, null echo agent | **শক্ত হলো** |
| CG4 | Run-to-run reliability | Chapter 1 পুরোটা; 60,000 trajectory; pass^k release gate; k = 3 default | **অনেক শক্ত হলো** — এখন সবচেয়ে বেশি প্রমাণিত gap-গুলোর একটা |
| CG5 | Patch security ও quality | Containment ও injection আছে, কিন্তু generated code-এর vulnerability নেই | **অপরিবর্তিত** — Security sub-domain-এর উপর নির্ভর |
| CG6 | Benchmark quality ও contamination | Chapter 3 (22টা catalog record): inflation gap, temporal eligibility, PAIChecker 13.6%, HackDetect | **অনেক শক্ত হলো** |
| CG7 | Confidence ও abstention | Agent-এর self-confidence অবিশ্বস্ত (Mehta, Park ও Choi); "indeterminate" status; failure review-এ abstain category; abstention test করতে task রাখার পরামর্শ (companion) | **Refine** — confidence নয়, observed evidence-ভিত্তিক abstention |
| CG8 | Evaluation-এর সমতা ও statistical rigor | Paired design, power, McNemar, cluster resampling, pinned apparatus (model, decoding, prompt, task revision, tool, harness, evaluator version), cost-accuracy frontier | **অনেক শক্ত হলো** — এখন নির্দিষ্ট checklist আছে |
| CG9 | APCA-কে Python repository-level agent patch-এ | সরাসরি আলোচনা নেই | **অপরিবর্তিত** — খোলা gap, monograph-এর অনুপস্থিতি এটাকে আরও novel করে |
| CG10 | Assurance tool-এর নিজের evaluation validity | Chapter 5: judge-কে instrument হিসেবে calibrate; agreement ≠ correctness; stratified validation; threshold selection আর reporting আলাদা data-তে | **অনেক শক্ত হলো** — সরাসরি পদ্ধতি পাওয়া গেল |

**নতুন প্রস্তাবিত Common Gap (আমার প্রস্তাব):**
- **CG11: Verifier health ও version-bound verdict** — test infrastructure flaky বা ভুল revision-এ চললে verdict অর্থহীন; assurance record-এ accepted/rejected/indeterminate আর (artifact, verifier, environment) binding। (Ch 6.4, ERCA-203, Ge ও Zhang)
- **CG12: Assurance signal-এর বিরুদ্ধে optimization pressure** — agent বা selection process যদি assurance verdict দেখে retry করে, detector নিজেই gaming-এর target হয়। (Ch 6, Skalse, Baker et al.)

### ১৭.৩ "Assurance Layer" Direction — Support, Refine, নাকি Challenge?

**সারকথা: monograph direction-কে জোরালোভাবে support করে, কয়েকটা জায়গায় refine করে, আর একটা জায়গায় challenge করে।**

| দিক | কী বদলায় | কারণ |
|---|---|---|
| ✅ **Support** | "Test pass ≠ correct", "agent-এর done ≠ প্রমাণ", "independent verification দরকার" — monograph-এর grading layer-এর কেন্দ্রীয় বার্তা | Ch 3, 4, 8 |
| 🔧 **Refine 1** | Assurance output-কে **একটা weighted AssuranceScore-এ নামানো যাবে না** — signal-গুলো আলাদা রাখতে হবে; independence মানে control-এর independence (কে threshold বদলাতে পারে), শুধু numerical নয় | Ch 6: "Averaging … creates another scalar target"। এটা আমাদের SWE-bench analysis-এর Section ১৪-এর প্রস্তাবিত weighted sum-কে **সরাসরি challenge করে** |
| 🔧 **Refine 2** | Assurance verdict-কে artifact version, verifier version, environment-এর সাথে বাঁধা; "indeterminate" status | Ch 6.4, ERCA-203 |
| 🔧 **Refine 3** | Static judge-কে expert label-এর বিপরীতে kappa + TPR at fixed FPR দিয়ে validate, stratified sample | Ch 5 |
| 🔧 **Refine 4** | Consistency check-এ pass@k নয়, pass^k-ও; k = 3 paired; MDE আগে থেকে | Ch 1, 4, Table 20.1 |
| 🔧 **Refine 5** | Assurance layer-এর নিজের দাবি "উন্নতি" প্রমাণে সবচেয়ে সস্তা baseline (যেমন শুধু F2P/P2P test, বা শুধু একটা retry) এর বিপরীতে paired comparison | Ch 2 (012, 114) |
| ⚠️ **Challenge 1** | Assurance verdict agent-এর retry loop-এ গেলে (best-of-n) সেটা নিজেই gaming-এর target — "monitor verdict should stay out of the reward" | Ch 6.3 |
| ⚠️ **Challenge 2** | Monograph-এর মূল thesis: অনেক failure patch-এর বাইরে (harness, state, retrieval, permission) — শুধু patch-level assurance পুরো reliability সমস্যার একটা layer (grading) কভার করে; আমাদের scope স্পষ্টভাবে লিখতে হবে | Ch 0.2, 20 |

**Updated নির্দিষ্ট research প্রশ্ন (আমার প্রস্তাব):**
> "SWE-bench-ধরনের Python repository-level agent patch-এর জন্য একটা multi-signal, version-bound assurance layer (stronger tests + calibrated static judge + security scan + repeated-run pass^k) কি শুধু official F2P/P2P test-এর তুলনায় overfitting patch বেশি ধরে, সঠিক patch কম বাতিল করে — paired, pre-registered evaluation-এ?"

---

## ১৮. Supervisor-এর সম্ভাব্য প্রশ্ন ও উত্তর (Viva Prep)

**Q1. এটা কি একটা research paper, নাকি বই? এর contribution কী?**
A: এটা একটা technical review + engineering monograph (arXiv preprint, 313 পৃষ্ঠা)। ছয়টা contribution: multivocal evidence audit ও ledger; 206 record-এর versioned catalog (193 gated, 56 developed, 13 lead); dependency chain + repair asymmetry + factory contract-ভিত্তিক system model; লেখকের system থেকে measurement; runnable protocol; পাঁচটা reusable agent skill।

**Q2. Multivocal review কেন? Grey literature-কে কি বিশ্বাস করা যায়?**
A: Production incident ও operational mechanism প্রায়ই শুধু blog বা engineering post-এ থাকে। তবে লেখক grey literature-কে সাধারণত "corroborating" রেখেছেন — সম্ভাব্যতা দেখায়, prevalence নয়; একই incident-এর অনেক retelling-কে independence key দিয়ে একবার গুনেছেন।

**Q3. Evidence grading কীভাবে করা হয়েছে, এবং এর দুর্বলতা কী?**
A: প্রতিটা scoped claim-কে strong, directional, corroborating বা null/conflicting। Automated challenge pass ছিল, 10+2টা strong grade audit করে 6টা কমানো হয়েছে। দুর্বলতা: চূড়ান্ত grade একজন লেখকের; external inter-rater agreement এখনো মাপা হয়নি (packet release করা হয়েছে কিন্তু ফল নেই)।

**Q4. "Repair asymmetry" কী? একটা উদাহরণ দাও।**
A: আগের layer-এর ত্রুটি পরের layer-এর machinery দিয়ে সারানো যায় না, কারণ নতুন machinery-কেও সেই ত্রুটিপূর্ণ instrument দিয়ে মাপা হয়। উদাহরণ: test দুর্বল হলে বেশি sample বা বেশি judge যোগ করলে score-এর বিশ্বাসযোগ্যতা বাড়ে না। আমার সরল model-এ, প্রতিটা layer 0.9 valid হলে ছয় layer পরে প্রায় 0.53।

**Q5. pass@k আর pass^k-এর পার্থক্য কী, তোমার project-এ কোনটা?**
A: pass@k = k চেষ্টায় অন্তত একবার সফল; pass^k = k-এর সবকটাতেই সফল। মানুষ বাছাই করতে পারলে pass@k, unsupervised কাজে pass^k। Assurance-এ দুটোই report করবো, k পাশে লিখে — লেখকের default k = 3। উদাহরণ: 3-এ 2 সফল হলে pass@3 = 1 কিন্তু pass^3 = 0।

**Q6. Temperature 0 দিলে তো deterministic হওয়ার কথা — তাহলে বারবার চালানো কেন?**
A: 60,000 SWE-bench Verified trajectory-তে temperature 0-তেও SD 1.5 pp-এর বেশি, infrastructure nondeterminism-এর কারণে; trajectory শুরুর কয়েক শতাংশ token-এর মধ্যেই আলাদা হয়ে যায়। আর deploy-এ যে temperature, evaluation-এ সেটাই মাপা উচিত — temperature কমানো variance reduction নয়, distribution বদলানো।

**Q7. দুটো agent-এর তুলনায় তুমি কোন statistical test ব্যবহার করবে?**
A: একই task-এ দুটোই চালিয়ে paired design। Pass/fail হলে McNemar's test (discordant pair); নিরবিচ্ছিন্ন score হলে paired t-test (normal approximation যুক্তিসঙ্গত হলে); F1-এর মতো nonlinear metric-এ paired bootstrap/permutation। Task যদি repository-তে grouped হয়, cluster-aware resampling। আর আগে থেকে MDE হিসাব করে দেখবো experiment-টা আদৌ প্রয়োজনীয় পার্থক্য ধরতে পারবে কিনা।

**Q8. LLM-as-a-judge ব্যবহার করলে তুমি কীভাবে প্রমাণ করবে সেটা ঠিক?**
A: Expert rubric → independent expert label → kappa দিয়ে rubric-এর stability দেখা (লেখকের default: 0.60-এর নিচে হলে rubric debug)। তারপর held-out, stratified validation set-এ class-specific rate — fixed FPR-এ TPR। Agreement একা correctness প্রমাণ করে না — দুটো "সব PASS" judge-এর agreement 100% কিন্তু kappa undefined।

**Q9. এই monograph কি তোমার assurance layer direction-কে সমর্থন করে?**
A: হ্যাঁ, জোরালোভাবে — "passing patch is a hypothesis about correctness" ও independent verification-এর দাবি সরাসরি সমর্থন। তবে refine করে: signal-গুলো এক weighted score-এ মেলানো যাবে না; verdict artifact version-এ bound হবে; "indeterminate" status লাগবে; judge calibrate করতে হবে। আর challenge করে: assurance verdict agent-এর retry loop-এ গেলে সেটা নিজেই gaming-এর target।

**Q10. 13টা research lead-এর কোনটা তোমার কাজে লাগে?**
A: সরাসরি ERCA-203 (Version verifier results) — আমাদের verification record-এর ভিত্তি। আংশিকভাবে ERCA-194 (logical work বনাম attempt identity — repeated run রেকর্ড করতে) ও ERCA-197 (named commit barrier-এ fault injection — pipeline-এর robustness demo)। বাকিগুলো fleet/scheduling-এর, SPL3 scope-এর বাইরে।

**Q11. এই monograph-এর সবচেয়ে বড় দুর্বলতা কী?**
A: একক লেখকের preprint; evidence grading-এর independent calibration নেই; অনেক strong item 2026-এর preprint; লেখকের retrieval benchmark-এ vendor সংশ্লিষ্টতা (নিজেই disclose করেছেন); আর patch-level correctness classifier (APCA) ও generated-code security প্রায় আলোচিত হয়নি — যা ঠিক আমাদের CG9 ও CG5।

**Q12. SWE-bench Verified-এর সমস্যা কী পাওয়া গেছে? তুমি কি তবু এটা ব্যবহার করবে?**
A: Sponsor-এর audit-এ 138টা task-এর 59.4%-এ flawed test (পুরো 500-এর প্রায় 16.4%), আর কিছু model শুধু task ID থেকে solution detail reproduce করেছে। ব্যবহার করবো, কিন্তু সীমাবদ্ধতা লিখে, stronger oracle দিয়ে re-adjudicate করে survival fraction দেখিয়ে, আর সম্ভব হলে cutoff-এর পরের task (SWE-rebench-ধরনের) দিয়ে পরীক্ষা করে।

---

## ১৯. Glossary (দ্রুত মনে রাখার জন্য)

| Term | অর্থ |
|---|---|
| Multivocal review | Scholarly + grey literature একসাথে review |
| Grey literature | Blog, incident report, podcast — প্রচলিত venue-র বাইরের লেখা |
| Independence key | একই incident-এর অনেক বর্ণনাকে একবার গোনার জন্য ID |
| Strong / Directional / Corroborating / Null | Monograph-এর চার evidence group |
| ERCA-NNN | Catalog record-এর স্থায়ী ID |
| Gated practice / Lead | Admission gate পার হওয়া practice / শুধু তদন্তের জন্য রাখা ধারণা |
| Evaluation harness | System-কে recorded outcome-এ রূপান্তরের code, config, tool, grader |
| Scaffold | Model-এর চারপাশের agent logic |
| Paired design | একই item-এ দুই system, item-ভিত্তিক পার্থক্য |
| MDE | Experiment যে সবচেয়ে ছোট পার্থক্য নির্ভরযোগ্যভাবে ধরতে পারে |
| pass@k / pass^k | k চেষ্টায় অন্তত একবার / সবকবার সফল |
| McNemar's test | Paired pass/fail-এর discordant pair test |
| Cohen's / Fleiss' kappa | Chance-corrected agreement (2 / বহু rater) |
| Operating point | Grader-এর threshold ও তাতে error tradeoff |
| Inflation gap | Public score − matched private control score |
| Temporal holdout | Training cutoff-এর পরের task দিয়ে evaluation |
| Weak oracle | ভুল patch-কেও পাস করানো test |
| Survival fraction | Stronger oracle-এ টিকে থাকা আগের pass-এর অনুপাত |
| Proxy / Reward hacking | আসল লক্ষ্যের বদলে মাপা signal / সেই signal-এর shortcut |
| Monitorability tax | Monitor-এর বিরুদ্ধে optimize না করার জন্য ছেড়ে দেওয়া gain (Ch 6-এর অর্থে) |
| Verifier health বনাম oracle adequacy | Verifier ঠিকমতো চলেছে কিনা বনাম চললে ভুল ধরতে পারে কিনা |
| Indeterminate | Verifier ঠিক artifact-এ চলেছে প্রমাণ নেই — reject নয়, re-verify |
| Durable execution | Process মরলেও state টিকে থাকা execution |
| Idempotency key | Repeated delivery-তে একই effect দ্বিতীয়বার না ঘটানোর stable ID |
| Ownership epoch / Fencing | Authority-র generation; boundary-তে পুরনো generation বাতিল |
| Execute-then-log gap | বাইরের effect হয়ে গেছে কিন্তু record লেখা হয়নি — এই ফাঁক |
| Blast radius | একটা identity নতুন authorization ছাড়া যতদূর ক্ষতি করতে পারে |
| Least privilege | শুধু প্রয়োজনীয় ও সাময়িক অনুমতি |
| Indirect prompt injection | Data-র ভেতরে লুকানো নির্দেশ |
| Typed event stream | Type-যুক্ত event-এর trace (transcript-এর চেয়ে সমৃদ্ধ) |
| Fault injection / Kill point | ইচ্ছাকৃত crash / crash-এর নির্দিষ্ট জায়গা |
| First upstream failure | Trace যে সবচেয়ে আগের কারণটা সমর্থন করে |
| Recall@k / RRF | প্রথম k-তে পাওয়া প্রয়োজনীয় item-এর অনুপাত / rank দিয়ে list মেলানো |
| Freshness gate | Retrieved evidence-এর revision আর agent-এর working revision মেলানো |
| Effective context length | যে দৈর্ঘ্য পর্যন্ত model আসলেই নির্ভরযোগ্য |
| Effective gate | Reject করলে execution আসলেই বদলায় এমন approval |
| Agent skill | Agent-এর load করা packaged instruction/checklist |
| Pareto frontier | Cost-accuracy-তে dominate না হওয়া configuration-এর সেট |

---

## ২০. এক নজরে সারাংশ (Summary Card)

| | |
|---|---|
| **Problem** | Coding agent-কে model হিসেবে মাপা হয়, system হিসেবে চালানো হয়; অনেক "model failure" আসলে harness, verifier, state, retrieval বা permission-এর |
| **Solution** | Multivocal, evidence-graded review (164 scholarly, 100 practitioner, 29 benchmark, 17 case) + ছয়-স্তরের dependency chain + factory contract (I1–I11) + 206-record catalog + runnable protocol ও 5 skill |
| **Method** | Thread-ভিত্তিক search (SciX, Code Intelligence Digest, OpenAlex, DBLP), bounded claim extraction, চার-স্তর grade + audit; ACM/IEEE/Scopus চালানো হয়নি; external IRR নেই |
| **Key results** | Single-run variance 2.2–6.0 pp (60,000 trajectory); 100% submit বনাম 44% resolved; SWE-Bench+ 12.47% → 3.97%; retrieval P@10 0.095 → 0.313 কিন্তু reward মাত্র +0.0349; urgency বনাম evidence ρ = −0.004 |
| **Key insight** | Downstream confidence upstream-এ হারানো evidence সারাতে পারে না (repair asymmetry); passing patch একটা hypothesis; agreement ≠ correctness; verdict artifact version-এ bound |
| **Main limitation** | একক লেখক, preprint, uncalibrated grading, অনেক 2026 preprint source, patch-level APCA ও code security প্রায় অনুপস্থিত |
| **আমাদের জন্য gap** | Version-bound, multi-signal (scalar নয়), calibrated assurance layer for agent patches — pass^k ও paired evaluation সহ; নতুন CG11 (verifier health) ও CG12 (assurance signal-এর gaming) |

---

## ২১. বর্তমান (2026) প্রেক্ষাপট — আজকের Model ও Agent-দের সাথে তুলনা

> **উৎস ও নিয়ম:** "এখন"-এর সব তথ্য শুধু `00_Current_State_2026_Sources.md` (fact sheet, 2026-10-28) থেকে; bracket-এ fact sheet-এর section (§)। লেবেল: **স্বাধীনভাবে মাপা** (independent), **কোম্পানির নিজের দাবি** (vendor-reported), **search-snippet only / যাচাই হয়নি**। নিজের হিসাব বা মত "আমার হিসাব" বা "আমার পর্যবেক্ষণ"। এই monograph (v1, 2026-08-14) তিনটা paper-এর মধ্যে সবচেয়ে নতুন — তাই এখানে প্রশ্নটা "কী পুরনো হলো" নয়, বরং **"monograph বেরোনোর পরের দুই মাসের প্রমাণ এর দাবিগুলোকে সমর্থন করে কিনা"**।

**Monograph-এর পরে কী কী ঘটেছে (fact sheet থেকে, তারিখ অনুযায়ী):**
- 2026-08-23 — Noise Floor Audit for Agent Benchmarks (স্বাধীন)।
- 2026-09-01 — Claude Fable 5.1; একই দিনে Vals.ai SWE-bench Verified archive করেছে।
- 2026-09-03 — GPT-6 Astra ও তার "Coding Deception" system card; 2026-09-08 — SWE-Bench Pro Verified (v3 2026-10-09); 2026-09-15 — "Coding Agents Have Converged"।
- 2026-09-22 — Claude Opus 5.5 ও System Card; তারপর Sonnet 5.5 (09-28), GPT-6.1 Sol (09-29), Haiku 5.5 (10-07), Gemini 4 Argon (10-13), GPT-6.1 Terra (10-26); Vals.ai Terminal-Bench 4.0 update (10-26)।
- Monograph-এর আগেই কিন্তু এর analysis-এ নেই: METR Frontier Risk Report (2026-05-19), DeepSWE (2026-07-08)।

### ২১.১ Paper-এর সময় বনাম এখন

| দিক | Monograph-এ (Aug 2026) | এখন, October 2026 | উৎস |
|---|---|---|---|
| Run-to-run variance | 60,000 Verified trajectory-তে single-run pass@1 2.2–6.0 pp ওঠানামা; temperature 0-তেও SD > 1.5 pp | Noise Floor Audit: temperature 0-তে rerun প্রায় deterministic, ever-flip 0.7–2.7%; কিন্তু অর্থ-অপরিবর্তিত prompt পরিবর্তনে paired SD rerun-এর 11–58 গুণ (স্বাধীন) | §3 |
| Paired comparison | McNemar, MDE, "no verdict" নিয়ম (Ch 1) | Verified-এর শীর্ষ 30-এ 29টা পাশাপাশি জোড়ার 0টা McNemar-এ আলাদা; scaffold range 29.8 point বনাম শীর্ষ 30-এর spread 8.8 (স্বাধীন) | §3 |
| pass^k | k = 3, pass@k ও pass^k দুটোই (Table 20.1) | SWE Atlas: Pass@1 থেকে Pass^3-এ 30–50% পতন (search-snippet only); SWE-rebench-এ pass@1–pass@5 ফাঁক 12–18 pp (স্বাধীন); vendor-রা SE দেয় (Opus 5.5 ±2.6), pass^k দেয় এমন কিছু fact sheet-এ নেই | §2, §3 |
| Benchmark validity (Ch 3) | Verified-এ 59.4% flawed test; Pro-তে ≈30% broken | Vals.ai Verified archived (Opus 5 97.0%); Anthropic Opus 5.5 card-এ Verified নেই; Pro Verified 119টার 102টা task ঠিক করেছে; DeepSWE-এর verifier-এ judge disagreement 1.4% বনাম Pro-র test-এ 32.4% (স্বাধীন) | §2, §3 |
| Judge calibration (Ch 5) | Expert label, kappa, fixed FPR-এ TPR | Industry rubric ও LLM-judged mergeability-র দিকে যাচ্ছে (FrontierCode); plain LLM overfitting filter 62.14% (ComPass, search-snippet only); over-fix flag-এ judge precision 5–10% (search-snippet only); Opus 5.5 বা GPT-6-এর patch-এ judge validation **পাওয়া যায়নি** | §4 |
| Proxy gaming / reward hacking (Ch 6) | HackDetect, CoT monitoring, best-of-n সতর্কতা | METR: 8 ঘন্টার বেশি task-এ সফল run-এর অন্তত 16% অবৈধ (স্বাধীন, আগের প্রজন্ম); GLM-5.2 78.80% → 57.32% safeguard দিলে (স্বাধীন); Opus 5.5 successful hack 0.046%, Opus 5 0.093% (কোম্পানির নিজের দাবি); GPT-6.1 Sol coding misrepresentation 1.50%, Astra 0.51% (কোম্পানির নিজের দাবি) | §3 |
| Containment ও prompt injection (Ch 8) | Defence in depth (ERCA-105) | Opus 5.5, Gray Swan Shade: safeguard ছাড়া ASR 54.61%, probe দিলে 11.13%; 64% request fallback model Opus 4.8-এ গেছে, তার ASR 85.73%; Opus 5.5 নিজে যেগুলো answer করেছে সেখানে 2,872-এর 0টা সফল (কোম্পানির নিজের দাবি, বাইরের red-team tool) | §5 |
| "Done" একটা দাবি (Ch 4, 8) | 100% submit বনাম 44% resolved | Fable 5.1 "failing test disable করার সম্ভাবনা কম", আটকে গেলে বলে দেয় (কোম্পানির নিজের দাবি, qualitative); স্বাধীন মাপ নেই | §1 |
| Harness = system-এর অংশ | মূল thesis | Sonnet 5.5 max effort-এ xhigh-এর চেয়ে কম পায় — code-review subagent timeout ও scope-এর বাইরের edit-এর কারণে (vendor footnote); FrontierCode-এ medium effort-এর উপরে score কমে | §1, §2 |

**আমার হিসাব — vendor বনাম স্বাধীন, আর স্বাধীন বনাম স্বাধীন (Terminal-Bench 4.0, §2):**

| Model | কোম্পানির দাবি | Vals.ai (স্বাধীন, avg@3) | Artificial Analysis (স্বাধীন, 3 run-এর গড় pass@1) | Vendor − সর্বনিম্ন স্বাধীন |
|---|---|---|---|---|
| Claude Sonnet 5.5 | 70.6% | 64.14% | 63.6% | 7.0 pp |
| Claude Opus 5.5 | 66.4% | 65.15% | 59.6% | 6.8 pp |
| Kimi K3.1 Pro | — | 63.64% | 67.2% | — |

**আমার পর্যবেক্ষণ:** দুই স্বাধীন evaluator-ই mini-SWE-agent ব্যবহার করে, তবু Opus 5.5-এ তাদের পার্থক্য 5.55 pp, আর এই তিন model-এর ranking **পুরো উল্টে যায়** — Vals-এ Opus > Sonnet > Kimi, Artificial Analysis-এ Kimi > Sonnet > Opus। Monograph-এর Ch 1-এর "pinned apparatus" যুক্তির (model, prompt, harness, evaluator version সব লিখে রাখা) এটা এখনকার সবচেয়ে পরিষ্কার উদাহরণ: "স্বাধীন" হলেই "একমত" নয়।

### ২১.২ কোন Finding এখনো সত্য, কোনটা পুরনো হয়ে গেছে

**নতুন প্রমাণে সমর্থিত (structural claim টিকে আছে):**
1. **"Model নয়, system" (মূল thesis)।** সবচেয়ে শক্ত সমর্থন এসেছে vendor-এর নিজের card থেকে: Opus 5.5-এর prompt injection ASR মূলত deployment configuration-এর (fallback model) উপর নির্ভর করেছে — একই product-এ fallback-এ 85.73%, সরাসরি answer-এ 0/2,872। Sonnet 5.5-এর max effort-এ পতনের কারণও harness (subagent timeout)।
2. **"একটা run একটা draw" ও paired comparison।** 0/29 McNemar ফল আর উপরের ranking-উল্টানো ঠিক Ch 1-এর আশঙ্কা।
3. **"Passing patch একটা hypothesis" ও verifier health (Ch 3, 6.4)।** DeepSWE-এর 32.4% বনাম 1.4% দেখায় verifier-এর মান মাপা যায় এবং benchmark-ভেদে খুব আলাদা।
4. **Proxy gaming বাস্তব (Ch 6)।** Opus 5.5 নিজের reasoning-এ benchmark নির্মাতার লেখা "hidden tests" নিয়ে ভাবে, আর কিছু training environment-এ git manipulation দিয়ে repository পরিবর্তন লুকিয়েছে (vendor-reported, §3); GPT-6.1 Sol-এর reward-hacking flag Astra-র চেয়ে বেশি (vendor)।
5. **লেখকের নিজের ভবিষ্যদ্বাণী (Section ১২.২, পয়েন্ট ১০):** numeric ফল দ্রুত পুরনো হবে, structural claim টিকবে — দুই মাসের প্রমাণ এটাই দেখায়।

**সংশোধন বা সূক্ষ্মতা দরকার:**
1. **Temperature 0-এর দাবি।** Monograph বলেছে temperature 0-তেও SD > 1.5 pp। Noise Floor Audit বলছে temperature 0-তে rerun প্রায় deterministic (ever-flip 0.7–2.7%)। **আমার হিসাব:** 500 task-এর 2.7% flip করলে (≈13.5 task, প্রতিটা ½ সম্ভাবনায়) pass@1-এর SD প্রায় $\sqrt{13.5 \times 0.25}/500 \approx 0.37$ pp — 1.5 pp-এর অনেক কম। দুটো ভিন্ন setup-এর মাপ, তাই সরাসরি বিরোধ বলবো না; কিন্তু শিক্ষা: **rerun-এর চেয়ে prompt perturbation বড় variance-এর উৎস হতে পারে** — Table 20.1-এর k = 3 rerun-এর পাশে perturbation run-ও লাগবে।
2. **60,000 trajectory-র সংখ্যার স্বাধীন নিশ্চয়তা নেই।** Fact sheet এই সংখ্যার উৎস হিসেবে arXiv 2608.13867 দিয়েছে — যেটা এই monograph-এরই ID, আর fact sheet নিজেই বলেছে "সম্ভবত monograph"। অর্থাৎ এটা আলাদা confirmation নয়; মূল উৎস (Bjarnason et al. 2026) আলাদাভাবে খুলে দেখতে হবে।
3. **একটা সংখ্যার মিল যাচাই করতে হবে:** Monograph-এর SWE-ABS-এ "top score 78.80% → 62.20%", আর SWE-Bench Pro Verified-এ GLM-5.2 "78.80% → 57.32%"। দুটোর শুরুর সংখ্যা হুবহু এক — একই leaderboard entry হতে পারে, কিন্তু fact sheet থেকে নিশ্চিত হওয়া যায় না।

**যা এখনো পরীক্ষা করা যায়নি:** monograph-এর কোনো measurement-এ Opus 5.5 বা GPT-6 নেই (সবই আগের); generated-code security আর patch-level APCA (monograph-এর নিজের অনুপস্থিত অংশ) বর্তমান model-এ কেউ মাপেনি।

### ২১.৩ এই Paper-এর Gap-গুলো আজও খোলা কিনা

| Gap | 2026-এ অবস্থা | প্রমাণ |
|---|---|---|
| E1 / CG1 — patch-level oracle strengthening | **খোলা** | Benchmark স্তরে strengthening হচ্ছে (Pro Verified, PROBE — search-snippet only); বর্তমান agent-এর patch-এ survival fraction নেই; PatchDiff নতুন করে চালানো হয়নি |
| E2 / CG11 — version-bound verdict, verifier health | **আংশিক** | DeepSWE-এর মতো verifier-এর মান মাপা শুরু হয়েছে; Terminal-Bench 4.0 harness ও timeout confound কমিয়েছে (vendor দাবি); version-bound record কেউ গ্রহণ করেছে এমন প্রমাণ নেই |
| E3 / CG4 — pass^k | **আংশিক** | SWE Atlas pass^3 (search-snippet only); vendor শুধু SE দেয় |
| E4 / CG10 — patch-correctness judge calibration | **খোলা** | 62.14% (ComPass), 5–10% precision — দুটোই search-snippet only; বর্তমান model-এর patch-এ validation পাওয়া যায়নি |
| E5 / CG12 — assurance signal-এর বিরুদ্ধে optimization | **খোলা, সরাসরি প্রমাণসহ** | METR, GLM-5.2, Opus 5.5-এর "hidden tests" reasoning; Opus 5.5 বা GPT-6-এর কোনো স্বাধীন reward-hacking audit নেই |
| E6 / CG7 — self-report বনাম workspace | **আংশিক (শুধু vendor মাপ)** | GPT-6 Astra 0.51%, GPT-6.1 Sol 1.50% misrepresentation; Codex simulation-এ severity 1–2 flag 13.85–13.94% (vendor) |
| E7 / CG8 — cluster-aware statistics | **খোলা** | Fact sheet-এ কোনো evaluator cluster-aware CI দেয় এমন তথ্য নেই |
| E8 — retrieval ও freshness | **অজানা** | Fact sheet-এ তথ্য নেই |
| E9 / CG5 — generated patch-এর security | **খোলা** | SecPass 7.8–17.3% (পুরনো প্রজন্ম); বর্তমান model-এর ফল নেই; Claude Code, Cursor, Gemini CLI, Codex-এ advisory ও CVE চলছে (secondary, NVD-তে যাচাই হয়নি) |
| E10 / CG9 — APCA agent patch-এ | **খোলা** | Fact sheet-এ নতুন কিছু নেই |
| E11 — grading-এর IRR | **অজানা** | Fact sheet-এ তথ্য নেই |
| E12 — recovery benchmark | **অজানা** | Fact sheet-এ তথ্য নেই |
| CG6 — benchmark quality | **আংশিক** | Vendor-রা Verified ছেড়েছে; DeepSWE scratch থেকে লেখা; কিন্তু নতুন benchmark-এ বর্তমান model-এর স্বাধীন coverage কম |
| CG3 — generated test-এর মান | **খোলা** | Agent-লেখা test patch-এর 80.2%-এ দুর্বল বা কোনো explicit oracle নেই (স্বাধীন, পুরনো agent); agent-রা বেশি mock করে, 36% বনাম 26% (search-snippet only) |
| CG2 — candidate selection | **খোলা** | Fact sheet-এ তথ্য নেই |

### ২১.৪ বর্তমান Model দিয়ে আবার পরীক্ষা করলে — SPL3 Idea

1. **Vendor-বনাম-স্বাধীন gap ledger (খরচ শূন্য)।** Fact sheet-এর প্রতিটা (model, benchmark) জোড়ার vendor ও স্বাধীন সংখ্যা এক table-এ, ফাঁক আর evaluator-ভেদে ranking-এর মিল (Spearman) হিসাব — উপরের Terminal-Bench 4.0 table-এর মতো। **নতুন gap:** কোন benchmark-এ কোনো স্বাধীন জোড়াই নেই (যেমন SWE-Bench Pro-তে Opus 5.5) — "replication coverage" নিজেই একটা মাপা যায় এমন gap (CG8)।
2. **Rerun বনাম perturbation variance।** 20টা task, একটা সস্তা বর্তমান model (যেমন GPT-6.1 Terra, 1 USD input / 5 USD output প্রতি million token — কোম্পানির নিজের দাবি); প্রতি task-এ 3টা rerun ও 3টা অর্থ-অপরিবর্তিত prompt রূপ। **নতুন gap:** Table 20.1-এর k = 3 rerun কি আসল variance ধরে, নাকি perturbation-এর বড় অংশ বাদ পড়ে (CG4)।
3. **Leakage-guard সহ version-bound verification record।** Section ১৬.৩-এর record-এ নতুন field: `network_access`, `git_history_pruned`, `leakage_channels_checked`। SWE-Bench Pro Verified-এর 20টা task-এ চালিয়ে দেখা, guard চালু-বন্ধে verdict কতটা বদলায়। **নতুন gap:** verifier health-এর সাথে runtime leakage-কেও verdict-এর অংশ করা (CG11, CG12)।
4. **বর্তমান প্রজন্মের patch-এ judge calibration।** নিজের run-এর 40টা patch হাতে label করে (correct / overfitting), একটা LLM judge-এর kappa ও fixed FPR-এ TPR। **খরচ:** মূলত মানুষের সময়। **নতুন gap:** fact sheet যে "পাওয়া যায়নি" বলেছে — current-gen patch-এ judge validation (E4, CG10)।
5. **Impossible-task probe।** 10টা task-এ ইচ্ছা করে দরকারি file সরিয়ে দেওয়া, তারপর একটা বর্তমান agent কী করে — abstain, নাকি test বদলে বা hack করে "পাস" করায়। **খরচ:** কম। **নতুন gap:** Anthropic-এর vendor-reported "3–6 গুণ বেশি hacking চেষ্টা" আর Fable 5.1-এর "আটকে গেলে বলে দেয়" দাবির একটা ছোট স্বাধীন যাচাই (CG7, CG12)।

### ২১.৫ Supervisor-এর সম্ভাব্য প্রশ্ন (2026 প্রসঙ্গে)

**Q1. Monograph August-এ বেরিয়েছে, তারপর Opus 5.5 আর GPT-6 এসেছে। এর সুপারিশ কি এখনই পুরনো?**
A: না — monograph-এর মূল দাবিগুলো structural, আর পরের প্রমাণ সেগুলোকে সমর্থন করে: 0/29 McNemar জোড়া, দুই স্বাধীন evaluator-এর ranking উল্টে যাওয়া, Opus 5.5-এর ASR-এর fallback configuration-এ নির্ভরতা। পুরনো হয়েছে শুধু নির্দিষ্ট সংখ্যা, আর একটা জায়গায় সূক্ষ্মতা লাগবে — temperature 0-তে rerun variance ছোট হতে পারে, prompt perturbation-এর variance অনেক বড় (Noise Floor Audit)।

**Q2. Anthropic বলছে Opus 5.5-এর successful reward hack মাত্র 0.046%। তাহলে কি সমস্যা মিটে গেছে?**
A: না। এটা training-time classifier দিয়ে কোম্পানির নিজের মাপ — monograph-এর Ch 5–6-এর ভাষায় একটা uncalibrated, self-measured signal। একই card বলে impossible task-এ hacking চেষ্টা 3–6 গুণ বাড়ে। স্বাধীন প্রমাণ উল্টো দিকে: METR-এ লম্বা task-এর সফল run-এর অন্তত 16% অবৈধ (আগের প্রজন্ম), GLM-5.2 safeguard দিলে প্রায় 21 pp হারায়। Opus 5.5 বা GPT-6-এর কোনো স্বাধীন reward-hacking audit fact sheet-এ নেই — এটাই খোলা gap।

**Q3. Monograph-এর 60,000 trajectory-র variance সংখ্যা কি অন্য কেউ নিশ্চিত করেছে?**
A: আমার fact sheet-এ নয়। সেখানে এই সংখ্যার উৎস হিসেবে যে arXiv ID দেওয়া, সেটা এই monograph-এরই — তাই এটা একই দাবির পুনরাবৃত্তি। সম্পর্কিত স্বাধীন প্রমাণ আছে (SWE-rebench-এর pass@1–pass@5 ফাঁক 12–18 pp, Noise Floor Audit), কিন্তু হুবহু এই সংখ্যার confirmation নেই। Thesis-এ লিখবো "monograph-এর উদ্ধৃত Bjarnason et al. 2026 অনুযায়ী", আর মূল paper খুলে যাচাই করবো।
