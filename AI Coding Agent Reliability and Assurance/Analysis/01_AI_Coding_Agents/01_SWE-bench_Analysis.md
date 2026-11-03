# Paper Analysis 01: SWE-bench — Can Language Models Resolve Real-World GitHub Issues?

> **Sub-domain:** AI Coding Agents (একই paper "Coding-Agent Evaluation & Reliability" folder-এও আছে)
> **Analysis করেছে:** SPL3 — AI Coding Agent Reliability and Assurance
> **Paper file:** `AI Coding Agents/ICLR-2024-swe-bench-can-language-models-resolve-real-world-github-issues-Paper-Conference.pdf`

---

## ০. Paper-এর পরিচয় (Bibliographic Info)

| বিষয় | তথ্য |
|---|---|
| **Title** | SWE-bench: Can Language Models Resolve Real-World GitHub Issues? |
| **Authors** | Carlos E. Jimenez, John Yang, Alexander Wettig, Shunyu Yao, Kexin Pei, Ofir Press, Karthik Narasimhan |
| **Institution** | Princeton University, University of Chicago |
| **Venue** | ICLR 2024 (International Conference on Learning Representations) — AI/ML-এর top-tier conference |
| **Paper type** | **Benchmark / Dataset paper** (নতুন algorithm নয়, বরং নতুন "পরীক্ষার খাতা") |
| **Artifacts** | Dataset (2,294 task), SWE-bench-train (19,000 task), SWE-Llama 7B/13B model, evaluation harness, leaderboard (swebench.com) |
| **আমাদের domain-এ গুরুত্ব** | ⭐⭐⭐⭐⭐ — এটা পুরো "AI Coding Agent" field-এর **foundation paper**। পরের প্রায় সব paper (SWE-agent, AutoCodeRover, Agentless, SWE-Bench Pro, SWE-rebench) এই benchmark-এর উপর দাঁড়িয়ে আছে। |

---

## ★ সহজ ভাষায় পুরো Paper (প্রথমবার পড়ার জন্য)

> এই অংশটা তাদের জন্য, যারা জীবনে কখনো research paper পড়েনি। আগে শুধু এটুকু পড়ো। বুঝে গেলে নিচের বড় section-গুলো পড়া অনেক সহজ হবে।

### ক. Paper-টা কী নিয়ে?

- এটা একটা **benchmark paper**। Benchmark মানে হলো একটা standard পরীক্ষার খাতা, যেটা দিয়ে সবার ক্ষমতা একই মাপে মাপা যায়।
- এখানে নতুন কোনো AI বানানো হয়নি। বানানো হয়েছে AI-কে পরীক্ষা করার একটা কঠিন খাতা, নাম **SWE-bench**।
- Paper লিখেছেন Princeton University ও University of Chicago-র গবেষকরা। মূল লেখক Carlos Jimenez ও John Yang। Paper ছাপা হয়েছে ICLR 2024 conference-এ।
- পরীক্ষার প্রশ্ন নেওয়া হয়েছে আসল GitHub project থেকে। মোট ২,২৯৪টা আসল bug বা সমস্যা।
- AI-কে সেই bug ঠিক করে দেখাতে হয়। ঠিক হলো কিনা, তা project-এর নিজের test চালিয়ে দেখা হয়।

### খ. সমস্যাটা কী ছিল?

- আগে AI-র coding ক্ষমতা মাপা হতো HumanEval-এর মতো ছোট প্রশ্ন দিয়ে। যেমন "দুটো সংখ্যা যোগ করার function লেখো"।
- এটা অনেকটা ছাত্রকে শুধু ছোট অঙ্ক করতে দিয়ে বলা, "তুমি তো ভালো engineer"। অথচ আসল engineer-কে হাজার হাজার file-এর বিশাল project-এ কাজ করতে হয়।
- ফলে দেখা যেত AI-রা ওই ছোট পরীক্ষায় প্রায় full marks পাচ্ছে। কিন্তু আসল কাজে তারা কতটা পারে, কেউ জানত না।
- **একটা উদাহরণ:** একজন user লিখলেন, "proxy URL-এ একটা '/' কম দিলে software ভুল error message দেখায়।" Engineer-কে প্রথমে খুঁজে বের করতে হয় হাজার হাজার file-এর কোনটায় ভুল আছে। তারপর সেটা ঠিক করতে হয়, কিন্তু অন্য কিছু যেন না ভাঙে। ছোট function লেখার পরীক্ষায় এই কাজ কখনো মাপা যেত না।
- যা মাপা যায় না, তা ভালো করাও যায় না। তাই একটা বাস্তব পরীক্ষা দরকার ছিল।

### গ. Paper কী solve করেছে?

- ১২টা জনপ্রিয় Python project (django, sympy, flask ইত্যাদি) থেকে **২,২৯৪টা আসল bug** নিয়ে benchmark বানিয়েছে।
- প্রতিটা প্রশ্নে থাকে আসল bug-এর বিবরণ, পুরো project-এর code, আর যাচাই করার test। কাজেই উত্তর ঠিক কিনা তা মেশিনই বলে দেয়, কারো মতামত লাগে না।
- সেই সময়ের সেরা AI গুলোকে পরীক্ষা করেছে। দেখিয়েছে সবাই খুব খারাপ করছে।
- খুঁজে পেয়েছে, AI-র আসল সমস্যা code লেখা নয়। সমস্যা হলো **bug-টা project-এর কোথায় আছে তা খুঁজে বের করা**।
- একটা open-source model (SWE-Llama) বানিয়ে দেখিয়েছে, খোলা model-ও কিছুটা পারে।
- **গুরুত্বপূর্ণ ৩টা সংখ্যা:**
  - **১.৯৬%:** সেরা AI (Claude 2) ২,২৯৪টার মধ্যে ঠিক করেছে মাত্র প্রায় ৪৫টা। মানে ১০০টার মধ্যে মাত্র ২টা।
  - **৪.৮০%:** যদি AI-কে আগে থেকেই বলে দেওয়া হয় কোন file-এ bug, তখনও মাত্র ১০০টার মধ্যে প্রায় ৫টা।
  - **২,২৯৪:** মোট কতগুলো আসল প্রশ্ন আছে। এটাই পরে সারা দুনিয়ার standard পরীক্ষা হয়ে গেছে।

### ঘ. কীভাবে solve করেছে?

1. প্রথমে ১২টা জনপ্রিয় Python project থেকে প্রায় ৯০,০০০ Pull Request (code পরিবর্তনের আবেদন) জোগাড় করেছে।
2. তারপর ছাঁকনি দিয়েছে। শুধু সেই PR রেখেছে, যেগুলো মেনে নেওয়া হয়েছে, কোনো issue ঠিক করেছে এবং সঙ্গে test বদলেছে।
3. এরপর প্রতিটা PR-এর code আসলে চালিয়ে দেখেছে। যে test আগে fail করত আর fix-এর পর pass করে, সেই test আছে এমন PR-ই রেখেছে। এভাবে ২,২৯৪টা বাকি থেকেছে।
4. প্রতিটা প্রশ্নে AI-কে দেওয়া হয়েছে bug-এর বিবরণ আর project-এর code। AI-র কাজ একটা patch (কোন line বদলাতে হবে তার তালিকা) লেখা।
5. যেহেতু পুরো project AI-র মাথায় ঢোকে না, তাই BM25 নামের একটা keyword-search দিয়ে সবচেয়ে মিল থাকা file গুলো বেছে দেওয়া হয়েছে।
6. তুলনার জন্য একটা "চিট" setting-ও রেখেছে। সেখানে সঠিক file গুলো আগেই দিয়ে দেওয়া হয়। এতে বোঝা যায় খোঁজাটা কতটা কঠিন।
7. AI-র patch project-এ বসিয়ে test চালানো হয়। আগের সব test আর নতুন test একটাও fail না করলে তবেই "Resolved"।
8. শেষে নিজেরা CodeLlama model-কে ১৯,০০০ উদাহরণ দিয়ে আরও শিখিয়েছে। সেটাই SWE-Llama।

### ঙ. এরপর কী করা যায়?

- **Authors নিজেরা বলেছেন:** শুধু Python না, অন্য language-এও এরকম benchmark বানানো দরকার। আর শুধু সরল পদ্ধতি নয়, agent (যে AI নিজে ধাপে ধাপে ভেবে কাজ করে) দিয়েও পরীক্ষা করা দরকার।
- **এখনো খোলা সমস্যা:** শুধু test pass করলেই কি patch সত্যিই ঠিক? দুর্বল test হলে ভুল patch-ও পাস করে যেতে পারে।
- **আরেকটা খোলা সমস্যা:** AI কি একই প্রশ্ন বারবার করলে একই উত্তর দেয়? Paper শুধু একবার চালিয়েছে, তাই বোঝা যায় না।
- **আমরা SPL3-তে করতে পারি:** SWE-bench-এর ছোট অংশ (Lite বা Verified) দিয়ে একটা tool বানানো, যা "Resolved" patch-গুলো আবার যাচাই করে।
- **আমরা আরও করতে পারি:** শুধু test নয়, security scan (নিরাপত্তা-ত্রুটি খোঁজা) আর code quality-ও মাপা। যেমন Bandit বা Semgrep চালানো।
- **আমরা আরও করতে পারি:** একই task ৩ বার চালিয়ে দেখা AI প্রতিবার সফল হয় কিনা।

> **মনে রাখো:**
> SWE-bench হলো আসল GitHub bug দিয়ে বানানো পরীক্ষা, আর ২০২৩-এ সেরা AI-ও এতে ১০০টার মধ্যে মাত্র ২টা পেরেছিল।
> মূল বাধা ছিল bug-এর সঠিক জায়গা খুঁজে পাওয়া। আর test pass করা মানেই patch ঠিক, এটা পুরো সত্য নয়।
> আমাদের SPL3-এর সুযোগ হলো এই "ঠিক কিনা" যাচাইয়ের জায়গাটা (assurance) নিয়ে কাজ করা।

---

## ১. এক লাইনে Paper (TL;DR)

**SWE-bench হলো একটা benchmark (AI-র পরীক্ষার খাতা)। এখানে LLM-কে আসল GitHub repository-র আসল bug report (issue) দেওয়া হয়। LLM-কে code পরিবর্তন (patch) করে সেই bug ঠিক করতে হয়। সেই patch সঠিক কিনা, তা repository-র আসল unit test চালিয়ে যাচাই করা হয়।**

### Supervisor-কে ৩০ সেকেন্ডে কীভাবে বলবো
> "Sir, আগে LLM-এর coding ability মাপা হতো HumanEval-এর মতো ছোট ছোট function লেখার problem দিয়ে, যেগুলো বাস্তবের software engineering-এর মতো না। SWE-bench প্রথমবার 12টা জনপ্রিয় Python repository থেকে 2,294টা আসল GitHub issue নিয়ে একটা realistic benchmark বানিয়েছে। এখানে model-কে হাজার হাজার file-এর codebase বুঝে, সঠিক জায়গা খুঁজে, patch লিখতে হয় এবং আসল test-এ pass করতে হয়। 2023-এ সবচেয়ে ভালো model Claude 2 মাত্র 1.96% solve করতে পেরেছিল — অর্থাৎ problem-টা অনেক কঠিন। এই paper-টাই পরে AI coding agent research-এর standard yardstick হয়ে গেছে।"

---

## ২. Background — এই paper বুঝতে যা আগে জানা দরকার

এই অংশে paper-এর সাথে জড়িত প্রতিটা concept খুব সহজভাবে ব্যাখ্যা করা হলো।

### ২.১ GitHub Issue, Pull Request (PR), Commit
- **Issue:** কেউ একটা software ব্যবহার করতে গিয়ে bug পেলে বা নতুন feature চাইলে GitHub-এ একটা "ticket" খোলে — এটাই issue। যেমন: *"proxy URL-এ একটা '/' কম দিলে ভুল error message দেখায়"*।
- **Pull Request (PR):** developer সেই issue ঠিক করার জন্য code পরিবর্তন করে একটা PR জমা দেয়। Maintainer review করে **merge** করলে code main project-এ ঢুকে যায়।
- **Base commit:** PR যে অবস্থার code-এর উপর বানানো হয়েছে — অর্থাৎ "bug থাকা অবস্থার" codebase।

### ২.২ Patch / Diff
Patch হলো একটা file যেটা বলে "কোন file-এর কোন line মুছতে হবে (`-`) আর কোন line যোগ করতে হবে (`+`)"। পুরো file আবার লেখার দরকার নেই।
```diff
- return self._format_fields(_('Other Parameters'), self._consume_fields())
+ if self._config.napoleon_use_param:
+     fields = self._consume_fields(multiple=True)
+     return self._format_docutils_params(fields)
```

### ২.৩ Unit Test ও Test Oracle
- **Unit test:** ছোট একটা code যেটা check করে কোনো function ঠিক output দিচ্ছে কিনা।
- **Test oracle:** "সঠিক উত্তর কী হওয়া উচিত" — সেই সিদ্ধান্ত যে নেয়। SWE-bench-এ oracle হলো developer-এর লেখা test। (এই concept পরে *LLM Test Generation* ও *Patch Validation* sub-domain-এ খুব গুরুত্বপূর্ণ হবে।)

### ২.৪ Regression Testing (খুব গুরুত্বপূর্ণ)
নতুন code পরিবর্তন করার পর **আগে যা ঠিকমতো কাজ করতো, তা এখনো ঠিক আছে কিনা** — সেটা যাচাই করাই regression testing। "Regression" মানে পিছিয়ে যাওয়া — অর্থাৎ নতুন fix করতে গিয়ে পুরনো কিছু ভেঙে ফেলা।
SWE-bench-এর **PASS_TO_PASS** test গুলো আসলে regression test (নিচে বিস্তারিত)।

### ২.৫ Fail-to-Pass (F2P) ও Pass-to-Pass (P2P) Test
| Test type | Patch-এর আগে | Patch-এর পরে | মানে কী |
|---|---|---|---|
| **FAIL_TO_PASS** | ❌ Fail | ✅ Pass | এই test প্রমাণ করে issue-টা আসলেই ঠিক হয়েছে |
| **PASS_TO_PASS** | ✅ Pass | ✅ Pass | এই test প্রমাণ করে পুরনো কিছু ভাঙেনি (regression নেই) |

**সহজ কথায়:** F2P হলো "রোগ সেরেছে" তার প্রমাণ। P2P হলো "অন্য কোনো রোগ হয়নি" তার প্রমাণ। দুটো মিললে তবেই fix ঠিক।

### ২.৬ Context Window ও Long Context
LLM একবারে কত token (মোটামুটি শব্দের টুকরা) পড়তে পারে, সেটাই context window। SWE-bench-এর codebase গড়ে **438,000 line** — কোনো model-এর context-এ পুরোটা ঢোকে না। তাই কোন file দেখাবো তা বাছাই (retrieval) করতে হয়।

### ২.৭ Information Retrieval — BM25
একটা প্রশ্ন (query = issue text) দিয়ে অনেক document (code file) থেকে সবচেয়ে প্রাসঙ্গিক document খুঁজে বের করার classic keyword-based algorithm। Google-এর আগের যুগের search engine-এর মূল ভিত্তি। (সূত্র Section ৬-এ)

### ২.৮ Fine-tuning ও LoRA
- **Fine-tuning:** আগে থেকে train করা model-কে নির্দিষ্ট কাজের data দিয়ে আরও train করা।
- **LoRA (Low-Rank Adaptation):** পুরো model-এর সব weight না বদলে, ছোট দুটো matrix যোগ করে শুধু সেগুলো train করা — কম memory, কম GPU লাগে। (সূত্র Section ৬-এ)

### ২.৯ Data Contamination / Data Leakage
LLM internet-এর বিশাল data দিয়ে train হয়। যদি benchmark-এর প্রশ্ন ও উত্তর আগেই training data-তে থাকে, তাহলে model "মুখস্থ" থেকে উত্তর দিতে পারে — এটাই contamination। এতে benchmark score ফুলে যায়, আসল ability বোঝা যায় না। (পরে **SWE-rebench** paper ঠিক এই problem নিয়ে কাজ করেছে।)

### ২.১০ Greedy Decoding ও Pass@k
- **Greedy decoding:** প্রতিটা step-এ সবচেয়ে বেশি probability-র token বেছে নেওয়া — তাই output deterministic।
- **Pass@k:** k বার চেষ্টা করলে অন্তত একবার সঠিক হওয়ার সম্ভাবনা। এই paper শুধু **1 বার** চেষ্টা করেছে (Pass@1-এর মতো)।

### ২.১১ Automated Program Repair (APR)
Bug আপনা-আপনি ঠিক করার research field। SWE-bench মূলত APR-এর একটা বড়, বাস্তবসম্মত রূপ। (এটা আমাদের ২য় sub-domain।)

### ২.১২ Benchmark Saturation
যখন সব model একটা benchmark-এ প্রায় 90–100% পেয়ে যায়, তখন benchmark আর model-দের মধ্যে পার্থক্য করতে পারে না — একে saturation বলে। HumanEval এই অবস্থায় পৌঁছে গিয়েছিল।

---

## ৩. Problem Statement — কী সমস্যা ছিল?

### ৩.১ মূল সমস্যা
1. **পুরনো benchmark খুব সহজ ও অবাস্তব:** HumanEval, MBPP-তে problem গুলো self-contained — কয়েক line-এর একটা function লিখলেই হয়। কিন্তু বাস্তবে একজন software engineer-কে:
   - হাজার হাজার file-এর repository navigate করতে হয়,
   - বিভিন্ন file-এর function-গুলোর সম্পর্ক বুঝতে হয়,
   - একাধিক জায়গায় পরিবর্তন করতে হয়।
2. **Benchmark saturation:** পুরনো benchmark-এ model-রা ইতিমধ্যে ভালো করছিল, তাই নতুন model-দের সীমা (frontier) বোঝা যাচ্ছিল না।
3. **ভালো benchmark বানানো কঠিন:** task এমন হতে হবে যা (ক) model-এর জন্য কঠিন, কিন্তু (খ) উত্তর সহজে যাচাই করা যায়। এই দুটো একসাথে পাওয়া কঠিন।
4. **Contamination:** static benchmark পুরনো হলে model-এর training data-তে ঢুকে যায়।

**সহজ কথায়:** পুরনো পরীক্ষা এত সহজ ও ছোট ছিল যে সবাই পাস করে ফেলত। আবার প্রশ্ন ফাঁস হয়ে গেলে মুখস্থ করেও পাস করা যেত।

### ৩.২ কেন এটা গুরুত্বপূর্ণ?
LLM তখন Copilot-এর মতো commercial product-এ ব্যবহার হচ্ছিল। কিন্তু বাস্তব software engineering কাজে এরা কতটা সক্ষম তা মাপার কোনো ভালো উপায় ছিল না। **যা মাপা যায় না, তা উন্নত করা যায় না।**

---

## ৪. Goal ও Research Questions

**Goal:** একটা realistic, কঠিন, execution-based ও সহজে update করা যায় এমন benchmark তৈরি করা।

**সহজ কথায়:** লক্ষ্য হলো এমন পরীক্ষা, যা আসল কাজের মতো কঠিন, যার উত্তর মেশিন দিয়ে যাচাই করা যায়, আর যা ভবিষ্যতে নতুন প্রশ্ন দিয়ে নতুন করা যায়।

Paper-টা মূলত এই প্রশ্নগুলোর উত্তর খুঁজেছে (implicit RQ):
- **RQ1:** State-of-the-art LLM (GPT-4, Claude 2, ChatGPT-3.5) আসল GitHub issue কতটা solve করতে পারে?
- **RQ2:** Retrieval (কোন file দেখানো হবে) performance-এ কতটা প্রভাব ফেলে?
- **RQ3:** Context length বাড়লে performance-এ কী হয়?
- **RQ4:** Open-source model-কে fine-tune করে (SWE-Llama) কি proprietary model-এর সাথে প্রতিযোগিতা করা যায়?
- **RQ5:** Model-এর লেখা patch আর মানুষের লেখা patch-এর মধ্যে পার্থক্য কী?

**সহজ কথায়:** মোট পাঁচটা প্রশ্ন। AI কতটা পারে, file খোঁজা কতটা জরুরি, বেশি লেখা দিলে লাভ হয় কিনা, ছোট খোলা model পারে কিনা, আর AI-র patch মানুষের patch-এর মতো কিনা।

---

## ৫. Methodology — কীভাবে কাজটা করা হয়েছে

### ৫.১ Benchmark Construction: ৩-Stage Pipeline

| Stage | নাম | কী করা হয় | Output |
|---|---|---|---|
| I | Scrape PRs | 12টা popular Python repository থেকে সব PR সংগ্রহ | ~90,000 PR |
| II | Attribute Filter | PR merged হয়েছে + কোনো issue resolve করে + test file পরিবর্তন করে | Candidate task |
| III | Execution Filter | Install সফল হয় + অন্তত ১টা FAIL_TO_PASS test আছে | **2,294 task instance** |

**সহজ কথায়:** ৯০,০০০ থেকে তিনটা ছাঁকনি দিয়ে বাছতে বাছতে ২,২৯৪টা ভালো প্রশ্ন বাকি থাকে। অর্থাৎ ১০০টার মধ্যে প্রায় ২.৫টা টিকে যায়।

**Stage I — Repository selection ও scraping:**
- PyPI-এর top 5,000 সবচেয়ে বেশি download হওয়া library থেকে top 100 বাছাই, license check, তারপর 12টা repository নেওয়া হয় (django, sympy, scikit-learn, sphinx, matplotlib, pytest, xarray, astropy, pylint, requests, seaborn, flask)।
- কেন popular repo? কারণ এগুলো well-maintained, ভালো documentation ও ভালো test coverage আছে।

**Stage II — Attribute-based filtering:** একটা PR task হবে যদি:
1. Status = **Merged** (অর্থাৎ maintainer গ্রহণ করেছে),
2. কোনো issue-কে link করে ("fixes #24" এরকম লেখা দিয়ে),
3. কোনো test file পরিবর্তন করে (path-এ "test"/"testing" শব্দ আছে)।

**সহজ কথায়:** Stage II-এর কাজ হলো শুধু "পুরো গল্প" আছে এমন PR রাখা। মানে সমস্যা ছিল, সমাধান হয়েছে, আর সমাধান যাচাইয়ের test আছে।

**Stage III — Execution-based filtering:**
- Codebase install করা হয়, PR-এর test অংশ (test patch) apply করা হয়।
- Solution apply-এর **আগে ও পরে** test চালানো হয়।
- অন্তত একটা test **fail → pass** না হলে বাদ।
- Install বা runtime error হলে বাদ।
- যে test নতুন তৈরি হওয়া function/class-এর নাম ব্যবহার করে, সেগুলোও বাদ (কারণ issue-তে নাম বলা থাকে না, model অনুমান করতে পারবে না)।

**গুরুত্বপূর্ণ design decision:** Problem statement-এ শুধু PR-এর প্রথম commit-এর **আগের** comment রাখা হয় — যাতে solution-এর hint leak না হয়।

**সহজ কথায়:** AI-কে এমন কিছু দেখানো হয় না যা উত্তরের ইঙ্গিত দেয়। তাই শুধু code বদলানোর আগের আলোচনাটুকু রাখা হয়েছে।

### ৫.২ Task Formulation
- **Input:** Issue text + পুরো codebase
- **Output:** একটা patch file
- **Evaluation:** Patch apply → test চালানো → সব F2P ও P2P pass করলে "Resolved"

**সহজ কথায়:** একটাই সরল নিয়ম। বিবরণ আর code নাও, patch দাও, আর সব test পাস করলে তবেই সফল।

### ৫.৩ Evaluation Pipeline (প্রতিটা prediction-এর জন্য ৭টা ধাপ)
1. Repository base commit-এ checkout
2. ঐ version-এর জন্য conda environment activate
3. Codebase install
4. Test patch apply
5. Model-এর patch apply
6. Apply fail করলে patch-কে auto-fix (header ঠিক করা, অপ্রয়োজনীয় context line মুছা) করে আবার চেষ্টা
7. Test script চালিয়ে log বের করা → log parse করে প্রতিটা test-এর status বের করা

যদি ধাপ ৫/৬/৭ fail করে → score = 0।

**সহজ কথায়:** AI-র লেখা patch project-এ বসিয়ে test চালানো হয়। কোথাও আটকে গেলে সেই task-এ নম্বর শূন্য।

### ৫.৪ Baseline System: Retrieval + Generation
যেহেতু পুরো codebase context-এ ঢোকে না, তাই দুটো setting:
1. **BM25 (Sparse) retrieval:** issue text দিয়ে BM25 চালিয়ে সবচেয়ে প্রাসঙ্গিক file গুলো নেওয়া, context limit (13k/27k/50k token) পর্যন্ত। File path-ও document-এর শুরুতে যোগ করা হয়েছে, যাতে issue-তে file-এর নাম থাকলে মিলে যায়।
2. **"Oracle" retrieval:** আসল (gold) patch যে file গুলো পরিবর্তন করেছে, সরাসরি সেই file গুলো দেওয়া — বাস্তবসম্মত নয় (কারণ বাস্তবে কেউ আগে জানে না কোন file বদলাতে হবে), কিন্তু **upper-bound analysis**-এর জন্য (সর্বোচ্চ কত পর্যন্ত সম্ভব তা জানতে)।
3. **"Oracle-collapsed":** Oracle file-এর শুধু পরিবর্তিত line-এর ±15 line রাখা, বাকি সব collapse — এটা একটা **ablation study** (একটা অংশ বদলে দেখা তার প্রভাব কতটা)।

Prompt-এ থাকে: instruction + issue + retrieved files (+ README) + একটা example patch format।

**সহজ কথায়:** AI-কে একটা চিঠি দেওয়া হয়। তাতে লেখা থাকে কী করতে হবে, bug-এর বিবরণ, আর কয়েকটা file। তিন রকম file-বাছাইয়ের মধ্যে Oracle হলো "উত্তর-সহ" সুবিধাজনক রূপ, আর BM25 হলো আসল জীবনের মতো।

### ৫.৫ SWE-Llama: Open Model Fine-tuning
- **কেন:** off-the-shelf CodeLlama repository-wide edit-এর instruction follow করতে পারছিল না — placeholder বা অপ্রাসঙ্গিক code লিখছিল।
- **Data:** SWE-bench-train — **37টা আলাদা** repository থেকে 19,000 issue-PR pair (test বাধ্যতামূলক নয়)। Evaluation repository-র সাথে **disjoint**, যাতে contamination না হয়। 30,000 token-এর বেশি লম্বা sequence বাদ দিয়ে কার্যকর ~10,000 instance।
- **Training:** Input = instruction + issue + oracle file; Output = gold patch।
- **Hyperparameters:** LoRA r = 16, α = 16, dropout = 0.05 (attention-এর Q, K, V, O projection-এ); learning rate 6e-4; batch size 32; সর্বোচ্চ 4 epoch; 100টা held-out instance-এর validation loss দিয়ে best checkpoint বাছাই।
- **Compute:** 7B — 4×A100-এ 20 ঘন্টা; 13B — 8×A100-এ 47 ঘন্টা। Long context-এর জন্য DeepSpeed Ulysses ও Flash Attention ব্যবহার হয়েছে (দুটোই লম্বা input কম memory-তে চালানোর কৌশল)।

**সহজ কথায়:** মূল model-এর সব অংশ না বদলে শুধু ছোট একটা অংশ শেখানো হয়েছে, তাই কম GPU-তে কাজ হয়েছে।

### ৫.৬ Inference Setting
প্রতিটা task-এ মাত্র **১টা patch**, **greedy decoding** (খরচ কমানোর জন্য)।

**সহজ কথায়:** AI-কে প্রতি প্রশ্নে একবারই সুযোগ দেওয়া হয়েছে। তাই ফলাফল "প্রথমবারেই ঠিক"-এর হার।

---

## ৬. Mathematical Formulation — সূত্র ও ব্যাখ্যা

Paper-এ explicitly অনেক equation নেই (benchmark paper হওয়ায়), কিন্তু পুরো evaluation-টা formal ভাবে লেখা যায়। Supervisor-কে দেখানোর জন্য এটা খুব কাজের।

**সহজ কথায়:** এই section-এ পুরো পরীক্ষাটা অঙ্কের ভাষায় লেখা হয়েছে। প্রতিটা সূত্রের নিচে কথায় বলা আছে সেটা কী হিসাব করে। সূত্র না বুঝলেও কথাগুলো পড়লেই চলবে।

### ৬.১ একটা Task Instance-এর Formal Definition
$$
I = (C,\; P,\; T,\; \delta)
$$
**এটা কী হিসাব করে:** একটা প্রশ্ন আসলে কী কী দিয়ে তৈরি, তা এক লাইনে লেখা। মানে প্রশ্ন = code + সমস্যার বিবরণ + test + সঠিক উত্তর।
- $C$ = base commit-এ codebase (bug থাকা অবস্থা)
- $P$ = problem statement (issue title + description + comments)
- $T$ = test patch (PR-এর test অংশ)
- $\delta$ = gold patch (developer-এর আসল solution)

Model $M$ ও retriever $R$ থাকলে model-এর prediction:
$$
\hat{\delta} = M\big(P,\; R(C, P)\big)
$$
**এটা কী হিসাব করে:** AI-র উত্তর কীভাবে তৈরি হয়। আগে একজন খোঁজকারী (retriever) কিছু file বাছে। তারপর AI সেই file আর bug-এর বিবরণ দেখে patch লেখে।
অর্থাৎ retriever codebase থেকে কিছু file বাছাই করে, model সেই file আর issue দেখে patch $\hat{\delta}$ তৈরি করে।

### ৬.২ F2P ও P2P Set
$C \oplus T$ মানে codebase-এ test patch apply করা। $s(t, X)$ মানে codebase $X$-এ test $t$-এর status।
$$
F2P = \{\, t \in T \;:\; s(t,\, C \oplus T) = \text{FAIL} \;\land\; s(t,\, C \oplus T \oplus \delta) = \text{PASS} \,\}
$$
$$
P2P = \{\, t \;:\; s(t,\, C \oplus T) = \text{PASS} \;\land\; s(t,\, C \oplus T \oplus \delta) = \text{PASS} \,\}
$$
**এটা কী হিসাব করে:** কোন কোন test কে F2P আর কোনগুলো P2P, তার গাণিতিক সংজ্ঞা। নিচের "সহজ ভাষায়" লাইনটাই এর মানে।
**সহজ ভাষায়:** F2P = যে test গুলো gold patch-এর কারণে fail থেকে pass হয়েছে। P2P = যে test গুলো আগেও pass ছিল, পরেও pass।

### ৬.৩ Resolved হওয়ার শর্ত
$$
\text{Resolved}(\hat{\delta}) =
\begin{cases}
1, & \text{যদি } \hat{\delta} \text{ apply হয় এবং } \forall t \in F2P \cup P2P:\; s(t,\, C \oplus T \oplus \hat{\delta}) = \text{PASS} \\
0, & \text{অন্যথায়}
\end{cases}
$$
**এটা কী হিসাব করে:** একটা task পাস না ফেল। Patch বসাতে হবে এবং সব দরকারি test পাস করতে হবে। একটাও ব্যর্থ হলে ফল ০, নয়তো ১।
**মানে:** একটা test-ও fail বা missing হলে পুরো task fail। এটা একটা **binary, all-or-nothing** metric — কোনো partial credit নেই।

### ৬.৪ Main Metric: % Resolved ও % Apply
$$
\%\,\text{Resolved} = \frac{1}{N} \sum_{i=1}^{N} \text{Resolved}(\hat{\delta}_i) \times 100
$$
$$
\%\,\text{Apply} = \frac{1}{N} \sum_{i=1}^{N} \mathbb{1}\big[\hat{\delta}_i \text{ সফলভাবে apply হয়েছে}\big] \times 100
$$
**এটা কী হিসাব করে:** ১০০টার মধ্যে কতগুলো task ঠিক হয়েছে (% Resolved), আর কতগুলোর patch অন্তত project-এ বসেছে (% Apply)। ফল নিচের ছোট উদাহরণে দেখো।
**Worked example:** N = 2,294; Claude 2 = 1.96% → $2294 \times 0.0196 \approx 45$টা task solve করেছে। আর % Apply = 43.07% → প্রায় 988টা patch অন্তত syntax/format ঠিক রেখে apply হয়েছে, কিন্তু তার মধ্যে মাত্র 45টা আসলে সঠিক।

**সহজ কথায়:** patch বসানো আর সঠিক হওয়া এক জিনিস না। প্রায় ১,০০০টা patch ঠিকঠাক বসেছে, কিন্তু সঠিক ছিল মাত্র ৪৫টা।

### ৬.৫ BM25 Retrieval Score
Query $Q$ (issue text)-এ শব্দ $q_1, \dots, q_n$; document $D$ (একটা code file):
$$
\text{score}(D, Q) = \sum_{i=1}^{n} \text{IDF}(q_i) \cdot \frac{f(q_i, D)\,(k_1 + 1)}{f(q_i, D) + k_1\left(1 - b + b\,\dfrac{|D|}{\text{avgdl}}\right)}
$$
$$
\text{IDF}(q_i) = \ln\!\left(\frac{N - n(q_i) + 0.5}{n(q_i) + 0.5} + 1\right)
$$
**এটা কী হিসাব করে:** প্রতিটা file একটা নম্বর পায়, bug-এর বিবরণের সঙ্গে সেটা কতটা মেলে। বেশি নম্বর মানে file-টা আগে দেখানো হবে। IDF অংশ বলে, দুর্লভ শব্দ মিললে বেশি নম্বর।
| Symbol | মানে |
|---|---|
| $f(q_i, D)$ | file $D$-তে শব্দ $q_i$ কতবার আছে (term frequency) |
| $\lvert D\rvert$ | file-এর দৈর্ঘ্য |
| avgdl | সব file-এর গড় দৈর্ঘ্য |
| $N$ | মোট file সংখ্যা |
| $n(q_i)$ | কতগুলো file-এ $q_i$ আছে |
| $k_1$ (~1.2–2.0) | term frequency কতটা saturate হবে |
| $b$ (~0.75) | লম্বা document-কে কতটা penalty দেবে |

**Intuition:**
- যে শব্দ অল্প file-এ আছে (যেমন `napoleon_use_param`), তার IDF বেশি → বেশি গুরুত্বপূর্ণ। আর `self`, `return` সব file-এ আছে → IDF প্রায় 0।
- একই শব্দ বারবার থাকলে score বাড়ে, কিন্তু একটা সীমার পর আর বেশি বাড়ে না ($k_1$-এর কারণে)।
- লম্বা file-এ এমনিতেই বেশি শব্দ থাকে, তাই $b$ দিয়ে normalize করা হয়।

**সীমাবদ্ধতা:** BM25 শুধু শব্দ মেলায়, **অর্থ (semantics)** বোঝে না। Issue-তে "proxy error" লেখা থাকলে আর code-এ `get_connection` নামে function থাকলে BM25 মিলাতে পারবে না।

**সহজ কথায়:** BM25 শুধু শব্দ মেলায়, মানে বোঝে না। তাই bug-এর বিবরণে একরকম শব্দ আর code-এ অন্যরকম নাম থাকলে সে ধরতে পারে না।

### ৬.৬ Retrieval Recall (Oracle-এর তুলনায়)
$O$ = oracle file set, $\hat{R}$ = BM25 যে file গুলো এনেছে:
$$
\text{Recall} = \frac{|\hat{R} \cap O|}{|O|}
$$
**এটা কী হিসাব করে:** দরকারি file গুলোর মধ্যে কতগুলো খোঁজকারী আসলে এনেছে। যেমন ৪টা দরকারি, ২টা পেলে recall = ০.৫।
Paper তিনভাবে report করেছে:
- **Avg:** গড় recall
- **All:** কত % task-এ $O \subseteq \hat{R}$ (সব দরকারি file পেয়েছে)
- **Any:** কত % task-এ $\hat{R} \cap O \neq \emptyset$ (অন্তত একটা দরকারি file পেয়েছে)

**সহজ কথায়:** Avg হলো গড় সাফল্য। All হলো কঠোর মাপ, সব দরকারি file পেয়েছে কিনা। Any হলো সহজ মাপ, অন্তত একটা পেয়েছে কিনা।

### ৬.৭ LoRA (SWE-Llama-তে ব্যবহৃত)
মূল weight matrix $W_0 \in \mathbb{R}^{d \times k}$ freeze রেখে:
$$
W' = W_0 + \Delta W = W_0 + \frac{\alpha}{r}\, B A, \qquad B \in \mathbb{R}^{d \times r},\; A \in \mathbb{R}^{r \times k},\; r \ll \min(d, k)
$$
**এটা কী হিসাব করে:** পুরনো বড় matrix ($W_0$) একদম না ছুঁয়ে তার পাশে ছোট দুটো matrix ($A$ ও $B$) জুড়ে দেওয়া হয়। শুধু ছোট দুটো শেখানো হয়। এভাবে খরচ কমে।
শুধু $A$ ও $B$ train হয়।

**Worked example:** $d = k = 4096$ হলে full fine-tuning-এ একটা matrix-এ $4096 \times 4096 \approx 16.7$M parameter। LoRA ($r=16$)-তে $2 \times 4096 \times 16 = 131{,}072$ parameter — **মাত্র ~0.78%**। তাই কম GPU memory-তে train করা যায়। এখানে $\alpha/r = 16/16 = 1$।

**সহজ কথায়:** পুরো matrix শেখালে প্রায় ১.৭ কোটি সংখ্যা শিখতে হতো। LoRA-তে মাত্র ১ লক্ষ ৩১ হাজার। মানে খরচ প্রায় ১০০ ভাগের ১ ভাগ।

### ৬.৮ Fine-tuning Loss (Causal LM Cross-Entropy)
Input $x$ (issue + code), target patch $y = (y_1, \dots, y_m)$:
$$
\mathcal{L}(\theta) = -\sum_{t=1}^{m} \log p_\theta(y_t \mid x,\, y_{<t})
$$
**এটা কী হিসাব করে:** model-এর "ভুলের মাপ"। সঠিক patch-এর প্রতিটা শব্দ model যত কম সম্ভাবনায় ধরেছে, loss তত বেশি। training-এ এটাকে কমানোই লক্ষ্য।
অর্থাৎ model-কে শেখানো হয় gold patch-এর প্রতিটা token সঠিকভাবে predict করতে।

### ৬.৯ Greedy Decoding
$$
y_t = \arg\max_{v \in V}\; p_\theta(v \mid x,\, y_{<t})
$$
**এটা কী হিসাব করে:** প্রতিবার সবচেয়ে সম্ভাব্য পরের শব্দটা বেছে নেওয়া। কোনো এলোমেলো বাছাই নেই, তাই একই input-এ একই output।

### ৬.১০ সম্পর্কিত সূত্র: Pass@k (Chen et al., 2021 — HumanEval)
Paper এটা ব্যবহার না করলেও তুলনার জন্য জানা দরকার। $n$টা sample-এর মধ্যে $c$টা সঠিক হলে:
$$
\text{pass@}k = \mathbb{E}\left[1 - \frac{\binom{n-c}{k}}{\binom{n}{k}}\right]
$$
**এটা কী হিসাব করে:** k বার চেষ্টা করলে অন্তত একবার সঠিক হওয়ার সম্ভাবনা। k = ১ হলে এটা সরাসরি "একবারে কত % ঠিক"।
SWE-bench শুধু 1টা sample নিয়েছে, তাই এটা মূলত **pass@1**।

**সহজ কথায়:** SWE-bench-এ একবারই চেষ্টা, তাই pass@1-ই যথেষ্ট। বেশি বার চেষ্টা করালে ফল ভালো দেখাত, কিন্তু সেটা আসল ব্যবহারের মতো হতো না।

### ৬.১১ Cyclomatic Complexity (Appendix-এ code quality analysis-এ ব্যবহৃত)
$$
M = E - N + 2P
$$
**এটা কী হিসাব করে:** code-এ কতগুলো আলাদা পথ (if, loop) আছে তার গণনা। সংখ্যা বেশি মানে code বোঝা ও test করা কঠিন।
$E$ = control-flow graph-এর edge, $N$ = node, $P$ = connected component। যত বেশি branch (if/else/loop), তত বেশি complexity। Paper দেখিয়েছে Claude 2-এর একটা সঠিক patch-ও gold patch-এর চেয়ে বেশি complexity তৈরি করেছে (3→5 বনাম 2→3)।

**সহজ কথায়:** AI-র patch পাস করলেও সেটা মানুষের patch-এর চেয়ে জটিল হতে পারে। জটিল code মানে ভবিষ্যতে bug-এর ঝুঁকি বেশি।

---

## ৭. Experimental Setup

| বিষয় | বিবরণ |
|---|---|
| **Test set** | 2,294 task, 12 repository |
| **Dev set** | 225 task, আলাদা 6 repository (2019-এর পরের) — hyperparameter tuning-এর জন্য |
| **Models** | ChatGPT-3.5 (16k), GPT-4 (32k), Claude 2 (100k), SWE-Llama 7B/13B (100k) |
| **Retrieval** | BM25 (13k/27k/50k token limit), Oracle, Oracle-collapsed |
| **Metric** | % Resolved, % Apply |
| **Budget constraint** | GPT-4 শুধু 25% random subset-এ test করা হয়েছে |

**Dataset statistics (Table 1):**
| Attribute | Mean | Max |
|---|---|---|
| Issue text (words) | 195.1 | 4,477 |
| Codebase files (non-test) | 3,010 | 5,890 |
| Codebase lines (non-test) | 438K | 886K |
| Gold patch: lines edited | 32.8 | 5,888 |
| Gold patch: files edited | 1.7 | 31 |
| Gold patch: functions edited | 3 | 36 |
| Fail-to-pass tests | 9.1 | 1,633 |
| Total tests | 120.8 | 9,459 |

**সহজ কথায়:** একটা সাধারণ প্রশ্নে bug-এর বিবরণ প্রায় ২০০ শব্দ, project প্রায় ৪ লক্ষ line, আর সঠিক উত্তর বদলায় গড়ে মাত্র ১.৭টা file। মানে বিশাল খড়ের গাদায় একটা ছোট সূচ খোঁজা।

---

## ৮. Results — মূল ফলাফল

### ৮.১ Main Results (BM25 vs Oracle)
| Model | BM25 % Resolved | BM25 % Apply | Oracle % Resolved | Oracle % Apply |
|---|---|---|---|---|
| **Claude 2** | **1.96** | 43.07 | **4.80** | 62.82 |
| ChatGPT-3.5 | 0.17 | 26.33 | 0.52 | 21.80 |
| GPT-4* | 0.00 | 14.83 | 1.74 | 34.00 |
| SWE-Llama 7B | 0.70 | 51.74 | 3.01 | 65.52 |
| SWE-Llama 13B | 0.70 | 53.62 | 3.97 | 66.78 |

*GPT-4 শুধু 25% subset-এ।

**সহজ কথায়:** সেরা AI-ও BM25-এ ১০০টার মধ্যে মাত্র ২টা পেরেছে। আগে থেকে সঠিক file দিলেও ১০০টার মধ্যে ৫টা। GPT-4-র ০.০০ মানে ওই সেটে একটাও ঠিক হয়নি।

### ৮.২ Context length বাড়লে কী হয় (Claude 2, BM25)
| Context limit | 13k | 27k | 50k |
|---|---|---|---|
| % Resolved | **1.96** | 1.87 | 1.22 |
| BM25 Recall (Avg) | 29.58 | 44.41 | 51.06 |

**গুরুত্বপূর্ণ paradox:** Context বাড়ালে সঠিক file পাওয়ার সম্ভাবনা (recall) **বাড়ে**, কিন্তু performance **কমে**! কারণ model অপ্রাসঙ্গিক code-এ "বিভ্রান্ত" হয়ে যায় (*lost in the middle* phenomenon)।

**সহজ কথায়:** বেশি পড়তে দিলে সঠিক file পাওয়ার সুযোগ বাড়ে। কিন্তু AI অপ্রয়োজনীয় লেখার ভিড়ে হারিয়ে যায়। ফল, বেশি দিলেও নম্বর কমে।

### ৮.৩ Oracle-collapsed (Ablation)
| Model | Oracle | Oracle-collapsed |
|---|---|---|
| Claude 2 | 4.8 | **5.93** |
| GPT-4 | 1.3 | **3.40** |

অপ্রাসঙ্গিক code সরিয়ে দিলে performance বাড়ে → **Localization (সঠিক জায়গা খুঁজে পাওয়া)-ই মূল bottleneck।**

**সহজ কথায়:** ভিড় কমিয়ে দিলে AI ভালো করে। তার মানে AI-র আসল কঠিন কাজ "কোথায় দেখতে হবে" ঠিক করা।

### ৮.৪ Model patch বনাম Gold patch (Oracle setting, Table 8)
| | Total lines | Files |
|---|---|---|
| Model patch (গড়) | ~17–30 | ~1.0 |
| Gold patch (সব) | 74.5 | 1.7 |

Model রা ছোট, সরল, "greedy" patch লেখে; প্রায় কখনো একাধিক file edit করে না।

**সহজ কথায়:** মানুষ গড়ে ৭৪.৫ line বদলায় এবং ১.৭টা file ছোঁয়। AI ছোট করে, প্রায় একটাই file বদলায়। অর্থাৎ বড় সমস্যায় AI অল্প করে ঠেকা দিতে চায়।

### ৮.৫ Date অনুযায়ী (Contamination check)
2023-এর আগে ও পরের issue-তে performance প্রায় একই (Claude 2: 4.87 বনাম 4.23) → model মুখস্থ থেকে উত্তর দিচ্ছে এমন শক্ত প্রমাণ নেই। (তবে এটা দুর্বল প্রমাণ — Section ১২ দেখো।)

---

## ৯. Key Findings / Insights (Supervisor-কে বলার মতো ৭টা পয়েন্ট)

1. **বাস্তব software engineering LLM-এর জন্য অনেক কঠিন** — সেরা model মাত্র 1.96%।
2. **Retrieval/Localization হলো সবচেয়ে বড় bottleneck** — Oracle file দিলে performance ~2.5 গুণ বাড়ে।
3. **বেশি context ≠ ভালো performance** — model noise-এ বিভ্রান্ত হয়।
4. **Patch format কঠিন, কিন্তু পুরো file লেখার চেয়ে ভালো** — পুরো file regenerate করলে Claude 2: 2.2% বনাম patch-এ 4.8%।
5. **Fine-tuned model distribution shift-এ sensitive** (train-এর ধরন আর test-এর ধরন আলাদা হলে ঘাবড়ে যায়) — SWE-Llama oracle context-এ train হয়েছে, তাই BM25 context-এ (যেখানে অনেক file বদলানোর দরকার নেই) খারাপ করেছে।
6. **Model-রা ভিন্ন ভিন্ন task solve করে** — Claude 2 ও SWE-Llama 13B প্রায় সমান সংখ্যক solve করলেও overlap মাত্র 42% → ensemble-এর (কয়েকটা model মিলিয়ে একসঙ্গে ব্যবহার) সুযোগ আছে।
7. **Test pass করা মানেই ভালো code নয়** — model-এর patch কম comprehensive, কম readable, বেশি complex হতে পারে (authors নিজেরাই স্বীকার করেছেন)।

**সহজ কথায়:** এই ৭টা কথা মনে রাখলেই paper-এর সারকথা বলা যায়। সবচেয়ে বড় দুটো হলো, "খোঁজাই আসল কঠিন কাজ" আর "test pass মানেই সঠিক নয়"।

---

## ১০. কেন এই Solution অন্যগুলোর থেকে ভালো?

| বৈশিষ্ট্য | HumanEval / MBPP | Defects4J (APR benchmark) | **SWE-bench** |
|---|---|---|---|
| Task-এর উৎস | মানুষের বানানো ছোট problem | আসল bug | **আসল GitHub issue + PR** |
| Input size | কয়েক line | একটা method/file | **পুরো repository (438K line)** |
| Natural language issue | ছোট docstring | সাধারণত নেই | **আসল bug report** |
| Multi-file edit | না | কম | **হ্যাঁ (গড় 1.7 file)** |
| Evaluation | কয়েকটা test | test suite | **F2P + P2P (regression সহ)** |
| Update করা যায়? | না (static) | কঠিন (manual) | **হ্যাঁ — automatic pipeline** |
| Contamination প্রতিরোধ | না | না | **নতুন PR দিয়ে refresh করা যায়** |
| Language | Python | Java | Python |

**সহজ কথায়:** অন্য benchmark ছোট বা আংশিক বাস্তব। SWE-bench-ই একমাত্র যেখানে আসল project, আসল bug, আর পুরনো feature না ভাঙার যাচাই একসঙ্গে আছে।

**মূল শক্তি:**
1. **Realism (ecological validity):** বাস্তব কাজের সাথে মিল।
2. **Execution-based verification:** subjective judgment নয়, test চালিয়ে objective যাচাই।
3. **Scalable ও continually updatable:** minimal human effort-এ নতুন task যোগ করা যায়।
4. **Level playing field:** retrieval-based, long-context, agent-based — সব ধরনের approach একই benchmark-এ তুলনা করা যায়।
5. **Open-source:** dataset, harness, model সব public — reproducible।

---

## ১১. কোন পরিস্থিতিতে এই paper/benchmark ভালো কাজ করে, কোথায় করে না

### ✅ ভালো কাজ করে যখন:
- **Python repository-level bug fixing** ক্ষমতা মাপতে চাও।
- বিভিন্ন **coding agent/tool তুলনা** করতে চাও (standard yardstick)।
- **Retrieval/localization technique** evaluate করতে চাও।
- Issue-তে পরিষ্কার description ও reproduce করার উপায় আছে।

### ❌ ভালো কাজ করে না / সীমিত যখন:
- **অন্য language** (Java, C++, JavaScript) — শুধু Python।
- **Underspecified issue** — issue অস্পষ্ট হলে model-এর দোষ নয় কিন্তু score কমে।
- **Weak test** — test দুর্বল হলে ভুল patch-ও "resolved" হয়ে যায় (false positive)।
- **Image-সহ issue** — matplotlib-এর 32% issue-তে image আছে, text-only model দেখতে পায় না।
- **Code quality, security, maintainability** মাপতে চাইলে — benchmark শুধু functional correctness দেখে।
- **Feature development / long-horizon task** — বেশিরভাগ task ছোট bug fix।

**সহজ কথায়:** SWE-bench ছোট bug ঠিক করার পরীক্ষা। নতুন বড় feature বানানো, অন্য language, নিরাপত্তা বা code-এর সৌন্দর্য মাপতে চাইলে এটা যথেষ্ট নয়।

---

## ১২. Limitations — দুর্বলতা

### ১২.১ Authors যা নিজেরা স্বীকার করেছেন
1. শুধু Python।
2. শুধু সরল baseline (retrieval + single generation) — agent-based approach test করা হয়নি।
3. Execution-based test একা reliability নিশ্চিত করে না — model patch কম comprehensive/efficient/readable হতে পারে।
4. Budget-এর কারণে GPT-4 শুধু 25% subset-এ।

### ১২.২ আমার Critical Analysis (Professor-level observation)
1. **Test adequacy problem (সবচেয়ে গুরুত্বপূর্ণ):** "Resolved" নির্ভর করে developer-এর লেখা test-এর উপর। গড়ে F2P test মাত্র 9.1টা, এবং 60% task-এ মাত্র ১টা F2P test। দুর্বল test হলে **plausible but incorrect patch** (test pass করে কিন্তু আসলে ভুল) "সঠিক" হিসেবে গণ্য হয়। এটা APR literature-এ পরিচিত **"patch overfitting"** problem। পরবর্তী গবেষণা (যেমন SWE-bench+) দেখিয়েছে যে leaderboard-এর "resolved" patch-এর একটা উল্লেখযোগ্য অংশ আসলে ভুল বা solution leak থেকে এসেছে।
2. **Construct validity:** Binary metric — প্রায় ঠিক patch আর একদম ভুল patch দুটোই 0। Partial progress মাপা যায় না।
3. **Contamination evidence দুর্বল:** শুধু "2023-এর আগে/পরে" তুলনা করা হয়েছে, কিন্তু GPT-4-এ পার্থক্য ছিল (1.96 বনাম 0.0)। তাছাড়া repository-গুলো popular হওয়ায় training data-তে থাকার সম্ভাবনা বেশি। Benchmark publish হওয়ার পর contamination আরও বাড়বে।
4. **Solution leakage:** কিছু issue-তে সমাধানের code বা hint সরাসরি লেখা থাকে — তাহলে আসলে "issue solving" নয়, "copy" মাপা হয়।
5. **Task distribution bias:** 850/2294 (~37%) task শুধু django থেকে — একটা repository result-কে dominate করে।
6. **Non-determinism ও reliability মাপা হয়নি:** একবার greedy run — একই model বারবার চালালে consistent কিনা তা জানা যায় না। **"Reliability"** domain-এর জন্য এটা বড় gap।
7. **Cost/efficiency metric নেই:** কত token, কত টাকা, কত সময় লাগলো — তা মাপা হয় না।
8. **Environment reproducibility:** প্রথম version conda-based ছিল; পরে Docker-এ নেওয়া হয়েছে কারণ environment flaky ছিল।
9. **Security dimension নেই:** Agent-এর patch নতুন vulnerability তৈরি করছে কিনা তা দেখা হয় না।

**সহজ কথায়:** মূল দুর্বলতা হলো "পরীক্ষাটাই কতটা নির্ভরযোগ্য"। দুর্বল test হলে ভুল উত্তরও নম্বর পায়। আর একবার মাত্র চালানো হয়েছে বলে AI কতটা ধারাবাহিক তা জানা যায় না।

---

## ১৩. Research Gaps — কোথায় কাজ করার সুযোগ আছে

| # | Gap | কেন গুরুত্বপূর্ণ | কে কিছুটা কাজ করেছে (আমাদের folder-এ) |
|---|---|---|---|
| G1 | **Weak test / patch overfitting** — test pass করা ভুল patch চিহ্নিত করা | Score inflated, agent-কে বিশ্বাস করা যায় না | Patch Validation sub-domain (HITL LLM-as-Judge, APCA) |
| G2 | **Contamination-free, continually updated evaluation** | Score আসল ability না মুখস্থ? | SWE-rebench |
| G3 | **Multi-language ও long-horizon task** | Python-only, ছোট bug fix | SWE-Bench Pro |
| G4 | **Non-functional quality: security, maintainability** | Test pass করেও vulnerable code | Security of AI-Generated Code sub-domain |
| G5 | **Reliability = consistency across runs** | একই input-এ বিভিন্ন output → অবিশ্বস্ত | Engineering Reliable Coding Agents |
| G6 | **Localization improvement** | মূল bottleneck | AutoCodeRover, Agentless, SWE-agent |
| G7 | **Underspecified issue detection** | Model-কে অসম্ভব task-এর জন্য দোষ দেওয়া হয় | — (খোলা) |
| G8 | **Graded / partial-credit metric** | Binary metric progress লুকায় | — (খোলা) |
| G9 | **Multimodal issue (image)** | UI/plotting bug | — (খোলা, পরে SWE-bench Multimodal এসেছে) |

**সহজ কথায়:** এই তালিকা হলো "কোথায় এখনো কাজ বাকি"। G1 ও G4 আমাদের domain-এর (reliability ও assurance) সবচেয়ে কাছের। G7, G8, G9-এ আমাদের folder-এর কোনো paper এখনো কাজ করেনি।

---

## ১৪. কী করলে আরও ভালো হবে — Improvement Ideas

1. **Test augmentation:** LLM বা mutation testing (code-এ ইচ্ছে করে ছোট ভুল ঢুকিয়ে test কতটা ধরতে পারে দেখা) দিয়ে প্রতিটা task-এ অতিরিক্ত test তৈরি করে "resolved" patch আবার যাচাই করা → false positive rate (ভুল patch-কে সঠিক বলে ধরার হার) মাপা।
2. **Multi-dimensional score:** শুধু `Resolved` নয় —
   $$\text{AssuranceScore} = w_1 \cdot \text{Correctness} + w_2 \cdot \text{Security} + w_3 \cdot \text{Quality} + w_4 \cdot \text{Consistency}$$
   (এটা আমার প্রস্তাবিত idea — paper-এ নেই।)
3. **Repeated-run reliability:** প্রতিটা task k বার চালিয়ে **pass^k** (সব k বার সফল হওয়ার হার) মাপা — pass@k-এর উল্টো, এটা reliability মাপে।
4. **Issue quality classifier:** কোন issue underspecified তা আগে detect করে আলাদা report।
5. **Semantic retrieval:** BM25-এর বদলে code-aware embedding বা AST/call-graph (code-এর গাছের মতো কাঠামো ও কে কাকে ডাকে তার নকশা) ভিত্তিক retrieval।

**সহজ কথায়:** আমাদের প্রস্তাব হলো শুধু "পাস না ফেল" না দেখে, patch-টা কতটা ভরসাযোগ্য সেটাও মাপা।

---

## ১৫. কোন Gap-এ Research করলে ভালো Result ও Publication আসতে পারে

> ⚠️ এটা প্রথম paper-এর ভিত্তিতে প্রাথমিক মত। ৭টা sub-domain শেষ করার পর চূড়ান্ত gap বাছাই করবো।

| Gap | SPL3-তে করা সম্ভব? | Novelty | Publication সম্ভাবনা |
|---|---|---|---|
| **G1: Patch overfitting detection** (test augmentation + LLM judge) | ✅ হ্যাঁ — SWE-bench Lite/Verified-এর ছোট subset দিয়ে | উচ্চ, এখনো সক্রিয় | ⭐⭐⭐⭐ |
| **G4+G1: Multi-dimensional assurance** (correctness + security + quality) | ✅ হ্যাঁ — Semgrep/Bandit/CodeQL + test | উচ্চ, domain-এর নামের সাথে সরাসরি মেলে | ⭐⭐⭐⭐⭐ |
| **G5: Run-to-run reliability** | ✅ হ্যাঁ, কিন্তু API cost বেশি | মাঝারি-উচ্চ | ⭐⭐⭐ |
| G2: নতুন contamination-free benchmark | ⚠️ কঠিন (অনেক infra লাগে) | মাঝারি (SWE-rebench আছে) | ⭐⭐ |

**সহজ কথায়:** ছাত্র হিসেবে সবচেয়ে বাস্তব পথ হলো G1 ও G4 মিলিয়ে কাজ করা। কম infra লাগে, নতুনত্বও আছে।

**সম্ভাব্য venue (general guidance):**
- **Conference:** ICSE, FSE, ASE, ISSTA (top SE); তাদের workshop (যেমন LLM4Code) — student-এর জন্য শুরু করা সহজ।
- **Journal:** ACM TOSEM, IEEE TSE (খুব high), Empirical Software Engineering (EMSE), Journal of Systems and Software (JSS), Information and Software Technology (IST) — Q1 এবং student-friendly।

---

## ১৬. SPL3 Implementation Perspective — Software-এ কীভাবে আনবো

**Paper implement করা মানে কী?** নতুন benchmark বানানো নয় — বরং SWE-bench-এর **evaluation pipeline** চালাতে পারে এমন একটা tool বানানো, যেটা দিয়ে অন্য student/researcher তাদের agent-এর patch evaluate করতে পারবে।

**প্রস্তাবিত module:**
1. **Task Loader:** HuggingFace থেকে SWE-bench Lite (300 task) / Verified (500 task) load।
2. **Retriever module:** BM25 baseline (`rank_bm25` library) + recall@k vs oracle হিসাব।
3. **Patch Generator:** যেকোনো LLM API দিয়ে patch তৈরি।
4. **Evaluation Harness wrapper:** official `swebench` package (Docker-based) দিয়ে F2P/P2P চালানো।
5. **Dashboard:** % Resolved, % Apply, repo-wise breakdown, patch size vs gold।
6. **(Gap solve অংশ) Assurance layer:** extra test, security scan, quality metric।

**Practical সতর্কতা:**
- Official harness Docker-ভিত্তিক এবং অনেক disk space ও RAM লাগে — Windows-এ **WSL2 + Docker Desktop** লাগবে। পুরো 2,294 না চালিয়ে Lite/Verified subset দিয়ে শুরু করা উচিত।
- LLM API খরচ হিসাব করে রাখতে হবে।

---

## ১৭. পরবর্তী গবেষণায় এই Paper-এর প্রভাব (Context)
- **SWE-bench Lite** (300 task) — সস্তায় evaluation।
- **SWE-bench Verified** (500 task, OpenAI, 2024) — মানুষ দিয়ে যাচাই করে underspecified ও ভুল test-এর task বাদ দেওয়া হয়েছে → প্রমাণ করে যে মূল benchmark-এ G1 ও G7 gap সত্যি ছিল।
- **SWE-agent, AutoCodeRover, Agentless** — এই benchmark-এ score বাড়ানোর জন্য agent design (আমাদের folder-এর পরের ৩টা paper)।
- **SWE-rebench, SWE-Bench Pro** — contamination ও task difficulty নিয়ে এর উন্নত version।
- Score 2023-এর ~2% থেকে বেড়ে কয়েক বছরের মধ্যে Verified-এ অনেক উঁচুতে পৌঁছেছে — তাই এখন প্রশ্ন "কত % solve" থেকে সরে **"solve করা patch কতটা বিশ্বাসযোগ্য (assurance)"**-এর দিকে যাচ্ছে। **এটাই আমাদের domain-এর মূল motivation।**

---

## ১৮. Supervisor-এর সম্ভাব্য প্রশ্ন ও উত্তর (Viva Prep)

**Q1. SWE-bench আর HumanEval-এর মূল পার্থক্য কী?**
A: HumanEval-এ ছোট self-contained function লিখতে হয়; SWE-bench-এ আসল repository-তে আসল issue solve করতে হয়, multi-file edit লাগে, আর regression test (P2P) সহ evaluate হয়।

**Q2. FAIL_TO_PASS আর PASS_TO_PASS কেন দুটোই দরকার?**
A: F2P প্রমাণ করে issue ঠিক হয়েছে; P2P প্রমাণ করে পুরনো functionality ভাঙেনি। শুধু F2P দেখলে model অন্য কিছু ভেঙে দিয়েও "সঠিক" হতে পারতো।

**Q3. Oracle retrieval কেন বাস্তবসম্মত নয়, তবুও কেন ব্যবহার করা হয়েছে?**
A: বাস্তবে আগে থেকে জানা যায় না কোন file বদলাতে হবে। কিন্তু এটা upper bound দেয় — retrieval perfect হলে model কতটা পারে, তা বোঝা যায়; এতে retrieval vs generation-এর দোষ আলাদা করা যায়।

**Q4. Context বাড়ালে recall বাড়ে কিন্তু performance কমে কেন?**
A: Model অপ্রাসঙ্গিক code-এ distracted হয়; লম্বা context-এর মাঝখানের তথ্য model ভালোভাবে ব্যবহার করতে পারে না। Oracle-collapsed experiment এটা প্রমাণ করে।

**Q5. Contamination কীভাবে handle করা হয়েছে?**
A: (১) SWE-Llama-র training repository আলাদা রাখা; (২) নতুন PR দিয়ে benchmark update করার ক্ষমতা; (৩) 2023-এর আগে/পরে তুলনা। তবে শেষেরটা দুর্বল প্রমাণ।

**Q6. এই paper-এর সবচেয়ে বড় দুর্বলতা কী, তোমার মতে?**
A: Test adequacy — অল্প সংখ্যক F2P test-এর উপর নির্ভরতা, যার ফলে ভুল patch-ও resolved গণ্য হতে পারে। Reliability ও assurance domain-এর জন্য এটাই সবচেয়ে প্রাসঙ্গিক gap।

**Q7. SWE-Llama BM25-এ খারাপ করলো কেন?**
A: Oracle context-এ train হওয়ায় model শিখেছে "যত file দেওয়া হবে সবগুলো edit করতে হবে"। BM25-এ অনেক অপ্রাসঙ্গিক file থাকে → train/test distribution mismatch।

**Q8. তুমি এই paper থেকে কী implement করবে?**
A: SWE-bench evaluation pipeline (Lite/Verified subset), BM25 baseline, এবং তার উপর একটা assurance layer — extra test + security + quality check — যাতে "resolved" patch-এর বিশ্বাসযোগ্যতা মাপা যায়।

---

## ১৯. Glossary (দ্রুত মনে রাখার জন্য)

| Term | অর্থ |
|---|---|
| Benchmark | Model-এর ক্ষমতা মাপার standard পরীক্ষা-সেট |
| Task instance | Benchmark-এর একটা প্রশ্ন (issue + codebase + test) |
| Gold patch | Developer-এর আসল সঠিক solution |
| F2P / P2P | Fail→Pass / Pass→Pass test |
| Regression | নতুন পরিবর্তনে পুরনো feature ভেঙে যাওয়া |
| Oracle retrieval | সঠিক file আগে থেকে দিয়ে দেওয়া (upper bound) |
| Ablation | একটা অংশ সরিয়ে/বদলে তার প্রভাব মাপা |
| BM25 | Keyword-ভিত্তিক document ranking algorithm |
| LoRA | কম parameter train করে fine-tuning |
| Contamination | Test data training-এ ঢুকে যাওয়া |
| Patch overfitting | Test pass করে কিন্তু আসলে ভুল patch |
| Localization | Bug-টা codebase-এর কোথায় তা খুঁজে বের করা |
| Saturation | Benchmark এত সহজ হয়ে যাওয়া যে সবাই full score পায় |

---

## ২০. এক নজরে সারাংশ (Summary Card)

| | |
|---|---|
| **Problem** | পুরনো code benchmark ছোট, অবাস্তব, saturated |
| **Solution** | আসল GitHub issue + PR + test দিয়ে 2,294 task-এর benchmark |
| **Method** | 3-stage filtering pipeline + execution-based F2P/P2P evaluation |
| **Key result** | সেরা model Claude 2 = 1.96% (BM25), 4.8% (Oracle) |
| **Key insight** | Localization হলো মূল bottleneck; বেশি context ক্ষতিকর |
| **Main limitation** | Python-only, weak tests, binary metric, contamination risk |
| **আমাদের জন্য gap** | Patch-এর **assurance** (overfitting, security, quality, consistency) |

---

## ২১. বর্তমান (2026) প্রেক্ষাপট — আজকের Model ও Agent-দের সাথে তুলনা

> **উৎস:** এই section-এর সব current-state তথ্য `00_Current_State_2026_Sources.md` (fact sheet, compiled 2026-10-28) থেকে নেওয়া। প্রতিটা সংখ্যার পাশে লেখা আছে সেটা **কোম্পানির নিজের দাবি (vendor-reported)** নাকি **স্বাধীনভাবে মাপা (independent)**। Fact sheet যেটাকে "search-snippet only" বলেছে, সেটা এখানেও তাই চিহ্নিত — supervisor-কে দেখানোর আগে মূল উৎস খুলে যাচাই করা উচিত। আমার নিজের যুক্তি "আমার পর্যবেক্ষণ" দিয়ে আলাদা করা।

### ২১.১ Paper-এর সময় বনাম এখন

| দিক | Paper-এ (2023, ICLR 2024) | এখন, October 2026 | উৎস |
|---|---|---|---|
| সেরা score | Claude 2: 1.96% (BM25), 4.80% (Oracle), full 2,294 task | SWE-bench Verified-এ Claude Opus 5: **97.0%**; DeepSeek V4 Pro 0813: 96.4%; GPT-5.6 Sol: 96.2% (mini-SWE-agent harness, **স্বাধীনভাবে মাপা**) | Vals.ai, updated 2026-09-01 |
| Official leaderboard | Paper-এর সাথে swebench.com চালু | শেষ Verified entry 2026-02-26; top 79.2% (Claude 4.5 Opus + Sonar Foundation Agent বা live-SWE-agent); bash-only board 2026-08-31-এ বাদ ("Drop bash-only board") | SWE-bench leaderboards.json ও commit log, fetched 2026-10-28 |
| Benchmark-এর অবস্থা | নতুন, কঠিন, "continually updatable" | Vals.ai **saturation**-এর কারণে Verified archive করেছে; OpenAI Verified-এ evaluate করা বন্ধ করেছে (contamination ও flawed test); Anthropic-এর Opus 5.5 System Card-এ Verified নেই | Vals.ai; OpenAI 2026-02-23 (search-snippet only, page 403); Opus 5.5 System Card |
| Test-এর মান | Paper ধরে নিয়েছে developer test-ই oracle | OpenAI-এর audit: প্রায়ই-fail হওয়া একটা hard subset-এর অন্তত **59.4%** task-এর test সঠিক submission-কেও reject করে | OpenAI 2026-02-23 (search-snippet only) |
| Contamination | 2023-এর আগে/পরে তুলনা — "শক্ত প্রমাণ নেই" | OpenAI: Verified "increasingly contaminated"; secondary report: GPT-5.2, Claude Opus 4.5, Gemini 3 Flash gold patch হুবহু reproduce করতে পারে | OpenAI (snippet); byteiota (secondary) |
| Lite subset | পরে বানানো (300 task) | Official board-এ শেষ Lite entry 2025-09-11 (top 60.33%); lab বা নতুন system card আর Lite report করে না | SWE-bench leaderboards.json |
| Multilingual (paper-এ শুধু Python) | — | Official top: Gemini 3 Flash 72.7% (Feb 2026, independent checked); Opus 5.5: 93.9% (**vendor-reported**) | leaderboards.json; Opus 5.5 System Card |
| Multimodal (paper-এ image-সহ issue বাদ পড়ে) | — | Official top 35.98% (শেষ entry 2025-11); Opus 5.5: 61.4% (**vendor-reported**) | leaderboards.json; Opus 5.5 System Card |
| প্রতি task-এর খরচ | Paper-এ মাপা হয়নি (critique #7) | Verified-এ USD 0.10 (DeepSeek V4 Pro) থেকে USD 2.05 (Fable 5) per test (**independent**) | Vals.ai, Sept 2026 |

**সহজ কথায়:** ২০২৩-এ সেরা ছিল ২%, আর ২০২৬-এ নতুন model-এর সংখ্যা ৯০%-এর উপরে। কিন্তু benchmark নিজেই দুর্বল ও পুরনো হয়ে যাওয়ায় সংখ্যাগুলো পুরোপুরি বিশ্বাসযোগ্য নয়।

**আমার পর্যবেক্ষণ:** $\frac{97.0}{1.96} \approx 49.5$ গুণ। কিন্তু এটা একই benchmark নয় (full 2,294 বনাম Verified 500), একই setting নয় (single-shot RAG বনাম agent harness)। আর fact sheet নিজেই বলছে official board-এ Feb 2026-এ ~79% আর Vals-এ Sept 2026-এ ~97% — একই 500 task-এ এত দ্রুত লাফ, সাথে 59.4% flawed test-এর তথ্য মিলিয়ে ~90%-এর উপরের score-এর একটা অংশ memorization বা contamination হতে পারে। এটা fact sheet-এর লেখকেরও **অনুমান, মাপা তথ্য নয়**।

### ২১.২ কোন Finding এখনো সত্য, কোনটা পুরনো হয়ে গেছে

- **পুরনো হয়ে গেছে — "বাস্তব software engineering LLM-এর জন্য অনেক কঠিন" (Key Finding ১):** Verified-এ 97.0% (Vals.ai, independent)। এই benchmark আর frontier model-দের আলাদা করতে পারে না — Section ২.১২-এর "saturation" সংজ্ঞা এখন SWE-bench-এর উপরেই খাটে, ঠিক যেমন paper HumanEval-এর ক্ষেত্রে বলেছিল।
- **পুরনো (অন্তত frontier-এর জন্য) — "বেশি context ক্ষতিকর":** আজকের agent harness (mini-SWE-agent) নিজে file খোঁজে, তাই paper-এর BM25 13k/27k/50k setting আর প্রাসঙ্গিক নয়। তবে বর্তমান model-এর জন্য context-length বনাম performance-এর SWE-bench-specific তথ্য fact sheet-এ **পাওয়া যায়নি**।
- **এখনো সত্য, আরও শক্ত প্রমাণসহ — "Test pass মানেই ভালো code নয়" (Key Finding ৭ ও critique #1):** PatchDiff (ICSE 2026): "correct" patch-এর 7.8% পুরো developer test suite-এ fail করে; plausible patch-এর 29.6% gold patch থেকে ভিন্ন আচরণ করে (independent)। কিন্তু এটা 2025-এর model-এর উপর; **বর্তমান model দিয়ে আবার মাপা হয়নি**।
- **এখনো সত্য — contamination-এর ঝুঁকি (critique #3):** Paper-এর দুর্বল "আগে/পরে" check-এর বদলে এখন OpenAI নিজেই contamination স্বীকার করে benchmark ছেড়েছে।
- **এখনো সত্য — "Model-রা ভিন্ন ভিন্ন task solve করে, ensemble-এর সুযোগ" (Key Finding ৬):** SWE-rebench-এ pass@1 ও pass@5-এর মধ্যে 12–18 point gap (independent) — অর্থাৎ একই model-এর ভিন্ন run-ও ভিন্ন task solve করে।
- **নতুন সমস্যা, paper-এ ছিল না — leaderboard আর ranking করতে পারে না:** "Coding Agents Have Converged" (arXiv 2609.17394): Verified-এর top-30-এর পাশাপাশি 29টা pair-এর **0টা** McNemar test-এ আলাদা করা যায়; একই model-এ scaffold বদলালে 29.8 point পর্যন্ত পার্থক্য, অথচ top-30-এর পুরো spread মাত্র 8.8 point (independent)।
- **Paper-এর "নতুন PR দিয়ে refresh" ধারণা — বাস্তবায়িত হয়েছে, কিন্তু অন্যের হাতে:** SWE-rebench (মাসিক নতুন task) এই কাজ করছে, তবে এর সর্বশেষ public window 2026-07-01-এ শেষ — Opus 5.5, Sonnet/Haiku 5.5 বা GPT-6 সেখানে **এখনো নেই**।

### ২১.৩ এই Paper-এর Gap-গুলো আজও খোলা কিনা

| Gap | 2026-এ অবস্থা | প্রমাণ |
|---|---|---|
| G1 / CG1: Weak test ও patch overfitting | **খোলা** | Verified-এর audited hard subset-এ ≥59.4% flawed test (OpenAI, snippet); PatchDiff 29.6% (2025 model); SWE-Bench Pro-তে 27.4–34.1% task broken (OpenAI audit, secondary report the-decoder) |
| G2 / CG6: Contamination-free evaluation | **আংশিক সমাধান** | SWE-rebench, DeepSWE v1.1 (113টা নতুন করে লেখা task), private SWE-Bench Pro আছে; কিন্তু SWE-rebench-এ Opus 5.5/GPT-6 নেই, আর Scale-এর commercial (private) set-এ বর্তমান model-এর সংখ্যা পাওয়া যায়নি (URL 404) |
| G3: Multi-language ও long-horizon | **আংশিক সমাধান** | Multilingual ও DeepSWE (5 language) আছে; কিন্তু vendor সংখ্যা (Multilingual 93.9%) আর official independent সংখ্যার (72.7%) মধ্যে বড় ফাঁক |
| G4 / CG5: Security ও maintainability | **খোলা** | SusVibes-এ SWE-agent + Claude 4 Sonnet: 57% functionally correct, মাত্র 11.8% secure; Cursor + Opus 4.6: FuncPass 84.4% কিন্তু SecPass 7.8% (Endor Labs)। Opus 5.5, GPT-6, Gemini 4-এর SusVibes বা BaxBench result **পাওয়া যায়নি** |
| G5 / CG4: Run-to-run reliability | **খোলা (এখন মাপা হচ্ছে, সমাধান নয়)** | Anthropic Terminal-Bench 4.0-এ ±2.6 SE report করে (vendor); Noise Floor Audit (arXiv 2608.22331): prompt-এর অর্থ-অপরিবর্তিত পরিবর্তনে SD rerun-এর চেয়ে 11–58 গুণ বেশি |
| G6: Localization | **বর্তমান model-এর জন্য তথ্য পাওয়া যায়নি** | Fact sheet-এ বর্তমান agent-এর localization accuracy-র কোনো সংখ্যা নেই |
| G7: Underspecified issue | **খোলা** | SWE-Bench Pro Verified 22টা misleading description ঠিক করেছে; OpenAI "underspecified prompts" কে failure category বলেছে; Anthropic: অসম্ভব task-এ reward hacking-এর চেষ্টা 3–6 গুণ বাড়ে (Opus 5.5 System Card, vendor) |
| G8: Graded / partial-credit metric | **আংশিক সমাধান** | FrontierCode v1.1 held-out test-এর সাথে model-graded "mergeability" rubric ব্যবহার করে; কিন্তু LLM judge নিজেই অবিশ্বস্ত — ComPass-এ plain LLM baseline মাত্র 62.14% (search-snippet only) |
| G9: Multimodal issue | **আংশিক সমাধান** | SWE-bench Multimodal আছে; official top 35.98% (2025-11), vendor দাবি 61.4% |
| CG10 / CG12: Evaluation validity ও verifier gaming | **খোলা, নতুন রূপে** | SWE-Bench Pro Verified (arXiv 2609.08149): GLM-5.2-এর score 78.80% থেকে anti-hacking safeguard দিলে 57.32%; agent `.git` history থেকে gold patch পড়ে |

**সহজ কথায়:** paper-এর রেখে যাওয়া বেশিরভাগ gap ২০২৬-এও পুরো সমাধান হয়নি। তাই আমাদের গবেষণার সুযোগ এখনো আছে।

### ২১.৪ বর্তমান Model দিয়ে আবার পরীক্ষা করলে — SPL3 Idea

1. **"Verified বনাম fresh" contamination gap মাপা:** একটা সস্তা current model (যেমন GPT-6.1 Terra, vendor-reported API দাম USD 1 input / USD 5 output per million token; বা DeepSeek V4 Pro, Vals-এ Verified-এ USD 0.10 per test) দিয়ে Verified-এর 30টা task আর SWE-rebench-এর সর্বশেষ window-এর 30টা task mini-SWE-agent harness-এ চালানো। **যে gap দেখাবে:** একই model-এ পুরনো বনাম নতুন task-এর পার্থক্য — G2-এর সরাসরি, ছোট-scale প্রমাণ।
2. **Resolved patch-এর behavioral audit (PatchDiff-ধাঁচে):** উপরের run-এর resolved patch-গুলোকে পুরো developer test suite ও gold patch-এর সাথে differential test দিয়ে তুলনা। **Gap:** 29.6%-এর সংখ্যাটা বর্তমান model-এ কমেছে কিনা — fact sheet বলছে এটা কেউ আবার মাপেনি।
3. **Leakage-safe harness তৈরি:** Container থেকে `.git` history ও network সরিয়ে (SWE-Bench Pro Verified-এর চারটা leakage channel অনুযায়ী) একই task আবার চালানো। **Gap:** CG12 — score-এর কত অংশ verifier gaming থেকে আসে।
4. **Repeated-run reliability:** 30টা task × 3 run, pass@3 ও pass^3 দুটোই report। **আমার পর্যবেক্ষণ (rough খরচ):** Vals-এর Verified cost range ধরে 90 run × USD 0.10–2.05 ≈ USD 9–185 — model বাছাইয়ের উপর অনেক নির্ভর করে। **Gap:** G5 — SWE Atlas-এ Pass@1 থেকে Pass^3-এ 30–50% পতন (search-snippet only) আমাদের ছোট sample-এ মেলে কিনা।
5. **Security overlay:** Resolved patch-এ Bandit/Semgrep চালিয়ে "resolved but insecure" হার। **Gap:** G4 — বর্তমান model-এর জন্য এই সংখ্যা কোথাও পাওয়া যায়নি, তাই ছোট study-ও নতুন তথ্য দেবে।

### ২১.৫ Supervisor-এর সম্ভাব্য প্রশ্ন (2026 প্রসঙ্গে)

**Q1. SWE-bench-এ এখন 97% — তাহলে এই paper কি আর প্রাসঙ্গিক?**
A: Benchmark হিসেবে frontier model-এর জন্য saturated — Vals.ai archive করেছে, OpenAI বাদ দিয়েছে। কিন্তু paper-এর **evaluation design** (আসল issue, execution-based F2P/P2P test, Docker harness) এখনো সব নতুন benchmark-এর (SWE-rebench, SWE-Bench Pro, DeepSWE) ভিত্তি। আর paper-এর নিজের স্বীকার করা দুর্বলতা — weak test ও contamination — ঠিক এই দুটো কারণেই benchmark-টা ছাড়তে হয়েছে।

**Q2. Opus 5.5-এর Verified score কত?**
A: Opus 5.5 System Card-এ Verified নেই — Anthropic SWE-bench Pro (89.9%), Multilingual (93.9%), Multimodal (61.4%) report করেছে, সবগুলো vendor-reported। Verified-এ সবচেয়ে বেশি স্বাধীন সংখ্যা Claude Opus 5-এর 97.0% (Vals.ai)। Opus 5.5-এর Verified সংখ্যা fact sheet-এ পাওয়া যায়নি।

**Q3. তাহলে তোমার SPL3-এ কোন benchmark ব্যবহার করবে?**
A: পুরনো literature-এর সাথে তুলনার জন্য Verified-এর ছোট subset, কিন্তু মূল দাবির জন্য contamination-resistant task (SWE-rebench-এর সর্বশেষ window) এবং leakage-safe harness। আর শুধু resolved rate নয় — behavioral audit, pass^k ও security scan একসাথে report করবো, কারণ "resolved" এখন আর trust-এর যথেষ্ট সূচক নয়।
