# CalibraPatch Review: Research Area-র পুনর্মূল্যায়ন ও নতুন Proposal-এর বিচার

> **কী নিয়ে:** Final Synthesis-এ বাছাই করা research area (PatchAssure) আবার যাচাই, আর নতুন প্রস্তাব "CalibraPatch"-এর কঠোর review।
> **তারিখ:** 3 November 2026। Web-এ প্রতিটা paper-এর মূল উৎস খুলে যাচাই করা হয়েছে; যেগুলো খোলা যায়নি তা স্পষ্ট করে লেখা আছে।
> **ভিত্তি:** `08_Final_Synthesis/Final_Synthesis.md`, ২৬টা paper analysis, আর নতুন web যাচাই (প্রায় ৫০টা search ও primary page)।

---

## ১. Executive Summary

**এক কথায় রায়: MODIFY।** CalibraPatch-এর মূল ধারণা টিকে আছে, কিন্তু যেভাবে লেখা আছে সেভাবে নয়।

- **পুরনো PatchAssure-এর novelty এখন দুর্বল।** "কয়েকটা signal একসাথে করে report" — এটা ইতিমধ্যে TrustPatch-X (IJACSA 2026), একটা master's thesis (Comillas 2026), PatchBench (2026) ও R2E-Gym (NeurIPS 2025) বিভিন্নভাবে করেছে। তার উপর "PatchAssure" নামটা একটা বাণিজ্যিক product-এর নাম। তাই এই নাম ও এই framing বাদ দেওয়া উচিত।
- **CalibraPatch-এর মূল অংশ এখনো খোলা বলে মনে হচ্ছে।** আমাদের search-এ এমন কোনো কাজ পাওয়া যায়নি, যেটা AI agent-এর patch-এর জন্য — test, security, test adequacy আর judge-এর মতো ভিন্ন ভিন্ন signal মিলিয়ে — একটা **calibrated** সম্ভাবনা দেয়, signal-দের **conflict** ধরে, আর প্রমাণ কম হলে **"Insufficient Evidence" বলে abstain** করে, এবং এটা **risk–coverage ও false assurance rate** দিয়ে মাপে।
- **কিন্তু খুব কাছের কাজ আছে।** Google-এর "Abstain and Validate" (ICSE-SEIP 2026) agentic repair-এ abstention আর patch validation করে। WEAVER (ICML 2025) verifier-দের reliability শিখে মেলায় (তবে math/reasoning-এ)। Calibration-এর দিকে Spiess et al. (ICSE 2025), Siddiq et al. (2026, "False Trust") আর Rathnasuriya & Yang (ICSE-NIER 2026) আছে। তাই novelty হবে **"application + evaluation"-ধরনের**, নতুন গণিত নয়।
- **সবচেয়ে বড় ঝুঁকি ground truth।** একটা patch "আসলে ঠিক ও নিরাপদ" কিনা — এটা ঠিক করা কঠিন। PatchDiff (ICSE 2026)-এ divergent patch-এর 66.2% "uncertain" ছিল। Calibration মাপতে কয়েকশো label করা patch লাগবে।
- **সুপারিশ:** Signal কমিয়ে ৪–৫টা করো, explanation-কে RQ থেকে সরাও, Python দিয়ে শুরু করো (Java পরে), নিজে agent না চালিয়ে প্রকাশিত patch ব্যবহার করো, আর মূল দাবি করো: *"Test pass-এর বদলে calibrated, abstention-সহ সিদ্ধান্ত নিলে একই coverage-এ false assurance কতটা কমে।"*

---

## ২. CalibraPatch সহজ ভাষায়

### ক. কী এটা?
AI agent একটা bug ঠিক করে patch দিলো। আজকের নিয়ম: test pass করলেই "ঠিক আছে"। CalibraPatch বলবে: "দাঁড়াও, আগে দেখি প্রমাণ কতটা শক্ত।"

### খ. উদাহরণ দিয়ে
ধরো ডাক্তারের কাছে ৫টা report আছে। রক্ত পরীক্ষা ভালো, X-ray ভালো, কিন্তু একটা scan-এ সন্দেহজনক দাগ, আর একটা পরীক্ষা করাই হয়নি। ভালো ডাক্তার বলবেন না "আপনি সুস্থ"। তিনি বলবেন "আরও পরীক্ষা লাগবে"। CalibraPatch ঠিক এটাই করে patch-এর জন্য।

### গ. তিনটা মূল কাজ
1. **প্রতিটা signal কতটা বিশ্বাসযোগ্য, তা মাপা।** যেমন: security scanner-এর অর্ধেক warning ভুল হতে পারে; test থাকলেও 80.2% ক্ষেত্রে দুর্বল oracle (All Smoke, No Alarm)।
2. **সব signal মিলিয়ে একটা সৎ সম্ভাবনা দেওয়া।** "এই patch 90% সম্ভাবনায় ঠিক" বললে, এমন ১০০টা patch-এর মধ্যে সত্যিই প্রায় ৯০টা ঠিক হওয়া উচিত। একেই **calibration** বলে।
3. **প্রমাণ কম বা পরস্পরবিরোধী হলে "জানি না" বলা।** একে **abstention** বলে।

### ঘ. কেন দরকার?
সবচেয়ে বিপজ্জনক ভুল হলো **false assurance** — খারাপ patch-কে "নিরাপদ" বলে দেওয়া। কারণ মানুষ তখন আর দেখে না। Papotti et al. (EMSE 2024) দেখিয়েছেন, reviewer-রা "security tool" label দেখলেই patch বেশি মেনে নেয়, patch ঠিক হোক বা না হোক।

> **মনে রাখো:** CalibraPatch-এর লক্ষ্য বেশি patch পাস করানো নয়। লক্ষ্য হলো যেগুলো পাস করানো হচ্ছে, সেগুলো যেন সত্যিই বিশ্বাসযোগ্য হয়, আর যেখানে প্রমাণ নেই সেখানে সৎভাবে "জানি না" বলা।

---

## ৩. Related Paper-গুলোর বিস্তারিত বিশ্লেষণ

যাচাইয়ের অবস্থা: ✅ = মূল উৎস খুলে যাচাই; ◐ = আংশিক (metadata বা secondary উৎস); ❌ = যাচাই করা যায়নি।

### ৩.১ Chen & Jiang — Evaluating Software Development Agents (✅)
- **প্রকাশ:** arXiv 2410.12468; SANER 2025 Research Track-এ গৃহীত (peer-reviewed)।
- **কী করেছে:** SWE-Bench Verified-এর top 10 agent-এর 4,892টা patch-কে developer-এর gold patch-এর সাথে তুলনা; SonarQube দিয়ে patch-এর আগে-পরে code quality।
- **মূল সংখ্যা:** 500 issue-এর 170টা কোনো agent-ই সমাধান করেনি। Gold file-এর সাথে হুবহু মেলা resolved patch agent-ভেদে 15.48% থেকে 94.59%। SonarQube patch-এর আগে-পরে **শূন্য** vulnerability পেয়েছে।
- **সীমাবদ্ধতা:** শুধু Python; gold patch-কে আদর্শ ধরা; SWE-bench test gold patch ঘিরে বানানো।
- **আমাদের জন্য শিক্ষা:** SonarQube-ধরনের "code quality" signal patch-এর ঝুঁকি প্রায় ধরেই না। তাই এটাকে মূল signal করা অর্থহীন।

### ৩.২ Sajadi et al. — How Safe Are AI-Generated Patches? (✅)
- **প্রকাশ:** arXiv 2507.02976 (v3, Dec 2025)। **Preprint** — কোনো venue নেই; venue হিসেবে cite করো না।
- **কী করেছে:** প্রায় 20,000 SWE-bench issue-এ Llama 3.3-70B বনাম developer; OpenHands, AutoCodeRover, HoneyComb-এর patch। CodeQL, Semgrep, Bandit — ৩টার অন্তত ২টা একমত হলে finding রাখা, তারপর manual review।
- **মূল সংখ্যা:** Llama-র patch-এ 135টা নিশ্চিত vulnerability, developer-এর 12টা (প্রায় 11 গুণ)। OpenHands-এ 44টা।
- **সীমাবদ্ধতা:** Manual review একজনই করেছেন; agent-এর ফলে কোনো statistical test নেই।
- **আমাদের জন্য শিক্ষা:** "২-এর-৩ voting" আসলে signal reliability সামলানোর একটা কাঁচা উপায়। CalibraPatch এটাকে নীতিগতভাবে করতে পারে। এটা একটা baseline-ও।

### ৩.৩ Peng et al. — When "Correct" Is Not Safe (✅)
- **প্রকাশ:** ACL 2026 Long (Vol. 1, pp. 15514–15546), peer-reviewed; arXiv 2510.17862।
- **কী করেছে:** "Functionally Correct yet Vulnerable" (FCV) patch দেখানো, আর FCV-Attack — issue-এ developer-এর মতো একটা hint ঢুকিয়ে agent-কে vulnerable patch লেখানো। 3 scaffold × 4 model।
- **মূল সংখ্যা:** স্বাভাবিক অবস্থায় test-pass করা patch-এর 4.3–6.0%-এ weakness। CWE-538-এ attack সফলতা 40.7% (GPT-5 mini + OpenHands) ও 55.6% (Claude Sonnet 4 + OpenHands)।
- **সীমাবদ্ধতা:** মাত্র ৪টা CWE; label এসেছে LLM judge থেকে, মানুষ বা static analysis থেকে নয়।
- **আমাদের জন্য শিক্ষা:** "Test pass মানে নিরাপদ নয়" — এর শক্ত প্রমাণ। কিন্তু এটা কোনো detector বা assurance পদ্ধতি বানায়নি। তাই CalibraPatch-এর সাথে সরাসরি overlap কম।

### ৩.৪ RETRACE — Independent Patch Verification (✅)
- **প্রকাশ:** arXiv 2608.08950 (9 Aug 2026), 8 page **preprint**। Authors: Chenglin Li, Yisen Xu, Zehao Wang, Shin Hwei Tan, Tse-Hsun (Peter) Chen।
- **কী করেছে:** Test ছাড়া, training ছাড়া patch যাচাই। Forward: issue + trajectory থেকে যুক্তি। Backward: patch থেকে "কোন সমস্যা ঠিক করছে" অনুমান। তারপর দুটো মিলিয়ে Same / Partial / Different রায়, আর Submit বা Revise সিদ্ধান্ত।
- **মূল সংখ্যা:** SWE-bench Verified-এ Pass@1 56.2% থেকে 63.2% (GPT-5-mini)। OpenHands (120 issue) 37.5% থেকে 56.7%।
- **সীমাবদ্ধতা:** শুধু Python; verifier আর generator একই LLM; একবার চালানো, variance নেই।
- **আমাদের জন্য শিক্ষা:** Issue-patch alignment signal-এর সবচেয়ে কাছের কাজ, আর **conflict detection-ও করে** (forward বনাম backward)। কিন্তু এর লক্ষ্য patch উন্নত করা, calibrated সিদ্ধান্ত দেওয়া নয়। Test, security বা adequacy signal-ও নেই।

### ৩.৫ Beyond Bypass — Vulnerability Regression (◐)
- **প্রকাশ:** IEEE AITest 2026, pp. 136–143, DOI 10.1109/AITest70988.2026.00029। Authors: Yasmeen Rawajfih, Adiba Mahmud, Ross Arnold। Crossref-এ title, author, venue নিশ্চিত।
- **বিষয়বস্তু: ❌ যাচাই করা যায়নি।** IEEE Xplore পাতা খোলেনি, abstract কোথাও পাওয়া যায়নি।
- **করণীয়:** University-র IEEE access দিয়ে PDF নিয়ে পড়ো। তার আগে এর method বা ফল নিয়ে কিছু লিখো না।

### ৩.৬ All Smoke, No Alarm — Oracle Signals in Agent-Authored Tests (✅)
- **প্রকাশ:** IEEE AITest 2026, pp. 197–200 (৪ পাতা, সম্ভবত short paper); arXiv 2606.18168। Authors: Dipayan Banik, Kowshik Chowdhury, Shazibul Islam Shamim।
- **কী করেছে:** 2,807 repo-র 33,596টা agent PR থেকে 86,156টা test-file patch। Regex-ভিত্তিক oracle taxonomy: দুর্বল (assertion নেই, শুধু non-null, শুধু boolean, শুধু mock, শুধু snapshot) বনাম শক্ত (value equality, error/type check)।
- **মূল সংখ্যা:** **80.2%** test patch-এ দুর্বল বা কোনো oracle নেই। শক্ত oracle merge-এর সম্ভাবনা বাড়ায় (OR = 1.28, p < 0.001)। Classifier-মানুষ মিল 86.7%, κ = 0.77।
- **আমাদের জন্য শিক্ষা:** "Test আছে ও pass করছে" signal নিজেই অবিশ্বাসযোগ্য হতে পারে। এই taxonomy সরাসরি CalibraPatch-এর **test adequacy / oracle strength** signal হিসেবে ব্যবহার করা যায় — সস্তা, regex-ভিত্তিক।

### ৩.৭ OpenAI — Why SWE-bench Verified no longer measures frontier coding (◐)
- **অবস্থা:** openai.com সরাসরি খোলা যায়নি (HTTP 403)। নিচের তথ্য search-engine-এর উদ্ধৃতি আর secondary খবর থেকে। **নিজে browser-এ খুলে মিলিয়ে তবেই cite করো।**
- **যা পাওয়া গেছে:** 23 Feb 2026। Audit করা সমস্যার অন্তত 59.4%-এ ত্রুটিপূর্ণ test সঠিক patch-কেও বাতিল করে (প্রায় 35.5% খুব সরু test, 18.8% issue-এ নেই এমন জিনিস test করে)। Frontier model-রা মূল fix বা problem text পুনরুৎপাদন করতে পেরেছে — contamination। OpenAI Verified report করা বন্ধ করেছে।
- **আমাদের জন্য শিক্ষা:** Test নিজেই ভুল হতে পারে — দুই দিকেই (ভুল patch পাস, সঠিক patch ফেল)। তাই test-কে ground truth ধরা যাবে না।

### ৩.৮ Wang, Pradel, Liu — Are "Solved Issues" Really Solved Correctly? (✅)
- **প্রকাশ:** ICSE 2026 Research Track (DOI 10.1145/3744916.3764576); arXiv 2503.15223।
- **কী করেছে:** PatchDiff — GPT-4o-mini দিয়ে এমন test বানানো যেখানে agent-এর patch আর developer-এর patch আলাদা আচরণ করে; তারপর manual label।
- **মূল সংখ্যা:** 877টা plausible patch-এর 29.6% (260টা) developer patch থেকে আলাদা আচরণ করে। 77টা sample-এর 28.6% নিশ্চিত ভুল, 5.2% সঠিক, **66.2% uncertain** (issue অস্পষ্ট)। "Correct" patch-এর 7.8% developer-এর পূর্ণ test suite-এ fail করে।
- **আমাদের জন্য শিক্ষা:** দুইটা বড় শিক্ষা। (১) Differential testing একটা শক্তিশালী signal। (২) Ground truth-এ "uncertain" একটা বাস্তব শ্রেণি — ground truth design-এ এটা মানতেই হবে।

### ৩.৯ PatchBench — Vulnerability Patching (✅)
- **প্রকাশ:** arXiv 2609.04075 (3 Sep 2026), **preprint**। Authors: Chihao Shen, Jiacheng Li, Aastha Mahajan, Jeffery Siyuan Tian, Yonghwi Kwon, Yizheng Chen।
- **কী করেছে:** 32 project-এর 213টা C/C++ task, 16টা CWE। Security check (PoC + fuzzed variant-এ sanitizer error বন্ধ) আর semantic check (benign input-এ নতুন error নেই, output reference-এর মতো, unit test pass)।
- **মূল সংখ্যা:** শুধু PoC দিয়ে যাচাই করলে সমাধানের হার গড়ে **1.83 গুণ** ফুলে যায় — 83.1% PoC পাস, কিন্তু 45.3% সত্যিই সমাধান। Top 3 agent 97%-এর বেশি PoC পাস করে, কিন্তু মাত্র প্রায় 57–59% সমাধান করে।
- **আমাদের জন্য শিক্ষা:** একটা signal (PoC) একা হলে false assurance বিশাল। কিন্তু PatchBench-এর সিদ্ধান্ত hard AND, কোনো uncertainty বা abstention নেই। আর এটা reference patch চায়, যা বাস্তবে থাকে না।

### ৩.১০ Papotti, Paramitha, Massacci — Reviewer acceptance of APR security patches (◐)
- **প্রকাশ:** Empirical Software Engineering 29(5), article 132, 2024, DOI 10.1007/s10664-024-10506-z (peer-reviewed)। শুরু ESEM 2022 Registered Report হিসেবে।
- **কী করেছে:** VU Amsterdam-এর master's student-রা 7টা Vul4J CVE-এর Java patch review করে; পরে (কখনো মিথ্যা) "security tool" label দেখানো হয়।
- **ফল (registered report version থেকে; final paper-এর সংখ্যা যাচাই হয়নি):** ভুল patch চেনা সঠিক patch চেনার চেয়ে সহজ; "security tool" label দেখলে reviewer সেই patch বেশি মেনে নেয়, patch ঠিক হোক বা না হোক।
- **আমাদের জন্য শিক্ষা:** Label-ভিত্তিক বিশ্বাস বিপজ্জনক — এটাই "evidence-based, calibrated" report-এর পক্ষে মানবিক যুক্তি।

### ৩.১১ TrustPatch-X (✅, কিন্তু মান দুর্বল)
- **প্রকাশ:** IJACSA (The SAI Organization), Vol. 17, No. 4, 2026, pp. 900–908। Open-access journal article; peer-review নামমাত্র বলে ধরা হয়। Authors: Sheetal Madhukar Parate, Jasmine Selvakumari Jeya I (VIT Bhopal)। PDF-এ কোনো DOI পাওয়া যায়নি।
- **Pipeline:** LLM patch → static filter (CWE signature চলে গেছে কিনা) → GNN দিয়ে পুরনো ও নতুন code-এর CFG/DFG-এর cosine similarity ≥ δ → test pass (থাকলে) → LLM-এর লেখা explanation।
- **সিদ্ধান্ত:** $V = \alpha I_{vuln} + \beta S_{sem} + \gamma T$, আর $V \geq \lambda$ হলে গ্রহণ। Weight আর threshold স্থির।
- **দাবি করা সংখ্যা:** 96.3% vulnerability-removal accuracy, false-fix rate 9.3% (base LLM-এ 34.5%)।
- **লাল পতাকা:** কোন LLM ব্যবহার হয়েছে বলা নেই; $\alpha, \beta, \gamma, \delta, \lambda$-এর মান দেওয়া নেই; data শুধু অনুরোধে।
- **CalibraPatch-এর সাথে overlap:** Multi-stage, weighted sum, explanation — **হ্যাঁ**। Uncertainty, calibration, conflict detection, abstention — **না**। তাই এটা পুরনো PatchAssure-এর novelty কমায়, কিন্তু CalibraPatch-এর নয়। এটা একটা ভালো baseline: "fixed weighted sum"।

### ৩.১২ Search-এ পাওয়া আরও কাছের কাজ (তুমি দাওনি, কিন্তু reviewer জিজ্ঞেস করবে)
| কাজ | প্রকাশ | কী করে | কেন গুরুত্বপূর্ণ |
|---|---|---|---|
| Cambronero et al., Abstain and Validate | ICSE-SEIP 2026, arXiv 2510.03217 (Google) | Bug-এ abstain করার LLM policy + LLM patch-validation critic; filtered success 0.11 থেকে 0.21 (abstention), 0.29 (validation) | **সবচেয়ে বড় overlap ঝুঁকি।** পার্থক্য: ওটা LLM policy, calibrated বা multi-signal নয় |
| WEAVER (Saad-Falcon et al.) | ICML 2025, arXiv 2506.18203 | Label ছাড়া প্রতিটা weak verifier-এর accuracy অনুমান করে মেলায় (Snorkel-ধরনের) | Reliability-aware fusion-এর পদ্ধতি আগেই আছে — কিন্তু math/reasoning-এ, patch-এ নয় |
| R2E-Gym (Jain et al.) | NeurIPS 2025 | Execution + execution-free verifier যোগ করে patch ranking; কোন verifier কোথায় ভুল করে দেখায় | Hybrid fusion আছে, কিন্তু uncalibrated, শুধু ranking |
| Spiess et al., Calibration and Correctness of LMs for Code | ICSE 2025, arXiv 2402.02047 | Code LM-এর confidence-এর calibration (program repair সহ); Platt scaling, ECE, Brier | Model-এর নিজের confidence, signal-এর নয় |
| Siddiq, Rahman, Santos, Security Calibration in LLMs for Code | arXiv 2606.31159 (preprint) | ECE, Brier, "False Trust" (vulnerable code-এ বেশি confidence) | তোমার "false assurance"-এর কাছাকাছি ধারণা — cite করতেই হবে |
| Rathnasuriya & Yang, When to Answer and When to Defer | ICSE 2026 NIER | Code prediction-এ uncertainty + calibration + abstention + coverage নিয়ন্ত্রণ | Selective prediction code-এ আছে, patch acceptance-এ নয় |
| Hernández Bas, Multi-Layer Verification Harness | Master's thesis, Comillas 2026 | SWE-bench Lite-এ static + dynamic + semantic layer | Abstract পাওয়া যায়নি; probability বা abstention আছে কিনা অজানা |

---

## ৪. বর্তমান Research Landscape

ছয়টা ধারা এখন সমান্তরালে চলছে:

| ধারা | প্রতিনিধি কাজ | কী প্রমাণ করেছে | কী করেনি |
|---|---|---|---|
| A. "Test pass ≠ ঠিক" | PatchDiff (ICSE 2026), OpenAI 2026, AutoCodeRover | Plausible patch-এর বড় অংশ আলাদা আচরণ করে; test নিজেও ভুল | কখন বিশ্বাস করা যাবে তার সিদ্ধান্ত-পদ্ধতি |
| B. "Test pass ≠ নিরাপদ" | FCV (ACL 2026), Sajadi et al., PatchBench, CWEval | Security signal ছাড়া false assurance বড় | Security signal-এর নিজের ভুলের হার নিয়ে সিদ্ধান্ত |
| C. Test-এর মান | All Smoke No Alarm, CoverUp, TestDecision | Agent-এর test-এর 80.2%-এ দুর্বল oracle | Adequacy-কে সিদ্ধান্তের input বানানো |
| D. Verifier / judge | RETRACE, SE-Jury, HITL LLM Judge, RePaCA, R2E-Gym | একক বা hybrid verifier patch বাছাই উন্নত করে | Calibrated, abstaining গ্রহণ-সিদ্ধান্ত |
| E. Calibration ও abstention | Spiess (ICSE 2025), Siddiq 2026, Rathnasuriya & Yang 2026, Abstain and Validate | Code model-এর confidence miscalibrated; abstention উপকারী | Multi-signal patch evidence-এর calibration |
| F. Multi-stage pipeline | TrustPatch-X, Comillas thesis, PatchBench | Signal জোড়া দেওয়া যায় | Signal-এর reliability, conflict, uncertainty |

**সহজ কথায়:** A, B, C বলছে "সমস্যা আছে"। D আর F বলছে "আরও যাচাই করো"। E বলছে "confidence মাপো"। কিন্তু **E-কে A–D-এর evidence-এর উপর প্রয়োগ** — এই সংযোগটা এখনো খালি দেখাচ্ছে।

---

## ৫. সবচেয়ে কাছের প্রতিদ্বন্দ্বী কাজ — তুলনা

### ৫.১ মূল তথ্য
| কাজ | বছর | উদ্দেশ্য | Signal | Aggregation | Dataset | প্রধান সীমাবদ্ধতা |
|---|---|---|---|---|---|---|
| TrustPatch-X | 2026 | LLM security patch validation | Static CWE, GNN semantic, test | স্থির weighted sum | Juliet, Devign, Defects4J | Weight অজানা, LLM অজানা, data বন্ধ |
| Abstain and Validate | 2026 | Agentic APR-এ noise কমানো | LLM bug-policy, LLM critic | Sequential filter | Google internal bug | Uncalibrated, LLM-নির্ভর |
| RETRACE | 2026 | Agent patch-এর স্বাধীন যাচাই | Issue-patch alignment (দুই দিক) | LLM reconciliation | SWE-bench Verified | Test বা security নেই, একই LLM |
| PatchBench | 2026 | Vulnerability patch benchmark | PoC, fuzzing, semantic, unit test | Hard AND | 213 C/C++ task | Reference patch লাগে |
| R2E-Gym | 2025 | SWE agent patch ranking | Execution + LLM verifier | যোগফল | R2E-Gym, SWE-bench | Ranking, absolute সিদ্ধান্ত নয় |
| WEAVER | 2025 | Weak verifier মেলানো | LM judge, reward model | Label model (reliability শেখে) | Math, reasoning | Patch-এ প্রয়োগ হয়নি |
| Sajadi et al. | 2025 | Patch-এর security ঝুঁকি | CodeQL, Semgrep, Bandit | 2-of-3 vote | SWE-bench | শুধু security, preprint |
| PatchDiff | 2025–26 | Solved issue কি সত্যিই solved | Differential test | নেই (study) | SWE-bench Verified, 877 patch | শুধু Python, ছোট manual sample |

### ৫.২ CalibraPatch-এর ক্ষমতার সাথে তুলনা
| কাজ | Uncertainty | Calibration | Conflict detection | Abstention | Explanation | Overlap |
|---|---|---|---|---|---|---|
| TrustPatch-X | না | না | না | না | হ্যাঁ | মাঝারি (পুরনো PatchAssure-এর সাথে বেশি) |
| Abstain and Validate | আংশিক | না | না | হ্যাঁ (LLM policy) | না | **বেশি** |
| RETRACE | না | না | হ্যাঁ (দুই view) | আংশিক (budget) | আংশিক | মাঝারি |
| PatchBench | না | না | আংশিক | না | না | কম |
| R2E-Gym | না | না | আংশিক (finding হিসেবে) | না | না | মাঝারি |
| WEAVER | আংশিক | আংশিক | পরোক্ষ | না | না | **পদ্ধতিতে বেশি** |
| Spiess / Siddiq | হ্যাঁ | হ্যাঁ | না | না | না | ধারণায় বেশি, বস্তুতে কম |
| Rathnasuriya & Yang | হ্যাঁ | হ্যাঁ | না | হ্যাঁ | না | ধারণায় বেশি (code prediction-এ) |
| **CalibraPatch (প্রস্তাব)** | হ্যাঁ | হ্যাঁ | হ্যাঁ | হ্যাঁ | হ্যাঁ | — |

**সহজ কথায়:** প্রতিটা ঘর আলাদাভাবে কেউ না কেউ করেছে। কিন্তু agent patch-এর উপর **সবগুলো একসাথে, আর calibration দিয়ে মাপা** — এমন কাজ আমাদের search-এ পাওয়া যায়নি।

---

## ৬. Research Gap বিশ্লেষণ

### ৬.১ তোমার ৭টা প্রশ্নের উত্তর
1. **Agent patch-এর uncertainty-aware verification হয়েছে কি?** আংশিক। Model বা agent-এর নিজের confidence নিয়ে কাজ আছে (Spiess, Lin et al. 2026, XConf 2026)। Multi-signal patch evidence-এর uncertainty পাওয়া যায়নি।
2. **Reliability-calibrated evidence aggregation হয়েছে কি?** পদ্ধতি হিসেবে হ্যাঁ — WEAVER, Snorkel, Dawid–Skene। কিন্তু agent patch-এর test + security + adequacy + judge-এ পাওয়া যায়নি।
3. **Conflict-aware patch assessment হয়েছে কি?** আংশিক। RETRACE দুই LLM view-এর conflict ধরে; R2E-Gym আর Lenarduzzi et al. (JSS 2023) tool-দের অমিল মাপে। কিন্তু test/SAST/judge-এর conflict দিয়ে abstain করার পদ্ধতি পাওয়া যায়নি।
4. **Patch assurance-এ abstention হয়েছে কি?** হ্যাঁ, একটা আছে — Abstain and Validate (Google)। তবে LLM policy, calibrated নয়, risk–coverage দিয়ে মাপা নয়।
5. **কোনো framework কি এগুলো একসাথে করে?** আমাদের search-এ পাওয়া যায়নি।
6. **আসলে কী নেই?** নিচের table।
7. **CalibraPatch কি defensible novel contribution দিতে পারে?** হ্যাঁ, **যদি** দাবিটা সংকীর্ণ ও পরিমাপযোগ্য রাখা হয়। "নতুন fusion algorithm" দাবি করলে টিকবে না। "Agent patch acceptance-এ calibrated selective decision-এর প্রথম পরিমাপ" দাবি করলে টিকতে পারে।

### ৬.২ Gap-গুলো, ক্রম অনুযায়ী
| ক্রম | Gap | Novelty | SPL3-তে সম্ভব | Research মূল্য | প্রমাণ |
|---|---|---|---|---|---|
| **G1** | Agent patch-এর জন্য multi-signal evidence থেকে calibrated acceptance probability আর abstention; risk–coverage ও false assurance rate দিয়ে মাপা | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Search-এ পাওয়া যায়নি; সবচেয়ে কাছে Abstain and Validate |
| **G2** | একই patch set-এ প্রতিটা signal-এর reliability (precision, recall, failure rate) আর signal-দের মধ্যে conflict-এর হার — একটা joint empirical study | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | আলাদা আলাদা paper আছে (PatchDiff, Sajadi, All Smoke), একসাথে নেই |
| **G3** | Conflict আর missing evidence কি নিজেই ভুলের পূর্বাভাস দেয়? অর্থাৎ conflict-এ abstain করা কি শুধু low-confidence-এ abstain করার চেয়ে ভালো? | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | পাওয়া যায়নি |
| G4 | Assurance report দেখালে reviewer-এর false acceptance কমে কিনা (user study) | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | Papotti et al.-এর বিপরীত দিক; মানুষ লাগবে |
| G5 | Distribution-free গ্যারান্টি: conformal risk control দিয়ে "false assurance ≤ α" নিশ্চিত করা | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | পাওয়া যায়নি; কিন্তু বড় sample লাগে |

**সিদ্ধান্ত:** G2 হলো ভিত্তি (এটা ছাড়া কিছুই হয় না), G1 মূল contribution, G3 বাড়তি নতুনত্ব। G4 আর G5 future work বা journal extension।

**সতর্কতা:** "পাওয়া যায়নি" মানে "নেই" নয়। প্রায় ৫০টা search করা হয়েছে; প্রতি দুই মাসে আবার search করতে হবে, কারণ এই এলাকায় প্রতি মাসে নতুন preprint আসছে।

---

## ৭. Novelty মূল্যায়ন

| দাবি | টিকবে? | কারণ |
|---|---|---|
| "আমরা প্রথম multi-signal patch assurance framework বানিয়েছি" | **না** | TrustPatch-X, Comillas thesis, PatchBench, R2E-Gym |
| "আমরা নতুন reliability-aware fusion পদ্ধতি দিয়েছি" | **না** | WEAVER, Snorkel, Dawid–Skene আগেই আছে |
| "আমরা প্রথম patch-এ abstention দিয়েছি" | **না** | Abstain and Validate (ICSE-SEIP 2026) |
| "আমরা দেখিয়েছি agent patch-এর verification signal-গুলো কতটা নির্ভরযোগ্য ও কতটা পরস্পরবিরোধী" | **হ্যাঁ, সম্ভবত** | একই patch set-এ joint study পাওয়া যায়নি |
| "Calibrated selective acceptance একই coverage-এ false assurance কতটা কমায়, তার প্রথম পরিমাপ" | **হ্যাঁ, সম্ভবত** | Risk–coverage patch acceptance-এ পাওয়া যায়নি |
| "Conflict-aware abstention শুধু confidence-ভিত্তিক abstention-এর চেয়ে ভালো" | **হ্যাঁ, যদি ফল তাই বলে** | পাওয়া যায়নি; negative result-ও publishable |

**Novelty-র ধরন:** পদ্ধতিগত নয়, **empirical + framing**। এটা খারাপ নয় — EMSE আর JSS ঠিক এই ধরনের কাজ ছাপে। কিন্তু TSE-র জন্য যথেষ্ট নাও হতে পারে।

---

## ৮. চূড়ান্ত প্রস্তাবিত শিরোনাম

**"CalibraPatch: Calibrated, Abstention-Aware Acceptance of AI Coding Agent Patches from Heterogeneous Verification Evidence"**

বিকল্প (ছোট): *"Knowing When Not to Trust an Agent's Patch: Calibrated Multi-Signal Assurance with Abstention"*

**কেন এই শিরোনাম:** "Acceptance" শব্দটা দাবিকে সংকীর্ণ করে — আমরা patch বানাই না বা ranking করি না, শুধু গ্রহণের সিদ্ধান্ত মাপি। এতে RETRACE, R2E-Gym-এর সাথে পার্থক্য স্পষ্ট হয়। "PatchAssure" নাম বাদ — এটা Doble Engineering-এর বাণিজ্যিক product।

---

## ৯. চূড়ান্ত Research Objectives

1. একটা label করা dataset বানানো, যেখানে AI agent-এর test-pass করা patch-গুলো "গ্রহণযোগ্য / অগ্রহণযোগ্য / অনিশ্চিত" হিসেবে যাচাই করা।
2. একই patch-গুলোর উপর ৪–৫টা স্বাধীন verification signal চালিয়ে প্রতিটার নির্ভরযোগ্যতা আর তাদের conflict-এর হার মাপা।
3. Signal-গুলো থেকে একটা calibrated acceptance probability আর তিন-অবস্থার সিদ্ধান্ত (Accept / Reject / Insufficient Evidence) তৈরির সহজ, ব্যাখ্যাযোগ্য পদ্ধতি বানানো।
4. Baseline-এর তুলনায় false assurance, calibration আর coverage-এর trade-off মাপা।
5. একটা open-source tool আর replication package প্রকাশ করা।

---

## ১০. চূড়ান্ত Research Questions

### ১০.১ তোমার RQ-গুলোর বিচার
| RQ | Research-worthy? | আগেই উত্তর আছে? | SPL3-তে সম্ভব? | Q1-এ বাড়ানো যাবে? | রায় |
|---|---|---|---|---|---|
| RQ1 signal-এর reliability | হ্যাঁ | আংশিক, আলাদা আলাদা paper-এ | হ্যাঁ | হ্যাঁ | রাখো, ধারালো করো |
| RQ2 reliability-aware fusion | হ্যাঁ | পদ্ধতি আছে (WEAVER), patch-এ নেই | হ্যাঁ | হ্যাঁ | রাখো, metric স্পষ্ট করো |
| RQ3 uncertainty দিয়ে false assurance কমানো | **হ্যাঁ, সবচেয়ে বেশি** | পাওয়া যায়নি | হ্যাঁ | হ্যাঁ | মূল RQ বানাও |
| RQ4 explanation কতটা কার্যকর | হ্যাঁ, কিন্তু | না | **কঠিন** — মানুষের study লাগে | হ্যাঁ, user study দিয়ে | RQ থেকে সরাও; report-কে artifact রাখো |

**RQ4-এর সমস্যা:** "Explanation কতটা কার্যকর" মাপতে হলে মানুষকে report দেখিয়ে তাদের সিদ্ধান্ত মাপতে হয় (Papotti et al.-এর মতো)। এটা ethics, participant আর সময় চায়। SPL3-এ এটা ঝুঁকিপূর্ণ।

### ১০.২ প্রস্তাবিত নতুন RQ
- **RQ1 (Signal reliability ও conflict):** AI agent-এর test-pass করা patch-এ প্রতিটা verification signal অগ্রহণযোগ্য patch কতটা ধরে (recall), সঠিক patch কতটা ভুল করে বাতিল করে (false rejection), কতবার চালানোই যায় না (missing), আর signal-রা কতবার পরস্পরবিরোধী?
- **RQ2 (Calibrated fusion):** Signal-গুলো থেকে শেখা calibrated model কি tests-only, rule-ভিত্তিক, majority vote আর fixed weighted sum-এর চেয়ে ভালো discrimination (AUROC) আর calibration (ECE, Brier) দেয়?
- **RQ3 (Selective acceptance — মূল):** Abstention ব্যবহার করলে একই coverage-এ false assurance rate কতটা কমে, আর false assurance ≤ 5% রাখতে কত coverage ছাড়তে হয়?
- **RQ4 (Conflict-এর মূল্য):** Conflict আর missing evidence-এর উপর abstain করা কি শুধু low-confidence-এর উপর abstain করার চেয়ে ভালো risk–coverage দেয়?

**সহজ কথায়:** RQ1 = "প্রতিটা পরীক্ষা কতটা ভালো?" RQ2 = "সব মিলিয়ে সৎ সম্ভাবনা দেওয়া যায়?" RQ3 = "জানি না বললে কতটা কম ঠকি?" RQ4 = "পরীক্ষাগুলোর ঝগড়া কি নিজেই সতর্কসংকেত?"

---

## ১১. প্রস্তাবিত Architecture (সরল করা)

### ১১.১ তোমার architecture-এর component-ভিত্তিক বিচার
| Component | আগে কেউ করেছে? | রাখবো? | কারণ |
|---|---|---|---|
| Patch input ও context analyzer | হ্যাঁ (সব harness) | হ্যাঁ, সাধারণ | শুধু engineering |
| Functional + regression test | হ্যাঁ (SWE-bench F2P/P2P) | হ্যাঁ, একটা signal হিসেবে | দুটো আসলে একই test run থেকে আসে |
| Security analysis | হ্যাঁ (Sajadi, FCV) | হ্যাঁ, **delta** হিসেবে | Patch-এর আগে-পরে নতুন finding শুধু |
| Test adequacy | আংশিক (All Smoke, CoverUp) | হ্যাঁ | Changed line coverage + oracle strength — সস্তা ও শক্ত signal |
| Issue-patch alignment | হ্যাঁ (RETRACE, judge) | ঐচ্ছিক | API খরচ; বাজেট থাকলে একটা সস্তা LLM judge |
| Code quality | হ্যাঁ (Chen & Jiang) | **না** | Chen & Jiang-এ SonarQube কার্যত কিছু ধরেনি; noise বাড়াবে |
| Differential test | হ্যাঁ (PatchDiff) | হ্যাঁ, যদি সম্ভব | সবচেয়ে শক্ত correctness signal, কিন্তু LLM দিয়ে test বানাতে খরচ |
| Evidence reliability analyzer | পদ্ধতি আছে (WEAVER) | হ্যাঁ — **মূল** | এখানেই contribution |
| Conflict ও uncertainty engine | আংশিক | হ্যাঁ — **মূল** | এখানেই contribution |
| Assurance report | হ্যাঁ (TrustPatch-X) | হ্যাঁ, artifact হিসেবে | RQ নয় |

### ১১.২ সরল architecture
1. **Input:** Issue, base commit, agent-এর patch।
2. **Signal layer (৪–৫টা):**
   - S1 Test outcome: F2P ও P2P একসাথে (pass / fail / চালানো যায়নি)।
   - S2 Test adequacy: changed line-এর কত % test-এ চলে, আর সংশ্লিষ্ট test-এ oracle শক্ত কিনা (All Smoke taxonomy)।
   - S3 Security delta: Semgrep + Bandit-এ patch-এর পরে নতুন finding (সংখ্যা ও severity)।
   - S4 Differential behaviour (ঐচ্ছিক): একই issue-এর অন্য candidate বা regenerated test-এ আচরণের পার্থক্য।
   - S5 Issue alignment judge (ঐচ্ছিক): rubric-চালিত সস্তা LLM judge।
3. **Evidence vector:** প্রতিটা signal-এর মান + "missing" indicator (tool চলেনি বা প্রযোজ্য নয়)।
4. **Calibrated model:** সহজ logistic regression → isotonic বা Platt calibration → probability $p_i$।
5. **Conflict score:** কতগুলো signal "ভালো" আর কতগুলো "খারাপ" বলছে তার অমিল।
6. **Decision:** Accept / Reject / Insufficient Evidence (নিচে নিয়ম)।
7. **Report:** সিদ্ধান্ত, $p_i$, প্রতিটা signal-এর মান ও তার পরিচিত reliability, conflict, missing evidence, পরামর্শ।

**সহজ কথায়:** জটিল deep learning দরকার নেই। মূল কাজ তিনটা সংখ্যা: সম্ভাবনা, অমিল, আর কতটা প্রমাণ নেই।

---

## ১২. প্রস্তাবিত Methodology

1. **Patch সংগ্রহ:** SWE-bench Verified / Lite-এ প্রকাশিত agent submission-এর patch ব্যবহার (নিজে agent না চালিয়ে)। প্রথমে শুধু test-pass করা patch নেওয়া, কারণ প্রশ্নটা হলো "pass করা patch-কে বিশ্বাস করা যায় কিনা"।
2. **Ground truth তৈরি:** ধাপ ১৫.২-এ বিস্তারিত।
3. **Signal চালানো:** প্রতিটা patch-এ S1–S5; tool fail করলে "missing" লেখা, বাদ না দেওয়া।
4. **Model শেখা:** Repository-ভিত্তিক cross-validation (একই repository train আর test-এ একসাথে নয়), যাতে leakage না হয়।
5. **Calibration:** Training fold-এর ভেতরেই আলাদা calibration অংশ।
6. **Threshold নির্বাচন:** Validation-এ false assurance ≤ α রাখার মতো threshold বাছাই, তারপর test-এ মাপা।
7. **তুলনা ও statistics:** Baseline-এর সাথে একই patch-এ paired তুলনা, bootstrap CI।

---

## ১৩. গাণিতিক / Statistical পদ্ধতি

শুধু যেটুকু দরকার, তাই। প্রতিটার পরে সহজ ব্যাখ্যা।

### ১৩.১ Calibrated acceptance probability
$$p_i = \sigma\left( w_0 + \sum_{k=1}^{K} w_k s_{ik} + \sum_{k=1}^{K} v_k m_{ik} \right)$$

**এটা কী হিসাব করে:** Patch $i$ গ্রহণযোগ্য হওয়ার সম্ভাবনা।
- $s_{ik}$ = signal $k$-এর মান (যেমন নতুন security finding-এর সংখ্যা)।
- $m_{ik}$ = signal $k$ missing হলে 1, না হলে 0।
- $w_k$ = signal $k$ কতটা গুরুত্বপূর্ণ, data থেকে শেখা — এটাই "reliability weight"।
- $v_k$ = signal না থাকলে সম্ভাবনা কতটা বদলায়।
- $\sigma$ = sigmoid, যেকোনো সংখ্যাকে 0 থেকে 1-এ আনে।

তারপর isotonic regression দিয়ে $p_i$-কে calibrate করা।

**সহজ কথায়:** প্রতিটা পরীক্ষার কথা কতটা বিশ্বাস করবো, তা data নিজেই শিখবে। আর পরীক্ষা না হলে সেটাও হিসাবে ঢুকবে।

**Label ছাড়া বিকল্প (baseline):** Dawid–Skene বা Snorkel label model — label ছাড়াই signal-দের accuracy অনুমান করে। WEAVER এই পথে গেছে। এটা তুলনার জন্য ভালো।

### ১৩.২ Conflict score
$$c_i = \frac{\min(n^{+}_i, n^{-}_i)}{n^{+}_i + n^{-}_i}$$

**এটা কী হিসাব করে:** $n^{+}_i$ = কতগুলো signal "ভালো" বলছে, $n^{-}_i$ = কতগুলো "খারাপ" বলছে (missing বাদে)। সবাই একমত হলে $c_i = 0$; ঠিক অর্ধেক-অর্ধেক হলে $c_i = 0.5$।

**সহজ কথায়:** পরীক্ষাগুলো কতটা ঝগড়া করছে, তার মাপ।

### ১৩.৩ Evidence completeness
$$e_i = 1 - \frac{1}{K} \sum_{k=1}^{K} m_{ik}$$

**এটা কী হিসাব করে:** কত ভাগ signal আসলে চালানো গেছে। সব চললে 1।

### ১৩.৪ সিদ্ধান্তের নিয়ম
- $e_i < \epsilon$ হলে → **Insufficient Evidence** (প্রমাণ খুব কম)।
- নাহলে $c_i > \kappa$ হলে → **Insufficient Evidence** (প্রমাণ পরস্পরবিরোধী)।
- নাহলে $p_i \geq \tau_{acc}$ হলে → **Accept**।
- নাহলে $p_i \leq \tau_{rej}$ হলে → **Reject**।
- বাকি সব → **Insufficient Evidence**।

$\epsilon, \kappa, \tau_{acc}, \tau_{rej}$ validation data থেকে বাছাই করা হবে, হাতে বসানো নয়।

**সহজ কথায়:** প্রথমে দেখো প্রমাণ যথেষ্ট কিনা, তারপর দেখো প্রমাণ একমত কিনা, শেষে সম্ভাবনা দেখে সিদ্ধান্ত।

### ১৩.৫ যা ব্যবহার করবো না, আর কেন
- **Dempster–Shafer theory:** এখানে প্রয়োজনের চেয়ে জটিল; reviewer জিজ্ঞেস করবে logistic regression-এর চেয়ে কেন ভালো।
- **Deep neural network:** কয়েকশো label-এ overfit করবে, আর ব্যাখ্যা করা কঠিন।
- **Conformal risk control:** তত্ত্বে খুব সুন্দর ("false assurance ≤ α"-এর গ্যারান্টি), কিন্তু ভালো গ্যারান্টির জন্য বড় calibration set লাগে। Journal extension-এ রাখো (G5)।

---

## ১৪. Dataset ও Tool সুপারিশ

### ১৪.১ Java নাকি Python?
| দিক | Python | Java |
|---|---|---|
| AI agent-এর প্রকাশিত patch | প্রচুর (SWE-bench-এর শত শত submission) | কম (Multi-SWE-bench-এর মতো multi-language benchmark আছে বলে জানা; যাচাই করতে হবে) |
| আগে থেকে label করা data | PatchDiff (877 patch), Sajadi et al.-এর security finding — artifact প্রকাশ হয়েছে কিনা যাচাই করতে হবে | APCA dataset (Defects4J), কিন্তু সেগুলো পুরনো APR tool-এর patch, AI agent-এর নয় |
| Execution environment | SWE-bench Docker image তৈরি আছে | Maven build ধীর ও ভারী |
| তোমার অভিজ্ঞতা | মৌলিক | ভালো |
| Security tool | Semgrep, Bandit, CodeQL | Semgrep, SpotBugs + FindSecBugs, CodeQL |

**সুপারিশ:** **মূল experiment Python-এ।** কারণ agent patch আর label — দুটোই Python-এ বেশি, আর তুলনাযোগ্য আগের কাজও Python-এ। Java-কে "generalization study" হিসেবে পরে রাখো। তোমার Java দক্ষতা কাজে লাগবে tool-এর backend বা report service-এ (Spring Boot), আর পরে Java extension-এ।

### ১৪.২ Tool
| কাজ | Tool | খরচ | ৮ GB laptop-এ চলবে? |
|---|---|---|---|
| Test চালানো | SWE-bench harness + Docker | বিনামূল্যে | একবারে ১টা container, ধীরে; disk অনেক লাগে |
| Coverage | coverage.py | বিনামূল্যে | হ্যাঁ |
| Oracle strength | All Smoke-এর regex taxonomy নিজে implement | বিনামূল্যে | হ্যাঁ |
| Security | Semgrep CE, Bandit | বিনামূল্যে | হ্যাঁ |
| Security (ঐচ্ছিক) | CodeQL | Open-source research-এ বিনামূল্যে | ধীর, memory বেশি |
| Model ও statistics | scikit-learn, numpy, pandas, scipy | বিনামূল্যে | হ্যাঁ |
| LLM judge (ঐচ্ছিক) | সস্তা API model বা free tier | কম খরচ | API-তে চলে, local নয় |
| Java extension | JUnit 5, JaCoCo, SpotBugs, Maven | বিনামূল্যে | হ্যাঁ, ছোট project-এ |

**বাদ:** SonarQube (ভারী, আর code quality signal দুর্বল), OWASP Dependency-Check (patch dependency প্রায় বদলায় না)।

---

## ১৫. Experimental Design ও Evaluation Metric

### ১৫.১ Dataset প্রস্তুতি
1. ২–৩টা agent-এর SWE-bench Verified submission থেকে test-pass করা patch নেওয়া।
2. Pilot: 50টা patch পুরো pipeline-এ চালিয়ে সময় আর ব্যর্থতার হার মাপা।
3. মূল: অন্তত 300–500টা label করা patch লক্ষ্য। এর কম হলে ECE-র confidence interval খুব চওড়া হবে (আমার অনুমান; pilot-এর পরে ঠিক করো)।

### ১৫.২ Ground truth (সবচেয়ে গুরুত্বপূর্ণ)
কোনো একক উৎসকে চূড়ান্ত সত্য ধরা যাবে না। তাই স্তরে স্তরে:
1. **Developer-এর পূর্ণ test suite** চালানো (শুধু F2P/P2P নয়)। PatchDiff দেখিয়েছে 7.8% "correct" patch এতে fail করে।
2. **Differential evidence:** Developer-এর patch আর agent-এর patch আলাদা আচরণ করে এমন input খোঁজা।
3. **Security:** Patch-এর পরে নতুন finding থাকলে দুইজন মানুষ যাচাই করবে, আসল vulnerability কিনা।
4. **মানুষের label:** দুইজন rater, লিখিত rubric, Cohen's κ report। মতভেদ হলে তৃতীয়জন বা আলোচনা।
5. **"Uncertain" শ্রেণি রাখা:** Issue অস্পষ্ট হলে label = uncertain। মূল analysis-এ বাদ, কিন্তু আলাদা sensitivity analysis-এ রাখা।
6. **Circularity এড়ানো:** যে signal (যেমন differential test) ground truth বানাতে ব্যবহার হয়েছে, সেটা model-এর input হলে ফল ফুলে যাবে। তাই হয় ground truth-এর জন্য আলাদা, শক্তিশালী version (developer patch-এর সাথে তুলনা) রাখো, আর input-এ reference ছাড়া version — নয়তো এই সীমাবদ্ধতা স্পষ্ট লেখো।

**সহজ কথায়:** Ground truth মানে "সবচেয়ে ভালোভাবে যাচাই করা অনুমান", নিখুঁত সত্য নয়। তাই কীভাবে বানিয়েছি আর কোথায় দুর্বল, সেটা খোলাখুলি লিখতে হবে।

### ১৫.৩ Baseline
| Baseline | প্রযোজ্য? | কেন |
|---|---|---|
| B1 Tests-only (F2P + P2P pass হলে accept) | হ্যাঁ | আজকের মান; এর false assurance-ই মূল সমস্যা |
| B2 Rule-based AND (সব signal ভালো হলে accept) | হ্যাঁ | PatchBench-এর মতো কঠোর নিয়ম |
| B3 Majority vote | হ্যাঁ | Sajadi et al.-এর 2-of-3-এর মতো |
| B4 Fixed weighted sum | হ্যাঁ | TrustPatch-X-এর মতো |
| B5 Label model (Dawid–Skene / Snorkel) | হ্যাঁ | WEAVER-এর মতো unsupervised reliability |
| B6 Single LLM judge | ঐচ্ছিক | বাজেট থাকলে; RETRACE বা Abstain and Validate হুবহু reproduce করা কঠিন, এটা তাদের proxy |
| B7 Calibrated model, abstention ছাড়া | হ্যাঁ | Abstention-এর আলাদা অবদান মাপতে |
| **CalibraPatch** | — | Calibrated + conflict + abstention |

### ১৫.৪ Metric
| Metric | কী মাপে | কেন দরকার |
|---|---|---|
| False Assurance Rate (FAR) | Accept করা patch-এর মধ্যে কত ভাগ আসলে অগ্রহণযোগ্য | **মূল metric** — নিচে সূত্র |
| Coverage | কত ভাগ patch-এ সিদ্ধান্ত দেওয়া হলো (abstain নয়) | FAR কমাতে কত দাম দিচ্ছি |
| Risk–coverage curve ও AURC | Threshold বদলালে FAR আর coverage কীভাবে বদলায়; curve-এর নিচের ক্ষেত্রফল | Abstention-ভিত্তিক পদ্ধতির মানক তুলনা |
| Coverage at FAR ≤ 5% | 5% false assurance-এর মধ্যে থেকে কত patch সিদ্ধান্ত পায় | বাস্তবে সবচেয়ে বোধগম্য সংখ্যা |
| Recall of bad patches | অগ্রহণযোগ্য patch-এর কত ভাগ ধরা পড়ে (reject বা abstain) | নিরাপত্তার দিক |
| False rejection rate | ভালো patch-এর কত ভাগ ভুল করে reject | Developer-এর বিরক্তি |
| AUROC | সিদ্ধান্ত ছাড়া, শুধু ranking কতটা ভালো | Calibration থেকে আলাদা দক্ষতা |
| Brier score | সম্ভাবনা আর আসল ফলের গড় বর্গ-ভুল | Calibration + discrimination একসাথে |
| ECE | বলা সম্ভাবনা আর বাস্তব হারের গড় ফারাক | Calibration-এর সরাসরি মাপ |
| Abstention rate | কত ভাগ "Insufficient Evidence" | Coverage-এর উল্টো |
| Runtime | প্রতি patch-এ সময় | ব্যবহারযোগ্যতা |

Precision/Recall/F1 আলাদাভাবে দরকার নেই — FAR আর recall of bad patches আসলে সেগুলোরই সঠিক রূপ। Explanation quality RQ থেকে সরানো হয়েছে।

**FAR-এর সূত্র:**
$$\text{FAR} = \frac{\text{FA}}{\text{FA} + \text{TA}}$$
এখানে FA = accept করা কিন্তু অগ্রহণযোগ্য patch-এর সংখ্যা, TA = accept করা আর সত্যিই গ্রহণযোগ্য patch-এর সংখ্যা।

**সহজ কথায়:** "যেগুলোকে আমরা ঠিক বললাম, তার কতগুলো আসলে ভুল?"

**Brier score:**
$$\text{BS} = \frac{1}{n} \sum_{i=1}^{n} (p_i - y_i)^2$$
$y_i$ = 1 হলে patch গ্রহণযোগ্য, 0 হলে নয়। ছোট মান মানে ভালো।

**ECE:**
$$\text{ECE} = \sum_{b=1}^{B} \frac{n_b}{n} \cdot | \text{acc}_b - \text{conf}_b |$$
Patch-গুলোকে সম্ভাবনা অনুযায়ী $B$টা ভাগে ভাগ করা হয়। প্রতি ভাগে বলা গড় সম্ভাবনা ($\text{conf}_b$) আর আসল গ্রহণযোগ্যতার হার ($\text{acc}_b$)-এর পার্থক্য, ভাগের আকার দিয়ে গড়।

**সহজ কথায়:** "90% বললে কি সত্যিই 90% ঠিক?" ECE শূন্যের কাছে হলে হ্যাঁ। ছোট sample-এ equal-mass bin আর bootstrap CI ব্যবহার করো।

### ১৫.৫ Ablation
- প্রতিটা signal একটা একটা করে সরিয়ে।
- Missing indicator ছাড়া।
- Conflict নিয়ম ছাড়া (RQ4-এর উত্তর)।
- Calibration ছাড়া (raw logistic output)।

### ১৫.৬ Statistical test
- সব metric-এ patch-স্তরে **bootstrap 95% CI** (repository অনুযায়ী cluster bootstrap ভালো)।
- দুই পদ্ধতির accept সিদ্ধান্তের তুলনায় **McNemar test**।
- একাধিক তুলনায় Holm সংশোধন।

### ১৫.৭ Reproducibility
- সব tool-এর version, Docker image hash, random seed লেখা।
- Label, rubric, script আর raw signal output প্রকাশ (Zenodo)।
- LLM judge ব্যবহার করলে model-এর নাম, তারিখ, prompt আর temperature লেখা।

### ১৫.৮ Validity-র ঝুঁকি
| ধরন | ঝুঁকি | প্রতিকার |
|---|---|---|
| Construct | "গ্রহণযোগ্য" সংজ্ঞা বিষয়গত | Rubric, দুই rater, κ, uncertain শ্রেণি |
| Internal | Ground truth আর signal-এর circularity | ১৫.২-এর ধাপ ৬ |
| External | শুধু Python, শুধু SWE-bench, কয়েকটা agent | Java extension, SWE-bench Pro বা SWE-rebench task পরে |
| Conclusion | ছোট sample | Bootstrap CI, effect size, pilot থেকে sample আকার |
| Contamination | SWE-bench Verified-এর পরিচিত সমস্যা (OpenAI 2026) | আমরা agent-এর ক্ষমতা মাপছি না, patch-এর verification মাপছি — তবু সীমাবদ্ধতা লেখা |

---

## ১৬. Implementation Roadmap (১০ মাস)

| মাস | কাজ | Output |
|---|---|---|
| 1 | Beyond Bypass আর OpenAI post নিজে পড়া; supervisor-এর সাথে direction চূড়ান্ত; WSL2 + Docker setup | চূড়ান্ত proposal |
| 2 | প্রকাশিত agent patch সংগ্রহ; SWE-bench harness-এ ১০টা patch চালানো | কাজ করা harness |
| 3 | S1–S3 signal implement; 50-patch pilot; সময় ও disk মাপা | Pilot report |
| 4 | Labelling rubric; দ্বিতীয় rater খোঁজা; 100টা patch label, κ | প্রথম label set |
| 5 | বাকি label (300+ লক্ষ্য); S4/S5 যদি বাজেট থাকে | Label করা dataset |
| 6 | RQ1: signal reliability ও conflict analysis | প্রথম ফল; workshop paper draft |
| 7 | RQ2–RQ3: model, calibration, abstention, baseline | মূল ফল |
| 8 | RQ4 ও ablation; statistics | সম্পূর্ণ ফল |
| 9 | Report UI (Spring Boot বা সাধারণ web); replication package; paper লেখা | Tool v1, paper draft |
| 10 | Submission; SPL3 presentation | চূড়ান্ত |

**আগে কী শিখবে:** (১) Python pandas ও scikit-learn — logistic regression, calibration, cross-validation; (২) Docker ও WSL2; (৩) SWE-bench harness কীভাবে চলে; (৪) Semgrep ও Bandit-এর output পড়া; (৫) মৌলিক statistics — bootstrap, McNemar।

---

## ১৭. খরচ ও Hardware

| Setup | কী পাবে | খরচ (আমার অনুমান) | Hardware |
|---|---|---|---|
| **১. সম্পূর্ণ বিনামূল্যে** | প্রকাশিত patch, S1–S3 (+ regex oracle), logistic model, সব metric | 0 USD | তোমার ৮ GB laptop + বড় external disk; একবারে ১টা Docker container; ধীর কিন্তু সম্ভব |
| **২. ঐচ্ছিক কম খরচে** | উপরের সব + সস্তা LLM judge (S5) + LLM-generated differential test (S4) + কিছু cloud compute | প্রায় 20–80 USD | একটা ছোট cloud VM কয়েকদিনের জন্য, অথবা university server |
| **৩. উন্নত research** | নিজে agent চালিয়ে নতুন patch, SWE-bench Pro / multi-language, বড় label set, conformal extension | কয়েকশো USD বা বেশি | ১৬–৩২ GB RAM-এর machine বা cloud |

**মূল ঝুঁকি:** ৮ GB RAM-এ SWE-bench-এর কিছু repository-র Docker image build বা test খুব ধীর বা ব্যর্থ হতে পারে। প্রতিকার: pilot-এ মাপো; ব্যর্থ হলে "missing" হিসেবে রাখো (এটাই তোমার পদ্ধতির অংশ!); দরকারে university-র lab machine চাও। নিজে বড় model host করার দরকার নেই।

---

## ১৮. সম্ভাব্য Q1 Journal

| Journal | Scopus/SJR (2025) | Web of Science JCR (second-hand) | Scope | তোমার কাজের সাথে মিল | বাস্তবতা |
|---|---|---|---|---|---|
| Journal of Systems and Software (Elsevier) | Q1, SJR 0.950 | Q1, IF প্রায় 3.8–4.1 (উৎসে বছর নিয়ে গরমিল) | বিস্তৃত SE, empirical ও tool | ভালো | **সবচেয়ে বাস্তবসম্মত** |
| Empirical Software Engineering (Springer) | Q1, SJR 0.920 | Q2, IF 3.4 (2025 JCR) | কঠোর empirical study | খুব ভালো — RQ1–RQ3 empirical | বাস্তবসম্মত, কিন্তু statistics ও replication package-এ কড়া |
| IEEE Transactions on Software Engineering | Q1, SJR 1.568 | Q1, IF প্রায় 6.0 | Flagship SE | মিল আছে, কিন্তু উচ্চ novelty চায় | **খুবই উচ্চাভিলাষী** |

**গুরুত্বপূর্ণ:** SJR মান scimagojr.com-এর indexed পাতা থেকে (সরাসরি খোলা যায়নি); JCR মান secondary site থেকে। Proposal-এ লেখার আগে university library login দিয়ে Clarivate JCR-এ নিজে দেখো। Scopus quartile আর JCR quartile আলাদা জিনিস — একটা দিয়ে অন্যটা দাবি করো না (যেমন EMSE: Scopus Q1, কিন্তু JCR Q2)।

**কী থাকলে Q1-এর জন্য যথেষ্ট হবে না:**
- 100-এর কম label করা patch, বা একজন rater।
- শুধু tool জোড়া দেওয়া, কোনো পরিমাপযোগ্য দাবি নেই।
- Baseline হিসেবে শুধু "tests-only"।
- Abstain and Validate, WEAVER, Spiess, Siddiq-এর সাথে তুলনা বা আলোচনা না থাকা।
- কোনো replication package না থাকা।

**বাস্তব পথ:** প্রথমে RQ1-এর ফল নিয়ে একটা workshop বা short paper (যেমন IEEE AITest, LLM4Code, AI-SQE) → তারপর পুরো কাজ JSS বা EMSE-তে। Acceptance-এর কোনো নিশ্চয়তা নেই।

---

## ১৯. ঝুঁকি ও সীমাবদ্ধতা

| ঝুঁকি | সম্ভাবনা | প্রভাব | প্রতিকার |
|---|---|---|---|
| Label বানাতে অনেক সময় লাগা | বেশি | বেশি | Pilot; rubric; ছোট কিন্তু পরিষ্কার set; দ্বিতীয় rater আগেই ঠিক করা |
| খুব কম অগ্রহণযোগ্য patch (class imbalance) | মাঝারি | বেশি | Test-pass patch-এ ভুল প্রায় 10–30% (PatchDiff, AutoCodeRover থেকে); তবু imbalance-এ AUROC, Brier ব্যবহার; ভুল patch বেশি এমন agent বাছাই |
| Calibration-এর জন্য data কম | মাঝারি | মাঝারি | সরল model; equal-mass bin; bootstrap CI; conformal বাদ |
| কাছের নতুন কাজ প্রকাশিত হয়ে যাওয়া | মাঝারি | বেশি | প্রতি দুই মাসে search; দাবি সংকীর্ণ রাখা |
| ৮ GB laptop-এ harness না চলা | মাঝারি | মাঝারি | Missing হিসেবে রাখা; lab machine |
| Calibrated model tests-only-কে হারাতে না পারা | কম–মাঝারি | মাঝারি | Negative result-ও publishable; RQ1 নিজেই মূল্যবান |
| Ground truth-এ circularity | মাঝারি | বেশি | ১৫.২-এর ধাপ ৬ |

---

## ২০. চূড়ান্ত সুপারিশ: **MODIFY**

### ২০.১ পুরনো বনাম নতুন direction
| দিক | PatchAssure (পুরনো) | CalibraPatch (নতুন, পরিবর্তিত) |
|---|---|---|
| Novelty | কম — TrustPatch-X ইত্যাদি | মাঝারি থেকে ভালো — calibrated selective acceptance |
| Overlap | বেশি | মাঝারি (Abstain and Validate, WEAVER) |
| Gap | দুর্বল ("জোড়া দেওয়া") | স্পষ্ট ও পরিমাপযোগ্য (false assurance বনাম coverage) |
| প্রযুক্তিগত জটিলতা | মাঝারি (৮টা signal) | মাঝারি (৪–৫টা signal + সরল statistics) |
| Experiment-এর সম্ভাব্যতা | মাঝারি | মাঝারি — label-ই প্রধান খরচ |
| Scientific contribution | Tool | Tool + empirical finding + decision পদ্ধতি |
| Q1 সম্ভাবনা | কম–মাঝারি | মাঝারি (JSS/EMSE) |
| Undergraduate-এর জন্য উপযোগী | হ্যাঁ | হ্যাঁ, scope কমালে |
| দীর্ঘমেয়াদি সম্ভাবনা | সীমিত | ভালো — conformal guarantee, user study, multi-language |

**সিদ্ধান্ত:** নতুন direction বেশি শক্তিশালী। কিন্তু এটা আসলে PatchAssure-কে ফেলে দেওয়া নয়। Final Synthesis-এর PatchAssure-এ আগেই "তিন অবস্থার রায়", "যাচাই করা যায়নি" আর CG7 (confidence ও abstention) ছিল। CalibraPatch সেটারই ধারালো রূপ। PatchAssure-এর RQ2 ("প্রতিটা signal-এর ভুলের দিক") এখন CalibraPatch-এর RQ1।

### ২০.২ Final Synthesis-এ যা বদলাতে হবে
- §৪.১ শিরোনাম: PatchAssure → CalibraPatch (নাম-সংঘাত আর novelty দুই কারণেই)।
- §১০ Q1-এর উত্তর ("আগের কাজ একটা signal নিয়ে"): আর সঠিক নয়। TrustPatch-X, PatchBench, R2E-Gym multi-signal। নতুন উত্তর: "Multi-signal আছে, কিন্তু কেউ calibrated, abstaining সিদ্ধান্ত দেয় না বা false assurance মাপে না।"
- Signal S1–S8 থেকে ৪–৫টায় নামানো; S6 (static classifier) আর S8 (run consistency) future work।
- Agent চালানোর বদলে প্রকাশিত patch।

### ২০.৩ শুরু করার আগে ৫টা করণীয়
1. Beyond Bypass-এর PDF আর OpenAI post নিজে পড়া (আমি খুলতে পারিনি)।
2. Abstain and Validate (arXiv 2510.03217) আর WEAVER (arXiv 2506.18203) পুরো পড়া — এরাই reviewer-এর প্রথম প্রশ্ন।
3. PatchDiff-এর label আর SWE-bench submission-এর patch আসলে download করা যায় কিনা দেখা।
4. Supervisor-কে RQ1–RQ4 আর MODIFY-এর কারণ দেখানো।
5. প্রতি দুই মাসে "patch calibration abstention" ধরনের search আবার করা।

> **মনে রাখো:**
> CalibraPatch তখনই নতুন, যখন এটা "আরেকটা multi-signal tool" নয়, বরং "কখন একটা agent patch-কে বিশ্বাস করা যাবে না" — তার পরিমাপযোগ্য উত্তর।
> মূল সংখ্যা হবে: একই coverage-এ false assurance কতটা কমলো।
> সবচেয়ে কঠিন অংশ code নয়, ground truth label — সেখানেই বেশি সময় দাও।

---

## পরিশিষ্ট: যাচাইয়ের উৎস

| Item | উৎস | অবস্থা |
|---|---|---|
| Chen & Jiang | arxiv.org/abs/2410.12468 | ✅ |
| Sajadi et al. | arxiv.org/abs/2507.02976 | ✅ (preprint) |
| FCV | aclanthology.org/2026.acl-long.707 | ✅ |
| RETRACE | arxiv.org/abs/2608.08950 | ✅ (preprint) |
| Beyond Bypass | Crossref, DOI 10.1109/AITest70988.2026.00029 | ◐ শুধু metadata |
| All Smoke, No Alarm | arxiv.org/abs/2606.18168; Crossref | ✅ |
| OpenAI SWE-bench Verified | openai.com (403) | ◐ secondary উৎস |
| PatchDiff | arxiv.org/abs/2503.15223; ICSE 2026 | ✅ |
| PatchBench | arxiv.org/abs/2609.04075 | ✅ (preprint) |
| Papotti et al. | EMSE, DOI 10.1007/s10664-024-10506-z | ◐ final paper-এর সংখ্যা যাচাই হয়নি |
| TrustPatch-X | thesai.org, IJACSA Vol. 17 No. 4 | ✅ (পুরো PDF পড়া) |
| Abstain and Validate | arxiv.org/abs/2510.03217 | ✅ abstract |
| WEAVER | arxiv.org/abs/2506.18203 | ✅ abstract |
| Spiess et al. | arxiv.org/abs/2402.02047 | ✅ |
| Siddiq et al. | arxiv.org/abs/2606.31159 | ✅ abstract |
| Rathnasuriya & Yang | ICSE 2026 NIER (researchr) | ✅ |
| Journal quartile | scimagojr (indexed), bioxbio, journalmetrics | ◐ JCR নিজে যাচাই করতে হবে |
