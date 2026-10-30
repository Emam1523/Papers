# Sub-domain 4 Summary: LLM Test Generation

> **Sub-domain:** LLM Test Generation (৫টা paper)
> **Paper:** 01 UniTSyn (arXiv 2024) · 02 CoverUp (FSE 2025) · 03 TestDecision (arXiv 2026) · 04 ExecutionAgent (ISSTA 2025) · 05 Oracle-Guided Program Selection (ISSTA 2024)
> **উদ্দেশ্য:** আমাদের assurance layer-এর "dynamic signal" — অর্থাৎ test বানিয়ে ও চালিয়ে patch যাচাই — কতটা নির্ভরযোগ্যভাবে করা যায়, তা এই পাঁচটা paper থেকে বোঝা; আর আগের common gap (CG1–CG12) ও direction আপডেট করা।

---

## ১. এক নজরে Sub-domain-এর গল্প

আগের তিন sub-domain বারবার একটা কথা বলেছে: test দুর্বল হলে ভুল patch-ও "সঠিক" হয়ে যায় (CG1, CG3)। স্বাভাবিক সমাধান মনে হয় — আরও ভালো test বানাও। এই sub-domain দেখায় সেটা কতটা কঠিন।

| ধাপ | Paper | মূল প্রশ্ন | উত্তর |
|---|---|---|---|
| 1 | **UniTSyn** | LLM-কে ভালো test লিখতে শেখাতে কী ধরনের data লাগে? | প্রতিটা test-কে সে যে function test করে (focal function) তার সাথে জুড়ে 2.7M জোড়ার বহু-ভাষার dataset; 1.1B model-এর accuracy গড়ে 51.5% |
| 2 | **CoverUp** | Code-এর কোন অংশ test-এ চলেনি তা LLM-কে দেখালে কি coverage বাড়ে? | হ্যাঁ — CM suite-এ line+branch coverage 60.3%, আগের সেরা CodaMosa 48.7% |
| 3 | **TestDecision** | একটা একটা করে test যোগ করে পুরো suite বানানোকে কি reinforcement learning দিয়ে শেখানো যায়? | হ্যাঁ — 7B model-এ line coverage 51.42% থেকে 69.69%, mutation score 33.80% থেকে 57.13% |
| 4 | **ExecutionAgent** | যেকোনো project-এর test কি agent নিজে build করে চালাতে পারে? | আংশিক — 50টা project-এর 33টায় test চালাতে পেরেছে, 29টায় ফল আসল ফলের 10%-এর মধ্যে |
| 5 | **Oracle-Guided Program Selection** | LLM-এর অনেকগুলো program থেকে সঠিকটা কীভাবে বাছবো? | যে input-এ program-গুলো আলাদা আচরণ করে, শুধু সেখানে "সঠিক output কী" জিজ্ঞেস করো — সঠিক output বাছাইয়ের accuracy 84.3%, সংখ্যাগরিষ্ঠের ভোটে 68.2% |

**মূল বার্তা (Supervisor-কে এক লাইনে):**
> "Test বানানো সহজ, কিন্তু এমন test বানানো কঠিন যা বলতে পারে আচরণটা **সঠিক** কিনা। Coverage বাড়লেও test-এর 'রায়' (oracle) দুর্বল থাকতে পারে, আর বর্তমান code-এর আচরণ দেখে লেখা test সেই code-এর ভুলকেও 'সঠিক' বলে মেনে নেয়। তাই assurance layer-এ test-কে ব্যবহার করতে হবে মূলত **তুলনার (differential) signal** হিসেবে, একমাত্র বিচারক হিসেবে নয়।"

---

## ২. পাঁচটা Paper-এর তুলনা

### ২.১ মৌলিক তুলনা

| বিষয় | UniTSyn | CoverUp | TestDecision | ExecutionAgent | Oracle-Guided Selection |
|---|---|---|---|---|---|
| **Type** | Dataset + model | Tool (prompting loop) | Training method (RL) | Agent | Selection technique |
| **Venue** | arXiv 2024 (প্রকাশস্থান অনিশ্চিত) | FSE 2025 | arXiv 2026 | ISSTA 2025 | ISSTA 2024 |
| **Language** | Python, Java, Go, C++, JavaScript | Python | Python | বহু-ভাষা | Python (HumanEval, MBPP) |
| **Model** | SantaCoder 1.1B (fine-tuned) | GPT-4o | Qwen2.5-Coder 7B/14B (RL) | GPT-4o-mini | ChatGPT-যুগের LLM |
| **কী মাপে** | Test-এর accuracy, coverage | Line ও branch coverage | Coverage, mutation score, bug detection | Build, test চালানো, ফলের মিল | সঠিক program বাছাইয়ের হার |
| **Test-এর oracle কোথা থেকে** | Model অনুমান করে | বর্তমান code-এর আচরণ | বর্তমান code-এর আচরণ | Project-এর নিজের test | মানুষ বা LLM-কে জিজ্ঞেস করে |

### ২.২ মূল সংখ্যা

| Paper | মূল সংখ্যা | উৎস |
|---|---|---|
| UniTSyn | 2.7M focal-test জোড়া (Python 1,218,311); UniTester গড় accuracy 51.5%, SantaCoder 33.9% | Table 1, 2 |
| CoverUp | CM suite: line+branch 60.3% বনাম CodaMosa (codex) 48.7%; MT suite: 89.0% বনাম MuTAP 77.7%; খরচ 399 USD, 4 ঘণ্টা | Table 1, 2, 3 |
| CoverUp | সফল test-এর প্রায় 40% এসেছে দ্বিতীয় বা তৃতীয় prompt থেকে (feedback loop-এর মূল্য) | RQ3 |
| TestDecision | Line 51.42% থেকে 69.69%, mutation 33.80% থেকে 57.13%, execution 16.86% থেকে 67.14%; LiveCodeBench-এ bug detection 20.50% থেকে 32.50% | Table 2, 3 |
| ExecutionAgent | 33/50 project-এ test চালাতে পেরেছে; আগের সেরা পদ্ধতির 6.6 গুণ; গড়ে 74 মিনিট ও 0.16 USD প্রতি project | Table 2, Section 5 |
| Oracle-Guided | সঠিক output বাছাই 84.3% (majority vote 68.2%); HumanEval+-এ pass@1 87.7% বনাম codeT 80.8%; token প্রায় 4 গুণ কম | Table 2, 3 |

---

## ৩. আগের Common Gap — এই Sub-domain কী যোগ করলো

| CG | Gap | এই sub-domain-এর প্রমাণ | অবস্থা |
|---|---|---|---|
| CG1 | Plausible ≠ correct | Generated test-এর oracle বেশিরভাগ ক্ষেত্রে বর্তমান code-এর আচরণ থেকে আসে (CoverUp, TestDecision) — তাই সেগুলো patch-এর ভুল ধরতে পারে না, শুধু আচরণ বদলেছে কিনা বলতে পারে | **আরও স্পষ্ট হলো** — test একা সমাধান নয় |
| CG2 | Candidate re-ranking | Oracle-Guided Selection: অনেক candidate-এর মধ্যে যে input-এ পার্থক্য হয়, সেখানে oracle জিজ্ঞেস করলে বাছাই 68.2% থেকে 84.3% | **সমাধানের একটা পথ পাওয়া গেছে** — তবে শুধু ছোট function-এ পরীক্ষিত |
| CG3 | Test ও validation-এর মান | Coverage বেশি হলেও assertion দুর্বল হতে পারে; TestDecision-এর reward assertion-এর শক্তি দেখে না | **শক্ত হলো** — oracle-এর শক্তি আলাদা করে মাপতে হবে |
| CG9 | অন্য language-এ নেওয়া | UniTSyn: একই model language-ভেদে 41.7% (JS) থেকে 59.7% (Go) — language বদলালে মান বদলায় | **শক্ত হলো** |
| CG12 | Signal-কে ঠকানো | যে test-কে "বর্তমান code-এ pass করা" দিয়ে পুরস্কার দেওয়া হয়, সেই test ভুল আচরণও মেনে নিতে শেখে (TestDecision analysis-এর নিজস্ব যুক্তি) | **নতুন দিক যোগ হলো** |

---

## ৪. এই Sub-domain থেকে নতুন শিক্ষা (আমার বিশ্লেষণ)

1. **Coverage ≠ oracle।** CoverUp ও TestDecision coverage অনেক বাড়ায়, কিন্তু যে test সব line চালায় সে আচরণ সঠিক কিনা যাচাই না-ও করতে পারে। Mutation score (TestDecision) কিছুটা ভালো মাপ, কারণ এটা দেখে test ইচ্ছাকৃত ভুল ধরতে পারে কিনা।
2. **বর্তমান code থেকে লেখা test আসলে "regression oracle"।** এটা বলে "আচরণ বদলেছে কি না", "আচরণ সঠিক কি না" নয়। তাই patch যাচাইয়ে এর সঠিক ব্যবহার হলো তুলনা: patch-এর আগে ও পরে, বা কয়েকটা candidate patch-এর মধ্যে।
3. **পার্থক্য-খোঁজা test সবচেয়ে মূল্যবান।** Oracle-Guided Selection দেখায় হাজার হাজার test লাগে না (গড়ে প্রতি task-এ 1.2–1.3টা distinguishing test); দরকার সেই কয়েকটা input যেখানে candidate-রা আলাদা আচরণ করে। Agentless-এর 40টা candidate patch-এর ক্ষেত্রেও এটা প্রয়োগ করা যেতে পারে — এটা আমাদের CG2-এর সবচেয়ে সম্ভাবনাময় পথ।
4. **Test চালাতে পারাই প্রথম বাধা।** ExecutionAgent 50টার 17টা project-এ test চালাতেই পারেনি। Assurance layer যদি test চালাতে না পারে, dynamic signal শূন্য — তখন সেটা স্পষ্টভাবে "যাচাই করা যায়নি" বলতে হবে, "pass" নয়।
5. **Feedback loop কাজ করে।** CoverUp-এর সফল test-এর প্রায় 40% এসেছে দ্বিতীয়-তৃতীয় চেষ্টায়। VRpilot-এও (Sub-domain 2) একই ধরনের ফল। তবে loop-কে কোন signal দিয়ে চালানো হচ্ছে তা গুরুত্বপূর্ণ (CG12)।

---

## ৫. Updated Common Gaps (চার Sub-domain মিলিয়ে)

| # | Gap | প্রমাণ (Sub-domain) | গুরুত্ব |
|---|---|---|---|
| CG1 | Plausible patch-এর correctness যাচাই | 1, 2, 3, 4 | ⭐⭐⭐⭐⭐ |
| CG2 | Candidate selection / re-ranking | 1, 4 (Oracle-Guided Selection) | ⭐⭐⭐⭐⭐ |
| CG3 | Validation ও generated test-এর মান | 1, 2, 3, 4 | ⭐⭐⭐⭐⭐ (আগে ⭐⭐⭐⭐) |
| CG4 | Run-to-run reliability | 1, 3 | ⭐⭐⭐⭐⭐ |
| CG5 | Patch-এর security ও quality | 1, 2 | ⭐⭐⭐⭐ |
| CG6 | Benchmark quality ও contamination | 1, 2, 3 | ⭐⭐⭐⭐ |
| CG7 | Confidence ও abstention | 1, 3 | ⭐⭐⭐⭐ |
| CG8 | Evaluation-এর সমতা ও statistical rigor | 1, 2, 3 | ⭐⭐⭐⭐ |
| CG9 | অন্য language ও repository-level-এ নেওয়া | 2, 3, 4 | ⭐⭐⭐⭐⭐ |
| CG10 | Assurance tool-এর নিজের evaluation validity | 2, 3 | ⭐⭐⭐⭐ |
| CG11 | Verifier health ও version-বাঁধা রায় | 3 | ⭐⭐⭐⭐ |
| CG12 | Assurance signal-এর বিরুদ্ধে optimization pressure | 2, 3, 4 | ⭐⭐⭐⭐ |
| **CG13 (নতুন)** | **Generated test-এর oracle-এর শক্তি মাপা** — coverage-এর বদলে assertion ও mutation-ভিত্তিক মাপ | 4 (CoverUp, TestDecision) | ⭐⭐⭐⭐⭐ |
| **CG14 (নতুন)** | **Repository-level patch-এর জন্য distinguishing test** — function-level selection-কে multi-file agent patch-এ নেওয়া | 4 (Oracle-Guided), 1 (Agentless) | ⭐⭐⭐⭐⭐ |
| **CG15 (নতুন)** | **Test চালানোর পরিবেশের নির্ভরযোগ্যতা** — build ব্যর্থ হলে "যাচাই করা যায়নি" আলাদা করে report | 4 (ExecutionAgent), 3 (SWE-rebench) | ⭐⭐⭐⭐ |

---

## ৬. Research Direction — Update

> ⚠️ এখনো প্রাথমিক মত। তিনটা sub-domain বাকি (Patch Validation, Security, Trustworthy AI for SE)।

**এই sub-domain-এর পর সিদ্ধান্ত: assurance report-এর "dynamic signal" অংশটা এখন অনেক স্পষ্ট।**

| Dynamic signal | কী করবে | কোন paper থেকে |
|---|---|---|
| 1. পরিবেশ তৈরি | Project build করে test চালানো; না পারলে "যাচাই করা যায়নি" | ExecutionAgent |
| 2. Regression check | Patch-এর আগে-পরে project-এর নিজের test | Agentless (Sub-domain 1) |
| 3. Patch-কেন্দ্রিক test | শুধু patch যে line বদলেছে সেগুলো চালায় এমন test, CoverUp-এর মতো "uncovered" অংশ দেখিয়ে | CoverUp, TestDecision |
| 4. Distinguishing test | কয়েকটা candidate patch যেখানে আলাদা আচরণ করে, সেই input খুঁজে বের করা আর সেখানে issue-এর বিবরণ থেকে সঠিক output অনুমান | Oracle-Guided Selection |
| 5. Oracle-শক্তি audit | প্রতিটা generated test-এর mutation score ও assertion-এর ধরন report | TestDecision, CoverUp-এর সীমাবদ্ধতা |

**সবচেয়ে সম্ভাবনাময় নির্দিষ্ট প্রশ্ন (আমার মত, আগেরটা থেকে আরও নির্দিষ্ট):**
> "একই issue-এর জন্য AI agent-এর কয়েকটা candidate patch-এর মধ্যে আচরণগত পার্থক্য খোঁজা distinguishing test, আর static reasoning judge — এই দুটো আলাদা signal কি বর্তমান agent-দের plausible-কিন্তু-ভুল patch চিনতে ও সঠিক patch বাছতে সাহায্য করে? প্রতিটা signal-এর শক্তি (mutation score, recall, specificity) আলাদা করে মাপলে কী দেখা যায়?"

এটা CG1 + CG2 + CG3 + CG13 + CG14 একসাথে ধরে।

---

## ৭. SPL3 Implementation — এই Sub-domain থেকে কী যোগ হবে

| ধাপ | কাজ | উৎস |
|---|---|---|
| 1 | Environment setup module (প্রথমে SWE-rebench-এর তৈরি Docker image, না থাকলে ExecutionAgent-ধরনের agent) | ExecutionAgent, SWE-rebench |
| 2 | Patch-diff থেকে বদলানো line চিহ্নিত করে সেগুলোর জন্য test generation | CoverUp |
| 3 | Candidate patch-গুলোর মধ্যে differential execution ও distinguishing input খোঁজা | Oracle-Guided Selection |
| 4 | Mutation testing দিয়ে generated test-এর শক্তি মাপা | TestDecision |
| 5 | Report: প্রতিটা signal আলাদা — "pass / fail / যাচাই করা যায়নি" + শক্তির মাপ | সব |

**Practical সতর্কতা:** CoverUp পুরো CM suite-এ 399 USD খরচ করেছিল (GPT-4o)। আমাদের patch-কেন্দ্রিক test শুধু বদলানো অংশে কাজ করবে, তাই খরচ অনেক কম হওয়ার কথা — তবে আগে 3–5টা task-এ ছোট pilot চালিয়ে খরচ মাপতে হবে।

---

## ৮. Supervisor-এর সম্ভাব্য প্রশ্ন ও উত্তর (Sub-domain স্তরে)

**Q1. বেশি coverage মানেই কি ভালো test?**
A: না। Coverage বলে কোন line চলেছে, আচরণ সঠিক কিনা নয়। এজন্য mutation score — test ইচ্ছাকৃত ভুল ধরতে পারে কিনা — বেশি অর্থবহ, আর TestDecision এটা report করে (33.80% থেকে 57.13%)।

**Q2. LLM-এর বানানো test দিয়ে কেন সরাসরি বলা যায় না patch সঠিক?**
A: কারণ সেই test সাধারণত বর্তমান code-এর আচরণ দেখে লেখা। Patch ভুল হলেও test সেই ভুল আচরণকেই "প্রত্যাশিত" ধরে নেয়। তাই এগুলো তুলনার signal হিসেবে কাজ করে, বিচারক হিসেবে নয়।

**Q3. Oracle-Guided Selection তোমার কাজে কীভাবে লাগবে?**
A: Agentless একটা issue-এর জন্য 40টা candidate patch বানায়। Oracle-Guided Selection-এর ধারণা অনুযায়ী, যে input-এ এই patch-গুলো আলাদা আচরণ করে শুধু সেখানে issue-এর বিবরণ থেকে সঠিক output বের করলে, majority vote-এর চেয়ে ভালো বাছাই সম্ভব। Paper-এ এটা ছোট function-এ 68.2% থেকে 84.3% উন্নতি দিয়েছে; repository-level patch-এ এটা কাজ করে কিনা সেটাই খোলা প্রশ্ন।

**Q4. Test চালাতে না পারলে কী হবে?**
A: ExecutionAgent 50টা project-এর 17টায় test চালাতে পারেনি। আমাদের tool এমন ক্ষেত্রে "pass" বা "fail" না বলে স্পষ্টভাবে "যাচাই করা যায়নি" বলবে — নইলে ফলাফল বিভ্রান্তিকর হবে।

**Q5. আজকের model-এর ক্ষেত্রে অবস্থা কী?**
A: 2026-এর একটা বড় গবেষণা অনুযায়ী agent-দের লেখা test patch-এর 80.2%-এ দুর্বল বা কোনো স্পষ্ট oracle নেই। আর বর্তমান model-দের (Opus 5.5, GPT-6) test generation নিয়ে কোনো benchmark ফল পাওয়া যায়নি — এটাই একটা খালি জায়গা।

---

## ৯. বর্তমান (2026) প্রেক্ষাপট — আজকের Agent-দের সাথে তুলনা

> **উৎস:** `00_Current_State_2026_Sources.md` (2026-10-28)। প্রতিটা paper-এর বিস্তারিত তুলনা সেই paper-এর section ২১-এ।

| দিক | Paper-এর সময় | এখন (October 2026) | উৎস |
|---|---|---|---|
| Agent-এর লেখা test-এর oracle | — | 33,596টা agent PR-এর 86,156টা test patch-এর 80.2%-এ দুর্বল বা কোনো স্পষ্ট oracle নেই; শক্ত oracle থাকলে merge হওয়ার সম্ভাবনা বেশি | "All Smoke, No Alarm" (June 2026, স্বাধীন) |
| Mock-এর ব্যবহার | — | Agent-দের commit-এর 36% test-এ mock যোগ করে, মানুষের 26% | MSR 2026 (search-snippet) |
| Test লেখার মূল্য | CoverUp/TestDecision: test লেখা coverage বাড়ায় | এক 2026 গবেষণা: issue সমাধানে agent-এর test লেখা সীমিত উন্নতি দেয়, প্রায়ই observation-ভিত্তিক debugging দিয়ে প্রতিস্থাপিত হয় | "Rethinking the Value of Agent-Generated Tests" (search-snippet) |
| কোম্পানির দাবি | — | Fable 5.1 "নিজের কাজ যাচাই করতে নিজে test লিখতে পারে" — শুধু গুণগত দাবি, সংখ্যা নেই | Anthropic (কোম্পানির দাবি) |
| বর্তমান model-এর test-generation benchmark | — | **পাওয়া যায়নি** — SWT-bench, TDD-Bench বা unit-test benchmark-এ Opus 5.5, GPT-6, Gemini 4-এর কোনো ফল নেই | Fact sheet §6 |

**আমার পর্যবেক্ষণ:** আজকের agent-রা প্রচুর test লেখে, কিন্তু সেই test-এর oracle দুর্বল — এটা CG13-কে 2026-এ সবচেয়ে প্রাসঙ্গিক gap-গুলোর একটা বানায়। বর্তমান model দিয়ে "patch-কেন্দ্রিক distinguishing test"-এর মান মাপার কোনো প্রকাশিত কাজ পাওয়া যায়নি।

---

## ১০. পরের ধাপ

1. **Sub-domain 5: Patch Validation** — Human-in-the-Loop LLM-as-a-Judge (Google), Code Representation in APCA, Harden and Catch (Meta)। এটা আমাদের "static signal" অংশ আর RePaCA-র (Sub-domain 2) সাথে সরাসরি তুলনা।
2. Meta-র "Harden and Catch" paper test-ভিত্তিক assurance নিয়ে — এই sub-domain-এর dynamic signal ধারণার সাথে মিলিয়ে পড়তে হবে।
