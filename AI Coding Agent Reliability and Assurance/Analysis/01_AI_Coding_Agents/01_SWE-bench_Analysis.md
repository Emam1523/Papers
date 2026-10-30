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

## ১. এক লাইনে Paper (TL;DR)

**SWE-bench হলো একটা benchmark যেখানে LLM-কে আসল GitHub repository-র আসল bug report (issue) দেওয়া হয়, আর LLM-কে code পরিবর্তন (patch) করে সেই bug ঠিক করতে হয়; সেই patch সঠিক কিনা তা repository-র আসল unit test চালিয়ে যাচাই করা হয়।**

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

### ৩.২ কেন এটা গুরুত্বপূর্ণ?
LLM তখন Copilot-এর মতো commercial product-এ ব্যবহার হচ্ছিল। কিন্তু বাস্তব software engineering কাজে এরা কতটা সক্ষম তা মাপার কোনো ভালো উপায় ছিল না। **যা মাপা যায় না, তা উন্নত করা যায় না।**

---

## ৪. Goal ও Research Questions

**Goal:** একটা realistic, কঠিন, execution-based ও সহজে update করা যায় এমন benchmark তৈরি করা।

Paper-টা মূলত এই প্রশ্নগুলোর উত্তর খুঁজেছে (implicit RQ):
- **RQ1:** State-of-the-art LLM (GPT-4, Claude 2, ChatGPT-3.5) আসল GitHub issue কতটা solve করতে পারে?
- **RQ2:** Retrieval (কোন file দেখানো হবে) performance-এ কতটা প্রভাব ফেলে?
- **RQ3:** Context length বাড়লে performance-এ কী হয়?
- **RQ4:** Open-source model-কে fine-tune করে (SWE-Llama) কি proprietary model-এর সাথে প্রতিযোগিতা করা যায়?
- **RQ5:** Model-এর লেখা patch আর মানুষের লেখা patch-এর মধ্যে পার্থক্য কী?

---

## ৫. Methodology — কীভাবে কাজটা করা হয়েছে

### ৫.১ Benchmark Construction: ৩-Stage Pipeline

| Stage | নাম | কী করা হয় | Output |
|---|---|---|---|
| I | Scrape PRs | 12টা popular Python repository থেকে সব PR সংগ্রহ | ~90,000 PR |
| II | Attribute Filter | PR merged হয়েছে + কোনো issue resolve করে + test file পরিবর্তন করে | Candidate task |
| III | Execution Filter | Install সফল হয় + অন্তত ১টা FAIL_TO_PASS test আছে | **2,294 task instance** |

**Stage I — Repository selection ও scraping:**
- PyPI-এর top 5,000 সবচেয়ে বেশি download হওয়া library থেকে top 100 বাছাই, license check, তারপর 12টা repository নেওয়া হয় (django, sympy, scikit-learn, sphinx, matplotlib, pytest, xarray, astropy, pylint, requests, seaborn, flask)।
- কেন popular repo? কারণ এগুলো well-maintained, ভালো documentation ও ভালো test coverage আছে।

**Stage II — Attribute-based filtering:** একটা PR task হবে যদি:
1. Status = **Merged** (অর্থাৎ maintainer গ্রহণ করেছে),
2. কোনো issue-কে link করে ("fixes #24" এরকম লেখা দিয়ে),
3. কোনো test file পরিবর্তন করে (path-এ "test"/"testing" শব্দ আছে)।

**Stage III — Execution-based filtering:**
- Codebase install করা হয়, PR-এর test অংশ (test patch) apply করা হয়।
- Solution apply-এর **আগে ও পরে** test চালানো হয়।
- অন্তত একটা test **fail → pass** না হলে বাদ।
- Install বা runtime error হলে বাদ।
- যে test নতুন তৈরি হওয়া function/class-এর নাম ব্যবহার করে, সেগুলোও বাদ (কারণ issue-তে নাম বলা থাকে না, model অনুমান করতে পারবে না)।

**গুরুত্বপূর্ণ design decision:** Problem statement-এ শুধু PR-এর প্রথম commit-এর **আগের** comment রাখা হয় — যাতে solution-এর hint leak না হয়।

### ৫.২ Task Formulation
- **Input:** Issue text + পুরো codebase
- **Output:** একটা patch file
- **Evaluation:** Patch apply → test চালানো → সব F2P ও P2P pass করলে "Resolved"

### ৫.৩ Evaluation Pipeline (প্রতিটা prediction-এর জন্য ৭টা ধাপ)
1. Repository base commit-এ checkout
2. ঐ version-এর জন্য conda environment activate
3. Codebase install
4. Test patch apply
5. Model-এর patch apply
6. Apply fail করলে patch-কে auto-fix (header ঠিক করা, অপ্রয়োজনীয় context line মুছা) করে আবার চেষ্টা
7. Test script চালিয়ে log বের করা → log parse করে প্রতিটা test-এর status বের করা

যদি ধাপ ৫/৬/৭ fail করে → score = 0।

### ৫.৪ Baseline System: Retrieval + Generation
যেহেতু পুরো codebase context-এ ঢোকে না, তাই দুটো setting:
1. **BM25 (Sparse) retrieval:** issue text দিয়ে BM25 চালিয়ে সবচেয়ে প্রাসঙ্গিক file গুলো নেওয়া, context limit (13k/27k/50k token) পর্যন্ত। File path-ও document-এর শুরুতে যোগ করা হয়েছে, যাতে issue-তে file-এর নাম থাকলে মিলে যায়।
2. **"Oracle" retrieval:** আসল (gold) patch যে file গুলো পরিবর্তন করেছে, সরাসরি সেই file গুলো দেওয়া — বাস্তবসম্মত নয় (কারণ বাস্তবে কেউ আগে জানে না কোন file বদলাতে হবে), কিন্তু **upper-bound analysis**-এর জন্য।
3. **"Oracle-collapsed":** Oracle file-এর শুধু পরিবর্তিত line-এর ±15 line রাখা, বাকি সব collapse — এটা একটা **ablation study**।

Prompt-এ থাকে: instruction + issue + retrieved files (+ README) + একটা example patch format।

### ৫.৫ SWE-Llama: Open Model Fine-tuning
- **কেন:** off-the-shelf CodeLlama repository-wide edit-এর instruction follow করতে পারছিল না — placeholder বা অপ্রাসঙ্গিক code লিখছিল।
- **Data:** SWE-bench-train — **37টা আলাদা** repository থেকে 19,000 issue-PR pair (test বাধ্যতামূলক নয়)। Evaluation repository-র সাথে **disjoint**, যাতে contamination না হয়। 30,000 token-এর বেশি লম্বা sequence বাদ দিয়ে কার্যকর ~10,000 instance।
- **Training:** Input = instruction + issue + oracle file; Output = gold patch।
- **Hyperparameters:** LoRA r = 16, α = 16, dropout = 0.05 (attention-এর Q, K, V, O projection-এ); learning rate 6e-4; batch size 32; সর্বোচ্চ 4 epoch; 100টা held-out instance-এর validation loss দিয়ে best checkpoint বাছাই।
- **Compute:** 7B — 4×A100-এ 20 ঘন্টা; 13B — 8×A100-এ 47 ঘন্টা। Long context-এর জন্য DeepSpeed Ulysses ও Flash Attention।

### ৫.৬ Inference Setting
প্রতিটা task-এ মাত্র **১টা patch**, **greedy decoding** (খরচ কমানোর জন্য)।

---

## ৬. Mathematical Formulation — সূত্র ও ব্যাখ্যা

Paper-এ explicitly অনেক equation নেই (benchmark paper হওয়ায়), কিন্তু পুরো evaluation-টা formal ভাবে লেখা যায়। Supervisor-কে দেখানোর জন্য এটা খুব কাজের।

### ৬.১ একটা Task Instance-এর Formal Definition
$$
I = (C,\; P,\; T,\; \delta)
$$
- $C$ = base commit-এ codebase (bug থাকা অবস্থা)
- $P$ = problem statement (issue title + description + comments)
- $T$ = test patch (PR-এর test অংশ)
- $\delta$ = gold patch (developer-এর আসল solution)

Model $M$ ও retriever $R$ থাকলে model-এর prediction:
$$
\hat{\delta} = M\big(P,\; R(C, P)\big)
$$
অর্থাৎ retriever codebase থেকে কিছু file বাছাই করে, model সেই file আর issue দেখে patch $\hat{\delta}$ তৈরি করে।

### ৬.২ F2P ও P2P Set
$C \oplus T$ মানে codebase-এ test patch apply করা। $s(t, X)$ মানে codebase $X$-এ test $t$-এর status।
$$
F2P = \{\, t \in T \;:\; s(t,\, C \oplus T) = \text{FAIL} \;\land\; s(t,\, C \oplus T \oplus \delta) = \text{PASS} \,\}
$$
$$
P2P = \{\, t \;:\; s(t,\, C \oplus T) = \text{PASS} \;\land\; s(t,\, C \oplus T \oplus \delta) = \text{PASS} \,\}
$$
**সহজ ভাষায়:** F2P = যে test গুলো gold patch-এর কারণে fail থেকে pass হয়েছে। P2P = যে test গুলো আগেও pass ছিল, পরেও pass।

### ৬.৩ Resolved হওয়ার শর্ত
$$
\text{Resolved}(\hat{\delta}) =
\begin{cases}
1, & \text{যদি } \hat{\delta} \text{ apply হয় এবং } \forall t \in F2P \cup P2P:\; s(t,\, C \oplus T \oplus \hat{\delta}) = \text{PASS} \\
0, & \text{অন্যথায়}
\end{cases}
$$
**মানে:** একটা test-ও fail বা missing হলে পুরো task fail। এটা একটা **binary, all-or-nothing** metric — কোনো partial credit নেই।

### ৬.৪ Main Metric: % Resolved ও % Apply
$$
\%\,\text{Resolved} = \frac{1}{N} \sum_{i=1}^{N} \text{Resolved}(\hat{\delta}_i) \times 100
$$
$$
\%\,\text{Apply} = \frac{1}{N} \sum_{i=1}^{N} \mathbb{1}\big[\hat{\delta}_i \text{ সফলভাবে apply হয়েছে}\big] \times 100
$$
**Worked example:** N = 2,294; Claude 2 = 1.96% → $2294 \times 0.0196 \approx 45$টা task solve করেছে। আর % Apply = 43.07% → প্রায় 988টা patch অন্তত syntax/format ঠিক রেখে apply হয়েছে, কিন্তু তার মধ্যে মাত্র 45টা আসলে সঠিক।

### ৬.৫ BM25 Retrieval Score
Query $Q$ (issue text)-এ শব্দ $q_1, \dots, q_n$; document $D$ (একটা code file):
$$
\text{score}(D, Q) = \sum_{i=1}^{n} \text{IDF}(q_i) \cdot \frac{f(q_i, D)\,(k_1 + 1)}{f(q_i, D) + k_1\left(1 - b + b\,\dfrac{|D|}{\text{avgdl}}\right)}
$$
$$
\text{IDF}(q_i) = \ln\!\left(\frac{N - n(q_i) + 0.5}{n(q_i) + 0.5} + 1\right)
$$
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

### ৬.৬ Retrieval Recall (Oracle-এর তুলনায়)
$O$ = oracle file set, $\hat{R}$ = BM25 যে file গুলো এনেছে:
$$
\text{Recall} = \frac{|\hat{R} \cap O|}{|O|}
$$
Paper তিনভাবে report করেছে:
- **Avg:** গড় recall
- **All:** কত % task-এ $O \subseteq \hat{R}$ (সব দরকারি file পেয়েছে)
- **Any:** কত % task-এ $\hat{R} \cap O \neq \emptyset$ (অন্তত একটা দরকারি file পেয়েছে)

### ৬.৭ LoRA (SWE-Llama-তে ব্যবহৃত)
মূল weight matrix $W_0 \in \mathbb{R}^{d \times k}$ freeze রেখে:
$$
W' = W_0 + \Delta W = W_0 + \frac{\alpha}{r}\, B A, \qquad B \in \mathbb{R}^{d \times r},\; A \in \mathbb{R}^{r \times k},\; r \ll \min(d, k)
$$
শুধু $A$ ও $B$ train হয়।

**Worked example:** $d = k = 4096$ হলে full fine-tuning-এ একটা matrix-এ $4096 \times 4096 \approx 16.7$M parameter। LoRA ($r=16$)-তে $2 \times 4096 \times 16 = 131{,}072$ parameter — **মাত্র ~0.78%**। তাই কম GPU memory-তে train করা যায়। এখানে $\alpha/r = 16/16 = 1$।

### ৬.৮ Fine-tuning Loss (Causal LM Cross-Entropy)
Input $x$ (issue + code), target patch $y = (y_1, \dots, y_m)$:
$$
\mathcal{L}(\theta) = -\sum_{t=1}^{m} \log p_\theta(y_t \mid x,\, y_{<t})
$$
অর্থাৎ model-কে শেখানো হয় gold patch-এর প্রতিটা token সঠিকভাবে predict করতে।

### ৬.৯ Greedy Decoding
$$
y_t = \arg\max_{v \in V}\; p_\theta(v \mid x,\, y_{<t})
$$

### ৬.১০ সম্পর্কিত সূত্র: Pass@k (Chen et al., 2021 — HumanEval)
Paper এটা ব্যবহার না করলেও তুলনার জন্য জানা দরকার। $n$টা sample-এর মধ্যে $c$টা সঠিক হলে:
$$
\text{pass@}k = \mathbb{E}\left[1 - \frac{\binom{n-c}{k}}{\binom{n}{k}}\right]
$$
SWE-bench শুধু 1টা sample নিয়েছে, তাই এটা মূলত **pass@1**।

### ৬.১১ Cyclomatic Complexity (Appendix-এ code quality analysis-এ ব্যবহৃত)
$$
M = E - N + 2P
$$
$E$ = control-flow graph-এর edge, $N$ = node, $P$ = connected component। যত বেশি branch (if/else/loop), তত বেশি complexity। Paper দেখিয়েছে Claude 2-এর একটা সঠিক patch-ও gold patch-এর চেয়ে বেশি complexity তৈরি করেছে (3→5 বনাম 2→3)।

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

### ৮.২ Context length বাড়লে কী হয় (Claude 2, BM25)
| Context limit | 13k | 27k | 50k |
|---|---|---|---|
| % Resolved | **1.96** | 1.87 | 1.22 |
| BM25 Recall (Avg) | 29.58 | 44.41 | 51.06 |

**গুরুত্বপূর্ণ paradox:** Context বাড়ালে সঠিক file পাওয়ার সম্ভাবনা (recall) **বাড়ে**, কিন্তু performance **কমে**! কারণ model অপ্রাসঙ্গিক code-এ "বিভ্রান্ত" হয়ে যায় (*lost in the middle* phenomenon)।

### ৮.৩ Oracle-collapsed (Ablation)
| Model | Oracle | Oracle-collapsed |
|---|---|---|
| Claude 2 | 4.8 | **5.93** |
| GPT-4 | 1.3 | **3.40** |

অপ্রাসঙ্গিক code সরিয়ে দিলে performance বাড়ে → **Localization (সঠিক জায়গা খুঁজে পাওয়া)-ই মূল bottleneck।**

### ৮.৪ Model patch বনাম Gold patch (Oracle setting, Table 8)
| | Total lines | Files |
|---|---|---|
| Model patch (গড়) | ~17–30 | ~1.0 |
| Gold patch (সব) | 74.5 | 1.7 |

Model রা ছোট, সরল, "greedy" patch লেখে; প্রায় কখনো একাধিক file edit করে না।

### ৮.৫ Date অনুযায়ী (Contamination check)
2023-এর আগে ও পরের issue-তে performance প্রায় একই (Claude 2: 4.87 বনাম 4.23) → model মুখস্থ থেকে উত্তর দিচ্ছে এমন শক্ত প্রমাণ নেই। (তবে এটা দুর্বল প্রমাণ — Section ১২ দেখো।)

---

## ৯. Key Findings / Insights (Supervisor-কে বলার মতো ৭টা পয়েন্ট)

1. **বাস্তব software engineering LLM-এর জন্য অনেক কঠিন** — সেরা model মাত্র 1.96%।
2. **Retrieval/Localization হলো সবচেয়ে বড় bottleneck** — Oracle file দিলে performance ~2.5 গুণ বাড়ে।
3. **বেশি context ≠ ভালো performance** — model noise-এ বিভ্রান্ত হয়।
4. **Patch format কঠিন, কিন্তু পুরো file লেখার চেয়ে ভালো** — পুরো file regenerate করলে Claude 2: 2.2% বনাম patch-এ 4.8%।
5. **Fine-tuned model distribution shift-এ sensitive** — SWE-Llama oracle context-এ train হয়েছে, তাই BM25 context-এ (যেখানে অনেক file বদলানোর দরকার নেই) খারাপ করেছে।
6. **Model-রা ভিন্ন ভিন্ন task solve করে** — Claude 2 ও SWE-Llama 13B প্রায় সমান সংখ্যক solve করলেও overlap মাত্র 42% → ensemble-এর সুযোগ আছে।
7. **Test pass করা মানেই ভালো code নয়** — model-এর patch কম comprehensive, কম readable, বেশি complex হতে পারে (authors নিজেরাই স্বীকার করেছেন)।

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

---

## ১৪. কী করলে আরও ভালো হবে — Improvement Ideas

1. **Test augmentation:** LLM বা mutation testing দিয়ে প্রতিটা task-এ অতিরিক্ত test তৈরি করে "resolved" patch আবার যাচাই করা → false positive rate মাপা।
2. **Multi-dimensional score:** শুধু `Resolved` নয় —
   $$\text{AssuranceScore} = w_1 \cdot \text{Correctness} + w_2 \cdot \text{Security} + w_3 \cdot \text{Quality} + w_4 \cdot \text{Consistency}$$
   (এটা আমার প্রস্তাবিত idea — paper-এ নেই।)
3. **Repeated-run reliability:** প্রতিটা task k বার চালিয়ে **pass^k** (সব k বার সফল হওয়ার হার) মাপা — pass@k-এর উল্টো, এটা reliability মাপে।
4. **Issue quality classifier:** কোন issue underspecified তা আগে detect করে আলাদা report।
5. **Semantic retrieval:** BM25-এর বদলে code-aware embedding বা AST/call-graph ভিত্তিক retrieval।

---

## ১৫. কোন Gap-এ Research করলে ভালো Result ও Publication আসতে পারে

> ⚠️ এটা প্রথম paper-এর ভিত্তিতে প্রাথমিক মত। ৭টা sub-domain শেষ করার পর চূড়ান্ত gap বাছাই করবো।

| Gap | SPL3-তে করা সম্ভব? | Novelty | Publication সম্ভাবনা |
|---|---|---|---|
| **G1: Patch overfitting detection** (test augmentation + LLM judge) | ✅ হ্যাঁ — SWE-bench Lite/Verified-এর ছোট subset দিয়ে | উচ্চ, এখনো সক্রিয় | ⭐⭐⭐⭐ |
| **G4+G1: Multi-dimensional assurance** (correctness + security + quality) | ✅ হ্যাঁ — Semgrep/Bandit/CodeQL + test | উচ্চ, domain-এর নামের সাথে সরাসরি মেলে | ⭐⭐⭐⭐⭐ |
| **G5: Run-to-run reliability** | ✅ হ্যাঁ, কিন্তু API cost বেশি | মাঝারি-উচ্চ | ⭐⭐⭐ |
| G2: নতুন contamination-free benchmark | ⚠️ কঠিন (অনেক infra লাগে) | মাঝারি (SWE-rebench আছে) | ⭐⭐ |

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
