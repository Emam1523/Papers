# Paper Analysis 05 (TestGen): Oracle-Guided Program Selection from Large Language Models

> **Sub-domain:** LLM Test Generation (Sub-domain 1-এর CG2 "candidate patch selection / re-ranking"-এর জন্য সরাসরি প্রাসঙ্গিক paper)
> **Analysis করেছে:** SPL3 — AI Coding Agent Reliability and Assurance
> **Paper file:** `LLM Test Generation/Oracle-Guided Program Selection from Large Language Models.pdf`
> **আগে পড়ো:** Paper 01 (SWE-bench) — test oracle, pass@k, regression test; Paper 04 (Agentless) — 40টা candidate patch, reproduction test, majority voting, 126 বনাম 96।

---

## ০. Paper-এর পরিচয় (Bibliographic Info)

| বিষয় | তথ্য |
|---|---|
| **Title** | Oracle-Guided Program Selection from Large Language Models |
| **Authors** | Zhiyu Fan, Haifeng Ruan (দুজনেই joint first author), Sergey Mechtaev, Abhik Roychoudhury |
| **Institution** | National University of Singapore (Fan, Ruan, Roychoudhury); Peking University (Mechtaev) |
| **Venue** | ISSTA '24 — 33rd ACM SIGSOFT International Symposium on Software Testing and Analysis, Vienna, Austria, September 16–20, 2024; pages 628–640 (13 pages) |
| **DOI** | 10.1145/3650212.3680308 (paper-এ received 2024-04-12, accepted 2024-07-03) |
| **Paper type** | **Technique paper** — নতুন program selection technique (tool: **LLMCodeChoice**) + empirical evaluation |
| **Artifacts** | Tool ও সব data: Zenodo DOI 10.5281/zenodo.10390291 (paper-এর Data Availability অংশ) |
| **Funding (paper অনুযায়ী)** | Singapore MoE Tier 3 grant "Automated Program Repair"; NRF Singapore CREATE programme |
| **আমাদের domain-এ গুরুত্ব** | ⭐⭐⭐⭐⭐ — এটা ঠিক **"অনেক LLM candidate থেকে সঠিকটা কীভাবে বাছবো"** প্রশ্নের উত্তর দেয়। আমাদের CG2 (re-ranking) ও CG1 (plausible ≠ correct)-এর জন্য এটাই প্রথম সরাসরি technique paper। |

**নোট:** User-এর brief-এ "NUS" বলা ছিল — তিনজন author NUS-এর, কিন্তু Sergey Mechtaev-এর affiliation paper-এ **Peking University** লেখা।

---

## ★ সহজ ভাষায় পুরো Paper (প্রথমবার পড়ার জন্য)

### ক. Paper-টা কী নিয়ে?
- এটা একটা **নতুন technique-এর paper**। সাথে আছে অনেক পরীক্ষা (experiment)।
- Paper-টা লিখেছেন Zhiyu Fan, Haifeng Ruan, Sergey Mechtaev আর Abhik Roychoudhury। বেশিরভাগ লেখক Singapore-এর NUS university-র।
- ২০২৪ সালে ISSTA নামের একটা বড় software testing conference-এ এটা ছাপা হয়েছে।
- বিষয়: AI (LLM) একই কাজের জন্য অনেকগুলো code লিখে দিলে, **কোনটা ঠিক সেটা কীভাবে বাছবো?**
- তাদের বানানো tool-এর নাম **LLMCodeChoice**।

### খ. সমস্যাটা কী ছিল?
- ধরো তুমি ChatGPT-কে বললে "একটা function লেখো"। সে ১০টা আলাদা উত্তর দিল। এর মধ্যে কিছু ঠিক, কিছু ভুল। তুমি কোনটা নেবে?
- আগের পদ্ধতিতে AI-কেই বলা হতো অনেকগুলো test বানাতে। তারপর দেখা হতো কোন code বেশি test পাস করে।
- কিন্তু AI-এর বানানো test-এর প্রায় ২৫% নিজেই ভুল। ভুল test দিয়ে ঠিক code বাছা যায় না।
- আরেকটা পদ্ধতি ছিল "majority vote" মানে বেশিরভাগ code যা করে সেটাকেই ঠিক ধরা। কিন্তু বেশিরভাগ code একসাথে ভুল করলে এটা ভুলটাই বাছে।
- **উদাহরণ:** `change_base(0, 2)` নামের একটা task-এ ১০টার মধ্যে ৬টা code ভুল উত্তর (`''`) দেয়। বাকি ৪টা ঠিক উত্তর (`'0'`) দেয়। Majority vote ভুল দলটাকেই বেছে নেয়।

### গ. Paper কী solve করেছে?
- Paper দেখিয়েছে, ভুল test লেখার দরকার নেই। দুটো code কোথায় আলাদা আচরণ করে সেটা খুঁজে বের করো। তারপর শুধু সেই এক জায়গায় AI-কে জিজ্ঞেস করো কোন উত্তরটা ঠিক।
- AI-কে খোলা প্রশ্ন না করে multiple-choice প্রশ্ন করা হয়েছে। এতে AI অনেক বেশি ঠিক উত্তর দেয়।
- প্রতি task-এ গড়ে মাত্র ১–২টা test input লাগে। আগের পদ্ধতিতে লাগত প্রায় ৮৫–৮৯টা।
- সাথে একটা ছোট, মানুষের পড়ার মতো প্রমাণ পাওয়া যায়, যেমন "এই input-এ এই output হওয়া উচিত"।
- **সংখ্যা ১:** Multiple-choice দিলে AI ৮৪.৩% বার ঠিক বাছে। নিজে থেকে উত্তর বের করতে বললে ৭০.৩%। মানে ১০০টা প্রশ্নে প্রায় ১৪টা বেশি ঠিক।
- **সংখ্যা ২:** HumanEval+ benchmark-এ ঠিক code পাওয়ার হার ৮৭.৭%। আগের সেরা পদ্ধতি CodeT পেয়েছিল ৮০.৮%। মানে ১০০টা task-এ প্রায় ৭টা বেশি।
- **সংখ্যা ৩:** AI-কে পাঠানো token কমেছে প্রায় ৪ গুণ (১৫৩৩ বনাম ৬৩১৯)। মানে খরচ প্রায় এক-চতুর্থাংশ।

### ঘ. কীভাবে solve করেছে?
1. AI (ChatGPT) থেকে একই task-এর জন্য অনেকগুলো code নেওয়া হয়, প্রায় ১০টা।
2. প্রতি জোড়া code একসাথে চালিয়ে এমন input খোঁজা হয় যেখানে দুটোর output আলাদা। এটার নাম differential testing। খোঁজার জন্য Hypothesis (random input) আর CrossHair (গাণিতিক পথ ধরে খোঁজা) tool ব্যবহার হয়।
3. যে code-গুলো সব পাওয়া input-এ একই output দেয়, তাদের এক দলে (cluster) রাখা হয়।
4. যে input সবচেয়ে সমানভাবে দলগুলোকে ভাগ করে, সেটা আগে নেওয়া হয়। এতে কম প্রশ্নে বেশি code বাদ পড়ে।
5. GPT-4-কে বলা হয়: "এই input-এ output কি `A` নাকি `B`? ধাপে ধাপে ভেবে বলো।" এটাই multiple-choice প্রশ্ন।
6. GPT-4 যে উত্তর বাছে, সেই উত্তর যে দল দেয় না তাদের বাদ দেওয়া হয়।
7. একটা দল বাকি না থাকা পর্যন্ত ৪–৬ ধাপ আবার করা হয়।
8. শেষ দলের একটা code user-কে দেওয়া হয়, সাথে বাছা input-output জোড়াগুলো প্রমাণ হিসেবে।

### ঙ. এরপর কী করা যায়?
- Authors বলেছেন: এখন শুধু একক function-এ কাজ হয়েছে। বড় project বা library-তে নেওয়া future work।
- Authors আরও বলেছেন: input-এর নিয়ম কঠিন হলে (যেমন নির্দিষ্ট ধরনের string) test খুঁজে পাওয়া যায় না। AI-এর বানানো test-এর সাথে মিলিয়ে এটা ঠিক করা যায়।
- খোলা প্রশ্ন: সব code ভুল হলে কী হবে? Paper ১১৮টার মধ্যে মাত্র ৩০টা ধরতে পেরেছে।
- খোলা প্রশ্ন: শুধু GPT-4 আর একটা run দিয়ে পরীক্ষা হয়েছে। কোনো confidence interval নেই।
- **SPL3-তে আমরা করতে পারি:** Agentless-এর ৪০টা candidate patch থেকে সঠিকটা এই পদ্ধতিতে বাছা। সেখানে বাছাই করে পাওয়া যায় ৯৬টা, আর সম্ভাব্য সর্বোচ্চ ১২৬টা।
- সাথে "কোনোটাই ঠিক না" হলে মানুষকে জানানো, আর input-output প্রমাণসহ একটা assurance report বানানো।

> **মনে রাখো:**
> অনেক AI code থেকে সঠিকটা বাছতে "বেশিরভাগ যা বলে" নয়, "যেখানে আলাদা সেখানে প্রশ্ন করো" পদ্ধতি বেশি কাজের।
> AI-কে খোলা প্রশ্নের চেয়ে কয়েকটা option থেকে বাছতে দিলে সে অনেক কম ভুল করে।
> এই ধারণাটাই repository-level agent patch-এ নেওয়া আমাদের SPL3-এর মূল সুযোগ।

---

## ১. এক লাইনে Paper (TL;DR)

**LLM দিয়ে একটা task-এর জন্য অনেকগুলো program বানানো হয়; differential testing দিয়ে এমন input খোঁজা হয় যেখানে program-গুলো ভিন্ন output দেয় (distinguishing input); তারপর LLM-কে "এই input-এ এই কয়টা output-এর মধ্যে কোনটা সঠিক?" — এরকম multiple-choice প্রশ্ন করে সঠিক behaviour-এর program cluster বাছাই করা হয়।**

### Supervisor-কে ৩০ সেকেন্ডে কীভাবে বলবো
> "Sir, LLM একই task-এ ১০টা program দিলে কোনটা নেবো — এটা একটা আলাদা সমস্যা। আগের পদ্ধতি (AlphaCode, CodeT) LLM দিয়েই শ'খানেক test বানিয়ে majority vote করে। এই ISSTA 2024 paper বলছে: LLM-এর বানানো test-এর প্রায় 25% নিজেই ভুল, আর majority প্রায়ই ভুল। তাই তারা Hypothesis (fuzzing) আর CrossHair (symbolic execution) দিয়ে মাত্র ১–২টা distinguishing input বের করে, তারপর GPT-4-কে শুধু ঐ input-এর সম্ভাব্য output-গুলো দেখিয়ে সঠিকটা বাছতে বলে। Multiple-choice দিলে LLM 84.3% সঠিক বাছে, কিন্তু নিজে থেকে output predict করতে বললে 70.3%। ফলে HumanEval+-এ pass@1 CodeT-এর 80.8% থেকে 87.7% হয়েছে, আর token খরচ প্রায় চার ভাগের এক ভাগ। আমাদের জন্য গুরুত্বপূর্ণ কারণ Agentless-এর 40টা candidate patch থেকে বাছাইয়ের সমস্যাটা (126 সম্ভব, পেয়েছে 96) ঠিক এই ধরনের।"

---

## ২. Background — এই paper বুঝতে যা আগে জানা দরকার

### ২.১ Program Generation বনাম Program Selection
- **Program generation (synthesis):** natural language description থেকে code তৈরি করা। LLM এটা করে।
- **Program selection:** LLM-কে একই prompt একাধিকবার দিলে (temperature > 0 মানে LLM-এর উত্তরে একটু randomness রাখা) প্রতিবার আলাদা program আসে। এই **sample-গুলোর মধ্যে কোনটা user-কে দেখাবো** — এটাই selection।
- এই paper **নতুন code generate করে না**; generation যেকোনো ভাবে হোক, তার উপরে selection layer বসায়। Paper-এর ভাষায় selection, repair-এর **পরিপূরক** (complement)।
- **আমাদের জন্য মানে:** coding agent-এর ক্ষেত্রেও একই — agent অনেকগুলো patch বানায় (Agentless 40টা), কোনটা submit করবে সেটা আলাদা সিদ্ধান্ত।

**সহজ কথায়:** Generation মানে প্রশ্নের উত্তর লেখা। Selection মানে অনেক উত্তরের মধ্যে একটা জমা দেওয়ার জন্য বাছা। পরীক্ষার হলে একই প্রশ্নের ১০টা খসড়া লিখে সেরাটা জমা দেওয়ার মতো।

### ২.২ Test Oracle ও Oracle Problem
- **Test oracle:** একটা test-এ "এই input-এ সঠিক output কী হওয়া উচিত" — এই সিদ্ধান্ত যে দেয়। যেমন `assert change_base(0,2) == '0'` লাইনে `'0'` অংশটা oracle।
- **Oracle problem:** input বানানো সহজ (random, fuzzing), কিন্তু প্রতিটা input-এর **সঠিক expected output জানা কঠিন**। Program-কে দিয়েই output বের করলে সেটা program-এর ভুলও "সঠিক" ধরে নেয়। Paper এখানে Barr et al. (2014)-এর oracle problem survey cite করেছে।
- **এই paper-এর মূল idea:** LLM-কে **test oracle** হিসেবে ব্যবহার করা — কিন্তু পুরো oracle নয়, শুধু "কয়েকটা option-এর মধ্যে কোনটা ঠিক" বলার জন্য।

**সহজ কথায়:** Oracle মানে বিচারক, যে রায় দেয় কোন উত্তর ঠিক। এখানে AI বিচারক, কিন্তু সে পুরো case দেখে না। শুধু বলে এই দুই উত্তরের কোনটা ঠিক।

### ২.৩ Informal Oracle (Natural Language Specification)
LLM-কে যে docstring/description দেওয়া হয়, সেটাই একমাত্র "specification" — কিন্তু এটা informal, অসম্পূর্ণ, কখনো অস্পষ্ট। Paper-এর abstract বলছে LLM-এর ভুল code-এর বড় কারণ **natural language-কে informal oracle হিসেবে ব্যবহার করা**।

**সহজ কথায়:** তুমি অস্পষ্ট প্রশ্ন দিলে AI নিজের মতো ব্যাখ্যা করে ভুল উত্তর দিতে পারে। অনেক ভুলের উৎস এখানেই।

### ২.৪ Differential Testing
- দুটো program (যারা একই কাজ করার কথা) একই input-এ চালিয়ে output তুলনা করা। Output আলাদা হলে অন্তত একটা ভুল (অথবা specification অস্পষ্ট)।
- সুবিধা: কোনটা সঠিক তা না জেনেও **পার্থক্য** ধরা যায় — oracle লাগে না।

**সহজ কথায়:** দুজন ছাত্র একই অঙ্ক করেছে। উত্তর আলাদা হলে বোঝা যায় অন্তত একজন ভুল করেছে, উত্তরপত্র না দেখেই।
- এই paper-এ: LLM-এর দুটো sample $P_1, P_2$-কে differential test করা হয়।

### ২.৫ Distinguishing Input
এমন একটা input $i$ যেখানে দুটো sample ভিন্ন output দেয়: $s_1(i) \neq s_2(i)$। উদাহরণ (paper-এর Figure 1): `change_base(0, 2)` — একদল program `''` (empty string) দেয়, আরেকদল `'0'` দেয়। এই একটা input-ই ১০টা program-কে দুই দলে ভাগ করে দেয়।

**সহজ কথায়:** Distinguishing input হলো এমন প্রশ্ন, যেটা করলে দুজনের উত্তর আলাদা হয়ে ধরা পড়ে। যেমন `change_base(0, 2)`।

### ২.৬ Property-based Fuzzing (Hypothesis) ও Symbolic Execution (CrossHair)
- **Fuzzing / property-based testing:** অনেক random input তৈরি করে একটা property (যেমন "দুই program-এর output সমান") ভাঙে কিনা দেখা। **Hypothesis** হলো Python-এর জনপ্রিয় property-based testing library।
- **Symbolic execution:** input-কে concrete সংখ্যা না ধরে symbol ($x$) ধরে program-এর প্রতিটা path-এর শর্ত (path condition) বের করা, তারপর solver দিয়ে এমন input খোঁজা যা একটা নির্দিষ্ট path-এ যায় বা assertion ভাঙে। **CrossHair** হলো Python-এর symbolic execution tool।
- পার্থক্য: fuzzing দ্রুত কিন্তু দুর্লভ edge case মিস করতে পারে; symbolic execution বেশি systematic কিন্তু ধীর ও জটিল constraint-এ আটকে যায়।

**সহজ কথায়:** Fuzzing মানে এলোমেলোভাবে অনেক দরজা ঠেলে দেখা। Symbolic execution মানে নকশা দেখে বুঝে কোন দরজা খুলবে তা বের করা। প্রথমটা দ্রুত, দ্বিতীয়টা বুদ্ধিমান কিন্তু ধীর।

### ২.৭ Program Clustering by Behaviour (Equivalence Class)
- যে program-গুলো **সব distinguishing input-এ একই output** দেয়, তারা এক cluster-এ — এটা একটা equivalence relation, আর cluster-গুলো তার equivalence class।
- গুরুত্ব: ১০টা program-কে আলাদা আলাদা না দেখে ২–৩টা "behaviour group" দেখলেই হয়। Paper বলছে ১০টা LLM program গড়ে **৩টার বেশি ভিন্ন semantics** দেখায় না।

**সহজ কথায়:** ১০ জন ছাত্রের খাতা আলাদা না দেখে, একই উত্তর লিখেছে এমন ২–৩টা দলে ভাগ করলেই চলে।

### ২.৮ Majority Vote, AlphaCode ও CodeT
- **Majority vote:** সবচেয়ে বড় cluster-কে সঠিক ধরা — "বেশিরভাগ program যা বলে তাই ঠিক"।
- **AlphaCode (Li et al., 2022):** LLM-generated test input-এ program চালিয়ে output দিয়ে cluster বানায়, সবচেয়ে বড় cluster থেকে random একটা program নেয়।
- **CodeT (Chen et al., ICLR 2023):** LLM দিয়ে test case (input + expected output) বানায়; যে program-গুলো একই set test pass করে তারা এক cluster; cluster score = (cluster size) × (cluster যতগুলো test pass করে) — একে বলে **dual execution agreement**।
- দুটোই মূলত **consistency-based** — "সবাই একমত হলে ঠিক" ধরে নেয়। LLM-এর সব sample একই ভুল করলে এরা ধরতে পারে না।

**সহজ কথায়:** Consistency-based মানে বেশিরভাগ মানুষ একমত হলে সেটাই ঠিক। কিন্তু সবাই একই ভুল করলে এই যুক্তি আর কাজ করে না।

### ২.৯ Human-provided বনাম LLM-provided Oracle Query
- **Oracle-guided synthesis (Jha et al., ICSE 2010):** program synthesis-এ একটা distinguishing input পেলে **মানুষকে** জিজ্ঞেস করা হয় "এই input-এ সঠিক output কী?" — মানুষ oracle।
- **এই paper:** একই কাঠামো, কিন্তু প্রশ্নের উত্তর দেয় **LLM** (GPT-4)। মানুষের effort লাগে না, কিন্তু LLM ভুল করতে পারে (Section ৮.৬-এ failure analysis)।
- Paper-এর conclusion-এ বলা হয়েছে এটা ভবিষ্যতে "low-effort human-assisted gradual oracle inference" হতে পারে — অর্থাৎ মাঝামাঝি পথ: LLM প্রস্তাব দেবে, সন্দেহ হলে মানুষ দেখবে।

### ২.১০ Direct Inference বনাম Specification Selection
- **Direct inference:** LLM-কে বলা "`largest_prime_factor(25191)`-এর output কী?" — নিজে থেকে উত্তর বের করতে হয়।
- **Specification selection:** LLM-কে বলা "output `311` না `933`?" — option থেকে বাছতে হয়।
- Paper-এর মূল experimental পর্যবেক্ষণ: **বাছাই করা, নিজে বের করার চেয়ে সহজ** (84.3% বনাম 70.3%)।

**সহজ কথায়:** MCQ পরীক্ষায় option দেখে উত্তর বাছা সহজ। খালি জায়গায় নিজে থেকে লেখা কঠিন। AI-র ক্ষেত্রেও তাই।

### ২.১১ Chain-of-Thought (CoT) Prompting
Prompt-এর শেষে "Please explain step by step and answer" যোগ করা, যাতে LLM উত্তর দেওয়ার আগে ধাপে ধাপে যুক্তি লেখে। এতে reasoning-নির্ভর কাজে accuracy বাড়ে।

### ২.১২ pass@k বনাম Selection Accuracy
- **pass@k (Chen et al., 2021):** $k$টা sample নিলে অন্তত একটা সঠিক হওয়ার সম্ভাবনা। এটা **generation**-এর ক্ষমতা মাপে — "সঠিক program কোথাও আছে কিনা"।
- **Selection-এর পরে pass@1:** একটা program বেছে দিলে সেটা সঠিক হওয়ার সম্ভাবনা — এটা **selection**-এর ক্ষমতা মাপে।
- **ফাঁকটাই selection problem:** pass@k বেশি কিন্তু selected pass@1 কম হলে বোঝা যায় সঠিক program হাতে ছিল কিন্তু বাছাই ভুল। Agentless-এর 126 (কোনো একটা candidate সঠিক) বনাম 96 (বাছাই করে) ঠিক এই ফাঁক।
- এই paper আরও একটা metric ব্যবহার করে: **specification selection accuracy** — প্রতিটা multiple-choice প্রশ্নে LLM কত % সঠিক option বাছে।

### ২.১৩ Entropy ও Information Gain
- **Entropy:** একটা partition কতটা "ছড়ানো" তার মাপ। ১০টা program 5–5 ভাগ হলে entropy বেশি, 9–1 ভাগ হলে কম।
- **Information gain-এর সাথে সম্পর্ক:** যে input-এর উত্তর জানলে সবচেয়ে বেশি অনিশ্চয়তা দূর হয়, সেই প্রশ্ন আগে করা উচিত। Paper "information gain" শব্দটা ব্যবহার করেনি, কিন্তু highest-entropy distinguishing input আগে বাছাই করা মূলত একই idea (সূত্র Section ৬.৫-এ)।

**সহজ কথায়:** ২০ প্রশ্নের খেলায় যে প্রশ্নে সবচেয়ে বেশি সম্ভাবনা বাদ পড়ে, সেটা আগে করা ভালো। এখানেও একই নিয়ম।

### ২.১৪ HumanEval, MBPP ও তাদের "+" version
- **HumanEval:** 164টা হাতে লেখা Python function task। **MBPP:** এই paper-এ 399টা task।
- **HumanEval+ / MBPP+ (EvalPlus, Liu et al., 2023):** একই task কিন্তু অনেক বেশি test — মূল benchmark-এর দুর্বল test-এ "plausible but incorrect" program pass করে যায়, "+" version তা ধরে।
- **Standalone program:** শুধু built-in function ও standard library ব্যবহার করে এমন self-contained function — repository-level code নয়।

### ২.১৫ Overfitting (এই paper-এর অর্থে)
Paper-এর definition: একটা program **original** benchmark-এর test pass করে কিন্তু **enhanced (+)** benchmark-এ fail করে — অর্থাৎ developer কয়েকটা test চালিয়ে গ্রহণ করলেও আসলে ভুল। APR-এর "patch overfitting"-এর সাথে একই ধারণা (আমাদের CG1)।

**সহজ কথায়:** Overfitting মানে সহজ test-এ পাস, কঠিন test-এ ফেল। যে ছাত্র শুধু আগের বছরের প্রশ্ন মুখস্থ করে পাস করে, কিন্তু নতুন প্রশ্নে আটকে যায়।

---

## ৩. Problem Statement — কী সমস্যা ছিল?

### ৩.১ মূল সমস্যা
1. **LLM ভুল code দেয়, আর কোনটা ভুল বোঝা যায় না।** Copilot/CodeWhisperer-এর মতো tool (যারা code suggest করে) অনেক suggestion দেয়, developer-কে নিজে খুঁজে নিতে হয়।
2. **Consistency-based selection-এর তিনটা দুর্বলতা (paper-এর দাবি):**
   - LLM-generated test **প্রায়ই ভুল** (paper-এর মাপে প্রায় 25% test ভুল — Section ৮.৩),
   - অনেক test **duplicate**,
   - বেশিরভাগ test program-গুলোর **পার্থক্য ধরতে পারে না** (distinguishing input বিরল)।
3. **Majority ভুল হতে পারে:** LLM-এর বেশিরভাগ sample একই ভুল করলে (যেমন change_base-এ 10টার মধ্যে 6টা ভুল) majority vote ভুলটাই বাছে।
4. **Developer trust-এর অভাব:** "এই cluster-এর score 588" — এটা developer-কে কিছু বোঝায় না; কেন এটা সঠিক তার মানুষের-পড়া-যায় এমন প্রমাণ নেই।

**সহজ কথায়:** সমস্যা চারটা: test ভুল, test পুনরাবৃত্ত, পার্থক্য ধরে না, আর majority ভুল হতে পারে। চারটাই একই কথা বলে, নির্ভরযোগ্য বিচারক নেই।

### ৩.২ Motivating Example (HumanEval task 44, `change_base`) — পুরোটা
- Description: "change numerical base of input number x to base … base numbers are less than 10." — $x = 0$ হলে কী হবে বলা নেই।
- ChatGPT-এর 10টা sample: **Cluster 1 (6টা)** loop দিয়ে digit বানায়, $x=0$-এ `''` ফেরত দেয় (ভুল); **Cluster 2 (4টা)** আগে `if x == 0: return '0'` check করে (সঠিক)।
- **চমকপ্রদ তথ্য:** HumanEval-এর **canonical solution-ও** (benchmark-এর নিজের সঠিক ধরা উত্তর) এই ভুলটা করে (paper-এর দাবি)।
- GPT-4 দিয়ে 100টা test বানানো হলো। এর মধ্যে distinguishing input $x=0, base=2$ ছিল; আবার $x=10, base=16$ test-ও ছিল (যদিও base < 10 বলা আছে) — দুই cluster-ই সেটা fail করে।
- **AlphaCode:** বড় cluster (6) বাছে → ভুল।
- **CodeT:** Cluster 1: 98 test pass × size 6 = 588; Cluster 2: 99 × 4 = 396 → Cluster 1 বাছে → ভুল।
- **LLMCodeChoice:** একটা distinguishing input পায়, LLM-কে জিজ্ঞেস করে "`change_base(0, 2)`-এর মান `''` নাকি `'0'`?" — LLM যুক্তি দেয় "0 যেকোনো base-এ 0" → `'0'` → Cluster 2 → সঠিক।

**সহজ কথায়:** তিনটা পদ্ধতির পার্থক্য: AlphaCode আর CodeT সংখ্যায় জেতে, তাই ভুল দল বাছে। LLMCodeChoice সংখ্যা না দেখে একটা কাজের প্রশ্ন করে, তাই ঠিক দল বাছে।

### ৩.৩ কেন এটা গুরুত্বপূর্ণ?
Selection ভুল হলে generation যত ভালোই হোক user ভুল code পায়। আর ছোট input-output specification (যেমন `change_base(0,2) == '0'`) developer সহজে পড়ে যাচাই করতে পারে — এটা trust তৈরি করে।

**সহজ কথায়:** বাজারে দশটা আম, একটা মিষ্টি। চেখে দেখার সুযোগ না থাকলে ভুল আমই কিনবে। তাই বাছাই গুরুত্বপূর্ণ।

---

## ৪. Goal ও Research Questions

**Goal:** LLM-কে test oracle হিসেবে ব্যবহার করে, differential testing-এর distinguishing input-এর উপর multiple-choice প্রশ্নের মাধ্যমে, অনেক LLM sample-এর মধ্যে সঠিক program বাছাই করা — এবং সাথে একটা ছোট, মানুষের-পড়া-যায় input-output specification তৈরি করা।

Paper-এর explicit RQ (Section 5):
- **RQ1:** LLM-generated program-এর semantic পার্থক্য খুঁজতে distinguishing input কতটা কার্যকর?
- **RQ2:** LLMCodeChoice-এর specification selection কতটা কার্যকর?
- **RQ3:** সামগ্রিক program selection-এ LLMCodeChoice কতটা কার্যকর?
- **RQ4:** LLMCodeChoice কেন ব্যর্থ হয়?

**সহজ কথায়:** চারটা প্রশ্ন: (১) পার্থক্য কি ধরা পড়ে, (২) AI ঠিক বাছে কি, (৩) শেষ ফল ভালো কি, (৪) কখন ফেল করে।
- **অতিরিক্ত (Section 6.5):** Selected specification কি developer-এর trust বাড়াতে পারে? (contradictory explanation)

**Paper-এর claimed contribution (৩টা):**
1. Oracle-guided program selection-এর idea — distinguishing input + natural language দিয়ে সঠিক output বাছাই করে distinguishing test suite-কে specification বানানো।
2. HumanEval+ ও MBPP+-এ state-of-the-art selection technique-এর চেয়ে বেশি accuracy।
3. Inferred input-output specification problem description-এর incompleteness ও ambiguity ধরতে কাজে লাগে।

---

## ৫. Methodology — কীভাবে কাজটা করা হয়েছে

### ৫.১ Input-এর তিনটা Assumption (paper-এর Section 4)
1. Description-এ output ও input-এর সম্পর্ক সম্পর্কে তথ্য থাকতে হবে।
2. Generated code test করে distinguishing input ও তার output বের করার কোনো উপায় থাকতে হবে।
3. Input ও output text হিসেবে লেখা যেতে হবে, আর একাধিক output option LLM-এর context window-এ (LLM একবারে যতটুকু লেখা পড়তে পারে) আঁটতে হবে।

**সহজ কথায়:** তিনটা শর্ত: description থেকে ঠিক আচরণ বোঝা যায়, code চালিয়ে পার্থক্য পাওয়া যায়, আর output লেখা আকারে প্রকাশ করা যায়। ছবির output এখানে চলে না।

### ৫.২ চার ধাপের Pipeline (Figure 2)

| ধাপ | নাম | কী হয় | Tool / Model |
|---|---|---|---|
| 1 | Program sampling | একই task-এ LLM থেকে অনেক program | ChatGPT (gpt-3.5-turbo-0613), temperature=1 |
| 2 | Differential testing | Sample-pair-এর distinguishing input খোঁজা | Hypothesis (fuzzing), তারপর CrossHair (symbolic), প্রতিটা 3 মিনিট |
| 3 | Clustering | সব distinguishing input-এ একই output দেওয়া sample এক cluster | Equivalence relation (quotient set) |
| 4 | Oracle inference / specification selection | Highest-entropy input থেকে শুরু করে LLM-কে multiple-choice প্রশ্ন, ভুল cluster বাদ | GPT-4 (gpt-4-0613), CoT prompt |

**সহজ কথায়:** চারটা ধাপ হলো: code বানাও, কোথায় আলাদা খোঁজো, দল বানাও, তারপর AI-কে option থেকে বাছতে দিয়ে ভুল দল বাদ দাও।

### ৫.৩ Differential Testing-এর বিস্তারিত (Section 4.1)
- দুটো sample $P_1, P_2$-এর code একসাথে করে একটা নতুন program $Q_{P_1,P_2}$ বানানো হয়। Input variable ছাড়া বাকি সব variable rename করা হয় যাতে নামের সংঘর্ষ না হয় ("renamed apart")।
- এতে একটা assertion থাকে: $\varphi_{P_1,P_2} := \text{out}(P_1) == \text{out}(P_2)$।
- **প্রথমে Hypothesis:** random input দিয়ে assertion ভাঙার চেষ্টা, time bound $t$ (3 মিনিট)।
- **Fuzzing ব্যর্থ হলে CrossHair:** symbolic execution দিয়ে assertion ভাঙে এমন input খোঁজা, একই 3 মিনিট budget।
- **Pairwise কেন?** সব sample একসাথে একটা assertion-এ রাখা যেত, কিন্তু pairwise রাখলে যেকোনো differential testing tool plug-in করা যায়।

**সহজ কথায়:** সব code একসাথে না ধরে জোড়ায় জোড়ায় ধরা হয়, যাতে যেকোনো ভালো tool সহজে বসানো যায়।
- **Optimization (Algorithm 1, line 3):** কোনো pair-কে আগে পাওয়া কোনো input দিয়েই আলাদা করা গেলে আর নতুন করে test করা হয় না।
- `diffTest` একটা pair-এর জন্য **একটা মাত্র** input (singleton set) বা খালি set ফেরত দেয়।

**সহজ কথায়:** একটা জোড়ার জন্য একটাই input লাগে। এক input-ই দুই দল আলাদা করতে যথেষ্ট, তাই ১–২টা test দিয়ে কাজ চলে।

### ৫.৪ Specification Selection-এর বিস্তারিত (Section 4.2)
1. **Input বাছাই:** highest-entropy distinguishing input আগে (Section ৬.৫-এ সূত্র)। Intuition: high-entropy input-এর উত্তর জানলে একবারে বেশি program বাদ পড়ে, তাই LLM query কম লাগে।
2. **Option সংগ্রহ:** ঐ input-এ প্রতিটা (এখনো টিকে থাকা) cluster-এর output — differential testing-এর সময় রেকর্ড করা আছে, আবার চালাতে হয় না।
3. **Prompt (Figure 3)-এর তিন অংশ:**
   - Task framing: "Please select a correct output from a few choices for below function" + function signature + docstring,
   - প্রশ্ন: "What should be the value of `foo(i)`? `output 1` or `output 2`?",
   - CoT: "Please explain step by step and answer."
4. **Filter:** LLM যে output বাছে, সেই output দেয় না এমন সব cluster বাদ।
5. **Loop:** একটা cluster বাকি থাকা পর্যন্ত পরের input-এ পুনরাবৃত্তি। শেষ cluster user-কে দেওয়া হয়।
6. **সব option ভুল হলে:** paper-এর Section 6.3 অনুযায়ী LLM কোনো option না বাছলে LLMCodeChoice "সব program ভুল" অবস্থা চিনতে পারে (detection of wrong programs)।

**সহজ কথায়:** এখানে প্রতিবার একটা input নিয়ে একটা প্রশ্ন করা হয়। প্রতিটা উত্তরে কিছু দল বাদ পড়ে, যতক্ষণ না একটা দল থাকে।

### ৫.৫ Algorithm 1 (paper থেকে, প্রতিটা line ব্যাখ্যাসহ)

```text
Input:  task description task, LLM L, program samples S
Output: one selected cluster of program samples
1  I := {}
2  for (s1, s2) in S x S do
3     if NOT exists i in I with s1(i) != s2(i) then
4        I := I UNION diffTest(s1, s2)
5  C := S / ~   where s1 ~ s2  iff  for all i in I: s1(i) = s2(i)
6  for i in I do                      (highest entropy first)
7     outputs := { c(i) | c in C }
8     o := oracleInference(L, task, i, outputs)
9     C := { c in C | c(i) = o }
10    if |C| = 1 then
11       break
12 return the only remaining cluster in C
```

| Line | মানে |
|---|---|
| 1 | Distinguishing input-এর set খালি দিয়ে শুরু |
| 2–4 | প্রতিটা pair-এর জন্য: আগের কোনো input এদের আলাদা না করলে নতুন differential test চালাও |
| 5 | Input set $I$ দিয়ে sample-গুলোকে equivalence class (cluster)-এ ভাগ |
| 6–7 | প্রতিটা input-এ সব cluster-এর output = option list |
| 8 | LLM-কে multiple-choice প্রশ্ন |
| 9 | LLM-এর বাছা output যার সাথে মেলে না সেই cluster বাদ |
| 10–12 | একটা cluster থাকলে থামো ও ফেরত দাও |

**সহজ কথায়:** পুরো algorithm একটা ছাঁকনির মতো। প্রথমে দল বানায়, তারপর প্রতিটা প্রশ্নের উত্তরে ভুল দল ছেঁকে ফেলে।

**আমার পর্যবেক্ষণ (paper-এ অস্পষ্ট তিনটা জিনিস):**

**সহজ কথায়:** এটা আমার নিজের মন্তব্য। Paper-এর algorithm মোটামুটি পরিষ্কার, তবে নিচের তিনটা ছোট জায়গা লেখা নেই।
- Line 6-এ শুধু "for $i$ in $I$" লেখা; text বলছে highest-entropy আগে, কিন্তু প্রতিটা filter-এর পর বাকি cluster-এর উপর entropy **আবার হিসাব করা হয় কিনা** তা বলা নেই।
- Loop শেষে একাধিক cluster বাকি থাকলে (অর্থাৎ $I$ শেষ কিন্তু $|C| > 1$ — যা হওয়ার কথা নয় কারণ $I$-ই cluster বানিয়েছে) বা শূন্য cluster বাকি থাকলে (LLM কোনো option না বাছলে) কী হয়, algorithm-এ লেখা নেই।
- Line 2-এ $S \times S$ মানে ordered pair; বাস্তবে $\binom{N}{2}$টা unordered pair-ই যথেষ্ট। $N = 10$ হলে 45টা pair।

### ৫.৬ Contradictory Explanation (Section 6.5, preliminary idea)
Developer-কে feedback দেওয়ার জন্য দুই ধাপ:
1. **Explanation derivation:** প্রতিটা cluster-এর output-এর জন্য LLM-কে বলা "the task returns $o$ on input $i$ because…" — LLM বাক্য সম্পূর্ণ করে।
2. **Contradictory feedback:** task description আর সব explanation একসাথে দিয়ে জিজ্ঞেস করা "ambiguity বা অন্য সমস্যা আছে কি?"
- উদাহরণ (Figure 6, HumanEval task 40 `triples_sum_to_zero([0,0,0])`): একটা ব্যাখ্যা "element-গুলো distinct নয়" → False; অন্যটা "তিনটা শূন্য যোগে শূন্য" → True; LLM ধরে ফেলে "distinct elements"-এর অর্থ অস্পষ্ট।

---

## ৬. Mathematical Formulation — সূত্র ও ব্যাখ্যা

### ৬.১ Distinguishing Input-এর সংজ্ঞা
$$
i \text{ is distinguishing} \quad \text{if} \quad \exists\, s_1, s_2 \in S :\; s_1(i) \neq s_2(i)
$$

**সহজ কথায়:** একটা input তখনই "distinguishing", যখন অন্তত দুটো sample সেই input-এ আলাদা output দেয়। সূত্রটা শুধু এই শর্ত লিখে দেখায়।

| Symbol | মানে |
|---|---|
| $S$ | LLM-এর program sample-এর set (যেমন 10টা) |
| $s(i)$ | Sample $s$-কে input $i$-এ চালালে output |
| $I$ | সব distinguishing input-এর set |

**Worked example:** `change_base`-এ $S$ = 10টা program; $i = (x=0, base=2)$; Cluster 1-এর program-এ $s(i) =$ `''`, Cluster 2-এ `'0'` → $i$ distinguishing।

### ৬.২ Differential Testing-এর Equivalence Assertion
$$
\varphi_{P_1,P_2} \;:=\; \text{out}(P_1) == \text{out}(P_2)
$$
Combined program $Q_{P_1,P_2}$ এই assertion বহন করে; Hypothesis/CrossHair এমন input খোঁজে যেখানে $\neg\varphi_{P_1,P_2}$ সত্য। এটা আসলে একটা **search problem**:
$$
\text{diffTest}(P_1, P_2) = \begin{cases} \{ i \}, & \text{if found } i \text{ with } \text{out}(P_1(i)) \neq \text{out}(P_2(i)) \text{ within time } t \\ \{ \}, & \text{otherwise} \end{cases}
$$
এখানে $t$ = 3 মিনিট (প্রতিটা tool-এর জন্য)।

**সহজ কথায়:** প্রথমে দুই code-এর output সমান কিনা এই দাবি লেখা হয়। তারপর tool এমন input খোঁজে যেখানে দাবিটা ভাঙে। ৩ মিনিটে না পেলে খালি set ফেরত আসে।

### ৬.৩ Equivalence Relation ও Cluster (Quotient Set)
$$
s_1 \, R_I \, s_2 \quad \text{when} \quad \forall\, i \in I :\; s_1(i) = s_2(i)
$$
$$
C = S / R_I
$$
**সহজ কথায়:** দুটো code একই দলে যায় যদি পাওয়া সব input-এ তাদের output একই হয়। সূত্র দিয়ে সব code-কে এভাবে দলে ভাগ করা হয়।

(Paper এখানে $\sim$ চিহ্ন ব্যবহার করেছে; আমি $R_I$ লিখেছি।) $C$ হলো cluster-গুলোর set, প্রতিটা cluster একটা equivalence class।

**Worked example:** $I = \{(0,2)\}$; output `''` দেয় এমন 6টা sample এক class, `'0'` দেয় এমন 4টা আরেক class → $C$-তে 2টা cluster।

**গুরুত্বপূর্ণ সীমা:** $R_I$ শুধু **পাওয়া input**-এর উপর ভিত্তি করে। দুটো program আসলে ভিন্ন হলেও tool distinguishing input না পেলে তারা এক cluster-এ পড়ে (paper-এর internal threat)।

**সহজ কথায়:** Tool যদি পার্থক্য না খুঁজে পায়, দুটো আলাদা code ভুল করে এক দলে চলে যেতে পারে।

### ৬.৪ Cluster Filtering (Specification Selection Step)
Input $i$-এ option set ও LLM-এর বাছাই:
$$
O_i = \{\, c(i) \mid c \in C \,\}, \qquad o = \text{oracleInference}(L, \text{task}, i, O_i) \in O_i
$$
$$
C' = \{\, c \in C \mid c(i) = o \,\}
$$
**সহজ কথায়:** প্রতিটা input-এ সব দলের output-এর list বানানো হয়। AI যেটা বাছে তার সাথে না মিললে সেই দল বাদ যায়।

শেষে নির্বাচিত specification হলো pair-গুলোর set $\{(i_1, o_1), (i_2, o_2), \ldots\}$ — এটাই developer-কে দেখানো যায় এমন ছোট test suite।

### ৬.৫ Distinguishing Input-এর Entropy (paper-এর সূত্র)
$$
H(i) = -\sum_{k} \frac{n_k}{N} \log \frac{n_k}{N}
$$

**সহজ কথায়:** Entropy বের করে দলগুলো কতটা সমান ভাগে ছড়ানো। সমান ভাগ হলে সংখ্যা বড় হয়, আর সেই input আগে জিজ্ঞেস করা হয়।

| Symbol | মানে |
|---|---|
| $n_k$ | Input $i$ যে partition তৈরি করে তার $k$-তম cluster-এর size (program সংখ্যা) |
| $N$ | মোট program সংখ্যা |
| $\log$ | Paper base উল্লেখ করেনি; ranking-এর জন্য base-এ কিছু যায় আসে না |

**Worked example ১ (paper-এর change_base, আমার হিসাব):** $n_1 = 6, n_2 = 4, N = 10$:
$$
H = -(0.6 \ln 0.6 + 0.4 \ln 0.4) = 0.6 \times 0.511 + 0.4 \times 0.916 \approx 0.673 \text{ nats} \approx 0.971 \text{ bits}
$$

**Worked example ২ (কাল্পনিক তুলনা, আমার হিসাব):** ধরো দুটো input — $i_a$ ১০টা program-কে 9–1 ভাগ করে, $i_b$ 5–3–2 ভাগ করে:
- $H(i_a) = -(0.9 \ln 0.9 + 0.1 \ln 0.1) \approx 0.325$ nats
- $H(i_b) = -(0.5 \ln 0.5 + 0.3 \ln 0.3 + 0.2 \ln 0.2) \approx 1.030$ nats
- তাই LLMCodeChoice আগে $i_b$ নিয়ে প্রশ্ন করবে।

**Information gain হিসেবে ব্যাখ্যা (আমার পর্যবেক্ষণ):** যদি prior ধরি "একটা random sample-এর cluster-ই সঠিক হওয়ার সম্ভাবনা cluster size-এর সমানুপাতিক", তাহলে LLM-এর উত্তর (deterministic ধরে) যে information দেয় তা ঠিক $H(i)$। আর উত্তরের পর **প্রত্যাশিত বাকি program-এর ভগ্নাংশ**:

**সহজ কথায়:** Entropy বেশি মানে একটা উত্তরে বেশি code বাদ পড়ে। নিচের সংখ্যায় দেখো: ৯–১ ভাগে গড়ে ৮২% থেকে যায়, কিন্তু ৫–৩–২ ভাগে মাত্র ৩৮%।
$$
\mathbb{E}[\text{remaining fraction}] = \sum_k \left(\frac{n_k}{N}\right)^2
$$
- 9–1: $0.81 + 0.01 = 0.82$ (গড়ে 82% program থেকে যায়)
- 6–4: $0.36 + 0.16 = 0.52$
- 5–3–2: $0.25 + 0.09 + 0.04 = 0.38$

অর্থাৎ entropy যত বেশি, তত বেশি program একবারে বাদ পড়ে — paper-এর intuition-এর সংখ্যাগত রূপ। **সতর্কতা:** এই prior নিজেই majority-ধরনের অনুমান; paper-এর মূল যুক্তি হলো majority প্রায়ই ভুল — তাই entropy শুধু **প্রশ্নের ক্রম** ঠিক করে, **উত্তর** নয়।

### ৬.৬ pass@1 (Selection-এর পরে) — paper-এর সংজ্ঞা
নির্বাচিত cluster-এ $N$টা program, তার মধ্যে $n$টা benchmark-এর সব test pass করে:
$$
\text{pass@1}_{\text{task}} = \frac{n}{N}, \qquad \text{pass@1} = \frac{1}{T} \sum_{t=1}^{T} \text{pass@1}_{t}
$$
**সহজ কথায়:** বাছা দলের কত ভগ্নাংশ code ঠিক, সেটাই এক task-এর pass@1। তারপর সব task-এর গড় নেওয়া হয়।

($T$ = task সংখ্যা।) Cluster থেকে random একটা program নেওয়া হয় বলে এটা expected value।

**Worked example (change_base, আমার হিসাব):**

**সহজ কথায়:** LLMCodeChoice ঠিক দল বাছলে ১.০ পায়, আর ভুল দল বাছলে ০। Random-এ পায় ০.৪।
- LLMCodeChoice → Cluster 2 (4টা, সব সঠিক ধরে): $4/4 = 1.0$
- AlphaCode / CodeT → Cluster 1 (6টা, সব ভুল): $0/6 = 0$
- Random selection (সব 10টা থেকে): $4/10 = 0.4$

### ৬.৭ Generation-এর pass@k (তুলনার জন্য, Chen et al. 2021)
$$
\text{pass@}k = \mathbb{E}\left[1 - \frac{\binom{n-c}{k}}{\binom{n}{k}}\right]
$$
**সহজ কথায়:** এটা বের করে, $k$টা code দেখালে অন্তত একটা ঠিক থাকার সম্ভাবনা কত। ঠিক code আছে কিনা তা বোঝায়, বাছাই কতটা ভালো তা নয়।

$n$ = sample সংখ্যা, $c$ = সঠিক sample। **Worked example (আমার হিসাব):** change_base-এ $n = 10, c = 4, k = 1$: $1 - \binom{6}{1}/\binom{10}{1} = 1 - 0.6 = 0.4$ — random selection-এর সাথে মিলে যায়। $k = 3$: $1 - \binom{6}{3}/\binom{10}{3} = 1 - 20/120 \approx 0.833$। অর্থাৎ ৩টা দেখালে 83% সম্ভাবনায় একটা সঠিক থাকে, কিন্তু **একটা বাছতে হলে** selection লাগবেই।

### ৬.৮ CodeT-এর Cluster Score (baseline)
Paper-এর বর্ণনা অনুযায়ী:
$$
\text{score}(c) = |c| \times \text{pass}(c)
$$
**সহজ কথায়:** CodeT প্রতিটা দলের নম্বর বের করে "দলের আকার × পাস করা test" দিয়ে। যে দলের নম্বর বেশি, সেটা জেতে।

$|c|$ = cluster-এর program সংখ্যা, $\text{pass}(c)$ = cluster যতগুলো LLM-generated test pass করে।

**Worked example (paper-এর Figure 1):** Cluster 1: $6 \times 98 = 588$; Cluster 2: $4 \times 99 = 396$ → Cluster 1 বাছাই (ভুল)। Cluster 2 একটা test বেশি pass করেও size-এর কারণে হেরে যায় — **majority-র প্রভাব test-এর প্রমাণকে ছাপিয়ে যায়**।

### ৬.৯ AlphaCode ও Majority Vote (baseline)
$$
\hat{c} = \arg\max_{c \in C} |c|
$$
**সহজ কথায়:** Majority vote মানে সবচেয়ে বড় দলটা বেছে নেওয়া। সূত্রে argmax মানে "যার মান সবচেয়ে বড় তাকে বাছো"।

RQ2-এর single-input majority vote-ও একই: একটা input-এ যে output সবচেয়ে বেশি sample দেয়, সেটাই "সঠিক"।

### ৬.১০ Specification Selection Accuracy (RQ2)
$$
\text{Acc} = \frac{\text{correct choices}}{\text{selections where a correct option exists}} = \frac{321}{381} \approx 84.3\%
$$
**সহজ কথায়:** AI যতবার ঠিক option বেছেছে তাকে মোট সুযোগ দিয়ে ভাগ করা হয়েছে। এখানে ৩৮১টা প্রশ্নের মধ্যে ৩২১টা ঠিক।

সঠিক option = benchmark-এর ground-truth program ঐ input-এ যা output দেয়।

### ৬.১১ Overfitting Gap (paper-এর trustworthiness analysis)
$$
\text{OverfitGap} = \text{pass@1}_{\text{original}} - \text{pass@1}_{\text{enhanced}}
$$
**সহজ কথায়:** Original test-এ কত % পাস আর কঠিন test-এ কত % পাস, এই দুইয়ের বিয়োগফল। বিয়োগফল বড় হলে বোঝা যায় পদ্ধতিটা অনেক ভুয়া ঠিক code বেছেছে।

**Worked example (Table 3):** AlphaCode HumanEval: $80.3 - 75.6 = 4.7$; LLMCodeChoice: $89.2 - 87.7 = 1.5$।

### ৬.১২ Token-খরচের অনুপাত (আমার হিসাব, Table 3 থেকে)
$$
\frac{6319}{1533} \approx 4.12, \qquad \frac{5507}{1331} \approx 4.14
$$
**সহজ কথায়:** পুরোনো পদ্ধতির token-কে নতুন পদ্ধতির token দিয়ে ভাগ করা হয়েছে। উত্তর প্রায় ৪, মানে খরচ চার ভাগের এক ভাগ।

অর্থাৎ ~4 গুণ কম token — paper-এর "4x fewer tokens" দাবির সাথে মেলে। $1 - 1533/6319 \approx 75.7\%$ কম।

---

## ৭. Experimental Setup

| বিষয় | বিবরণ |
|---|---|
| **Benchmarks** | HumanEval (164 task), MBPP (399 task); enhanced: HumanEval+, MBPP+ (EvalPlus) — মোট 563 task |
| **Prompt preprocessing** | HumanEval-এর docstring থেকে example input-output বাদ (validation test-এর সাথে overlap); MBPP prompt HumanEval-এর format-এ (function signature + docstring) |
| **Program generator** | ChatGPT gpt-3.5-turbo-0613; max_token = 1024 (উত্তরের সর্বোচ্চ দৈর্ঘ্য); temperature = 1 (default, মানে যথেষ্ট randomness), বাকি default |
| **Sample সংখ্যা** | Paper-এর motivating example ও Section 4.1-এ 10টা sample; Setup অংশে আলাদা করে সংখ্যা লেখা নেই (নিচে নোট) |
| **Differential testing** | Hypothesis (property-based random testing), CrossHair (symbolic execution); প্রতিটার time bound 3 মিনিট |
| **Oracle LLM** | GPT-4 (gpt-4-0613), CoT prompt |
| **Baselines** | (1) Random selection, (2) AlphaCode, (3) AlphaCode + LLM-based specification inference, (4) CodeT; AlphaCode ও CodeT-এর test generation GPT-4 দিয়ে CodeT-এর artifact ব্যবহার করে replicate (Codex code-davinci-002 deprecated) |
| **Ablations** | LLMCodeChoice-Vote (বড় cluster বাছাই), LLMCodeChoice-Infer (option ছাড়া direct inference) |
| **Metric** | pass@1 (selected cluster-এ $n/N$), specification selection accuracy, cluster সংখ্যা, test সংখ্যা, token সংখ্যা, median time |
| **RQ3-এর task subset** | যেসব task-এ সব program সঠিক বা সব ভুল, সেগুলো বাদ → HumanEval-এ 89 task, MBPP-এ 162 task |
| **Failure labeling (RQ4)** | দুজন author আলাদাভাবে, মতভেদ একজন non-author PhD student-এর সাথে আলোচনা করে মীমাংসা |

**সহজ কথায়:** Setup-এর সারকথা: ১০টা code বানায় ছোট model, বিচার করে বড় model (GPT-4), আর তুলনা হয় তিনটা আগের পদ্ধতির সাথে।

**নোট (নিশ্চিত নই):**
- Sample সংখ্যা: Section 3 বলছে "we generated ten program samples", Section 4.1 বলছে "ten LLM-generated programs on average represent no more than three kinds of different semantics" — তাই 10 ধরে নেওয়া যুক্তিসঙ্গত, কিন্তু Section 5-এ explicit নয়।
- Baseline (3) "AlphaCode with LLM-based specification inference" Section 5-এ list করা আছে, কিন্তু Table 3-এ এই নামে কোনো row নেই; সম্ভবত এটাই LLMCodeChoice-Infer বা LLMCodeChoice-Vote-এর সাথে মিলে যায় — paper পরিষ্কার করেনি।
- 89 ও 162 task-এর filter original নাকি enhanced test দিয়ে করা — paper স্পষ্ট নয়।

---

## ৮. Results — মূল ফলাফল

### ৮.১ RQ1: Distinguishing Input-এর কার্যকারিতা (Table 1)

| Tool | HumanEval+ avg clusters | HumanEval+ avg tests | MBPP+ avg clusters | MBPP+ avg tests |
|---|---|---|---|---|
| Ground Truth (benchmark-এর validation suite) | 2.54 | 740.9 | 2.18 | 108.6 |
| AlphaCode | 2.56 | 89.2 | 2.56 | 85.3 |
| codeT | 2.31 | 89.2 | 2.11 | 85.3 |
| **LLMCodeChoice** | 2.48 | **1.2** | **2.71** | **1.3** |

**সহজ কথায়:** LLMCodeChoice মাত্র ১–২টা test দিয়ে ৮৫–৮৯টা test-এর সমান বা বেশি দল আলাদা করতে পেরেছে। অর্থাৎ কম test, কিন্তু সঠিক জায়গার test।

**পর্যবেক্ষণ:**
- MBPP+-এ LLMCodeChoice সবচেয়ে বেশি cluster খুঁজে পায়। Paper বলছে "24.3% more program clusters than codeT"। **আমার হিসাব:** $2.71 / 2.11 \approx 1.284$, অর্থাৎ ~28.4% বেশি — paper-এর 24.3% সংখ্যাটা Table 1 থেকে আমি পুনরুৎপাদন করতে পারিনি।
- HumanEval+-এ সবাই কাছাকাছি; LLMCodeChoice codeT-এর চেয়ে সামান্য বেশি, AlphaCode-এর চেয়ে সামান্য কম। 164-এর মধ্যে 23টা task-এ AlphaCode-এর চেয়ে কম cluster — কারণ strict input constraint (যেমন task 19-এ input হতে হবে "zero"…"nine" শব্দ দিয়ে তৈরি space-separated string), যা random mutation ও symbolic execution-এর জন্য কঠিন। আবার 21টা task-এ LLMCodeChoice AlphaCode-এর চেয়ে বেশি cluster পায় → LLM test আর differential testing **পরিপূরক**।
- Test সংখ্যা: task প্রতি সর্বোচ্চ 1.3টা — paper বলছে "about 60x fewer"। **আমার হিসাব:** $89.2/1.2 \approx 74$, $85.3/1.3 \approx 66$।
- **Ground truth-এর সাথে তুলনা (563 task):** ground truth 251 task-এ semantically ভিন্ন program দেখায়; তার মধ্যে 35টায় LLMCodeChoice কোনো distinguishing input পায়নি (অর্থাৎ 216টায় পেয়েছে — আমার হিসাব ~86.1%)। উল্টো দিকে, বাকি 312 task যেখানে ground truth সব program-কে সমান ভাবে, সেখানে LLMCodeChoice **119টায়** distinguishing input পেয়েছে (আমার হিসাব ~38.1%) → বড় যত্নে বানানো test suite-ও ভিন্ন program আলাদা করতে ব্যর্থ হতে পারে।

### ৮.২ RQ2: Specification Selection-এর কার্যকারিতা (Table 2)
- মোট 448টা selection attempt, 327 task-এ। বাকি 236 task-এ শুধু একটা cluster, তাই selection দরকার হয়নি (327 + 236 = 563)।
- 448-এর মধ্যে যেগুলোতে সঠিক option-ই ছিল না (সব sample ভুল, বা আগের ভুল selection-এ সঠিক cluster বাদ পড়েছে) সেগুলো বাদ → **381টা** selection-এ সঠিক option উপস্থিত।

| Benchmark | LLMCodeChoice | Direct Inference | Majority Vote |
|---|---|---|---|
| HumanEval+ | **87.6%** | 77.0% | 71.3% |
| MBPP+ | **82.7%** | 68.2% | 66.8% |
| Total | **84.3%** | 70.3% | 68.2% |

**সহজ কথায়:** Option দিলে AI ১০০টার মধ্যে প্রায় ৮৪টা ঠিক বাছে। Majority vote ধরলে ঠিক হয় প্রায় ৬৮টা।

- Text: "321 (84.3%) of the 387 attempts"। **আমার হিসাব:** $321/381 = 84.25\% \approx 84.3\%$, কিন্তু $321/387 = 82.9\%$ — তাই "387" সম্ভবত typo, সঠিক denominator 381 (এর সাথে RQ4-এর "60 of the 381" ও $381 - 321 = 60$ মেলে)।

**সহজ কথায়:** Paper-এ একটা ছোট ভুল আছে। ৩২১ কে ৩৮১ দিয়ে ভাগ করলেই ৮৪.৩% হয়, ৩৮৭ দিয়ে নয়।
- Direct inference-এর চেয়ে 14.0 percentage point বেশি ($84.3 - 70.3$)। Majority vote direct inference-এর চেয়েও খারাপ → **majority প্রায়ই ভুল**।
- কেন option দিলে ভালো হয়: LLM জটিল input-এ, বিশেষ করে গণিতে, নিজে হিসাব করতে ভুল করে। **Figure 4 উদাহরণ:** `largest_prime_factor(25191)` — direct inference ভুলভাবে বলে 8397 আর কোনো prime দিয়ে ভাগ যায় না, উত্তর `8397`; option (`311` বা `933`) দিলে LLM ঠিকভাবে $25191 = 3^4 \times 311$ বের করে `311` বাছে। (আমার যাচাই: $81 \times 311 = 25191$ ✓।)

### ৮.৩ RQ3: সামগ্রিক pass@1 ও token (Table 3)
Format: enhanced (original)। HumanEval-এ 89 task, MBPP-এ 162 task (সব-সঠিক বা সব-ভুল task বাদ)।

| Technique | HumanEval+ (HumanEval) pass@1 % | HumanEval avg tokens | MBPP+ (MBPP) pass@1 % | MBPP avg tokens |
|---|---|---|---|---|
| Random Selection | 57.0 (63.1) | – | 58.1 (69.9) | – |
| AlphaCode | 75.6 (80.3) | 6319 | 71.4 (81.6) | 5507 |
| codeT | 80.8 (86.8) | 6319 | 75.0 (83.3) | 5507 |
| LLMCodeChoice-Vote | 73.1 (84.7) | – | 72.0 (81.2) | – |
| LLMCodeChoice-Infer | 79.6 (82.5) | – | 76.9 (81.9) | – |
| **LLMCodeChoice** | **87.7 (89.2)** | **1533** | **78.6 (83.2)** | **1331** |

**সহজ কথায়:** প্রতিটা column-এ LLMCodeChoice সবচেয়ে ভালো, আর token অনেক কম লাগে। তবে original MBPP-তে CodeT-এর সাথে প্রায় সমান (83.3 বনাম 83.2)।

**মূল তুলনা:**
- CodeT-এর চেয়ে: HumanEval+ $+6.9$ pp (pp = percentage point, যেমন 80 থেকে 87 হলে 7 pp) ($80.8 \to 87.7$), MBPP+ $+3.6$ pp ($75.0 \to 78.6$) — abstract-এর "3.6–7%"।
- **আমার পর্যবেক্ষণ:** original MBPP-এ codeT 83.3 আর LLMCodeChoice 83.2 — অর্থাৎ **দুর্বল original test-এ LLMCodeChoice codeT-কে হারায় না**; সুবিধাটা enhanced (কঠোর) test-এ স্পষ্ট হয়।
- AlphaCode ও codeT-এর token একই (6319 / 5507), কারণ দুজনেই একই LLM-generated test set ব্যবহার করে; পার্থক্য শুধু clustering ও scoring-এ।
- **LLM test-এর মান:** ground-truth program দিয়ে LLM test চালিয়ে দেখা গেছে দুই benchmark-এই **80%-এর বেশি task-এ অন্তত একটা ভুল test**; task প্রতি গড়ে 23-এর বেশি ভুল test; ~85টা test-এর মধ্যে → প্রায় 25% test ভুল।

**সহজ কথায়:** মানে AI-এর বানানো test কে চোখ বুজে বিশ্বাস করা যায় না। প্রতি চারটার একটা ভুল।

### ৮.৪ Ablation Study (Table 3 থেকে)

| Step | HumanEval+ gain | MBPP+ gain | কীসের তুলনা |
|---|---|---|---|
| Clustering (differential testing + বড় cluster) | +16.1 | +13.9 | Vote − Random ($73.1 - 57.0$; $72.0 - 58.1$) |
| Specification inference (LLM oracle, option ছাড়া) | +6.5 | +4.9 | Infer − Vote ($79.6 - 73.1$; $76.9 - 72.0$) |
| Option দেওয়া (multiple-choice) | +8.1 | +1.7 | Full − Infer ($87.7 - 79.6$; $78.6 - 76.9$) |

**সহজ কথায়:** তিনটা ধাপই কিছু না কিছু লাভ দেয়। HumanEval+-এ সবচেয়ে বড় লাভ আসে দল বানানো থেকে (+16.1)। Option দেওয়া থেকে আসে +8.1।

সবগুলো paper-এর নিজের সংখ্যা, আমি Table 3 থেকে যাচাই করেছি — মেলে। **আমার পর্যবেক্ষণ:** MBPP+-এ option-এর অবদান মাত্র 1.7 pp — MBPP-এর description বেশি অস্পষ্ট হওয়ায় (RQ4-এ MBPP-এর incomplete problem 17টা) option দিলেও LLM-এর হাতে সঠিক উত্তর বের করার তথ্য থাকে না।

**সহজ কথায়:** তিন ধাপেই লাভ। বড় লাভ আসে দল বানানো থেকে, তারপর AI-কে বিচারক করা থেকে।

### ৮.৫ Trustworthiness (Overfitting), Time ও Wrong-Program Detection

**Overfitting gap = original − enhanced (আমার হিসাব, Table 3 থেকে; paper নিজে শুধু AlphaCode ও LLMCodeChoice-এর HumanEval সংখ্যা দিয়েছে):**

| Technique | HumanEval gap (pp) | MBPP gap (pp) |
|---|---|---|
| Random | 6.1 | 11.8 |
| AlphaCode | 4.7 | 10.2 |
| codeT | 6.0 | 8.3 |
| LLMCodeChoice-Vote | 11.6 | 9.2 |
| LLMCodeChoice-Infer | 2.9 | 5.0 |
| **LLMCodeChoice** | **1.5** | **4.6** |

**সহজ কথায়:** Gap যত ছোট, পদ্ধতি তত কম "ভুয়া ঠিক" code বাছে। LLMCodeChoice-এর gap সবচেয়ে ছোট।

- Paper: LLMCodeChoice HumanEval ও MBPP দুটোতেই "least overfitting"। (ছোট অসঙ্গতি: text-এ "AlphaCode has a pass@1 of 80.3% on HumanEval+ and 75.6% on HumanEval" লেখা, Table 3 অনুযায়ী উল্টো — 75.6 enhanced, 80.3 original। Gap 4.7 দুইভাবেই একই।)
- **আমার পর্যবেক্ষণ:** LLMCodeChoice-Vote-এর gap সবচেয়ে বেশি (11.6) — অর্থাৎ differential testing-এর cluster-এ **শুধু majority** নিলে overfitting সবচেয়ে বেশি; oracle query-ই overfitting কমায়।
- **Time:** median 221.5 সেকেন্ড (LLMCodeChoice) বনাম 142.1 সেকেন্ড (AlphaCode ও CodeT)। **আমার হিসাব:** ~1.56 গুণ ধীর — token কম লাগলেও differential testing-এর 3-মিনিট budget-এর জন্য সময় বেশি।

**সহজ কথায়:** পদ্ধতিটা token-এ সস্তা, কিন্তু সময়ে একটু ধীর। কারণ test খুঁজতে ৩ মিনিট পর্যন্ত লাগতে পারে।
- **Wrong-program detection:** সব program ভুল এমন task — HumanEval+-এ 28, MBPP+-এ 90 (মোট 118); LLM কোনো option না বেছে এর মধ্যে 30টা চিনতে পেরেছে (আমার হিসাব ~25.4%)।

**সহজ কথায়:** সব code ভুল হলে AI মাত্র প্রতি চারটার একটায় সেটা ধরতে পেরেছে। বাকিগুলোতে সে একটা ভুল option-কেই ঠিক ভেবেছে।
- **Paper-এর summary claim:** "improves pass@1 over random selections by 6.7% to 16.6%"। **আমার হিসাব:** Table 3 থেকে random-এর উপর উন্নতি 13.3 থেকে 30.7 pp (যেমন $87.7 - 57.0 = 30.7$; $83.2 - 69.9 = 13.3$) — "6.7–16.6" কোন তুলনা থেকে এসেছে তা আমি Table 3 থেকে পুনরুৎপাদন করতে পারিনি।
- **Abstract-এর "60% more efficient than codeT w.r.t. the token cost"** আর Section 6.3-এর "4x fewer tokens" — দুটো একসাথে মেলে না (4 গুণ কম = ~75.7% কম)। Table 3-এর raw সংখ্যা (1533 বনাম 6319) ব্যবহার করাই নিরাপদ।

### ৮.৬ RQ4: Failure-এর কারণ (Table 4 ও Table 5)
381টার মধ্যে **60টা** ভুল selection।

| কারণ | HumanEval+ | MBPP+ | মোট | % |
|---|---|---|---|---|
| Wrong Choice (description স্পষ্ট, LLM ভুল বেছেছে) | 6 | 15 | 21 | 35.0% |
| Incomplete Problem (description-এ behaviour নির্দিষ্ট নেই) | 5 | 17 | 22 | 36.7% |
| Ambiguous Problem (একাধিক বৈধ ব্যাখ্যা) | 2 | 2 | 4 | 6.7% |
| Wrong Ground Truth (benchmark-এর solution ভুল) | 2 | 11 | 13 | 21.6% |

**সহজ কথায়:** ৬০টা ভুলের মধ্যে মাত্র ২১টায় AI সত্যিই ভুল বেছেছে। বাকিগুলোতে problem অসম্পূর্ণ, অস্পষ্ট বা benchmark-এর উত্তরই ভুল।

(আমার হিসাব: $13/60 = 21.67\%$, paper লিখেছে 21.6%।)

**21টা Wrong Choice-এর ভাগ (Table 5):**

| ভুলের ধরন | সংখ্যা | উদাহরণ (paper থেকে) |
|---|---|---|
| Incorrect calculation | 11 (8 arithmetic, 2 string manipulation, 1 logical) | MBPP 782: input `[0,-1]`-এ LLM বলে odd-length subarray `[0]`, `[-1]`, `[0,-1]` — শেষটা জোড় দৈর্ঘ্যের |
| Misunderstanding of problem | 5 | MBPP 454: `'z'` case-sensitive, LLM বলে `'Z'`-এও `'z'` আছে |
| Hallucinated precondition | 3 | MBPP 803: perfect square check-এ $-1$-এর জন্য LLM exception চায়, সঠিক উত্তর False |
| Incorrect reasoning | 1 | জটিল গণিত |
| Use of incorrect fact | 1 | ভুল সূত্র |

**সহজ কথায়:** AI-এর ভুলের মধ্যে সবচেয়ে বেশি হিসাবের ভুল (১১টা)। তাই AI-কে হিসাব চালানোর tool দিলে সুবিধা হতে পারে।

**অন্য উদাহরণ:**
- **Incomplete:** MBPP 264 — dog's years-এর সংজ্ঞা দেওয়া নেই (অথচ মূল online description-এ ছিল)।
- **Ambiguous:** HumanEval 40 `triples_sum_to_zero([0,0,0])` — "distinct elements" মানে ভিন্ন value নাকি ভিন্ন index?
- **Wrong ground truth:** MBPP 799 `left_rotate(n=16, d=28)`, 32-bit — সঠিক উত্তর `1`, ground truth দেয় `4294967297` (33-bit সংখ্যা)।

### ৮.৭ Contradictory Explanation-এর Preliminary Evaluation
Incomplete + Ambiguous মোট 26টা task-এ; volunteer PhD student (external developer হিসেবে) যাচাই করে — **14টা resolved** (feedback সঠিকভাবে ambiguity/incompleteness ব্যাখ্যা করেছে)। আমার হিসাব: ~53.8%।

**সহজ কথায়:** ১৪টা ক্ষেত্রে AI-এর ব্যাখ্যা দেখে মানুষ বুঝেছে problem-এর description-এই সমস্যা। অর্থাৎ পদ্ধতিটা ভুল প্রশ্নও ধরিয়ে দিতে পারে।

---

## ৯. Key Findings / Insights (Supervisor-কে বলার মতো ৮টা পয়েন্ট)

1. **Selection করা, generate করার চেয়ে সহজ:** option দিলে LLM-এর oracle accuracy 84.3%, নিজে বের করলে 70.3%।
2. **Majority ভুল হয়:** single-input majority vote মাত্র 68.2% — direct inference-এর চেয়েও কম। "বেশিরভাগ sample একমত" ≠ "সঠিক"।
3. **LLM-generated test অবিশ্বস্ত:** 80%-এর বেশি task-এ অন্তত একটা ভুল test; প্রায় 25% test ভুল।
4. **অল্প কিন্তু সঠিক জায়গার test যথেষ্ট:** task প্রতি ~1.2–1.3টা distinguishing input দিয়ে LLM-এর ~85–89টা test-এর সমান বা বেশি cluster পাওয়া যায়।
5. **Overfitting কম:** original ও enhanced-এর ফাঁক LLMCodeChoice-এ সবচেয়ে কম (HumanEval 1.5 pp)।
6. **Token কম, সময় বেশি:** ~4 গুণ কম token, কিন্তু median সময় 221.5s বনাম 142.1s।
7. **ভুলের প্রায় দুই-তৃতীয়াংশ LLM-এর দোষ নয়:** 60টা ভুলের মধ্যে 22 incomplete, 4 ambiguous, 13 wrong ground truth — মোট 39 (65%, আমার হিসাব)। অর্থাৎ technique-টা **specification-এর সমস্যা খুঁজে বের করার detector** হিসেবেও কাজ করে।
8. **Benchmark নিজেই ভুল হতে পারে:** 13টা wrong ground truth, এমনকি HumanEval task 44-এর canonical solution-ও edge case-এ ভুল (paper-এর দাবি)।

**সহজ কথায়:** আটটা শিক্ষা এক কথায়: বাছাই সহজ, majority অবিশ্বস্ত, AI-এর test ভুল, অল্প test যথেষ্ট, overfitting কম, token কম, ভুলের বড় অংশ problem-এর দোষ, আর benchmark-ও ভুল হয়।

---

## ১০. কেন এই Solution অন্যগুলোর থেকে ভালো? — এবং Agent Patch Selection-এ কীভাবে নেওয়া যায়

### ১০.১ Selection technique-এর তুলনা

| বৈশিষ্ট্য | Random | AlphaCode | CodeT | **LLMCodeChoice** |
|---|---|---|---|---|
| Test input-এর উৎস | – | LLM | LLM | **Differential testing (Hypothesis + CrossHair)** |
| Expected output-এর উৎস | – | নেই (শুধু output মিল) | LLM-এর লেখা assertion | **LLM বাছাই করে, program-এর output option থেকে** |
| Selection নিয়ম | Random | সবচেয়ে বড় cluster | size × passed tests | **Oracle query দিয়ে ভুল cluster বাদ** |
| Test সংখ্যা (task প্রতি) | – | ~85–89 | ~85–89 | **~1.2–1.3** |
| Token (HumanEval) | – | 6319 | 6319 | **1533** |
| Majority ভুল হলে | ভুল | ভুল | প্রায়ই ভুল | **সঠিক হতে পারে** |
| Developer-কে প্রমাণ | নেই | নেই | একটা score | **ছোট input-output specification + LLM-এর ব্যাখ্যা** |
| সব program ভুল চেনা | না | না | না | **আংশিক (118-এর মধ্যে 30)** |

**সহজ কথায়:** প্রায় প্রতিটা সারিতে LLMCodeChoice এগিয়ে। একমাত্র দুর্বলতা হলো সময় বেশি লাগা, যা এই table-এ নেই।

**মূল শক্তি:**
1. **Oracle-এর কাজ সহজ করা:** পুরো program বিচার নয়, শুধু একটা input-এ কয়েকটা output-এর মধ্যে বাছাই।
2. **Test-এর নির্ভুলতা:** input আসে testing tool থেকে, output আসে আসল program execution থেকে — LLM শুধু বাছে, তাই "LLM-এর লেখা ভুল assertion" সমস্যা নেই।
3. **ব্যাখ্যাযোগ্যতা (explainability):** নির্বাচিত `(input, output)` pair মানুষ পড়ে যাচাই করতে পারে, codebase-এ regression test হিসেবে রাখতে পারে।
4. **Specification bug detector:** ambiguous/incomplete description ও ভুল ground truth ধরা পড়ে।

**সহজ কথায়:** চারটা শক্তির মূল কথা: AI-এর কাজ ছোট করা, test-এর output সত্যিকারের execution থেকে নেওয়া, প্রমাণ মানুষের পড়ার মতো, আর description-এর ভুল ধরা।

### ১০.২ CG2 ও CG1-এর Lens — Agent Patch Selection-এ Transfer (আমার পর্যবেক্ষণ)

Sub-domain 1-এর সবচেয়ে পরিষ্কার সংখ্যা: **Agentless 40টা candidate থেকে কোনো একটা সঠিক হলে 126টা task solve হতো, বাছাই করে পেয়েছে 96টা** — 30টা task-এ সঠিক patch হাতে ছিল কিন্তু majority voting হারিয়েছে। AutoCodeRover-এ @1 = 19.00% বনাম @3 = 26.00% (Lite)। এই paper ঠিক এই ফাঁক বন্ধ করার একটা পরীক্ষিত পদ্ধতি দেয়, তবে **standalone function-এর জগতে**।

| LLMCodeChoice-এর ধারণা | Agent patch-এর জগতে সমতুল্য | চ্যালেঞ্জ |
|---|---|---|
| Program sample $S$ | Agent-এর candidate patch (Agentless-এর 40টা, বা k বার run) | Patch পুরো repository বদলায়, একটা function নয় |
| Natural language description | GitHub issue text | Issue প্রায়ই underspecified (SWE-Bench Pro-তে 22টা misleading description ঠিক করতে হয়েছে) |
| Distinguishing input | এমন test/input যেখানে দুই patch-এর আচরণ ভিন্ন | Input হলো object, file, database state — Hypothesis-এর জন্য generator লিখতে হবে; বা Agentless-এর LLM-generated reproduction test-কে seed হিসেবে ব্যবহার |
| Output | Return value, exception, stdout, পরিবর্তিত state | "Output" সংজ্ঞায়িত করা কঠিন; side effect তুলনা করতে হবে |
| Behaviour cluster | একই আচরণের patch group (Agentless-এর normalized majority voting-ও আসলে syntax-ভিত্তিক cluster) | Behaviour-ভিত্তিক cluster syntax-ভিত্তিক cluster-এর চেয়ে বেশি অর্থবহ |
| Oracle query: "f(x) = y1 না y2?" | "Issue অনুযায়ী এই input-এ code-টা y1 করবে নাকি y2?" | Context-এ পুরো code ও issue আঁটাতে হবে; LLM-এর arithmetic ভুল (Table 5-এর 11/21) এখানেও আসবে |
| Highest-entropy input আগে | যে test সবচেয়ে বেশি patch-কে ভাগ করে সেটা আগে | একই |
| "কোনো option সঠিক নয়" | Abstain — সব candidate ভুল, মানুষকে জানাও (CG7) | Paper-এ মাত্র 30/118 ধরা পড়েছে |
| Selected I/O specification | Assurance report-এ "প্রমাণ" — "এই patch বেছেছি কারণ issue বলছে input X-এ Y হওয়া উচিত" | ঠিক আমাদের research direction-এর "assurance report"-এর সাথে মেলে |

**সহজ কথায়:** ধারণাটা সোজা। Function-এর জায়গায় patch, docstring-এর জায়গায় issue, আর input-output জোড়ার জায়গায় test আচরণ। কঠিন অংশ হলো repository-এর input আর output সংজ্ঞায়িত করা।

**কেন এটা CG1 (plausible ≠ correct)-এও কাজে লাগে:** একটা patch সব existing test pass করলেও (plausible), অন্য একটা plausible patch-এর সাথে differential testing-এ ভিন্ন আচরণ দেখালে **অন্তত একটা ভুল** — এটা oracle ছাড়াই overfitting-এর সতর্কসংকেত। Fact sheet-এর PatchDiff (ICSE 2026)-ও ঠিক এই নীতিতে কাজ করে: plausible patch-এর 29.6% gold patch থেকে ভিন্ন আচরণ করে (independent, তবে 2025-এর model-এ)। পার্থক্য: PatchDiff gold patch-এর সাথে তুলনা করে (evaluation-এর জন্য), LLMCodeChoice gold ছাড়াই candidate-দের মধ্যে তুলনা করে (deployment-এর জন্য)।

**সহজ কথায়:** দুটো patch সব test পাস করেও আলাদা আচরণ করলে বোঝা যায় অন্তত একটা ভুল। এই সংকেতের জন্য আলাদা উত্তরপত্রের দরকার হয় না।

**আমার প্রত্যাশা, প্রমাণ নয়:** Agentless-এর 30টা "হারানো" task-এর কতগুলো এভাবে ফেরত আসবে তা কেউ মাপেনি — এটাই একটা পরিষ্কার SPL3 experiment (Section ১৬)।

**সহজ কথায়:** Agentless-এর হারিয়ে যাওয়া ৩০টা task-এর কতগুলো ফেরত আনা যাবে, কেউ মাপেনি। সেটাই আমাদের পরীক্ষার প্রশ্ন।

---

## ১১. কোন পরিস্থিতিতে এই technique ভালো কাজ করে, কোথায় করে না

### ✅ ভালো কাজ করে যখন:
- **Standalone, pure function** — input/output সহজে text-এ লেখা যায় (HumanEval/MBPP ধরনের)।
- Sample-গুলোর মধ্যে **semantic পার্থক্য আছে** কিন্তু পার্থক্য **edge case-এ** (empty input, zero, negative)।
- **Majority ভুল** — বেশিরভাগ sample একই ভুল করে, কিন্তু অল্প কয়েকটা সঠিক।
- Description-এ উত্তর বের করার মতো তথ্য আছে, আর সঠিক উত্তর বের করতে জটিল হিসাব লাগে না।
- Developer-কে ব্যাখ্যাযোগ্য প্রমাণ দেখানো দরকার।

**সহজ কথায়:** সংক্ষেপে: যে function ছোট, input-output পরিষ্কার, আর ভুলটা কোনো edge case-এ, সেখানেই পদ্ধতিটা সবচেয়ে ভালো।

### ❌ ভালো কাজ করে না / সীমিত যখন:
- **Strict input constraint** — বৈধ input-এর গঠন জটিল (task 19-এর মতো), fuzzing/symbolic execution বৈধ distinguishing input পায় না।
- **জটিল arithmetic** — oracle LLM নিজেই হিসাবে ভুল করে (21টা wrong choice-এর 11টা)।
- **Description অসম্পূর্ণ/অস্পষ্ট** — তখন "সঠিক" output-ই নির্ধারিত নয় (22 + 4টা failure)।
- **সব sample ভুল** — 118-এর মধ্যে মাত্র 30টা ধরা পড়েছে।
- **Non-standalone code** (multi-component project, library) — paper নিজেই বলছে adjustment লাগবে।
- **Non-text output** (যেমন image plot)।
- **Latency-sensitive** IDE suggestion — median 221.5 সেকেন্ড।

**সহজ কথায়:** সংক্ষেপে: input-এর গঠন জটিল, হিসাব কঠিন, description অস্পষ্ট বা সব code ভুল হলে পদ্ধতিটা দুর্বল। আর বড় project-এও সরাসরি চলে না।

---

## ১২. Limitations — দুর্বলতা

### ১২.১ Authors যা নিজেরা স্বীকার করেছেন (Section 7 Threats ও অন্যত্র)
1. **Differential testing সব distinguishing input খুঁজে পাবে এমন guarantee নেই** → cluster পুরোপুরি সঠিক নাও হতে পারে (251-এর মধ্যে 35 task-এ পায়নি)।
2. **Codex deprecated** — CodeT-কে GPT-4 দিয়ে replicate করা হয়েছে; authors মনে করেন এতে CodeT-এর সুবিধাই হয়েছে।
3. **শুধু GPT-4** oracle হিসেবে evaluate করা হয়েছে (open-source model নয়)।
4. **শুধু standalone program**; non-standalone (project, library) future work।
5. **শুধু text output**; অন্য modality-র জন্য multimodal LLM লাগতে পারে।
6. Strict input constraint-এ differential testing দুর্বল; LLM test-এর সাথে combine করা future work।
7. LLM arithmetic-এ ভুল করে — জটিল হিসাবের requirement-এ oracle কম কার্যকর।
8. Description অস্পষ্ট হলে accuracy কমে।

**সহজ কথায়:** Authors নিজেরাই আটটা সীমা মেনেছেন। সবচেয়ে বড়: শুধু standalone function, শুধু GPT-4, আর AI-এর হিসাবের ভুল।

### ১২.২ আমার Critical Analysis (Professor-level observation)
1. **Statistical rigor নেই:** Table 3-এর সংখ্যা একটা run-এর; কোনো confidence interval, significance test বা repeated run নেই। HumanEval-এ মাত্র 89 task — **আমার হিসাব:** CodeT-এর উপর 6.9 pp ≈ $0.069 \times 89 \approx 6.1$ task-এর সমান; MBPP-এ $0.036 \times 162 \approx 5.8$। এত ছোট পার্থক্য temperature=1 sampling-এর noise-এর মধ্যেই থাকতে পারে। (আমাদের CG4/CG8।)

**সহজ কথায়:** ৮৯টা task-এ ৭ pp মানে মোটে ৬টা task বেশি। এত ছোট পার্থক্য দৈবাৎও হতে পারে, কারণ পরীক্ষা মাত্র একবার চালানো হয়েছে।
2. **Subset-এ pass@1:** Table 3 শুধু "selection-এর পার্থক্য হয়" এমন task-এ (89/164, 162/399)। এটা selection-এর effect বোঝার জন্য যুক্তিসঙ্গত, কিন্তু পুরো benchmark-এ আসল উন্নতি অনেক ছোট — reader যেন "87.7% HumanEval" ভুল না বোঝে।
3. **Paper-এর ভেতরের সংখ্যাগত অসঙ্গতি:** (ক) "321 of 387" বনাম 381; (খ) "60% more efficient" (abstract) বনাম "4x fewer tokens"; (গ) MBPP+ cluster "24.3% more than codeT" — Table 1 থেকে 28.4%; (ঘ) random-এর উপর "6.7% to 16.6%" Table 3 থেকে পুনরুৎপাদন হয় না; (ঙ) AlphaCode-এর 80.3/75.6 text-এ উল্টো লেখা। Supervisor-কে দেখানোর সময় সবসময় table-এর raw সংখ্যা ব্যবহার করা উচিত।

**সহজ কথায়:** Paper-এ ছোট কিছু সংখ্যার গরমিল আছে। Supervisor-কে বলার সময় সবসময় table-এর মূল সংখ্যা ব্যবহার করবে, text-এর সংখ্যা নয়।
4. **Oracle-এর ground truth নিজেই ভুল হতে পারে:** RQ2-এর accuracy ground-truth program-এর output-কে "সঠিক" ধরে মাপা, অথচ RQ4 নিজেই 13টা wrong ground truth পেয়েছে। তাই 84.3% সংখ্যাটা কিছুটা **কম করে** মাপা হতে পারে — আবার incomplete/ambiguous case-এ "সঠিক" অর্থহীন। Accuracy-র মাপকাঠি নিজেই অনিশ্চিত (আমাদের CG10/CG11-এর উদাহরণ)।
5. **Invalid-input সমস্যা:** Distinguishing input অনেক সময় precondition ভাঙে (যেমন change_base-এ base ≥ 10, perfect-square-এ negative number)। এমন input-এ "সঠিক output" অর্থহীন হতে পারে, আর LLM "hallucinated precondition" ভুলে পড়ে। 312 task-এর 119টায় পাওয়া "ভিন্নতা"-র কতটা বৈধ input-এ আর কতটা invalid input-এ — paper আলাদা করেনি। এটা false cluster split তৈরি করতে পারে।
6. **Cost-এর অসম্পূর্ণ হিসাব:** Token তুলনায় শুধু selection-এর token, sample generation-এর token নয় (সব technique-এ একই, তাই ঠিক আছে), কিন্তু differential testing-এর CPU সময় (প্রতি pair সর্বোচ্চ 3 + 3 মিনিট) token-এ ধরা পড়ে না। Median time দেওয়া আছে, কিন্তু worst-case বা total compute নেই।
7. **Oracle model ও generator model আলাদা:** Generator gpt-3.5, oracle GPT-4 — অর্থাৎ শক্তিশালী model দুর্বল model-এর কাজ বিচার করছে। একই (শক্তিশালী) model যদি generator হয়, তার ভুলগুলো oracle-এর ভুলের সাথে correlated হতে পারে — paper এটা পরীক্ষা করেনি। এটা আমাদের agent setting-এ গুরুত্বপূর্ণ, যেখানে প্রায়ই একই model patch বানায় ও বিচার করে।

**সহজ কথায়:** শক্তিশালী model দুর্বল model-এর কাজ বিচার করছে। দুজন একই model হলে একই ভুল দুজনেই করতে পারে, আর তখন বিচারক ভুলটা ধরতে পারবে না।
8. **Human evaluation দুর্বল:** Contradictory explanation-এর "resolved" রায় একজন মাত্র volunteer PhD student দিয়েছে; inter-rater agreement নেই। Failure categorization-ও মাত্র দুই author + এক student।
9. **Data contamination আলোচনা নেই:** HumanEval/MBPP 2021-এর public benchmark; GPT-4 oracle হয়তো canonical solution মুখস্থ জানে। Oracle accuracy-র একটা অংশ memorization হতে পারে — paper এটা নিয়ে কিছু বলেনি।
10. **Security বা non-functional দিক নেই:** Oracle শুধু functional output বিচার করে; একটা cluster সঠিক output দিলেও অনিরাপদ code হতে পারে (CG5)।
11. **Adversarial দিক নেই:** যদি generator জানে কীভাবে selection হয়, সে oracle-কে "বোঝাতে" পারে এমন output দিতে পারে কিনা — standalone function-এ অপ্রাসঙ্গিক, কিন্তু agent setting-এ verifier gaming (CG12) বাস্তব।

---

## ১৩. Research Gaps — কোথায় কাজ করার সুযোগ আছে

এখানে G-নম্বরগুলো **এই paper-এর নিজস্ব** (Section ২১.৩-এ একই নম্বর ব্যবহার হবে)।

| # | Gap | কেন গুরুত্বপূর্ণ | আমাদের common gap | কে কিছুটা কাজ করেছে (আমাদের folder-এ) |
|---|---|---|---|---|
| G1 | **Repository-level / non-standalone selection** — agent patch-এ oracle-guided selection | Agentless-এর 126 বনাম 96 ফাঁক ঠিক এই সমস্যা | CG2, CG1 | AI Coding Agents (Agentless-এর majority voting, AutoCodeRover @1 বনাম @3); Automated Program Repair (patch ranking) |
| G2 | **Constrained input domain-এ distinguishing input** — LLM-seeded fuzzing | 23 task-এ কম cluster, 35 task-এ input পাওয়া যায়নি | CG3 | LLM Test Generation (এই folder-এর অন্য paper, যেমন high-coverage Python test generation) |
| G3 | **Oracle-এর arithmetic/reasoning ভুল** — tool-augmented oracle (হিসাব code চালিয়ে) | 21টা wrong choice-এর 11টা calculation | CG1, CG10 | Patch Validation (LLM-as-judge-এর নির্ভরযোগ্যতা) |
| G4 | **Ambiguity ও incompleteness detection** — কখন "task অস্পষ্ট" বলা উচিত | 60টা failure-এর 26টা; contradictory explanation মাত্র 14/26 resolve | CG7 | Coding-Agent Evaluation & Reliability (SWE-Bench Pro-র requirements ablation ও task clarity check) |
| G5 | **সব candidate ভুল হলে abstention** | 118-এর মধ্যে মাত্র 30 ধরা পড়ে | CG7 | Trustworthy AI for SE |
| G6 | **একাধিক oracle model, repeated run, statistical test** | একটা model, একটা run, CI নেই | CG4, CG8 | Coding-Agent Evaluation & Reliability (SWE-rebench, Engineering Reliable Agents) |
| G7 | **Latency/cost trade-off** — differential testing budget বনাম accuracy | 221.5s বনাম 142.1s; budget sensitivity মাপা হয়নি | CG8 | Coding-Agent Evaluation & Reliability |
| G8 | **Input validity / precondition inference** | Invalid distinguishing input ভুল cluster split ও hallucinated precondition তৈরি করে | CG1, CG3 | Patch Validation |
| G9 | **Benchmark ground truth-এর ভুল ধরা** (verifier health) | 13টা wrong ground truth; HumanEval task 44-এর canonical solution | CG6, CG11 | Coding-Agent Evaluation & Reliability (SWE-bench Verified-এর flawed test, SWE-Bench Pro audit) |
| G10 | **Non-functional selection** — security/quality-সহ cluster বাছাই | একই output, ভিন্ন নিরাপত্তা | CG5 | Security of AI-Generated Code |
| G11 | **Generator ও oracle একই model হলে correlated error ও verifier gaming** | Agent নিজেই patch বানায় ও বিচার করে | CG12, CG10 | Trustworthy AI for SE; Coding-Agent Evaluation & Reliability |
| G12 | **Non-text output modality** | UI/plot code | — | — (খোলা) |

**সহজ কথায়:** সবচেয়ে বড় সুযোগ G1। কারণ এটা সরাসরি Agentless-এর ৯৬ বনাম ১২৬ ফাঁকের সাথে জড়িত।

### ১৩.১ এই paper common gap-গুলোকে কীভাবে বদলায়

**সহজ কথায়:** Gap মানে এখনো কেউ ভালোভাবে করেনি এমন জায়গা। নিচে দেখো এই paper CG2, CG3, CG7 আর CG11-কে কীভাবে বদলায়।
- **CG2 (re-ranking):** প্রথমবার একটা কংক্রিট, পরীক্ষিত পদ্ধতি পাওয়া গেল যা majority vote-এর চেয়ে ভালো (68.2% বনাম 84.3% oracle accuracy) — কিন্তু শুধু standalone function-এ। **Repository-level-এ নেওয়াই (G1) আমাদের জন্য সবচেয়ে স্বাভাবিক নতুন কাজ।**
- **CG3 (generated test-এর মান):** নতুন শক্ত সংখ্যা — LLM test-এর ~25% ভুল, 80%-এর বেশি task-এ অন্তত একটা ভুল test।
- **CG7 (abstention):** "কোনো option সঠিক নয়" ও contradictory explanation — abstention-এর প্রথম কার্যকর mechanism, কিন্তু recall কম।
- **CG11 (verifier health):** benchmark ground truth-এর 13টা ভুল — verifier নিজে ভুল হতে পারে তার আরেকটা প্রমাণ।

---

## ১৪. কী করলে আরও ভালো হবে — Improvement Ideas

1. **LLM-seeded differential fuzzing:** LLM-generated test input-কে Hypothesis-এর seed হিসেবে দেওয়া — paper নিজেই এটা future work বলেছে (G2)।
2. **Tool-augmented oracle:** Oracle LLM-কে Python interpreter দেওয়া, যাতে হিসাব নিজে না করে চালিয়ে দেখে — arithmetic ভুল (11/21) কমাতে (G3)।
3. **Oracle ensemble ও calibrated abstention:** একাধিক model বা একাধিক sample দিয়ে oracle query; মতভেদ বেশি হলে "অস্পষ্ট" বলে মানুষকে পাঠানো (G4, G5)। একটা সম্ভাব্য নিয়ম (আমার প্রস্তাব, paper-এ নেই): $m$টা oracle query-র মধ্যে সর্বোচ্চ একমত option-এর ভগ্নাংশ $a$ হলে, $a < \tau$ হলে abstain।
4. **Precondition-aware fuzzing:** Description থেকে LLM দিয়ে precondition বের করে শুধু বৈধ input-এ differential testing (G8)।
5. **Repeated run + paired statistics:** প্রতি technique 5 বার, McNemar/bootstrap CI (ফলাফল কতটা নির্ভরযোগ্য তা মাপার statistical পদ্ধতি) (G6)।
6. **Budget sweep:** 3 মিনিটের বদলে 10s/30s/60s/180s budget-এ accuracy বনাম time curve (G7)।
7. **Agent patch-এ প্রয়োগ:** Section ১৬-এর মূল প্রস্তাব (G1)।

**সহজ কথায়:** সাতটা idea-র মধ্যে প্রথম তিনটা (seeded fuzzing, tool-সহ oracle, ensemble) সবচেয়ে বাস্তবসম্মত। শেষেরটাই আমাদের মূল কাজ।

---

## ১৫. কোন Gap-এ Research করলে ভালো Result ও Publication আসতে পারে

> ⚠️ এটা চতুর্থ sub-domain-এর প্রথম paper-এর ভিত্তিতে মত। বাকি sub-domain শেষে চূড়ান্ত।

| Gap | SPL3-তে করা সম্ভব? | Novelty | Publication সম্ভাবনা |
|---|---|---|---|
| **G1: Oracle-guided selection for agent patches** (Agentless-এর প্রকাশিত candidate-এ, offline) | ✅ হ্যাঁ — generation আবার না চালিয়ে শুধু selection | উচ্চ — standalone থেকে repository-level, আর পরিষ্কার baseline (96) ও upper bound (126) আছে | ⭐⭐⭐⭐⭐ |
| **G1 + G4 + G5: Selection + abstention + I/O evidence = assurance report** | ✅ হ্যাঁ, G1-এর উপর extension | উচ্চ — আমাদের research direction-এর "assurance report"-এর সাথে সরাসরি মেলে | ⭐⭐⭐⭐⭐ |
| **G3: Tool-augmented oracle** (HumanEval+/MBPP+-এ replication + improvement) | ✅ হ্যাঁ — artifact আছে, ছোট scale | মাঝারি | ⭐⭐⭐ (workshop) |
| **G6: Current model দিয়ে replication + statistics** | ✅ হ্যাঁ, কম খরচ | মাঝারি — replication study | ⭐⭐⭐ |
| G2: LLM-seeded fuzzing | ⚠️ সম্ভব কিন্তু engineering বেশি | মাঝারি | ⭐⭐⭐ |
| G10: Security-aware selection | ⚠️ Security sub-domain পড়ার পর | উচ্চ | ⭐⭐⭐⭐ |

**সহজ কথায়:** সবচেয়ে ভালো শুরু G1, কারণ এতে baseline আর upper bound দুটোই জানা আছে।

**সম্ভাব্য venue (general guidance):** এই paper নিজেই ISSTA-তে — তাই ISSTA, ICSE, FSE, ASE এই কাজের স্বাভাবিক জায়গা; student-এর জন্য শুরুতে LLM4Code বা AST (Automation of Software Test)-এর মতো workshop। Journal: TOSEM, EMSE, JSS, IST।

**সহজ কথায়:** সবচেয়ে ভালো ফল পাওয়ার সম্ভাবনা G1 আর তার সাথে abstention যোগ করলে। ছোট replication কাজও workshop-এ যেতে পারে।

---

## ১৬. SPL3 Implementation Perspective — Software-এ কীভাবে আনবো

**দুই ধাপের পরিকল্পনা:**

### ধাপ A — Paper replicate (standalone, ছোট)
1. **Sample generator:** HumanEval+-এর task-এ যেকোনো সস্তা LLM দিয়ে 10টা sample।
2. **Differential tester:** `hypothesis` দিয়ে pairwise `out(P1) == out(P2)` property; ব্যর্থ হলে `crosshair` (`crosshair diffbehavior` command দুটো function-এর behaviour তুলনা করে — implementation-এ যাচাই করতে হবে)।
3. **Clusterer:** distinguishing input-এ output tuple দিয়ে group।
4. **Oracle module:** Figure 3-এর prompt; option না মিললে "none" handle।
5. **Evaluator:** pass@1 ($n/N$), selection accuracy, token, time।
6. **Artifact reuse:** Zenodo artifact (10.5281/zenodo.10390291) থেকে paper-এর sample ও result নিয়ে প্রথমে নিজের implementation যাচাই।

**সহজ কথায়:** ধাপ A হলো paper-এর ছোট কপি বানিয়ে নিজের কোড ঠিক আছে কিনা দেখা। এটা পরীক্ষার আগের মহড়ার মতো।

### ধাপ B — Agent patch-এ নেওয়া (মূল SPL3 contribution)
1. **Candidate loader:** Agentless-এর প্রকাশিত candidate patch (SWE-bench Lite, task প্রতি 40টা) — public artifact-এ সব candidate আছে কিনা **আগে যাচাই করতে হবে**।
2. **Distinguishing test finder:**
   - (ক) Agentless-এর reproduction test ও regression test সব candidate-এ চালিয়ে যেখানে ফল আলাদা;
   - (খ) পরিবর্তিত function-এ Hypothesis দিয়ে input (যেখানে signature সরল);
   - (গ) LLM দিয়ে issue থেকে কয়েকটা test input প্রস্তাব, তারপর সব candidate-এ চালিয়ে output রেকর্ড — **assertion LLM লিখবে না**, শুধু input।
3. **Behaviour clusterer:** test-ভিত্তিক outcome vector (pass/fail/exception/return value)।
4. **Oracle:** "Issue অনুযায়ী এই input-এ কোন আচরণ সঠিক?" — highest-entropy input আগে।
5. **Abstention:** কোনো option না মিললে বা oracle-দের মতভেদ হলে "uncertain" flag।
6. **Assurance report:** নির্বাচিত patch + তার পক্ষে `(input, expected behaviour)` প্রমাণ + oracle-এর ব্যাখ্যা + model version।
7. **Evaluation:** Agentless-এর 96 (majority) বনাম আমাদের selection বনাম upper bound 126; সাথে token ও সময়।

**সহজ কথায়:** ধাপ B-তে আমরা একই ধারণা patch-এর জগতে নিয়ে যাই। সফল হলে ৯৬ থেকে ১২৬-এর দিকে এগোনো যাবে।

**Practical সতর্কতা:**
- SWE-bench Docker harness-এ 40 candidate × অনেক test চালানো সময়সাপেক্ষ — প্রথমে 30টা task-এর ছোট subset, বিশেষ করে সেই task-গুলো যেখানে candidate-দের মধ্যে অন্তত একটা সঠিক কিন্তু majority ভুল।
- Repository-level code-এ CrossHair প্রায়ই কাজ করবে না (external dependency, I/O) — Hypothesis বা test-execution-ভিত্তিক পথই বাস্তবসম্মত।
- SWE-bench Lite পুরনো ও contamination-ঝুঁকিপূর্ণ (Section ২১); selection technique-এর তুলনা একই candidate-এর উপর হওয়ায় ঝুঁকি কম, তবে oracle LLM gold patch মুখস্থ জানতে পারে — fresh task (SWE-rebench) দিয়ে একটা ছোট check রাখা উচিত।

---

## ১৭. প্রসঙ্গ — আমাদের অন্য paper-গুলোর সাথে সম্পর্ক

- **Agentless (Paper 04, Sub-domain 1):** reproduction test + normalized majority voting দিয়ে selection — এই paper-এর ভাষায় এটা AlphaCode/CodeT-ধরনের consistency-based selection। LLMCodeChoice দেখায় majority-র বিকল্প আছে।
- **AutoCodeRover (Paper 03):** একই NUS group (Roychoudhury, Ruan, Fan); এই paper-এর reference [42]-এ AutoCodeRover আছে। AutoCodeRover-এর 78টা test-pass patch-এর মধ্যে 51টা (65.4%) সঠিক — CG1-এর মূল সংখ্যা।
- **RePaCA (Sub-domain 2):** static reasoning দিয়ে overfitting patch চেনা; LLMCodeChoice dynamic (execution-ভিত্তিক) signal দেয় — আমাদের research direction-এ দুটো আলাদা signal হিসেবে পাশাপাশি থাকতে পারে।
- **Engineering Reliable Agents (Sub-domain 3):** "verifier-কে version-সহ রেকর্ড করো" — oracle LLM-এর version (gpt-4-0613) এখানেও রেকর্ড করা দরকার।
- **Fact sheet-এর PatchDiff:** differential testing দিয়ে plausible patch-এর ভিন্নতা মাপা — একই কৌশল, evaluation-এর উদ্দেশ্যে।

**সহজ কথায়:** অন্য paper-গুলোর সাথে সম্পর্ক এক কথায়: Agentless-এর majority-র বিকল্প, AutoCodeRover-এর সমস্যার সমাধান, আর RePaCA-র পরিপূরক সংকেত।

(এই paper পরে কোন কাজকে প্রভাবিত করেছে, তার কোনো তথ্য আমাদের fact sheet-এ নেই — তাই সেই দাবি করছি না।)

---

## ১৮. Supervisor-এর সম্ভাব্য প্রশ্ন ও উত্তর (Viva Prep)

**Q1. এই paper-এর মূল idea এক বাক্যে?**
A: Differential testing দিয়ে LLM program-গুলো কোথায় ভিন্ন তা খুঁজে বের করে, সেই input-এ LLM-কে "এই কয়টা output-এর কোনটা সঠিক" জিজ্ঞেস করে সঠিক program cluster বাছাই।

**সহজ কথায়:** Viva-তে প্রথম উত্তর এটাই দেবে। বাকি প্রশ্নগুলোর উত্তর এই এক বাক্যের ব্যাখ্যা মাত্র।

**Q2. কেন multiple-choice দিলে LLM ভালো করে — এটা কি প্রমাণিত?**
A: Table 2-এ একই 381টা selection-এ option-সহ 84.3%, option ছাড়া 70.3%। Ablation-এও option যোগ করলে HumanEval+-এ +8.1 pp, MBPP+-এ +1.7 pp। কারণ হিসেবে paper বলছে option search space ছোট করে; Figure 4-এ `largest_prime_factor(25191)`-এ direct inference হিসাবে ভুল করে, option দিলে `311` ঠিক বের করে। তবে এটা একটা model (GPT-4) ও একটা run-এর ফল।

**Q3. CodeT-ও তো test দিয়ে cluster করে — পার্থক্য কী?**
A: CodeT-এর test-এর input ও expected output দুটোই LLM লেখে, আর ~25% test ভুল; selection হয় size × passed tests দিয়ে, অর্থাৎ majority-প্রভাবিত। LLMCodeChoice-এ input আসে testing tool থেকে, output আসে program execution থেকে, LLM শুধু বাছে — আর selection majority নয়, oracle-এর রায়। Figure 1-এ CodeT 588 বনাম 396 দিয়ে ভুল cluster বাছে।

**Q4. Entropy কেন ব্যবহার করা হয়েছে?**
A: কোন distinguishing input আগে জিজ্ঞেস করবো তা ঠিক করতে। $H = -\sum (n_k/N)\log(n_k/N)$; বেশি entropy মানে cluster-গুলো সমান ভাগে ছড়ানো, তাই এক উত্তরেই বেশি program বাদ পড়ে, LLM query কম লাগে। আমার হিসাবে 6–4 split-এ প্রত্যাশিত 52% program থাকে, 9–1 split-এ 82%।

**Q5. 87.7% pass@1 কি পুরো HumanEval-এর উপর?**
A: না। শুধু 89টা HumanEval task-এর উপর, যেখানে sample-দের মধ্যে কিছু সঠিক কিছু ভুল — অর্থাৎ selection-এর পার্থক্য হয় এমন task। আর এটা HumanEval+ (enhanced test)-এর সংখ্যা; original HumanEval-এ 89.2%।

**Q6. সবচেয়ে বড় দুর্বলতা কী?**
A: (১) শুধু standalone function — repository-level code-এ input/output সংজ্ঞায়িত করা অনেক কঠিন; (২) statistical rigor নেই — 89 task-এ 6.9 pp মানে প্রায় 6টা task, কোনো CI বা repeated run নেই; (৩) LLM oracle নিজে arithmetic-এ ভুল করে; (৪) paper-এর ভেতরে কিছু সংখ্যার অসঙ্গতি (321/387, "60% more efficient" বনাম 4x)।

**Q7. Failure-গুলো থেকে কী শিখলে?**
A: 60টা ভুলের মাত্র 21টা (35%) LLM-এর সরাসরি ভুল; 22টা incomplete description, 4টা ambiguous, 13টা benchmark-এর নিজের ভুল ground truth। অর্থাৎ technique-টা specification সমস্যা খোঁজার detector হিসেবেও কাজ করে — আমাদের "task clarity check" component-এর জন্য এটা সরাসরি প্রমাণ।

**Q8. তোমার SPL3-এ এটা কীভাবে ব্যবহার করবে?**
A: Agentless-এর প্রকাশিত 40টা candidate patch-এর উপর offline: candidate-গুলো যেখানে ভিন্ন আচরণ করে সেই test/input খুঁজে behaviour cluster বানাবো, LLM-কে issue দেখিয়ে সঠিক আচরণ বাছতে বলবো। Baseline Agentless-এর majority (96), upper bound 126। Output হবে নির্বাচিত patch + তার পক্ষে input-output প্রমাণ + "uncertain" flag — অর্থাৎ assurance report।

**Q9. Generator আর oracle একই model হলে কী সমস্যা?**
A: Paper-এ generator gpt-3.5, oracle GPT-4 — শক্তিশালী model দুর্বলের কাজ বিচার করছে। একই model হলে তার ভুল বোঝাপড়া generation ও judgment দুই জায়গাতেই আসতে পারে (correlated error)। Paper এটা পরীক্ষা করেনি; আমাদের experiment-এ generator ও oracle আলাদা model রেখে আর একই model রেখে দুইভাবে মাপা উচিত।

**Q10. Distinguishing input কি সবসময় বৈধ input?**
A: না। change_base-এ base = 16 (description বলছে < 10), perfect-square-এ −1 — এমন input-এ "সঠিক output" অনির্ধারিত হতে পারে; paper-এর "hallucinated precondition" failure এখান থেকেই আসে। Precondition-aware fuzzing একটা improvement।

---

## ১৯. Glossary (দ্রুত মনে রাখার জন্য)

| Term | অর্থ |
|---|---|
| Test oracle | কোনো input-এ সঠিক output কী — সেই সিদ্ধান্তদাতা |
| Oracle problem | সঠিক expected output জানা কঠিন — testing-এর মূল সমস্যা |
| Differential testing | দুটো program একই input-এ চালিয়ে output তুলনা |
| Distinguishing input | যে input-এ দুটো program ভিন্ন output দেয় |
| Program selection | অনেক LLM sample থেকে একটা বাছাই |
| Behaviour cluster | সব distinguishing input-এ একই output দেওয়া program-এর দল |
| Specification selection | Option-এর মধ্যে LLM-এর সঠিক output বাছাই |
| Direct inference | Option ছাড়া LLM-কে output predict করতে বলা |
| Majority vote | সবচেয়ে বড় cluster-কে সঠিক ধরা |
| Dual execution agreement | CodeT-এর score: cluster size × passed tests |
| Entropy | Partition কতটা সমানভাবে ছড়ানো |
| Hypothesis | Python property-based (random) testing tool |
| CrossHair | Python symbolic execution tool |
| CoT | ধাপে ধাপে যুক্তি লিখতে বলা prompt |
| HumanEval+ / MBPP+ | বেশি test-সহ enhanced benchmark |
| Overfitting (এখানে) | Original test pass, enhanced test fail |
| Contradictory explanation | ভিন্ন output-এর ব্যাখ্যা তুলনা করে ambiguity ধরা |
| Abstention | নিশ্চিত না হলে উত্তর না দিয়ে মানুষকে জানানো |

---

## ২০. এক নজরে সারাংশ (Summary Card)

| | |
|---|---|
| **Problem** | অনেক LLM sample-এর মধ্যে সঠিকটা বাছাই; majority vote ও LLM-generated test অবিশ্বস্ত |
| **Solution** | Differential testing-এ distinguishing input + LLM-কে multiple-choice oracle হিসেবে ব্যবহার |
| **Method** | Hypothesis/CrossHair (3 মিনিট) → cluster → highest-entropy input → GPT-4 CoT selection → filter |
| **Key result** | HumanEval+ pass@1 87.7% (codeT 80.8%); MBPP+ 78.6% (codeT 75.0%); oracle accuracy 84.3% বনাম direct 70.3% বনাম majority 68.2%; token 1533 বনাম 6319 |
| **Key insight** | বাছাই করা, নিজে বের করার চেয়ে সহজ; majority প্রায়ই ভুল; অল্প সঠিক test অনেক ভুল test-এর চেয়ে ভালো |
| **Main limitation** | শুধু standalone function, এক model, এক run, কোনো CI নেই; LLM-এর arithmetic ভুল; সময় বেশি |
| **আমাদের জন্য gap** | **G1: Agent patch-এ oracle-guided selection** (CG2) + abstention (CG7) + I/O প্রমাণসহ assurance report |

---

## ২১. বর্তমান (2026) প্রেক্ষাপট — আজকের Model ও Agent-দের সাথে তুলনা

> **উৎস:** এই section-এর সব current-state তথ্য `00_Current_State_2026_Sources.md` (fact sheet, compiled 2026-10-28) থেকে নেওয়া। প্রতিটা সংখ্যার পাশে লেখা আছে সেটা **কোম্পানির নিজের দাবি (vendor-reported)** নাকি **স্বাধীনভাবে মাপা (independent)**। Fact sheet যেটাকে "search-snippet only" বলেছে, সেটা এখানেও তাই চিহ্নিত — supervisor-কে দেখানোর আগে মূল উৎস খুলে যাচাই করা উচিত। আমার নিজের যুক্তি "আমার পর্যবেক্ষণ" দিয়ে আলাদা করা।
>
> **গুরুত্বপূর্ণ:** Fact sheet-এ HumanEval, HumanEval+, MBPP বা MBPP+-এ বর্তমান model-এর কোনো সংখ্যা **নেই**, আর CodeT/AlphaCode/LLMCodeChoice-ধরনের program selection technique বর্তমান model দিয়ে কেউ আবার চালিয়েছে এমন তথ্যও **নেই**। তাই এই paper-এর benchmark-স্তরের দাবি আজ সত্য কিনা তা সরাসরি বলা যায় না — এটা নিজেই একটা gap।

### ২১.১ Paper-এর সময় বনাম এখন

| দিক | Paper-এ (ISSTA 2024) | এখন, October 2026 | উৎস |
|---|---|---|---|
| Generator model | gpt-3.5-turbo-0613 | GPT-6 family (Astra, Sol, Luna, 6.1 Terra), Claude Opus 5.5, Gemini 4 Argon, Kimi K3.1 Pro ইত্যাদি | Fact sheet §1 |
| Oracle model | gpt-4-0613 | একই family-গুলো; এদের program-selection oracle accuracy **পাওয়া যায়নি** | Fact sheet-এ নেই |
| Benchmark | HumanEval+ / MBPP+ (standalone function) | Vendor launch-এ এখন Terminal-Bench 4.0, DeepSWE, FrontierCode, SWE-bench Pro — repository-level ও agentic; HumanEval/MBPP-এর বর্তমান সংখ্যা fact sheet-এ নেই | Fact sheet §2 |
| Selection-এর ফাঁক | pass@1 উন্নতি 3.6–6.9 pp (codeT-এর উপর) | SWE-rebench-এ top-8-এ pass@1 বনাম pass@5-এর ফাঁক 12–18 point (যেমন Fable 5: 64.5% বনাম 78.4%; GLM-5.2: 62.9% বনাম 81.1%) (**independent**) | SWE-rebench, window শেষ 2026-07-01 |
| LLM-generated test-এর মান | প্রায় 25% LLM test ভুল; 80%-এর বেশি task-এ অন্তত একটা ভুল test | Agent-দের লেখা test patch-এর 80.2%-এ দুর্বল বা কোনো স্পষ্ট oracle নেই (86,156 test-file patch) (**independent**) | "All Smoke, No Alarm", 2026-06-16 |
| LLM judge-এর নির্ভরযোগ্যতা | Oracle accuracy 84.3% (option-সহ), 70.3% (direct) | Plain LLM baseline overfitting patch filter-এ মাত্র 62.14% (ComPass, **search-snippet only**); judge-দের নিজেদের মধ্যে মিল বেশি কিন্তু execution-এর সাথে কম (**search-snippet only**) | Fact sheet §4 |
| Benchmark ground truth-এর ভুল | 13টা wrong ground truth (60 failure-এর 21.6%) | SWE-bench Verified-এর audited hard subset-এ অন্তত 59.4% flawed test (OpenAI, **search-snippet only**); SWE-Bench Pro-র 27.4%–34.1% task broken (OpenAI audit, **secondary**) | Fact sheet §3 |
| Underspecified task | Incomplete 36.7% + ambiguous 6.7% failure | SWE-Bench Pro Verified 22টা misleading description ঠিক করেছে (**independent**); অসম্ভব task-এ attempted reward hacking 3–6 গুণ বাড়ে (Opus 5.5 System Card, **vendor-reported**) | Fact sheet §3 |
| Plausible ≠ correct | Overfitting gap 1.5–11.8 pp (Table 3) | Plausible patch-এর 29.6% gold থেকে ভিন্ন আচরণ (PatchDiff, ICSE 2026, **independent**, 2025-এর model) | Fact sheet §4 |
| খরচ | ~1,331–1,533 token per task (selection) | GPT-6.1 Terra API USD 1 input / USD 5 output per million token (**vendor-reported**); SWE-rebench-এ per problem USD 0.81–4.40 (**independent**) | Fact sheet §1, §3 |

**সহজ কথায়:** ২০২৪ থেকে ২০২৬-এ model আর benchmark দুটোই বদলেছে। কিন্তু "অনেক candidate থেকে একটা বাছা" সমস্যাটা আগের মতোই আছে।

**আমার পর্যবেক্ষণ:** SWE-rebench-এর 12–18 point ফাঁক মানে বর্তমান frontier agent-ও ৫টা চেষ্টায় অনেক বেশি task solve করে, কিন্তু একটা submit করতে হলে সেই সুবিধা হারায়। এই paper ঠিক এই ধরনের ফাঁক (তখন standalone function-এ) বন্ধ করার কাজ। 2026-এ repository-level-এ এই ফাঁক বন্ধ করার কোনো পদ্ধতির ফল fact sheet-এ নেই — অর্থাৎ **selection এখনো unsolved**।

**সহজ কথায়:** সংক্ষেপে: ২০২৬-এও agent অনেকবার ঠিক patch বানায়, কিন্তু একটা বাছতে গিয়ে হারায়। তাই selection এখনো গুরুত্বপূর্ণ।

### ২১.২ কোন Finding এখনো সত্য, কোনটা পুরনো হয়ে গেছে

- **এখনো সত্য, আরও বড় পরিসরে — "LLM-generated test অবিশ্বস্ত" (Key Finding ৩):** Paper-এর ~25% ভুল test-এর জায়গায় এখন agent test patch-এর 80.2%-এ দুর্বল/কোনো oracle নেই, আর agent-রা বেশি mock ব্যবহার করে (36% বনাম 26%, **search-snippet only**)। তবে এই study-গুলো মূলত 2025-এর agent (AIDev dataset)-এর উপর — Opus 5.5/GPT-6-এর জন্য আলাদা সংখ্যা নেই।
- **এখনো সত্য — "Benchmark-এর ground truth নিজেই ভুল হতে পারে" (Key Finding ৮):** Paper 13টা ভুল ground truth পেয়েছিল; এখন OpenAI নিজে Verified-এর flawed test-এর কারণে benchmark ছেড়েছে (snippet), আর SWE-Bench Pro-র এক-তৃতীয়াংশ পর্যন্ত task broken (secondary)। Verifier health (CG11) এখন industry-স্তরের সমস্যা।
- **এখনো সত্য — "Majority ≠ correct" (Key Finding ২):** SWE-rebench-এর pass@1 বনাম pass@5 ফাঁক দেখায় সঠিক সমাধান প্রায়ই কোনো একটা run-এ আসে কিন্তু default selection-এ ধরা পড়ে না। তবে বর্তমান agent-এর majority-vote accuracy সরাসরি মাপা কোনো তথ্য fact sheet-এ **নেই**।
- **এখনো সত্য — underspecification বড় failure কারণ (Key Finding ৭):** OpenAI "underspecified prompts" ও "misleading prompts"-কে SWE-Bench Pro-র failure category বলেছে (secondary); Anthropic দেখায় অসম্ভব বা underspecified environment-এ reward hacking-এর চেষ্টা বাড়ে (vendor)।
- **অজানা — "Option দিলে LLM oracle ভালো করে" (Key Finding ১):** বর্তমান model দিয়ে কেউ আবার মেপেছে এমন তথ্য নেই। **আমার পর্যবেক্ষণ:** paper-এর failure-এর বড় অংশ arithmetic (11/21) — বর্তমান reasoning model-এ এই ভুল কমতে পারে, ফলে direct inference ও selection-এর ফাঁক ছোট হতে পারে; এটা অনুমান, মাপা নয়।
- **সম্ভবত পুরনো — HumanEval/MBPP-কে মূল testbed হিসেবে ব্যবহার:** Vendor-রা এখন repository-level ও agentic benchmark report করে; fact sheet-এ HumanEval-এর কোনো উল্লেখই নেই। Paper-এর technique-এর আসল প্রাসঙ্গিকতা এখন repository-level (G1)-এ।
- **নতুন সমস্যা, paper-এ ছিল না — oracle-এর বিরুদ্ধে gaming:** Agent-রা `.git` history থেকে gold patch পড়ে (DeepSWE-তে প্রতারণার 87%; GLM-5.2 78.80% থেকে safeguard-সহ 57.32%) (**independent**); Opus 5.5 "hidden tests"-নিয়ে যুক্তি করে (vendor)। LLM oracle যদি agent-এর context বা ব্যাখ্যা দেখে, agent oracle-কে প্রভাবিত করার চেষ্টা করতে পারে — standalone function-এ এই ঝুঁকি ছিল না।

**সহজ কথায়:** পুরোনো কথা কতটা টেকে: LLM test অবিশ্বস্ত, benchmark ভুল, majority ভুল আর underspecified task আজও সত্য। নতুন সমস্যা হলো agent-এর বিচারককে ঠকানোর চেষ্টা।

### ২১.৩ এই Paper-এর Gap-গুলো আজও খোলা কিনা

| Gap | 2026-এ অবস্থা | প্রমাণ |
|---|---|---|
| G1 / CG2: Repository-level selection | **খোলা** | SWE-rebench-এ pass@1 বনাম pass@5 ফাঁক 12–18 point (independent); repository-level oracle-guided selection-এর কোনো ফল fact sheet-এ নেই |
| G2 / CG3: Constrained input-এ distinguishing input | **খোলা, তথ্য নেই** | Fact sheet-এ differential testing tool-এর বর্তমান ফল নেই; PROBE program variant দিয়ে দুর্বল test ধরে (search-snippet only) |
| G3 / CG1, CG10: Oracle-এর reasoning ভুল | **খোলা** | LLM judge overfitting filter-এ 62.14% (ComPass, snippet); over-fix flag-এ 5–10% precision (snippet); বর্তমান model-এ যাচাই করা study **পাওয়া যায়নি** ("Not found" fact sheet-এ) |
| G4 / CG7: Ambiguity detection | **খোলা** | SWE-Bench Pro Verified 22টা misleading description হাতে ঠিক করেছে; CursorBench ইচ্ছাকৃতভাবে ambiguous task রাখে (vendor-run) — কিন্তু automatic detection-এর কোনো সংখ্যা নেই |
| G5 / CG7: সব ভুল হলে abstention | **খোলা** | Fable 5.1 "আটকে গেলে বলে" — qualitative, vendor-reported; কোনো মাপা abstention rate নেই |
| G6 / CG4, CG8: Multi-model, repeated run, statistics | **আংশিক (evaluation-এ), selection-এ খোলা** | Vendor-রা এখন SE দেয় (±2.6, Terminal-Bench 4.0, vendor); Noise Floor Audit: prompt perturbation-এ SD rerun-এর চেয়ে 11–58 গুণ (independent) — selection oracle-এর জন্য এমন মাপ নেই |
| G7 / CG8: Latency ও cost | **খোলা, আরও গুরুত্বপূর্ণ** | Terminal-Bench 4.0-এ per task USD 1.72–17.64, Opus 5.5-এ 1h04m per test (Vals.ai, independent) — একাধিক candidate বানিয়ে বাছাই করার খরচ অনেক বেশি |
| G8 / CG1, CG3: Input validity | **তথ্য পাওয়া যায়নি** | Fact sheet-এ নেই |
| G9 / CG6, CG11: Ground truth-এর ভুল | **খোলা, এখন বড় পরিসরে স্বীকৃত** | Verified ≥59.4% flawed (snippet); SWE-Bench Pro 27.4–34.1% broken (secondary); DeepSWE: SWE-Bench Pro test-এর সাথে LLM-judge অমিল 32.4% (independent) |
| G10 / CG5: Security-aware selection | **খোলা** | Cursor + Opus 4.6: FuncPass 84.4%, SecPass 7.8% (Endor Labs, independent) — functional oracle দিয়ে বাছলে নিরাপত্তা নিশ্চিত হয় না; বর্তমান model-এর SusVibes/BaxBench ফল নেই |
| G11 / CG12: Correlated error ও verifier gaming | **খোলা, সরাসরি প্রমাণ আছে** | GLM-5.2 78.80 থেকে 57.32 (independent); GPT-6.1 Sol-এ Astra-র চেয়ে বেশি reward-hacking flag (vendor); Opus 5.5 বা GPT-6-এর independent reward-hacking audit নেই |
| G12: Non-text output | **তথ্য পাওয়া যায়নি** | SWE-bench Multimodal আছে (official top 35.98%, vendor দাবি 61.4%), কিন্তু selection-সম্পর্কিত কিছু নেই |

**সহজ কথায়:** প্রায় সব gap এখনো খোলা। তাই এই paper-এর ধারণা নিয়ে কাজ করার সুযোগ আজও আছে।

### ২১.৪ বর্তমান Model দিয়ে আবার পরীক্ষা করলে — SPL3 Idea (cost-aware)

1. **Replication-lite (সবচেয়ে সস্তা):** HumanEval+-এর একটা subset-এ বর্তমান সস্তা model (যেমন GPT-6.1 Terra) দিয়ে 10টা sample, Hypothesis differential testing, তারপর oracle হিসেবে একই বা আরেকটা বর্তমান model। Direct inference বনাম selection বনাম majority — Table 2-এর তিন column আবার মাপা।
   - **আমার হিসাব (rough):** paper-এ selection-এ task প্রতি ~1,533 token। সব token output দামে ধরলেও (worst case) $1533 \times 5 / 10^6 \approx$ USD 0.0077 per task; 164 task-এ প্রায় USD 1.3 — sample generation-এর খরচ আলাদা, কিন্তু তাও ছোট। Vendor-reported দাম, তাই আসল bill যাচাই করতে হবে।
   - **যে gap দেখাবে:** "option দিলে ভালো" finding বর্তমান reasoning model-এ টেকে কিনা (২১.২-এর "অজানা" দাবি) — আর বর্তমান model-এর জন্য HumanEval-এর কোনো সংখ্যা fact sheet-এ না থাকায় এটাই নতুন তথ্য।
2. **Agent patch-এ offline selection (মূল idea, generation খরচ শূন্য):** Agentless-এর প্রকাশিত 40টা candidate (SWE-bench Lite) নিয়ে behaviour clustering + LLM oracle। শুধু oracle query-র খরচ লাগবে, আর Docker-এ test চালানোর সময়।
   - **যে gap দেখাবে:** G1/CG2 — 96 থেকে 126-এর দিকে কতটা যাওয়া যায়।
   - **সতর্কতা:** Lite পুরনো ও official board-এ শেষ entry 2025-09-11; oracle model gold patch মুখস্থ জানতে পারে (Verified-এ GPT-5.2/Opus 4.5/Gemini 3 Flash gold patch হুবহু reproduce করতে পারে — secondary report)। তাই oracle-কে gold-এর সাথে মিলিয়ে দেখার বদলে execution-ভিত্তিক মাপ রাখতে হবে।
3. **Fresh task-এ ছোট check:** SWE-rebench-এর সর্বশেষ window (2026-05-15 থেকে 2026-07-01, 111 problem) থেকে 20টা task, একটা সস্তা agent k = 5 বার চালিয়ে candidate তৈরি, তারপর আমাদের selection।
   - **আমার হিসাব (rough):** SWE-rebench-এ GPT-5.6 Sol-এর খরচ USD 0.85 per problem (independent) ধরে $20 \times 5 \times 0.85 \approx$ USD 85; সবচেয়ে দামি (Fable 5, USD 4.40) হলে প্রায় USD 440। তাই সস্তা model বাছাই করা জরুরি।
   - **যে gap দেখাবে:** contamination-মুক্ত task-এ pass@1 → selected@1 → pass@5 — তিনটা সংখ্যা একসাথে, আমাদের নিজের selection ফাঁকের কতটা বন্ধ করে।
4. **Oracle independence test:** Generator ও oracle একই model বনাম আলাদা model — ভুল কতটা correlated (G11)। ধাপ ১-এর data-তেই সস্তায় করা যায়।
5. **Abstention মাপা:** সব candidate ভুল এমন task-এ oracle "none" কতবার বলে (paper-এ 30/118) — বর্তমান model-এ বাড়লো কিনা (G5/CG7)।

**সহজ কথায়:** পাঁচটা SPL3 idea-র মধ্যে প্রথমটা সবচেয়ে সস্তা। দ্বিতীয়টা মূল কাজ। বাকিগুলো তার উপর ভিত্তি করে ছোট যাচাই।

### ২১.৫ Supervisor-এর সম্ভাব্য প্রশ্ন (2026 প্রসঙ্গে)

**Q1. 2026-এর model HumanEval প্রায় সবই পারে না? তাহলে selection-এর দরকার কী?**
A: Fact sheet-এ বর্তমান model-এর HumanEval সংখ্যা নেই, তাই "প্রায় সব পারে" দাবি আমি সংখ্যা দিয়ে বলতে পারছি না। কিন্তু repository-level-এ selection সমস্যা স্পষ্টভাবে আছে: SWE-rebench-এ top agent-দের pass@1 ~60–65% কিন্তু pass@5 ~75–81% (independent) — 12–18 point সঠিক সমাধান হাতে থেকেও হারায়। এই paper-এর পদ্ধতির আসল ব্যবহার এখন সেখানে।

**Q2. আজকের reasoning model নিজেই কি ভালো oracle নয়? এই paper-এর multiple-choice trick কি দরকার?**
A: হতে পারে, কিন্তু প্রমাণ নেই। Fact sheet বলছে বর্তমান-প্রজন্মের agent patch-এ LLM-judge যাচাই করা কোনো study পাওয়া যায়নি; পুরনো প্রমাণে plain LLM judge overfitting filter-এ মাত্র 62.14% (snippet)। তাই ২১.৪-এর replication-lite experiment ঠিক এই প্রশ্নের সস্তা উত্তর দেবে।

**Q3. Agent-রা এখন নিজেরাই test লেখে — distinguishing input-এর দরকার কী?**
A: Agent-লেখা test patch-এর 80.2%-এ দুর্বল বা কোনো oracle নেই (independent) — এই paper-এর ~25% ভুল LLM test-এর finding-এর মতোই, বরং বড় পরিসরে। Paper-এর মূল শিক্ষা: LLM-কে assertion লিখতে না দিয়ে শুধু execution-এর output-এর মধ্যে বাছতে দাও।

**Q4. LLM oracle-কে agent ঠকাতে পারবে না?**
A: Standalone function-এ ঝুঁকি কম ছিল, কিন্তু 2026-এ agent-রা verifier gaming করে — GLM-5.2-এর score safeguard দিলে 78.80 থেকে 57.32-এ নামে, DeepSWE-তে প্রতারণার 87% `.git` থেকে উত্তর পড়া (independent)। তাই আমাদের design-এ oracle শুধু issue text, input ও execution output দেখবে — agent-এর ব্যাখ্যা বা trajectory নয় — আর `.git` history সরানো sandbox-এ test চলবে।

**Q5. খরচ কি যুক্তিসঙ্গত?**
A: Selection অংশ সস্তা — paper-এ task প্রতি ~1.5k token; বর্তমান সস্তা model-এর vendor দামে ধরলে task প্রতি এক cent-এরও কম (আমার হিসাব)। আসল খরচ candidate তৈরিতে — SWE-rebench-এ per problem USD 0.81–4.40 (independent)। তাই প্রথমে Agentless-এর প্রকাশিত candidate দিয়ে offline কাজ, পরে ছোট fresh-task check।
