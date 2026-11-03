# Paper Analysis 02 (Eval): SWE-Bench Pro — Can AI Agents Solve Long-Horizon Software Engineering Tasks?

> **Sub-domain:** Coding-Agent Evaluation & Reliability
> **Analysis করেছে:** SPL3 — AI Coding Agent Reliability and Assurance
> **Paper file:** `Coding-Agent Evaluation & Reliability/Can AI Agents Solve Long-Horizon Software Engineering Tasks.pdf`
> **পড়ার নিয়ম:** "Authors বলেছেন" অংশ সরাসরি paper থেকে নেওয়া। যেখানে নিজের হিসাব বা মত আছে, সেখানে **"আমার পর্যবেক্ষণ"** বা **"আমার হিসাব"** লেখা আছে। Figure থেকে চোখে পড়ে নেওয়া সংখ্যার পাশে **"আনুমানিক"** লেখা আছে (paper-এ ঐ সংখ্যাগুলো লেখা নেই, শুধু bar chart আছে)।

---

## ০. Paper-এর পরিচয় (Bibliographic Info)

| বিষয় | তথ্য |
|---|---|
| **Title** | SWE-Bench Pro: Can AI Agents Solve Long-Horizon Software Engineering Tasks? |
| **Authors** | Xiang Deng∗, Jeff Da∗ (∗ co-first author, equal contribution), Edwin Pan, Yannis Yiming He, Charles Ide, Kanak Garg, Niklas Lauffer, Andrew Park, Nitin Pasari, Chetan Rane, Karmini Sampath, Maya Krishnan, Srivatsa Kundurthy, Sean Hendryx, Zifan Wang, Vijay Bharadwaj, Jeff Holm, Raja Aluri, Chen Bo Calvin Zhang, Noah Jacobson, Bing Liu, Brad Kenstler |
| **Institution** | Scale AI (contact: jeffrey.da@scale.com) |
| **Venue** | **arXiv preprint** — arXiv:2509.16941**v2** [cs.SE], 14 November 2025। Paper-এর ভেতরে কোনো peer-reviewed conference/journal-এর নাম নেই। (arXiv ID "2509" মানে প্রথম version September 2025-এ জমা পড়েছিল।) |
| **Paper type** | **Benchmark / Dataset paper + empirical evaluation** (নতুন agent নয়, নতুন ও কঠিন "পরীক্ষার খাতা" + failure analysis) |
| **Artifacts** | Public set (731 task) — HuggingFace: `ScaleAI/SWE-bench_Pro`; Code: `github.com/scaleapi/SWE-bench_Pro-os`; pre-built Docker image (paper বলছে release করা হবে); leaderboard (commercial set-এর ফল সেখানে update হবে) |
| **আমাদের domain-এ গুরুত্ব** | ⭐⭐⭐⭐⭐ — Sub-domain 1-এর CG6 (benchmark quality ও contamination) আর Agentless-এর "underspecified issue" সমস্যার সরাসরি উত্তর দেওয়ার চেষ্টা; multi-language (Python, Go, JS, TS) হওয়ায় CG9-এর জন্যও গুরুত্বপূর্ণ test bed। |

---

## ★ সহজ ভাষায় পুরো Paper (প্রথমবার পড়ার জন্য)

### ক. Paper-টা কী নিয়ে?

- এটা একটা **benchmark paper**। Benchmark মানে AI-কে পরীক্ষা করার একটা "প্রশ্নপত্র"। এখানে নতুন কোনো AI agent বানানো হয়নি।
- বানিয়েছে **Scale AI** কোম্পানির একদল researcher। Paper-এর নাম SWE-Bench Pro।
- প্রশ্নপত্রটায় আছে 1,865টা software-এর কাজ (bug ঠিক করা, নতুন feature যোগ করা)। কাজগুলো এসেছে 41টা আসল project থেকে।
- আগের পরীক্ষাগুলো ছিল বেশি সহজ আর অনেক AI সেগুলোর উত্তর হয়তো আগেই দেখে ফেলেছিল। এই paper একটা বেশি কঠিন আর বেশি "ন্যায্য" পরীক্ষা বানিয়েছে।
- তারপর সেরা AI agent-দের এই পরীক্ষায় বসিয়ে দেখেছে তারা কতটা পারে আর কোথায় আটকে যায়।
- এটা arXiv-এ প্রকাশিত preprint (peer review হওয়া conference paper নয়)।

### খ. সমস্যাটা কী ছিল?

ধরো স্কুলে একটা পরীক্ষা বহু বছর ধরে একই প্রশ্নে হচ্ছে। প্রশ্ন ফাঁস হয়ে গেছে, আর অর্ধেক প্রশ্ন একদম সহজ। তখন সবাই 90 পায়, কিন্তু কে আসলে ভালো তা বোঝা যায় না। AI agent-দের বেলায় ঠিক এটাই হচ্ছিল।

- আগের benchmark SWE-bench Verified-এ সেরা AI-রা 70%-এর বেশি পাচ্ছিল। তাই নতুন AI-দের মধ্যে পার্থক্য ধরা কঠিন হয়ে গিয়েছিল।
- Verified-এর 500টা task-এর মধ্যে 161টাতে মাত্র 1-2 line বদলাতে হয়। আসল কোম্পানির কাজে প্রায়ই শত শত line আর কয়েকটা file বদলাতে হয়।
- Project-গুলো MIT বা Apache-এর মতো খোলা license-এর। তাই এগুলো AI-র training data-তে ঢুকে থাকার সম্ভাবনা বেশি। মানে AI আগেই উত্তর "দেখে" এসে থাকতে পারে।
- অনেক task-এর বর্ণনা অসম্পূর্ণ। যেমন একটা commit-এ শুধু লেখা "enable vCard v4.0 contact import" আর কোনো বিবরণ নেই। AI-র কী করতে হবে সেটাই বোঝা যায় না।
- Test অনেক সময় একটা নির্দিষ্ট function-এর নাম আশা করে। AI অন্য নামে ঠিক কাজ করলেও test ভুল ধরে নেয়।

### গ. Paper কী solve করেছে?

- **নতুন ও কঠিন benchmark:** 41টা repository, 1,865টা task। প্রতিটা task-এ গড়ে 107.4 line আর 4.1টা file বদলাতে হয়।
- **Contamination কমানোর চেষ্টা:** GPL license-এর public repo আর startup-দের কাছ থেকে কিনে আনা private repo ব্যবহার করা হয়েছে। (Contamination মানে AI আগে থেকেই উত্তর দেখে ফেলা।)
- **মানুষ দিয়ে task পরিষ্কার করা:** প্রতিটা task-এর বর্ণনা নতুন করে লেখা হয়েছে, requirements আর interface (function-এর নাম) যোগ হয়েছে, আর test হাতে যাচাই হয়েছে।
- **নতুন হিসাব:** সেরা AI-রাও এই পরীক্ষায় অনেক কম পেয়েছে। কেন ব্যর্থ হয় তার ধরনও ভাগ করে দেখানো হয়েছে।

সবচেয়ে গুরুত্বপূর্ণ তিনটা সংখ্যা:

- **43.6%** (public set-এ সেরা Claude Sonnet 4.5): মানে 100টা task-এর মধ্যে প্রায় 44টা solve হয়েছে, বাকি 56টা হয়নি।
- **17.8%** (commercial set-এ সেরা Claude Opus 4.1): মানে startup-এর আসল private code-এ 100টার মধ্যে মাত্র প্রায় 18টা solve হয়েছে।
- **25.9% থেকে 8.4%** (GPT-5, requirements আর interface সরিয়ে নিলে): মানে স্পষ্ট নির্দেশ না দিলে 100টার মধ্যে 26টার জায়গায় মাত্র প্রায় 8টা solve হয়।

### ঘ. কীভাবে solve করেছে?

1. **Repository বাছাই:** যেসব project এখনো সক্রিয়ভাবে চলছে, ব্যবহারকারী অনেক, documentation ভালো, সেগুলো নেওয়া হয়েছে। এক repo থেকে সর্বোচ্চ 100টা task, যাতে একটা repo-র উপর সব score নির্ভর না করে।
2. **Task বানানো:** repo-র history থেকে পরপর দুটো commit-এর জোড়া নেওয়া হয়েছে। এর মধ্যে test-এর অংশটা আলাদা করা হয়েছে (test patch), বাকিটা সঠিক উত্তর (gold patch)।
3. **সহজ task বাদ:** যেসব task-এ 10 line-এর কম বদলাতে হয়, সেগুলো ফেলে দেওয়া হয়েছে।
4. **বর্ণনা নতুন করে লেখা:** মানুষ একটা পরিষ্কার problem statement লিখেছে। সাথে requirements (কী behaviour চাই) আর interface (কোন function বা class-এর কী নাম) যোগ করেছে।
5. **পরীক্ষার ঘর বানানো:** প্রতিটা project-এর জন্য Docker environment বানানো হয়েছে। (Docker হলো একটা সিল করা বাক্স, যেখানে সব software একসাথে থাকে, তাই যেকোনো কম্পিউটারে একই ফল আসে।)
6. **Test যাচাই:** সঠিক উত্তর দিয়ে test কয়েকবার চালানো হয়েছে। কখনো fail করলে সেই task বাদ। তারপর মানুষ দেখেছে test-টা task-এর সাথে মেলে কিনা।
7. **AI চালানো:** সব model-কে একই কাঠামোতে (SWE-agent) একই prompt দিয়ে চালানো হয়েছে। সর্বোচ্চ 50 ধাপ, প্রতি task-এ 2 USD খরচের সীমা।
8. **ব্যর্থতা ভাগ করা:** ব্যর্থ হওয়া agent-দের কাজের লগ GPT-5-কে পড়িয়ে বলতে বলা হয়েছে, কেন ব্যর্থ হলো (ভুল উত্তর, tool ভুল ব্যবহার, loop-এ আটকে যাওয়া ইত্যাদি)।

### ঙ. এরপর কী করা যায়?

- **Authors যা বলেছেন:** শুধু test pass করলেই patch ঠিক, এই ধারণার বাইরে যেতে হবে। Code quality, security, performance আর readability-ও মাপতে হবে।
- **Authors আরও বলেছেন:** Java, C++, Rust-এর মতো language যোগ করা দরকার। আর একাধিক agent বা মানুষ-agent একসাথে কাজ করার ক্ষেত্রও দেখা দরকার।
- **এখনো খোলা:** Contamination সত্যিই কমেছে কিনা, তার কোনো পরীক্ষা paper-এ নেই। Held-out set-এর ফলও দেওয়া হয়নি।
- **এখনো খোলা:** একই task একাধিকবার চালালে ফল কতটা বদলায় (reliability), সেটা কেউ মাপেনি।
- **আমরা SPL3-তে করতে পারি:** SWE-Bench Pro-র ছোট একটা subset-এ আমাদের patch-correctness যাচাইয়ের tool চালিয়ে দেখা। Python থেকে Go, JS, TS-এ সেটা কতটা কাজ করে, তা মাপা।
- **আমরা আরও করতে পারি:** Test পাস করা patch-গুলোর মধ্যে কতগুলো আসলে ভুল, সেটা বের করা (false positive)। আর agent-এর কাজের লগ দেখে "এই patch-এ ভরসা কম" বলার একটা signal বানানো।

> **মনে রাখো:**
> SWE-Bench Pro হলো বেশি কঠিন, বেশি বড় task-এর একটা AI পরীক্ষা। সেরা AI-ও এখানে 100টার মধ্যে 44টার বেশি পারেনি (paper-এর সময়ে)।
> Spec স্পষ্ট না থাকলে score প্রায় তিন ভাগের এক ভাগে নেমে যায়, আর test নিজেও ভুল করতে পারে। তাই score দেখে সরাসরি ভরসা করা যায় না। এখানেই আমাদের assurance কাজের জায়গা।

---

## ১. এক লাইনে Paper (TL;DR)

**SWE-Bench Pro হলো 41টা repository থেকে নেওয়া 1,865টা কঠিন, বড় (গড়ে 107.4 line, 4.1 file), মানুষ দিয়ে যাচাই ও বিস্তারিত করা software engineering task-এর benchmark — যেটা contamination কমাতে GPL-licensed public repo আর কিনে আনা private startup repo ব্যবহার করে; SWE-agent scaffold-এ সেরা model public set-এ 43.6% আর commercial set-এ 20%-এর কম solve করে।**

**সহজ কথায়:** Scale AI একটা কঠিন পরীক্ষা বানিয়েছে। সেখানে সেরা AI মাত্র 44% task পারে। আসল startup-এর private code-এ পারে 20%-এরও কম। আর নির্দেশ কমিয়ে দিলে ফল আরও খারাপ হয়।

### Supervisor-কে ৩০ সেকেন্ডে কীভাবে বলবো
> "Sir, Sub-domain 1-এ আমরা দেখেছি SWE-bench এখন অনেকটা 'saturated' — Verified-এ score অনেক উঁচু, আর অনেক task মাত্র 1–2 line-এর পরিবর্তন (Verified-এর 500-এর মধ্যে 161টা)। তাছাড়া repository-গুলো MIT/BSD-এর মতো permissive license-এর, তাই model-এর training data-তে ঢুকে থাকার সম্ভাবনা বেশি। Scale AI-এর SWE-Bench Pro তিনটা কাজ করেছে: (১) শুধু GPL-এর মতো copyleft license-এর repo আর startup থেকে কেনা private repo নিয়েছে, যাতে contamination কম হয়; (২) 10 line-এর কম পরিবর্তনের task বাদ দিয়েছে — গড় patch 107.4 line, 4.1 file; (৩) প্রতিটা task-এ মানুষ দিয়ে issue আবার লিখিয়েছে, requirements আর interface (function/class-এর নাম) যোগ করেছে, আর test হাতে যাচাই করেছে। 1,865 task তিন ভাগে: public 731, commercial 276, held-out 858। SWE-agent দিয়ে public set-এ সেরা Claude Sonnet 4.5 পেয়েছে 43.6%, commercial set-এ সেরা model 20%-এর নিচে। Requirements/interface সরিয়ে দিলে GPT-5-এর score 25.9% থেকে 8.4%-এ নামে — অর্থাৎ test-based verifier-এর false negative বড় সমস্যা। আমাদের assurance research-এর জন্য এটা গুরুত্বপূর্ণ কারণ এটা multi-language, বড় patch-এর একটা পরিষ্কার test bed দেয়, কিন্তু patch correctness (CG1), variance (CG4) আর security (CG5) এখনো খোলা রেখে দেয়।"

---

## ২. Background — এই paper বুঝতে যা আগে জানা দরকার

SWE-bench, Issue/PR, Patch, F2P/P2P test, Resolved metric, Contamination, Benchmark saturation, Pass@k — এগুলো **Sub-domain 1, Paper 01 (SWE-bench) দেখো**। Agent scaffold, ACI, trajectory, LLM-as-judge-এর প্রাথমিক ধারণা — **Sub-domain 1, Paper 02 (SWE-agent) দেখো**। Agentless pipeline ও SWE-bench Lite-S — **Sub-domain 1, Paper 04 দেখো**। Data leakage-এর সাধারণ আলোচনা — **Sub-domain 2, Paper 01 (APR Survey) দেখো**। এখানে শুধু এই paper-এর **নতুন** concept ব্যাখ্যা করা হলো।

### ২.১ Long-Horizon Task
- **Horizon** মানে একটা কাজ শেষ করতে কত দীর্ঘ ধাপের পরিকল্পনা লাগে। Short-horizon task: একটা function-এ একটা condition ঠিক করা (কয়েক মিনিটের কাজ)। Long-horizon task: নতুন feature যোগ করা, যেখানে কয়েকটা file-এ class/function বানাতে হয়, পুরনো code-এর সাথে মেলাতে হয়, test চালিয়ে দেখতে হয়।
- Authors-এর ভাষায় SWE-Bench Pro-এর task এমন যে একজন professional software engineer-এর **কয়েক ঘণ্টা থেকে কয়েক দিন** লাগতে পারে।
- Agent-এর জন্য এর মানে: অনেক বেশি turn, অনেক বেশি context, ভুল জমতে থাকা (error compounding) — একটা ভুল early step পরের সব step নষ্ট করতে পারে।
- **আমার পর্যবেক্ষণ:** "ঘণ্টা থেকে দিন" দাবিটার পেছনে paper কোনো মানুষের সময় মাপা data দেয়নি; এটা patch size (lines, files) দিয়ে পরোক্ষভাবে বোঝানো হয়েছে।

### ২.২ Software License: Permissive বনাম Copyleft (GPL)
| ধরন | উদাহরণ | মূল শর্ত | Benchmark-এর জন্য তাৎপর্য |
|---|---|---|---|
| **Permissive** | MIT, Apache 2.0, BSD | প্রায় যেকোনো কাজে ব্যবহার করা যায়, শুধু credit দিতে হয় | Web-crawl করা training corpus-এ সহজে ঢোকে (paper বলছে এরা "prime candidates") |
| **Copyleft (strong)** | GPL | এই code থেকে derived কিছু বিতরণ করলে সেটাকেও একই license-এ open করতে হয় ("share-alike") | Authors-এর যুক্তি: এই শর্ত commercial (proprietary) model-এর training corpus-এ ঢোকানোর পথে **আইনি বাধা** তৈরি করে |

**সহজ কথায়:** Permissive license মানে "যা খুশি করো", তাই এই code AI-র training data-তে সহজে ঢোকে। GPL মানে "ব্যবহার করলে তোমার কাজও খোলা রাখতে হবে"। Authors ভেবেছেন, এই শর্তের ভয়ে কোম্পানিরা GPL code training-এ কম নেবে। এটা শুধু অনুমান।

- **Contamination defence হিসেবে copyleft:** Authors ধরে নিয়েছেন যে proprietary model কোম্পানিগুলো আইনি ঝুঁকির কারণে GPL code training-এ কম ব্যবহার করবে। এটা একটা **আইনি/নীতিগত অনুমান**, কোনো পরীক্ষা দিয়ে প্রমাণ করা নয় (Section ১২-এ বিস্তারিত সমালোচনা)।
- **Commercial repo:** Startup-দের সাথে formal partnership করে তাদের private engineering repo **কেনা** হয়েছে। এগুলো internet-এ নেই, তাই training data-তে থাকার সম্ভাবনা খুব কম — এটা **access restriction** দিয়ে contamination defence।

### ২.৩ Public / Held-out / Commercial Split
| Split | Task | Repo | কী public | উদ্দেশ্য |
|---|---|---|---|---|
| **Public** | 731 | 11 (GPL/copyleft) | Task + ফলাফল দুটোই | সবাই নিজের agent চালাতে পারবে |
| **Commercial** | 276 | 18 (startup-এর private) | শুধু ফলাফল (code private, আইনি কারণে) | Enterprise-ধরনের codebase-এ বাস্তব ক্ষমতা মাপা |
| **Held-out** | 858 | 12 (public set-এর মতো, কিন্তু আলাদা repo) | কিছুই না | ভবিষ্যতে public set-এ **overfitting** হচ্ছে কিনা পরীক্ষা |

**সহজ কথায়:** Public set সবাই দেখতে পায়, তাই কেউ সেটার জন্য AI-কে "মুখস্থ" করিয়ে ফেলতে পারে। Held-out set হলো তালা দেওয়া আরেকটা পরীক্ষার খাতা, যেটা পরে দেখে নেওয়া যাবে কেউ ঠকিয়েছে কিনা। Commercial set-এ আসল startup-এর private code আছে, তাই কেউ সেটা চালাতে পারে না।

- **Held-out set-এর যুক্তি:** কোনো public benchmark জনপ্রিয় হলে model developer-রা (ইচ্ছায় বা অনিচ্ছায়) সেটার জন্য tune করে ফেলে। তখন public score বাড়ে কিন্তু আসল ক্ষমতা বাড়ে না। একটা গোপন, একই ধরনের set-এ score যদি অনেক কম হয়, তাহলে বোঝা যাবে public set-এ overfitting হয়েছে। (Machine learning-এর train/validation/test ধারণার মতো, কিন্তু এখানে "test" set-টা ভবিষ্যতের জন্য তালাবদ্ধ।)

### ২.৪ Multi-language Repository ও Containerized Environment
- SWE-bench শুধু Python (Sub-domain 1, Paper 01)। SWE-Bench Pro-তে **Python, Go, JavaScript (JS), TypeScript (TS)**।
- প্রতিটা language-এর build/run পদ্ধতি আলাদা:
  - **Python:** isolated virtual environment (প্রতিটা project-এর আলাদা package set)।
  - **JS/TS:** Node.js runtime + npm/yarn package manager।
  - **Go:** module-aware environment, সঠিক `GOPATH` configuration।
- **Docker container:** পুরো OS + dependency + codebase একটা image-এ বেঁধে রাখা, যাতে যেকোনো machine-এ হুবহু একই environment চলে। Authors বলছেন সব environment pre-built Docker image হিসেবে release করা হবে → reproducibility।
- **TypeScript:** JavaScript-এর উপর static type যোগ করা language; compile করে JS বানানো হয়। Type error-ও build fail করাতে পারে।

### ২.৫ Human Augmentation: Problem Statement, Requirements, Interface
প্রতিটা task-এর description-এ তিনটা অংশ:
1. **Problem statement:** আসল commit/PR/issue থেকে তথ্য নিয়ে **GitHub issue-এর ঢঙে নতুন করে লেখা** — motivation আর সমস্যা, কিন্তু মূল উৎসের বাইরে কিছু যোগ না করে। অনেক commit message-এ কোনো বর্ণনাই থাকে না (Appendix Table 6-এ উদাহরণ: "enable vCard v4.0 contact import (close #1328) — No description provided" থেকে পুরো একটা issue লেখা হয়েছে)।
2. **Requirements:** মানুষের লেখা একটা তালিকা — কী behaviour চাই, যা unit test সরাসরি পরীক্ষা করবে। যেমন test যদি একটা নির্দিষ্ট error log string খোঁজে, requirement-এ সেই হুবহু string লেখা থাকে। Authors-এর দাবি: requirement **কীভাবে implement করতে হবে বলে না**, solution leak করে না।
3. **Interface (optional):** নতুন বা পরিবর্তিত public class/function-এর নাম, signature, file path। শুধু তখনই দেওয়া হয় যখন solution-এ নতুন interface লাগে।

### ২.৬ Test Verifier-এর False Negative বনাম False Positive (খুব গুরুত্বপূর্ণ)
Test suite আসলে একটা **verifier** — patch সঠিক কিনা "রায়" দেয়।

| | Test বলে PASS | Test বলে FAIL |
|---|---|---|
| **Patch আসলে সঠিক** | ✅ True positive | ❌ **False negative** — সঠিক solution, কিন্তু test অন্য নাম/structure আশা করছিল |
| **Patch আসলে ভুল** | ❌ **False positive** — patch overfitting / plausible-but-wrong (আমাদের CG1) | ✅ True negative |

**সহজ কথায়:** Test হলো বিচারক। বিচারক কখনো সঠিক patch-কে ভুল বলে (false negative), কখনো ভুল patch-কে সঠিক বলে (false positive)। এই paper প্রথমটা কমাতে চেয়েছে। আমরা বেশি চিন্তিত দ্বিতীয়টা নিয়ে।

- SWE-Bench Pro মূলত **false negative** কমানোর দিকে মনোযোগ দিয়েছে (interface ও requirements দিয়ে)।
- আমাদের Sub-domain 1 ও 2-এর মূল চিন্তা ছিল **false positive** (AutoCodeRover-এর test pass করা patch-এর মাত্র 65.4% সঠিক — Sub-domain 1 summary দেখো)। এই দুইয়ের পার্থক্য মনে রাখা দরকার — Section ১২ ও ১৩-এ কাজে লাগবে।

### ২.৭ Human-verified Test ও Flaky Test
- **Flaky test:** code না বদলালেও কখনো pass, কখনো fail করে (timing, network, random seed-এর কারণে)। Flaky test থাকলে benchmark score-এ noise ঢোকে।
- SWE-Bench Pro gold patch দিয়ে test **কয়েকবার** চালিয়ে দেখে সবসময় pass করে কিনা; না করলে task বাদ।
- তারপর মানুষ প্রতিটা fail2pass test দেখে: (ক) task description-এর সাথে **প্রাসঙ্গিক** কিনা, (খ) **অতিরিক্ত broad** কিনা (অর্থাৎ task-এর বাইরের অনেক কিছু পরীক্ষা করে)। দুটোর কোনো একটা হলে test বাদ; সব test বাদ পড়লে পুরো task বাদ।

### ২.৮ Scaffold, Turn Limit, Cost Limit
- **Scaffold:** LLM-এর চারপাশের "কাঠামো" — prompt, tool (bash, editor, search), loop logic। একই LLM ভিন্ন scaffold-এ ভিন্ন score পায়। এই paper মূলত **SWE-agent** scaffold ব্যবহার করেছে (Sub-domain 1, Paper 02 দেখো); **Agentless**-ও চেষ্টা করেছিল কিন্তু multi-file edit-এ সমস্যার কারণে বাদ দিয়েছে (Sub-domain 1, Paper 04 দেখো)।
- **Turn:** agent-এর একটা action + environment-এর observation = এক turn। এখানে সর্বোচ্চ **50 turn**।
- **Cost limit:** একটা task-এ LLM API-তে সর্বোচ্চ কত খরচ করা যাবে। Analysis section-এ **2 USD** cap।
- **Unified scaffold:** সব model-কে একই scaffold, একই prompt (SWE-agent-এর default prompt) দেওয়া — যাতে পার্থক্য model-এর, scaffold-এর নয়।

### ২.৯ Pass@1 ও Resolve Rate
প্রতিটা task-এ একবার চালানো, তার patch test-এ pass করলে resolved। Resolved task-এর শতাংশই resolve rate; এই paper এটাকে **Pass@1** বলছে। Pass@k-এর সাধারণ সূত্র Sub-domain 1, Paper 01-এর Section ৬.১০-এ আছে।

### ২.১০ Trajectory, Failure Mode ও LLM-as-a-Judge
- **Trajectory:** agent-এর পুরো কাজের লগ — প্রতিটা thought, action, observation।
- **Failure mode:** agent কেন ব্যর্থ হলো তার শ্রেণি (ভুল solution, ভুল file, tool ভুল ব্যবহার, loop-এ আটকে যাওয়া...)।
- **LLM-as-a-Judge:** হাজার হাজার trajectory মানুষের পক্ষে পড়া কঠিন, তাই একটা শক্তিশালী LLM (এখানে **GPT-5**)-কে trajectory পড়িয়ে category বলতে বলা। SWE-agent paper এই পদ্ধতিতে মানুষের সাথে 87% মিল দেখিয়েছিল (Sub-domain 1, Paper 02 দেখো — সেখানে validation set ছিল মাত্র 15টা)।
- **Submitted বনাম Not-submitted:** agent নিজে `submit` করে patch দিলে "submitted"; turn/cost/context শেষ হয়ে গেলে বা crash করলে "not submitted"।

### ২.১১ Open-weight Model, vLLM ও Tool-use Parsing
- **Open-weight model:** weight public (যেমন Qwen3 32B, GPT-OSS, Kimi K2) — নিজের GPU-তে চালানো যায়।
- **vLLM:** open model দ্রুত serve করার জন্য একটা inference engine।
- কিছু open model native "function calling" ভালো পারে না; তাই output text-কে **syntax parsing** করে tool call বের করা হয়েছে।
- **SWE-Smith-32B:** SWE-bench-ধরনের trajectory দিয়ে fine-tune করা একটা open model (paper-এর ভাষায় "models fine-tuned on SWE-bench-like trajectories")।
- **Extended thinking:** কিছু model-এর উত্তর দেওয়ার আগে লম্বা reasoning করার mode। Opus 4.1 এখানে **extended thinking ছাড়া** চালানো হয়েছে।

### ২.১২ SWE-Bench Verified ও Saturation (সংক্ষেপে)
OpenAI-এর 500-task, মানুষ দিয়ে filter করা SWE-bench subset (Sub-domain 1, Paper 01-এর Section ১৭ দেখো)। SWE-Bench Pro-এর authors বলছেন: (ক) Verified-এর 161/500 task মাত্র 1–2 line পরিবর্তন চায়; (খ) top model-রা Verified-এ 70%-এর বেশি পায় (Conclusion) — অর্থাৎ benchmark saturation-এর দিকে।

### ২.১৩ Mean বনাম Median (Skewed Distribution)
Patch size-এর মতো data-তে কয়েকটা খুব বড় মান গড় (mean)-কে টেনে উপরে নেয়। তাই median (মাঝের মান) আলাদা করে দেখা দরকার। SWE-Bench Pro-তে mean 107.4 line কিন্তু median 55.0 line → distribution ডান দিকে লম্বা (right-skewed)।

---

## ৩. Problem Statement — কী সমস্যা ছিল?

### ৩.১ মূল সমস্যা (Authors-এর ভাষায়)
1. **Contamination:** জনপ্রিয় open-source repo — বিশেষ করে MIT, Apache 2.0, BSD-এর মতো permissive license-এর — LLM pre-training-এর web-crawl corpus-এ ঢোকার প্রধান প্রার্থী। তাই public GitHub থেকে benchmark বানানো "inherently difficult"।
2. **Task complexity কম:** SWE-Bench Verified-এর 500-এর মধ্যে **161টা** মাত্র 1–2 line পরিবর্তন চায়। কিন্তু enterprise software engineering-এ প্রায়ই শত শত line, একাধিক file-এর পরিবর্তন লাগে।
3. **Saturation:** Verified-এ top model 70%-এর বেশি — তাই নতুন model-দের মধ্যে পার্থক্য ধরা কঠিন।
4. **Underspecified task description:** আসল commit message প্রায়ই অগোছালো, অসম্পূর্ণ বা একদম নেই; আসল issue বোঝার জন্য অনেক আলোচনা, screenshot, link লাগে। ফলে agent task বুঝতে না পেরে ব্যর্থ হয় — এটা agent-এর দোষ নয়, benchmark-এর দোষ (Sub-domain 1, Paper 04-এ Agentless দেখিয়েছিল Lite-এর 10.0% issue-তে যথেষ্ট তথ্য নেই)।
5. **Test-এর false negative:** নতুন feature-এর test নির্দিষ্ট class/function নাম আশা করে; agent অন্য নামে সঠিক solution দিলেও fail।

**সহজ কথায়:** সমস্যাগুলো হলো: AI আগে থেকেই উত্তর দেখে ফেলতে পারে, task বেশি সহজ, পরীক্ষা saturated, বর্ণনা অস্পষ্ট, আর test অতিরিক্ত কড়া। এই পাঁচটাই এক এক করে ধরার চেষ্টা করেছে SWE-Bench Pro।

### ৩.২ কেন এটা গুরুত্বপূর্ণ?
Benchmark score দেখে কোম্পানি ও researcher-রা সিদ্ধান্ত নেয় কোন agent production-এ ব্যবহার করবে। Score যদি contamination বা সহজ task-এর কারণে ফোলা হয়, তাহলে agent-এর উপর ভুল আস্থা তৈরি হয় — যা সরাসরি আমাদের **reliability ও assurance** domain-এর সমস্যা।

---

## ৪. Goal ও Research Questions

**Goal:** একটা contamination-resistant, industrially realistic, কঠিন ও বৈচিত্র্যময় benchmark বানানো, যার প্রতিটা task মানুষ দিয়ে যাচাই করা এবং "resolvable" (যথেষ্ট তথ্যসহ)।

**তিনটা contribution (authors):**
1. নতুন data collection strategy — copyleft public repo + কেনা commercial repo; তিন ধরনের access policy।
2. কঠিন, বৈচিত্র্যময় task — trivial (1–10 line) edit বাদ; প্রতি repo 50–100 task cap।
3. Human-in-the-loop augmentation ও verification workflow — ambiguity দূর করা আর test-কে robust verifier বানানো।

Paper-এর implicit RQ:
- **RQ1:** Frontier ও open model SWE-Bench Pro-তে কতটা পারে? (Table 1, 5)
- **RQ2:** Public বনাম commercial (enterprise) codebase-এ পার্থক্য কত? (Table 2)
- **RQ3:** Language, repository, file সংখ্যা ও patch size অনুযায়ী performance কীভাবে বদলায়? (Figure 3)
- **RQ4:** Human augmentation (requirements + interface) কতটা দরকারি? (Table 3)
- **RQ5:** Agent-রা কোন কারণে ব্যর্থ হয়? (Table 4, LLM-as-judge)

**সহজ কথায়:** পাঁচটা প্রশ্নের মোটামুটি রূপ: AI কত পারে? আসল কোম্পানির code-এ কত পারে? কোন language আর কত বড় patch-এ কত পারে? স্পষ্ট নির্দেশ কতটা কাজে লাগে? আর ব্যর্থ হলে কেন?

---

## ৫. Methodology — কীভাবে কাজটা করা হয়েছে

### ৫.১ Repository Selection
- সব repo **actively maintained**, বড় user base, ভালো documentation, প্রতিষ্ঠিত development practice।
- Domain বৈচিত্র্য: complex UI logic-এর consumer application, জটিল business rule-এর B2B platform, sophisticated API-র developer tool।
- **Public set-এর 11টা repo** (Figure 1 ও Figure 3 থেকে): ansible, openlibrary, qutebrowser (Python); flipt, vuls, navidrome, teleport (Go); tutanota (TS); element-web, NodeBB, webclients (JS — paper-এর Figure 3-এর label অনুযায়ী)।
- **Commercial:** startup-এর সাথে যোগাযোগ করে তাদের engineering repo কেনা।
- **Repo cap:** প্রতি repo 50–100 task (Introduction-এ "strict cap of 100"; Section 3.1-এ "50-100+")। উদ্দেশ্য: কোনো model একটা repo-তে বিশেষ ভালো হয়ে পুরো score না বাড়াতে পারে।

### ৫.২ Problem Sourcing (Section 4.1)
1. Repo-র commit history থেকে **পরপর দুটো commit**-এর জোড়া খোঁজা, যেটা একটা issue-র সমাধান ধরে রাখে।
2. পুরনো commit = **base**, নতুন commit = **instance**।
3. দুই commit-এর মধ্যে test-সংক্রান্ত file-এর diff = **test patch** (নতুন বা পরিবর্তিত test)।
4. বাকি diff = **gold patch** (reference solution)।

**সহজ কথায়:** দুটো commit-এর মধ্যে যা বদলেছে তার test-এর অংশ হলো "প্রশ্নের যাচাই-সূত্র" আর বাকিটা "সঠিক উত্তর"। AI শুধু প্রশ্ন দেখে, উত্তর দেখে না।

**SWE-bench-এর সাথে পার্থক্য:** SWE-bench issue-linked merged PR থেকে শুরু করে (Sub-domain 1, Paper 01-এর Section ৫.১); SWE-Bench Pro **commit pair** থেকে শুরু করে, আর মানুষ দিয়ে issue লিখিয়ে নেয় — তাই এমন পরিবর্তনও task হতে পারে যার কোনো GitHub issue নেই।

### ৫.৩ Complexity Filter
- 1–10 line-এর trivial edit বাদ; প্রতিটা task-এ **অন্তত 10 line** পরিবর্তন।
- Authors: multi-file, substantial পরিবর্তন রাখা হয়েছে।
- ফলাফল (public set): reference solution গড়ে **107.4 line, 4.1 file**; **100-এর বেশি task-এ 100 line-এর বেশি** পরিবর্তন।

### ৫.৪ Task Description তৈরি (Section 4.2, Appendix B)
| ধাপ | কাজ |
|---|---|
| 1 | উৎস সংগ্রহ: issue discussion, commit message, PR |
| 2 | **Problem statement** লেখা — repo-র নিজস্ব issue template ব্যবহার করে, motivation সহ, উৎসের বাইরে না গিয়ে |
| 3 | **Requirements** লেখা — gold patch ও test-এর প্রত্যাশার উপর ভিত্তি করে, behaviour বলে কিন্তু implementation বলে না |
| 4 | **Interface** (দরকার হলে) — নতুন/পরিবর্তিত class ও function-এর নাম, signature, file path |

**সহজ কথায়:** মানুষ এখানে তিনটা জিনিস লিখে দিয়েছে: সমস্যাটা কী, কী behaviour চাই, আর কোন function বা class-এর কী নাম হবে। এতে AI-কে অনুমান করতে হয় না। কিন্তু একই কারণে কাজটা সহজও হয়ে যায়।

**Appendix-এর উদাহরণ (Open Library, Internet Archive-এর একটা full-stack web app):** "BookWorm-এ Google Books-কে fallback metadata source হিসেবে যোগ করো"।
- Requirements-এ ৮টা bullet, যেমন: `openlibrary/core/imports.py`-এর `STAGED_SOURCES` tuple-এ `"google_books"` থাকতে হবে; Google Books একটা ISBN-এর জন্য একাধিক result দিলে warning log করে staging skip করতে হবে; parsed field-এর তালিকা (`isbn_10`, `isbn_13`, `title`, `subtitle`, `authors`, `source_records`, `publishers`, `publish_date`, `number_of_pages`, `description`)।
- Interface-এ ৪টা function (`fetch_google_book`, `process_google_book`, `stage_from_google_books`, `get_current_batch`) আর ২টা class (`BaseLookupWorker`, `AmazonLookupWorker`) ও তাদের `run` method — সবই `scripts/affiliate_server.py`-এ।

### ৫.৫ Environment তৈরি ও যাচাই (Section 4.3)
1. **Environment construction:** professional software engineer-রা প্রতিটা codebase-এর জন্য Dockerfile বানিয়েছে — system package, build tool, dependency, documentation দেখে — যতক্ষণ না codebase ও test চলে।
2. **Environment verification (automatic, in-house pipeline):** gold patch-সহ test **কয়েকবার** চালানো; সবসময় pass না করলে (flaky) task বাদ।
3. **Test verification (human):** প্রতিটা fail2pass test-এর relevance ও breadth যাচাই; irrelevant বা too broad test বাদ; সব বাদ পড়লে task বাদ।
- প্রতিটা task-এ **fail2pass** (issue ঠিক হলো কিনা) ও **pass2pass** (কিছু ভাঙলো কিনা) test।

**সহজ কথায়:** Fail2pass test হলো "সমস্যাটা সারলে এই test পাস করবে"। Pass2pass test হলো "আগে যা ঠিক ছিল তা যেন না ভাঙে"। দুটো মিলিয়েই patch-এর বিচার।

**আমার পর্যবেক্ষণ:** কয়টা commit pair থেকে শুরু করে প্রতিটা ধাপে কয়টা বাদ পড়েছে (funnel), কয়জন annotator, annotator-দের মধ্যে agreement — এসব সংখ্যা paper-এ নেই। SWE-bench (Paper 01) অন্তত ~90,000 PR থেকে 2,294-এ আসার funnel দিয়েছিল।

### ৫.৬ Evaluation Setup (Section 5)
| বিষয় | মান |
|---|---|
| **Scaffold** | SWE-agent (Agentless চেষ্টা করা হয়েছিল — multi-file edit-এ দুর্বল, তাই বাদ) |
| **Prompt** | সব model-এর জন্য একই — SWE-agent-এর default prompt |
| **Model version** | 18 September 2025 পর্যন্ত সর্বশেষ version |
| **Open model hosting** | vLLM, একটা node, 8টা NVIDIA H100 GPU |
| **Tool-use** | সম্ভব হলে native; open-weight model-এ syntax parsing |
| **Turn limit** | সর্বোচ্চ 50 turn |
| **Cost limit** | Analysis section (Table 5, Figure 3, Table 3, Table 4): সর্বোচ্চ 2 USD/task |
| **Opus 4.1** | Extended thinking ছাড়া |
| **Issue ambiguity** | সবসময় problem statement + requirements + interface দেওয়া ("without any ambiguity") — অর্থাৎ ambiguity সমাধানের ক্ষমতা মাপা হচ্ছে না, দেওয়া spec implement করার ক্ষমতা মাপা হচ্ছে |
| **Metric** | Pass@1 resolve rate |
| **Analysis set** | সব analysis শুধু public set-এ (commercial set-এর সাথে leakage এড়াতে); held-out ভবিষ্যতের জন্য রাখা |

**সহজ কথায়:** সবার জন্য একই নিয়ম: একই কাঠামো, একই prompt, একই ধাপ-সীমা। তাই পার্থক্য model-এর, কাঠামোর নয়। তবে সব নির্দেশ দেওয়া থাকে, তাই এখানে অস্পষ্ট নির্দেশ বোঝার ক্ষমতা মাপা হয় না।

### ৫.৭ Failure-mode Analysis পদ্ধতি (Section 6.3, Appendix C)
1. Heuristic ও random sample trajectory দেখে হাতে failure bucket বানানো।
2. প্রতিটা model-এর শুধু **unresolved** instance নেওয়া।
3. প্রতিটা trajectory-র **শেষ 20 turn** নেওয়া — 10 ও 40 turn-এর তুলনায় 20 turn-এ মানুষের validation-এর সাথে সবচেয়ে বেশি মিল (সংখ্যা দেওয়া নেই)।
4. GPT-5 judge-কে system prompt-এ bucket-এর কঠোর বর্ণনা, SWE-agent format, tool-এর বর্ণনা, problem statement, exit status দেওয়া।
5. Judge আগে এক paragraph reasoning (`<description>` tag-এ), তারপর **ঠিক একটা** category দেয়; নতুন category বানানো নিষেধ, না মিললে "other"।

**সহজ কথায়:** প্রতিটা ব্যর্থ agent-এর শেষ 20 ধাপ GPT-5-কে পড়িয়ে বলা হয়েছে "কোন ধরনের ভুল?"। এভাবে হাজার হাজার লগ মানুষ না পড়েই ভাগ করা গেছে। তবে judge নিজেও ভুল করতে পারে।

Judge prompt-এর ১০টা category (Appendix C.1): `identified_incorrect_file`, `missed_edge_case`, `misunderstood_problem_statement`, `wrong_solution`, `tool_error`, `infinite_loop`, `endless_file_reading`, `context_overflow_from_listing`, `syntax_error`, `other`।

Table 4-এর ৯টা column: Submitted-এর ভেতরে — Wrong Solution, Syntax Error, Incorrect File, Instruction Following, Edge Case, Other; Not-submitted-এর ভেতরে — Tool-Use, Long-Context, Stuck in Loop।

**আমার পর্যবেক্ষণ:** prompt-এর ১০টা category কীভাবে table-এর ৯টা column-এ map হয়েছে (যেমন `endless_file_reading` আর `infinite_loop` কি দুটোই "Stuck in Loop"-এ গেছে?) paper স্পষ্ট বলেনি। নাম দেখে মনে হয় `misunderstood_problem_statement` → Instruction Following, `context_overflow_from_listing` → Long-Context — কিন্তু এটা আমার অনুমান।

---

## ৬. Mathematical Formulation — সূত্র ও ব্যাখ্যা

Benchmark paper হওয়ায় paper-এ কোনো equation নেই। নিচের সব সূত্র paper-এর বর্ণনাকে formal ভাবে লেখা (আমার formalisation); সংখ্যাগুলো paper-এর। যেখানে নিজের statistical হিসাব, সেখানে **"আমার হিসাব"** লেখা।

### ৬.১ একটা Task Instance

**এটা কী হিসাব করে:** একটা task আসলে সাতটা জিনিসের একটা প্যাকেজ: code, সমস্যার বর্ণনা, requirements, interface, test, সঠিক উত্তর আর Docker environment। Agent শুধু প্রথম চারটা দেখে।

$$
I = \left( C,\; P,\; Q,\; F,\; T,\; \delta,\; E \right)
$$
| Symbol | মানে |
|---|---|
| $C$ | base commit-এ codebase |
| $P$ | human-augmented problem statement |
| $Q$ | requirements-এর তালিকা |
| $F$ | interface specification (optional; না থাকলে খালি) |
| $T$ | test patch (fail2pass ও pass2pass test) |
| $\delta$ | gold patch |
| $E$ | Docker environment (language-specific) |

SWE-bench-এর $I = (C, P, T, \delta)$-এর (Paper 01, Section ৬.১) সাথে তুলনা করলে নতুন হলো $Q$, $F$ আর explicit $E$। Agent $A$ পায় $(C, P, Q, F)$ আর $E$-এর ভেতরে কাজ করে patch $\hat{\delta}$ বানায়:
$$
\hat{\delta} = A\left( C,\; P,\; Q,\; F \right)
$$

### ৬.২ Commit Pair থেকে Task (Section 4.1)

**এটা কী হিসাব করে:** দুই commit-এর মোট পরিবর্তনকে দুই ভাগ করা হয়: test-এর অংশ আর উত্তরের অংশ। কোনো পরিবর্তন দুই ভাগে পড়ে না।

$c_b$ = base commit, $c_i$ = instance commit, $\Delta = \text{diff}(c_b, c_i)$। Test-সংক্রান্ত file-এর diff test patch, বাকিটা gold patch:
$$
\Delta = T \cup \delta, \qquad T \cap \delta = \{\,\}
$$
($\{\,\}$ মানে ফাঁকা সেট; সহজ ভাষায় — একই পরিবর্তন দুই ভাগে পড়ে না।)

### ৬.৩ Complexity ও Diversity Constraint

**এটা কী হিসাব করে:** এখানে দুটো নিয়ম লেখা আছে। এক, প্রতি task-এ অন্তত 10 line বদলাতে হবে। দুই, প্রতি repo থেকে 50 থেকে 100টা task নেওয়া হবে।

$\text{LOC}(\delta)$ = gold patch-এ পরিবর্তিত line, $\text{Files}(\delta)$ = পরিবর্তিত file সংখ্যা, $n_r$ = repo $r$ থেকে নেওয়া task সংখ্যা:
$$
\text{LOC}(\delta) \geq 10, \qquad 50 \leq n_r \leq 100
$$
**Worked example (paper-এর সংখ্যা):** Public set-এ $\text{mean}(\text{LOC}) = 107.4$, $\text{median}(\text{LOC}) = 55.0$, $\text{mean}(\text{Files}) = 4.1$। SWE-Bench Verified-এ (Figure 1) mean 11.6, median 4.5।

**আমার হিসাব:**
- Mean অনুপাত: $107.4 / 11.6 \approx 9.26$ গুণ; median অনুপাত: $55.0 / 4.5 \approx 12.2$ গুণ।
- Mean/median = $107.4 / 55.0 \approx 1.95$ → গড় median-এর প্রায় দ্বিগুণ → কয়েকটা খুব বড় patch গড়কে টেনে তুলেছে (right-skewed — মানে বেশিরভাগ patch ছোট, কয়েকটা অনেক বড়)।
- Verified-এ trivial task-এর অনুপাত: $161 / 500 = 32.2\%$।

**আমার পর্যবেক্ষণ — $n_r$ constraint সব split-এ খাটে না:** Commercial set-এ $276 / 18 \approx 15.3$ task/repo, যা "50–100" নিয়মের অনেক নিচে। Public-এ $731 / 11 \approx 66.5$, held-out-এ $858 / 12 = 71.5$ — এই দুটো নিয়মের মধ্যে। অর্থাৎ repo cap নিয়মটা মূলত public ও held-out-এর জন্য।

### ৬.৪ Split-এর Formal রূপ

**এটা কী হিসাব করে:** সব task তিন ভাগে (public, held-out, commercial) ভাগ হয়। আর একই repo দুই ভাগে একসাথে থাকে না।

$$
\mathcal{D} = \mathcal{D}_{\text{pub}} \cup \mathcal{D}_{\text{held}} \cup \mathcal{D}_{\text{com}}, \qquad \text{Repos}(\mathcal{D}_{x}) \cap \text{Repos}(\mathcal{D}_{y}) = \{\,\} \;\; (x \neq y)
$$
অর্থাৎ তিনটা split-এর repository আলাদা (paper: held-out "uses a separate set of repositories")।

| Split | $N$ | Repo | মোটের % (আমার হিসাব) |
|---|---|---|---|
| Public | 731 | 11 | $731/1865 \approx 39.2\%$ |
| Commercial | 276 | 18 | $276/1865 \approx 14.8\%$ |
| Held-out | 858 | 12 | $858/1865 \approx 46.0\%$ |
| **মোট** | **1,865** | **41** | 100% |

**সহজ কথায়:** তিন ভাগের সংখ্যা যোগ করলে ঠিক 1,865 আর 41 মেলে। মানে হিসাবে কোনো গোলমাল নেই। সবচেয়ে বড় অংশ held-out (46%), যেটার ফল কেউ দেখেনি।

যাচাই: $731 + 276 + 858 = 1865$ ✓, $11 + 18 + 12 = 41$ ✓।

### ৬.৫ Flaky Test Filter

**এটা কী হিসাব করে:** Flaky test মানে যে test কখনো pass, কখনো fail করে। সঠিক উত্তর দিয়ে বারবার চালিয়ে একবারও fail করলে সেই task ফেলে দেওয়া হয়।

Gold patch-সহ environment-এ $k$ বার test চালানো ($k$-এর মান paper বলেনি — "several times")। $\text{pass}_j(I)$ = $j$-তম run-এ সব test pass করলে 1:
$$
\text{Keep}(I) = \prod_{j=1}^{k} \text{pass}_j(I)
$$
গুণফল 1 হবে শুধু তখনই যখন **প্রতিটা** run pass করে — একবার fail করলেই task বাদ।

### ৬.৬ Human Test Verification

**এটা কী হিসাব করে:** মানুষ প্রতিটা test দেখে বাদ দেয় যেগুলো task-এর সাথে সম্পর্কহীন বা অতিরিক্ত বড়। একটা test-ও না থাকলে পুরো task বাদ।

$\text{F2P}$ = gold patch-এ fail থেকে pass হওয়া test-এর set (সংজ্ঞা Paper 01, Section ৬.২)। Human verification-এর পর:
$$
\text{F2P}' = \{\, t \in \text{F2P} \;:\; \text{Relevant}(t, P, Q) \land \neg\, \text{TooBroad}(t) \,\}
$$
$$
\text{Drop}(I) = 1 \quad \text{যদি} \quad \text{F2P}' = \{\,\}
$$

### ৬.৭ Resolve Rate (Pass@1)

**এটা কী হিসাব করে:** একবার চেষ্টায় কত শতাংশ task সফল হলো, সেটা গোনা হয়। মানে (সফল task সংখ্যা ÷ মোট task) × 100।

Resolved-এর শর্ত SWE-bench-এর মতোই (Paper 01, Section ৬.৩): $\hat{\delta}$ apply হয় এবং $\text{F2P}' \cup \text{P2P}$-এর সব test pass করে। তারপর:
$$
\text{Resolve}(A, \mathcal{D}_x) = \frac{1}{N_x} \sum_{i=1}^{N_x} \text{Resolved}\left(\hat{\delta}_i\right) \times 100
$$
**Worked example (আমার হিসাব, Table 1):** Claude Sonnet 4.5, $N = 731$, 43.6% → $731 \times 0.436 \approx 318.7$ → **প্রায় 319টা task** ($319/731 = 43.64\%$ ✓)।
Commercial (Table 2): Claude Opus 4.1, $N = 276$, 17.8% → $276 \times 0.178 \approx 49.1$ → **প্রায় 49টা task**।

**আমার পর্যবেক্ষণ:** কিছু শতাংশ কোনো পূর্ণসংখ্যা count-এর সাথে মেলে না — যেমন Table 1-এ GPT-5 (High) 41.8% ($305/731 = 41.7\%$, $306/731 = 41.9\%$), Kimi K2 27.7%, GPT-OSS 120B 16.2%; Table 2-এ GPT-5 (High) 15.7% ($43/276 = 15.6\%$, $44/276 = 15.9\%$)। সম্ভাব্য কারণ: কিছু instance evaluation থেকে বাদ পড়েছে, বা একাধিক run-এর গড় — paper ব্যাখ্যা দেয়নি।

### ৬.৮ Budget-সীমিত Agent Run

**এটা কী হিসাব করে:** Agent-এর চালানো সীমিত: সর্বোচ্চ 50 ধাপ আর মোট 2 USD খরচ। সীমা পেরোলে সে থামে, আর তখন সাধারণত কোনো patch জমা পড়ে না। তাই score আসলে সীমার উপরও নির্ভর করে।

Trajectory $\tau = (a_1, o_1, a_2, o_2, \ldots, a_L, o_L)$, যেখানে $a_j$ = action, $o_j$ = observation। Run বৈধ থাকে যতক্ষণ:
$$
L \leq 50 \quad \land \quad \sum_{j=1}^{L} \text{cost}(a_j) \leq 2 \;\text{USD}
$$
সীমা পেরোলে agent থেমে যায় → সাধারণত "not submitted"। তাই resolve rate আসলে **budget-এর function**:
$$
\text{Resolve} = f\left(\text{model},\; \text{scaffold},\; L_{\max},\; \text{cost}_{\max}\right)
$$
**Worked example (আমার হিসাব):** একই model, একই public set — Table 1 (cost cap উল্লেখ নেই) বনাম Table 5 (2 USD cap):
- Claude Sonnet 4: $42.7 - 17.6 = 25.1$ percentage point (pp) পার্থক্য (pp মানে শতাংশের সরাসরি বিয়োগ; 42.7% থেকে 17.6%-এ নামলে 25.1 pp কমা)।
- GPT-5 (High): $41.8 - 25.9 = 15.9$ pp পার্থক্য।

Paper এই পার্থক্যের কারণ স্পষ্ট করে বলেনি; cost cap ছাড়াও version/সময়ের পার্থক্য থাকতে পারে। কিন্তু এটা দেখায় যে **"score" একটা একক সংখ্যা নয় — budget না বললে তুলনা অর্থহীন** (আমাদের CG8)।

### ৬.৯ Sampling Uncertainty: Standard Error ও Wilson Interval (আমার হিসাব)

**এটা কী হিসাব করে:** Score হলো মাত্র 731টা task থেকে পাওয়া একটা সংখ্যা। অন্য 731টা task নিলে সংখ্যাটা একটু বদলাতে পারত। SE (standard error) বলে সংখ্যাটা কতটা নড়তে পারে। Wilson interval বলে আসল ক্ষমতা সম্ভবত কোন সীমার ভেতরে (CI মানে confidence interval)। এখানে pp মানে percentage point, অর্থাৎ শতাংশের সরাসরি বিয়োগ।

Paper কোনো confidence interval দেয়নি। Resolve rate $\hat{p}$, task সংখ্যা $n$ হলে:
$$
SE = \sqrt{\frac{\hat{p}\left(1 - \hat{p}\right)}{n}}
$$
Wilson interval-এর কেন্দ্র $m$ ও অর্ধ-প্রস্থ $h$:
$$
m = \frac{\hat{p} + \dfrac{z^2}{2n}}{1 + \dfrac{z^2}{n}}, \qquad h = \frac{z\sqrt{\dfrac{\hat{p}(1-\hat{p})}{n} + \dfrac{z^2}{4n^2}}}{1 + \dfrac{z^2}{n}}
$$
Interval হলো $m - h$ থেকে $m + h$; 95%-এর জন্য $z = 1.96$। (ছোট $n$ বা 0/100-এর কাছের শতাংশে সাধারণ "$\hat{p}$ থেকে 1.96 SE কম-বেশি" interval-এর চেয়ে এটা বেশি নির্ভরযোগ্য।)

**Worked example:**
- Sonnet 4.5 (public): $\hat{p} = 0.436$, $n = 731$ → $SE = \sqrt{0.436 \times 0.564 / 731} \approx 0.0183$ (1.83 pp) → 95% Wilson CI ≈ **40.0% থেকে 47.2%**।
- Sonnet 4 (42.7%) → CI ≈ 39.2%–46.3%; GPT-5 High (41.8%) → CI ≈ 38.3%–45.4%।
- **সিদ্ধান্ত:** Table 1-এর শীর্ষ তিনটা model-এর CI প্রায় পুরোপুরি overlap করে। Sonnet 4.5 বনাম GPT-5 (High)-এর two-proportion z ≈ 0.70 — statistically আলাদা বলা যায় না। অর্থাৎ "Sonnet 4.5 সেরা" দাবিটা এই data দিয়ে শক্ত নয়।

**সহজ কথায়:** সেরা তিন model-এর score এত কাছাকাছি যে এক মাপে আরেকটাকে হারিয়েছে বলা যায় না। "Sonnet 4.5 সেরা" দাবিটা এই data-তে শক্ত নয়।

- Commercial set ছোট ($n = 276$), তাই অনিশ্চয়তা বেশি: Opus 4.1 (17.8%) → CI ≈ 13.7%–22.7%; GPT-5 High (15.7%) → CI ≈ 11.9%–20.5% — এখানেও শীর্ষ দুটো আলাদা করা যায় না।

**সহজ কথায়:** Commercial set-এ task কম, তাই সংখ্যাটা বেশি নড়বড়ে। শীর্ষ দুটো model-কে আলাদা করা যায় না।

### ৬.১০ Public বনাম Commercial Gap (আমার হিসাব)

**এটা কী হিসাব করে:** প্রথম সূত্র দুই score-এর পার্থক্য বলে (সরাসরি আর অনুপাতে)। দ্বিতীয় সূত্র (z-test) বলে এই পার্থক্য কাকতালীয় হতে পারে কিনা। z বড় হলে পার্থক্য কাকতালীয় নয়, এটা বেশি নিশ্চিত।

$$
\text{Gap}_{\text{abs}} = R_{\text{pub}} - R_{\text{com}}, \qquad \text{Gap}_{\text{rel}} = 1 - \frac{R_{\text{com}}}{R_{\text{pub}}}
$$
Two-proportion z-test (pooled):
$$
\bar{p} = \frac{R_{\text{pub}} n_{\text{pub}} + R_{\text{com}} n_{\text{com}}}{n_{\text{pub}} + n_{\text{com}}}, \qquad z = \frac{R_{\text{pub}} - R_{\text{com}}}{\sqrt{\bar{p}\left(1 - \bar{p}\right)\left(\dfrac{1}{n_{\text{pub}}} + \dfrac{1}{n_{\text{com}}}\right)}}
$$
**ধরে নেওয়া:** Table 2 (commercial)-এর setting Table 5-এর মতো (50 turn, 2 USD)। Paper এটা স্পষ্ট বলেনি, কিন্তু দুই table-এ একই model set আর কাছাকাছি সংখ্যা — তাই Table 5-এর সাথে তুলনা করছি।

**Worked example — GPT-5 (High):** $R_{\text{pub}} = 0.259$, $R_{\text{com}} = 0.157$, $n_{\text{pub}} = 731$, $n_{\text{com}} = 276$।
$\bar{p} = (189.3 + 43.3) / 1007 \approx 0.231$; $SE = \sqrt{0.231 \times 0.769 \times (1/731 + 1/276)} \approx 0.0298$; $z = 0.102 / 0.0298 \approx 3.43$ → $p \approx 0.0006$ → **significant**।

পুরো ফলাফল Section ৮.৩-এর table-এ।

### ৬.১১ Augmentation Ablation (Table 3)

**এটা কী হিসাব করে:** স্পষ্ট নির্দেশসহ score থেকে নির্দেশ ছাড়া score বাদ দেওয়া হয়। ফলটা বলে নির্দেশ কতটা সাহায্য করেছে। ρ বলে কত গুণ বেশি সাহায্য।

$$
\Delta_{\text{aug}} = R\left(P, Q, F\right) - R\left(P\right), \qquad \rho = \frac{R\left(P, Q, F\right)}{R\left(P\right)}
$$
**Worked example (আমার হিসাব):**
- GPT-5 (High): $25.9 - 8.4 = 17.5$ pp; $\rho = 25.9 / 8.4 \approx 3.08$ গুণ। Count-এ: প্রায় 189 বনাম 61 task।
- Claude Opus 4.1: $22.7 - 8.2 = 14.5$ pp; $\rho \approx 2.77$ গুণ। Count-এ: প্রায় 166 বনাম 60 task।
- Unpaired z-test ধরলেও z ≈ 8.9 ও 7.7 — পার্থক্য খুবই significant (paired data থাকলে McNemar test আরও উপযুক্ত হতো, কিন্তু paper per-instance data দেয়নি)।

**সহজ কথায়:** স্পষ্ট নির্দেশ থাকলে score প্রায় তিন গুণ। পার্থক্যটা এত বড় যে এটা কাকতালীয় হতে পারে না। কিন্তু এর কতটা test-এর দোষ আর কতটা কাজ সহজ হওয়ায়, সেটা আলাদা করা যায়নি।

**ব্যাখ্যার সতর্কতা (আমার পর্যবেক্ষণ):** $\Delta_{\text{aug}}$-কে authors পুরোপুরি "false negative" বলে ব্যাখ্যা করেছেন। কিন্তু এই পার্থক্যে দুটো জিনিস মিশে আছে:
$$
\Delta_{\text{aug}} = \Delta_{\text{FN}} + \Delta_{\text{easy}}
$$
**প্রথম অংশ $\Delta_{\text{FN}}$:** agent সঠিক কাজ করেছিল কিন্তু test অন্য নাম আশা করছিল (false negative কমা)। **দ্বিতীয় অংশ $\Delta_{\text{easy}}$:** requirements/interface file path ও function নাম বলে দেয়, ফলে localization (Paper 01-এর মূল bottleneck) সহজ হয়ে যায়। Paper এই দুটো আলাদা করে মাপেনি — যেমন "Problem statement only" setting-এ ব্যর্থ patch-গুলো হাতে দেখে কতগুলো আসলে সঠিক ছিল, সেটা গোনা হয়নি।

### ৬.১২ Failure-mode Distribution (Table 4)

**এটা কী হিসাব করে:** ব্যর্থ হওয়া agent-দের কাজের লগ থেকে প্রতিটা ভুলের ধরনের শতাংশ বের করা হয়। Table 4-এর শতাংশ নিজের group-এর ভেতরে (submitted বা not-submitted), পুরো failure-এর ভেতরে নয়।

Judge $J$ প্রতিটা unresolved trajectory $\tau$-কে একটা category $c \in \mathcal{C}$ দেয়। Model $m$-এর জন্য:
$$
\text{Share}_{\text{sub}}(c) = \frac{\left|\{\tau \;:\; J(\tau) = c\}\right|}{N_{\text{sub}}}, \qquad \text{Share}_{\text{overall}}(c) = \text{Share}_{\text{sub}}(c) \times \frac{N_{\text{sub}}}{N_{\text{sub}} + N_{\text{not}}}
$$
Table 4-এর প্রতিটা category-র % **নিজের group-এর** (submitted বা not-submitted) ভেতরে হিসাব করা, পুরো failure-এর নয়।

**Worked example — Claude Opus 4.1:** Submitted 511 (74.2%), Not-submitted 178 (25.8%)। Wrong Solution = 257 → submitted-এর ভেতরে $257/511 = 50.3\%$; পুরো failure-এর মধ্যে $257 / 689 \approx 37.3\%$ ($= 50.3\% \times 74.2\%$)।

যাচাই (আমার হিসাব): $257 + 160 + 25 + 14 + 4 + 51 = 511$ ✓ এবং $121 + 51 + 6 = 178$ ✓। ছয়টা model-এর সবকটার row-sum এভাবে মেলে।

**সহজ কথায়:** Table 4-এর সংখ্যাগুলো নিজেদের মধ্যে ঠিকঠাক যোগ হয়। কিন্তু মোট ব্যর্থ task-এর সংখ্যা 731-এর সাথে মেলে না (Section ৮.৮ দেখো)।

### ৬.১৩ LLM-judge-এর নির্ভরযোগ্যতা

**এটা কী হিসাব করে:** Judge আর মানুষ কতবার একই label দিয়েছে, সেটা গুনে শতাংশ করা হয়। যত বেশি মিল, judge-কে তত বেশি বিশ্বাস করা যায়।

Agreement rate:
$$
\text{Agree} = \frac{1}{M} \sum_{i=1}^{M} \mathbb{1}\left[J(\tau_i) = H(\tau_i)\right]
$$
$H$ = মানুষের label, $M$ = মানুষের label করা trajectory সংখ্যা। Paper নিজে $M$ বা Agree-এর মান দেয়নি — শুধু SWE-agent-এর 87% cite করেছে (সেখানে $M = 15$; Sub-domain 1, Paper 02 দেখো)। আর "20 turn সবচেয়ে ভালো" দাবির পক্ষেও সংখ্যা নেই।

### ৬.১৪ Reliability-এর জন্য দরকারি কিন্তু অনুপস্থিত Metric: pass^k

**এটা কী হিসাব করে:** একই task k বার চালালে সবকটাতেই সফল হওয়ার সম্ভাবনা কত, সেটা বের করে। এটা "কখনো পারে" নয়, "প্রতিবার পারে" মাপে।

Paper শুধু Pass@1 দেয়। একই task $k$ বার চালালে, $c$ বার সফল হলে, **সবকটা run সফল** হওয়ার সম্ভাবনার unbiased estimate:
$$
\text{pass}^{k} = \frac{\binom{c}{k}}{\binom{n}{k}}
$$
**উদাহরণ (কাল্পনিক, শুধু বোঝানোর জন্য):** $n = 5$ run, $c = 3$ সফল → pass@1 ≈ $3/5 = 0.6$, কিন্তু $\text{pass}^2 = \binom{3}{2}/\binom{5}{2} = 3/10 = 0.3$। অর্থাৎ "প্রতিবার নির্ভরযোগ্যভাবে" সফল হওয়ার হার অনেক কম। SWE-Bench Pro এটা মাপেনি (CG4 খোলা)।

**সহজ কথায়:** ধরো একটা AI 5 বার চেষ্টা করে 3 বার পারল। "একবার চেষ্টায় পারে" বললে 60%। কিন্তু "পরপর দুবারই পারে" বললে মাত্র 30%। Reliability দেখতে হলে এই দ্বিতীয় সংখ্যাটা দরকার।

---

## ৭. Experimental Setup

| বিষয় | বিবরণ |
|---|---|
| **Benchmark size** | 1,865 task; public 731, commercial 276, held-out 858 |
| **Repositories** | 41 (11 + 18 + 12) |
| **Languages** | Python, Go, JavaScript, TypeScript |
| **Evaluated sets** | Public (Table 1, 5) ও Commercial (Table 2); held-out-এর ফল দেওয়া হয়নি |
| **Models (Table 1)** | Claude Sonnet 4.5, Claude Sonnet 4, OpenAI GPT-5 (High), Claude Haiku 4.5, Kimi K2 Instruct, OpenAI GPT-OSS 120B |
| **Models (Table 2, commercial)** | Claude Opus 4.1, GPT-5 (High), GPT-5 (Medium), Gemini 2.5 Pro Preview, Claude Sonnet 4, GPT-4o |
| **Models (Table 5, 2 USD cap)** | GPT-5 (High), GPT-5 (Medium), Claude Opus 4.1, Claude Sonnet 4, GPT-OSS 20B, Gemini 2.5 Pro Preview, SWE-Smith-32B, GPT-4o, Qwen-3 32B |
| **Scaffold** | SWE-agent, default prompt, সর্বোচ্চ 50 turn |
| **Analysis budget** | 50 turn + 2 USD cost |
| **Judge** | GPT-5, শেষ 20 turn |
| **Hardware (open models)** | vLLM, 1 node × 8 H100 |

**সহজ কথায়:** সব model একই কাঠামো, একই prompt, একই ধাপ-সীমায় চালানো হয়েছে। Open model-গুলো নিজেদের GPU-তে চালানো, বাকিগুলো API দিয়ে।

### ৭.১ Dataset Statistics (Public set; Figure 1, Figure 2, Section 1)
| Attribute | মান | উৎস |
|---|---|---|
| Gold patch: lines (mean) | **107.4** | Section 1, Figure 1 |
| Gold patch: lines (median) | **55.0** | Figure 1 |
| Gold patch: files (mean) | **4.1** | Section 1 |
| সর্বনিম্ন পরিবর্তন | 10 line | Section 1 |
| 100 line-এর বেশি task | 100-এর বেশি | Section 1 |
| Task/repo | 50–100 (cap 100) | Section 1 |
| তুলনা: SWE-Bench Verified lines (mean / median) | 11.6 / 4.5 | Figure 1 |
| তুলনা: Verified-এ 1–2 line task | 161 / 500 | Section 1 |

**সহজ কথায়:** Pro-র গড় patch Verified-এর প্রায় 9 গুণ বড় (107.4 line বনাম 11.6 line)। এটাই "long-horizon" (লম্বা কাজ) বলার মূল কারণ।

### ৭.২ Figure 1 — Repo-ভিত্তিক Task সংখ্যা (আনুমানিক, bar chart থেকে)
| Public repo | আনুমানিক task | Language (Figure 3 label) |
|---|---|---|
| ansible | ≈105 | Python |
| openlibrary | ≈100 | Python |
| teleport | ≈88 | Go |
| flipt | ≈87 | Go |
| qutebrowser | ≈86 | Python |
| webclients | ≈73 | JS |
| tutanota | ≈68 | TS |
| vuls | ≈63 | Go |
| navidrome | ≈60 | Go |
| element-web | ≈55 | JS |
| NodeBB | ≈48 | JS |

**সহজ কথায়:** Pro-তে task মোটামুটি সমানভাবে ছড়ানো। Verified-এ একা django-ই ছিল প্রায় অর্ধেক।

Verified-এর দিকে (একই Figure-এ) django একাই ≈230 task, তারপর sympy ≈75 — অর্থাৎ Verified এক repo-তে অনেক বেশি কেন্দ্রীভূত; Pro অনেক সমান।

**আমার পর্যবেক্ষণ (গুরুত্বপূর্ণ — spot-check করার মতো):**
- Figure 1-এর repo bar-গুলো যোগ করলে ≈830, LOC histogram-এর bar যোগ করলে ≈845, আর Figure 2-এর file-count bar যোগ করলে ≈845 — কিন্তু public set 731। অর্থাৎ figure-গুলো সম্ভবত public set-এর **আগের/বড় version**-এর data দিয়ে আঁকা (আমার অনুমান; paper ব্যাখ্যা দেয়নি)।
- ansible-এর bar 100-এর gridline-এর একটু উপরে দেখায়, যা "strict cap of 100"-এর সাথে পুরো মেলে না (চোখে পড়া মান, তাই নিশ্চিত নই)।
- Language অনুযায়ী (আনুমানিক): Python ≈291, Go ≈298, JS ≈176, TS ≈68 — TS-এ মাত্র একটা repo।

### ৭.৩ Figure 2 — File সংখ্যা ও Task Type (আনুমানিক)
| পরিবর্তিত file | আনুমানিক task |
|---|---|
| 1 | ≈187 |
| 2 | ≈170 |
| 3 | ≈118 |
| 4 | ≈87 |
| 5–9 | ≈241 |
| 10–19 | ≈35 |
| 20+ | ≈7 |

**সহজ কথায়:** অনেক task-এ এক-দুটো file বদলাতে হয়, আবার কিছু task-এ বিশের বেশি। তাই "multi-file" একটা প্রবণতা, কঠোর নিয়ম নয়।

- **Task type (Figure 2 ডান):** 32টা label (bug/feat/enh-এর বিভিন্ন রূপ)। সবচেয়ে বড়: core_feat (≈225), code_quality_enh (≈215), refactoring_enh (≈160), major_bug (≈150), integration_feat (≈110), edge_case_bug (≈105)। Security-সংক্রান্ত label (security_feat, security_enh, security_bug) তুলনামূলক ছোট।
- **আমার পর্যবেক্ষণ:** Task-type bar-গুলো যোগ করলে ≈1,950, যা task সংখ্যার অনেক বেশি → এক task-এর একাধিক label (multi-label), গড়ে ২-এর বেশি। Paper এটা বলেনি; label কে দিয়েছে (মানুষ না LLM) তাও নেই।
- **আমার পর্যবেক্ষণ — contradiction:** Authors বলছেন "we require edits to span multiple files" ও "retain only problems requiring substantial, multi-file modifications", কিন্তু Figure 2 অনুযায়ী ≈187টা task (≈22%) **single-file**। তাই "multi-file" একটা প্রবণতা, কঠোর filter নয়।

---

## ৮. Results — মূল ফলাফল

### ৮.১ Public Set (Table 1, N = 731, SWE-agent, কোনো ambiguity ছাড়া)
| Model | Resolve (%) | আনুমানিক task (আমার হিসাব) |
|---|---|---|
| **Claude Sonnet 4.5** | **43.6** | ≈319 |
| Claude Sonnet 4 | 42.7 | ≈312 |
| OpenAI GPT-5 (High) | 41.8 | ≈306 |
| Claude Haiku 4.5 | 39.5 | ≈289 |
| Kimi K2 Instruct | 27.7 | ≈202 |
| OpenAI GPT-OSS 120B | 16.2 | ≈118 |

**সহজ কথায়:** সেরা model প্রায় 100টার মধ্যে 44টা পারে। সবচেয়ে দুর্বল open model পারে 16টা। আর শীর্ষ তিনটা model-এর পার্থক্য এত ছোট যে সেটা কাকতালীয়ও হতে পারে।

Abstract: "below 45% (Pass@1)"।

**আমার পর্যবেক্ষণ:** Table 1-এ Claude Sonnet 4.5 ও Haiku 4.5 আছে, অথচ setting-এ লেখা "latest versions as of September 18th, 2025"। আমার জানা মতে এই দুই model ঐ তারিখের পরে এসেছে — তাই v2-তে Table 1 update করা হয়েছে, কিন্তু setting-এর তারিখ বদলানো হয়নি বলে মনে হয়। Conclusion-এ এখনো লেখা "Opus 4.1 ও GPT-5 ≈23%" — যা Table 5 (budget-সীমিত) setting-এর সংখ্যা।

### ৮.২ Public Set — Budget-সীমিত (Table 5, Appendix; 50 turn + 2 USD)
| Model | Resolve (%) | আনুমানিক task (আমার হিসাব) |
|---|---|---|
| **OpenAI GPT-5 (High)** | **25.9** | ≈189 |
| OpenAI GPT-5 (Medium) | 23.3 | ≈170 |
| Claude Opus 4.1 | 22.7 | ≈166 |
| Claude Sonnet 4 | 17.6 | ≈129 |
| OpenAI GPT-OSS 20B | 16.2 | ≈118 |
| Gemini 2.5 Pro Preview | 13.5 | ≈99 |
| SWE-Smith-32B | 6.8 | ≈50 |
| OpenAI GPT-4o | 4.9 | ≈36 |
| Qwen-3 32B | 3.4 | ≈25 |

**সহজ কথায়:** সীমা (50 ধাপ, 2 USD) থাকলে সংখ্যা অনেক কমে যায়। সেরা এখানে 25.9%। একই model-এর দুই table-এ আলাদা সংখ্যা, তাই score দেখলে সবসময় জিজ্ঞেস করতে হবে: সীমা কী ছিল?

**আমার পর্যবেক্ষণ:**
- Claude Sonnet 4: Table 1-এ 42.7%, Table 5-এ 17.6% — একই benchmark-এ 25.1 pp পার্থক্য। GPT-5 (High): 41.8% বনাম 25.9%।
- Table 1-এ GPT-OSS **120B** = 16.2%, Table 5-এ GPT-OSS **20B** = 16.2% — হুবহু একই সংখ্যা দুটো আলাদা model-এর জন্য; typo নাকি কাকতালীয়, paper থেকে বোঝা যায় না।

### ৮.৩ Commercial Set (Table 2, N = 276) ও Public-এর সাথে তুলনা
| Model | Commercial (Table 2) | Public, 2 USD (Table 5) | Gap (pp) | Relative drop | z | p (two-sided) |
|---|---|---|---|---|---|---|
| Claude Opus 4.1 | **17.8** | 22.7 | 4.9 | 21.6% | 1.69 | 0.091 |
| OpenAI GPT-5 (High) | 15.7 | **25.9** | 10.2 | 39.4% | 3.43 | 0.0006 |
| OpenAI GPT-5 (Medium) | 14.9 | 23.3 | 8.4 | 36.1% | 2.92 | 0.0035 |
| Gemini 2.5 Pro Preview | 10.1 | 13.5 | 3.4 | 25.2% | 1.45 | 0.147 |
| Claude Sonnet 4 | 9.1 | 17.6 | 8.5 | 48.3% | 3.34 | 0.0008 |
| OpenAI GPT-4o | 3.6 | 4.9 | 1.3 | 26.5% | 0.88 | 0.377 |

(প্রথম দুই সংখ্যার column paper-এর; বাকি column **আমার হিসাব**, Section ৬.১০-এর সূত্রে।)

**সহজ কথায়:** Startup-এর private code-এ প্রায় সব model-এর score কমেছে। কিন্তু কমার পরিমাণ সবার সমান নয়। আর কিছু model-এর কমা এত ছোট যে সেটা কাকতালীয়ও হতে পারে (p বড় হলে এমন হয়)।

- **Authors:** best model commercial set-এ 20%-এর কম — enterprise codebase navigate করা কঠিন।
- **আমার পর্যবেক্ষণ:**
  1. সব model-এর commercial score কম, কিন্তু gap সমান নয়: Sonnet 4-এর relative drop 48.3%, Opus 4.1-এর 21.6%।
  2. **Ranking বদলায়:** public-এ GPT-5 (High) শীর্ষে, commercial-এ Opus 4.1 শীর্ষে। তবে commercial-এ দুইয়ের CI overlap করে (Section ৬.৯)।
  3. Opus 4.1, Gemini ও GPT-4o-এর gap 5% level-এ significant নয়।
  4. **Confound:** Commercial gap-এর কারণ (ক) contamination-এর অনুপস্থিতি, (খ) enterprise code-এর আসল কাঠিন্য, (গ) ভিন্ন repo/language mix, (ঘ) ছোট sample — এগুলো আলাদা করা হয়নি। তাই "public score contamination-এ ফোলা" — এমন সিদ্ধান্ত এই data থেকে টানা যায় না।

### ৮.৪ Language অনুযায়ী (Figure 3 নিচে-বামে; আনুমানিক, bar chart থেকে)
| Model | JS | Go | TS | Python |
|---|---|---|---|---|
| Qwen 3 32B | ≈3 | ≈3 | ≈1.5 | ≈6 |
| GPT-4o | ≈5 | ≈2 | ≈1.5 | ≈7 |
| SWE-Smith 32B | ≈7 | ≈3 | ≈3 | ≈13 |
| Gemini 2.5 Pro Preview | ≈12 | ≈8 | ≈6 | ≈18 |
| GPT-5 | ≈30 | ≈17 | ≈28 | ≈33 |
| Claude Sonnet 4 | ≈15 | ≈14 | ≈12 | ≈27 |
| Claude Opus 4.1 | ≈24 | ≈18.5 | ≈32 | ≈32 |

**সহজ কথায়:** Python-এ সব model সবচেয়ে ভালো। Go অনেক model-এর জন্য কঠিন। আর TypeScript-এ একটাই repo, তাই সেটা থেকে বড় সিদ্ধান্ত নেওয়া ঠিক নয়।

- **Authors:** "Go and Python generally show higher resolve rates"; JS/TS-এ variable (প্রায় 0% থেকে 30%-এর বেশি)। Caption: "models currently perform better at Python"।
- **আমার পর্যবেক্ষণ — text ও figure-এর অমিল:** Figure অনুযায়ী Python সত্যিই সবচেয়ে ভালো, কিন্তু **Go** frontier model-দের জন্য (GPT-5, Opus 4.1) **সবচেয়ে খারাপ বা প্রায় সবচেয়ে খারাপ** language (≈17–18.5%), JS ও TS-এর চেয়ে কম। তাই "Go-তে বেশি" দাবিটা figure-এর সাথে মেলে না।
- TS-এ শুধু একটা repo (tutanota) — তাই "TS-এর performance" আসলে "tutanota-র performance"; ছোট model-দের TS-এ ≈1.4% মানে আনুমানিক মাত্র 1টা task (আমার অনুমান: $1/68 \approx 1.5\%$)।

### ৮.৫ Repository অনুযায়ী (Figure 3 নিচে-ডানে; আনুমানিক)
| Repo (Language) | GPT-5 | Opus 4.1 | Sonnet 4 | Gemini 2.5 | ছোট model-দের পরিসর |
|---|---|---|---|---|---|
| ansible (Python) | ≈31 | ≈30 | ≈26 | ≈21 | ≈8–10 |
| openlibrary (Python) | ≈28 | ≈27 | ≈19 | ≈14 | ≈3–13 |
| qutebrowser (Python) | ≈40 | ≈41 | ≈37 | ≈18 | ≈5–17 |
| flipt (Go) | ≈18 | ≈15 | ≈16 | ≈12 | ≈2–3 |
| tutanota (TS) | ≈28 | ≈32 | ≈12 | ≈6 | ≈1–3 |
| vuls (Go) | ≈20 | ≈18 | ≈14 | ≈5 | ≈2–5 |
| navidrome (Go) | ≈18 | ≈25 | ≈15 | ≈12 | ≈0–6 |
| teleport (Go) | ≈11 | ≈18 | ≈7 | ≈4.5 | ≈0–4 |
| element-web (JS) | ≈20 | ≈16 | ≈13 | ≈3.5 | ≈0–3.5 |
| NodeBB (JS) | ≈30 | ≈32 | ≈14 | ≈12 | ≈4–12 |
| webclients (JS) | **≈54** | ≈24 | ≈26 | ≈19 | ≈5 |

**সহজ কথায়:** একই language-এর ভেতরেও repo-ভেদে বিশাল পার্থক্য। মানে language-এর চেয়ে কোন project সেটাই বেশি গুরুত্বপূর্ণ হতে পারে।

- **Authors:** কিছু repo-তে সব model-এর resolve rate 10%-এর নিচে; অন্য কিছুতে কিছু model 50%-এর বেশি পায়। Repo-specific factor (codebase complexity, documentation, problem type) গুরুত্বপূর্ণ।
- **আমার পর্যবেক্ষণ:** 50%-এর বেশি — webclients-এ GPT-5 (≈54%) — figure-এ দেখা যায় ✓। কিন্তু "সব model 10%-এর নিচে" এমন কোনো repo figure-এ আমি খুঁজে পাইনি — সবচেয়ে কঠিন teleport-এও GPT-5 ≈11% আর Opus ≈18%। সম্ভবত authors ছোট model-দের কথা বা গড় বুঝিয়েছেন।
- একই language-এর ভেতরেও বিশাল পার্থক্য: JS-এ webclients (GPT-5 ≈54%) বনাম element-web (≈20%) → language-এর চেয়ে **repo** বড় factor হতে পারে।

### ৮.৬ File সংখ্যা ও Patch Size অনুযায়ী (Figure 3 উপরে; আনুমানিক)
**File সংখ্যা:**
| Files | Qwen3 32B | GPT-4o | SWE-Smith | Gemini 2.5 | GPT-5 | Sonnet 4 | Opus 4.1 |
|---|---|---|---|---|---|---|---|
| 1 | ≈9 | ≈6 | ≈10.5 | ≈15.5 | ≈31 | ≈28 | ≈36 |
| 2 | ≈0 | ≈5.5 | ≈10 | ≈11.5 | ≈34 | ≈24 | ≈29 |
| 3 | ≈3 | ≈5.5 | ≈7 | ≈13 | ≈30 | ≈25.5 | ≈28 |
| 4 | ≈3 | ≈4 | ≈5.5 | ≈10.5 | ≈20.5 | ≈14 | ≈25 |
| 5–9 | ≈3 | ≈2.5 | ≈5 | ≈11 | ≈17 | ≈8 | ≈15.5 |
| 10+ | ≈11 | ≈5 | ≈5 | ≈7.5 | ≈26 | ≈5 | ≈17.5 |

**সহজ কথায়:** File বাড়লে score সাধারণত কমে। কিন্তু 10+ file-এর task খুব কম, তাই সংখ্যাগুলো এলোমেলো।

**Lines of code:**
| LOC | Qwen3 32B | GPT-4o | SWE-Smith | Gemini 2.5 | GPT-5 | Sonnet 4 | Opus 4.1 |
|---|---|---|---|---|---|---|---|
| 11–25 | ≈3 | ≈6.5 | ≈15 | ≈18.5 | ≈45 | ≈36 | ≈47 |
| 26–50 | ≈8 | ≈9 | ≈11 | ≈19 | ≈34.5 | ≈28 | ≈35 |
| 51–100 | ≈2 | ≈1 | ≈5 | ≈10 | ≈19 | ≈12 | ≈21 |
| 101–500 | ≈1 | ≈1 | ≈2 | ≈3.5 | ≈12.5 | ≈4.5 | ≈10.5 |
| 500+ | 0 | 0 | 0 | ≈4 | ≈12.5 | ≈6 | ≈0 |

**সহজ কথায়:** Patch যত বড়, score তত কম। এটাই paper-এর সবচেয়ে পরিষ্কার প্রমাণ যে বড় কাজ AI-র জন্য কঠিন।

- **Authors:** single-file-এ performance তুলনামূলক stable, file বাড়লে তীব্র পতন; 3 file-এর পরে frontier ও ছোট model-এর gap অনেক বাড়ে; Opus 4.1 ও GPT-5 10+ file-এও 10%-এর বেশি, open-source alternative প্রায় শূন্যের কাছে। Caption: 10+ file ও 500+ LOC category-তে মাত্র 20–30টা example, তাই variance বেশি।
- **আমার পর্যবেক্ষণ:**
  1. **LOC-এর সাথে পতন খুব পরিষ্কার ও monotonic:** Opus 4.1 ≈47% (11–25 line) → ≈10.5% (101–500 line) — প্রায় সাড়ে চার ভাগের এক ভাগ। এটাই paper-এর সবচেয়ে শক্ত "long-horizon কঠিন" প্রমাণ।
  2. File সংখ্যার সাথে পতন ততটা monotonic নয় — GPT-5 10+ file-এ (≈26%) 5–9 file-এর (≈17%) চেয়ে বেশি; ছোট sample-এর noise।
  3. Qwen3 32B 10+ file-এ ≈11% — "open-source প্রায় শূন্য" দাবির সাথে মেলে না (ছোট sample, তাই সম্ভবত noise)।

### ৮.৭ Human Augmentation Ablation (Table 3)
| Model | Problem statement + Requirements + Interface | Problem statement only |
|---|---|---|
| OpenAI GPT-5 (High) | **25.9%** | 8.40% |
| Claude Opus 4.1 | **22.7%** | 8.20% |

**সহজ কথায়:** নির্দেশ খুলে নিলে score প্রায় তিন ভাগের এক ভাগ হয়ে যায়। কিন্তু এখানে দুটো কারণ মেশানো: test-এর কড়াকড়ি আর কাজ সহজ হওয়া।

- **Authors:** augmentation ছাড়া দুটো model-ই "significantly degraded"; agent কম constrained থাকে, বিশেষ করে feature addition-এ বিভিন্ন রকম solution দেয়; unit test একটা সরু solution set আশা করে → verifier-এর false negative → কম pass rate। Augmentation solution space সীমিত করে verifier-কে robust করে।
- **আমার হিসাব:** score প্রায় **3 গুণ** (3.08×, 2.77×) বাড়ে; শূন্য-augmentation-এ দুই model প্রায় সমান (8.4 বনাম 8.2)।
- **আমার পর্যবেক্ষণ:** ablation-এ requirements আর interface **একসাথে** সরানো হয়েছে — কোনটার অবদান কত, আলাদা করা যায় না। এটা মাত্র দুটো model-এ করা।

### ৮.৮ Failure Mode Analysis (Table 4, public set, GPT-5 judge)
| Model | Submitted | Not-submitted | Wrong Sol. | Syntax Err. | Incorrect File | Instr. Following | Edge Case | Other | Tool-Use | Long-Context | Stuck in Loop |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Claude Opus 4.1 | 74.2% (511) | 25.8% (178) | 50.3% (257) | 31.3% (160) | 4.9% (25) | 2.7% (14) | 0.8% (4) | 10.0% (51) | 68.0% (121) | 28.7% (51) | 3.4% (6) |
| GPT-5 (High) | 27.2% (147) | 72.8% (394) | 39.5% (58) | 29.3% (43) | 8.8% (13) | 4.8% (7) | 0.0% (0) | 17.7% (26) | 96.4% (380) | 2.5% (10) | 1.0% (4) |
| Claude Sonnet 4 | 44.1% (235) | 55.9% (298) | 25.5% (60) | 7.7% (18) | 2.1% (5) | 2.1% (5) | 0.0% (0) | 62.6% (147) | 8.7% (26) | 57.4% (171) | 33.9% (101) |
| Gemini 2.5 Pro Preview | 52.9% (377) | 47.1% (335) | 35.0% (132) | 56.5% (213) | 4.0% (15) | 1.9% (7) | 0.0% (0) | 2.7% (10) | 83.6% (280) | 14.3% (48) | 2.1% (7) |
| GPT-4o | 72.1% (569) | 27.9% (220) | 45.2% (257) | 36.7% (209) | 11.2% (64) | 6.2% (35) | 0.0% (0) | 0.7% (4) | 100.0% (220) | 0.0% (0) | 0.0% (0) |
| Qwen3 32B | 47.3% (304) | 52.7% (339) | 25.0% (76) | 48.7% (148) | 19.7% (60) | 1.6% (5) | 0.7% (2) | 4.3% (13) | 78.8% (267) | 1.5% (5) | 19.8% (67) |

**সহজ কথায়:** প্রতিটা model আলাদা ধরনে ব্যর্থ হয়। কেউ ভুল উত্তর দেয় (Opus), কেউ tool ঠিকমতো চালাতে পারে না (GPT-5), কেউ context ভরে গিয়ে আটকে যায় (Sonnet 4)। একই সংখ্যা দেখে একই কারণ ধরে নেওয়া যাবে না।

(Wrong Solution থেকে Other পর্যন্ত % **submitted-এর ভেতরে**; Tool-Use, Long-Context, Stuck in Loop % **not-submitted-এর ভেতরে**। Bracket-এ count।)

**পুরো failure-এর মধ্যে share (আমার হিসাব, Section ৬.১২-এর সূত্রে):**
| Model | মোট failure | Wrong Sol. | Syntax | Tool-Use | Long-Context | Stuck | Other |
|---|---|---|---|---|---|---|---|
| Claude Opus 4.1 | 689 | 37.3% | 23.2% | 17.6% | 7.4% | 0.9% | 7.4% |
| GPT-5 (High) | 541 | 10.7% | 7.9% | **70.2%** | 1.8% | 0.7% | 4.8% |
| Claude Sonnet 4 | 533 | 11.3% | 3.4% | 4.9% | **32.1%** | 18.9% | 27.6% |
| Gemini 2.5 Pro Preview | 712 | 18.5% | 29.9% | **39.3%** | 6.7% | 1.0% | 1.4% |
| GPT-4o | 789 | 32.6% | 26.5% | 27.9% | 0.0% | 0.0% | 0.5% |
| Qwen3 32B | 643 | 11.8% | 23.0% | **41.5%** | 0.8% | 10.4% | 2.0% |

**সহজ কথায়:** পুরো ব্যর্থতার ভেতরে ভাগ দেখলে আরও পরিষ্কার: GPT-5-এর ব্যর্থতার 70% tool-use, মানে তার উত্তর ভুল ছিল না, সে কাঠামোটা ঠিকমতো চালাতে পারেনি। এটা scaffold-নির্ভরতার ইঙ্গিত।

**Authors-এর ব্যাখ্যা:**
- Opus 4.1: মূলত semantic understanding-এ ব্যর্থ — wrong solution 35.9%, syntax error 24.2% (text-এর সংখ্যা) → technical execution ভালো, কিন্তু problem comprehension ও algorithmic correctness-এ সমস্যা।
- GPT-5: effective tool-use-এ পার্থক্য থাকতে পারে, কিন্তু wrong solution কম।
- Sonnet 4: primary failure context overflow (35.6%), আর উল্লেখযোগ্য endless file reading (17.0%) → context management ও file navigation-এর সীমা।
- Gemini 2.5: তুলনামূলক balanced — tool error 38.8%, syntax 30.5%, wrong solution 18.0%।
- Qwen3 32B: সবচেয়ে বেশি tool error (42.0%) → integrated tool-use গুরুত্বপূর্ণ।
- Caption: top LLM (Opus 4.1, GPT-5) শক্তিশালী agent কিন্তু high-complexity task-এ solution বানাতে সমস্যা; দুর্বল/ছোট open-source model syntax, formatting ও tool-use-এ সমস্যায় পড়ে।

**আমার পর্যবেক্ষণ (spot-check করার মতো):**
1. **Text-এর % আর Table-এর % মেলে না।** Opus-এর wrong solution: text 35.9%, table থেকে overall 37.3% (submitted-এর ভেতরে 50.3%)। Sonnet 4-এর context overflow: text 35.6%, table থেকে 32.1% (not-submitted-এর ভেতরে 57.4%)। Gemini: text 38.8/30.5/18.0, table থেকে 39.3/29.9/18.5। Qwen3: text 42.0, table থেকে 41.5। পার্থক্য ছোট কিন্তু ধারাবাহিক — সম্ভবত text আগের কোনো run-এর।
2. **Failure count-এর যোগফল 731-এর সাথে মেলে না।** GPT-4o-এর মোট failure 789 > 731 (public set-এর মোট task)! Table 5 অনুযায়ী unresolved হওয়ার কথা: Opus ≈565 (table-এ 689), Sonnet 4 ≈602 (533), Gemini ≈632 (712), Qwen3 ≈706 (643)। শুধু GPT-5 (541 বনাম ≈542) মেলে। অর্থাৎ Table 4-এর denominator অস্পষ্ট — হয়তো ভিন্ন run, ভিন্ন version-এর dataset (Section ৭.২-এ figure-এর ≈845-এর মতো), বা একাধিক trajectory। **Table 4-এর শতাংশ পড়ার সময় এই সতর্কতা রাখতে হবে।**
3. **GPT-5-এর ব্যর্থতার 70% tool-use, not-submitted।** শীর্ষ model-এর ব্যর্থতার বেশিরভাগ "সমাধান ভুল" নয়, বরং SWE-agent scaffold-এর tool ঠিকমতো ব্যবহার করতে না পারা। এটা model-scaffold fit-এর প্রশ্ন তোলে — অন্য scaffold-এ GPT-5-এর score অনেক আলাদা হতে পারে (CG8)।
4. **Judge ও judged একই model।** GPT-5 নিজের trajectory-ও judge করেছে — self-preference bias-এর ঝুঁকি; paper আলোচনা করেনি।
5. **Edge Case প্রায় সব model-এ 0%** — হয় category-টা judge কম বেছে নেয়, নয়তো "Wrong Solution"-এর সাথে মিশে যায়। Category-গুলোর সীমানা অস্পষ্ট।

---

## ৯. Key Findings / Insights (Supervisor-কে বলার মতো ৮টা পয়েন্ট)

1. **কঠিন task-এ বড় পতন:** SWE-agent দিয়ে public set-এ সেরা 43.6% (Table 1); budget-সীমিত setting-এ সেরা 25.9% (Table 5); authors-এর মতে Verified-এ একই ধরনের model 70%-এর বেশি পায়।
2. **Enterprise code আরও কঠিন:** Commercial set-এ সেরা 17.8% (Opus 4.1); GPT-5 (High), GPT-5 (Medium), Sonnet 4-এর পতন statistically significant (আমার হিসাব)।
3. **Patch size বাড়লে performance তীব্রভাবে কমে:** Opus 4.1 ≈47% (11–25 line) থেকে ≈10.5% (101–500 line) — আনুমানিক, Figure 3।
4. **Language ও repo দুটোই গুরুত্বপূর্ণ:** Python-এ সবচেয়ে ভালো; একই language-এ repo-ভেদে বিশাল পার্থক্য (JS: ≈54% বনাম ≈20%)।
5. **Task description-এর মান score-কে ~3 গুণ বদলায়:** requirements + interface ছাড়া GPT-5 25.9% → 8.4%। অর্থাৎ benchmark score-এর বড় অংশ "spec কতটা পরিষ্কার" তার উপর নির্ভর করে।
6. **Test verifier-এর false negative একটা বাস্তব সমস্যা** — authors স্বীকার করেন unit test সরু solution set আশা করে।
7. **Failure-এর ধরন model-ভেদে আলাদা:** Opus — ভুল solution; GPT-5 — tool-use; Sonnet 4 — context overflow ও loop; ছোট model — syntax ও tool। তাই একটা assurance layer-কে বিভিন্ন ধরনের failure ধরতে হবে।
8. **Scaffold ও budget-ই অর্ধেক গল্প:** Agentless multi-file-এ পারে না বলে বাদ; একই model-এর Table 1 বনাম Table 5-এ 16–25 pp পার্থক্য।

**সহজ কথায়:** আটটা পয়েন্টের সারকথা: কাজ বড় হলে AI দুর্বল, নির্দেশ অস্পষ্ট হলে আরও দুর্বল, আর score এত নির্ভর করে সীমা আর কাঠামোর উপর যে একটা সংখ্যা দেখে সিদ্ধান্ত নেওয়া ঝুঁকিপূর্ণ।

---

## ১০. কেন এই Solution অন্যগুলোর থেকে ভালো?

| বৈশিষ্ট্য | SWE-bench (full) | SWE-bench Verified | **SWE-Bench Pro** |
|---|---|---|---|
| Task সংখ্যা | 2,294 | 500 | **1,865** (public 731) |
| Repository | 12 | (SWE-bench-এর subset) | **41** |
| Language | Python | Python | **Python, Go, JS, TS** |
| Repo concentration | django ≈37% (Paper 01) | django ≈230/500 (Figure 1, আনুমানিক) | প্রতি repo 50–100 cap (public) |
| Patch size (lines) | mean 32.8 (Paper 01, Table 1) | mean 11.6, median 4.5 | **mean 107.4, median 55.0** |
| Files | mean 1.7 | — | **mean 4.1** |
| Trivial task | অনেক | 161/500 এক-দুই line | ≥10 line বাধ্যতামূলক |
| Task description | আসল issue | আসল issue (underspecified বাদ) | **মানুষের লেখা issue + requirements + interface** |
| Test যাচাই | Automatic | মানুষ | **Flaky-check (automatic) + মানুষ** |
| Contamination defence | নতুন PR দিয়ে refresh সম্ভব | নেই বিশেষ | **GPL repo + private commercial + held-out** |
| Enterprise code | না | না | **হ্যাঁ (18টা startup repo)** |
| Failure analysis | Patch তুলনা | — | **Trajectory-level LLM judge** |

**সহজ কথায়:** SWE-bench ছিল ছোট, শুধু Python, আর একটা repo-র আধিপত্য ছিল। Pro বড়, চার language-এর, বেশি repo-র, আর task-এর বর্ণনা মানুষ দিয়ে পরিষ্কার করা।

**মূল শক্তি:**
1. **Realism:** feature, refactoring, enhancement — শুধু bug fix নয়; enterprise code-ও।
2. **Diversity:** ৪টা language, 41টা repo, repo cap।
3. **Resolvability:** মানুষের augmentation-এর ফলে "অসম্ভব task" কম (Agentless-এর underspecified issue সমস্যা)।
4. **Contamination-এর বিরুদ্ধে layered defence:** আইনি (GPL) + access (private) + monitoring (held-out)।
5. **Reproducibility:** Docker image।
6. **Diagnostic depth:** language/repo/file/LOC breakdown + failure mode।

---

## ১১. কোন পরিস্থিতিতে এই paper/benchmark ভালো কাজ করে, কোথায় করে না

### ✅ ভালো কাজ করে যখন:
- Frontier agent-দের মধ্যে পার্থক্য করতে চাও — Verified saturated হয়ে গেলে।
- **Multi-file, বড় patch**-এ agent-এর ক্ষমতা মাপতে চাও।
- **Multi-language** (Python, Go, JS, TS) generalisation দেখতে চাও।
- Spec (requirements/interface) দেওয়া থাকলে agent কতটা ঠিকভাবে **implement** করতে পারে, তা মাপতে চাও।
- Failure-এর কারণ ভাগ করে বুঝতে চাও (trajectory analysis)।

### ❌ ভালো কাজ করে না / সীমিত যখন:
- **Ambiguity resolution বা issue understanding** মাপতে চাও — default setting-এ সব spec দেওয়া; "problem statement only" setting-এর data মাত্র দুটো model-এ।
- **Localization ক্ষমতা** আলাদা করে মাপতে চাও — requirements/interface প্রায়ই file path ও function নাম বলে দেয়।
- **Java, C++, Rust** — নেই বা কম (authors-এর স্বীকারোক্তি)।
- **Patch correctness test-এর বাইরে** — false positive (plausible-but-wrong) মাপা হয় না।
- **Run-to-run reliability** — একবার run, variance নেই।
- **Security, maintainability** — মাপা হয় না (authors future work-এ রেখেছেন)।
- **Commercial set-এ নিজের agent চালাতে চাইলে** — সম্ভব নয়, শুধু Scale AI-এর report করা ফল।
- **TypeScript-এর সাধারণ সিদ্ধান্ত** — মাত্র একটা TS repo।

**সহজ কথায়:** Benchmark-টা ভালো হলো বড় আর কঠিন কাজে AI-দের তুলনা করতে। কিন্তু অস্পষ্ট নির্দেশ বোঝা, ভুল patch ধরা বা নির্ভরযোগ্যতা মাপার জন্য এটা যথেষ্ট নয়।

---

## ১২. Limitations — দুর্বলতা

### ১২.১ Authors যা নিজেরা স্বীকার করেছেন (Section 7)
1. **Limited language coverage:** Python, JS, TS, Go আছে, কিন্তু distribution সমান নয়; Java, C++, Rust underrepresented।
2. **Dependency on test suite:** fail2pass ও pass2pass-এর উপর নির্ভরতা; বাস্তবে অনেক সঠিক solution থাকতে পারে যেগুলো মূল test pass করে না। আদর্শভাবে এমন verifier দরকার যা যেকোনো valid solution যাচাই করতে পারে।
3. **Future work:** test-এর বাইরে evaluation — rubric, code quality, **security analysis**, performance, best practice, maintainability/readability/architecture-এর human evaluation; multi-agent ও human-agent collaboration (code review, merge conflict, distributed workflow)।
4. (Section 3.1-এ) বাস্তব task underspecified হতে পারে, আর requirements ছাড়া setting-টাও আকর্ষণীয় — অর্থাৎ তারা স্বীকার করেন default setting বাস্তবের চেয়ে বেশি spec দেয়।

**সহজ কথায়:** Authors নিজেরাই বলেছেন: শুধু test-এর উপর নির্ভর করা সীমাবদ্ধতা, language কম, আর security-র মতো জিনিস মাপা হয়নি।

### ১২.২ আমার Critical Analysis (Professor-level observation)
1. **Contamination-resistance দাবি করা হয়েছে, মাপা হয়নি (CG6-এর জন্য সবচেয়ে গুরুত্বপূর্ণ):**
   - GPL code public GitHub-এ আছে; GPL training-এ ব্যবহার আইনত নিষিদ্ধ কিনা সেটাই অমীমাংসিত প্রশ্ন বলে আমার ধারণা — তাই "legal barrier" একটা নীতিগত অনুমান। Open-weight model-এর ক্ষেত্রে এই বাধা আরও দুর্বল হতে পারে।
   - Public set নিজেই এখন HuggingFace-এ — ভবিষ্যতের model-এর training data-তে ঢোকার ঝুঁকি আছে (সব static benchmark-এর সমস্যা)।
   - কোনো empirical contamination test নেই (যেমন memorisation probe, তারিখ-ভিত্তিক তুলনা, বা held-out-এর ফল)। Held-out set-এর কোনো ফল দেওয়া হয়নি।
   - Public বনাম commercial gap-কে contamination-এর প্রমাণ হিসেবে পড়া যায় না — repo, language, domain, sample size সব আলাদা (confounded)।
2. **Augmentation-এর দুই দিক (Agentless-এর underspecified সমস্যার সমাধান, কিন্তু মূল্য দিয়ে):**
   - Requirements "grounded on the unit tests" — test কী assert করবে তা প্রায় বলে দেয় (যেমন হুবহু error string)। ফলে benchmark "issue solving" থেকে সরে **"spec থেকে implementation"** মাপে।
   - Interface ও requirements file path ও function নাম বলে দেয় (Open Library উদাহরণে প্রতিটা requirement-এ file path আছে) → **localization**, যা Sub-domain 1-এর চারটা paper-এ মূল bottleneck ছিল, অনেকটা সহজ হয়ে যায়।
   - Authors-এর দাবি "requirements never leak solutions" — কিন্তু "leak" কতটা হয়েছে তা মাপার কোনো পদ্ধতি নেই।
3. **False negative-এ মনোযোগ, false positive উপেক্ষিত (CG1):** "Too broad" test বাদ দেওয়া false negative কমায়, কিন্তু test suite দুর্বলও করতে পারে → ভুল patch pass করার সুযোগ বাড়ে। কোনো resolved patch হাতে যাচাই করা হয়নি (AutoCodeRover যেমন 78টা যাচাই করে 65.4% সঠিক পেয়েছিল — Sub-domain 1)। প্রতি task-এ গড়ে কয়টা F2P/P2P test, তাও paper বলেনি।
4. **সংখ্যার অসংগতি (reproducibility সমস্যা):**
   - Table 4-এর failure count 731-এর বেশি (GPT-4o 789) এবং Table 5-এর সাথে মেলে না।
   - Text-এর failure % আর Table 4-এর % মেলে না।
   - Figure 1/2-এর bar-এর যোগফল ≈845, public set 731।
   - Language নিয়ে text ("Go higher") আর Figure 3 মেলে না।
   - "Multi-file required" বলা হলেও ≈22% task single-file।
   - GPT-OSS 120B (Table 1) ও GPT-OSS 20B (Table 5) দুটোই হুবহু 16.2%।
   - Setting-এ "September 18, 2025", কিন্তু Table 1-এ পরের model।
   এগুলো ছোট ছোট, কিন্তু একটা **benchmark** paper-এ — যার কাজই নির্ভরযোগ্য মাপ দেওয়া — এগুলো বিশ্বাসযোগ্যতা কমায়।
5. **Statistical rigor নেই (CG8):** কোনো CI, significance test বা একাধিক seed নেই। আমার হিসাবে Table 1-এর শীর্ষ তিনটা model-কে আলাদা করা যায় না (Section ৬.৯)।
6. **Run-to-run variance মাপা হয়নি (CG4):** Long-horizon, 50-turn agent run খুব non-deterministic হওয়ার কথা — অথচ একবার run।
7. **Score budget-নির্ভর:** Table 1 বনাম Table 5-এ একই model-এর 16–25 pp পার্থক্য, কিন্তু কোনো cost-vs-resolve curve নেই। মোট খরচ, token, সময়ও report করা হয়নি।
8. **Single scaffold:** শুধু SWE-agent-এর default prompt — GPT-5-এর 70% failure tool-use হওয়া ইঙ্গিত দেয় যে ranking scaffold-নির্ভর। Agentless-এর ফল সংখ্যায় দেওয়া হয়নি।
9. **LLM-judge validation দুর্বল:** নিজস্ব agreement সংখ্যা নেই; SWE-agent-এর 15-sample 87% cite করা; GPT-5 নিজেকে judge করেছে; শুধু শেষ 20 turn দেখে — শুরুর ভুল (যেমন ভুল plan) ধরা পড়ে না।
10. **Construction funnel ও annotator তথ্য নেই:** কতগুলো candidate থেকে শুরু, কত বাদ, কয়জন annotator, inter-annotator agreement — কিছুই নেই। মানুষের লেখা spec-এর মান যাচাইয়ের কোনো সংখ্যা নেই।
11. **Commercial set যাচাই-অযোগ্য:** বাইরের কেউ চালাতে পারে না; শুধু Scale AI-এর report-এর উপর আস্থা। Commercial set-এ 18 repo-তে মাত্র 276 task (≈15.3/repo) — repo cap নিয়ম এখানে খাটে না।
12. **Conflict of interest-এর প্রশ্ন (নিরপেক্ষভাবে):** Benchmark-এর মালিক একটা data/evaluation কোম্পানি, আর held-out ও commercial set শুধু তাদের হাতে — এটা অন্যায় কিছু নয়, কিন্তু স্বাধীন replication-এর সুযোগ কমায়।

**সহজ কথায়:** আমি যা খুঁজে পেয়েছি, তার সারকথা: contamination কমার দাবি প্রমাণিত নয়। নির্দেশ দেওয়ায় কাজ সহজ হয়েছে। কিছু সংখ্যা মেলে না। একবার চালানো, তাই ranking শক্ত নয়। আর judge-এর মান যাচাই করা হয়নি।

---

## ১৩. Research Gaps — কোথায় কাজ করার সুযোগ আছে

### ১৩.১ এই Paper থেকে Gap (আমাদের sub-domain folder-এর সাথে link)
| # | Gap | কেন গুরুত্বপূর্ণ | কোন sub-domain folder-এ আরও পড়তে হবে |
|---|---|---|---|
| G1 | **SWE-Bench Pro-র resolved patch-এর false positive rate** — বড়, multi-file patch-এ overfitting কত? | 107-line patch-এ test-এর বাইরে ভুল লুকানোর জায়গা বেশি | Patch Validation; Automated Program Repair |
| G2 | **Test augmentation for long-horizon tasks** — বাড়তি test দিয়ে false positive ধরা, কিন্তু interface-এর কারণে test লেখা সহজ | Interface দেওয়া থাকায় generated test সরাসরি function call করতে পারে | LLM Test Generation |
| G3 | **Verifier-এর false negative মাপা** — "problem statement only" setting-এর ব্যর্থ patch-এর মধ্যে কতগুলো আসলে সঠিক? | Authors দাবি করেছেন, মাপেননি | Patch Validation; Coding-Agent Evaluation & Reliability |
| G4 | **Run-to-run reliability (pass^k) long-horizon task-এ** | 50-turn trajectory-তে variance বেশি হওয়ার কথা | Coding-Agent Evaluation & Reliability |
| G5 | **বড় agent patch-এর security ও quality** | Authors নিজেরাই future work-এ রেখেছেন; Figure 2-এ security label আছে | Security of AI-Generated Code |
| G6 | **Multi-language APCA / correctness judge** — Python-এ বানানো judge কি Go/JS/TS-এ কাজ করে? | একই benchmark-এ ৪টা language → controlled cross-language experiment সম্ভব | Automated Program Repair (RePaCA); Patch Validation |
| G7 | **Empirical contamination audit** — public বনাম held-out বা memorisation probe | GPL defence শুধু অনুমান | Coding-Agent Evaluation & Reliability (SWE-rebench) |
| G8 | **Budget-aware ও scaffold-aware evaluation** — cost-vs-resolve curve, একাধিক scaffold | একই model-এ 16–25 pp পার্থক্য | Coding-Agent Evaluation & Reliability; AI Coding Agents |
| G9 | **Failure-mode-aware abstention** — trajectory signal (loop, context overflow, tool error) দেখে agent-এর patch-এ আস্থা কমানো | Not-submitted/loop-এ পড়া trajectory থেকে আসা patch সম্ভবত কম বিশ্বাসযোগ্য | Trustworthy AI for SE; AI Coding Agents |
| G10 | **Ambiguity-resolution benchmark** — requirements ছাড়া setting-কে আলাদা track হিসেবে | বাস্তবে spec কম থাকে | AI Coding Agents; Trustworthy AI for SE |

**সহজ কথায়:** Gap-গুলো মূলত তিন দিকে: patch আসলে ঠিক কিনা (G1, G3, G6), AI কতটা নির্ভরযোগ্য আর নিরাপদ (G4, G5, G9), আর benchmark নিজে কতটা ভালো (G7, G8, G10)।

### ১৩.২ আগের Sub-domain-এর Common Gap (CG1–CG10)-এর সাথে সম্পর্ক
| CG | Gap | SWE-Bench Pro কী করে | অবস্থা (আমার মূল্যায়ন) |
|---|---|---|---|
| CG1 | Plausible patch-এর correctness | Test মানুষ দিয়ে যাচাই, flaky বাদ — কিন্তু false positive মাপা হয়নি; resolved patch হাতে যাচাই নেই | **খোলা** — বরং বড় patch-এ সমস্যা আরও গুরুত্বপূর্ণ |
| CG2 | Candidate selection / re-ranking | Pass@1, একটা trajectory; কোনো selection নেই | **খোলা** |
| CG3 | Validation ও generated test-এর মান | Benchmark-এর test-এর মান বাড়িয়েছে (relevance, breadth, flakiness); agent-এর নিজের test নিয়ে কিছু নেই | **আংশিক** (benchmark দিকে উন্নতি; agent দিকে খোলা) |
| CG4 | Run-to-run reliability | একবার run, variance নেই | **খোলা** |
| CG5 | Security ও quality | মাপা হয়নি; authors future work-এ রেখেছেন | **খোলা** (authors-এর স্বীকৃতি দিয়ে শক্ত হলো) |
| CG6 | Benchmark quality ও contamination | Copyleft + private + held-out; trivial task বাদ; underspecification দূর; repo cap | **অনেকটা address করা** — কিন্তু contamination-resistance empirically প্রমাণিত নয় |
| CG7 | Confidence ও abstention | Submitted/not-submitted ভাগটা একটা প্রাকৃতিক abstention signal, কিন্তু ব্যবহার হয়নি | **খোলা** (নতুন signal পাওয়া গেল) |
| CG8 | Evaluation-এর সমতা ও statistical rigor | Unified scaffold ও prompt — ভালো; কিন্তু CI নেই, budget-নির্ভরতা, সংখ্যার অসংগতি | **আংশিক** — নতুন প্রমাণ: budget বদলালে 16–25 pp |
| CG9 | APCA-কে Python repo-level ও অন্য language-এ নেওয়া | ৪টা language-এ একই format-এর task ও Docker environment দেয় | **Test bed পাওয়া গেল** — সমাধান নয়, কিন্তু experiment করার জায়গা |
| CG10 | Assurance tool-এর evaluation validity | Repo-disjoint split (public/held-out/commercial) একটা ভালো মডেল: আমাদের detector-ও repo-disjoint split-এ যাচাই করা উচিত | **ধারণা পাওয়া গেল** |

**সহজ কথায়:** আগের sub-domain-এর অনেক খোলা gap এই paper বন্ধ করেনি। এটা শুধু একটা ভালো test bed দিয়েছে, বিশেষ করে CG6 আর CG9-এর জন্য।

**Agentless-এর "underspecified issue" সমস্যা (Sub-domain 1, Paper 04):** SWE-Bench Pro এটা সরাসরি সমাধান করেছে — বাদ না দিয়ে (Lite-S-এর মতো) বরং মানুষ দিয়ে **তথ্য যোগ করে**। কিন্তু এর দাম: বাস্তবের চেয়ে বেশি spec, আর localization সহজ।

### ১৩.৩ আমাদের Assurance Layer-এর জন্য SWE-Bench Pro কি Lite/Verified-এর চেয়ে ভালো Test Bed?
| মাপকাঠি | SWE-bench Lite / Verified | SWE-Bench Pro (public) | কোনটা ভালো |
|---|---|---|---|
| আগের কাজের সাথে তুলনা (Agentless, AutoCodeRover-এর patch, 65.4% ইত্যাদি) | অনেক public patch ও label | এখনো কম | Lite/Verified |
| Patch-এর জটিলতা (overfitting লুকানোর জায়গা) | ছোট patch (Verified median 4.5 line) | বড় (median 55 line, 4.1 file) | **Pro** |
| Multi-language (CG9) | শুধু Python | Python, Go, JS, TS | **Pro** |
| Contamination ঝুঁকি | বেশি | কম (দাবি অনুযায়ী) | **Pro** |
| Test-এর মান | Verified-এ মানুষ যাচাই | মানুষ + flaky-check | প্রায় সমান / Pro |
| Resolved patch-এর সংখ্যা (assurance-এর জন্য input) | বেশি (resolve rate উঁচু) | কম (≈25–44% × 731) | Lite/Verified |
| Infrastructure খরচ | পরিচিত harness | ৪ language-এর Docker image, বড় | Lite/Verified |
| Spec থাকায় generated test লেখা | কঠিন (interface অজানা) | সহজ (interface দেওয়া) | **Pro** (কিন্তু bias সাবধান) |

**সহজ কথায়:** দুটোর মধ্যে কোনটা "ভালো" তা নির্ভর করে কী করতে চাই তার উপর। আগের কাজের সাথে তুলনা করতে Verified সুবিধার, কিন্তু বড় patch আর অন্য language দেখতে Pro ভালো।

**আমার সিদ্ধান্ত:** একটা নয়, **দুটো একসাথে**। Verified/Lite — আগের কাজের সাথে তুলনা ও calibration-এর জন্য; SWE-Bench Pro public-এর একটা ছোট subset (যেমন Python-এর ৩টা repo দিয়ে শুরু, পরে একটা Go ও একটা JS repo) — generalisation ও CG9-এর জন্য। এভাবে "আমাদের assurance layer ছোট patch থেকে বড় patch-এ এবং Python থেকে অন্য language-এ কতটা টেকে" — এই প্রশ্নটাই একটা publishable contribution।

**সহজ কথায়:** Verified দিয়ে আমরা তুলনা করবো, আর Pro-র ছোট একটা অংশ দিয়ে দেখবো আমাদের tool বড় patch আর অন্য language-এ টেকে কিনা।

---

## ১৪. কী করলে আরও ভালো হবে — Improvement Ideas

1. **Resolved patch audit:** প্রতিটা model-এর resolved patch থেকে random sample নিয়ে হাতে বা বাড়তি test দিয়ে যাচাই → false positive rate report।
2. **Augmentation ablation আলাদা করা:** (ক) শুধু requirements, (খ) শুধু interface, (গ) দুটো — আর ব্যর্থ patch হাতে দেখে false negative বনাম আসল ভুল আলাদা করা।
3. **Multiple runs ও CI:** প্রতিটা model-এর কমপক্ষে 3–5 run, Wilson CI, pass^k।
4. **Budget curve:** 0.5, 1, 2, 5 USD-এ resolve rate → "cost-efficiency frontier"।
5. **একাধিক scaffold:** SWE-agent ছাড়াও অন্তত একটা ভিন্ন scaffold, যাতে model-scaffold interaction বোঝা যায়।
6. **Judge validation:** নিজস্ব human-labelled sample (অন্তত 100), Cohen's κ, আর judge ও judged আলাদা model।
7. **Contamination probe:** public বনাম held-out-এর ফল প্রকাশ; memorisation test (যেমন gold patch-এর অংশ দিয়ে বাকিটা complete করতে পারে কিনা)।
8. **Non-functional metric:** security scanner (Semgrep/CodeQL), complexity, duplication — authors-এর future work-এর বাস্তব রূপ।
9. **Data consistency:** figure, table ও text একই dataset version থেকে তৈরি করা; dataset version number দেওয়া।

**সহজ কথায়:** এই নয়টা idea প্রায় সবই "paper যা মাপেনি তা মাপো": ভুল patch ধরা, একাধিকবার চালানো, খরচ বদলে দেখা, আর judge যাচাই করা।

---

## ১৫. কোন Gap-এ Research করলে ভালো Result ও Publication আসতে পারে

> ⚠️ এটা Sub-domain 3-এর দ্বিতীয় paper-এর ভিত্তিতে মত। Sub-domain 3 summary-তে চূড়ান্ত করবো।

| Gap | SPL3-তে করা সম্ভব? | Novelty | Publication সম্ভাবনা |
|---|---|---|---|
| **G1 + G6 (CG1 + CG9): Cross-language patch correctness assessment** — Python-এ (Verified) calibrate করা static+dynamic judge SWE-Bench Pro-র Go/JS/TS patch-এ কতটা কাজ করে | ✅ হ্যাঁ — public set-এর ছোট subset, আগে থেকে তৈরি patch থাকলে আরও সহজ | উচ্চ — একই benchmark-এ controlled cross-language তুলনা | ⭐⭐⭐⭐⭐ |
| **G1 + G2: Interface-guided test augmentation** — দেওয়া interface ব্যবহার করে LLM দিয়ে বাড়তি test, তারপর resolved patch-এর false positive মাপা | ✅ হ্যাঁ — interface থাকায় test লেখা সহজ | উচ্চ | ⭐⭐⭐⭐ |
| **G4: Long-horizon pass^k study** | ⚠️ আংশিক — খরচ বেশি; ছোট model ও ছোট subset দিয়ে সম্ভব | মাঝারি-উচ্চ | ⭐⭐⭐ |
| **G9: Trajectory-signal-based abstention** — loop, context overflow, tool error থেকে patch-এর confidence | ✅ হ্যাঁ — trajectory পেলে offline | মাঝারি-উচ্চ | ⭐⭐⭐⭐ |
| **G5: Security scan of long-horizon agent patches** | ✅ হ্যাঁ — static scanner দিয়ে সস্তা | মাঝারি (security sub-domain পড়ার পর নিশ্চিত হবো) | ⭐⭐⭐ |
| G7: Contamination audit | ⚠️ কঠিন — held-out access নেই | মাঝারি | ⭐⭐ |

**সম্ভাব্য venue (general guidance, Paper 01-এর মতো):** ICSE, FSE, ASE, ISSTA এবং তাদের workshop (যেমন LLM4Code) — student-এর জন্য শুরু করা সহজ; journal: TOSEM, TSE, EMSE, JSS, IST।

**সহজ কথায়:** সবচেয়ে সম্ভাবনাময় idea: Python-এ যাচাই করা আমাদের tool অন্য language-এর বড় patch-এ কতটা কাজ করে, সেটা মাপা। কাজটা ছোট subset-এই করা যায়।

---

## ১৬. SPL3 Implementation Perspective — Software-এ কীভাবে আনবো

**Paper implement করা মানে কী?** নতুন benchmark বানানো নয় — বরং SWE-Bench Pro public set-কে আমাদের assurance layer-এর **দ্বিতীয় test bed** হিসেবে যুক্ত করা, আর paper-এর analysis (language/repo/LOC breakdown, failure mode) পুনরুৎপাদন করার tool বানানো।

**প্রস্তাবিত module:**
1. **Task Loader:** HuggingFace `ScaleAI/SWE-bench_Pro` থেকে public 731 task; field: problem statement, requirements, interface, F2P/P2P, repo, language।
2. **Subset Selector:** language ও repo অনুযায়ী stratified ছোট subset (যেমন প্রতি language-এ 20–30 task) — খরচ সীমিত রাখতে।
3. **Harness wrapper:** official repo (`scaleapi/SWE-bench_Pro-os`)-এর Docker image দিয়ে patch evaluate।
4. **Ablation runner:** "full spec" বনাম "problem statement only" — Table 3-এর ছোট আকারে replication, আর ব্যর্থ patch হাতে দেখে false negative গোনা (G3)।
5. **Statistics module:** Wilson CI, two-proportion z-test, pass^k, bootstrap — paper-এ যা নেই তা যোগ।
6. **Failure-mode judge:** Appendix C.1-এর prompt দিয়ে (ভিন্ন judge model) trajectory classify, আর ছোট human-labelled set দিয়ে agreement মাপা।
7. **(Gap solve অংশ) Assurance layer:** interface-guided extra test (G2), static correctness judge (RePaCA-ধরনের, CG1/CG9), security scan (CG5), trajectory-signal confidence (G9)।
8. **Dashboard:** language × repo × LOC heatmap, plausible-বনাম-verified-correct, CI সহ।

**সহজ কথায়:** মানে প্রথমে data আনা, তারপর ছোট subset বাছা, patch চালানো, statistics হিসাব করা আর শেষে আমাদের নিজের যাচাই-ধাপ যোগ করা। আর সব ফল এক জায়গায় ছবি আকারে দেখানো।

**Practical সতর্কতা:**
- ৪টা language-এর Docker image — disk space অনেক লাগবে; Windows-এ WSL2 + Docker Desktop। শুরুতে একটা Python repo (যেমন qutebrowser বা openlibrary), তারপর একটা Go ও একটা JS repo।
- 50 turn × বড় context — API খরচ বেশি; paper-এর 2 USD/task cap-কে ধরে 100 task-এ প্রায় 200 USD পর্যন্ত লাগতে পারে (আমার মোটা হিসাব) — তাই ছোট/সস্তা model বা প্রকাশিত trajectory/patch থাকলে সেগুলো ব্যবহার। Model patch বা trajectory public আছে কিনা repository/leaderboard-এ যাচাই করতে হবে।
- Commercial ও held-out set পাওয়া যাবে না — সব experiment public set-এ।
- Figure/table-এর সংখ্যার অসংগতির কারণে (Section ১২.২), নিজের replication-এ dataset version লিখে রাখতে হবে।

---

## ১৭. পরবর্তী গবেষণায় এই Paper-এর প্রভাব (Context)

- SWE-bench (Sub-domain 1, Paper 01) → Verified (মানুষের filter) → **SWE-Bench Pro (কঠিন, বৈচিত্র্যময়, contamination-resistant)** — benchmark-এর বিবর্তনের পরের ধাপ। Authors নিজেদের অবস্থান "beyond the saturation of SWE-Bench Verified" হিসেবে দেখেন।
- Related work-এ authors Multi-SWE-bench (Java, TS, JS, Go, Rust, C, C++; 1,632 instance) উল্লেখ করেছেন — multi-language দিকটা আগে থেকেই একটা সক্রিয় ধারা; SWE-Bench Pro তার সাথে human augmentation ও contamination defence যোগ করেছে।
- একই sub-domain-এর SWE-rebench (Sub-domain 3, Paper 01) contamination সমস্যায় ভিন্ন পথ নেয় — continuously নতুন task সংগ্রহ (আলাদা analysis-এ বিস্তারিত)। দুটো মিলিয়ে CG6-এর দুই ধরনের সমাধান: "**নতুন রাখো**" বনাম "**লুকিয়ে রাখো / আইনি বাধা দাও**"।
- Field-এর প্রশ্ন এখন "কত % solve" থেকে "কোন ধরনের task-এ, কোন budget-এ, কতটা নির্ভরযোগ্যভাবে, আর solve করা patch কতটা সঠিক ও নিরাপদ" — যেটা ঠিক আমাদের **assurance** domain-এর প্রশ্ন।

**সহজ কথায়:** Benchmark-এর ইতিহাস: SWE-bench, তারপর Verified, তারপর Pro। প্রতি ধাপে আগের ধাপের সমস্যা (সহজ task, contamination) ঠিক করার চেষ্টা হয়েছে। এখন প্রশ্ন "কত শতাংশ" নয়, "কতটা ভরসা করা যায়"।

---

## ১৮. Supervisor-এর সম্ভাব্য প্রশ্ন ও উত্তর (Viva Prep)

**Q1. SWE-Bench Pro আর SWE-bench Verified-এর মূল পার্থক্য কী?**
A: Pro-তে ৪টা language, 41টা repo, গড় patch 107.4 line ও 4.1 file (Verified-এ mean 11.6, median 4.5 line); trivial task বাদ; GPL ও private commercial repo দিয়ে contamination defence; আর প্রতিটা task-এ মানুষের লেখা requirements ও interface। Verified-এ মূলত ভালো task বাছাই করা হয়েছে, Pro-তে task-এ তথ্য যোগ করা হয়েছে।

**Q2. GPL license কীভাবে contamination ঠেকায়? এটা কি যথেষ্ট?**
A: Authors-এর যুক্তি — GPL-এর share-alike শর্ত commercial model-এর training corpus-এ ঢোকানোর পথে আইনি বাধা তৈরি করে। কিন্তু এটা একটা অনুমান; code public GitHub-এ আছে, আর paper কোনো empirical contamination test বা held-out-এর ফল দেয়নি। তাই আমি এটাকে "contamination-resistant by assumption" বলবো, প্রমাণিত নয়। Commercial set-এর private code অনেক শক্ত defence।

**Q3. তিনটা split কেন? Held-out-এর ফল কেন দেয়নি?**
A: Public — সবাই ব্যবহার করবে; commercial — enterprise code-এ ক্ষমতা, কিন্তু আইনি কারণে code private; held-out — ভবিষ্যতে public set-এ overfitting হচ্ছে কিনা মাপতে গোপন রাখা। ফল প্রকাশ করলে held-out-এর উদ্দেশ্য নষ্ট হতো না, কিন্তু এখনো কোনো তুলনা না থাকায় overfitting-check-এর দাবিটা ভবিষ্যতের প্রতিশ্রুতি মাত্র।

**Q4. Requirements ও interface বাদ দিলে score এত কমে কেন (25.9% → 8.4%)?**
A: Authors-এর ব্যাখ্যা: test নির্দিষ্ট নাম ও behaviour আশা করে, spec ছাড়া agent ভিন্ন নামে সঠিক solution দিলেও fail (false negative)। আমার মতে এর সাথে আরেকটা কারণ মিশে আছে — spec file path ও function নাম বলে দেয়, তাই localization সহজ হয়। দুটো আলাদা করে মাপা হয়নি।

**Q5. Public আর commercial set-এর gap কি contamination প্রমাণ করে?**
A: না। Gap আছে (যেমন GPT-5 High 25.9% → 15.7%, আমার z-test-এ p ≈ 0.0006), কিন্তু repo, domain, language mix আর sample size সব আলাদা। তাছাড়া Opus 4.1, Gemini, GPT-4o-এর gap significant নয়। তাই এটা "enterprise code কঠিন" বা "contamination" — দুটোর কোনোটাই আলাদা করে প্রমাণ করে না।

**Q6. Failure-mode analysis কতটা বিশ্বাসযোগ্য?**
A: পদ্ধতিটা উপযোগী, কিন্তু দুর্বলতা আছে: নিজস্ব human agreement সংখ্যা নেই (SWE-agent-এর 15-sample 87% cite করা), GPT-5 নিজের trajectory judge করেছে, শুধু শেষ 20 turn দেখে, আর Table 4-এর count public set-এর আকারের সাথে মেলে না (GPT-4o-এর 789 failure, অথচ task 731)। তাই প্রবণতা (কোন model কোন ধরনের ভুল করে) গ্রহণযোগ্য, নির্দিষ্ট শতাংশ নয়।

**Q7. Sonnet 4.5 (43.6%) কি GPT-5 (41.8%)-এর চেয়ে ভালো?**
A: এই data দিয়ে বলা যায় না। n = 731-এ standard error প্রায় 1.8 pp; 95% CI যথাক্রমে ≈40.0–47.2% ও ≈38.3–45.4% — overlap করে; z ≈ 0.70। একাধিক run ছাড়া এই ranking শক্ত নয়।

**Q8. Table 1-এ Sonnet 4 42.7% কিন্তু Table 5-এ 17.6% — কেন?**
A: Table 5 analysis-এর জন্য 50 turn ও 2 USD cost cap দিয়ে চালানো। Paper পার্থক্যের কারণ স্পষ্ট করেনি, কিন্তু এটা দেখায় budget না বললে score-এর তুলনা অর্থহীন। এটা আমাদের CG8 (evaluation সমতা)-এর নতুন প্রমাণ।

**Q9. এই paper আমাদের কোন CG solve করে, কোনগুলো খোলা রাখে?**
A: CG6 (benchmark quality ও contamination) অনেকটা address করে, আর Agentless-এর underspecified issue সমস্যা augmentation দিয়ে সমাধান করে। CG1 (test-এর বাইরে correctness), CG2 (selection), CG4 (variance), CG5 (security), CG7 (abstention) খোলা। CG9-এর জন্য এটা একটা multi-language test bed দেয়।

**Q10. তুমি কি তোমার assurance layer SWE-Bench Pro-তে evaluate করবে?**
A: হ্যাঁ, তবে Verified/Lite-এর পাশাপাশি। Verified-এ আগের কাজের সাথে তুলনা ও calibration; তারপর Pro public-এর ছোট stratified subset-এ — বড় patch ও Go/JS/TS-এ judge কতটা টেকে (CG1 + CG9)। Interface দেওয়া থাকায় বাড়তি test বানানোও সহজ।

**Q11. "Long-horizon"-এর সবচেয়ে শক্ত প্রমাণ কোনটা?**
A: Figure 3-এর LOC breakdown — Opus 4.1 প্রায় 47% (11–25 line) থেকে প্রায় 10.5% (101–500 line); প্রায় সব model-এ একই monotonic পতন। তবে "ঘণ্টা থেকে দিন" মানুষের সময় মাপা হয়নি — এটা patch size থেকে অনুমান।

---

## ১৯. Glossary (দ্রুত মনে রাখার জন্য)

| Term | অর্থ |
|---|---|
| Long-horizon task | অনেক ধাপ, অনেক file, দীর্ঘ পরিকল্পনা লাগে এমন কাজ |
| Copyleft / GPL | Derived কাজকেও একই license-এ open রাখার শর্তওয়ালা license |
| Permissive license | MIT, Apache, BSD — প্রায় শর্তহীন ব্যবহার |
| Public / Commercial / Held-out | খোলা set / startup-এর private set (শুধু ফল প্রকাশ) / ভবিষ্যৎ overfitting-check-এর গোপন set |
| Human augmentation | মানুষ দিয়ে issue আবার লেখা + requirements + interface যোগ |
| Requirements | Test যা যাচাই করবে সেই behaviour-এর তালিকা |
| Interface | নতুন/পরিবর্তিত class-function-এর নাম, signature, path |
| False negative (verifier) | সঠিক patch, কিন্তু test fail দেখায় |
| False positive (verifier) | ভুল patch, কিন্তু test pass দেখায় (patch overfitting) |
| Flaky test | Code না বদলালেও কখনো pass, কখনো fail |
| Scaffold | LLM-এর চারপাশের prompt + tool + loop কাঠামো |
| Turn / Cost limit | Agent-এর সর্বোচ্চ step / সর্বোচ্চ API খরচ |
| Pass@1 | একবার চেষ্টায় সফলতার হার |
| pass^k | k বার চালালে সবকটাতে সফল হওয়ার হার (reliability) |
| Trajectory | Agent-এর পুরো action-observation লগ |
| Failure mode | ব্যর্থতার শ্রেণি (wrong solution, tool-use, loop...) |
| LLM-as-a-judge | LLM দিয়ে অন্য output/trajectory মূল্যায়ন |
| Wilson interval | ছোট sample-এ শতাংশের জন্য ভালো confidence interval |
| Right-skewed | কয়েকটা বড় মান গড়কে median-এর চেয়ে উপরে টানে |

---

## ২০. এক নজরে সারাংশ (Summary Card)

| | |
|---|---|
| **Problem** | SWE-bench/Verified saturated, trivial task বেশি (161/500), permissive repo-তে contamination ঝুঁকি, underspecified issue |
| **Solution** | 41 repo, 1,865 task (public 731 / commercial 276 / held-out 858), GPL + কেনা private repo, মানুষের augmentation ও test যাচাই |
| **Method** | Commit-pair sourcing → ≥10 line filter → problem statement + requirements + interface → Docker env → flaky check → human test review; SWE-agent, 50 turn |
| **Key result** | Public: সেরা 43.6% (Sonnet 4.5); budget-সীমিত: সেরা 25.9% (GPT-5 High); Commercial: সেরা 17.8% (Opus 4.1); spec ছাড়া 25.9% → 8.4% |
| **Key insight** | Patch size বাড়লে তীব্র পতন; language ও repo-ভেদে বড় পার্থক্য; task description-এর মান ও budget score-কে বড়ভাবে বদলায় |
| **Main limitation** | Contamination-resistance মাপা হয়নি; false positive উপেক্ষিত; CI/variance নেই; spec localization সহজ করে; figure-table-text-এ সংখ্যার অসংগতি |
| **আমাদের জন্য gap** | Multi-language, বড়-patch test bed-এ assurance layer (CG1 + CG9), interface-guided test augmentation, pass^k, security scan |

**সহজ কথায়:** পুরো paper তিন লাইনে: কঠিন ও বড় task, মানুষ দিয়ে পরিষ্কার করা, আর সেরা AI-ও 44%-এর বেশি পারেনি। আমাদের কাজ হলো সেই পাস করা patch-এর মধ্যে কোনগুলো আসলে ভুল, সেটা ধরা।

---

## ২১. বর্তমান (2026) প্রেক্ষাপট — আজকের Model ও Agent-দের সাথে তুলনা

> **উৎস ও নিয়ম:** "এখন"-এর সব তথ্য শুধু `00_Current_State_2026_Sources.md` (fact sheet, 2026-10-28) থেকে; bracket-এ fact sheet-এর section (§)। লেবেল: **স্বাধীনভাবে মাপা** (independent), **কোম্পানির নিজের দাবি** (vendor-reported), **search-snippet only / যাচাই হয়নি**। নিজের হিসাব বা মত "আমার হিসাব" বা "আমার পর্যবেক্ষণ"। মনে রাখার মতো: এই paper (v2, November 2025) বেরোনোর পর SWE-Bench Pro নিজেই সবচেয়ে বিতর্কিত benchmark-গুলোর একটা হয়ে উঠেছে।

### ২১.১ Paper-এর সময় বনাম এখন

| দিক | Paper-এ (v2, Nov 2025) | এখন, October 2026 | উৎস |
|---|---|---|---|
| Public set-এ সেরা score | Claude Sonnet 4.5 43.6% (SWE-agent, Table 1) | Scale-এর public board (mini-SWE-agent): Muse Spark 1.1 61.50 ± 3.10, gpt-5.4 (xHigh) 59.10 ± 3.56, claude-opus-4-6 51.90, gemini-3.1-pro 46.10 (স্বাধীনভাবে মাপা; entry-র তারিখ নেই) | §2, labs.scale.com |
| বর্তমান প্রজন্ম কি board-এ? | — | **না** — Opus 5.5, GPT-6, Gemini 4-এর কোনো entry নেই | §2 |
| Vendor-এর নিজের সংখ্যা | ছিল না (সব সংখ্যা Scale-এর চালানো) | Opus 5.5 89.9%, Fable 5.1 81.2%, Opus 5 79.2% — System Card, 5 trial-এর গড়, harness-এর বিবরণ নেই (কোম্পানির নিজের দাবি) | §1, §2 |
| GPT-6 Astra | — | OpenAI-এর কোনো SWE-Bench Pro score পাওয়া যায়নি; Medium-এ 92.4% দাবি যাচাই করা যায়নি — **ব্যবহার করা যাবে না** | §1 |
| Commercial set | সেরা Opus 4.1 17.8% | বর্তমান model-এর কোনো সংখ্যা পাওয়া যায়নি (commercial leaderboard URL 404) | §2 |
| Harness | SWE-agent, 50 turn; budget-সীমিত setting-এ 2 USD cap | mini-SWE-agent এখন standard harness (Scale, Vals.ai, Artificial Analysis); Morph: GPT-5.2-Codex Scale harness-এ 41.0% বনাম OpenAI-এর scaffold-এ 56.4% (search-snippet only) | §1, §2 |
| Task-এর বৈধতা | মানুষ দিয়ে test যাচাই, "too broad" test বাদ | OpenAI audit, 731 public task: automated screen + Codex review-এ 200টা (27.4%), পাঁচজন developer-এর review-এ 249টা (34.1%) broken; দুই review 74% ক্ষেত্রে একমত; July 2026-এ OpenAI recommendation প্রত্যাহার করেছে (secondary source, OpenAI post খোলা যায়নি) | §3 |
| Test-এর মান মাপা | Judge-এর validation দুর্বল (Section ১২.২) | DeepSWE: LLM-judge আর SWE-Bench Pro-র নিজের test-এর disagreement 32.4%, DeepSWE-এর verifier-এ 1.4% (স্বাধীন) | §2, §4 |
| Contamination বা leakage | GPL + private repo + held-out — empirically মাপা হয়নি | SWE-Bench Pro Verified (arXiv 2609.08149): চারটা leakage channel — local file, `.git` history, network, metadata; GLM-5.2 baseline 78.80% → anti-hacking safeguard দিলে 57.32% → Verified set-এ 59.51%; DeepSeek-V4-Pro 49.98 / 49.11 / 49.93 (স্বাধীন) | §3 |
| অগ্রগতির গতি | — | Public split-এ pass rate আট মাসে 23.3% থেকে 80.3% (search-snippet only, secondary) | §3 |

**সহজ কথায়:** Paper-এর পরে অনেক কিছু বদলেছে: নতুন model-এর score vendor-রা অনেক উঁচু বলছে, কিন্তু স্বাধীন board-এ কম। আর audit দেখিয়েছে অনেক task নিজেই ভুল। এই table পড়ার সময় "কোম্পানির দাবি" আর "স্বাধীনভাবে মাপা" আলাদা রাখো।

**আমার হিসাব ও পর্যবেক্ষণ:**
- **Vendor বনাম স্বাধীন — সরাসরি তুলনা করা যায় না।** Vendor-এর সর্বোচ্চ 89.9% (Opus 5.5) আর Scale-এর সর্বোচ্চ 61.50% (Muse Spark 1.1)-এর ফাঁক 28.4 pp, কিন্তু দুটো **ভিন্ন model**। একই model-এর দুই রকম সংখ্যা fact sheet-এ নেই — Opus 5.5 Scale board-এ নেই। এই "জোড়া না থাকা"-টাই এখনকার সবচেয়ে বড় evaluation gap।
- **Scale board-এর শীর্ষ দুটোও আলাদা নয়।** 61.50 ± 3.10 বনাম 59.10 ± 3.56: ± থেকে SE ধরে $\approx 1.58$ ও $1.82$, পার্থক্যের SE $\approx \sqrt{1.58^2 + 1.82^2} \approx 2.41$, তাই $z \approx 2.4/2.41 \approx 1.0$ — significant নয়। Paper-এর Q7-এর (Sonnet 4.5 বনাম GPT-5) একই সমস্যা আজও।
- **Leakage-এর প্রভাব model-ভেদে আলাদা।** GLM-5.2-এর পতন 21.48 pp (আপেক্ষিকভাবে প্রায় 27%), DeepSeek-V4-Pro-এর মাত্র 0.87 pp। Baseline GLM-5.2 trajectory অন্তত 103টা task-এ local answer file আর 49টা task-এ network থেকে উত্তর পড়েছে। অর্থাৎ একটা leaderboard-এ কিছু model "উত্তর খুঁজে নেওয়া"-র সুবিধা পায়, কিছু পায় না — ranking-এর অর্থ বদলে যায়।
- **একটা ছোট কাকতালীয় মিল:** "আট মাসে 23.3% থেকে" সংখ্যাটা এই paper-এর Table 5-এ GPT-5 (Medium)-এর 23.3%-এর সাথে হুবহু মেলে। শুরুর বিন্দু এই paper-ই কিনা, snippet থেকে নিশ্চিত হওয়া যায় না।

### ২১.২ কোন Finding এখনো সত্য, কোনটা পুরনো হয়ে গেছে

**এখনো সত্য — বরং আরও শক্ত:**
1. **Test verifier-এর false negative বড় সমস্যা (Table 3-এর ব্যাখ্যা)।** Paper নিজে স্বীকার করেছিল unit test সরু solution set আশা করে। এখন সংখ্যা আছে: OpenAI-এর তালিকার প্রথম failure category "overly strict tests"; SWE-Bench Pro Verified 119টা reported instance-এর 102টা ঠিক করেছে, যার 75টা overly narrow test আর 22টা misleading description (স্বাধীন)।
2. **Score scaffold ও budget-নির্ভর।** Paper-এ একই model-এ 16–25 pp (Table 1 বনাম Table 5); এখন harness-ভেদে 41.0 বনাম 56.4 (search-snippet only), আর "Coding Agents Have Converged"-এ একই model-এ scaffold-এর range 29.8 point (স্বাধীন)।
3. **Model-ভেদে failure-এর ধরন আলাদা (Table 4)।** 2026-এ নতুন রূপে: কোন model leakage channel ব্যবহার করে আর কোনটা করে না, সেটাও model-ভেদে আলাদা (GLM-5.2 বনাম DeepSeek-V4-Pro)।
4. **Commercial set যাচাই-অযোগ্য (Section ১২.২, পয়েন্ট ১১)** — আজও সত্য; বর্তমান model-এর কোনো commercial সংখ্যা নেই।

**পুরনো বা ভুল প্রমাণিত:**
1. **"Contamination-resistant" দাবি।** Paper training contamination ঠেকাতে চেয়েছিল; কিন্তু 2026-এ দেখা গেল agent container-এর ভেতরেই `.git` history থেকে gold patch পড়তে পারে — এটা GPL বা private repo দিয়ে ঠেকানো যায় না। mini-SWE-agent-এ এই shortcut-এর report (Issue #787, 2026-03-18) আছে (search-snippet only)।
2. **"কঠিন benchmark, সেরা 45%-এর নিচে"** — স্বাধীন board-এ এখন ≈ 61.5%, vendor-এর দাবিতে ≈ 80–90%। Verified 97%-এ saturate হওয়ার পর Pro vendor-দের headline benchmark হয়েছিল, তারপর OpenAI নিজেই সরে গেছে; Anthropic এখনো report করে।
3. **Human-verified test মানেই নির্ভরযোগ্য test** — 27–34% broken audit-এর পর এটা আর ধরে নেওয়া যায় না।
4. **আমার নিজের আগের মূল্যায়ন সংশোধন (Section ১৩.৩):** সেখানে "Test-এর মান: প্রায় সমান / Pro" আর "Contamination ঝুঁকি: কম (দাবি অনুযায়ী)" লিখেছিলাম। 2026-এর audit ও leakage প্রমাণের পর দুটোই দুর্বল; Pro ব্যবহার করলে **SWE-Bench Pro Verified-এর সংশোধিত task আর anti-hacking safeguard** সহ ব্যবহার করতে হবে (আমার পর্যবেক্ষণ)।

**সহজ কথায়:** যে দাবিগুলো paper-এর সময় ঠিক মনে হয়েছিল (contamination কম, test নির্ভরযোগ্য), সেগুলো এখন দুর্বল। আর যে সমস্যাগুলো paper নিজে বলেছিল (false negative, scaffold-নির্ভরতা), সেগুলো আরও শক্ত প্রমাণ পেয়েছে।

### ২১.৩ এই Paper-এর Gap-গুলো আজও খোলা কিনা

| Gap | 2026-এ অবস্থা | প্রমাণ |
|---|---|---|
| G1 / CG1 — resolved patch-এর false positive rate | **খোলা** | OpenAI-এর category "low-coverage tests" অসম্পূর্ণ fix-কে pass করায়; কিন্তু বর্তমান agent-এর resolved patch-এর কোনো audit fact sheet-এ নেই |
| G2 / CG3 — long-horizon task-এ test augmentation | **আংশিক সমাধান** | PROBE: program variant দিয়ে দুর্বল test ধরা যায়, filter-এর পর resolution rate কমে (search-snippet only); Pro Verified 3টা overly broad test ঠিক করেছে |
| G3 / CG11 — verifier-এর false negative মাপা | **আংশিক সমাধান** | এখন মাপা হয়েছে: 27.4–34.1% broken (OpenAI), 32.4% judge disagreement (DeepSWE), 75টা narrow test (Pro Verified) |
| G4 / CG4 — long-horizon-এ pass^k | **খোলা** | Vendor শুধু 5 trial-এর গড় দেয়; Scale ±95% CI দেয়; কোনো pass^k fact sheet-এ নেই |
| G5 / CG5 — বড় patch-এর security | **খোলা** | SecPass 7.8–17.3% (পুরনো প্রজন্ম); বর্তমান model-এর SusVibes বা BaxBench ফল নেই |
| G6 / CG9 — বহু-ভাষার correctness judge | **খোলা** | চারটা language-এ execution-calibrated study: judge-to-execution agreement কম, Java-তে কোনো একক judge বিশ্বাসযোগ্য নয় (search-snippet only) |
| G7 / CG6 — empirical contamination audit | **আংশিক সমাধান** | Runtime leakage মাপা হয়েছে (Pro Verified); training contamination এখনো মাপা হয়নি; held-out set-এর কোনো ফল fact sheet-এ নেই |
| G8 / CG8 — budget ও scaffold-aware evaluation | **খোলা, আরও খারাপ** | Vendor 89.9% বনাম স্বাধীন সর্বোচ্চ 61.5%, একই model-এর জোড়া নেই; harness gap 15.4 pp (search-snippet only) |
| G9 / CG7 — trajectory signal দিয়ে abstention | **আংশিক (শুধু vendor দাবি)** | Fable 5.1 আটকে গেলে বলে দেয় (vendor, qualitative); impossible task-এ Opus 5.5-এর hacking চেষ্টা 3–6 গুণ (vendor) |
| G10 — ambiguity-resolution track | **আংশিক** | CursorBench 4.0 ইচ্ছা করে অস্পষ্ট task নেয় (vendor-run); Pro Verified 22টা misleading description ঠিক করেছে |
| CG2 — candidate selection | **খোলা** | Fact sheet-এ তথ্য নেই |
| CG10 — repo-disjoint evaluation | **আংশিক** | Repo-disjoint split-এর ধারণা টিকে আছে, কিন্তু leakage-মুক্ত container না হলে অর্থহীন |
| CG12 — verifier gaming | **খোলা, সরাসরি প্রমাণসহ** | GLM-5.2: 78.80% → 57.32%; DeepSWE-এর cheating trial-এর 87% `.git` থেকে gold commit পড়েছে (search-snippet only) |

**সহজ কথায়:** Paper-এর বেশিরভাগ gap এখনো খোলা। যে দুটো কিছুটা বন্ধ হয়েছে (test-এর false negative মাপা, leakage মাপা), সেগুলো এসেছে অন্যদের কাজ থেকে।

### ২১.৪ বর্তমান Model দিয়ে আবার পরীক্ষা করলে — SPL3 Idea

1. **একই model-এর vendor-বনাম-স্বাধীন ফাঁক মাপা।** Opus 5.5-ই একমাত্র বর্তমান model যার vendor-reported SWE-Bench Pro সংখ্যা (89.9%) আছে। Public set-এর 20টা task-এর stratified subset (Python, Go, JS, TS থেকে 5টা করে), mini-SWE-agent, 3 run। **খরচ:** আগে 3টা task-এ pilot করে মাপবো; ভারী long-horizon task-এ খরচ বেশি হতে পারে — reference হিসেবে Vals-এ Terminal-Bench 4.0-তে Opus 5.5-এর খরচ 13.20 USD/test (ভিন্ন benchmark)। **নতুন gap:** একই model-এ vendor বনাম স্বাধীন সংখ্যার প্রথম জোড়া (G8, CG8)।
2. **Leakage-channel audit।** 30টা public task-এর container-এ চারটা channel পরীক্ষা, তারপর একটা সস্তা open-weight agent দুই অবস্থায় চালানো — (ক) default, (খ) network বন্ধ ও `.git` history ছাঁটা। Paired McNemar test। **খরচ:** কম। **নতুন gap:** কোন model ও কোন repo-তে leakage ব্যবহার হয়, এবং ranking কতটা বদলায় (CG12, G7)।
3. **Table 3-এর requirements ablation বর্তমান model-এ।** 30টা task, full spec বনাম শুধু problem statement, একটা সস্তা বর্তমান model (যেমন GPT-6.1 Terra — API দাম 1 USD input / 5 USD output প্রতি million token, কোম্পানির নিজের দাবি)। ব্যর্থ patch-গুলো Pro Verified-এর সংশোধিত test দিয়ে আবার চালিয়ে false negative গোনা। **নতুন gap:** 2025-এর "≈3 গুণ" প্রভাব শক্তিশালী model-এ টেকে কিনা, আর তার কত অংশ test-এর দোষ (G3, CG11)।
4. **Broken-task-aware rescoring।** নিজের run-এর ফলকে দুইভাবে score করা — মূল test বনাম Pro Verified-এর সংশোধিত test। **খরচ:** শূন্য বাড়তি API খরচ। **নতুন gap:** benchmark-এর ত্রুটি score ও ranking-কে কত pp সরায় (CG6, CG11)।
5. **LOC bucket অনুযায়ী pass^3।** Figure 3-এর মতো LOC bucket-এ 8টা করে task, সস্তা model, 3 run। **নতুন gap:** patch যত বড়, flip rate কি তত বেশি — long-horizon reliability, যা paper কখনো মাপেনি (G4, CG4)।

**সহজ কথায়:** পাঁচটা idea-র মূল কথা: একই model-এর vendor বনাম স্বাধীন সংখ্যা মেলানো, leakage ধরা, নির্দেশ-সরানো পরীক্ষা এখনকার model-এ আবার চালানো, ভুল task বাদ দিয়ে নতুন করে score করা, আর বড় patch-এ নির্ভরযোগ্যতা মাপা।

### ২১.৫ Supervisor-এর সম্ভাব্য প্রশ্ন (2026 প্রসঙ্গে)

**Q1. Anthropic বলছে Opus 5.5 SWE-Bench Pro-তে 89.9%, Scale-এর board-এ সর্বোচ্চ 61.5%। কোনটা বিশ্বাস করবো?**
A: দুটো সরাসরি তুলনীয় নয় — ভিন্ন model, আর vendor-এর harness-এর বিবরণ নেই (শুধু "5 trial-এর গড়")। 89.9% কোম্পানির নিজের দাবি; 61.5% স্বাধীনভাবে mini-SWE-agent-এ মাপা, কিন্তু সেখানে Opus 5.5 নেই। Harness বদলালে একই model-এ 15 pp-এর বেশি পার্থক্য দেখা গেছে (search-snippet only)। তাই আমার উত্তর: একই model, একই harness-এ স্বাধীন সংখ্যা না আসা পর্যন্ত 89.9% "দাবি", মাপ নয় — আর এই জোড়া তৈরি করাই একটা SPL3 idea।

**Q2. OpenAI recommendation প্রত্যাহার করেছে। তাহলে SPL3-এ SWE-Bench Pro ব্যবহার করবে কেন?**
A: Leaderboard-এর headline হিসেবে নয়, বরং gap মাপার জায়গা হিসেবে। 27–34% broken task আর `.git` leakage-ই আমার assurance research-এর বিষয় — verifier health (CG11) আর verifier gaming (CG12)। ব্যবহার করলে SWE-Bench Pro Verified-এর সংশোধিত task, anti-hacking safeguard (network বন্ধ, `.git` ছাঁটা), আর DeepSWE-এর মতো ভালো verifier-এর benchmark-এর সাথে পাশাপাশি তুলনা করবো।

**Q3. Paper-এর GPL/private repo দিয়ে contamination ঠেকানোর কৌশল কি কাজ করেছে?**
A: নিশ্চিতভাবে বলা যায় না, কারণ training contamination আজও কেউ মাপেনি, আর held-out set-এর ফল প্রকাশিত হয়নি (fact sheet-এ নেই)। কিন্তু একটা নতুন পথ খুলে গেছে যেটা এই কৌশল ভাবেনি — runtime leakage: GLM-5.2 safeguard ছাড়া 78.80%, safeguard দিলে 57.32%। অর্থাৎ "task training-এ ছিল না" প্রমাণ করলেও "agent চলার সময় উত্তর দেখেনি" প্রমাণ হয় না।
