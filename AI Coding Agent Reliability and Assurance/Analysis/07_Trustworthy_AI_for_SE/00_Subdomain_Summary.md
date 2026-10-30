# Sub-domain 7 Summary: Trustworthy AI for Software Engineering

> **Paper:** 01 Trustworthy AI Software Engineers (vision, arXiv 2602.06310, 2026) · 02 Proof-Carrying Code Completions (vision, ASE 2024 Workshops) · 03 AI Assurance: A Comprehensive Testing Strategy (Thoughtworks, arXiv 2605.23459, 2026)
> **উদ্দেশ্য:** আমাদের assurance report-এর ধারণাগত কাঠামো (trust কী, কোন প্রমাণ যথেষ্ট) আর সবচেয়ে শক্ত signal (formal proof) বোঝা; শেষ gap আপডেট।

---

## ১. এক নজরে

| Paper | ধরন | মূল বক্তব্য |
|---|---|---|
| **Trustworthy AI SE** | Vision (5 পৃষ্ঠা, কোনো experiment নেই) | AI software engineer-কে বিশ্বাস করতে হলে একটা মাত্রা নয়, কয়েকটা মাত্রা লাগে; শুধু output নয়, process আর "সে কী জানে" (epistemic) স্তরেও যাচাই; code review-কে runtime monitoring হিসেবে দেখা; trust interface — ৬টা "New Idea" |
| **Proof-Carrying Completions** | Vision + একটা case study | LLM-এর code-এর সাথে Dafny-তে যাচাইযোগ্য proof থাকবে; GPT-4 দিয়ে একটা file-system task প্রথম চেষ্টাতেই verify হয়েছে (সর্বোচ্চ 5 চেষ্টা, প্রতি query গড়ে 0.109 USD) |
| **AI Assurance** | Industry strategy (কোনো measured ফল নেই) | 5 স্তরের testing pyramid, 15টা failure mode; একই prompt 10 বার চালিয়ে pass rate 0.5-এর নিচে "স্থায়ী ব্যর্থতা", 0.9-এর নিচে "অস্থির"; quality gate (যেমন faithfulness 0.90) আর 7 দিনে 5% পতনে drift সতর্কতা |

**মূল বার্তা:**
> "Trust একটা সংখ্যা নয়, প্রমাণের সমষ্টি — আর প্রতিটা প্রমাণের নিজের সীমা আছে। Proof সবচেয়ে শক্ত signal, কিন্তু spec দুর্বল হলে proof অর্থহীন; industry-র assurance কাঠামো বাস্তবসম্মত, কিন্তু তাদের threshold-গুলো পরিসংখ্যানগতভাবে যাচাই করা নয়।"

---

## ২. নতুন শিক্ষা (আমার বিশ্লেষণ)

1. **আমাদের "আলাদা signal" ধারণার তাত্ত্বিক ভিত্তি পাওয়া গেল।** Trustworthy AI SE paper-এর বহুমাত্রিক trust কাঠামো Engineering Reliable Coding Agents monograph-এর "একক score নয়" যুক্তির সাথে মেলে। Assurance report-এর প্রতিটা signal একটা trust মাত্রার প্রমাণ।
2. **Process-ও যাচাই করতে হবে, শুধু output নয়।** সঠিক patch ভুল বা প্রতারণামূলক পথে (যেমন .git থেকে উত্তর পড়ে) আসতে পারে — SWE-Bench Pro Verified-এর GLM-5.2 উদাহরণ (78.80% থেকে 57.32%) ঠিক এটাই। তাই agent-এর trajectory দেখাও assurance-এর অংশ।
3. **Proof সবচেয়ে শক্ত, কিন্তু spec-ই আসল প্রশ্ন।** Proof-Carrying Completions দেখায় proof সম্ভব, কিন্তু মাত্র একটা task-এ (n = 1), আর spec মানুষ লিখেছে। Agent-এর patch-এর ক্ষেত্রে spec কে লিখবে, আর দুর্বল বা ফাঁকা spec কীভাবে ধরা যাবে — এটা খোলা। "Proof পাওয়া যায়নি" মানে code ভুল নয়; তাই তিন-অবস্থার ফল দরকার (verified / failed / প্রযোজ্য নয়)।
4. **Threshold-গুলোও যাচাই করতে হবে।** AI Assurance-এর "10 বারে 9 pass" নিয়ম — analysis-এর হিসাবে 9/10-এর 95% interval প্রায় 0.60–0.98, আর 8/10-এর প্রায় 0.49–0.94; সীমানা দুটো একে অপরের সাথে মিশে যায়। Industry threshold পরিসংখ্যান ছাড়া বসানো।
5. **Repeated-run নিয়ম আমাদের কাজে লাগবে।** AI Assurance-এর "consistent failure / flaky" ভাগ আমাদের CG4 (run-to-run variance)-এর একটা সরল, ব্যবহারযোগ্য রূপ — তবে confidence interval যোগ করে।

---

## ৩. Common Gap — শেষ আপডেট

| CG | এই sub-domain-এর প্রমাণ | অবস্থা |
|---|---|---|
| CG4 variance | AI Assurance-এর repeated-run নিয়ম আছে, কিন্তু CI নেই | আংশিক পদ্ধতি পাওয়া গেছে |
| CG11 verifier health | Proof-এর trusted base (verifier, solver version, interface) যাচাই করা হয়নি | শক্ত হলো |
| CG12 / CG18 gaming | Trust-এর প্রমাণও ঠকানো যায় (Trustworthy AI SE-এর নিজের সতর্কতা) | শক্ত হলো |
| CG22 tri-state verdict | Proof-এর ক্ষেত্রেও "যাচাই করা যায়নি" আলাদা দরকার | শক্ত হলো |
| **CG23 (নতুন)** | **Specification-এর পর্যাপ্ততা** — agent-এর patch-এর spec কে লিখবে, spec দুর্বল বা ফাঁকা কিনা কীভাবে মাপা যাবে | ⭐⭐⭐⭐ |
| **CG24 (নতুন)** | **Trajectory-স্তরের assurance** — সঠিক patch ভুল বা প্রতারণামূলক পথে এসেছে কিনা (leakage, test বদলানো) | ⭐⭐⭐⭐⭐ |
| **CG25 (নতুন)** | **প্রতিটা trust মাত্রার পরিমাপযোগ্য metric ও যাচাই করা threshold** — review-এর সীমিত সময়ে কোন প্রমাণ সবচেয়ে মূল্যবান | ⭐⭐⭐⭐ |

---

## ৪. Research Direction — চূড়ান্ত রূপের আগে

এই sub-domain direction বদলায়নি, বরং কাঠামো দিয়েছে:
- **Assurance report-এর প্রতিটা signal = একটা trust মাত্রার প্রমাণ**, আলাদা দেখানো, প্রত্যেকটার uncertainty ও version সহ।
- **নতুন signal:** trajectory check (leakage ও test বদলানো ধরা) — CG24।
- **ঐচ্ছিক উচ্চ-স্তরের signal:** যেখানে spec আছে বা বানানো যায়, সেখানে formal proof (Dafny-ধরনের); না পারলে "প্রযোজ্য নয়"।
- **Repeated-run নিয়ম:** AI Assurance-এর flaky/consistent-failure ভাগ, তবে confidence interval সহ।

চূড়ান্ত research প্রশ্ন আর পরিকল্পনা **Final Synthesis**-এ ঠিক করা হবে।

---

## ৫. Supervisor-এর সম্ভাব্য প্রশ্ন

**Q1. "Trustworthy" বলতে তুমি কী বোঝো?**
A: একক accuracy নয়; output সঠিক কিনা, process সৎ কিনা, আর agent নিজের অনিশ্চয়তা জানে কিনা — এই কয়েকটা মাত্রার প্রমাণ। আমাদের assurance report প্রতিটা মাত্রার জন্য আলাদা signal দেয়।

**Q2. Formal proof থাকলে test কি দরকার নেই?**
A: Proof শুধু spec-এর সাথে মিল প্রমাণ করে। Spec ভুল বা দুর্বল হলে proof-ও কিছু বলে না, আর বেশিরভাগ agent patch-এর spec নেই। তাই proof একটা অতিরিক্ত শক্ত signal, বিকল্প নয়।

**Q3. Industry assurance কাঠামো থেকে কী নেবে?**
A: Repeated-run নিয়ম, quality gate আর drift monitoring-এর ধারণা — তবে তাদের threshold-গুলো পরিসংখ্যানগতভাবে যাচাই করা নয়, তাই আমরা confidence interval আর paired test যোগ করবো।

---

## ৬. পরের ধাপ
**Final Synthesis** — সাতটা sub-domain মিলিয়ে: সব gap (CG1–CG25) একত্রে সাজানো, সবচেয়ে মূল্যবান ও SPL3-তে করা সম্ভব gap বাছাই, চূড়ান্ত research প্রশ্ন, SPL3 software-এর পরিকল্পনা, আর publication পরিকল্পনা।
