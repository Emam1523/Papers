# Sub-domain 1 Summary: AI Coding Agents

> **Sub-domain:** AI Coding Agents (৪টা paper)
> **Paper:** 01 SWE-bench · 02 SWE-agent · 03 AutoCodeRover · 04 Agentless
> **উদ্দেশ্য:** ৪টা paper পাশাপাশি রেখে তুলনা করা, common gap খুঁজে বের করা, আর আমাদের domain **"Reliability and Assurance"**-এর জন্য এই sub-domain থেকে সবচেয়ে ভালো research সুযোগ বাছাই করা।

---

## ১. এক নজরে Sub-domain-এর গল্প

এই ৪টা paper মিলে একটা পরিষ্কার ধারাবাহিক গল্প বলে:

| ধাপ | Paper | মূল প্রশ্ন | উত্তর |
|---|---|---|---|
| 1 | **SWE-bench** (ICLR 2024) | LLM কি আসল GitHub issue solve করতে পারে? মাপবো কীভাবে? | একটা realistic benchmark; সরল retrieval + LLM মাত্র 1.96% solve করে |
| 2 | **SWE-agent** (NeurIPS 2024) | LLM-কে computer ব্যবহারের জন্য বিশেষ interface দিলে কি ভালো করে? | হ্যাঁ — Agent-Computer Interface (ACI) দিয়ে full SWE-bench-এ 12.47% |
| 3 | **AutoCodeRover** (ISSTA 2024) | Software engineering-এর জ্ঞান (AST, code search, SBFL) কাজে লাগালে কি আরও ভালো ও সস্তা হয়? | হ্যাঁ — Lite-এ 19% (@1), খরচ প্রায় 0.43 USD/issue |
| 4 | **Agentless** (arXiv 2024) | আদৌ কি জটিল agent লাগে? | না — সরল ৩-ধাপের pipeline Lite-এ 32.00%, 0.70 USD/issue; আর benchmark-এর নিজেরই সমস্যা আছে |

**মূল বার্তা (Supervisor-কে এক লাইনে):**
> "AI coding agent-এর score খুব দ্রুত বেড়েছে, কিন্তু চারটা paper-ই আলাদা আলাদা ভাবে দেখায় যে **'test pass করা' মানেই 'সঠিক ও বিশ্বাসযোগ্য' নয়** — plausible patch ভুল হতে পারে, একই agent বারবার চালালে ফল বদলায়, আর benchmark-এর task-ও ত্রুটিপূর্ণ। এই ফাঁকটাই আমাদের domain-এর মূল research জায়গা।"

---

## ২. চারটা Paper-এর তুলনা

### ২.১ মৌলিক তুলনা

| বিষয় | SWE-bench | SWE-agent | AutoCodeRover | Agentless |
|---|---|---|---|---|
| **Paper type** | Benchmark/Dataset | Agent system + interface study | Agent system (SE-oriented) | Pipeline + benchmark audit |
| **Venue** | ICLR 2024 | NeurIPS 2024 | ISSTA 2024 | arXiv 2024 (পরে প্রকাশের তথ্য DBLP-তে যাচাই করতে হবে) |
| **পরের action কে ঠিক করে?** | কেউ না (একবারে patch) | LLM (ReAct loop) | LLM (search API-র ভেতরে) | কেউ না — নির্দিষ্ট pipeline |
| **Localization** | BM25 file retrieval | `find_file`, `search_dir`, `search_file`, file viewer | AST-ভিত্তিক class/method search API + SBFL | Hierarchical: file → class/function → edit line |
| **Patch তৈরি** | একটা patch (greedy) | Linter-guarded `edit` command | Retry সহ patch generation | প্রতি issue-তে 40টা candidate (search/replace format) |
| **Patch validation** | নেই | Agent নিজে reproduce script চালায় | Developer test থাকলে চালায় | Reproduction test + regression test + majority voting |
| **Open-source?** | হ্যাঁ | হ্যাঁ | হ্যাঁ | হ্যাঁ |

### ২.২ একই Benchmark-এ ফলাফল (SWE-bench Lite, 300 task)

সব সংখ্যা একটা উৎস থেকে নেওয়া — **Agentless paper-এর Table 1** — যাতে তুলনা সমান থাকে।

| System | LLM | Resolved | Avg cost (USD) | Correct location: Line / Function / File |
|---|---|---|---|---|
| RAG (SWE-bench baseline) | GPT-4 | 8 (2.67%) | 0.13 | 12.7% / 23.3% / 47.3% |
| RAG (SWE-bench baseline) | Claude 3 Opus | 13 (4.33%) | 0.25 | 22.0% / 30.0% / 57.0% |
| SWE-agent | GPT-4 | 54 (18.00%) | 2.51 | 30.7% / 45.3% / 61.0% |
| SWE-agent | GPT-4o | 55 (18.33%) | 2.53 | 29.3% / 42.3% / 58.3% |
| AutoCodeRover | GPT-4 | 57 (19.00%) | 0.45 | 29.0% / 42.3% / 62.3% |
| **Agentless** | GPT-4o | **96 (32.00%)** | **0.70** | **35.3% / 52.0% / 69.7%** |

### ২.৩ Full SWE-bench (2,294 task)

| System | Resolved | উৎস |
|---|---|---|
| Claude 2 + BM25 (SWE-bench baseline) | 1.96% | Paper 01, Table 5 |
| SWE-agent + GPT-4 Turbo | 12.47% (286) | Paper 02 |
| AutoCodeRover @1 | 12.42% (285) | Paper 03, Table 2 |
| AutoCodeRover @3 | 17.96% (422) | Paper 03, Table 2 |

### ২.৪ গুরুত্বপূর্ণ পর্যবেক্ষণ (আমার বিশ্লেষণ)

1. **Localization-ই বড় পার্থক্য তৈরি করে।** উপরের table-এ যার file/function-level localization ভালো, তার resolve rate-ও ভালো। RAG-এর function-level 23.3% থেকে Agentless-এর 52.0% — এই উন্নতিই মূলত score বাড়িয়েছে। Paper 01-এর "localization হলো মূল bottleneck" দাবিটা পরের তিনটা paper-ই সমর্থন করে।
2. **বেশি জটিলতা মানেই বেশি ভালো নয়।** সবচেয়ে সরল (Agentless) সবচেয়ে ভালো ও তুলনামূলক সস্তা। কারণ: (ক) একাধিক candidate তৈরি করে বাছাই করা, (খ) LLM-কে ভুল পথে বারবার ঘুরতে না দেওয়া।
3. **খরচের হিসাবও সমান নয়।** SWE-agent (GPT-4 Turbo)-এর Lite খরচ SWE-agent paper নিজে (Table 1) বলেছে 1.67 USD, কিন্তু AutoCodeRover (Table 2) ও Agentless (Table 1) paper একই system-এর জন্য বলছে 2.51 USD। অর্থাৎ **evaluation-এর মাপকাঠিই paper-ভেদে আলাদা** — এটা নিজেই একটা reliability সমস্যা।
4. **Model বদলালে ফল বদলায়।** SWE-agent-এর Claude 3.5 Sonnet দিয়ে 23.00%, GPT-4 দিয়ে 18.00% — তাই "কোন approach ভালো" আর "কোন model ভালো" আলাদা করা কঠিন। Controlled comparison (একই model, একই সেটিং) খুব কম।

---

## ৩. Reliability ও Assurance-এর প্রমাণ — চারটা Paper কী বলে

এটাই এই summary-র সবচেয়ে গুরুত্বপূর্ণ অংশ, কারণ আমাদের domain-এর নাম "Reliability and Assurance"।

### ৩.১ "Resolved" ≠ "Correct" (Patch overfitting)

| Paper | প্রমাণ |
|---|---|
| SWE-bench | গড়ে মাত্র 9.1টা F2P test; প্রায় 60% task-এ মাত্র ১টা F2P test — দুর্বল test ভুল patch-কেও pass করাতে পারে |
| SWE-agent | Unresolved instance-এর 12.1% "Overly Specific Implementation" — patch শুধু নির্দিষ্ট case ঠিক করে |
| AutoCodeRover | Test pass করা 78টা patch হাতে যাচাই করে মাত্র **51টা (65.4%) আসলে সঠিক** — বাকি 27টা overfitting |
| Agentless | 40টা candidate-এর মধ্যে কোনো একটা সঠিক হলে 126টা (42.0%) solve হতো, কিন্তু বাছাই করে পেয়েছে 96টা — **সঠিক patch হাতে থেকেও বাছাইয়ে হারায়** |

**সারকথা:** Test-based evaluation যথেষ্ট নয়। AutoCodeRover-এর 65.4% সংখ্যাটা খুব শক্ত motivation — প্রতি ৩টা "solved" patch-এর ১টা আসলে ভুল হতে পারে।

### ৩.২ Run-to-run Consistency (Non-determinism)

| Paper | প্রমাণ |
|---|---|
| SWE-agent | Lite-এ 6 বার চালিয়ে গড় 17.94% ± 0.49, কিন্তু pass@6 = 32.67% — অর্থাৎ অনেক instance কোনো run-এ solve হয়, কোনোটায় হয় না |
| AutoCodeRover | @1 = 19.00% কিন্তু @3 = 26.00% — তিনবার চালালে অনেক বেশি |
| Agentless | একটা run-ই report করেছে; variance মাপা হয়নি |

**সারকথা:** গড় score stable দেখালেও **কোন নির্দিষ্ট issue solve হবে তা অনিশ্চিত**। একজন developer-এর কাছে এটাই আসল reliability প্রশ্ন। কোনো paper-ই pass^k (k বারের সবকটাতেই সফল) report করেনি।

### ৩.৩ Agent-এর নিজের Test-এর মান

| Paper | প্রমাণ |
|---|---|
| SWE-agent | 2.4% failure "Can't Reproduce"; কিছু ক্ষেত্রে test না চালিয়েই submit |
| AutoCodeRover | SBFL ও validation-এর জন্য developer test লাগে — যা বাস্তবে সবসময় থাকে না, আর SWE-bench-এর evaluation test-এর সাথে মিলে গেলে leakage-এর সন্দেহ |
| Agentless | 213টা issue-তে reproduction test bug reproduce করেছে, কিন্তু মাত্র 94টা gold patch-এ pass করে — **অর্ধেকের বেশি generated test নিজেই ভুল** |

### ৩.৪ Benchmark-এর নিজের মান

| Paper | প্রমাণ |
|---|---|
| SWE-bench | Python-only, binary metric, contamination-এর দুর্বল প্রমাণ (নিজের critique) |
| Agentless | Lite-এর 4.3% issue-তে exact solution লেখা, 10.0%-এ যথেষ্ট তথ্য নেই, 5.0%-এ misleading solution → এগুলো বাদ দিয়ে **Lite-S (249 task)** |

### ৩.৫ কী কেউ দেখেনি

চারটা paper-এর কোনোটাই agent-এর patch-এর **security** (নতুন vulnerability তৈরি হলো কিনা) বা **maintainability/code quality** পদ্ধতিগতভাবে মাপেনি। SWE-bench-এর appendix-এ cyclomatic complexity-র একটা উদাহরণ ছাড়া এ বিষয়ে কিছু নেই।

---

## ৪. Common Research Gaps (সব Paper মিলিয়ে)

| # | Gap | কোন paper-এর প্রমাণ | কোন sub-domain-এ আরও পড়তে হবে | গুরুত্ব |
|---|---|---|---|---|
| CG1 | **Plausible patch-এর correctness যাচাই (overfitting detection)** | 01, 02, 03, 04 — চারটাই | Patch Validation; Automated Program Repair | ⭐⭐⭐⭐⭐ |
| CG2 | **Candidate patch selection / re-ranking** | 04 (126 vs 96), 03 (@1 vs @3) | Patch Validation; LLM Test Generation (Oracle-Guided Program Selection) | ⭐⭐⭐⭐⭐ |
| CG3 | **Generated reproduction test-এর মান** | 04 (213 → 94), 02, 03 | LLM Test Generation | ⭐⭐⭐⭐ |
| CG4 | **Run-to-run reliability (pass^k, flip rate)** | 02, 03 | Coding-Agent Evaluation & Reliability | ⭐⭐⭐⭐ |
| CG5 | **Patch-এর security ও quality** | কেউ মাপেনি | Security of AI-Generated Code | ⭐⭐⭐⭐ |
| CG6 | **Benchmark quality ও contamination** | 01, 04 | Coding-Agent Evaluation & Reliability (SWE-rebench, SWE-Bench Pro) | ⭐⭐⭐ |
| CG7 | **Confidence ও abstention** — agent কখন বলবে "আমি নিশ্চিত নই" | 03, 04 (নিজের প্রস্তাব) | Trustworthy AI for SE | ⭐⭐⭐ |
| CG8 | **Evaluation-এর সমতা** — একই model, একই খরচের হিসাব | 02 বনাম 03/04-এর ভিন্ন cost | Coding-Agent Evaluation & Reliability | ⭐⭐⭐ |

---

## ৫. এই Sub-domain থেকে সবচেয়ে ভালো Research Direction (প্রাথমিক মত)

> ⚠️ এটা শুধু ১ম sub-domain-এর ভিত্তিতে। বাকি ৬টা sub-domain পড়ার পর চূড়ান্ত সিদ্ধান্ত নেবো। বিশেষ করে Patch Validation, LLM Test Generation ও Security sub-domain এই direction-কে শক্ত বা দুর্বল করতে পারে।

### প্রস্তাবিত direction: "Assurance Layer for AI Coding Agent Patches"

**মূল idea:** একটা agent যে patch দেয়, সেটা test pass করলেই গ্রহণ না করে একটা **assurance layer** দিয়ে যাচাই করা, যেটা বলবে patch-টা কতটা বিশ্বাসযোগ্য।

| Component | কী করবে | কোন gap |
|---|---|---|
| 1. Extra test generation | Patch-এর জন্য বাড়তি test তৈরি করে overfitting ধরা | CG1, CG3 |
| 2. Candidate re-ranking | Agentless-এর 40টা candidate থেকে ভালো patch বাছাই | CG2 |
| 3. Security ও quality scan | Bandit/Semgrep, complexity metric | CG5 |
| 4. Consistency check | একাধিক run-এ ফল মিলছে কিনা | CG4 |
| 5. Confidence score ও abstention | সব signal মিলিয়ে একটা score; কম হলে মানুষকে জানানো | CG7 |

**কেন এটা SPL3-এর জন্য ভালো:**
1. **সরাসরি domain-এর নামের সাথে মেলে** — "Reliability and Assurance"।
2. **খরচ কম রাখা যায়:** Agentless ও AutoCodeRover-এর patch public, তাই নতুন করে বড় agent চালাতে হবে না; offline experiment করা যায়।
3. **পরিষ্কার baseline আছে:** Agentless-এর majority voting (96) আর upper bound (126) — উন্নতি সহজে মাপা যায়।
4. **পরিষ্কার motivation সংখ্যা আছে:** AutoCodeRover-এর 65.4% correctness rate।
5. **Software হিসেবে অন্যরা ব্যবহার করতে পারবে** — যেকোনো agent-এর patch দিলে assurance report দেবে।

**সম্ভাব্য evaluation:** SWE-bench Lite / Lite-S / Verified-এর একটা subset; metric — re-ranking-এর পরে resolved সংখ্যা, overfitting detection-এর precision/recall, security finding সংখ্যা, pass^k।

---

## ৬. SPL3 Implementation — এই Sub-domain থেকে কী Software বানাবো

| ধাপ | কাজ | উৎস paper |
|---|---|---|
| 1 | SWE-bench Lite/Verified load করা ও official Docker harness দিয়ে evaluate করা | 01 |
| 2 | Agentless pipeline (open-source) চালানো বা তাদের প্রকাশিত patch ব্যবহার করা — সবচেয়ে reproducible baseline | 04 |
| 3 | তুলনার জন্য SWE-agent ও AutoCodeRover-এর প্রকাশিত patch সংগ্রহ | 02, 03 |
| 4 | Localization accuracy (file/function/line) মাপার module | 04 |
| 5 | (Gap solve) Assurance layer — উপরের ৫টা component | নিজেদের কাজ |
| 6 | Dashboard: resolved, plausible-বনাম-correct, security, consistency | নিজেদের কাজ |

**Practical সতর্কতা:** Windows-এ WSL2 + Docker লাগবে; পুরো benchmark না চালিয়ে ছোট subset দিয়ে শুরু; LLM API খরচের হিসাব আগে করে রাখা।

---

## ৭. Supervisor-এর সম্ভাব্য প্রশ্ন ও উত্তর (Sub-domain স্তরে)

**Q1. চারটা paper-এর মধ্যে সম্পর্ক কী?**
A: SWE-bench মাপার মানদণ্ড দিয়েছে; SWE-agent দেখিয়েছে interface design গুরুত্বপূর্ণ; AutoCodeRover দেখিয়েছে SE জ্ঞান (AST, SBFL) কাজে লাগালে সস্তায় ভালো ফল; Agentless দেখিয়েছে জটিল agent ছাড়াই সরল pipeline আরও ভালো করে, আর benchmark-এর নিজেরই ত্রুটি আছে।

**Q2. Agent না Agentless — কোনটা ভালো?**
A: এই paper-গুলোর সময়ে SWE-bench Lite-এ Agentless (32.00%) সব open-source agent-এর চেয়ে ভালো ও সস্তা। তবে Agentless নিজেই স্বীকার করেছে যে issue-তে কোনো location clue না থাকলে জটিল search tool-ওয়ালা agent ভালো করে। তাই উত্তর task-এর ধরনের উপর নির্ভর করে।

**Q3. তোমার মতে এই sub-domain-এর সবচেয়ে বড় দুর্বলতা কী?**
A: সবাই "test pass করা"-কে সফলতা ধরে। কিন্তু AutoCodeRover নিজেই দেখিয়েছে test pass করা patch-এর মাত্র 65.4% আসলে সঠিক। Patch-এর correctness, security ও consistency কেউ পদ্ধতিগতভাবে যাচাই করেনি।

**Q4. তুমি কোন gap নিয়ে কাজ করতে চাও এবং কেন?**
A: প্রাথমিকভাবে agent patch-এর জন্য একটা assurance layer — overfitting detection, re-ranking, security scan ও consistency check মিলিয়ে। কারণ এটা domain-এর নামের সাথে সরাসরি মেলে, public data দিয়ে কম খরচে করা যায়, আর Agentless-এর 96 বনাম 126 একটা পরিষ্কার মাপার জায়গা দেয়। তবে বাকি sub-domain পড়ার পর চূড়ান্ত করবো।

**Q5. Localization কেন এত গুরুত্বপূর্ণ?**
A: Agentless Table 1-এ দেখা যায় যাদের function-level localization ভালো, তাদের resolve rate-ও ভালো (RAG 23.3% → Agentless 52.0%)। ভুল জায়গায় edit করলে সঠিক patch সম্ভব নয়।

**Q6. এই paper-গুলোর ফল কি সরাসরি তুলনা করা যায়?**
A: পুরোপুরি না। ভিন্ন LLM, ভিন্ন সময়, ভিন্ন খরচের হিসাব (যেমন SWE-agent-এর খরচ এক paper-এ 1.67, অন্যটায় 2.51 USD)। তাই আমি তুলনার জন্য একটা উৎস (Agentless Table 1) ব্যবহার করেছি এবং সীমাবদ্ধতা উল্লেখ করেছি।

---

## ৮. বর্তমান (2026) প্রেক্ষাপট — আজকের Agent-দের সাথে তুলনা

> **উৎস:** `00_Current_State_2026_Sources.md` (2026-10-28-এ সংকলিত, প্রতিটা তথ্যের URL সহ)। "কোম্পানির দাবি" মানে model বানানো কোম্পানি নিজে মেপেছে; "স্বাধীন" মানে তৃতীয় পক্ষ (Vals.ai, Scale, Nebius ইত্যাদি) একই harness-এ মেপেছে। প্রতিটা paper-এর বিস্তারিত তুলনা সেই paper-এর section ২১-এ।

### ৮.১ তখন বনাম এখন

| দিক | Paper-এর সময় (2023–2024) | এখন (October 2026) |
|---|---|---|
| সেরা model/agent | GPT-4, Claude 2/3, GPT-4o | Claude Opus 5.5, Fable 5.1, Sonnet 5.5; GPT-6 family (Astra, Sol, Luna, 6.1 Terra); Gemini 4 Argon; open-weight Kimi K3.1 Pro, GLM-5.x, DeepSeek V4 |
| Agent product | গবেষণার prototype (SWE-agent, AutoCodeRover, Agentless) | বাণিজ্যিক agent: Claude Code, OpenAI Codex, Gemini CLI, Cursor, Devin, OpenHands; গবেষণায় standard harness এখন **mini-SWE-agent** (SWE-agent-এর উত্তরসূরি) |
| SWE-bench (full) | Claude 2: 1.96% | — (আর report হয় না) |
| SWE-bench Lite | Agentless 32.00% | Official board-এর শেষ entry September 2025, সেরা 60.33%; labs এখন আর Lite report করে না |
| SWE-bench Verified | — | Official board-এ February 2026-এ সেরা 79.2%; Vals.ai-তে Claude Opus 5 97.0% (স্বাধীন, September 2026) — তারপর Vals benchmark-টা "saturated" বলে বন্ধ করেছে; OpenAI February 2026-এ Verified-এ evaluate করা বন্ধ করেছে (contamination আর flawed test-এর কারণে) |
| এখনকার প্রধান benchmark | — | Terminal-Bench 4.0, SWE-Bench Pro, DeepSWE, FrontierCode, CursorBench |

### ৮.২ আজকের Agent-দের Score (একই harness-এ স্বাধীনভাবে মাপা)

| Benchmark | Model | Score | উৎস |
|---|---|---|---|
| Terminal-Bench 4.0 | Claude Opus 5.5 | 65.15% (প্রতি task প্রায় 13.20 USD) | Vals.ai, Oct 2026 |
| Terminal-Bench 4.0 | Claude Sonnet 5.5 | 64.14% | Vals.ai |
| Terminal-Bench 4.0 | Kimi K3.1 Pro (open) | 63.64% (4.57 USD) | Vals.ai |
| Terminal-Bench 4.0 | GPT-6 Astra | 59.60% | Vals.ai |
| Terminal-Bench 4.0 | Gemini 4 Argon | 57.58% | Vals.ai |
| SWE-Bench Pro (public) | সেরা entry (Muse Spark 1.1) | 61.50 ± 3.10 | Scale leaderboard; এখানে Opus 5.5, GPT-6 বা Gemini 4-এর entry নেই |
| SWE-Bench Pro | Claude Opus 5.5 | 89.9% | **কোম্পানির দাবি** (Opus 5.5 System Card) — স্বাধীন board-এর সেরার চেয়ে প্রায় 28 point বেশি |

### ৮.৩ Sub-domain 1-এর Common Gap — 2026-এ অবস্থা

| CG | Gap | 2026-এ অবস্থা | প্রমাণ |
|---|---|---|---|
| CG1 | Plausible patch-এর correctness | **খোলা** | PatchDiff (ICSE 2026): plausible patch-এর 29.6% gold patch থেকে আলাদা আচরণ করে; বর্তমান model-এ আবার মাপা হয়নি |
| CG2 | Candidate re-ranking | **খোলা** | SWE-rebench-এ pass@1 আর pass@5-এর ফাঁক 12–18 point — অর্থাৎ সঠিক সমাধান প্রায়ই কোনো একটা run-এ আসে, কিন্তু বাছাই হয় না |
| CG4 | Run-to-run reliability | **খোলা** | SWE-rebench-এর ফাঁক উপরে; prompt-এর অর্থ না বদলে শুধু ভাষা বদলালে ফলাফলের ওঠানামা একই prompt বারবার চালানোর চেয়ে 11–58 গুণ বেশি (Noise Floor Audit, Aug 2026) |
| CG5 | Security | **খোলা, বর্তমান model-এর তথ্য প্রায় নেই** | SusVibes-এ পুরনো agent-দের functional pass 62–84%, কিন্তু secure pass মাত্র 7.8–17.3%; Opus 5.5/GPT-6-এর ফল পাওয়া যায়নি |
| CG6 | Benchmark quality ও contamination | **খোলা, এখন কোম্পানিগুলোও স্বীকার করছে** | OpenAI Verified বাদ দিয়েছে; Vals archive করেছে; Opus 5.5 card-এ Verified নেই |
| CG8 | Evaluation-এর সমতা | **আরও খারাপ** | কোম্পানির দাবি আর স্বাধীন মাপের মধ্যে বড় ফাঁক (উপরের table); একই model-এর score শুধু harness বদলালে 29.8 point পর্যন্ত বদলায় |

### ৮.৪ এর অর্থ — আমার পর্যবেক্ষণ
1. **প্রশ্নটা "কত % solve" থেকে "কতটা বিশ্বাসযোগ্য"-তে সরে গেছে।** পুরনো benchmark-এ score ছাদ ছুঁয়েছে (97%), কিন্তু সেই score-এর কতটা আসল তা নিয়েই এখন সন্দেহ। আমাদের assurance direction তাই 2023-এর চেয়ে আজ আরও বেশি প্রাসঙ্গিক।
2. **আমাদের experiment বর্তমান model দিয়ে করতে হবে, তবে খরচ মাথায় রেখে।** Opus 5.5-এর Terminal-Bench task-প্রতি খরচ প্রায় 13.20 USD; GPT-6.1 Sol প্রায় 1.72 USD; open-weight Kimi K3.1 Pro প্রায় 4.57 USD (Vals.ai)। ছোট subset আর সস্তা বর্তমান model দিয়ে শুরু করা বাস্তবসম্মত।
3. **"কোম্পানির দাবি" আর "স্বাধীন মাপ" সবসময় আলাদা করে লিখতে হবে।** Supervisor-কে কোনো score দেখানোর সময় এটা না বললে ভুল ধারণা তৈরি হবে।

---

## ৯. পরের ধাপ

1. **Sub-domain 2: Automated Program Repair** — overfitting ও patch correctness-এর ঐতিহাসিক প্রেক্ষাপট বুঝতে।
2. বিশেষ নজর দেবো: **Patch Validation** ও **LLM Test Generation** sub-domain-এ, কারণ CG1, CG2 ও CG3-এর সমাধান সেখানে থাকতে পারে।
3. প্রতিটা sub-domain শেষে এই direction শক্ত হলো না দুর্বল হলো, তা আপডেট করবো।
