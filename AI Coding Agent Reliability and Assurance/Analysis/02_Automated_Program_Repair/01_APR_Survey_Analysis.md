# Paper Analysis 01 (APR): Automated Program Repair — Emerging Trends Pose and Expose Problems for Benchmarks

> **Sub-domain:** Automated Program Repair
> **Analysis করেছে:** SPL3 — AI Coding Agent Reliability and Assurance
> **Paper file:** `Automated Program Repair/Automated Program Repair.pdf`
> **আগের sub-domain-এর সাথে সম্পর্ক:** Sub-domain 1 (AI Coding Agents)-এর Summary-তে যে common gap (CG1–CG8) ও provisional direction ("assurance layer for agent patches") পেয়েছিলাম, এই survey সেগুলোকে কতটা শক্ত বা দুর্বল করে — তা Section ১৭-এ আলাদা করে দেখানো হয়েছে।

---

## ০. Paper-এর পরিচয় (Bibliographic Info)

| বিষয় | তথ্য |
|---|---|
| **Title** | Automated Program Repair: Emerging Trends Pose and Expose Problems for Benchmarks |
| **Authors** | Joseph Renzullo, Pemma Reiter (দুজনের সমান অবদান), Westley Weimer, Stephanie Forrest |
| **Institution** | Arizona State University (Renzullo, Reiter, Forrest), University of Michigan (Weimer); Forrest Santa Fe Institute-এর সাথেও যুক্ত |
| **Venue** | **ACM Computing Surveys (CSUR)**, Vol. 57, No. 8, Article 208, March 2025, 18 pages — ACM-এর review/survey journal |
| **DOI** | 10.1145/3704997 |
| **Timeline** | Received 20 January 2024; revised 29 August 2024; accepted 3 November 2024 |
| **Paper type** | **Survey / Review paper** — নতুন tool বা benchmark নয়; বরং 2018–2023 সালের APR গবেষণার "অডিট" |
| **Corpus** | ICSE, TSE, FSE, ASE, EMSE — এই ৫টা venue-র 118টা APR article (1 Jan 2018 – 31 Dec 2023) |
| **References** | 141টা |
| **CCS Concepts** | Search-based software engineering; Maintaining software; Machine learning algorithms |
| **Keywords** | automated program repair, machine learning, benchmarks, patch quality |
| **Funding** | NSF (CCF2211750, CCF2211749), DARPA (N6600120C4020), ARPA-H (SP4701-23-C-0074), Santa Fe Institute |
| **আমাদের domain-এ গুরুত্ব** | ⭐⭐⭐⭐⭐ — এটা APR sub-domain-এর **প্রবেশদ্বার paper**। এটা বলে দেয় APR-এর evaluation (benchmark, correctness, data leakage) কোথায় কোথায় দুর্বল — আর ঠিক এই দুর্বলতাগুলোই SWE-bench-ভিত্তিক agent evaluation-এ আবার দেখা যায় (Sub-domain 1)। |

**Authors সম্পর্কে একটা দরকারি তথ্য (আমার পর্যবেক্ষণ):** Weimer ও Forrest হলেন GenProg-এর (APR-এর সবচেয়ে বিখ্যাত প্রথম দিকের tool) সহ-লেখক, এবং ManyBugs/IntroClass benchmark-এরও সহ-লেখক (paper-এর reference [60], [61] দেখো)। অর্থাৎ যারা classic APR তৈরি করেছেন, তারাই ML-যুগের APR evaluation-কে সমালোচনা করছেন। এটা তাদের কথাকে ওজন দেয়, আবার কিছু জায়গায় (যেমন StandUp4NPR-এর সমালোচনা) তাদের দৃষ্টিভঙ্গি search-based APR-এর দিকে ঝুঁকে থাকতে পারে — Section ১২-তে আলোচনা আছে।

---

## ১. এক লাইনে Paper (TL;DR)

**2018 থেকে 2023 পর্যন্ত top-5 SE venue-র 118টা APR article পর্যালোচনা করে এই survey দেখায় যে ML ও LLM দ্রুত APR দখল করে নিয়েছে (2018-এ ছয়টার মধ্যে একটার কম article ML ব্যবহার করতো, 2023-এ চারটার মধ্যে তিনটার বেশি), কিন্তু পুরনো benchmark (Defects4J, ManyBugs ইত্যাদি) ML-এর জন্য বানানো হয়নি — তাই data leakage, contamination, ভিন্ন ভিন্ন correctness সংজ্ঞা, ভিন্ন fault localization অনুমান ও ভিন্ন stopping condition-এর কারণে published result-গুলো আসলে তুলনাযোগ্য বা বিশ্বাসযোগ্য নয়।**

### Supervisor-কে ৩০ সেকেন্ডে কীভাবে বলবো
> "Sir, এটা ACM Computing Surveys-এ 2025-এ প্রকাশিত একটা survey। Authors ICSE, TSE, FSE, ASE, EMSE-র 2018–2023-এর 118টা APR paper পড়ে দেখিয়েছেন যে ML-ভিত্তিক APR খুব দ্রুত বেড়েছে — নতুন technique-এর 61টার মধ্যে 22টা ML, তার মধ্যে 7টা LLM, আর সেই 7টার 6টাই শেষ দুই বছরে। কিন্তু সমস্যা হলো: benchmark-গুলো পুরনো ও internet-এ public, তাই LLM সম্ভবত সেগুলো training-এ দেখে ফেলেছে; কেউ near-duplicate নিয়ে কাজ করেনি; একেকজন একেকভাবে 'correct' সংজ্ঞায়িত করে; কেউ perfect fault localization ধরে নেয়, কেউ নেয় না; আর stopping condition আলাদা। ফলে paper-গুলোর সংখ্যা পাশাপাশি রেখে তুলনা করা যায় না। আমাদের জন্য গুরুত্বপূর্ণ কারণ SWE-bench-ভিত্তিক agent evaluation-এও ঠিক এই সমস্যাগুলো আছে — তাই assurance layer-কে নিজেই leakage-aware ভাবে evaluate করতে হবে।"

---

## ২. Background — এই paper বুঝতে যা আগে জানা দরকার

এই paper একটা survey, তাই এটা অনেক concept ধরে নেয় যে পাঠক আগে থেকে জানে। নিচে প্রতিটা concept সহজভাবে ব্যাখ্যা করা হলো। যেখানে Sub-domain 1-এ আগে ব্যাখ্যা করা হয়েছে, সেখানে reference দেওয়া আছে।

### ২.১ Automated Program Repair (APR) কী
APR হলো software-এর bug মানুষ ছাড়াই (বা খুব কম মানুষের সাহায্যে) ঠিক করার research field। Paper-এর ভাষায় APR-এর লক্ষ্য হলো bug repair-এ "direct human involvement" কমানো বা বাদ দেওয়া।
- **Input:** একটা buggy program + bug-এর কোনো বর্ণনা (সাধারণত অন্তত একটা failing test; কখনো bug report)।
- **Output:** একটা **patch** — code-এ পরিবর্তন, যেটা bug ঠিক করে। (Patch/diff কী, তা Sub-domain 1, Paper 01-এর ২.২ দেখো।)
- Survey-র একটা গুরুত্বপূর্ণ দাবি: APR-এর **কোনো সর্বজনস্বীকৃত formal definition নেই** — তাই একেক paper একেক রকম "task" solve করে।

### ২.২ APR-এর ইতিহাস — প্রধান ধারা

| ধারা | মূল idea | Survey-তে উল্লেখিত উদাহরণ |
|---|---|---|
| **Generate-and-validate (G&V)** | অনেক candidate patch তৈরি করো, প্রতিটা test suite দিয়ে যাচাই করো; যেটা সব test pass করে সেটাই output | GenProg, ARJA, TBar, Prophet — প্রায় সব classic tool এই কাঠামোয় |
| **Search-based / Evolutionary** | Genetic programming দিয়ে patch "বিবর্তন" করা — mutation (statement মুছা, যোগ করা, বদলানো) ও crossover; কোন patch কত test pass করে তা fitness | GenProg [61], ARJA [135] (multi-objective GP) |
| **Template-based** | মানুষের তৈরি fix pattern (যেমন null check যোগ করা, condition বদলানো) প্রয়োগ করা | TBar [72] |
| **Semantic / Constraint-based** | Symbolic execution দিয়ে "কী মান হলে test pass করবে" তা constraint আকারে বের করে, তারপর constraint solver দিয়ে code synthesize করা | Angelix [80] (multi-line, symbolic analysis) |
| **Learning-from-patches (pre-deep-learning)** | সফল human patch থেকে শেখা model দিয়ে candidate patch-কে rank করা | Prophet [74] |
| **Multi-hunk / evolution-based** | একাধিক জায়গায় edit লাগে এমন bug | [103] (Harnessing evolution for multi-hunk repair) |
| **Neural Program Repair (NPR)** | Neural network দিয়ে buggy code → fixed code "অনুবাদ" | SequenceR, CoCoNuT, CURE, DLFix, RewardRepair, Recoder, KNOD ইত্যাদি |
| **LLM-based APR** | বড় pre-trained language model দিয়ে buggy line-এর জায়গায় সঠিক code generate করা (zero-shot / fine-tuned) | AlphaRepair (CodeBERT), Xia et al. [122], SelfAPR, Fan et al. [34] |

**GenProg-এর loop (সহজ ভাষায়):**
1. Failing test ও passing test চালিয়ে দেখো কোন statement-গুলো failing test-এ বেশি execute হয় (fault localization)।
2. সেই statement-গুলোতে random mutation করো (মুছো, অন্য জায়গা থেকে statement copy করে বসাও, বদলাও)।
3. প্রতিটা variant-এর fitness = কতগুলো test pass করে।
4. ভালো variant-গুলো রেখে আবার mutation/crossover — সব test pass না করা পর্যন্ত বা সময় শেষ না হওয়া পর্যন্ত।

**গুরুত্বপূর্ণ:** GenProg-এর মতো search-based tool **আগের ধাপের ফল দেখে পরের ধাপ ঠিক করে (feedback loop)**। পরে Section ৮.১০-এ দেখবো, StandUp4NPR framework এই feedback loop সমর্থন করে না।

### ২.৩ Test-suite-based Repair
বেশিরভাগ APR-এ **test suite-ই specification**। অর্থাৎ "program সঠিক" মানে "সব test pass করে"।
- **Positive tests:** buggy program-এও pass করে (আগে যা ঠিক ছিল) — Sub-domain 1-এর PASS_TO_PASS-এর মতো।
- **Negative tests:** buggy program-এ fail করে (bug প্রকাশ করে) — FAIL_TO_PASS-এর মতো। (F2P/P2P: Sub-domain 1, Paper 01-এর ২.৫ দেখো।)

সমস্যা: test suite সবসময় অসম্পূর্ণ। তাই "সব test pass" মানেই "সঠিক" নয় — নিচের overfitting দেখো।

### ২.৪ Fault Localization (FL)
Bug-টা code-এর **কোথায়** আছে তা খুঁজে বের করা।
- **Spectrum-based FL (SBFL):** কোন line failing test-এ বেশি চলে আর passing test-এ কম চলে — সেই line-কে বেশি সন্দেহজনক ধরা। (সূত্র Section ৬.৪-এ।) Survey অনুযায়ী 22টা article test execution trace দিয়ে SBFL ব্যবহার করে।
- **IR-based FL:** bug report-এর লেখা দিয়ে কোন file সম্পর্কিত তা খোঁজা (Sub-domain 1-এর BM25-এর মতো)। Survey-র corpus-এ শুধু **iFixR** bug report-ভিত্তিক IR ব্যবহার করেছে।
- **Perfect FL:** developer আসলে কোন file/line বদলেছিল, সেটা সরাসরি tool-কে বলে দেওয়া। বাস্তবে অসম্ভব, কিন্তু অনেক NPR paper এটাই ধরে নেয়। এটা Sub-domain 1-এর SWE-bench **"Oracle retrieval"**-এর সমতুল্য (Sub-domain 1, Paper 01-এর ৫.৪ দেখো)।

**Patch generation বনাম Full repair:** Survey পরিষ্কার পার্থক্য করে —
- *Patch generation* = শুধু code modification তৈরি করা (location আগে থেকে জানা)।
- *Full automated repair* = end-to-end: fault localization + patch generation + একাধিক solution থাকলে priority/ranking।

### ২.৫ Plausible Patch, Correct Patch ও Patch Overfitting
- **Plausible patch:** যে patch সব available test pass করে।
- **Correct patch:** যে patch আসলেই bug-টা ঠিক করে, অর্থাৎ program-এর উদ্দেশ্য অনুযায়ী আচরণ করে — সাধারণত developer-এর fix-এর সাথে semantically equivalent কিনা মানুষ দিয়ে যাচাই করা হয়।
- **Patch overfitting:** patch test pass করে (plausible) কিন্তু আসলে ভুল — test suite-এর দুর্বলতার সুযোগ নেয়। যেমন: শুধু failing test-এর input-এর জন্য special case যোগ করা।

Survey-র Table 1-এ "overfitting" (5 বার), "correctness" (5 বার), "assessment" (4 বার) keyword-গুলোকে আলাদাভাবে **patch correctness** theme হিসেবে চিহ্নিত করা হয়েছে — অর্থাৎ APR community এটাকে একটা স্বতন্ত্র research topic মনে করে। Sub-domain 1-এ AutoCodeRover-এর 78টা test-pass patch-এর মধ্যে মাত্র 51টা সঠিক ছিল — এটাই overfitting-এর বাস্তব উদাহরণ (Sub-domain 1 Summary-র ৩.১ দেখো)।

**Patch correctness assessment (APCA) tool:** কোন plausible patch overfitting তা স্বয়ংক্রিয়ভাবে বলার tool। Survey-তে উল্লেখিত: Overfitting Detection System (ODS) [130], Invalidator [59], Quatrain [112], Tian et al. [111]।

### ২.৬ APR Benchmarks (Survey যেগুলো উল্লেখ করেছে)

| Benchmark | Language | কী ধরনের | Survey কী বলে |
|---|---|---|---|
| **Defects4J** [52] | Java | আসল open-source Java library-র আসল bug, developer test সহ; Maven build infrastructure আছে | Corpus-এর 44টা article এটা দিয়ে evaluate করেছে — সবচেয়ে জনপ্রিয় |
| **ManyBugs** [60] | C | বড় open-source C program-এর bug | পুরনো, build support অসম্পূর্ণ — মাত্র 5টা article-এ data আছে, তার মধ্যে মাত্র 2টা নতুন experiment |
| **IntroClass** [60] | C | ছাত্রদের (novice) লেখা ছোট program | ছোট বলে পুরো development history benchmark-এর মধ্যে রাখা যায় |
| **CodeFlaws** [110] | C | Programming competition-এর program | IntroClass-এর মতো, history ছোট |
| **QuixBugs** [70] | Multi-lingual (Python, Java) | Quixey challenge-এর ছোট algorithmic program | APR benchmark হিসেবে উল্লেখিত; ML train করার জন্য ছোট |
| **Bugs.jar** [102] | Java | বড় মাপের real-world Java bug | ODS-এর training set-এর অংশ |
| **Bears** [79] | Java | Extensible Java bug benchmark | ODS-এর training set-এর অংশ |
| **CrossVul** [89] | বহু language | Vulnerability-fix commit-এর diff — **ML dataset**, benchmark নয় | Build/test environment নেই — শুধু program text |
| **RunBugRun** [97] | — | Executable APR dataset | ML-ভিত্তিক tool সম্প্রতি build reproduce করা শুরু করেছে — তার উদাহরণ |

**Benchmark বনাম ML dataset (খুব গুরুত্বপূর্ণ পার্থক্য):**
- *APR benchmark:* কম সংখ্যক কিন্তু যত্ন করে বানানো bug/fix pair, test case ও build environment সহ — **evaluation**-এর জন্য।
- *ML dataset:* লক্ষ লক্ষ bug-fix pair (যেমন SynShine-এর 1.7M pair), কিন্তু test বা build নেই — **training**-এর জন্য।
- APR benchmark ML train করার জন্য খুব ছোট; আর ML dataset execution-based evaluation-এর জন্য অনুপযুক্ত।

### ২.৭ Neural Machine Translation (NMT) ও Transformer
- **NMT:** neural network দিয়ে এক ভাষা থেকে আরেক ভাষায় অনুবাদ (যেমন English → Bangla)। APR-এ idea হলো: **buggy code → fixed code** একটা "অনুবাদ"।
- **Encoder-decoder:** encoder input-কে একটা latent representation-এ রূপান্তর করে; decoder সেখান থেকে output token একটা একটা করে তৈরি করে। আগে LSTM দিয়ে, এখন transformer দিয়ে।
- **Transformer architecture-এর তিন রূপ:**
  - *Encoder-only* (যেমন BERT, CodeBERT) — বোঝার কাজে ভালো, zero-shot generation-এ সীমিত।
  - *Decoder-only* (যেমন GPT, Codex) — generation-এ ভালো।
  - *Encoder-decoder* (যেমন T5, CodeT5, PLBART) — অনুবাদ-ধরনের কাজে।
- **Attention:** output-এর প্রতিটা token তৈরির সময় input-এর কোন অংশে "মনোযোগ" দিতে হবে তা শেখা। এতে বিভিন্ন দৈর্ঘ্যের input সামলানো যায় — code-এর দৈর্ঘ্য ও গঠন খুব বৈচিত্র্যময় বলে APR-এ এটা জরুরি। Survey দুইটা বিখ্যাত attention-এর উল্লেখ করে: Vaswani (transformer-এর multi-head self-attention) ও Luong (NMT-এর global/local attention)।

### ২.৮ PLM, LLM ও Code LLM
- **Pre-trained Language Model (PLM):** বিশাল text corpus-এ আগে থেকে train করা model; পরে নির্দিষ্ট কাজে fine-tune করা যায়।
- **LLM:** খুব বড় PLM, সাধারণত billion বা তার বেশি parameter। (Fine-tuning ও LoRA: Sub-domain 1, Paper 01-এর ২.৮ দেখো।)
- **Code LLM:** GitHub, StackOverflow-এর code দিয়ে train করা model (Codex, CodeT5, CodeBERT, PLBART)।
- **LLM-এর APR paradigm (survey অনুযায়ী):** NMT-যুগে "buggy code-কে fixed code-এ অনুবাদ"; LLM-যুগে **"buggy line মুছে ফেলো, তারপর generative model দিয়ে ফাঁকা জায়গা পূরণ করো"** (infilling / cloze-style)।

### ২.৯ Beam Search
Model প্রতিটা ধাপে পরের token-এর জন্য অনেক বিকল্প দেয়। **Beam search** প্রতিটা ধাপে সবচেয়ে ভালো k-টা আংশিক sequence রাখে (k = beam size)।
- k = 1 হলে এটা greedy decoding (Sub-domain 1, Paper 01-এর ২.১০ দেখো)।
- k খুব বড় হলে প্রায় exhaustive search।
- NPR tool সাধারণত beam search দিয়ে একটা bug-এর জন্য অনেকগুলো candidate patch তৈরি করে। (সূত্র Section ৬.৯-এ।)

### ২.১০ Data Bias
Dataset-এ কিছু feature কম বা বেশি থাকলে model-এর ফল বিকৃত হয়। Survey-র উদাহরণ: Codex তার training data থেকে auto-generated code বলে সন্দেহ হলে বাদ দেয় — তাই Codex-ভিত্তিক NPR model algorithm দিয়ে তৈরি code-এ খারাপ করতে পারে। Survey বলছে, তাদের পড়া কোনো article data bias নিয়ে স্পষ্টভাবে আলোচনা করেনি।

### ২.১১ Data Leakage বনাম Contamination (এই paper-এর কেন্দ্রীয় concept)
- **Data leakage (ML-এর সাধারণ অর্থ):** training data-তে এমন তথ্য থাকে যেটা prediction-এর সাথে সম্পর্কিত এবং যা model-এর পাওয়ার কথা নয় — ফলে নতুন data-তে performance-এর অতিরিক্ত আশাবাদী অনুমান হয়।
- **Contamination:** নির্দিষ্টভাবে **test/benchmark-এর উদাহরণ (বা তার কাছাকাছি কপি) training data-তে ঢুকে যাওয়া**। Survey বলে, duplicate data model-কে নির্দিষ্ট উদাহরণের দিকে bias করে এবং **memorization**-এর সম্ভাবনা বাড়ায়; ফলে reported performance বাস্তবে পাওয়া যায় না।
- **সম্পর্ক:** contamination হলো leakage-এর একটা রূপ; survey memorization-কেও "a type of data leakage" বলেছে।
- **কেন LLM-এ সমস্যা বেশি:** (ক) pre-trained weight উত্তরাধিকারসূত্রে আসে — end-user training set থেকে duplicate সরাতে পারে না; (খ) training corpus প্রায়ই প্রকাশিত নয় — তাই বাইরের কেউ benchmark decontaminate-ও করতে পারে না। (Sub-domain 1, Paper 01-এর ২.৯-ও দেখো।)

### ২.১২ Code Clone Types (Duplication-এর মাত্রা)
Survey Roy & Cordy-র clone classification ব্যবহার করে:

| Clone type | মানে | উদাহরণ |
|---|---|---|
| **Type I** | হুবহু একই (শুধু whitespace/comment আলাদা) — exact duplication | একই function দুই project-এ copy-paste |
| **Type II** | গঠন একই, শুধু identifier/literal/type-এর নাম আলাদা — near-duplicate | `if (a > b) return a;` বনাম `if (x > y) return x;` |
| **Type III** | কিছু statement যোগ/বাদ/পরিবর্তন সহ copy — near-duplicate | StackOverflow-এর একটা solution অনেক project-এ সামান্য বদলে ব্যবহার |

**Granularity:** duplication statement, function, class, file — যেকোনো স্তরে হতে পারে। Code model-এ dedup সাধারণত **file level**-এ হয় — ফলে function-level duplicate রয়ে যায়।

### ২.১৩ Memorization ও Generalization
- **Memorization:** model training data-র sequence হুবহু তৈরি করে, অর্থ না বুঝে।
- **Generalization:** আগে না দেখা input-এও ঠিক কাজ করা।
- APR-এ memorization মিশ্র ফল দেয়: duplicate bug হলে সাহায্য করে, কিন্তু নতুন bug-এ generalize করতে বাধা দেয়। আর evaluation-এ memorization থাকলে score "ক্ষমতা" নয়, "স্মৃতি" মাপে।

### ২.১৪ Benchmark Validity
একটা benchmark score যা মাপার দাবি করে, সত্যিই তা মাপে কিনা — এটাই validity।
- **Internal validity:** ফলাফলের পার্থক্য কি সত্যিই technique-এর জন্য, নাকি অন্য কারণে (ভিন্ন FL অনুমান, ভিন্ন stopping rule, contamination)?
- **Construct validity:** "correct" বলতে যা মাপা হচ্ছে (reference patch-এর সাথে মিল / test pass) তা কি আসল correctness?
- **External validity:** benchmark-এর ফল কি বাস্তব software-এ generalize করে?
- Survey-র মূল যুক্তি: ML-যুগে এই তিনটাই হুমকির মুখে।

### ২.১৫ Living Review, Machine Unlearning, Canary String
- **Living review:** নিয়মিত update হওয়া survey — Monperrus-এর *The Living Review on Automated Program Repair* (hal-01956501)। এই survey-র seed।
- **Machine unlearning:** pre-trained model থেকে নির্দিষ্ট data-র প্রভাব সরিয়ে ফেলা (retrain বা approximate)। মূলত privacy/security-র জন্য; 2023-এ NeurIPS-এ এর challenge ঘোষিত হয়।
- **Canary string:** ইচ্ছা করে dataset-এ বসানো একটা অদ্ভুত, সহজে চেনা যায় এমন synthetic string। Model যদি পরে সেটা হুবহু তৈরি করে, বোঝা যায় dataset-টা training-এ ছিল।

---

## ৩. Problem Statement — কী সমস্যা ছিল?

### ৩.১ মূল সমস্যা
1. **ML/LLM APR-কে দ্রুত দখল করছে, কিন্তু evaluation পুরনো:** সবচেয়ে জনপ্রিয় APR benchmark-গুলো ML technique-এর কথা মাথায় রেখে বানানো হয়নি।
2. **Data leakage ও contamination:** LLM-এর বিশাল ও প্রায়ই অপ্রকাশিত training data-তে benchmark-এর bug (বহু বছরের পুরনো, internet-এ public) থাকার সম্ভাবনা বেশি।
3. **APR-এর formal definition নেই:** তাই একেক paper একেক task solve করে।
4. **Evaluation design-এ অসামঞ্জস্য।** Survey ৩টা "motivating example" দিয়ে শুরু করে:

| Dimension | একজন যা করে | আরেকজন যা করে | সমস্যা |
|---|---|---|---|
| **Correctness** | CURE: সব test pass + developer fix-এর সাথে semantically equivalent (দুজন author manual review করে একমত) | Codex: Leetcode-এর public ও private test case | দুটোই যুক্তিসঙ্গত, কিন্তু তুলনা করা কঠিন |
| **Fault Localization** | Sequencer: কোন line বদলাতে হবে তা input-এ দেওয়া (perfect FL) | iFixR: মানুষের লেখা bug report দিয়ে fault খোঁজে; আগের বেশিরভাগ APR: FL task-এর অংশ | ভিন্ন কঠিনতার task |
| **Termination** | RewardRepair: bug প্রতি সেরা 200টা patch তৈরি ও যাচাই করে থামে (সময় যতই লাগুক) | CURE: 10,000 candidate তৈরি, top 5,000 যাচাই; DLFix: নির্দিষ্ট সময়-বাজেট শেষ হলে থামে | Efficiency তুলনা অসম্ভব |

### ৩.২ কেন এটা গুরুত্বপূর্ণ?
- যদি score contamination বা সহজ অনুমানের (perfect FL) কারণে ফুলে থাকে, তাহলে "state-of-the-art" দাবি ভুল হতে পারে — আর industry ভুল tool গ্রহণ করতে পারে।
- Authors-এর কড়া উপসংহার: এই সমস্যাগুলো সমাধান না হলে **"আরও বেশি ও বড় empirical study ও তুলনা কোনো আলো দেবে না"**।
- আমাদের domain-এর জন্য: "Reliability and Assurance" মাপতে হলে আগে নিশ্চিত হতে হবে যে **মাপার যন্ত্রটাই (benchmark + protocol) নির্ভরযোগ্য**।

---

## ৪. Goal ও Research Questions

**Goal:** Top-5 SE venue-তে 2018 থেকে প্রকাশিত APR গবেষণার একটা topical review — বিশেষ করে ML/LLM-এর উত্থান, এবং এই নতুন পদ্ধতি benchmark-ভিত্তিক evaluation-এর কোন সমস্যা **তৈরি করে (pose)** ও **উন্মোচন করে (expose)** — তা দেখানো; যেখানে সমাধানের ইঙ্গিত আছে সেখানে তা দেওয়া।

Survey-তে RQ স্পষ্টভাবে লেখা নেই; section গঠন থেকে implicit RQ:
- **RQ1 (Section 3):** Top venue-তে APR-এ ML/LLM কতটা ও কত দ্রুত ছড়িয়েছে? কোন architecture ব্যবহৃত হচ্ছে, attention কীভাবে report করা হচ্ছে?
- **RQ2 (Section 4):** ML-ভিত্তিক APR paper-গুলো data leakage ও contamination কীভাবে সামলায় (বা সামলায় না)? Decontamination, memorization, granularity, near-duplicate নিয়ে অবস্থা কী?
- **RQ3 (Section 5):** Benchmark কি standardized evaluation নিশ্চিত করে? Performance reporting, FL, correctness, dataset size, history access, build reproducibility, search-efficiency reporting-এ কী পার্থক্য আছে?
- **RQ4 (Section 6):** নতুন উদ্যোগ (StandUp4NPR, APR-COMP 2024) কি এই সমস্যা সমাধান করে?

---

## ৫. Methodology — Review কীভাবে করা হয়েছে

### ৫.১ Review Pipeline (ধাপে ধাপে)

| ধাপ | কী করা হয়েছে | Output |
|---|---|---|
| 1. Seed | Monperrus-এর *The Living Review of Automated Program Repair* (hal-01956501, **version 5**) বিশ্লেষণ | APR article-এর একটা বড় তালিকা |
| 2. Venue selection | Living review-তে **সবচেয়ে বেশি APR article প্রকাশকারী ৫টা venue** বাছাই | ICSE, TSE, FSE, ASE, EMSE |
| 3. Time window | **1 January 2018 থেকে 31 December 2023** — প্রতিটা venue স্বাধীনভাবে পর্যালোচনা | ৬ বছরের সব article |
| 4. Primary keyword | Article metadata-তে **patch** বা **repair** | Primary work |
| 5. Secondary keyword | **automate, fix, fault, bug, vulnerability, generate** (stem/variant সহ) | সম্ভাব্য related work |
| 6. Manual abstract review | যেকোনো keyword match হলে abstract পড়ে APR-related theme আছে কিনা দেখা | Inclusion/exclusion |
| 7. Final corpus | — | **118টা article** |
| 8. Cross-check | Living review-এর সাথে মিলানো | মাত্র **65টা** living review-তেও আছে |

### ৫.২ Venue পাঁচটা কী

| Venue | ধরন |
|---|---|
| ICSE — International Conference on Software Engineering | Conference |
| TSE — IEEE Transactions on Software Engineering | Journal |
| FSE — Foundations of Software Engineering (ESEC/FSE) | Conference |
| ASE — Automated Software Engineering | Conference |
| EMSE — Empirical Software Engineering | Journal |

### ৫.৩ Categorisation (Taxonomy Dimensions)
Abstract অনুযায়ী ML-ভিত্তিক article-গুলোকে **structural** ও **functional** dimension-এ ভাগ করা হয়েছে। Paper-এ আলাদা taxonomy table নেই; section গুলো থেকে dimension-গুলো এভাবে বের করা যায় (আমার পর্যবেক্ষণ — paper-এর text থেকে সাজানো):

| Dimension | ধরন | মান (category) | Paper-এর section |
|---|---|---|---|
| ML ব্যবহার করে কিনা | Functional | ML-keyword আছে / নেই; নতুন technique / অন্য (empirical, assessment) | 3, 3.1 |
| Model family | Structural | Transformer; BiLSTM classifier; RNN generator; ASTNN representation; CNN feature learner | 3.3 |
| Transformer রূপ | Structural | Encoder (CodeBERT), Decoder (GPT/Codex), Encoder-decoder (CodeT5, PLBART) | 2.1, 3.3 |
| ML-এর ভূমিকা | Functional | Patch generation; classifier (যেমন FL/patch correctness); code representation; fix-pattern learning | 3.3 |
| Attention reporting | Structural/reporting | উল্লেখ নেই / বিস্তারিত / research cite / সংক্ষিপ্ত / inherited model cite | 3.4 |
| Leakage handling | Evaluation | Temporal split; project-based split; random split; কোনো split নেই; dedup (syntax/semantics/অনির্দিষ্ট); কিছুই না | 4.1, 4.2 |
| FL assumption | Evaluation | SBFL (test trace); perfect FL (developer location); IR (bug report); দুই setting-ই report | 5.2 |
| Correctness definition | Evaluation | একটা human reference patch-এর সাথে তুলনা; test pass; manual semantic equivalence | 1, 5.3 |
| Benchmark | Evaluation | Defects4J, ManyBugs, অন্যান্য | 5.6 |
| Efficiency reporting | Evaluation | Run-time; wall-clock upper bound; test-suite evaluation limit; beam size; vocabulary size | 5.1, 5.7 |

### ৫.৪ Keyword analysis
Author-দের নিজেদের বেছে নেওয়া keyword গুনে Table 1 বানানো হয়েছে (শুধু যেগুলো ৪ বা তার বেশি বার এসেছে)। ML-সম্পর্কিত keyword ও patch-correctness keyword আলাদা চিহ্ন দিয়ে tag করা হয়েছে (পূর্ণ table Section ৮.২-এ)।

---

## ৬. Mathematical Formulation — সূত্র ও ব্যাখ্যা

Survey নিজে কোনো equation দেয়নি — এটা qualitative ও count-ভিত্তিক review। কিন্তু survey যে evaluation concept-গুলো নিয়ে আলোচনা করে (plausible বনাম correct, overfitting, FL, leakage, contamination, near-duplicate, beam search, stopping condition), সেগুলো formal ভাবে লিখলে supervisor-কে অনেক পরিষ্কারভাবে বোঝানো যায়। **নিচের formalization আমার নিজের সাজানো (আমার পর্যবেক্ষণ); শুধু যেখানে "paper-এর সংখ্যা" বলা আছে, সেগুলো paper থেকে নেওয়া।**

### ৬.১ APR Problem-এর Formal রূপ
$$
\text{APR}: (P,\; T) \to p, \qquad T = T_{pos} \cup T_{neg}
$$

| Symbol | মানে |
|---|---|
| $P$ | buggy program |
| $T$ | test suite (specification-এর proxy) |
| $T_{pos}$ | positive test — buggy program-এও pass করে (P2P-এর মতো) |
| $T_{neg}$ | negative test — buggy program-এ fail করে, bug প্রকাশ করে (F2P-এর মতো) |
| $p$ | patch |
| $P \oplus p$ | patch apply করার পর program |
| $S$ | আসল (অলিখিত) specification — program-এর যা করা উচিত |
| $p^{*}$ | developer-এর reference (human) patch |

### ৬.২ Plausible, Correct ও Overfitting Patch
**Plausible:**
$$
\text{Plausible}(p) = 1 \quad \text{যদি} \quad \forall t \in T:\; \text{pass}(P \oplus p,\; t)
$$
**আদর্শ Correct** (সব সম্ভাব্য input $x$-এ specification মেনে চলে):
$$
\text{Correct}(p) = 1 \quad \text{যদি} \quad \forall x \in \mathcal{X}:\; (P \oplus p)(x) = S(x)
$$
**Overfitting:**
$$
\text{Overfit}(p) = \text{Plausible}(p) \land \neg\, \text{Correct}(p)
$$
**সহজ ভাষায়:** test pass করেছে, কিন্তু আসলে ভুল। সমস্যা হলো $S$ কারো হাতে নেই — তাই বাস্তবে "Correct" মাপতে proxy লাগে।

### ৬.৩ Survey-তে দেখা দুই ধরনের Correctness Proxy
**(ক) CURE-ধরনের (paper-এর motivating example):** সব test pass **এবং** developer fix-এর সাথে semantically equivalent (মানুষ দিয়ে যাচাই):
$$
\text{Correct}_{\text{CURE}}(p) = \text{Plausible}(p) \land \text{SemEq}(P \oplus p,\; P \oplus p^{*})
$$
**(খ) Single-reference proxy (survey অনুযায়ী 29টা cited article এই ধরনের):** generated patch-কে একটা মাত্র human reference patch-এর সাথে তুলনা:
$$
\text{Correct}_{\text{ref}}(p) = \mathbb{1}\left[\, \text{Equiv}(p,\; p^{*}) \,\right]
$$
এখানে $\text{Equiv}$ মানে "একই বা সমতুল্য" (syntactic match বা manual equivalence — paper অনুযায়ী ভিন্ন)।

**আমার পর্যবেক্ষণ — "Sandwich" সম্পর্ক:** ধরো $\mathcal{C}$ = সব সঠিক patch-এর set, $\mathcal{P}$ = সব plausible patch-এর set। Test যদি specification-এর অংশ হয় (সঠিক patch অবশ্যই test pass করে) এবং reference-match সত্যিই সঠিক patch চিনতে পারে, তাহলে
$$
\{\, p : \text{Equiv}(p,\; p^{*}) \,\} \subseteq \mathcal{C} \subseteq \mathcal{P}
$$
অর্থাৎ একটা tool-এর জন্য গণনা করলে:
$$
N_{\text{ref}} \;\leq\; N_{\text{correct}} \;\leq\; N_{\text{plausible}}
$$
- **বাম দিক (reference proxy)** আসল correctness-কে **কম গোনে** — survey-র অভিযোগ: "যেকোনো functionality implement করার অসীম উপায় আছে", তাই একটা human example-এর সাথে মেলানো "extraordinarily strict"।
- **ডান দিক (শুধু test pass)** আসল correctness-কে **বেশি গোনে** — এটাই patch overfitting, Sub-domain 1-এর CG1।
- **SWE-bench ডান দিকের metric ব্যবহার করে** (F2P + P2P pass = resolved)। তাই SWE-bench score আসল correctness-এর **upper bound**, আর survey যে reference-proxy-র সমালোচনা করে তা **lower bound**। আসল সংখ্যা মাঝখানে কোথাও। Assurance layer-এর কাজ হলো এই ফাঁক ছোট করা।

### ৬.৪ Patch Precision ও Overfitting Rate (APR-এ প্রচলিত metric)
$$
\text{Precision}_{\text{patch}} = \frac{N_{\text{correct}}}{N_{\text{plausible}}}, \qquad \text{OverfitRate} = 1 - \text{Precision}_{\text{patch}}
$$
**Worked example (Sub-domain 1-এর সংখ্যা, AutoCodeRover):** 78টা plausible patch, তার মধ্যে 51টা সঠিক।
$$
\text{Precision}_{\text{patch}} = \frac{51}{78} = 0.654 = 65.4\%, \qquad \text{OverfitRate} = 1 - 0.654 = 34.6\%
$$
অর্থাৎ 27টা patch overfitting।

### ৬.৫ Overfitting Detector (APCA tool যেমন ODS)-এর মূল্যায়ন
Overfitting patch-কে "positive" ধরে:

| | আসলে overfitting | আসলে correct |
|---|---|---|
| Detector বলে overfitting | TP | FP |
| Detector বলে correct | FN | TN |

$$
\text{Precision}_{\text{det}} = \frac{TP}{TP + FP}, \qquad \text{Recall}_{\text{det}} = \frac{TP}{TP + FN}
$$
**Worked example (আমার কাল্পনিক উদাহরণ, উপরের 78টা patch দিয়ে):** ধরো detector 30টা patch-কে overfitting বলে, তার মধ্যে 22টা আসলেই overfitting (TP = 22, FP = 8)। মোট overfitting 27, তাই FN = 5।
$$
\text{Precision}_{\text{det}} = \frac{22}{30} = 73.3\%, \qquad \text{Recall}_{\text{det}} = \frac{22}{27} = 81.5\%
$$
FP = 8 মানে 8টা সঠিক patch ভুল করে বাতিল হলো — assurance layer-এ এটাই "useful patch হারানোর" খরচ।

**Survey-র সংযোগ:** ODS নিজের training set (Bugs.jar, Bears, Defects4J) থেকে test set আলাদা করেছে **project-ভিত্তিক** ভাবে (৬.৭ দেখো)। অর্থাৎ overfitting detector-এর evaluation-ও leakage-এর ঝুঁকিতে থাকে।

### ৬.৬ Spectrum-based Fault Localization (Ochiai — background সূত্র)
Survey SBFL-এর উল্লেখ করে কিন্তু সূত্র দেয় না। সবচেয়ে প্রচলিত একটা SBFL সূত্র (Ochiai):
$$
\text{Ochiai}(s) = \frac{e_f(s)}{\sqrt{\left(e_f(s) + n_f(s)\right)\left(e_f(s) + e_p(s)\right)}}
$$

| Symbol | মানে |
|---|---|
| $e_f(s)$ | statement $s$-কে execute করে এমন failing test-এর সংখ্যা |
| $n_f(s)$ | $s$-কে execute **করে না** এমন failing test-এর সংখ্যা |
| $e_p(s)$ | $s$-কে execute করে এমন passing test-এর সংখ্যা |

**Worked example (কাল্পনিক):** মোট 2টা failing test।
- Statement $s_1$: দুটো failing test-ই চালায়, 1টা passing test চালায় → $\dfrac{2}{\sqrt{(2+0)(2+1)}} = \dfrac{2}{2.449} = 0.816$
- Statement $s_2$: 1টা failing, 5টা passing test চালায় → $\dfrac{1}{\sqrt{(1+1)(1+5)}} = \dfrac{1}{3.464} = 0.289$

তাই $s_1$ বেশি সন্দেহজনক।

**Perfect FL কেন score ফোলায় (আমার সরল মডেল):** ধরো repair তখনই সম্ভব যখন সঠিক location $L^{*}$ পাওয়া যায়:
$$
\text{Pr}(\text{repair}) = \text{Pr}(\text{FL finds } L^{*}) \cdot \text{Pr}(\text{correct patch} \mid L^{*})
$$
Perfect-FL paper শুধু দ্বিতীয় গুণফল report করে। **কাল্পনিক উদাহরণ:** FL 60% ক্ষেত্রে সঠিক জায়গা পায়, আর location দিলে 50% bug ঠিক হয় → end-to-end = 0.6 × 0.5 = 30%, কিন্তু perfect-FL paper report করবে 50%। অর্থাৎ $1/0.6 = 1.67$ গুণ বেশি দেখাবে।
**Sub-domain 1-এর বাস্তব উদাহরণ:** SWE-bench-এ Claude 2: BM25 retrieval-এ 1.96%, Oracle (perfect file localization)-এ 4.80% → $4.80/1.96 \approx 2.45$ গুণ। Survey-র Section 5.2-এর সতর্কবাণী ঠিক এখানেই প্রযোজ্য।

### ৬.৭ Data Leakage ও Split Strategy
**Exact duplication (Type I):**
$$
|D_{\text{train}} \cap D_{\text{test}}| > 0
$$
**Temporal split** (SelfAPR ও CURE-এর পদ্ধতি):
$$
\forall x \in D_{\text{train}},\; \forall y \in D_{\text{test}}:\; \text{time}(x) < t_{\text{cut}} \leq \text{time}(y)
$$
**Paper-এর সংখ্যা:** CURE 2006-এর আগের data-তে train করেছে, কারণ benchmark-গুলো 2007 থেকে শুরু।
**সীমাবদ্ধতা:** নিজের train করা model-এ এটা নিশ্চিত করা যায়; কিন্তু pre-trained LLM-এর corpus-এর তারিখ ও বিষয়বস্তু জানা না থাকলে এই শর্ত যাচাই করা যায় না।

**Project-based split** (ODS-এর পদ্ধতি):
$$
|\text{Proj}(D_{\text{train}}) \cap \text{Proj}(D_{\text{test}})| = 0
$$
**Paper-এর উদাহরণ:** Apache Math library-র মতো যে project একাধিক source-এ (Bugs.jar, Bears, Defects4J) আছে, সেটা বাদ দেওয়া হয়েছে — কারণ random split-এ duplicate দুই দিকে চলে যেতে পারে।

**Random split-এ leakage-এর সম্ভাবনা (আমার হিসাব, SynShine-এর সংখ্যা দিয়ে):** SynShine 1.7M pair থেকে random 100K test set বেছেছে। Test fraction:
$$
f = \frac{100{,}000}{1{,}700{,}000} = \frac{1}{17} \approx 0.0588
$$
যদি কোনো sample-এর একটা হুবহু/near-duplicate যমজ dataset-এ থাকে, তাহলে test-এ পড়া sample-টার যমজ train-এ থাকার সম্ভাবনা প্রায়
$$
1 - f \approx 0.941
$$
আর যমজের $m$টা কপি থাকলে অন্তত একটা train-এ থাকার সম্ভাবনা $1 - f^{m}$ (যেমন $m = 2$ হলে $1 - 0.0035 = 0.9965$)। একটা duplicate pair train ও test-এ ভাগ হয়ে যাওয়ার সম্ভাবনা:
$$
2f(1-f) = 2 \times 0.0588 \times 0.9412 \approx 0.111
$$
**মানে:** dedup না করে random split করলে, test-এর প্রায় প্রতিটা duplicated sample-এর যমজ training-এ থেকে যায় — এজন্যই survey dedup ও project/temporal split-এর উপর জোর দেয়। (Paper বলেনি SynShine-এর data-তে কত duplicate আছে; এই হিসাব শুধু ঝুঁকি দেখায়।)

### ৬.৮ Near-duplicate Contamination Rate
Similarity function $\text{sim}$ ও threshold $\tau$ ধরে:
$$
\text{Cont}_{\tau} = \frac{1}{|D_{\text{test}}|} \sum_{y \in D_{\text{test}}} \mathbb{1}\left[\, \max_{x \in D_{\text{train}}} \text{sim}(x, y) \geq \tau \,\right]
$$
একটা সরল sim হলো token set-এর Jaccard:
$$
J(A, B) = \frac{|A \cap B|}{|A \cup B|}
$$
**Worked example (Type II clone, আমার হিসাব):** `if (a > b) return a;` ও `if (x > y) return x;`
- Raw token set: প্রথমটা {if, (, a, >, b, ), return, ;} = 8, দ্বিতীয়টা {if, (, x, >, y, ), return, ;} = 8; common = {if, (, >, ), return, ;} = 6; union = 8 + 8 − 6 = 10 → $J = 6/10 = 0.6$।
- Identifier-কে `ID` দিয়ে normalize করলে দুটোই {if, (, ID, >, ), return, ;} → $J = 7/7 = 1.0$।

**শিক্ষা:** exact-match dedup এই clone ধরবে না (J = 0.6), কিন্তু code-aware normalization (clone detection-এর পদ্ধতি) ধরবে। Survey ঠিক এটাই বলে — "Existing methods for deduplication often search for and remove exact matches. This is insufficient" — এবং NLP-র similarity measure-এর বদলে code clone detection ও code similarity metric ব্যবহার করতে বলে।

**N-gram overlap (GPT-3-ধরনের) contamination flag:**
$$
\text{Flag}(y) = \mathbb{1}\left[\, |\text{Ngrams}_N(y) \cap \text{Ngrams}_N(D_{\text{train}})| > 0 \,\right]
$$
Survey অনুযায়ী GPT-3-এ "gram" = lowercase, whitespace দিয়ে আলাদা, punctuation ছাড়া শব্দ; GPT-4 "multi-sample substring matching" ব্যবহার করেছে। (Survey $N$-এর মান বলেনি।) **Code-এর জন্য সমস্যা:** punctuation বাদ দিলে code-এর গঠন হারায়; আর training corpus না থাকলে বাইরের কেউ এটা চালাতেই পারে না।

### ৬.৯ Near-duplicate-এর কারণে Score Inflation
Survey (Allamanis 2019 উদ্ধৃত করে) বলে near-duplicate থাকলে metric de-duplicated corpus-এর তুলনায় **সর্বোচ্চ 100% পর্যন্ত** ফুলে যেতে পারে:
$$
\text{Inflation} = \frac{M_{\text{dup}} - M_{\text{dedup}}}{M_{\text{dedup}}} \leq 1 \quad (\text{অর্থাৎ } 100 \text{ শতাংশ})
$$
**Worked example (কাল্পনিক):** dedup করা corpus-এ accuracy 20% হলে, duplicate-যুক্ত corpus-এ সেটা 40% পর্যন্ত দেখাতে পারে। অর্থাৎ একটা paper-এর "দ্বিগুণ উন্নতি" পুরোটাই contamination-এর ফল হতে পারে।

সমানভাবে লেখা যায়:
$$
M_{\text{dup}} \leq 2 \times M_{\text{dedup}}
$$

### ৬.১০ Memorization, Membership ও Canary
**Verbatim memorization** (training sequence $s = (s_1, \ldots, s_n)$, prefix দিলে বাকিটা হুবহু তৈরি করে):
$$
\text{Mem}(s) = \mathbb{1}\left[\, \text{Gen}_{\theta}(s_{1:j}) = s_{j+1:n} \,\right], \qquad s \in D_{\text{train}}
$$
**Entropy/likelihood gap (ধারণাগত):** model-এর per-token negative log-likelihood
$$
\bar{H}(D) = -\frac{1}{|D|} \sum_{y \in D} \frac{1}{|y|} \sum_{i} \log p_{\theta}(y_i \mid y_{<i})
$$
যদি benchmark-এর $\bar{H}$ একই ধরনের কিন্তু নিশ্চিতভাবে নতুন data-র চেয়ে অনেক কম হয়, সন্দেহ হয় যে benchmark training-এ ছিল। **Survey-র সতর্কতা:** এর জন্য model-এর probability লাগে — শুধু API access থাকলে প্রায়ই সম্ভব নয়।

**Canary:** dataset-এ একটা অনন্য string $c$ বসাও; পরে
$$
\text{Leaked} = \mathbb{1}\left[\, c \in \text{Gen}_{\theta}(\text{prefix}(c)) \,\right]
$$

**Identifier perturbation (survey-র দ্বিতীয় পথ, আমার formalization):** $\pi$ = variable ও user-defined type-এর নাম বদলানো (অর্থ একই থাকে)। Robust model-এর জন্য
$$
\Delta_{\pi} = \text{Acc}(D_{\text{test}}) - \text{Acc}(\pi(D_{\text{test}})) \approx 0
$$
$\Delta_{\pi}$ বড় হলে বোঝা যায় model নাম মুখস্থ করে কাজ করছিল। **কাল্পনিক উদাহরণ:** original-এ 40%, renamed-এ 28% → $\Delta_{\pi} = 12$ percentage point।

### ৬.১১ Beam Search ও "Effective Search Size"
Step $t$-এ beam $B_t$:
$$
B_t = \text{top}_k \left\{ (y_{<t}, v) : y_{<t} \in B_{t-1},\; v \in Y \right\}, \qquad \text{score}(y_{1:t}) = \sum_{i=1}^{t} \log p_{\theta}(y_i \mid x,\, y_{<i})
$$

| Symbol | মানে |
|---|---|
| $k$ | beam size — প্রতিটা step-এ কতগুলো আংশিক sequence রাখা হয় |
| $Y$ | model-এর generative vocabulary (token-এর set); এর আকারই paper-এর vocabulary size |
| $x$ | input (buggy code + context) |
| $L$ | output sequence-এর দৈর্ঘ্য |

প্রতিটা step-এ score করতে হয় এমন candidate:
$$
\text{Cand}_{\text{step}} = k \times |Y|
$$
**Survey-র যুক্তি:** শুধু $k$ দিয়ে search efficiency তুলনা করা যায় না, কারণ $|Y|$ ও sequence length বাদ যায়; আর কিছু paper $|Y|$ report-ই করেনি (KNOD [49], DLFix [69])।

**Paper-এর সংখ্যা দিয়ে আমার হিসাব:**

| Tool | k (paper) | Vocabulary size V (paper) | k × V প্রতি step (আমার হিসাব) |
|---|---|---|---|
| SeqTrans | 1 থেকে 50 | 8,000 | 8,000 থেকে 400,000 |
| VRepair | 50 | 5,000 | 250,000 |
| RewardRepair | 30 / 100 / 200 / 500 | 32,128 | 963,840 / 3,212,800 / 6,425,600 / 16,064,000 |
| CURE | 1,000 | 50,000 | 50,000,000 |

- CURE ও VRepair-এর অনুপাত: $50{,}000{,}000 / 250{,}000 = 200$ গুণ। অথচ দুজনেই শুধু "beam size" report করলে পার্থক্য দেখায় $1000/50 = 20$ গুণ — অর্থাৎ vocabulary বাদ দিলে পার্থক্য **10 গুণ কম** দেখায়।
- Exhaustive search কত বড়: $|Y|^{L}$; যেমন $|Y| = 5{,}000$, $L = 10$ হলে $5000^{10} \approx 9.77 \times 10^{36}$ — তাই beam search অপরিহার্য।
- Survey-তে পাওয়া beam size-এর পরিসর: **50** (VRepair, SeqTrans) থেকে **200** (RewardRepair) থেকে **1000** (KNOD, Rete)।

### ৬.১২ Stopping Condition ও Validation Budget
Survey-র উদাহরণ থেকে (আমার হিসাব):
$$
\text{ValRatio}_{\text{CURE}} = \frac{5{,}000 \text{ validated}}{10{,}000 \text{ generated}} = 50\%
$$
Bug প্রতি validation: CURE 5,000 বনাম RewardRepair 200 → $5000/200 = 25$ গুণ বেশি test-suite run। DLFix-এর budget আবার সময়ভিত্তিক — তাই তিনটা একই এককে নেই।

**আমার প্রস্তাবিত normalized metric** (paper-এ নেই):
$$
\text{Yield} = \frac{N_{\text{correct}}}{N_{\text{validated}}} \times 1000
$$
অর্থাৎ প্রতি 1,000টা যাচাই-করা candidate-এ কয়টা সঠিক fix। এতে ভিন্ন stopping rule-এর tool তুলনা করা যায় (Sub-domain 1-এর CG8 — cost/budget-এর সমতা — এর সাথে সরাসরি সম্পর্কিত)।

### ৬.১৩ Survey-র Proportion ও তাদের অনিশ্চয়তা
Proportion:
$$
\hat{p} = \frac{x}{n}, \qquad \text{SE} = \sqrt{\frac{\hat{p}(1 - \hat{p})}{n}}, \qquad \text{CI}_{95} \approx \left[\, \hat{p} - 1.96\, \text{SE},\;\; \hat{p} + 1.96\, \text{SE} \,\right]
$$

| Statistic (paper-এর count) | $\hat{p}$ (আমার হিসাব) | 95% CI (আমার হিসাব, normal approx.) |
|---|---|---|
| 22 ML / 61 নতুন technique | 36.1% | 24.0% থেকে 48.1% |
| 29 ML article / 118 মোট | 24.6% | 16.8% থেকে 32.3% |
| 7 LLM / 22 ML technique | 31.8% | 12.4% থেকে 51.3% |
| 6 সাম্প্রতিক / 7 LLM technique | 85.7% | n = 7 খুব ছোট — normal approx. অর্থহীন |

**আমার পর্যবেক্ষণ:** survey-টা পুরো population (৫ venue-র সব article) গুনেছে, তাই এটা sampling নয় — CI-এর অর্থ এখানে "এই trend কি অন্য venue বা অন্য সময়েও এমন হতো" ধরনের সাধারণীকরণের অনিশ্চয়তা। তবুও দেখায় যে 7 ও 22-এর মতো ছোট সংখ্যা থেকে বড় দাবি করতে সাবধান থাকা দরকার।

---

## ৭. Experimental Setup (Review Setup)

Survey-তে experiment নেই; এর "setup" হলো review-এর parameter:

| বিষয় | বিবরণ |
|---|---|
| **Seed source** | Monperrus living review, hal-01956501, version 5 |
| **Venues** | ICSE, TSE, FSE, ASE, EMSE (living review-এ সবচেয়ে বেশি APR article) |
| **Time window** | 1 Jan 2018 – 31 Dec 2023 (৬ বছর) |
| **Primary keywords** | patch, repair |
| **Secondary keywords** | automate, fix, fault, bug, vulnerability, generate (stem/variant সহ) |
| **Screening** | Keyword match হলে abstract manual review |
| **Corpus size** | 118 article |
| **Living review overlap** | 65 article (আমার হিসাব: 65/118 = 55.1%; বাকি 53টা = 44.9% living review-এ নেই) |
| **Analysis unit** | Article; tool-level detail (architecture, leakage handling, FL, correctness, benchmark, beam/vocab) |
| **Quantitative output** | Keyword frequency (Table 1), কয়েকটা count ও proportion |
| **Survey-র নিজের length** | 18 পৃষ্ঠা, 1টা table, কোনো figure নেই |

---

## ৮. Results — Review-এর মূল ফলাফল

### ৮.১ Corpus-এর মৌলিক সংখ্যা (paper থেকে)

| মাপ | সংখ্যা |
|---|---|
| মোট APR article | **118** |
| Living review-এ cross-listed | **65** |
| নতুন APR technique প্রস্তাব করেছে | **61** |
| এই 61-এর মধ্যে ML model ব্যবহার করেছে | **22** |
| এই 22-এর মধ্যে LLM | **7** |
| 7টা LLM technique-এর মধ্যে শেষ দুই বছরে প্রকাশিত | **6** |
| ML technique ব্যবহারকারী মোট article | **29** |
| এই 29-এর মধ্যে transformer ব্যবহার করেছে | **20** (নাম দেওয়া tool 18টা) |
| ML-related keyword তালিকাভুক্ত করেছে | **29%** article |
| 2018-এ ML ব্যবহার | **ছয়টায় একটার কম** (< 16.7%) |
| 2023-এ ML ব্যবহার | **চারটায় তিনটার বেশি** (> 75%) |

**আমার হিসাব:** 2018 থেকে 2023-এ ML share অন্তত $75 / 16.7 \approx 4.5$ গুণ বেড়েছে। আর 61 − 22 = 39টা নতুন technique ML ছাড়া; 29 − 22 = 7টা ML article নতুন repair technique নয় (যেমন patch correctness assessment বা empirical study)।

**আমার পর্যবেক্ষণ (সম্ভাব্য অসামঞ্জস্য):** "29% article ML keyword list করেছে" মানে প্রায় $0.29 \times 118 \approx 34$টা article; আবার "29টা article ML technique ব্যবহার করে" মানে $29/118 = 24.6\%$। দুটো আলাদা মাপ (keyword বনাম আসল ব্যবহার) হতে পারে, অথবা একটা typo — paper থেকে নিশ্চিত হওয়া যায় না। Supervisor জিজ্ঞেস করলে এটা সৎভাবে বলা উচিত।

### ৮.২ Table 1 — Author-selected Keyword (৪ বা তার বেশি বার ব্যবহৃত)
চিহ্ন: **ML** = ML-সম্পর্কিত keyword (paper-এ ✓ দিয়ে tag); **PC** = patch correctness keyword (paper-এ † দিয়ে tag); **Primary** = primary search keyword (paper-এ + চিহ্ন); **Secondary** = secondary search keyword (paper-এ তারকা চিহ্ন)।

| Keyword | Count | Tag |
|---|---|---|
| program | 101 | — |
| repair | 93 | Primary |
| automated | 36 | Secondary |
| learning | 25 | ML |
| software | 25 | — |
| patch | 23 | Primary |
| automatic | 19 | Secondary |
| code | 15 | — |
| synthesis | 12 | — |
| neural | 11 | ML |
| generation | 10 | — |
| debugging | 10 | Secondary |
| deep | 10 | ML |
| analysis | 10 | — |
| testing | 9 | — |
| vulnerability | 9 | Secondary |
| machine | 9 | ML |
| fault | 7 | Secondary |
| empirical | 7 | — |
| execution | 7 | — |
| localization | 6 | — |
| based | 6 | — |
| test | 6 | — |
| java | 6 | — |
| engineering | 5 | — |
| bug | 5 | Secondary |
| symbolic | 5 | — |
| overfitting | 5 | PC |
| correctness | 5 | PC |
| fix | 5 | Secondary |
| quality | 5 | — |
| networks | 4 | ML |
| search | 4 | — |
| assessment | 4 | PC |
| static | 4 | — |
| mutation | 4 | — |
| fixing | 4 | Secondary |
| apr | 4 | — |
| bugs | 4 | Secondary |
| representation | 4 | — |

(PDF-এর text extraction-এ এই table-এর column গুলো এলোমেলো ছিল; PDF-এর text layer আবার পড়ে count ও tag মিলিয়ে নেওয়া হয়েছে।)

**আমার পর্যবেক্ষণ:**
- ML-tagged keyword-এর মোট উপস্থিতি: 25 + 11 + 10 + 9 + 4 = **59** বার; patch-correctness keyword: 5 + 5 + 4 = **14** বার।
- "java" (6) আছে, কিন্তু "c" বা "python" নেই — Java-কেন্দ্রিকতা (Defects4J-এর প্রভাব) keyword-এও দেখা যায়।
- "localization" (6) ও "fault" (7) — FL এখনো APR-এর বড় theme।

### ৮.৩ ML Architecture-এর বিভাজন
**Transformer-ভিত্তিক 18টা tool (paper-এর তালিকা):** RewardRepair, CURE, DLFix, VRepair, SeqTrans, SynShine, SequenceR, AlphaRepair, VulRepair, Recoder, Quatrain, SelfAPR, TransRepair, Reptory, TENURE, Tare, KNOD, Rete।

**Pre-trained code LLM-এর উপর দাঁড়ানো tool (paper-এর উদাহরণ):**

| Tool | Base model | Base model-এর ধরন |
|---|---|---|
| AlphaRepair | CodeBERT | Encoder |
| CoditT5 | CodeT5 | Encoder-decoder |
| RewardRepair | CodeT5 | Encoder-decoder |
| SelfAPR | PLBART | Encoder-decoder |
| SynShine | RoBERTa (pre-trained) | Encoder |
| CURE | GPT (multi-head attention inherited) | Decoder |

**অন্যান্য neural architecture:**

| ভূমিকা | Architecture | Tool |
|---|---|---|
| Classifier | BiLSTM-ভিত্তিক multi-classifier | TRANSFER |
| Generative model | RNN | SynFix |
| Code representation | ASTNN | AccPR |
| Fix pattern feature learning | CNN | Liu et al. (FindBugs violation fix pattern mining) |

**Paradigm shift:** প্রথম তরঙ্গ — NMT (buggy → fixed অনুবাদ); বর্তমান — LLM (buggy line মুছে infill)।

### ৮.৪ Attention কীভাবে report করা হয়েছে (20টা transformer article)

| Reporting ধরন | Article সংখ্যা | Reference |
|---|---|---|
| কোনো নির্দিষ্ট attention model উল্লেখ নেই | 1 | [140] Recoder |
| খুব বিস্তারিত বর্ণনা | 5 | [27, 28, 49, 69, 141] |
| Attention research cite করেছে (Vaswani/Luong) | 4 | [33, 50, 88, 94] |
| সংক্ষিপ্ত ব্যাখ্যা | 3 | [26, 67, 83] |
| শুধু inherited NMT model cite | 7 | [4, 37, 111, 112, 123, 131, 133] |
| **মোট (আমার যোগফল)** | **20** | — paper-এর 20-এর সাথে মেলে |

উদাহরণ: CURE তার GPT থেকে পাওয়া attention-এর জন্য Vaswani cite করে; SeqTrans attention খুব বিস্তারিত বর্ণনা করে কিন্তু আসলে OpenNMT (Luong attention) পুনর্ব্যবহার করে। Authors-এর ব্যাখ্যা: attention-এর কোনো স্বীকৃত taxonomy নেই।

### ৮.৫ Data Leakage ও Contamination — কে কী করেছে

| Tool / Paper | Leakage handling | Survey-র মন্তব্য |
|---|---|---|
| **SelfAPR** | Temporal split (bug-fix commit-এর timestamp); training corpus থেকে **সব duplicate buggy sample** সরিয়েছে | প্রতিটা sample যাচাই করে শুধু unique রাখে |
| **CURE** | 2006-এর আগে rollback করা GitHub Java project-এ train (benchmark 2007 থেকে); CoCoNuT-এর মতো manual duplicate-bug removal | Coarse dedup; GitHub project-গুলো পরস্পর স্বাধীন এবং commit ও repair স্বাধীন — "strong assumption" |
| **ODS** (Overfitting Detection System) | Project-based segmentation: একাধিক source-এ থাকা project (যেমন Apache Math) বাদ | Random split-এ duplicate সমস্যা এড়ায় |
| **RewardRepair** | Syntactic training-এর bug-fix pair corpus-এ **কোনো train-test segmentation বা decontamination নেই** | ঝুঁকিপূর্ণ |
| **SynShine** | 1.7M pair থেকে random 100K test (standard segmentation) | Random split near-duplicate ধরতে পারে না (৬.৭ দেখো) |
| **Xia et al. [122]** | Open-source training-ওয়ালা প্রতিটা PLM-এর জন্য contamination তথ্য report; কোন repair (developer change-এর হুবহু) training data থেকে এসেছে তা গুনেছে | PLM contamination নিয়ে আলোচনা করা একমাত্র article |
| **5টা LLM-APR article** [4, 34, 37, 94, 123] (SynShine, Fan et al., VulRepair, Rete, AlphaRepair) | Leakage/contamination-এর প্রভাব বিবেচনা করেনি | — |
| **3টা LLM method** যারা corpus dedup করেছে | Syntax দিয়ে (Invalidator [59]); semantics দিয়ে (Quatrain [112]); পদ্ধতি অনির্দিষ্ট ([111] Tian et al.) | **লক্ষ্য করো:** তিনটাই patch correctness assessment-এর কাজ |
| **Near-duplicate** | **কোনো APR article near-duplicate নিয়ে কাজ করেনি** | সবচেয়ে বড় ফাঁক |

### ৮.৬ Decontamination-এর বিদ্যমান উপায় ও সীমা

| পদ্ধতি | কী করে | APR-এ সমস্যা |
|---|---|---|
| N-gram overlap (GPT-3) | Lowercase শব্দ-ভিত্তিক N-gram মিলায় | Corpus প্রকাশিত নয়; code-এর punctuation হারায় |
| Multi-sample substring matching (GPT-4) | Test-এর কয়েকটা substring corpus-এ খোঁজে | Third party-র পক্ষে চালানো অসম্ভব |
| Entropy gap (seen বনাম unseen) | Likelihood পার্থক্য দিয়ে membership অনুমান | Model-এ সরাসরি access লাগে; API-তে হয় না |
| Machine unlearning | Pre-trained weight থেকে data-র প্রভাব সরানো | মূলত privacy-কেন্দ্রিক; নতুন research (2023 NeurIPS challenge) |
| Decontamination package (যেমন EleutherAI) | Contaminated test sample চিহ্নিত করে clean benchmark দেয় | খুব কম model এটা দেয় |
| Canary string | Synthetic চিহ্ন বসিয়ে পরে খোঁজা | শুধু ভবিষ্যৎ dataset-এ কাজ করে |
| Identifier perturbation (SeqTrans ও adversarial text generation থেকে অনুপ্রাণিত) | Validation-এর সময় variable/type নাম বদলে generalization যাচাই | সম্ভাবনাময়, কিন্তু standard নয় |
| Code clone detection-ভিত্তিক similarity | Granularity অনুযায়ী train-test cross-contamination মাপা ও report করা | Survey-র সুপারিশ; specialized code similarity tool সাধারণ string similarity-র চেয়ে ভালো |

**Granularity-র ফলাফল:** code model-এ dedup বেশিরভাগ file-level-এ; অথচ NPR tool-এর input ছোট — max-token-limited context (SeqTrans, DLFix, SelfAPR, RewardRepair) থেকে পুরো buggy method (CURE) — তাই function/statement-level duplicate-এ এরা বিশেষভাবে ঝুঁকিপূর্ণ।

### ৮.৭ Benchmark ও Evaluation Practice-এর সমস্যা (Section 5-এর catalogue)

| # | সমস্যা | Survey-র প্রমাণ / সংখ্যা |
|---|---|---|
| B1 | **Performance reporting অসম** | ManyBugs paper-গুলো সাধারণত বিস্তারিত run-time দেয়; Defects4J paper-গুলো প্রায়ই শুধু "patch পাওয়া গেছে কিনা" দেয়। কেউ wall-clock upper bound, কেউ test-suite evaluation-এর সীমা দেয় |
| B2 | **FL অনুমান ভিন্ন** | 22টা article SBFL (test trace) ব্যবহার করে; 16টা article developer-এর repair location সরাসরি input নেয় (perfect FL); 5টা article [34, 83, 123, 140, 141] দুই setting-ই report করে। NPR tool সাধারণত perfect FL ধরে নেয় |
| B3 | **Correctness = একটা human reference patch-এর সাথে মিল** | 29টা cited article এই proxy ব্যবহার করে — "extraordinarily strict" |
| B4 | **APR benchmark ML train করার জন্য খুব ছোট; ML dataset-এ build/test নেই** | CrossVul শুধু diff; অন্যান্য বড় bug-fix pair dataset (যেমন CURE-এর) "program-text-only" |
| B5 | **History/bug report access** | শুধু iFixR bug-report IR ব্যবহার করে; বেশিরভাগ benchmark repository link দেয়, কিন্তু পুরো history ধারণ করা অসম্ভব; ব্যতিক্রম CodeFlaws, IntroClass |
| B6 | **Reproducible build** | ManyBugs (C, অসম্পূর্ণ build): 5টা article-এ data, মাত্র 2টা নতুন result; Defects4J (Java, Maven): 44টা article। কিছু author ManyBugs চালাতেই পারেননি, তাই human repair-এর সাথে syntactic তুলনা করেছেন। Angelix, Prophet-এর মতো tool build process বদলায় বলে container-এ সংঘাত হয় |
| B7 | **Search efficiency-র কোনো standard নেই** | Beam size 50 থেকে 1000; vocabulary size সবসময় report হয় না (KNOD, DLFix); প্রতি bug-এ অনেক unverified patch |

**আমার হিসাব (B6):** Defects4J ব্যবহার $44/118 = 37.3\%$, ManyBugs $5/118 = 4.2\%$ — প্রায় $44/5 = 8.8$ গুণ পার্থক্য; নতুন result ধরলে $44/2 = 22$ গুণ। অথচ survey মনে করিয়ে দেয় যে C/C++ software development-এর বড় অংশ — অর্থাৎ benchmark-এর সুবিধার কারণে research Java-র দিকে ঝুঁকে গেছে।

**আমার হিসাব (B2, citation গুনে):** SBFL list-এ 22টা reference, perfect-FL list-এ 16টা reference। অর্থাৎ FL-এর অনুমান স্পষ্ট এমন 38টা article-এর মধ্যে প্রায় $16/38 = 42\%$ perfect FL ধরে নেয়। (দুই list-এ কিছু article থাকতে পারে কিনা paper নিশ্চিত করেনি; আমি যা দেখেছি তাতে দুই list-এ কোনো common reference নেই।)

### ৮.৮ Survey-তে উল্লেখিত সংখ্যাগত detail (সংক্ষেপে)

| বিষয় | সংখ্যা |
|---|---|
| SynShine dataset | 1.7M erroneous/fixed program pair; random test set 100K |
| CURE | 10,000 candidate তৈরি, top 5,000 যাচাই; 2006-এর আগের data-তে training, benchmark 2007 থেকে |
| RewardRepair | Bug প্রতি সেরা 200 patch তৈরি ও যাচাই; beam 30/100/200/500; vocabulary 32,128 |
| VRepair | Beam 50; vocabulary 5,000 |
| SeqTrans | Beam 1 থেকে 50; vocabulary 8,000 |
| CURE beam/vocab | Beam 1,000; vocabulary 50,000 |
| Near-duplicate inflation | সর্বোচ্চ 100% পর্যন্ত (Allamanis 2019) |
| APR-COMP 2024 | 4টা track |

### ৮.৯ StandUp4NPR — মূল্যায়ন

| দিক | Survey-র মত |
|---|---|
| উদ্দেশ্য | ML-ভিত্তিক APR tool-এর evaluation standardize করা |
| ভালো দিক | Training/testing-এর well-defined interface; সব model-এ resource restriction; existing dataset থেকে data নিয়ে exact duplicate কমানোর জন্য process ও filter; data access, resource, runtime, evaluation criteria-র standardization — "much more level field" |
| খারাপ দিক ১ | শুধু দেওয়া training data ব্যবহার করা যায় → এটা মাপে "architecture কতটা দক্ষভাবে এই data কাজে লাগায়"; অন্য dataset curate করা বা auxiliary input (program history, অন্য project-এর history) ব্যবহার বাদ পড়ে |
| খারাপ দিক ২ | Neural technique-এর জন্য তৈরি; সব patch একসাথে তৈরি হয়ে স্বাধীনভাবে যাচাই হবে ধরে নেয় → GenProg, ARJA-র মতো feedback-loop-নির্ভর search-based technique তুলনা করা যায় না |
| Near-duplicate | Exact duplicate কমানোর চেষ্টা আছে, near-duplicate নিয়ে কিছু বলা নেই (survey-র ভাষা "exact duplicates") |

### ৮.১০ APR-COMP 2024 — মূল্যায়ন

| দিক | Survey-র মত |
|---|---|
| কী | 1st International Competition on Automated Program Repair |
| Track (4টা) | Functional errors; vulnerabilities; student assignments; AI-generated code |
| খারাপ দিক | Functional track-এর program existing benchmark (Defects4J, ManyBugs, Bears, Bugs.jar) থেকে sample → পুরনো সমস্যা উত্তরাধিকার, এবং content model designer-রা আগেই জানে। ImageNet-এর মতো competition public training data দেয় কিন্তু test data গোপন রাখে — এখানে তা নয় |
| ভালো দিক | একাধিক benchmark-এ standard API → interoperability; common time ও resource limit → তুলনাযোগ্য data; public pull request-এ submission → কার্যত executable artifact প্রকাশ বাধ্যতামূলক (যা অনেক APR article দেয় না) |

---

## ৯. Key Findings / Insights (Supervisor-কে বলার মতো ৮টা পয়েন্ট)

1. **ML APR দখল করেছে:** 2018-এ ছয়টায় একটার কম article ML ব্যবহার করতো, 2023-এ চারটায় তিনটার বেশি। নতুন 61টা technique-এর 22টা ML, 7টা LLM, যার 6টা শেষ দুই বছরে।
2. **Transformer প্রধান architecture:** 29টা ML article-এর 20টা transformer; কিন্তু attention কীভাবে কাজ করে তা report করার মান খুব অসম (20-এর মধ্যে মাত্র 5টা বিস্তারিত)।
3. **Leakage নিয়ে সচেতনতা কম:** 5টা LLM-APR article contamination বিবেচনাই করেনি; near-duplicate নিয়ে কেউ কাজ করেনি; dedup বেশিরভাগ file-level বা exact-match।
4. **Pre-trained LLM-এ decontamination প্রায় অসম্ভব:** corpus অপ্রকাশিত, weight উত্তরাধিকারসূত্রে আসে, API-তে likelihood পাওয়া যায় না। আর APR benchmark-এর bug বহু বছরের পুরনো ও public — "PLMs have likely scraped them"।
5. **Near-duplicate score-কে দ্বিগুণ পর্যন্ত ফোলাতে পারে** (100% পর্যন্ত inflation)।
6. **Correctness-এর সংজ্ঞা অতিরিক্ত কঠোর বা অসম:** 29টা article একটা human reference patch-কে মানদণ্ড ধরে; অন্যরা test বা manual semantic equivalence।
7. **FL ও stopping condition-এর পার্থক্য তুলনাকে অর্থহীন করে:** perfect FL বনাম SBFL; 200 patch বনাম 5,000 validation বনাম time budget; beam size vocabulary ছাড়া বিভ্রান্তিকর।
8. **Benchmark-এর সুবিধা research-এর দিক ঠিক করে দেয়:** build সহজ বলে Defects4J (44) ManyBugs-কে (5) ছাপিয়ে গেছে — ফলে APR research Java-কেন্দ্রিক। আর নতুন standardization উদ্যোগ (StandUp4NPR, APR-COMP) উপকারী হলেও সমস্যাগুলো পুরো সমাধান করে না।

---

## ১০. কেন এই Survey অন্যগুলোর থেকে ভালো (বা আলাদা)?

Survey নিজে তিনটা "high-quality general survey"-র উল্লেখ করে: Gazzola et al. (TSE 2019) [39], Le Goues, Pradel & Roychoudhury (CACM 2019) [62], Monperrus-এর Living Review [84]। পার্থক্য:

| বৈশিষ্ট্য | General APR survey (Gazzola, Le Goues et al.) | Monperrus Living Review | **এই Survey (Renzullo et al.)** |
|---|---|---|---|
| Scope | পুরো APR field | পুরো APR field, নিয়মিত update | **শুধু top-5 SE venue, 2018–2023** |
| Focus | Technique-এর শ্রেণীবিভাগ | বিস্তৃত তালিকা (domain, error type, human study) | **ML/LLM ও benchmark validity** |
| Data leakage / contamination | ML-যুগের আগে, তাই সীমিত | তালিকাভিত্তিক | **কেন্দ্রীয় বিষয়** |
| Evaluation inconsistency | আংশিক | না | **বিস্তারিত (FL, correctness, termination, beam/vocab, build)** |
| Corpus completeness | — | এই survey-র 118-এর মাত্র 65টা এতে আছে | পাঁচ venue-তে exhaustive |
| সমাধানের ইঙ্গিত | সাধারণ | না | Clone detection, canary, perturbation, unlearning, standard API |

**মূল শক্তি:**
1. **Timely:** LLM-APR-এর ঠিক উত্থানের সময় benchmark validity-র প্রশ্ন তুলেছে।
2. **Cross-field insight:** NLP/ML-এর contamination, memorization, unlearning গবেষণা থেকে SE-তে ধারণা এনেছে।
3. **Concrete evidence:** tool-ধরে ধরে কে কী করেছে (SelfAPR, CURE, ODS, RewardRepair, SynShine) — শুধু সাধারণ কথা নয়।
4. **Insider perspective:** GenProg ও ManyBugs-এর লেখকরা নিজেরাই benchmark-এর বয়স ও সীমা স্বীকার করছেন।
5. **Practical:** StandUp4NPR ও APR-COMP-এর ভালো-মন্দ দুই দিকই দেখিয়েছে।

---

## ১১. কোন পরিস্থিতিতে এই Survey কাজে লাগে, কোথায় লাগে না

### ✅ কাজে লাগে যখন:
- কোনো ML/LLM-ভিত্তিক repair বা coding-agent paper-এর **evaluation critically পড়তে** চাও — একটা checklist হিসেবে (FL অনুমান? correctness সংজ্ঞা? leakage handling? stopping rule?)।
- নিজের experiment **design** করছো এবং leakage এড়াতে চাও (temporal/project split, near-duplicate check)।
- APR-এর পুরনো benchmark (Defects4J, ManyBugs, QuixBugs) কেন সমস্যাযুক্ত তা supervisor-কে বোঝাতে চাও।
- LLM-যুগের আগে ও পরে APR কীভাবে বদলেছে তার একটা মানচিত্র চাও।

### ❌ সীমিত যখন:
- **Repository-level / agent-based repair** (SWE-bench, SWE-agent, Agentless) — corpus 2023-এ শেষ, এবং এই survey SWE-bench বা agent-এর উল্লেখই করে না।
- **Concrete quantitative contamination estimate** চাও — survey কোনো benchmark-এর contamination মেপে দেখায়নি।
- **Technique-এর performance তুলনা** চাও — survey ইচ্ছাকৃতভাবে leaderboard দেয়নি (কারণ তাদের মতে তুলনাগুলো অবৈধ)।
- **arXiv-only বা ML venue-র (ICLR, NeurIPS) কাজ** — বাদ পড়েছে।
- **Security, maintainability, code quality**-ভিত্তিক patch evaluation — আলোচনা নেই।

---

## ১২. Limitations — দুর্বলতা

### ১২.১ Authors যা নিজেরা স্বীকার করেছেন / scope হিসেবে বলেছেন
Paper-এ আলাদা "Threats to Validity" section নেই। Text থেকে যা স্বীকারোক্তি পাওয়া যায়:
1. **Narrow scope ইচ্ছাকৃত:** "we take a narrower view" — শুধু top-5 venue, 2018 থেকে; general survey-র বিকল্প নয়।
2. **Data bias অনাবিষ্কৃত:** APR-এ bias কীভাবে প্রকাশ পায় তা "not well-studied"; পড়া article-গুলোও এটা আলোচনা করেনি — survey নিজেও এটা খতিয়ে দেখেনি।
3. **সমাধান নয়, ইঙ্গিত:** "offer pointers to solutions where they are available" — অনেক সমস্যার (যেমন closed LLM-এর decontamination) কোনো standard সমাধান তারা দেয়নি।
4. **Decontamination এখনো অমীমাংসিত:** standard method "has not yet emerged", code task-এ তো আরও কম।
5. **Benchmark adoption-এর অন্য কারণ:** Defects4J বনাম ManyBugs-এর পার্থক্যে language-এর পার্থক্যসহ "other factors" আছে বলে স্বীকার করেছে।

### ১২.২ আমার Critical Analysis (Professor-level observation)
1. **Systematic review protocol দুর্বল:** PRISMA-ধরনের flow (কতগুলো hit → কতগুলো বাদ → কেন) দেখানো হয়নি; কে abstract review করেছেন, inter-rater agreement (যেমন Cohen's kappa) কত — কিছুই নেই। 118 সংখ্যাটা reproduce করা কঠিন।
2. **Venue selection bias:** ISSTA-র মতো গুরুত্বপূর্ণ SE venue (যেখানে Defects4J ও TBar প্রকাশিত) বাদ; ML venue (ICLR/NeurIPS — যেখানে SWE-bench প্রকাশিত) ও arXiv বাদ — অথচ LLM-APR-এর বড় অংশ সেখানে আসে। ফলে "LLM-এর উত্থান" আসলে কম করে দেখানো হতে পারে।
3. **Time cut-off-এর কারণে দ্রুত পুরনো:** 2023-এর শেষে কাটা; 2024-এর agent-যুগ (SWE-agent, AutoCodeRover, Agentless) পুরো বাদ। Submission (January 2024) থেকে publication (March 2025)-এর মধ্যে field অনেক বদলে গেছে।
4. **গণনায় ছোট অসামঞ্জস্য:** "29% ML keyword" বনাম "29টা ML article (24.6%)"; "20টা transformer article" কিন্তু 18টা tool-এর নাম। এগুলো ব্যাখ্যা করা নেই (আমার যোগফলে attention breakdown 20 মেলে, তাই 20 সংখ্যাটা ঠিক মনে হয়)।
5. **Contamination নিজে মাপেনি:** তারা বলে PLM "likely scraped" benchmark — কিন্তু open-source corpus-ওয়ালা model-এ (যেমন Xia et al. যা করেছে) নিজেরা Defects4J-এর overlap মেপে দেখাতে পারতো। দাবিটা যুক্তিসঙ্গত কিন্তু quantitative প্রমাণ ছাড়া।
6. **একদিকের correctness সমালোচনা:** reference-patch proxy "too strict" তা জোর দিয়ে বলেছে, কিন্তু উল্টো সমস্যা — test-suite-based plausibility "too lenient" (overfitting) — body text-এ প্রায় নেই, যদিও Table 1-এ overfitting/correctness/assessment keyword আলাদাভাবে tag করেছে। আমাদের domain-এর জন্য এটাই বেশি গুরুত্বপূর্ণ দিক (৬.৩-এর sandwich দেখো)।
7. **Beam × vocabulary-ও অসম্পূর্ণ metric:** $k \times |Y|$ শুধু decoding-এর search space বোঝায়; আসল খরচ নির্ভর করে model size, sequence length, আর কতগুলো candidate **test দিয়ে validate** হলো তার উপর। Survey নিজেই "unverified patches"-এর কথা বলে, কিন্তু validated-candidate-ভিত্তিক কোনো metric প্রস্তাব করেনি (৬.১২-এ আমার Yield প্রস্তাব দেখো)।
8. **কোনো concrete reporting checklist নেই:** সমস্যার catalogue চমৎকার, কিন্তু "একটা ML-APR paper-এ কী কী report করা বাধ্যতামূলক" এমন একটা checklist দিলে বেশি actionable হতো।
9. **Perspective bias-এর সম্ভাবনা:** StandUp4NPR-এর প্রধান সমালোচনা হলো এটা GenProg/ARJA-ধরনের feedback-loop technique সমর্থন করে না — আর authors-এর দুজন GenProg-এর লেখক। সমালোচনাটা যৌক্তিক, তবে পাঠককে এই প্রেক্ষাপট জানা উচিত।
10. **Survey হিসেবে ছোট:** 18 পৃষ্ঠা, 1টা table, কোনো figure বা year-wise chart নেই — "2018-এ ছয়টায় একটা, 2023-এ চারটায় তিনটা" ছাড়া বছরভিত্তিক trend data দেখানো হয়নি।

---

## ১৩. Research Gaps — কোথায় কাজ করার সুযোগ আছে

| # | Gap | কেন গুরুত্বপূর্ণ | আমাদের folder-এ কে কিছুটা কাজ করেছে / কোথায় দেখবো |
|---|---|---|---|
| A1 | **Near-duplicate contamination মাপা (code-aware, granularity-sensitive)** | কোনো APR article near-duplicate নিয়ে কাজ করেনি; inflation 100% পর্যন্ত | Coding-Agent Evaluation & Reliability (SWE-rebench — decontaminated evaluation) |
| A2 | **Closed LLM-এর জন্য black-box contamination probe** (identifier perturbation, metamorphic test) | Corpus ও weight না থাকলে বাকি উপায় অচল | Coding-Agent Evaluation & Reliability; Trustworthy AI for Software Engineering |
| A3 | **Plausible বনাম correct ফাঁক মাপা ও কমানো (patch overfitting)** | Test-only metric correctness-কে বেশি গোনে; reference-only কম গোনে | Patch Validation (HITL LLM-as-a-Judge, Harden and Catch, code representation for correctness); AI Coding Agents (Sub-domain 1, CG1) |
| A4 | **Patch correctness assessment tool-এর নিজের leakage-aware evaluation** | ODS, Invalidator, Quatrain-এর মতো tool নিজেরাই ML; project/temporal split ছাড়া তাদের precision ফুলে থাকতে পারে | Patch Validation |
| A5 | **Test-suite শক্তিশালী করা (extra test generation) overfitting ধরতে** | Survey-র Defects4J list-এ test generation দিয়ে overfitting কমানোর কাজও আছে [134]; LLM দিয়ে এখন সহজ | LLM Test Generation (Oracle-Guided Program Selection, coverage-oriented test generation) |
| A6 | **Standard reporting protocol (FL অনুমান, budget, stopping rule, candidates validated, cost)** | তুলনাযোগ্যতা নেই; Sub-domain 1-এর CG8-এর সাথে একই | Coding-Agent Evaluation & Reliability (Engineering Reliable Coding Agents) |
| A7 | **Multi-language / C-C++ executable benchmark** | Build সমস্যার কারণে research Java-কেন্দ্রিক | Coding-Agent Evaluation & Reliability (Long-horizon SWE task paper); APR folder-এর পরের paper-গুলো |
| A8 | **Vulnerability repair-এর leakage ও correctness** | VRepair, SeqTrans, VulRepair-এর মতো vulnerability tool-ও একই সমস্যায়; security patch-এর "correct" আরও কঠিন | Security of AI-Generated Code; APR folder-এর "LLM for Automated Vulnerability Repair" case study |
| A9 | **Data bias in APR** | কেউ study করেনি (survey নিজেই বলেছে) | — (খোলা) |
| A10 | **Hidden test set / private evaluation** | APR-COMP-এর benchmark আগে থেকে জানা; ImageNet-এর মতো hidden test নেই | Coding-Agent Evaluation & Reliability (SWE-rebench-এর fresh task) |

---

## ১৪. কী করলে আরও ভালো হবে — Improvement Ideas

(সবগুলো আমার প্রস্তাব — paper-এ এই রূপে নেই।)

1. **Reporting card বাধ্যতামূলক করা:** প্রতিটা APR/agent paper-এ একটা ছোট table — FL setting (perfect/SBFL/IR/agent-নিজে), correctness definition (test/reference/manual), candidates generated ও validated, stopping rule, time/cost, model training cutoff, leakage handling।
2. **Two-sided correctness report:** শুধু "plausible" বা শুধু "reference-match" নয় — তিনটাই: $N_{\text{plausible}}$, $N_{\text{correct}}$ (manual বা extra-test), $N_{\text{ref}}$ — যাতে ৬.৩-এর sandwich দেখা যায়।
3. **Clone-aware contamination report:** benchmark-এর buggy/fixed function-কে public corpus-এর সাথে Type I/II/III clone detection দিয়ে মিলিয়ে $\text{Cont}_{\tau}$ report করা।
4. **Perturbation robustness gap:** প্রতিটা evaluation-এ original ও identifier-renamed version দুটোতেই চালিয়ে $\Delta_{\pi}$ report।
5. **Temporal hold-out:** model-এর training cutoff-এর পরের bug নিয়ে আলাদা subset (SWE-rebench-ধরনের fresh task)।
6. **Validated-candidate normalized efficiency (Yield):** beam size-এর বদলে প্রতি 1,000 validated candidate-এ সঠিক fix।
7. **Feedback-loop-friendly standard harness:** StandUp4NPR-এর মতো standardization, কিন্তু iterative/agentic technique-এর জন্য step-by-step test feedback সমর্থন সহ — আজকের coding agent-এর জন্য এটা আরও জরুরি।

---

## ১৫. কোন Gap-এ Research করলে ভালো Result ও Publication আসতে পারে

> ⚠️ এটা APR sub-domain-এর প্রথম paper-এর ভিত্তিতে প্রাথমিক মত। বাকি দুইটা APR paper ও পরের sub-domain পড়ে আপডেট করবো।

| Idea | Gap | SPL3-তে করা সম্ভব? | Novelty | Publication সম্ভাবনা |
|---|---|---|---|---|
| **I1: Agent-paper evaluation audit** — এই survey-র method (venue + keyword + manual coding) 2024–2025-এর coding-agent paper-এ প্রয়োগ করে FL setting, correctness definition, contamination handling, cost reporting-এর অবস্থা মাপা | A6, CG8 | ✅ হ্যাঁ — শুধু paper পড়া ও coding; API খরচ নেই | মাঝারি-উচ্চ (agent-যুগে এমন audit কম) | ⭐⭐⭐⭐ |
| **I2: Identifier-perturbation contamination probe on SWE-bench Lite/Verified subset** — Python `ast` দিয়ে rename করে agent-এর patch-এর resolve rate তুলনা | A2, CG6 | ✅ হ্যাঁ — 30–50 task-এর ছোট subset, open-source pipeline (যেমন Agentless) | উচ্চ | ⭐⭐⭐⭐ |
| **I3: Leakage-aware evaluation of patch-correctness assessors** — LLM-judge বা classifier-কে random split বনাম repository-split বনাম temporal split-এ মেপে precision কতটা বদলায় তা দেখানো | A3, A4, CG1 | ✅ হ্যাঁ — public patch label (Sub-domain 1-এর agent patch) ব্যবহার | উচ্চ, সরাসরি assurance-এর সাথে যুক্ত | ⭐⭐⭐⭐⭐ |
| **I4: Two-sided correctness (sandwich) report for agent patches** — একই patch set-এ test-pass, extra-test, reference-similarity তিনটা মেপে ফাঁক দেখানো | A3, A5, CG1 | ✅ হ্যাঁ | মাঝারি-উচ্চ | ⭐⭐⭐⭐ |
| I5: Clone-aware contamination মাপা (benchmark বনাম বড় public code corpus) | A1 | ⚠️ কঠিন — বড় corpus download ও indexing লাগে | উচ্চ | ⭐⭐⭐ |
| I6: নতুন C/C++ executable benchmark | A7 | ❌ SPL3-এর জন্য বড় | মাঝারি | ⭐⭐ |

**সম্ভাব্য venue (general guidance):**
- **Conference/Workshop:** ICSE, FSE, ASE, ISSTA (top SE); তাদের workshop (যেমন LLM4Code, APR workshop) — student-এর জন্য শুরু করা সহজ। I1-ধরনের audit ESEM বা MSR-এর মতো empirical venue-তে মানায়।
- **Journal:** EMSE, JSS, IST (Q1, student-friendly); TOSEM/TSE (খুব high)। I1 বড় হলে ACM Computing Surveys-ধরনের review journal-ও বিবেচনা করা যায়।

---

## ১৬. SPL3 Implementation Perspective — Software-এ কীভাবে আনবো

**Survey "implement" করা মানে কী?** কোনো algorithm নেই — বরং survey-র সতর্কবাণীগুলোকে একটা **Evaluation Validity Checker** module হিসেবে বানানো, যেটা Sub-domain 1-এর assurance layer-এর পাশে বসবে। Agent-এর patch-এর বিশ্বাসযোগ্যতা মাপার আগে এটা যাচাই করবে যে **মাপার পদ্ধতিটাই** বৈধ কিনা।

**প্রস্তাবিত module:**
1. **Reporting Card Generator:** প্রতিটা evaluation run-এর জন্য JSON/Markdown card — FL setting, candidates generated/validated, stopping rule, time, token cost, model name ও training cutoff, task-এর তারিখ। (Survey-র B1, B2, B7 ও Sub-domain 1-এর CG8)
2. **Temporal Leakage Flagger:** প্রতিটা SWE-bench task-এর issue/PR তারিখ বনাম model-এর ঘোষিত training cutoff; cutoff-এর আগের task-কে "contamination-risk" tag। ফল দুই ভাগে report (আগে/পরে)।
3. **Identifier Perturbation Engine (Python):** `ast` (বা `libcst`) দিয়ে local variable ও private function rename; perturbed repository-তে agent চালিয়ে $\Delta_{\pi}$ হিসাব। Test যেন না ভাঙে সেজন্য শুধু local scope rename।
4. **Similarity / Clone Checker:** agent-এর patch বনাম gold patch এবং বনাম (ঐচ্ছিক) public snippet — normalized-token Jaccard (৬.৮), হুবহু gold patch reproduce করছে কিনা flag (memorization-এর সংকেত)।
5. **Two-sided Correctness Panel:** $N_{\text{plausible}}$ (official harness), $N_{\text{correct}}$ (extra-test/LLM-judge/manual sample), $N_{\text{ref}}$ (gold-similarity threshold) — sandwich চার্ট।
6. **Split-aware evaluator for assessors:** assurance layer-এর ভেতরের যেকোনো learned component (classifier/judge prompt tuning) repository-ভিত্তিক বা temporal split-এ evaluate করার utility।

**Practical সতর্কতা:**
- Official SWE-bench harness Docker-ভিত্তিক — Windows-এ WSL2 + Docker Desktop লাগবে (Sub-domain 1-এর মতো)।
- Perturbation-এর পরে নিজেই আগে test চালিয়ে নিশ্চিত হতে হবে যে original gold patch এখনো pass করে — নাহলে perturbation নিজেই bug তৈরি করেছে।
- Closed model-এর training cutoff শুধু vendor-এর ঘোষণা — তাই temporal flag "ঝুঁকি", প্রমাণ নয়।
- Small subset (30–50 task) দিয়ে শুরু; API খরচ আগে হিসাব।

---

## ১৭. পরবর্তী গবেষণায় এই Paper-এর প্রভাব (Context)

### ১৭.১ প্রেক্ষাপট
- Survey-টা 2025-এ প্রকাশিত, তাই এর citation প্রভাব এখনো নতুন — নির্দিষ্ট কোন কাজ একে অনুসরণ করেছে তা আমি যাচাই করিনি, তাই দাবি করছি না।
- তবে এর তোলা প্রশ্নগুলো (contamination, fresh task, hidden/standardized evaluation) পরে coding-agent evaluation-এ প্রধান বিষয় হয়ে উঠেছে — যেমন আমাদের folder-এর **SWE-rebench** (decontaminated evaluation), **SWE-bench Verified**-এর মতো human-validated subset, এবং **APR-COMP**-এর মতো competition। এরা এই survey-র ফল কিনা নয়, বরং একই সমস্যার স্বাধীন উত্তর বলে ধরা নিরাপদ।

### ১৭.২ Sub-domain 1 (SWE-bench-style agent evaluation)-এর সাথে সংযোগ

Survey SWE-bench-এর নাম নেয়নি (corpus 2023-এ শেষ, SWE-bench ICLR 2024)। কিন্তু এর প্রায় প্রতিটা সতর্কবাণী SWE-bench-ভিত্তিক agent evaluation-এ খাটে (নিচের mapping আমার বিশ্লেষণ):

| Survey-র সতর্কবাণী | SWE-bench / Agent-এ কোথায় দেখা যায় | Sub-domain 1-এর প্রমাণ | সম্পর্কিত CG |
|---|---|---|---|
| Benchmark-এর bug পুরনো ও public → PLM সম্ভবত দেখেছে | SWE-bench-এর 12টা repo খুব জনপ্রিয়; issue ও PR public | SWE-bench-এর contamination check শুধু 2023-এর আগে/পরে তুলনা — দুর্বল (Paper 01, ১২.২) | CG6 |
| Closed model-এ decontamination অসম্ভব | GPT-4, Claude-এর corpus অপ্রকাশিত | Sub-domain 1-এর সব প্রধান result closed model-এ | CG6 |
| Perfect FL score ফোলায় | SWE-bench "Oracle retrieval" | Claude 2: Oracle 4.80% বনাম BM25 1.96% (প্রায় 2.45 গুণ) | CG8 |
| Correctness proxy-র সমস্যা | SWE-bench test-pass ব্যবহার করে (reference-match নয়) — তাই survey-র "too strict" সমস্যা নেই, কিন্তু উল্টো "too lenient" সমস্যা আছে | AutoCodeRover: 78-এর মধ্যে 51 সঠিক (65.4%) | **CG1** |
| Termination / stopping rule ভিন্ন | Agent-এর step limit, cost limit, @1 বনাম @3, candidate সংখ্যা | Agentless 40 candidate; AutoCodeRover @1 19.00% বনাম @3 26.00%; SWE-agent-এর খরচ 1.67 বনাম 2.51 USD | CG2, CG8 |
| Beam/candidate সংখ্যা report-এর অসমতা | Agentless-এর majority voting, pass@k | 126 (upper bound) বনাম 96 (বাছাই) | CG2 |
| Reproducible build | SWE-bench প্রথমে conda, পরে Docker | Paper 01, ১২.২ | CG6 |
| Benchmark আগে থেকে জানা (APR-COMP-এর সমালোচনা) | SWE-bench test set public; hidden test নেই | Agentless: Lite-এর 4.3% issue-তে exact solution লেখা | CG6 |
| Memorization ও identifier perturbation | Agent gold patch হুবহু reproduce করছে কিনা কেউ মাপেনি | — | CG6 (নতুন উপ-gap) |
| ML-ভিত্তিক correctness assessor-এরও leakage ঝুঁকি (ODS-এর project split) | LLM-as-judge বা classifier দিয়ে agent patch যাচাই | Sub-domain 1-এ এখনো কেউ করেনি | CG1, CG7 |

### ১৭.৩ Provisional "Assurance Layer" direction — শক্ত হলো না দুর্বল? (আমার মূল্যায়ন)

**সামগ্রিক রায়: শক্ত হয়েছে, তবে একটা শর্ত যোগ হয়েছে।**

**CG1 (plausible patch-এর correctness) — শক্ত হয়েছে:**
- APR community-তে patch correctness একটা স্বীকৃত আলাদা theme (Table 1-এ overfitting, correctness, assessment আলাদা tag)।
- ODS, Invalidator, Quatrain, Tian et al.-এর মতো APCA tool-এর অস্তিত্ব দেখায় যে "test pass করা patch-কে আরেক স্তরে যাচাই" — এটা প্রতিষ্ঠিত research line। Assurance layer এই ধারাকে **agent-যুগে ও repository-level-এ** নিয়ে যাওয়া — novelty সেখানে।
- ৬.৩-এর sandwich দেখায় যে শুধু test-pass (SWE-bench) বা শুধু reference-match (পুরনো NPR) — কোনোটাই যথেষ্ট নয়; একাধিক signal মেলানো assurance layer-ই যৌক্তিক মাঝামাঝি।

**CG6 (benchmark quality ও contamination) — অনেক বেশি শক্ত হয়েছে:**
- Sub-domain 1-এ CG6 ছিল ⭐⭐⭐; এই survey দেখায় এটা APR-এর একটা কেন্দ্রীয় ও অমীমাংসিত সমস্যা। আমার মতে CG6-কে ⭐⭐⭐⭐-এ তোলা উচিত।
- Assurance layer-এ একটা নতুন component যোগ করার যুক্তি পাওয়া গেল: **Evaluation Validity / Contamination Probe** (temporal flag + identifier perturbation + gold-patch reproduction check)।

**শর্ত (দুর্বলতার দিক / সতর্কতা):**
- Assurance layer নিজেই যদি ML বা LLM-judge ব্যবহার করে, তাহলে survey-র সব leakage সতর্কবাণী **assurance layer-এর নিজের evaluation-এ**ও খাটে। তাই design-এ বাধ্যতামূলক: repository-ভিত্তিক বা temporal split, judge-এর prompt যেন evaluation task দেখে tune না হয়, আর result-এ split-ভিত্তিক তুলনা।
- Contaminated benchmark-এ assurance layer-এর "উন্নতি" দেখালে সেটাও প্রশ্নবিদ্ধ — তাই fresh/temporal subset-এ আলাদা report দরকার।

**আপডেট করা direction (প্রস্তাব):** "Leakage-aware Assurance Layer for AI Coding Agent Patches" — আগের ৫টা component (extra test, re-ranking, security/quality scan, consistency, confidence/abstention) + **৬ নম্বর component: Evaluation Validity Checker** (Section ১৬)।

---

## ১৮. Supervisor-এর সম্ভাব্য প্রশ্ন ও উত্তর (Viva Prep)

**Q1. এটা তো survey — এখান থেকে নতুন কী শিখলে?**
A: তিনটা জিনিস: (ক) ML/LLM APR-এ কত দ্রুত ঢুকেছে — 2018-এ ছয়টায় একটার কম থেকে 2023-এ চারটায় তিনটার বেশি; (খ) data leakage ও contamination কেন ML-APR-এর result-কে সন্দেহজনক করে, আর কেন closed LLM-এ এটা সমাধান করা প্রায় অসম্ভব; (গ) FL অনুমান, correctness সংজ্ঞা ও stopping rule-এর পার্থক্যের কারণে paper-গুলোর সংখ্যা সরাসরি তুলনা করা যায় না।

**Q2. Data leakage আর contamination-এর পার্থক্য কী?**
A: Leakage হলো সাধারণ ধারণা — training-এ এমন তথ্য থাকা যা prediction-এ অন্যায় সুবিধা দেয়। Contamination নির্দিষ্টভাবে benchmark/test-এর উদাহরণ (হুবহু বা near-duplicate) training data-তে ঢুকে যাওয়া। Survey memorization-কেও leakage-এর একটা রূপ বলেছে।

**Q3. Exact dedup কেন যথেষ্ট নয়?**
A: Type II/III clone (নাম বদলানো বা সামান্য পরিবর্তিত copy) exact match-এ ধরা পড়ে না। আমার উদাহরণে `if (a > b) return a;` আর `if (x > y) return x;`-এর raw Jaccard 0.6, কিন্তু identifier normalize করলে 1.0। Survey বলে near-duplicate score 100% পর্যন্ত ফোলাতে পারে, আর কোনো APR article near-duplicate নিয়ে কাজ করেনি।

**Q4. CURE ও SelfAPR কীভাবে leakage এড়িয়েছে, আর তাদের সীমা কী?**
A: দুজনেই temporal split করেছে — CURE 2006-এর আগের data-তে train করেছে কারণ benchmark 2007 থেকে। CURE manual coarse dedup করেছে এবং GitHub project ও commit স্বাধীন ধরে নিয়েছে — survey একে strong assumption বলে। SelfAPR সব duplicate buggy sample সরিয়েছে। কিন্তু দুজনেই নিজের model train করেছে; pre-trained LLM-এ এই নিয়ন্ত্রণ সম্ভব নয়।

**Q5. Perfect fault localization ধরে নেওয়া কেন সমস্যা?**
A: কারণ তখন tool শুধু patch generation করছে, full repair নয় — সহজতর task। বাস্তবে developer-এর location জানা থাকে না। Survey অনুযায়ী 16টা article এটা ধরে নেয়, 22টা SBFL ব্যবহার করে, মাত্র 5টা দুটোই report করে। SWE-bench-এ Oracle বনাম BM25 (4.80% বনাম 1.96%) এর বাস্তব উদাহরণ।

**Q6. Reference patch-এর সাথে মিলিয়ে correctness মাপা কেন "extraordinarily strict"?**
A: একটা functionality অনেকভাবে implement করা যায়; developer যেভাবে লিখেছে শুধু সেটাকে সঠিক ধরলে ভিন্ন কিন্তু সঠিক patch বাদ পড়ে। আমার formalization-এ reference-match আসল correctness-এর lower bound, আর test-pass upper bound — আসল সংখ্যা মাঝখানে।

**Q7. Beam size দিয়ে efficiency তুলনা কেন ভুল?**
A: Beam size vocabulary size ও sequence length বাদ দেয়। CURE (k = 1,000, V = 50,000) আর VRepair (k = 50, V = 5,000)-এর beam অনুপাত 20, কিন্তু প্রতি step-এ candidate অনুপাত 50,000,000 / 250,000 = 200। তার উপর কিছু paper vocabulary report-ই করেনি। আর আসল খরচ নির্ভর করে কতগুলো candidate test দিয়ে validate হলো তার উপর।

**Q8. StandUp4NPR আর APR-COMP 2024 কি সমস্যা সমাধান করে?**
A: আংশিক। StandUp4NPR interface, resource ও exact-duplicate filtering standardize করে, কিন্তু শুধু দেওয়া data ব্যবহার করতে দেয় এবং feedback-loop-ভিত্তিক search technique (GenProg, ARJA) সমর্থন করে না। APR-COMP-এর 4টা track ও standard API আছে, submission-এ executable দিতে হয়, কিন্তু benchmark পুরনো ও আগে থেকে জানা — ImageNet-এর মতো hidden test set নেই।

**Q9. এই survey কীভাবে তোমার SWE-bench-ভিত্তিক কাজকে প্রভাবিত করে?**
A: SWE-bench-এর repo public ও জনপ্রিয়, তাই contamination-এর ঝুঁকি একই; Oracle retrieval = perfect FL; test-pass correctness = overfitting ঝুঁকি; agent-ভেদে stopping rule ও cost আলাদা। তাই আমার assurance layer-এ একটা Evaluation Validity Checker যোগ করছি, আর assurance layer-এর নিজের learned অংশ repository/temporal split-এ evaluate করবো।

**Q10. Survey-র সবচেয়ে বড় দুর্বলতা কী, তোমার মতে?**
A: Systematic review protocol অস্পষ্ট (PRISMA flow, inter-rater agreement নেই), ISSTA ও ML venue বাদ, 2023-এ কাটা বলে agent-যুগ নেই, আর contamination নিজে quantitatively মাপেনি। এছাড়া "29% ML keyword" বনাম "29টা ML article"-এর মতো ছোট অসামঞ্জস্য আছে।

**Q11. Survey-র 118টা article-এর মধ্যে মাত্র 65টা living review-এ আছে — এর মানে কী?**
A: প্রায় 45% article (53টা) Monperrus living review-এ নেই। হয় living review এই venue-গুলোর সব APR কাজ ধরেনি, অথবা এই survey-র inclusion একটু বিস্তৃত (যেমন vulnerability বা correctness assessment article)। যেভাবেই হোক, শুধু একটা তালিকার উপর নির্ভর করে review করা ঝুঁকিপূর্ণ।

---

## ১৯. Glossary (দ্রুত মনে রাখার জন্য)

| Term | অর্থ |
|---|---|
| APR | স্বয়ংক্রিয়ভাবে bug ঠিক করা |
| Generate-and-validate | অনেক patch তৈরি করে test দিয়ে যাচাই |
| GenProg | Genetic programming-ভিত্তিক প্রথম দিকের বিখ্যাত APR tool |
| Template-based APR | পূর্বনির্ধারিত fix pattern প্রয়োগ (যেমন TBar) |
| Semantic / constraint-based APR | Symbolic execution ও constraint solving দিয়ে patch synthesize (যেমন Angelix) |
| NPR | Neural Program Repair — neural network দিয়ে repair |
| NMT | Neural Machine Translation — buggy থেকে fixed code "অনুবাদ" |
| PLM / LLM | Pre-trained / Large Language Model |
| Fault localization (FL) | Bug কোথায় তা খোঁজা |
| SBFL | Test execution spectrum দিয়ে সন্দেহজনক line ranking |
| Perfect FL | Developer-এর repair location সরাসরি input দেওয়া |
| Plausible patch | সব test pass করে এমন patch |
| Correct patch | আসলেই bug ঠিক করে এমন patch |
| Patch overfitting | Test pass করে কিন্তু আসলে ভুল |
| APCA | Automated Patch Correctness Assessment |
| Data leakage | Training-এ prediction-সংশ্লিষ্ট অন্যায় তথ্য |
| Contamination | Test/benchmark data training-এ ঢুকে যাওয়া |
| Near-duplicate | প্রায় একই content (Type II/III clone) |
| Type I/II/III clone | হুবহু / নাম বদলানো / কিছু পরিবর্তিত copy |
| Memorization | Training sequence হুবহু তৈরি করা |
| Decontamination | Test set থেকে training-এ দেখা অংশ সরানো |
| Temporal split | সময় দিয়ে train ও test আলাদা করা |
| Project-based split | Project দিয়ে train ও test আলাদা করা |
| Canary string | Leak ধরার জন্য বসানো অনন্য synthetic string |
| Machine unlearning | Model থেকে নির্দিষ্ট data-র প্রভাব সরানো |
| Beam search / beam size k | প্রতি step-এ সেরা k sequence রাখা |
| Vocabulary size (Y) | Model যতগুলো token তৈরি করতে পারে |
| Defects4J | সবচেয়ে জনপ্রিয় Java APR benchmark |
| ManyBugs / IntroClass | C APR benchmark (বড় program / ছাত্রদের program) |
| QuixBugs | ছোট algorithmic multi-lingual benchmark |
| StandUp4NPR | NPR evaluation standardize করার framework |
| APR-COMP 2024 | APR-এর প্রথম আন্তর্জাতিক competition (4টা track) |
| Living review | নিয়মিত update হওয়া survey |

---

## ২০. এক নজরে সারাংশ (Summary Card)

| | |
|---|---|
| **Paper type** | Survey — ACM Computing Surveys 57(8), Article 208, March 2025 |
| **Problem** | ML/LLM APR দখল করছে, কিন্তু benchmark ও evaluation ML-এর জন্য তৈরি নয় |
| **Method** | Monperrus living review (v5) থেকে top-5 venue (ICSE, TSE, FSE, ASE, EMSE) বাছাই; 2018–2023; keyword + manual abstract review → 118 article |
| **Key numbers** | 61 নতুন technique → 22 ML → 7 LLM (6টা শেষ দুই বছরে); 29 ML article → 20 transformer; Defects4J 44 বনাম ManyBugs 5 (2 নতুন); 29টা article single-reference correctness |
| **Key insight** | Leakage/contamination (বিশেষত near-duplicate) অবহেলিত; FL, correctness, stopping rule-এর পার্থক্যে তুলনা অবৈধ |
| **Main limitation** | Protocol অস্পষ্ট, venue/time scope সংকীর্ণ, agent-যুগ নেই, contamination নিজে মাপেনি |
| **আমাদের জন্য gap** | Leakage-aware assurance: plausible-বনাম-correct ফাঁক মাপা + evaluation validity check |
| **Sub-domain 1-এর সাথে** | CG1 ও CG6 শক্ত হলো; assurance layer-এ "Evaluation Validity Checker" যোগ, এবং assurance layer-এর নিজের evaluation leakage-aware হতে হবে |

---

## ২১. বর্তমান (2026) প্রেক্ষাপট — আজকের Model ও Agent-দের সাথে তুলনা

Survey-র corpus 2023-এর শেষে থেমেছে; তখনকার "LLM-APR" মানে ছিল CodeBERT, CodeT5, PLBART-এর উপর বানানো tool (Section ৮.৩)। আজ (October 2026) frontier হলো Claude Opus 5.5 (2026-09-22), Claude Fable 5.1, GPT-6 Astra ও GPT-6.1 Sol, Gemini 4 Argon (2026-10-13), আর open-weight দিকে GLM-5.2/5.3, DeepSeek V4, Qwen3.8 (Kimi K3.1 Pro-র weight 2026-11-04-এর মধ্যে দেওয়ার প্রতিশ্রুতি); এরা Claude Code, Codex CLI, mini-SWE-agent-এর মতো agent-এর ভেতরে চলে। এই section-এর সব current-state তথ্য `00_Current_State_2026_Sources.md` (2026-10-28-এ সংকলিত fact sheet) থেকে নেওয়া। প্রতিটা সংখ্যার পাশে লেখা আছে সেটা **কোম্পানির নিজের দাবি (vendor-reported)** নাকি **স্বাধীনভাবে মাপা (independent)**; যেটা শুধু search-snippet থেকে এসেছে বা যাচাই হয়নি, সেটাও চিহ্নিত। আমার নিজের যুক্তি "আমার পর্যবেক্ষণ" লেবেলে।

### ২১.১ Paper-এর সময় বনাম এখন

| দিক | Paper-এ (corpus 2018–2023) | এখন, October 2026 | উৎস (fact sheet) |
|---|---|---|---|
| Contamination-এর স্বীকৃতি | PLM benchmark "likely scraped" — দাবি যুক্তিসঙ্গত, কিন্তু মাপা হয়নি; মাত্র একটা article (Xia et al.) contamination আলোচনা করেছে | OpenAI নিজেই SWE-bench Verified-এ evaluate করা বন্ধ করেছে (2026-02-23), কারণ benchmark "increasingly contaminated"; secondary রিপোর্ট বলে আগের প্রজন্মের frontier model gold patch হুবহু লিখে দিতে পারে | §3 — OpenAI post (search-snippet only, page 403); byteiota (secondary) |
| Benchmark saturation | Defects4J, ManyBugs-এর মতো পুরনো public benchmark | Vals.ai SWE-bench Verified archive করেছে; সেরা Claude Opus 5 **97.0%** (স্বাধীনভাবে মাপা, 2026-09-01)। Opus 5.5 system card-এ Verified-এর নামই নেই | §2, §3 — Vals.ai [independent]; Opus 5.5 card |
| Test নিজেই ভুল ("too strict") | B3: reference-match proxy "extraordinarily strict" | OpenAI: audit করা কঠিন subset-এর অন্তত **59.4%** task-এর test সঠিক submission-কেও reject করে। SWE-Bench Pro public set-এ automated audit **27.4%**, পাঁচজন মানুষের audit **34.1%** task broken | §3 — OpenAI (search-snippet only); the-decoder (secondary) |
| Test খুব ঢিলা ("too lenient") | Survey body-তে প্রায় অনুপস্থিত (Section ১২.২, পয়েন্ট 6) | PatchDiff (ICSE 2026): plausible patch-এর **29.6%** gold patch থেকে ভিন্ন আচরণ করে; "solved" patch-এর **7.8%** পুরো developer test suite-এ fail করে — স্বাধীনভাবে মাপা, তবে আগের প্রজন্মের agent-এ | §4 — arXiv 2503.15223 [independent] |
| Leakage-এর পথ | শুধু training-time: temporal/project split, near-duplicate | নতুন পথ **runtime leakage**: agent container-এর `.git` history বা network থেকে gold patch পড়ে। SWE-Bench Pro Verified-এ GLM-5.2: baseline **78.80%**, anti-hacking safeguard সহ **57.32%**; DeepSWE-এর 38টা cheating trial-এর 33টা (87%) `.git` থেকে gold commit পড়েছে | §3 — arXiv 2609.08149 [independent]; DeepSWE (search-snippet only) |
| Hidden / fresh test set (A10) | APR-COMP-এর benchmark আগে থেকে জানা; hidden test নেই | SWE-rebench প্রতি মাসে নতুন task দেয় (শেষ window 2026-05-15 থেকে 07-01; Opus 5.5 ও GPT-6 এখনো নেই); DeepSWE v1.1-এর 113টা task শূন্য থেকে লেখা; SWE-Bench Pro-র private commercial set-এ current-model সংখ্যা পাওয়া যায়নি | §2 — swe-rebench.com, DeepSWE [primary]; Scale (commercial board URL 404) |
| তুলনাযোগ্যতা (A6, B1–B7) | FL অনুমান, stopping rule, beam/vocab ভিন্ন, তাই সংখ্যা তুলনীয় নয় | Opus 5.5 SWE-bench Pro **89.9%** (কোম্পানির নিজের দাবি) বনাম Scale-এর mini-SWE-agent board-এর সেরা **61.50 ± 3.10** (স্বাধীন; Opus 5.5-এর entry নেই)। একই model-এ শুধু scaffold বদলালে **29.8 point** পর্যন্ত পার্থক্য | §2, §3 — Opus 5.5 card; Scale board; Liu et al. arXiv 2609.17394 [independent] |
| Statistical rigor | কোনো uncertainty report নেই | Verified-এর top-30-এ পাশাপাশি 29টা জোড়ার **0টা** McNemar test-এ আলাদা করা যায়; vendor এখন SE দেয় (Opus 5.5 Terminal-Bench 4.0 ±2.6) | §3 — Liu et al. [independent]; Opus 5.5 card [vendor-reported] |
| Standard harness | StandUp4NPR, APR-COMP-এর standard API | mini-SWE-agent এখন Scale-এর SWE-Bench Pro board, Vals.ai ও Artificial Analysis-এর standard harness | §1 — mini-swe-agent GitHub [primary] |
| Efficiency-র একক (B7) | Beam size, vocabulary size | প্রতি task-এর খরচ ও সময়: Terminal-Bench 4.0-এ **1.72 USD** (GPT-6.1 Sol) থেকে **17.64 USD** (Gemini 4 Argon); Opus 5.5 প্রতি task-এ গড়ে 1h04m | §3 — Vals.ai [independent] |

### ২১.২ কোন Finding এখনো সত্য, কোনটা পুরনো হয়ে গেছে

**এখনো সত্য — বরং আরও শক্ত প্রমাণ পেয়েছে:**
1. **"পুরনো, public benchmark-এ contamination হয়েছে" (Key Finding 4):** 2024-এ এটা ছিল যুক্তিভিত্তিক সন্দেহ; 2026-এ OpenAI নিজে contamination-কে কারণ দেখিয়ে Verified ছেড়েছে, Vals.ai saturation-এর কারণে archive করেছে, আর Anthropic Opus 5.5 card-এ Verified বাদ দিয়েছে। অর্থাৎ survey-র সতর্কবাণী এখন vendor-রাও মেনে নিচ্ছে। তবে লক্ষ করো: vendor-রা contamination-এর **পরিমাণ** প্রকাশ করেনি — survey-র নিজের দুর্বলতা ("contamination নিজে মাপেনি", Section ১২.২) এখন পুরো field-এর জন্য সত্য।
2. **"Closed model-এ third party decontamination করতে পারে না":** এখনো সত্য। Field এর উত্তরে decontamination করেনি, বরং নতুন task বানিয়েছে (SWE-rebench, DeepSWE)। Survey-র প্রস্তাবিত canary string, machine unlearning বা clone-detection-ভিত্তিক report গ্রহণ করা হয়েছে — এমন কোনো প্রমাণ fact sheet-এ নেই।
3. **"Evaluation-এর অসমতায় সংখ্যা তুলনীয় নয়" (Key Finding 7):** আমার পর্যবেক্ষণ — অবস্থা আরও খারাপ হয়েছে। প্রতিটা vendor আলাদা benchmark set headline করে (Anthropic: Terminal-Bench 4.0, FrontierCode, CursorBench; Google-এর launch post-এ coding সংখ্যাই নেই), আর official SWE-bench leaderboard 2026-02-এর পর নতুন entry নেয়নি।
4. **Correctness সংজ্ঞার সমস্যা:** Survey reference-match-কে "too strict" বলেছিল। 2026-এর প্রমাণ দেখায় **test-ভিত্তিক সংজ্ঞাও দুই দিকেই ভুল করে** — সঠিক patch reject (OpenAI-এর 59.4%) আর ভুল patch accept (PatchDiff-এর 29.6%)। Section ৬.৩-এর "sandwich" ধারণা তাই আজও সবচেয়ে কাজের মডেল।

**পুরনো হয়ে গেছে বা বদলাতে হবে:**
1. **Leakage-এর taxonomy অসম্পূর্ণ:** Survey শুধু training data নিয়ে ভেবেছে। আজকের agent sandbox-এ কাজ করে, তাই local file, `.git` history, network আর metadata — এই চারটা runtime channel (SWE-Bench Pro Verified) দিয়েও উত্তর ফাঁস হয়। আমার পর্যবেক্ষণ: GLM-5.2-এর প্রায় 21.5 point পতন দেখায় এর প্রভাব survey-র near-duplicate inflation-এর আশঙ্কার মতোই বড় — mechanism আলাদা, ফল একই (ফোলানো score)।
2. **Beam × vocabulary efficiency metric (৬.১১) agent-যুগে অচল:** এখন তুলনার একক USD প্রতি task ও wall-clock সময়। Survey-র মূল দাবি ("standard efficiency report দরকার") টেকে, কিন্তু একক বদলে গেছে।
3. **Perfect FL (B2) বিতর্ক কম প্রাসঙ্গিক:** আজকের agent benchmark-এ (SWE-bench-ধরনের, Terminal-Bench) agent নিজেই localize করে। আমার পর্যবেক্ষণ: B2-এর জায়গা নিয়েছে **scaffold ও effort level-এর পার্থক্য** — একই model-এ 29.8 point পর্যন্ত ফারাক, আর FrontierCode-এ medium effort-এর উপরে score কমে।
4. **Section ১৭.১-এর একটা সূক্ষ্মতা:** সেখানে SWE-bench Verified-কে "human-validated subset" হিসেবে একই সমস্যার উত্তর বলা হয়েছিল। এটা ভুল নয়, কিন্তু 2026-এর তথ্য যোগ করা দরকার: human-validated হলেও audit-এ কঠিন subset-এর বড় অংশের test ত্রুটিপূর্ণ পাওয়া গেছে, আর এখন benchmark-টা saturated।

### ২১.৩ এই Paper-এর Gap-গুলো আজও খোলা কিনা

| Gap | 2026-এ অবস্থা | প্রমাণ (fact sheet) |
|---|---|---|
| A1 — Near-duplicate contamination মাপা | **খোলা** | Near-duplicate মাপার কোনো 2026 study fact sheet-এ নেই; gold patch হুবহু লেখার খবর শুধু secondary source-এ, আর সেটা আগের প্রজন্মের model নিয়ে |
| A2 — Closed LLM-এর black-box contamination probe | **খোলা** | Field fresh task-এর দিকে গেছে, probe-এর দিকে নয়। Noise Floor Audit (independent): অর্থ-অপরিবর্তিত prompt perturbation rerun-এর চেয়ে 11–58 গুণ বড় SD দেয় — তাই perturbation probe-এর ফল থেকে noise আলাদা করা কঠিন |
| A3 — Plausible বনাম correct ফাঁক | **খোলা** | PatchDiff-এর 29.6% current agent-এ আবার মাপা হয়নি; SWE-Bench Pro-র broken task-এর একটা ধরন "low-coverage tests" |
| A4 — APCA tool-এর leakage-aware evaluation | **খোলা** | ComPass: সাধারণ LLM baseline overfitting patch বাছাইয়ে মাত্র 62.14% accuracy (search-snippet only); current agent patch-এ LLM judge যাচাইয়ের কোনো study পাওয়া যায়নি |
| A5 — Test শক্তিশালী করে overfitting ধরা | **আংশিক সমাধান** | PROBE: program variant দিয়ে দুর্বল test ধরা যায়, filter-এর পরে resolution rate কমে (search-snippet only)। অন্যদিকে agent-এর লেখা test patch-এর 80.2%-এ দুর্বল বা কোনো explicit oracle নেই (independent) |
| A6 — Standard reporting protocol | **খোলা (আরও খারাপ)** | Vendor বনাম independent ফাঁক: Sonnet 5.5 Terminal-Bench 4.0-এ 70.6% (কোম্পানির নিজের দাবি) বনাম 63.6–64.1% (স্বাধীন) |
| A7 — Multi-language executable benchmark | **আংশিক সমাধান** | SWE-bench Multilingual (official top 72.7%, Gemini 3 Flash), DeepSWE-এ 5টা language; কিন্তু C/C++-কেন্দ্রিক current-model data fact sheet-এ নেই |
| A8 — Vulnerability repair-এর leakage ও correctness | **খোলা** | Current model-এ শুধু vendor-reported CWE-bench v1 (Gemini 4 Argon 68.0%, secondary, search-snippet only); স্বাধীন মাপ নেই |
| A9 — APR-এ data bias | **খোলা** | সরাসরি কিছু নেই। কাছাকাছি একটা সংকেত: agent PR-এর merge rate repository popularity-র উপর নির্ভর করে (0 star-এ প্রায় 92%, 1,000+ star-এ প্রায় 60%; low-tier venue) |
| A10 — Hidden / private evaluation | **আংশিক সমাধান** | SWE-Bench Pro private set (276 instance) আছে, কিন্তু current-model সংখ্যা নেই; SWE-rebench-এর শেষ window Opus 5.5 ও GPT-6-এর আগে শেষ |
| CG4 — Run-to-run reliability | **খোলা** | SWE-rebench top-8-এ pass@1 ও pass@5-এর ফাঁক 12–18 point (independent) |
| CG6 — Benchmark quality ও contamination | **খোলা, তবে এখন স্বীকৃত** | OpenAI, Vals.ai, Anthropic — তিন দিক থেকেই Verified পরিত্যক্ত |
| CG8 — Evaluation-এর সমতা | **খোলা** | 0/29 adjacent pair আলাদা করা যায়; scaffold-এ 29.8 point |
| CG11 — Verifier health | **খোলা** | DeepSWE: SWE-Bench Pro-র inherited test-এর সাথে LLM-judge-এর অমিল 32.4%, DeepSWE-এর নিজের verifier-এ 1.4% |
| CG12 — Verifier-এর বিরুদ্ধে optimization pressure | **খোলা, সরাসরি প্রমাণসহ** | METR: 8 ঘণ্টার বেশি task-এ সফল run-এর অন্তত 16% অবৈধ (আগের প্রজন্ম); Opus 5.5 বা GPT-6-এর কোনো স্বাধীন reward-hacking audit পাওয়া যায়নি |

### ২১.৪ বর্তমান Model দিয়ে আবার পরীক্ষা করলে — SPL3 Idea

সব idea আমার প্রস্তাব। খরচের অনুমান fact sheet-এর independent cost range থেকে (Vals.ai, SWE-bench Verified: প্রতি task 0.10–2.05 USD); আসল খরচ আগে 5টা task-এর pilot দিয়ে মেপে নিতে হবে।

1. **Training-leakage বনাম runtime-leakage আলাদা করা:** 30টা পুরনো SWE-bench task ও 30টা SWE-rebench-এর নতুন task নিয়ে mini-SWE-agent + একটা সস্তা current model (যেমন DeepSeek V4 Pro, Vals-এ প্রতি task প্রায় 0.10 USD) চালানো — দুই অবস্থায়: (ক) সাধারণ container, (খ) `.git` history মুছে ও network বন্ধ করে। চার ঘরের তুলনা দেখাবে score-এর কতটা পুরনো task-এর সুবিধা থেকে আর কতটা runtime shortcut থেকে আসে। **যে নতুন gap বেরোবে:** survey-র taxonomy-তে runtime leakage নেই; ছোট scale-এ দুটো আলাদা করে মাপার পদ্ধতিও নেই (A1, A2, CG12)।
2. **Issue-only gold-patch recall test:** Repository না দিয়ে শুধু issue text দিয়ে model-কে patch লিখতে বলা, তারপর gold patch-এর সাথে normalized-token similarity (Section ৬.৮)। পুরনো বনাম নতুন task-এ similarity-র পার্থক্য = memorization-এর সংকেত। প্রতি task-এ একটা API call — সবচেয়ে সস্তা idea। **যে নতুন gap বেরোবে:** verbatim reproduction-এর দাবি এখন শুধু secondary source-এ এবং আগের প্রজন্মে; current model-এ মাপা হয়নি (A1)।
3. **Identifier-perturbation probe, noise-সহ (I2-এর আপডেট):** আগের I2 idea-য় একটা শর্ত যোগ করতে হবে — প্রতিটা condition-এ অন্তত 3 run, কারণ Noise Floor Audit বলে prompt perturbation নিজেই বড় noise আনে। Original বনাম renamed-এর পার্থক্যকে rerun-SD-এর সাথে তুলনা করে report করা। **যে নতুন gap বেরোবে:** contamination effect আর perturbation noise আলাদা করার statistical পদ্ধতি (A2, CG4)।
4. **2026 vendor-report audit (I1-এর আপডেট):** কোনো API খরচ নেই। Opus 5.5, Sonnet 5.5, GPT-6.1 Sol/Terra, Gemini 4 Argon-এর launch page ও system card পড়ে একটা coding sheet — কোন benchmark, কোন harness, effort level, কতগুলো trial, SE আছে কিনা, Verified আছে কিনা। **যে নতুন gap বেরোবে:** survey-র reporting-card ধারণা (Section ১৪) vendor release-এ কতটা মানা হয়, তার পরিমাপ (A6, CG8)।
5. **Current agent patch-এ "sandwich" report (I4-এর আপডেট):** 20–30টা resolved patch-এ official test-pass, বাড়তি differential test (PatchDiff-ধরনের) আর gold-similarity — তিনটা একসাথে। **যে নতুন gap বেরোবে:** PatchDiff-এর 29.6% current agent-এ আবার মাপা (A3, CG1)।

### ২১.৫ Supervisor-এর সম্ভাব্য প্রশ্ন (2026 প্রসঙ্গে)

**Q1. Survey-র corpus 2023-এ শেষ; আজ model SWE-bench Verified-এ 97% পায়। Survey কি এখন অপ্রাসঙ্গিক?**
A: বরং উল্টো। 97% (Vals.ai, স্বাধীনভাবে মাপা) আসার পরেই benchmark-টা archive হয়েছে, OpenAI contamination-এর কারণে ছেড়েছে, Anthropic card থেকে বাদ দিয়েছে। Survey ঠিক এই পরিণতির সতর্কবাণী দিয়েছিল। যেটা বদলেছে তা হলো উদাহরণ — Defects4J-এর জায়গায় এখন SWE-bench Verified।

**Q2. তাহলে আজকের model আসলে কতটা ভালো, কোন সংখ্যা বিশ্বাস করবে?**
A: স্বাধীন ও contamination-প্রতিরোধী board-এর সংখ্যা: SWE-rebench-এ Fable 5 pass@1 64.5% (window শেষ 2026-07-01); Terminal-Bench 4.0-এ Opus 5.5 Vals-এ 65.15%, Artificial Analysis-এ 59.6%। Vendor-এর 89.9% (SWE-bench Pro) একই harness-এ মাপা নয়। আর Opus 5.5 ও GPT-6 এখনো SWE-rebench বা Scale-এর SWE-Bench Pro board-এ নেই — তাই fresh repository-repair task-এ তাদের স্বাধীন মাপ এখনো নেই।

**Q3. আজ survey লিখলে কী যোগ করতে হতো?**
A: আমার পর্যবেক্ষণ — চারটা জিনিস: (ক) runtime leakage (`.git`, network) আলাদা category হিসেবে; (খ) grader-এর নিজের মান — SWE-Bench Pro-র 27–34% task broken; (গ) run-to-run variance ও scaffold-এর প্রভাব, uncertainty সহ report; (ঘ) beam size-এর বদলে USD প্রতি task ও সময়। চারটাই survey-র মূল যুক্তির স্বাভাবিক বিস্তার।
