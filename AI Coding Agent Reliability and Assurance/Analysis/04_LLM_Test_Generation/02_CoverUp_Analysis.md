# Paper Analysis 02 (TestGen): CoverUp — Effective High Coverage Test Generation for Python

> **Sub-domain:** LLM Test Generation
> **Analysis করেছে:** SPL3 — AI Coding Agent Reliability and Assurance
> **Paper file:** `LLM Test Generation/Effective High Coverage Test Generation forPython.pdf`
> **কোন চোখে পড়া হয়েছে:** আমাদের assurance layer-এ generated test হলো **"dynamic signal"** (CG1, CG3)। তাই পুরো analysis-এ একটা প্রশ্ন বারবার আসবে — **high coverage মানেই কি শক্ত oracle?** (উত্তর: না, আর এই paper সেটা মাপেনি।)

---

## ০. Paper-এর পরিচয় (Bibliographic Info)

| বিষয় | তথ্য |
|---|---|
| **Title** | CoverUp: Effective High Coverage Test Generation for Python |
| **Authors** | Juan Altmayer Pizzorno, Emery D. Berger |
| **Institution** | University of Massachusetts Amherst (Berger: UMass Amherst ও Amazon Web Services); কাজটা UMass Amherst-এ করা |
| **Venue** | Proc. ACM Softw. Eng. (PACMSE), Vol. 2, No. FSE, Article FSE128, July 2025 — অর্থাৎ **FSE 2025** (ACM International Conference on the Foundations of Software Engineering), top-tier SE venue |
| **তারিখ** | Received 2024-09-12; accepted 2025-04-01; publication July 2025। Tool-টা প্রথম GitHub-এ এসেছিল **2023-08-07** (paper নিজেই বলেছে) |
| **DOI** | 10.1145/3729398 (23 pages) |
| **Paper type** | **Tool / technique paper + empirical evaluation** — নতুন test generation পদ্ধতি, সাথে baseline তুলনা ও ablation |
| **Artifacts** | CoverUp tool (github.com/plasma-umass/coverup), replication package (github.com/plasma-umass/coverup-eval), Zenodo archive; state pollution handling-এর জন্য আলাদা package `pytest-cleanslate` |
| **ব্যবহৃত LLM** | OpenAI `gpt-4o-2024-05-13`, temperature 0 |
| **আমাদের domain-এ গুরুত্ব** | ⭐⭐⭐⭐ — Assurance layer-এর **dynamic signal** (generated test) কীভাবে বানানো যায়, তার সবচেয়ে পরিষ্কার "coverage-guided LLM loop" design। কিন্তু oracle-এর শক্তি মাপেনি — ঠিক এখানেই আমাদের gap। |

---

## ★ সহজ ভাষায় পুরো Paper (প্রথমবার পড়ার জন্য)

### ক. Paper-টা কী নিয়ে?
- এটা একটা **নতুন tool-এর paper**, সাথে পরীক্ষা-নিরীক্ষাও আছে।
- Tool-এর নাম **CoverUp**। কাজ: Python code-এর জন্য নিজে নিজে unit test লিখে দেওয়া।
- বানিয়েছেন Juan Altmayer Pizzorno ও Emery Berger, University of Massachusetts Amherst থেকে।
- Paper ছাপা হয়েছে FSE 2025-এ। এটা software engineering-এর একটা বড় conference।
- Tool-টা একটা LLM (GPT-4o) ব্যবহার করে। কিন্তু শুধু LLM-কে "test লেখো" বললে হয় না। CoverUp LLM-কে ঠিক পথ দেখায়।
- এই paper-এর সবচেয়ে বড় দাবি: আগের সেরা tool CodaMosa-র চেয়ে অনেক বেশি code CoverUp-এর test দিয়ে চালানো যায়।

### খ. সমস্যাটা কী ছিল?
- Developer-রা test লিখতে চায় না। Test লেখা ক্লান্তিকর আর সময়ও লাগে। তাই অনেক project-এ test কম থাকে।
- আগের tool-গুলো (যেমন Pynguin) random ভাবে test বানিয়ে বানিয়ে খোঁজে। এক জায়গায় গিয়ে এরা আটকে যায়। একে বলে coverage plateau (উন্নতি থেমে যাওয়া)।
- একটা উদাহরণ: ধরো একটা `if` শুধু তখনই চলে যখন input একটা বিশেষ format-এর string। Random ভাবে সেই string পাওয়া প্রায় অসম্ভব।
- আগের LLM-ভিত্তিক tool-গুলোও পুরো ঠিক ছিল না। এরা LLM-কে বলত না "কোন line এখনো চলেনি"। ফলে LLM আন্দাজে test লিখত।
- তুলনা করো এভাবে: পরীক্ষার আগে শিক্ষক বলছেন "যা ইচ্ছা পড়ো"। এটা এক কথা। আর "এই তিনটা chapter তুমি এখনো পড়োনি, এগুলো পড়ো" বললে অন্য কথা।

### গ. Paper কী solve করেছে?
- CoverUp আগে মাপে কোন line ও branch এখনো কোনো test-এ চলেনি। তারপর শুধু সেই অংশটুকু LLM-কে দেখায়।
- LLM-কে একটা `get_info` tool দেওয়া হয়েছে। LLM চাইলে কোনো function বা class-এর definition নিজে চেয়ে নিতে পারে।
- Test fail করলে বা coverage না বাড়লে error-টা LLM-কে আবার জানানো হয়। LLM আবার চেষ্টা করে।
- সবচেয়ে দরকারি তিনটা সংখ্যা:
  - CodaMosa-র কঠিন benchmark-এ CoverUp-এর per-module median coverage **79.6%**, CodaMosa (gpt4o)-এর **47.2%**। মানে মাঝের module-এ CoverUp প্রতি ১০০টা item-এর প্রায় ৮০টা চালায়, CodaMosa প্রায় ৪৭টা।
  - শুধু LLM-কে "test লেখো" বললে overall coverage **34.0%**, CoverUp-এ **60.3%**। মানে লাভটা শুধু LLM-এর জন্য নয়, CoverUp-এর design-এর জন্য।
  - সফল test-এর প্রায় **40%** এসেছে chat চালিয়ে যাওয়ার পর। মানে ১০০টার মধ্যে ৬০টা প্রথমবারে মিলেছে, বাকি ৪০টা আবার চেষ্টা করে।

### ঘ. কীভাবে solve করেছে?
1. আগে বর্তমান test চালিয়ে coverage মাপে। কোন line ও branch চলেনি তার list বানায়।
2. যে function বা method-এ ওই line আছে, সেটা কেটে নেয়। একে বলে segment, সাধারণত ৫০ line পর্যন্ত।
3. LLM-কে prompt পাঠায়: "তুমি expert Python developer। এই segment-এর এই line-গুলো চালায় এমন pytest test লেখো।" যে line চলেনি সেখানে `19:` ধরনের number বসানো থাকে।
4. LLM চাইলে `get_info` দিয়ে অন্য code-এর definition চেয়ে নেয়।
5. CoverUp test-টা চালায়। Pass করলে আর coverage বাড়লে test রেখে দেয়।
6. Fail করলে error message পাঠায়। Pass করে কিন্তু coverage না বাড়লে বলে "এই line-গুলো এখনো চলেনি"। এভাবে মোট ৩ বার পর্যন্ত চেষ্টা হয়।
7. প্রতিটা test আলাদা process-এ চালায়, যাতে এক test অন্য test নষ্ট না করে। কয়েকবার repeat-ও করে, যাতে কখনো pass কখনো fail করা (flaky) test ধরা যায়।
8. সব segment শেষে পুরো suite একসাথে চালিয়ে দেখে সব ঠিক আছে কিনা।

### ঙ. এরপর কী করা যায়?
- Authors নিজেরা বলেছেন: এক উত্তরে একাধিক test থাকলে একটা fail করলেই সব বাদ যায়। প্রতিটা আলাদা যাচাই করা ভালো হতো।
- Authors আরও বলেছেন: test-এর timeout ১ মিনিট একটু কম ছিল, আর conditional import-এ tool ভুল context দেয়।
- যা এখনো খোলা: paper শুধু coverage মেপেছে। Test আসলে ভুল ধরতে পারে কিনা (mutation score, assertion-এর মান) মাপেনি।
- আরেকটা খোলা প্রশ্ন: CoverUp বর্তমান code-কে ঠিক ধরে test লেখে (regression test)। AI agent-এর patch ভুল হলেও এই test pass করতে পারে।
- আমরা SPL3-তে করতে পারি: CoverUp-এর test-গুলোর উপর mutation score মাপা (কয়েকটা CM module-এ)।
- আমরা আরও করতে পারি: পুরনো code-এ test বানিয়ে patch করা code-এ চালানো (differential)। তাহলে agent-এর ভুল patch ধরা পড়বে।

> **মনে রাখো:**
> CoverUp = "কোন line চলেনি" LLM-কে বলে দেওয়া + error পেলে আবার চেষ্টা। তাই CodaMosa-র চেয়ে অনেক বেশি coverage।
> কিন্তু coverage মানে শুধু code চলেছে, ফল ঠিক কিনা যাচাই হয়েছে তা নয়। Paper oracle-এর শক্তি মাপেনি, আর এটাই আমাদের gap।


---

## ১. এক লাইনে Paper (TL;DR)

**CoverUp একটা tool যেটা প্রথমে মাপে কোন line/branch এখনো test-এ চলে না, তারপর শুধু সেই অংশের code (segment) LLM-কে দেখিয়ে বলে "এই নির্দিষ্ট line-গুলো চালায় এমন pytest test লেখো"; test চালিয়ে coverage আবার মাপে, আর error বা coverage না বাড়লে সেই কথা LLM-কে জানিয়ে chat চালিয়ে যায় — ফলে CodaMosa-র চেয়ে অনেক বেশি coverage পায় (per-module median line+branch 80% বনাম 47%)।**

**সহজ কথায়:** CoverUp LLM-কে বলে দেয় "এই line-গুলো এখনো চলেনি, ওগুলো চালানোর test লেখো"। Test ভুল হলে বা কাজ না করলে আবার জানায়। এতে CodaMosa-র চেয়ে অনেক বেশি code চলে।

### Supervisor-কে ৩০ সেকেন্ডে কীভাবে বলবো
> "Sir, Python-এ automatic unit test বানানোর আগের সেরা tool ছিল Pynguin (genetic algorithm) আর তার LLM-সহ version CodaMosa। CoverUp একটা সহজ কিন্তু কার্যকর idea দেখিয়েছে — LLM-কে পুরো code না দিয়ে, coverage tool দিয়ে বের করা 'কোন line চলেনি' সেই তথ্য prompt-এ সরাসরি দেওয়া, LLM-কে একটা `get_info` tool দেওয়া যাতে দরকারি definition নিজে চেয়ে নিতে পারে, আর test fail করলে বা coverage না বাড়লে error message ফেরত দিয়ে আবার চেষ্টা করানো। GPT-4o দিয়ে CodaMosa-র কঠিন benchmark-এ overall line+branch coverage 60.3% (CodaMosa-GPT-4o 45.2%) আর per-module median 79.6% (47.2%)। Ablation দেখায় এই লাভ শুধু LLM-এর জন্য নয় — শুধু LLM-কে জিজ্ঞেস করলে 34.0%। কিন্তু আমাদের assurance-এর জন্য বড় সতর্কতা: paper শুধু coverage মেপেছে, test-গুলো আসলে ভুল ধরতে পারে কিনা (mutation score, assertion-এর মান) মাপেনি। আর test-গুলো বর্তমান code-কেই 'সঠিক' ধরে লেখা regression test।"

---

## ২. Background — এই paper বুঝতে যা আগে জানা দরকার

### ২.১ Unit Test, pytest ও Test Suite
- **Unit test:** ছোট একটা function যেটা code-এর একটা অংশকে (function/method) কিছু input দিয়ে চালায় আর output ঠিক আছে কিনা `assert` দিয়ে যাচাই করে।
- **pytest:** Python-এর সবচেয়ে জনপ্রিয় test framework। `test_` দিয়ে শুরু হওয়া function-গুলো নিজে খুঁজে (test discovery) চালায়।
- **Test suite:** একটা project-এর সব test একসাথে।
- **monkeypatch / pytest-mock:** test চলার সময় কোনো variable, function বা environment সাময়িকভাবে বদলে দেওয়া, আর test শেষে **নিজে থেকে আগের অবস্থায় ফেরত** আনা। CoverUp prompt-এ এগুলো ব্যবহার করতে বলে (state pollution এড়াতে)।

**সহজ কথায়:** এগুলো দিয়ে test-এর সময় কোনো জিনিস সাময়িক বদলানো যায়। Test শেষ হলে আগের অবস্থা ফিরে আসে, তাই অন্য test নষ্ট হয় না।

### ২.২ Regression Testing বনাম Bug-finding Testing (খুব গুরুত্বপূর্ণ)
- **Regression test:** ধরে নেওয়া হয় **এখনকার code সঠিক**। Test এখনকার আচরণকে "লিখে রাখে", যাতে ভবিষ্যতে কেউ code বদলালে আচরণ বদলে গেলে ধরা পড়ে।
- CoverUp স্পষ্টভাবে **regression test** বানায় (paper-এর Introduction: test generation tool সাধারণত "assuming that the source code is correct")।
- **আমাদের জন্য তাৎপর্য (আমার পর্যবেক্ষণ):** যদি AI agent-এর patch করা code-এর উপর CoverUp চালাই, তাহলে test-গুলো patch-এর আচরণকেই "সঠিক" ধরে নেবে — patch ভুল হলেও test pass করবে। তাই patch যাচাইয়ে এটা সরাসরি oracle নয়; **differential** ভাবে (পুরনো code বনাম patch করা code) ব্যবহার করতে হবে (Section ১৪, ১৬)।

### ২.৩ Test Oracle ও Oracle Problem
- **Test oracle:** "সঠিক output কী" — সেই সিদ্ধান্ত। Unit test-এ oracle হলো `assert` statement।
- **Oracle problem:** automatic ভাবে input বানানো সহজ, কিন্তু "সঠিক উত্তর কী হওয়া উচিত" তা জানা কঠিন। Assertion ছাড়া test শুধু "crash করে না" যাচাই করে — এটা খুব দুর্বল oracle।
- Paper নিজেই একটা উদাহরণ দিয়েছে: CodaMosa-র `mimesis` package-এর জন্য বানানো test-এ **কোনো assertion নেই**, তাই random value-তেও fail করে না (Section 4.1)।

### ২.৪ Code Coverage: Line ও Branch
- **Line (statement) coverage:** মোট executable line-এর মধ্যে কত % অন্তত একবার চলেছে।
- **Branch coverage:** প্রতিটা সিদ্ধান্তের (if/else, loop) প্রতিটা দিক — অর্থাৎ control flow-এর প্রতিটা "arc" (source line থেকে destination line) — চলেছে কিনা। CoverUp prompt-এ branch লেখে এভাবে: `603->exit` (line 603 থেকে function থেকে বের হয়ে যাওয়া), `610->608` (line 610 থেকে line 608-এ লাফ)।
- **Line + Branch (combined):** দুটোকে একসাথে গুনে একটা সংখ্যা (সূত্র Section ৬-এ)।
- **Python-এ branch coverage line coverage-কে "subsume" করে না:** সাধারণত ভাবা হয় সব branch চললে সব line-ও চলবে। কিন্তু paper বলছে Python-এ exception ছুঁড়লে সেটা branch হিসেবে রেকর্ড হয় না, তাই দুটো metric-ই আলাদা করে দরকার।
- **সবচেয়ে গুরুত্বপূর্ণ সতর্কতা:** coverage শুধু বলে code **চলেছে কিনা**, ফল **ঠিক কিনা যাচাই হয়েছে কিনা** বলে না। Assertion ছাড়া test-ও 100% coverage দিতে পারে।

**সহজ কথায়:** Coverage হলো "কোন প্রশ্ন পড়া হলো" গোনা। "উত্তর ঠিক কিনা" সেটা এখানে দেখা হয় না।

### ২.৫ Coverage Tool: SlipCover ও coverage.py
- **coverage.py:** Python-এর প্রচলিত coverage tool। Paper অনুযায়ী এটা **260% পর্যন্ত overhead** যোগ করে।
- **SlipCover:** একই authors-এর আগের tool (ISSTA 2023), "near-zero overhead"। CoverUp প্রতিটা generated test চালিয়ে বারবার coverage মাপে, তাই দ্রুত tool জরুরি।

### ২.৬ AST (Abstract Syntax Tree)
Source code-কে একটা গাছের মতো structure-এ রূপান্তর — কোন class-এর ভেতরে কোন method, কোন method-এর ভেতরে কোন line। CoverUp Python-এর `ast` module দিয়ে খুঁজে বের করে কোন "uncovered" line কোন function/class-এর ভেতরে আছে।

### ২.৭ Search-Based Software Testing (SBST) ও Pynguin
- **SBST:** test generation-কে একটা optimization সমস্যা হিসেবে দেখা। **Genetic algorithm** ব্যবহার হয়: কিছু random test দিয়ে শুরু (population), প্রতিটার "fitness" (কত coverage দেয়) মাপা, ভালোগুলো থেকে mutation (ছোট পরিবর্তন) ও crossover (দুটো মেশানো) করে নতুন প্রজন্ম — যতক্ষণ coverage বাড়ে।
- **Pynguin:** Python-এর জন্য SBST tool (Lukasczyk & Fraser, ICSE 2022)।
- **সমস্যা — Coverage plateau:** test mutation বারবার একই execution path-এ ঘুরতে থাকে, search "আটকে" যায়। যেমন একটা branch-এ যেতে একটা নির্দিষ্ট format-এর string বা নির্দিষ্ট object লাগে — random mutation দিয়ে তা পাওয়া প্রায় অসম্ভব।

### ২.৮ CodaMosa (Hybrid SBST + LLM)
- **CodaMosa (Lemieux et al., ICSE 2023):** Pynguin-এর progress দেখে; search আটকে গেছে মনে হলে **Codex** LLM-কে একটা test চায়, সেই test দিয়ে SBST-কে আবার "seed" করে।
- **Codex:** OpenAI-এর পুরনো code model, এখন আর পাওয়া যায় না — তাই এই paper CodaMosa (codex)-এর পুরনো generated test ব্যবহার করেছে আর নিজেরা GPT-4o দিয়ে একটা version বানিয়েছে।
- CodaMosa-র প্রতিটা module-এ 10 মিনিট sequential search চলে।
- CoverUp বনাম CodaMosa-র মূল দার্শনিক পার্থক্য: CodaMosa-তে **search মূল, LLM সাহায্যকারী**; CoverUp-এ **LLM মূল, coverage measurement তাকে দিক দেখায়**।

### ২.৯ Mutation Testing ও MuTAP
- **Mutation testing:** code-এ ইচ্ছা করে ছোট ভুল ঢোকানো (যেমন `>` কে `>=` করা) — প্রতিটা ভুল version-কে **mutant** বলে। Test suite যদি mutant-এ fail করে, mutant "killed"; না করলে "survived"।
- **Mutation score:** কত % mutant killed হলো। এটা **oracle-এর শক্তি** মাপে — coverage যা পারে না (সূত্র Section ৬-এ)।
- **MuTAP (Dakhel et al., IST 2024):** LLM দিয়ে test চায়, MutPy দিয়ে mutation testing করে, আর survived mutant-এর জন্য LLM-কে নতুন assertion লিখতে বলে।
- **খুব গুরুত্বপূর্ণ:** CoverUp নিজে mutation testing **ব্যবহারও করে না, মাপেও না**। MuTAP-এর সাথে তুলনাও শুধু coverage দিয়ে করা হয়েছে। অর্থাৎ MuTAP-এর মূল শক্তি (assertion-এর মান) এই তুলনায় ধরা পড়েনি — Section ১২-এ critique।

**সহজ কথায়:** Mutation score হলো test-এর "ভুল ধরার ক্ষমতা"-র পরীক্ষা। ইচ্ছা করে code-এ ভুল ঢুকিয়ে দেখা হয় test সেটা ধরে কিনা। CoverUp এটা মাপেনি।

### ২.১০ Coverage-guided Generation ও Segment / Gap Prompting
- **Coverage-guided generation:** test generation-এর প্রতিটা ধাপে coverage মেপে পরের ধাপ ঠিক করা।
- **Segment prompting (CoverUp-এর idea):** পুরো file না দিয়ে শুধু সেই function/method/class (segment) দেওয়া যেখানে "gap" (uncovered line/branch) আছে, আর gap-এর line number চিহ্নিত করে দেওয়া (যেমন `19:` tag)। এতে prompt ছোট, সস্তা, আর LLM-এর মনোযোগ সঠিক জায়গায়।

### ২.১১ Iterative LLM Feedback Loop (Continued Chat)
LLM-এর প্রথম উত্তর ভুল হলে নতুন chat শুরু না করে **আগের সব message + LLM-এর উত্তর + নতুন feedback** একসাথে পাঠানো। CoverUp দুই ধরনের feedback দেয়:
1. **Error feedback:** test fail করলে pytest-এর error output (Figure 7)।
2. **Coverage feedback:** test pass করলেও coverage না বাড়লে "এখনো line 615 আর branch `603->exit`… চলেনি" (Figure 6)।

Default-এ প্রথম prompt-এর পর **সর্বোচ্চ আরও ২টা prompt** (মোট ৩টা চেষ্টা)।

**সহজ কথায়:** একজন ছাত্রকে ভুল উত্তরের পর "এই জায়গায় ভুল হয়েছে, আবার চেষ্টা করো" বলার মতো। CoverUp LLM-কে মোট ৩ বার সুযোগ দেয়।

### ২.১২ Tool / Function Calling
LLM API-তে একটা "tool" (function)-এর বর্ণনা পাঠানো যায়; LLM চাইলে text না লিখে বলতে পারে "এই function-টা এই argument দিয়ে চালাও"। Program সেটা চালিয়ে ফল আবার chat-এ যোগ করে। CoverUp-এর tool: **`get_info(name)`** — কোনো class, function, variable বা module-এর definition চাইলে CoverUp static analysis দিয়ে source code-এর প্রাসঙ্গিক অংশ ফেরত দেয়। এটা আজকের coding agent-দের "file পড়া" tool-এর একটা ছোট, নিয়ন্ত্রিত রূপ।

### ২.১৩ Persona Prompting ও Temperature
- **Persona:** prompt-এর শুরুতে "You are an expert Python test-driven developer" — LLM-কে একটা ভূমিকা দেওয়া।
- **Temperature 0:** সবচেয়ে সম্ভাব্য token বাছাই, তাই output প্রায় deterministic (পুরোপুরি নয়)।

### ২.১৪ State Pollution ও Test Isolation
- **State pollution:** একটা test global variable, file, environment বদলে দিয়ে পরিষ্কার না করলে **অন্য test** fail করে, যদিও একা চালালে সব pass। Paper-এর Figure 10: LLM-এর test `ansible`-এর global constant বদলে তারপর `del` করে মুছে ফেলে — অন্য test ভেঙে যায়।
- আগের গবেষণা (Fraser & Arcuri 2014): EvoSuite-এর generated test class-গুলোর **50%-এ side effect**।
- **Test isolation:** প্রতিটা test আলাদা process-এ চালানো — CoverUp Unix `fork()` দিয়ে করে, যাতে এক test-এর memory পরিবর্তন অন্যটায় না পৌঁছায়।

### ২.১৫ Flaky Test
একই code-এ কখনো pass, কখনো fail করা test (যেমন randomness, সময়, network-এর উপর নির্ভরশীল)। Paper-এর Figure 11: `mimesis`-এর blood type random; LLM ভেবেছে "0-", "0+" (শূন্য), আসলে "O-", "O+" (ইংরেজি অক্ষর O) — তাই test মাঝে মাঝে fail করে। CoverUp **pytest-repeat** দিয়ে প্রতিটা নতুন test কয়েকবার চালায়, যাতে flaky আচরণ ধরা পড়ে।

### ২.১৬ Ablation Study
একটা system-এর একটা অংশ সরিয়ে দিয়ে দেখা performance কতটা কমে — তাহলে বোঝা যায় কোন অংশ কতটা দরকারি।

### ২.১৭ Overall Coverage বনাম Per-module Median
- **Overall:** সব module-এর সব line একসাথে গুনে একটা % — বড় module বেশি ওজন পায়।
- **Per-module median:** প্রতিটা module-এর আলাদা % বের করে মাঝের মান — প্রতিটা module সমান ওজন পায়।
CoverUp-এ এই দুটো সংখ্যা অনেক আলাদা (60.3% বনাম 79.6%) — কারণ Section ৬-এ।

### ২.১৮ Paired Permutation Test
দুটো tool একই module-গুলোতে চালানো হলে, প্রতিটা module-এ পার্থক্য নিয়ে দেখা হয় — "পার্থক্যগুলোর চিহ্ন এলোমেলো হলে এত বড় গড় পার্থক্য কত ঘন ঘন আসতো?" খুব কম হলে (p-value ছোট) পার্থক্যটা কাকতালীয় নয়। কোনো distribution ধরে নিতে হয় না।

### ২.১৯ Asynchronous Execution ও Rate Limiting (Leaky Bucket)
- **asyncio:** অনেকগুলো LLM request একসাথে পাঠানো, উত্তরের অপেক্ষায় বসে না থেকে। Paper অনুযায়ী serial-এর তুলনায় **500x speedup**।
- **Leaky bucket:** request একটা "বালতি"-তে জমে আর নির্দিষ্ট হারে বের হয় — যাতে OpenAI-এর rate limit পার না হয় (`aiolimiter` module)।

**সহজ কথায়:** অনেক request একসাথে পাঠালে OpenAI আটকে দেয়। তাই request-গুলো একটা বালতিতে জমে, আর ধীরে ধীরে বের হয়।
- **Checkpointing:** মাঝপথে থামলে (যেমন account-এ টাকা শেষ) পরে আবার সেখান থেকে শুরু।

### ২.২০ Property-based Test
নির্দিষ্ট input-এর বদলে একটা "property" (যেমন "sort করার পর list-এর দৈর্ঘ্য একই থাকে") অনেক random input-এ যাচাই করা। CoverUp এটা চায় না, তবে LLM লিখলে গ্রহণ করে।

---

## ৩. Problem Statement — কী সমস্যা ছিল?

### ৩.১ মূল সমস্যা
1. **হাতে test লেখা পরিশ্রমসাধ্য** — developer-রা প্রায়ই লেখেই না (Daka & Fraser 2014)।
2. **High coverage test বানানো কঠিন:** SBST (Pynguin) coverage plateau-তে আটকে যায়; CodaMosa কিছুটা উন্নতি করলেও কঠিন code-এ coverage কম।
3. **আগের LLM-based পদ্ধতিগুলো coverage তথ্য ব্যবহার করে না:**
   - Codex-based Java test generation (Bareiß et al.): compile না হলে test ফেলে দেয়, coverage-এর কথা বলে না।
   - TestPilot (JavaScript): error হলে chat চালায়, কিন্তু coverage-ভিত্তিক prompt নেই, coverage না বাড়লে chat চালায় না, tool function নেই।
   - ChatUniTest (Java): coverage দিয়ে কোন line বাকি তা বলে না।
   - TestGen-LLM (Meta, Kotlin): coverage না বাড়লে test ফেলে দেয়, LLM-কে ঠিক করতে বলে না।
   - MuTAP: syntax error ছাড়া অন্য error বা coverage-এর জন্য chat চালায় না; context দেওয়ার ব্যবস্থা নেই; dataset code-এর ভেতরে hardcoded।
   - SymPrompt: path constraint দিয়ে prompt বানায়, কিন্তু public নয়; error হলে শুধু line মুছে syntax ঠিক করার চেষ্টা।
4. **বাস্তব Python package-এ কাজ করা:** অনেক code-এর dependency অনেক, type annotation নেই, external code ব্যবহার করে — LLM ভুল ধারণা করে।
5. **Practical সমস্যা:** LLM-এর context limit, token খরচ, API rate limit, ধীর test execution, state pollution, flaky test।

**সহজ কথায়:** সমস্যা তিন স্তরের। প্রথমে test লেখাই কষ্ট। তারপর আগের tool-গুলো ঠিকমতো gap বোঝে না। শেষে বাস্তব project-এ নানা ঝামেলা (dependency, flaky test) আছে।

### ৩.২ কেন এটা গুরুত্বপূর্ণ?
Regression test না থাকলে code বদলানোর সময় পুরনো feature ভাঙছে কিনা ধরা যায় না। আর **আমাদের domain-এ**: AI agent-এর patch যাচাই করতে যে test লাগে, সেটা প্রায়ই নেই বা দুর্বল (SWE-bench-এ 60% task-এ মাত্র ১টা F2P test — SWE-bench analysis দেখো)। তাই automatic, high-coverage test generation হলো assurance layer-এর একটা মৌলিক উপাদান।

---

## ৪. Goal ও Research Questions

**Goal:** Coverage analysis + code context + feedback একসাথে prompt-এ দিয়ে LLM-কে এমনভাবে চালানো যাতে Python-এর জন্য high line ও branch coverage-এর regression test তৈরি হয় — যেকোনো Python package-এ।

Paper-এর explicit RQ:
- **RQ1:** CoverUp-এর test-এর coverage কি state of the art-এর (CodaMosa, MuTAP) চেয়ে ভালো? (Section 4.2)
- **RQ2:** শুধু LLM-কে test চাওয়ার তুলনায় CoverUp কতটা কার্যকর? (Section 4.3)
- **RQ3:** Continued dialogue (chat চালিয়ে যাওয়া) coverage বাড়াতে কতটা কার্যকর? (Section 4.4)
- **RQ4:** CoverUp চালানোর খরচ CodaMosa-র তুলনায় কেমন? (Section 4.5)
- **RQ5:** CoverUp-এর প্রতিটা component performance-এর জন্য কতটা জরুরি? (Section 4.6)

**Contribution (paper-এর দাবি):** (১) CoverUp approach; (২) empirical analysis যে এটা state of the art এগিয়ে নেয়; (৩) ablation study যে লাভের বড় অংশ LLM-এর বাইরে, CoverUp-এর design থেকে আসে।

**সহজ কথায়:** Authors তিনটা কথা বলছেন। এক: নতুন একটা পদ্ধতি বানিয়েছি। দুই: সেটা আগের সেরার চেয়ে ভালো। তিন: ভালো হওয়ার কারণ শুধু LLM নয়, আমাদের design।

---

## ৫. Methodology — কীভাবে কাজটা করা হয়েছে

### ৫.১ সামগ্রিক Algorithm (Figure 1)
1. বিদ্যমান test suite চালিয়ে coverage মাপা (না থাকলে শূন্য থেকে)।
2. Coverage-এর gap থেকে **code segment** বের করা (Section 3.1)।
3. প্রতিটা segment-এর জন্য LLM-কে **initial prompt** (Section 3.2)।
4. LLM-এর test চালিয়ে **verification** — pass করে ও coverage বাড়ায়? হলে রাখা; না হলে **continued chat** (Section 3.3)।
5. পুরো সময় LLM `get_info` tool ব্যবহার করতে পারে (Section 3.4)।
6. সব segment শেষে **integration check** — পুরো suite একসাথে ঠিক চলে কিনা (Section 3.5)।
7. পুরো প্রক্রিয়া আবার চালানো যায় — আগের বার বাদ পড়া segment-এ আবার মনোযোগ।

**সহজ কথায়:** CoverUp একটা চক্র: gap খোঁজো, LLM-কে বলো, test চালাও, ফল দেখো, দরকারে আবার বলো। চক্র শেষ হলে চাইলে আবার শুরু করা যায়।

### ৫.২ Code Segmentation (Section 3.1, Algorithm 1)
- প্রথমে "interesting" line-এর set: যে line চলেনি, আর যে branch চলেনি তার source বা destination line।
- AST-এ খোঁজা হয় কোন class/function/method এই line ধারণ করে।
- যদি পাওয়া node একটা **class** হয় এবং তার দৈর্ঘ্য limit-এর বেশি হয়, তাহলে class-এর definition "context" হিসেবে রেখে ভেতরের ছোট node (method) খোঁজা — recursive।
- Method-এর segment-এ class definition-এর কয়েকটা line context হিসেবে থাকে, অন্য method বাদ (Figure 2: `flutils`-এর একটা উদাহরণে line 1 আর 2-এর মাঝের 200 line বাদ দেওয়া হয়েছে)।
- **Comment রেখে দেওয়া হয়** — authors দেখেছেন এতে LLM-এর বোঝা ভালো হয়।
- **Default segment size: 50 line** (evaluation-এও এটাই)।
- কেন ছোট segment: context window শুধু প্রথম prompt নয়, পুরো chat (tool call, উত্তর, continued prompt) মিলিয়ে ভরে যায়; লম্বা code prompt-এ ভুল বাড়ে (Rosas et al. 2024); আর token-এ টাকা লাগে।

**সহজ কথায়:** পুরো file দিলে LLM গোলমাল করে, খরচও বেশি। তাই শুধু যেখানে gap, সেই ছোট অংশ দেওয়া হয়।

### ৫.৩ Initial Prompt-এর ছয় অংশ (Section 3.2, Figure 3)
| অংশ | কী থাকে | কেন |
|---|---|---|
| 1 | Persona: "expert Python test-driven developer" | ভালো মানের test-এর দিকে ঠেলা |
| 2 | কোন file থেকে code, আর কোন line/branch চলে না (line range দিয়ে সংক্ষেপে) | Gap-এর তথ্য, কম token |
| 3 | pytest test function চাওয়া, যা সব missing line ও branch চালায়; `get_info` ব্যবহারে উৎসাহ | মূল নির্দেশ |
| 4 | "include assertions", "clean up… avoid state pollution", `monkeypatch`/`pytest-mock` ব্যবহার, top-level code না রাখা, `pytest.main` call না করা, সবসময় পুরো test script পাঠানো | ব্যবহারযোগ্য test |
| 5 | শুধু backtick-এর ভেতরে Python code, ব্যাখ্যা নয় | Extraction সহজ, কম token |
| 6 | Code segment — আগে generated import statement, আর uncovered line-গুলোতে line number tag (যেমন `19:`) | Context ও gap-এর অবস্থান |

গুরুত্বপূর্ণ design detail:
- **Top-level `pytest.main` নিষেধ:** GPT-4-এর প্রথম দিকের test-এ এমন call ছিল, যাতে pytest বারবার test discovery শুরু করে অচল হয়ে যেত।
- **Generated import:** source থেকে হুবহু না নিয়ে static analysis দিয়ে তৈরি; relative import-কে absolute import-এ রূপান্তর (না হলে package-এর বাইরে test-এ invalid)। Import না দিলে LLM symbol সম্পর্কে ভুল ধারণা করে।
- **প্রতিটা uncovered line-এ number tag:** শুধু excerpt-এর শুরুর line number দিলে LLM-এর test coverage বাড়ায় না — authors-এর পর্যবেক্ষণ।
- Prompt OpenAI chat API-এর JSON request-এ `messages`-এর ভেতরে যায়, সাথে `model` ও `temperature` (Figure 4)।

**সহজ কথায়:** Prompt-এর ছয়টা অংশ আসলে ছয়টা ছোট নির্দেশ: তুমি কে, কোথায় gap, কী চাই, কী করা যাবে না, কীভাবে উত্তর দেবে, আর code-টা কী।

### ৫.৪ Verification ও Continued Chat (Section 3.3)
- নতুন test চালিয়ে SlipCover দিয়ে coverage মাপা।
- **Test pass করে এবং coverage বাড়ায় → save।**
- **Coverage বাড়ায় না, অথবা failure/error → chat চালানো:** আগের message + LLM-এর উত্তর + নতুন prompt (Figure 5)।
  - Coverage follow-up (Figure 6): "এই test-এ এখনো coverage নেই: line 615 আর branch `603->exit`, `610->608`, `618->exit` চলে না। ঠিক করো।"
  - Error follow-up (Figure 7): "Test চালালে error আসে" + pytest-এর error excerpt (যেমন `AssertionError: assert 13 == 11`)।
- **সীমা:** প্রথম prompt-এর পর সর্বোচ্চ ২টা অতিরিক্ত prompt (default ও evaluation দুটোতেই)।
- **Missing module:** test-এ এমন module লাগলে যা install নেই (যেমন `ansible`-এর জন্য `pytest-ansible`), CoverUp চাইলে নিজে install করে `requirements.txt` format-এ লিখে রাখে।
- **একটা দুর্বলতা (paper নিজে বলেছে):** LLM-এর এক উত্তরে একাধিক test function থাকলে, একটা fail করলেই **সবগুলো reject**।

**সহজ কথায়:** একটা test খারাপ হলে বাকিগুলো ভালো হলেও সব ফেলে দেওয়া হয়। এতে কিছু ভালো test নষ্ট হয়।

### ৫.৫ Tool Function `get_info` (Section 3.4, Figure 8–9)
- প্রতিটা chat request-এর `tools` JSON element-এ `get_info`-এর বর্ণনা থাকে।
- LLM text-এর বদলে এক বা একাধিক `get_info` call চাইতে পারে; CoverUp ফল যোগ করে chat চালায়।
- `get_info` function, class, module বা **variable** খোঁজে (Python-এ constant ও alias variable assignment দিয়ে তৈরি হয় বলে variable জরুরি)। প্রথমে segment-এর module-এ, তারপর import ধরে অন্য module-এ।
- Assignment, import, function — পুরো definition দেয়। Class/module বড় হলে সংক্ষিপ্ত রূপ: method-এর body বাদ দিয়ে `...` (Python-এ valid no-op) বসায় — যাতে LLM বোঝে method আছে, কিন্তু body দেখানো হয়নি।
- উদাহরণ: `class A`-এর `__init__(self, *, initial_x=0)` দেখে LLM বোঝে `x` keyword argument `initial_x` দিয়ে দিতে হয়। Tool না দিলে LLM সরাসরি `x` পাঠাতে চেষ্টা করে, error হয়।
- Initial ও continuation — দুই ধরনের prompt-এই tool পাওয়া যায়।

**সহজ কথায়:** `get_info` হলো LLM-এর "ওই function-টা একটু দেখাও" বলার সুযোগ। আজকের coding agent-রা যে file পড়ে, এটা তারই ছোট রূপ।

### ৫.৬ Integration Check ও State Pollution (Section 3.5)
CoverUp শুধু সেই test রাখে যা **একা চালালে** pass করে; কিন্তু একসাথে চালালে state pollution হতে পারে। তিনটা বিকল্প:
1. **প্রতিটা test isolation-এ চালানো** (`fork()`-ভিত্তিক) — **default, evaluation-এ এটাই ব্যবহৃত**।
2. **Polluting test disable:** পুরো suite চালিয়ে fail হলে subset ছোট করে করে polluting test খোঁজা ও বন্ধ করা।
3. **Failing test disable:** দ্রুত, কিন্তু অপ্রয়োজনে test বন্ধ হতে পারে (coverage কমে), আর polluting test থেকেও যেতে পারে।

বন্ধ করা test user-এর review-এর জন্য রাখা থাকে।

**সহজ কথায়:** Test-গুলো আলাদা করে চালালে ঠিক, কিন্তু একসাথে চালালে একটা অন্যটাকে নষ্ট করতে পারে। CoverUp তাই প্রতিটাকে আলাদা ঘরে (process) রেখে চালায়।

### ৫.৭ Flaky Test Handling (Section 3.6)
`pytest-repeat` দিয়ে প্রতিটা নতুন test একাধিকবার চালানো; fail করলে chat চালিয়ে LLM-কে ঠিক করার সুযোগ। **কতবার repeat — paper-এ নির্দিষ্ট সংখ্যা দেওয়া নেই** ("a few times")।

### ৫.৮ অন্যান্য Engineering (Section 3.7)
- asyncio দিয়ে async prompting ও verification — serial-এর তুলনায় **500x speedup** (evaluation-এ পর্যবেক্ষণ)।
- Timeout ও API error নিজে handle করা; `aiolimiter` দিয়ে leaky bucket rate limiting; file-এ checkpointing।

---

## ৬. Mathematical Formulation — সূত্র ও ব্যাখ্যা

Paper-এ formal equation প্রায় নেই (Algorithm 1 ছাড়া)। নিচে paper-এর বর্ণনা থেকে formal রূপ দেওয়া হলো, যাতে supervisor-কে metric-গুলো স্পষ্টভাবে দেখানো যায়। সূত্রের ভাষা আমার, কিন্তু সব সংখ্যা paper-এর; নিজের হিসাব "আমার হিসাব" দিয়ে চিহ্নিত।

### ৬.১ মূল Notation
- $P$ = code under test (একটা module বা পুরো package)
- $L$ = $P$-এর executable line-এর set; $N_L$ = তাদের সংখ্যা
- $B$ = $P$-এর branch (arc)-এর set; প্রতিটা branch একটা জোড়া $(s, d)$ — source line $s$ থেকে destination $d$ (destination হতে পারে "exit"); $N_B$ = সংখ্যা
- $T$ = test suite; প্রতিটা test $t \in T$
- $\text{lines}(t) \subseteq L$, $\text{arcs}(t) \subseteq B$ = test $t$ চালালে যে line ও branch চলে

### ৬.২ Suite-এর Coverage
Suite-এর covered set হলো প্রতিটা test-এর covered set-এর union:
$$
L_T = \cup_{t \in T}\, \text{lines}(t), \qquad B_T = \cup_{t \in T}\, \text{arcs}(t)
$$
(Paper-এ সব test isolation-এ চালানো হয়, তাই প্রতিটা test-এর coverage আলাদা এবং suite-এর coverage এই union।)

**সহজ কথায়:** পুরো suite-এর coverage মানে প্রতিটা test যা যা চালিয়েছে তার মিলিত তালিকা। একটা line কোনো একটা test-এ চললেই সেটা গোনা হয়।

Line, branch ও combined coverage (coverage.py/SlipCover-এর প্রচলিত সংজ্ঞা; paper সূত্রটা লেখেনি):
$$
\text{Cov}_{L}(T) = \frac{N_{L_T}}{N_L} \times 100, \qquad \text{Cov}_{B}(T) = \frac{N_{B_T}}{N_B} \times 100
$$
$$
\text{Cov}_{L+B}(T) = \frac{N_{L_T} + N_{B_T}}{N_L + N_B} \times 100
$$
**মানে:** combined metric-এ line আর branch দুটোকে একই "item" হিসেবে গোনা হয়। তাই combined মান সবসময় line ও branch-এর মাঝামাঝি থাকে — Table 1-এ CoverUp: line 63.8%, branch 49.2%, combined 60.3% (মাঝে, line-এর কাছে, কারণ সাধারণত line-এর সংখ্যা branch-এর চেয়ে বেশি)।

**সহজ কথায়:** Line coverage = চলা line ÷ মোট line। Branch coverage = চলা branch ÷ মোট branch। Combined হলো দুটোকে একসাথে গুনে একটা সংখ্যা।

**Missing set (prompt-এ যা যায়):**
$$
M_L = \{\, l \in L : l \notin L_T \,\}, \qquad M_B = \{\, b \in B : b \notin B_T \,\}
$$
অর্থাৎ যে line ও branch এখনো কোনো test-এ চলেনি।

**সহজ কথায়:** $M_L$ আর $M_B$ হলো "বাকি কাজের তালিকা"। CoverUp এটাই LLM-কে বলে দেয়।

**Worked example (Figure 6, আসল সংখ্যা):** একটা segment-এ coverage follow-up prompt বলছে line 615 আর branch `603->exit`, `610->608`, `618->exit` চলেনি। তাহলে ঐ segment-এর জন্য $M_L = \{615\}$, $M_B = \{(603, \text{exit}), (610, 608), (618, \text{exit})\}$ — মোট 1 + 3 = 4টা item বাকি।

### ৬.৩ "Interesting" Line ও Segment (Algorithm 1)
প্রতিটা file $f$-এর জন্য:
$$
I_f = M_L(f) \cup \{\, s, d : (s, d) \in M_B(f) \,\}
$$
প্রতিটা $l \in I_f$-এর জন্য AST-এ $l$ ধারণকারী সবচেয়ে বাইরের class/function node $n$ খোঁজা হয়; তারপর:
$$
\text{while } \left(n \text{ is a Class}\right) \land \left(\text{len}(n) > s_{\max}\right) \land \left(\exists\, n' \subseteq n \text{ যা } l \text{ ধারণ করে}\right): \quad \text{context} = \text{context} \cup \{n\},\; n = n'
$$
শেষে segment set-এ $\{n, \text{context}\}$ যোগ হয়। এখানে $s_{\max}$ = Algorithm 1-এর `max_len`; evaluation-এ $s_{\max} = 50$ line।

**সহজ ভাষায়:** class ছোট হলে পুরো class একটা segment; বড় হলে class-এর মাথাটুকু context হিসেবে রেখে ভেতরের method-টা segment।

**সহজ কথায়:** Algorithm 1 আসলে "কোন অংশ কাটবো" ঠিক করে। ছোট হলে পুরোটা, বড় হলে শুধু সংশ্লিষ্ট method আর class-এর মাথাটুকু।

### ৬.৪ Feedback Loop — Formal রূপ
Segment $s$, বর্তমান suite $T$। চেষ্টা $k = 1, 2, \ldots, K$ (evaluation-এ $K = 3$: প্রথম prompt + সর্বোচ্চ 2টা continuation)। চেষ্টা $k$-এ LLM test set $U_k$ দেয়। Acceptance:
$$
\text{Accept}(U_k) = \text{pass}(U_k) \;\land\; \text{Cov}(T \cup U_k) > \text{Cov}(T)
$$

**সহজ কথায়:** Test রাখা হবে দুটো শর্তে: সব test pass করতে হবে, আর coverage বাড়তে হবে। একটাও না মিললে feedback দিয়ে আবার চেষ্টা।

- $\text{pass}(U_k)$ = $U_k$-এর **সব** test isolation-এ pass করে (একটা fail করলে পুরো $U_k$ reject — Section 4.2)। Flaky ধরতে প্রতিটা কয়েকবার চালানো হয়।
- Accept হলে $T = T \cup U_k$, loop শেষ।
- না হলে, feedback $F_k$ তৈরি:
$$
F_k = \begin{cases}
\text{error excerpt}, & \text{যদি } \neg\, \text{pass}(U_k) \\
\text{remaining } M_L, M_B \text{ of } s, & \text{যদি pass কিন্তু coverage বাড়েনি}
\end{cases}
$$
- পরের request-এর message history: $H_{k+1} = H_k \oplus U_k \oplus F_k$ (এখানে $\oplus$ = message যোগ করা)। $k = K$ হলেও accept না হলে segment-টা এই pass-এ বাদ।
- যেকোনো সময় LLM $U_k$-এর বদলে `get_info` call চাইতে পারে; তখন ফল $H$-এ যোগ হয়।

**গুরুত্বপূর্ণ পর্যবেক্ষণ (আমার):** Acceptance শর্তে **oracle-এর কোনো শর্ত নেই** — test-এ assertion আছে কিনা, assertion অর্থবহ কিনা, তা যাচাই হয় না। শুধু "pass" আর "coverage বাড়ে"। তাই optimization pressure পুরোপুরি coverage-এর দিকে। এটা CG12-এর (assurance signal-এর বিরুদ্ধে optimization) একটা ছোট রূপ।

**সহজ কথায়:** CoverUp শুধু "চলেছে কিনা" দেখে, "ঠিক কিনা" দেখে না। তাই যে test শুধু code চালায় কিন্তু কিছু যাচাই করে না, সেটাও রয়ে যেতে পারে।

### ৬.৫ Continued Chat-এর অবদান (RQ3)
$S$ = মোট successful test (pass করে ও coverage বাড়ায়), $S_k$ = যেগুলো চেষ্টা $k$-এ এসেছে:
$$
\pi_k = \frac{S_k}{S} \times 100, \qquad \sum_{k=1}^{3} \pi_k = 100
$$
Paper (CM suite): $\pi_1 = 60.3$%, $\pi_2 = 27.2$%, $\pi_3 = 12.5$%। যোগ = 100.0 ✓।
$$
\text{Iteration-এর অবদান} = \pi_2 + \pi_3 = 27.2 + 12.5 = 39.7 \approx 40 \text{ percent}
$$
**ব্যাখ্যা:** প্রতিটা নতুন চেষ্টায় সাফল্য কমে (60.3 → 27.2 → 12.5), কিন্তু chat না চালালে প্রায় 40% সফল test হারাতাম। **সতর্কতা (আমার পর্যবেক্ষণ):** এগুলো সফল test-এর **ভাগ**, প্রতিটা চেষ্টার **success rate** নয় — কতগুলো segment-এ মোট কতবার চেষ্টা হয়েছে, paper তা দেয়নি।

**সহজ কথায়:** ১০০টা সফল test-এর মধ্যে ৬০টা প্রথমবারে, ২৭টা দ্বিতীয় চেষ্টায়, ১২-১৩টা তৃতীয় চেষ্টায়। Chat বন্ধ রাখলে প্রায় ৪০টা হারাতাম।

### ৬.৬ Coverage Gain
দুটো tool $A$ ও $B$-এর জন্য:
$$
\Delta_{pp} = \text{Cov}(A) - \text{Cov}(B) \quad (\text{percentage point}), \qquad \rho = \frac{\text{Cov}(A)}{\text{Cov}(B)}
$$
আর "বাকি gap-এর কত অংশ বন্ধ হলো" (আমার প্রস্তাবিত, paper-এ নেই):
$$
\text{GapClosed} = \frac{\text{Cov}(A) - \text{Cov}(B)}{100 - \text{Cov}(B)}
$$

**সহজ কথায়:** Coverage gain মানে "কতটা এগিয়েছে"। 32.4 percentage point এগিয়ে থাকা মানে CodaMosa যে অংশ বাকি রেখেছিল, তার প্রায় ৬১% CoverUp ধরেছে।

**Worked example (Table 1, per-module median line+branch, CoverUp বনাম CodaMosa-gpt4o):**
- $\Delta_{pp} = 79.6 - 47.2 = 32.4$ pp
- $\rho = 79.6 / 47.2 \approx 1.69$
- **আমার হিসাব:** $\text{GapClosed} = 32.4 / (100 - 47.2) = 32.4 / 52.8 \approx 0.614$ — অর্থাৎ CodaMosa (gpt4o) যা cover করতে পারেনি, তার প্রায় 61% CoverUp cover করেছে।

Overall line+branch: $60.3 - 45.2 = 15.1$ pp (gpt4o), $60.3 - 48.7 = 11.6$ pp (codex)। Ablated-এর তুলনায়: $60.3 - 34.0 = 26.3$ pp; per-module median branch-এ সবচেয়ে বড় লাফ $66.7 - 7.3 = 59.4$ pp।

### ৬.৭ Overall বনাম Per-module Median — কেন এত পার্থক্য?
Module $i = 1, \ldots, m$, প্রতিটার item সংখ্যা $n_i = N_{L,i} + N_{B,i}$, covered $c_i$:
$$
\text{Overall} = \frac{\sum_{i=1}^{m} c_i}{\sum_{i=1}^{m} n_i} \times 100 = \sum_{i=1}^{m} w_i \cdot \text{Cov}_i, \quad w_i = \frac{n_i}{\sum_j n_j}
$$
$$
\text{Median} = \text{median}\left(\text{Cov}_1, \ldots, \text{Cov}_m\right)
$$
**মানে:** Overall হলো **আকার-ভারযুক্ত গড়** — বড় module বেশি প্রভাব ফেলে। Median-এ প্রতিটা module সমান।
CoverUp-এ Overall line+branch 60.3% কিন্তু median 79.6%। **আমার পর্যবেক্ষণ:** এর মানে কিছু **বড়** module-এ coverage অনেক কম (যেমন paper বলেছে `youtube_dl`-এ timeout সবচেয়ে বড় ব্যর্থতার উৎস), যারা overall-কে টেনে নামায়, অথচ অর্ধেকের বেশি module-এ coverage প্রায় 80% বা তার বেশি। Paper per-module distribution-এর পুরো data table আকারে দেয়নি (Figure 13-এ bar হিসেবে আছে)।


**সহজ কথায়:** Overall বড় module-এর দিকে ঝোঁকে। Median প্রতিটা module-কে সমান ধরে। তাই কিছু বড় module খারাপ হলে overall কমে, কিন্তু median ঠিক থাকে।

CM suite-এর গড় module size (**আমার হিসাব**): $100{,}000 / 425 \approx 235$ line/module। PY: $5{,}000 / 84 \approx 60$। MT: $2{,}000 / 163 \approx 12$ line/function — MT যে অনেক সহজ, এটাও তার একটা ইঙ্গিত।

### ৬.৮ Paired Permutation Test (Statistical Significance)
প্রতিটা module $i$-এ পার্থক্য $d_i = \text{Cov}_i(\text{CoverUp}) - \text{Cov}_i(\text{CodaMosa})$। Test statistic, যেমন $\bar{d} = \frac{1}{m}\sum_i d_i$। Null hypothesis-এ (দুই tool সমান) প্রতিটা $d_i$-এর চিহ্ন সমান সম্ভাবনায় $+$ বা $-$:
$$
p = \text{Pr}\left( \text{abs}\left(\frac{1}{m}\sum_{i=1}^{m} \epsilon_i d_i\right) \geq \text{abs}\left(\bar{d}\right) \right), \qquad \epsilon_i \in \{+1, -1\} \text{ সমান সম্ভাবনায়}
$$

**সহজ কথায়:** দুই tool-এর পার্থক্য কাকতালীয় কিনা এই test দিয়ে দেখা হয়। p খুব ছোট (0.00002) মানে পার্থক্যটা কাকতালীয় নয়।

Paper: per-module improvement-এর জন্য CodaMosa (GPT-4o) ও CodaMosa (Codex) দুটোর বিরুদ্ধেই $p = 2.0 \times 10^{-5}$, যা $0.05$-এর অনেক নিচে। (Paper কোন statistic বা কতগুলো permutation ব্যবহার করেছে তা বলেনি; উপরের সূত্রটা প্রচলিত রূপ।) MuTAP তুলনা ও ablation-এর জন্য কোনো significance test report করা হয়নি।

### ৬.৯ Flaky Test ধরার সম্ভাবনা (pytest-repeat)
একটা test প্রতিবার স্বাধীনভাবে $q$ সম্ভাবনায় fail করলে, $r$ বার চালালে অন্তত একবার fail দেখার সম্ভাবনা:
$$
\text{Pr}(\text{detect}) = 1 - (1 - q)^{r}
$$

**সহজ কথায়:** Test একবার চালালে flaky bug ধরা না-ও পড়তে পারে। যত বেশি বার চালানো হয়, ধরা পড়ার সম্ভাবনা তত বাড়ে।

**Worked example (আমার হিসাব, অনুমানসহ):** Figure 11-এর blood type test-এ LLM-এর list-এ "0-" ও "0+" ভুল। যদি code 8টা blood type থেকে **সমান সম্ভাবনায়** বাছাই করে (এই অনুমান paper-এর নয়), তাহলে test fail করে যখন O- বা O+ আসে: $q = 2/8 = 0.25$।
- $r = 1$: $1 - 0.75 = 0.25$
- $r = 3$: $1 - 0.75^3 \approx 0.578$
- $r = 5$: $1 - 0.75^5 \approx 0.763$

অর্থাৎ কয়েকবার চালালেও এমন flaky test প্রায় এক-চতুর্থাংশ সম্ভাবনায় ধরা না পড়ে suite-এ ঢুকে যেতে পারে। Paper $r$-এর মান দেয়নি, আর রাখা test-এর মধ্যে flaky test-এর হার মাপেনি।

### ৬.১০ খরচ (RQ4, Table 3)
Prompt token $\tau_{in}$, completion token $\tau_{out}$, প্রতি million token দাম $c_{in}, c_{out}$:
$$
\text{Cost} = \frac{\tau_{in}}{10^6} \cdot c_{in} + \frac{\tau_{out}}{10^6} \cdot c_{out}
$$

**সহজ কথায়:** খরচ = (input token × দাম) + (output token × দাম)। মানে LLM-কে যত লম্বা prompt দেবে আর যত লম্বা উত্তর পাবে, তত টাকা।

**মোট token (আমার হিসাব, Table 3 থেকে):**
- CoverUp: $58{,}081{,}908 + 7{,}257{,}400 = 65{,}339{,}308$
- CodaMosa (gpt4o): $39{,}508{,}559 + 4{,}504{,}329 = 44{,}012{,}888$
- অনুপাত $65{,}339{,}308 / 44{,}012{,}888 \approx 1.485$ → **48% বেশি token** ✓ (paper-এর দাবির সাথে মেলে)

**সময়:** $71.0 / 4.0 = 17.75 \approx 18$ গুণ দ্রুত ✓। CodaMosa-র সময়ের check (**আমার হিসাব**): $425 \text{ module} \times 10 \text{ min} = 4{,}250$ min $\approx 70.8$ ঘন্টা — Table 3-এর 71.0-এর সাথে মেলে।

**দাম check (আমার হিসাব, বাইরের অনুমান):** paper GPT-4o-র দাম লেখেনি; কিন্তু input-এ 5 USD ও output-এ 15 USD per million ধরলে CoverUp $58.08 \times 5 + 7.26 \times 15 \approx 399.3$, ablated $\approx 75.4$, CodaMosa $\approx 265.1$ USD — Table 3-এর 399, 75, 265-এর সাথে প্রায় হুবহু মেলে। তাই Table 3-এর cost সম্ভবত এই দামে হিসাব করা।

**প্রতি unit খরচ (আমার হিসাব):**
| মাপ | CoverUp | CoverUp (ablated) | CodaMosa (gpt4o) |
|---|---|---|---|
| Prompt token / prompt | ≈ 2,024 | ≈ 380 | ≈ 1,301 |
| Completion token / completion | ≈ 253 | ≈ 420 | ≈ 155 |
| Cost / module (425 module) | ≈ 0.94 USD | ≈ 0.18 USD | ≈ 0.62 USD |
| Prompt / module | ≈ 67.5 | ≈ 21.7 | ≈ 71.5 |

CoverUp-এর prompt ablated-এর ~5.3 গুণ লম্বা, কারণ continued chat-এ পুরো history আর `get_info`-এর ফল যায়।

**Marginal cost per coverage point (আমার হিসাব):** CoverUp বনাম ablated: $(399 - 75) / 26.3 \approx 12.3$ USD প্রতি overall line+branch pp; CoverUp বনাম CodaMosa (gpt4o): $(399 - 265)/15.1 \approx 8.9$ USD প্রতি pp।

### ৬.১১ Ablation-এ Component-এর অবদান (RQ5)
Variant $v$-এর জন্য: $\text{Loss}_v = \text{Cov}(\text{CoverUp}) - \text{Cov}(v)$। Paper-এর ভাষ্য (Figure 17): error fixing বাদ দিলে "between 14% and 37%" কম; code context বাদ দিলে "between 7% and 16%"; coverage তথ্য বাদ দিলে "up to 2%"। **অস্পষ্টতা:** এগুলো percentage point নাকি relative % — paper স্পষ্ট করেনি, আর Figure 17-এর bar-এর সঠিক মান text-এ নেই।

**সহজ কথায়:** Ablation মানে এক এক করে অংশ সরিয়ে দেখা কোনটা না থাকলে সবচেয়ে বেশি ক্ষতি। Error fixing সরালে ক্ষতি সবচেয়ে বেশি।

**Function bloat (আমার হিসাব):** coverage-ablated prompt 11,222টা test function বানিয়েছে, CoverUp 7,366টা: $11{,}222 / 7{,}366 \approx 1.52$ → **~52% বেশি** function প্রায় একই coverage-এর জন্য।

### ৬.১২ Mutation Score — Paper মাপেনি, কিন্তু আমাদের lens-এর জন্য জরুরি
Mutant set $\mathcal{M}$, equivalent mutant (যা আচরণ বদলায় না) $\mathcal{M}_{eq}$:
$$
\text{MS}(T) = \frac{N_{\text{killed}}}{N_{\mathcal{M}} - N_{\mathcal{M}_{eq}}} \times 100
$$

**সহজ কথায়:** Mutation score = কত % নকল ভুল test ধরতে পেরেছে। Mutation testing coverage-এর চেয়ে কঠিন, কারণ এখানে test-কে সত্যিকারের ভুল ধরতে হয়।

একটা test mutant-কে kill করতে তিনটা শর্ত লাগে (RIP model — Reachability, Infection, Propagation):
$$
\text{kill}(t, m) = \text{Reach}(t, m) \land \text{Infect}(t, m) \land \text{Propagate}(t, m) \land \text{Assert-detects}(t, m)
$$
**Coverage শুধু প্রথম শর্ত ($\text{Reach}$) মাপে।** তাই:
$$
\text{Cov}(T) = 100 \text{ হলেও } \text{MS}(T) \text{ বেশি হবে এমন কোনো নিশ্চয়তা নেই}
$$ উদাহরণ: `assert True`-ধরনের বা assertion-ছাড়া test সব line চালাতে পারে, কিন্তু কোনো mutant kill করবে না। **এই gap-টাই এই analysis-এর মূল critique।**

**সহজ কথায়:** ভুল ধরতে চারটা ধাপ পার হতে হয়: ভুল জায়গায় পৌঁছানো, ভুল মান বানানো, সেই মান বাইরে আসা, আর assertion সেটা ধরা। Coverage শুধু প্রথম ধাপ দেখে।

---

## ৭. Experimental Setup

### ৭.১ Benchmark (Section 4.1)
| Suite | উৎস | আকার | কেন |
|---|---|---|---|
| **CM** | CodaMosa-র authors-এর সংগ্রহ (BugsInPy ও Pynguin-এর evaluation-এর 35টা open-source project থেকে); যেসব module-এ Pynguin কম coverage পায় | 100,000 line, 425 Python module | কঠিন code; মূল তুলনা |
| **PY** | CodaMosa থেকে বাদ পড়া module, যেখানে Pynguin আগেই ভালো | 5,000 line, 84 module | "সহজ" code-এও CoverUp ভালো কিনা |
| **MT** | HumanEval থেকে নেওয়া function (MuTAP-এর evaluation) | 2,000 line, 163 function | MuTAP-এর সাথে তুলনা (MuTAP যেকোনো package-এ চলে না) |

CM থেকে বাদ: `mimesis` (random data generator — non-flaky test বানানো কঠিন; CodaMosa-র test-এ assertion নেই বলে fail করতো না), `sanic` ও `thef∗ck` (প্রয়োজনীয় module আর পাওয়া যায় না বা CoverUp-এর সাথে conflict)।

**সহজ কথায়:** CM হলো কঠিন code-এর সংগ্রহ (মূল তুলনা), PY সহজ code, আর MT ছোট function-এর সংগ্রহ (MuTAP-এর সাথে তুলনার জন্য)।

### ৭.২ Baseline
| Baseline | LLM | বিবরণ |
|---|---|---|
| CodaMosa (codex) | Codex | Codex আর নেই, তাই CodaMosa-র মূল evaluation-এর test; সেরা configuration "0.8-uninterp" (নামের অর্থ এই paper ব্যাখ্যা করেনি) |
| CodaMosa (gpt4o) | GPT-4o | Authors-এর adapted version — chat API, code completion-এর অনুরোধ prompt-এর আগে যোগ |
| MuTAP (codex few-shot) | Codex | মূল evaluation-এর test; prompt-এ 2টা উদাহরণ |
| MuTAP (codex zero-shot) | Codex | মূল test; উদাহরণ ছাড়া |
| MuTAP (gpt4o few-shot) | GPT-4o | Adapted; নতুন test |
| MuTAP (gpt4o zero-shot) | GPT-4o | Adapted; নতুন test |
| CoverUp (ablated) — RQ2 | GPT-4o | প্রায় একই prompt, কিন্তু coverage তথ্য নেই, line tag নেই, generated import নেই, `get_info` নেই, continued chat নেই; চায় "tests that execute all lines and branches" |

SymPrompt তুলনা করা যায়নি — public নয়।

**সহজ কথায়:** তুলনা ন্যায্য রাখতে authors CodaMosa আর MuTAP-কে GPT-4o দিয়েও চালিয়েছেন। আর নিজের tool-এর সরল রূপ (ablated) দিয়ে দেখেছেন লাভটা কোথা থেকে আসে।

### ৭.৩ RQ5-এর Ablation (Table 4)
Table 4-এ পাঁচটা element: (১) কোন coverage missing তার উল্লেখ, (২) coverage না বাড়লে continued chat, (৩) generated import, (৪) `get_info`, (৫) error হলে continued chat। Variant: **no coverage**, **no code context**, **no error fixing**, আর সবগুলো ছাড়া **ablated [RQ2]**।
> **নোট:** Table 4-এর check mark-গুলো PDF-এ graphic, text হিসেবে বের করা যায়নি। Section 4.6-এর "তিনটা function — coverage তথ্য, code context, error feedback" বর্ণনা থেকে আমার ধারণা: no coverage = (১)+(২) বাদ; no code context = (৩)+(৪) বাদ; no error fixing = (৫) বাদ। Supervisor-কে দেখানোর আগে PDF-এর Table 4 চোখে দেখে নিশ্চিত হতে হবে।

### ৭.৪ Metric
- Line, branch, line+branch coverage — **overall** (পুরো suite) ও **per-module median**।
- সব generated test isolation-এ চালিয়ে, SlipCover দিয়ে মাপা।
- **যা মাপা হয়নি:** mutation score, assertion count/quality, bug detection, flaky rate, test readability/maintainability।

### ৭.৫ Environment ও Configuration
| বিষয় | মান |
|---|---|
| Docker image | `codamosa-docker` (Microsoft), শুধু SlipCover install আর default entrypoint বন্ধ করা |
| OS / Python | Debian 11, Python 3.10.2 (MuTAP-এর জন্য Python 3.9.12, কারণ MutPy পুরনো Python চায়) |
| Host | Linux kernel 5.6, 10টা Intel i9 core @ 3.7GHz, 64GB RAM |
| Dependency | CodaMosa-র `package.txt` pip দিয়ে install; কিছু install fail করে — CodaMosa-র মূল evaluation-এর মতো উপেক্ষা করা |
| LLM | `gpt-4o-2024-05-13`, temperature 0, output token-এর কোনো সীমা নেই |
| Segment size | 50 line (default) |
| Flaky check | চালু (repeat সংখ্যা বলা নেই) |
| Continuation | সর্বোচ্চ 2টা অতিরিক্ত prompt |
| Test timeout | 1 মিনিট (paper নিজেই বলেছে সম্ভবত কম ছিল) |
| Run | প্রথমে কোনো test suite ছাড়া (CodaMosa-র সমান অবস্থা), তারপর **আরও দুইবার** — প্রতিবার আগের suite-এর উপর |
| Missing module | স্বয়ংক্রিয়ভাবে install |
| CodaMosa | প্রতি module 10 মিনিট (মূল paper-এর setting) |

**সহজ কথায়:** পুরো পরীক্ষা Docker-এর ভেতরে একই setting-এ চালানো হয়েছে, যাতে সব tool সমান অবস্থায় থাকে।

---

## ৮. Results — মূল ফলাফল

### ৮.১ RQ1 — CM Suite-এ CodaMosa-র সাথে তুলনা (Table 1, Figure 12)
| Test Generator | Overall Line | Overall Branch | Overall L+B | Median Line | Median Branch | Median L+B |
|---|---|---|---|---|---|---|
| **CoverUp** | **63.8%** | **49.2%** | **60.3%** | **82.4%** | **66.7%** | **79.6%** |
| CodaMosa (codex) | 53.5% | 33.6% | 48.7% | 62.9% | 35.6% | 55.1% |
| CodaMosa (gpt4o) | 50.6% | 28.6% | 45.2% | 54.2% | 19.0% | 47.2% |
| CoverUp (ablated) | 38.8% | 19.0% | 34.0% | 43.8% | 7.3% | 38.5% |
| CoverUp on PY suite | 97.0% | 99.2% | 97.1% | 100.0% | 100.0% | 100.0% |

- সব metric-এ CoverUp দুই CodaMosa-র চেয়ে বেশি।
- Per-module improvement statistically significant: paired permutation test, $p = 2.0 \times 10^{-5}$ (দুটো baseline-এর বিরুদ্ধেই)।
- **নতুন model মানেই ভালো নয়:** CodaMosa (gpt4o) CodaMosa (codex)-এর চেয়ে সামান্য খারাপ (overall মাপ 5%-এর মধ্যে)। কিন্তু per-module median branch-এ পার্থক্য বড়: 35.6% বনাম 19.0%।
- Abstract-এর headline "80% vs. 47%" = CoverUp বনাম CodaMosa (gpt4o)-এর median L+B; "60% vs. 45%" = overall L+B।

**সহজ কথায়:** সব সংখ্যায় CoverUp এগিয়ে। বিশেষ করে median branch coverage-এ 66.7% বনাম 19.0%। মানে CodaMosa (gpt4o) মাঝের module-এ ১০০টা branch-এর মধ্যে মাত্র প্রায় ১৯টা ধরেছে।

### ৮.২ RQ1 — Module-ভিত্তিক পার্থক্য ও ব্যর্থতার কারণ (Figure 13)
Figure 13 প্রতিটা module-এ CoverUp − CodaMosa (L+B) দেখায়; বেশিরভাগ module সবুজ (CoverUp ভালো), কিন্তু কিছু module-এ CoverUp খারাপ। Paper-এর log বিশ্লেষণ:
1. **`youtube_dl`-এর module-এ test timeout** — সবচেয়ে বড় একক ব্যর্থতার উৎস; 1 মিনিট timeout সম্ভবত কম ছিল (CodaMosa-র authors-ও এই package-এ timeout-এর কথা বলেছিলেন)।
2. **Conditional import** (Python version অনুযায়ী ভিন্ন import) থাকলে CoverUp-এর static analysis সঠিক context দিতে পারে না।
3. **এক উত্তরের সব test reject** একটা fail করলে — আলাদা আলাদা যাচাই করলে coverage হয়তো বেশি হতো।

### ৮.৩ RQ1 — PY Suite (Figure 14)
CoverUp: overall line 97.0%, branch 99.2%, L+B 97.1%; median তিনটাই 100.0%। অর্থাৎ যেখানে Pynguin আগেই ভালো, সেখানেও CoverUp প্রায় পূর্ণ coverage পায়। (PY-তে CodaMosa বা Pynguin-এর সংখ্যা এই paper-এ দেওয়া হয়নি।)

### ৮.৪ RQ1 — MT Suite-এ MuTAP-এর সাথে তুলনা (Table 2, Figure 15)
| Test Generator | Overall Line | Overall Branch | Overall L+B | Median Line | Median Branch | Median L+B |
|---|---|---|---|---|---|---|
| **CoverUp** | **89.2%** | **88.7%** | **89.0%** | 100.0% | 100.0% | 100.0% |
| MuTAP (codex few-shot) | 80.8% | 71.7% | 77.7% | 100.0% | 100.0% | 100.0% |
| MuTAP (codex zero-shot) | 79.2% | 72.7% | 77.0% | 100.0% | 100.0% | 100.0% |
| MuTAP (gpt4o zero-shot) | 78.0% | 74.5% | 76.8% | 100.0% | 100.0% | 100.0% |
| MuTAP (gpt4o few-shot) | 15.9% | 0.0% | 10.4% | 16.7% | 0.0% | 11.1% |

- Overall-এ CoverUp সব metric-এ বেশি; median-এ সমান (100%), শুধু MuTAP (gpt4o few-shot) বাদে।
- **MuTAP (gpt4o few-shot)-এর ধস:** few-shot prompt-এর উদাহরণ GPT-4o-কে বিভ্রান্ত করে — function under test-এর বদলে **উদাহরণের function-এর জন্য test** লেখে; test চললেও coverage-এ অবদান নেই। **আমার পর্যবেক্ষণ:** এটা prompt sensitivity-র একটা শক্ত উদাহরণ — একই LLM, শুধু prompt format বদলে 76.8% থেকে 10.4%।
- MT suite সহজ: function self-contained, কদাচিৎ শুধু standard library ব্যবহার, প্রায়ই type annotation আছে। CM-এর code-এ dependency বেশি, external code, annotation নেই।
- **একটা ছোট অসঙ্গতি:** text বলছে overall branch "89% (vs. 73% to 0%)", কিন্তু Table 2-এ baseline-দের সর্বোচ্চ branch 74.5% (MuTAP gpt4o zero-shot)। Table-এর মানই এখানে নেওয়া হয়েছে।

**সহজ কথায়:** ছোট function-এ CoverUp প্রায় সবকিছু ধরেছে। MuTAP (gpt4o few-shot) প্রায় কিছুই ধরেনি, কারণ উদাহরণ দেখে LLM ভুল function-এর test লিখেছে।

### ৮.৫ RQ2 — শুধু LLM বনাম CoverUp (Table 1, Figure 16)
| Metric | CoverUp | CoverUp (ablated) | পার্থক্য (pp, আমার হিসাব) |
|---|---|---|---|
| Overall line | 63.8% | 38.8% | 25.0 |
| Overall branch | 49.2% | 19.0% | 30.2 |
| Overall L+B | 60.3% | 34.0% | 26.3 |
| Median line | 82.4% | 43.8% | 38.6 |
| Median branch | 66.7% | 7.3% | 59.4 |
| Median L+B | 79.6% | 38.5% | 41.1 |

**মূল বার্তা:** CoverUp-এর লাভ শুধু GPT-4o-র কারণে নয়; design (coverage তথ্য, context, feedback) বড় অবদান রাখে। Ablated version CodaMosa-র চেয়েও খারাপ (overall L+B 34.0% বনাম 45.2%)।

**সহজ কথায়:** একই LLM, শুধু CoverUp-এর design যোগ করলে coverage প্রায় ২৬ percentage point বাড়ে। মানে design-ই আসল শক্তি।

### ৮.৬ RQ3 — Continued Dialogue
CM suite-এর log: সফল test-এর **60.3%** প্রথম prompt-এ, **27.2%** দ্বিতীয়তে, **12.5%** তৃতীয়তে → প্রায় **40%** সাফল্য iteration থেকে।

**সহজ কথায়:** প্রথমবারেই বেশিরভাগ test আসে। কিন্তু শেষ ৪০% আসে আবার চেষ্টা করে, তাই chat চালিয়ে যাওয়া দরকারি।

### ৮.৭ RQ4 — খরচ (Table 3)
| Test Generator | Prompts | P. Tokens | Completions | C. Tokens | Time (h) | Cost (USD) |
|---|---|---|---|---|---|---|
| CoverUp | 28,690 | 58,081,908 | 28,654 | 7,257,400 | 4.0 | 399 |
| CoverUp (ablated) | 9,224 | 3,501,827 | 9,188 | 3,859,444 | 1.7 | 75 |
| CodaMosa (gpt4o) | 30,368 | 39,508,559 | 29,136 | 4,504,329 | 71.0 | 265 |

- CoverUp ~**18 গুণ দ্রুত** (4 বনাম 71 ঘন্টা), কিন্তু **48% বেশি token**।
- **আমার হিসাব:** টাকায় CoverUp CodaMosa-র চেয়ে $399/265 \approx 1.51$ গুণ — অর্থাৎ ~51% বেশি খরচ। Paper "18x faster"-কে headline করেছে, কিন্তু টাকার হিসাবে CoverUp বেশি দামি।

**সহজ কথায়:** CoverUp সময়ে অনেক দ্রুত (৪ ঘন্টা বনাম ৭১ ঘন্টা), কিন্তু টাকায় প্রায় দেড় গুণ বেশি। দ্রুত হওয়া আর সস্তা হওয়া এক কথা নয়।
- **সময়ের তুলনার সীমা (paper নিজেই বলেছে):** CoverUp parallel ও async, OpenAI-এর rate limit ও response time-এ আটকে থাকে; CodaMosa sequential, module প্রতি 10 মিনিট (configurable)। OpenAI-এর compute অজানা ও সময়ের সাথে বদলায়। তাই "18x" একটা deployment-নির্ভর সংখ্যা, algorithm-এর মৌলিক গুণ নয়।

### ৮.৮ RQ5 — Component Ablation (Table 4, Figure 17, Figure 18)
**Figure 17 (CM suite):** সব ablation coverage কমায়।
- Error fixing বাদ: সবচেয়ে বড় ক্ষতি — বিভিন্ন metric-এ 14% থেকে 37%।
- Code context বাদ: 7% থেকে 16%।
- Coverage তথ্য বাদ: সর্বোচ্চ 2%।
- Component-গুলো স্বাধীন নয়: error feedback অপর্যাপ্ত context-এর ঘাটতি পূরণ করতে পারে; ভালো context ভুল ধারণা থেকে আসা error কমায়।

**Figure 18 — Successive run-এ coverage-improving function-এর হার:**
| Run | CoverUp | CoverUp (no coverage) |
|---|---|---|
| 1st | 62.2% | 51.4% |
| 2nd | 66.5% | 28.6% |
| 3rd | 66.6% | 12.2% |

(Figure-এর label ক্রম থেকে পড়া; কোন সংখ্যা কোন bar তা figure-এর বর্ণনা — "coverage-ablated prompt generates fewer and fewer" — দিয়ে মিলিয়ে নেওয়া।)

- **ব্যাখ্যা:** Suite-এর coverage যত বাড়ে, coverage তথ্য ছাড়া prompt তত বেশি "ইতিমধ্যে covered" জায়গার test লেখে। CoverUp-এর prompt কার্যকর থাকে কারণ বলে দেয় ঠিক কোথায় gap।
- **Bloat:** coverage-ablated prompt overall coverage-এ সামান্য পিছিয়ে থাকলেও 11,222টা function বানিয়েছে (CoverUp 7,366) — 50%-এর বেশি। Suite-এ রাখলে suite ধীর হয়; ফেলে দিলেও token-এর খরচ।
- **আমার পর্যবেক্ষণ:** Figure 17-এ coverage তথ্যের অবদান মাত্র ~2% দেখালেও Figure 18 দেখায় এর আসল মূল্য **efficiency ও পরের run-এ** — একবারের coverage সংখ্যা দিয়ে component-এর মূল্য বিচার করলে ভুল হতে পারে।

**সহজ কথায়:** Coverage তথ্য প্রথম run-এ কম কাজে লাগে। কিন্তু পরের run-এ যখন অনেক line আগেই covered, তখন সেটা LLM-কে বাকি জায়গা দেখিয়ে দেয়, আর এটাই আসল লাভ।

### ৮.৯ SymPrompt-এর সাথে মোটা দাগে তুলনা (Section 2)
- SymPrompt: GPT-4 দিয়ে 897টা function-এর (অপ্রকাশিত subset, অন্তত 4,546টা থেকে) উপর 74% line coverage; নিজের baseline prompt-এর প্রায় 2 গুণ।
- CoverUp: GPT-4o দিয়ে CodaMosa থেকে নেওয়া 4,116-function suite-এ median per-module line 82%, overall line 64%; ablated version-এর প্রায় 2 গুণ (**আমার হিসাব:** $82.4/43.8 \approx 1.88$)।
- Function list না পাওয়ায় সরাসরি তুলনা সম্ভব হয়নি — authors নিজেরাই "coarse comparison" বলেছেন।

**সহজ কথায়:** SymPrompt-এর সাথে সরাসরি তুলনা সম্ভব হয়নি। তাই এটা শুধু মোটামুটি আন্দাজ।

---

## ৯. Key Findings / Insights (Supervisor-কে বলার মতো ৮টা পয়েন্ট)

1. **Coverage তথ্য prompt-এ দিলে LLM-এর মনোযোগ gap-এ যায়** — CM-এ median L+B 79.6% বনাম CodaMosa (gpt4o) 47.2%।
2. **Scaffold (design) LLM-এর চেয়ে কম গুরুত্বপূর্ণ নয়** — একই GPT-4o, শুধু prompt-এ চাইলে overall L+B 34.0%, CoverUp-এ 60.3%।
3. **Error feedback সবচেয়ে মূল্যবান component** — বাদ দিলে 14–37% ক্ষতি; সফল test-এর ~40% আসে continued chat থেকে।
4. **Coverage feedback-এর মূল্য পরের run-এ দেখা যায়** — coverage-ablated prompt-এর সফল function হার 51.4% → 28.6% → 12.2%, CoverUp-এর 62.2% → 66.5% → 66.6%।
5. **Tool calling দিয়ে context নিজে খুঁজতে দেওয়া কাজ করে** — static context + `get_info` বাদ দিলে 7–16% ক্ষতি।
6. **নতুন LLM মানেই ভালো ফল নয়** — CodaMosa (gpt4o) < CodaMosa (codex); MuTAP-এর few-shot prompt GPT-4o-তে 10.4%-এ নেমে যায়। Prompt/scaffold-কে model-এর সাথে মানিয়ে নিতে হয়।
7. **LLM-generated test-এর practical সমস্যা আসল** — state pollution (global মুছে ফেলা), flaky test (O বনাম 0), top-level `pytest.main`; isolation ও repeat ছাড়া suite অচল হতে পারে।
8. **দ্রুত কিন্তু সস্তা নয়** — 18 গুণ দ্রুত, কিন্তু 48% বেশি token ও ~51% বেশি টাকা (399 বনাম 265 USD)।

**আমাদের assurance lens থেকে যোগ (আমার পর্যবেক্ষণ):**
9. **High coverage ≠ শক্ত oracle** — paper একবারও mutation score বা assertion-এর মান মাপেনি; acceptance শর্ত শুধু pass + coverage।
10. **Error feedback = "test-কে code-এর সাথে মানিয়ে নাও"** — Figure 7-এ assertion fail করলে CoverUp LLM-কে test "correct" করতে বলে। Code ভুল হলে LLM সম্ভবত assertion বদলে code-এর ভুল আচরণকেই লিখে রাখবে। Regression test-এর জন্য ঠিক, কিন্তু patch যাচাইয়ের জন্য বিপজ্জনক।

**সহজ কথায়:** CoverUp-এর কিছু লাভ আসলে ঝুঁকিও। Test ভুল হলে LLM test-কে code-এর সাথে মেলাতে পারে, code ভুল হলেও।

---

## ১০. কেন এই Solution অন্যগুলোর থেকে ভালো?

| বৈশিষ্ট্য | Pynguin (SBST) | CodaMosa | MuTAP | TestPilot / ChatUniTest / TestGen-LLM | **CoverUp** |
|---|---|---|---|---|---|
| মূল চালক | Genetic search | Search + LLM (আটকে গেলে) | LLM + mutation | LLM | **LLM, coverage দিয়ে চালিত** |
| Prompt-এ কোন line বাকি তা বলে | — | না | না | না | **হ্যাঁ (line number tag)** |
| Coverage না বাড়লে LLM-কে আবার বলে | — | না | না | না (TestGen-LLM ফেলে দেয়) | **হ্যাঁ** |
| Error হলে chat চালায় | — | না | শুধু syntax error | হ্যাঁ (TestPilot, ChatUniTest আংশিক) | **হ্যাঁ, সব error** |
| LLM নিজে context চাইতে পারে (tool) | — | না | না | না | **হ্যাঁ (`get_info`)** |
| State pollution handling | — | — | — | — | **হ্যাঁ (fork isolation, ৩টা বিকল্প)** |
| Flaky detection | — | — | — | — | **হ্যাঁ (pytest-repeat)** |
| যেকোনো Python package-এ চলে | হ্যাঁ | হ্যাঁ | না (dataset hardcoded) | ভিন্ন language | **হ্যাঁ** |
| Oracle-এর শক্তি নিয়ে সরাসরি কাজ | না | না | **হ্যাঁ (mutant দিয়ে assertion)** | না | **না** |

**মূল শক্তি:**
1. **সরল ও general idea:** coverage measurement + LLM + feedback — যেকোনো language-এ নেওয়া যায় (paper শুধু Python-এ দেখিয়েছে)।
2. **Ablation দিয়ে দাবি প্রমাণ:** লাভ কোথা থেকে আসছে, component ধরে দেখানো।
3. **Practical engineering:** isolation, flaky, async, rate limit, checkpoint — বাস্তব package-এ চলে।
4. **Open-source ও replication package:** পুনরায় চালানো যায়।
5. **Statistical test:** per-module improvement-এ permutation test।

**দুর্বল দিক তুলনায়:** oracle-এর দিক থেকে MuTAP-এর approach (survived mutant-এর জন্য assertion) বেশি সরাসরি — CoverUp-এর তুলনা শুধু coverage-এ হওয়ায় MuTAP-এর এই শক্তি দেখা যায়নি।

**সহজ কথায়:** CoverUp coverage-এ সেরা, কিন্তু oracle-এর শক্তিতে MuTAP-এর idea বেশি সরাসরি। এই দুই শক্তি এখনো এক জায়গায় আসেনি।

---

## ১১. কোন পরিস্থিতিতে এই Paper/Tool ভালো কাজ করে, কোথায় করে না

### ✅ ভালো কাজ করে যখন:
- **বিদ্যমান, সঠিক বলে ধরে নেওয়া Python code-এর regression test** বানাতে হবে।
- Code-এ অনেক dependency, annotation নেই — যেখানে SBST আটকে যায় (CM suite-এর মতো)।
- Coverage বাড়ানো লক্ষ্য (যেমন CI-তে coverage threshold)।
- বারবার চালিয়ে ধাপে ধাপে coverage বাড়াতে হবে (incremental run)।
- Unix system (fork-ভিত্তিক isolation)।

### ❌ ভালো কাজ করে না / সীমিত যখন:
- **Code-এ bug আছে কিনা জানতে চাই** — regression test bug-কেই লিখে রাখতে পারে।
- **Patch সঠিক কিনা যাচাই** — patch করা code-এ চালালে patch-এর আচরণই oracle হয়ে যায় (differential ব্যবহার না করলে)।
- **Randomness-নির্ভর code** (`mimesis`-এর মতো) — flaky test।
- **লম্বা সময় লাগে এমন test** (`youtube_dl`) — 1 মিনিট timeout।
- **Conditional import** — static analysis ভুল context দেয়।
- **Network, file system, database-নির্ভর code** — paper এ বিষয়ে আলাদা মাপ দেয়নি; prompt শুধু mock ব্যবহারে উৎসাহ দেয়।
- **অন্য language** — শুধু Python।
- **Windows** — `fork()`-ভিত্তিক isolation Unix-এর (paper Windows-এর কথা বলেনি; আমার পর্যবেক্ষণ)।
- **কম বাজেট** — CM-এর জন্য 399 USD (GPT-4o)।

**সহজ কথায়:** CoverUp তখন ভালো যখন code ঠিক ধরে নিয়ে regression test চাই। Bug খোঁজা বা patch যাচাইয়ের কাজে এটা এমনিই যথেষ্ট নয়।

---

## ১২. Limitations — দুর্বলতা

### ১২.১ Authors যা নিজেরা স্বীকার করেছেন
1. **Benchmark selection:** CM, PY, MT বাছাই করা হয়েছে CodaMosa/MuTAP ও Codex-এর ফলের সাথে তুলনার সুবিধার জন্য; অন্য benchmark-এ ফল ভিন্ন হতে পারে।
2. **Execution environment:** CodaMosa-র মূল environment-এ কিছু dependency install হয় না; সেটা উপেক্ষা করা হয়েছে — দুই tool-ই dependency থাকলে ভালো করতো।
3. **LLM model dependency:** GPT-4, GPT-4 Turbo, GPT-4o দিয়েই develop ও evaluate করা; চূড়ান্ত performance model-এর prompt বোঝার ক্ষমতার উপর নির্ভর করে।
4. **Timeout:** 1 মিনিট সম্ভবত কম ছিল (`youtube_dl`)।
5. **Conditional import-এ static analysis ব্যর্থ।**
6. **এক উত্তরের সব test একসাথে reject** — আলাদা যাচাই করলে ভালো হতে পারতো।
7. **সময় তুলনার সীমা:** OpenAI-এর compute অজানা; CodaMosa-র 10 মিনিট configurable।
8. **Prompt নির্দেশ সত্ত্বেও side effect-ওয়ালা test আসে** — তাই isolation দরকার।

### ১২.২ আমার Critical Analysis (Professor-level observation)
1. **Oracle-এর শক্তি একেবারেই মাপা হয়নি (সবচেয়ে গুরুত্বপূর্ণ):** একমাত্র metric coverage। Mutation score, assertion সংখ্যা, assertion-ছাড়া test-এর হার, বা আসল bug ধরার ক্ষমতা (যেমন BugsInPy-এর bug — CM suite তো BugsInPy-র project থেকেই এসেছে!) — কিছুই নেই। Prompt-এ "include assertions" বলা হলেও acceptance-এ যাচাই হয় না। তাই "CoverUp-এর test ভালো" দাবিটা আসলে "CoverUp-এর test বেশি code চালায়"।
2. **MuTAP-এর সাথে অসম তুলনা:** MuTAP-এর মূল লক্ষ্য mutation-ভিত্তিক শক্ত assertion; তাকে শুধু coverage-এ বিচার করা হয়েছে — যে metric-এ MuTAP-এর design-গত সুবিধা দেখাই যায় না।
3. **Error feedback-এর অন্ধকার দিক — "test-কে code-এ fit করানো":** Figure 7-এ `assert 13 == 11` fail করলে CoverUp বলে "Modify the test to correct it"। LLM-এর expectation যদি আসলে ঠিক হয় আর code-এ bug থাকে, তাহলে এই loop bug-টাকে test-এ "সঠিক" হিসেবে লিখে ফেলবে। Regression setting-এ এটা by design, কিন্তু paper এর ঝুঁকি আলোচনা করেনি। APR sub-domain-এ VRpilot-এ দেখা **feedback overfitting**-এর (CG3) এটাই test-generation রূপ।
4. **একটাই LLM, একটাই run, temperature 0:** Variance, seed, বা অন্য model (open-weight) দিয়ে কোনো পরীক্ষা নেই। CoverUp-এর তিনটা "run" আসলে ধারাবাহিক (একটার উপর আরেকটা), পুনরাবৃত্তি নয়। Reliability (CG4) জানা যায় না।
5. **Contamination ঝুঁকি:** CM-এর project-গুলো open-source ও পুরনো (BugsInPy, Pynguin evaluation), MT HumanEval থেকে — GPT-4o-র training data-তে এগুলোর code ও হয়তো test-ও থাকতে পারে। Paper এটা আলোচনা করেনি (CG6)।
6. **Combined statistical rigor সীমিত:** permutation test শুধু CodaMosa-র সাথে per-module-এ; ablation (RQ5) ও MuTAP তুলনায় কোনো significance বা confidence interval নেই। Figure 17-এর মান শুধু range আকারে, pp নাকি relative % তা অস্পষ্ট।
7. **Baseline adaptation-এর ন্যায্যতা:** CodaMosa ও MuTAP-এর GPT-4o version authors নিজেরা বানিয়েছেন (prompt-এর আগে instruction যোগ করে)। MuTAP (gpt4o few-shot)-এর 10.4% দেখায় adaptation খুব sensitive — baseline-এর জন্য কতটা prompt tuning করা হয়েছে, CoverUp-এর তুলনায়, তা অজানা।
8. **Cost headline:** "18x faster" সামনে রাখা হয়েছে, কিন্তু টাকায় CoverUp ~51% বেশি দামি; CodaMosa-র অধিকাংশ সময় local CPU-তে search, যার টাকা Table 3-এ ধরা হয়নি। দুই দিকের পূর্ণ cost model নেই।
9. **Test quality-র অন্য দিক মাপা হয়নি:** readability, maintainability, over-mocking, test smell, suite execution time (bloat শুধু function সংখ্যায়)।
10. **Flaky rate ও pollution rate report নেই:** কতগুলো test pollution বা flakiness-এর কারণে বাদ গেছে বা রয়ে গেছে, জানা যায় না। Evaluation-এ isolation default ছিল, তাই integration-এর সমস্যা চাপা পড়েছে — বাস্তবে suite একসাথে চালালে কী হতো, তা অজানা।
11. **Test isolation evaluation-কে সহজ করে দেয়:** সব test isolation-এ চালিয়ে coverage মাপা হয়েছে। ব্যবহারকারী isolation ছাড়া (সাধারণ `pytest`) চালালে ফল ভিন্ন হতে পারে — coverage সংখ্যা এই setting-নির্ভর।
12. **Missing module auto-install-এর নিরাপত্তা ঝুঁকি:** LLM যে module-এর নাম লেখে তা স্বয়ংক্রিয়ভাবে install করা — LLM ভুল বা অস্তিত্বহীন package নাম লিখলে (package hallucination) supply-chain ঝুঁকি। Paper এটা আলোচনা করেনি (CG5-এর সাথে যুক্ত)।

**সহজ কথায়:** দুর্বলতা দুই ভাগে: authors যা নিজে বলেছেন (সৎ স্বীকারোক্তি), আর আমরা যা দেখছি। সবচেয়ে বড়টা: কোনো oracle মাপা হয়নি।

---

## ১৩. Research Gaps — কোথায় কাজ করার সুযোগ আছে

| # | Gap | কেন গুরুত্বপূর্ণ | Common gap | কে কিছুটা কাজ করেছে (আমাদের folder-এ) |
|---|---|---|---|---|
| G1 | **Coverage-এর বাইরে oracle-এর শক্তি মাপা** (mutation score, assertion quality) | Dynamic signal দুর্বল হলে ভুল patch-ও pass করে | CG3, CG1 | LLM Test Generation (MuTAP-ধারা; এই folder-এর অন্য paper পড়ে দেখতে হবে); Patch Validation |
| G2 | **Regression oracle-কে patch যাচাইয়ে ব্যবহার — differential testing** (পুরনো বনাম patch করা code-এ একই test) | Patch করা code-এ test বানালে patch-ই oracle হয়ে যায় | CG1, CG3 | Patch Validation; Coding-Agent Evaluation & Reliability (PatchDiff fact sheet-এ) |
| G3 | **Diff-targeted coverage** — শুধু patch-এ বদলানো line/branch-কে "gap" ধরে segment prompting | Agent patch যাচাইয়ে পুরো module নয়, পরিবর্তিত অংশই মুখ্য | CG3, CG1 | AI Coding Agents (Agentless-এর reproduction test, 213 থেকে 94) |
| G4 | **Feedback loop-এ "test-কে code-এ fit করানো" (feedback overfitting)** — assertion বদলের হার ও তার ঝুঁকি মাপা | Bug-কে test-এ পাকা করে ফেলা | CG3, CG12 | Automated Program Repair (VRpilot-এর feedback overfitting) |
| G5 | **Run-to-run variance ও model-ভেদে stability** | একবারের temperature-0 run reliability বলে না | CG4, CG8 | Coding-Agent Evaluation & Reliability (Engineering Reliable Agents) |
| G6 | **Contamination-মুক্ত test-generation benchmark** | Open-source পুরনো project LLM-এর training-এ থাকতে পারে | CG6 | Coding-Agent Evaluation & Reliability (SWE-rebench-ধরনের নতুন repo) |
| G7 | **Cost-effectiveness frontier** — coverage/oracle per USD, ছোট বা open model দিয়ে | 399 USD/100K LOC অনেকের নাগালের বাইরে | CG8 | — (খোলা) |
| G8 | **Flaky ও polluting test-এর হার report ও কমানো** | Assurance signal নিজেই অস্থির হলে রায় অবিশ্বস্ত | CG4, CG11 | — (খোলা; paper-এর tool আছে, মাপ নেই) |
| G9 | **Security-কেন্দ্রিক test generation** (input validation, injection path-এ coverage) ও auto-install-এর supply-chain ঝুঁকি | Functional coverage security নিশ্চিত করে না | CG5 | Security of AI-Generated Code |
| G10 | **Python-এর বাইরে ও repository-level setting** | Assurance tool বহু-ভাষায় দরকার | CG9 | Coding-Agent Evaluation & Reliability (SWE-Bench Pro বহু-ভাষা) |
| G11 | **Generated test-এর quality/smell** (over-mocking, bloat, readability) | Developer-রা দুর্বল test review-এ বাদ দেয় | CG3 | Trustworthy AI for SE (human review দিক) |
| G12 | **Test generator-এর নিজের validity** — generated test কতটা নির্ভরযোগ্য judge, তার version-সহ রেকর্ড | Verifier নিজেই ভুল হলে পুরো assurance ভুল | CG10, CG11 | Coding-Agent Evaluation & Reliability (monograph-এর verifier versioning) |
| G13 | **"অনিশ্চিত" segment-এ abstention** — LLM যখন code-এর উদ্দেশ্য বোঝে না (randomness, conditional import), তখন test না লিখে জানানো | ভুল oracle লেখার চেয়ে "জানি না" ভালো | CG7 | Trustworthy AI for SE |

**সহজ কথায়:** এই table-এ প্রতিটা সারি একটা সুযোগ। G1, G2, G3, G4 আমাদের assurance layer-এর সবচেয়ে কাছের, তাই এগুলো আগে ভাবা ভালো।

---

## ১৪. কী করলে আরও ভালো হবে — Improvement Ideas

1. **Acceptance শর্তে oracle যোগ:** $\text{Accept}(U) = \text{pass} \land \Delta\text{Cov} > 0 \land \Delta\text{MS} > 0$ — অর্থাৎ নতুন test অন্তত একটা নতুন mutant kill করলে তবেই রাখা (MuTAP-এর idea CoverUp-এর loop-এ)। (আমার প্রস্তাব।)
2. **Mutation feedback prompt:** coverage follow-up-এর মতো "এই line চলে, কিন্তু `>` থেকে `>=` mutant survive করেছে — এমন assertion যোগ করো যা এটা ধরে।"
3. **Assertion বদলের audit:** error follow-up-এর পর LLM assertion-এর expected value বদলেছে কিনা log করা; বদলালে flag — "test code-এর সাথে মানিয়ে নেওয়া হয়েছে, মানুষের দেখা দরকার"।
4. **Differential mode (patch validation-এর জন্য):** test generate করা হবে **original (pre-patch) code-এ, patch-এর পরিবর্তিত অংশ target করে**; তারপর একই test patch করা code-এ চালিয়ে আচরণের পার্থক্য দেখা — যে পার্থক্য issue-এর সাথে সম্পর্কিত নয়, তা regression সন্দেহ। (PatchDiff-ধাঁচ।)
5. **Per-function acceptance:** এক উত্তরের সব test একসাথে reject না করে প্রতিটা আলাদা যাচাই (paper নিজেই ইঙ্গিত দিয়েছে)।
6. **Adaptive timeout ও conditional import-এর জন্য dynamic context** (runtime-এ module inspect)।
7. **Repeated generation:** একই segment-এ k বার generation চালিয়ে coverage ও mutation score-এর variance report।
8. **Open-weight model দিয়ে replication:** খরচ কমানো ও contamination নিয়ন্ত্রণ।
9. **Install whitelist:** auto-install শুধু known package list থেকে।

**সহজ কথায়:** মূল ধারণা: test-কে শুধু "চালানো"র বদলে "ভুল ধরা"-র দিকে ঠেলে দাও। Mutation score ও assertion audit এই কাজ করে।

---

## ১৫. কোন Gap-এ Research করলে ভালো Result ও Publication আসতে পারে

> ⚠️ LLM Test Generation sub-domain-এর প্রথম দিকের paper-এর ভিত্তিতে প্রাথমিক মত। বাকি paper ও sub-domain শেষে চূড়ান্ত বাছাই।

| Gap | SPL3-তে করা সম্ভব? | Novelty | Publication সম্ভাবনা |
|---|---|---|---|
| **G1: Coverage বনাম mutation score — CoverUp-ধরনের test-এর oracle audit** | ✅ হ্যাঁ — CM-এর ছোট subset, open-source CoverUp, mutmut-ধরনের Python mutation tool | মাঝারি-উচ্চ (coverage-only evaluation-এর সরাসরি critique) | ⭐⭐⭐⭐ |
| **G2+G3: Diff-targeted, differential test generation দিয়ে agent patch-এর overfitting ধরা** | ✅ হ্যাঁ — SWE-rebench-এর কয়েকটা task + একটা agent-এর patch | উচ্চ — আমাদের assurance layer-এর dynamic signal সরাসরি | ⭐⭐⭐⭐⭐ |
| **G4: Feedback loop-এ assertion বদলের হার ও bug "পাকা করা"** | ✅ হ্যাঁ — BugsInPy-এর buggy version-এ CoverUp চালিয়ে দেখা কত test bug-কে সঠিক ধরে | উচ্চ, কেউ সরাসরি মেপেছে বলে আমার জানা নেই (যাচাই করতে হবে) | ⭐⭐⭐⭐ |
| G5: Run-to-run variance | ✅ হ্যাঁ, কিন্তু API খরচ k গুণ | মাঝারি | ⭐⭐⭐ |
| G6: নতুন contamination-মুক্ত test-gen benchmark | ⚠️ কঠিন | মাঝারি | ⭐⭐ |

**সহজ কথায়:** G2+G3 সবচেয়ে ভালো বাজি: আমাদের project-এর সাথে মেলে, আর কাজটা ছোট scale-এ করা যায়। G1 আর G4-ও করা সম্ভব।

**সম্ভাব্য venue (general guidance):**
- **Conference:** ICSE, FSE, ASE, ISSTA, ICST (testing-এর জন্য বিশেষভাবে উপযুক্ত); workshop — LLM4Code, AST (Automation of Software Test), SBFT tool competition।
- **Journal:** ACM TOSEM, IEEE TSE, EMSE, STVR (Software Testing, Verification and Reliability), JSS, IST (MuTAP এখানেই প্রকাশিত)।

---

## ১৬. SPL3 Implementation Perspective — Software-এ কীভাবে আনবো

**Paper implement করা মানে কী?** CoverUp নিজে open-source, তাই নতুন করে লেখার দরকার নেই। আমাদের কাজ: CoverUp-এর **coverage-guided loop-কে assurance layer-এর "dynamic signal" module** হিসেবে ব্যবহার করা, আর তার উপর **oracle-strength মাপ** যোগ করা।

**প্রস্তাবিত module:**
1. **Target selector:** দুই mode —
   - *Module mode:* পুরো module (paper-এর মতো), replication-এর জন্য।
   - *Diff mode:* agent-এর patch-এর diff থেকে পরিবর্তিত line/branch বের করে সেগুলোকেই "gap" ধরা (G3)।
2. **Coverage engine:** SlipCover (paper-এর মতো) বা coverage.py; line, branch, combined, overall ও per-module median দুটোই।
3. **Generator wrapper:** CoverUp-কে বাইরে থেকে চালানো; model, temperature, continuation সংখ্যা, seed config-এ রাখা; প্রতিটা run-এর token ও USD লগ।
4. **Oracle auditor (নতুন অবদান):**
   - Mutation tool চালিয়ে mutation score।
   - Assertion count; assertion-ছাড়া test-এর হার; mock-এর হার।
   - Error follow-up-এর আগে-পরে assertion-এর expected value বদলেছে কিনা (G4)।
5. **Differential runner (patch validation):** generated test original ও patched code-এ চালিয়ে আচরণের পার্থক্য।
6. **Assurance report output:** আলাদা আলাদা signal — coverage, mutation score, flaky rate, differential পার্থক্য — প্রতিটার মান, uncertainty (k run থেকে) আর tool/model version। (Sub-domain 3-এর "assurance report" direction অনুযায়ী, weighted sum নয়।)
7. **Dashboard:** coverage বনাম mutation score scatter — "high coverage, low oracle" segment চিহ্নিত।

**Practical সতর্কতা:**
- CoverUp-এর default isolation `fork()`-নির্ভর — Windows-এ **WSL2** লাগবে (আমার পর্যবেক্ষণ; paper Windows নিয়ে কিছু বলেনি)।
- Paper-এর MuTAP setup MutPy-এর জন্য Python 3.9.12 লেগেছিল — mutation tool বাছাইয়ে Python version মিলিয়ে নিতে হবে।
- Auto-install বন্ধ রাখা বা whitelist করা (supply-chain ঝুঁকি)।
- খরচ: CM-এর 425 module-এ GPT-4o দিয়ে 399 USD — তাই ছোট subset (যেমন 20 module) দিয়ে শুরু; বর্তমান model-এ খরচের হিসাব Section ২১.৪-এ।
- Test timeout বাড়ানো (paper-এর 1 মিনিট কম ছিল)।

**সহজ কথায়:** CoverUp নতুন করে লিখতে হবে না। তার উপর একটা পরীক্ষার স্তর (oracle auditor) বসানোই আমাদের কাজ।

---

## ১৭. পরবর্তী গবেষণায় এই Paper-এর প্রভাব (Context)

> এই paper-এর পরবর্তী citation বা প্রভাব নিয়ে fact sheet-এ নির্দিষ্ট তথ্য নেই, তাই এখানে শুধু আমাদের literature-এর সাথে সম্পর্ক দেখানো হলো।

- **SWE-bench (Sub-domain 1):** SWE-bench-এর "resolved" নির্ভর করে developer test-এর উপর, আর 60% task-এ মাত্র ১টা F2P test। CoverUp-ধরনের tool দিয়ে বাড়তি test বানিয়ে resolved patch আবার যাচাই করা যায় — কিন্তু G2 মেনে differential ভাবে।
- **Agentless (Sub-domain 1):** reproduction test generation (213 থেকে 94) — CG3-এর উৎস; CoverUp-এর coverage feedback সেই test-কে আরও লক্ষ্যভেদী করতে পারে।
- **VRpilot (Sub-domain 2):** validator feedback-এ chat চালানো — CoverUp-এর error feedback-এর মতোই; দুটোতেই feedback overfitting-এর ঝুঁকি।
- **RePaCA (Sub-domain 2):** static judge; CoverUp dynamic signal — দুটো মিলিয়ে assurance report-এর দুই খুঁটি।
- **Engineering Reliable Agents monograph (Sub-domain 3):** verifier-কেও version-সহ রেকর্ড করা আর optimizer verifier-কে ঠকাতে পারে — CoverUp-এর loop নিজেই coverage-কে optimize করে, তাই এখানেও প্রযোজ্য (CG11, CG12)।
- **একই folder-এর অন্য paper (LLM Test Generation):** "An LLM Agent to Execute Tests of Arbitrary Projects" (CoverUp-এর dependency install সমস্যার সাথে সম্পর্কিত হতে পারে) ও "Oracle-Guided Program Selection from Large Language Models" (oracle দিক) — পড়ে মিলিয়ে দেখতে হবে।

**সহজ কথায়:** এই paper আমাদের আগের analysis-গুলোর সাথে জুড়ে যায়: SWE-bench-এর test-এর অভাব, Agentless-এর reproduction test, আর VRpilot-এর feedback overfitting।

---

## ১৮. Supervisor-এর সম্ভাব্য প্রশ্ন ও উত্তর (Viva Prep)

**Q1. CoverUp-এর মূল idea এক কথায় কী?**
A: LLM-কে বলে দেওয়া ঠিক কোন line ও branch এখনো test-এ চলে না, শুধু সেই code segment দেখানো, দরকারি definition নিজে চাওয়ার tool দেওয়া, আর test fail বা coverage না বাড়লে সেই feedback দিয়ে chat চালিয়ে যাওয়া।

**Q2. CodaMosa থেকে পার্থক্য কী?**
A: CodaMosa-তে genetic search মূল, LLM শুধু search আটকে গেলে একটা test দেয়। CoverUp-এ LLM মূল generator, আর coverage measurement তাকে দিক দেখায়। ফল: CM-এ median L+B 79.6% বনাম 47.2% (gpt4o) ও 55.1% (codex)।

**Q3. লাভটা কি শুধু GPT-4o-র জন্য নয়?**
A: না। একই GPT-4o-কে প্রায় একই prompt দিয়ে কিন্তু CoverUp-এর component ছাড়া চালালে overall L+B 34.0%, median 38.5% — CoverUp-এ 60.3% ও 79.6%। আর CodaMosa-কে GPT-4o দিলে Codex-এর চেয়েও সামান্য খারাপ হয়েছে।

**Q4. কোন component সবচেয়ে গুরুত্বপূর্ণ?**
A: Error feedback (বাদ দিলে 14–37% ক্ষতি), তারপর code context (7–16%)। Coverage তথ্য একবারের coverage-এ মাত্র ~2% যোগ করে, কিন্তু successive run-এ তার মূল্য স্পষ্ট — তা ছাড়া সফল function-এর হার 51.4% থেকে 12.2%-এ নামে আর function ~52% বেশি লাগে।

**Q5. Overall 60.3% কিন্তু median 79.6% — কেন?**
A: Overall হলো আকার-ভারযুক্ত, বড় module বেশি প্রভাব ফেলে; median-এ প্রতিটা module সমান। কিছু বড় module-এ (যেমন timeout-এর কারণে `youtube_dl`) coverage কম, তাই overall কম। দুটোই report করা ঠিক, কারণ একটা দিয়ে পুরো ছবি পাওয়া যায় না।

**Q6. High coverage মানে কি ভালো test?**
A: না। Coverage শুধু বলে code চলেছে; fault ধরতে হলে সেই ভুল output-এ পৌঁছাতে হবে আর assertion-কে তা ধরতে হবে। Paper mutation score বা assertion-এর মান মাপেনি — CodaMosa-র `mimesis` test-এ assertion-ই ছিল না। আমাদের assurance-এর জন্য এটাই মূল gap।

**Q7. এই tool দিয়ে কি AI agent-এর patch সঠিক কিনা যাচাই করা যায়?**
A: সরাসরি নয়। CoverUp regression test বানায় — বর্তমান code-কে সঠিক ধরে। Patch করা code-এ চালালে patch-এর আচরণকেই সঠিক ধরবে। তাই differential ভাবে ব্যবহার করতে হবে: original code-এ patch-এর পরিবর্তিত অংশ target করে test বানানো, তারপর patched code-এ চালিয়ে পার্থক্য দেখা — আর mutation score দিয়ে test-এর শক্তি মাপা।

**Q8. Error feedback loop-এর কোনো ঝুঁকি আছে?**
A: হ্যাঁ। Assertion fail করলে CoverUp LLM-কে "test ঠিক করো" বলে। Code-এ bug থাকলে LLM assertion বদলে bug-কেই সঠিক বানিয়ে ফেলতে পারে। এটা APR-এ দেখা feedback overfitting-এর test-generation রূপ (CG3, CG12)। Paper এটা মাপেনি।

**Q9. খরচ কেমন?**
A: CM suite (100K line, 425 module)-এ GPT-4o দিয়ে 399 USD, 4 ঘন্টা; CodaMosa (gpt4o) 265 USD, 71 ঘন্টা। CoverUp 18 গুণ দ্রুত কিন্তু 48% বেশি token। আমার হিসাবে module প্রতি ~0.94 USD, আর input 5 / output 15 USD per million token ধরলে Table 3-এর cost হুবহু মেলে।

**Q10. Statistical significance কীভাবে দেখানো হয়েছে?**
A: Per-module coverage-এ paired permutation test, দুই CodaMosa baseline-এর বিরুদ্ধেই p = 2.0 × 10⁻⁵। কিন্তু ablation ও MuTAP তুলনায় কোনো significance test বা variance নেই, আর একটাই run — এটা দুর্বলতা।

**Q11. MuTAP (gpt4o few-shot) এত খারাপ কেন?**
A: Few-shot prompt-এর উদাহরণ দেখে GPT-4o আসল function-এর বদলে উদাহরণের function-এর test লিখেছে — test চলেছে কিন্তু coverage দেয়নি (overall L+B 10.4%)। এটা দেখায় prompt format model বদলালে ভেঙে যেতে পারে।


**সহজ কথায়:** Viva-তে মূল তিনটা কথা মনে রাখলেই হবে: CoverUp কী করে, কেন CodaMosa-র চেয়ে ভালো, আর কেন coverage একা যথেষ্ট নয়।

**Q12. তুমি এই paper থেকে কী implement করবে?**
A: CoverUp-কে wrapper হিসেবে চালিয়ে দুটো mode — module mode (replication, ছোট CM subset) আর diff mode (agent patch-এর পরিবর্তিত অংশ)। তার উপর oracle auditor: mutation score, assertion-ছাড়া test, assertion বদলের হার। Output আলাদা আলাদা signal-এর assurance report।

---

## ১৯. Glossary (দ্রুত মনে রাখার জন্য)

| Term | অর্থ |
|---|---|
| Line coverage | কত % executable line অন্তত একবার চলেছে |
| Branch coverage | কত % control-flow arc (যেমন `610->608`) চলেছে |
| Line + Branch | Line ও branch একসাথে গুনে coverage |
| Overall বনাম median | পুরো suite একসাথে (আকার-ভারযুক্ত) বনাম module-গুলোর মাঝের মান |
| Segment | Uncovered line ধারণকারী function/method/class-এর ছোট excerpt |
| Continued chat | আগের history + feedback দিয়ে LLM-কে আবার জিজ্ঞাসা |
| Tool / function calling | LLM-এর বাইরের function চালানোর অনুরোধ |
| `get_info` | CoverUp-এর tool — নাম দিলে definition ফেরত দেয় |
| SBST | Genetic algorithm দিয়ে test খোঁজা |
| Pynguin | Python-এর SBST tool |
| CodaMosa | Pynguin + LLM (plateau-তে) |
| MuTAP | LLM + mutation testing দিয়ে assertion |
| Mutation score | কত % কৃত্রিম ভুল (mutant) test ধরেছে |
| Test oracle | সঠিক output কী — তা নির্ধারণকারী (assertion) |
| Regression test | বর্তমান আচরণ সংরক্ষণকারী test |
| State pollution | এক test-এর side effect অন্য test ভাঙে |
| Test isolation | প্রতিটা test আলাদা process-এ |
| Flaky test | একই code-এ কখনো pass কখনো fail |
| Ablation | অংশ বাদ দিয়ে প্রভাব মাপা |
| Permutation test | চিহ্ন এলোমেলো করে significance মাপা |
| Leaky bucket | নির্দিষ্ট হারে request পাঠানোর rate limiter |
| Feedback overfitting | Validator-এর feedback-কে "খুশি" করতে শেখা, আসল লক্ষ্য নয় |

**সহজ কথায়:** এই glossary-র সবচেয়ে দরকারি শব্দ তিনটা: Oracle, Mutation score আর Regression test।

---

## ২০. এক নজরে সারাংশ (Summary Card)

| | |
|---|---|
| **Problem** | Python-এ high coverage test বানানো কঠিন; SBST আটকে যায়, আগের LLM tool coverage তথ্য ব্যবহার করে না |
| **Solution** | Coverage gap থেকে segment, gap-চিহ্নিত prompt, `get_info` tool, error ও coverage feedback-এ continued chat, isolation ও flaky check |
| **Method** | GPT-4o (temp 0); CM (425 module), PY (84), MT (163 function); CodaMosa, MuTAP ও নিজের ablation-এর সাথে তুলনা |
| **Key result** | CM: overall L+B 60.3% (CodaMosa-gpt4o 45.2%), median 79.6% (47.2%); MT: 89.0% (MuTAP সেরা 77.7%); PY: 97.1% |
| **Key insight** | Design-ই বড় অবদান (ablated 34.0%); error feedback সবচেয়ে জরুরি; ~40% সাফল্য iteration থেকে |
| **Cost** | 399 USD, 4 ঘন্টা (CodaMosa 265 USD, 71 ঘন্টা) |
| **Main limitation** | শুধু coverage মাপা — oracle শক্তি, variance, contamination, flaky rate নেই |
| **আমাদের জন্য gap** | Dynamic signal হিসেবে **oracle-strength audit** আর **patch-এর জন্য differential, diff-targeted generation** |

---

## ২১. বর্তমান (2026) প্রেক্ষাপট — আজকের Model ও Agent-দের সাথে তুলনা

> **উৎস:** এই section-এর সব current-state তথ্য `00_Current_State_2026_Sources.md` (fact sheet, compiled 2026-10-28) থেকে নেওয়া — বিশেষত §6 (Test generation by current agents)। প্রতিটা সংখ্যার পাশে লেখা আছে সেটা **কোম্পানির নিজের দাবি (vendor-reported)** নাকি **স্বাধীনভাবে মাপা (independent)**। Fact sheet যেটাকে "search-snippet only" বলেছে, সেটা এখানেও তাই চিহ্নিত — supervisor-কে দেখানোর আগে মূল উৎস খুলে যাচাই করা উচিত। আমার নিজের যুক্তি "আমার পর্যবেক্ষণ" দিয়ে আলাদা করা।
>
> **গুরুত্বপূর্ণ:** Fact sheet-এ **CoverUp, CodaMosa, Pynguin বা MuTAP-এর কোনো বর্তমান-model পুনঃপরীক্ষা নেই**, আর coverage-guided unit test generation-এর কোনো 2026 benchmark সংখ্যাও নেই। অর্থাৎ "আজকের model (Opus 5.5, GPT-6, Gemini 4) CM suite-এ কত coverage পায়" — এই প্রশ্নের উত্তর জানা নেই। **এটা নিজেই একটা gap।**

### ২১.১ Paper-এর সময় বনাম এখন

| দিক | Paper-এ (tool 2023-08, evaluation GPT-4o, প্রকাশ FSE 2025) | এখন, October 2026 | উৎস |
|---|---|---|---|
| ব্যবহৃত model | `gpt-4o-2024-05-13`, temperature 0 | OpenAI-এর GPT-6 family (Astra, Sol, Luna) ও GPT-6.1 Sol/Terra; Anthropic Opus 5.5 (2026-09-22), Sonnet/Haiku 5.5; Google Gemini 4 Argon (2026-10-13) | Fact sheet §1 (vendor pages, primary) |
| Coverage-guided test generation-এ বর্তমান model-এর ফল | CM: overall L+B 60.3%, median 79.6% | **পাওয়া যায়নি** — fact sheet-এ কোনো সংখ্যা নেই | — |
| Reproduction test benchmark (SWT-bench, TDD-Bench) | (paper-এর বিষয় নয়) | Opus 5.5, GPT-6, Gemini 4-এর কোনো 2026 entry **পাওয়া যায়নি** | Fact sheet §6 |
| Agent-দের লেখা test-এর oracle | Paper oracle মাপেনি; prompt-এ শুধু "include assertions" | 86,156টা test-file patch (33,596 agent PR; Codex, Copilot, Devin, Cursor, Claude Code)-এর **80.2%-এ দুর্বল বা কোনো স্পষ্ট oracle নেই**; শক্ত oracle merge-এর সম্ভাবনা বাড়ায় (OR 1.28, p<0.001) — **independent** | "All Smoke, No Alarm", arXiv 2606.18168 |
| Mocking | Prompt `monkeypatch`/`pytest-mock` ব্যবহারে উৎসাহ দেয় | Agent commit-এর 36% test-এ mock যোগ করে, non-agent-এর 26% — **independent, search-snippet only** | arXiv 2602.00409 (MSR 2026) |
| Coverage বনাম মানুষ | CoverUp বনাম tool তুলনা | AI test-adding commit-এর 16.4% লিখেছে; coverage gain মানুষের test-এর **কাছাকাছি**; test লম্বা, assertion বেশি — **independent, search-snippet only** | arXiv 2603.13724 (MSR 2026 Mining Challenge) |
| Weak assertion | মাপা হয়নি | AIDev-এর ~205k test file-এ agent test-এ weak assertion সামান্য বেশি, প্রায় 14.3% বনাম 11.9% — **secondary summary থেকে, যাচাই করা হয়নি** | arXiv 2607.12068 |
| Agent-এর জন্য test লেখার মূল্য | — | Test লেখা issue resolution-এ সীমিত উন্নতি দেয়, প্রায়ই observation-based debugging দিয়ে প্রতিস্থাপিত — **independent, search-snippet only** | "Rethinking the Value of Agent-Generated Tests", 2602.07900 |
| Vendor দাবি | — | Fable 5.1 "can write its own tests to check its work"; "less likely to disable a failing test to pass" — **vendor-reported, qualitative** | Anthropic Fable page; AWS blog |
| Benchmark test-এর মান | CoverUp coverage-কেই লক্ষ্য ধরে | SWE-Bench Pro audit-এ broken task-এর একটা category "low-coverage tests" (অসম্পূর্ণ fix pass করে); 731 task-এর 27.4% (automated) বা 34.1% (মানুষ) broken — **secondary report** | the-decoder (OpenAI post নিজে পৌঁছানো যায়নি) |
| Run-to-run variance | একটাই run, temperature 0 | Temperature 0-এ rerun প্রায় deterministic (ever-flip 0.7–2.7%), কিন্তু অর্থ-অপরিবর্তিত prompt পরিবর্তনে SD **11–58 গুণ বেশি** — **independent** | Noise Floor Audit, arXiv 2608.22331 |
| Scaffold-এর প্রভাব | RQ2: একই GPT-4o, scaffold বদলে 34.0% থেকে 60.3% | SWE-bench Verified-এ একই model-এ scaffold বদলালে **29.8 point** পর্যন্ত পার্থক্য — **independent** (ভিন্ন task: patch, test নয়) | "Coding Agents Have Converged", arXiv 2609.17394 |
| খরচ | GPT-4o: 399 USD (CM) | API দাম per million token: GPT-6.1 Terra 1 input / 5 output USD (**vendor**); Opus 5.5 4 / 20 USD (**secondary, search-snippet only**); Fable 5.1 10 / 50 USD (**secondary, search-snippet only**) | Fact sheet §1 |

**সহজ কথায়:** Paper-এর সময় আর এখনকার মধ্যে সবচেয়ে বড় পার্থক্য: model অনেক নতুন, কিন্তু coverage-guided test generation-এর কোনো নতুন সংখ্যা নেই।

### ২১.২ কোন Finding এখনো সত্য, কোনটা পুরনো হয়ে গেছে

- **এখনো সত্য, আরও শক্ত প্রমাণসহ — "coverage ≠ শক্ত oracle" (আমাদের critique ১):** Paper নিজে মাপেনি, কিন্তু 2026-এ বাস্তব agent PR-এ 80.2% test patch-এ দুর্বল বা কোনো স্পষ্ট oracle নেই (independent), যদিও AI test-এর coverage gain মানুষের কাছাকাছি (search-snippet)। **আমার পর্যবেক্ষণ:** এই দুই তথ্য একসাথে ঠিক CoverUp-এর blind spot দেখায় — coverage-এ ভালো, oracle-এ দুর্বল।
- **এখনো সত্য (অন্য task-এ পরোক্ষ প্রমাণ) — "scaffold LLM-এর মতোই গুরুত্বপূর্ণ" (Key Finding ২):** Patch-generation-এ scaffold বদলে 29.8 point (independent)। তবে test generation-এ বর্তমান model দিয়ে scaffold-ablation **কেউ মেপেছে বলে fact sheet-এ নেই**।
- **এখনো সত্য — prompt sensitivity (MuTAP few-shot-এর ধস):** Noise Floor Audit-এ prompt-এর ছোট পরিবর্তনে 11–58 গুণ বেশি ওঠানামা (independent)। CoverUp-এর prompt-এর অনেক "নিয়ম" (top-level code নয়, line tag) GPT-4-যুগে বানানো — বর্তমান model-এ এগুলো এখনো দরকার কিনা **জানা নেই**।
- **এখনো সত্য — LLM test-এ mock ও side effect-এর সমস্যা:** Paper-এর state pollution উদাহরণের পাশাপাশি এখন agent-রা বেশি mock করে (36% বনাম 26%, search-snippet)। অতিরিক্ত mock coverage বাড়ায় কিন্তু oracle দুর্বল করতে পারে (আমার পর্যবেক্ষণ)।
- **সম্ভবত পুরনো — context window-এর চাপ:** Paper-এ segment ছোট রাখার একটা কারণ ছিল context limit। এখনকার কিছু model-এ 1M context (Kimi K3.1 Pro, fact sheet-এ secondary)। কিন্তু paper-এর অন্য দুই কারণ — লম্বা prompt-এ ভুল বাড়ে আর token-এ খরচ — এখনো প্রাসঙ্গিক; বর্তমান model-এ এ বিষয়ে test-gen-specific তথ্য **পাওয়া যায়নি**।
- **অজানা — বর্তমান agent কি CoverUp ছাড়াই এমন coverage পায়?** Claude Code, Codex CLI-এর মতো agent এখন নিজেই file পড়ে, test চালায় (CoverUp-এর `get_info` + feedback loop-এর সাধারণ রূপ)। কিন্তু তারা CM-এর মতো suite-এ কত coverage পায় — **কোনো সংখ্যা নেই**। "Rethinking the Value of Agent-Generated Tests" (search-snippet) বলছে agent-রা প্রায়ই test না লিখে observation দিয়ে debug করে — অর্থাৎ test generation নিজে থেকে হয় না, CoverUp-এর মতো explicit loop এখনো মূল্যবান হতে পারে (আমার পর্যবেক্ষণ, প্রমাণ নয়)।

**সহজ কথায়:** আজকের agent-রা নিজেই test লেখে ও চালায়। কিন্তু তারা কত coverage পায় আর test কতটা শক্ত, তা কেউ মাপেনি। এটাই খোলা সুযোগ।
- **নতুন ঝুঁকি, paper-এ ছিল না — test নিয়ে reward hacking:** Vendor-রা এখন বলছে model "failing test disable" করে কম (Fable 5.1, vendor qualitative); Opus 5.5 "hidden tests" নিয়ে explicit reasoning করে (vendor)। CoverUp-এর loop LLM-কে test বদলাতে বলে — আধুনিক model এখানে কী করে, **independent audit নেই**।

### ২১.৩ এই Paper-এর Gap-গুলো আজও খোলা কিনা

| Gap | Common gap | 2026-এ অবস্থা | প্রমাণ |
|---|---|---|---|
| G1: Oracle শক্তি (mutation, assertion) | CG3, CG1 | **খোলা** | 80.2% agent test patch-এ দুর্বল/অনুপস্থিত oracle (independent); weak assertion 14.3% বনাম 11.9% (secondary, যাচাই হয়নি) |
| G2: Differential use for patch validation | CG1, CG3 | **খোলা** | PatchDiff: plausible patch-এর 29.6% gold থেকে ভিন্ন আচরণ (independent, ICSE 2026), কিন্তু **বর্তমান model-এ আবার মাপা হয়নি**; PROBE-ধরনের test augmentation-এ resolution rate কমে (search-snippet) |
| G3: Diff-targeted coverage | CG3 | **খোলা** | SWE-Bench Pro audit-এ "low-coverage tests" broken-task category (secondary) — patch-এর বদলানো অংশ কম cover হলে অসম্পূর্ণ fix pass করে |
| G4: Feedback overfitting / test-কে code-এ fit করানো | CG3, CG12 | **খোলা** | Fact sheet-এ test-generation loop-এ assertion বদলের হার নিয়ে কোনো তথ্য নেই; verifier gaming-এর সাধারণ প্রমাণ আছে (GLM-5.2: 78.80% থেকে 57.32%, independent) |
| G5: Run-to-run variance | CG4, CG8 | **খোলা (মাপা হচ্ছে, test-gen-এ নয়)** | Noise Floor Audit 11–58 গুণ (independent); SWE Atlas pass@1 থেকে pass^3-এ 30–50% পতন (search-snippet) — দুটোই patch/agent task, test generation নয় |
| G6: Contamination-মুক্ত test-gen benchmark | CG6 | **খোলা** | Patch-এর জন্য SWE-rebench, DeepSWE আছে; test generation-এর জন্য contamination-মুক্ত benchmark fact sheet-এ **নেই** |
| G7: Cost-effectiveness | CG8 | **খোলা, কিন্তু দাম কমেছে** | Terra 1/5 USD per M (vendor) — GPT-4o-যুগের চেয়ে সস্তা model আছে; কিন্তু coverage per USD-এর মাপ নেই |
| G8: Flaky ও polluting test-এর হার | CG4, CG11 | **তথ্য পাওয়া যায়নি** | AIDev-এ flakiness নিয়ে একটা গবেষণার উল্লেখ আছে (2607.12068), কিন্তু fact sheet-এ flaky হারের সংখ্যা নেই |
| G9: Security-কেন্দ্রিক test ও auto-install ঝুঁকি | CG5 | **খোলা** | Agent code-এ FuncPass 62–84% কিন্তু SecPass 7.8–17.3% (Endor/SusVibes, independent, পুরনো model); security test generation-এর বর্তমান তথ্য নেই |
| G10: অন্য language ও repository-level | CG9 | **তথ্য পাওয়া যায়নি** | Agent PR গবেষণা বহু-ভাষার repo কভার করে, কিন্তু CoverUp-ধরনের tool-এর বহু-ভাষা evaluation fact sheet-এ নেই |
| G11: Test quality / smell | CG3 | **খোলা** | Over-mocking 36% বনাম 26% (search-snippet); শক্ত oracle merge বাড়ায় (OR 1.28) — মানুষ quality-কে মূল্য দেয় |
| G12: Generator/verifier-এর নিজের validity | CG10, CG11 | **খোলা** | LLM judge-এর দুর্বলতা (ComPass plain LLM 62.14%, search-snippet); DeepSWE: SWE-Bench Pro-র test-এর সাথে judge-এর অমিল 32.4% (independent) |
| G13: Abstention | CG7 | **খোলা** | অসম্ভব/অস্পষ্ট task-এ reward hacking-এর চেষ্টা 3–6 গুণ বাড়ে (Opus 5.5 System Card, vendor) — test generation-এ "জানি না" বলার ক্ষমতা মাপা হয়নি |

**সহজ কথায়:** ২০২৬-এ প্রায় সব gap এখনো খোলা। বিশেষ করে বর্তমান model দিয়ে test generation-এর কোনো মাপ নেই।

### ২১.৪ বর্তমান Model দিয়ে আবার পরীক্ষা করলে — SPL3 Idea (cost-aware)

**খরচের ভিত্তি (আমার হিসাব):** Paper-এ CM-এর 425 module-এ CoverUp 58.08M input + 7.26M output token নিয়েছে। একই token ধরে (বর্তমান model বেশি বা কম token নিতে পারে — এটা অনুমান):
- GPT-6.1 Terra (1/5 USD, vendor): $58.08 \times 1 + 7.26 \times 5 \approx 94.4$ USD পুরো CM; **20 module-এ ≈ 4.4 USD**।
- Opus 5.5 (4/20 USD, secondary snippet): $58.08 \times 4 + 7.26 \times 20 \approx 377.5$ USD পুরো CM; **20 module-এ ≈ 17.8 USD**।

1. **Coverage বনাম oracle audit (G1):** CoverUp-কে একটা সস্তা current model (যেমন GPT-6.1 Terra) দিয়ে CM-এর 20টা module-এ চালানো; coverage-এর পাশাপাশি mutation score, assertion-ছাড়া test-এর হার, mock-এর হার মাপা। **যে gap দেখাবে:** "high coverage, low mutation score" segment কত % — বর্তমান model-এর জন্য এই সংখ্যা fact sheet-এ কোথাও নেই। খরচ ≈ 4–5 USD LLM + local mutation compute।
2. **Bug "পাকা করা" পরীক্ষা (G4):** CM-এর project-গুলো BugsInPy থেকে — buggy version-এ CoverUp চালিয়ে দেখা কত generated test bug-কে "সঠিক" বলে assert করে (fixed version-এ fail করে), আর কতগুলো error follow-up-এ assertion বদলে এসেছে। **Gap:** feedback overfitting-এর প্রথম সরাসরি মাপ (আমার জানামতে; literature যাচাই করতে হবে)। 10–15টা bug-এ কয়েক USD।
3. **Diff-targeted differential test দিয়ে agent patch যাচাই (G2, G3):** SWE-rebench-এর সর্বশেষ window থেকে ~20টা task-এ একটা agent-এর resolved patch নিয়ে, patch-এর বদলানো line-কে gap ধরে original code-এ test generate, তারপর patched code-এ চালানো। **Gap:** PatchDiff-এর 29.6% বর্তমান agent-এ কত — কেউ আবার মাপেনি। Patch পাওয়ার খরচ: SWE-rebench-এ প্রতি problem 0.81–4.40 USD (independent), তাই 20 task-এ ≈ 16–88 USD (আমার হিসাব) — সস্তা model দিয়ে নিচের দিকে।
4. **Variance (G5):** একই 20 module-এ 3টা run (temperature 0 ও একটা non-zero), coverage ও mutation score-এর SD। **Gap:** Noise Floor Audit-এর ফল test generation-এ খাটে কিনা। খরচ idea ১-এর 3 গুণ (Terra-তে ≈ 13 USD)।
5. **Scaffold বনাম model (RQ2-এর 2026 version):** একই current model-এ CoverUp বনাম "plain agent" (যেমন mini-SWE-agent-কে শুধু 'এই module-এর test লেখো' বলা) — coverage ও mutation score। **Gap:** CoverUp-এর design-এর মূল্য আধুনিক agent-এর যুগে টিকে আছে কিনা — fact sheet-এ কোনো তথ্য নেই।

**সহজ কথায়:** ২০২৬-এ করার মতো পরীক্ষাগুলো ছোট। কয়েক USD-তে ২০টা module-এ চালিয়ে সংখ্যা পাওয়া যায়।

### ২১.৫ Supervisor-এর সম্ভাব্য প্রশ্ন (2026 প্রসঙ্গে)

**Q1. আজকের Claude Code বা Codex তো নিজেই test লেখে — CoverUp কি এখন অপ্রাসঙ্গিক?**
A: জানা নেই, আর সেটাই gap। Fact sheet-এ বর্তমান agent-দের CM-ধরনের suite-এ coverage-এর কোনো সংখ্যা নেই। যা জানা: বাস্তব agent PR-এর test patch-এর 80.2%-এ দুর্বল বা অনুপস্থিত oracle (independent), আর agent-রা প্রায়ই test না লিখে observation দিয়ে debug করে (search-snippet)। তাই CoverUp-এর explicit coverage-feedback loop আর তার উপর oracle check এখনো প্রাসঙ্গিক মনে হয় — কিন্তু এটা মাপতে হবে (২১.৪-এর idea ৫)।

**Q2. বর্তমান model-এ CoverUp-এর coverage কি আরও বেশি হবে?**
A: সম্ভবত, কিন্তু প্রমাণ নেই। Paper নিজেই দেখিয়েছে নতুন model মানেই ভালো নয় (CodaMosa gpt4o < codex; MuTAP few-shot gpt4o 10.4%), আর 2026-এ prompt পরিবর্তনে ফলাফল 11–58 গুণ বেশি ওঠানামা করে (independent)। তাই replication ছাড়া দাবি করা যাবে না।

**Q3. আমাদের assurance layer-এ CoverUp-এর ভূমিকা কী হবে?**
A: Dynamic signal-এর generator — কিন্তু তিনটা শর্তে: (১) differential mode-এ, original code-এ test বানিয়ে patched code-এ চালানো; (২) coverage-এর সাথে mutation score report করা, কারণ coverage oracle শক্তি বলে না; (৩) generator-এর model ও version, k run-এর variance assurance report-এ রেকর্ড করা (CG4, CG11)।

**Q4. খরচ কি SPL3-এর জন্য সম্ভব?**
A: হ্যাঁ, ছোট scale-এ। Paper-এর token হিসাব ধরে GPT-6.1 Terra-তে (vendor দাম) 20 module ≈ 4.4 USD, Opus 5.5-এ (secondary দাম) ≈ 17.8 USD। আসল খরচ বর্তমান model-এর token ব্যবহারের উপর নির্ভর করবে, তাই প্রথমে 2–3 module-এ pilot চালিয়ে মেপে নেবো।
