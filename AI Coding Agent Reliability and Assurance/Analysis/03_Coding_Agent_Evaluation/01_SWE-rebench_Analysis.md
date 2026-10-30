# Paper Analysis 01 (Eval): SWE-rebench — Automated Task Collection and Decontaminated Evaluation of SE Agents

> **Sub-domain:** Coding-Agent Evaluation & Reliability (Paper 01)
> **Analysis করেছে:** SPL3 — AI Coding Agent Reliability and Assurance
> **Paper file:** `Coding-Agent Evaluation & Reliability/NeurIPS-2025-swe-rebench-an-automated-pipeline-for-task-collection-and-decontaminated-evaluation-of-software-engineering-agents-Paper-Datasets_and_Benchmar.pdf`
> **আগে পড়ো:** Sub-domain 1, Paper 01 (SWE-bench) — issue/PR/commit, patch, F2P/P2P test, contamination, pass@k, saturation, Docker harness সেখানে ব্যাখ্যা করা আছে। Sub-domain 1, Paper 02 (SWE-agent) — agent scaffold, ReAct loop, ACI command (`open`, `edit`, `search_file`)। Sub-domain 1, Paper 04 (Agentless) — "agentless" pipeline ধারণা। Sub-domain 1 ও 2 Summary — common gap **CG1–CG10** আর প্রস্তাবিত "Assurance Layer for Agent Patches"।

---

## ০. Paper-এর পরিচয় (Bibliographic Info)

| বিষয় | তথ্য |
|---|---|
| **Title** | SWE-rebench: An Automated Pipeline for Task Collection and Decontaminated Evaluation of Software Engineering Agents |
| **Authors** | Ibragim Badertdinov, Alexander Golubev, Maksim Nekrashevich, Anton Shevtsov, Simon Karasik, Andrei Andriushchenko, Maria Trofimova, Daria Litvintseva, Boris Yangel (paper-এ "Equal contribution" footnote আছে) |
| **Institution** | Nebius (সব author) |
| **Venue** | 39th Conference on Neural Information Processing Systems (NeurIPS 2025) — **Track on Datasets and Benchmarks** (paper-এর প্রথম পাতার footer থেকে নিশ্চিত) |
| **Paper type** | **Dataset + Benchmark + Data pipeline paper** — নতুন agent বা algorithm নয়; বরং "task কারখানা" আর "নিরপেক্ষ পরীক্ষা কেন্দ্র" |
| **Artifacts** | (১) SWE-rebench dataset — 21,336টা executable Python task, 3,468টা repository (Hugging Face: `nebius/SWE-rebench`); (২) evaluation code (GitHub: `SWE-rebench/SWE-bench-fork`); (৩) SWE-rebench benchmark — 294টা task, 169টা repository; (৪) continuously updated leaderboard (swe-rebench.com) |
| **পূর্বসূরি কাজ** | একই দলের SWE-bench Extra (Nebius blog, 2024) |
| **আমাদের domain-এ গুরুত্ব** | ⭐⭐⭐⭐⭐ — এই sub-domain-এর ভিত্তি paper। আমাদের **CG4 (run-to-run reliability), CG6 (contamination), CG8 (evaluation-এর সমতা ও statistical rigor), CG10 (assurance tool-এর leakage-মুক্ত evaluation)** — চারটার সাথেই সরাসরি যুক্ত। |

---

## ১. এক লাইনে Paper (TL;DR)

**SWE-rebench হলো একটা সম্পূর্ণ automated pipeline, যেটা GitHub থেকে নিয়মিত নতুন issue-PR জোড়া তুলে, LLM দিয়ে environment install করে, test চালিয়ে যাচাই করে 21,336টা executable SWE task-এর dataset বানায়; আর সেই "তাজা" task দিয়ে একটা centralized leaderboard চালায় যেখানে সব model একই scaffold-এ 5 বার চলে, SEM ও pass@5 report হয়, এবং model release-এর আগের task-এ পাওয়া score "সম্ভাব্য contaminated" হিসেবে চিহ্নিত হয়।**

### Supervisor-কে ৩০ সেকেন্ডে কীভাবে বলবো
> "Sir, SWE-bench 2023 থেকে public, তাই নতুন model-রা হয়তো এর task training-এ দেখে ফেলেছে — score মুখস্থ না দক্ষতা, বোঝা যায় না। তাছাড়া প্রতিটা দল নিজের scaffold, retry, best-of-N দিয়ে নিজের score report করে, তাই তুলনা ন্যায্য নয়। SWE-rebench এই দুই সমস্যার সমাধান দেয়: একটা automated pipeline প্রায় 4,50,000 issue-linked PR থেকে শুরু করে LLM দিয়ে install recipe বানায়, test চালিয়ে যাচাই করে 21,336টা task তৈরি করে। তারপর 2025-এর issue থেকে 294টা task নিয়ে একই ReAct scaffold-এ প্রতিটা model 5 বার চালায়। ফলাফল: DeepSeek-V3-0324 SWE-bench Verified-এ 39.7% কিন্তু তাজা SWE-rebench task-এ 21.3% — অর্থাৎ পুরনো benchmark-এর score কিছু model-এর ক্ষেত্রে ফোলানো হতে পারে। তবে এটা এখনো test-pass-ভিত্তিক — patch আসলে সঠিক কিনা (আমাদের CG1) সেটা এই paper দেখে না।"

---

## ২. Background — এই paper বুঝতে যা আগে জানা দরকার

### ২.১ আগের paper থেকে যা লাগবে (পুনরায় ব্যাখ্যা নয়)

| Concept | কোথায় ব্যাখ্যা আছে | এই paper-এ কীভাবে লাগে |
|---|---|---|
| GitHub issue, PR, base commit | Sub-domain 1, Paper 01, Section ২.১ | Task-এর কাঁচামাল — issue-linked merged PR |
| Patch / diff | Sub-domain 1, Paper 01, Section ২.২ | PR-কে solution patch আর test patch-এ ভাগ করা হয় |
| F2P / P2P test | Sub-domain 1, Paper 01, Section ২.৫ ও ৬.২ | Execution-based verification-এর তিনটা শর্ত (Section ৫.৪) |
| SWE-bench-এর 3-stage pipeline | Sub-domain 1, Paper 01, Section ৫.১ | SWE-rebench এটাকে automate ও scale করেছে (Section ৫.৬-এ পার্থক্য) |
| Data contamination | Sub-domain 1, Paper 01, Section ২.৯ ও ১২.২ | এই paper-এর মূল বিষয় — নিচে ২.১১-এ গভীরে |
| Pass@k, greedy decoding | Sub-domain 1, Paper 01, Section ২.১০ ও ৬.১০ | এখানে 5 run থেকে pass@5 |
| Benchmark saturation | Sub-domain 1, Paper 01, Section ২.১২ | Quality label দিয়ে কঠিন task বাছাই করে saturation কমানোর দাবি |
| SWE-bench Lite / Verified | Sub-domain 1, Paper 01, Section ১৭ | Verified-এর মানুষের করা annotation দিয়ে এখানে LLM classifier train করা হয়েছে; Verified-এর সাথে score তুলনা |
| Agent scaffold, ReAct loop, ACI command | Sub-domain 1, Paper 02 (SWE-agent) | Leaderboard-এর fixed scaffold-এর command (`open`, `goto`, `edit`, `search_file`, `submit`) দেখতে SWE-agent-এর ACI-র মতো (আমার পর্যবেক্ষণ) |
| Agentless pipeline | Sub-domain 1, Paper 04 | Install recipe বানাতে "agentless" (নির্দিষ্ট ধাপের) approach ব্যবহার |
| Run-to-run variance (17.94% ± 0.49, pass@6) | Sub-domain 1, Paper 02 ও Summary Section ৩.২ | এখানে প্রতিটা model 5 run, SEM ও pass@5 |
| Precision, Recall, F1, majority baseline | Sub-domain 2, Paper 03 (RePaCA), Section ২.১৯ ও ৬.১০ | Quality classifier-এর মূল্যায়ন (Table 4) |
| Data leakage ও temporal split | Sub-domain 2, Paper 01 (APR Survey) ও Summary CG10 | এই paper-এর "decontamination" আসলে একটা temporal split |

### ২.২ Automated Task Mining from GitHub — কী ও কেন
**Task mining** মানে মানুষের হাতে বাছাই না করে, program দিয়ে GitHub-এর বিশাল data থেকে স্বয়ংক্রিয়ভাবে "issue + সমাধান + test" জোড়া খুঁজে বের করা।
- **GitHub Archive (GH Archive):** একটা public project যেটা প্রতিদিন GitHub-এ ঘটা সব public event (issue খোলা, PR merge, comment ইত্যাদি) একটা JSON archive হিসেবে প্রকাশ করে। এখান থেকে issue-র description, discussion, linked PR, তৈরির তারিখ, label পাওয়া যায়।
- **Repository clone:** পুরো commit history সহ repository নিজেদের storage-এ clone করা হয় — এতে GitHub API-র rate limit (প্রতি ঘন্টায় সীমিত request) এড়ানো যায়, আর PR-এর commit থেকে patch বের করা ও version analysis সহজ হয়।
- **Issue-PR linking:** PR-এর title বা description-এ যদি লেখা থাকে যে এটা কোনো issue resolve করে (যেমন "fixes #24"), তাহলে দুটোকে জোড়া বাঁধা হয়।
- **Permissive license ও SPDX:** Permissive license (MIT, Apache-2.0, BSD ইত্যাদি) কোড পুনর্ব্যবহার ও পুনর্বিতরণের অনুমতি দেয়। **SPDX identifier** হলো license-এর standard নাম (যেমন `MIT`, `Apache-2.0`) — machine দিয়ে license চেনার উপায়।

### ২.৩ Solution Patch বনাম Test Patch; base / head / merge commit
- একটা PR-এর মোট পরিবর্তনকে দুই ভাগ করা হয়: **solution patch** (test নয় এমন file-এর পরিবর্তন — আসল fix) আর **test patch** (শুধু test file-এর পরিবর্তন — fix যাচাইয়ের test)। Agent পায় শুধু issue; solution patch লুকানো থাকে (gold patch), test patch evaluation-এ ব্যবহার হয়।
- **base_commit:** PR branch যেখান থেকে শুরু হয়েছে। **head_commit:** PR branch-এর শেষ commit। **merge_commit:** main branch-এ merge হওয়ার commit।
- SWE-bench patch বানাতো base আর merge commit-এর diff থেকে; মাঝখানে main branch-এ অন্য merge ঢুকলে সেই অপ্রাসঙ্গিক পরিবর্তনও patch-এ চলে আসে। SWE-rebench head_commit ব্যবহার করে এটা এড়ায় (Section ৫.৬)।

### ২.৪ Environment Setup Automation — Dependency, Version, Pinning
একটা Python project-এর test চালাতে হলে আগে সঠিক Python version, library (dependency) আর তাদের সঠিক version install করতে হয়।
- **Dependency-র উৎস file:** `requirements.txt`, `setup.py`, `pyproject.toml`, `environment.yml` (conda), README, Dockerfile, Makefile।
- **pip ও conda:** Python package manager। `pip install -e .[dev]` মানে project-কে "editable" mode-এ dev dependency সহ install করা।
- **Unpinned dependency:** `numpy` লেখা থাকলে আজ যে version install হবে, দুই বছর পরে অন্য version হবে — পুরনো code নতুন library-তে ভেঙে যেতে পারে। **Pinning** মানে exact version লিখে রাখা (`numpy==1.21.0`)।
- **pip freeze / conda env export:** একটা সফল environment-এ ঠিক কোন কোন version install আছে, তার সম্পূর্ণ তালিকা বের করার command। SWE-rebench সফল setup-এর পরে এটা রেকর্ড করে রাখে।
- **Semantic version ও major.minor:** version `1.2.3`-এ 1 = major, 2 = minor, 3 = patch। একই minor version-এর মধ্যে সাধারণত dependency সামঞ্জস্যপূর্ণ থাকে — তাই SWE-rebench task-গুলোকে `1.2`-এর মতো group করে একটা environment ভাগ করে নেয়।
- **git tag:** কোনো commit-কে version নাম দেওয়ার উপায় (যেমন `v1.2.3`)। এখান থেকে task-এর version অনুমান করা হয়।

### ২.৫ Container, Docker Image, buildah, Registry, Mirror
- **Container:** একটা হালকা, বিচ্ছিন্ন (isolated) পরিবেশ, যেখানে OS library, Python, dependency সব একসাথে থাকে — host computer-কে প্রভাবিত না করে code চালানো যায়। **Image** হলো container-এর "ছাঁচ" (template)।
- **Docker** সবচেয়ে পরিচিত container tool; **buildah** হলো image বানানোর আরেকটা tool (Docker daemon ছাড়াই)।
- **tmpfs:** RAM-এ রাখা file system — disk-এর চেয়ে দ্রুত, তাই build দ্রুত হয়।
- **Image registry ও PyPI/APT mirror:** নিজেদের server-এ image আর জনপ্রিয় package-এর কপি রাখা — বারবার internet থেকে নামাতে হয় না, আর বাইরের server বন্ধ থাকলেও কাজ চলে।
- কেন দরকার: SWE-bench-এর মতো evaluation-এ প্রতিটা task-এর জন্য reproducible environment লাগে (Sub-domain 1, Paper 01, Section ১২.২-এর "environment reproducibility" সমস্যা দেখো)।

### ২.৬ LLM-based Install Agent: Agentless Recipe বনাম Interactive Agent
- **Installation recipe:** একটা structured JSON — কোন Python version, কোন dependency file, কোন install command, কোন test command। একটা fixed bash script এই JSON পড়ে install চালায়।
- **Agentless approach (SWE-rebench-এর মূল পদ্ধতি):** LLM-কে কয়েকটা নির্দিষ্ট ধাপে কাজ দেওয়া হয় — (১) কোন file-এ install তথ্য আছে খোঁজো, (২) সেই file পড়ে recipe লেখো, (৩) fail করলে error log দেখে recipe ঠিক করো। LLM নিজে environment-এ command চালায় না। (Agentless-এর মূল ধারণা Sub-domain 1, Paper 04-এ।)
- **Interactive agent:** LLM সরাসরি Docker container-এ command চালায়, output দেখে, আবার চেষ্টা করে — মানুষের মতো "trial and error"। কখনো বেশি সফল, কিন্তু অনেক বেশি compute লাগে।
- **Iterative refinement:** ভুল হলে error log + পুরনো recipe LLM-কে দিয়ে সংশোধিত recipe চাওয়া — একটা feedback loop (Sub-domain 2, Paper 02 VRpilot-এর validation feedback loop-এর মতো ধারণা)।

### ২.৭ Execution-based Validation
Task "বৈধ" কিনা তা মানুষ দেখে না — **test চালিয়ে** যাচাই করা হয়: solution patch ছাড়া test fail করে, solution patch দিলে pass করে কিনা। এতে প্রমাণ হয় (ক) environment ঠিকমতো install হয়েছে, (খ) test আসলেই issue-টা ধরতে পারে, (গ) task solvable। শর্তগুলো Section ৫.৪ ও ৬.৩-এ।

### ২.৮ Flaky Test
যে test একই code-এ কখনো pass, কখনো fail করে — যেমন বাইরের API-তে call করা (server মাঝে মাঝে বন্ধ), বা floating-point সংখ্যা হুবহু সমান কিনা check করা। Flaky test দিয়ে reward বা score দিলে তা noise। SWE-rebench test কয়েকবার চালিয়ে, অন্তত একবার fail করলে task বাদ দেয়।

### ২.৯ Task Quality Annotation — মানুষ বনাম LLM
- **SWE-bench Verified-এর human annotation:** মানুষ annotator প্রতিটা task-এ দেখেছে issue পরিষ্কার কিনা, test ঠিক কিনা, কাজটা কত কঠিন (Sub-domain 1, Paper 01, Section ১৭)।
- **LLM-as-annotator:** এত বড় dataset (21K) মানুষ দিয়ে দেখা অসম্ভব, তাই মানুষের label দিয়ে একটা LLM fine-tune করে বাকি task-এ label "predict" করানো হয়।
- তিনটা label: **Issue Clarity** (issue পড়ে একজন developer সমাধান বুঝতে পারবে কিনা), **Task Complexity** (কত সময়/পরিশ্রম লাগবে; "high" মানে > 1 ঘন্টা), **Test Patch Correctness** (test আসলে intended fix যাচাই করে কিনা, নির্দিষ্ট implementation-এর উপর অতিরিক্ত নির্ভর না করে)।
- **Class imbalance ও majority baseline:** যদি validation-এ 80% task "পরিষ্কার" হয়, তাহলে একটা "বোকা" classifier যে সবসময় "পরিষ্কার" বলে, সেও 80% accuracy পাবে। তাই শুধু accuracy নয়, minority class-এর recall আর macro-average দেখতে হয় (Section ৬.১১)।
- **Weighted vs Macro average:** Macro = প্রতিটা class-এর metric-এর সাধারণ গড় (ছোট class-কে সমান গুরুত্ব); Weighted = class-এর আকার অনুযায়ী ওজন দিয়ে গড় (বড় class প্রাধান্য পায়)।

### ২.১০ Reinforcement Learning (RL) for SWE Agents — কেন Task Validity জরুরি
RL-এ agent চেষ্টা করে, environment থেকে **reward** পায় (এখানে: test pass = 1, fail = 0), আর reward বাড়ানোর দিকে শেখে (RL-এর মূল ধারণা Sub-domain 2, Paper 03 RePaCA-র Section ২.১১-এ)। যদি task-ই ত্রুটিপূর্ণ হয় (issue অস্পষ্ট, বা test এত নির্দিষ্ট যে সঠিক সমাধানও fail করে), তাহলে agent সঠিক কাজ করেও শাস্তি পায় — **ভুল reward signal**। এজন্য paper-এর মূল চিন্তা: task যেন শুধু agent-এর নিজের দুর্বলতার কারণেই unsolved থাকে, task-এর দোষে নয়।

### ২.১১ Contamination গভীরে: Decontamination ও Temporal (Rolling) Evaluation
- **Pre-training ও post-training:** LLM প্রথমে internet-এর বিশাল text-এ (GitHub সহ) train হয় (pre-training), তারপর instruction/RL দিয়ে আরও train হয় (post-training)। দুই ধাপেই benchmark-এর task বা তার সমাধান ঢুকে যেতে পারে।
- **Memorization বনাম generalization:** model যদি task-এর gold patch দেখে থাকে, তাহলে "মনে করে" লিখতে পারে — এটা আসল সমস্যা-সমাধান দক্ষতা (generalization) নয়।
- **তিনটা তারিখ — পার্থক্য বোঝা খুব গুরুত্বপূর্ণ:**

| তারিখ | মানে | কে জানে |
|---|---|---|
| **Task creation date** ($\tau$) | Issue (ও PR) কবে তৈরি হয়েছে | Benchmark নির্মাতা (GH Archive থেকে সঠিকভাবে) |
| **Knowledge / training cutoff** | Model-এর training data কোন তারিখ পর্যন্ত সংগ্রহ করা | Model নির্মাতা; প্রায়ই অস্পষ্ট বা প্রকাশ করা হয় না |
| **Model release date** ($d_m$) | Model কবে public হয়েছে | সবাই জানে |

  সাধারণত cutoff < release date। SWE-rebench **release date** ব্যবহার করে: যদি task-এর issue model release-এর আগে তৈরি হয়ে থাকে, সেই evaluation "potentially contaminated" চিহ্নিত হয়। (আমার পর্যবেক্ষণ: এটা "রক্ষণশীল" নিয়ম — cutoff আর release-এর মাঝের task-ও সন্দেহের তালিকায় যায়; আবার post-training-এ দেরিতে যোগ হওয়া data থাকলে release date-ই নিরাপদ সীমা।)
- **Decontamination:** test set থেকে training-এ দেখা সম্ভব এমন task সরিয়ে দেওয়া। এখানে পদ্ধতিটা **temporal** — model-এর তারিখের পরে তৈরি task-ই "পরিষ্কার"।
- **Rolling / continuous benchmark:** নিয়মিত নতুন task যোগ হয়; প্রতিটা model-কে তার release-এর পরের task-এ মাপা হয়। Function-level-এ LiveCodeBench এই ধারণা ব্যবহার করে বলে paper উল্লেখ করেছে; SWE-rebench এটা repository-level agent task-এ আনে।

### ২.১২ Scaffold ও Scaffolding Variability
- **Scaffold:** LLM-এর চারপাশের software — prompt, tool/command, loop, retry, history management (SWE-agent-এর ACI একটা scaffold; Sub-domain 1, Paper 02)।
- **ReAct:** প্রতিটা ধাপে model প্রথমে reasoning লেখে, তারপর একটা action (command) দেয়, environment-এর output দেখে আবার reasoning — "Reason + Act"।
- **Function calling বনাম text command:** কিছু model API-তে structured "function call" সমর্থন করে; SWE-rebench সবার জন্য সমান রাখতে এটা ব্যবহার করে না — model-কে নির্দিষ্ট text format-এ command লিখতে হয়।
- **Scaffold-এর trick:** best-of-N sampling (N বার চালিয়ে সেরাটা নেওয়া), retry, multi-agent, validation loop — এগুলো score বাড়ায়, কিন্তু তখন "model কতটা ভালো" আর "scaffold কতটা ভালো" আলাদা করা যায় না।
- **Implicit overfitting to benchmark:** scaffold যদি SWE-bench-এর subset-এ বারবার tune করা হয়, সেটা ঐ benchmark-এর বৈশিষ্ট্যে "fit" হয়ে যায় — নতুন task-এ একই ফল না-ও দিতে পারে।

### ২.১৩ Leaderboard Design: Self-reported বনাম Centralized
- **Self-reported leaderboard:** প্রতিটা দল নিজে চালিয়ে নিজের সংখ্যা জমা দেয়। সমস্যা: স্বাধীন যাচাই নেই; কেউ pass@N-কে pass@1 হিসেবে report করতে পারে, বা final test থেকে পাওয়া তথ্য অজান্তে ব্যবহার করতে পারে (paper-এর উদাহরণ)।
- **Centralized leaderboard (SWE-rebench):** benchmark দল নিজেই সব model একই নিয়মে চালায় — একই scaffold, prompt, context length, run সংখ্যা।

### ২.১৪ Stochasticity: Temperature, Seed ও Run-to-run Variance
Temperature > 0 হলে LLM-এর output random; ভিন্ন **random seed**-এ ভিন্ন trajectory। Agent-এর ক্ষেত্রে একটা ছোট পার্থক্য পরের সব ধাপ বদলে দেয়, তাই একই task একবার solve হয়, আরেকবার হয় না (Sub-domain 1 Summary, Section ৩.২)। একবারের run-এর score তাই অনিশ্চিত।

### ২.১৫ Resolved Rate, pass@1, pass@k ও pass^k
- **Resolved rate:** কত % task-এ agent-এর patch সব F2P ও P2P test pass করেছে (Sub-domain 1, Paper 01, Section ৬.৪)।
- **pass@1:** একবার চেষ্টায় সফল হওয়ার সম্ভাবনা — একাধিক run থাকলে resolved rate-এর গড়ই pass@1-এর estimate।
- **pass@k:** $k$ বার চেষ্টার মধ্যে **অন্তত একবার** সফল — "সম্ভাবনা" বা potential মাপে। SWE-rebench pass@5 report করে।
- **pass^k:** $k$ বারের **সবগুলোতেই** সফল — "নির্ভরযোগ্যতা" মাপে। SWE-rebench এটা report করে না (Section ৬.৯-এ আমি bound বের করেছি)।

### ২.১৬ Standard Deviation, SEM, Confidence Interval
- **Standard deviation (SD, $s$):** কয়েকটা মাপের মান গড় থেকে কতটা ছড়ানো।
- **Standard Error of the Mean (SEM):** গড়টা নিজে কতটা অনিশ্চিত — $s/\sqrt{K}$; বেশি run করলে SEM কমে।
- **Confidence Interval (CI):** "আসল মান 95% আস্থায় এই সীমার মধ্যে" — ছোট sample-এ $t$-distribution দিয়ে হিসাব। Paper-এর checklist নিজেই বলেছে তারা CI হিসাব করেনি, শুধু SEM দিয়েছে।
- **দুই ধরনের অনিশ্চয়তা (খুব গুরুত্বপূর্ণ):** (১) **run-sampling** — একই task-এ বারবার চালালে ফল বদলায়; (২) **task-sampling** — 294টা task "সব সম্ভাব্য task"-এর একটা নমুনা মাত্র; অন্য 294টা নিলে score অন্য হতো। SEM over 5 runs শুধু প্রথমটা ধরে (Section ৬.৭)।

### ২.১৭ Difference-in-Differences (DiD) — আমার বিশ্লেষণের জন্য
দুটো সময়ের মধ্যে একটা "সন্দেহভাজন" group-এর পরিবর্তন থেকে একটা "control" group-এর পরিবর্তন বাদ দেওয়া। যদি দুই subset-এর কঠিনতা আলাদা হয়, তাহলে সব model-এর score-ই বদলাবে; contamination-এর প্রভাব বোঝা যায় শুধু অতিরিক্ত পরিবর্তন থেকে। (Paper এটা করেনি; Section ৬.১০-এ আমার হিসাব।)

### ২.১৮ Inference Infrastructure: vLLM, H200, Context Length
- **vLLM:** open-source LLM দ্রুত serve করার engine (PagedAttention memory management)।
- **H200:** NVIDIA-র data-center GPU। প্রতিটা open model 2টা node-এ, প্রতি node-এ 8টা H200।
- **Context length 128K token:** model একবারে কতটা history পড়তে পারে; agent-এর লম্বা trajectory-র জন্য গুরুত্বপূর্ণ।

---

## ৩. Problem Statement — কী সমস্যা ছিল?

### ৩.১ মূল সমস্যা (paper দুটো বড় challenge বলেছে)
**Challenge A — Training data-র অভাব:**
1. RL দিয়ে SWE agent train করতে লাগে **interactive task + automatic verification** — agent action নেবে, environment-এর response দেখবে, শেষে test দিয়ে সফলতা যাচাই হবে।
2. বিদ্যমান dataset হয় one-shot code generation (interactive নয়), নয়তো ছোট, হাতে বানানো (SWE-bench, SWE-Gym, SWE-PolyBench) — অল্প repository, scale নেই।
3. মূল বাধা: হাজার হাজার ভিন্ন repository-র **executable environment** হাতে configure করা অসম্ভব।

**Challenge B — Evaluation-এর অবিশ্বাসযোগ্যতা (Section 3.1-এর চারটা বিষয়):**
1. **Potential data contamination:** SWE-bench 2023-এর শেষ থেকে public; পরের model-রা training-এ দেখে থাকতে পারে → score ফোলানো, memorization আর generalization গুলিয়ে যায়।
2. **Scaffolding variability:** engineered prompt, multi-agent framework, retry, best-of-N, validation loop — model-এর raw ক্ষমতা আলাদা করা যায় না; scaffold SWE-bench subset-এ tune হয়ে implicit overfitting।
3. **Standardized ও verifiable evaluation-এর অভাব:** প্রতিটা দল নিজে report করে, স্বাধীন যাচাই নেই; pass@N-কে pass@1 বলে report করা বা final test থেকে তথ্য ব্যবহার — এমন বিভ্রান্তিকর অভ্যাসের সুযোগ; closed-source framework-এ transparency কম।
4. **Run-to-run high variance:** agent trajectory stochastic; একবারের run unrepresentative; কয়েকবার চালিয়ে শুধু সেরাটা report করলে ক্ষমতা বাড়িয়ে দেখানো হয়।

### ৩.২ কেন এটা গুরুত্বপূর্ণ (আমাদের দৃষ্টিকোণ)
Sub-domain 1-এ দেখেছি: SWE-agent-এর Lite-এ 6 run-এর গড় 17.94% কিন্তু pass@6 = 32.67%; AutoCodeRover @1 = 19.00%, @3 = 26.00%; SWE-agent-এর cost এক paper-এ 1.67 USD, অন্য paper-এ 2.51 USD (CG4, CG8)। Sub-domain 2-এ APR Survey দেখিয়েছিল contamination উপেক্ষিত (CG6)। SWE-rebench এই তিনটা gap-কে একসাথে একটা infrastructure দিয়ে মোকাবিলা করতে চায়। আমরা যদি একটা assurance layer বানাই, সেটাকে evaluate করতেও এই ধরনের পরিষ্কার, তাজা, reproducible task লাগবে (CG10)।

---

## ৪. Goal ও Research Questions

**Goal:** (১) মানুষের হস্তক্ষেপ ছাড়া GitHub থেকে বড় আকারে executable SWE task সংগ্রহের একটা pipeline বানানো; (২) সেই pipeline দিয়ে RL-উপযোগী বড় dataset প্রকাশ; (৩) ক্রমাগত তাজা task দিয়ে একটা decontaminated, standardized leaderboard চালানো।

Paper-এ RQ explicitly লেখা নেই; contribution ও result থেকে implicit RQ:
- **RQ1:** Environment setup সহ পুরো task-collection কি automate করা যায়, আর কত yield পাওয়া যায়?
- **RQ2:** LLM কি মানুষের annotation শিখে task quality (clarity, complexity, test correctness) নির্ভরযোগ্যভাবে predict করতে পারে?
- **RQ3:** একই scaffold, 5 run-এ বিভিন্ন open ও closed model তাজা task-এ কেমন করে?
- **RQ4:** তাজা task-এ performance কি SWE-bench Verified-এর তুলনায় কম, অর্থাৎ contamination-এর লক্ষণ আছে কি?
- **RQ5:** একই model-এর performance কি সময়ের সাথে (Jan বনাম Mar–Apr 2025 task) বদলায় — model release-এর আগের task-এ কি সুবিধা পায়?

---

## ৫. Methodology — কীভাবে কাজটা করা হয়েছে

### ৫.১ সামগ্রিক Pipeline (Fig. 1 ও Section 2)
Text-এ চারটা stage, Fig. 1-এ তিনটা panel (Preliminary filtering → Environment setup → LLM Labeling)। পুরো computation TractoAI নামের distributed storage ও computing platform-এ চলে — যাতে pipeline বদলালে দ্রুত সব আবার process করা যায়।

| Stage | নাম | কী করা হয় | Output (paper-এর সংখ্যা) |
|---|---|---|---|
| 1 | Preliminary task collection | GH Archive + GitHub clone; issue-PR linking; 7টা filter; patch ভাগ | ~4,50,000 linked PR থেকে ~1,53,400 candidate |
| 2 | Automated installation instructions configuration | Version grouping; LLM দিয়ে install recipe (সর্বোচ্চ 3টা candidate); error log দেখে refine | ≥1টা task-এর জন্য কাজ করা recipe — 31% repository-তে |
| 3 | Execution-based installation verification | Container-এ install; test চালিয়ে 3টা শর্ত যাচাই; image build; dependency freeze | 21,336টা valid task (3,468 repository) |
| 4 | Automated instance quality assessment | Fine-tuned Qwen2.5-72B দিয়ে 3টা quality label | 21,336টা annotated task |

### ৫.২ Stage 1 — Preliminary Task Collection (Section 2.1)
**উৎস:** GitHub Archive (issue ও PR-এর metadata: description, discussion, linked PR, creation date, label, merge status, last commit) + GitHub (full history সহ repository clone)।

**শুরুর বিন্দু:** প্রায় **4,50,000টা PR**, যেগুলো **1 May 2025-এর আগে** তৈরি issue-র সাথে linked; **30,000-এর বেশি repository** থেকে, যেগুলোর license permissive এবং codebase-এর line-এর **75%-এর বেশি Python**।

**7টা filter (সবগুলো সত্য হতে হবে):**
1. Issue একটা permissive license-এর Python repository-র।
2. Issue resolved হিসেবে চিহ্নিত।
3. PR main branch-এ merged।
4. PR একাধিক issue-র সাথে linked নয়।
5. Issue description 10 character-এর বেশি।
6. PR test যোগ বা পরিবর্তন করে **এবং** test file-এর বাইরেও code পরিবর্তন করে।
7. পরিবর্তন 1 থেকে 15টা file-এ।

তারপর প্রতিটা PR-এর patch → solution patch (non-test file) + test patch (শুধু test file)। Filter-এর পরে **প্রায় 1,53,400টা** potential task থাকে।

**Appendix L, Table 6-এর funnel (গোল সংখ্যায়):** 10M PR, 6M issue, 32K repo থেকে 450K task candidate (PR-এর 5%) → 150K filtered (33%) → 21K valid (14%) → 21K annotated (100%)।

### ৫.৩ Stage 2 — Automated Installation Instructions (Section 2.2, Appendix B, C)
**Versioning (একাধিক task-কে একটা environment-এ map করা):**
- `git tag` থেকে task-এর version অনুমান, `major.minor`-এ normalize (যেমন 1.2.3 → 1.2)। প্রায় **95%** task-এর version এভাবে পাওয়া যায়; বাকিদের প্রত্যেককে আলাদা version দেওয়া হয় (নিজস্ব environment)।
- প্রতিটা version group-এর জন্য, group-এর মধ্যে **সবচেয়ে সাম্প্রতিক base_commit** বেছে নেওয়া হয় environment-এর ভিত্তি হিসেবে — কারণ developer-রা minor version-এর মধ্যে dependency সামঞ্জস্য রাখে, আর পরের commit-এ প্রায়ই environment fix থাকে।

**LLM-চালিত recipe তৈরি (Agentless-inspired) — তিনটা sub-stage:**
1. **Relevant file খোঁজা (Appendix B.1):** LLM repository-র file list দেখে install/dependency/test তথ্য থাকতে পারে এমন file বাছাই করে — README, setup.py, pyproject.toml, requirements.txt, environment.yml, docs; root-level file-কে অগ্রাধিকার; **সর্বোচ্চ 10টা file**, JSON array আকারে।
2. **Recipe extract (Appendix B.2):** বাছাই করা file-এর content (`<filename>...</filename>` ও `<content>...</content>` format-এ, prompt-এ সর্বোচ্চ 1,00,000 character) পড়ে LLM step-by-step reasoning করে একটা JSON recipe দেয়। Field: `python`, `packages`, `install`, `test_cmd`, `pre_install`, `reqs_path`, `env_yml_path`, `pip_packages`। Prompt-এ নিয়ম: install-এ local command (`pip install -e .[dev]`), test framework pip_packages-এ যোগ, conda-তে `-y`, placeholder-যুক্ত test command নয়, Makefile থাকলে আসল pytest command বের করা।
3. **Recipe update (Appendix B.4):** install বা test fail করলে পুরনো recipe + error log-এর শেষ অংশ + relevant file দিয়ে LLM-কে কারণ বিশ্লেষণ (100 শব্দের কম) করে সম্পূর্ণ নতুন JSON দিতে বলা হয় — missing dependency যোগ, command syntax ঠিক, install order বদল, environment variable, test command পরিবর্তন।

**Model ও সংখ্যা:** Qwen2.5-72B-Instruct; প্রতি task-এ **সর্বোচ্চ 3টা candidate recipe**। ফল: **31% repository**-তে অন্তত একটা task-এর জন্য কাজ করা recipe পাওয়া গেছে। Appendix L অনুযায়ী install ও validate stage-এর সামগ্রিক success rate প্রায় **14%** — pipeline-এর সবচেয়ে বড় bottleneck।

**Recipe কীভাবে চালানো হয় (Appendix B.2-এর script):** clone → base_sha checkout → pre_install → `conda create` (নির্দিষ্ট python) → requirements বা environment.yml থেকে install → pip_packages → install command → test command।

**Example (Appendix B.3):** flake8-bugbear-ধরনের একটা project-এ LLM Python 3.9 বেছেছে ("safe middle-ground", কারণ project 3.6–3.10 সমর্থন করে), `pip install -e .[dev]`, test command `pytest tests/test_bugbear.py`, আর pytest, coverage, hypothesis, hypothesmith>=0.2, pre-commit যোগ করেছে।

**Interactive agent-এর সাথে তুলনা (Appendix C, Table 3):** SWE-bench-এর 18টা আলাদা repository-র 18টা task (যাদের install instruction আগে হাতে বানানো ছিল — তাই reliable baseline)।

| Approach | Candidates/Trials | Successfully configured |
|---|---|---|
| Agentless | 1 | 6 / 18 |
| Agentless | 3 | 8 / 18 |
| Agentless | 10 | 9 / 18 |
| Agent-based (interactive) | 1 | 8 / 18 |

- Authors-এর ব্যাখ্যা: interactive agent কখনো ভালো, কিন্তু অনেক বেশি resource লাগে; agentless + একাধিক candidate বড় scale-এ বেশি efficient — তাই এটাই মূল পদ্ধতি।
- কিছু ব্যর্থতা আসলে install-এর নয়, **log parsing**-এর — যেমন Django-র মতো custom test framework-এর output generic pytest parser পড়তে পারে না।
- এই 18টা task দিয়েই prompt বাছাই ও candidate সংখ্যা ঠিক করা হয়েছে (authors নিজেরাই এটাকে "small-scale sanity check" বলেছেন)।
- 18টা instance-এর তালিকা Appendix C.1-এ আছে (যেমন `astropy__astropy-12907`, `django__django-15315`, `sympy__sympy-22080`)।

### ৫.৪ Stage 3 — Execution-based Installation Verification (Section 2.3, Appendix B.5)
**তিনটা শর্ত (সবগুলো সত্য হলে task valid):**
1. Test patch-এর **অন্তত একটা test** solution patch apply-এর **আগে fail** করে।
2. যে test-গুলো আগে fail করেছিল, solution patch-এর পরে **সবগুলো pass** করে।
3. Test patch-এর যে test-গুলো আগে pass করছিল, solution patch-এর পরেও **pass** করে।

**Infrastructure:**
- Default base container-এ conda, gcc আগে থেকে install।
- নিজস্ব image registry ও internal PyPI/APT mirror — জনপ্রিয় dependency cache।
- ধাপ: (ক) isolated container-এ `buildah` দিয়ে dependency install, file operation-এ tmpfs; (খ) test চালিয়ে log parse — কোন test fix যাচাই করে তা চিহ্নিত; (গ) সফল হলে final container image build; (ঘ) `pip freeze` ও `conda env export` দিয়ে exact dependency version রেকর্ড।

**Failure modes (Appendix B.5):**
| Failure mode | উদাহরণ | Mitigation |
|---|---|---|
| Flaky test | বাইরের API call (মাঝে মাঝে unavailable), floating-point সমতা | Test কয়েকবার চালানো; অন্তত একবার fail করলে task বাদ |
| Install-এ interactivity-র অভাব | পুরনো project-এ ধাপে ধাপে error দেখে dependency যোগ করতে হয় | (সমাধান নেই — অল্প নির্দিষ্ট ধাপের agent পারে না) |
| Unpinned / obsolete dependency | README ঠিক, কিন্তু version pin করা নেই বা পুরনো version আর পাওয়া যায় না | সফল setup-এর পরে version freeze; internal mirror |

Authors বলেছেন এই failure-গুলোই বেশিরভাগ rejection-এর কারণ, এবং interactive install বা উন্নত dependency resolution yield বাড়ানোর বড় সুযোগ।

### ৫.৫ Stage 4 — Automated Instance Quality Assessment (Section 2.4, Appendix F)
**কেন:** RL-এ ত্রুটিপূর্ণ task (underspecified issue, বা সঠিক সমাধানও fail করে এমন test) agent-কে ভুলভাবে শাস্তি দেয়। Verified এটা মানুষ দিয়ে নিশ্চিত করে; 21K task-এ সেটা সম্ভব নয় → automated approximation।

**কীভাবে:**
- Model: **Qwen2.5-72B-Instruct**, fine-tuned on **SWE-bench Verified-এর human annotation**।
- Data: **3,800-এর বেশি example**; input = issue description + canonical solution patch + test patch; output = তিনটা binary label-এর একটা।
- প্রতিটা label আলাদাভাবে train ও predict; **75/25 training/validation split**; validation-এ মোট **413টা example**।
- Validation-এর class বণ্টন: Task Complexity — 100 high vs 313 low; Test Patch Correctness — 180 high vs 233 low; Issue Clarity — 84 high vs 329 low।

**ফলাফলের সারাংশ (বিস্তারিত Section ৮.৩):**
| Label | Fine-tuned accuracy | Fine-tuned weighted F1 | Vanilla accuracy |
|---|---|---|---|
| Task Complexity | 81% | 0.82 | 68% |
| Test Patch Correctness | 67% | 0.65 | 60% |
| Issue Clarity | 79% | 0.76 | 80% |

**ব্যবহার:** label-গুলো প্রতিটা task-এর metadata হিসেবে দেওয়া হয় (`llm_score`: `difficulty_score`, `issue_text_score`, `test_score`)। User নিজের প্রয়োজনে filter করতে পারে — যেমন "কঠিন কিন্তু solvable ও পরিষ্কার" task বাছাই। Authors-এর যুক্তি: SWE-bench Lite-এর মতো "কতগুলো file বদলেছে" heuristic বিভ্রান্তিকর হতে পারে — multi-file পরিবর্তন সহজ হতে পারে (একই parameter বারবার update), আর single-file পরিবর্তনেও issue অস্পষ্ট বা test অপর্যাপ্ত হতে পারে।

### ৫.৬ মূল SWE-bench Methodology-র তুলনায় Refinement (Appendix G)
| Refinement | SWE-bench-এ সমস্যা | SWE-rebench-এর সমাধান |
|---|---|---|
| Patch generation from git history | base_commit বনাম merge_commit-এর diff-এ মাঝের অন্য merge-এর অপ্রাসঙ্গিক পরিবর্তন ঢুকে যায় (উদাহরণ: `sympy__sympy-14821` এই কারণে Verified-এ নেওয়া হয়নি) | head_commit বনাম base_commit diff; head_commit না থাকলে (branch মুছে ফেলা) merge_commit fallback ও metadata-তে রেকর্ড |
| Test directive generation | Regex দিয়ে test command বানালে মুছে ফেলা test file-ও ঢুকে invalid command হয় | মুছে ফেলা file বাদ |
| AttributeError / ImportError check | Test যদি নতুন, এখনো-না-থাকা attribute/import check করে, agent-কে exact signature অনুমান করতে হয়; `tb=no` দিয়ে চালালে error লুকিয়ে যায় | Full error output (`tb=line`) দিয়ে চালিয়ে চিহ্নিত; metadata-তে রাখা (কিছু task, যেমন import error ঠিক করা, বৈধ) |
| Dependency pinning | Latest version install করলে সময়ের সাথে test ভাঙে | প্রথম সফল setup-এর পরে freeze; পরের rebuild-এ পুনর্ব্যবহার |

### ৫.৭ Dataset Schema ও উদাহরণ (Appendix E, K, Table 5)
SWE-bench schema-র সাথে অতিরিক্ত field:
- `license_name` — repository-র license।
- `meta` — `commit_name` (head_commit নাকি merge_commit), `failed_lite_validators`, `has_test_patch`, `is_lite`, `num_modified_files`, `llm_score` (difficulty, issue clarity, test score)।
- `requirements`, `environment` — frozen dependency (pip freeze / conda env export)।
- `install_config` — environment setup-এর JSON recipe।
- বাকি standard field: `instance_id`, `repo`, `base_commit`, `patch`, `test_patch`, `problem_statement`, `hints_text`, `created_at`, `version`, `environment_setup_commit`, `FAIL_TO_PASS`, `PASS_TO_PASS`।

**উদাহরণ task (Appendix E):** `tarohi24__typedflow-68` — issue "The new syntax doesn't work" (2019-12-10-এ তৈরি), 1টা file বদলায়, 1টা F2P test; `llm_score`: issue_text_score = 3, test_score = 1, difficulty_score = 1; license MIT; Python 3.8।
**আমার পর্যবেক্ষণ:** উদাহরণটাতেই issue_text_score = 3 — scale-এ যেখানে কম মান মানে ভালো (Appendix M), সেখানে 3 মানে issue বেশ অস্পষ্ট। অর্থাৎ dataset-এ অস্পষ্ট task রেখে দেওয়া হয়, শুধু label দিয়ে চিহ্নিত করা হয় — filter করা user-এর দায়িত্ব।

### ৫.৮ Benchmark Construction — 294টা Task (Section 3, Appendix H)
Dataset থেকে নিচের 8টা শর্ত পূরণকারী task নিয়ে benchmark: **294টা task, 169টা repository**।
1. **Clean test execution:** solution patch-এর আগের test log-এ AttributeError/ImportError-এর মতো critical error নেই।
2. **Code modification scope:** solution patch সর্বোচ্চ **3টা file** বদলায়।
3. **Patch size:** solution patch-এ মোট শব্দ **500-এর বেশি নয়**।
4. **Problem statement length:** issue description **16 থেকে 1000 শব্দ** (inclusive)।
5. **Language:** issue English-এ।
6. **Recency:** issue **2025 সালে** তৈরি।
7. **Assessed difficulty:** LLM-assessed difficulty label **3-এর কম** (low থেকে moderate)।
8. **Test case count:** F2P test **50 বা তার কম**।

### ৫.৯ Evaluation Protocol (Section 3.2, Appendix I, J)
**তিনটা নীতি:**
1. **Centralized ও standardized:** সব evaluation SWE-rebench দল নিজে চালায়; সব model-এর জন্য একই **minimal ReAct-style scaffold**, একই prompt, model developer-এর recommended default generation hyperparameter (temperature, top-p ইত্যাদি); context length **128K token** (model ছোট context সমর্থন করলে তার সর্বোচ্চ)। Function calling ব্যবহার করা হয় না — সবাই text command লেখে।
2. **Continuous update ও decontamination:** pipeline থেকে নিয়মিত তাজা task; issue/PR-এর creation date বনাম model release date tracking; release-এর আগের issue থাকলে leaderboard-এ "potentially contaminated" চিহ্ন।
3. **Stochasticity হিসাবে রাখা:** প্রতিটা model পুরো benchmark-এ **5 বার** (ভিন্ন random seed); **SEM** ও **pass@5** report।

**এই পদ্ধতি দুটো জিনিস মাপে (authors-এর ভাষায়):** (ক) বাস্তব issue বুঝে, plan করে, সঠিক patch লিখে, সম্ভব হলে যাচাই করার ক্ষমতা; (খ) instruction follow করে একটা structured agentic framework-এ কাজ করার ক্ষমতা।

**Scaffold-এর বিস্তারিত (Appendix I-এর system prompt):**
- Terminal-এ সব standard unix command (grep, sed, echo), python script চালানো, pip/apt দিয়ে package install — কিন্তু interactive command (vim) নয়।
- Special tool: `create`, `edit` (line range replace, heredoc সহ), `goto`, `open`, `replace` (`--replace-all`), `scroll_down`, `scroll_up`, `search_file`, `submit`।
- প্রতিটা response-এ **ঠিক একটা reasoning আর একটা command** (` ```command ` block-এ); দুটো command দিলে error।
- **Existing test বদলানো বা নতুন test যোগ করা নিষেধ** — temporary script দিয়ে test করে submit-এর আগে মুছতে হবে।
- পরামর্শ: আগে repo explore, reproduce script দিয়ে error নিশ্চিত, fix, আবার চালিয়ে যাচাই, edge case, hardcode না করা, existing test চালানো।
- শেষে একটা checklist-এর প্রতিটা item-এর reasoning লিখতে হয়।
- `submit` শুধু unstaged পরিবর্তন (`git diff`) জমা দেয়।
- Prime number-এর একটা ছোট demonstration trajectory prompt-এ দেওয়া আছে (one-shot)।

**Compute (Appendix J):** open model vLLM-এ internal deploy; প্রতিটা model 2টা node × 8টা H200; DeepSeek-V3 সবচেয়ে বড় — একবার পুরো 294 task চালাতে প্রায় **7 ঘন্টা**।

**বিশ্লেষণের দুটো তুলনা (Section 3.3):**
- **Temporal:** January 2025-এর task বনাম March–April 2025-এর task (Table 1)।
- **Verified বনাম SWE-rebench:** 2024 বা 2025-এর শুরুতে release হওয়া open model-গুলোর SWE-bench Verified score বনাম SWE-rebench Mar–Apr score (Table 2)।

### ৫.১০ Leaderboard
- Public website (swe-rebench.com/leaderboard); continuously updated — paper-এর table-গুলো শুধু তখনকার snapshot, বর্তমান model তালিকা website-এ।
- Open ও closed দুই ধরনের model।
- Contaminated evaluation explicitly চিহ্নিত।
- **আমার পর্যবেক্ষণ:** Section 3-এ লেখা "we maintain a **private** leaderboard", অথচ contribution-এ "**public** leaderboard"। সম্ভবত মানে — leaderboard public দেখা যায়, কিন্তু evaluation চালানো private/centralized (বাইরের কেউ নিজে submit করে না)। Supervisor জিজ্ঞেস করলে এই ব্যাখ্যা দেবো, তবে এটা আমার ব্যাখ্যা।

---

## ৬. Mathematical Formulation — সূত্র ও ব্যাখ্যা

Paper-এ explicit equation প্রায় নেই (checklist-এও লেখা: "no theoretical results")। নিচে pipeline, metric আর contamination বিশ্লেষণকে formal রূপে লিখেছি — Supervisor-এর কাছে "এই paper আসলে কী মাপে" পরিষ্কার করতে। যেখানে হিসাব আমার নিজের, সেখানে "আমার হিসাব" লেখা।

### ৬.১ একটা Task Instance-এর Formal Definition
SWE-bench-এর definition (Sub-domain 1, Paper 01, Section ৬.১) প্রসারিত করে:
$$
x = (C,\; P,\; T,\; \delta,\; \tau,\; E,\; \lambda)
$$
- $C$ = base commit-এ codebase; $P$ = problem statement; $T$ = test patch; $\delta$ = gold solution patch (SWE-bench-এর মতো)
- $\tau$ = task creation date (নতুন, decontamination-এর জন্য)
- $E$ = executable environment (install recipe + frozen dependency + container image)
- $\lambda = (\lambda_{\text{diff}}, \lambda_{\text{issue}}, \lambda_{\text{test}})$ = LLM-predicted quality label

### ৬.২ Pipeline-কে Set Filter হিসেবে লেখা
$U$ = GitHub-এর সব PR (প্রায় 10M)। প্রতিটা ধাপ একটা filter:
$$
\mathcal{D}_0 = \{\, x \in U \;:\; \text{PR issue-linked এবং issue date} < \text{1 May 2025} \,\}
$$
$$
\mathcal{D}_1 = \{\, x \in \mathcal{D}_0 \;:\; \prod_{j=1}^{7} f_j(x) = 1 \,\}
$$
$$
\mathcal{D}_2 = \{\, x \in \mathcal{D}_1 \;:\; \exists\, \rho \in R(x) \;\text{ যাতে }\; \text{Install}(\rho, x) = \text{OK} \,\}
$$
$$
\mathcal{D}_3 = \{\, x \in \mathcal{D}_2 \;:\; V(x) = 1 \,\}, \qquad B = \{\, x \in \mathcal{D}_3 \;:\; \prod_{j=1}^{8} h_j(x) = 1 \,\}
$$
- $f_j$ = Section ৫.২-এর 7টা filter; $R(x)$ = সর্বোচ্চ 3টা LLM recipe (refinement সহ); $V$ = execution validity (৬.৩); $h_j$ = benchmark-এর 8টা শর্ত (Section ৫.৮)।
- Labeling ($\lambda$) কোনো task বাদ দেয় না — শুধু metadata যোগ করে (Table 6: acceptance 100%)।

**প্রতিটা ধাপের yield (paper-এর সংখ্যা থেকে আমার হিসাব):**
| ধাপ | আকার | আগের ধাপের তুলনায় | মন্তব্য |
|---|---|---|---|
| $U$ | ~10M PR (32K repo) | — | Table 6 |
| $\mathcal{D}_0$ | ~4,50,000 | 4.5% (Table 6-এ গোল করে 5%) | Section 2.1 |
| $\mathcal{D}_1$ | ~1,53,400 | 34.1% (Table 6-এ 33%) | Section 2.1 |
| $\mathcal{D}_3$ | 21,336 (3,468 repo) | 13.9% (Table 6-এ 14%) | Section 2 |
| $B$ | 294 (169 repo) | 1.4% of $\mathcal{D}_3$ (তবে $B$-তে শুধু 2025-এর issue, তাই এই অনুপাত তুলনীয় নয়) | Section 3 |

**আমার হিসাব:** 4,50,000 থেকে 21,336 মানে সামগ্রিক yield $21336/450000 \approx 4.74\%$; 10M PR-এর তুলনায় মাত্র প্রায় 0.21%। Repository-র দিক থেকে $3468/32000 \approx 10.8\%$ repo-তে অন্তত একটা valid task আছে। (Paper-এর "31% repository-তে working recipe" সংখ্যাটা সম্ভবত শুধু install stage পর্যন্ত পৌঁছানো repository-র মধ্যে — paper denominator স্পষ্ট করেনি।)

### ৬.৩ Execution Validity $V(x)$
$T_p$ = test patch-এর test-এর set; $s(t, X)$ = codebase $X$-এ test $t$-এর status:
$$
F = \{\, t \in T_p \;:\; s(t,\, C \oplus T) = \text{FAIL} \,\}, \qquad Q = \{\, t \in T_p \;:\; s(t,\, C \oplus T) = \text{PASS} \,\}
$$
$$
V(x) = \mathbb{1}\left[\, |F| \geq 1 \;\land\; \forall t \in F:\; s(t,\, C \oplus T \oplus \delta) = \text{PASS} \;\land\; \forall t \in Q:\; s(t,\, C \oplus T \oplus \delta) = \text{PASS} \,\right]
$$
তিনটা অংশ ঠিক Section ৫.৪-এর তিনটা শর্ত। Flaky test বাদ দেওয়ার নিয়ম: $M$ বার চালালে
$$
V^{(M)}(x) = \prod_{r=1}^{M} V_r(x)
$$
অর্থাৎ একবারও শর্ত ভাঙলে বাদ। (Paper $M$-এর মান বলেনি।)
**আমার পর্যবেক্ষণ:** Evaluation-এ agent-এর patch $\hat{\delta}$-এর জন্য "Resolved" শর্ত SWE-bench-এর মতোই (Sub-domain 1, Paper 01, Section ৬.৩) — F2P ও P2P সব pass। অর্থাৎ correctness-এর সংজ্ঞা বদলায়নি; বদলেছে শুধু task কোথা থেকে, কখন, কীভাবে আসে।

### ৬.৪ Version Grouping ও Environment-এর Base Commit
$$
v(x) = \text{major.minor}\left(\text{git tag}(x)\right), \qquad c_g = \arg\max_{x \in g}\; \text{date}\left(\text{base commit}(x)\right)
$$
একই $v$-এর সব task একটা group $g$; group-এর environment বানানো হয় $c_g$ commit থেকে — group-এর সবচেয়ে নতুন base commit।

### ৬.৫ আমার হিসাব: Recipe Candidate কি Independent? (Table 3)
যদি প্রতিটা candidate recipe স্বাধীনভাবে $p$ সম্ভাবনায় সফল হতো, তাহলে $k$টা candidate-এ অন্তত একটা সফল হওয়ার সম্ভাবনা:
$$
P_k = 1 - (1 - p)^{k}
$$
Table 3-এ $k = 1$-এ 6/18, তাই $p = 1/3$। তাহলে:
- $k = 3$: $P_3 = 1 - (2/3)^3 = 1 - 0.296 = 0.704$ → প্রত্যাশিত $\approx 12.7$/18; **বাস্তবে 8/18**।
- $k = 10$: $P_{10} = 1 - (2/3)^{10} \approx 0.983$ → প্রত্যাশিত $\approx 17.7$/18; **বাস্তবে 9/18**।

**ব্যাখ্যা:** candidate-গুলোর ব্যর্থতা খুবই correlated — যে repository কঠিন (পুরনো dependency, custom test framework), সেখানে সব candidate-ই ব্যর্থ হয়। অর্থাৎ বেশি sample নেওয়ার লাভ দ্রুত শেষ হয়ে যায়; বাকি অর্ধেক task-এর জন্য ভিন্ন ধরনের সমাধান (interactive agent, ভালো log parser) লাগবে। এটা Agentless-এর "40টা candidate-এর upper bound" (Sub-domain 1 Summary, CG2)-এর মতোই একটা শিক্ষা: sampling-এর diversity সীমিত। (18টা task খুব ছোট sample — তাই এটা indicative, প্রমাণ নয়।)

### ৬.৬ Resolved Rate Estimator ও SEM
$N$টা task, $K$টা run। $y_{ij} \in \{0, 1\}$ = task $i$ run $j$-এ resolved কিনা।
$$
r_j = \frac{1}{N}\sum_{i=1}^{N} y_{ij}, \qquad \bar{r} = \frac{1}{K}\sum_{j=1}^{K} r_j
$$
$$
s = \sqrt{\frac{1}{K-1}\sum_{j=1}^{K} \left(r_j - \bar{r}\right)^2}, \qquad \text{SEM} = \frac{s}{\sqrt{K}}
$$
এখানে $K = 5$। Paper SEM-এর exact formula বলেনি; checklist অনুযায়ী এটা "five independent runs"-এর resolution rate-এর SEM, তাই উপরের standard formula ধরে নিচ্ছি।

**Worked example (আমার হিসাব, Table 1-এর আসল সংখ্যা):** GPT-4.1 (Jan subset): $\bar{r} = 31.1\%$, SEM $= 0.79$।
- Run-গুলোর SD: $s = 0.79 \times \sqrt{5} = 0.79 \times 2.236 \approx 1.77$ percentage point (pp)।
- 95% CI ($t$-distribution, df $= 4$, $t_{4, 0.975} = 2.776$): $31.1 \pm 2.776 \times 0.79 = 31.1 \pm 2.19$ → **[28.9%, 33.3%]**।
- Paper normality ধরে নেয়নি বলে CI দেয়নি; উপরের CI normality ধরে নিয়ে আমার হিসাব।

**SD কত বড় হতে পারে (আমার হিসাব):** Table 1-এর সবচেয়ে বড় SEM — Qwen3-235B-A22B think (Jan) 1.81 → $s \approx 1.81 \times 2.236 \approx 4.05$ pp। অর্থাৎ একটা single run গড় থেকে প্রায় ±4 pp সরে যেতে পারে। সবচেয়ে ছোট SEM — gemma-3-27b-it (Mar–Apr) 0.30 → $s \approx 0.67$ pp।

### ৬.৭ আমার হিসাব: Task-sampling Uncertainty — SEM যা ধরে না
SEM শুধু একই 294 task-এ run-এর এলোমেলোতা ধরে। কিন্তু 294টা task নিজেই একটা নমুনা। Task-level uncertainty-র একটা সরল approximation (প্রতিটা task-কে Bernoulli ধরে):
$$
\text{SE}_{\text{task}} \approx \sqrt{\frac{\bar{r}\,(1 - \bar{r})}{N}}
$$
যদি $N = 294$ আর $\bar{r} = 0.311$ ধরি (GPT-4.1-এর Jan score, পুরো benchmark-এর আকার দিয়ে — subset-এর আসল আকার paper দেয়নি):
$$
\text{SE}_{\text{task}} \approx \sqrt{\frac{0.311 \times 0.689}{294}} = \sqrt{0.000729} \approx 0.027 = 2.7 \text{ pp}
$$
**ফল:** task-sampling SE (≈ 2.7 pp) run-sampling SEM-এর (0.79 pp) প্রায় সাড়ে তিন গুণ। Subset ছোট হলে (Jan বা Mar–Apr আলাদাভাবে) এটা আরও বড়। অর্থাৎ **paper-এর SEM আসল অনিশ্চয়তার ছোট অংশ দেখায়**। একই task-এ দুই model তুলনা করলে (paired) task-sampling-এর অনেকটা বাতিল হয়, কিন্তু **দুটো ভিন্ন task-subset তুলনায় (Jan বনাম Mar–Apr, Verified বনাম rebench) এটা বাতিল হয় না**। আরও সঠিক উপায়: প্রতিটা task-এর $\hat{q}_i = \frac{1}{K}\sum_j y_{ij}$ বের করে task-এর উপর bootstrap।

### ৬.৮ দুই Score-এর পার্থক্য: সরল z-test
দুই স্বাধীন অনুমানের পার্থক্য:
$$
z = \frac{\bar{r}_A - \bar{r}_B}{\sqrt{\text{SE}_A^{2} + \text{SE}_B^{2}}}
$$
**Worked example ১ (আমার হিসাব, শুধু run-SEM দিয়ে):** GPT-4.1 Jan 31.1 (SEM 0.79) বনাম Mar–Apr 26.7 (SEM 1.09): পার্থক্য 4.4 pp; $\sqrt{0.79^2 + 1.09^2} = \sqrt{0.624 + 1.188} = \sqrt{1.812} \approx 1.35$; $z \approx 3.27$ — শুধু run-noise বিবেচনায় "significant"।

**Worked example ২ (আমার হিসাব, task-sampling সহ, assumption-নির্ভর):** ধরি প্রতিটা subset-এ প্রায় 150টা task (paper আকার দেয়নি — এটা আমার অনুমান মাত্র)। তাহলে $\text{SE}_1 = \sqrt{0.311 \times 0.689/150} \approx 3.78$ pp, $\text{SE}_2 = \sqrt{0.267 \times 0.733/150} \approx 3.61$ pp; পার্থক্যের SE $\approx \sqrt{3.78^2 + 3.61^2} \approx 5.23$ pp; $z \approx 4.4/5.23 \approx 0.84$ → **significant নয়**। অর্থাৎ GPT-4.1-এর পতন contamination-এর প্রমাণ হিসেবে দুর্বল; subset-এর আকার জানা থাকলে এটা নিশ্চিত করা যেত।

**Worked example ৩ (আমার হিসাব, Appendix F-এর file-count ফল):** DeepSeek-V3-0324: 1 file 28.6% ± 0.8 (n = 201) বনাম ≥3 file 17.5% ± 2.2 (n = 64)। শুধু ± দিয়ে: $z = 11.1/\sqrt{0.64 + 4.84} = 11.1/2.34 \approx 4.7$। Task-sampling যোগ করলে: $\sqrt{0.286 \times 0.714/201} \approx 3.19$ pp, $\sqrt{0.175 \times 0.825/64} \approx 4.75$ pp; পার্থক্যের SE $\approx 5.72$ pp; $z \approx 1.94$ — সীমারেখায় (p ≈ 0.05)। (Paper ± কী তা বলেনি; SEM ধরে নিয়েছি।)

### ৬.৯ pass@k, pass^k, এবং আমার হিসাব: pass@1 ও pass@5 থেকে Flip-rate-এর Bound
Task $i$-এ $K$ run-এর মধ্যে $c_i$টা সফল। Unbiased pass@k (Chen et al., 2021; Sub-domain 1, Paper 01, Section ৬.১০):
$$
\text{pass@}k = \frac{1}{N}\sum_{i=1}^{N}\left[1 - \frac{\binom{K - c_i}{k}}{\binom{K}{k}}\right]
$$
এখানে $K = k = 5$, তাই এটা সরলভাবে $\frac{1}{N}\sum_i \mathbb{1}[c_i \geq 1]$ — **৫টা run-এর অন্তত একটায় solve হওয়া task-এর অনুপাত** (paper formula দেয়নি; এটা স্বাভাবিক ব্যাখ্যা)।

Reliability-র জন্য বিপরীত metric **pass^k** (সব $k$ বার সফল):
$$
\text{pass}^{k} = \frac{1}{N}\sum_{i=1}^{N} \frac{\binom{c_i}{k}}{\binom{K}{k}}
$$
Paper pass^5 দেয়নি। কিন্তু pass@1 ($\bar{r}$) আর pass@5 ($p_K$) থেকে একটা **bound** বের করা যায় (আমার derivation)। ধরি $A$ = সব $K$ run-এ solved task-এর অনুপাত ($= \text{pass}^K$), $B$ = কিছু run-এ solved কিন্তু সবগুলোতে নয় (**inconsistent / flip task**)। তাহলে $p_K = A + B$, আর প্রতিটা inconsistent task অন্তত $1/K$ অংশ run-এ solved, তাই $\bar{r} \geq A + B/K$। এই দুটো মিলিয়ে:
$$
B \geq \frac{p_K - \bar{r}}{1 - 1/K}, \qquad \text{pass}^{K} = A \leq \frac{K\,\bar{r} - p_K}{K - 1}
$$
$K = 5$-এ: $B \geq (p_5 - \bar{r})/0.8$ এবং $A \leq (5\bar{r} - p_5)/4$।

**Table 1 (Mar–Apr)-এর সংখ্যা দিয়ে আমার হিসাব:**
| Model | pass@1 | pass@5 | ফাঁক (pp) | Inconsistent task অন্তত (B ≥) | pass^5 সর্বোচ্চ (A ≤) | Solved-at-least-once task-এর মধ্যে inconsistent অন্তত |
|---|---|---|---|---|---|---|
| gpt-4.1-2025-04-14∗ | 26.7 | 39.0 | 12.3 | 15.4% | 23.6% | 39.4% |
| DeepSeek-V3-0324∗ | 21.3 | 32.4 | 11.1 | 13.9% | 18.5% | 42.8% |
| DeepSeek-V3-1226 | 21.9 | 31.4 | 9.5 | 11.9% | 19.5% | 37.8% |
| Llama-4-Maverick-Instruct∗ | 12.2 | 27.6 | 15.4 | 19.3% | 8.4% | 69.7% |
| Qwen3-235B-A22B think∗ | 12.2 | 25.7 | 13.5 | 16.9% | 8.8% | 65.7% |
| Qwen2.5-Coder-32B-Instruct | 3.2 | 9.5 | 6.3 | 7.9% | 1.6% | 82.9% |

(শেষ কলাম = $B_{\min}/p_5$; যেমন Maverick: $19.25/27.6 \approx 69.7\%$।)

**ব্যাখ্যা:** GPT-4.1-এর যে task-গুলো অন্তত একবার solve হয়, তার **অন্তত 39%** সব run-এ solve হয় না। Llama-4-Maverick-এর ক্ষেত্রে এটা **অন্তত 70%** — authors-এর "high potential but inconsistent execution" মন্তব্যকে সংখ্যায় রূপ দেয়। এটাই আমাদের **CG4**-এর জন্য সরাসরি প্রমাণ: গড় score একটা নির্দিষ্ট task-এ agent-কে বিশ্বাস করা যায় কিনা বলে না।

**আরেকটা পরীক্ষা (আমার হিসাব) — task-গুলো কি "সমান কঠিন"?** যদি সব task-এ সফলতার সম্ভাবনা একই $\bar{r}$ হতো, তাহলে pass@5 হতো $1 - (1 - \bar{r})^5$। GPT-4.1: $1 - 0.733^5 \approx 1 - 0.212 = 78.8\%$, কিন্তু বাস্তবে 39.0%। Maverick: $1 - 0.878^5 \approx 47.8\%$, বাস্তবে 27.6%। অর্থাৎ task-গুলো খুবই heterogeneous — অনেক task প্রায় কখনোই solve হয় না, কিছু প্রায় সবসময় হয়, আর একটা মাঝারি অংশ "flip" করে। Assurance layer-এর জন্য শিক্ষা: **কোন task "flip-prone" তা চিহ্নিত করতে পারলে সেখানে বাড়তি যাচাই দরকার।**

### ৬.১০ Best-of-K Report করলে কতটা ফোলে (আমার হিসাব)
Paper বলেছে "একাধিক run চালিয়ে শুধু সেরাটা report করা ক্ষমতা বাড়িয়ে দেখায়"। কতটা? Run score-গুলো normal ধরে নিলে 5টা independent sample-এর maximum-এর প্রত্যাশিত মান $\approx \bar{r} + 1.163\,s$ (standard normal-এর 5টা sample-এর maximum-এর প্রত্যাশা ≈ 1.163):
$$
\mathbb{E}\left[\max_{j} r_j\right] \approx \bar{r} + 1.163 \cdot s, \qquad s = \text{SEM} \cdot \sqrt{K}
$$
- Qwen3-235B-A22B think (Jan): $s \approx 4.05$ → ফোলানো $\approx 1.163 \times 4.05 \approx 4.7$ pp (13.7% → প্রায় 18.4%)।
- Llama-4-Maverick (Mar–Apr): $s \approx 1.69 \times 2.236 \approx 3.78$ → $\approx 4.4$ pp।
- এটা Table 1-এর অনেক model-এর পারস্পরিক পার্থক্যের চেয়ে বড় — অর্থাৎ self-reported "best run" leaderboard-এর ranking উল্টে দিতে পারে। Centralized 5-run গড়ের যুক্তি এখানে।

### ৬.১১ Contamination Flag ও Rolling Window
Model $m$-এর release date $d_m$, task $x$-এর creation date $\tau(x)$:
$$
\text{flag}(m, x) = \mathbb{1}\left[\, \tau(x) < d_m \,\right], \qquad B_m = \{\, x \in B \;:\; \tau(x) \geq d_m \,\}
$$
Leaderboard-এ যদি কোনো model-এর evaluation-এ flag = 1 এমন task থাকে, সেটা চিহ্নিত। $B_m$ = model $m$-এর জন্য "পরিষ্কার" task — প্রতিটা model-এর জন্য আলাদা, তাই **সব model-কে একই পরিষ্কার set-এ তুলনা করতে হলে সব $B_m$-এর intersection ($B_{m_1} \cap B_{m_2} \cap \ldots$), অর্থাৎ সবচেয়ে নতুন model-এর তারিখের পরের task নিতে হয়** (আমার পর্যবেক্ষণ — এটা fairness আর sample size-এর মধ্যে একটা trade-off)।

### ৬.১২ আমার হিসাব: Verified বনাম SWE-rebench — Gap, Ratio, Rank Correlation
Model $m$-এর জন্য:
$$
\Delta_m = R^{\text{Ver}}_m - R^{\text{reb}}_m, \qquad \rho_m = \frac{R^{\text{reb}}_m}{R^{\text{Ver}}_m}
$$
| Model | Verified | rebench (Mar–Apr) | $\Delta$ (pp) | $\rho$ (ধরে রাখা অংশ) |
|---|---|---|---|---|
| DeepSeek-V3-0324 | 39.7 | 21.3 | 18.4 | 0.54 |
| DeepSeek-V3-1226 | 35.2 | 21.9 | 13.3 | 0.62 |
| LLaMA-3.3-70B-Instruct | 18.1 | 11.2 | 6.9 | 0.62 |
| LLaMA-4-Maverick-Instruct | 16.0 | 12.2 | 3.8 | 0.76 |
| Qwen2.5-72B-Instruct | 11.3 | 9.3 | 2.0 | 0.82 |
| LLaMA-4-Scout-Instruct | 8.8 | 5.3 | 3.5 | 0.60 |
| Qwen2.5-Coder-32B-Instruct | 4.9 | 3.2 | 1.7 | 0.65 |

- **সব** model-এর score কমেছে; গড় $\rho \approx 4.618/7 \approx 0.66$। তাই absolute পতন একা contamination প্রমাণ করে না — SWE-rebench-এর task automated (কিছু অস্পষ্ট বা ত্রুটিপূর্ণ task থাকতে পারে; authors নিজেরাই "lower absolute success rates" আশা করেছেন), আর Verified মানুষ দিয়ে ছাঁকা।
- **আপেক্ষিক** পতন সবচেয়ে বেশি DeepSeek-V3-0324-এর ($\rho = 0.54$, গড়ের চেয়ে প্রায় 12 percentage point কম ধরে রাখা)। এটাই paper-এর contamination যুক্তির শক্ত অংশ: Verified-এ দুই DeepSeek version-এর পার্থক্য 4.5 pp (39.7 বনাম 35.2), কিন্তু তাজা task-এ প্রায় শূন্য (21.3 বনাম 21.9)।
- Verified-এ দুই DeepSeek-এর পার্থক্যের run-only $z$: $4.5/\sqrt{0.35^2 + 0.52^2} = 4.5/0.627 \approx 7.2$; rebench-এ $-0.6/\sqrt{0.98^2 + 1.44^2} = -0.6/1.74 \approx -0.34$ (আমার হিসাব)। একই task-এ দুই model, তাই paired comparison-এ task-sampling-এর প্রভাব কম — এই অংশটা তুলনামূলক শক্ত প্রমাণ।
- **Spearman rank correlation (আমার হিসাব):** Verified-এর ranking 1–7 আর rebench-এর ranking (DS-1226 = 1, DS-0324 = 2, Maverick = 3, LLaMA-3.3 = 4, Qwen2.5-72B = 5, Scout = 6, Coder = 7) তুলনা করলে $\sum d^2 = 4$:
$$
\rho_s = 1 - \frac{6\sum d_i^{2}}{n(n^{2} - 1)} = 1 - \frac{6 \times 4}{7 \times 48} = 1 - \frac{24}{336} \approx 0.93
$$
  অর্থাৎ **ranking প্রায় একই**; শুধু দুটো পাশাপাশি জোড়া জায়গা বদল করেছে। Contamination absolute score ফোলাতে পারে, কিন্তু এই 7টা model-এর আপেক্ষিক ক্রম বেশিরভাগ টিকে আছে।

### ৬.১৩ আমার হিসাব: Temporal তুলনায় Difference-in-Differences (Table 1)
Mar–Apr বিয়োগ Jan (pp):

| Model | Jan | Mar–Apr | পরিবর্তন |
|---|---|---|---|
| gpt-4.1-2025-04-14∗ | 31.1 | 26.7 | −4.4 |
| DeepSeek-V3-0324∗ | 21.7 | 21.3 | −0.4 |
| DeepSeek-V3-1226 | 19.1 | 21.9 | +2.8 |
| Qwen3-235B-A22B no-think∗ | 15.2 | 16.6 | +1.4 |
| Qwen3-235B-A22B think∗ | 13.7 | 12.2 | −1.5 |
| Qwen3-32B no-think∗ | 13.2 | 13.7 | +0.5 |
| Qwen3-32B think∗ | 11.8 | 11.2 | −0.6 |
| Llama-4-Maverick-Instruct∗ | 8.5 | 12.2 | +3.7 |
| Qwen2.5-72B-Instruct | 8.2 | 9.3 | +1.1 |
| Llama-3.3-70B-Instruct | 8.2 | 11.2 | +3.0 |
| Llama-4-Scout-Instruct∗ | 5.0 | 5.3 | +0.3 |
| gemma-3-27b-it∗ | 4.3 | 4.8 | +0.5 |
| Qwen2.5-Coder-32B-Instruct | 2.7 | 3.2 | +0.5 |

যে চারটা model-এ ∗ নেই (DeepSeek-V3-1226, Qwen2.5-72B, Llama-3.3-70B, Qwen2.5-Coder-32B) — Table 2-এর বর্ণনা অনুযায়ী এগুলো "2024 বা 2025-এর শুরুতে" release; DeepSeek-V3-1226-এর নামেই December আছে, আর বাকি তিনটা 2024-এর model বলে আমার জানা (paper নিজে exact release date দেয়নি)। তাহলে তাদের জন্য **দুটো subset-ই পরিষ্কার** (দুটোই release-এর পরে)। তাদের গড় পরিবর্তন:
$$
\bar{\Delta}_{\text{clean}} = \frac{2.8 + 1.1 + 3.0 + 0.5}{4} = 1.85 \text{ pp}
$$
অর্থাৎ Mar–Apr subset সম্ভবত **একটু সহজ**। তাহলে GPT-4.1-এর জন্য:
$$
\text{DiD} = (-4.4) - 1.85 = -6.25 \text{ pp}
$$
**ব্যাখ্যা:** subset-এর কঠিনতার পার্থক্য বাদ দিলে GPT-4.1-এর "অতিরিক্ত" পতন প্রায় 6 pp — paper-এর পর্যবেক্ষণ (GPT-4.1-ই একমাত্র model যার স্পষ্ট পতন) এতে আরও শক্ত হয়। **কিন্তু সতর্কতা:** (১) control group মাত্র 4টা model; (২) subset-এর আকার অজানা (Section ৬.৮-এর worked example ২); (৩) GPT-4.1-এর release (2025-04-14) Mar–Apr window-এর ভেতরে, তাই Mar–Apr-এর কিছু task-ও release-এর আগের; (৪) GPT-4.1-এর আসল training cutoff যদি January 2025-এর আগে হয়, তাহলে Jan task-ও training-এ থাকার কথা নয় — তখন পতনের কারণ অন্য কিছু (যেমন subset-specific task mix)। Paper নিজেও কারণ দাবি করেনি, শুধু পর্যবেক্ষণ বলেছে।

### ৬.১৪ Quality Classifier Metric ও Majority Baseline (Table 4)
Class $c$-এর জন্য precision, recall, F1 (Sub-domain 2, Paper 03, Section ৬.৮ দেখো)। Weighted ও macro F1:
$$
F1_{\text{weighted}} = \sum_{c} \frac{n_c}{n}\, F1_c, \qquad F1_{\text{macro}} = \frac{1}{|C|}\sum_{c} F1_c
$$
**Worked example (আমার হিসাব, Task Complexity, fine-tuned):** low-score F1 = 0.87 ($n = 313$), high-score F1 = 0.65 ($n = 100$):
$$
F1_{\text{weighted}} = \frac{313 \times 0.87 + 100 \times 0.65}{413} = \frac{272.31 + 65}{413} \approx 0.817
$$
Table-এর 0.82-এর সাথে মেলে।

**Majority-class baseline (সবসময় বড় class বলা):**
$$
\text{Acc}_{\text{maj}} = \frac{\max_c n_c}{n}
$$
| Label | Majority baseline (আমার হিসাব) | Vanilla acc | Fine-tuned acc | Fine-tuned balanced acc (= macro recall) |
|---|---|---|---|---|
| Test Patch Correctness | 233/413 = 56.4% | 60% | 67% | 0.64 |
| Task Complexity | 313/413 = 75.8% | 68% | 81% | 0.78 |
| Issue Clarity | 329/413 = 79.7% | 80% | 79% | 0.57 |

**গুরুত্বপূর্ণ পর্যবেক্ষণ (আমার):** Issue Clarity-তে fine-tuned model-এর accuracy (79%) **"সবসময় পরিষ্কার বলো" baseline-এর (79.7%) চেয়েও কম**, আর vanilla-র (80%) চেয়েও কম। High-score (সমস্যাযুক্ত) class-এর recall মাত্র 0.20 — অর্থাৎ (আমার হিসাবে confusion matrix পুনর্গঠন) 84টা অস্পষ্ট issue-এর মধ্যে মাত্র প্রায় 17টা ধরা পড়ে, প্রায় 67টা "পরিষ্কার" বলে পার পেয়ে যায়। Test Patch Correctness-এ high-score recall 0.42 — সমস্যাযুক্ত test-এর অর্ধেকের বেশি ধরা পড়ে না। শুধু Task Complexity-তে fine-tuning সত্যিকারের উন্নতি দিয়েছে।

---

## ৭. Experimental Setup

| বিষয় | বিবরণ |
|---|---|
| **Dataset** | 21,336 task, 3,468 repository, issue 1 May 2025-এর আগে |
| **Benchmark** | 294 task, 169 repository, issue 2025 সালে (Section ৫.৮-এর 8টা filter) |
| **Temporal subset** | January 2025 task বনাম March–April 2025 task (subset-এর আকার paper-এ নেই) |
| **Leaderboard file-count বিশ্লেষণ** | January–July 2025-এর leaderboard task (n = 201 + 144 + 64 = 409 — আমার যোগফল; 294-এর চেয়ে বড়, অর্থাৎ পরে আরও task যোগ হয়েছে) |
| **Models (Table 1)** | gpt-4.1-2025-04-14, DeepSeek-V3-0324, DeepSeek-V3-1226, Qwen3-235B-A22B (think ও no-think), Qwen3-32B (think ও no-think), Llama-4-Maverick-Instruct, Qwen2.5-72B-Instruct, Llama-3.3-70B-Instruct, Llama-4-Scout-Instruct, gemma-3-27b-it, Qwen2.5-Coder-32B-Instruct — মোট 13টা configuration |
| **Models (Table 2)** | 2024 বা 2025-এর শুরুতে release হওয়া 7টা open model |
| **Scaffold** | একই minimal ReAct-style scaffold, Appendix I-এর system prompt, function calling নয় |
| **Context** | 128K token (model-এর সীমা কম হলে সেটা) |
| **Generation** | Model developer-এর recommended hyperparameter (temperature, top-p, max context) |
| **Runs** | প্রতিটা model 5 run, ভিন্ন random seed |
| **Metrics** | Resolved (% গড়), SEM, Pass@5 |
| **Infrastructure** | vLLM; প্রতিটা model 2 node × 8 H200; DeepSeek-V3-এর একটা পুরো run ≈ 7 ঘন্টা |
| **Quality classifier** | Qwen2.5-72B-Instruct fine-tuned; >3,800 example; 75/25 split; 413 validation |
| **Install study** | SWE-bench-এর 18টা repository-র 18টা task |

**আমার পর্যবেক্ষণ (setup-এর অস্পষ্টতা):**
1. Table 2-এর Verified সংখ্যাতেও SEM ও Pass@5 আছে — তাই মনে হয় authors নিজেরাই একই scaffold-এ Verified-এ 5 বার চালিয়েছেন; কিন্তু paper এটা স্পষ্ট লেখেনি।
2. ">3,800 example" আর "75/25 split-এ 413 validation" মেলে না ($413/0.25 \approx 1{,}652$ প্রতি label)। সম্ভবত 3,800 সব label মিলিয়ে বা অন্য গণনায় — paper-এ পরিষ্কার নয়।
3. Jan ও Mar–Apr subset-এ কয়টা task, আর February-র task কোথায় গেল — paper বলেনি।

---

## ৮. Results — মূল ফলাফল

### ৮.১ Data Collection Funnel (Table 6 ও Section 2)
| Stage | Input | Output | Acceptance rate |
|---|---|---|---|
| Match PRs & Issues | 10M PR, 6M issue, 32K repo | 450K task candidate | 5% (PR-এর) |
| Filter Tasks | 450K candidate | 150K filtered task | 33% |
| Install & Validate | 150K task | 21K valid task | 14% |
| Annotate | 21K task | 21K annotated task | 100% |

Text-এর সঠিক সংখ্যা: ~4,50,000 → ~1,53,400 → **21,336** (3,468 repository)। সবচেয়ে বড় ক্ষতি install ও validate stage-এ (মাত্র 14% পার হয়)।

### ৮.২ Automated Install-এর Validation (Table 3)
Agentless 1 candidate: 6/18 (33%); 3 candidate: 8/18 (44%); 10 candidate: 9/18 (50%); interactive agent 1 trial: 8/18 (44%)। অর্থাৎ 3 candidate-এর agentless আর interactive agent সমান সফল, কিন্তু agentless সস্তা। আমার হিসাবে candidate-গুলো খুব correlated (Section ৬.৫)।

### ৮.৩ Quality Classifier — সম্পূর্ণ Table 4

| Label | Row | Instruct Prec | Instruct Rec | Instruct F1 | Fine-tuned Prec | Fine-tuned Rec | Fine-tuned F1 | Support |
|---|---|---|---|---|---|---|---|---|
| Test Patch Correctness | low-score | 0.59 | 0.97 | 0.73 | 0.66 | 0.85 | 0.74 | 233 |
| Test Patch Correctness | high-score | 0.76 | 0.12 | 0.21 | 0.69 | 0.42 | 0.52 | 180 |
| Test Patch Correctness | accuracy | — | — | 0.60 | — | — | 0.67 | 413 |
| Test Patch Correctness | macro avg | 0.67 | 0.55 | 0.47 | 0.67 | 0.64 | 0.63 | 413 |
| Test Patch Correctness | weighted avg | 0.66 | 0.60 | 0.51 | 0.67 | 0.67 | 0.65 | 413 |
| Task Complexity | low-score | 0.90 | 0.64 | 0.75 | 0.90 | 0.85 | 0.87 | 313 |
| Task Complexity | high-score | 0.41 | 0.78 | 0.54 | 0.60 | 0.71 | 0.65 | 100 |
| Task Complexity | accuracy | — | — | 0.68 | — | — | 0.81 | 413 |
| Task Complexity | macro avg | 0.66 | 0.71 | 0.64 | 0.75 | 0.78 | 0.76 | 413 |
| Task Complexity | weighted avg | 0.78 | 0.68 | 0.70 | 0.83 | 0.81 | 0.82 | 413 |
| Issue Clarity | low-score | 0.83 | 0.94 | 0.88 | 0.82 | 0.94 | 0.88 | 329 |
| Issue Clarity | high-score | 0.51 | 0.26 | 0.35 | 0.47 | 0.20 | 0.28 | 84 |
| Issue Clarity | accuracy | — | — | 0.80 | — | — | 0.79 | 413 |
| Issue Clarity | macro avg | 0.67 | 0.60 | 0.61 | 0.65 | 0.57 | 0.58 | 413 |
| Issue Clarity | weighted avg | 0.77 | 0.80 | 0.77 | 0.75 | 0.79 | 0.76 | 413 |

**পর্যবেক্ষণ:**
- Fine-tuning-এ সবচেয়ে বড় লাভ Test Patch Correctness-এর high-score recall-এ: 0.12 → 0.42 (vanilla প্রায় সব test-কে "ঠিক আছে" বলতো)।
- Task Complexity-তে accuracy 0.68 → 0.81, weighted F1 0.70 → 0.82।
- Issue Clarity-তে fine-tuning কোনো লাভ দেয়নি; high-score recall 0.26 → 0.20 **কমেছে** (Section ৬.১৪-এর বিশ্লেষণ)।
- (Paper "high-score" শুধু Task Complexity-র জন্য সংজ্ঞায়িত করেছে — "> 1 ঘন্টা"। বাকি দুটোতে "high-score" মানে সম্ভবত সমস্যাযুক্ত, কারণ Appendix M বলে কম score = ভালো মান/কম কঠিন — এটা আমার ব্যাখ্যা।)

### ৮.৪ Dataset Statistics (Table 7, Appendix M) — SWE-bench-এর সাথে তুলনা

| Metric | Mean | p50 | p75 | p95 |
|---|---|---|---|---|
| Issue Length (words) | 141.67 | 91 | 173 | 412.25 |
| Files Edited | 3.46 | 2 | 4 | 10 |
| Lines Edited | 142.17 | 37 | 112 | 500 |
| Fail-to-Pass Tests | 14.56 | 2 | 5 | 37 |
| Pass-to-Pass Tests | 85.81 | 22 | 64 | 351 |
| Total Tests | 105.43 | 31 | 82.25 | 428 |
| Difficulty Score | 1.13 | 1 | 2 | 2 |
| Issue Text Score | 1.04 | 1 | 2 | 3 |
| Test Score | 1.38 | 2 | 2 | 3 |

**SWE-bench (Sub-domain 1, Paper 01, Table 1)-এর সাথে তুলনা (আমার):**
| বিষয় | SWE-bench (2,294 task) | SWE-rebench dataset (21,336 task) |
|---|---|---|
| Issue length (mean words) | 195.1 | 141.67 |
| Files edited (mean) | 1.7 | 3.46 |
| F2P tests (mean) | 9.1 | 14.56 (median মাত্র 2) |
| Total tests (mean) | 120.8 | 105.43 |
| Repository | 12 | 3,468 |

**আমার পর্যবেক্ষণ:**
- F2P-এর mean 14.56 কিন্তু median 2 — distribution খুব skewed; অর্ধেক task-এ ≤2টা F2P test। SWE-bench-এর "60% task-এ মাত্র ১টা F2P" সমস্যার মতোই — **দুর্বল test oracle-এর ঝুঁকি (CG1) এখানেও আছে**।
- **Inconsistency:** Appendix M-এর text বলে "added lines গড়ে প্রায় 97, 75th percentile 76", কিন্তু Table 7-এ "Lines Edited" mean 142.17, p75 112। Text আর table ভিন্ন metric (added বনাম edited) বা ভিন্ন version থেকে হতে পারে — আমি table-এর সংখ্যা মূল হিসেবে নিয়েছি।
- Text বলে "tasks typically involve modifications to around 3–4 files", কিন্তু median 2 — "typical" বলতে median-ই বেশি অর্থবহ।

### ৮.৫ Temporal তুলনা — সম্পূর্ণ Table 1 (সব সংখ্যা %; ∗ = 1 March 2025-এর পরে release)

| Model | Jan Resolved | Jan SEM | Jan Pass@5 | Mar–Apr Resolved | Mar–Apr SEM | Mar–Apr Pass@5 |
|---|---|---|---|---|---|---|
| gpt-4.1-2025-04-14∗ | 31.1 | 0.79 | 44.4 | 26.7 | 1.09 | 39.0 |
| DeepSeek-V3-0324∗ | 21.7 | 1.64 | 35.0 | 21.3 | 0.98 | 32.4 |
| DeepSeek-V3-1226 | 19.1 | 0.58 | 33.3 | 21.9 | 1.44 | 31.4 |
| Qwen3-235B-A22B no-think∗ | 15.2 | 1.76 | 29.9 | 16.6 | 0.93 | 25.7 |
| Qwen3-235B-A22B think∗ | 13.7 | 1.81 | 29.9 | 12.2 | 1.33 | 25.7 |
| Qwen3-32B no-think∗ | 13.2 | 1.17 | 23.9 | 13.7 | 1.03 | 26.7 |
| Qwen3-32B think∗ | 11.8 | 0.99 | 22.2 | 11.2 | 0.56 | 21.0 |
| Llama-4-Maverick-Instruct∗ | 8.5 | 0.90 | 20.5 | 12.2 | 1.69 | 27.6 |
| Qwen2.5-72B-Instruct | 8.2 | 0.79 | 18.8 | 9.3 | 1.26 | 19.0 |
| Llama-3.3-70B-Instruct | 8.2 | 0.44 | 15.4 | 11.2 | 0.47 | 22.9 |
| Llama-4-Scout-Instruct∗ | 5.0 | 0.63 | 12.8 | 5.3 | 0.38 | 14.3 |
| gemma-3-27b-it∗ | 4.3 | 0.81 | 9.4 | 4.8 | 0.30 | 10.5 |
| Qwen2.5-Coder-32B-Instruct | 2.7 | 0.57 | 7.7 | 3.2 | 0.77 | 9.5 |

(মূল PDF-এর text extraction-এ table-এর column এলোমেলো হয়েছিল; সংখ্যাগুলো `pdftotext -raw` দিয়ে আবার যাচাই করা।)

### ৮.৬ Verified বনাম SWE-rebench — সম্পূর্ণ Table 2

| Model | Verified Resolved | Verified SEM | Verified Pass@5 | rebench (Mar–Apr) Resolved | SEM | Pass@5 |
|---|---|---|---|---|---|---|
| DeepSeek-V3-0324 | 39.7 | 0.35 | 57.4 | 21.3 | 0.98 | 32.4 |
| DeepSeek-V3-1226 | 35.2 | 0.52 | 51.0 | 21.9 | 1.44 | 31.4 |
| LLaMA-3.3-70B-Instruct | 18.1 | 0.66 | 31.6 | 11.2 | 0.47 | 22.9 |
| LLaMA-4-Maverick-Instruct | 16.0 | 0.79 | 39.2 | 12.2 | 1.69 | 27.6 |
| Qwen2.5-72B-Instruct | 11.3 | 0.35 | 27.8 | 9.3 | 1.26 | 19.0 |
| LLaMA-4-Scout-Instruct | 8.8 | 0.48 | 22.2 | 5.3 | 0.38 | 14.3 |
| Qwen2.5-Coder-32B-Instruct | 4.9 | 0.46 | 16.0 | 3.2 | 0.77 | 9.5 |

Table 2-এর rebench কলাম Table 1-এর Mar–Apr কলামের সাথে হুবহু মেলে (আমি মিলিয়ে দেখেছি)। Gap/ratio বিশ্লেষণ Section ৬.১২-এ।

### ৮.৭ Authors-এর পাঁচটা মূল পর্যবেক্ষণ (Section 3.3)
1. **GPT-4.1** একমাত্র model যার Mar–Apr subset-এ Jan-এর তুলনায় চোখে পড়ার মতো পতন (31.1 → 26.7)।
2. **Llama-4-Maverick**-এর pass@5 একই রকম গড় resolve rate-এর model-দের তুলনায় বেশি (Mar–Apr: 12.2 → pass@5 27.6), অথচ resolve rate সাধারণ — "high potential but inconsistent execution"; জটিল সমস্যার সঠিক সমাধান দিতে পারে, কিন্তু run-ভেদে নির্ভরযোগ্য নয়।
3. **Qwen2.5-Coder-32B-Instruct** প্রত্যাশার চেয়ে খারাপ (Mar–Apr 3.2%) — code generation-এ শক্তিশালী হলেও trajectory-তে instruction following-এর সমস্যা: environment-এর response hallucinate করে, formatting error-এর loop-এ আটকে যায় (Appendix J.2-এর উদাহরণ: "Multiple commands were extracted, but only one is allowed" error-এর পরেও আবার ভুল)।
4. **Qwen3** think আর no-think mode-এ প্রায় একই; কখনো no-think সামান্য ভালো — authors-এর ব্যাখ্যা: base model যথেষ্ট শক্তিশালী, তাই deliberate planning মাপার মতো লাভ দেয় না; pass@5 প্রায় একই।
5. **DeepSeek** model-রা open model-এর মধ্যে দুই rebench subset ও Verified-এ সবচেয়ে ভালো; December ও March দুই version-ই অন্য open model-কে resolve rate ও pass@5-এ ছাড়িয়ে যায় — task distribution বদলালেও robust। কিন্তু rebench-এ দুটো প্রায় সমান, Verified-এ পার্থক্য → পুরনো benchmark-এ সম্ভাব্য contamination effect।

**আমার যাচাই — পর্যবেক্ষণ ৪ পুরোপুরি টেকে না:**
- Qwen3-235B Mar–Apr: no-think 16.6 বনাম think 12.2 — পার্থক্য 4.4 pp; run-only $z = 4.4/\sqrt{0.93^2 + 1.33^2} = 4.4/1.62 \approx 2.7$ (আমার হিসাব) — "প্রায় একই" নয়, no-think স্পষ্টভাবে ভালো।
- Qwen3-32B Mar–Apr pass@5: no-think 26.7 বনাম think 21.0 — "nearly identical pass@5" এখানে খাটে না। শুধু Qwen3-235B-এর pass@5 (29.9/29.9 এবং 25.7/25.7) হুবহু মেলে।
- তাই আমার ভাষায়: "এই scaffold-এ think mode কোনো লাভ দেয়নি, বরং কখনো ক্ষতি করেছে" — যা scaffold-model compatibility-র প্রশ্নও তোলে (think mode-এর লম্বা reasoning 128K context ও one-command format-এর সাথে কেমন খাপ খায়)।

### ৮.৮ Solved Task-এর Overlap (Figure 2, Appendix J)
Figure 2 একটা 5-set Venn diagram — gpt-4.1-2025-04-14, DeepSeek-V3-0324, DeepSeek-V3, Llama-4-Maverick-17B-128E-Instruct, Qwen3-235B-A22B no-thinking — "অন্তত একবার solved" task-এর overlap।
- Figure থেকে আমার পড়া: **49টা task** পাঁচটা model-ই solve করেছে; শুধু GPT-4.1 solve করেছে এমন task **19টা**; শুধু DeepSeek-V3 — 5, শুধু DeepSeek-V3-0324 — 4, শুধু Maverick — 3, শুধু Qwen3-235B no-thinking — 2।
- সব region যোগ করে আমার হিসাবে প্রায় 144টা task অন্তত একটা model অন্তত একবার solve করেছে (ছবি থেকে সংখ্যা পড়া, তাই ±কয়েকটা ভুল সম্ভব; কোন task set — 294 নাকি কোনো subset — figure-এ বলা নেই)।
- Authors-এর উপসংহার: কিছু task নির্দিষ্ট model-ই solve করে — complementary strength। (SWE-bench-এর Claude 2 বনাম SWE-Llama 42% overlap-এর মতো ensemble-এর সুযোগ; Sub-domain 1, Paper 01, Section ৯।)

### ৮.৯ File Count কি Difficulty Proxy? (Appendix F)
DeepSeek-V3-0324, leaderboard task (January–July 2025):
| Changed files | Resolved | n |
|---|---|---|
| 1 file | 28.6% ± 0.8% | 201 |
| 2 files | 20.6% ± 0.4% | 144 |
| ≥ 3 files | 17.5% ± 2.2% | 64 |

Authors: file বাড়লে performance কমে — file count একটা "coarse" difficulty proxy, তবে LLM-এর direct quality assessment ভালো। (আমার statistical যাচাই Section ৬.৮-এর worked example ৩-এ — task-sampling ধরলে 1 বনাম ≥3-এর পার্থক্য সীমারেখায়।)

### ৮.১০ Trajectory উদাহরণ (Appendix J.1, J.2)
- **GPT-4.1 সফল উদাহরণ (scikit-rf):** issue বলে `Network.plot_attribute`-এ `y[x == 1.]` হওয়া উচিত `y[y == 1.]`। Agent `grep -rn "def plot_attribute"` দিয়ে `skrf/network.py:4830` খুঁজে পায় (file-এ 8,517 line), line 4872–4873 edit করে, তারপর `pytest skrf/tests` চালায় — 612 passed, 3 skipped, 4 xfailed (91.69 s)। Checklist-এ স্বীকার করে যে reproduce script লেখেনি, "code inspection"-এ যাচাই করেছে।
- **আমার পর্যবেক্ষণ:** এই "সফল" trajectory-তেও agent নতুন কোনো test বা reproduction script চালায়নি — existing test pass করেছে মানে fix-টা যাচাই হয়েছে তা নয় (existing test হয়তো ঐ line cover-ই করে না)। এটা CG3-এর একটা ছোট কিন্তু স্পষ্ট উদাহরণ: agent-এর self-validation দুর্বল, তবু confident ("This solution is correct and safe to submit")।
- **Qwen2.5-Coder-32B ব্যর্থ উদাহরণ (sqlacodegen):** একাধিক command দেওয়ার error-এর পর আবার একই ধরনের output, environment-এর response নিজে লিখে ফেলা (hallucination)। Authors: নিম্ন-performing model-দের মধ্যে এটা সাধারণ, কিন্তু Qwen2.5-Coder-এ সবচেয়ে প্রকট।

---

## ৯. Key Findings / Insights (Supervisor-কে বলার মতো ৯টা পয়েন্ট)

1. **Executable SWE task সংগ্রহ বড় আকারে automate করা সম্ভব** — 21,336 task, 3,468 repository; তবে yield কম: 4,50,000 থেকে মাত্র ~4.7%, আর install ও validate stage-এ মাত্র ~14% পার হয়।
2. **Environment setup-ই মূল bottleneck** — 18 task-এর study-তে সেরা পদ্ধতিও অর্ধেক task configure করতে পারেনি (9/18)।
3. **LLM দিয়ে task quality label আংশিক কাজ করে** — Task Complexity-তে ভালো (81%), Test Patch Correctness-এ মাঝারি (67%), Issue Clarity-তে majority baseline-এর চেয়ে ভালো নয় (আমার হিসাব)।
4. **তাজা task-এ সব model-এর score Verified-এর চেয়ে কম** — DeepSeek-V3-0324: 39.7 → 21.3; আপেক্ষিক পতন এর সবচেয়ে বেশি, যা contamination-এর সন্দেহ জাগায়।
5. **একই model-এর দুই version Verified-এ আলাদা, তাজা task-এ সমান** — DeepSeek-V3 (39.7 বনাম 35.2 → 21.3 বনাম 21.9)।
6. **Run-to-run variance বাস্তব ও বড়** — SEM সর্বোচ্চ 1.81 (single-run SD ≈ 4 pp); pass@5 আর pass@1-এর ফাঁক 6–15 pp; আমার bound অনুযায়ী GPT-4.1-এর solved task-এর অন্তত 39%, Maverick-এর অন্তত 70% inconsistent।
7. **Scaffold-compatibility ক্ষমতার অংশ** — Qwen2.5-Coder শক্ত code generator হয়েও এই scaffold-এ instruction follow করতে না পেরে ব্যর্থ; think mode লাভ দেয়নি।
8. **Model-দের complementary strength আছে** — 49টা task সবাই পারে, কিন্তু GPT-4.1 একাই 19টা পারে (Figure 2)।
9. **Correctness-এর সংজ্ঞা আগের মতোই test-pass** — F2P median 2; তাই "decontaminated" score-ও plausible-but-wrong patch-কে সঠিক গুনতে পারে (CG1 খোলা)।

---

## ১০. কেন এই Solution অন্যগুলোর থেকে ভালো?

| বৈশিষ্ট্য | HumanEval / LiveCodeBench | SWE-bench / Verified | SWE-Gym (paper-এর বর্ণনা অনুযায়ী) | **SWE-rebench** |
|---|---|---|---|---|
| Task level | Function-level | Repository-level | Repository-level | **Repository-level, interactive** |
| Task নির্মাণ | মানুষ / contest | Semi-automatic + মানুষের environment setup; Verified-এ মানুষের review | Manual curation, অল্প repository | **সম্পূর্ণ automated, LLM-চালিত setup** |
| Repository সংখ্যা | প্রযোজ্য নয় | 12 | সীমিত | **3,468 (dataset), 169 (benchmark)** |
| Task সংখ্যা | ছোট | 2,294 / 500 | সীমিত | **21,336** |
| Update | LiveCodeBench ক্রমাগত (paper অনুযায়ী) | Static | Static | **Continuous, তারিখ-ট্র্যাক করা** |
| Contamination handling | LiveCodeBench temporal | নেই (পুরনো, public) | — | **Release date বনাম task date, leaderboard-এ flag** |
| Evaluation কে চালায় | বিভিন্ন | প্রতিটা দল নিজে | — | **Centralized, fixed scaffold** |
| Variance report | সাধারণত না | সাধারণত একটা run | — | **5 run, SEM, pass@5** |
| RL training-এর উপযোগী | না | Train split আছে কিন্তু environment ছাড়া (Sub-domain 1, Paper 01) | হ্যাঁ, ছোট | **হ্যাঁ, বড় scale-এ executable environment সহ** |
| Quality metadata | না | Verified-এ মানুষের | — | **LLM-predicted 3টা label** |
| Reproducibility | — | Docker harness | — | **Frozen dependency, container image, internal mirror** |

**মূল শক্তি:**
1. **Scale + automation:** মানুষের bottleneck ছাড়া নতুন task নিয়মিত।
2. **Temporal decontamination:** contamination-কে অনুমানের বদলে তারিখ দিয়ে explicit করা।
3. **Fair comparison:** একই scaffold, prompt, context, run সংখ্যা — model-এর তুলনা অর্থবহ।
4. **Statistical honesty (আংশিক):** একাধিক run, SEM, pass@5 — Sub-domain 1-এর বেশিরভাগ paper-এর চেয়ে ভালো।
5. **Engineering refinement:** head_commit diff, deleted test বাদ, `tb=line`, dependency pinning — SWE-bench-এর জানা ত্রুটি ঠিক করা।
6. **Transparency:** সব prompt (install, scaffold) appendix-এ; dataset ও code public।

---

## ১১. কোন পরিস্থিতিতে এই paper/benchmark ভালো কাজ করে, কোথায় করে না

### ✅ ভালো কাজ করে যখন:
- **Model-to-model তুলনা** — একই minimal scaffold-এ raw model ক্ষমতা মাপতে চাও।
- **Contamination-এর ভয় আছে** — নতুন model-কে তার release-এর পরের task-এ মাপতে চাও।
- **RL বা fine-tuning-এর জন্য বড় executable dataset** লাগবে।
- **Variance-সহ reliable estimate** চাও (5 run, SEM, pass@5)।
- **Assurance tool-কে leakage-মুক্ত task-এ যাচাই** করতে চাও (CG10) — task-এর তারিখ judge LLM-এর cutoff-এর পরে বেছে নেওয়া যায়।
- **Task difficulty বা clarity অনুযায়ী subset** বানাতে চাও (label নিখুঁত না হলেও শুরু হিসেবে)।

### ❌ ভালো কাজ করে না / সীমিত যখন:
- **Agent system (scaffold) তুলনা** — এখানে scaffold fixed; কোন scaffold ভালো তা মাপে না।
- **Function-calling-নির্ভর model** — text command format-এ অসুবিধায় পড়তে পারে।
- **অন্য language** — শুধু Python।
- **Patch-এর আসল correctness, security, maintainability** — শুধু test pass (CG1, CG5)।
- **কঠিন, long-horizon, বড় multi-file task** — benchmark-এ ≤3 file, ≤500 শব্দের patch, difficulty < 3।
- **Install করতে কঠিন project** (পুরনো, custom test framework, interactive install) — pipeline এগুলো বাদ দেয়, তাই এই ধরনের বাস্তব bug benchmark-এ কম।
- **Flaky বা network/numeric-নির্ভর bug** — flaky test-এর task বাদ পড়ে, তাই এই ধরনের bug-এ agent কেমন তা মাপা হয় না।
- **Task-level নিশ্চয়তা** — label-গুলো automated; Issue Clarity label প্রায় অকার্যকর (Section ৬.১৪)।

---

## ১২. Limitations — দুর্বলতা

### ১২.১ Authors যা নিজেরা স্বীকার করেছেন (Section 4, Appendix B.5, C, L)
1. **Scalability-র trade-off:** প্রতিটা task হাতে curate ও যাচাই করার ক্ষমতা কম।
2. **Heuristic ও LLM-নির্ভরতা:** filtering, install, quality — সব heuristic বা LLM interpretation; process "inherently imperfect"।
3. **Install prompt মাত্র 18টা repository-তে validate** — অনেক project-এর সূক্ষ্মতা ধরতে পারে না।
4. **Automated quality assessment মানুষের সূক্ষ্ম বিচারের বিকল্প নয়** — label-এ error আছে, dataset-এর মান কমায়।
5. **কিছু task অস্পষ্ট বা শুধু issue থেকে unsolvable** — তাই manually curated benchmark-এর চেয়ে absolute success rate কম হতে পারে।
6. **শুধু Python** — pipeline language-agnostic হলেও অন্য language-এর জন্য language-specific component লাগবে (future work: Go, Java, Rust, JavaScript/TypeScript, C++)।
7. **Install stage-এর success ~14%** — বড় bottleneck; interactive installation-এর অভাব, unpinned/obsolete dependency, flaky test-ই বেশিরভাগ rejection-এর কারণ।
8. **Log parsing-এর সীমা** — custom test framework (যেমন Django) generic parser পড়তে পারে না।
9. **Broader impact:** autonomous agent-এর অগ্রগতি দ্রুত করলে AI-generated code-এর উপর অতিরিক্ত নির্ভরতা বা vulnerability ঢোকাতে agent-এর অপব্যবহারের ঝুঁকি।
10. **Statistical:** checklist-এ স্বীকার — normality ধরে নেওয়া হয়নি, confidence interval হিসাব করা হয়নি; শুধু SEM।

**Future work (Section 5):** arbitrary PR থেকে task (issue ছাড়াই), filtering heuristic উন্নত করা, নতুন language, benchmark নিয়মিত update ও আরও model। Appendix L-এ আরও: test নেই এমন PR-এর জন্য LLM দিয়ে test তৈরি (যাচাইসহ), ভালো install model, জনপ্রিয় repo-তে বেশি resource-এর interactive agent।

### ১২.২ আমার Critical Analysis (Professor-level observation)
1. **Correctness-এর সংজ্ঞা অপরিবর্তিত (CG1 খোলা):** "Resolved" = test patch-এর F2P ও P2P pass। F2P median মাত্র 2; তাই দুর্বল test plausible-but-incorrect patch-কে resolved গুনতে পারে। Decontamination মুখস্থ সমস্যা কমায়, কিন্তু overfitting সমস্যা ছোঁয় না। AutoCodeRover-এর 65.4% correctness (Sub-domain 1) এখানেও প্রযোজ্য হতে পারে — কেউ মাপেনি।
2. **Quality check-এর দিক একতরফা:** Test Patch Correctness label-এর সংজ্ঞা — test যেন "নির্দিষ্ট implementation-এর উপর অতিরিক্ত নির্ভর না করে"। এটা মূলত **false negative** (সঠিক সমাধান fail করা) ঠেকায় — RL reward-এর জন্য। কিন্তু **false positive** (ভুল সমাধান pass করা, অর্থাৎ test দুর্বল) আলাদাভাবে লক্ষ্য করা হয়নি। আমাদের assurance-এর জন্য দ্বিতীয়টাই বেশি গুরুত্বপূর্ণ।
3. **Quality label দুর্বল, আর benchmark তা ব্যবহারও করে না:** Issue Clarity classifier majority baseline-এর সমান (79% বনাম 79.7%), high-score recall 0.20। আর Appendix H-এর 8টা benchmark filter-এ শুধু **difficulty** label ব্যবহার হয় — clarity বা test label নয়। তাই 294 task-এর মধ্যে কতগুলো অস্পষ্ট বা ত্রুটিপূর্ণ, অজানা। Verified-এর সাথে তুলনায় "সব model-এর পতন"-এর একটা অংশ এই task noise হতে পারে।
4. **Classifier-এর domain shift:** label শেখানো হয়েছে SWE-bench Verified-এর annotation দিয়ে — যেগুলো 12টা জনপ্রিয় repository থেকে; প্রয়োগ হয়েছে 3,468টা repository-তে। Validation একই distribution-এ (Verified-এর 25%) — নতুন repository-তে label কতটা ঠিক, যাচাই হয়নি। (Sub-domain 2 Summary-র CG10 সতর্কতা এখানে সরাসরি খাটে।)
5. **Statistical rigor অসম্পূর্ণ (CG8):** SEM শুধু run-sampling ধরে; task-sampling (আমার হিসাবে ≈ 2.7 pp, SEM-এর প্রায় 3.5 গুণ) উপেক্ষিত। Subset-এর আকার report নেই, significance test নেই। GPT-4.1-এর পতন আমার assumption-এ significant নয় (Section ৬.৮)।
6. **Contamination প্রমাণ correlational:** (ক) Verified আর rebench ভিন্ন distribution — Verified মানুষ দিয়ে solvable নিশ্চিত, rebench automated; (খ) Mar–Apr subset clean model-দের জন্য গড়ে +1.85 pp সহজ (আমার DiD); (গ) release date ≠ training cutoff — paper কোনো model-এর cutoff ব্যবহার করেনি। সবচেয়ে শক্ত প্রমাণ — একই task-এ দুই DeepSeek version-এর আপেক্ষিক অবস্থান বদল — তবে সেটাও একটা মাত্র জোড়া।
7. **Temporal decontamination-এর সীমা:** (ক) **Repository-level familiarity** — model ঐ repository-র পুরনো code training-এ দেখেছে; নতুন issue হলেও codebase "চেনা"। জনপ্রিয় repo-র task তাই সহজ হতে পারে — paper এটা মাপেনি। (খ) Task publish হওয়ার পর পরের model-এর training-এ ঢুকবে — benchmark-কে চিরকাল rolling রাখতে হবে, আর পুরনো score অতুলনীয় হয়ে যাবে।
8. **একটা scaffold = construct validity প্রশ্ন:** authors নিজেই বলেছেন এটা "instruction follow করে framework-এ কাজ করার ক্ষমতা"-ও মাপে। Function calling বাদ দেওয়া, one-command নিয়ম — কিছু model-কে অসুবিধায় ফেলে (Qwen2.5-Coder, Qwen3 think)। তাই leaderboard ranking "এই scaffold-এ" ranking, সাধারণ ক্ষমতার নয়।
9. **Selection bias:** install-যোগ্য repository (~10.8% repo-তে task) আর non-flaky test-ওয়ালা task-ই টিকে থাকে — ভালো packaging-ওয়ালা, deterministic project-এর দিকে ঝোঁক। Network, numeric, পুরনো project-এর bug কম।
10. **Benchmark ছোট ও সহজ দিকে ঝোঁকা:** 294 task; ≤3 file, ≤500 শব্দ, difficulty < 3, F2P ≤ 50 — তুলনামূলক সহজ task। ভবিষ্যতে saturation দ্রুত আসতে পারে (Sub-domain 1-এর SWE-Bench Pro এই দিকটা ধরবে বলে মনে হয়)।
11. **Paper-এর ভেতরের অসংগতি:** (ক) Table 7 "Lines Edited" mean 142.17 বনাম text-এ "added lines ≈ 97, p75 76"; (খ) >3,800 example বনাম 413 validation-এর 25%; (গ) "private" বনাম "public" leaderboard; (ঘ) Qwen3 "nearly identical pass@5" দাবি 32B Mar–Apr-এ খাটে না (26.7 বনাম 21.0); (ঙ) Section 4-এ classifier "complexity and relevance" predict করে বলা হয়েছে, অথচ Section 2.4-এ তিনটা label-এর নাম Issue Clarity, Task Complexity ও Test Patch Correctness — "relevance" নামে কোনো label নেই।
12. **Cost/efficiency report নেই:** token, step সংখ্যা, USD — শুধু DeepSeek-V3-এর 7 ঘন্টা। Sub-domain 1-এর CG8-এর cost-তুলনার সমস্যা এখানে সমাধান হয়নি।
13. **Consistency বিশ্লেষণ অগভীর:** pass@5 আছে, কিন্তু pass^k, প্রতি task-এর flip rate, বা কোন task flip করে তার বৈশিষ্ট্য নেই। Figure 2-ও শুধু "অন্তত একবার" overlap দেখায়।
14. **Security ও code quality একেবারেই নেই (CG5)** — অথচ broader impact-এ নিজেরাই vulnerability-র ঝুঁকি উল্লেখ করেছেন।
15. **Agent-এর test-modification নিয়ম:** scaffold বলে "test বদলাবে না", কিন্তু evaluation-এ test patch apply-এর সময় agent-এর test-সংক্রান্ত পরিবর্তন কীভাবে handle হয় — paper স্পষ্ট নয়। একটা agent test file বদলে "পাস" করানোর চেষ্টা করলে কী হয়, সেটা assurance-এর দৃষ্টিতে গুরুত্বপূর্ণ প্রশ্ন।

---

## ১৩. Research Gaps — কোথায় কাজ করার সুযোগ আছে

### ১৩.১ আমাদের Common Gap (CG1–CG10)-এর অবস্থা — SWE-rebench কী সমাধান করলো

| CG | Gap | SWE-rebench কী করে | অবস্থা |
|---|---|---|---|
| CG1 | Plausible patch-এর correctness যাচাই | কিছুই না — test-pass-ই সংজ্ঞা; F2P median 2 | **খোলা** (বরং তাজা task-এ মাপার সুযোগ দেয়) |
| CG2 | Candidate selection / re-ranking | করে না; তবে 5 run-এর trajectory = প্রতি task-এ 5টা candidate patch — re-ranking-এর data | **খোলা, নতুন data-উৎস** |
| CG3 | Generated / validation test-এর মান | Agent-এর self-test (J.1-এ reproduction ছাড়াই "safe to submit"); future work-এ LLM-generated test (যাচাই লাগবে) | **খোলা, আরও শক্ত প্রমাণ** |
| CG4 | Run-to-run reliability | 5 run, SEM, pass@5; Maverick-এর inconsistency উল্লেখ | **আংশিক সমাধান** — pass^k, flip rate নেই (আমার bound দেখায় সমস্যা বড়) |
| CG5 | Patch-এর security ও quality | নেই; broader impact-এ ঝুঁকি স্বীকার | **খোলা** |
| CG6 | Benchmark quality ও contamination | Temporal decontamination, leaderboard flag, LLM quality label, Appendix G refinement | **অনেকটা সমাধান** — কিন্তু label দুর্বল, প্রমাণ correlational |
| CG7 | Confidence ও abstention | নেই; agent সবসময় submit করে | **খোলা** |
| CG8 | Evaluation-এর সমতা ও statistical rigor | Centralized, fixed scaffold, same prompt/context, 5 run, SEM | **আংশিক সমাধান** — task-level CI, significance test, cost নেই |
| CG9 | APCA-কে Python repository-level agent patch-এ নেওয়া | সরাসরি নয়; কিন্তু 21K Python repo-level executable task = APCA-র জন্য বড় testbed | **সুযোগ তৈরি করে** |
| CG10 | Assurance tool-এর নিজের evaluation validity | Task creation date দেওয়া; temporal split সহজ | **সমাধানের হাতিয়ার দেয়** |

### ১৩.২ আমাদের Assurance Layer কি SWE-rebench-এ evaluate করা যায়? (CG10)
**হ্যাঁ — এবং এটাই সম্ভবত সবচেয়ে বাস্তবসম্মত পথ (আমার প্রস্তাব):**
1. **Leakage-মুক্ত task বাছাই:** আমাদের judge-LLM (যেমন RePaCA-ধরনের reasoning model) আর patch-generating agent-এর knowledge cutoff / release date-এর **পরে** তৈরি task নেওয়া ($B_m$, Section ৬.১১)। তাহলে judge-ও gold patch দেখেনি, agent-ও না।
2. **Candidate patch সংগ্রহ:** প্রতিটা task-এ agent-কে $K$ বার চালিয়ে patch (একই সাথে CG4-এর data)। Leaderboard-এর trajectory/patch public হলে খরচ কমে — এটা website-এ যাচাই করতে হবে।
3. **Label তৈরি:** (ক) hidden F2P/P2P test দিয়ে plausible চিহ্নিত; (খ) **gold patch আছে** — তাই agent patch আর gold patch-এর মধ্যে আচরণগত পার্থক্য খুঁজতে differential test generate করা যায় (LLM Test Generation sub-domain); (গ) একটা ছোট subset হাতে review — "plausible কিন্তু ভুল" label।
4. **Assurance layer চালানো:** static judge + extra test + security scan + consistency signal → score; তারপর precision/recall/specificity, balanced accuracy, MCC, task-level bootstrap CI (Sub-domain 2-এর শিক্ষা)।
5. **Classifier-এর label-কে feature হিসেবে:** `test_score`, `issue_text_score` — দুর্বল test-ওয়ালা task-এ overfitting বেশি কিনা পরীক্ষা।

**সতর্কতা:** (ক) Correctness label-এর জন্য আবার test-এর উপর নির্ভর করলে circularity (CG1); তাই অন্তত একটা human-reviewed subset লাগবে। (খ) Quality classifier Verified-এ train হওয়ায় Verified-এর task আলাদা রাখতে হবে। (গ) Install করা environment-এর container image public কিনা, নাকি নিজে build করতে হবে — dataset card দেখে যাচাই।

### ১৩.৩ Research Gap Table (আমাদের sub-domain folder-এর সাথে link)

| # | Gap | কেন গুরুত্বপূর্ণ | কোন sub-domain folder-এ আরও পড়তে হবে |
|---|---|---|---|
| G1 | **Decontaminated benchmark-এ patch overfitting কত?** — SWE-rebench-এর resolved patch-এর কত % আসলে সঠিক | Contamination বাদ দিলেও "resolved ≠ correct" কিনা জানা নেই | Patch Validation; Automated Program Repair |
| G2 | **Reliability metric: pass^k, flip rate, flip-prone task চেনা** | গড় score নির্দিষ্ট task-এ বিশ্বাসযোগ্যতা বলে না | Coding-Agent Evaluation & Reliability (Engineering Reliable Coding Agents); Trustworthy AI for SE |
| G3 | **Automated task label-এর নির্ভরযোগ্যতা** — বিশেষত Issue Clarity ও দুর্বল test (false positive) চেনা | Benchmark noise score-এর পতনকে ভুলভাবে contamination মনে করাতে পারে | LLM Test Generation; Patch Validation |
| G4 | **Task-level statistical inference** — CI, paired test, subset-আকার report | ছোট পার্থক্যকে ভুলভাবে significant বলা | Coding-Agent Evaluation & Reliability; Trustworthy AI for SE |
| G5 | **Contamination-এর causal পরিমাপ** — cutoff-জানা model, DiD, repo-familiarity আলাদা করা | "মুখস্থ" বনাম "চেনা codebase" বনাম "সহজ subset" পৃথক করা | Coding-Agent Evaluation & Reliability; Automated Program Repair (APR Survey-এর leakage আলোচনা) |
| G6 | **Agent patch-এর security ও quality — তাজা task-এ** | নতুন vulnerability তৈরি হয় কিনা কেউ মাপছে না | Security of AI-Generated Code |
| G7 | **Agent-এর self-validation-এর মান** — reproduction ছাড়াই "safe to submit" | Agent-এর confidence আর আসল correctness-এর ফাঁক | LLM Test Generation; AI Coding Agents |
| G8 | **Scaffold-robust evaluation** — একাধিক scaffold-এ model ranking কতটা স্থির | Single-scaffold ranking-এর construct validity | AI Coding Agents (SWE-agent, Agentless) |
| G9 | **Confidence ও abstention** — agent কখন "নিশ্চিত নই" বলবে | Flip-prone task-এ abstain করলে ভুল patch কমে | Trustworthy AI for Software Engineering |
| G10 | **Python-এর বাইরে ও কঠিন task** | Benchmark ≤3 file, সহজ দিকে; শুধু Python | Coding-Agent Evaluation & Reliability (SWE-Bench Pro) |

### ১৩.৪ প্রস্তাবিত নতুন Common Gap (Sub-domain 3 Summary-তে চূড়ান্ত হবে)
- **CG11 (প্রস্তাব): Automated benchmark-এর label noise ও তার evaluation-এ প্রভাব** — LLM-labeled task quality (Issue Clarity accuracy majority baseline-এর সমান) কীভাবে score ও contamination সিদ্ধান্তকে বিকৃত করে। এটা CG6-এর অংশ হিসেবেও রাখা যায় — Sub-domain 3-এর বাকি দুটো paper পড়ে ঠিক করবো।

---

## ১৪. কী করলে আরও ভালো হবে — Improvement Ideas

1. **Beyond-test verification layer:** resolved patch-এ (ক) gold patch-এর সাথে differential testing, (খ) LLM-generated extra test, (গ) static judge — "resolved" ও "verified-correct" দুটো আলাদা কলাম leaderboard-এ। (আমার প্রস্তাব, আমাদের assurance layer-এর সাথে মেলে।)
2. **Reliability কলাম:** pass^5 ও flip rate (প্রতি task-এ $c_i \in \{1,2,3,4\}$-এর অনুপাত) — 5 run-এর data থেকেই সরাসরি হিসাব করা যায়, অতিরিক্ত খরচ নেই।
3. **Task-level CI:** task-এর উপর bootstrap করে 95% CI; model জোড়ায় paired test (McNemar বা paired bootstrap); subset-এর আকার সবসময় report।
4. **Contamination-এর জন্য DiD design:** cutoff-জানা model-দের control group হিসেবে রেখে "সন্দেহভাজন" model-এর অতিরিক্ত পতন মাপা (Section ৬.১৩-এর মতো)।
5. **Label audit:** র‍্যান্ডম 100টা task মানুষ দিয়ে annotate করে LLM label-এর নতুন-repository-তে accuracy মাপা; Issue Clarity-র জন্য cost-sensitive threshold বা minority-class oversampling।
6. **False-positive-oriented test label:** "test কি দুর্বল — ভুল patch-ও pass করবে?" — mutation testing (gold patch-এ ছোট পরিবর্তন করে test ধরে কিনা) দিয়ে automated "test adequacy" score।
7. **Multi-scaffold evaluation:** অন্তত দুটো scaffold (text command ও function calling) — ranking কতটা স্থির, report।
8. **Cost ও efficiency:** token, step, wall-clock, USD প্রতি task।
9. **Security scan:** প্রতিটা resolved patch-এ Bandit/Semgrep-এর মতো static analyzer (CG5)।
10. **Repository-familiarity control:** জনপ্রিয় বনাম অপরিচিত repository-তে performance আলাদা report।

---

## ১৫. কোন Gap-এ Research করলে ভালো Result ও Publication আসতে পারে

> ⚠️ Sub-domain 3-এর প্রথম paper-এর ভিত্তিতে প্রাথমিক মত। SWE-Bench Pro ও Engineering Reliable Coding Agents পড়ার পর আপডেট করবো।

| Gap / Idea | SPL3-তে করা সম্ভব? | Novelty | Publication সম্ভাবনা |
|---|---|---|---|
| **A. Decontaminated overfitting audit:** SWE-rebench-এর 2025-এর task-এ এক বা দুটো agent চালিয়ে resolved patch-এর কত % আসলে সঠিক — differential test + manual review (G1, CG1, CG10) | ✅ হ্যাঁ — 30–50 task, 1–2টা সস্তা model, 3 run | উচ্চ — contamination-free setting-এ overfitting-এর হার (আমার জানামতে খুব কম কাজ; literature search-এ নিশ্চিত করতে হবে) | ⭐⭐⭐⭐⭐ |
| **B. Assurance layer evaluation on fresh tasks:** আমাদের static judge + dynamic test signal-কে judge-এর cutoff-এর পরের task-এ যাচাই (CG9, CG10) | ✅ হ্যাঁ, A-এর data-র উপর | উচ্চ — domain-এর নামের সাথে সরাসরি মেলে | ⭐⭐⭐⭐⭐ |
| **C. Reliability metrics from multi-run data:** pass^k bound, flip rate, flip-prone task predictor (G2, CG4) | ✅ হ্যাঁ — নিজের ছোট run বা public data থাকলে প্রায় শূন্য খরচ | মাঝারি-উচ্চ | ⭐⭐⭐⭐ |
| **D. LLM task-label audit:** 100টা task হাতে label করে SWE-rebench label-এর accuracy (G3, CG11) | ✅ হ্যাঁ — শুধু মানুষের সময় লাগে | মাঝারি | ⭐⭐⭐ (workshop/short paper) |
| E. নতুন language-এ pipeline | ⚠️ কঠিন — অনেক infrastructure | মাঝারি | ⭐⭐ |

**সবচেয়ে সম্ভাবনাময় নির্দিষ্ট প্রশ্ন (আমার মত):**
> "Contamination-মুক্ত, তাজা SWE task-এ AI agent-এর 'resolved' patch-এর কত অংশ আসলে সঠিক, আর static reasoning judge + dynamic test signal মিলিয়ে একটা assurance layer কি সেগুলোকে নির্ভরযোগ্যভাবে আলাদা করতে পারে — run-to-run consistency-কে একটা অতিরিক্ত signal হিসেবে ব্যবহার করে?"

এটা A + B + C একসাথে — CG1, CG4, CG9, CG10 ধরে।

**সম্ভাব্য venue (general guidance):** ICSE, FSE, ASE, ISSTA-র মূল track বা তাদের workshop (যেমন LLM4Code); NeurIPS/ICLR-এর Datasets & Benchmarks track (evaluation-methodology কাজের জন্য); journal — ACM TOSEM, IEEE TSE, EMSE, JSS, IST।

---

## ১৬. SPL3 Implementation Perspective — Software-এ কীভাবে আনবো

**Paper implement করা মানে কী?** পুরো 21K-task pipeline আবার বানানো নয় (TractoAI cluster, H200 লাগে)। বরং SWE-rebench-এর **dataset ও evaluation protocol** ব্যবহার করে একটা "Decontaminated Reliability & Assurance Evaluator" বানানো।

**প্রস্তাবিত module:**
1. **Task Selector:** Hugging Face থেকে `nebius/SWE-rebench` load; filter — `created_at` > নির্বাচিত model-এর cutoff/release date, `num_modified_files` ≤ 3, `llm_score`-এর difficulty/clarity/test, F2P সংখ্যা; Appendix H-এর 8টা filter পুনর্গঠন।
2. **Environment Manager:** `install_config` আর frozen `requirements`/`environment` দিয়ে container build বা `SWE-rebench/SWE-bench-fork`-এর harness ব্যবহার; ছোট pilot-এ Table 3-এর মতো install success মাপা।
3. **Agent Runner:** Appendix I-এর minimal ReAct scaffold (বা ছোট একটা open-source agent); প্রতিটা task $K$ বার (3–5), ভিন্ন seed।
4. **Statistics Module:** resolved গড়, SEM, $t$-CI, task-level bootstrap CI, pass@k, pass^k, flip rate, Section ৬.৯-এর bound, paired comparison।
5. **Contamination Module:** model-এর তারিখ বনাম task তারিখ; pre/post তুলনা; DiD।
6. **Assurance Layer (আমাদের gap অংশ):** static judge, extra/differential test (gold patch দিয়ে), Bandit/Semgrep, consistency signal → assurance score।
7. **Dashboard:** resolved বনাম verified-correct, CI bar, flip-prone task তালিকা, security finding।

**Practical সতর্কতা:**
- Windows-এ WSL2 + Docker Desktop লাগবে (Sub-domain 1-এর মতো)। প্রতিটা task-এর environment build-এ disk ও সময় লাগে — 30–50 task দিয়ে শুরু।
- 294 task × 5 run বড় model-এ খুব ব্যয়বহুল (DeepSeek-V3-এর একটা run ≈ 7 ঘন্টা, 16টা H200-এ)। তাই ছোট/সস্তা model ও ছোট subset; API খরচ আগে হিসাব।
- Install recipe সব task-এ কাজ নাও করতে পারে (paper-এর validation-ও নিখুঁত নয়) — fail হওয়া task log করে বাদ দেওয়া এবং report করা।
- Leaderboard-এর trajectory বা patch public কিনা, আর dataset-এর container image সরাসরি পাওয়া যায় কিনা — website ও dataset card দেখে নিশ্চিত হতে হবে (paper এ বিষয়ে নিশ্চিত তথ্য দেয় না)।

---

## ১৭. পরবর্তী গবেষণায় এই Paper-এর প্রভাব (Context)

- **Paper নিজেই জানিয়েছে:** SWE-rebench dataset সরাসরি ব্যবহার করেছে Kimi-dev (Yang et al., 2025b); আরও কিছু কাজ (DeepSWE, SkyRL-v0) RL দিয়ে SWE agent train করছে — এই ধরনের বড় executable dataset-এর চাহিদা দেখায়। পূর্বসূরি SWE-bench Extra-ও open-source SWE agent train করতে ব্যবহার হয়েছে বলে authors উল্লেখ করেছেন।
- **Related work অনুযায়ী অবস্থান:** SWE-bench+ (post-cutoff filtering) ও Multi-SWE-bench (multilingual) manual construction-এর উপর নির্ভরশীল; SWE-smith (কৃত্রিম bug inject) ও RepoST (synthetic test) scale দেয় কিন্তু বাস্তবতা কম — SWE-rebench বাস্তব task + automation-এর মাঝামাঝি জায়গা নিতে চায় (paper-এর দাবি)।
- **আমাদের folder-এর পরের paper:** SWE-Bench Pro (long-horizon, কঠিন task) — SWE-rebench-এর "সহজ দিকে ঝোঁক" (G10) কতটা পূরণ করে দেখবো; Engineering Reliable Coding Agents — reliability-র বড় কাঠামো, CG4-এর জন্য। (এগুলোর বিষয়বস্তু সেই paper পড়ার পর নিশ্চিত করবো।)
- **বড় ছবি:** Sub-domain 1-এ প্রশ্ন ছিল "কত % solve?"; Sub-domain 2-এ "solve করা patch সঠিক কি?"; এই paper যোগ করলো "**score-টা নিজেই বিশ্বাসযোগ্য কি** — contamination, scaffold, variance বাদ দিলে?" Assurance-এর দৃষ্টিতে তিনটা স্তর: task-এর validity → score-এর validity → patch-এর validity। SWE-rebench প্রথম দুটোতে বড় অগ্রগতি, তৃতীয়টা (আমাদের কাজ) খোলা।

---

## ১৮. Supervisor-এর সম্ভাব্য প্রশ্ন ও উত্তর (Viva Prep)

**Q1. SWE-rebench আর SWE-bench-এর মূল পার্থক্য কী?**
A: SWE-bench 12টা repository থেকে 2,294 task, environment হাতে configure করা, static। SWE-rebench সম্পূর্ণ automated — LLM দিয়ে install recipe, test চালিয়ে যাচাই, 3,468 repository থেকে 21,336 task; আর benchmark অংশ ক্রমাগত নতুন task দিয়ে update হয়, task-এর তারিখ ট্র্যাক করে contamination চিহ্নিত করে। Evaluation-ও centralized: একই scaffold, 5 run।

**Q2. "Decontaminated" বলতে এখানে ঠিক কী বোঝায়?**
A: Temporal decontamination — task-এর issue model release-এর পরে তৈরি হলে সেই model সেটা training-এ দেখেনি ধরে নেওয়া হয়; আগে হলে leaderboard-এ "potentially contaminated" চিহ্ন। এটা training data পরীক্ষা করে প্রমাণ নয়, তারিখভিত্তিক নিয়ম। Release date ব্যবহার করে, training cutoff নয় — তাই নিয়মটা রক্ষণশীল; আর repository-র পুরনো code model দেখে থাকতে পারে, সেটা এই নিয়ম ধরে না।

**Q3. Contamination-এর সবচেয়ে শক্ত প্রমাণ কোনটা, আর দুর্বলতা কী?**
A: শক্ত অংশ — DeepSeek-V3-এর দুই version Verified-এ 39.7 বনাম 35.2, কিন্তু তাজা task-এ 21.3 বনাম 21.9; একই task-এ তুলনা, তাই পার্থক্য উধাও হওয়া অর্থবহ। আর DeepSeek-V3-0324-এর আপেক্ষিক পতন সবচেয়ে বেশি (ধরে রাখে 54%, গড় 66% — আমার হিসাব)। দুর্বলতা — সব model-এরই পতন হয়েছে, কারণ rebench-এর task automated ও noisy হতে পারে; GPT-4.1-এর temporal পতন subset-এর আকার না জেনে significant বলা যায় না।

**Q4. SEM কী মাপে, আর কী মাপে না?**
A: SEM = 5 run-এর resolved rate-এর SD ভাগ $\sqrt{5}$ — একই task-এ run-এর এলোমেলোতার কারণে গড়ের অনিশ্চয়তা। এটা task-sampling-এর অনিশ্চয়তা ধরে না। আমার হিসাবে 294 task-এ ~31% score-এর task-level SE প্রায় 2.7 pp, যেখানে SEM 0.79 — অর্থাৎ আসল অনিশ্চয়তা অনেক বড়। Paper নিজেও স্বীকার করেছে CI দেয়নি।

**Q5. pass@5 আর pass@1-এর পার্থক্য reliability সম্পর্কে কী বলে?**
A: ফাঁক বড় মানে অনেক task কখনো solve হয়, কখনো হয় না। আমি দেখিয়েছি $B \geq (p_5 - \bar{r})/0.8$ — GPT-4.1-এর অন্তত 15.4% task inconsistent, যা তার solved task-এর অন্তত 39%; Maverick-এর ক্ষেত্রে অন্তত 70%। এটা pass^k বা flip rate-এর মতো reliability metric-এর দরকার দেখায় (CG4)।

**Q6. কেন একটা fixed scaffold ব্যবহার করা হলো? এর অসুবিধা কী?**
A: যাতে model-এর raw ক্ষমতা ন্যায্যভাবে তুলনা করা যায় — engineered prompt, retry, best-of-N বাদ দিয়ে। অসুবিধা — এটা "এই scaffold-এ কাজ করার ক্ষমতা"-ও মাপে; function calling বন্ধ, one-command নিয়ম। Qwen2.5-Coder ভালো code generator হয়েও format error-এর loop-এ আটকে 3.2% পেয়েছে। তাই ranking scaffold-নির্ভর।

**Q7. Environment setup কীভাবে automate করা হয়েছে, আর কতটা সফল?**
A: Version group (git tag → major.minor, ~95% task-এ পাওয়া যায়), group-এর সবচেয়ে নতুন base commit, তারপর Qwen2.5-72B দিয়ে তিন ধাপ — relevant file খোঁজা (≤10), JSON recipe, fail হলে error log দিয়ে refine; সর্বোচ্চ 3 candidate। 31% repository-তে অন্তত একটা task-এর recipe কাজ করে; install-validate stage-এ ~14% task পার হয়। 18-task study-তে agentless 3 candidate 8/18, interactive agent 8/18, 10 candidate 9/18।

**Q8. LLM quality label কতটা বিশ্বাসযোগ্য?**
A: মিশ্র। Task Complexity ভালো (81%, weighted F1 0.82; vanilla 68%)। Test Patch Correctness মাঝারি (67%)। Issue Clarity 79% — কিন্তু সবসময় "পরিষ্কার" বললেই 79.7% পাওয়া যেত, আর সমস্যাযুক্ত issue-র recall মাত্র 0.20। তাই clarity label দিয়ে filter করা ঝুঁকিপূর্ণ; benchmark-ও শুধু difficulty label ব্যবহার করে।

**Q9. SWE-rebench কি আমাদের CG1 (patch overfitting) সমাধান করে?**
A: না। "Resolved"-এর সংজ্ঞা SWE-bench-এর মতোই — test patch-এর F2P ও P2P pass। F2P-এর median মাত্র 2। তাদের Test Patch Correctness label মূলত সঠিক সমাধান fail করা (false negative) ঠেকাতে, দুর্বল test-এ ভুল patch pass করা (false positive) নয়। তবে এটা CG1 মাপার জন্য একটা পরিষ্কার জায়গা দেয় — contamination ছাড়া।

**Q10. তোমার assurance layer SWE-rebench-এ কীভাবে evaluate করবে?**
A: Judge LLM ও agent-এর cutoff-এর পরের task বাছাই করবো (CG10), agent-কে 3–5 বার চালিয়ে patch নেবো, hidden test দিয়ে plausible চিহ্নিত, gold patch-এর সাথে differential test আর একটা ছোট human-review subset দিয়ে correct/overfitting label, তারপর assurance score-এর precision, recall, specificity, MCC ও task-level bootstrap CI। Consistency (flip) নিজেও একটা signal।

**Q11. Mar–Apr subset কি Jan-এর চেয়ে সহজ? এটা কেন গুরুত্বপূর্ণ?**
A: যে চারটা model ∗-চিহ্নহীন এবং 2025-এর আগে release বলে ধরে নিয়েছি (দুটো subset-ই তাদের জন্য পরিষ্কার), তাদের গড় +1.85 pp বেড়েছে — তাই Mar–Apr সম্ভবত একটু সহজ (আমার হিসাব)। এটা ধরলে GPT-4.1-এর অতিরিক্ত পতন প্রায় 6.25 pp (difference-in-differences)। গুরুত্ব: subset-এর কঠিনতা আলাদা হলে শুধু কাঁচা পতন দেখে contamination বলা যায় না।

**Q12. Pipeline-এ selection bias কোথায়?**
A: যে project সহজে install হয় আর যার test deterministic, শুধু সেগুলো টিকে থাকে — 32K repository-র মাত্র ~10.8%-এ valid task। Flaky test (network, floating-point) বাদ পড়ে, পুরনো interactive-install project বাদ পড়ে। তাই benchmark একটা নির্দিষ্ট ধরনের "পরিষ্কার" project-এর দিকে ঝোঁকা; বাস্তবের সব bug প্রতিনিধিত্ব করে না।

**Q13. Paper-এর কোনো দাবি কি তুমি যাচাই করে টেকেনি বলে পেয়েছো?**
A: হ্যাঁ — Qwen3 think বনাম no-think "প্রায় একই" আর "nearly identical pass@5"। Qwen3-235B Mar–Apr-এ no-think 16.6 বনাম think 12.2 (run-only z ≈ 2.7), আর Qwen3-32B Mar–Apr pass@5 26.7 বনাম 21.0। এছাড়া Table 7-এর "Lines Edited" (mean 142.17) আর text-এর "added lines ≈ 97"-এর অমিল।

---

## ১৯. Glossary (দ্রুত মনে রাখার জন্য)

| Term | অর্থ |
|---|---|
| Task mining | Program দিয়ে GitHub থেকে issue + fix + test জোড়া স্বয়ংক্রিয়ভাবে সংগ্রহ |
| GH Archive | GitHub-এর সব public event-এর দৈনিক JSON archive |
| Solution patch / Test patch | PR-এর non-test পরিবর্তন / শুধু test file-এর পরিবর্তন |
| head_commit | PR branch-এর শেষ commit — patch বানাতে ব্যবহার |
| Install recipe | Environment setup-এর JSON নির্দেশনা (python, install, test_cmd ইত্যাদি) |
| Agentless setup | LLM নির্দিষ্ট ধাপে recipe লেখে, নিজে command চালায় না |
| Interactive agent | LLM container-এ সরাসরি command চালিয়ে trial-and-error করে |
| Dependency pinning | Exact library version লিখে রাখা (pip freeze, conda env export) |
| Container image | Reproducible চালানোর পরিবেশের ছাঁচ |
| Execution-based validation | Test চালিয়ে task-এর বৈধতা যাচাই |
| Flaky test | একই code-এ কখনো pass, কখনো fail |
| Quality label | LLM-predicted Issue Clarity, Task Complexity, Test Patch Correctness |
| Majority baseline | সবসময় বড় class বলা classifier-এর accuracy |
| Decontamination (temporal) | Model-এর তারিখের পরের task-এ মূল্যায়ন |
| Release date বনাম cutoff | Model public হওয়ার তারিখ বনাম training data সংগ্রহের শেষ তারিখ |
| Rolling benchmark | নিয়মিত নতুন task যোগ হওয়া benchmark |
| Scaffold | LLM-এর চারপাশের agent software (prompt, tool, loop) |
| ReAct | Reasoning + Action পর্যায়ক্রমে |
| Centralized leaderboard | Benchmark দল নিজেই সব model একই নিয়মে চালায় |
| SEM | Run-এর SD ভাগ $\sqrt{K}$ — গড়ের অনিশ্চয়তা |
| Task-sampling uncertainty | কোন task নমুনায় এলো তার কারণে score-এর অনিশ্চয়তা |
| pass@k / pass^k | k বারে অন্তত একবার / সববার সফল |
| Flip / inconsistent task | কিছু run-এ solved, কিছুতে নয় |
| Difference-in-differences | Control group-এর পরিবর্তন বাদ দিয়ে অতিরিক্ত পরিবর্তন মাপা |
| Selection bias | Pipeline-এর filter-এর কারণে নির্দিষ্ট ধরনের task বেশি থাকা |

---

## ২০. এক নজরে সারাংশ (Summary Card)

| | |
|---|---|
| **Problem** | SWE agent-এর জন্য বড় interactive training data নেই; static benchmark contaminated, scaffold-ভেদে অতুলনীয়, single-run noisy |
| **Solution** | সম্পূর্ণ automated pipeline (GitHub mining → LLM install recipe → execution validation → LLM quality label) + centralized, decontaminated leaderboard |
| **Scale** | ~4,50,000 linked PR → ~1,53,400 → **21,336 task, 3,468 repo**; benchmark **294 task, 169 repo** (2025-এর issue) |
| **Evaluation** | একই ReAct scaffold, 128K context, function calling নয়, **5 run**, SEM ও pass@5, release-date-ভিত্তিক contamination flag |
| **Key result** | DeepSeek-V3-0324: Verified 39.7% বনাম rebench 21.3%; GPT-4.1: Jan 31.1% বনাম Mar–Apr 26.7%; সর্বোচ্চ SEM 1.81 |
| **Key insight** | পুরনো benchmark-এর score কিছু model-এর জন্য ফোলানো হতে পারে; run-to-run inconsistency বড় (আমার bound: GPT-4.1-এর solved task-এর ≥39%, Maverick-এর ≥70% inconsistent) |
| **Main limitation** | Correctness এখনো test-pass (F2P median 2); quality label দুর্বল (Issue Clarity ≈ majority baseline); শুধু run-SEM, task-level CI নেই; শুধু Python; selection bias |
| **CG অবস্থা** | CG6 অনেকটা সমাধান; CG4, CG8 আংশিক; CG1, CG3, CG5, CG7 খোলা; CG9, CG10-এর জন্য testbed |
| **আমাদের জন্য gap** | তাজা, leakage-মুক্ত task-এ agent patch-এর **assurance** (overfitting, consistency, security) মাপা ও assurance layer-কে নিজেই সেখানে যাচাই করা |

---

## ২১. বর্তমান (2026) প্রেক্ষাপট — আজকের Model ও Agent-দের সাথে তুলনা

> **উৎস ও নিয়ম:** এই section-এর সব "এখন"-এর তথ্য শুধু `00_Current_State_2026_Sources.md` (fact sheet, compile করা 2026-10-28) থেকে নেওয়া; bracket-এ fact sheet-এর section (§) দেওয়া। প্রতিটা সংখ্যার পাশে লেবেল: **স্বাধীনভাবে মাপা** (independent), **কোম্পানির নিজের দাবি** (vendor-reported), আর যেখানে fact sheet নিজেই বলেছে **search-snippet only / যাচাই হয়নি**। নিজের হিসাব বা মত "আমার পর্যবেক্ষণ" বা "আমার হিসাব" লেখা।

### ২১.১ Paper-এর সময় বনাম এখন

| দিক | Paper-এ (NeurIPS 2025) | এখন, October 2026 | উৎস |
|---|---|---|---|
| Benchmark window | 294 task, 169 repo, 2025-এর issue; Jan বনাম Mar–Apr subset | সর্বশেষ দেখানো window 2026-05-15 থেকে 2026-07-01: 111 problem, 65 repo; news-log-এর শেষ entry 2026-07-01 (স্বাধীনভাবে মাপা) | §2, swe-rebench.com |
| সেরা resolved rate | gpt-4.1: Jan 31.1%, Mar–Apr 26.7% | Fable 5 [high] 64.5%, Grok 4.5 63.8%, Opus 5 63.4%, GLM-5.2 62.9%, GPT-5.6 Sol 62.3% (স্বাধীনভাবে মাপা) | §2 |
| Open-weight model-এর অবস্থান | সেরা open model DeepSeek-V3-1226 21.9%, closed GPT-4.1-এর অনেক নিচে | GLM-5.2 62.9%, pass@5 81.1% — শীর্ষ থেকে 1.6 pp দূরে, pass@5-এ তালিকার সর্বোচ্চ (স্বাধীনভাবে মাপা) | §2 |
| pass@1 বনাম pass@5 ফাঁক | 6–15 pp (Table 1) | শীর্ষ 8-এ 12–18 pp; যেমন Fable 5: 64.5% বনাম 78.4% (স্বাধীনভাবে মাপা) | §2, §3 |
| কী মাপা হয় | শুধু model, একটা fixed ReAct scaffold-এ | Agent product-ও board-এ: Junie 61.8%, Claude Code 60.4%, OpenAI Codex 58.0% (স্বাধীনভাবে মাপা) | §2 |
| খরচ | Report করা হয়নি (শুধু DeepSeek-V3-এর এক run ≈ 7 ঘন্টা) | প্রতি problem 0.81–4.40 USD; Fable 5 সবচেয়ে দামি 4.40 USD, GPT-5.6 Sol 0.85 USD (স্বাধীনভাবে মাপা) | §2, §3 |
| সবচেয়ে নতুন model কি board-এ? | GPT-4.1, Qwen3 release-এর পরের task-এ মাপা হয়েছিল | **না** — Opus 5.5 (2026-09-22), Sonnet 5.5, Haiku 5.5, GPT-6 family, Gemini 4 Argon কোনোটাই window-এ নেই | §1, §2 |
| SWE-bench Verified-এর অবস্থা | DeepSeek-V3-0324: Verified 39.7% বনাম rebench 21.3% | Vals.ai-তে Opus 5 97.0%, তারপর saturation-এর কারণে archived (স্বাধীনভাবে মাপা); OpenAI Feb 2026-এ Verified বাদ দিয়েছে "increasingly contaminated" বলে (OpenAI page fetcher-এ 403, search snippet থেকে) | §2, §3 |
| Leaderboard-এর সংখ্যা নিয়ে বিরোধ | — | BenchLM বলছে "Opus 4.6 leads at 65.3%" — সম্ভবত অন্য window (search-snippet only) | §2 |

**আমার হিসাব — paper-এর Section ৬.১২-এর ratio আজকের সংখ্যায়:** একই model-এর Verified (Vals) আর SWE-rebench score দুটোই fact sheet-এ আছে মাত্র দুটো model-এর:
- Opus 5: $\rho = 63.4/97.0 \approx 0.65$, ফাঁক 33.6 pp।
- GPT-5.6 Sol: $\rho = 62.3/96.2 \approx 0.65$, ফাঁক 33.9 pp।

Paper-এ 7টা open model-এর গড় $\rho \approx 0.66$ ছিল। অর্থাৎ ধরে রাখা অংশ প্রায় একই, কিন্তু absolute ফাঁক 2025-এর সর্বোচ্চ 18.4 pp থেকে প্রায় 34 pp-এ পৌঁছেছে। **সতর্কতা:** দুটো সংখ্যা ভিন্ন harness-এ মাপা (Vals mini-SWE-agent ব্যবহার করে; SWE-rebench-এর এখনকার scaffold কী, fact sheet বলেনি), আর ভিন্ন সময়ে। তাই এটা contamination-এর প্রমাণ নয়, শুধু একই দিকের লক্ষণ।

**আমার হিসাব — Section ৬.৯-এর bound নতুন সংখ্যায় ($K = 5$ ধরে; board কয়টা run দিয়ে pass@5 মাপে, fact sheet-এ নেই):**

| Model | pass@1 | pass@5 | Inconsistent task অন্তত (B ≥) | pass^5 সর্বোচ্চ (A ≤) | Solved-at-least-once-এর মধ্যে inconsistent অন্তত |
|---|---|---|---|---|---|
| Fable 5 [high] (2026 window) | 64.5 | 78.4 | 17.4% | 61.0% | 22.2% |
| GLM-5.2 (2026 window) | 62.9 | 81.1 | 22.8% | 58.4% | 28.1% |
| তুলনা: gpt-4.1 (2025, Mar–Apr) | 26.7 | 39.0 | 15.4% | 23.6% | 39.4% |

**আমার পর্যবেক্ষণ:** solved task-এর মধ্যে inconsistent অংশ কমেছে (39% থেকে 22–28%), কিন্তু **মোট task-এর মধ্যে flip করা task-এর অংশ কমেনি, বরং বেড়েছে** (অন্তত 15.4% থেকে অন্তত 17–23%)। Model শক্তিশালী হয়েছে, কিন্তু "একই task-এ বারবার একই ফল" — এই reliability আপনা থেকে আসেনি।

**আমার হিসাব — শীর্ষ 5-কে আলাদা করা যায় কি?** শীর্ষ 5টা model 62.3% থেকে 64.5% — মাত্র 2.2 pp-এর মধ্যে। Window-এ 111 task, তাই task-sampling SE $\approx \sqrt{0.64 \times 0.36 / 111} \approx 0.046$, অর্থাৎ প্রায় 4.6 pp। এই ranking statistically অর্থহীন; "Coding Agents Have Converged" paper-ও Verified-এ শীর্ষ 30-এর 29টা পাশাপাশি জোড়ার 0টা McNemar test-এ আলাদা করতে পেরেছে (স্বাধীনভাবে মাপা, §3)।

### ২১.২ কোন Finding এখনো সত্য, কোনটা পুরনো হয়ে গেছে

**এখনো সত্য — বরং আরও শক্ত:**
1. **Static benchmark contaminated হয়ে যায়।** Paper-এর মূল যুক্তি এখন vendor-রাও মেনে নিয়েছে: OpenAI Verified বাদ দিয়েছে (search snippet), Vals.ai 97% saturation-এ archive করেছে (স্বাধীন), Anthropic Opus 5.5 System Card-এ Verified রাখেনি (§3)।
2. **Run-to-run variance বড়।** pass@1–pass@5 ফাঁক 6–15 pp থেকে 12–18 pp হয়েছে। SWE Atlas-এ Pass@1 থেকে Pass^3-এ 30–50% পতন (search-snippet only)। Noise Floor Audit: prompt-এর অর্থ-অপরিবর্তিত পরিবর্তনে paired SD rerun-এর চেয়ে 11–58 গুণ বড় (স্বাধীন, §3)।
3. **Centralized evaluation দরকার।** Vendor-এর সংখ্যা আর স্বাধীন সংখ্যার ফাঁক এখনো আছে: Sonnet 5.5 Terminal-Bench 4.0-এ কোম্পানির নিজের দাবি 70.6%, স্বাধীনভাবে মাপা 63.6–64.1% (§2)।
4. **Scaffold ক্ষমতার অংশ।** একই model-এর ভেতরে শুধু scaffold বদলে score 29.8 point পর্যন্ত বদলায়, যেখানে শীর্ষ 30-এর পুরো spread 8.8 point (স্বাধীন, §3)। Board-এ Claude Code (60.4%) আর Codex (58.0%) agent হিসেবে bare model Opus 5 (63.4%) বা GPT-5.6 Sol (62.3%)-এর নিচে — কিন্তু এই agent-গুলো কোন model দিয়ে চলেছে, fact sheet বলেনি, তাই সরাসরি তুলনা করা যায় না (আমার পর্যবেক্ষণ)।
5. **Resolved ≠ correct (CG1)।** PatchDiff: plausible patch-এর 29.6% gold patch থেকে ভিন্ন আচরণ করে, আর 7.8% "সঠিক" patch পুরো developer test suite-এ fail করে (স্বাধীন, §3)। তবে এটা **পুরনো model-এ মাপা; বর্তমান agent-এ নতুন করে মাপা হয়নি।**

**পুরনো হয়ে গেছে:**
1. **Absolute সংখ্যা।** 2025-এর "সেরা ≈ 27–31%" এখন ≈ 64%। Paper-এর Table 1–2 আজ শুধু ঐতিহাসিক baseline।
2. **"Open model অনেক পিছিয়ে"** — আর সত্য নয়; GLM-5.2 শীর্ষের 1.6 pp-এর মধ্যে, যা task-sampling noise-এর চেয়ে ছোট (আমার হিসাব)।
3. **"Continuously updated" প্রতিশ্রুতির ব্যবহারিক সীমা।** Fact sheet-এর তারিখে window প্রায় চার মাস পুরনো, আর September–October 2026-এর কোনো model নেই। Paper-এর release-date নিয়মে নতুন model মাপতে release-এর পরের task লাগে — তাই সবচেয়ে নতুন model-এর decontaminated সংখ্যা স্বাভাবিকভাবেই দেরিতে আসে। **এই দেরিটাই আজ একটা gap** (আমার পর্যবেক্ষণ)।
4. **Benchmark-এর "সহজ দিকে ঝোঁক" (Section ১২.২, পয়েন্ট ১০)** — ≈64% শীর্ষ score-এ saturation-এর ঝুঁকি বাস্তব হয়ে উঠছে। Task filter (≤3 file ইত্যাদি) এখন বদলানো হয়েছে কিনা, fact sheet বলেনি।

**নতুন হুমকি যা paper ভাবেনি — runtime leakage:** Paper-এর decontamination শুধু training-এ দেখা task আটকায়। 2026-এ দেখা গেছে agent চলার সময়েই উত্তর খুঁজে নেয়: DeepSWE-এ 38টা cheating trial-এর 33টা (87%) `.git` history থেকে gold commit পড়েছে (search-snippet only); SWE-Bench Pro Verified চারটা leakage channel চিহ্নিত করেছে — local file, `.git` history, network, metadata (স্বাধীন, §3)। SWE-rebench pipeline full history সহ repository clone করে (Section ২.২); task container-এ ভবিষ্যতের commit থাকে কিনা, fact sheet-এ তথ্য নেই — **যাচাই করা দরকার** (আমার পর্যবেক্ষণ)।

### ২১.৩ এই Paper-এর Gap-গুলো আজও খোলা কিনা

(CG নম্বর Sub-domain Summary-র চূড়ান্ত সংজ্ঞা অনুযায়ী: CG11 = verifier health, CG12 = assurance signal-এর gaming। এই file-এর Section ১৩.৪-এ প্রস্তাবিত label-noise gap-কে এখানে CG6-এর অংশ ধরা হলো।)

| Gap | 2026-এ অবস্থা | প্রমাণ |
|---|---|---|
| G1 / CG1 — decontaminated task-এ patch overfitting | **খোলা** | PatchDiff-এর 29.6% পুরনো model-এ; বর্তমান agent-এ fresh task-এ কোনো মাপ fact sheet-এ নেই |
| G2 / CG4 — pass^k, flip rate | **আংশিক সমাধান** | Board pass@5 দেয়, pass^k দেয় না; SWE Atlas pass^3 (search-snippet only); vendor-রা এখন SE দেয় (Opus 5.5 ±2.6, Terminal-Bench 4.0, vendor-reported) |
| G3 / CG6 — automated task label-এর নির্ভরযোগ্যতা | **খোলা** | অন্য benchmark-এ বড় ত্রুটি: SWE-Bench Pro public-এর 27.4–34.1% task broken (OpenAI audit, secondary source); SWE-rebench-এর label-এর নতুন কোনো audit fact sheet-এ নেই |
| G4 / CG8 — task-level CI, paired test | **আংশিক সমাধান** | Scale ±95% CI দেয়, Vals avg@3; কিন্তু SWE-rebench board-এ ± শুধু একটা row-এ (Fable 5: 1.41); Verified-এ 0/29 জোড়া আলাদা করা যায় না |
| G5 / CG6 — contamination-এর causal পরিমাপ | **আংশিক সমাধান** | Vendor-রা Verified ছেড়েছে, DeepSWE scratch থেকে লেখা; কিন্তু fresh benchmark-এ বর্তমান model নেই, আর runtime leakage নতুন confound |
| G6 / CG5 — fresh task-এ patch security | **খোলা** | SecPass 7.8–17.3% যেখানে FuncPass 62.6–84.4% (Opus 4.6 / GPT-5.4 যুগ); Opus 5.5, GPT-6-এর কোনো SusVibes বা BaxBench ফল নেই |
| G7 / CG3 — agent-এর self-validation | **খোলা** | Agent-লেখা test patch-এর 80.2%-এ দুর্বল বা কোনো explicit oracle নেই (স্বাধীন, পুরনো agent); Fable 5.1 "নিজের test লিখে যাচাই করে" — কোম্পানির নিজের দাবি, qualitative |
| G8 — scaffold-robust ranking | **খোলা** | Scaffold-এর range 29.8 point (স্বাধীন) |
| G9 / CG7 — abstention | **আংশিক (শুধু vendor দাবি)** | Fable 5.1 আটকে গেলে বলে দেয় — কোম্পানির নিজের দাবি; Opus 5.5-এ impossible task-এ reward hacking-এর চেষ্টা 3–6 গুণ বাড়ে (vendor-reported) |
| G10 — Python-এর বাইরে, কঠিন task | **আংশিক সমাধান (অন্য benchmark-এ)** | DeepSWE: 5টা language, 113টা long-horizon task; SWE-rebench নিজে language বাড়িয়েছে কিনা fact sheet-এ নেই |
| CG2 — candidate re-ranking | **খোলা** | Fact sheet-এ কোনো তথ্য নেই |
| CG9 — APCA repository-level | **খোলা** | Plain LLM baseline overfitting filter-এ মাত্র 62.14% accuracy (ComPass, search-snippet only) |
| CG10 — assurance tool-এর leakage-মুক্ত evaluation | **আংশিক** | Fresh task এখনো সেরা হাতিয়ার, কিন্তু runtime leakage যাচাই না করলে অসম্পূর্ণ |
| CG11 — verifier health | **খোলা** | SWE-Bench Pro-র test-এর সাথে LLM-judge disagreement 32.4% বনাম DeepSWE-এর 1.4% (স্বাধীন); SWE-rebench-এর verifier-এর এমন মাপ নেই |
| CG12 — verifier gaming | **খোলা, সরাসরি প্রমাণসহ** | METR: 8 ঘন্টার বেশি task-এ সফল run-এর অন্তত 16% অবৈধ (স্বাধীন, আগের প্রজন্ম); GLM-5.2 anti-hacking safeguard দিলে 78.80% থেকে 57.32% (স্বাধীন) |

### ২১.৪ বর্তমান Model দিয়ে আবার পরীক্ষা করলে — SPL3 Idea

| Idea | কী করবো | খরচের ধারণা (আমার হিসাব) | কোন নতুন gap দেখাবে |
|---|---|---|---|
| A. Post-release mini-window | Paper-এর public pipeline বা dataset filter দিয়ে 2026-09-22-এর পরের 20–30টা Python issue বাছাই; একটা বর্তমান model 5 বার | Board-এ GPT-5.6 Sol ≈ 0.85 USD/problem; 30 × 5 run হলে প্রায় 130 USD (নতুন model-এর আসল খরচ 3টা task-এর pilot-এ মাপতে হবে) | Opus 5.5 বা GPT-6-এর জন্য এখনো না থাকা decontaminated সংখ্যা (G5) |
| B. pass^5 ও flip rate | A-এর data থেকেই per-task $c_i$; pass^5, flip rate, Section ৬.৯-এর bound মিলিয়ে দেখা | বাড়তি খরচ শূন্য | Flip task-এর মোট অংশ কমেছে কিনা (G2, CG4) |
| C. Runtime leakage audit | 30–50টা SWE-rebench task container-এ চারটা channel (local file, `.git` history, network, metadata) পরীক্ষা | API খরচ শূন্য, শুধু Docker-এর সময় | Temporal decontamination কি runtime-এ ভেঙে যায় (CG10, CG12) |
| D. Fresh-task overfitting audit | A-এর resolved patch-এ gold patch-এর সাথে differential test, আর 20টা হাতে review | ছোট; মূলত মানুষের সময় | PatchDiff-ধরনের হার 2026-এর agent-এ (G1, CG1) |
| E. Verified-বনাম-fresh ratio, open-weight model | একটা সস্তা open-weight model একই scaffold-এ 50 Verified + 50 fresh task-এ | Vals-এ DeepSeek V4 Pro Verified-এ ≈ 0.10 USD/test; 100 task-এ মোটামুটি 10–20 USD | 2026-এর model-এ paper-এর $\rho$, এবার একই harness-এ (G5) |

**আমার পর্যবেক্ষণ:** A + B + D একসাথে Section ১৫-এর "সবচেয়ে সম্ভাবনাময় প্রশ্ন"-এরই 2026 সংস্করণ — শুধু task-এর তারিখ এখন 2026-09-22-এর পরে রাখতে হবে, আর C না করলে "decontaminated" দাবিটা অসম্পূর্ণ থাকবে।

### ২১.৫ Supervisor-এর সম্ভাব্য প্রশ্ন (2026 প্রসঙ্গে)

**Q1. SWE-rebench-এ আজ কে শীর্ষে, আর Opus 5.5 বা GPT-6 কোথায়?**
A: সর্বশেষ দেখানো window (2026-05-15 থেকে 2026-07-01, 111 problem)-এ Fable 5 [high] 64.5%, তারপর Grok 4.5, Opus 5, GLM-5.2, GPT-5.6 Sol — সবাই 62.3–64.5%-এর মধ্যে, স্বাধীনভাবে মাপা। Opus 5.5, Sonnet/Haiku 5.5, GPT-6 আর Gemini 4 Argon window-এর পরে এসেছে, তাই board-এ নেই। অর্থাৎ বর্তমান প্রজন্মের জন্য কোনো decontaminated SWE-rebench সংখ্যা এখনো নেই — এটা নিজেই একটা gap।

**Q2. Paper-এর contamination যুক্তি কি 2026-এ শক্ত হয়েছে, না দুর্বল?**
A: শক্ত হয়েছে। OpenAI Verified বাদ দিয়েছে (search snippet), Vals 97%-এ archive করেছে, Anthropic card-এ Verified নেই। আমার হিসাবে Opus 5 ও GPT-5.6 Sol Verified score-এর প্রায় 65% fresh task-এ ধরে রাখে — paper-এর গড় 0.66-এর কাছাকাছি, যদিও harness আলাদা বলে এটা প্রমাণ নয়। তবে নতুন একটা দুর্বলতাও দেখা গেছে: temporal decontamination training leakage আটকায়, কিন্তু runtime-এ `.git` বা network থেকে উত্তর পড়া আটকায় না।

**Q3. শীর্ষ 5 model 2.2 pp-এর মধ্যে। Ranking কি বিশ্বাস করা যায়?**
A: না। 111 task-এ task-sampling SE প্রায় 4.6 pp (আমার হিসাব), যা পুরো শীর্ষ-5 spread-এর দ্বিগুণ। "Coding Agents Have Converged" paper Verified-এর শীর্ষ 30-এ 29টা পাশাপাশি জোড়ার একটাকেও আলাদা করতে পারেনি। তাই SPL3-এ আমি ranking-এর বদলে paired test আর CI report করবো, আর model বাছবো খরচ দেখে — যেমন প্রতি problem-এ GPT-5.6 Sol 0.85 USD বনাম Fable 5 4.40 USD, অথচ score-এর পার্থক্য noise-এর ভেতরে।
