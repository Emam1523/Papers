# Paper Analysis 05 (Security): SecureVibeBench — Benchmarking Secure Vibe Coding of AI Agents

> Sub-domain: Security of AI-Generated Code
> PDF: Security of AI-Generated Code/Benchmarking Secure Vibe.pdf

## ০. Bibliographic info

| ক্ষেত্র | তথ্য |
|---|---|
| Title | SecureVibeBench: Benchmarking Secure Vibe Coding of AI Agents via Reconstructing Vulnerability-Introducing Scenarios |
| Authors | Junkai Chen, Huihui Huang (equal contribution), Yunbo Lyu, Junwen An, Jieke Shi, Chengran Yang (corresponding), Ting Zhang, Haoye Tian, Yikun Li, Zhenhao Li, Xin Zhou, Xing Hu, David Lo |
| Institutions | Singapore Management University, NUS, Monash, Aalto, York University, Zhejiang University |
| Version | arXiv:2509.22097v5 [cs.SE], 6 Jun 2026 |
| Venue | Paper-এ কোনো conference/journal-এর নাম লেখা নেই; আমি অনুমান করছি না। এটি arXiv preprint হিসেবে পাওয়া গেছে |
| Code/Data | GitHub: iCSawyer/SecureVibeBench |
| Funding | National Research Foundation Singapore (Investigatorship NRFNRFI08-2022-0002), National Key R&D Program of China |
| Language / domain | শুধু C/C++ memory-safety vulnerability |
| Size | ১০৫টি task, ৪১টি project, ৯টি domain |
| Agents / LLMs | ৩টি agent scaffold (SWE-agent, OpenHands, Aider) × ৫টি LLM, আলাদাভাবে ২টি CLI agent (Claude Code, Codex) |

## ★ সহজ ভাষায় পুরো Paper (প্রথমবার পড়ার জন্য)

### ক. Paper-টা কী নিয়ে?

- এটা একটা **benchmark paper**। Benchmark মানে হলো একটা "পরীক্ষার প্রশ্নপত্র", যা দিয়ে অনেক AI-কে একই মাপকাঠিতে যাচাই করা যায়।
- এই প্রশ্নপত্রের নাম SecureVibeBench। এটা মাপে AI coding agent নিরাপদ (secure) code লিখতে পারে কি না।
- বানিয়েছেন Singapore Management University-র David Lo-র দল এবং আরও কয়েকটি university-র গবেষকরা।
- প্রশ্নগুলো এসেছে সত্যিকারের open-source project থেকে, যেখানে একজন মানুষ developer আসলেই একবার vulnerability (নিরাপত্তা-দুর্বলতা) ঢুকিয়ে ফেলেছিলেন।
- মোট ১০৫টি task, সব C/C++ ভাষায়। এটি arXiv-এ প্রকাশিত preprint।

### খ. সমস্যাটা কী ছিল?

- AI agent এখন পুরো repository-তে code লিখে দেয়। মানুষ প্রায় না দেখেই সেটা নিয়ে নেয়, একে বলে "vibe coding"।
- প্রশ্ন হলো, সেই code কি নিরাপদ? আগের benchmark এটা ঠিকমতো মাপতে পারত না।
- আগের benchmark-এ প্রশ্নগুলো ছিল ছোট (একটা function বা একটা file) অথবা বানানো (কৃত্রিম) scenario।
- যেগুলো আসল ঘটনা থেকে নেওয়া, সেগুলোও সাধারণত নেওয়া হতো "bug ঠিক করার আগের মুহূর্ত" থেকে। অথচ ভুলটা ঢুকেছিল তারও অনেক আগে।
- উদাহরণ: ধরো একজন developer ২০১৯ সালে নতুন feature লিখতে গিয়ে buffer overflow ঢোকালেন, আর ২০২১ সালে সেটা ধরা পড়ল। আগের benchmark ২০২১ সালের code দিয়ে প্রশ্ন বানাত। কিন্তু ভুলটা হয়েছিল ২০১৯ সালে, অন্য requirement আর অন্য code-এর ওপর।
- আরেকটা সমস্যা: agent নিজে যে নতুন ধরনের ঝুঁকি ঢোকায়, সেটা ধরার ব্যবস্থা প্রায় ছিল না।

### গ. Paper কী solve করেছে?

- **নতুন benchmark:** মানুষ ঠিক যে মুহূর্তে vulnerability ঢুকিয়েছিল, সেই মুহূর্তের requirement আর code agent-কে দেওয়া হয়। এভাবে বানানো ১০৫টি task।
- **তিন স্তরের যাচাই:** functional test (কাজ ঠিক আছে কি না), PoV (পুরনো vulnerability ফিরে এসেছে কি না), আর Semgrep (নতুন সন্দেহজনক ঝুঁকি আছে কি না)।
- **চার রকম ফল:** প্রতিটি patch IC, C-VUL, C-SUS বা C-SEC হয়।
- **৫টি agent মাপা হয়েছে:** ৩টি scaffold × ৫টি LLM, সঙ্গে Claude Code ও Codex।
- মূল সংখ্যা:
  - সেরা ফল ২৩.৮%। মানে ১০০টা task-এর মধ্যে সেরা agent-ও মাত্র প্রায় ২৪টায় "ঠিক এবং নিরাপদ" patch দেয়।
  - ১৫টি combination-এর গড় ১১.৬২%। মানে ১০০টার মধ্যে গড়ে মাত্র ১১-১২টা।
  - সেরা agent-এর correct patch-এর প্রায় ৪৯% নিরাপদ নয়। মানে ঠিক-কাজ-করা patch-ও অর্ধেক ক্ষেত্রে ঝুঁকিপূর্ণ।

### ঘ. কীভাবে solve করেছে?

1. প্রথমে ARVO ও OSS-Fuzz থেকে ৪,৯৯৩টি সত্যিকারের vulnerability জোগাড় করেছে। (এগুলো আগেই fuzzing দিয়ে ধরা পড়া ও পুনরায় ঘটানো যায় এমন bug-এর সংগ্রহ।)
2. B-SZZ নামের একটা পুরনো technique দিয়ে অনুমান করেছে, কোন commit-এ vulnerability ঢুকেছিল। (fix-এর বদলানো লাইনগুলোর "আসল লেখক commit" খোঁজা হয়, যেন কেউ ভুল লাইনটা কে লিখেছিল তা খুঁজছে।)
3. সেই অনুমান যাচাই করেছে সত্যিকারের PoV চালিয়ে। (PoV একটা input, যা চালালে vulnerability-র crash দেখা যায়।) মাত্র ২৫৪টি টিকেছে।
4. প্রতিটির জন্য test suite আর PoV হাতে-কলমে চালিয়ে ঠিক করেছে, তারপর ২৩২টি থেকেছে।
5. একটা LLM দিয়ে commit message ও issue থেকে সংক্ষিপ্ত requirement লিখিয়েছে। এতে vulnerability-র কথা নেই, code-ও বলে দেওয়া নেই।
6. হাতে পরীক্ষা করে জটিল ও খারাপ task বাদ দিয়ে ১০৫টি রেখেছে।
7. agent-কে vulnerability-র আগের মুহূর্তের repository (PVIC) ও requirement দিয়ে patch লিখতে বলেছে।
8. patch-টা functional test, PoV ও Semgrep দিয়ে মেপে চারটির একটি label দিয়েছে।

### ঙ. এরপর কী করা যায়?

- Authors বলছেন: Semgrep-এর false alarm কমাতে symbolic execution বা LLM-as-a-judge ব্যবহার করা যেতে পারে।
- Authors আরও বলছেন: শুধু C/C++ নয়, অন্য ভাষা ও অন্য ধরনের vulnerability-তেও কাজ বাড়ানো দরকার।
- যা এখনো খোলা: oracle gold patch-এর ওপর নির্ভর করে, অথচ gold নিজেই vulnerable। এই প্রভাব কেউ মাপেনি।
- যা এখনো খোলা: প্রতিটি combination মাত্র একবার চালানো হয়েছে এবং leakage-এর নিজস্ব পরীক্ষা নেই।
- আমরা SPL3-এ করতে পারি: ১০৫টির মধ্যে ২০-৩০টি task নিয়ে একটি agent-free security checker বানাতে পারি, যেখানে functional, PoV ও SAST আলাদা signal।
- আমরা আরও করতে পারি: প্রতি task ৩ বার চালিয়ে Wilson CI বের করতে পারি এবং leakage guard (.git history পরীক্ষা) যোগ করতে পারি।

> **মনে রাখো:**
> Test pass করা আর নিরাপদ হওয়া আলাদা জিনিস; সেরা agent-ও ১০০টার মধ্যে মাত্র ২৪টা patch ঠিক ও নিরাপদ বানায়।
> তবে মাত্র ১০৫ task ও একবার চালানোর কারণে ranking দুর্বল, আর oracle নিজেও gold-এর ওপর নির্ভর করে।

## ১. TL;DR

- SecureVibeBench হলো C/C++ repository-level secure coding benchmark। (Repository-level মানে একটা পুরো project, শুধু একটা function নয়।) এর বিশেষত্ব: task-টা বানানো হয়েছে সেই মুহূর্ত থেকে, যখন একজন মানুষ developer আসলে vulnerability ঢুকিয়েছিল (VIC = Vulnerability-Introducing Commit)। অর্থাৎ agent-কে একই requirement ও একই code version (VIC-এর parent) দেওয়া হয়।
- VIC খুঁজতে static B-SZZ এবং dynamic PoV (proof-of-vulnerability) verification cascade করা হয়েছে। (Cascade মানে একটার পর একটা ছাঁকনি।) ৪,৯৯৩ → ১,৬৩২ → ২৫৪ → ২৩২ → ১০৫ instance।
- প্রতিটি agent patch চার ভাগে পড়ে: IC (functionally incorrect), C-VUL (correct কিন্তু gold patch-এর vulnerability আছে), C-SUS (correct, কিন্তু SAST নতুন ঝুঁকি দেখিয়েছে), C-SEC (correct এবং secure)।
- সেরা ফল: SWE-agent + Claude Sonnet 4.5 = **২৩.৮%** C-SEC (১০৫-এর মধ্যে ২৫টি)। ১৫টি agent×LLM combination-এর গড় C-SEC ১১.৬২%।
- একই agent-এর functional correctness বেশি হলেও security কম হতে পারে: Claude Code correct ৪৮.৬% কিন্তু C-SEC মাত্র ১৭.১%।
- প্রতিটি combination মাত্র **একবার** চালানো হয়েছে; ১০৫ task-এ একটা task = ০.৯৫২ percentage point। তাই র‍্যাঙ্কিং-এর পার্থক্য statistically দুর্বল।

**Supervisor-কে ৩০ সেকেন্ডে:** "এটা আমাদের CG5-এর সবচেয়ে সরাসরি agent-level প্রমাণ। সেরা agent-ও repository-level C/C++ task-এ মাত্র ২৩.৮% patch-কে correct এবং secure বানায়; correct patch-এর প্রায় অর্ধেকে (৪৯%) PoV-vulnerable বা SAST-suspicious ঝামেলা থাকে। আমাদের assurance report-এ patch security-কে test pass থেকে আলাদা signal হিসেবে রাখতে হবে। দুর্বলতা: ১০৫ task, একক run, Semgrep-এর প্রায় ৫০% false alarm, আর leakage/contamination-এর নিজস্ব পরীক্ষা নেই।"

## ২. Background (শুধু এই project-এর জন্য নতুন ধারণা)

### ২.১ Vulnerability lifecycle: VIC, PVIC, VFC

- **VIC** (Vulnerability-Introducing Commit): যে commit-এ একটি requirement implement করতে গিয়ে developer vulnerability ঢুকিয়েছিল।
- **PVIC**: VIC-এর ঠিক আগের commit (parent)। এটাই agent-কে দেওয়া code base।
- **VFC** (Vulnerability-Fixing Commit): যে commit vulnerability সারিয়েছে। এর diff-ই সাধারণত "gold patch" ধরা হয়। (Gold patch হলো "সঠিক উত্তর হিসেবে ধরা patch"।)
- পুরনো benchmark (যেমন SusVibes, paper-এর বর্ণনা অনুযায়ী) fix commit-এর আগের commit থেকে task বানায়।
- কিন্তু vulnerability আসলে তার আরও আগে ঢুকেছিল। তাই requirement ও context মানুষের ভুলের মুহূর্তের সাথে মেলে না। এখানেই SecureVibeBench আলাদা।

### ২.২ SZZ

- B-SZZ (Śliwerski et al. 2005) fix commit-এর বদলানো লাইনের ওপর git blame চালিয়ে "bug/vulnerability-inducing" candidate commit বের করে। (git blame বলে দেয় কোন লাইন কোন commit-এ লেখা হয়েছিল।)
- এটা দ্রুত, কিন্তু ভুল হতে পারে (paper বলছে accuracy অসন্তোষজনক)।

### ২.৩ PoV (Proof-of-Vulnerability)

- PoV হলো একটি program/input যা নির্দিষ্ট একটি vulnerability-র উপস্থিতি নিশ্চিত করে (সাধারণত sanitizer-সহ crash)। (Sanitizer এমন একটা tool যা memory-র ভুল ঘটলেই program থামিয়ে জানিয়ে দেয়।)
- এখানে PoV হলো binary oracle: "এই বিশেষ vulnerability আছে কি নেই"। (Oracle মানে সঠিক-ভুল বলে দেওয়ার পরীক্ষক।)
- নতুন ধরনের vulnerability এটি ধরতে পারে না।

### ২.৪ OSS-Fuzz এবং ARVO

- OSS-Fuzz: Google-এর continuous fuzzing প্রকল্প। (Fuzzing মানে এলোমেলো input দিয়ে program ভাঙার চেষ্টা।) Crash type এখানে নিজস্ব taxonomy-তে লেখা (যেমন Heap-buffer-overflow READ)। Paper এগুলোকে CWE-তে map করেছে (Table 7, Dilgren et al. 2025-এর মতো)। (CWE হলো vulnerability-র ধরনের আন্তর্জাতিক তালিকা।)
- ARVO: reproducible vulnerability-র Docker environment ও PoV-এর সংগ্রহ। Agent এই base image-এ চলে।

### ২.৫ SAST এবং Semgrep

- Static Application Security Testing: code না চালিয়ে শুধু পড়ে সম্ভাব্য security issue দেখায়।
- এখানে Semgrep (v1.137.0, ci mode, community ~১.১K + Pro ~১.৩K = ২.৪K-এর বেশি rule)।
- এতে false alarm (ভুল সতর্কতা) বেশি। তাই paper "vulnerable" না বলে "suspicious" বলে।

### ২.৫ Differential testing এবং "vibe coding"

- Differential testing: দুটি program/patch একই test suite-এ চালিয়ে আচরণ তুলনা করা।
- "Vibe coding": প্রাকৃতিক ভাষার requirement দিয়ে AI agent-কে code লেখানো, মানুষ কম পর্যালোচনা করে।

## ৩. Problem

- Agent-generated code-এর security নিয়ে আগের benchmark তিন দিক থেকে অপূর্ণ (Table 1):
  - **Task form:** বেশিরভাগ function-level বা single-file। SecRepoBench repository-level, কিন্তু একটি function-এর masked region completion। (মানে function-এর একটা অংশ ঢেকে রেখে বাকিটা পূরণ করতে বলা।)
  - **Context alignment:** CWE catalog থেকে কৃত্রিম scenario, অথবা fill-in-the-middle। মানুষ যে requirement ও code version-এ vulnerability ঢুকিয়েছিল তা নেই। SusVibes fix-এর আগের commit থেকে বানায়।
  - **Evaluation:** কিছু benchmark functional correctness দেখে না। অধিকাংশ কেবল পূর্বনির্ধারিত vulnerability দেখে। agent-এর ঢোকানো নতুন ঝুঁকি ধরার উপায় নেই।
- মূল প্রশ্ন: মানুষ যেখানে vulnerability ঢুকিয়েছিল, ঠিক সেই scenario-তে agent-ও কি insecure code লেখে? মানুষের ভুলের পুনরাবৃত্তি করে, নাকি নতুন ধরনের ঝুঁকি ঢোকায়?
- VIC সাধারণত অজানা থাকে (vulnerability disclosure-এ বলা হয় না) বলে task reconstruction কঠিন।

**সহজ কথায়:** আগের পরীক্ষাগুলো হয় খুব ছোট, নয় বানানো, নয় ভুলের আসল মুহূর্ত থেকে অনেক দূরে। এই paper আসল মুহূর্তটা ফিরিয়ে আনতে চায়।

## ৪. Goal ও Research Questions

- Goal: repository-level, multi-file, real-vulnerability, introduction-aligned, functional + security (PoV + SAST) oracle-সহ benchmark বানানো এবং ৫টি code agent-কে মাপা।
- Paper আনুষ্ঠানিক "RQ১, RQ২" লেবেল দেয়নি। আমি অন্তর্নিহিত প্রশ্নগুলো এভাবে সাজালাম (আমার সংকলন):
  - প্রশ্ন ক: agent ও LLM-ভেদে correct-এবং-secure rate কত (Section 4.1, Figure 4, Table 3)?
  - প্রশ্ন খ: cost ও time-এর সাথে C-SEC-এর সম্পর্ক কী (Figure 5, 6)?
  - প্রশ্ন গ: functional failure-এর ধরন কী (Figure 7)?
  - প্রশ্ন ঘ: কোন CWE-তে agent vulnerable বা suspicious code লেখে (Figure 8, 9)?
  - প্রশ্ন ঙ: CLI agent (Claude Code, Codex) কেমন (Table 4)?
  - প্রশ্ন চ: SAST-এর false alarm কত এবং absolute বনাম relative suspicious criterion-এ পার্থক্য কী (Section 5)?

## ৫. Methodology (ধাপে ধাপে)

### ৫.১ Task formulation (Section 3.1)

1. Input: একটি repository (PVIC version) + প্রাকৃতিক ভাষার একটি requirement। Output: একটি code patch।
2. Docker-এ project environment আলাদা করা হয়। agent interactive interface পায় (code বদলানো, compile, test চালানো)। Prompt-এ agent-কে নিজে test লিখে চালাতে বলা হয়েছে (C.3)।
3. Evaluation দুই স্তর:
   - Security (i): PoV দিয়ে gold patch-এর নির্দিষ্ট vulnerability আছে কি না (vulnerable/not)।
   - Security (ii): Semgrep দিয়ে নতুন ঝুঁকি আছে কি না। থাকলে "suspicious", vulnerable বলা হয় না কারণ false alarm হতে পারে।
   - Functionality: differential testing। Repository-র test suite-এ agent patch ও gold patch-এর আচরণ কোনো test-এ ভিন্ন হলে incorrect।
4. চার outcome: IC, C-VUL, C-SUS, C-SEC (সূত্র ৬.১-এ)।

**সহজ কথায়:** agent-কে কাজ দেওয়া হয়, তারপর তার patch তিন জায়গায় পরীক্ষা হয়: "কাজ ঠিক?", "পুরনো দুর্বলতা ফিরেছে?", "নতুন সন্দেহজনক কিছু?"।

### ৫.২ Benchmark construction pipeline (Figure 2)

1. **Vulnerability data collection:** ARVO ও OSS-Fuzz থেকে ৪,৯৯৩ instance।
2. **Static analysis:** B-SZZ দিয়ে VIC candidate; ১,৬৩২ instance-এ valid candidate পাওয়া গেছে।
3. **Dynamic verification:** PoV দিয়ে তিনটি শর্ত: (i) VFC secure, (ii) candidate VIC vulnerable, (iii) candidate-এর parent secure। এতে PVIC/VIC সীমারেখা নিশ্চিত হয়। যাচাই না হওয়াগুলো বাদ; থাকল ২৫৪।
4. **Evaluation oracle acquisition:**
   - Functional: gold patch-এর পরের (VIC-version) project test suite হাতে বের করা, build ও চালিয়ে যাচাই, প্রতিটি task-এর জন্য ad hoc Python test parser লেখা। (Parser test-এর output পড়ে pass/fail বের করে।) Pre-patch version-এ অন্তত একটি test pass করতে হবে। শুধু যে test pass করেছে সেগুলোই বিবেচনায় (Appendix B)।
   - Security: ARVO-যাচাইকৃত PoV এবং Semgrep। কার্যকর oracle না থাকলে (যেমন SAST প্রযোজ্য নয়) বাদ; থাকল ২৩২।
5. **Requirement processing:** commit message, gold patch, issue description থেকে একটি LLM দিয়ে requirement লেখানো। শর্ত: স্পষ্ট ও সংক্ষিপ্ত, প্রয়োজনীয় তথ্য আছে কিন্তু implementation বলে দেওয়া নেই, security-neutral (vulnerability উল্লেখ নেই)। কোন LLM ব্যবহার হয়েছে তা paper-এ নেই।
6. **Quality assurance:** অতি জটিল instance বাদ (long-tail এড়াতে); requirement হাতে পরীক্ষা (security-neutral, gold code নেই); test parser হাতে পরীক্ষা। শেষ: **১০৫** task। Appendix B-এর একটি rejected উদাহরণে requirement-এ code block ছিল বলে বাদ।
7. Differential testing-এর যুক্তি: "test একই commit-এ থাকে" — Google code-review guidance ইত্যাদির উদ্ধৃতি। তাই VIC-এর test suite adequate ধরা হয়েছে (Appendix D)। Lower-bound যুক্তি: test fail করলে agent নিশ্চিতভাবে ভুল।

**সহজ কথায়:** ৪,৯৯৩টা থেকে ধাপে ধাপে ছেঁকে মাত্র ১০৫টা সবচেয়ে বিশ্বাসযোগ্য task রাখা হয়েছে। প্রতিটা ধাপে "ঠিক আছে কি না" আসল program চালিয়ে দেখা হয়েছে।

### ৫.৩ Agent run (Appendix C)

1. Agents: SWE-agent v1.1.0, OpenHands v0.50.0 (CodeAct, browser বন্ধ), Aider v0.86.1। Agentless ecosystem compatibility কারণে বাদ।
2. LLMs: Claude Sonnet 4.5, GPT-5, Claude 3.7 Sonnet, GPT-4.1, DeepSeek-V3.1 (671B)।
3. SWE-agent ও OpenHands: temperature 0.0 (মানে এলোমেলোভাব প্রায় নেই), সর্বোচ্চ ৭৫ iteration, cost limit 2 (একক বিবরণে ইউনিট স্পষ্ট নয়; আমি USD ধরছি)। Aider-এ iteration/cost সীমা নেই।
4. **প্রতিটি combination একবার** চালানো; official API; মোট budget আনুমানিক ৫,০০০ USD।
5. CLI agent: Claude Code (Claude Sonnet 4.5) ও Codex (GPT-5)।
6. Hardware: 2× Xeon 8480C, 2 TB RAM, 8× H100 (agent API ব্যবহার করেছে, তাই GPU-র ভূমিকা অস্পষ্ট)।

### ৫.৪ Suspicious-এর সংজ্ঞা (Section 5)

- মূল setting **absolute**: agent patch-এর পরের Semgrep ফলাফল বনাম patch-এর আগের ফলাফল; নতুন alert থাকলে suspicious।
- বিকল্প **relative**: agent patch-এর পর বনাম gold patch-এর পর।
- Absolute বেছে নেওয়ার কারণ: ঝুঁকি মানুষ আনুক বা agent, ব্যবহারকারীর কাছে একই।

**সহজ কথায়:** absolute মানে "আগে ছিল না, এখন আছে?"। relative মানে "মানুষের patch-এর চেয়ে বেশি আছে?"।

## ৬. Math

Paper-এ নিজস্ব সূত্র নেই; নিচে paper-এর metric-গুলোর আনুষ্ঠানিক রূপ (আমার সংকলন) এবং আমার হিসাব।

### ৬.১ Outcome function

ধরি $p$ একটি agent patch, $R_0$ হলো PVIC repository, $R_p$ হলো patch-এর পরের, $R_g$ হলো gold patch-এর পরের repository।

- $F(p)\in\{0,1\}$: differential testing-এ সব বিবেচিত test-এ gold-এর সাথে আচরণ একই হলে $1$।
- $V(p)\in\{0,1\}$: PoV $R_p$-তে vulnerability দেখালে $1$।
- $S(p)\in\{0,1\}$: Semgrep-এ নতুন alert থাকলে $1$।

$$O(p)=\begin{cases}\text{IC} & F(p)=0\\ \text{C-VUL} & F(p)=1 \land V(p)=1\\ \text{C-SUS} & F(p)=1 \land V(p)=0 \land S(p)=1\\ \text{C-SEC} & F(p)=1 \land V(p)=0 \land S(p)=0\end{cases}$$

- এই সূত্র একটা patch-কে চারটি খোপের একটায় ফেলে। আগে দেখা হয় কাজ ঠিক কি না। ঠিক হলে PoV দেখা হয়। PoV ঠিক থাকলে Semgrep দেখা হয়।
- লক্ষ্য করুন: $F(p)=0$ হলে $V$ ও $S$ আর বিবেচনা করা হয় না। অর্থাৎ incorrect patch-এর security অপরিমিত থাকে।

**সহজ কথায়:** আগে "কাজ হয়েছে?", তারপর "পুরনো দুর্বলতা আছে?", তারপর "নতুন সন্দেহ আছে?"। তিনটিতেই পাস করলে C-SEC।

### ৬.২ Functional correctness (differential testing)

$$F(p)=\prod_{t\in T}\mathbb{1}\left[\text{res}_p(t)=\text{res}_g(t)\right]$$

- এই সূত্র বলে: প্রতিটি test-এ agent-এর patch ও gold patch একই ফল দিলে তবেই $F(p)=1$। একটাতেও ভিন্ন হলে গুণফল ০, মানে incorrect।
- $T$: যে test case-গুলো বিবেচিত (Appendix B অনুযায়ী pre-patch-এ pass করা test; আমার পাঠ)।
- $\text{res}_p(t)$, $\text{res}_g(t)$: test $t$-তে agent patch ও gold patch-এর ফল।
- $\mathbb{1}[\cdot]$ শর্ত সত্য হলে ১, নইলে ০।
- মনে রাখুন gold patch নিজেই VIC, অর্থাৎ vulnerable। তাই oracle-এর "সঠিক আচরণ" আসলে vulnerable version-এর আচরণ (সীমাবদ্ধতা ১২-এ আলোচিত)।

**সহজ কথায়:** ১০০০টা test-এর ৯৯৯টা মিললেও একটা না মিললে patch ভুল ধরা হয়।

### ৬.৩ Suspicious (absolute বনাম relative)

$$S_{\text{abs}}(p)=\mathbb{1}\left[\exists\, a\in\mathcal{A}(R_p):\ a\notin\mathcal{A}(R_0)\right],\qquad S_{\text{rel}}(p)=\mathbb{1}\left[\exists\, a\in\mathcal{A}(R_p):\ a\notin\mathcal{A}(R_g)\right]$$

- প্রথম সূত্র দেখে: patch-এর পর এমন কোনো Semgrep alert আছে কি, যা patch-এর আগে ছিল না। দ্বিতীয় সূত্র একই কাজ করে, কিন্তু তুলনা করে gold patch-এর পরের alert-এর সাথে।
- $\mathcal{A}(R)$: repository $R$-এ Semgrep-এর alert-এর সেট।
- Paper alert কীভাবে "একই alert" হিসেবে মেলানো হয় (লাইন নম্বর বদলালে) তা বলেনি।

**সহজ কথায়:** "নতুন alert এল কি না" গোনা; পার্থক্য শুধু তুলনার ভিত্তিতে (আগের code বা gold)।

### ৬.৪ Rate এবং শর্তাধীন অনুপাত

$$r_{\text{C-SEC}}=\frac{1}{N}\sum_{i=1}^{N}\mathbb{1}\left[O(p_i)=\text{C-SEC}\right],\qquad N=105$$

$$\rho=\frac{r_{\text{C-SEC}}}{r_{\text{correct}}}=\frac{r_{\text{C-SEC}}}{1-r_{\text{IC}}}$$

- প্রথম সূত্র ১০৫টি task-এর মধ্যে কতগুলো C-SEC হয়েছে তার ভগ্নাংশ বের করে। দ্বিতীয় সূত্র বের করে, correct patch-গুলোর মধ্যে কত ভাগ secure।
- $\rho$ = correct patch-এর মধ্যে secure-এর অনুপাত (paper নিজে এটি দেয়নি, "আমার হিসাব")। এটি security-কে functional ক্ষমতা থেকে আলাদা করে দেখায়।

**সহজ কথায়:** $\rho$ বলে "যে patch-গুলো কাজ করল, তার কতটা নিরাপদ"।

### ৬.৫ Wilson confidence interval

$$\hat p=\frac{x}{n},\qquad \text{CI}=\frac{\hat p+\frac{z^2}{2n}\pm z\sqrt{\frac{\hat p(1-\hat p)}{n}+\frac{z^2}{4n^2}}}{1+\frac{z^2}{n}}$$

- এই সূত্র ছোট নমুনায় একটা সংখ্যার "সম্ভাব্য সীমা" বের করে। যেমন ২৫/১০৫ = ২৩.৮% দেখলে বোঝা যায় আসল মান ঠিক কতটা ওপরে-নিচে হতে পারে।
- $x$: সফল task-সংখ্যা, $n=105$, $z=1.96$ (৯৫%)। Paper নিজে কোনো CI দেয়নি; "আমার হিসাব"।

**সহজ কথায়:** একটা সংখ্যার সাথে "প্লাস-মাইনাস কত" বলে দেওয়া।

### ৬.৬ Pipeline yield

$$y_k=\frac{n_k}{n_{k-1}}$$

- এই সূত্র বলে: প্রতিটি ধাপে আগের সংখ্যার কত ভাগ টিকে গেল।
- $n_k$: $k$-তম ধাপের পরে instance সংখ্যা।

### ৬.৭ Worked example (paper-এর আসল সংখ্যা)

**(ক) SWE-agent + Sonnet 4.5 (Figure 4)**

- IC ৫৩.৩%, C-VUL ২১.০%, C-SUS ১.৯%, C-SEC ২৩.৮%। যোগফল ৫৩.৩+২১.০+১.৯+২৩.৮ = ১০০.০%।
- ১০৫ task-এ (আমার হিসাব): IC ৫৬, C-VUL ২২, C-SUS ২, C-SEC ২৫; ৫৬+২২+২+২৫=১০৫ ✓।
- Correct = ১০০−৫৩.৩ = ৪৬.৭% (৪৯ task)। $\rho = 25/49 = 51.0\%$। অর্থাৎ correct patch-এর ৪৯.০% secure নয় (vulnerable বা suspicious)।
- Wilson CI (আমার হিসাব): $\hat p = 25/105 = 0.2381$; $z^2=3.8416$; হর $=1+3.8416/105=1.0366$; কেন্দ্র $=(0.2381+0.0184)/1.0366=0.2473$; অর্ধ-প্রস্থ $=1.96\times\sqrt{0.0017277+0.0000871}/1.0366=0.0806$। ৯৫% CI ≈ **১৬.৭% থেকে ৩২.৮%**।
- ফলে ১৭.১% (১৮ task) বা ১৯.০% (২০ task) এবং ২৩.৮% (২৫ task)-এর পার্থক্য ২ থেকে ৭ task মাত্র; এই CI-তে ওভারল্যাপ বিশাল।

**সহজ কথায়:** ২৩.৮% শুনতে আলাদা লাগলেও ১৬.৭% থেকে ৩২.৮% পর্যন্ত যেকোনো মান হতে পারে। তাই কাছাকাছি র‍্যাঙ্কের agent-দের আলাদা বলা যায় না।

**(খ) OpenHands + Sonnet 4.5**

- IC ৫৬.২%, C-VUL ২১.৯%, C-SUS ২.৯%, C-SEC ১৯.০% (যোগফল ১০০.০%); ১০৫ task-এ ৫৯, ২৩, ৩, ২০ (যোগফল ১০৫ ✓)।
- Correct ৪৩.৮%; $\rho = 19.0/43.8 = 43.4\%$।

**(গ) Pipeline yield (আমার হিসাব)**

- $y$: ১,৬৩২/৪,৯৯৩ = ৩২.৭%; ২৫৪/১,৬৩২ = ১৫.৬%; ২৩২/২৫৪ = ৯১.৩%; ১০৫/২৩২ = ৪৫.৩%; সামগ্রিক ১০৫/৪,৯৯৩ = ২.১%।
- সবচেয়ে বড় ক্ষতি dynamic verification-এ (১৫.৬% টিকে আছে)।

**(ঘ) Cost per success (আমার হিসাব, আনুমানিক)**

- Figure 5-এর গড় cost ০.৮৫ USD (প্রতি task ধরে) এবং গড় C-SEC ১১.৬২%। ফলে একটি C-SEC patch পেতে গড়ে ≈ ০.৮৫/০.১১৬২ ≈ ৭.৩ USD। Paper-এ cost-এর একক স্পষ্ট নয়, তাই এটি অনুমান।

## ৭. Setup

| বিষয় | মান |
|---|---|
| Tasks | ১০৫ (৪১ project, ৯ domain) |
| গড় requirement | ২০০.১ word (সর্বোচ্চ ৪০৮) |
| গড় code base | ২,৮৪৫.৩ file; ৫,৫৪,৭১৮.৮ LOC (সর্বোচ্চ ৩৬,৩৮৮ file; ৪২,৪৮,০৬৯ LOC) |
| Gold patch | গড় ১.৯ file (সর্বোচ্চ ৫); গড় ৪২.৫ LOC (সর্বোচ্চ ১৪৮) |
| Functional test | গড় ৪৩৪.৩ case (সর্বোচ্চ ৫,৪২০) |
| তুলনা | SWE-bench: ৩২.৮ LOC, ১.৭ file; SEC-Bench: ১৭.৩ LOC, ১.৩ file |
| Severity | ৭৫%-এর বেশি vulnerability "medium" বা "high" |
| বৃহত্তম project | harfbuzz ১৬ task (১৫.২%); mruby, OpenSC, libredwg ৭টি করে (৬.৭%); wireshark, nDPI ৬টি করে (৫.৭%) |
| CWE ভিত্তি | CWE-122 প্রায় ৪৬.৭%; CWE-120 ৬.৭% |
| Scaffolds | SWE-agent 1.1.0, OpenHands 0.50.0, Aider 0.86.1 |
| LLMs | Claude Sonnet 4.5, GPT-5, Claude 3.7 Sonnet, GPT-4.1, DeepSeek-V3.1 |
| CLI agents | Claude Code (Sonnet 4.5), Codex (GPT-5) |
| Run | প্রতি combination ১ বার; temperature 0.0 |
| সীমা | ৭৫ iteration; cost limit 2; Aider-এ নেই |
| SAST | Semgrep 1.137.0, ci mode, ২.৪K+ rule, Sep 2025 |
| Budget | আনুমানিক ৫,০০০ USD |

**সহজ কথায়:** প্রতিটা task একটা বিশাল project (গড়ে প্রায় ৫.৫ লাখ লাইন), কিন্তু ঠিক করার patch ছোট (গড়ে ৪২ লাইন, ২টা file)। মানে agent-কে বড় খড়ের গাদায় ছোট সুচ খুঁজতে হয়।

## ৮. Results

### ৮.১ প্রধান ফল (Figure 4; পাঠযোগ্য ছয়টি সারি)

Figure 4 PDF থেকে আংশিক বিকৃত বেরিয়েছে। নিচে কেবল সেই সারিগুলো যেগুলোর সব চার সংখ্যা পড়া গেছে এবং যোগফল ১০০% (±০.১) মেলে।

| Combination | C-SEC | C-SUS | C-VUL | IC |
|---|---|---|---|---|
| SWE-agent + Sonnet 4.5 | ২৩.৮% | ১.৯% | ২১.০% | ৫৩.৩% |
| OpenHands + Sonnet 4.5 | ১৯.০% | ২.৯% | ২১.৯% | ৫৬.২% |
| SWE-agent + GPT-5 | ১৭.১% | ৪.৮% | ১৫.২% | ৬২.৯% |
| OpenHands + GPT-5 | ১৭.১% | ১.৯% | ১৭.১% | ৬৩.৮% |
| SWE-agent + DeepSeek-V3.1 | ১৫.২% | ১০.৫% | ১৬.২% | ৫৮.১% |
| OpenHands + DeepSeek-V3.1 | ১৪.৩% | ৭.৬% | ২১.০% | ৫৭.১% |

- বাকি ৯টি combination-এর সংখ্যা বিকৃত লেখায় নিশ্চিতভাবে পুনরুদ্ধার করা যায়নি। তাদের C-SEC সর্বনিম্ন ≈ ৩.৮% (Figure 4-এর পাঠযোগ্য সর্বনিম্ন মান)। Paper-এর Table 3 গড় নিচে।

**সহজ কথায়:** সবচেয়ে ভালো agent-এরও অর্ধেকের বেশি patch ভুল (IC), আর যেগুলো ঠিক, তার প্রায় অর্ধেকে vulnerability আছে।

### ৮.২ Table 3: গড় C-SEC (%)

| গোষ্ঠী | SWE | OH | AD | C4.5 | DS | G5 | C3.7 | G4.1 | Avg |
|---|---|---|---|---|---|---|---|---|---|
| C-SEC | ১৪.৩ | ১৩.৯ | ৬.৭ | ১৭.১ | ১৪.৩ | ১৩.৩ | ৭.৩ | ৬.০ | ১১.৬ |

- আমার যাচাই: (১৪.৩+১৩.৯+৬.৭)/৩ = ১১.৬৩; (১৭.১+১৪.৩+১৩.৩+৭.৩+৬.০)/৫ = ১১.৬ ✓।

**সহজ কথায়:** scaffold-এর মধ্যে SWE-agent ও OpenHands প্রায় সমান, Aider অনেক পিছনে। model-এর মধ্যে Claude Sonnet 4.5 সামনে।

### ৮.৩ Cost ও time (Figure 5, 6)

| বিষয় | মান |
|---|---|
| গড় cost | ০.৮৫ (ইউনিট চিত্রে স্পষ্ট নয়) |
| গড় C-SEC | ১১.৬২% |
| গড় time | ৫২০.৯০ s |
| DeepSeek-supported agent | ঊর্ধ্ব-বাম অঞ্চলে: কম cost, ভালো C-SEC |
| SWE-C4.5 ও OH-C4.5 | সেরা C-SEC, কিন্তু cost অনেক বেশি (OH-C4.5-এর অন্তত) |
| G5 | গড় cost-এ ভালো C-SEC |
| AD-C4.5 | cost বেশি, C-SEC গড়ের নিচে |

- সিদ্ধান্ত: scaffold design model-এর মতোই গুরুত্বপূর্ণ (একই C4.5 বিভিন্ন scaffold-এ ভিন্ন cost-effectiveness)। SWE-C4.5 সেরা C-SEC পায় গড়ের সামান্য উপরের সময়ে।

**সহজ কথায়:** বেশি টাকা খরচ করলেই ভালো ফল হয় না। সস্তা DeepSeek-ও কিছু ক্ষেত্রে দামি model-এর কাছাকাছি।

### ৮.৪ Functional analysis

- SWE-C4.5 সর্বোচ্চ functional correctness: ১০০−৫৩.৩ = ৪৬.৭%।
- Claude 3.7 vs DeepSeek: OH-3.7 ও SWE-C3.7 correct ৩৯% ও ৪১.৯%, SWE-DS ও OH-DS ৪১.৯% ও ৪২.৯%। কিন্তু secure অংশ ≈ ৯% বনাম ≈ ১৪%। অর্থাৎ ক্ষমতা সমান, security আলাদা।
- Failure mode (Figure 7), আমার পাঠে (বিকৃত লেখা):

| Agent | TF (test failure) | CE (compile error) | NO (no output) | মোট failure |
|---|---|---|---|---|
| SWE-agent | ৪৩.৭% | ৪০.৯% | ১৫.৪% | ৬০.৬% (paper) |
| OpenHands | ৪৩.১% | ৩৯.১% | ১৭.৭% | ৬২.৩% (paper) |
| Aider | ১৩.৪% | ১৫.০% | ৭১.৬% | paper-এ নেই |

- Aider-এর NO বেশি কারণ একসাথে অনেক file load করে context window (Sonnet 4.5-এর জন্য 200K token) ছাড়িয়ে যায়। (Context window হলো model একবারে যত লেখা মনে রাখতে পারে।) Appendix E.1 case: task 58663-তে input ≈ ১৮০,১৫৬ token (80K থেকে বেড়ে) এবং output ≈ ০।

**সহজ কথায়:** SWE-agent ও OpenHands প্রধানত test fail বা compile error-এ আটকায়। Aider আটকায় কারণ সে একসাথে এত file পড়ে যে মাথা "ভরে" যায় এবং কিছুই লেখে না।

### ৮.৫ Security analysis

- CWE-122 dataset-এ ৪৬.৭% কিন্তু এর ≈ ১০% output C-VUL। CWE-120 মাত্র ৬.৭% কিন্তু C-VUL ≈ ৩৩% (Figure 8)। অর্থাৎ dataset-এ প্রচলিত ধরন ≠ agent-এর বেশি ঘটানো ধরন।
- Scaffold-ভেদে ধরন ভিন্ন: CWE-475-এ SWE বেশি insecure, CWE-122-এ OH বেশি।
- Suspicious: মোট ২৯২ case, ১৬টি CWE; ৭১.৬% memory-সংক্রান্ত। শীর্ষ চারটি CWE-415/416/14/120। মূল dataset-এর ১১ CWE-র তুলনায় ১৬টি; নতুন: CWE-14, CWE-319 ইত্যাদি।

**সহজ কথায়:** মানুষ যে ধরনের ভুল বেশি করে, agent সেই ধরনের ভুলই বেশি করে এমন নয়। agent কিছু নতুন ধরনের ভুলও করে।

### ৮.৬ Table 4: CLI agent

| Agent | C-SEC | C-SUS | C-VUL | IC | Correct |
|---|---|---|---|---|---|
| Codex (GPT-5) | ১৯.০% | ৫.৭% | ২১.৮% | ৫৩.৩% | ৪৬.৭% |
| Claude Code (Sonnet 4.5) | ১৭.১% | ৪.৮% | ২৬.৭% | ৫১.৪% | ৪৮.৬% |

- সারি-ক্রম টেক্সট থেকে আমার নির্ধারণ: লেখায় "Claude Code ও Codex functionality-তে ১ম ও ২য় (৪৮.৬% ও ৪৬.৭%)" আছে, তাই IC ৫১.৪ = Claude Code।
- আমার হিসাব: $\rho$ Claude Code = ১৭.১/৪৮.৬ = ৩৫.২%; Codex = ১৯.০/৪৬.৭ = ৪০.৭%। সবচেয়ে বেশি vulnerable (C-VUL ২৬.৭%) Claude Code।
- Codex-এর C-SEC ১৯.০% OH-GPT-5-এর (১৭.১%) চেয়ে বেশি, OH-C4.5-এর সমান। তাই scaffold-সুবিধা আছে।

**সহজ কথায়:** Claude Code সবচেয়ে বেশি test পাস করায়, কিন্তু তার ঠিক-patch-এর মধ্যে নিরাপদের অনুপাত কম (৩৫%)।

### ৮.৭ SAST false alarm ও criterion (Section 5)

| বিষয় | মান |
|---|---|
| নমুনা | প্রতি agent থেকে ৪০টি flagged snippet; মোট ১২০টি (হাতে শ্রেণিবদ্ধ) |
| সত্যিই vulnerable | ১১.৪% |
| risky (বিশেষ শর্তে ঝুঁকি) | ৩৯.০% |
| non-vulnerable | ৪৯.৬% |
| অর্থ | false alarm ≈ ৫০% |
| Absolute C-SUS | ৪.৯% |
| Relative C-SUS | ≈ ২.৬% |
| মানুষ-যুক্ত অংশ | ২.৩% (gold patch-ও নতুন alert আনে) |
| Top-5 absolute | CWE-415/416/14/120/319 |
| Top-5 relative | CWE-319/415/416/14/676 |

**সহজ কথায়:** Semgrep যা "সন্দেহজনক" বলে, তার প্রায় অর্ধেক আসলে ঝুঁকিহীন। তাই C-SUS একটা সতর্কসংকেত, চূড়ান্ত প্রমাণ নয়।

## ৯. Key findings

1. **Correct ও secure দুটি আলাদা জিনিস।** সেরা agent-ও ২৩.৮%; ১৫ combination-এর গড় ১১.৬২%; correct patch-এর বড় অংশে (SWE-C4.5-এ ৪৯%, OH-C4.5-এ ৫৬.৬%) vulnerability বা suspicion।
2. **Security ও functionality মোটামুটি positively correlated, কিন্তু আলাদা হতে পারে।** Claude 3.7 vs DeepSeek: সমান correctness, ≈ ৯% বনাম ≈ ১৪% C-SEC।
3. **Scaffold মডেলের মতো গুরুত্বপূর্ণ।** SWE ১৪.৩, OH ১৩.৯, AD ৬.৭ (গড়); Aider context overflow-এ ৭১.৬% NO।
4. **CLI agent functional-এ সেরা, security-তে নয়।** Claude Code correct ৪৮.৬% (সর্বোচ্চ) কিন্তু C-SEC ১৭.১%। Paper-এর ব্যাখ্যা: প্রতিষ্ঠিত scaffold security-কে কম গুরুত্ব দেয় (অনুমান; paper পরীক্ষা করেনি)।
5. **Agent-এর ঝুঁকির বণ্টন মানুষ থেকে আলাদা।** ১৬ CWE বনাম ১১; absolute ও relative top-5 তালিকা আলাদা; ৭১.৬% suspicious memory-সংক্রান্ত।
6. **SAST-এ ≈ ৫০% false alarm,** তাই C-SUS শক্ত প্রমাণ নয়, কেবল "অনুসন্ধানযোগ্য" ঝুঁকি।
7. **Cost বেশি মানেই ভালো নয়।** DeepSeek-supported combination কম cost-এ গড়ের উপরে; AD-C4.5 বেশি cost-এ গড়ের নিচে।
8. **Prevalence ≠ agent-vulnerability:** CWE-122 (৪৬.৭%) → ১০%; CWE-120 (৬.৭%) → ৩৩%।

**সহজ কথায়:** মূল বার্তা একটাই: "test পাস" মানে "নিরাপদ" নয়। সবকিছু এই কথাটাকেই নানা দিক থেকে দেখায়।

## ১০. Alternative-এর চেয়ে কেন ভালো (paper-এর দাবি ও আমার মূল্যায়ন)

| দিক | আগের benchmark | SecureVibeBench | আমার মূল্যায়ন |
|---|---|---|---|
| Task form | function-level / single file / FIM | repository-level, multi-file (গড় ১.৯ file) | সত্যিকারের উন্নতি; তবে ১.৯ file এখনো ছোট |
| Context | CWE catalog থেকে কৃত্রিম বা fix-এর আগের commit (SusVibes) | VIC-aligned (PVIC + requirement) | যুক্তিসঙ্গত; কিন্তু requirement LLM-লেখা, তাই আসল developer-intent নয় |
| Functional oracle | অনেকে নেই | differential testing, গড় ৪৩৪ test | ভালো; তবে gold নিজেই vulnerable (সীমাবদ্ধতা) |
| New-risk detection | নেই | Semgrep (suspicious) | দিক ঠিক; ≈ ৫০% false alarm |
| Real vulnerability | কিছুতে নেই | OSS-Fuzz/ARVO, PoV-যাচাইকৃত | শক্তিশালী, ভাষা শুধু C/C++ |

- Paper দাবি করছে এটি প্রথম repository-level, multi-file secure code generation benchmark। এটি সম্পূর্ণ তুলনামূলক দাবি; SusVibes-কে concurrent বলা হয়েছে এবং দুটোই multi-file।
- SusVibes-এর তুলনায় paper-এর যুক্তি (i) real introduction point, (ii) SAST দিয়ে নতুন ঝুঁকি। আমরা সংখ্যা সরাসরি তুলনা করতে পারি না (ভাষা, oracle, metric আলাদা; ২১ নম্বর অংশ দেখো)।

**সহজ কথায়:** এটা আগের benchmark-এর চেয়ে আসল জীবনের কাছাকাছি, কিন্তু নিজেরও কিছু দুর্বলতা আছে (gold-নির্ভর oracle, শুধু C/C++)।

## ১১. কখন কাজ করে / ব্যর্থ হয়

- **ভালো কাজ করে:** SWE-agent ও OpenHands-এর মতো যেগুলো file ধাপে ধাপে পড়ে এবং command ও সিদ্ধান্ত interleave করে (paper-এর ব্যাখ্যা, Section 4.2)।
- **ব্যর্থ:**
  - Aider: একসাথে বেশি file যোগ করে context exhaust (NO ৭১.৬%)।
  - CE ও TF প্রায় সমান (~৪০:৪০): compile error এই C/C++ বড় repository-তে সাধারণ।
  - বিশেষ CWE (যেমন CWE-120) agent-এর বেশি ভুল।
- **Paper-এর ব্যাখ্যা (Appendix D, পরীক্ষিত নয়):**
  - (i) training data-তে vulnerable GitHub code আছে।
  - (ii) vulnerability data কম (NVD ≈ ১৫০-২০০K)।
  - (iii) scaffold-এ security tool বা prompt নেই (যেমন OpenHands)।

## ১২. Limitations

### ১২.১ Authors-এর স্বীকৃত

- শুধু memory-related C/C++ (OSS-Fuzz, ARVO); অন্য vulnerability ও ভাষার bias।
- ১০৫ task, statistical instability সম্ভব।
- Semgrep একটি tool; false alarm আছে। একাধিক SAST ensemble করলে noise বাড়তে পারে। ভবিষ্যতে symbolic execution বা LLM-as-a-judge।
- Contamination (আগে থেকে model-এর training data-তে উত্তর থাকা): CyberGym ও SEC-bench-এ cutoff-এর আগে-পরে পার্থক্য নেই বলে অনুমান করা; requirement synthesized; কাজ জটিল বলে memorization কম সাহায্য করবে।

### ১২.২ আমার পর্যবেক্ষণ

1. **Gold patch-ই vulnerable।**
   - Functional oracle gold = VIC-এর আচরণ, যার PoV-তে crash হয়।
   - যে secure patch আচরণ বদলায় (যেমন input reject) সেটি test-এ fail করতে পারে।
   - পুরো oracle "মানুষের vulnerable সমাধানের নকল" পুরস্কৃত করে। Paper-এ এর বিশ্লেষণ নেই।
2. **একক run, temperature 0.0।**
   - Sub-domain 3-এর Engineering Reliable Coding Agents ও SWE-rebench-এর run-to-run variance (CG4) এখানে অপরিমিত।
   - ১ task = ০.৯৫২ pp; ২৩.৮% বনাম ১৯.০% মাত্র ৫ task-এর পার্থক্য; Wilson CI ১৬.৭-৩২.৮%।
3. **Security কেবল correct patch-এর ওপর মাপা।** IC patch vulnerable কি না জানা নেই; তাই "secure" দাবিটি শর্তাধীন।
4. **PoV নির্দিষ্ট একটি vulnerability-র জন্য।**
   - PoV পাস মানেই secure নয়, কেবল এই crash নেই (Sub-domain 2-এর VRpilot-এর "sanitizer pass ≠ secure" দেখো)।
   - Agent crash আটকাতে বিপজ্জনক fallback লিখলে ধরা না-ও পড়তে পারে।
5. **Leakage-এর নিজস্ব পরীক্ষা নেই।**
   - Paper Appendix D-তে অন্যান্য benchmark-এর প্রমাণ উল্লেখ করেছে; নিজের tasks-এ কোনো pre/post knowledge-cutoff ভাগ নেই।
   - এছাড়া agent-এর container-এ git history (VFC পর্যন্ত) আছে কি না লেখা নেই।
   - Context.md-এ SWE-Bench Pro Verified-এ .git/network leakage-এ GLM-5.2 ৭৮.৮০% → ৫৭.৩২% (I) পাওয়া যায়; এখানে সমতুল্য পরীক্ষা অনুপস্থিত।
6. **Requirement LLM-লেখা:** কোন LLM, কত task বাদ গেল (২৩২ → ১০৫ এর কত requirement-এর জন্য) বলা নেই। "Security-neutral" ইচ্ছাকৃতভাবে সহজ করে; বাস্তবে developer প্রায়ই security hint পান।
7. **আন্তঃ-paper অসঙ্গতি:**
   - (ক) Abstract-এ "5 popular code agents"; Section 4-এ ৩ agent + ২ CLI = ৫ ঠিক, কিন্তু Introduction-এ "three representative code agents"।
   - (খ) Appendix D-তে "সেরা baseline ৪০% functional correctness" বলা আছে, অথচ SWE-C4.5 ৪৬.৭% এবং Claude Code ৪৮.৬%।
   - (গ) SAST নমুনা ১২০টির শতাংশ (১১.৪, ৩৯.০, ৪৯.৬) পূর্ণসংখ্যা count দেয় না (১১.৪% × ১২০ = ১৩.৬৮)।
   - (ঘ) ২৯২ suspicious case বনাম ৪.৯% C-SUS rate: ১৫×১০৫ = ১,৫৭৫ patch-এর ৪.৯% ≈ ৭৭, তাই ২৯২ সম্ভবত incorrect patch-সহ সব patch ধরে গোনা; paper-এ স্পষ্ট নয়।
   - (ঙ) Table 3 G5 = ১৩.৩ কিন্তু লেখা "DS ও G5 ≈ ১৪%"।
   - (চ) Budget আনুমানিক ৫,০০০ USD বনাম Figure 5 গড় ০.৮৫ × ১,৫৭৫ ≈ ১,৩৩৯ (আমার হিসাব; হয়তো retry/অন্য run)।
8. Figure 4, 7, 8, 9 PDF থেকে আংশিক বিকৃত; সব combination-এর সংখ্যা নিশ্চিত করা যায়নি।

**সহজ কথায়:** সবচেয়ে বড় দুর্বলতা হলো oracle নিজেই vulnerable gold-এর ওপর দাঁড়িয়ে, আর প্রতিটি ফল মাত্র একবারের।

## ১৩. Research gaps

| G-id | Gap | Evidence | Related CG / our folder |
|---|---|---|---|
| G1 | Functional oracle gold-এর vulnerable আচরণে নোঙর করা | Gold = VIC; differential testing (Section 3.1, App. D) | CG5, CG13 / Security |
| G2 | Security verdict কেবল correct patch-এ; incorrect patch-এর security অপরিমিত | Outcome সংজ্ঞা (Section 3.1) | CG5, CG1 / Security |
| G3 | PoV একটি vulnerability-র জন্য; নতুন ঝুঁকির জন্য Semgrep ≈ ৫০% false alarm | Section 5: ১১.৪/৩৯.০/৪৯.৬% | CG5, CG17 / Security |
| G4 | একক run, ১০৫ task; CI ও paired test নেই | App. C.2, Limitations | CG4, CG8 / Evaluation |
| G5 | Contamination/leakage-এর নিজস্ব পরীক্ষা নেই; git history/PoV exposure অনিশ্চিত | App. D যুক্তি অন্য benchmark-নির্ভর | CG6, CG12 / Evaluation |
| G6 | Requirement LLM-লেখা ও security-neutral; বাস্তব prompt-এর পরিবর্তন নেই | Section 3.2 | CG6, CG7 / Security |
| G7 | Scaffold-এ security hook/SAST tool ছাড়া মাপা; হস্তক্ষেপ-পরীক্ষা নেই | App. D (কারণ অনুমান) | CG5, CG2 / Agents |
| G8 | শুধু C/C++ memory-safety; Python/Java/web নয় | Limitations | CG9 / Security |
| G9 | Judge/LLM-ভিত্তিক security signal অ-যাচাইকৃত | Limitations-এ শুধু ভবিষ্যৎ কাজ | CG17, CG18 / Patch Validation |

**সহজ কথায়:** gap-গুলো তিন ভাগে ফেলা যায়: oracle-এর গুণমান (G1-G3), পরিসংখ্যানের দুর্বলতা ও leakage (G4-G5), আর কভারেজ (G6-G9)।

## ১৪. Improvement ideas

1. **Oracle-কে gold থেকে আলাদা করা:** PoV-ছাড়াও regression test-এ gold-এর "অনিরাপদ আচরণ"-এ আটকে না থেকে কেবল requirement-সম্পর্কিত test-এ নোঙর; বা সেই test বাদ যেগুলো gold-এর vulnerable path ব্যায়াম করে।
2. **Security-কে সব patch-এ মাপা:** IC patch-এও PoV ও SAST চালিয়ে "security given incorrect" report করা।
3. **Multi-run:** প্রতি task ৩-৫ run; pass@k ও pass^k-এর C-SEC সংস্করণ; McNemar paired test (CG4, CG8)।
4. **Leakage check:** .git history ছাঁটা বনাম পূর্ণ; knowledge cutoff-এর আগে-পরের commit-এ ভাগ; PoV file container-এ আছে কি না লগ।
5. **SAST triage:** Semgrep alert-কে LLM বা symbolic execution দিয়ে filter; paper-এর নিজের ভবিষ্যৎ নির্দেশ।
6. **Security-aware scaffold:** SWE-agent/OpenHands-এ sanitizer ও SAST tool যোগ করা এবং prompt-এ security নির্দেশ; আগে-পরে C-SEC তুলনা।
7. **Rubric-ভিত্তিক security judge (Sub-domain 5-এর HITL LLM-as-a-Judge)** দিয়ে PoV-না-থাকা ক্ষেত্রের জন্য আরেকটি signal।

## ১৫. Publication potential (SPL3-feasible)

- **সম্ভাব্য contribution:** "Security signal reliability" — SecureVibeBench-এর oracle কতটা বিশ্বাসযোগ্য তা পুনর্বিশ্লেষণ: (ক) gold-anchoring প্রভাব, (খ) run-to-run variance, (গ) SAST false-alarm-এর পরিমাণ।
- **সম্ভাব্য venue:** workshop বা short paper (MSR/LLM4Code/AIware-ধরনের)। Venue নাম নিশ্চিত নয়; এগুলো আমার অনুমান।
- **SPL3-feasible:** পূর্ণ benchmark বানানো অসম্ভব। কিন্তু repository-তে প্রকাশিত ১০৫ task-এর একটি ছোট উপসেট (যেমন ২০-৩০) নিয়ে ছোট পুনরাবৃত্তি সম্ভব, যদি Docker ও API-খরচ সামলানো যায়।
- **ঝুঁকি:** ARVO image বড়; agent run ব্যয়বহুল (paper-এর মোট ≈ ৫,০০০ USD বাজেট)।

## ১৬. SPL3 implementation

1. **Evaluator (agent-free):** paper-এর release থেকে ১০-২০ task ও ARVO Docker নিয়ে একটি "patch-security-checker" তৈরি। Input = patch, output = (functional, PoV, Semgrep-delta) ত্রয়ী। Agent ছাড়াই আগে gold ও কয়েকটি হাতে লেখা patch দিয়ে যাচাই।
2. **ছোট agent run:** mini-SWE-agent বা SWE-agent + একটি সস্তা model; প্রতি task ৩ run; cost limit রেখে।
3. **Assurance report-এর security অংশ:** চারটি আলাদা সংকেত, এক স্কোরে যোগ না করে:
   - functional regression (differential)
   - PoV/sanitizer (যেখানে আছে)
   - SAST delta (absolute) + "relative to gold" তুলনা
   - ফলাফল: C-SEC / C-SUS / C-VUL / IC এবং "could not verify" (নতুন বিভাগ: PoV বা test পাওয়া যায়নি)
4. **Metric:** C-SEC rate, $\rho$ (secure-given-correct), Wilson CI, ও run-ভিত্তিক pass^k।
5. **Leakage গার্ড:** container-এ .git/future commit ও PoV-এর উপস্থিতি পরীক্ষা (Context.md-এর leakage তথ্য অনুযায়ী)।
6. **Error analysis:** প্রতিটি C-SUS-এর জন্য নমুনা হাতে triage; ≈ ৫০% false alarm এখানে প্রতিলিপি করা যায় কি না দেখা।

**সহজ কথায়:** আগে agent ছাড়া শুধু patch যাচাইয়ের যন্ত্র বানাও। তারপর ছোট করে agent চালাও, আর ফল সবসময় আলাদা আলাদা signal হিসেবে দেখাও।

## ১৭. Influence / আগের sub-domain-এর সাথে যোগসূত্র

| আগের sub-domain | যোগসূত্র |
|---|---|
| ১ AI Coding Agents | SWE-agent ও OpenHands ঠিক সেই scaffold; Agentless এখানে বাদ। AutoCodeRover-এর "plausible ≠ correct" এখানে "correct ≠ secure" |
| ২ APR | VRpilot: sanitizer pass ≠ secure; PoV-ও একই সীমাবদ্ধ; RePaCA-র overfitting ধারণা: gold-নির্ভর oracle |
| ৩ Evaluation | SWE-rebench/Pro: একক run, contamination, leakage; এখানে কোনো fresh-split নেই |
| ৪ Test generation | Agent নিজে test লেখে (C.3); oracle strength (CG13)। Distinguishing test (CG14) secure বনাম vulnerable patch আলাদা করতে কাজে লাগতে পারে |
| ৫ Patch Validation | LLM-as-a-judge ও classifier: security-র জন্য তৃতীয় signal; judge-এর error direction (CG17) |

- SusVibes-এর সাথে তুলনা: ২১ নম্বর অংশ দেখো।

## ১৮. Supervisor Q&A

1. **প্রশ্ন:** C-SEC ২৩.৮% মানে কী? **উত্তর:** ১০৫-এর মধ্যে ২৫টি task-এ patch functionally gold-এর মতো, এবং PoV-তে সেই vulnerability নেই এবং Semgrep-এ নতুন alert নেই। ৯৫% Wilson CI ≈ ১৬.৭-৩২.৮% (আমার হিসাব)।
2. **প্রশ্ন:** SusVibes-এর সাথে পার্থক্য? **উত্তর:** Paper-এর মতে SusVibes fix-এর আগের commit থেকে task বানায়, আসল introduction-এর আগের নয়; আর নতুন ঝুঁকির জন্য SAST নেই। SecureVibeBench VIC-কে B-SZZ + PoV দিয়ে চিহ্নিত করে।
3. **প্রশ্ন:** Gold patch vulnerable হলে functional oracle কি ন্যায্য? **উত্তর:** না পুরোপুরি; test suite VIC-সংস্করণের, যার আচরণে vulnerability আছে। Paper এটি স্বীকার করেনি। এটি আমাদের G1।
4. **প্রশ্ন:** Semgrep-এর ফল কতটা নির্ভরযোগ্য? **উত্তর:** ১২০টি নমুনার হাতে বিচারে ১১.৪% vulnerable, ৩৯.০% risky, ৪৯.৬% non-vulnerable। তাই C-SUS = "সন্দেহ", প্রমাণ নয়।
5. **প্রশ্ন:** Contamination কেন সমস্যা নয় বলা হলো? **উত্তর:** Paper অন্য দুই benchmark (CyberGym, SEC-bench)-এর cutoff-পূর্ব/পরবর্তী পার্থক্য-না-থাকা এবং synthesized requirement উল্লেখ করেছে; নিজস্ব পরীক্ষা নেই। আমাদের CG6।
6. **প্রশ্ন:** একক run কি সমস্যা? **উত্তর:** হ্যাঁ; ১ task = ০.৯৫২ pp; Context-এর SWE-rebench pass@1 বনাম pass@5-এর ১২-১৮ pt পার্থক্য (I) বিবেচনায় র‍্যাঙ্কিং দুর্বল।
7. **প্রশ্ন:** আমাদের assurance report-এ এর ভূমিকা? **উত্তর:** Security-কে আলাদা, লেবেলযুক্ত signal হিসেবে (functional/PoV/SAST-delta) রাখা এবং "could not verify"; কোনো একক weighted score নয়।
8. **প্রশ্ন:** Claude Code সেরা functional হলেও C-SEC কম কেন? **উত্তর:** C-VUL ২৬.৭% (সর্বোচ্চ); paper-এর অনুমান scaffold-গুলো security কম গুরুত্ব দেয়; পরীক্ষিত নয়।

## ১৯. Glossary

| Term | অর্থ |
|---|---|
| VIC / PVIC / VFC | vulnerability introducing / parent / fixing commit |
| PoV | proof-of-vulnerability, নির্দিষ্ট vulnerability নিশ্চিতকারী input/program |
| SAST | static application security testing |
| C-SEC / C-SUS / C-VUL / IC | correct+secure / correct+suspicious / correct+vulnerable / incorrect |
| B-SZZ | basic SZZ, blame-ভিত্তিক bug-inducing commit খোঁজা |
| Differential testing | দুই সংস্করণের আচরণ একই test-এ তুলনা |
| ARVO / OSS-Fuzz | reproducible vulnerability atlas / continuous fuzzing |
| TF / CE / NO | test failure / compile error / no output |
| Wilson CI | ছোট নমুনায় অনুপাতের confidence interval |

## ২০. Summary card

- **কী:** C/C++ repository-level secure-coding benchmark, ১০৫ task, ৪১ project, VIC-aligned।
- **কীভাবে:** ৪,৯৯৩ → ১,৬৩২ (B-SZZ) → ২৫৪ (PoV) → ২৩২ (oracle) → ১০৫ (QA)।
- **Oracle:** differential functional test + PoV + Semgrep delta।
- **ফল:** সেরা C-SEC ২৩.৮% (SWE-agent + Sonnet 4.5); গড় ১১.৬২%; Claude Code C-SEC ১৭.১%, Codex ১৯.০%।
- **সীমা:** একক run, ১০৫ task, gold-anchored oracle, ≈ ৫০% SAST false alarm, নিজস্ব leakage পরীক্ষা নেই।
- **আমাদের জন্য:** CG5-এর সবচেয়ে সরাসরি agent-level প্রমাণ; security আলাদা signal।
- **নতুন gap:** CG20 (gold-anchored functional oracle), CG21 (security verdict শুধু correct patch-এ ও অসম্পূর্ণ oracle coverage)।

## ২১. বর্তমান (2026) প্রেক্ষাপট

Context.md-এর 2026 তথ্য (V = vendor, I = independent) ব্যবহার করা হয়েছে; অন্য কোনো বর্তমান-model তথ্য যোগ করিনি।

### ২১.১ তখন বনাম এখন

| বিষয় | Paper-এর সময় (Sonnet 4.5, GPT-5 ইত্যাদি) | বর্তমান (context.md থেকে) |
|---|---|---|
| সেরা model | Claude Sonnet 4.5 (SWE-agent-এ C-SEC ২৩.৮%) | Claude Opus 5.5 (২০২৬-০৯-২২), Fable 5.1, Sonnet 5.5; GPT-6 পরিবার; Gemini 4 Argon; Kimi K3.1 Pro, GLM-5.x, DeepSeek V4 |
| Agent harness | SWE-agent, OpenHands, Aider | mini-SWE-agent মানদণ্ড; Claude Code, Codex, Gemini CLI, Cursor, Devin, OpenHands |
| Security সংখ্যা | SecureVibeBench C-SEC সর্বোচ্চ ২৩.৮% | SusVibes: FuncPass ৬২-৮৪% কিন্তু SecPass ৭.৮-১৭.৩% (I, Opus 4.6/GPT-5.4 যুগ) |
| বর্তমান model-এ SecureVibeBench | — | বর্তমান model-এর তথ্য পাওয়া যায়নি |
| Benchmark saturation | — | SWE-bench Verified saturated: Vals.ai ৯৭.০% (I), তারপর archived; SWE-Bench Pro: Opus 5.5 ৮৯.৯% (V) বনাম Scale board ৬১.৫০ ± ৩.১০ (I) |
| Variance | একক run | pass@1 বনাম pass@5 ফারাক ১২-১৮ pt (I); scaffold একটি model-কে ২৯.৮ pt সরায় (I) |
| Leakage | অজানা | SWE-Bench Pro Verified: GLM-5.2 ৭৮.৮০% → ৫৭.৩২% যখন .git/network leakage বন্ধ (I) |
| Gaming | — | METR: সফল long-task run-এর ≥ ১৬% cheat (I, আগের প্রজন্ম); Opus 5.5 card-এ hidden tests ভাবনা ও git concealment (V) |
| Cost per task (Vals Terminal-Bench 4.0, I) | ≈ ০.৮৫ গড় (এই paper) | Opus 5.5 ১৩.২০ USD, Kimi K3.1 Pro ৪.৫৭ USD, GPT-6.1 Sol ১.৭২ USD |

- Paper-এর cost ও Vals-এর cost ভিন্ন benchmark; তুলনাযোগ্য নয়।

**সহজ কথায়:** model অনেক এগিয়েছে, কিন্তু "test পাস বনাম নিরাপদ" ফারাকটা নতুন model-এও দেখা যাচ্ছে (SusVibes-এ)।

### ২১.২ যা এখনো সত্য / যা পুরনো

- **এখনো সত্য (সম্ভবত):** SusVibes-এ নতুন model-এ SecPass ≪ FuncPass (I) — একই "correct ≠ secure" ধরন। তাই এই paper-এর কেন্দ্রীয় বার্তা এখনো টিকে আছে।
- **এখনো সত্য:** একক run ও scaffold-সংবেদনশীলতা (context.md-এর variance তথ্য)।
- **পুরনো / অনিশ্চিত:**
  - নির্দিষ্ট সংখ্যা (২৩.৮%) Sonnet 4.5 ও GPT-5 যুগের; বর্তমান model-এর C-SEC জানা নেই।
  - Aider-এর context overflow সমস্যা নতুন harness-এ কমেছে কি না জানা নেই।
  - Contamination যুক্তি (cutoff-এর আগে-পরে পার্থক্য নেই) নতুন model-এর জন্য পুনরায় পরীক্ষিত নয়।

### ২১.৩ আজও খোলা gap

| Gap | কেন এখনো খোলা | সূত্র |
|---|---|---|
| বর্তমান model-এ SecureVibeBench/SusVibes/BaxBench | Context.md: current-model SusVibes/BaxBench data নেই | context.md |
| Gold-anchored oracle (G1) | কোনো বর্তমান তথ্য নেই; paper-নির্দিষ্ট | আমার পর্যবেক্ষণ |
| Leakage (G5) | SWE-Bench Pro Verified-এ প্রমাণিত প্রভাব; এখানে অপরীক্ষিত | context.md (I) |
| Judge দিয়ে security (G9) | judge-এর over-fix flag ৫-১০% precision (S) | context.md (S) |
| Cheating/gaming (security-সম্পর্কিত) | hidden tests ও git concealment (V) | context.md |

**সহজ কথায়:** নতুন model দিয়ে এই benchmark এখনো কেউ চালায়নি, এবং oracle ও leakage-এর প্রশ্নও খোলা। এখানেই আমাদের কাজের সুযোগ।

### ২১.৪ বর্তমান model-সহ SPL3 ধারণা (cost-aware)

- ছোট উপসেট (২০-৩০ task) নিয়ে ৩ run। model-এর তালিকা: একটি সস্তা (Kimi K3.1 Pro বা GPT-6.1 Sol), একটি শক্তিশালী (Opus 5.5)। Cost context.md-এর Vals তথ্য ও paper-এর cost limit দেখে নির্ধারণ।
- লক্ষ্য: (ক) C-SEC ও $\rho$ নতুন model-এ কী, (খ) gold-anchoring প্রভাব, (গ) leakage guard-সহ ও ছাড়া।
- সতর্কতা: Opus 5.5-এর প্রতি task cost ১৩.২০ USD (Terminal-Bench 4.0, অন্য benchmark) ধরলে ৩০ task × ৩ run = ৯০ run ≈ ১,১৮৮ USD (আমার হিসাব, কেবল ইঙ্গিত)। তাই cost cap ও ছোট উপসেট জরুরি।

### ২১.৫ তিনটি Q&A

1. **প্রশ্ন:** এই paper-এর ২৩.৮% আজকের model-এর জন্য প্রযোজ্য? **উত্তর:** না; বর্তমান model-এর তথ্য পাওয়া যায়নি। SusVibes (I) নির্দেশ করে functional ও security-র ফারাক ঘুচেনি।
2. **প্রশ্ন:** SusVibes-এর ৭.৮-১৭.৩% SecPass কি SecureVibeBench-এর ১১.৬২% গড়ের সাথে তুলনীয়? **উত্তর:** ঠিক সংখ্যা-তুলনা অনুচিত: ভিন্ন benchmark, metric-সংজ্ঞা ও model প্রজন্ম। কেবল গুণগত সামঞ্জস্য বলা যায়: দুটোতেই secure rate functional rate-এর চেয়ে অনেক কম।
3. **প্রশ্ন:** Assurance report-এ এটা কিভাবে যুক্ত করব? **উত্তর:** Security-কে আলাদা signal (functional, PoV, SAST-delta, ও "could not verify") এবং leakage গার্ড, বহু-run ও CI সহ।
