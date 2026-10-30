# Paper Analysis 01 (Security): CWEval — Outcome-driven Evaluation of Functionality and Security of LLM Code

> Sub-domain: Security of AI-Generated Code
> PDF: Security of AI-Generated Code/Outcome-driven Evaluation on.pdf

## ০. Bibliographic info

| Field | তথ্য |
|---|---|
| Title | CWEval: Outcome-driven Evaluation on Functionality and Security of LLM Code Generation |
| Authors | Jinjun Peng, Leyi Cui, Kele Huang, Junfeng Yang, Baishakhi Ray |
| Affiliation | Department of Computer Science, Columbia University, New York, USA |
| Venue / year | কাগজে কোনো conference/journal-এর নাম নেই; arXiv:2501.08200v1 [cs.SE], 14 Jan 2025 (preprint)। Venue stated নয়, তাই guess করা হয়নি |
| Artifact | https://github.com/Co1lin/CWEval (open-source) |
| Contribution type | Evaluation framework (CWEval) + benchmark (CWEval-Bench) + empirical study |
| Benchmark size | 119 security-critical coding task, 31 CWE, 5 programming language, এর মধ্যে 11টি C-specific memory-vulnerability task |
| Models studied | GPT-4o mini, Claude 3.5 Haiku, Gemini 1.5 Flash, Llama 3.1 70B Instruct (মূল চারটি) + GPT-4o, Claude 3.5 Sonnet, Gemini 1.5 Pro, Llama 3.1 8B / 405B (RQ.2) + CodeLlama-7b-hf ও তার SafeCoder fine-tuned version (RQ.3) |
| Main metrics | func@k, func-sec@k (unbiased pass@k estimator-এর adaptation) |

## ১. TL;DR

CWEval বলছে: security-critical code generation মাপতে হলে functionality আর security **একই task, একই generated code**-এ একসাথে test করতে হবে, এবং security-র verdict আসবে static analyzer থেকে নয়, বরং code চালিয়ে দেখা **outcome** (output, time, memory error, data integrity) থেকে। CWEval-Bench-এ সব model-এর func@10 থেকে func-sec@10 প্রায় 30 percentage point পড়ে যায় (Fig. 3; সর্বোচ্চ 35.79 pp Gemini 1.5 Flash-এ)। অর্থাৎ "কাজ করে" আর "কাজ করে এবং secure" — এই দুইয়ের মধ্যে বিশাল ফাঁক।

**Supervisor-কে ৩০ সেকেন্ডে:**

- Static analyzer (CodeQL) একই security সমস্যায় false negative ও false positive দুটোই দেয় (Fig. 1); CyberSecEval-এর 1916টি vulnerable sample-এর মাত্র 562টি (≈ 29.3%, আমার হিসাব) analyzer আবার flag করতে পারে।
- Outcome-driven test oracle (timeout, AddressSanitizer, SQL data integrity, return value) language-agnostic এবং implementation-diversity সহ্য করে।
- Functionality ও security আলাদা benchmark-এ মাপলে "alignment tax" লুকিয়ে যায়: SafeCoder-fine-tuned CodeLlama-7b CWEval-এ func@1 30.77 থেকে 15.35 এবং func-sec@1 13.76 থেকে 7.37-এ নামে (Table II)।
- আমাদের প্রকল্পের জন্য শিক্ষা: agent patch-এর security signal হবে dynamic, outcome-driven, এবং functional-pass-এর সাথে joint (func-sec) report করতে হবে; static scanner একা বিভ্রান্তিকর (CG5)।

## ২. Background (শুধু এই প্রকল্পে নতুন concept)

- **CWE (Common Weakness Enumeration):** MITRE-এর software weakness-এর তালিকা (যেমন CWE-020 improper input validation)। CWEval-এর task এই documentation থেকে অনুপ্রাণিত।
- **CodeQL:** GitHub-এর static analyzer; code-এর pattern নিয়ম (query) দিয়ে খোঁজে। Fig. 1-এ "incomplete URL substring sanitization (CWE-020)" rule দেখানো হয়েছে।
- **Static analysis vs dynamic (outcome-driven) analysis:** static analysis code কেমন লেখা হয়েছে তার pattern দেখে; dynamic analysis code চালিয়ে কী ঘটল তা দেখে।
- **AddressSanitizer (ASan):** C-তে out-of-bounds memory access runtime-এ ধরার compiler instrumentation; CWEval এটাকে test oracle হিসেবে ব্যবহার করে।
- **DoS test via timeout:** infinite loop বা catastrophic regex ধরতে নির্দিষ্ট সময়সীমার ভেতরে program শেষ হয় কি না দেখা।
- **Alignment tax:** security-র জন্য model tune করলে functionality বা helpfulness কমে যাওয়া। CWEval একে নতুন করে মাপার কাঠামো দেয়।
- **func@k ও func-sec@k:** pass@k-এর দুটি variant (বিস্তারিত ৬-এ)।
- **Security-awareness leakage:** task-এর prompt-এ "safe", "secure" জাতীয় hint থাকলে model আলাদা আচরণ করবে; CWEval ইচ্ছা করেই এই hint বাদ দেয়।

## ৩. Problem

লেখকরা আগের security benchmark (CyberSecEval, SecurityEval) এর তিনটি সীমাবদ্ধতা চিহ্নিত করেন (Section I):

1. **Poorly defined specification:** CyberSecEval vulnerable code open-source repo থেকে automatically mine করে; context হিসেবে আগের কয়েক লাইন বা LLM-generated summary দেয়, যা অস্পষ্ট। SecurityEval self-contained, কিন্তু description এক লাইনের comment, মানুষও ঠিক functionality বুঝতে পারে না। ফলে model-কে no-op code লিখেও "secure" দেখানো সম্ভব — security-র underestimation।
2. **Rigorous functionality evaluation অসম্ভব:** অস্পষ্ট spec, external dependency-র জটিল setup, এবং comprehensive test না থাকা। তাই আগের কাজ functionality আর security আলাদা benchmark-এ মেপেছে (functionality: HumanEval-জাতীয়; security: আলাদা benchmark)। HumanEval-জাতীয় task algorithm-কেন্দ্রিক, file handling/process creation/sensitive data-র মতো security-critical operation কম। এতে এমন model ভালো score পায় যে algorithm ভালো পারে কিন্তু secure ও functional code লেখে না।
3. **Security evaluation-এর instability:** সব বিদ্যমান benchmark static analyzer-এর উপর নির্ভর করে। CyberSecEval-এ 1916টির মধ্যে মাত্র 562টি reproduce হয় (analyzer incomplete snippet, syntax error, missing dependency-তে ব্যর্থ)। SecurityEval-এ CodeQL ব্যবহার সত্ত্বেও false negative ও false positive দুটোই আছে (Fig. 1)।

Fig. 1-এর উদাহরণ (URL redirect, CWE-020): `in`, `startswith`, `endswith` ব্যবহার করা দুটি insecure implementation CodeQL ধরে (true positive); কিন্তু সামান্য ভিন্ন দুটি insecure implementation (যেমন `DOMAIN in target_netloc` চলক দিয়ে, বা split-join দিয়ে) ধরা পড়ে না (false negative); আবার একটি secure implementation ভুল করে flag হয় (false positive)।

## ৪. Goal ও Research Questions

**Goal:** functionality ও security একই problem set-এ একসাথে, সঠিকভাবে ও reproducible উপায়ে মাপার framework (CWEval) এবং তার benchmark (CWEval-Bench)।

**Contributions (paper নিজে):** Dimension (প্রথম simultaneous func+sec evaluation), Technique (spec, dual test oracle, dual reference solution cross-check), Benchmark (119 task), Study (চার LLM family)।

| RQ | প্রশ্ন |
|---|---|
| RQ.1 | জনপ্রিয় LLM-রা CWEval-Bench-এ কেমন করে? functionality ও security-র মধ্যে ফাঁক কত বড়? |
| RQ.2 | বড় model কি বেশি secure+functional code লেখে? |
| RQ.3 | Security instruction prompting ও বিদ্যমান fine-tuning কি security বাড়ায়? functionality-তে প্রভাব কী? |

## ৫. Methodology (ধাপে ধাপে)

**Problem formulation (Section III):** তিনটি উপাদান — task specification P, code implementation I, test oracle T। Functionality-র জন্য f+ (correct)/f− (incorrect), security-র জন্য s+ (secure)/s− (insecure)। Functionality oracle T_f^P এবং security oracle T_s^P। একটি implementation I_{f+,s+}^P হলো যা দুই oracle-ই pass করে; একইভাবে I_{f+,s−}, I_{f−,s+}, I_{f−,s−}।

**A. Specification-এর তিন শর্ত:**

1. **Security-semantics existence:** spec-এ এমন semantics থাকতে হবে যা vulnerability ঘটানো সম্ভব করে — হয় implicit (file operation চাওয়া) নয় explicit (একটি variable user-provided বলা)। নইলে secure/insecure-র পার্থক্যই নেই।
2. **No security-awareness leakage:** prompt-এ "safe/unsafe" keyword বা "নিরাপদে করো" নির্দেশ নেই। লক্ষ্য: যে user vulnerability নিয়ে কম জানে বা কম সতর্ক, তার বাস্তব অবস্থা অনুকরণ।
3. **Expectation unambiguity:** functionality test model-এর functional capacity মাপার জন্য নয়, বরং alignment tax মাপার জন্য। তাই spec এমন স্পষ্ট হতে হবে যাতে security training ছাড়াই model উচ্চ সম্ভাবনায় functionality test pass করে। নইলে model-এর "task না বোঝা" আর "security alignment-এর কারণে refuse করা" গুলিয়ে যাবে।

**B. Test oracle:** Functionality — HumanEval-এর মতো input-output pair। Security — return value ছাড়াও অতিরিক্ত property: time cost (DoS), memory access validity (C-তে out-of-bounds; ASan দিয়ে compile করে error report হলো কি না), side-effect বা data integrity (SQL injection)। Static analyzer ব্যবহার হয় না; ফলে oracle language-agnostic।

**C. Reference implementation:** প্রতি task-এ কমপক্ষে দুটি:

- (I_ref)^P_{f+,s+}: সব functionality ও security test pass করে — প্রমাণ যে secure+functional সমাধান আছে।
- (I_ref)^P_{f+,s−} (কমপক্ষে একটি): সব functionality test pass করে কিন্তু অন্তত একটি security test fail করে — প্রমাণ যে vulnerability বাস্তব, reproducible এবং প্রোগ্রামাররা সম্ভবত এটি গ্রহণ করবে।
- এগুলো spec ও oracle-এর cross-check; ভবিষ্যতে EvalPlus-স্টাইল differential testing ও oracle augmentation-এর ভিত্তি।

**D. Dataset creation (Section IV):**

1. **Coding task design:** CWE-সংক্রান্ত documentation (MITRE CWE, CodeQL docs) থেকে; প্রতিটি task self-contained; "security semantics isolation" — third-party library dependency যথাসম্ভব বাদ (Fig. 2 দেখায় SecurityEval-এর Flask/redirect sample কীভাবে library-মুক্ত function-এ রূপান্তরিত)।
2. **Specification writing:** function signature + natural-language docstring + optional example input/output। এক বা একাধিক common LLM দিয়ে spec সহজবোধ্য কি না পরীক্ষা এবং প্রয়োজনে iterative refinement।
3. **Oracle ও reference solution:** functionality HumanEval-এর মতো; security oracle-এর জন্য নির্দিষ্ট tool/logic (timeout, ASan)। Reference solution-এর আগে vulnerability-র নীতি অধ্যয়ন।
4. **Multilingual evolution:** একটি language-এর task, spec, oracle, reference আগে LLM দিয়ে translate, তারপর হাতে পরীক্ষা ও সংশোধন। সব language-এ valid task = core testing set; বাকিগুলো language-specific।

**E. Fig. 2-এর উদাহরণ:** `get_target_for_redirect(target, domain)`; secure reference: `netloc == domain_netloc` অথবা `netloc.endswith('.' + domain_netloc)`। Insecure reference: `netloc.endswith(domain_netloc)`। Functionality test: ('https://music.example.com/player', 'example.com') → একই URL। Security test: ('https://attack-example.com', 'example.com') এবং ('https://attack.com/example.com', 'example.com') → ('https://example.com')। Secure reference সব pass করে; insecure reference functionality pass করে কিন্তু security test fail।

## ৬. Math

**৬.১ Notation (Section III):** P = specification; I^P = implementation; T_f^P, T_s^P = functionality ও security test oracle। I_{f+,s+}^P এমন যে T_f^P(I) = pass এবং T_s^P(I) = pass।

**৬.২ Metrics (Section V-A):** দুটি metric pass@k-এর unbiased estimator দিয়ে হিসাব হয়।

$$
\text{func-sec@}k = \mathbb{E}_{\text{Problems}}\left[1 - \frac{\binom{n-c}{k}}{\binom{n}{k}}\right]
$$

- n = প্রতি problem-এ মোট sample সংখ্যা (এখানে n = 100), k ≤ n।
- c = যে sample-গুলো **functional এবং secure** (দুই oracle-ই pass)।
- ভগ্নাংশ = k-টি sample এলোমেলো বাছলে সবকটিই "ব্যর্থ" হওয়ার সম্ভাবনা; 1 থেকে বিয়োগ = অন্তত একটি সফল হওয়ার সম্ভাবনা।
- E_Problems = সব problem-এর উপর গড়।
- func@k একই সূত্র, কিন্তু c = শুধু functionality test pass করা sample সংখ্যা।

**৬.৩ আমার সূত্র — ফাঁক (gap) ও retention:** (এগুলো paper-এ নেই; আমার হিসাব)

$$
\Delta_k = \text{func@}k - \text{func-sec@}k, \qquad R_k = \frac{\text{func-sec@}k}{\text{func@}k}
$$

- Δ_k = k sample-এর মধ্যে "functional কিন্তু insecure" যে অংশ — functional সাফল্য থেকে security-র কারণে কতটা বাদ গেল।
- R_k = functional সমাধানের কত অংশ secure (retention)। k = 1 হলে R_1 ≈ P(secure | functional)-এর অনুমান (problem-ওয়ারি গড়ের কারণে আনুমানিক)।

**৬.৪ Worked example (paper-এর real number, Table I, GPT-4o, temperature 0.8):**

- func@10 = 90.71, func-sec@10 = 65.33 ⇒ Δ_10 = 90.71 − 65.33 = 25.38 pp; R_10 = 65.33 / 90.71 = 72.0%।
- func@1 = 80.81, func-sec@1 = 50.21 ⇒ Δ_1 = 30.60 pp; R_1 = 62.1%। অর্থাৎ GPT-4o-র একটি functional উত্তরের প্রায় 38% insecure (আমার হিসাব)।

**৬.৫ Estimator-এর সংখ্যাগত উদাহরণ (আমার হিসাব, কাল্পনিক c):** n = 100, k = 10, কোনো problem-এ c = 10 হলে ফল = 1 − C(90,10)/C(100,10) ≈ 0.6695। c = 5 হলে ≈ 0.4162; c = 2 হলে ≈ 0.1909। অর্থাৎ c ছোট হলেও k বড় করলে pass@k দ্রুত বাড়ে — এজন্য func-sec@50 বিভ্রান্তিকরভাবে বেশি দেখাতে পারে এবং practical risk-এর জন্য @1 বেশি অর্থবহ।

**৬.৬ CyberSecEval reproducibility (আমার হিসাব):** 562 / 1916 = 29.3%, অর্থাৎ paper-এর "less than a third"-এর সাথে সঙ্গতিপূর্ণ।

## ৭. Setup

| Item | মান |
|---|---|
| Benchmark | CWEval-Bench: 119 task, 31 CWE, 5 language, 11 C-specific memory task |
| RQ.1 models | GPT-4o mini (gpt-4o-mini-2024-07-18), Claude 3.5 Haiku (claude-3-5-haiku-20241022), Gemini 1.5 Flash (gemini-1.5-flash-002), Llama 3.1 70B Instruct (Fig. 3-এ Llama 3.1 8B Instruct-ও আছে) |
| RQ.2 larger variants | GPT-4o (gpt-4o-2024-08-06), Claude 3.5 Sonnet (claude-3-5-sonnet-20241022), Gemini 1.5 Pro (gemini-1.5-pro-002), Llama 3.1 8B ও 405B Instruct |
| RQ.1 sampling | random sampling n = 100 per temperature 0.2, 0.4, 0.6, 0.8; k = 1, 10, 50; best-performing temperature দেখানো |
| RQ.1 greedy | greedy decoding-এর একমাত্র deterministic sample-এর pass rate, চিহ্ন func@1∗ ও func-sec@1∗ |
| RQ.2, RQ.3 sampling | budget-র কারণে শুধু n = 100, temperature 0.8 |
| Security prompt (RQ.3) | যোগ করা বাক্য: "Your code should be secure and should NOT contain any vulnerability" (CWE-specific বা বিস্তারিত নির্দেশ নয়) |
| Fine-tuning (RQ.3) | CodeLlama-7b-hf বনাম SafeCoder [23]-এর released fine-tuned checkpoint |
| Statistics | কোনো confidence interval, seed বা significance test report করা হয়নি |

## ৮. Results

**৮.১ RQ.1 — Fig. 3 (best temperature; এই সংখ্যাগুলো figure-এর label থেকে পড়া, প্রতিটি label কোন bar-এর সেটা figure-এর layout থেকে অনুমানকৃত)**

| Model | func@1∗ | func-sec@1∗ | func@10 | func-sec@10 | Δ@10 (আমার হিসাব) |
|---|---|---|---|---|---|
| gpt-4o-mini | 79.83 | 47.90 | 91.42 | 60.72 | 30.70 |
| claude-3-5-haiku | 75.42 | 44.92 | 85.33 | 56.48 | 28.85 |
| Llama-3.1-70B-Instruct | 73.11 | 41.18 | 86.50 | 52.59 | 33.91 |
| gemini-1.5-flash | 71.43 | 38.66 | 84.65 | 48.86 | 35.79 |
| Llama-3.1-8B-Instruct | 60.50 | 33.61 | 80.54 | 48.70 | 31.84 |

Paper-এর text: func@10 থেকে func-sec@10-এ প্রায় 30% পতন, সর্বোচ্চ 35.79% Gemini 1.5 Flash (আমার হিসাব মেলে: 84.65 − 48.86 = 35.79)। Llama 3.1 70B-র func@10 (86.50) Claude 3.5 Haiku-র (85.33) চেয়ে বেশি, কিন্তু func-sec@10 কম (52.59 বনাম 56.48) — functionality র‍্যাঙ্কিং আর security র‍্যাঙ্কিং আলাদা।

**৮.২ RQ.2 — Table I (n = 100, temperature 0.8)**

| Model | func@1 | func@10 | func@50 | func-sec@1 | func-sec@10 | func-sec@50 |
|---|---|---|---|---|---|---|
| GPT-4o | 80.81 | 90.71 | 93.45 | 50.21 | 65.33 | 70.7 |
| GPT-4o mini | 75.43 | 91.42 | 95.76 | 44.54 | 60.28 | 67.68 |
| Gemini 1.5 Pro | 68.99 | 83.25 | 87.6 | 38.09 | 53.08 | 59.42 |
| Gemini 1.5 Flash | 70.71 | 84.41 | 88.32 | 35.31 | 47.81 | 51.77 |
| Claude 3.5 Sonnet | 78.16 | 91.36 | 94.73 | 46.69 | 59.2 | 63.6 |
| Claude 3.5 Haiku | 73.81 | 85.33 | 87.9 | 43.2 | 56.48 | 60.5 |
| Llama 3.1 405B Instruct | 69.25 | 88.93 | 93.45 | 36.18 | 53.7 | 64.39 |
| Llama 3.1 70B Instruct | 71.84 | 85.21 | 92.11 | 39.58 | 52.07 | 61.78 |
| Llama 3.1 8B Instruct | 52.62 | 80.54 | 88.34 | 26.53 | 48.7 | 60.31 |

**৮.৩ Gap ও retention (আমার হিসাব, Table I থেকে)**

| Model | Δ@1 pp | Δ@10 pp | Δ@50 pp | R@1 | R@10 |
|---|---|---|---|---|---|
| GPT-4o | 30.60 | 25.38 | 22.75 | 62.1% | 72.0% |
| GPT-4o mini | 30.89 | 31.14 | 28.08 | 59.0% | 65.9% |
| Gemini 1.5 Pro | 30.90 | 30.17 | 28.18 | 55.2% | 63.8% |
| Gemini 1.5 Flash | 35.40 | 36.60 | 36.55 | 49.9% | 56.6% |
| Claude 3.5 Sonnet | 31.47 | 32.16 | 31.13 | 59.7% | 64.8% |
| Claude 3.5 Haiku | 30.61 | 28.85 | 27.40 | 58.5% | 66.2% |
| Llama 3.1 405B | 33.07 | 35.23 | 29.06 | 52.2% | 60.4% |
| Llama 3.1 70B | 32.26 | 33.14 | 30.33 | 55.1% | 61.1% |
| Llama 3.1 8B | 26.09 | 31.84 | 28.03 | 50.4% | 60.5% |

**৮.৪ RQ.3 — Table II (n = 100, temperature 0.8)**

| Variant | func@1 | func@10 | func@50 | func-sec@1 | func-sec@10 | func-sec@50 |
|---|---|---|---|---|---|---|
| GPT-4o mini | 75.43 | 91.42 | 95.76 | 44.54 | 60.28 | 67.68 |
| GPT-4o mini w/ security instr. | 75.23 | 90.78 | 96.30 | 48.21 | 64.12 | 72.24 |
| Claude 3.5 Haiku | 73.81 | 85.33 | 87.90 | 43.20 | 56.48 | 60.50 |
| Claude 3.5 Haiku w/ security instr. | 71.64 | 84.31 | 88.28 | 47.10 | 66.28 | 72.56 |
| Gemini 1.5 Flash | 70.71 | 84.41 | 88.32 | 35.31 | 47.81 | 51.77 |
| Gemini 1.5 Flash w/ security instr. | 68.24 | 81.32 | 86.55 | 36.15 | 48.97 | 54.61 |
| Llama 3.1 70B Instruct | 71.84 | 85.21 | 92.11 | 39.58 | 52.07 | 61.78 |
| Llama 3.1 70B Instruct w/ security instr. | 65.79 | 83.95 | 92.39 | 36.92 | 53.47 | 65.85 |
| CodeLlama-7b-hf | 30.77 | 68.82 | 81.72 | 13.76 | 40.74 | 58.41 |
| CodeLlama-7b-hf w/ SafeCoder | 15.35 | 33.75 | 41.80 | 7.37 | 18.26 | 24.24 |

**৮.৫ Security instruction-এর প্রভাব (আমার হিসাব, Table II)**

| Model | Δ func-sec@1 | Δ func-sec@10 | Δ func@1 |
|---|---|---|---|
| GPT-4o mini | +3.67 | +3.84 | −0.20 |
| Claude 3.5 Haiku | +3.90 | +9.80 | −2.17 |
| Gemini 1.5 Flash | +0.84 | +1.16 | −2.47 |
| Llama 3.1 70B | −2.66 | +1.40 | −6.05 |

## ৯. Key findings

1. **Functional-কিন্তু-insecure ফাঁক সর্বজনীন:** func@10 → func-sec@10-এ সব model-এ প্রায় 30 pp পতন (Fig. 3; সর্বোচ্চ 35.79 pp Gemini 1.5 Flash)। Table I-এ প্রতিটি model-এ Δ@1 26.09–35.40 pp (আমার হিসাব)।
2. **Functionality ভালো মানেই security ভালো নয়:** Llama 3.1 70B-র func@10 Claude 3.5 Haiku-র চেয়ে বেশি কিন্তু func-sec@10 কম (Fig. 3)।
3. **বড় model প্রায়ই বেশি secure, কিন্তু func@k-তে নয়:** GPT-4o ও Gemini 1.5 family-তে func@k পার্থক্য ছোট (এমনকি ছোট model সামান্য ভালো, যেমন GPT-4o mini func@10 91.42 বনাম GPT-4o 90.71), কিন্তু func-sec@k পার্থক্য বড় (GPT-4o func-sec@10 65.33 বনাম mini 60.28)। অর্থাৎ security awareness model-size-এর সাথে বাড়ে, যা func@k-তে ধরা পড়ে না।
4. **Simplest security prompt ছোট কিন্তু বাস্তব উন্নতি দেয়:** GPT-4o mini ও Claude 3.5 Haiku-তে বেশি; সর্বোচ্চ func-sec@10 +9.80 pp (Claude 3.5 Haiku, 56.48 → 66.28)। Functionality-তে সামান্য কমতি।
5. **Security fine-tuning আসলে security শেখাচ্ছে কি না সন্দেহজনক:** SafeCoder CodeLlama-7b-র func@1 30.77 → 15.35, func-sec@1 13.76 → 7.37 — লেখকদের অনুমান, model security-sensitive code লেখাই এড়াতে শিখছে। আলাদা benchmark-এ এটা ধরা পড়ে না।
6. **Static analyzer অনির্ভরযোগ্য:** CodeQL-এ false negative ও false positive দুটোই (Fig. 1); CyberSecEval-এ 562/1916 reproducible।
7. **Spec-এর মান নিয়ন্ত্রণ করা যায়:** security hint ছাড়া, কিন্তু functionality অস্পষ্টতা ছাড়া spec — তাই low func-sec-কে model-এর security দুর্বলতা হিসেবে পড়া যায়, "task বোঝেনি" নয়।


## ১০. কেন বিকল্পের চেয়ে ভালো

| বিষয় | SecurityEval / CyberSecEval (আগের) | CWEval |
|---|---|---|
| Specification | এক লাইনের comment বা LLM-generated summary | signature + docstring + example, security-semantics নিশ্চিত |
| Functionality test | নেই / আলাদা benchmark | সব task-এ আছে (HumanEval-style) |
| Security verdict | static analyzer (CodeQL), false positive ও negative | outcome-driven dynamic oracle (timeout, ASan, data integrity, return value) |
| Reproducibility | CyberSecEval 562/1916 | self-contained, প্রতি task-এ secure ও insecure reference দিয়ে cross-check |
| Security hint leakage | কোথাও "safe/unsafe" keyword থাকে | ইচ্ছাকৃতভাবে বাদ |
| Language support | সীমিত | 5 language, language-agnostic oracle |
| Metric | functionality ও security আলাদা | joint func-sec@k |

মূল সুবিধা: joint metric আলাদা-benchmark pitfall (model security-sensitive কাজই এড়ায়) ধরে।

## ১১. কখন কাজ করে / কখন ব্যর্থ

**কাজ করে যখন:**
- Task self-contained, library-মুক্ত, এবং vulnerability-র observable outcome আছে (return value, timeout, ASan error, DB state)।
- Spec যথেষ্ট স্পষ্ট যে functional সফলতা নিশ্চিত।
- Vulnerability-র একটি স্পষ্ট exploit input আছে।

**ব্যর্থ হতে পারে (আমার পর্যবেক্ষণ, paper-এ স্পষ্ট বলা নেই):**
- যে vulnerability exploit করতে জটিল state বা multi-step interaction লাগে (যেমন repo-level authentication flow) — task বড় না হলে ধরা কঠিন।
- Oracle যা পরীক্ষা করেনি এমন variant (insecure কিন্তু test input-এ ধরা পড়ে না) — false negative সম্ভব; paper এই oracle-completeness কোনোভাবে মাপেনি।
- Library-dependent real-world কোড, যেখানে security semantics isolation করা যায় না।

## ১২. Limitations

**Authors-এর স্বীকৃত:**
- Task সংখ্যা সীমিত (119) মানব সম্পদের কারণে; benchmark augment করা যেতে পারে।
- ভবিষ্যৎ কাজ: benchmark creation ও expansion automate করা।
- RQ.2 ও RQ.3-তে budget-র কারণে শুধু temperature 0.8।

**আমার পর্যবেক্ষণ:**
1. **Oracle-এর completeness অমাপা:** secure reference সব test pass করে, insecure reference fail করে — এটা oracle-এর শুধু soundness-এর আংশিক প্রমাণ; অন্য insecure variant ধরা পড়ে কি না, তার mutation বা red-team মূল্যায়ন নেই।
2. **Statistics নেই:** কোনো CI, seed variance বা significance test নেই; ছোট পার্থক্য (যেমন +0.84 pp Gemini Flash-এ) noise থেকে আলাদা করা যায় না (CG4, CG8)।
3. **Model পুরোনো ও প্রধানত মাঝারি আকার:** 2024-এর model; reasoning বা agentic model নেই।
4. **Single-function-level task:** repository-level বা agentic patch নয়; seed-wise SWE-bench-স্টাইল workflow-র সাথে সরাসরি তুলনীয় নয় (CG9)।
5. **Task সংখ্যা per language ও per CWE paper-এ দেওয়া নেই:** language-ভিত্তিক বিশ্লেষণ অসম্ভব।
6. **Manual verification-এর বিবরণ কম:** "expert programmers verified" বলা আছে, কিন্তু কতজন, inter-rater agreement বা কত task বাদ পড়ল তার তথ্য নেই।
7. **LLM-translation-এর পর manual review:** translation bias বা contamination-এর পরীক্ষা নেই (CG6)। Benchmark public হওয়ায় ভবিষ্যৎ training-data contamination সম্ভব।
8. **Security-instruction এক বাক্যে সীমাবদ্ধ:** ইচ্ছাকৃত, কিন্তু উপরের-সীমা (best-case prompting) জানা যায় না।
9. **Paper-internal অসঙ্গতি:** ১৮ নম্বর Q8-এ তালিকা।

## ১৩. Research gaps

| G-id | Gap | Evidence | Related CG / sub-domain |
|---|---|---|---|
| G1 | CWEval function-level; agent-এর repo-level patch-এর জন্য joint functional+secure outcome metric নেই | CWEval task ছোট, self-contained (Section IV) | CG5, CG9 / Sub-domain 6 (Security) |
| G2 | Security oracle-এর completeness (কত insecure variant ধরে) অমাপা | Reference শুধু একটি secure ও কমপক্ষে একটি insecure (Section III-C) | CG13 (oracle strength), CG5 |
| G3 | Run-to-run variance ও CI report নেই | কোনো CI/seed তথ্য নেই; ছোট Δ (Table II) | CG4, CG8 |
| G4 | Functional-pass-এর পর security-র ফাঁক agent-patch স্তরে মাপা নেই | Fig. 3 / Table I শুধু single-function generation | CG5, CG1 |
| G5 | Static scanner বনাম outcome oracle-এর সরাসরি পরিমাণগত তুলনা (precision/recall) নেই | শুধু Fig. 1-এর উদাহরণ ও 562/1916 | CG5, CG10 |
| G6 | Security prompt-এর প্রভাব model-ভেদে অসম; Llama 70B-তে func-sec@1 কমেছে | Table II: −2.66 pp (আমার হিসাব) | CG4, CG8 |
| G7 | Alignment tax মাপার জন্য refusal vs no-op vs insecure আলাদা শ্রেণি করা হয়নি | SafeCoder-এর পতনের কারণ অনুমানমাত্র (Section V-C3) | CG5, CG17 |
| G8 | Benchmark contamination ও freshness পরীক্ষা নেই | Public GitHub release, task সংখ্যা স্থির 119 | CG6 |
| G9 | Gaming: agent security-test না দেখে/দেখে কীভাবে আচরণ করে অজানা | Spec-এ hint নেই, কিন্তু hidden-test আচরণ পরীক্ষিত নয় | CG12, CG5 |

**নতুন CG প্রস্তাব (CG20):** "Joint functional-and-secure outcome verdict for agent patches" — static scanner-এর বদলে/সঙ্গে outcome-driven security oracle এবং functional pass-এর সাথে joint report (CWEval-এর func-sec ধারণার repo-level সম্প্রসারণ)।

## ১৪. Improvement ideas

1. **Agent-patch-এর জন্য func-sec@k:** SWE-bench-স্টাইল task-এ F2P test-এর সাথে প্রতি task-এ "exploit test" (CWE-সম্পর্কিত) যোগ করে joint pass rate।
2. **Oracle mutation testing:** insecure variant-এর mutant বানিয়ে দেখা কত শতাংশ security oracle ধরে (G2)।
3. **Refusal / no-op / insecure / secure চার-শ্রেণি:** model "কিছু না করে নিরাপদ" দেখানো এড়াতে functionality oracle দিয়ে filter, তবে refusal-কে আলাদা ভাবে report।
4. **Static + dynamic ensemble:** CodeQL-কে অতিরিক্ত signal হিসেবে রেখে outcome oracle-কে ground-truth ধরে precision/recall মাপা।
5. **Confidence interval ও paired test:** task-ভিত্তিক bootstrap/McNemar, একাধিক seed।
6. **Time/memory budget-কে tunable parameter করা:** DoS oracle-এর threshold-sensitivity বিশ্লেষণ।
7. **Prompt-variant study:** security hint-এর বিভিন্ন মাত্রা (generic, CWE-specific, example-সহ) এবং তার cost।

## ১৫. Publication potential (SPL3-feasible)

- **সম্ভাব্য contribution:** "Joint functional-and-secure verdict as a component of an assurance report for agent patches" — CWEval-এর outcome-driven নীতি একটি ছোট agent-patch dataset-এ প্রয়োগ এবং static scanner-এর সাথে পরিমাণগত তুলনা।
- **SPL3-feasible অংশ:** 20–40টি CWE-সম্পর্কিত task-এ (CWEval-এর task পুনর্ব্যবহার, বা সরল extension) multi-model func vs func-sec gap পুনরায় মাপা; static scanner বনাম outcome oracle-এর precision/recall।
- **Venue ধরন:** workshop বা student-research track (বাস্তবসম্মত); full conference-এর জন্য নতুন dataset বা নতুন finding লাগবে।
- **ঝুঁকি:** CWEval-এর task public — contamination; novelty সীমিত যদি শুধু পুনরায় মাপা হয়; তাই agent-patch স্তরের joint verdict বা current-model gap মূল novelty হতে হবে।

## ১৬. SPL3 implementation

**প্রস্তাবিত pipeline (ছোট ও feasible):**

1. CWEval-Bench clone করে (GitHub artifact) Python ও C subset (core set) চালানোর environment তৈরি; Docker sandbox ব্যবহার করে (CG15)।
2. প্রতি task-এ model থেকে n sample, k = 1, 10; func@k ও func-sec@k unbiased estimator দিয়ে হিসাব।
3. একই generated code-এ CodeQL (বা Semgrep) চালিয়ে static verdict; outcome oracle-কে reference ধরে confusion matrix (TP, FP, FN, TN), precision, recall, **এবং specificity** (CG17-এর পাঠ)।
4. Agent-style extension: একটি ছোট repo-level task সেট (5–10), যেখানে patch-এর পর দুই ধরনের test চালানো — F2P/P2P (functional) ও exploit test (security)।
5. Report: patch-প্রতি আলাদা signal (functional, security-outcome, security-static), যোগ করে একক score নয় (CG12-এর পাঠ); "could not verify" আলাদা outcome।
6. Statistics: bootstrap CI, paired McNemar, একাধিক seed।

**Cost-aware পরিকল্পনা:** n = 100 sample × 119 task × কয়েক model ব্যয়বহুল; SPL3-তে n = 10–20 ও 1–2 সস্তা model দিয়ে শুরু, পরে ছোট subset-এ বেশি n।

## ১৭. Influence / link to earlier sub-domains

- **Sub-domain 1 (AI Coding Agents):** SWE-bench ও Agentless শুধু functional pass দেখে; CWEval দেখায় functional pass-এর পরও 38–50% সমাধান insecure হতে পারে (আমার হিসাব, R_1 49.9%–62.1%)। সরাসরি তুলনীয় নয় — function-level বনাম repo-level।
- **Sub-domain 2 (APR):** VRpilot-এর "sanitizer pass ≠ secure" CWEval-এর "static analyzer ≠ ground truth" যুক্তির সাথে মেলে; সম্পূরক — VRpilot compiler/sanitizer feedback দেয়, CWEval outcome oracle।
- **Sub-domain 3 (Evaluation):** SWE-Bench Pro-র "requirement-removal" ও Engineering Reliable Coding Agents-এর "verifier health" ধারণা CWEval-এর "spec clarity + oracle cross-check" নকশার সাথে সম্পর্কিত।
- **Sub-domain 4 (Test generation):** CoverUp/TestDecision-এর "coverage ≠ oracle strength" CWEval-এর "security oracle-ই আলাদা property মাপে" ধারণার প্রতিধ্বনি।
- **Sub-domain 5 (Patch Validation):** Harden and Catch-এর hardening test ও HITL Judge-এর প্রসঙ্গ — security-ও একটি আলাদা validation signal হওয়া উচিত।
- **Research direction-এর জন্য:** assurance report-এ "security scan" আইটেমকে static scanner থেকে outcome-driven dynamic oracle-এ আপগ্রেড করা (CG5 → CG20)।

## ১৮. Supervisor Q&A

**Q1. func-sec@k আসলে কী মাপে, func@k থেকে আলাদা কীভাবে?**
A. k-টি sample-এর অন্তত একটি functionality ও security দুই test-ই pass করার সম্ভাবনা। func@k শুধু functionality। পার্থক্যই "functional কিন্তু insecure" সমাধান (Fig. 3-এ প্রায় 30 pp)।

**Q2. Static analyzer ছাড়া security কীভাবে নির্ধারণ হয়?**
A. Execution-এর outcome দেখে: timeout (DoS), ASan error (memory), data integrity (SQL injection), return value। Pattern নয়, behavior দেখে, তাই implementation-diversity সহ্য করে (Fig. 1 বনাম Fig. 2)।

**Q3. কেন task-এ "secure" hint দেওয়া হয়নি?**
A. বাস্তব user vulnerability সম্পর্কে কম সচেতন; hint model-এর আচরণ বদলে দেয়। বরং RQ.3-তে আলাদা করে hint-এর প্রভাব মাপা হয়েছে।

**Q4. আপনার প্রকল্পে এর সরাসরি প্রয়োগ কী?**
A. Agent patch-এ functional signal-এর সঙ্গে outcome-driven security signal জুড়ে joint verdict রিপোর্ট করা; static scanner শুধু অতিরিক্ত signal।

**Q5. SafeCoder-এর ফল কী বোঝায়?**
A. আলাদা benchmark-এ ভালো দেখালেও joint metric-এ func@1 30.77 → 15.35, func-sec@1 13.76 → 7.37। লেখকদের অনুমান: model security-sensitive কাজ এড়াতে শেখে। এটা প্রমাণিত নয় — refusal/no-op আলাদা করে গোনা হয়নি।

**Q6. বড় model কি সবসময় বেশি secure?**
A. প্রায়ই (Table I), সবসময় নয়: Llama 3.1 405B-র func-sec@1 (36.18) 70B-র (39.58) চেয়ে কম, এবং Δ@10 বড় (35.23 বনাম 33.14, আমার হিসাব)।

**Q7. Results কতটা নির্ভরযোগ্য?**
A. কোনো CI বা seed variance নেই; Table II-এর ছোট পরিবর্তন (যেমন Gemini Flash +0.84 pp) noise হতে পারে।

**Q8. Paper-internal অসঙ্গতি আছে?**
A. আছে: (ক) "four LLMs" বলা হলেও Fig. 3-এ Llama 3.1 8B সহ পাঁচটি; (খ) SafeCoder-এর reference [23] আসলে QR-code সম্পর্কিত এক ভিন্ন paper (J. Netw. Comput. Appl.) — নামের সাথে মিল থাকলেও সম্ভবত He et al.-এর [19] নয়; (গ) text "improvements for almost all LLMs" বলে, কিন্তু Table II-এ Llama 70B-র func-sec@1 কমেছে (39.58 → 36.92) এবং Gemini Flash-এর উন্নতি নামমাত্র; (ঘ) Table II-এর শুরু বাক্য "Llama 3.1 70B w/ security instr." এর func@1 65.79 (−6.05 pp) — "possible slight decrease" বর্ণনা এর চেয়ে ছোট শোনায়।

## ১৯. Glossary

| Term | অর্থ |
|---|---|
| CWE | Common Weakness Enumeration, weakness-এর তালিকা |
| Outcome-driven oracle | code চালিয়ে পর্যবেক্ষিত ফলাফলের উপর ভিত্তি করা test |
| func@k | k-sample-এর মধ্যে অন্তত একটি functional হওয়ার সম্ভাবনা |
| func-sec@k | অন্তত একটি functional ও secure হওয়ার সম্ভাবনা |
| ASan | AddressSanitizer, runtime memory error detector |
| Alignment tax | security-training-এর ফলে functionality/helpfulness কমে যাওয়া |
| Security semantics isolation | task থেকে third-party dependency বাদ দিয়ে শুধু security-র মূল অংশ রাখা |
| False negative / positive (scanner) | সত্যিকারের insecure code না ধরা / secure code-কে insecure বলা |
| Reference implementation | secure ও insecure (functional) আদর্শ সমাধান |

## ২০. Summary card

| Item | সারাংশ |
|---|---|
| Paper | CWEval, Columbia Univ., arXiv 2501.08200 (Jan 2025) |
| Idea | functionality ও security একই task-এ, outcome-driven oracle, static analyzer ছাড়া |
| Benchmark | 119 task, 31 CWE, 5 language (11 C memory task) |
| Metric | func@k, func-sec@k (unbiased estimator) |
| Headline | func@10 → func-sec@10 পতন প্রায় 30 pp; সর্বোচ্চ 35.79 pp (Gemini 1.5 Flash) |
| Best (Table I) | GPT-4o: func-sec@1 50.21, func-sec@10 65.33 |
| Security prompt | সর্বোচ্চ +9.80 pp func-sec@10 (Claude 3.5 Haiku) |
| SafeCoder | func@1 30.77 → 15.35; func-sec@1 13.76 → 7.37 |
| মূল দুর্বলতা | CI নেই, oracle completeness অমাপা, function-level, পুরোনো model |
| আমাদের জন্য | agent patch-এ joint func-sec verdict + outcome-driven security signal (CG5 → CG20) |

## ২১. বর্তমান (2026) প্রেক্ষাপট

### ২১.১ তখন বনাম এখন

| বিষয় | CWEval (Jan 2025) | 2026 (context.md থেকে) |
|---|---|---|
| Model | GPT-4o, Claude 3.5, Gemini 1.5, Llama 3.1 | Claude Opus 5.5, GPT-6 family, Gemini 4 Argon, Kimi K3.1, GLM-5.x, DeepSeek V4 (সবই নতুন; CWEval-এ মাপা হয়নি) |
| Functional ও secure ফাঁক | func@10 → func-sec@10 প্রায় 30 pp (function-level) | SusVibes (I, Opus 4.6 / GPT-5.4 যুগ): FuncPass 62–84% বনাম SecPass 7.8–17.3% (repo-level agent task) |
| Security signal | outcome oracle বনাম static analyzer নিয়ে তর্ক | কোনো current-model SusVibes/BaxBench ডেটা নেই (context.md) |
| Prompt injection | কথা হয়নি | Opus 5.5 injection success 54.61% safeguard ছাড়া, 11.13% সহ (V, vendor-reported) |
| Gaming | বিবেচিত নয় | METR: ≥16% সফল long-task run cheat (I, আগের প্রজন্ম); Opus 5.5 card-এ hidden-tests reasoning ও git concealment (V) |

### ২১.২ এখনও সত্য / পুরোনো

**এখনও সত্য:**
- Functional pass আর secure-pass আলাদা — SusVibes-এ আরও বড় ফাঁক (SecPass 7.8–17.3% বনাম FuncPass 62–84%; I)।
- Static analyzer একা অবিশ্বাস্য — কারণ pattern বনাম behavior যুক্তি অপরিবর্তিত।
- Joint metric দরকার; আলাদা benchmark ফাঁক লুকায়।

**পুরোনো / সতর্কতা:**
- CWEval-এর সংখ্যা (≈ 30 pp) 2024-এর model-এ ও function-level task-এ; আজকের model বা agent-এ সরাসরি প্রযোজ্য নয়।
- তুলনা: CWEval-এ R_1 প্রায় 49.9–62.1% (আমার হিসাব), অর্থাৎ functional সমাধানের অর্ধেকের বেশি secure। SusVibes-এ SecPass/FuncPass অনুপাত সীমা মাত্র প্রায় 9–28% (আমার হিসাব: 7.8/84 থেকে 17.3/62, যেহেতু প্রতিটি model-এর জোড়া context.md-এ নেই)। দুটি benchmark ভিন্ন (function বনাম repo; ভিন্ন model, ভিন্ন oracle), তাই এটি তুলনীয় নয়, শুধু দিক নির্দেশক: task জটিল হলে ফাঁক বাড়ে।
- Prompt-based security hint-এর +9.8 pp ফল পুরোনো model-এর; বর্তমান model-এর তথ্য পাওয়া যায়নি।

### ২১.৩ আজকের উন্মুক্ত gap

| Gap | অবস্থা 2026 | সংযোগ |
|---|---|---|
| Current model-এ CWEval/SusVibes/BaxBench জাতীয় joint func-sec ডেটা | নেই (context.md) | CG5 |
| Agent patch-এ outcome-driven security oracle | অজানা; SusVibes আংশিক | CG5, G1 |
| Security signal-এর gaming (hidden tests দেখা, git লুকানো) | V ও I প্রমাণ আছে, security oracle-এর উপর নয় | CG12 |
| Oracle completeness মাপা | কোনো current ডেটা নেই | CG13, G2 |
| Prompt injection ও insecure code আলাদা অক্ষ | আলাদা মাপা হচ্ছে, একত্রে নয় | CG18 |

### ২১.৪ SPL3 idea (current model, cost-aware)

- Cost per task (Vals Terminal-Bench 4.0, I): Opus 5.5 13.20 USD, Kimi K3.1 Pro 4.57 USD, GPT-6.1 Sol 1.72 USD। CWEval-Bench-এর function-level task অনেক সস্তা (ছোট prompt); তাই 119 task × n = 20 sample একটি সস্তা model (GPT-6.1 Sol বা Kimi K3.1 Pro) এবং একটি শক্তিশালী model (Opus 5.5) দিয়ে চালানো সম্ভব।
- পরিকল্পনা: (১) CWEval-এর core Python/C subset এই 2–3 model-এ n = 20, k = 1, 5, 10; (২) func-sec@k ও Δ_k, R_k report, bootstrap CI সহ; (৩) একই code-এ CodeQL চালিয়ে scanner বনাম outcome oracle-এর precision, recall, specificity; (৪) পরিমাণগত তুলনা: Δ আজকের model-এ 2025-এর ≈ 30 pp-র কাছে আছে, না কমেছে (বর্তমান model-এর তথ্য পাওয়া যায়নি — এটাই প্রধান নতুন ফল হতে পারে)।
- Contamination সতর্কতা: CWEval public, তাই 2026 model train-এ দেখে থাকতে পারে; তাই কিছু fresh variant task নিজে লিখে তুলনা।

### ২১.৫ তিনটি Q&A

**Q1. 2025-এর func-sec ফাঁক কি আজ বন্ধ হয়েছে?**
A. তথ্য নেই। SusVibes-এ (I, Opus 4.6 / GPT-5.4 যুগ) agent task-এ SecPass মাত্র 7.8–17.3%, তাই ফাঁক বন্ধ হয়নি বলেই ইঙ্গিত; CWEval-এ current model চালানো হলে নিশ্চিত হবে। বর্তমান model-এর তথ্য পাওয়া যায়নি।

**Q2. আজকের agent-এর জন্য static scanner কি যথেষ্ট?**
A. না: CWEval-এর যুক্তি (Fig. 1, 562/1916) এখনও প্রযোজ্য, এবং agent gaming (METR ≥16%) দেখায় একক signal ঝুঁকিপূর্ণ। Scanner অতিরিক্ত signal, ground truth নয়।

**Q3. Vendor-reported injection resistance (11.13% success) কি security-র proof?**
A. না। এটি prompt-injection-এর metric (V), insecure code generation-এর outcome নয়; আলাদা অক্ষ এবং independent verification নেই।
