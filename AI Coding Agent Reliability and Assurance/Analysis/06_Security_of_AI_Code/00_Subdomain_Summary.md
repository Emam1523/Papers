# Sub-domain 6 Summary: Security of AI-Generated Code

> **Paper:** 01 CWEval · 02 Security & Quality in LLM Code (arXiv 2026) · 03 Automated Correctness Assessment for Security (JSS 2024) · 04 Enhancing Reliability in Secure Code Generation (arXiv 2026) · 05 SecureVibeBench (arXiv 2026)
> **উদ্দেশ্য:** Assurance report-এর security signal কীভাবে মাপা উচিত, আর AI agent-এর patch কতটা নিরাপদ — তা বোঝা; gap ও direction আপডেট।

---

## ১. এক নজরে

| Paper | মূল প্রশ্ন | উত্তর |
|---|---|---|
| **CWEval** | Code কাজ করে আর নিরাপদ — দুটো একসাথে কীভাবে মাপবো? | Execution দিয়ে দুটোই যাচাই (func-sec@k); GPT-4o-তে func@1 80.81% কিন্তু func-sec@1 মাত্র 50.21% |
| **Security & Quality** | Language আর model-ভেদে vulnerability ও code quality কেমন? | 4,000 program-এ 284টা security finding; C সবচেয়ে খারাপ (122টা, যার 66টা buffer overflow-জাতীয় CWE-120); সবচেয়ে সঠিক model সবসময় সবচেয়ে নিরাপদ নয় |
| **Automated Correctness (JSS)** | Security code (assembly exploit) সঠিক কিনা স্বয়ংক্রিয়ভাবে বলা যায়? | Symbolic execution-ভিত্তিক ACCA মানুষের রায়ের সাথে correlation 0.84 (BLEU 0.56); তবে reference-এর মতো না হলে সঠিক code-কেও ভুল বলে |
| **Enhancing Reliability** | Prompt-এ নিরাপত্তার জ্ঞান ঢোকালে কি কম vulnerability হয়? | হ্যাঁ — SonarQube finding 92 থেকে 39 (57.6%), LLMSecEval-এ 73 থেকে 4; তবে মাপা হয়েছে একটাই scanner দিয়ে, একবার চালিয়ে |
| **SecureVibeBench** | Coding agent (Claude Code, Codex, SWE-agent…) repository-level কাজে কতটা নিরাপদ code লেখে? | সেরা মাত্র 23.8% correct-and-secure; Claude Code 48.6% সঠিক কিন্তু 17.1% সঠিক ও নিরাপদ; Semgrep-এর সতর্কতার প্রায় অর্ধেক ভুল |

**মূল বার্তা:**
> "Functional correctness আর security আলাদা জিনিস — সঠিক code-এর অর্ধেকের মতো নিরাপদ নয়, agent-দের ক্ষেত্রেও। আর security মাপার যন্ত্রগুলো (static scanner) নিজেই অনির্ভরযোগ্য: প্রায় অর্ধেক ভুল সতর্কতা, আর অনেক আসল দুর্বলতা ধরে না। তাই security signal-কে execution-ভিত্তিক করতে হবে, আর তার নিজের নির্ভরযোগ্যতাও report করতে হবে।"

---

## ২. মূল সংখ্যা

| Paper | সংখ্যা | উৎস |
|---|---|---|
| CWEval | 119 task, 31 CWE, 5 language; func@10 থেকে func-sec@10-এ সব model প্রায় 30 pp পড়ে; GPT-4o func@10 90.71 বনাম func-sec@10 65.33 | Table I, Fig. 3 |
| CWEval | পুরনো benchmark-এর 1,916টা vulnerable sample-এর মাত্র 562টা static analyzer আবার ধরে | §II |
| Security & Quality | Finding: Java 69, Python 40, C++ 53, C 122; Java ও Python-এ সবচেয়ে বেশি CWE-780 (OAEP ছাড়া RSA) | Table 11, 12 |
| JSS (ACCA) | মানুষের সাথে মিলের হার গড়ে 0.93; Pearson 0.84; প্রতি snippet 0.20 সেকেন্ড বনাম মানুষের প্রায় 20 সেকেন্ড | Table 3, 6, 7 |
| Enhancing Reliability | 7,200 program; finding 92 থেকে 39; zero-shot ও CoT prompt উল্টো বাড়িয়েছে (100, 98) | Table III, VI |
| SecureVibeBench | 4,993 vulnerability commit থেকে 105 task; 15 agent-model জোড়ার গড় correct-and-secure 11.62%; সেরা 23.8% (SWE-agent + Claude Sonnet 4.5) | Table 3, Fig. 4 |
| SecureVibeBench | হাতে যাচাই করা 120টা Semgrep সতর্কতার 49.6% আসলে নিরাপদ | §5 |

---

## ৩. নতুন শিক্ষা (আমার বিশ্লেষণ)

1. **"সঠিক" patch-এর বড় অংশ অনিরাপদ।** SecureVibeBench-এ সঠিক patch-এর প্রায় 49–57% নিরাপদ নয় (agent analysis-এর হিসাব); CWEval-এ function-স্তরেও একই চিত্র। CG1 (plausible ≠ correct)-এর পাশাপাশি এখন "correct ≠ secure"।
2. **Static scanner একা বিশ্বাসযোগ্য নয়।** Semgrep-এর প্রায় অর্ধেক সতর্কতা ভুল; পুরনো dataset-এর বেশিরভাগ vulnerability CodeQL আর ধরে না। তাই security signal-এর মূল ভিত্তি হওয়া উচিত execution (CWEval-এর মতো exploit/PoV test), scanner হবে সহায়ক।
3. **Scanner-কে খুশি করা ≠ নিরাপদ।** "Enhancing Reliability"-এর prompt checklist সেই একই SonarQube rule-এর সাথে মিল রেখে বানানো — finding কমা হয়তো আংশিকভাবে scanner-কে "শেখানো" (CG12-এর security রূপ)।
4. **Reference-এর সাথে মিলিয়ে বিচারও বিপজ্জনক।** ACCA reference-এর মতো না হলে সঠিক code-কেও বাতিল করে; SecureVibeBench-এ functional test gold patch-এর আচরণে বাঁধা, অথচ সেই commit-ই vulnerability এনেছিল।
5. **কোনো paper-ই variance মাপেনি।** সবাই একবার চালিয়েছে (SecureVibeBench temperature 0, Enhancing Reliability এক sample)। 105 task-এ 2–7 task-এর পার্থক্য পরিসংখ্যানগতভাবে দুর্বল।

---

## ৪. Common Gap — Update

| CG | এই sub-domain-এর প্রমাণ | অবস্থা |
|---|---|---|
| CG5 security | Agent-স্তরে সেরা 23.8% correct-and-secure; 2026-এ SusVibes-এ SecPass 7.8–17.3% (context.md) | **খোলা, আরও শক্ত প্রমাণ** |
| CG4 variance | পাঁচটা paper-এর কোনোটাই একাধিক run বা CI দেয়নি | খোলা |
| CG9 language | C-তে finding অনেক বেশি; একই model language-ভেদে আলাদা | শক্ত হলো |
| CG12 gaming | Scanner-এর rule-এর সাথে মিল রেখে prompt | নতুন দিক |
| **CG20 (নতুন)** | **একসাথে functional ও security রায়** — শুধু সঠিক patch-এর জন্য নয়, প্রতিটা patch-এর জন্য execution-ভিত্তিক "কাজ করে ও নিরাপদ" verdict, patch-এর আগে-পরের পার্থক্যসহ | ⭐⭐⭐⭐⭐ |
| **CG21 (নতুন)** | **Security signal-এর নিজের নির্ভরযোগ্যতা** — scanner-এর precision/recall, একাধিক scanner-এর মিল, finding-কে KLoC বা patch-অনুযায়ী normalise করা | ⭐⭐⭐⭐⭐ |
| **CG22 (নতুন)** | **Reference-বাঁধা oracle** — gold বা reference-এর সাথে মিল দিয়ে বিচার সঠিক বিকল্প বাতিল করে, আর gold নিজেই ভুল বা অনিরাপদ হতে পারে; তিন-অবস্থার ফল (সমতুল্য / ভিন্ন / যাচাই করা যায়নি) দরকার | ⭐⭐⭐⭐ |

---

## ৫. Research Direction — Update

> ⚠️ প্রাথমিক মত; একটা sub-domain বাকি (Trustworthy AI for SE)।

| Security signal | আগে | এখন |
|---|---|---|
| পদ্ধতি | Bandit/Semgrep scan | **Execution-ভিত্তিক** security test (CWEval/PoV-ধরনের) মূল; scanner সহায়ক, আর patch-এর আগে-পরে **নতুন** finding-ই গণ্য |
| Report | একটা security flag | Functional ও security আলাদা কিন্তু একসাথে (2×2: correct-secure, correct-vulnerable, incorrect…), প্রতিটা scanner-এর জানা false alarm হার সহ |
| নির্ভরযোগ্যতা | — | একাধিক run আর একাধিক scanner-এর মিল; "যাচাই করা যায়নি" আলাদা |

**পরিমার্জিত research প্রশ্ন (আমার মত):**
> "বর্তমান AI agent-এর test-pass করা patch-এ, আলাদা আলাদা signal — rubric-চালিত judge, distinguishing test, আর execution-ভিত্তিক security test — দিয়ে কতগুলো 'ভুল' আর কতগুলো 'অনিরাপদ' patch ধরা যায়, আর প্রতিটা signal-এর নিজের ভুলের হার কত?"

---

## ৬. Supervisor-এর সম্ভাব্য প্রশ্ন

**Q1. Agent-এর code কতটা নিরাপদ?**
A: SecureVibeBench-এ সেরা agent-ও মাত্র 23.8% ক্ষেত্রে সঠিক ও নিরাপদ code দিয়েছে; Claude Code 48.6% সঠিক কিন্তু 17.1% সঠিক ও নিরাপদ। 2026-এর SusVibes-এ secure pass 7.8–17.3%।

**Q2. Static analyzer দিয়ে কেন যথেষ্ট নয়?**
A: Semgrep-এর হাতে-যাচাই করা সতর্কতার 49.6% আসলে নিরাপদ ছিল; আর CWEval দেখায় পুরনো vulnerable sample-এর মাত্র 562/1,916 analyzer ধরে। Scanner ভুলও বলে, অনেক কিছু মিসও করে।

**Q3. Prompt দিয়ে নিরাপত্তা বাড়ানো যায়?**
A: কিছুটা — Enhancing Reliability-তে finding 57.6% কমেছে, CWEval-এ security instruction সর্বোচ্চ +9.80 pp দিয়েছে। কিন্তু সাধারণ CoT উল্টো finding বাড়িয়েছে, আর মাপকাঠি একটাই scanner হওয়ায় ফল আংশিক।

**Q4. বর্তমান model-এর অবস্থা?**
A: Opus 5.5, GPT-6 বা Gemini 4-এর SecureVibeBench, SusVibes বা BaxBench ফল পাওয়া যায়নি; শুধু Opus 5.5-এর prompt injection সফলতা (safeguard ছাড়া 54.61%, কোম্পানির দাবি) জানা — এটা একটা খালি জায়গা।

---

## ৭. পরের ধাপ
**Sub-domain 7: Trustworthy AI for SE** (৩টা paper), তারপর **Final Synthesis** — সব sub-domain মিলিয়ে চূড়ান্ত gap ও research direction।
