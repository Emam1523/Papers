# Sub-domain 5 Summary: Patch Validation

> **Paper:** 01 Human-in-the-Loop LLM-as-a-Judge (Google, AI-SQE '26) · 02 Code Representation in Deep-Learning APCA (arXiv 2026) · 03 Harden and Catch (Meta, position paper)
> **উদ্দেশ্য:** আমাদের assurance report-এর "static signal" (LLM judge, learned classifier) আর test-ভিত্তিক "catching" ধারণা কতটা নির্ভরযোগ্য, তা যাচাই; আগের gap ও direction আপডেট।

---

## ১. এক নজরে

| Paper | মূল প্রশ্ন | উত্তর |
|---|---|---|
| **HITL LLM-as-a-Judge** | মানুষ ও LLM কি একই মাপকাঠিতে patch-এর সঠিকতা বিচার করতে পারে? | নিজস্ব rubric-এ মানুষদের মিল কম (Fleiss κ 0.31); একই rubric দিলে বাড়ে (0.66)। Rubric-চালিত LLM judge: κ 0.57, recall 0.93, precision 0.65 |
| **Code Representation in APCA** | Patch-কে কোন রূপে (text, AST, graph) model-কে দিলে overfitting সবচেয়ে ভালো ধরা যায়? | Graph (GGNN + CPG) সেরা: accuracy 83.73%; heuristic ও sequence মিলিয়ে 85.95%; তিন-চারটা রূপ মেলালে আর উন্নতি হয় না |
| **Harden and Catch** | LLM-এর বানানো test কীভাবে "এই পরিবর্তনে bug আছে" তা সময়মতো ধরবে? | Hardening (ভবিষ্যৎ regression থেকে রক্ষা) আর catching (এখনকার পরিবর্তনের bug ধরা) আলাদা; 8 ধরনের test (5টা বিভ্রান্তিকর); মাপ হওয়া উচিত precision ≥ 0.8-এ সর্বোচ্চ recall (R@P=α), F1 নয় |

**মূল বার্তা:**
> "Patch-এর সঠিকতা বিচারে মানুষরাও একমত নয় যতক্ষণ না একটা স্পষ্ট rubric থাকে। LLM judge আর learned classifier দুটোই 80%-এর কাছাকাছি নির্ভুল, কিন্তু তাদের ভুলের দিক আলাদা — তাই একটা judge একা নয়, একাধিক আলাদা signal আর তাদের precision ও specificity আলাদা করে report করাই নিরাপদ।"

---

## ২. মূল সংখ্যা

| Paper | সংখ্যা | উৎস |
|---|---|---|
| HITL | নিজস্ব rubric-এ মানুষদের মিল κ 0.31; shared rubric-এ জোড়া-জোড়া 0.53–0.84, নতুন তিনজনের 0.66 | Table 1, 3 |
| HITL | Judge (115 patch): κ 0.57, precision 0.65, recall 0.93; শুধু "স্পষ্ট" 81 patch-এ κ 0.75, precision 0.80 | Table 6 |
| HITL | Rubric ছাড়া (free-form) κ 0.29; draft rubric 0.38; LLM-এর খসড়া rubric-এর 88% মানুষকে সংশোধন করতে হয়েছে | Table 6, §5.1 |
| HITL | F2P test pass করা 504 patch-এর 219টা (43.5%) judge-এর মতে INVALID; pass@20 96% থেকে 80%-এ নামে | §7, Fig. 3 |
| APCA Representation | সেরা প্রতিটা ধরন: TF-IDF 80.41%, Transformer 82.48%, TreeLSTM 82.94%, GGNN+CPG 83.73% (recall 87.09%) | Table 6 |
| APCA Representation | Heuristic + sequence fusion 85.95% | Table 7 |
| Harden and Catch | কোনো experiment নেই; 15টা definition, 8 ধরনের test, 4টা research challenge; R@P=0.8 মানে ভুল সতর্কতা : সঠিক ধরা ≤ 1:4 | §3, Fig. 1 |

---

## ৩. নতুন শিক্ষা (আমার বিশ্লেষণ)

1. **Judge-দের ভুলের দিক উল্টো।** HITL judge প্রায় সব ভুল patch ধরে না, বরং সঠিক patch-কে ঠিকমতো গ্রহণ করে (recall 0.93, specificity আমার হিসাবে প্রায় 0.69); RePaCA (Sub-domain 2) উল্টো — overfitting প্রায় সব ধরে কিন্তু অনেক সঠিক patch বাতিল করে। দুটো আলাদা dataset-এ মাপা, তাই এটা অনুমান — কিন্তু এটা "একাধিক আলাদা signal" ধারণাকে সমর্থন করে।
2. **Test pass করা patch-এর বড় অংশ সন্দেহজনক।** HITL-এ F2P pass করা patch-এর 43.5% judge-এর মতে ভুল — AutoCodeRover-এর 65.4% সঠিকতার (Sub-domain 1) সাথে মেলে।
3. **Rubric-ই আসল চাবি।** Rubric ছাড়া judge-এর κ 0.29, gold rubric-এ 0.57। Issue থেকে rubric বানানো আর তা যাচাই করা নিজেই একটা কঠিন কাজ।
4. **Label-এর উৎস নিয়ে সাবধান।** APCA dataset-এ সঠিক patch-এর 82.5% developer-এর লেখা (agent analysis-এর হিসাব) — model হয়তো "কে লিখেছে" শিখছে, "সঠিক কিনা" নয়। Random cross-validation এটা ধরতে পারে না।
5. **সঠিক মাপকাঠি দরকার।** Harden and Catch F1-এর বদলে "precision ≥ 0.8 রেখে সর্বোচ্চ recall" প্রস্তাব করে — developer ভুল সতর্কতায় বিরক্ত হয়ে tool ব্যবহার বন্ধ করে দেয়।

---

## ৪. Common Gap — Update

| CG | এই sub-domain-এর প্রমাণ | অবস্থা |
|---|---|---|
| CG1 plausible ≠ correct | F2P pass করা patch-এর 43.5% INVALID (HITL) | আরও শক্ত |
| CG3 / CG13 test ও oracle-এর মান | Harden and Catch: 8 ধরনের test-এর 5টা বিভ্রান্তিকর; oracle-ই মূল সমস্যা | আরও শক্ত |
| CG10 tool-এর নিজের validity | APCA-তে random CV, developer-patch confound; HITL-এ rubric লেখক আর rater একই মানুষ | শক্ত হলো |
| CG12 signal-কে ঠকানো | কোনো paper-ই judge-কে প্ররোচনা বা prompt injection দিয়ে পরীক্ষা করেনি | খোলা |
| **CG16 (নতুন)** | **Correctness label-এর validity** — label-এর উৎসজনিত বিভ্রান্তি, random split leakage, rubric-লেখক ও rater এক হওয়া, "স্পষ্ট" subset বাছাইয়ের bias | ⭐⭐⭐⭐ |
| **CG17 (নতুন)** | **Judge-দের ভুলের দিক ও প্রকৃত হারে precision** — specificity report না করা; বাস্তবে tool-generated patch-এর মাত্র ~15.6% সঠিক (APCA agent-এর হিসাব), অথচ test set প্রায় 50/50 | ⭐⭐⭐⭐⭐ |
| **CG18 (নতুন)** | **Judge-এর robustness** — patch-এর ভেতরে লুকানো প্ররোচনা বা prompt injection-এ judge ঠকে কিনা | ⭐⭐⭐⭐ |
| **CG19 (নতুন)** | **Agent-এর লেখা patch-এ "author oracle" নেই** — মানুষের patch-এ লেখকের উদ্দেশ্য জানা যায়, agent-এর ক্ষেত্রে নয়; issue/PR text থেকে oracle বের করা LLM-চক্রাকার হতে পারে | ⭐⭐⭐⭐ |

---

## ৫. Research Direction — Update

> ⚠️ প্রাথমিক মত; দুটো sub-domain বাকি (Security, Trustworthy AI for SE)।

| দিক | আগে | এখন |
|---|---|---|
| Static signal | একটা reasoning judge (RePaCA-ধরনের) | **দুটো আলাদা static signal**: rubric-চালিত LLM judge (HITL) + learned classifier (graph representation) — ভুলের দিক আলাদা বলে দুটো আলাদা report |
| Rubric | — | Issue থেকে rubric তৈরি + মানুষ দিয়ে ছোট অংশ যাচাই (HITL-এর মতো) |
| মাপকাঠি | Recall ও specificity | + **R@P=0.8** (Harden and Catch) আর বাস্তব হারে (prevalence-adjusted) precision |
| Evaluation split | Repository/temporal split | + label-উৎস নিয়ন্ত্রণ (developer বনাম tool patch আলাদা) |
| নতুন পরীক্ষা | — | Judge robustness test: patch-এর comment-এ প্ররোচনা ঢুকিয়ে রায় বদলায় কিনা (CG18) |

**পরিমার্জিত research প্রশ্ন:**
> "বর্তমান AI agent-এর test-pass করা patch-এ, rubric-চালিত LLM judge, learned classifier আর distinguishing test — এই তিনটা আলাদা signal-এর প্রতিটার ভুলের দিক কী, আর সেগুলো আলাদা রেখে report করলে কি precision ≥ 0.8-এ ভুল patch ধরার হার বাড়ে? Judge কি patch-এর ভেতরের প্ররোচনায় ঠকে?"

---

## ৬. Supervisor-এর সম্ভাব্য প্রশ্ন

**Q1. LLM judge কি patch যাচাইয়ে মানুষের বিকল্প?**
A: এখনো না। Rubric থাকলে κ 0.57 (মাঝারি), স্পষ্ট ক্ষেত্রে 0.75। আর judge-এর rubric নিজেও মানুষকে ঠিক করতে হয়েছে (88% ক্ষেত্রে)।

**Q2. কোন code representation ব্যবহার করবে?**
A: Graph (CPG) সেরা একক রূপ (83.73%), heuristic + sequence মিলিয়ে 85.95%। তবে সব পরীক্ষা Java Defects4J-এ; Python agent patch-এ যাচাই হয়নি (CG9)।

**Q3. F1 কেন যথেষ্ট নয়?**
A: Developer-এর কাছে ভুল সতর্কতার খরচ বেশি। Harden and Catch-এর প্রস্তাব: precision অন্তত 0.8 রেখে recall সর্বোচ্চ করা।

**Q4. 2026-এ এই ক্ষেত্রের অবস্থা কী?**
A: শিল্প rubric আর LLM-judge-ভিত্তিক grading-এর দিকে যাচ্ছে (FrontierCode), কিন্তু একটা গবেষণায় সাধারণ LLM judge overfitting ছাঁকতে মাত্র 62.14% পেয়েছে (search-snippet)। Opus 5.5 বা GPT-6-এর patch-এ judge যাচাইয়ের কোনো কাজ পাওয়া যায়নি — এটাই আমাদের সুযোগ।

---

## ৭. পরের ধাপ
**Sub-domain 6: Security of AI-Generated Code** (৫টা paper) — CG5 (security) আর CG18 (prompt injection)-এর জন্য।
