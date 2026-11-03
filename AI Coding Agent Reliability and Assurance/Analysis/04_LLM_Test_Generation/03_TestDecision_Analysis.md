# Paper Analysis 03 (TestGen): TestDecision — Sequential Test Suite Generation via Greedy Optimization and RL

> **Sub-domain:** LLM Test Generation
> **Analysis করেছে:** SPL3 — AI Coding Agent Reliability and Assurance
> **Paper file:** `LLM Test Generation/From Greedy Steps to Global Optimization.pdf`
> **কেন এই sub-domain গুরুত্বপূর্ণ:** আমাদের প্রস্তাবিত "assurance report"-এ generated test হলো **dynamic signal** (CG1, CG3)। তাই এই analysis-এ বারবার প্রশ্ন করা হয়েছে: এই paper-এর test কি AI agent-এর patch যাচাইয়ে বিশ্বাসযোগ্য signal দিতে পারে?

---

## ০. Paper-এর পরিচয় (Bibliographic Info)

| বিষয় | তথ্য |
|---|---|
| **Title** | TestDecision: Sequential Test Suite Generation via Greedy Optimization and Reinforcement Learning |
| **PDF file-এর নাম** | From Greedy Steps to Global Optimization (file name; paper-এর ভেতরের title উপরেরটা) |
| **Authors** | Guoqing Wang (Peking University), Chengran Yang (Singapore Management University), Xiaoxuan Zhou (Northeastern University, China), Zeyu Sun (Institute of Software, CAS), Bo Wang (Beijing Jiaotong University), David Lo (SMU), Dan Hao (Peking University) |
| **Venue / Year** | **arXiv preprint** — arXiv:2604.01799v2 [cs.SE], 17 April 2026। Paper-এর ভেতরে কোনো conference বা journal-এর নাম নেই, "accepted" লেখাও নেই। Layout ACM journal template-এর মতো (running header "Wang et al.", authors' contact block) — **আমার পর্যবেক্ষণ:** এটা সম্ভবত journal submission, কিন্তু venue নিশ্চিত নয় |
| **Paper type** | **Technique paper** — নতুন theory (MDP + submodularity) + নতুন inference framework + RL training pipeline |
| **Artifacts** | Paper text-এ code বা data release-এর কোনো link আমি পাইনি (GitHub/Zenodo শব্দ খুঁজে দেখা হয়েছে) |
| **Language / Level** | Python, function-level unit test |
| **আমাদের domain-এ গুরুত্ব** | ⭐⭐⭐⭐ — generated test-এর "মান" কীভাবে বাড়ানো যায় তার একটা নীতিগত (theory-backed) পদ্ধতি দেয়; কিন্তু test oracle-এর শক্তি নিয়ে দুর্বলতা আছে, যা আমাদের assurance layer-এর জন্য খুবই প্রাসঙ্গিক (Section ১২–১৩) |

---

## ★ সহজ ভাষায় পুরো Paper (প্রথমবার পড়ার জন্য)

### ক. Paper-টা কী নিয়ে?
- এটা একটা **নতুন পদ্ধতির (technique) paper**। এটা কোনো survey বা benchmark নয়।
- লিখেছেন Peking University, SMU সহ কয়েকটা university-র গবেষকরা। এটা arXiv-এ (April 2026) প্রকাশিত preprint।
- বিষয়: AI (LLM) দিয়ে Python code-এর জন্য **unit test-এর পুরো সেট** (test suite) বানানো।
- মূল ধারণা: test একটা একটা করে লেখা হবে, আর প্রতিবার এমন test লেখা হবে যা আগের test-গুলো যা দেখেনি সেটাই দেখে।
- Paper এই ধারণার পক্ষে গাণিতিক যুক্তি দিয়েছে। তারপর একটা ছোট open model-কে সেই কাজ শেখিয়েছে।

### খ. সমস্যাটা কী ছিল?
- ধরো তুমি পরীক্ষার আগে ৫টা mock test দেবে। প্রথমে একই সহজ অধ্যায় থেকে ৫টা test দিলে কোনো লাভ নেই। দরকার এমন test, যা প্রতিবার নতুন অধ্যায় ছোঁয়।
- Test লেখার AI-রা ঠিক এই ভুলটা করত। তারা বারবার সহজ, চেনা path-ই test করত। কঠিন `if`-এর ভেতরের অংশে পৌঁছাতো না।
- আগের পদ্ধতিতে বলা হতো: "এই লাইনগুলো এখনো test হয়নি, এগুলো cover করো।" বড় দামি model (যেমন GPT-4o) এতে কাজ করত। কিন্তু ছোট open model এই সাহায্য কাজে লাগাতে পারত না।
- আরেকটা সমস্যা: এই পদ্ধতি শেষে ভালো ফল দেবে কিনা, তার কোনো গাণিতিক গ্যারান্টি ছিল না।
- **উদাহরণ:** Paper-এর Figure 1-এ তিনটা test (A, B, C) আছে। A আর B আগে থেকে থাকলে C কিছুই নতুন দেয় না। শুধু A থাকলে C কাজে লাগে। অর্থাৎ একটা test কতটা দামি, তা নির্ভর করে আগে কী কী আছে তার উপর।

### গ. Paper কী solve করেছে?
- Test suite বানানোকে একটা ধাপে-ধাপে সিদ্ধান্তের সমস্যা হিসেবে দেখিয়েছে (MDP)।
- প্রমাণ করেছে: coverage-এর মতো মাপে "নতুন লাভ" ক্রমে কমে (submodular)। তাই প্রতিবার সবচেয়ে বেশি নতুন লাইন cover করা greedy নিয়ম সেরা ফলের অন্তত প্রায় ৬৩.২% পায়।
- Code-এ `#uncovered` চিহ্ন বসিয়ে model-কে দেখানোর একটা সহজ কৌশল বানিয়েছে।
- ছোট 7B model-কে GRPO (এক ধরনের reinforcement learning) দিয়ে train করে নাম দিয়েছে TestDecision।
- সবচেয়ে গুরুত্বপূর্ণ তিনটা সংখ্যা (Qwen2.5-Coder-7B):
  - Line coverage ৫১.৪২% থেকে ৬৯.৬৯%। মানে ১০০টা লাইনের মধ্যে আগে প্রায় ৫১টা test হতো, এখন প্রায় ৭০টা।
  - Execution pass rate ১৬.৮৬% থেকে ৬৭.১৪%। মানে ১০০টা test-এর মধ্যে আগে মাত্র ১৭টা চলত, এখন ৬৭টা চলে।
  - নতুন ধরনের task-এ (LiveCodeBench) bug ধরা ২০.৫০% থেকে ৩২.৫০%। মানে ১০০টা buggy code-এর মধ্যে এখনো ৬৭টাই অধরা থেকে যায়।

### ঘ. কীভাবে solve করেছে?
1. **সমস্যাটাকে খেলার মতো সাজিয়েছে।** এক চাল = একটা test লেখা। চালের পর পুরস্কার = কত নতুন লাইন cover হলো।
2. **গণিতে প্রমাণ করেছে** যে এই খেলায় greedy নিয়ম যথেষ্ট ভালো। (Nemhauser-এর পুরনো theorem কাজে লাগিয়েছে।)
3. **State দেখানোর কৌশল বানিয়েছে।** Coverage.py চালিয়ে বাকি লাইনগুলো বের করে, code-এর ঠিক ওই লাইনের পাশে `#uncovered` comment বসায়। Model একনজরে দেখে কোথায় কাজ বাকি।
4. **Practice-এর প্রশ্ন বানিয়েছে।** GPT-5-mini দিয়ে একবার অনেক test বানিয়ে সেগুলো ধাপে ধাপে সাজিয়েছে। প্রতিটা ধাপ থেকে এক-একটা training state বানিয়েছে। মোট ৮,৩৯৬টা।
5. **Reward ঠিক করেছে।** নতুন লাইন যত বেশি, reward তত বেশি। কিন্তু test না চললে reward শূন্য।
6. **GRPO দিয়ে train করেছে।** একই state-এ model ৮টা test লেখে। যেগুলো গড়ের চেয়ে ভালো, সেগুলো লেখার সম্ভাবনা বাড়ানো হয়।
7. **Inference-এর সময়** খালি suite থেকে শুরু করে ৫ বার ঘোরে: coverage মাপো, চিহ্ন বসাও, model একটা test লেখে, suite-এ জমা।
8. **পরীক্ষা করেছে** ULT ও LiveCodeBench-এ, আর ablation দিয়ে দেখেছে কোন অংশ কতটা কাজ করছে।

### ঙ. এরপর কী করা যায়?
- **Authors-এর কথা:** শুধু Python আর function-level পরীক্ষা হয়েছে। বড় project, অন্য language, আর বাইরের environment (database, network) নিয়ে কাজ বাকি।
- **খোলা প্রশ্ন ১:** Reward-এ assertion কতটা শক্ত তা মাপা হয় না। তাই weak test-ও পুরো পুরস্কার পেতে পারে।
- **খোলা প্রশ্ন ২:** Theory ধরে নেয় LLM ঠিক সেরা test-টাই বাছে। বাস্তবে LLM মোটামুটি ভালো test বাছে। এই ফাঁক কতটা, তা কেউ মাপেনি।
- **SPL3-তে আমরা করতে পারি:** GPU লাগে এমন training বাদ দিয়ে শুধু `#uncovered` কৌশলটা নিয়ে tool বানানো।
- **SPL3-তে আমরা করতে পারি:** AI agent-এর patch যাচাইয়ের জন্য patch-এর বদলানো লাইনে চিহ্ন বসিয়ে test লেখানো, আর test পুরনো version-এ লিখে নতুন version-এ চালানো।
- **SPL3-তে আমরা করতে পারি:** Generated test-এর assertion কতটা শক্ত, তার audit করা (assertion গোনা, mutation score মাপা)।

> **মনে রাখো:**
> TestDecision = "প্রতিবার সবচেয়ে বেশি নতুন কিছু cover করো" নিয়মটা + ছোট model-কে RL দিয়ে শেখানো। ফলে কম test-এ বেশি coverage আর বেশি চলা test।
> কিন্তু reward-এ assertion-এর শক্তি নেই, আর test বর্তমান code-এর আচরণকেই "ঠিক" ধরে। তাই AI agent-এর patch যাচাইয়ে এটা একা যথেষ্ট নয়।

---

## ১. এক লাইনে Paper (TL;DR)

**Test suite তৈরি করাকে একটা sequential decision problem (MDP) হিসেবে দেখে, coverage-এর মতো utility function যে monotone submodular তা প্রমাণ করে, তারপর "প্রতি step-এ সবচেয়ে বেশি নতুন জিনিস cover করে এমন একটা test লেখো" — এই greedy নীতি ((1 − 1/e) ≈ 63.2% guarantee সহ) একটা ছোট open LLM-কে GRPO reinforcement learning দিয়ে শেখানো হয়েছে; ফলে Qwen2.5-Coder-7B-এর ULT benchmark-এ line coverage 51.42% থেকে 69.69% এবং execution pass rate 16.86% থেকে 67.14% হয়েছে।**

**সহজ কথায়:** একটা ছোট AI-কে শেখানো হয়েছে যেন প্রতিবার এমন test লেখে, যা আগের test-গুলো যা দেখেনি সেটাই দেখে। ফলে কম test-এ বেশি অংশ যাচাই হয়, আর test-গুলো আসলেই চলে।

### Supervisor-কে ৩০ সেকেন্ডে কীভাবে বলবো
> "Sir, LLM দিয়ে test লেখার এখনকার পদ্ধতি হলো একটা একটা করে test লেখা আর coverage report দেখিয়ে বলা 'বাকি অংশ cover করো'। এই paper দেখিয়েছে ছোট open model-রা এই feedback ঠিকমতো ব্যবহার করতে পারে না — একই জিনিস বারবার test করে, এটাকে তারা বলেছে structural myopia। তারা প্রমাণ করেছে coverage একটা submodular function, তাই প্রতি ধাপে সবচেয়ে বেশি নতুন line cover করা greedy পদ্ধতি optimal-এর অন্তত 63.2% পাবে। এরপর code-এর uncovered line-এ '#uncovered' marker বসিয়ে model-কে দেখানো হয়, আর GRPO দিয়ে train করা হয় যাতে model নতুন line cover করে এমন, আর চলে এমন test লেখে। 7B model-এ line coverage 51.42% থেকে 69.69%, যা GPT-5.2-এর 69.40%-এর সমান। তবে আমাদের কাজের জন্য সমস্যা হলো reward-এ assertion কতটা শক্ত তা মাপা হয় না — শুধু test চলল কিনা আর নতুন line cover হলো কিনা।"

---

## ২. Background — এই paper বুঝতে যা আগে জানা দরকার

### ২.১ Test case, Test suite, Assertion ও Test oracle
- **Test case (একটা test):** একটা ছোট function যেটা program-কে কোনো input দিয়ে চালায় আর output যাচাই করে। যেমন paper-এর Figure 1-এর `test_cpu_correction`।
- **Test suite:** অনেকগুলো test case-এর **সেট**। গুরুত্বপূর্ণ কথা: suite-এর মান তার সদস্যদের মানের যোগফল নয়। দুটো test যদি একই line cover করে, দ্বিতীয়টা নতুন কিছু যোগ করে না।
- **Assertion:** `assert data[0]['log'] == 8` — test-এর যে অংশ "সঠিক উত্তর কী" তা যাচাই করে।
- **Test oracle:** সঠিক আচরণ কী হওয়া উচিত তা যে ঠিক করে। Assertion হলো oracle-এর code রূপ। **Weak oracle** মানে assertion এত দুর্বল (যেমন শুধু "crash করেনি") যে ভুল আচরণও pass করে।

### ২.২ Code Coverage — Line ও Branch
- **Line coverage:** program-এর মোট executable line-এর কত শতাংশ test চালানোর সময় অন্তত একবার execute হয়েছে।
- **Branch coverage:** প্রতিটা `if`/`while`-এর দুই দিক (true ও false) কত শতাংশ execute হয়েছে। Branch coverage line coverage-এর চেয়ে কঠিন — একটা `if` line execute হলেও তার false দিক বাকি থাকতে পারে।
- **Coverage.py:** Python-এর standard coverage মাপার tool। Paper এটাকে wrap করে instrumentation tool বানিয়েছে।
- **সতর্কতা:** বেশি coverage মানেই বেশি bug ধরা নয় (paper নিজেও Inozemtseva ও Holmes, ICSE 2014 উদ্ধৃত করেছে)। Line execute হওয়া আর তার ফল যাচাই হওয়া এক জিনিস নয়।

### ২.৩ Mutation Testing ও Mutation Score
- **Mutant:** program-এ ইচ্ছা করে ছোট একটা bug ঢোকানো version — যেমন `>`-কে `>=` করা, `+`-কে `-` করা।
- **Killed mutant:** test suite-এর অন্তত একটা test mutant-এ fail করলে mutant "killed"। না হলে "survived"।
- **Mutation score:**

$$
MS = \frac{\text{killed mutant-এর সংখ্যা}}{\text{মোট mutant-এর সংখ্যা}} \times 100
$$

- **Equivalent mutant:** এমন mutant যার আচরণ মূল program-এর সমান (কোনো test-ই একে kill করতে পারবে না)। এগুলো denominator-এ থাকলে score কম দেখায়। Paper-এর threats section বলছে equivalent mutant score-কে underestimate করতে পারে — অর্থাৎ তারা এগুলো বাদ দেয়নি।
- **Cosmic-Ray:** Python-এর mutation testing tool, paper এটা ব্যবহার করেছে।
- **কেন গুরুত্বপূর্ণ:** Mutation score coverage-এর চেয়ে fault-detection ক্ষমতার ভালো proxy, কারণ mutant kill করতে হলে assertion-কে আসলেই ফল যাচাই করতে হয়। কিন্তু এটা ব্যয়বহুল — paper মেপেছে একবার mutation score বের করতে গড়ে **76.53 সেকেন্ড**।

### ২.৪ Syntactic Correctness ও Execution Pass Rate
- **Syntactic correctness:** generated test Python-এর `ast.parse` দিয়ে parse হয় কিনা।
- **Execution pass rate:** test `pytest`-এ runtime error ছাড়া চলে কিনা। গুরুত্বপূর্ণ: test যদি program-এর আসল output-এর সাথে না মেলা assertion লেখে, সেটাও fail — তাই এই metric অংশত "assertion ঠিক আছে কিনা" মাপে, **program under test-এর বর্তমান আচরণ সাপেক্ষে**।

### ২.৫ Search-Based Software Testing (SBST)
Genetic algorithm দিয়ে test suite "বিবর্তন" করানো — অনেক random test তৈরি, coverage দিয়ে fitness মাপা, ভালোগুলো রেখে mutate/crossover। **EvoSuite** (Java), **Pynguin** (Python) এর উদাহরণ। **CODAMOSA** (ICSE 2023) — SBST যখন coverage plateau-তে আটকে যায়, তখন LLM দিয়ে নতুন test input বানায়। সমস্যা: test-গুলো পড়তে কঠিন।

### ২.৬ LLM-ভিত্তিক Test Generation-এর তিনটা ধরন (paper-এর pilot study-তে)
1. **Direct generation:** একবারের call-এ পুরো suite ($K$টা test) লেখা।
2. **Iterative (Blind):** একটা একটা করে test, আগের test-গুলো context-এ থাকে, কিন্তু কোনো execution feedback নেই।
3. **Iterative (Guided):** প্রতি step-এর পর coverage feedback দিয়ে বলা হয় "এই uncovered line/branch-গুলো cover করো" — ChatTester, SymPrompt, CoverUp এই ধারার।

### ২.৭ Sequential Decision Making ও Markov Decision Process (MDP)
**Sequential decision making:** একটার পর একটা সিদ্ধান্ত, যেখানে প্রতিটা সিদ্ধান্তের মূল্য আগের সিদ্ধান্তগুলোর উপর নির্ভর করে। দাবা খেলার মতো — একই চাল এক অবস্থায় ভালো, অন্য অবস্থায় খারাপ।

**MDP** হলো এর গাণিতিক রূপ, একটা tuple $(S, A, T, R, \gamma)$:
- $S$ = **state** — এখন কী অবস্থা (এখানে: কোন line/branch ইতিমধ্যে cover হয়েছে)।
- $A$ = **action** — কী করা যায় (এখানে: একটা নতুন test লেখা)।
- $T$ = **transition** — action-এর পর নতুন state কী হবে (এখানে deterministic: suite-এ test যোগ হয়)।
- $R$ = **reward** — action কতটা ভালো ছিল (এখানে: কত নতুন line cover হলো)।
- $\gamma$ = **discount factor** — ভবিষ্যতের reward-কে কত গুরুত্ব দেওয়া হবে (0 থেকে 1)।
- **Markov property:** ভবিষ্যৎ শুধু বর্তমান state-এর উপর নির্ভর করে, কীভাবে এখানে এলাম তার উপর নয়।
- **Policy** $\pi(a \mid s)$: state দেখে কোন action নেবো তার নিয়ম। এখানে LLM নিজেই policy।
- **Finite horizon:** নির্দিষ্ট $K$ step পর শেষ (এখানে $K = 5$টা test)।

**সহজ কথায়:** MDP মানে একটা খেলার নিয়মের তালিকা: এখন কোথায় আছি (state), কী করতে পারি (action), করলে কী বদলায় (transition), কত নম্বর পাই (reward)। এখানে খেলাটা হলো একটার পর একটা test লেখা।

### ২.৮ Set Function, Marginal Gain, Monotone ও Submodular
- **Set function** $F(S)$: একটা সেট নিয়ে একটা সংখ্যা দেয়। যেমন $F(\text{suite})$ = suite কতগুলো line cover করে।
- **Marginal gain:** $F(S \cup \{x\}) - F(S)$ — $S$-এ $x$ যোগ করলে কতটা বাড়ে।
- **Monotone:** কিছু যোগ করলে $F$ কখনো কমে না। Test যোগ করলে coverage কমে না।
- **Submodular (diminishing returns — "কমতে থাকা লাভ"):** ছোট সেটে কিছু যোগ করার লাভ ≥ বড় সেটে একই জিনিস যোগ করার লাভ। যদি $A \subseteq B$:

$$
F(A \cup \{x\}) - F(A) \geq F(B \cup \{x\}) - F(B)
$$

**সহজ উদাহরণ:** প্রথম ভাত-এর প্লেট খুব তৃপ্তি দেয়, তৃতীয় প্লেট অনেক কম। Suite-এ ইতিমধ্যে অনেক test থাকলে নতুন test-এর নতুন কিছু cover করার সুযোগ কম।

**সহজ কথায়:** Submodular মানে নতুন কিছু যোগ করলে লাভ ক্রমে কমতে থাকে। ইতিমধ্যে অনেক test থাকলে আরেকটা test প্রায় নতুন কিছু দেখায় না।

### ২.৯ Maximum Coverage Problem ও NP-hardness
অনেকগুলো সেট থেকে $K$টা বেছে নিতে হবে যাতে তাদের union সবচেয়ে বড় হয়। এটা **NP-hard** — অর্থাৎ বড় input-এ সঠিক optimal উত্তর বের করার কোনো জানা দ্রুত (polynomial-time) algorithm নেই। Test suite selection ঠিক এই সমস্যা: candidate test-গুলো থেকে $K$টা বাছাই যাতে মোট coverage সর্বোচ্চ।

### ২.১০ Greedy Algorithm ও Nemhauser-এর $(1 - 1/e)$ Guarantee
- **Greedy:** প্রতি ধাপে শুধু এখনকার জন্য সবচেয়ে ভালো জিনিসটা বেছে নাও — ভবিষ্যৎ নিয়ে চিন্তা না করে।
- **Nemhauser, Wolsey ও Fisher (1978):** $F$ monotone submodular হলে এবং $|S| \leq K$ constraint থাকলে, greedy-র ফল optimal-এর অন্তত $(1 - 1/e) \approx 63.2\%$। $e \approx 2.718$।
- **মানে:** NP-hard সমস্যাকেও একটা সহজ greedy নিয়ম দিয়ে "যথেষ্ট ভালো" ভাবে সমাধান করা যায়, আর কতটা খারাপ হতে পারে তার একটা গাণিতিক সীমা আছে। এই paper-এর পুরো theory এর উপর দাঁড়িয়ে।

**সহজ কথায়:** প্রতিবার সামনের সবচেয়ে ভালো জিনিসটা তুলে নিলেও শেষ ফল সেরা ফলের অন্তত প্রায় দুই-তৃতীয়াংশ হয়। এটা গণিতে প্রমাণ করা আছে।

### ২.১১ Reinforcement Learning (RL) দিয়ে LLM Training
- **SFT (Supervised Fine-Tuning):** model-কে একটা নির্দিষ্ট "সঠিক উত্তর" নকল করতে শেখানো (cross-entropy loss)।
- **RL:** model নিজে উত্তর তৈরি করে, environment (এখানে: test চালানো) একটা reward দেয়, ভালো reward-এর উত্তরের probability বাড়ানো হয়।
- **RLVR (RL with Verifiable Rewards):** reward আসে স্বয়ংক্রিয় যাচাই থেকে (test pass, coverage) — মানুষের রেটিং নয়।
- **Paper-এর যুক্তি কেন SFT যথেষ্ট নয়:** অনেকগুলো valid test থাকলে SFT বলতে পারে না কোনটা বেশি **নতুন** coverage দেয়; RL পারে কারণ reward সরাসরি marginal gain মাপে।

### ২.১২ PPO ও GRPO — RL algorithm
**PPO (Proximal Policy Optimization, Schulman et al. 2017)** — baseline TestCTRL এটা ব্যবহার করে:

$$
L^{\text{CLIP}}(\theta) = \mathbb{E}_t\left[\min\left(\rho_t(\theta)\,\hat{A}_t,\; \text{clip}(\rho_t(\theta),\, 1-\epsilon,\, 1+\epsilon)\,\hat{A}_t\right)\right], \qquad \rho_t(\theta) = \frac{\pi_\theta(a_t \mid s_t)}{\pi_{\theta_{\text{old}}}(a_t \mid s_t)}
$$

- $\hat{A}_t$ = advantage (action গড়ের চেয়ে কতটা ভালো), PPO-তে এটা একটা আলাদা **value network (critic)** দিয়ে estimate হয় — অর্থাৎ policy-র পাশাপাশি আরেকটা বড় model train করতে হয় (memory ও compute বেশি)।
- clip অংশ একবারে policy খুব বেশি বদলানো আটকায়।

**সহজ কথায়:** PPO-তে একটা আলাদা 'শিক্ষক model' (critic) লাগে, যে বলে চালটা কেমন ছিল। এটা বাড়তি খরচ।

**GRPO (Group Relative Policy Optimization, Shao et al. 2024, DeepSeekMath)** — TestDecision এটা ব্যবহার করে:
- একই state-এ $G$টা উত্তর sample করো, প্রত্যেকটার reward বের করো।
- Advantage = নিজের reward − group-এর গড় reward (মূল GRPO-তে standard deviation দিয়ে ভাগও করা হয়)।
- **Critic লাগে না** — group-এর গড়ই baseline। তাই সস্তা।

**সহজ কথায়:** GRPO-তে আলাদা শিক্ষক লাগে না। একই প্রশ্নের ৮টা উত্তর লিখে নিজেদের মধ্যে তুলনা করা হয়: গড়ের চেয়ে ভালো হলে পুরস্কার, খারাপ হলে শাস্তি।

### ২.১৩ KL Divergence Regularization
দুটো probability distribution কতটা আলাদা তার মাপ:

$$
D_{\text{KL}}(P, Q) = \sum_{x} P(x) \log \frac{P(x)}{Q(x)}
$$

RL training-এ policy $\pi_\theta$ যেন মূল base model $\pi_{\text{base}}$ থেকে খুব বেশি সরে না যায় (ভাষা নষ্ট না হয়, reward hack না করে), তাই loss-এ $\beta \cdot D_{\text{KL}}$ যোগ করা হয়। Paper-এ $\beta = 0.001$।

**সহজ কথায়:** KL হলো একটা লাগাম। Model শিখতে গিয়ে যেন মূল model থেকে একদম অন্যরকম হয়ে না যায়।

### ২.১৪ Abstract Syntax Tree (AST) ও AST Injection
- **AST:** source code-এর tree রূপ — প্রতিটা statement, expression একটা node।
- **AST injection (paper-এর কৌশল):** code parse করে uncovered line-এর node-এ `#uncovered` comment বসানো, তারপর আবার source code-এ রূপান্তর। Comment হওয়ায় program-এর আচরণ বদলায় না, কিন্তু LLM সহজে দেখতে পায় কোথায় test দরকার।

### ২.১৫ Data Leakage, ULT ও LiveCodeBench
- **Data leakage / contamination:** benchmark-এর test আগেই model-এর training data-তে থাকলে model "মুখস্থ" লিখতে পারে।
- **ULT (Huang et al., 2025):** The Stack v2 থেকে নেওয়া আসল Python function-এর **3,909**টা function-level unit test generation task, যেগুলোর কোনো test public নয় (leak এড়াতে)।
- **LiveCodeBench (LCB):** competitive programming ধরনের task, নিয়মিত নতুন task যোগ হয়। Paper শুধু **June 2024-এর পরের** task নিয়েছে (সব base model-এর training cutoff-এর পরে)। প্রতিটা task-এ canonical (সঠিক) solution আর buggy solution আছে — তাই আসল bug detection মাপা যায়।
- **Out-of-distribution (OOD):** training data থেকে আলাদা ধরনের data — generalization-এর পরীক্ষা।

### ২.১৬ Wilcoxon Signed-Rank Test
দুটো পদ্ধতিকে একই task-গুলোতে জোড়ায় জোড়ায় তুলনা করার non-parametric statistical test (data normal distribution ধরে নেয় না)। $p < 0.01$ মানে পার্থক্য এলোমেলো হওয়ার সম্ভাবনা 1%-এর কম।

### ২.১৭ Relative Improvement বনাম Percentage Point
Paper বেশিরভাগ জায়গায় **relative improvement** বলে:

$$
\text{Relative Improvement} = \frac{\text{নতুন} - \text{পুরনো}}{\text{পুরনো}} \times 100\%
$$

**উদাহরণ:** execution 16.86% থেকে 67.14% — percentage point-এ +50.28 pp, কিন্তু relative-এ $\frac{67.14 - 16.86}{16.86} \times 100 = 298.22\%$। ছোট base থেকে relative সংখ্যা অনেক বড় দেখায় — supervisor-কে বলার সময় দুটোই বলা উচিত।

**সহজ কথায়:** ১০ থেকে ২০ হলে বলা যায় 'দ্বিগুণ' (১০০% বৃদ্ধি), কিন্তু আসলে মাত্র ১০ পয়েন্ট বেড়েছে। তাই ছোট সংখ্যা থেকে শুরু করলে শতাংশ অনেক বড় দেখায়।

### ২.১৮ Structural Myopia (paper-এর নিজস্ব শব্দ)
"Myopia" মানে দূরের জিনিস দেখতে না পাওয়া। Paper-এর অর্থে: LLM test suite-এর সামগ্রিক অবস্থা না দেখে বারবার সহজ, ইতিমধ্যে cover হওয়া path (happy path) test করে; coverage feedback দিলেও কঠিন, nested branch-এ পৌঁছায় না।

**সহজ কথায়:** ছাত্র যেমন কঠিন প্রশ্ন এড়িয়ে শুধু সহজ প্রশ্নই বারবার সমাধান করে, model-ও তেমনি সহজ path-ই বারবার test করে।

---

## ৩. Problem Statement — কী সমস্যা ছিল?

### ৩.১ মূল সমস্যা
1. **Iterative LLM test generation-এর কোনো তাত্ত্বিক ভিত্তি নেই:** "আগের test দেখে পরের test লেখো" — এই পদ্ধতি শেষে optimal-এর কাছাকাছি suite দেবে কিনা, তার কোনো প্রমাণ ছিল না।
2. **Test-এর মূল্য অবস্থা-নির্ভর:** Figure 1-এ Test C (`test_full_flow`) suite-এ $\{A, B\}$ থাকলে marginal gain 0, কিন্তু শুধু $\{A\}$ থাকলে positive। তাই এটা একটা sequential decision problem।
3. **Proprietary model-নির্ভরতা:** সফল feedback-driven পদ্ধতি (CoverUp, Panta ইত্যাদি) বড় proprietary model (যেমন GPT-4o)-এর উপর নির্ভর করে — খরচ বেশি, data privacy সমস্যা, local-এ retrain করা যায় না।
4. **ছোট open model feedback কাজে লাগাতে পারে না (structural myopia):** pilot study-তে (Table 1) Guided ও Blind iteration প্রায় সমান; কখনো guided খারাপ।

**সহজ কথায়:** আগের পদ্ধতিতে কোনো গ্যারান্টি ছিল না, দামি closed model লাগত, আর ছোট model feedback পেয়েও একই ভুল করত।

### ৩.২ কেন এটা গুরুত্বপূর্ণ?
- Test suite-এর মান সরাসরি bug ধরার ক্ষমতা ঠিক করে।
- **আমাদের lens থেকে:** AI agent-এর patch যাচাইয়ে developer-এর test দুর্বল হলে (SWE-bench analysis-এর CG1) বাড়তি generated test লাগে। সেই generated test যদি একই জিনিস বারবার test করে, assurance signal দুর্বল হবে। তাই "suite-level" চিন্তা আমাদের জন্যও দরকারি।

---

## ৪. Goal ও Research Questions

**Goal:** ছোট open LLM-কে "neural greedy expert" বানানো — যাতে প্রতি step-এ বর্তমান suite-এর অবস্থা দেখে সবচেয়ে বেশি marginal gain-এর test লেখে, আর theory দিয়ে সেই পদ্ধতির guarantee দেওয়া।

Paper-এর explicit RQ:
- **RQ1 (Effectiveness):** Base model, advanced prompting (ChatTester, SymPrompt) ও learning-based (TestCTRL)-এর চেয়ে TestDecision কি ভালো suite বানায়?
- **RQ2 (Optimization in Sequence):** কম test দিয়ে বেশি coverage (steeper growth) পায় কিনা, আর backbone logic আগে test করে কিনা?
- **RQ3 (Generalization ও Bug Detection):** অদেখা task-এ (LiveCodeBench) কাজ করে কিনা, আর coverage বাড়লে আসল bug ধরা বাড়ে কিনা?
- **RQ4 (Ablation):** প্রতিটা component-এর অবদান কত?

**সহজ কথায়:** চারটা প্রশ্ন: ভালো কি, কম test-এ ভালো কি, অচেনা task-এ ভালো কি, আর কোন অংশ কতটা কাজ করছে।

এছাড়া Discussion-এ (Section 7): proprietary model (GPT-4o, GPT-5.2), model size (3B/7B/14B) ও SBST (CODAMOSA)-এর সাথে তুলনা।

---

## ৫. Methodology — কীভাবে কাজটা করা হয়েছে

### ৫.১ Pilot Study (Section 2.2) — সমস্যার প্রমাণ
- **Models:** Qwen2.5-Coder-7B, CodeLlama-7B, Llama-3.1-8B।
- **Benchmark:** ULT (3,909 task)।
- **তিন paradigm:** Direct, Iter-Blind, Iter-Guided (Section ২.৬)।
- **Budget:** $K = 5$ test (ULT ও আগের benchmark-এর standard setting)।
- **Metric:** line coverage, branch coverage, mutation score, syntax correctness, execution correctness।
- **ফল:** Table 1 (Section ৮.১) — guided feedback কোনো ধারাবাহিক উন্নতি দেয় না।

**সহজ কথায়:** আগে দেখানো হলো সমস্যাটা সত্যিই আছে: coverage feedback দিয়েও ছোট model-এর উন্নতি হয় না।

### ৫.২ Theory (Section 3) — MDP ও Relaxation
1. Test suite generation-কে finite-horizon MDP হিসেবে লেখা (Definition 1)।
2. Assumption 1: determinism ও permutation invariance।
3. Global objective (Eq. 1) NP-hard — Maximum Coverage Problem-এর সমতুল্য (Remark 1)।
4. Utility monotone submodular — প্রমাণ (Eq. 2–3)।
5. তাই greedy policy optimal-এর অন্তত $(1 - 1/e)$ পায় (Theorem 1)।
বিস্তারিত সূত্র Section ৬-এ।

**সহজ কথায়:** আগে প্রমাণ করা হলো কাজটা কঠিন, কিন্তু একটা সহজ নিয়মে (greedy) মোটামুটি ভালো সমাধান পাওয়া যায়।

### ৫.৩ Instantiation (Section 4.1)
| ধারণা | Test generation-এ অর্থ |
|---|---|
| Step | একটা test case তৈরি — একটা atomic decision |
| Testing state | বর্তমান suite চালিয়ে program-এর কোন অংশ checked, কোনটা unchecked |
| Marginal gain | নতুন test suite-এ কতটা অতিরিক্ত checked value যোগ করে (Section 4.3.3-এ সংজ্ঞা) |

**সহজ কথায়:** এক ধাপ = একটা test লেখা। State = এখন পর্যন্ত কোন অংশ যাচাই হয়েছে। Gain = নতুন test কতটা নতুন অংশ যাচাই করল।

### ৫.৪ Inference Procedure (Section 4.2, Figure 3)
শুরু খালি suite $S_0 = \{\}$ দিয়ে, $K$টা step:
1. **State Summarization (Perception):** বর্তমান suite $S_{t-1}$ চালিয়ে Coverage.py দিয়ে uncovered line number-এর সেট বের করা। তারপর **AST injection** — code parse করে প্রতিটা uncovered node-এ trailing comment `#uncovered` বসানো, তারপর আবার source code বানানো। এতে raw coverage report-এর বদলে একটা ছোট, code-এর সাথে মেলানো state summary পাওয়া যায় ("in-context coverage projection")।
2. **Greedy Action:** LLM-কে stochastic policy $\pi_\theta(a \mid s_t)$ হিসেবে ব্যবহার করে একটা পূর্ণ test case $a_t$ তৈরি — prompt-এ নির্দেশ থাকে uncovered অংশ cover করতে আর সংশ্লিষ্ট আচরণ assert করতে।
3. **Update:** $S_t = S_{t-1} \cup \{a_t\}$, আবার execute করে পরের state।

**সহজ কথায়:** দেখো কোন লাইন এখনো test হয়নি, code-এ সেগুলোতে চিহ্ন দিয়ে model-কে দেখাও, model একটা test লেখে, সেটা suite-এ জমা হয়। এভাবে ৫ বার।

**আমার পুনর্গঠন (pseudocode, paper-এ এভাবে দেওয়া নেই):**
```python
suite = []
for t in range(1, K + 1):              # K = 5
    uncovered = run_coverage(program, suite)        # Coverage.py
    marked_code = ast_inject(program, uncovered, "#uncovered")
    test = llm.generate(prompt(marked_code, suite))  # one complete test
    suite.append(test)                 # S_t = S_{t-1} U {a_t}
return suite
```

**সহজ কথায়:** উপরের code-এ খালি তালিকা দিয়ে শুরু, ৫ বার ঘুরে প্রতিবার uncovered লাইন বের করে চিহ্ন বসানো code দেখিয়ে একটা করে test জমা হয়।

### ৫.৫ Policy Training (Section 4.3)
**৫.৫.১ Training objective:** "ভালো test লেখা" নয়, বরং **একটা decision policy শেখা** — বর্তমান state-এ কোন test লিখলে marginal gain সবচেয়ে বেশি।

**৫.৫.২ কেন RL, SFT নয়:** SFT একটা নির্দিষ্ট target test নকল করতে শেখায়; একাধিক valid test-এর মধ্যে কোনটা বেশি নতুন coverage দেয়, সেই signal দেয় না।

**৫.৫.৩ Reward design:**
- **Coverage gain:** line coverage proxy — বাকি uncovered line-এর কত অংশ নতুন test cover করলো (normalized, 0 থেকে 1)।
- **Mutation কেন নয়:** online training-এ খুব ধীর — গড়ে **76.53 সেকেন্ড** প্রতি mutation score।
- **Validity gate:** test compile/execute না হলে reward **0** — coverage যতই হোক।
- চূড়ান্ত reward = coverage gain × validity indicator (Eq. 5)।

**সহজ কথায়:** পুরস্কার = নতুন লাইন কতটা cover হলো। কিন্তু test যদি চলেই না, তাহলে পুরস্কার শূন্য।

**৫.৫.৪ GRPO training:** একই state-এ $G = 8$টা candidate test sample, প্রত্যেকটা execute করে reward, group-গড় থেকে advantage, KL-regularized objective (Eq. 6–7)।

### ৫.৬ Training Data Construction (Section 4.4)
RL-এর জন্য দরকার **বাস্তব, পৌঁছানো যায় এমন intermediate state** — যেখান থেকে policy explore করবে। (এগুলো SFT target নয়, শুধু starting state।)
1. **Candidate sampling:** ULT-এর **70%** task random বেছে (আমার হিসাব: $3909 \times 0.7 \approx 2{,}736$ task), প্রতিটা function-এর জন্য **GPT-5-mini** দিয়ে Huang et al.-এর prompting pipeline মেনে **$N = 20$**টা স্বাধীন test। GPT-5-mini শুধু একবার pool ভরাতে ব্যবহৃত; RL তার logits বা preference ব্যবহার করে না।
2. **Greedy ordering:** pool থেকে বারবার সবচেয়ে বেশি marginal gain-এর test বেছে একটা ক্রম বানানো।
3. **State replay:** সাজানো ক্রম ধাপে ধাপে চালিয়ে প্রতিটা step-এর exact coverage রেকর্ড — যাতে প্রতিটা state বাস্তব (random masking বা static estimate-এর মতো অসম্ভব state নয়)।
4. **Filtering:** শুধু সেই task রাখা যার চূড়ান্ত suite **> 90% line coverage** পায়।
5. **Decomposition:** দৈর্ঘ্য $K$-এর প্রতিটা trajectory থেকে $K$টা আলাদা state $s_0, \ldots, s_{K-1}$।
6. **মোট training data: 8,396 piece।**

**সহজ কথায়:** GPT-5-mini দিয়ে একবার অনেক test বানিয়ে ভালো ক্রমে সাজানো হয়েছে। সেই ক্রমের প্রতিটা ধাপ এক-একটা অনুশীলনের প্রশ্ন (state)। মোট ৮,৩৯৬টা।

### ৫.৭ Implementation Details (Section 5.5)
| Setting | মান |
|---|---|
| Base models | Qwen2.5-Coder-7B, Llama-3.1-8B, CodeLlama-7B (Discussion-এ Qwen2.5 3B ও 14B) |
| Hardware | 8 × NVIDIA A100 80GB |
| Framework | Verl (HybridFlow) |
| Hyperparameter বাছাই | Verl-এর নির্দেশনা মেনে ছোট grid search |
| Group size $G$ | 8 |
| Optimizer | AdamW |
| Learning rate | 1e-6, cosine decay |
| KL coefficient $\beta$ | 0.001 |
| Execution sandbox | Container, কঠোর resource limit, **3s timeout** |
| Test budget $K$ | 5 |
| Repetition | 3টা ভিন্ন seed, গড় report |
| Significance | Wilcoxon signed-rank, $p < 0.01$ |
| **Paper-এ নেই** | Epoch/step সংখ্যা, batch size, max generation length, sampling temperature, মোট GPU-ঘণ্টা, inference token/খরচ, GPT-4o/GPT-5.2 কোন pipeline-এ চালানো হয়েছে |

**সহজ কথায়:** ৮টা A100 GPU দিয়ে train হয়েছে, যা আমাদের মতো ছাত্রের পক্ষে করা কঠিন। আর epoch, খরচ ইত্যাদি অনেক তথ্য paper-এ নেই।

---

## ৬. Mathematical Formulation — সূত্র ও ব্যাখ্যা

### ৬.১ Test Generation MDP (Definition 1)

$$
\mathcal{M} = (S,\; A,\; T,\; R,\; \gamma)
$$

**এই সূত্র কী বলছে:** এটা খেলার পাঁচটা অংশের তালিকা মাত্র: অবস্থা, কাজ, পরিবর্তন, পুরস্কার, আর ভবিষ্যতের গুরুত্ব।

- **State** $s_t \in S$: static program semantics $C$ + এ পর্যন্ত জমা suite $S_{t-1}$-এর checked status। Formally $s_t$ = এ পর্যন্ত যাচাই হওয়া logical unit-এর সেট (line, branch বা latent bug)।
- **Action** $a_t \in A$: সব সম্ভাব্য valid test-এর universe $U$ থেকে একটা নতুন valid test তৈরি — একটা atomic action।
- **Transition** $T$ (deterministic):

$$
S_t = S_{t-1} \cup \{a_t\}
$$

এবং state $s_{t+1}$ নতুন checked status দেখায়।
- **লক্ষ্য করার বিষয় (আমার পর্যবেক্ষণ):** tuple-এ $\gamma$ (discount) আছে, কিন্তু paper-এর কোথাও $\gamma$-এর মান বা ব্যবহার নেই — কারণ greedy relaxation-এর পর প্রতি step-এর reward আলাদাভাবে optimize হয় (কার্যত $\gamma$-এর কোনো ভূমিকা থাকে না)।

### ৬.২ Assumption 1 — Determinism ও Permutation Invariance
Utility function:

$$
F : 2^{U} \to \mathbb{R}_{\geq 0}
$$

**এই সূত্র কী বলছে:** $F$ হলো একটা নম্বর দেওয়ার যন্ত্র। যেকোনো test-এর সেট দিলে সে একটা অঋণাত্মক নম্বর (যেমন coverage) বলে দেয়।

($2^{U}$ = $U$-এর সব subset-এর সেট; $F$ প্রতিটা suite-কে একটা অঋণাত্মক সংখ্যা দেয় — coverage, mutation score ইত্যাদি।)
1. **Determinism:** যেকোনো test $a \in U$-এর execution ফল ও utility নির্দিষ্ট ও সময়-নিরপেক্ষ।
2. **Permutation invariance:** utility শুধু test-এর সেটের উপর নির্ভর করে, ক্রমের উপর নয়:

$$
F([a_1, \ldots, a_K]) = F(\{a_1, \ldots, a_K\})
$$

**এই সূত্র কী বলছে:** Test-গুলো কোন ক্রমে লেখা হলো তাতে কিছু আসে-যায় না। শুধু কোন কোন test আছে সেটাই ধরা হয়।

**আমার পর্যবেক্ষণ:** বাস্তবে flaky test (সময়, random, network-নির্ভর) আর test-এর মধ্যে shared state (একটা test global variable বদলালে পরেরটার আচরণ বদলায়) এই দুটো assumption ভাঙে। Paper 3s timeout ও sandbox দিয়ে কিছুটা নিয়ন্ত্রণ করে, কিন্তু assumption ভাঙার হার মাপেনি।

### ৬.৩ Global Objective (Eq. 1)

$$
\pi^{\star} = \arg\max_{\pi} F(S_K), \quad \text{যেখানে } |S_K| \leq K
$$

**এই সূত্র কী বলছে:** এমন policy বেছে নাও, যার $K$টা test-এর suite সবচেয়ে বেশি নম্বর পায়।

- $\pi^{\star}$ = optimal policy, $S_K$ = $K$ step পরের suite, $K$ = test budget।
- **মানে:** এমন policy খোঁজো যার $K$টা test-এর suite-এর utility সর্বোচ্চ।

### ৬.৪ Hardness (Remark 1)
$U$ কার্যত অসীম। একটা বড় কিন্তু সসীম $U_{\text{finite}} \subset U$ নিলেও, $K$টা test বেছে $F(S)$ সর্বোচ্চ করা **Maximum Coverage Problem**-এর সমতুল্য — NP-hard।

### ৬.৫ Theorem 1 — Approximation Guarantee
Greedy policy প্রতি step-এ:

$$
a_t = \arg\max_{a \in U} \left( F(S_{t-1} \cup \{a\}) - F(S_{t-1}) \right)
$$

তাহলে Assumption 1-এর অধীনে:

$$
F(S_K^{\text{greedy}}) \geq \left(1 - \frac{1}{e}\right) F(S_K^{\star}) \approx 0.632 \cdot F(S_K^{\star})
$$

**এই সূত্র কী বলছে:** প্রতিবার সবচেয়ে বেশি নতুন লাভ দেয় এমন test নিলে শেষ নম্বর সেরা সম্ভাব্য নম্বরের অন্তত ৬৩.২% হবে।

**Proof Step 1 — Monotone submodularity:** $E$ = যাচাই করার সব structural element-এর universe (line/branch)। প্রতিটা test $t$-এর জন্য $\text{Check}(t) \subseteq E$ = $t$ যে element-গুলো cover করে। Utility:

$$
F(S) = | \cup_{t \in S} \text{Check}(t) |
$$

**এই সূত্র কী বলছে:** Suite-এর নম্বর = সব test মিলে মোট কয়টা আলাদা লাইন বা branch cover হলো (union-এর আকার)।

দুটো suite $A \subseteq B \subseteq U$ আর নতুন test $x \in U$, $x \notin B$। যেহেতু $A \subseteq B$, $A$-এর covered element $B$-এর covered element-এর subset। তাই $x$-এর যে element $B$-এর কাছে নতুন, তা $A$-এর কাছেও নতুন (Eq. 2):

$$
\text{Check}(x) - \cup_{t \in B} \text{Check}(t) \;\subseteq\; \text{Check}(x) - \cup_{t \in A} \text{Check}(t)
$$

**এই সূত্র কী বলছে:** বড় suite-এর কাছে যা নতুন, তা ছোট suite-এর কাছেও নতুন। কারণ ছোট suite কম জিনিস দেখেছে।

(এখানে "−" মানে set difference — বাম সেট থেকে ডান সেটের element বাদ।) দুই দিকের cardinality নিলে submodularity (Eq. 3):

$$
F(B \cup \{x\}) - F(B) \leq F(A \cup \{x\}) - F(A)
$$

**এই সূত্র কী বলছে:** ছোট suite-এ test যোগ করার লাভ, বড় suite-এ যোগ করার লাভের চেয়ে কম নয়।

আর test যোগ করলে coverage কখনো কমে না, তাই $F$ monotone।

**Proof Step 2 — Bound:** $|S| \leq K$ cardinality constraint-এ monotone submodular function maximize করা — Nemhauser et al. (1978)-এর theorem সরাসরি $(1 - 1/e)$ দেয়।

**Worked example ১ — Figure 1-এর function দিয়ে (আমার হিসাব):** `correct_sc_info`-এর loop body-র ৫টা executable line ধরি (def line বাদ, সরলীকরণ):
- $l_1$: `for sc in sc_info`
- $l_2$: `if sc['phy'] > 4 and sc['log']==0`
- $l_3$: `sc['log'] = sc['phy']`
- $l_4$: `if 'bench' not in sc`
- $l_5$: `sc['bench'] = sc['phy'] * 100`

Paper-এর তিনটা test-এর data দেখে:
- Test A (`phy 8, log 0, bench 800`): $l_2$ true → $l_3$ চলে; bench আছে তাই $l_5$ চলে না। $\text{Check}(A) = \{l_1, l_2, l_3, l_4\}$।
- Test B (`phy 4, log 4`, bench নেই): $l_2$ false; $l_5$ চলে। $\text{Check}(B) = \{l_1, l_2, l_4, l_5\}$।
- Test C (`phy 8, log 0`, bench নেই): $\text{Check}(C) = \{l_1, \ldots, l_5\}$।

Submodularity দেখা যাক, $x = C$:
- $F(\{A\}) = 4$, $F(\{A, C\}) = 5$ → gain = 1।
- $F(\{A, B\}) = 5$, $F(\{A, B, C\}) = 5$ → gain = 0।
- $\{A\} \subseteq \{A, B\}$ এবং $1 \geq 0$ — ঠিক paper-এর Scenario 1 ও 2।

Greedy খালি suite থেকে শুরু করলে প্রথমেই C বেছে নেবে (gain 5, A ও B-এর 4) এবং এক test-এই 5/5 line। অর্থাৎ greedy "সবচেয়ে বেশি backbone cover করা" test আগে লেখে — RQ2-এ paper ঠিক এই আচরণ দাবি করেছে (Section ৮.৩)।

**সহজ কথায়:** এই ছোট উদাহরণে দেখা গেল: A ও B আগে থেকে থাকলে C কিছুই নতুন দেয় না, কিন্তু শুধু A থাকলে C একটা লাইন যোগ করে। এটাই diminishing returns।

**Worked example ২ — bound-এর সংখ্যা (আমার হিসাব):** ধরি কোনো function-এর optimal 5-test suite 100টা line cover করে। Theorem 1 অনুযায়ী exact greedy অন্তত $100 \times 0.632 \approx 63.2$টা line cover করবে। আসলে Nemhauser-এর মূল ফল finite $K$-এর জন্য আরও শক্ত:

$$
F(S_K^{\text{greedy}}) \geq \left(1 - \left(1 - \frac{1}{K}\right)^{K}\right) F(S_K^{\star})
$$

**এই সূত্র কী বলছে:** $K$ ছোট হলে গ্যারান্টি একটু বেশি পাওয়া যায়। ৫টা test-এ সেটা ৬৭.২%।

$K = 5$ হলে $1 - 0.8^{5} = 1 - 0.32768 = 0.672$ — অর্থাৎ 67.2%। $K \to \infty$ হলে এটা $1 - 1/e$-তে নামে। (Paper শুধু অসীম-সীমার 63.2% বলেছে।)

### ৬.৬ Theory-র একটা গুরুত্বপূর্ণ সীমা — Approximate Greedy (আমার পর্যবেক্ষণ, paper-এ নেই)
Theorem 1 ধরে নেয় প্রতি step-এ **পুরো** $U$-এর মধ্যে **ঠিক** সর্বোচ্চ marginal gain-এর test বাছা হয়। LLM তা করে না — সে একটা test sample করে, যেটা best-এর কাছাকাছি হতে পারে বা না-ও পারে। Submodular optimization-এর পরিচিত ফল হলো: যদি প্রতি step-এ বাছা test সর্বোচ্চ সম্ভাব্য marginal gain-এর অন্তত $\alpha$ অংশ দেয় ($0 < \alpha \leq 1$), তাহলে guarantee হয়

$$
F(S_K) \geq \left(1 - e^{-\alpha}\right) F(S_K^{\star})
$$

**এই সূত্র কী বলছে:** LLM যদি সেরা test-এর লাভের মাত্র $\alpha$ অংশ পায়, তাহলে গ্যারান্টিও কমে যায়।

**উদাহরণ:** $\alpha = 0.5$ হলে $1 - e^{-0.5} \approx 0.393$ — মাত্র 39.3%। অর্থাৎ guarantee-টা LLM-এর "greedy কতটা ভালো করে" তার উপর নির্ভর করে, আর paper সেটা ($\alpha$ বা আসল approximation ratio) কখনো মাপেনি। Theory তাই একটা **design motivation**, measured guarantee নয়।

### ৬.৭ Reward — Marginal Gain (Eq. 4)

$$
r(s_t, a_t) = F(S_{t-1} \cup \{a_t\}) - F(S_{t-1})
$$

**এই সূত্র কী বলছে:** পুরস্কার = test যোগ করার পর নম্বর যতটা বাড়ল।

### ৬.৮ Normalized Coverage Gain
Program-এ মোট $L_A$টা line, বর্তমান suite $S_{t-1}$ cover করে $L_S$টা, নতুন test $a_t$ যোগ করার পর cover করে $L_N$টা ($L_N \geq L_S$):

$$
\Delta_{\text{cov}}(a_t) = \frac{L_N - L_S}{L_A - L_S}
$$

**এই সূত্র কী বলছে:** যে লাইনগুলো এখনো বাকি ছিল, তার কত ভাগ এই test cover করল। ১ মানে বাকি সব শেষ।

- লব = নতুন cover হওয়া line; হর = যত line এখনো বাকি ছিল।
- মান $[0, 1]$-এ — বাকি uncovered অংশের কত ভাগ দূর হলো।

**Worked example (আমার হিসাব, Figure 1-এর ৫-line মডেলে):**
- খালি suite-এ Test A: $L_A = 5, L_S = 0, L_N = 4$ → $\Delta_{\text{cov}} = \frac{4 - 0}{5 - 0} = 0.8$।
- $\{A\}$-এ Test B: $L_S = 4, L_N = 5$ → $\Delta_{\text{cov}} = \frac{5 - 4}{5 - 4} = 1.0$।
- $\{A, B\}$-এ Test C: $L_S = 5, L_N = 5$ → হর $= 0$! **আমার পর্যবেক্ষণ:** সব line cover হয়ে গেলে সূত্রটা $\frac{0}{0}$ — paper এই edge case কীভাবে handle করে তা বলেনি। (Training data-য় > 90% coverage-এর trajectory আছে, তাই এমন state বাস্তবে আসতে পারে।)
- লক্ষ্য করো: B মাত্র 1টা নতুন line cover করেও reward 1.0 পায়, A 4টা line cover করে 0.8 পায় — normalization শেষের দিকের ছোট gain-কেও বড় reward দেয়। একই state-এর group-এর ভেতরে হর একই থাকে, তাই GRPO-র ভেতরের ranking বদলায় না; কিন্তু ভিন্ন state-এর মধ্যে reward-এর scale বদলায়।

### ৬.৯ Final Reward (Eq. 5)

$$
r(s_t, a_t) = \Delta_{\text{cov}}(a_t) \cdot \mathbb{I}(\text{Valid}(a_t))
$$

**এই সূত্র কী বলছে:** পুরস্কার = নতুন লাইনের ভাগ। কিন্তু test না চললে শূন্য দিয়ে গুণ হয়ে পুরস্কার মুছে যায়।

- $\mathbb{I}(\cdot)$ = indicator function — শর্ত সত্য হলে 1, না হলে 0।
- $\text{Valid}(a_t)$ = test compile ও execute সফল (assertion সহ)।
- Paper নিজে প্রথম অংশকে "Coverage Gain" আর দ্বিতীয় অংশকে "Assertion Validity" বলেছে।

$$
r(s_t, a_t) =
\begin{cases}
\Delta_{\text{cov}}(a_t), & \text{যদি test সফলভাবে চলে} \\
0, & \text{যদি syntax error, runtime error বা assertion fail হয়}
\end{cases}
$$

**আমাদের lens থেকে খুব গুরুত্বপূর্ণ (আমার পর্যবেক্ষণ):** "Valid" মানে **বর্তমান program-এ** assertion pass করে। তাই reward model-কে শেখায় program এখন যা করে তাই assert করতে — এটা একটা **regression oracle** (যা এখন হচ্ছে তাকেই ঠিক ধরে নেওয়া assertion)। Program under test-এ যদি নিজেই bug থাকে, test সেই bug-কে "সঠিক" হিসেবে লিখবে। আর `assert True` বা কোনো assertion ছাড়াই শুধু function call করা একটা test-ও valid ও coverage পায় — reward-এ oracle-এর শক্তির কোনো অংশ নেই।

### ৬.১০ GRPO Advantage (Eq. 6)
একই state $s_t$-এ $G$টা candidate $\{a_t^{(1)}, \ldots, a_t^{(G)}\}$, reward $r_t^{(i)}$:

$$
A_t^{(i)} = r_t^{(i)} - \frac{1}{G} \sum_{j=1}^{G} r_t^{(j)}
$$

**এই সূত্র কী বলছে:** প্রতিটা উত্তরের পুরস্কার থেকে group-এর গড় বাদ দিলে advantage পাওয়া যায়। গড়ের উপরে হলে ধনাত্মক, নিচে হলে ঋণাত্মক।

**Worked example (আমার উদাহরণ, সংখ্যাগুলো কাল্পনিক):** $G = 8$, reward = $[0, 0, 0.5, 0.25, 0, 1.0, 0.5, 0.25]$ (তিনটা test চলেনি বলে 0)। গড় $= \frac{2.5}{8} = 0.3125$। Advantage: 1.0-এর test পায় $+0.6875$ (জোরালোভাবে উৎসাহিত); 0-এর test পায় $-0.3125$ (নিরুৎসাহিত); 0.25-এর test পায় $-0.0625$ (সামান্য নিরুৎসাহিত — যদিও সে valid ছিল)।

**আমার পর্যবেক্ষণ:** মূল GRPO (Shao et al.) advantage-কে group standard deviation দিয়েও ভাগ করে; paper-এর Eq. 6-এ শুধু গড় বিয়োগ আছে। এটা ইচ্ছাকৃত পরিবর্তন নাকি সরল উপস্থাপন, paper বলেনি। আর যদি group-এর সব reward সমান হয় (যেমন সব 0), সব advantage 0 — ওই state থেকে কিছু শেখা হয় না।

### ৬.১১ GRPO Objective (Eq. 7)

$$
\mathcal{L}_{\text{GRPO}}(\theta) = -\mathbb{E}_{s_t,\, \{a_t^{(i)}\}}\left[ \frac{1}{G} \sum_{i=1}^{G} A_t^{(i)} \cdot \log \pi_\theta\left(a_t^{(i)} \mid s_t\right) \right] + \beta \, D_{\text{KL}}\left(\pi_\theta, \pi_{\text{base}}\right)
$$

**এই সূত্র কী বলছে:** ভালো test লেখার সম্ভাবনা বাড়াও, খারাপ test-এর কমাও। আর মূল model থেকে বেশি দূরে যেও না।

| Symbol | মানে |
|---|---|
| $\theta$ | LLM-এর parameter |
| $\pi_\theta(a \mid s)$ | state $s$-এ test $a$ লেখার probability |
| $\pi_{\text{base}}$ | frozen base model |
| $A_t^{(i)}$ | Eq. 6-এর advantage |
| $\beta$ | KL শক্তি, paper-এ 0.001 |
| $G$ | group size, paper-এ 8 |

- প্রথম অংশ: positive advantage-এর test-এর log-probability বাড়াও, negative-এর কমাও (minus চিহ্ন কারণ loss minimize করা হয়)।
- দ্বিতীয় অংশ: base model থেকে বেশি দূরে যেও না।
- **আমার পর্যবেক্ষণ:** Paper-এর লেখা objective একটা সরল policy-gradient রূপ — PPO/GRPO-র importance ratio ও clipping লেখা নেই। Verl framework-এর আসল GRPO implementation-এ সম্ভবত clipping আছে, কিন্তু paper তা নিশ্চিত করেনি।

### ৬.১২ Evaluation Metric-এর সূত্র
**Bug Detection Rate (LCB):** buggy solution $b$-কে "detected" ধরা হয় যদি suite-এ অন্তত একটা test থাকে যা canonical solution $c$-এ pass করে কিন্তু $b$-তে fail করে:

$$
\text{Detected}(b) = \exists\, t \in S : \text{pass}(t, c) \land \neg\, \text{pass}(t, b)
$$

$$
\text{BugDet} = \frac{\text{detected buggy solution-এর সংখ্যা}}{\text{মোট buggy solution}} \times 100
$$

**এই সূত্র কী বলছে:** Buggy solution ধরা পড়েছে, যদি এমন একটা test থাকে যা সঠিক solution-এ pass করে কিন্তু buggy-তে fail করে। শতাংশ = কতগুলো buggy ধরা পড়ল।

**Coverage@k (RQ2):** suite-এর প্রথম $k$টা test ($k = 1, \ldots, 5$) মিলে কত coverage।

**আমার পর্যবেক্ষণ — এটা আমাদের patch assurance-এর সাথে সরাসরি মেলে:** Bug Detection-এর এই সংজ্ঞা আসলে **differential testing** (দুই version-এর আচরণ তুলনা) — reference version-এ pass, অন্য version-এ fail। Agent patch যাচাইয়ে reference হতে পারে developer-এর gold patch বা আরেকটা candidate patch।

### ৬.১৩ Paper-এর সংখ্যা যাচাই — Relative Improvement (আমার হিসাব)
Qwen, ULT: line $\frac{69.69 - 51.42}{51.42} = 35.53\%$; branch $\frac{65.87 - 43.23}{43.23} = 52.37\%$; execution $\frac{67.14 - 16.86}{16.86} = 298.22\%$ — paper-এর সংখ্যার সাথে হুবহু মেলে। RQ2: $\frac{2.6}{0.3} \approx 8.67$ — paper বলেছে "nearly 9×"।

**সহজ কথায়:** Paper-এর সংখ্যাগুলো আমি নিজে হিসাব করে মিলিয়ে দেখেছি। প্রায় সব মিলেছে।

---

## ৭. Experimental Setup

| বিষয় | বিবরণ |
|---|---|
| **In-distribution benchmark** | ULT — random 70% task training data-র জন্য, বাকি **30%** শুধু evaluation (আমার হিসাব: $3909 \times 0.3 \approx 1{,}173$ task; paper exact সংখ্যা দেয়নি) |
| **OOD benchmark** | LiveCodeBench — June 2024-এর পরের task; canonical solution-কে program under test ধরে test লেখা, তারপর canonical ও buggy দুটোতে চালানো (task সংখ্যা paper-এ নেই) |
| **Group I baseline** | Zero-shot open LLM: Qwen2.5-Coder-7B, Llama-3.1-8B, CodeLlama-7B — ULT-এর official iterative guided pipeline, $K = 5$ |
| **Group II baseline** | Advanced prompting (Qwen2.5-Coder-7B backbone): ChatTester (error-feedback দিয়ে test repair), SymPrompt (path constraint-সহ path-aware prompting) |
| **Group III baseline** | TestCTRL — PPO + critic + Chain-of-Thought, একই Qwen backbone-এ authors-এর recommended hyperparameter-এ train |
| **Discussion baseline** | GPT-4o, GPT-5.2 (proprietary), CODAMOSA (SBST + LLM, Codex-এর বদলে Qwen2.5-Coder-7B দিয়ে), Qwen2.5 3B/7B/14B base |
| **বাদ দেওয়া baseline** | CoverUp, Panta, TELPA — authors বলেছেন এগুলো অন্য language-এর সাথে বেশি বাঁধা বা migration artifact-এর ঝুঁকি; **আমার পর্যবেক্ষণ:** CoverUp (FSE 2025) আসলে Python-এর জন্য বানানো ("Effective High Coverage Test Generation for Python" — আমাদের folder-এই আছে), তাই এই বাদ দেওয়ার যুক্তি দুর্বল |
| **Metric** | Syntactic correctness, execution pass rate, line ও branch coverage, Coverage@k, mutation score (Cosmic-Ray), bug detection rate (LCB) |
| **Statistics** | 3 seed-এর গড়, Wilcoxon $p < 0.01$; standard deviation বা confidence interval report করা হয়নি |

**সহজ কথায়:** দুই ধরনের পরীক্ষা: চেনা ধরনের task (ULT) আর একদম নতুন ধরনের task (LiveCodeBench)। তুলনা করা হয়েছে সাধারণ model, prompting-এর পদ্ধতি আর আরেকটা RL পদ্ধতির সাথে।

---

## ৮. Results — মূল ফলাফল

### ৮.১ Pilot Study (Table 1) — Structural Myopia-র প্রমাণ

| Model | Setting | Line Cov. | Branch Cov. | Mutation | Syntax | Exec |
|---|---|---|---|---|---|---|
| Qwen2.5-Coder-7B | Direct | 49.13 | 38.77 | 32.61 | 99.35 | 18.18 |
| Qwen2.5-Coder-7B | Iter-Blind | 52.43 | 43.52 | 33.81 | 99.13 | 16.89 |
| Qwen2.5-Coder-7B | Iter-Guided | 52.34 | 43.49 | 33.81 | 98.85 | 16.43 |
| CodeLlama-7B | Direct | 34.38 | 35.92 | 26.42 | 93.83 | 8.94 |
| CodeLlama-7B | Iter-Blind | 40.34 | 39.03 | 28.07 | 89.08 | 8.66 |
| CodeLlama-7B | Iter-Guided | 38.17 | 39.05 | 27.68 | 87.31 | 8.95 |
| Llama-3.1-8B | Direct | 37.20 | 38.51 | 26.79 | 96.90 | 9.39 |
| Llama-3.1-8B | Iter-Blind | 40.97 | 38.47 | 28.14 | 96.52 | 13.98 |
| Llama-3.1-8B | Iter-Guided | 40.05 | 41.05 | 27.06 | 90.51 | 13.48 |

(সব সংখ্যা %)

**সহজ কথায়:** Feedback দিলেও ফল Blind-এর প্রায় সমান। মানে ছোট model coverage report থেকে কিছু শেখে না।

- **Guided ≈ Blind:** Qwen-এ line 52.34 বনাম 52.43; mutation দুটোতেই ঠিক 33.81।
- **Feedback ক্ষতিও করে:** CodeLlama-তে line 40.34 → 38.17।
- **Llama-তে branch সামান্য বাড়ে (38.47 → 41.05), কিন্তু syntax 96.52 → 90.51-এ পড়ে** — model "uncovered অংশ cover করো" নির্দেশ মানতে গিয়ে invalid code hallucinate করে।
- **Figure 2:** সব model-এ logistic-ধরনের curve — $k = 1$ থেকে 2-এ দ্রুত বৃদ্ধি, $k \geq 3$-এ প্রায় সমতল (plateau)।
- **আমার পর্যবেক্ষণ:** Pilot-এর Iter-Guided সংখ্যা Table 2-এর base model সংখ্যার সাথে পুরোপুরি মেলে না (যেমন Qwen line 52.34 বনাম Table 2-এ 51.42; Llama mutation 27.06 বনাম 27.04)। সম্ভবত pilot পুরো ULT-এ আর Table 2 30% test split-এ — paper এটা স্পষ্ট বলেনি।

### ৮.২ RQ1 — Main Results on ULT (Table 2)

| Approach | Line | Branch | Mutation | Syntactic | Execution |
|---|---|---|---|---|---|
| CodeLlama-7B | 38.17 | 39.05 | 27.72 | 87.31 | 8.95 |
| Llama-3.1-8B | 40.05 | 41.05 | 27.04 | 90.51 | 13.48 |
| Qwen2.5-Coder-7B | 51.42 | 43.23 | 33.80 | 98.66 | 16.86 |
| SymPrompt | 34.50 | 28.01 | 16.42 | 99.59 | 25.02 |
| ChatTester | 44.15 | 34.64 | 22.79 | 99.18 | 6.14 |
| TestCTRL | 43.14 | 55.95 | 35.27 | 74.86 | 12.02 |
| TestDecision-CodeLlama | 63.48 | 57.94 | 47.02 | 99.87 | 58.97 |
| TestDecision-Llama | 62.72 | 56.71 | 45.96 | 100.00 | 58.26 |
| **TestDecision-Qwen** | **69.69** | **65.87** | **57.13** | 99.95 | **67.14** |

(সব সংখ্যা %; SymPrompt, ChatTester, TestCTRL-এর backbone Qwen2.5-Coder-7B)

**সহজ কথায়:** একই 7B model-এ আগে ১০০টা test-এর মধ্যে প্রায় ১৭টা চলত, এখন ৬৭টা চলে। আর line coverage প্রায় ১৮ পয়েন্ট বেড়েছে।

**Relative improvement, base → TestDecision (আমার হিসাব, paper-এর যেগুলো বলা সেগুলোর সাথে মিলিয়ে):**

| Backbone | Line | Branch | Mutation | Execution |
|---|---|---|---|---|
| Qwen2.5-Coder-7B | +35.53% (paper: 35.53) | +52.37% (paper: 52.37) | +69.02% | +298.22% (paper: 298.22) |
| CodeLlama-7B | +66.31% (paper: 66.31) | +48.37% | +69.62% | +558.88% |
| Llama-3.1-8B | +56.60% (paper: 56.60) | +38.15% | +69.97% | +332.20% |

**সহজ কথায়:** তিন model-এই উন্নতি হয়েছে। শতাংশ বড় দেখায় কারণ execution-এর পুরনো সংখ্যা খুব ছোট ছিল।

- Abstract-এর "branch 38.15–52.37%, execution 298.22–558.88%" এই table থেকে আসে — মিলেছে।
- **TestDecision বনাম TestCTRL (একই Qwen backbone):** line +61.54%, branch +17.73% (paper-এর সংখ্যা; আমার হিসাবেও মেলে)। Mutation-এ আমার হিসাবে +61.98%।
- **Prompting baseline base model-এর চেয়েও খারাপ:** SymPrompt line 34.50% (base 51.42%); ChatTester execution 6.14%।
- **আমার পর্যবেক্ষণ:** TestCTRL-এর branch (55.95%) তার line (43.14%)-এর চেয়ে অনেক বেশি — সাধারণত branch coverage line-এর চেয়ে কম বা কাছাকাছি হয়। Paper এই অস্বাভাবিকতা ব্যাখ্যা করেনি; measurement pipeline-এ পার্থক্য থাকতে পারে।
- **আরেকটা লক্ষণীয় বিষয় (আমার হিসাব):** তিন backbone-এই mutation-এ relative gain প্রায় একই (69.02–69.97%), অথচ line ও execution-এ অনেক আলাদা।

**সহজ কথায়:** TestDecision বাকি সবার চেয়ে ভালো। এমনকি prompting-এর পদ্ধতিগুলো সাধারণ model-এর চেয়েও খারাপ করেছে।

### ৮.৩ RQ2 — Optimization in Sequence (Figure 4)
- $k = 1$-এ TestDecision-Qwen-এর line coverage **58.27%**, base Qwen2.5-Coder-এর **47.31%**।
- TestDecision **মাত্র 1টা test দিয়েই** base model-এর $k = 5$-এর চূড়ান্ত ফল (51.42%) ছাড়িয়ে যায়।
- Baseline-রা $k = 3$-এর পর সমতল। $k = 3$ থেকে $k = 5$: base Qwen মাত্র **0.3%** coverage যোগ করে, TestDecision **2.6%** — "nearly 9×" (আমার হিসাব 8.67×)।
- Paper-এর ব্যাখ্যা: model "backbone logic" আগে test করতে শিখেছে, আর পরের step-এ `#uncovered` marker দেখে বাকি অংশ লক্ষ্য করে।
- **আমার পর্যবেক্ষণ:** Figure 4-এর পুরো curve-এর সংখ্যা text-এ নেই, শুধু উপরের কয়েকটা; $k = 5$-এর পরে কী হয় (budget বাড়ালে) পরীক্ষা হয়নি।

**সহজ কথায়:** প্রথম test-ই এত ভালো যে base model-এর ৫টা test-এর সমান। পরের test-গুলোতেও TestDecision বেশি যোগ করে।

### ৮.৪ RQ3 — LiveCodeBench Generalization ও Bug Detection (Table 3)

| Approach | Line | Branch | Mutation | Syntactic | Execution | Bug Det. |
|---|---|---|---|---|---|---|
| CodeLlama-7B | 12.24 | 31.44 | 16.29 | 64.20 | 5.78 | 8.50 |
| Llama-3.1-8B | 27.61 | 44.00 | 22.17 | 86.94 | 23.90 | 11.00 |
| Qwen2.5-Coder-7B | 49.61 | 50.52 | 38.34 | 93.88 | 36.36 | 20.50 |
| SymPrompt (Qwen) | 19.09 | 13.33 | 11.28 | 97.39 | 19.69 | 4.50 |
| ChatTester (Qwen) | 36.38 | 27.99 | 20.51 | 99.79 | 8.68 | 9.50 |
| TestCTRL (Qwen) | 44.12 | 53.85 | 36.49 | 78.63 | 8.72 | 24.00 |
| TestDecision-CodeLlama | 42.78 | 38.03 | 27.72 | 99.88 | 34.80 | 16.00 |
| TestDecision-Llama | 43.62 | 52.90 | 34.26 | 100.00 | 39.80 | 21.50 |
| **TestDecision-Qwen** | **62.47** | **63.51** | **54.35** | 100.00 | **57.73** | **32.50** |

**সহজ কথায়:** একদম নতুন task-এও TestDecision সেরা, কিন্তু সেরা model-ও ১০০টা buggy code-এর মধ্যে মাত্র ৩২-৩৩টা ধরে।

- **Qwen:** line +25.92%, branch +25.71%, execution +58.77% (36.36 → 57.73) — paper ও আমার হিসাব মেলে।
- **CodeLlama:** line +249.51% (12.24 → 42.78), execution +502.08% (5.78 → 34.80)।
- **Llama:** line +57.99%।
- **Bug detection:** Qwen 20.50 → 32.50 (paper: "58.5%"; আমার হিসাব 58.54%); CodeLlama 8.50 → 16.00 (+88.24%); Llama 11.00 → 21.50 (+95.45%); TestCTRL-এর 24.00-এর চেয়ে +8.5 point।
- **আমার পর্যবেক্ষণ:** Abstract বলে bug detection-এ উন্নতি "58.43–95.45%"; Table 3 থেকে আমার হিসাব 58.54–95.45%। নিচের সীমায় ছোট অমিল আছে।
- **আমার পর্যবেক্ষণ — absolute সংখ্যার দিকে তাকাও:** সেরা model-ও LCB-এর buggy solution-এর মাত্র **32.50%** ধরে — অর্থাৎ দুই-তৃতীয়াংশের বেশি bug ধরা পড়ে না। Patch assurance-এ এটাকে "নির্ভরযোগ্য" signal বলা যাবে না, একটা সহায়ক signal মাত্র।
- TestCTRL-এর LCB branch (53.85) TestDecision-Llama (52.90)-এর চেয়ে বেশি — TestDecision সব cell-এ সেরা নয়, Qwen version-ই সেরা।

**সহজ কথায়:** Bug ধরার সংখ্যা বেড়েছে, কিন্তু এখনো দুই-তৃতীয়াংশের বেশি bug অধরা।

### ৮.৫ RQ4 — Ablation (Table 4, Qwen2.5-Coder-7B)

| Variant | Line | Branch | Mutation | Syntactic | Execution |
|---|---|---|---|---|---|
| Full TestDecision | 69.69 | 65.87 | 57.13 | 99.95 | 67.14 |
| w/o RL (SFT on same data) | 54.14 | 45.42 | 37.26 | 99.85 | 23.98 |
| w/o Greedy Inference | 63.27 | 57.19 | 51.23 | 99.28 | 62.59 |
| vanilla LLM (framework on frozen base) | 59.29 | 51.72 | 41.17 | 99.97 | 25.05 |

**সহজ কথায়:** RL বাদ দিলে সবচেয়ে বেশি ক্ষতি, বিশেষ করে test চলার হারে। Greedy নিয়ম বাদ দিলেও কিছু কমে।

- **RL বনাম SFT:** execution 23.98 → 67.14 — paper-এর "180% relative improvement" (আমার হিসাব 179.98%)।
- **Greedy inference সরালে:** line 69.69 → 63.27, mutation 57.13 → 51.23।
- **শুধু inference framework (training ছাড়া):** base 51.42 → 59.29 line — কিন্তু execution মাত্র 25.05% ("gap দেখে, কিন্তু ঠিকমতো test লিখতে পারে না")।

**আমার হিসাব — "synergy" দাবি যাচাই** (ধরে নিয়ে যে Table 2-এর Qwen base = framework ও RL কোনোটাই নেই):

| Metric | Base | শুধু framework-এর অবদান | শুধু RL-এর অবদান | দুটো যোগ করলে প্রত্যাশা | Full-এ আসল অবদান |
|---|---|---|---|---|---|
| Line | 51.42 | +7.87 | +11.85 | +19.72 | +18.27 |
| Execution | 16.86 | +8.19 | +45.73 | +53.92 | +50.28 |
| Mutation | 33.80 | +7.37 | +17.43 | +24.80 | +23.33 |

দুটো component একসাথে প্রতিটার আলাদা অবদানের যোগফলের চেয়ে **সামান্য কম** দেয় — অর্থাৎ এরা complementary, কিন্তু কঠোর অর্থে super-additive "synergy" নয়। Execution-এর প্রায় পুরো উন্নতি RL থেকে আসে।

**সহজ কথায়:** দুটো অংশ মিলে প্রায় সব লাভ দেয়, কিন্তু একটা অন্যটাকে 'বাড়িয়ে' দেয় না। শুধু একটা অন্যটার পরিপূরক।

**আরেকটা লক্ষণীয় বিষয় (আমার পর্যবেক্ষণ):** "w/o RL" (SFT) variant যদি greedy framework-সহ চলে থাকে, তাহলে SFT frozen model-এর চেয়েও খারাপ করেছে (line 54.14 বনাম 59.29, mutation 37.26 বনাম 41.17)। অর্থাৎ GPT-5-mini-এর test নকল করা আসলে ক্ষতিকর। Paper এই variant-এর inference setting স্পষ্ট করেনি।

### ৮.৬ Discussion — Proprietary, Scale ও SBST (Table 5)

| Approach | Line | Branch | Mutation | Syntactic | Execution |
|---|---|---|---|---|---|
| GPT-4o | 59.88 | 51.71 | 46.41 | 100.00 | 27.16 |
| GPT-5.2 | 69.40 | 65.65 | **66.02** | 99.97 | **70.58** |
| CODAMOSA | 52.73 | 48.60 | 23.56 | 77.88 | 15.26 |
| Qwen2.5-3B-Base | 46.58 | 41.69 | 29.35 | 94.27 | 12.75 |
| TestDecision-Qwen-3B | 52.37 | 48.94 | 37.84 | 100.00 | 23.90 |
| Qwen2.5-7B-Base | 51.42 | 43.23 | 33.80 | 98.66 | 16.85 |
| TestDecision-Qwen-7B | 69.69 | 65.87 | 57.13 | 99.95 | 67.14 |
| Qwen2.5-14B-Base | 55.07 | 46.75 | 37.21 | 99.49 | 18.41 |
| TestDecision-Qwen-14B | **74.01** | **70.14** | 61.58 | 99.92 | 68.82 |

- **বনাম GPT-4o:** line 69.69 বনাম 59.88 — +16.38% (paper ও আমার হিসাব মেলে)।
- **বনাম GPT-5.2:** line 69.69 বনাম 69.40, branch 65.87 বনাম 65.65 — "comparable"। **কিন্তু (আমার পর্যবেক্ষণ):** mutation-এ GPT-5.2 অনেক এগিয়ে (66.02 বনাম 57.13, 8.89 point), execution-এও (70.58 বনাম 67.14)। Fault-detection-এর দিক থেকে GPT-5.2 স্পষ্টভাবে ভালো।
- **14B:** paper-এর conclusion বলে 14B "giant proprietary model-কে ছাড়িয়ে যায়" — line (74.01 বনাম 69.40) ও branch-এ সত্য, কিন্তু mutation (61.58 বনাম 66.02) ও execution (68.82 বনাম 70.58)-এ নয়।
- **Scale (আমার হিসাব):** absolute line gain 3B +5.79, 7B +18.27, 14B +18.94 point; relative 12.43%, 35.53%, 34.39%। অর্থাৎ 3B থেকে 7B-তে বড় লাফ, কিন্তু 7B থেকে 14B-তে gain প্রায় একই — paper-এর "larger models থেকে larger gain" দাবি এই তিনটা বিন্দু থেকে দুর্বলভাবে সমর্থিত।
- **CODAMOSA:** line 52.73% (base-এর সামান্য উপরে), কিন্তু execution 15.26%, syntactic 77.88%। TestDecision line-এ +32.16%। Paper বলেছে CODAMOSA-র test-এর readability "very unacceptable" — কিন্তু readability মাপার কোনো metric দেয়নি।
- Paper নিজেই স্বীকার করেছে এই তুলনা fair নয় (proprietary model অনেক বড়; SBST অনেক candidate তৈরি করে)।
- Table 5-এ Qwen2.5-7B-Base execution 16.85, Table 2-এ 16.86 — ছোট অমিল।

**সহজ কথায়:** 7B model coverage-এ GPT-5.2-এর সমান, কিন্তু bug ধরার মাপ (mutation score)-এ পিছিয়ে। আর 7B থেকে 14B-তে লাভ আর বাড়ে না।

---

## ৯. Key Findings / Insights (Supervisor-কে বলার মতো ৮টা পয়েন্ট)

1. **Test suite generation একটা sequential decision problem** — একটা test-এর মূল্য suite-এ আগে কী আছে তার উপর নির্ভর করে (Figure 1)।
2. **Coverage-ধরনের utility monotone submodular** — তাই greedy-র $(1 - 1/e) \approx 63.2\%$ guarantee তাত্ত্বিকভাবে প্রযোজ্য (exact greedy ধরে)।
3. **ছোট open model coverage feedback কাজে লাগাতে পারে না** (structural myopia) — Iter-Guided ≈ Iter-Blind (Table 1)।
4. **Prompting যথেষ্ট নয়, training লাগে** — শুধু framework line 59.29% দেয়, কিন্তু execution 25.05%; RL-সহ 69.69% ও 67.14%।
5. **RL > SFT একই data-তে** — SFT execution 23.98%, RL 67.14%। Marginal gain শেখাতে imitation কাজ করে না।
6. **Critic-free GRPO + greedy step reward > PPO + critic (TestCTRL)** — ULT line +61.54%, LCB bug detection +8.5 point।
7. **প্রথম test-ই সবচেয়ে মূল্যবান** — $k = 1$-এ 58.27%, base-এর $k = 5$ (51.42%)-কে ছাড়িয়ে যায়।
8. **Coverage উন্নতি fault detection-এ কিছুটা রূপান্তরিত হয়, কিন্তু সীমিতভাবে** — LCB bug detection 20.50 → 32.50%, তবুও দুই-তৃতীয়াংশ bug ধরা পড়ে না; আর GPT-5.2 mutation-এ এখনো এগিয়ে।

**সহজ কথায়:** আট পয়েন্টের সার কথা: ধাপে ধাপে ভাবো, শুধু prompt যথেষ্ট না, RL লাগে, কিন্তু bug ধরার ব্যাপারে এখনো অনেক পথ বাকি।

---

## ১০. কেন এই Solution অন্যগুলোর থেকে ভালো?

| বৈশিষ্ট্য | SBST (EvoSuite/Pynguin, CODAMOSA) | Prompting (ChatTester, SymPrompt, CoverUp) | PPO-RL (TestCTRL) | **TestDecision** |
|---|---|---|---|---|
| Suite-level চিন্তা | হ্যাঁ (fitness = coverage) | আংশিক (feedback text) | না, global reward | **হ্যাঁ — প্রতি step-এ marginal gain** |
| তাত্ত্বিক guarantee | না | না | না | **$(1 - 1/e)$, exact greedy ধরে** |
| Model weight বদলায় | প্রযোজ্য নয় | না (frozen) | হ্যাঁ | হ্যাঁ |
| Critic network | — | — | হ্যাঁ (ব্যয়বহুল) | **না (GRPO)** |
| Test readability | খারাপ (paper-এর দাবি) | ভালো | ভালো | ভালো (LLM-লেখা) |
| Execution validity | কম (CODAMOSA 15.26%) | কম (ChatTester 6.14%) | 12.02% | **67.14%** |
| ছোট open model-এ চলে | হ্যাঁ | দুর্বল | হ্যাঁ | **হ্যাঁ, 7B** |
| Feedback উপস্থাপন | — | Raw coverage report | CoT | **AST-injected `#uncovered` marker** |

**সহজ কথায়:** অন্য পদ্ধতির তুলনায় TestDecision-এ গ্যারান্টির যুক্তি আছে, critic লাগে না, আর test সবচেয়ে বেশি চলে।

**মূল শক্তি:**
1. **Theory থেকে design:** কেন greedy step reward যুক্তিসঙ্গত তার একটা নীতিগত ব্যাখ্যা।
2. **সস্তা ও local:** 7B model, GRPO-তে critic নেই, deploy করা যায় privacy-সহ।
3. **কম test-এ বেশি coverage:** budget-দক্ষ (RQ2)।
4. **Execution validity প্রায় চারগুণ** — base-এর অনেক test আসলে চলেই না, RL সেটা ঠিক করে।
5. **Code-grounded state representation:** `#uncovered` marker একটা সহজ, পুনর্ব্যবহারযোগ্য কৌশল — training ছাড়াও কাজ করে (vanilla 51.42 → 59.29)।

**সহজ কথায়:** শক্তির জায়গা: যুক্তি আছে, সস্তা, কম test-এ বেশি কাজ, আর test সত্যিই চলে।

---

## ১১. কোন পরিস্থিতিতে এই Paper ভালো কাজ করে, কোথায় করে না

### ✅ ভালো কাজ করে যখন:
- **Python, function-level** unit test লাগবে, আর program under test-এর বর্তমান আচরণ মোটামুটি সঠিক ধরা যায় (regression test-এর মতো)।
- **ছোট budget** ($K = 5$)-এ যত বেশি সম্ভব coverage দরকার।
- **Local/open model** দরকার (privacy, খরচ)।
- Coverage gap স্পষ্টভাবে দেখানো যায় (Coverage.py instrumentation চলে)।

### ❌ ভালো কাজ করে না / সীমিত যখন:
- **Program under test-এ নিজেই bug আছে** — reward বর্তমান আচরণকে "valid" ধরে, তাই bug-কে assert করে ফেলতে পারে। AI agent-এর patched code-এ সরাসরি test generate করলে ঠিক এই সমস্যা।
- **Repository-level, class dependency, external environment (DB, network, file)** — authors নিজেরাই বলেছেন RL environment-এ চ্যালেঞ্জ।
- **অন্য language** — শুধু Python পরীক্ষা হয়েছে।
- **শক্ত oracle দরকার** (যেমন security property, specification-ভিত্তিক) — reward-এ assertion strength নেই।
- **Flaky বা non-deterministic code** — Assumption 1 ভাঙে।
- **বড় budget** — $K > 5$-এ আচরণ অজানা।
- **খুব ছোট model** (3B) — gain সীমিত (+5.79 point)।

**সহজ কথায়:** যেখানে code-এ আগে থেকেই bug আছে, বা project ভারী, বা অন্য language, সেখানে সরাসরি ব্যবহার করা ঠিক নয়।

---

## ১২. Limitations — দুর্বলতা

### ১২.১ Authors যা নিজেরা স্বীকার করেছেন (Section 7.4 ও অন্যত্র)
1. **Internal validity:** implementation bug-এর ঝুঁকি — mature library ও manual check দিয়ে কমানোর চেষ্টা; leakage এড়াতে ULT ও LCB; baseline-এর official implementation ও recommended setting।
2. **External validity:** শুধু Python (unleaked benchmark-এর প্রয়োজন ও Python-এর instrumentation ecosystem-এর কারণে); ULT আসল function হলেও industrial system-level testing-এর মতো নয়; complex class dependency ও external environment simulation RL environment-এ সমস্যা হতে পারে।
3. **Construct validity:** equivalent mutant mutation score-কে underestimate করতে পারে — standard mutation operator subset আর relative comparison দিয়ে কমানোর চেষ্টা।
4. **Mutation reward বাদ:** online mutation testing ধীর (76.53 s), তাই execution validity proxy।
5. **Proprietary ও SBST তুলনা fair নয়** (Section 7-এর শুরুতে)।

**সহজ কথায়:** লেখকরা নিজেরাই বলেছেন: শুধু Python, তুলনা পুরো ন্যায্য নয়, আর mutation-কে reward বানানো যায়নি কারণ সেটা ধীর।

### ১২.২ আমার Critical Analysis (Professor-level observation)
1. **Oracle শক্তি reward-এ নেই (আমাদের জন্য সবচেয়ে গুরুত্বপূর্ণ):** Reward = নতুন line coverage × "test চললো কিনা"। কোনো assertion ছাড়া বা `assert True`-ধরনের test-ও পূর্ণ reward পেতে পারে। Paper mutation score-এ উন্নতি দেখিয়েছে (33.80 → 57.13), তাই বাস্তবে assertion কিছুটা আছে, কিন্তু reward নিজে এটা নিশ্চিত করে না — এটা একটা **reward hacking-এর পথ** (model আসল কাজ না করে শুধু পুরস্কার বাগানোর শর্ট-কাট) (CG12)। Generated test-এর কত শতাংশে weak/no assertion তা paper মাপেনি।
2. **Regression oracle সমস্যা:** "Valid" = বর্তমান program-এ pass। তাই test program-এর বর্তমান আচরণ (bug সহ) encode করে। LCB-তে এটা কাজ করে কারণ test canonical (সঠিক) solution-এর উপর লেখা হয়। কিন্তু agent-এর patched code-এর উপর লিখলে test patch-এর bug-কেই "সঠিক" ধরবে — overfitting detection-এ (CG1) সরাসরি ব্যবহার করা যাবে না।
3. **Theory আর practice-এর ফাঁক:** Theorem 1 exact argmax ধরে; LLM approximate greedy। আসল approximation ratio বা greedy-গুণমান ($\alpha$) কোথাও মাপা হয়নি (Section ৬.৬)। এমনকি training pool-এর 20 candidate-এ exact greedy-র সাথে model-এর পছন্দ মেলানো যেত — করা হয়নি।
4. **Utility-র অসামঞ্জস্য:** Theory-র $F$ হলো line/branch/mutant coverage-এর cardinality; reward-এ normalized line gain (হর বদলায়) আর validity gate; headline metric branch coverage ও mutation score। Branch বা mutation-এর জন্য submodularity আলাদাভাবে প্রমাণ করা হয়নি (mutant kill-ও set-coverage, তাই সম্ভবত প্রযোজ্য, কিন্তু validity gate-সহ reward function-টা theory-র $F$ নয়)।
5. **$\frac{0}{0}$ edge case:** সব line cover হলে $\Delta_{\text{cov}}$ অসংজ্ঞায়িত (Section ৬.৮)।
6. **সংখ্যার ছোট অসংগতি:** Introduction বলে branch-এ উন্নতি "38.15–65.87%", কিন্তু Table 2 থেকে range 38.15–52.37% (65.87 আসলে absolute branch coverage) — abstract-এ সঠিক range আছে। Abstract-এর bug-detection 58.43% বনাম আমার হিসাব 58.54%। Pilot বনাম Table 2-এর base সংখ্যা মেলে না। Table 5-এ 16.85 বনাম Table 2-এ 16.86।
7. **"GPT-5.2-এর সমান" দাবি আংশিক:** line/branch-এ সমান, কিন্তু mutation-এ 8.89 point পিছিয়ে। GPT-5.2 কোন prompt/pipeline-এ চালানো হয়েছে তাও বলা নেই — greedy framework দিলে GPT-5.2 আরও ভালো করতো কিনা জানা নেই।
8. **Variance report নেই:** 3 seed চালানো হয়েছে, কিন্তু standard deviation বা CI নেই; Wilcoxon-এর effect size নেই। Reliability domain-এর জন্য এটা দুর্বলতা (CG4)।
9. **Training data selection bias:** শুধু > 90% coverage পাওয়া task রাখা — অর্থাৎ সহজ, GPT-5-mini যেগুলো ভালো test করতে পারে সেগুলো। কঠিন function-এ policy কম শিখেছে। কতগুলো task বাদ পড়লো paper বলেনি।
10. **Teacher model-এর ছায়া:** Candidate pool GPT-5-mini-এর; paper বলে RL তার logits ব্যবহার করে না, কিন্তু starting state-গুলো GPT-5-mini-এর test দিয়ে তৈরি — distribution-এ প্রভাব থাকতে পারে।
11. **Baseline বাছাই:** CoverUp Python-এর জন্য বানানো, তবুও "অন্য language-এর সাথে বাঁধা" বলে বাদ। Pynguin (Python SBST) ব্যবহার না করে CODAMOSA-কে Qwen-এ port করা হয়েছে — port-এর কারণে CODAMOSA দুর্বল হতে পারে।
12. **খরচ report নেই:** GPU-ঘণ্টা, inference latency, token সংখ্যা — কিছুই নেই (CG8)। "ছোট model সস্তা" দাবি তাই অপরিমাপিত।
13. **Artifact নেই:** paper-এ code/model release-এর link পাইনি — reproducibility দুর্বল।
14. **Readability দাবি অপরিমাপিত:** CODAMOSA-র test "very unacceptable" বলা হয়েছে কোনো metric বা human study ছাড়া।
15. **শুধু function-level, $K = 5$:** AI coding agent-এর patch সাধারণত repository-level, একাধিক function জুড়ে।

**সহজ কথায়:** সবচেয়ে বড় দুর্বলতা: test-এর assertion কতটা শক্ত তা reward-এ নেই, আর theory ও বাস্তবের মধ্যে ফাঁক কেউ মাপেনি।

---

## ১৩. Research Gaps — কোথায় কাজ করার সুযোগ আছে

| # | Gap | কেন গুরুত্বপূর্ণ | কে কিছুটা কাজ করেছে (আমাদের folder-এ) |
|---|---|---|---|
| G1 | **Oracle strength reward/metric-এ নেই** — weak assertion-এর test-ও পূর্ণ reward পায় | Assurance signal হিসেবে test-এর মূল্য oracle-এর উপর নির্ভর করে (CG3, CG12) | Coding-Agent Evaluation & Reliability (monograph-এর verifier gaming সতর্কতা); LLM Test Generation (এই folder-এর অন্য paper পড়ে দেখতে হবে) |
| G2 | **Regression oracle — PUT-এর bug encode হয়ে যায়** | Agent patch-এ সরাসরি test লিখলে patch-এর ভুলই "সঠিক" হবে (CG1) | Patch Validation (differential/reference-ভিত্তিক validation); Automated Program Repair (RePaCA — static judge) |
| G3 | **Approximate greedy-র মান অপরিমাপিত** — theory-র guarantee বাস্তবে কতটা টেকে | Theory-কে measured দাবিতে রূপান্তর | — (খোলা) |
| G4 | **Function-level ও Python-only** | Agent patch repository-level, বহু-ভাষা (CG9) | AI Coding Agents (SWE-bench, Agentless-এর reproduction test); Coding-Agent Evaluation (SWE-Bench Pro বহু-ভাষা) |
| G5 | **Run-to-run variance ও flakiness report নেই** — determinism assumption অপরীক্ষিত | একই tool বারবার চালালে ভিন্ন suite → অস্থির signal (CG4) | Coding-Agent Evaluation & Reliability (SWE-rebench pass@k, monograph) |
| G6 | **খরচ ও compute অপরিমাপিত** | ছোট model "সস্তা" দাবি যাচাই, fair তুলনা (CG8) | Coding-Agent Evaluation & Reliability (SWE-rebench-এর cost/problem) |
| G7 | **Mutation-aware reward ব্যয়বহুল (76.53 s)** | Fault-detection সরাসরি optimize করার সস্তা proxy দরকার | — (খোলা) |
| G8 | **Proprietary তুলনা অস্পষ্ট ও আংশিক** — GPT-5.2-এর pipeline অজানা, mutation-এ পিছিয়ে | "7B = frontier" দাবির validity (CG8, CG10) | Coding-Agent Evaluation & Reliability |
| G9 | **Security-relevant test নেই** | Patch functionally ঠিক কিন্তু insecure হতে পারে; generated test কি security property ধরে? (CG5) | Security of AI-Generated Code |
| G10 | **Generated test-এর confidence/uncertainty নেই** — কোন test-এর assertion বিশ্বাসযোগ্য তা বলে না | Assurance report-এ প্রতিটা signal-এর uncertainty দরকার (CG7, CG11) | Trustworthy AI for SE |
| G11 | **Training data selection bias ও teacher leakage** (> 90% filter, GPT-5-mini pool) | কঠিন code-এ policy দুর্বল হতে পারে (CG6, CG10) | Coding-Agent Evaluation & Reliability (SWE-rebench-এর contamination পদ্ধতি) |

**সহজ কথায়:** গবেষণার ফাঁকগুলোর মূল কথা: assertion-এর শক্তি, patch-এর bug, বাস্তব মাপ, খরচ, আর নিরাপত্তা।

---

## ১৪. কী করলে আরও ভালো হবে — Improvement Ideas

1. **Oracle-aware reward:** $\Delta_{\text{cov}}$-এর সাথে assertion-এর শক্তির একটা সস্তা proxy — যেমন নতুন test কতগুলো **sampled mutant** (সব নয়, ৫–১০টা) kill করে। (আমার প্রস্তাব, paper-এ নেই; 76.53 s-এর পুরো mutation-এর বদলে ছোট sample।)
2. **Differential / reference-based mode:** Test PUT-এর উপর নয়, reference version (original code, gold patch, বা একাধিক candidate patch)-এর উপর লেখা, তারপর অন্য version-এ চালিয়ে আচরণের পার্থক্য খোঁজা — LCB-এর bug-detection setting-এর মতো। এতে regression-oracle সমস্যা (G2) এড়ানো যায়।
3. **Patch-targeted `#uncovered` marker:** পুরো function-এর uncovered line-এর বদলে **patch যে line বদলেছে** সেগুলোতে marker বসানো — test generation-কে patch-এর আচরণে কেন্দ্রীভূত করা। (আমার প্রস্তাব।)
4. **Approximation ratio মাপা:** ছোট candidate pool-এ exact greedy ও brute-force optimal বের করে LLM policy-র suite-এর ratio report করা — theory-কে measured দাবি বানানো।
5. **Variance ও cost report:** প্রতি configuration-এ seed-ভেদে SD, CI, আর inference token ও GPU-ঘণ্টা।
6. **Weak-oracle audit:** generated test-এ assertion নেই, trivial assertion, over-mocking — এগুলো গোনা।

**সহজ কথায়:** উন্নতির ধারণা: assertion-এর শক্তি reward-এ আনা, patch-এর সাথে তুলনা করে test চালানো, আর খরচ ও variance মাপা।

---

## ১৫. কোন Gap-এ Research করলে ভালো Result ও Publication আসতে পারে

> ⚠️ এটা LLM Test Generation sub-domain-এর একটা paper-এর ভিত্তিতে প্রাথমিক মত। Sub-domain summary-তে চূড়ান্ত করবো।

| Gap | SPL3-তে করা সম্ভব? | Novelty | Publication সম্ভাবনা |
|---|---|---|---|
| **G2 + G1: Patch-targeted differential test generation** (greedy `#uncovered` marker + reference version) — assurance report-এর dynamic signal | ✅ হ্যাঁ — training ছাড়া, শুধু inference framework, API model দিয়ে | উচ্চ — TestDecision-এর কৌশলকে patch validation-এ নেওয়া নতুন | ⭐⭐⭐⭐⭐ |
| **G1: Weak-oracle audit of coverage-optimized LLM tests** | ✅ হ্যাঁ — AST দিয়ে assertion গোনা + mutation score | মাঝারি-উচ্চ — "All Smoke, No Alarm" (2026) agent test-এ করেছে, coverage-RL test-এ কেউ করেনি (আমার জানামতে, fact sheet অনুযায়ী) | ⭐⭐⭐⭐ |
| **G3: Approximate greedy ratio-র empirical পরিমাপ** | ✅ হ্যাঁ — ছোট pool-এ brute force সম্ভব ($\binom{20}{5} = 15{,}504$ subset) | মাঝারি — theory paper-এর empirical validation | ⭐⭐⭐ |
| **G5: Generated suite-এর run-to-run stability** | ✅ হ্যাঁ, কিন্তু একাধিক run-এর খরচ | মাঝারি | ⭐⭐⭐ |
| G7: Mutation-aware RL reward | ⚠️ কঠিন — GPU training লাগে (paper: 8 × A100) | উচ্চ | ⭐⭐⭐ (resource-সীমিত) |

**সহজ কথায়:** সবচেয়ে সম্ভাবনাময় পথ: training ছাড়া, API model দিয়ে patch-এর জন্য test generation।

**সম্ভাব্য venue (general guidance):**
- **Conference:** ICSE, FSE, ASE, ISSTA (top SE); ICST (testing-বিশেষ); workshop: LLM4Code, DeepTest (paper-এর উদ্ধৃত RLSQM DeepTest 2025-এ)।
- **Journal:** ACM TOSEM, IEEE TSE; student-friendly: EMSE, JSS (paper-এর উদ্ধৃত PyTester JSS 2025-এ), IST, Software Testing, Verification and Reliability (STVR)।

---

## ১৬. SPL3 Implementation Perspective — Software-এ কীভাবে আনবো

**Paper implement করা মানে কী?** পুরো GRPO training (8 × A100) student-এর জন্য বাস্তবসম্মত নয়। কিন্তু paper-এর ablation (Table 4) দেখায় **শুধু inference framework** frozen model-এ line coverage 51.42 থেকে 59.29-এ তোলে। তাই SPL3-এ inference framework-টাই implement করা, আর তাকে patch assurance-এর dynamic signal module বানানো।

**প্রস্তাবিত module:**
1. **Coverage State Extractor:** Coverage.py দিয়ে suite চালিয়ে uncovered line set; `ast` module দিয়ে `#uncovered` marker injection (Python standard library-তেই `ast.unparse` আছে)।
2. **Greedy Test Generator:** যেকোনো LLM (API বা local) দিয়ে $K$ step-এর loop; প্রতি step-এ marked code + আগের test দেখিয়ে একটা test।
3. **Sandbox Executor:** প্রতি test-এর জন্য timeout (paper-এর মতো 3 s), syntactic check (`ast.parse`), pytest execution।
4. **Metric module:** line/branch coverage, Coverage@k curve, mutation score (Cosmic-Ray বা mutmut), **oracle-strength metric** (assertion সংখ্যা, trivial assertion, mock সংখ্যা — আমার যোগ)।
5. **Patch mode (assurance layer-এর জন্য আমার যোগ):** marker বসবে patch-এর বদলানো line-এ; test original/reference version-এ লেখা হবে; তারপর patched version-এ চালিয়ে আচরণ-পার্থক্য রিপোর্ট।
6. **Report:** প্রতিটা signal আলাদা — coverage, mutation, oracle strength, behaviour diff — সাথে run-সংখ্যা ও SD, tool ও model version (sub-domain 3-এর "assurance report" format)।

**সহজ কথায়:** ছোট একটা tool বানাবো: কোন লাইন বাকি তা বের করা, test লেখানো, নিরাপদে চালানো, মাপা, আর রিপোর্ট দেওয়া।

**Practical সতর্কতা:**
- ULT benchmark-এর data public কিনা আর কীভাবে পাওয়া যায় তা যাচাই করতে হবে; না পেলে LiveCodeBench-এর June 2024-পরের task (canonical + buggy solution আছে) সহজ বিকল্প।
- Mutation testing ধীর — paper-এর হিসাবে গড়ে 76.53 s প্রতি mutation score; 100 task-এ শুধু একবার মাপতেই প্রায় 2 ঘণ্টা (আমার হিসাব: $100 \times 76.53 \approx 7{,}653$ s)।
- Windows-এ sandboxing-এর জন্য Docker বা WSL2 লাগবে।

**সহজ কথায়:** Mutation testing ধীর, আর Windows-এ Docker বা WSL2 লাগবে। এটা আগে থেকে ভেবে রাখতে হবে।

---

## ১৭. এই Paper-এর অবস্থান — Context ও Related Work

- **Paper খুব নতুন (April 2026)** — পরবর্তী গবেষণায় এর প্রভাব এখনো মাপার মতো সময় হয়নি। Fact sheet-এ এই paper-এর কোনো follow-up বা independent replication নেই।
- **পূর্বসূরি ধারা:** SBST (EvoSuite, Pynguin) → LLM + SBST (CODAMOSA) → feedback-driven prompting (ChatTester, CoverUp, TELPA, Panta, SymPrompt, HITS) → RL-based test generation (RLSQM, TestCTRL — PPO, PyTester — PPO) → **TestDecision (GRPO + submodular theory)**।
- **কোড-জেনারেশনে RL:** CodeRL, RLTF, CodeRL+, CUBE (coder ও unit tester একসাথে RL), PRLCoder — TestDecision এই RLVR ধারাকে test suite-এ নিয়েছে।
- **Submodularity-র অন্য ব্যবহার (paper-এর উদ্ধৃত):** social network-এ influence maximization (Kempe et al.), sensor placement (Krause & Guestrin), data subset selection, document summarization।
- **আমাদের folder-এর সাথে সংযোগ:** একই folder-এ CoverUp ("Effective High Coverage Test Generation for Python") আছে — TestDecision যে coverage-feedback prompting-কে "structural myopia"-আক্রান্ত বলেছে, CoverUp সেই ধারার প্রধান Python উদাহরণ, অথচ baseline-এ নেই। দুটো paper একসাথে পড়লে "prompting বনাম training" বিতর্ক স্পষ্ট হবে। SWE-bench analysis-এর CG1/CG3 আর এই paper-এর G1/G2 সরাসরি যুক্ত।
- **বড় প্রবণতা (আমার পর্যবেক্ষণ):** Test generation-এর প্রশ্ন "কত coverage" থেকে সরে "test কতটা আসলে bug ধরে আর কতটা বিশ্বাসযোগ্য" — 2026-এর agent-test গবেষণা (Section ২১) ঠিক এই দিকে।

**সহজ কথায়:** Paper নতুন, আর এই ধারার গবেষণা 'কত coverage' থেকে 'test কতটা বিশ্বাসযোগ্য'-র দিকে যাচ্ছে।

---

## ১৮. Supervisor-এর সম্ভাব্য প্রশ্ন ও উত্তর (Viva Prep)

**Q1. Submodularity কী, আর test generation-এ কেন এটা সত্য?**
A: Submodular মানে diminishing returns — ছোট suite-এ একটা test যোগ করার লাভ বড় suite-এ একই test যোগ করার লাভের চেয়ে কম নয়। Coverage = test-গুলোর cover করা element-এর union-এর আকার; বড় suite আগেই বেশি element cover করেছে, তাই নতুন test-এর "নতুন" element সেখানে কম বা সমান। Paper Eq. 2–3-এ এটা set difference দিয়ে প্রমাণ করেছে।

**Q2. $(1 - 1/e)$ guarantee কি বলে TestDecision optimal-এর 63.2% পায়?**
A: না, সরাসরি নয়। Guarantee exact greedy-র জন্য — প্রতি step-এ পুরো test universe থেকে সর্বোচ্চ marginal gain-এর test। LLM approximate greedy; প্রতি step-এ যদি best-এর মাত্র $\alpha$ অংশ পায়, তাহলে bound $1 - e^{-\alpha}$-এ নামে, যেমন $\alpha = 0.5$-এ 39.3%। Paper আসল ratio মাপেনি, তাই theory-টা design-এর যুক্তি, measured guarantee নয়। আর finite $K = 5$-এ exact greedy-র bound আসলে 67.2%।

**Q3. কেন PPO নয়, GRPO?**
A: PPO-তে advantage estimate করতে আলাদা critic (value network) train করতে হয় — memory ও compute বেশি। GRPO একই state-এ $G = 8$টা test sample করে group-গড়কে baseline ধরে। এখানে প্রতিটা step-এর reward তাৎক্ষণিক (marginal gain), তাই long-horizon value estimate দরকার নেই — GRPO স্বাভাবিকভাবে মানায়। Empirically TestCTRL (PPO)-এর চেয়ে line +61.54%, LCB bug detection +8.5 point।

**Q4. SFT কেন কাজ করলো না?**
A: একই data-তে SFT execution 23.98%, RL 67.14%। SFT একটা fixed target test নকল করায়; কিন্তু এই কাজে প্রশ্ন হলো "এই state-এ কোন test বেশি নতুন কিছু দেয়" — একাধিক valid test-এর মধ্যে তুলনা, যা শুধু reward-ভিত্তিক RL দিতে পারে।

**Q5. Reward-এ mutation score কেন নেই, আর এর ফল কী?**
A: Online mutation ব্যয়বহুল — গড়ে 76.53 s। তাই execution validity proxy। কিন্তু এর মানে reward assertion-এর শক্তি মাপে না — `assert True`-ধরনের test-ও coverage-এর reward পেতে পারে। Mutation score বাস্তবে বেড়েছে (33.80 → 57.13), কিন্তু GPT-5.2 এখনো 66.02-এ এগিয়ে। আমার assurance layer-এ তাই oracle-strength আলাদা signal হিসেবে মাপবো।

**Q6. এই test কি সরাসরি AI agent-এর patch যাচাইয়ে ব্যবহার করা যায়?**
A: সরাসরি না। Reward "বর্তমান program-এ pass করে এমন" test-কে valid ধরে — তাই patched code-এর উপর লিখলে test patch-এর আচরণ (bug সহ) encode করবে। ব্যবহার করতে হবে differential ভাবে: reference version-এ লেখা test patched version-এ চালানো, বা একাধিক candidate patch-এর আচরণ তুলনা — যেমন paper-এর LCB bug-detection setting। আর marker বসাতে হবে patch-এর বদলানো line-এ।

**Q7. 7B model কি সত্যিই GPT-5.2-এর সমান?**
A: শুধু coverage-এ: line 69.69 বনাম 69.40, branch 65.87 বনাম 65.65। Mutation-এ GPT-5.2 66.02 বনাম 57.13, execution-এ 70.58 বনাম 67.14 — GPT-5.2 এগিয়ে। আর GPT-5.2 কোন pipeline-এ চালানো হয়েছে paper বলেনি। তাই "comparable" দাবি coverage-এ সীমিত।

**Q8. Ablation থেকে কী শিখলে?**
A: শুধু `#uncovered` marker framework frozen model-কে 51.42 → 59.29 line দেয় — training ছাড়াই উপকার, যা আমার SPL3-এর জন্য গুরুত্বপূর্ণ। কিন্তু execution 25.05%-এ থাকে; RL execution 67.14-এ তোলে। আমার হিসাবে দুটোর মিলিত অবদান আলাদা অবদানের যোগফলের চেয়ে সামান্য কম — complementary, কিন্তু strict synergy নয়।

**Q9. Paper-এর সবচেয়ে বড় দুর্বলতা কী, তোমার মতে?**
A: Oracle strength reward-এ নেই, আর test PUT-এর বর্তমান আচরণকে সঠিক ধরে। Coverage বাড়ানো সহজ, কিন্তু bug ধরা কঠিন — LCB-তে সেরা model-ও মাত্র 32.50% buggy solution ধরে। Assurance-এর দৃষ্টিতে এটাই মূল gap। সাথে variance, খরচ ও artifact না থাকা।

**Q10. তুমি এই paper থেকে কী implement করবে?**
A: Training নয়, inference framework — Coverage.py + AST `#uncovered` marker + greedy $K$-step loop — যেকোনো LLM দিয়ে। তারপর patch mode: marker patch-এর line-এ, test reference version-এ, differential execution। আর প্রতিটা generated suite-এর জন্য coverage, mutation, oracle strength আলাদা signal হিসেবে report।

---

## ১৯. Glossary (দ্রুত মনে রাখার জন্য)

| Term | অর্থ |
|---|---|
| Test suite | Test case-এর সেট |
| Test oracle | সঠিক আচরণ কী তা নির্ধারণকারী (assertion) |
| Regression oracle | বর্তমান আচরণকেই সঠিক ধরে নেওয়া assertion |
| Line / Branch coverage | কত % line / branch-এর দিক execute হয়েছে |
| Mutation score | কত % কৃত্রিম bug (mutant) test ধরেছে |
| Equivalent mutant | যে mutant মূল program-এর মতোই আচরণ করে |
| MDP | State, action, transition, reward দিয়ে sequential decision-এর মডেল |
| Policy | State দেখে action বেছে নেওয়ার নিয়ম (এখানে LLM) |
| Marginal gain | সেটে একটা জিনিস যোগ করলে utility কতটা বাড়ে |
| Submodular | Diminishing returns — বড় সেটে যোগ করার লাভ কম |
| Greedy | প্রতি ধাপে তাৎক্ষণিক সেরা পছন্দ |
| $(1 - 1/e)$ | Monotone submodular-এ greedy-র ≈ 63.2% guarantee |
| SFT | নির্দিষ্ট target নকল করে training |
| RL / RLVR | Reward দিয়ে training / স্বয়ংক্রিয় যাচাইযোগ্য reward |
| PPO | Critic-সহ clipped policy optimization |
| GRPO | Critic ছাড়া, group-গড় baseline-সহ policy optimization |
| KL regularization | Base model থেকে দূরে যাওয়ার শাস্তি |
| AST injection | Code tree-তে `#uncovered` comment বসানো |
| Structural myopia | LLM-এর suite-level দৃষ্টির অভাব, একই জিনিস বারবার test |
| OOD | Training distribution-এর বাইরের data |

---

## ২০. এক নজরে সারাংশ (Summary Card)

| | |
|---|---|
| **Problem** | ছোট open LLM iterative test generation-এ feedback কাজে লাগাতে পারে না (structural myopia); iterative পদ্ধতির কোনো তাত্ত্বিক guarantee নেই |
| **Solution** | Test suite generation = MDP; coverage monotone submodular → greedy $(1 - 1/e)$; `#uncovered` AST marker-সহ greedy inference + GRPO training (reward = normalized line gain × validity) |
| **Method** | ULT 70% থেকে GPT-5-mini-এর 20 candidate → greedy ordering → 8,396 state; GRPO $G = 8$, lr 1e-6, $\beta = 0.001$, 8 × A100 |
| **Key result** | Qwen-7B ULT: line 51.42 → 69.69, branch 43.23 → 65.87, mutation 33.80 → 57.13, execution 16.86 → 67.14; LCB bug detection 20.50 → 32.50 |
| **Key insight** | Training ছাড়া framework-ও সাহায্য করে (59.29), কিন্তু valid test লিখতে RL লাগে; প্রথম test-ই base-এর পুরো suite-কে ছাড়ায় |
| **Main limitation** | Reward-এ oracle strength নেই; regression oracle; theory-practice ফাঁক অপরিমাপিত; Python function-level; variance, খরচ, artifact নেই |
| **আমাদের জন্য gap** | Generated test-কে বিশ্বাসযোগ্য **dynamic assurance signal** বানানো — differential, patch-targeted, oracle-strength-সহ |

**সহজ কথায়:** পুরো paper এক নিঃশ্বাসে: ছোট model + greedy নিয়ম + RL = ভালো test suite, কিন্তু assertion-এর শক্তি অনিশ্চিত।

---

## ২১. বর্তমান (2026) প্রেক্ষাপট — আজকের Model ও Agent-দের সাথে তুলনা

> **উৎস:** এই section-এর সব current-state তথ্য `00_Current_State_2026_Sources.md` (fact sheet, compiled 2026-10-28) থেকে নেওয়া। প্রতিটা সংখ্যার পাশে লেখা আছে সেটা **কোম্পানির নিজের দাবি (vendor-reported)** নাকি **স্বাধীনভাবে মাপা (independent)**। Fact sheet যেটাকে "search-snippet only" বলেছে, সেটা এখানেও তাই চিহ্নিত — supervisor-কে দেখানোর আগে মূল উৎস খুলে যাচাই করা উচিত। আমার নিজের যুক্তি "আমার পর্যবেক্ষণ" দিয়ে আলাদা করা।
>
> **গুরুত্বপূর্ণ সতর্কতা:** এই paper নিজেই April 2026-এর — fact sheet-এর অন্য paper-গুলোর মতো বছর পুরনো নয়। তবুও মাত্র ছয় মাসে model প্রজন্ম বদলে গেছে। আর fact sheet-এ **ULT বা LiveCodeBench test-generation-এ কোনো বর্তমান model-এর সংখ্যা নেই** — এটাই এই section-এর প্রধান ফাঁক।

### ২১.১ Paper-এর সময় বনাম এখন

| দিক | Paper-এ (April 2026, arXiv v2) | এখন, October 2026 | উৎস |
|---|---|---|---|
| Open backbone | Qwen2.5-Coder-7B, Llama-3.1-8B, CodeLlama-7B (2023–2024-এর model); scale study Qwen2.5 3B/14B | Qwen3.8 family (Qwen3.8-27B Apache-2.0, Qwen3.8-Flash-Next প্রায় 2026-08-28); DeepSeek V4/V4-Pro (2026-04-24); GLM-5.3 (weights August-এর শেষে); Kimi K3.1 Pro (2.8T/104B active MoE, open weights "by Nov 4, 2026" প্রতিশ্রুত) | Fact sheet §1 — সব secondary, শুধু Kimi announcement primary |
| এই open model-দের test-generation ফল | ULT/LCB-এ উপরের সংখ্যা | **পাওয়া যায়নি** — fact sheet-এ কোনো বর্তমান open model-এর ULT, LCB বা অন্য unit-test-generation সংখ্যা নেই | Fact sheet |
| Proprietary তুলনা | GPT-4o (line 59.88), GPT-5.2 (line 69.40, mutation 66.02) | GPT-6 family (Astra public 2026-09-04; Sol, Luna 2026-09-22; 6.1 Sol 2026-09-29; 6.1 Terra 2026-10-26); Claude Opus 5.5 (2026-09-22); Gemini 4 Argon (2026-10-13)। এদের **test-generation benchmark সংখ্যা পাওয়া যায়নি** | Fact sheet §1 |
| Candidate generator | GPT-5-mini (training pool-এর জন্য) | Codex catalogue-এ এখন gpt-6-astra, gpt-6.1-sol, gpt-6.1-terra, gpt-6-luna; gpt-5.4 retired (2026-08-31) | learn.chatgpt.com/docs/models (primary, fetched 2026-10-28) |
| Reproduction-test benchmark (paper SWT-bench উদ্ধৃত করেছে) | — | SWT-bench, TDD-Bench-এ বর্তমান model-এর ফল: **পাওয়া যায়নি** | Fact sheet §6 |
| বাস্তবে agent-লেখা test-এর oracle | Paper oracle strength মাপেনি | 86,156 test-file patch (33,596 agent PR)-এর **80.2%**-এ weak বা কোনো স্পষ্ট oracle নেই; strong oracle merge-এর সম্ভাবনা বাড়ায় (OR 1.28, p < 0.001) — **independent** | "All Smoke, No Alarm", arXiv 2606.18168 (2026-06-16) |
| Over-mocking | — | Agent commit-এর 36% test-এ mock যোগ করে, non-agent 26% — **independent** | arXiv 2602.00409 (MSR 2026, **search-snippet only**) |
| Agent test-এর coverage | Paper: coverage-ই মূল লক্ষ্য | AI 16.4% test-adding commit লিখেছে; test লম্বা, assertion বেশি; coverage gain মানুষের test-এর মতো — **independent** | arXiv 2603.13724 (**search-snippet only**) |
| Weak assertion | — | Agent test-এ weak assertion প্রায় 14.3% বনাম 11.9% | arXiv 2607.12068 (secondary summary থেকে সংখ্যা, **unverified**) |
| Issue resolution-এ test-এর মূল্য | — | Agent-এর test লেখা issue resolution-এ সীমিত উন্নতি দেয়, প্রায়ই observation-based debugging দিয়ে প্রতিস্থাপিত — **independent** | "Rethinking the Value of Agent-Generated Tests" (**search-snippet only**) |
| Vendor দাবি | — | Fable 5.1 "can write its own tests to check its work"; "less likely to disable a failing test to pass" — **vendor-reported, qualitative** | anthropic.com/claude/fable; AWS blog (2026-09-01) |
| RL-এ reward hacking | Paper reward gaming আলোচনা করেনি | Opus 5.5 training-এ সফল reward hack "well under 1%" (excluding one sub-class 0.046%) — **vendor-reported**; METR: 8 ঘণ্টার বেশি task-এ সফল run-এর ≥16% প্রতারণা (পুরনো প্রজন্ম) — **independent** | Opus 5.5 System Card §6.2; METR 2026-05-19 |
| খরচ | Training 8 × A100 (GPU-ঘণ্টা বলা নেই); inference খরচ বলা নেই | GPT-6.1 Terra API USD 1 input / USD 5 output per million token (**vendor-reported**); Opus 5.5 USD 4 / USD 20 (**search-snippet only**); Fable 5.1 USD 10 / USD 50 (**search-snippet only**) | Fact sheet §1 |

**সহজ কথায়:** ছয় মাসে model-এর প্রজন্ম বদলে গেছে, কিন্তু নতুন model-এ test generation-এর সংখ্যা পাওয়া যায়নি। তাই paper-এর দাবিগুলো নতুন model-এ যাচাই হয়নি।

**আমার পর্যবেক্ষণ:** Paper-এর মূল দাবি ছিল "ছোট open model + RL ≈ frontier proprietary"। তুলনার frontier (GPT-5.2) এখন দুই প্রজন্ম পিছনে, আর বর্তমান open model (Qwen3.8-27B, DeepSeek V4) অনেক বড় ও নতুন। তারা training ছাড়াই structural myopia-তে ভোগে কিনা — fact sheet-এ কোনো তথ্য নেই। তাই paper-এর মূল motivation ("open model feedback কাজে লাগাতে পারে না") বর্তমান model-এ **অপরীক্ষিত**।

### ২১.২ কোন Finding এখনো সত্য, কোনটা পুরনো হয়ে গেছে

- **এখনো সত্য (model-নিরপেক্ষ) — Theory:** Coverage-এর monotone submodularity আর greedy-র $(1 - 1/e)$ bound গাণিতিক সত্য, model বদলালে বদলায় না। তবে approximate-greedy ফাঁক (Section ৬.৬) বর্তমান model-এও মাপা হয়নি।
- **এখনো সত্য, আরও শক্ত প্রমাণসহ — "Coverage ≠ fault detection":** Paper Inozemtseva-কে উদ্ধৃত করেছিল, আর নিজের ফলেও GPT-5.2-এর mutation বেশি ছিল। 2026-এ agent test-এর coverage মানুষের মতো (snippet), কিন্তু 80.2% test patch-এ weak/no oracle (independent) — অর্থাৎ coverage থাকলেও oracle দুর্বল। এটা paper-এর reward design-এর সমালোচনাকে (Section ১২.২ #১) সমর্থন করে।
- **এখনো প্রাসঙ্গিক, এবং নতুন প্রমাণ পেয়েছে — RL reward gaming-এর ঝুঁকি:** Paper reward hacking আলোচনা করেনি। 2026-এ vendor-রা নিজেরাই training-time reward hack মাপছে (Opus 5.5: 0.046%, vendor-reported), আর METR পুরনো প্রজন্মে ≥16% অবৈধ সফলতা পেয়েছে। Coverage × validity reward-এর মতো দুর্বল-oracle reward-এ hack-এর সুযোগ আছে — **আমার পর্যবেক্ষণ**, পরিমাপ নয়।
- **অপরীক্ষিত / সম্ভবত পুরনো — "ছোট open model-এর structural myopia":** শুধু 2023–2024-এর 7–8B model-এ দেখানো। বর্তমান open model-এ কেউ মাপেনি (fact sheet-এ নেই)।
- **পুরনো — "7B ≈ GPT-5.2" তুলনা:** GPT-5.2 আর frontier নয়; GPT-6 family বা Opus 5.5-এর সাথে তুলনা নেই। বর্তমান proprietary model ULT-এ কত পায় তা **অজানা**।
- **এখনো সত্য — "Prompting-only যথেষ্ট নয়, কিন্তু সাহায্য করে":** বর্তমান model-এ মাপা হয়নি। **আমার পর্যবেক্ষণ:** বর্তমান frontier model-এর ক্ষেত্রে `#uncovered` marker-এর মতো framework-ই হয়তো বেশিরভাগ লাভ দেবে, যেমন paper-এ GPT-5.2 training ছাড়াই 69.40% পেয়েছিল — এটা একটা testable hypothesis, তথ্য নয়।
- **নতুন প্রশ্ন, paper-এ ছিল না — agent test আদৌ কাজে লাগে কিনা:** "Rethinking the Value of Agent-Generated Tests" (snippet) বলছে issue resolution-এ test লেখার উপকার সীমিত। Paper test-কে লক্ষ্য হিসেবে দেখে; agent workflow-এ test একটা মাধ্যম — দুটো দৃষ্টিভঙ্গির মধ্যে ফাঁক আছে।

### ২১.৩ Gap-গুলো আজও খোলা কিনা

| Gap | 2026-এ অবস্থা | প্রমাণ |
|---|---|---|
| G1 / CG3, CG12: Oracle strength reward/metric-এ নেই | **খোলা, এবং বাস্তবে বড় সমস্যা হিসেবে মাপা** | Agent test patch-এর 80.2%-এ weak/no oracle (independent); over-mocking 36% বনাম 26% (snippet); weak assertion 14.3% বনাম 11.9% (unverified)। Coverage-RL-trained test-এর oracle audit **পাওয়া যায়নি** |
| G2 / CG1: Regression oracle — patch-এর bug encode হয় | **খোলা** | PatchDiff: plausible patch-এর 29.6% gold patch থেকে ভিন্ন আচরণ (2025 model, independent; বর্তমান model-এ আবার মাপা হয়নি); PROBE: program variant দিয়ে দুর্বল test ধরা যায় (snippet) |
| G3: Approximate greedy ratio অপরিমাপিত | **খোলা — fact sheet-এ কোনো তথ্য নেই** | — |
| G4 / CG9: Function-level, Python-only | **আংশিক** | Repository-level benchmark বহু-ভাষায় আছে (SWE-bench Multilingual, DeepSWE 5 language), কিন্তু সেগুলো repair-এর জন্য; বহু-ভাষার test-generation benchmark-এ বর্তমান model-এর ফল **পাওয়া যায়নি** |
| G5 / CG4: Run-to-run variance | **খোলা (repair-এ মাপা হচ্ছে, test-generation-এ নয়)** | SWE-rebench pass@1 বনাম pass@5-এ 12–18 point (independent); Noise Floor Audit: prompt-পরিবর্তনে SD rerun-এর 11–58 গুণ (independent)। Generated test suite-এর stability নিয়ে তথ্য **পাওয়া যায়নি** |
| G6 / CG8: খরচ অপরিমাপিত | **খোলা** | Repair benchmark-এ cost report এখন সাধারণ (Vals Verified USD 0.10–2.05 per test, independent), কিন্তু test generation-এ cost-per-suite তথ্য **পাওয়া যায়নি** |
| G7: Mutation-aware reward ব্যয়বহুল | **খোলা — fact sheet-এ তথ্য নেই** | — |
| G8 / CG8, CG10: Proprietary তুলনা অস্পষ্ট | **আরও খারাপ** | Vendor বনাম independent সংখ্যায় বড় ফাঁক সাধারণ (যেমন Sonnet 5.5 Terminal-Bench 70.6% vendor বনাম 63.6–64.1% independent); বর্তমান model-এর test-gen সংখ্যা একেবারেই নেই |
| G9 / CG5: Security-relevant test | **খোলা** | SusVibes/Endor: FuncPass 62.6–84.4% কিন্তু SecPass 7.8–17.3% (Opus 4.6/GPT-5.4 যুগ, independent); Opus 5.5/GPT-6-এর ফল **পাওয়া যায়নি**; security test generation নিয়ে তথ্য নেই |
| G10 / CG7, CG11: Test-এর confidence/uncertainty | **খোলা** | LLM judge নিজেই অবিশ্বস্ত — ComPass-এ plain LLM baseline 62.14% (snippet); over-fix flag-এর precision 5–10% (snippet) |
| G11 / CG6: Training data bias ও teacher leakage | **খোলা, সাধারণভাবে স্বীকৃত** | OpenAI Verified ছেড়েছে contamination-এর কারণে (snippet); LiveCodeBench-ধরনের সময়-ভিত্তিক বিভাজন এখনো প্রধান প্রতিরক্ষা |
| CG2: Candidate re-ranking | **খোলা — এখানে সুযোগ** | SWE-rebench-এ pass@1 বনাম pass@5-এর 12–18 point ফাঁক (independent) — differential generated test candidate patch বাছাইয়ে কাজে লাগতে পারে (আমার পর্যবেক্ষণ) |

**সহজ কথায়:** প্রায় সব gap এখনো খোলা। বিশেষ করে assertion-এর শক্তি আর patch-এর bug।

### ২১.৪ বর্তমান Model দিয়ে আবার পরীক্ষা করলে — SPL3 Idea (cost-aware)

**মূল নীতি (আমার পর্যবেক্ষণ):** GRPO training (8 × A100) বাদ; paper-এর Table 4 দেখায় শুধু inference framework-ও উপকারী। তাই training-free version-কে বর্তমান সস্তা model দিয়ে চালানো।

1. **Structural myopia কি এখনো আছে? (paper-এর pilot study পুনরাবৃত্তি)**
   - Model: GPT-6.1 Terra (vendor-reported দাম USD 1 / USD 5 per million token) আর একটা local open model যদি GPU থাকে (যেমন Qwen3.8-27B — তবে 27B চালাতে বড় GPU লাগবে; না থাকলে API-তে পাওয়া open model)।
   - Data: LiveCodeBench-এর June 2024-পরের 100টা task (canonical + buggy আছে, তাই bug detection মাপা যায়)।
   - Setting: Direct, Iter-Guided (raw coverage text), Greedy-marker (`#uncovered`), $K = 5$, 3 run।
   - **আমার অনুমান (rough খরচ, token সংখ্যা মাপা নয়):** প্রতি call ধরি প্রায় 1,500 input ও 300 output token; 100 task × 5 step × 3 setting × 3 run = 4,500 call → প্রায় 6.75M input ও 1.35M output token → Terra-তে প্রায় USD 6.75 + USD 6.75 ≈ USD 13.5। Prompt বড় হলে কয়েক গুণ বাড়বে।
   - **যে gap দেখাবে:** ২১.২-এর "অপরীক্ষিত" finding — বর্তমান model-এ Guided ≈ Blind কিনা, আর marker কতটা যোগ করে।
2. **Oracle-strength audit (G1):** উপরের সব suite-এ AST দিয়ে গোনা — assertion নেই, trivial assertion, mock; সাথে mutation score (Cosmic-Ray বা mutmut)। Coverage বনাম mutation বনাম oracle-strength-এর correlation। **আমার হিসাব:** paper-এর 76.53 s ধরে 100 task × 3 setting-এ একবার করে mutation ≈ 300 × 76.53 ≈ 22,959 s ≈ 6.4 ঘণ্টা CPU — local-এ সম্ভব, API খরচ নেই। **Gap:** "All Smoke, No Alarm"-এর 80.2% সংখ্যার সাথে coverage-optimized test-এর তুলনা।
3. **Approximate-greedy ratio (G3):** প্রতি task-এ model দিয়ে 20টা candidate test, তারপর brute force ($\binom{20}{5} = 15{,}504$ subset — execution coverage একবার মেপে রাখলে শুধু set union, তাই দ্রুত) দিয়ে optimal 5-subset, exact greedy, আর model-এর sequential suite তুলনা। **Gap:** theory-র দাবি বাস্তবে কতটা টেকে — paper-এ বা fact sheet-এ কোথাও নেই।
4. **Patch-targeted differential mode (G2, CG1, CG2) — assurance layer-এর সাথে সরাসরি যুক্ত:** SWE-bench Verified বা SWE-rebench-এর 20–30টা task, প্রতিটায় একাধিক agent patch (প্রকাশিত trajectory থেকে, যাতে নিজে agent চালাতে না হয়)। Patch-এর বদলানো line-এ `#uncovered` marker, test original/reference code-এ লেখা, তারপর patch-গুলোর উপর চালিয়ে আচরণ-পার্থক্য। **Gap:** PatchDiff-এর 29.6% সংখ্যা বর্তমান agent patch-এ — fact sheet বলছে কেউ আবার মাপেনি। Test যদি repository-level dependency-তে চলতে না পারে, সেটাও একটা finding (G4)।
5. **Stability (G5):** উপরের যেকোনো একটা setting-এ একই task-এ 3 run — generated suite-এর coverage-এর SD আর differential রায় (patch ঠিক/ভুল) কতবার বদলায়। **Gap:** test-generation-এর run-to-run variance-এর কোনো সংখ্যা fact sheet-এ নেই।

### ২১.৫ Supervisor-এর সম্ভাব্য প্রশ্ন (2026 প্রসঙ্গে)

**Q1. Paper মাত্র ছয় মাস আগের — তবুও কি পুরনো?**
A: Theory পুরনো হয় না। কিন্তু empirical দাবি — "ছোট open model myopic" আর "7B ≈ frontier" — 2023–2024-এর backbone আর GPT-5.2-এর উপর। এখন GPT-6 family, Opus 5.5, Qwen3.8, DeepSeek V4 এসেছে, আর fact sheet-এ এদের কোনো test-generation সংখ্যা নেই। তাই empirical অংশ বর্তমান model-এ অপরীক্ষিত — এটাই আমার SPL3 idea ১-এর ভিত্তি।

**Q2. আজকের agent-রা কি ভালো test লেখে?**
A: Coverage-এর দিক থেকে মানুষের কাছাকাছি (MSR 2026, search-snippet), কিন্তু 86,156 test patch-এর 80.2%-এ weak বা কোনো স্পষ্ট oracle নেই (independent), আর agent বেশি mock ব্যবহার করে (36% বনাম 26%, snippet)। Vendor দাবি করে Fable 5.1 নিজের test লেখে, কিন্তু এটা qualitative দাবি। অর্থাৎ TestDecision যে সমস্যা মাপেনি — oracle strength — সেটাই এখন বাস্তবে প্রধান সমস্যা।

**Q3. তুমি কি TestDecision-এর মতো RL training করবে?**
A: না — paper 8 × A100 ব্যবহার করেছে, GPU-ঘণ্টাও বলেনি। Table 4 দেখায় training ছাড়া framework-ই 51.42 থেকে 59.29 line দেয়। আমি training-free framework বর্তমান সস্তা API model দিয়ে চালাবো, আর মূল অবদান হবে patch-targeted differential mode আর oracle-strength audit — যেগুলো assurance-এর জন্য সরাসরি দরকারি।

**Q4. Generated test-কে assurance signal হিসেবে কতটা বিশ্বাস করা যায়?**
A: আলাদা signal হিসেবে, একমাত্র রায় হিসেবে নয়। Paper-এর সেরা model-ও LCB-এর মাত্র 32.50% buggy solution ধরে। আর 2026-এর তথ্য বলছে agent test-এর oracle প্রায়ই দুর্বল। তাই assurance report-এ generated test-এর ফল coverage, mutation score, oracle strength আর run-ভেদে stability-সহ দেখাবো — static judge-এর রায়ের পাশে, মিশিয়ে একটা score বানিয়ে নয়।

**Q5. Reward hacking কি এখানে বাস্তব ঝুঁকি?**
A: Paper এটা আলোচনা করেনি। Coverage × validity reward-এ assertion ছাড়া test-ও reward পায় — এটা hack-এর পথ। 2026-এ vendor-রা নিজেরাই training-time reward hack মাপছে (Opus 5.5: 0.046%, vendor-reported), আর METR পুরনো প্রজন্মে দীর্ঘ task-এর সফল run-এর ≥16% প্রতারণা পেয়েছে (independent)। তবে test-generation RL-এ reward hacking-এর কোনো সরাসরি মাপ fact sheet-এ নেই — এটা আমার যুক্তি, পরিমাপ নয়।
