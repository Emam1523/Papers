# Final Synthesis: AI Coding Agent Reliability and Assurance

> **ভিত্তি:** ৭টা sub-domain-এর ২৬টা paper-এর analysis, প্রতিটা sub-domain summary, আর October 2026-এর বর্তমান অবস্থার fact sheet (`00_Current_State_2026_Sources.md`)।
> **উদ্দেশ্য:** সব gap এক জায়গায় সাজানো, SPL3-তে সবচেয়ে মূল্যবান ও করা-সম্ভব gap বাছাই, চূড়ান্ত research প্রশ্ন, SPL3 software-এর পরিকল্পনা, ১০ মাসের timeline আর publication পরিকল্পনা।

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

---

## ৪. চূড়ান্ত Research Direction ও প্রশ্ন

### ৪.১ শিরোনাম (প্রস্তাব)
**"PatchAssure: Multi-Signal Assurance Reports for Patches from AI Coding Agents"**

### ৪.২ মূল ধারণা
AI agent একটা issue-এর জন্য patch দিলে, test pass করলেই গ্রহণ না করে, একটা **assurance report** তৈরি হবে। এতে কয়েকটা **আলাদা** signal থাকবে — কোনো weighted একক score নয় — প্রতিটার রায় তিন অবস্থার একটা (pass / fail / যাচাই করা যায়নি), সাথে অনিশ্চয়তা আর tool/model version।

| Signal | কী যাচাই করে | কোন paper থেকে | Gap |
|---|---|---|---|
| S1 Leakage ও trajectory check | Agent .git history, network বা test file থেকে উত্তর নিয়েছে বা test বদলেছে কিনা | SWE-Bench Pro Verified, Agentless, Trustworthy AI SE | CG12, CG24 |
| S2 Regression check | Project-এর নিজের test, patch-এর আগে-পরে | Agentless, SWE-bench | CG3 |
| S3 Patch-targeted test | Patch যে line বদলেছে সেগুলো চালায় এমন generated test, mutation score সহ | CoverUp, TestDecision | CG13 |
| S4 Distinguishing test | একই issue-এর কয়েকটা candidate patch যেখানে আলাদা আচরণ করে, সেই input-এ issue থেকে সঠিক output অনুমান | Oracle-Guided Selection | CG2, CG14 |
| S5 Rubric-চালিত LLM judge | Issue থেকে rubric বানিয়ে patch বিচার | HITL LLM-as-a-Judge | CG1, CG17 |
| S6 Static correctness classifier | RePaCA-ধরনের reasoning judge (বা graph-ভিত্তিক classifier) | RePaCA, APCA Representation | CG1, CG17 |
| S7 Security delta | Patch-এর আগে-পরে নতুন security finding; সম্ভব হলে execution-ভিত্তিক check | CWEval, SecureVibeBench | CG5, CG20, CG21 |
| S8 Run consistency | একই agent কয়েকবার চালালে একই আচরণের patch আসে কিনা (pass^k) | SWE-rebench, AI Assurance | CG4 |

### ৪.৩ Research Questions
- **RQ1 (সমস্যার আকার):** বর্তমান AI coding agent-দের test-pass করা patch-এর কত অংশ আসলে ভুল বা অনিরাপদ — contamination-মুক্ত task-এ, মানুষের যাচাই করা label দিয়ে?
- **RQ2 (প্রতিটা signal):** প্রতিটা signal (S1–S8) আলাদাভাবে কতটা ভুল patch ধরে, আর কতটা সঠিক patch ভুল করে বাতিল করে (recall, specificity, precision ≥ 0.8-এ recall)? Signal-গুলোর ভুলের দিক কি আলাদা?
- **RQ3 (একসাথে):** আলাদা signal-গুলো একসাথে দেখালে (একক score না বানিয়ে) কি candidate patch বাছাই উন্নত হয় (Agentless-ধরনের majority vote-এর তুলনায়), আর "যাচাই করা যায়নি" কতবার আসে?
- **RQ4 (নির্ভরযোগ্যতা ও robustness):** Assurance report নিজে কতটা স্থির (বারবার চালালে একই রায়?) আর judge-ভিত্তিক signal কি patch-এর ভেতরের প্ররোচনায় (comment-এ লুকানো নির্দেশ) ঠকে?

---

## ৫. Evaluation পরিকল্পনা

| দিক | পরিকল্পনা | কেন |
|---|---|---|
| Task | SWE-rebench-এর সর্বশেষ window থেকে নতুন task (contamination এড়াতে) + SWE-Bench Pro Verified-এর সংশোধিত subset (বহু-ভাষা) | CG6, CG9 |
| Agent | অন্তত একটা বর্তমান সস্তা model (যেমন GPT-6.1 Sol বা open-weight Kimi/GLM) mini-SWE-agent harness-এ; আর প্রকাশিত trajectory/patch যেখানে পাওয়া যায় | খরচ, CG8 |
| Candidate | প্রতিটা task-এ কয়েকটা (যেমন 5) patch | S4, S8 |
| Ground truth | দুজন rater, shared rubric, Cohen's κ report; বিতর্কিত ক্ষেত্র আলাদা; developer-এর পূর্ণ test suite চালানো | CG16, HITL-এর শিক্ষা |
| Metric | Recall, specificity, precision ≥ 0.8-এ recall, প্রকৃত হারে precision, "যাচাই করা যায়নি"-এর হার | CG17, Harden and Catch |
| Statistics | Bootstrap CI, McNemar paired test, একাধিক run | CG4, CG8 |
| Baseline | (১) শুধু test pass; (২) শুধু একটা LLM judge; (৩) majority vote (Agentless) | তুলনা |
| Validity | Repository-ভিত্তিক split, label-উৎস নিয়ন্ত্রণ, version লেখা | CG10, CG11 |

**আকার ও খরচ (প্রাথমিক):** প্রথমে 5টা task-এ pilot চালিয়ে প্রতি task-এর আসল খরচ মাপা হবে; তারপর 60–100 task-এ মূল experiment। খরচের সংখ্যা এখনই নিশ্চিত বলা যাচ্ছে না — pilot-এর পরে ঠিক হবে।

---

## ৬. SPL3 Software পরিকল্পনা

SPL3-এর নিয়ম অনুযায়ী আগে paper-এর কাজ software-এ implement করতে হবে, তারপর gap সমাধান।

| অংশ | Module | কী করে | কোন paper implement হচ্ছে |
|---|---|---|---|
| **ধাপ ১: Paper implementation** | Task loader ও harness | SWE-rebench / SWE-Bench Pro task load, Docker-এ চালানো, F2P/P2P evaluation | SWE-bench, SWE-rebench |
| | Candidate generator | Agentless-ধরনের pipeline বা mini-SWE-agent দিয়ে কয়েকটা patch | Agentless, SWE-agent |
| | Baseline judge | Rubric-চালিত LLM judge | HITL LLM-as-a-Judge |
| | Baseline selector | Majority vote ও distinguishing-test selection | Agentless, Oracle-Guided Selection |
| **ধাপ ২: Gap সমাধান** | Signal S1–S8 | উপরের table অনুযায়ী | নিজস্ব |
| | Assurance report | প্রতিটা signal আলাদা, তিন-অবস্থার রায়, CI ও version | নিজস্ব |
| | Evaluation dashboard | Recall/specificity, R@P=0.8, CI, signal-ভিত্তিক তুলনা | নিজস্ব |

**অন্য researcher কীভাবে ব্যবহার করবে:** যেকোনো agent-এর patch আর issue দিলে tool একটা assurance report দেবে; আর নতুন signal plugin হিসেবে যোগ করা যাবে।

---

## ৭. ১০ মাসের Timeline (প্রস্তাব)

| মাস | কাজ | Output |
|---|---|---|
| 1 | Literature চূড়ান্ত, supervisor-এর সাথে direction ঠিক, পরিবেশ (WSL2 + Docker) তৈরি | Proposal |
| 2–3 | ধাপ ১: harness, candidate generator, baseline judge ও selector | কাজ করা prototype |
| 3 | 5-task pilot: খরচ ও সময় মাপা | Pilot report |
| 4 | Ground-truth labelling protocol, দুজন rater, κ | Labelled dataset (ছোট) |
| 5–6 | ধাপ ২: signal S1–S8 ও assurance report | Tool v1 |
| 7 | মূল experiment (RQ1–RQ3) | Result tables |
| 8 | Robustness ও reliability (RQ4), ablation | Result tables |
| 9 | Paper লেখা, tool documentation | Paper draft, release |
| 10 | Submission, SPL3 presentation | Final |

---

## ৮. Publication পরিকল্পনা

| স্তর | Venue (সাধারণ নির্দেশনা) | কী পাঠানো যায় |
|---|---|---|
| প্রথম | Workshop (যেমন LLM4Code, AI-SQE-ধরনের AI-for-software-quality workshop) | RQ1 + pilot ফল: বর্তমান agent patch-এর কত অংশ ভুল/অনিরাপদ |
| মূল | ICSE, FSE, ASE, ISSTA (research track) বা journal: EMSE, JSS, IST, TOSEM | RQ1–RQ4 সম্পূর্ণ, tool artifact সহ |

**Paper-এর মূল দাবি (আশা):** "Test pass করা এখন যথেষ্ট নয়; আলাদা আলাদা signal আর তাদের ভুলের দিক দেখিয়ে আমরা বর্তমান agent-এর patch সম্পর্কে আরও বিশ্বাসযোগ্য সিদ্ধান্ত নিতে পারি।" — দাবিটা experiment-এর ফলের উপর নির্ভর করবে।

**Validity-র ঝুঁকি (আগে থেকে লিখে রাখা):** ছোট sample, label-এর বিষয়গততা, একটা harness, LLM judge-এর নিজের contamination, খরচের কারণে সীমিত model।

---

## ৯. ঝুঁকি ও সমাধান

| ঝুঁকি | সমাধান |
|---|---|
| API খরচ বেশি | Pilot আগে; সস্তা বা open-weight model; প্রকাশিত patch/trajectory ব্যবহার |
| Docker environment build ব্যর্থ | SWE-rebench-এর তৈরি image; "যাচাই করা যায়নি" হিসেবে report |
| Label বানাতে বেশি সময় | ছোট কিন্তু সাবধানে label করা set; rubric দিয়ে দ্রুত |
| Distinguishing test repository-level-এ কাজ না করা | এটাই একটা ফলাফল হিসেবে report (negative result-ও মূল্যবান) |
| নতুন কাজ আগেই প্রকাশিত হয়ে যাওয়া | প্রতি দুই মাসে literature check; fact sheet আপডেট |

---

## ১০. Supervisor-এর সম্ভাব্য প্রশ্ন

**Q1. তোমার কাজ কেন নতুন?**
A: আগের কাজগুলো একটা signal নিয়ে (একটা judge, বা test, বা security scan), আর বেশিরভাগ পুরনো model-এ। বর্তমান (2026) agent-এর patch-এ একাধিক আলাদা signal-এর ভুলের দিক মেপে, contamination-মুক্ত task-এ, পরিসংখ্যানসহ — এমন কাজ আমাদের fact sheet-এ পাওয়া যায়নি।

**Q2. একটা score না দিয়ে আলাদা signal কেন?**
A: Engineering Reliable Coding Agents দেখায় weighted একক score-কে optimizer ঠকাতে পারে; আর HITL ও RePaCA দেখায় judge-দের ভুলের দিক আলাদা — একসাথে মেশালে সেই তথ্য হারায়।

**Q3. Ground truth কীভাবে ঠিক করবে?**
A: Developer-এর পূর্ণ test suite, distinguishing input-এ আচরণ তুলনা, আর দুজন rater shared rubric দিয়ে (Cohen's κ report)। HITL paper দেখিয়েছে rubric ছাড়া মানুষের মিল খুব কম।

**Q4. খরচ সামলাবে কীভাবে?**
A: প্রথমে 5-task pilot, তারপর 60–100 task; সস্তা বর্তমান model আর প্রকাশিত patch ব্যবহার।

**Q5. যদি দেখা যায় কোনো signal কাজ করে না?**
A: সেটাও একটা গুরুত্বপূর্ণ ফল — "এই signal বর্তমান agent patch-এ নির্ভরযোগ্য নয়" — যা পরের গবেষকদের সময় বাঁচাবে।

---

## ১১. Supervisor-কে দেখানোর আগে যা যাচাই করতে হবে
1. Fact sheet-এ "search-snippet" চিহ্নিত তথ্য (যেমন OpenAI-এর SWE-bench Verified ঘোষণা, ComPass-এর 62.14%, SWE Atlas) মূল উৎসে খুলে দেখা।
2. কয়েকটা paper-এর প্রকাশস্থান অনিশ্চিত (UniTSyn, SecureVibeBench, Security & Quality, TestDecision, Trustworthy AI SE) — DBLP বা arXiv-এ দেখা।
3. SWE-rebench-এর সর্বশেষ window আর Scale-এর SWE-Bench Pro board-এ নতুন entry এসেছে কিনা দেখা — বর্তমান model-এর সংখ্যা দ্রুত বদলায়।
4. প্রস্তাবিত venue-গুলোর এ বছরের deadline দেখা।
