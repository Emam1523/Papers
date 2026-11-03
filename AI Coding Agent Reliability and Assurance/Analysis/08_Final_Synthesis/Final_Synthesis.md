# Final Synthesis: AI Coding Agent Reliability and Assurance

> **ভিত্তি:** ৭টা sub-domain-এর ২৬টা paper-এর analysis, প্রতিটা sub-domain summary, আর October 2026-এর বর্তমান অবস্থার fact sheet (`00_Current_State_2026_Sources.md`)।
> **উদ্দেশ্য:** সব gap এক জায়গায় সাজানো, SPL3-তে সবচেয়ে মূল্যবান ও করা-সম্ভব gap বাছাই, চূড়ান্ত research প্রশ্ন, SPL3 software-এর পরিকল্পনা, ১০ মাসের timeline আর publication পরিকল্পনা।
> **সংশোধন (3 November 2026):** Research direction PatchAssure থেকে **CalibraPatch**-এ বদলানো হয়েছে। কারণ ও বিস্তারিত যাচাই: `09_CalibraPatch_Review/CalibraPatch_Review.md`। §১–§২ অপরিবর্তিত; §৩-এর শেষে নোট; §৪ থেকে নতুন করে লেখা।

---

## ১. পুরো Domain এক নজরে

| # | Sub-domain | Paper | এক লাইনে শিক্ষা |
|---|---|---|---|
| 1 | AI Coding Agents | SWE-bench, SWE-agent, AutoCodeRover, Agentless | Agent-এর score দ্রুত বেড়েছে, কিন্তু "test pass করা" patch-এর বড় অংশ আসলে ভুল (AutoCodeRover: 51/78 = 65.4% সঠিক) |
| 2 | Automated Program Repair | APR Survey, VRpilot, RePaCA | Patch overfitting পুরনো সমস্যা; LLM judge (RePaCA) overfitting ধরে কিন্তু অনেক সঠিক patch বাতিল করে |
| 3 | Coding-Agent Evaluation | SWE-rebench, SWE-Bench Pro, Engineering Reliable Coding Agents | Contamination, run-ভেদে পার্থক্য আর অস্পষ্ট task score-কে বিকৃত করে; একক weighted score ঠকানো যায় |
| 4 | LLM Test Generation | UniTSyn, CoverUp, TestDecision, ExecutionAgent, Oracle-Guided Selection | বেশি coverage ≠ শক্ত oracle; distinguishing test দিয়ে candidate বাছাই ভালো (68.2% থেকে 84.3%) |
| 5 | Patch Validation | HITL LLM-as-a-Judge, APCA Code Representation, Harden and Catch | Rubric ছাড়া মানুষও একমত নয়; judge-দের ভুলের দিক আলাদা; F1-এর বদলে precision ≥ 0.8-এ recall |
| 6 | Security of AI Code | CWEval, Security & Quality, ACCA (JSS), Enhancing Reliability, SecureVibeBench | Correct ≠ secure: সেরা agent মাত্র 23.8% correct-and-secure; scanner-এর প্রায় অর্ধেক সতর্কতা ভুল |
| 7 | Trustworthy AI for SE | Trustworthy AI SE, Proof-Carrying Completions, AI Assurance | Trust বহুমাত্রিক; process-ও যাচাই করতে হবে; proof শক্ত কিন্তু spec-নির্ভর |

**পুরো domain-এর মূল কথা (Supervisor-কে এক মিনিটে):**
> "২০২৩ থেকে ২০২৬-এ AI coding agent-এর benchmark score ২% থেকে প্রায় ৯৭%-এ উঠেছে, কিন্তু সেই score-এর বিশ্বাসযোগ্যতা ভেঙে পড়েছে: পুরনো benchmark-এ contamination আর ত্রুটিপূর্ণ test, test pass করা patch-এর বড় অংশ ভুল বা অনিরাপদ, একই agent বারবার চালালে ফল বদলায়, আর agent-রা কখনো verifier-কে ঠকায়। প্রশ্ন এখন 'agent কত % সমাধান করে' নয় — 'agent-এর একটা নির্দিষ্ট patch আমি কতটা বিশ্বাস করবো, আর কেন'। আমার SPL3 এই প্রশ্নের একটা পরিমাপযোগ্য উত্তর দেবে।"

---

## ২. সব Gap একসাথে (CG1–CG25), পাঁচটা বিষয়ে ভাগ করে

| বিষয় | Gap | কোন sub-domain-এ প্রমাণ | 2026-এ অবস্থা |
|---|---|---|---|
| **A. Patch সঠিক কিনা** | CG1 plausible ≠ correct | 1, 2, 3, 4, 5 | খোলা (PatchDiff: plausible patch-এর 29.6% আলাদা আচরণ করে) |
| | CG2 candidate selection | 1, 4 | খোলা (SWE-rebench pass@1 বনাম pass@5 ফাঁক 12–18 pt) |
| | CG17 judge-দের ভুলের দিক ও প্রকৃত হারে precision | 2, 5 | খোলা |
| | CG19 agent patch-এ লেখকের উদ্দেশ্য নেই | 5 | খোলা |
| | CG22 reference-বাঁধা oracle | 6 | খোলা |
| | CG23 spec-এর পর্যাপ্ততা | 7 | খোলা |
| **B. Test ও oracle** | CG3 test/validation-এর মান | 1–5 | খোলা (agent-এর test patch-এর 80.2%-এ দুর্বল oracle) |
| | CG13 generated test-এর oracle-শক্তি | 4, 5 | খোলা |
| | CG14 repository-level distinguishing test | 4 | খোলা |
| | CG15 test চালানোর পরিবেশ | 3, 4 | আংশিক (ExecutionAgent 33/50) |
| **C. Security** | CG5 patch-এর security | 1, 2, 6 | খোলা (SecPass 7.8–17.3%) |
| | CG20 একসাথে functional ও security রায় | 6 | খোলা |
| | CG21 security signal-এর নিজের নির্ভরযোগ্যতা | 6 | খোলা |
| **D. Evaluation-এর বিশ্বাসযোগ্যতা** | CG4 run-to-run variance | 1, 3, 6, 7 | খোলা |
| | CG6 contamination ও benchmark মান | 1, 2, 3 | খোলা, কোম্পানিরাও স্বীকার করছে |
| | CG8 evaluation-এর সমতা ও statistics | 2, 3 | আরও খারাপ (কোম্পানির দাবি বনাম স্বাধীন মাপ) |
| | CG9 অন্য language ও repository-level | 2–6 | খোলা |
| | CG10 assurance tool-এর নিজের validity | 2, 3, 5 | খোলা |
| | CG16 correctness label-এর validity | 5 | খোলা |
| | CG25 trust মাত্রার metric ও যাচাই করা threshold | 7 | খোলা |
| **E. ঠকানো ও প্রক্রিয়া** | CG7 confidence ও abstention | 1, 3 | খোলা |
| | CG11 verifier health ও version | 3, 7 | খোলা |
| | CG12 assurance signal-কে ঠকানো | 2, 3, 6, 7 | খোলা, সরাসরি প্রমাণ (GLM-5.2: 78.80% → 57.32%) |
| | CG18 judge-এর prompt injection robustness | 5 | খোলা (Opus 5.5 coding prompt injection 54.61% safeguard ছাড়া, কোম্পানির দাবি) |
| | CG24 trajectory-স্তরের assurance | 7 | খোলা |

---

## ৩. Gap বাছাই — কোনটা SPL3-এর জন্য সেরা

**বাছাইয়ের মাপকাঠি:** (১) গুরুত্ব — কত sub-domain-এ প্রমাণ; (২) 2026-এ নতুনত্ব — বর্তমান model-এ কেউ করেছে কিনা; (৩) SPL3-তে সম্ভব — ১০ মাস, একজন student, সীমিত টাকা ও GPU; (৪) data পাওয়া যায় কিনা; (৫) publication সম্ভাবনা।

| প্রার্থী direction | গুরুত্ব | 2026-এ নতুনত্ব | SPL3-তে সম্ভব | Data | Publication | মোট |
|---|---|---|---|---|---|---|
| **A. বহু-signal patch assurance (CG1, CG2, CG13, CG14, CG17)** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ (বর্তমান agent patch-এ judge যাচাই পাওয়া যায়নি) | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | **সেরা** |
| B. Agent patch-এর security assurance (CG5, CG20, CG21) | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ (security test বানানো কঠিন) | ⭐⭐⭐ | ⭐⭐⭐⭐ | ভালো, A-এর অংশ হিসেবে |
| C. Run-to-run reliability study (CG4) | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | A-এর evaluation-এ যোগ |
| D. Verifier gaming / leakage audit (CG12, CG24) | ⭐⭐⭐⭐ | ⭐⭐⭐ (SWE-Bench Pro Verified ইতিমধ্যে করেছে) | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | A-এর একটা signal হিসেবে |
| E. Formal proof-carrying patch (CG23) | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ (spec লেখা কঠিন) | ⭐⭐ | ⭐⭐⭐ | ঝুঁকিপূর্ণ |

**সিদ্ধান্ত (আমার সুপারিশ):** Direction **A** মূল কাজ; B, C, D তার অংশ হিসেবে; E বাদ (future work)।

**সংশোধনী নোট (3 November 2026):** Direction A-এর "নতুনত্ব ⭐⭐⭐⭐⭐" এখন আর পুরো সত্য নয়। নতুন যাচাইয়ে পাওয়া গেছে, কয়েকটা signal জোড়া দেওয়া patch validation আগেই আছে: TrustPatch-X (IJACSA 2026, স্থির weighted sum), PatchBench (arXiv 2609.04075, hard AND), R2E-Gym (NeurIPS 2025, hybrid verifier), আর একটা master's thesis (Comillas 2026)। কিন্তু এদের কেউই **calibrated সম্ভাবনা, signal-এর conflict ধরা, আর প্রমাণ কম হলে abstention** দেয় না। তাই direction A টিকে আছে, কিন্তু তার কেন্দ্র সরে গেছে CG7 (confidence ও abstention), CG10, CG21 আর CG25-এর দিকে। নতুন রূপ নিচে।

---

## ৪. চূড়ান্ত Research Direction ও প্রশ্ন

### ৪.১ শিরোনাম
**"CalibraPatch: Calibrated, Abstention-Aware Acceptance of AI Coding Agent Patches from Heterogeneous Verification Evidence"**

পুরনো নাম "PatchAssure" বাদ, দুই কারণে: (১) এটা Doble Engineering-এর একটা বাণিজ্যিক product-এর নাম; (২) শুধু "multi-signal assurance report" এখন আর নতুন দাবি নয়।

### ৪.২ মূল ধারণা
AI agent একটা patch দিলে, test pass করলেই গ্রহণ না করে, কয়েকটা আলাদা signal থেকে তিনটা জিনিস হিসাব হবে:
- **Calibrated acceptance probability** $p$ — "90%" বললে এমন patch-এর সত্যিই প্রায় 90% গ্রহণযোগ্য হতে হবে।
- **Conflict score** — signal-রা কতটা পরস্পরবিরোধী।
- **Evidence completeness** — কতগুলো signal আসলে চালানো গেছে।

এই তিনটা থেকে সিদ্ধান্ত: **Accept / Reject / Insufficient Evidence**। মূল লক্ষ্য **false assurance** কমানো — খারাপ patch-কে "ঠিক আছে" বলা।

| Signal | কী যাচাই করে | কোন paper থেকে | Gap |
|---|---|---|---|
| S1 Test outcome | F2P ও P2P একসাথে: pass / fail / চালানো যায়নি | SWE-bench, Agentless | CG3 |
| S2 Test adequacy | Changed line-এর coverage, আর সংশ্লিষ্ট test-এ oracle শক্ত কিনা (All Smoke, No Alarm-এর taxonomy) | CoverUp, TestDecision, All Smoke No Alarm | CG3, CG13 |
| S3 Security delta | Semgrep ও Bandit-এ patch-এর পরে নতুন finding | CWEval, Sajadi et al., SecureVibeBench | CG5, CG20, CG21 |
| S4 Differential behaviour (ঐচ্ছিক) | অন্য candidate বা generated test-এ আচরণের পার্থক্য | Oracle-Guided Selection, PatchDiff | CG1, CG2, CG14 |
| S5 Issue alignment judge (ঐচ্ছিক) | Rubric-চালিত সস্তা LLM judge | HITL LLM-as-a-Judge, RETRACE | CG1, CG17 |

**বাদ দেওয়া (future work):** পুরনো S1 leakage/trajectory check, S6 static classifier, S8 run consistency। Code quality signal-ও বাদ — Chen & Jiang (SANER 2025)-এ SonarQube patch-এর আগে-পরে কার্যত কিছুই ধরেনি।

### ৪.৩ Research Questions
- **RQ1 (Signal reliability ও conflict):** AI agent-এর test-pass করা patch-এ প্রতিটা signal অগ্রহণযোগ্য patch কতটা ধরে, সঠিক patch কতটা ভুল করে বাতিল করে, কতবার চালানোই যায় না, আর signal-রা কতবার পরস্পরবিরোধী?
- **RQ2 (Calibrated fusion):** Signal থেকে শেখা calibrated model কি tests-only, rule-ভিত্তিক, majority vote আর fixed weighted sum-এর চেয়ে ভালো AUROC, ECE ও Brier দেয়?
- **RQ3 (Selective acceptance — মূল):** Abstention ব্যবহার করলে একই coverage-এ false assurance rate কতটা কমে, আর false assurance ≤ 5% রাখতে কত coverage ছাড়তে হয়?
- **RQ4 (Conflict-এর মূল্য):** Conflict আর missing evidence-এর উপর abstain করা কি শুধু low-confidence-এর উপর abstain করার চেয়ে ভালো risk–coverage দেয়?

**সহজ কথায়:** RQ1 = "প্রতিটা পরীক্ষা কতটা ভালো?" RQ2 = "সব মিলিয়ে সৎ সম্ভাবনা দেওয়া যায়?" RQ3 = "জানি না বললে কতটা কম ঠকি?" RQ4 = "পরীক্ষাগুলোর ঝগড়া কি নিজেই সতর্কসংকেত?"

Explanation-এর কার্যকারিতা RQ নয় (user study লাগে); assurance report একটা artifact হিসেবে থাকবে।

### ৪.৪ সবচেয়ে কাছের কাজ ও পার্থক্য
| কাজ | কী করে | CalibraPatch-এর পার্থক্য |
|---|---|---|
| Abstain and Validate (Google, ICSE-SEIP 2026) | LLM policy দিয়ে abstain + LLM critic | Calibrated, multi-signal, risk–coverage দিয়ে মাপা |
| WEAVER (ICML 2025) | Weak verifier-দের reliability শিখে মেলায় | Math/reasoning-এ; আমরা agent patch-এ, abstention সহ |
| TrustPatch-X (IJACSA 2026) | স্থির weighted sum + explanation | Weight data থেকে শেখা, calibration, conflict, abstention |
| RETRACE (arXiv 2608.08950) | Issue-patch দুই দিক মিলিয়ে conflict | Test, security, adequacy signal সহ; সিদ্ধান্ত calibrated |
| Spiess (ICSE 2025), Siddiq (2026) | Code model-এর confidence calibration, "False Trust" | Model-এর confidence নয়, verification evidence-এর calibration |

---

## ৫. Evaluation পরিকল্পনা

| দিক | পরিকল্পনা | কেন |
|---|---|---|
| Patch | SWE-bench Verified / Lite-এর প্রকাশিত agent submission থেকে test-pass করা patch; নিজে agent চালানো নয় | খরচ শূন্য, ৮ GB laptop-এ সম্ভব |
| Language | মূল experiment Python; Java পরে generalization হিসেবে | Agent patch আর label Python-এ বেশি; CG9 |
| আকার | 50-patch pilot, তারপর 300–500টা label করা patch লক্ষ্য | Calibration মাপতে কয়েকশো label লাগে |
| Ground truth | Developer-এর পূর্ণ test suite + differential evidence + security finding-এর মানব যাচাই + দুজন rater, rubric, Cohen's κ; "uncertain" শ্রেণি আলাদা | CG16; PatchDiff-এ 66.2% uncertain ছিল |
| Model | Logistic regression + missing indicator → isotonic/Platt calibration | সরল, ব্যাখ্যাযোগ্য, অল্প data-য় চলে |
| Metric | False assurance rate, coverage, risk–coverage ও AURC, coverage at FAR ≤ 5%, AUROC, Brier, ECE, bad-patch recall, false rejection | CG7, CG25 |
| Baseline | (১) tests-only; (২) rule AND; (৩) majority vote; (৪) fixed weighted sum (TrustPatch-X-ধরনের); (৫) Dawid–Skene/Snorkel label model (WEAVER-ধরনের); (৬) calibrated, abstention ছাড়া; ঐচ্ছিক (৭) একক LLM judge | তুলনা |
| Statistics | Repository-ভিত্তিক cross-validation, cluster bootstrap CI, McNemar, Holm সংশোধন | CG4, CG8 |
| Validity | Ground truth আর signal-এর circularity এড়ানো, version লেখা | CG10, CG11 |

**খরচ:** সম্পূর্ণ বিনামূল্যে শুরু করা যায় (S1–S3)। ঐচ্ছিক S4/S5-এর জন্য প্রায় 20–80 USD (অনুমান; pilot-এর পরে ঠিক হবে)।

---

## ৬. SPL3 Software পরিকল্পনা

SPL3-এর নিয়ম অনুযায়ী আগে paper-এর কাজ software-এ implement করতে হবে, তারপর gap সমাধান।

| অংশ | Module | কী করে | কোন paper implement হচ্ছে |
|---|---|---|---|
| **ধাপ ১: Paper implementation** | Patch loader ও harness | প্রকাশিত agent patch load, Docker-এ F2P/P2P চালানো | SWE-bench |
| | Oracle-strength checker | Test-এর oracle দুর্বল না শক্ত, regex taxonomy দিয়ে | All Smoke, No Alarm |
| | Security delta | Semgrep + Bandit, patch-এর আগে-পরে, 2-of-3-ধরনের voting baseline | Sajadi et al., CWEval |
| | Baseline aggregator | Tests-only, rule AND, majority vote, fixed weighted sum | TrustPatch-X, PatchBench |
| **ধাপ ২: Gap সমাধান** | Calibrated model | Logistic + calibration, missing indicator | নিজস্ব |
| | Conflict ও completeness | $c_i$ আর $e_i$ হিসাব | নিজস্ব |
| | Decision engine | Accept / Reject / Insufficient Evidence, validation থেকে threshold | নিজস্ব |
| | Assurance report ও dashboard | সিদ্ধান্ত, সম্ভাবনা, conflict, missing evidence; risk–coverage curve | নিজস্ব (Spring Boot বা সাধারণ web) |

**অন্য researcher কীভাবে ব্যবহার করবে:** যেকোনো agent-এর patch আর issue দিলে tool একটা calibrated সিদ্ধান্ত আর report দেবে; নতুন signal plugin হিসেবে যোগ করা যাবে, আর model নতুন label দিয়ে আবার calibrate করা যাবে।

---

## ৭. ১০ মাসের Timeline (প্রস্তাব)

| মাস | কাজ | Output |
|---|---|---|
| 1 | Beyond Bypass ও OpenAI post নিজে পড়া; Abstain and Validate ও WEAVER পড়া; supervisor-এর সাথে direction চূড়ান্ত; WSL2 + Docker | চূড়ান্ত proposal |
| 2 | প্রকাশিত agent patch সংগ্রহ; harness-এ ১০টা patch চালানো | কাজ করা harness |
| 3 | S1–S3 implement; 50-patch pilot; সময় ও disk মাপা | Pilot report |
| 4 | Labelling rubric; দ্বিতীয় rater; 100টা patch label, κ | প্রথম label set |
| 5 | বাকি label (300+ লক্ষ্য); বাজেট থাকলে S4/S5 | Label করা dataset |
| 6 | RQ1: signal reliability ও conflict | প্রথম ফল; workshop paper draft |
| 7 | RQ2–RQ3: model, calibration, abstention, baseline | মূল ফল |
| 8 | RQ4 ও ablation; statistics | সম্পূর্ণ ফল |
| 9 | Report UI; replication package; paper লেখা | Tool v1, paper draft |
| 10 | Submission; SPL3 presentation | চূড়ান্ত |

---

## ৮. Publication পরিকল্পনা

| স্তর | Venue | কী পাঠানো যায় |
|---|---|---|
| প্রথম | Workshop বা short paper (যেমন IEEE AITest, LLM4Code, AI-SQE) | RQ1: agent patch-এর verification signal কতটা নির্ভরযোগ্য ও পরস্পরবিরোধী |
| মূল (বাস্তবসম্মত) | Journal of Systems and Software (Scopus Q1; JCR Q1, second-hand) | RQ1–RQ4 সম্পূর্ণ, tool ও replication package সহ |
| মূল (বাস্তবসম্মত, কড়া) | Empirical Software Engineering (Scopus Q1; JCR Q2, second-hand) | একই, আরও কঠোর statistics ও threats to validity |
| উচ্চাভিলাষী | IEEE TSE, বা ICSE/FSE/ASE research track | বড় dataset, Java extension, conformal guarantee যোগ হলে |

Proposal-এ quartile লেখার আগে Clarivate JCR library login দিয়ে নিজে দেখতে হবে। Scopus আর JCR quartile আলাদা।

**Paper-এর মূল দাবি (আশা):** "Test pass-এর বদলে calibrated, abstention-সহ সিদ্ধান্ত নিলে একই coverage-এ false assurance কমে; আর signal-দের conflict নিজেই ভুলের পূর্বাভাস দেয়।" — দাবিটা experiment-এর ফলের উপর নির্ভর করবে।

**Validity-র ঝুঁকি (আগে থেকে লিখে রাখা):** label-এর বিষয়গততা, ground truth ও signal-এর circularity, শুধু Python ও SWE-bench, ছোট sample-এ ECE-র অনিশ্চয়তা, SWE-bench Verified-এর পরিচিত contamination।

---

## ৯. ঝুঁকি ও সমাধান

| ঝুঁকি | সমাধান |
|---|---|
| Label বানাতে বেশি সময় | Pilot; rubric; দ্বিতীয় rater আগেই ঠিক; ছোট কিন্তু পরিষ্কার set |
| অগ্রহণযোগ্য patch খুব কম (imbalance) | Test-pass patch-এ ভুল প্রায় 10–30%; AUROC ও Brier; ভুল বেশি এমন agent বাছাই |
| Calibration-এর জন্য data কম | সরল model; equal-mass bin; bootstrap CI; conformal পরে |
| ৮ GB laptop-এ Docker harness না চলা | "Missing" হিসেবে রাখা (পদ্ধতিরই অংশ); lab machine |
| Calibrated model tests-only-কে হারাতে না পারা | Negative result-ও publishable; RQ1 নিজেই মূল্যবান |
| কাছের নতুন কাজ প্রকাশিত হয়ে যাওয়া | প্রতি দুই মাসে search; দাবি সংকীর্ণ রাখা |

---

## ১০. Supervisor-এর সম্ভাব্য প্রশ্ন

**Q1. তোমার কাজ কেন নতুন?**
A: Multi-signal patch validation আগেই আছে (TrustPatch-X, PatchBench, R2E-Gym), আর abstention-ও আছে (Google-এর Abstain and Validate)। কিন্তু কেউ agent patch-এর জন্য ভিন্ন ভিন্ন verification signal থেকে **calibrated** সম্ভাবনা দেয় না, signal-দের conflict ধরে abstain করে না, আর **false assurance বনাম coverage** মাপে না। আমার কাজ সেই পরিমাপ।

**Q2. WEAVER তো ইতিমধ্যে verifier-দের reliability শিখে মেলায় — তফাত কী?**
A: WEAVER math ও reasoning-এ, ranking-এর জন্য। আমরা agent patch-এ, absolute গ্রহণ-সিদ্ধান্তের জন্য, abstention আর risk–coverage দিয়ে। WEAVER-ধরনের label model আমাদের একটা baseline।

**Q3. Ground truth কীভাবে ঠিক করবে?**
A: Developer-এর পূর্ণ test suite, developer patch-এর সাথে আচরণের তুলনা, security finding-এর মানব যাচাই, আর দুজন rater shared rubric দিয়ে (Cohen's κ)। অস্পষ্ট issue-কে "uncertain" রাখবো — PatchDiff-এ এমন ছিল 66.2%।

**Q4. খরচ সামলাবে কীভাবে?**
A: নিজে agent চালাবো না; প্রকাশিত patch ব্যবহার করবো। মূল signal (test, adequacy, security) সম্পূর্ণ বিনামূল্যের tool-এ চলে।

**Q5. যদি calibrated model tests-only-এর চেয়ে ভালো না হয়?**
A: সেটাও ফল — "এই signal-গুলো দিয়ে false assurance কমানো যায় না" — আর RQ1-এর signal reliability ফল এমনিতেই মূল্যবান।

---

## ১১. Supervisor-কে দেখানোর আগে যা যাচাই করতে হবে
1. Beyond Bypass (IEEE AITest 2026)-এর PDF university access দিয়ে পড়া — এর বিষয়বস্তু এখনো যাচাই হয়নি।
2. OpenAI-এর "Why SWE-bench Verified no longer measures frontier coding capabilities" নিজে browser-এ খুলে সংখ্যা (59.4% ইত্যাদি) মেলানো।
3. Abstain and Validate (arXiv 2510.03217) ও WEAVER (arXiv 2506.18203) পুরো পড়া।
4. PatchDiff-এর label আর SWE-bench submission-এর patch download করা যায় কিনা দেখা।
5. JSS, EMSE, TSE-এর JCR quartile Clarivate-এ নিজে দেখা।
6. প্রতি দুই মাসে "patch calibration abstention" ধরনের search আবার করা।
