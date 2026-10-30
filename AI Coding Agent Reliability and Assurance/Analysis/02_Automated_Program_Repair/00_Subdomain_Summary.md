# Sub-domain 2 Summary: Automated Program Repair

> **Sub-domain:** Automated Program Repair (৩টা paper)
> **Paper:** 01 APR Survey (ACM Computing Surveys 2025) · 02 VRpilot — LLM Vulnerability Repair (AIware 2024) · 03 RePaCA (Neurocomputing 2026)
> **নোট:** এই folder-এর "Human-in-the-Loop Patch Evaluation (LLM-as-a-Judge)" paper-টা Patch Validation sub-domain-এ analyse করা হবে (index অনুযায়ী)।
> **উদ্দেশ্য:** তিনটা paper তুলনা করা, Sub-domain 1-এর common gap (CG1–CG8) আর প্রাথমিক research direction এই paper-গুলো দিয়ে শক্ত হলো না দুর্বল হলো তা যাচাই করা।

---

## ১. এক নজরে Sub-domain-এর গল্প

Sub-domain 1 (AI Coding Agents) দেখিয়েছিল যে agent-এর "resolved" patch সবসময় সঠিক নয়। এই sub-domain সেই সমস্যার **পুরনো ও গভীর শিকড়** দেখায় — Automated Program Repair (APR) field বহু বছর ধরে এই একই সমস্যার সাথে লড়ছে।

| ধাপ | Paper | মূল প্রশ্ন | উত্তর |
|---|---|---|---|
| 1 | **APR Survey** (Renzullo et al.) | ML/LLM আসার পর APR-এর evaluation কি এখনো বিশ্বাসযোগ্য? | না পুরোপুরি — data leakage, ভিন্ন ভিন্ন correctness সংজ্ঞা, পুরনো benchmark ML-এর জন্য বানানো নয় |
| 2 | **VRpilot** (Kulsum et al.) | Reasoning আর validation feedback কি security bug (vulnerability) ঠিক করতেও কাজ করে? | হ্যাঁ — C-তে plausible patch 33.4% থেকে 63.8%; তবে plausible আর correct-এর পার্থক্য রয়ে যায় |
| 3 | **RePaCA** (Fuster-Pena et al.) | Test না চালিয়ে শুধু code দেখে কি বলা যায় patch সঠিক নাকি overfitting? | হ্যাঁ, অনেকটা — reasoning LLM + GRPO দিয়ে 83.1% accuracy; তবে সঠিক patch বাতিলের হার উল্লেখযোগ্য |

**মূল বার্তা (Supervisor-কে এক লাইনে):**
> "APR field-এ 'test pass করা patch' আর 'সঠিক patch'-এর পার্থক্য (patch overfitting) পুরনো সমস্যা। LLM আসার পর এর সাথে যোগ হয়েছে data leakage আর অসংগত evaluation। এই sub-domain-এর তিনটা paper মিলে দেখায়: সমস্যা সমাধানের যন্ত্র (RePaCA-র মতো APCA) আছে, কিন্তু সেগুলোর নিজেদেরও trade-off আছে, আর সেগুলোকেও leakage-মুক্তভাবে যাচাই করতে হবে।"

---

## ২. তিনটা Paper-এর তুলনা

### ২.১ মৌলিক তুলনা

| বিষয় | APR Survey | VRpilot | RePaCA |
|---|---|---|---|
| **Paper type** | Survey / Review | Technique + case study | Technique (APCA) |
| **Venue** | ACM Computing Surveys 57(8), 2025 | AIware 2024 (ACM) | Neurocomputing 701, 2026 |
| **কাজের ধরন** | 5টা top venue-র 118টা APR article বিশ্লেষণ | LLM দিয়ে vulnerability repair | Patch সঠিক নাকি overfitting — classify করা |
| **Language** | Language-নিরপেক্ষ (বেশিরভাগ Java benchmark) | C ও Java | Java (Defects4J-ভিত্তিক) |
| **মূল কৌশল** | Taxonomy ও সমালোচনামূলক বিশ্লেষণ | Chain-of-thought reasoning + compiler/sanitizer/test feedback loop | Reasoning LLM + GRPO (reinforcement learning) fine-tuning |
| **Test চালাতে হয়?** | প্রযোজ্য নয় | হ্যাঁ (dynamic validation) | না (static) |
| **Sub-domain 1-এর সাথে সম্পর্ক** | Evaluation validity (CG6, CG8) | Validation feedback ও security (CG3, CG5) | Overfitting detection (CG1) |

### ২.২ মূল সংখ্যা

| Paper | মূল সংখ্যা | উৎস |
|---|---|---|
| APR Survey | 118 article (2018–2023); 61টা নতুন technique-এর মধ্যে 22টা ML, 7টা LLM (যার 6টা শেষ দুই বছরে) | Section 1, 3 |
| APR Survey | 44টা article Defects4J ব্যবহার করেছে; near-duplicate data থাকলে metric 100% পর্যন্ত ফুলে যেতে পারে (cited study) | Section 4, 5 |
| VRpilot (C, ChatGPT) | Compilable 55.6% থেকে 90.4%; Plausible 33.4% থেকে 63.8% (baseline CodexVR* বনাম VRpilot) | Table 3 |
| VRpilot (C, manual check) | হাতে যাচাই করা 7টা case-এ গড় correct 50% থেকে 57% | Table 4 |
| VRpilot (Java, 50টা vulnerability) | Plausible 15.5 থেকে 20.0; Correct 10.2 থেকে 14.0 | Table 5 |
| RePaCA (Small dataset, 5-fold) | Accuracy 83.1, Precision 84.0, Recall 85.7, F1 84.8, AUC 82.8 | Table 4 |
| RePaCA (cross-dataset) | Accuracy 72.7 (APPT 60.5) | Table 6 |
| RePaCA (INVALIDATOR split, 139 patch) | 109টা overfitting-এর 106টা ধরেছে; কিন্তু 30টা সঠিক patch-এর মাত্র 16টা সঠিক চিনেছে | Fig. 3 |

---

## ৩. Sub-domain 1-এর Common Gap — এই Sub-domain কী যোগ করলো

| CG | Gap (Sub-domain 1 থেকে) | এই sub-domain-এর প্রমাণ | অবস্থা |
|---|---|---|---|
| CG1 | Plausible patch-এর correctness যাচাই | Survey: অনেক article একটা মাত্র human reference patch-কে correctness-এর মাপকাঠি ধরেছে (Section 5.3-এর citation list গুনলে 29টা)। VRpilot: plausible আর correct-এর মধ্যে বড় ফাঁক (Java-তে 20.0 plausible, 14.0 correct)। RePaCA: static APCA দিয়ে overfitting ধরা সম্ভব | **আরও শক্ত** — সমস্যা পুরনো, আর সমাধানের একটা কার্যকর পথ (APCA) আছে |
| CG3 | Generated test ও validation-এর মান | VRpilot-এর feedback loop compiler/sanitizer/test-এর উপর নির্ভরশীল — সেই validator দুর্বল হলে patch-ও validator-কে "খুশি" করতে শেখে | **শক্ত হলো** — নতুন দিক: "feedback overfitting" |
| CG5 | Patch-এর security | VRpilot vulnerability repair করে, কিন্তু নির্দিষ্ট input-এ sanitizer pass করা মানেই code নিরাপদ নয় | **আংশিক** — Security sub-domain-এ আরও পড়তে হবে |
| CG6 | Benchmark quality ও contamination | Survey: LLM-APR-এর 5টা article contamination উপেক্ষা করেছে, কেউ near-duplicate handle করেনি | **অনেক শক্ত** (⭐⭐⭐ থেকে ⭐⭐⭐⭐) |
| CG8 | Evaluation-এর সমতা | Survey-র উদাহরণ: CURE 10,000টা candidate বানিয়ে 5,000টা যাচাই করে, RewardRepair থামে 200-তে; কেউ perfect fault localization ধরে নেয়, কেউ নেয় না | **শক্ত হলো** — Sub-domain 1-এর ভিন্ন cost হিসাবের মতোই সমস্যা |

---

## ৪. এই Sub-domain থেকে নতুন শিক্ষা (আমার বিশ্লেষণ)

1. **Overfitting detector-এর নিজেরও trade-off আছে।** RePaCA প্রায় সব overfitting patch ধরে (106/109), কিন্তু INVALIDATOR split-এ সঠিক patch-এর প্রায় অর্ধেক বাতিল করে (16/30 চেনে)। Training-এ overfitting ঠিক ধরলে reward 2.0, সঠিক patch ঠিক চিনলে 1.0 — এই অসমান reward model-কে "overfitting" বলার দিকে ঠেলে দেয় (analysis file-এর নিজস্ব decision-theory যুক্তি)। **শিক্ষা:** Assurance layer-এ কোনো detector-কে শুধু accuracy দিয়ে বিচার করা যাবে না; recall আর specificity দুটোই report করতে হবে।
2. **Assurance tool-কেও leakage-মুক্তভাবে যাচাই করতে হবে।** Survey-র সতর্কতা শুধু repair tool-এর জন্য নয় — আমরা যদি একটা judge বা classifier বানাই, সেটাকেও random split নয়, repository-ভিত্তিক বা সময়-ভিত্তিক (temporal) split দিয়ে যাচাই করতে হবে।
3. **Validation feedback দুইভাবে ব্যবহার হয়।** VRpilot validation দিয়ে একটা patch-কে বারবার *শোধরায়* (refine); Agentless (Sub-domain 1) validation দিয়ে অনেকগুলো candidate থেকে *বাছাই* করে (select)। দুটোই validator-এর মানের উপর নির্ভরশীল।
4. **Statistical rigor কম।** VRpilot-এর "C-তে 14% বেশি correct patch" দাবি মাত্র 7টা case-এর উপর; analysis file-এর নিজস্ব sign test-এ এটা statistically significant নয় (p = 0.625)। RePaCA McNemar test করেছে (χ² = 25.90, p = 3.6 × 10⁻⁷) — এটা ভালো উদাহরণ। **শিক্ষা:** আমাদের নিজেদের কাজে significance test ও confidence interval রাখতেই হবে।
5. **Java থেকে Python, method থেকে repository।** RePaCA ও প্রায় সব APCA কাজ Java method-level patch-এ। SWE-bench-এর Python, multi-file, repository-level agent patch-এ এগুলো কাজ করবে কিনা — এটা একটা খোলা প্রশ্ন বলে মনে হচ্ছে (নিশ্চিত হতে আলাদা literature search লাগবে)।

---

## ৫. Updated Common Gaps (দুই Sub-domain মিলিয়ে)

| # | Gap | প্রমাণ (Sub-domain) | গুরুত্ব |
|---|---|---|---|
| CG1 | Plausible patch-এর correctness যাচাই | 1 (চারটা paper), 2 (তিনটা paper) | ⭐⭐⭐⭐⭐ |
| CG2 | Candidate patch selection / re-ranking | 1 (Agentless 96 বনাম 126) | ⭐⭐⭐⭐⭐ |
| CG3 | Validation ও generated test-এর মান (feedback overfitting সহ) | 1, 2 (VRpilot) | ⭐⭐⭐⭐ |
| CG4 | Run-to-run reliability | 1 | ⭐⭐⭐⭐ |
| CG5 | Patch-এর security ও quality | 1 (কেউ মাপেনি), 2 (VRpilot আংশিক) | ⭐⭐⭐⭐ |
| CG6 | Benchmark quality ও contamination | 1, 2 (Survey) | ⭐⭐⭐⭐ (আগে ⭐⭐⭐) |
| CG7 | Confidence ও abstention | 1 | ⭐⭐⭐ |
| CG8 | Evaluation-এর সমতা ও statistical rigor | 1, 2 (Survey, VRpilot) | ⭐⭐⭐⭐ (আগে ⭐⭐⭐) |
| **CG9 (নতুন)** | **APCA-কে Python repository-level agent patch-এ নেওয়া** — Java method-level থেকে SWE-bench-ধরনের patch-এ | 2 (RePaCA), 1 (AutoCodeRover-এর 78টা patch) | ⭐⭐⭐⭐⭐ |
| **CG10 (নতুন)** | **Assurance tool-এর নিজের evaluation validity** — detector-কে leakage-মুক্ত split ও balanced metric দিয়ে যাচাই | 2 (Survey, RePaCA) | ⭐⭐⭐⭐ |

---

## ৬. Research Direction — Update

> ⚠️ এখনো প্রাথমিক মত। পাঁচটা sub-domain বাকি।

**Sub-domain 1-এর প্রস্তাব ছিল:** "Assurance Layer for AI Coding Agent Patches" — overfitting detection, re-ranking, security scan, consistency check, confidence score।

**এই sub-domain-এর পর সিদ্ধান্ত: direction আরও শক্ত হয়েছে, সাথে কিছু পরিবর্তন।**

| Component | আগে | এখন (পরিবর্তন) | কারণ |
|---|---|---|---|
| 1. Overfitting detection | Extra test generation | **Static (RePaCA-ধরনের reasoning judge) + dynamic (extra test) মিলিয়ে** | Static detector-এর specificity কম; dynamic signal দিয়ে ভারসাম্য আনা যায় |
| 2. Re-ranking | Agentless candidate বাছাই | অপরিবর্তিত | — |
| 3. Security scan | Bandit/Semgrep | অপরিবর্তিত, তবে "sanitizer pass ≠ নিরাপদ" মাথায় রেখে | VRpilot |
| 4. Consistency check | একাধিক run | অপরিবর্তিত | — |
| 5. Confidence + abstention | একটা score | Recall ও specificity আলাদা করে report | RePaCA-র trade-off |
| **6. Evaluation validity (নতুন)** | — | Assurance layer-কে নিজেই leakage-মুক্ত split, balanced metric ও significance test দিয়ে যাচাই | Survey, RePaCA |

**সবচেয়ে সম্ভাবনাময় নির্দিষ্ট প্রশ্ন (আমার মত):**
> "RePaCA-ধরনের reasoning-based static patch correctness assessment কি SWE-bench-এর Python repository-level agent patch-এ কাজ করে? Dynamic signal (generated test) যোগ করলে কি সঠিক patch বাতিলের হার কমে?"

এটা CG1 + CG9 + CG10 একসাথে ধরে, আর AutoCodeRover-এর 78টা যাচাই করা patch (Sub-domain 1) একটা ছোট কিন্তু বাস্তব test set হতে পারে (public artifact-এ label আছে কিনা যাচাই করতে হবে)।

---

## ৭. SPL3 Implementation — এই Sub-domain থেকে কী যোগ হবে

| ধাপ | কাজ | উৎস |
|---|---|---|
| 1 | Patch correctness label-সহ dataset তৈরি/সংগ্রহ (Java APCA dataset + agent patch) | RePaCA, Sub-domain 1 |
| 2 | Reasoning LLM দিয়ে static judge (প্রথমে prompting, সম্ভব হলে ছোট model fine-tuning) | RePaCA |
| 3 | Validation feedback loop module (compile, test, sanitizer) | VRpilot |
| 4 | Evaluation module: Accuracy, Precision, Recall, F1, Specificity, Balanced accuracy, MCC, McNemar test, bootstrap CI | RePaCA, Survey |
| 5 | Leakage check: repository/temporal split, near-duplicate detection | Survey |

**Practical সতর্কতা:** RePaCA-র training H100 GPU-তে হয়েছে; student project-এ fine-tuning-এর বদলে প্রথমে prompting দিয়ে শুরু করা বাস্তবসম্মত (paper অনুযায়ী inference 8 GB VRAM-এ চলে)।

---

## ৮. Supervisor-এর সম্ভাব্য প্রশ্ন ও উত্তর (Sub-domain স্তরে)

**Q1. APR আর AI coding agent-এর সম্পর্ক কী?**
A: AI coding agent আসলে APR-এর আধুনিক, বড় রূপ — bug report থেকে repository-তে patch। APR field-এর পুরনো সমস্যা (patch overfitting, দুর্বল test, benchmark leakage) agent-এও হুবহু আছে।

**Q2. Patch overfitting কী, আর কেন এত গুরুত্বপূর্ণ?**
A: Test pass করে কিন্তু আসল bug ঠিক করে না এমন patch। Sub-domain 1-এ AutoCodeRover-এর test pass করা patch-এর মাত্র 65.4% সঠিক ছিল; VRpilot-এর Java-তে 20.0টা plausible-এর মধ্যে 14.0টা correct। অর্থাৎ test pass-কে বিশ্বাস করলে অনেক ভুল patch গ্রহণ হবে।

**Q3. RePaCA কি সমস্যার সমাধান করে ফেলেছে?**
A: আংশিক। Defects4J-ভিত্তিক dataset-এ 83.1% accuracy, অন্য dataset-এ 72.7%। কিন্তু একটা split-এ সঠিক patch-এর প্রায় অর্ধেক বাতিল করেছে। আর এটা Java method-level-এ পরীক্ষিত; Python repository-level agent patch-এ এখনো যাচাই হয়নি।

**Q4. Survey থেকে সবচেয়ে বড় শিক্ষা কী?**
A: ML/LLM-ভিত্তিক APR-এর ফলাফল তুলনা করা কঠিন, কারণ correctness-এর সংজ্ঞা, fault localization-এর অনুমান আর থামার নিয়ম paper-ভেদে আলাদা, আর training data-য় benchmark ঢুকে থাকতে পারে। আমাদের নিজের কাজেও এই ভুলগুলো এড়াতে হবে।

**Q5. Vulnerability repair সাধারণ APR থেকে কোথায় আলাদা?**
A: লক্ষ্য শুধু test pass নয়, নিরাপত্তা ঝুঁকি দূর করা। VRpilot sanitizer দিয়ে যাচাই করে, কিন্তু নির্দিষ্ট input-এ crash না হওয়া মানেই code নিরাপদ নয় — এটা CG5-এর অংশ।

**Q6. এই sub-domain-এর পর তোমার research direction কি বদলেছে?**
A: Direction একই আছে (agent patch-এর assurance layer), কিন্তু আরও নির্দিষ্ট হয়েছে: static reasoning judge আর dynamic test signal মিলিয়ে Python agent patch-এর correctness যাচাই, আর detector-কে leakage-মুক্ত ও balanced metric দিয়ে মূল্যায়ন।

---

## ৯. বর্তমান (2026) প্রেক্ষাপট — আজকের Model-দের সাথে তুলনা

> **উৎস:** `00_Current_State_2026_Sources.md` (2026-10-28)। "search-snippet" চিহ্নিত তথ্য মূল পৃষ্ঠা খুলে যাচাই হয়নি — supervisor-কে দেখানোর আগে আবার মিলিয়ে নিতে হবে। প্রতিটা paper-এর বিস্তারিত তুলনা সেই paper-এর section ২১-এ।

### ৯.১ তখন বনাম এখন

| দিক | Paper-এর সময় | এখন (October 2026) | উৎস |
|---|---|---|---|
| Contamination নিয়ে সতর্কতা (Survey) | Survey বলেছিল LLM-APR-এর 5টা article contamination উপেক্ষা করেছে | এখন বড় কোম্পানিগুলো নিজেরাই স্বীকার করছে: OpenAI SWE-bench Verified-এ evaluate করা বন্ধ করেছে, Vals.ai সেটা archive করেছে | OpenAI (Feb 2026, search-snippet), Vals.ai (Sept 2026) |
| Plausible বনাম correct | Survey: অনেকে একটা human reference patch-কে মাপকাঠি ধরে; VRpilot: Java-তে plausible 20.0, correct 14.0 | PatchDiff (ICSE 2026): SWE-bench-এর plausible patch-এর 29.6% gold patch থেকে আলাদা আচরণ করে | arXiv 2503.15223 |
| LLM দিয়ে patch correctness যাচাই (RePaCA-র ধরন) | RePaCA: Defects4J-এ 83.1% accuracy | ComPass paper অনুযায়ী সাধারণ LLM baseline overfitting patch ছাঁকতে মাত্র 62.14% accuracy পায় (search-snippet); এক গবেষণায় LLM judge-দের "over-fix" সতর্কতার precision মাত্র 5–10% (search-snippet); শিল্পে এখন rubric আর LLM judge দিয়ে "mergeability" যাচাইয়ের দিকে ঝোঁক (FrontierCode) | ফাইলের §4 |
| Vulnerability ও security (VRpilot) | VRpilot: sanitizer দিয়ে যাচাই | SusVibes: পুরনো agent-দের secure pass 7.8–17.3%; Opus 5.5-এর বিরুদ্ধে coding environment-এ prompt injection সফলতা safeguard ছাড়া 54.61%, safeguard সহ 11.13% (কোম্পানির দাবি) | ফাইলের §5 |
| Agent-এর patch-এ বর্তমান model-এর correctness study | — | **পাওয়া যায়নি** — Opus 5.5 বা GPT-6-এর agent patch-এ LLM judge যাচাইয়ের কোনো গবেষণা নেই | ফাইলের §4 |

### ৯.২ Gap-গুলো আজ কোথায়

| CG | 2026-এ অবস্থা | কেন |
|---|---|---|
| CG1 (plausible ≠ correct) | **খোলা** | PatchDiff-এর 29.6%; বর্তমান agent-এ আবার মাপা হয়নি |
| CG3 (validation-এর মান) | **খোলা, দুই দিক থেকে** | Agent-দের লেখা test patch-এর 80.2%-এ দুর্বল বা কোনো স্পষ্ট oracle নেই ("All Smoke, No Alarm", 2026) |
| CG5 (security) | **খোলা** | বর্তমান model-এর SusVibes/BaxBench ফল নেই |
| CG9 (APCA-কে অন্য language ও repository-level-এ নেওয়া) | **খোলা, আর আরও মূল্যবান** | শিল্প যখন LLM judge-এর দিকে যাচ্ছে, অথচ judge-দের নির্ভরযোগ্যতা প্রমাণিত নয় |
| CG10 (assurance tool-এর নিজের validity) | **খোলা** | একটা গবেষণা বলছে judge-দের নিজেদের মধ্যে মিল অনেক বেশি, কিন্তু আসল execution-এর সাথে মিল কম — অর্থাৎ judge-রা একই ভুল একসাথে করতে পারে (search-snippet) |

### ৯.৩ এর অর্থ — আমার পর্যবেক্ষণ
- RePaCA-ধরনের reasoning judge **বর্তমান model দিয়ে বানিয়ে, বর্তমান agent-দের patch-এ** পরীক্ষা করা এখন একটা পরিষ্কার খালি জায়গা: শিল্প এই পদ্ধতির দিকে যাচ্ছে, কিন্তু কেউ এটা যাচাই করেনি।
- Judge-কে test-এর ফলাফলের সাথে মিলিয়ে (execution-calibrated) মাপতে হবে, শুধু অন্য judge-এর সাথে নয়।

---

## ১০. পরের ধাপ

1. **Sub-domain 3: Coding-Agent Evaluation & Reliability** — SWE-rebench (contamination-free evaluation), SWE-Bench Pro (কঠিন long-horizon task), আর Engineering Reliable Coding Agents (বড় monograph)। CG4, CG6 ও CG8-এর জন্য গুরুত্বপূর্ণ।
2. Patch Validation sub-domain-এ Human-in-the-Loop LLM-as-a-Judge paper-টা RePaCA-র সাথে তুলনা করতে হবে।
