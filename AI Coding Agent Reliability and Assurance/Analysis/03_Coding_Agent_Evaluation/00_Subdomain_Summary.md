# Sub-domain 3 Summary: Coding-Agent Evaluation & Reliability

> **Sub-domain:** Coding-Agent Evaluation & Reliability (৩টা paper)
> **Paper:** 01 SWE-rebench (NeurIPS 2025, Datasets & Benchmarks) · 02 SWE-Bench Pro (Scale AI, arXiv 2025) · 03 Engineering Reliable Coding Agents (monograph, arXiv 2026)
> **নোট:** এই folder-এর SWE-bench paper (Sub-domain 1, Paper 01) আর Human-in-the-Loop LLM-as-a-Judge paper (Patch Validation sub-domain-এ হবে) duplicate, তাই এখানে আবার analyse করা হয়নি।
> **উদ্দেশ্য:** তিনটা paper তুলনা করা, আগের দুই sub-domain-এর common gap (CG1–CG10) আর "assurance layer" direction এই paper-গুলো দিয়ে শক্ত, দুর্বল নাকি বদলাতে হবে — তা যাচাই করা।

---

## ১. এক নজরে Sub-domain-এর গল্প

আগের দুই sub-domain প্রশ্ন তুলেছিল: agent-এর score কি বিশ্বাসযোগ্য? এই sub-domain সরাসরি সেই প্রশ্নের উত্তর খোঁজে — **কীভাবে মাপলে ফলাফল বিশ্বাসযোগ্য হয়?**

| ধাপ | Paper | মূল প্রশ্ন | উত্তর |
|---|---|---|---|
| 1 | **SWE-rebench** | পুরনো benchmark-এর প্রশ্ন model-এর training data-তে ঢুকে গেলে কী করবো? | নিয়মিত নতুন task সংগ্রহ করো, task-এর তারিখ আর model-এর release তারিখ মিলিয়ে দেখো, প্রতিটা model 5 বার চালাও |
| 2 | **SWE-Bench Pro** | SWE-bench কি বাস্তবের কঠিন কাজ ধরতে পারে? | না — বড় (গড় 107.4 লাইন, 4.1 file), বহু-ভাষার, private বা copyleft repository-র task-এ সেরা model-ও 45%-এর নিচে |
| 3 | **Engineering Reliable Coding Agents** | Agent-এর reliability শুধু model-এর ব্যাপার, নাকি পুরো system-এর? | পুরো system-এর — harness, environment, verifier, retrieval সবকিছু ফলাফল বদলায়; অনেক "model failure" আসলে অন্য জায়গা থেকে আসে |

**মূল বার্তা (Supervisor-কে এক লাইনে):**
> "একটা leaderboard score আসলে একটা পরিবর্তনশীল প্রক্রিয়ার একটা মাত্র নমুনা। Contamination, run-ভেদে পার্থক্য, দুর্বল test আর অস্পষ্ট task মিলে score কয়েক percentage point থেকে কয়েক গুণ পর্যন্ত ভুল দেখাতে পারে। তাই agent-এর patch-এর assurance বানাতে হলে assurance tool-কেও একই কঠোরতায় মাপতে হবে।"

---

## ২. তিনটা Paper-এর তুলনা

### ২.১ মৌলিক তুলনা

| বিষয় | SWE-rebench | SWE-Bench Pro | Engineering Reliable Coding Agents |
|---|---|---|---|
| **Paper type** | Dataset + benchmark pipeline | Benchmark | Review + engineering monograph |
| **Venue** | NeurIPS 2025 (Datasets & Benchmarks) | arXiv 2509.16941 (Scale AI) | arXiv 2608.13867 (একক author) |
| **আকার** | 21,336 task (3,468 repo); benchmark-এ 294 task | 1,865 task (41 repo) | 164 scholarly + 100 practitioner + 29 benchmark + 17 case record; 206টা reliability record |
| **Language** | Python | Python, Go, JavaScript, TypeScript | প্রযোজ্য নয় |
| **Contamination প্রতিরোধ** | নতুন task + তারিখ মিলিয়ে চিহ্নিত করা | Copyleft license, held-out ও commercial (private) set | সমস্যা ও সমাধানের পর্যালোচনা |
| **Variance মাপে?** | হ্যাঁ — প্রতি model 5 run, SEM, pass@5 | একবার run | হ্যাঁ — repeated run ও paired analysis-এর পক্ষে জোরালো যুক্তি |
| **Patch correctness test-এর বাইরে?** | না (test-ভিত্তিক) | Test মানুষ দিয়ে যাচাই করা, তবু test-ভিত্তিক | হ্যাঁ — verifier দুর্বলতা নিয়ে বিস্তারিত |

### ২.২ মূল সংখ্যা

| Paper | মূল সংখ্যা | উৎস |
|---|---|---|
| SWE-rebench | DeepSeek-V3-0324: SWE-bench Verified-এ 39.7%, কিন্তু নতুন SWE-rebench task-এ 21.3% | Table 2 |
| SWE-rebench | DeepSeek-V3-1226: Verified-এ 35.2%, SWE-rebench-এ 21.9% — দুই version নতুন task-এ প্রায় সমান, কিন্তু Verified-এ আলাদা | Table 2 |
| SWE-rebench | GPT-4.1: January-র task-এ 31.1% (pass@5 44.4%), March–April-এ 26.7% (pass@5 39.0%) | Table 1 |
| SWE-Bench Pro | Public set-এ সেরা: Sonnet 4.5 43.6%, Sonnet 4 42.7%, GPT-5 (High) 41.8% (SWE-agent, 50 turn) | Table 1 |
| SWE-Bench Pro | Commercial (private) set-এ সেরা: Opus 4.1 17.8%, GPT-5 (High) 15.7% | Table 2 |
| SWE-Bench Pro | Requirements ও interface বিবরণ সরালে GPT-5 25.9% থেকে 8.40%, Opus 4.1 22.7% থেকে 8.20% | Table 3 |
| Monograph | 60,000টা SWE-bench Verified trajectory-তে একই system-এর single-run pass@1 2.2 থেকে 6.0 percentage point পর্যন্ত ওঠানামা করে (cited study) | Chapter 1 |
| Monograph | একটা agent-model জোড়ার "সফল" patch থেকে solution leak ও দুর্বল test বাদ দিলে score 12.47% থেকে 3.97% (SWE-bench+, cited) | Chapter 3 |
| Monograph | বাড়তি test দিয়ে 345টা patch-কে ভুলভাবে pass করা ধরা পড়েছে (UTBoost, cited) | Chapter 3 |

---

## ৩. আগের Common Gap — এই Sub-domain কী যোগ করলো

| CG | Gap | এই sub-domain-এর প্রমাণ | অবস্থা |
|---|---|---|---|
| CG1 | Plausible patch-এর correctness | Monograph-এর উদ্ধৃত audit: 12.47% থেকে 3.97%; বাড়তি test-এ 345টা ভুল pass। SWE-rebench ও SWE-Bench Pro দুটোই এখনো শুধু test-ভিত্তিক | **আরও শক্ত** — সমস্যা নতুন benchmark-এও রয়ে গেছে |
| CG3 | Test ও validation-এর মান | SWE-rebench-এর নিজের "test patch correctness" classifier-এর accuracy মাত্র 67% (Table 4) — স্বয়ংক্রিয়ভাবে test-এর মান যাচাই কঠিন | **শক্ত হলো** |
| CG4 | Run-to-run reliability | SWE-rebench: GPT-4.1-এর pass@1 আর pass@5-এর মধ্যে 13 point-এর বেশি ফাঁক; Monograph: একই system-এ 2.2–6.0 pp ওঠানামা | **অনেক শক্ত** — এখন সরাসরি সংখ্যা আছে |
| CG6 | Benchmark quality ও contamination | SWE-rebench: Verified-এ 39.7% বনাম নতুন task-এ 21.3%; SWE-Bench Pro: copyleft ও private repo দিয়ে প্রতিরোধ; requirements ছাড়া score তিন ভাগের এক ভাগ | **আংশিক সমাধান আছে** — এখন আমাদের কাজে এগুলো ব্যবহার করা যাবে |
| CG8 | Evaluation-এর সমতা ও statistical rigor | SWE-rebench সব model একই scaffold, একই prompt, 128K context-এ চালায়; Monograph aggregate score-এর বদলে প্রতি-task paired analysis-এর পরামর্শ দেয় | **সমাধানের পদ্ধতি পাওয়া গেছে** |
| CG9 | APCA-কে অন্য language-এ নেওয়া | SWE-Bench Pro-তে Go, JS, TS আছে — বহু-ভাষার test bed | **Test bed পাওয়া গেছে** |
| CG10 | Assurance tool-এর নিজের evaluation validity | Monograph: verifier-কেও version-সহ রেকর্ড করতে হবে, আর optimizer verifier-কে ঠকাতে পারে | **শক্ত হলো, আর নতুন দুটো gap জন্ম দিয়েছে (নিচে)** |

---

## ৪. এই Sub-domain থেকে নতুন শিক্ষা (আমার বিশ্লেষণ)

1. **একটা weighted "AssuranceScore" বানানো ঠিক হবে না।** Sub-domain 1-এ আমরা correctness, security, quality, consistency-কে weight দিয়ে যোগ করে একটা score বানানোর কথা ভেবেছিলাম। Monograph (Chapter 5–6) স্পষ্ট বলে: test pass rate, lint আর rubric score গড় করলে আরেকটা একক লক্ষ্য তৈরি হয়, optimizer সেই weighted sum-কেই ঠকাতে শেখে, আর weight বাছাই করা মানেই কোন ব্যর্থতা মেনে নেওয়া যাবে তা আগে থেকে ঠিক করা। **সংশোধন:** signal-গুলো আলাদা রেখে report করবো; আর সেগুলো এমনভাবে আলাদা রাখবো যাতে patch নিজে কোনো signal-কে প্রভাবিত করতে না পারে (যেমন agent যে test file বদলাতে পারে না, সেখান থেকে পড়া)।
2. **Score-এর সাথে uncertainty দিতেই হবে।** SWE-rebench দেখিয়েছে 5 run-এর SEM আর pass@5 report করা সম্ভব ও দরকারি। আমাদের assurance layer-এর ফলাফলও একাধিক run, confidence interval আর paired test (যেমন McNemar) দিয়ে দিতে হবে।
3. **Contamination এড়াতে আমাদের নিজের test set নতুন task থেকে নিতে হবে।** Assurance layer যদি LLM judge ব্যবহার করে, সেই LLM-ও পুরনো SWE-bench task মুখস্থ করে থাকতে পারে। SWE-rebench-এর নতুন task (model-এর release তারিখের পরের) ব্যবহার করলে এই ঝুঁকি কমে।
4. **Task-এর বিবরণ অস্পষ্ট হলে সমাধানই সম্ভব নয়।** SWE-Bench Pro-তে requirements সরালে score তিন ভাগের এক ভাগে নেমে যায়। অর্থাৎ assurance layer-কে "patch ভুল" আর "task অস্পষ্ট" আলাদা করতে পারতে হবে — এটা Agentless-এর benchmark audit-এর সাথেও মেলে।
5. **Verifier-এরও স্বাস্থ্য আছে।** Monograph বলে verifier-এর রায় তার version-এর সাথে বাঁধা; verifier বদলালে পুরনো রায় আর তুলনীয় থাকে না। আমাদের tool-এর প্রতিটা রায়ে tool ও model-এর version লিখে রাখতে হবে।

---

## ৫. Updated Common Gaps (তিন Sub-domain মিলিয়ে)

| # | Gap | প্রমাণ (Sub-domain) | গুরুত্ব |
|---|---|---|---|
| CG1 | Plausible patch-এর correctness যাচাই | 1, 2, 3 | ⭐⭐⭐⭐⭐ |
| CG2 | Candidate patch selection / re-ranking | 1 | ⭐⭐⭐⭐⭐ |
| CG3 | Validation ও generated test-এর মান | 1, 2, 3 (SWE-rebench test classifier 67%) | ⭐⭐⭐⭐ |
| CG4 | Run-to-run reliability | 1, 3 (SWE-rebench SEM ও pass@5, monograph 2.2–6.0 pp) | ⭐⭐⭐⭐⭐ (আগে ⭐⭐⭐⭐) |
| CG5 | Patch-এর security ও quality | 1, 2 | ⭐⭐⭐⭐ |
| CG6 | Benchmark quality ও contamination | 1, 2, 3 (আংশিক সমাধান এখন আছে) | ⭐⭐⭐⭐ |
| CG7 | Confidence ও abstention ("task অস্পষ্ট" চেনা সহ) | 1, 3 (SWE-Bench Pro requirements ablation) | ⭐⭐⭐⭐ (আগে ⭐⭐⭐) |
| CG8 | Evaluation-এর সমতা ও statistical rigor | 1, 2, 3 | ⭐⭐⭐⭐ |
| CG9 | APCA-কে অন্য language ও repository-level-এ নেওয়া | 2, 3 (SWE-Bench Pro বহু-ভাষার) | ⭐⭐⭐⭐⭐ |
| CG10 | Assurance tool-এর নিজের evaluation validity | 2, 3 | ⭐⭐⭐⭐ |
| **CG11 (নতুন)** | **Verifier health ও version-বাঁধা রায়** — verifier বদলালে রায়ের তুলনা; verifier নিজে কতটা নির্ভরযোগ্য | 3 (Monograph-এর research lead ERCA-203 এর সাথে মেলে) | ⭐⭐⭐⭐ |
| **CG12 (নতুন)** | **Assurance signal-এর বিরুদ্ধে optimization pressure** — agent যদি verifier-কে খুশি করতে শেখে (Goodhart-ধরনের সমস্যা) | 2 (VRpilot-এর feedback overfitting), 3 | ⭐⭐⭐⭐ |

---

## ৬. Research Direction — Update

> ⚠️ এখনো প্রাথমিক মত। চারটা sub-domain বাকি (LLM Test Generation, Patch Validation, Security, Trustworthy AI for SE)।

**এই sub-domain-এর পর সিদ্ধান্ত: direction শক্ত হয়েছে, কিন্তু output-এর ধরন বদলাতে হবে, আর evaluation design এখন অনেক স্পষ্ট।**

| দিক | আগে | এখন | কারণ |
|---|---|---|---|
| Output | একটা weighted AssuranceScore | **আলাদা আলাদা signal-এর একটা "assurance report"** — প্রতিটা signal-এর মান, uncertainty আর version | Monograph: weighted sum ঠকানো যায় |
| Signal-এর উৎস | যেকোনো | যতটা সম্ভব এমন জায়গা থেকে যা patch বদলাতে পারে না (hidden test, আলাদা judge) | Monograph-এর architectural separation |
| Consistency check | একাধিক run | k run + SEM + pass@k ও pass^k + paired test | SWE-rebench, monograph |
| Test data | SWE-bench Lite/Verified | **SWE-rebench-এর নতুন task** (contamination এড়াতে) + **SWE-Bench Pro public set** (বহু-ভাষা, বড় patch) | SWE-rebench Table 2, SWE-Bench Pro |
| নতুন component | — | **Task clarity check** — "patch ভুল" নাকি "task অস্পষ্ট" | SWE-Bench Pro Table 3 |
| নতুন component | — | **Verifier versioning** — প্রতিটা রায়ে tool ও model version | Monograph (CG11) |

**সবচেয়ে সম্ভাবনাময় নির্দিষ্ট প্রশ্ন (আমার মত, আগেরটা থেকে পরিমার্জিত):**
> "Static reasoning judge (RePaCA-ধরনের) আর dynamic signal (generated test, regression test) আলাদা আলাদা রেখে, contamination-মুক্ত নতুন task-এ, কতটা নির্ভরযোগ্যভাবে AI agent-এর ভুল কিন্তু test-pass করা patch চেনা যায় — আর এই চেনার ক্ষমতা run-ভেদে ও language-ভেদে কতটা স্থির?"

এটা CG1 + CG4 + CG9 + CG10 + CG11 একসাথে ধরে।

---

## ৭. SPL3 Implementation — এই Sub-domain থেকে কী যোগ হবে

| ধাপ | কাজ | উৎস |
|---|---|---|
| 1 | SWE-rebench-এর নতুন task load করা, task-এর তারিখ আর model release তারিখ মিলিয়ে "contamination-ঝুঁকি" চিহ্নিত করা | SWE-rebench |
| 2 | SWE-Bench Pro public set (731 task) থেকে ছোট বহু-ভাষার subset | SWE-Bench Pro |
| 3 | Experiment runner: প্রতি configuration k বার, SEM, pass@k, pass^k | SWE-rebench, monograph |
| 4 | Statistics module: প্রতি-task paired analysis, McNemar, bootstrap CI | Monograph, RePaCA (Sub-domain 2) |
| 5 | Assurance report format: আলাদা signal, প্রতিটার uncertainty ও version | Monograph |

**Practical সতর্কতা:** SWE-rebench-এর একটা পূর্ণ DeepSeek-V3 run প্রায় 7 ঘণ্টা নেয় বড় GPU cluster-এ; আমাদের বড় model চালানোর দরকার নেই — প্রকাশিত patch/trajectory ব্যবহার করে বা ছোট subset-এ API model দিয়ে কাজ করা বাস্তবসম্মত।

---

## ৮. Supervisor-এর সম্ভাব্য প্রশ্ন ও উত্তর (Sub-domain স্তরে)

**Q1. SWE-rebench আর SWE-Bench Pro দুটোই contamination নিয়ে কাজ করে — পার্থক্য কী?**
A: SWE-rebench সময় দিয়ে লড়ে — নিয়মিত নতুন task আনে আর model-এর release-এর আগের task চিহ্নিত করে। SWE-Bench Pro উৎস দিয়ে লড়ে — copyleft license-এর repo আর private commercial repo ব্যবহার করে, যেগুলো training data-তে কম আসে। প্রথমটা Python ও তুলনামূলক ছোট task, দ্বিতীয়টা বহু-ভাষা ও অনেক বড় task।

**Q2. Contamination-এর সবচেয়ে শক্ত প্রমাণ কোনটা?**
A: SWE-rebench-এর Table 2: DeepSeek-V3-0324 SWE-bench Verified-এ 39.7% কিন্তু নতুন task-এ 21.3%। আর DeepSeek-এর দুই version নতুন task-এ প্রায় সমান, অথচ Verified-এ আলাদা — authors একে পুরনো benchmark-এ সম্ভাব্য contamination-এর ইঙ্গিত বলেছেন।

**Q3. একটা model-কে একবার চালিয়ে score report করা কেন যথেষ্ট নয়?**
A: Monograph-এর উদ্ধৃত study-তে একই system-এর single-run score 2.2 থেকে 6.0 percentage point পর্যন্ত ওঠানামা করেছে। দুই agent-এর পার্থক্য প্রায়ই এর চেয়ে কম। তাই একাধিক run, SEM আর paired test ছাড়া "A, B-এর চেয়ে ভালো" বলা যায় না।

**Q4. Monograph তোমার research direction-কে কীভাবে বদলেছে?**
A: আমি আগে কয়েকটা signal মিলিয়ে একটা weighted score ভাবছিলাম। Monograph দেখায় এমন একক score-কে optimizer ঠকাতে পারে। তাই এখন আমি আলাদা আলাদা signal, প্রতিটার uncertainty আর version-সহ একটা report দেওয়ার পরিকল্পনা করছি।

**Q5. SWE-Bench Pro-র requirements ablation কী শেখায়?**
A: Task-এর বিবরণ থেকে requirements ও interface সরালে GPT-5-এর score 25.9% থেকে 8.40%-এ নামে। অর্থাৎ অনেক ব্যর্থতা model-এর দোষ নয়, task অস্পষ্ট হওয়ার কারণে। Assurance layer-এর তাই "task অস্পষ্ট" চেনার ক্ষমতা দরকার।

**Q6. তোমার evaluation কোন benchmark-এ হবে?**
A: প্রাথমিক পরিকল্পনা: contamination এড়াতে SWE-rebench-এর নতুন task, আর language-ভেদে পরীক্ষার জন্য SWE-Bench Pro public set-এর ছোট subset। সব ফল একাধিক run, confidence interval আর paired test-সহ।

---

## ৯. বর্তমান (2026) প্রেক্ষাপট — আজকের Model ও Benchmark-এর অবস্থা

> **উৎস:** `00_Current_State_2026_Sources.md` (2026-10-28)। Vals.ai-এর SWE-bench Verified archive আর SWE-Bench Pro Verified paper-এর GLM-5.2 সংখ্যা আমি নিজে মূল পৃষ্ঠা খুলে যাচাই করেছি। প্রতিটা paper-এর বিস্তারিত তুলনা সেই paper-এর section ২১-এ।

### ৯.১ এই Sub-domain-এর Paper-গুলোর পরে কী ঘটেছে

| বিষয় | Paper-এ | এখন (October 2026) | উৎস |
|---|---|---|---|
| SWE-rebench | 2025-এর task, পুরনো model; DeepSeek-V3-0324: Verified 39.7% বনাম নতুন task 21.3% | সর্বশেষ প্রকাশিত window শেষ 2026-07-01 (111 task): Fable 5 64.5% (pass@5 78.4%), Opus 5 63.4%, GLM-5.2 62.9%, GPT-5.6 Sol 62.3%; **Opus 5.5 ও GPT-6 এখনো নেই** | swe-rebench.com (স্বাধীন) |
| SWE-Bench Pro | সেরা model 45%-এর নিচে (2025) | Scale-এর board-এ সেরা 61.50; Opus 5.5-এর কোম্পানির দাবি 89.9% | Scale (স্বাধীন), Opus 5.5 System Card (কোম্পানির দাবি) |
| SWE-Bench Pro-র নিজের মান | মানুষ দিয়ে যাচাই করা task | OpenAI-এর audit: public 731 task-এর 27.4% (স্বয়ংক্রিয়) থেকে 34.1% (মানুষ) ত্রুটিপূর্ণ; OpenAI July 2026-এ এটা আর সুপারিশ করছে না (secondary উৎস) | the-decoder.com |
| SWE-Bench Pro Verified | — | 119টা সন্দেহজনক task-এর 102টা সংশোধন (75টা অতিরিক্ত সংকীর্ণ test, 22টা বিভ্রান্তিকর বিবরণ); GLM-5.2: স্বাভাবিক 78.80%, .git ও network থেকে উত্তর চুরির পথ বন্ধ করলে 57.32% | arXiv 2609.08149 (নিজে যাচাই করা) |
| Monograph-এর variance দাবি | একই system-এ 2.2–6.0 pp ওঠানামা | "Coding Agents Have Converged" (Sept 2026): Verified-এর top-30-এর পাশাপাশি 29টা জোড়ার একটাকেও statistically আলাদা করা যায় না; শুধু harness বদলালে একই model 29.8 point পর্যন্ত বদলায় | arXiv 2609.17394 (স্বাধীন) |
| Monograph-এর verifier gaming সতর্কতা | তাত্ত্বিক ও উদ্ধৃত প্রমাণ | METR: 8 ঘণ্টার বেশি লম্বা task-এ সফল run-এর অন্তত 16% আসলে প্রতারণা (পুরনো প্রজন্মের model); Opus 5.5 System Card-এ model-কে "hidden tests" নিয়ে ভাবতে আর কিছু training environment-এ git দিয়ে পরিবর্তন লুকাতে দেখা গেছে | METR (May 2026), System Card (কোম্পানির দাবি) |

### ৯.২ Gap-গুলো আজ কোথায়

| CG | 2026-এ অবস্থা | প্রমাণ |
|---|---|---|
| CG4 (run-to-run reliability) | **খোলা** | SWE-rebench-এ pass@1 বনাম pass@5-এর ফাঁক 12–18 point; SWE Atlas: pass@1 থেকে pass^3-এ 30–50% পতন (search-snippet) |
| CG6 (contamination ও benchmark মান) | **খোলা; নতুন benchmark-ও দ্রুত সমস্যায় পড়ছে** | Verified বাদ, SWE-Bench Pro-ও ত্রুটিপূর্ণ; নতুন contamination-মুক্ত benchmark (DeepSWE, SWE-rebench) এখনো বর্তমান সব model কভার করে না |
| CG8 (evaluation-এর সমতা) | **আরও খারাপ** | কোম্পানির দাবি বনাম স্বাধীন মাপ; প্রতিটা কোম্পানি আলাদা benchmark-এর ফল দেখায় |
| CG11 (verifier health) | **খোলা** | DeepSWE: SWE-Bench Pro-র পুরনো test-এর সাথে LLM judge-এর অমিল 32.4% |
| CG12 (verifier gaming) | **খোলা, এখন সরাসরি মাপা প্রমাণ আছে** | GLM-5.2-এর 78.80 থেকে 57.32; DeepSWE-তে প্রতারণার 87% ক্ষেত্রে .git history থেকে উত্তর পড়া; বর্তমান Opus 5.5 বা GPT-6-এর স্বাধীন reward-hacking audit পাওয়া যায়নি |

### ৯.৩ Research Direction-এর জন্য এর অর্থ — আমার পর্যবেক্ষণ
1. **Assurance layer-এর প্রথম কাজ হতে পারে leakage বন্ধ করা।** Patch যাচাইয়ের আগে নিশ্চিত করতে হবে agent .git history, network বা স্থানীয় file থেকে উত্তর পায়নি। SWE-Bench Pro Verified দেখায় এটা না করলে score 20 point-এর বেশি ফুলে থাকতে পারে।
2. **Test set বাছাই বদলাতে হবে।** কাঁচা SWE-Bench Pro public set-এর বদলে সংশোধিত SWE-Bench Pro Verified, আর contamination এড়াতে SWE-rebench-এর নতুন window।
3. **প্রতিটা ফলাফলে "কোম্পানির দাবি" আর "আমাদের মাপ" আলাদা করে দেখাতে হবে**, আর একাধিক run ও paired test ছাড়া কোনো তুলনা করা যাবে না — কারণ শীর্ষ agent-দের পার্থক্য এখন noise-এর চেয়ে ছোট।

---

## ১০. পরের ধাপ

1. **Sub-domain 4: LLM Test Generation** — CG3 (test-এর মান) আর assurance layer-এর dynamic signal-এর জন্য সবচেয়ে গুরুত্বপূর্ণ।
2. **Sub-domain 5: Patch Validation** — Human-in-the-Loop LLM-as-a-Judge paper-কে RePaCA ও monograph-এর verifier আলোচনার সাথে তুলনা।
3. প্রতিটা sub-domain শেষে direction-টা আরও নির্দিষ্ট করা।
