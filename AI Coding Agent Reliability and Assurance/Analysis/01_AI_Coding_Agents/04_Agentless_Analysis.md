# Paper Analysis 04: Agentless — Demystifying LLM-based Software Engineering Agents

> **Sub-domain:** AI Coding Agents (Paper 04 — এই sub-domain-এর শেষ paper)
> **Analysis করেছে:** SPL3 — AI Coding Agent Reliability and Assurance
> **Paper file:** `AI Coding Agents/Demystifying LLM-based Software Engineering Agents.pdf`
> **আগে পড়ো:** Paper 01 (SWE-bench) — SWE-bench, F2P/P2P, BM25, patch, regression test, contamination, greedy decoding সেখানে ব্যাখ্যা করা আছে। Paper 02 (SWE-agent) ও Paper 03 (AutoCodeRover) হলো এই paper-এর মূল "agent" প্রতিপক্ষ।

---

## ০. Paper-এর পরিচয় (Bibliographic Info)

| বিষয় | তথ্য |
|---|---|
| **Title** | AGENTLESS: Demystifying LLM-based Software Engineering Agents |
| **Authors** | Chunqiu Steven Xia, Yinlin Deng, Soren Dunn, Lingming Zhang |
| **Institution** | University of Illinois Urbana-Champaign (UIUC) |
| **Version** | arXiv:2407.01489v2 [cs.SE], 29 Oct 2024 (আমাদের PDF এই version) |
| **Venue** | PDF-এ কোনো conference-এর নাম নেই (arXiv preprint)। আমার জানামতে পরে এটা একটা top SE venue-তে (FSE 2025) প্রকাশিত হয়েছে — **supervisor-কে বলার আগে DBLP/ACM DL-এ যাচাই করো।** |
| **Paper type** | **Technique paper + Empirical/benchmark-quality study** — (ক) নতুন একটা সরল approach (Agentless), (খ) SWE-bench Lite-এর প্রতিটা problem হাতে-কলমে classify করে benchmark-এর সমস্যা খুঁজে বের করা ও filtered subset **SWE-bench Lite-S** (249 problem) তৈরি |
| **Artifacts** | Open-source code: `github.com/OpenAutoCoder/Agentless`; SWE-bench Lite-S problem list; manual classification |
| **Funny fact** | প্রথম কয়েকজন author-এর ordering "Nigiri" দিয়ে ঠিক করা হয়েছে (footnote) — equal contribution |
| **আমাদের domain-এ গুরুত্ব** | ⭐⭐⭐⭐⭐ — (১) সবচেয়ে **reproducible ও সস্তা** strong baseline; (২) **benchmark reliability** নিয়ে প্রথম দিকের গুরুত্বপূর্ণ evidence (solution leakage, insufficient info, misleading solution); (৩) **generated test দিয়ে patch validation** — আমাদের Patch Validation ও LLM Test Generation sub-domain-এর সাথে সরাসরি যুক্ত |

## ★ সহজ ভাষায় পুরো Paper (প্রথমবার পড়ার জন্য)

> এই অংশটা শুধু প্রথমবার পড়ার জন্য। নিচের সব section-এর বিস্তারিত তথ্য আগের মতোই আছে। আগে এই ৫টা ছোট অংশ পড়ে নাও, তারপর বাকিটা পড়লে সবকিছু সহজ লাগবে।

### ক. Paper-টা কী নিয়ে?
- এটা একটা **নতুন technique-এর paper**। সাথে একটা **benchmark যাচাইয়ের কাজও** আছে।
- বানিয়েছেন Illinois বিশ্ববিদ্যালয়ের (UIUC) চারজন গবেষক: Chunqiu Steven Xia, Yinlin Deng, Soren Dunn ও Lingming Zhang। সাল 2024।
- বিষয়: AI দিয়ে software-এর bug নিজে নিজে ঠিক করানো। Test-এর জন্য ব্যবহার হয়েছে SWE-bench Lite (GitHub থেকে নেওয়া 300টা আসল bug)।
- তখন সবাই "বুদ্ধিমান agent" বানাচ্ছিল, যে নিজে সিদ্ধান্ত নেয় কী করবে। এই paper বলছে: অত জটিলতা কি আদৌ দরকার?
- তাদের tool-এর নাম **Agentless**। এখানে সিদ্ধান্ত নেয় মানুষের লেখা একটা সরল তিন-ধাপের নিয়ম, AI নিজে নয়।
- শেষে তারা দেখিয়েছে, যে benchmark দিয়ে সবাই মাপছে সেটাতেই অনেক ভুল আছে।

### খ. সমস্যাটা কী ছিল?
- তখনকার agent-গুলো (যেমন SWE-agent) AI-কে বলত "নিজে ঠিক করো কোন file খুলবে, কী চালাবে"। একটা bug ঠিক করতে লাগত ৩০–৪০টা ধাপ।
- **উপমা:** কাউকে বলা হলো "বাড়ির লোডশেডিং-এর কারণ খুঁজে ঠিক করো", কিন্তু কোনো নিয়ম বলে দেওয়া হলো না। সে প্রথমে ভুল মিটার বোর্ড খুলল। তারপর পরের সব সিদ্ধান্ত সেই ভুলের উপর দাঁড়াল।
- ফলে তিনটা কষ্ট: (১) খরচ বেশি, (২) কোথায় ভুল হলো বোঝা যায় না, (৩) অনেক tool-এর code-ই প্রকাশিত নয়, তাই তাদের দাবি যাচাই করা যায় না।
- **দ্বিতীয় সমস্যা:** SWE-bench Lite-এর কিছু problem-এর issue-তেই উত্তর লেখা আছে। কিছুতে এত কম তথ্য যে সঠিক কাজ করলেও test fail করে। কেউ এগুলো যাচাই করেনি।
- **উদাহরণ:** Test চাইছে error message ঠিক "invalid date" হতে হবে। কিন্তু issue-তে সেটা কোথাও লেখা নেই। AI ভালো fix লিখেও fail করবে।

### গ. Paper কী solve করেছে?
- **Agentless** বানিয়েছে: bug-এর জায়গা খোঁজা, অনেকগুলো fix বানানো, তারপর test চালিয়ে সেরাটা বাছাই। এই তিন ধাপ আগে থেকেই ঠিক করা।
- SWE-bench Lite-এর 300টা problem-এর **96টা (32.00%)** সমাধান করেছে। মানে ১০০টার মধ্যে ৩২টা। সব open-source agent-এর চেয়ে বেশি।
- খরচ গড়ে মাত্র **USD 0.70** প্রতি issue। একই AI (GPT-4o) দিয়ে SWE-agent-এর খরচ USD 2.53। মানে প্রায় ৩.৬ গুণ সস্তা।
- SWE-bench Lite-এর প্রতিটা problem হাতে পড়ে দেখেছে। **4.3%**-এ হুবহু উত্তর লেখা, **10%**-এ তথ্যই অপর্যাপ্ত, **5%**-এ ভুল পথ দেখানো। এগুলো বাদ দিয়ে পরিষ্কার সেট বানিয়েছে: **Lite-S (249টা)**।
- আরেকটা গুরুত্বপূর্ণ সংখ্যা: 40টা fix বানানোর পর **126টা (42.0%) issue-তে** অন্তত একটা fix ঠিক ছিল। কিন্তু বাছাই করে পাওয়া গেছে মাত্র 96টা। মানে সঠিক উত্তর হাতে পেয়েও প্রায় ৩০টা issue-তে ভুলটা বেছে ফেলেছে।

### ঘ. কীভাবে solve করেছে?
1. **Repo-র মানচিত্র বানাও:** পুরো project-এর শুধু folder ও file-এর নাম একটা তালিকায় সাজাও। কোনো code নেই। এতে AI অল্প লেখায় পুরো project দেখতে পায়।
2. **সন্দেহজনক file খোঁজো:** AI-কে issue ও মানচিত্র দেখিয়ে বলো "কোন ৩টা file-এ bug থাকতে পারে?" সাথে অর্থ মিলিয়ে খোঁজার (embedding) আরেকটা পদ্ধতি চালিয়ে দুটোর ফল মেলাও।
3. **ধাপে ধাপে zoom করো:** ঠিকানা খোঁজার মতো। আগে file, তারপর file-এর ভেতরের class/function-এর শুধু নাম, শেষে সেই function-এর পুরো code দেখে ঠিক কোথায় বদলাতে হবে।
4. **অনেক fix বানাও:** একই জায়গার জন্য AI-কে দিয়ে বারবার fix লেখাও। মোট 40টা। প্রতিটা "খুঁজে বদলাও" ধরনের সরল format-এ।
5. **Bug-টা দেখানোর test বানাও:** AI-কে দিয়ে একটা ছোট test লেখাও যা issue-র bug-টা ঘটিয়ে দেখায়। মূল code-এ চালিয়ে দেখো সত্যিই bug দেখা যায় কিনা।
6. **পুরনো test চালাও:** project-এর আগের test-গুলো চালাও। যে fix পুরনো কিছু ভেঙে দেয়, তাকে বাদ দাও।
7. **নতুন test-এ পরীক্ষা করো:** বাকি fix-গুলোর মধ্যে যেগুলো পাওয়া bug-test পাস করে, শুধু সেগুলো রাখো।
8. **ভোট নাও:** যে fix সবচেয়ে বেশিবার এসেছে (বানান-ফাঁকা-comment-এর পার্থক্য মুছে মিলিয়ে) সেটাই জমা দাও।

### ঙ. এরপর কী করা যায়?
- **Authors যা বলেছেন:** যে issue-তে "কোথায় bug" তার কোনো ইঙ্গিত নেই, সেখানে agent-রা ভালো। Agentless-কে সেখানে ভালো করানো future কাজ। আর fix বাছাইয়ের পদ্ধতি (re-ranking) আরও ভালো করা।
- **যা খোলা আছে:** 126 বনাম 96-এর ফাঁক। মানে সঠিক fix হাতে থেকেও ভুলটা বাছা।
- **যা খোলা আছে:** AI-র বানানো bug-test-এর অর্ধেকের বেশি (213-এর মধ্যে 119টা) ভালো নয়। আর "pass করল" মানেই "ঠিক" নয়।
- **আমরা SPL3-তে করতে পারি:** Agentless-এর 40টা fix একবার বানিয়ে জমিয়ে রাখি। তারপর নতুন নতুন বাছাইয়ের নিয়ম (re-ranker) বিনা খরচে পরীক্ষা করি।
- **আমরা করতে পারি:** একই pipeline বারবার চালিয়ে দেখি ফল একই আসে কিনা (reliability)।
- **আমরা করতে পারি:** বাছাই করা fix-এ security scan চালাই। Test pass করেও যে fix ঝুঁকিপূর্ণ, সেটা ধরি।

> **মনে রাখো:** ১. জটিল agent ছাড়াও সরল ৩-ধাপ pipeline দিয়ে 32.00% সমাধান ও কম খরচ সম্ভব।
> ২. SWE-bench Lite নিজেই নিখুঁত নয়, তাই score দেখে অন্ধভাবে বিশ্বাস করা যায় না।
> ৩. আসল সুযোগ হলো সঠিক fix বাছাই করা: 126 হাতে, কিন্তু পেয়েছি 96।

---

## ১. এক লাইনে Paper (TL;DR)

**জটিল autonomous agent ছাড়াই, শুধু একটা নির্দিষ্ট ৩-ধাপের pipeline (Localization → Repair → Patch Validation) দিয়ে LLM-কে চালালে SWE-bench Lite-এ সব open-source agent-এর চেয়ে বেশি issue (96/300 = 32.00%) সমাধান করা যায়, তাও গড়ে মাত্র USD 0.70 খরচে; সাথে paper-টা দেখিয়েছে যে SWE-bench Lite-এর বেশ কিছু problem নিজেই ত্রুটিপূর্ণ (solution আগেই লেখা, তথ্য অপর্যাপ্ত, বা ভুল পথ দেখানো)।**

**সহজ কথায়:** AI-কে সব সিদ্ধান্ত নিতে না দিয়ে মানুষ আগে থেকে তিনটা ধাপ ঠিক করে দিয়েছে: bug কোথায় খোঁজো, অনেক fix বানাও, test দিয়ে সেরাটা বাছো। এতে ফল ভালো এসেছে, খরচ কমেছে, আর কোন ধাপে ভুল হলো তা বোঝা যায়। আরেকটা আবিষ্কার: যে benchmark দিয়ে সবাই মাপছে, তার নিজেরই কিছু problem ত্রুটিপূর্ণ।

### Supervisor-কে ৩০ সেকেন্ডে কীভাবে বলবো
> "Sir, SWE-bench আসার পর সবাই SWE-agent, AutoCodeRover-এর মতো autonomous agent বানাচ্ছিল — যেখানে LLM নিজেই ঠিক করে পরের ধাপে কী করবে, কোন tool চালাবে। এই paper প্রশ্ন তুলেছে: এত জটিলতা কি আসলেই দরকার? তারা Agentless বানিয়েছে — LLM কোনো সিদ্ধান্ত নেয় না, মানুষের ঠিক করা ৩টা ধাপ চলে: প্রথমে hierarchical ভাবে bug-এর জায়গা খোঁজা (file → function → line), তারপর অনেকগুলো candidate patch তৈরি, শেষে regression test আর LLM-এর বানানো reproduction test দিয়ে filter করে majority voting-এ একটা patch বাছাই। GPT-4o দিয়ে এটা SWE-bench Lite-এ 32% solve করেছে — সব open-source agent-এর চেয়ে বেশি — আর খরচ SWE-agent-এর প্রায় চার ভাগের এক ভাগ। সাথে তারা দেখিয়েছে SWE-bench Lite-এর 4.3% issue-তে হুবহু solution লেখা আছে, 10% issue-তে যথেষ্ট তথ্য নেই, 5% issue ভুল সমাধান suggest করে — তাই তারা 249টা problem-এর পরিষ্কার subset Lite-S বানিয়েছে। পরে OpenAI-এর SWE-bench Verified একই দিকে গেছে। আমাদের reliability ও assurance domain-এর জন্য এটা দুই দিক থেকে গুরুত্বপূর্ণ: সরল-বোধগম্য pipeline, আর benchmark নিজেই কতটা বিশ্বাসযোগ্য সেই প্রশ্ন।"

---

## ২. Background — এই paper বুঝতে যা আগে জানা দরকার

### ২.১ আগের paper থেকে যা লাগবে (পুনরায় ব্যাখ্যা নয়)

| Concept | কোথায় ব্যাখ্যা আছে | এই paper-এ কীভাবে লাগে |
|---|---|---|
| SWE-bench, task instance, gold patch | Paper 01, Section ২ ও ৫ | Evaluation-এর মূল ভিত্তি |
| FAIL_TO_PASS / PASS_TO_PASS | Paper 01, Section ২.৫ | Final "resolved" যাচাই; Agentless নিজে P2P list ব্যবহার করে না (Section ৫.৩ দেখো) |
| Regression testing | Paper 01, Section ২.৪ | Patch filter-এর প্রথম ধাপ |
| Patch / unified diff | Paper 01, Section ২.২ | Agentless অন্য format (Search/Replace) ব্যবহার করে |
| BM25 retrieval | Paper 01, Section ২.৭ ও ৬.৫ | "RAG" baseline-এ ব্যবহৃত |
| Greedy decoding, Pass@k | Paper 01, Section ২.১০ ও ৬.৯–৬.১০ | Agentless greedy + sampling দুটোই ব্যবহার করে |
| Data contamination | Paper 01, Section ২.৯ | Threats to validity |
| Ablation study, Oracle | Paper 01, Section ৫.৪ | Section ৮-এর ablation |
| APR (Automated Program Repair) | Paper 01, Section ২.১১ | Repair phase |

### ২.২ SWE-bench Lite ও SWE-bench Verified
- **SWE-bench Lite:** SWE-bench-এর maintainer-দের বানানো **300টা problem**-এর subset — মূলত bug fixing, তুলনামূলক "self-contained" problem, যাতে সস্তায় evaluate করা যায়। এই paper-এর মূল evaluation dataset।
- **SWE-bench Verified:** OpenAI-এর বানানো **500টা problem**-এর subset, যেখানে মানুষ (developer) যাচাই করেছে যে প্রতিটা issue-তে সমাধান করার মতো যথেষ্ট তথ্য আছে। Paper-এর Table 6-এ এর উপর result আছে।

### ২.৩ LLM Agent কী? (Agent-based approach)
- **Agent** = LLM + **tool** (file খোলা/লেখা, code search, test চালানো, shell command) + **loop**।
- প্রতিটা **turn**-এ LLM একটা action বেছে নেয় → environment থেকে **feedback/observation** পায় → সেই অনুযায়ী পরের action **নিজে plan** করে।
- একটা issue সমাধানে agent **30–40টা turn** পর্যন্ত নিতে পারে (paper-এর ভাষ্য)।
- উদাহরণ: **Devin** (commercial), **OpenDevin** (open-source), **SWE-agent** (Paper 02 — custom Agent-Computer Interface বা ACI), **AutoCodeRover** (Paper 03 — code search API দিয়ে context খোঁজা), **Aider** (repository map + simple diff + regression test), **Moatless** (code search tool + LLM-বানানো query দিয়ে retrieval), **SpecRover** (AutoCodeRover-এর উন্নত রূপ, specification inference + reproduction test)।

**সহজ উপমা:** Agent হলো এমন একজন intern-এর মতো যাকে বলা হয়েছে "যা দরকার করো" — সে নিজে ঠিক করে কোন file খুলবে, কী চালাবে। ভালো হলে দারুণ, কিন্তু ভুল পথে গেলে ঘুরতেই থাকে।

### ২.৪ Agentless approach কী?
- **Agentless** = workflow আগে থেকে **মানুষ ঠিক করে দিয়েছে**। LLM প্রতিটা ধাপে শুধু একটা নির্দিষ্ট ছোট কাজ করে (যেমন "এই tree থেকে সন্দেহজনক 3টা file বলো"), কিন্তু **পরের ধাপ কী হবে তা LLM ঠিক করে না**, আর LLM কোনো জটিল tool চালায় না।
- উপমা: Agent = "নিজে রান্না শিখে নাও"; Agentless = "রেসিপি-র প্রতিটা ধাপ লেখা আছে, শুধু প্রতিটা ধাপ ভালোভাবে করো"।
- Paper নিজেই স্বীকার করে: কোনো একক technique নতুন বা "revolutionary" নয় — নতুনত্ব হলো **সঠিকভাবে combine করা** এবং প্রমাণ করা যে এত সরল design দিয়েও agent-এর সমান বা বেশি ভালো করা যায়।

### ২.৫ Fault Localization (FL)
Bug-টা code-এর **কোথায়** আছে তা খুঁজে বের করা। Paper-এর related work অনুযায়ী প্রধান ধরন:

| ধরন | মূল ধারণা | উদাহরণ |
|---|---|---|
| **Spectrum-based FL (SBFL)** | যে line বেশি failing test-এ execute হয়, কম passing test-এ — সেটা বেশি সন্দেহজনক | Tarantula, Ochiai |
| **Mutation-based FL (MBFL)** | কোনো line-এ ছোট পরিবর্তন (mutant) করলে test result কতটা বদলায় | Metallaxis-FL |
| **IR-based FL** | Bug report-কে query ধরে code-এর সাথে text similarity মিলানো (static) | BugLocator ধরনের কাজ |
| **Learning-based FL** | একাধিক signal ML দিয়ে combine | DeepFL, FLUCCS, TRANSFER |
| **LLM-based FL** | LLM সরাসরি code ও bug report বুঝে location বলে | AgentFL ইত্যাদি |

**সহজ কথায়:** Bug খোঁজার পুরনো পদ্ধতিগুলো মূলত test চালিয়ে বা শব্দ মিলিয়ে কাজ করে। Agentless দুটো আলাদা সংকেত মেলায়: AI-র বুদ্ধি আর অর্থ-মেলানো খোঁজ।

Agentless-এর localization = **LLM-based + IR-based (embedding)** এর মিশ্রণ, আর এটা **test চালায় না** (তাই SBFL/MBFL নয়)। কারণ SWE-bench-এর বাস্তব setting-এ শুরুতে কোনো bug-triggering test থাকে না।

### ২.৬ Hierarchical Localization (file → class/function → edit location)
বড় repository-তে সরাসরি "কোন line বদলাতে হবে" জিজ্ঞেস করা অসম্ভব (হাজার হাজার file)। তাই ধাপে ধাপে zoom-in:
1. **File level:** পুরো repo-র শুধু folder/file নামের tree দেখে সন্দেহজনক top-N file।
2. **Element level:** ঐ file-গুলোর শুধু class/function-এর **header (skeleton)** দেখে প্রাসঙ্গিক class/function।
3. **Edit location level:** ঐ element-গুলোর পুরো code দেখে নির্দিষ্ট line/function/class।

**উপমা:** ঠিকানা খোঁজা — আগে জেলা, তারপর থানা, তারপর বাড়ির নম্বর। প্রতিটা ধাপে context ছোট হয়, তাই LLM বিভ্রান্ত হয় কম (Paper 01-এর "বেশি context = খারাপ performance" finding মনে করো)।

### ২.৭ Repository Structure Format
Linux-এর `tree` command-এর মতো repository-র একটা text representation — শুধু folder ও file-এর নাম, indentation দিয়ে hierarchy বোঝানো। কোনো code থাকে না। উদাহরণ (আমার বানানো):
```text
django/
    forms/
        fields.py
        widgets.py
    views/
        static.py
        generic/
            detail.py
```
এতে পুরো repo-র "মানচিত্র" খুব কম token-এ (token = LLM-এর পড়া বা লেখার ছোট শব্দ-টুকরা) LLM-কে দেখানো যায়।

### ২.৮ Skeleton Format
একটা file-এর **compressed রূপ**: শুধু class ও function-এর declaration header, class-এর field ও method signature, আর class/module level comment — function-এর ভেতরের body বাদ (`...` দিয়ে বোঝানো)। উদাহরণ (আমার বানানো, paper-এর Figure 2-এর মতো):
```python
class UUIDField(CharField):
    default_error_messages = {...}
    def prepare_value(self, value):
        ...
    def to_python(self, value):
        ...
def slugify(value, allow_unicode=False):
    ...
```
হাজার line-এর file কয়েক ডজন line-এ নেমে আসে। (মানে: বইয়ের শুধু সূচিপত্র দেখা, পুরো বই নয়।)

### ২.৯ Embedding ও Embedding-based Retrieval
- **Embedding:** একটা text বা code টুকরাকে একটা লম্বা সংখ্যার vector-এ রূপান্তর, যাতে **অর্থে কাছাকাছি** দুটো text-এর vector-ও কাছাকাছি হয়।
- **Chunking:** বড় file-কে ছোট ছোট টুকরায় (chunk) ভাগ করা — Agentless-এ chunk size 512, overlap 0।
- **Cosine similarity:** দুটো vector-এর মধ্যে কোণের cosine — 1 মানে একই দিকে (খুব মিল), 0 মানে সম্পর্কহীন। (সূত্র Section ৬-এ)
- **BM25 (Paper 01) বনাম Embedding:** BM25 শুধু **শব্দ মেলায়**; embedding **অর্থ (semantics)** কিছুটা ধরতে পারে — যেমন issue-তে "proxy error" আর code-এ `get_connection` — শব্দ আলাদা হলেও embedding কাছাকাছি হতে পারে।
- **Tool:** LlamaIndex (retrieval framework), OpenAI-এর `text-embedding-3-small` model।

### ২.১০ Search/Replace Diff Format
Unified diff (Paper 01-এর `-`/`+` format) LLM-এর জন্য লেখা কঠিন — line number, header, context line সব ঠিক হতে হয়। আর পুরো file আবার লেখা ব্যয়বহুল ও hallucination-প্রবণ (মানে LLM বানিয়ে ভুল কিছু লিখে ফেলে)। **Search/Replace** format (Aider tool থেকে নেওয়া) অনেক সহজ:
```text
### django/utils/text.py
<<<<<<< SEARCH
def slugify(value, allow_unicode=False):
    value = str(value)
=======
def slugify(value, allow_unicode=False):
    value = str(value).strip()
>>>>>>> REPLACE
```
- **SEARCH** অংশ = মূল file-এ যে code হুবহু আছে।
- **REPLACE** অংশ = তার জায়গায় যা বসবে।
- Apply করতে শুধু SEARCH text খুঁজে REPLACE দিয়ে বদলে দিলেই হয়। Line number লাগে না।
- লাভ: কম token (সস্তা), ছোট edit-এ মনোযোগ, hallucination-এর সুযোগ কম (paper-এর দাবি)।

### ২.১১ Sampling with Temperature
- **Greedy decoding** (Paper 01): প্রতিবার সবচেয়ে সম্ভাব্য token → একই input-এ একই output।
- **Sampling:** probability অনুযায়ী random ভাবে token বাছাই → প্রতিবার ভিন্ন output।
- **Temperature (T):** কতটা "random" হবে তার knob। T ছোট → প্রায় greedy; T বড় → বেশি বৈচিত্র্য। Agentless-এ **T = 0.8**। (সূত্র Section ৬-এ)
- কেন দরকার: একই issue-র জন্য **অনেক ভিন্ন candidate patch** পেতে, যাতে অন্তত একটা সঠিক হওয়ার সম্ভাবনা বাড়ে।

### ২.১২ Generate-and-Validate APR, Plausible বনাম Correct Patch
- APR-এর classic ধারা: **অনেক candidate patch generate করো → test দিয়ে validate করো**।
- **Plausible patch:** যে patch available test pass করে। **Correct patch:** যেটা আসলেই developer-এর উদ্দেশ্য অনুযায়ী ঠিক। Plausible সবসময় correct নয় (patch overfitting — Paper 01, Section ১২ দেখো)।
- Classic setup-এ bug-triggering test আগে থেকেই থাকে। কিন্তু **SWE-bench-এর বাস্তব setting-এ issue সবে খোলা হয়েছে, তাই bug-triggering test নেই** — শুধু পুরনো regression test আছে। এজন্যই Agentless নিজে reproduction test বানায়।

### ২.১৩ Reproduction Test (Bug-reproducing test)
LLM-কে দিয়ে লেখানো একটা test file যেটা issue-তে বর্ণিত bug-টা **পুনরায় ঘটায়**, আর patch-এর পরে bug ঠিক হয়েছে কিনা তাও **যাচাই** করে। এর তিনটা নির্দিষ্ট output:

| Output | মানে |
|---|---|
| `Issue reproduced` | Bug এখনো আছে (মূল codebase-এ এটাই আসা উচিত) |
| `Issue resolved` | Bug ঠিক হয়েছে (সঠিক patch-এর পরে এটাই আসা উচিত) |
| `Other issues` | অপ্রত্যাশিত কিছু ঘটেছে (crash, import error ইত্যাদি) |

উদাহরণ (আমার বানানো, paper-এর Figure 4-এর ধাঁচে):
```python
from mylib import parse_date

def test_issue():
    try:
        result = parse_date("2024-02-30")
    except Exception:
        print("Other issues")
        return
    if result is not None:
        print("Issue reproduced")   # invalid date গ্রহণ করছে = bug
    else:
        print("Issue resolved")

test_issue()
```

### ২.১৪ Regression Test Filtering
- Repository-র **সব existing test** মূল codebase-এ চালিয়ে যেগুলো pass করে সেগুলো নেওয়া হয়।
- কিন্তু সবগুলো regression test হিসেবে রাখা ঠিক না — issue ঠিক করতে গিয়ে কিছু পুরনো behaviour **ইচ্ছাকৃতভাবে বদলাতে** হতে পারে, তখন সেই পুরনো test fail করাই স্বাভাবিক।
- তাই LLM-কে passing test-এর list দিয়ে জিজ্ঞেস করা হয় "কোন test গুলো এই fix-এর কারণে বদলাতে পারে?" — সেগুলো বাদ দিয়ে বাকিগুলো = **final regression test set**।
- গুরুত্বপূর্ণ: SWE-bench-এর দেওয়া PASS_TO_PASS list **ব্যবহার করা হয়নি** (SWE-bench maintainer-দের অনুরোধে), কারণ সেটা gold patch দেখে বানানো — বাস্তবে আগে থেকে জানা যায় না।

### ২.১৫ Majority Voting ও Patch Normalization
- **Majority voting (self-consistency):** অনেক independent sample-এর মধ্যে যে উত্তর সবচেয়ে বেশিবার এসেছে, সেটা বেছে নাও — ধারণা হলো "সঠিক উত্তরে model বারবার পৌঁছায়, ভুল উত্তর ছড়িয়ে-ছিটিয়ে থাকে"।
- **সমস্যা:** দুটো patch অর্থে একই কিন্তু space, newline, comment-এ আলাদা হলে আলাদা গণনা হবে।
- **Normalization:** Patch apply করার আগের ও পরের code-কে Python-এর `ast` library দিয়ে **Abstract Syntax Tree (AST)**-এ parse → আবার canonical source code-এ unparse (docstring বাদ) → এই standardized পুরনো ও নতুন code-এর diff = **normalized patch**। এতে surface-level পার্থক্য মুছে যায়।
- **AST:** code-এর গঠনগত tree representation — space, comment, formatting হারিয়ে যায়, শুধু structure থাকে।

### ২.১৬ Benchmark Quality Problem — Agentless যেগুলো খুঁজে পেয়েছে
| সমস্যা | মানে | কেন বিপজ্জনক |
|---|---|---|
| **Solution leakage (Exact patch)** | Issue description-এই হুবহু সঠিক patch লেখা | Tool "copy" করে score পায় — আসল ability নয় |
| **Complete steps in NL** | সমাধানের সব ধাপ ভাষায় লেখা | Problem অনেক সহজ হয়ে যায় |
| **Insufficient information** | যথেষ্ট তথ্য নেই — যেমন test একটা নির্দিষ্ট function নাম বা error message string চায় যা issue-তে বলা নেই; বা issue-তে দুটো সমাধান suggest করা, test শুধু একটাকে মানে | Functionally ঠিক patch-ও fail — tool-কে অন্যায়ভাবে শাস্তি |
| **Misleading solution** | Issue-তে প্রস্তাবিত সমাধান developer-এর আসল patch-এর সাথে মেলে না | Issue অনুসরণ করলেই ভুল patch |

**সহজ কথায়:** চার ধরনের গোলমাল আছে। কোথাও উত্তর আগেই লেখা (নকল করা সহজ)। কোথাও তথ্য কম (সঠিক fix-ও fail করে)। কোথাও ভুল পরামর্শ দেওয়া। এগুলো থাকলে score দেখে tool-এর আসল ক্ষমতা বোঝা যায় না।

### ২.১৭ SWE-bench Lite-S
উপরের তিন ধরনের problematic problem (exact patch, misleading solution, insufficient info) বাদ দিয়ে SWE-bench Lite-এর **249টা problem-এর filtered subset**। লক্ষ্য: কম "অযৌক্তিক" problem, আর difficulty level normalize করা।

### ২.১৮ Cost ও Token Metric
- **Avg. Cost (USD):** প্রতিটা issue-তে LLM API-র গড় খরচ।
- **Avg. # Tokens:** প্রতিটা issue-তে LLM-কে পাঠানো ও পাওয়া মোট token-এর গড়।
- Paper 01-এ cost মাপা হয়নি (Paper 01, Section ১২ critique #7) — এই paper সেই gap কিছুটা পূরণ করেছে।

---

## ৩. Problem Statement — কী সমস্যা ছিল?

### ৩.১ মূল সমস্যা: Agent-based approach-এর তিনটা সীমাবদ্ধতা (authors-এর যুক্তি)
1. **Complex tool usage/design:** Agent-কে tool দিতে হলে environment আর LLM-এর মাঝে একটা abstraction layer (API call format) বানাতে হয়। Input/output format সতর্কভাবে design না করলে tool ভুলভাবে ব্যবহার হয় — performance কমে আর wasted LLM query-তে খরচ বাড়ে। Agent iterative হওয়ায় একবারের ভুল পরের সব turn-এ প্রভাব ফেলে।
2. **Lack of control in decision planning:** কখন কী action নেবে তা agent নিজে ঠিক করে, প্রায় কোনো check ছাড়াই। Action space বড় হওয়ায় agent সহজেই বিভ্রান্ত হয়ে অপ্রয়োজনীয় exploration করে। 30–40 turn-এর trajectory-তে (trajectory = agent-এর ধাপে ধাপে করা সব কাজের পুরো ইতিহাস) কোথায় ভুল সিদ্ধান্ত হয়েছে তা বোঝা ও debug করা খুব কঠিন।
3. **Limited ability to self-reflect:** Agent সব feedback গ্রহণ করে, কিন্তু অপ্রাসঙ্গিক, ভুল বা বিভ্রান্তিকর তথ্য filter করতে পারে না। ফলে একটা ভুল step পরের সব সিদ্ধান্তে **amplify** হয়।

### ৩.২ দ্বিতীয় সমস্যা: Benchmark নিজেই কতটা বিশ্বাসযোগ্য?
সবাই leaderboard-এ র‍্যাঙ্ক নিয়ে ব্যস্ত, কিন্তু কেউ যাচাই করেনি SWE-bench Lite-এর problem-গুলো আদৌ ন্যায্য কিনা — কিছু problem-এ solution আগেই লেখা, কিছু অসম্ভব।

### ৩.৩ কেন এটা গুরুত্বপূর্ণ?
- জটিল agent **reproduce করা কঠিন** (fully autonomous, non-deterministic trajectory), অনেক commercial tool code বা trajectory-ই release করে না — তাই তাদের দাবি **যাচাই করা যায় না**।
- **Reliability ও assurance-এর দৃষ্টিতে (আমার মন্তব্য):** যে system-এর সিদ্ধান্তের পথ বোঝা যায় না, তাকে assure করাও কঠিন। Agentless-এর প্রতিটা ধাপ আলাদাভাবে মাপা যায় — এটা assurance-এর জন্য বড় সুবিধা।

---

## ৪. Goal ও Research Questions

**Goal:** "Do we really have to employ complex autonomous software agents?" — এই প্রশ্নের উত্তর দেওয়া, এবং autonomous software agent-এর জন্য baseline, starting point ও horizon "reset" করা।

Paper-এ RQ explicitly numbered নেই; evaluation section থেকে implicit RQ গুলো:
- **RQ1 (Effectiveness):** একটা সরল agentless pipeline কি state-of-the-art agent-দের সাথে প্রতিযোগিতা করতে পারে? (Table 1)
- **RQ2 (Cost):** খরচ ও token ব্যবহারে কেমন? (Table 1)
- **RQ3 (Localization quality):** Submitted patch সঠিক file/function/line-এ edit করছে কি? (Table 1, Table 2)
- **RQ4 (Component contribution):** Localization, repair, patch validation-এর প্রতিটা অংশ কতটা অবদান রাখে? (Table 2, 3, 4; Figure 6, 7)
- **RQ5 (Benchmark quality):** SWE-bench Lite-এর problem-গুলোর মান কেমন — leakage, অপর্যাপ্ত তথ্য, misleading solution কত %? (Figure 8)
- **RQ6 (Robust comparison):** Problematic problem বাদ দিলে (Lite-S) ranking কি বদলায়? কোন ধরনের problem কে ভালো solve করে? (Table 5, Figure 9)
- **RQ7 (Generalization):** SWE-bench Verified-এও কি ফল ধরে রাখে? (Table 6)

---

## ৫. Methodology — কীভাবে কাজটা করা হয়েছে

### ৫.১ পুরো Pipeline এক নজরে (Figure 1-এর ১০টা ধাপ)

| ধাপ | Phase | কী হয় | LLM কী দেখে | Output |
|---|---|---|---|---|
| 1 | Localization | Codebase-কে tree-আকারের repository structure-এ রূপান্তর | — | Repo structure text |
| 2 | Localization | LLM-কে top-N সন্দেহজনক file বলতে বলা | Issue + repo structure | Prompting-based file list |
| 3 | Localization | Embedding-based retrieval দিয়ে আরও file | Issue + code chunk (embedding) | Retrieval-based file list → দুটো মিলিয়ে final file list |
| 4 | Localization | প্রতিটা file-এর skeleton দেখে প্রাসঙ্গিক class/function | Issue + সব file-এর skeleton (এক prompt-এ) | Related elements |
| 5 | Localization | Element-গুলোর পুরো code দেখে নির্দিষ্ট edit location | Issue + element-গুলোর code | Edit locations (line/function/class) |
| 6 | Repair | Edit location-এর code দেখে অনেক candidate patch | Issue + context window | Search/Replace patches |
| 7 | Patch Validation | অনেক reproduction test sample | Issue + example test format | Candidate tests |
| 8 | Patch Validation | মূল codebase-এ চালিয়ে "Issue reproduced" দেয় এমন test বাছাই, normalize করে সবচেয়ে frequent টা | Execution result | Final reproduction test |
| 9 | Patch Validation | Regression test + reproduction test দিয়ে patch filter ও rank | Execution result | Filtered patches |
| 10 | Patch Validation | Majority voting দিয়ে top patch | Normalized patches | **Submitted patch** |

**সহজ কথায়:** ১০টা ধাপ আসলে তিন ভাগে ভাগ করা: (১) bug কোথায় খোঁজো (ধাপ ১–৫), (২) fix বানাও (ধাপ ৬), (৩) test দিয়ে সেরা fix বাছাই করো (ধাপ ৭–১০)। প্রতিটা ভাগ আলাদা করে মাপা যায়।

### ৫.২ Phase 1: Localization (৩ ধাপ, hierarchical)

**৫.২.১ Suspicious file-এ localize করা**
1. **Prompting-based:** Repository structure format (root থেকে recursive traverse, একই level-এর file/folder সারিবদ্ধ, sub-directory indented) + issue description LLM-কে দিয়ে **top N সন্দেহজনক file** চাওয়া হয়। এটা শুধু file-এর **নাম** দেখে সিদ্ধান্ত।
2. **Embedding-based (পরিপূরক):** শুধু নাম দেখে সব বোঝা যায় না, তাই code content-ভিত্তিক retrieval:
   - প্রথমে LLM-কে repo structure দিয়ে **irrelevant folder**-এর list চাওয়া হয় → সেগুলোর সব file বাদ।
   - বাকি file-গুলোকে chunk-এ ভাগ করে প্রতিটা chunk-এর embedding।
   - Issue description-এর embedding (query) ও প্রতিটা chunk-এর cosine similarity → সবচেয়ে মিল থাকা chunk যেসব file-এ আছে সেগুলো।
3. **Combine:** দুই পদ্ধতিতে পাওয়া file-গুলোর মধ্যে "top N most common" file নেওয়া হয় → final suspicious file list।
- **Default:** N = **3** file, greedy decoding।

**৫.২.২ Related element-এ localize করা (class / function / variable)**
- প্রতিটা suspicious file-এর **skeleton format** বানানো (class/function header, class field ও method signature, class/module-level comment)।
- **সব file-এর skeleton একসাথে এক prompt-এ** দেওয়া হয়, যাতে LLM তুলনা করে সবচেয়ে প্রাসঙ্গিক element বাছতে পারে।
- Output: পরীক্ষা করার মতো class ও function-এর list। **Default:** সংখ্যার কোনো সীমা নেই (unrestricted), greedy decoding।

**৫.২.৩ Edit location-এ localize করা**
- আগের ধাপের element-গুলোর (বিভিন্ন file থেকে আসতে পারে) **পুরো code** LLM-কে দেওয়া হয়।
- LLM final edit location বলে — line number, function, বা class হিসেবে।
- **Default:** এই ধাপে **4টা sample** নেওয়া হয় → **4টা আলাদা edit location set** (merge করা হয় না — Section ৮.৬ দেখো কেন)।

**সহজ কথায়:** Localization-এ বড় থেকে ছোটর দিকে যাওয়া হয়। প্রথমে ৩টা file, তারপর কয়েকটা function, শেষে কয়েকটা line। প্রতিবার AI কম code দেখে, তাই বিভ্রান্ত হয় কম।

### ৫.৩ Phase 2: Repair
1. **Context window তৈরি:** Edit location যদি line $a$ থেকে $b$ হয়, তাহলে $[a - x,\; b + x]$ line পর্যন্ত code দেওয়া হয় ($x$ = context size)। একাধিক location হলে window-গুলো `...` দিয়ে জোড়া লাগানো হয়। **Default:** $x$ = **±10 line**।
2. **Patch generation:** LLM-কে **Search/Replace** format-এ patch লিখতে বলা হয় (Aider-এর format)।
3. **Multiple sampling:** প্রতিটা location set-এর জন্য **10টা patch: 1টা greedy + 9টা sampled (T = 0.8)**।
4. **মোট:** 4 location set × 10 = **প্রতি issue-তে 40টা candidate patch**।

**সহজ কথায়:** Repair-এ AI একটা fix নয়, অনেকগুলো (40টা) fix বানায়। একটা ভুল হলেও বাকিগুলোর মধ্যে ঠিকটা থাকার সম্ভাবনা বাড়ে। AI-কে শুধু বদলানোর জায়গার আশপাশের কয়েকটা line দেখানো হয়, যাতে সে সহজে ঠিক জায়গায় মন দেয়।

### ৫.৪ Phase 3: Patch Validation

**৫.৪.১ Reproduction test generation**
1. LLM-কে issue description + একটা example reproduction test (format দেখানোর জন্য) দেওয়া হয়।
2. **40টা candidate test (1 greedy + 39 sampled)** তৈরি।
3. প্রতিটা test **মূল (bug থাকা) codebase-এ চালানো** হয় → যেগুলো `Issue reproduced` print করে না সেগুলো বাদ।
4. বাকিগুলোকে **normalize** (comment, extra space মুছে, test-এর নাম standardize) করে **সবচেয়ে বেশিবার আসা** test-টা = final reproduction test।
5. Paper-এর জোর: agent-based tool যেখানে LLM-কে দিয়েই বিচার করায় "test ঠিক কিনা", Agentless সেখানে **সত্যিকারের execution result** দেখে বিচার করে।

**৫.৪.২ Regression test নির্বাচন**
1. Repository-র **সব existing test** মূল codebase-এ চালিয়ে passing test-গুলো বের করা।
2. LLM-কে এই list দিয়ে জিজ্ঞেস — কোন test গুলো fix-এর পরে চালানো উচিত না (fix করতে গিয়ে যেগুলো update হতে পারে)?
3. সেগুলো বাদ দিয়ে = **regression test set**।
4. **SWE-bench-এর PASS_TO_PASS list ব্যবহার করা হয়নি** (maintainer-দের অনুরোধ)। Footnote অনুযায়ী, P2P list সরাসরি ব্যবহার করলে SWE-bench Lite-এ performance হতো **98** (96-এর বদলে)।
5. এজন্য official SWE-bench evaluation setup **modify** করা হয়েছে যাতে ইচ্ছামতো regression ও reproduction test চালানো যায়।

**৫.৪.৩ Patch selection (filtering + re-ranking)**
1. সব 40টা patch-এ regression test চালানো → **সবচেয়ে কম regression failure** যেসব patch-এর, শুধু সেগুলো রাখা।
2. সেগুলোতে final reproduction test চালানো → শুধু যেগুলো `Issue resolved` দেয় সেগুলো রাখা।
3. **Fallback:** কোনো patch-ই reproduction test pass না করলে (test নিজেই ভুল হতে পারে) → শুধু regression result দিয়ে selection।
4. **Majority voting:** বাকি patch-গুলোকে AST দিয়ে normalize করে সবচেয়ে বেশিবার আসা normalized patch = **final submission**।
5. **Conservative design:** একটা patch reproduction test pass করলেও যদি regression-এ খারাপ করে, সেটা বাদ — অর্থাৎ ভুল reproduction test একটা ভুল patch-কে টেনে তোলার সম্ভাবনা কমানো হয়েছে।

**সহজ কথায়:** ৪০টা fix থেকে সেরা বাছাইয়ের ছাঁকনি তিনটা: (১) পুরনো কিছু ভাঙল কিনা (regression), (২) বানানো bug-test পাস করল কিনা, (৩) বাকিদের মধ্যে ভোটে কে এগিয়ে। পরীক্ষা বেশিরভাগ ক্ষেত্রে সত্যিকারের চালানো ফল দেখে হয়, AI-র মতামতে নয়।

### ৫.৫ Benchmark Analysis-এর পদ্ধতি (Section 6 of paper)
- SWE-bench Lite-এর **300টা problem-এর প্রতিটা manually classify** করা হয়েছে — issue description ও ground-truth developer patch দেখে।
- **৩টা dimension:**
  1. **Description quality:** (i) NL-এ যথেষ্ট তথ্য, (ii) reproducible failure example আছে, (iii) আংশিক reproducible example, (iv) যথেষ্ট তথ্য নেই।
  2. **Solution in description:** (i) কোনো solution নেই, (ii) আংশিক (কিছু ধাপ NL-এ), (iii) সম্পূর্ণ ধাপ NL-এ, (iv) exact patch, (v) misleading solution।
  3. **Location information** (line / function / file তিন granularity-তে): (i) NL-এ exact location, (ii) stack trace-এ (error-এর সময় program কোন কোন জায়গা দিয়ে গিয়েছিল তার তালিকা) exact location, (iii) location খোঁজার মতো keyword, (iv) কিছুই নেই।
- **Lite-S তৈরি:** "exact patch", "misleading solution" ও "not enough info" — এই problem-গুলো বাদ → **249টা problem**।

**সহজ কথায়:** এই paper-এর দ্বিতীয় অংশের কাজ ছিল পুরো SWE-bench Lite হাতে পড়ে problem-গুলো ভাগ করা: description কেমন, উত্তর আগেই দেওয়া আছে কিনা, bug-এর জায়গার ইঙ্গিত আছে কিনা। এর ফলেই Lite-S তৈরি হয়েছে।

### ৫.৬ Agent বনাম Agentless — design তুলনা

| দিক | Agent-based (SWE-agent, AutoCodeRover ইত্যাদি) | Agentless |
|---|---|---|
| পরের ধাপ কে ঠিক করে? | LLM নিজে | মানুষের লেখা fixed pipeline |
| Tool ব্যবহার | LLM tool call করে (edit, search, bash) | LLM কোনো tool চালায় না; script test চালায় |
| Turn সংখ্যা | পরিবর্তনশীল, 30–40 পর্যন্ত | নির্দিষ্ট সংখ্যক prompt |
| Trajectory বোঝা/debug | কঠিন | প্রতিটা phase আলাদা মাপা যায় |
| Patch সংখ্যা | সাধারণত একটা trajectory → একটা patch | 40টা candidate → selection |
| Reproduction test বিচার | প্রায়ই LLM নিজে বিচার করে test ঠিক কিনা | Execution result দিয়ে বিচার |

**সহজ কথায়:** Agent-এ "এরপর কী করব" AI ঠিক করে। Agentless-এ সেটা মানুষ আগে থেকে লিখে রেখেছে, তাই এটা একটা সোজা পাইপলাইন, যাতে কোথাও ঘুরে বেড়ানোর সুযোগ নেই।

---

## ৬. Mathematical Formulation — সূত্র ও ব্যাখ্যা

Paper-এ কোনো formal equation নেই — সবই ভাষায় বর্ণনা। নিচের formalization **আমার নিজের** (paper-এর বর্ণনা থেকে বানানো), যাতে supervisor-কে precise ভাবে দেখানো যায়। সব সংখ্যা paper-এর।

### ৬.১ Task ও পুরো Pipeline (function composition হিসেবে)
Paper 01-এর notation অনুযায়ী একটা task: issue $P$, codebase $C$। Agentless একটা function:
$$
\hat{\delta} = \text{Agentless}(P, C) = \text{Select}\left( \text{Repair}\left( \text{Loc}(P, C) \right),\; \text{Tests}(P, C) \right)
$$
Localization নিজেই তিনটা function-এর composition:
$$
\text{Loc} = L_{\text{edit}} \circ L_{\text{elem}} \circ L_{\text{file}}
$$

**সূত্রের মানে (কথায়):** প্রথম সূত্র বলছে, শেষ patch আসে তিনটা কাজ পরপর করে: bug-এর জায়গা খোঁজা, সেখানে fix বানানো, তারপর test দিয়ে সেরা fix বাছা। দ্বিতীয় সূত্র বলছে, জায়গা খোঁজার কাজটাও নিজে তিন ধাপের: file, তারপর function, তারপর line।

| Symbol | মানে |
|---|---|
| $P$ | Issue description (problem statement) |
| $C$ | Bug থাকা অবস্থার codebase |
| $L_{\text{file}}$ | File-level localization → file set $F$ |
| $L_{\text{elem}}$ | Skeleton দেখে element-level localization → element set $\mathcal{E}$ |
| $L_{\text{edit}}$ | Edit-location localization → location set-গুলো $E_1, \ldots, E_4$ |
| $\text{Repair}$ | Location থেকে candidate patch set $\mathcal{P}$ |
| $\text{Tests}$ | Regression set $\mathcal{T}_{\text{reg}}$ ও reproduction test $r^{*}$ |
| $\text{Select}$ | Filtering + majority voting → final patch $\hat{\delta}$ |
| $\circ$ | Function composition (ডান থেকে বামে প্রয়োগ) |

**মূল পার্থক্য (agent-এর সাথে):** Agent-এ পরের function কোনটা হবে তা LLM-এর output-এর উপর নির্ভর করে (dynamic)। এখানে composition-টা **fixed** — তাই এটা "agentless"।

### ৬.২ File-level Localization
**Prompting-based:**
$$
F_{\text{prompt}} = \text{LLM}_{\text{greedy}}\left( P,\; S(C) \right), \qquad \text{size} \leq N
$$
এখানে $S(C)$ = repository structure format।

**Embedding-based:** প্রথমে irrelevant folder বাদ দিয়ে বাকি file-গুলোকে chunk $c_1, \ldots, c_m$-এ ভাগ। Embedding function $\phi$:
$$
\text{sim}(P, c_i) = \cos\theta = \frac{\phi(P) \cdot \phi(c_i)}{\| \phi(P) \| \; \| \phi(c_i) \|}
$$
সবচেয়ে বেশি similarity-র chunk যে file-গুলোতে আছে = $F_{\text{embed}}$।

**Combine:**
$$
F = \text{Top}_N \left( F_{\text{prompt}} \cup F_{\text{embed}} \right) \quad \text{(দুই list-এ কতবার এসেছে সেই অনুযায়ী)}, \qquad N = 3
$$

**সূত্রের মানে (কথায়):** প্রথম সূত্র বলছে, AI-কে file-এর নামের তালিকা ও issue দিলে সে সর্বোচ্চ N-টা সন্দেহজনক file বলবে। দ্বিতীয় সূত্র (cosine) দুটো লেখা অর্থে কতটা কাছাকাছি তা মাপে। ১-এর কাছে মানে খুব মিল, ০-এর কাছে মানে কোনো মিল নেই। তৃতীয় সূত্র দুই পদ্ধতির ফল মিলিয়ে সবচেয়ে বেশিবার আসা N-টা file বাছে।

| Symbol | মানে |
|---|---|
| $\phi(\cdot)$ | Embedding model (`text-embedding-3-small`) — text কে vector বানায় |
| $c_i$ | একটা code chunk (size 512, overlap 0) |
| $\cdot$ | Dot product |
| $\| v \|$ | Vector-এর দৈর্ঘ্য (norm) |
| $N$ | কতগুলো file রাখা হবে (= 3) |

**নোট:** "top N most common" এর সঠিক tie-breaking rule paper-এ বলা নেই — implementation-এ code দেখে নিশ্চিত হতে হবে।

**Cosine similarity worked example (খেলনা 3-dimension vector, আমার বানানো):** $\phi(P) = (1, 2, 0)$, chunk $c_1 = (2, 4, 1)$, chunk $c_2 = (0, 1, 3)$।
- $\phi(P) \cdot c_1 = 2 + 8 + 0 = 10$; $\| \phi(P) \| = \sqrt{5} \approx 2.236$; $\| c_1 \| = \sqrt{21} \approx 4.583$ → $\cos = 10 / 10.247 \approx 0.976$
- $\phi(P) \cdot c_2 = 0 + 2 + 0 = 2$; $\| c_2 \| = \sqrt{10} \approx 3.162$ → $\cos = 2 / 7.071 \approx 0.283$
- তাই $c_1$-এর file অনেক বেশি প্রাসঙ্গিক। আসল embedding-এ হাজারের উপর dimension থাকে, কিন্তু হিসাব একই।

### ৬.৩ Element ও Edit-location Localization
$$
\mathcal{E} = \text{LLM}_{\text{greedy}}\left( P,\; \text{Skel}(F) \right)
$$
$$
E_j = \text{LLM}_{T}\left( P,\; \text{Code}(\mathcal{E}) \right), \qquad j = 1, 2, 3, 4
$$

**সূত্রের মানে (কথায়):** প্রথম সূত্র: সন্দেহজনক file-গুলোর শুধু ছোট রূপ (skeleton) দেখে AI বলে কোন function বা class দেখতে হবে। দ্বিতীয় সূত্র: সেই function-গুলোর পুরো code দেখে AI ৪ বার আলাদা করে ঠিক করে কোথায় বদলাতে হবে।

- $\text{Skel}(F)$ = $F$-এর সব file-এর skeleton (এক prompt-এ)।
- $\text{Code}(\mathcal{E})$ = element-গুলোর পুরো code।
- $E_j$ = $j$-তম sampled edit location set (paper: "four samples of edit locations")।

### ৬.৪ Repair Context Window
Location line $a$ থেকে $b$ হলে:
$$
W(a, b) = [\, a - x,\; b + x \,], \qquad x = 10
$$

**সূত্রের মানে (কথায়):** Bug-এর line-এর দুই পাশে কয়েকটা করে বাড়তি line যোগ করে AI-কে দেখানো হয়, যাতে আশপাশের context-ও থাকে। এখানে সেটা ১০ line করে।

**Worked example (paper-এর নিজের উদাহরণ ব্যবহার করে):** Paper বলে একটা class line 40 থেকে 78। $x = 10$ হলে window = $[30, 88]$, অর্থাৎ $88 - 30 + 1 = 59$ line code LLM দেখবে (মূল 39 line + দুই পাশে 10 করে)।

### ৬.৫ Temperature Sampling
Model প্রতিটা সম্ভাব্য token $v$-এর জন্য একটা score (logit) $z_v$ দেয়। Temperature $T$ সহ probability:
$$
p_T(v) = \frac{\exp(z_v / T)}{\sum_{u \in V} \exp(z_u / T)}
$$

**সূত্রের মানে (কথায়):** সূত্রটা প্রতিটা সম্ভাব্য শব্দের জন্য একটা সম্ভাবনা বের করে। T ছোট হলে প্রায় সবসময় সবচেয়ে সম্ভাব্য শব্দটাই আসে। T বড় হলে অন্য শব্দও আসার সুযোগ পায়। তাই T = 0.8 দিয়ে একই issue-র জন্য নানা রকম fix বানানো যায়।

- $T \to 0$ হলে → greedy (সবচেয়ে বড় logit-এর probability → 1)।
- $T = 1$ → model-এর আসল distribution।
- $T = 0.8$ (Agentless) → একটু "তীক্ষ্ণ" distribution, তবে বৈচিত্র্য থাকে।

**Worked example (খেলনা logit, আমার বানানো):** তিনটা token-এর logit $z = (2.0,\; 1.0,\; 0.5)$।

| T | $\exp(z/T)$ | Probability |
|---|---|---|
| 1.0 | 7.389, 2.718, 1.649 (যোগফল 11.756) | 0.629, 0.231, 0.140 |
| 0.8 | 12.182, 3.490, 1.868 (যোগফল 17.540) | 0.695, 0.199, 0.107 |
| → 0 | — | 1, 0, 0 (greedy) |

অর্থাৎ $T = 0.8$-এ বেশিরভাগ সময় সেরা token আসে, কিন্তু প্রায় 30% সময় অন্য token — এতেই ভিন্ন ভিন্ন patch তৈরি হয়।

### ৬.৬ Candidate Patch Set
$$
\mathcal{P} = \{\, p_{j,k} \;:\; j = 1, \ldots, 4;\; k = 1, \ldots, 10 \,\}, \qquad p_{j,1} = \text{greedy},\;\; p_{j,2..10} \sim \text{LLM}_{T=0.8}
$$
$$
\text{মোট patch} = 4 \times 10 = 40
$$

**সূত্রের মানে (কথায়):** ৪০টা patch মানে ৪টা জায়গা × ১০টা করে চেষ্টা। প্রতি জায়গায় ১টা greedy আর ৯টা random চেষ্টা, যাতে বৈচিত্র্য থাকে।

### ৬.৭ Reproduction Test নির্বাচন
Candidate test $r_1, \ldots, r_{40}$ (1 greedy + 39 sampled)। $\text{out}(r, X)$ = codebase $X$-এ test $r$ চালালে কী print করে।
$$
\mathcal{R}' = \{\, r_i \;:\; \text{out}(r_i, C) = \text{"Issue reproduced"} \,\}
$$
$$
r^{*} = \arg\max_{r \in \mathcal{R}'} \; \sum_{r' \in \mathcal{R}'} \mathbb{1}\left[ \nu_t(r') = \nu_t(r) \right]
$$

**সূত্রের মানে (কথায়):** প্রথম সূত্র শুধু সেই test-গুলো রাখে যেগুলো bug-সহ code-এ "Issue reproduced" বলে। দ্বিতীয় সূত্র সেগুলোর মধ্যে সবচেয়ে বেশিবার আসা (comment ও ফাঁকা অংশ বাদ দিয়ে মিলিয়ে) test-টা বাছে।

- $\nu_t$ = test normalization (comment, extra space মুছা, test নাম standardize)।
- $\mathbb{1}[\cdot]$ = indicator — শর্ত সত্য হলে 1, না হলে 0।
- অর্থাৎ: যে normalized test সবচেয়ে বেশিবার এসেছে সেটাই $r^{*}$। $\mathcal{R}'$ খালি হলে reproduction test নেই।

### ৬.৮ Regression Test Set
$$
\mathcal{T}_{\text{pass}} = \{\, t \;:\; s(t, C) = \text{PASS} \,\}, \qquad \mathcal{T}_{\text{reg}} = \mathcal{T}_{\text{pass}} - \mathcal{T}_{\text{LLM-excluded}}
$$

**সূত্রের মানে (কথায়):** মূল code-এ যে test-গুলো পাস করে, সেখান থেকে AI-র বলা "এই fix-এ বদলাতেই পারে" test-গুলো বাদ দিলে আমাদের regression test set পাওয়া যায়।

- $s(t, X)$ = codebase $X$-এ test $t$-এর status (Paper 01-এর notation)।
- $\mathcal{T}_{\text{LLM-excluded}}$ = যেগুলো LLM বলেছে fix-এর কারণে বদলাতে পারে।
- পার্থক্য লক্ষ করো: SWE-bench-এর P2P (Paper 01, Section ৬.২) gold patch $\delta$ দেখে বানানো; Agentless-এর $\mathcal{T}_{\text{reg}}$ বানানো হয় $\delta$ না দেখে — এটাই বাস্তবসম্মত।

### ৬.৯ Patch Selection Rule (সবচেয়ে গুরুত্বপূর্ণ)
প্রতিটা patch $p$-এর regression failure সংখ্যা:
$$
f(p) = \sum_{t \in \mathcal{T}_{\text{reg}}} \mathbb{1}\left[ s(t,\, C \oplus p) \neq \text{PASS} \right]
$$
**ধাপ ১ — regression filter:**
$$
\mathcal{P}_1 = \{\, p \in \mathcal{P} \;:\; f(p) = \min_{q \in \mathcal{P}} f(q) \,\}
$$
**ধাপ ২ — reproduction filter (fallback সহ):**
$$
\mathcal{P}_2 =
\begin{cases}
\{\, p \in \mathcal{P}_1 \;:\; \text{out}(r^{*},\, C \oplus p) = \text{"Issue resolved"} \,\}, & \text{যদি এই set খালি না হয়} \\
\mathcal{P}_1, & \text{অন্যথায় (fallback)}
\end{cases}
$$
**ধাপ ৩ — normalized majority voting:**
$$
\hat{\delta} = \arg\max_{p \in \mathcal{P}_2} \; \sum_{q \in \mathcal{P}_2} \mathbb{1}\left[ \nu(q) = \nu(p) \right]
$$
$$
\nu(p) = \text{diff}\left( \text{unparse}(\text{parse}(C)),\; \text{unparse}(\text{parse}(C \oplus p)) \right) \quad \text{(docstring বাদ)}
$$

**সূত্রের মানে (কথায়):** প্রথমে গোনা হয় প্রতিটা patch কয়টা পুরনো test ভেঙেছে। দ্বিতীয় ধাপে যাদের ভাঙা সবচেয়ে কম তারা থাকে। তৃতীয় ধাপে তাদের মধ্যে যারা bug-test পাস করে তারা থাকে (কেউ না পারলে আগের দলই থাকে)। চতুর্থ ধাপে যে patch সবচেয়ে বেশিবার এসেছে সেটাই চূড়ান্ত।

| Symbol | মানে |
|---|---|
| $C \oplus p$ | Codebase-এ patch $p$ apply করা |
| $f(p)$ | Patch $p$ কতগুলো regression test ভেঙেছে |
| $\mathcal{P}_1$ | সবচেয়ে কম regression failure-এর patch-গুলো |
| $\mathcal{P}_2$ | যেগুলো reproduction test-ও pass করে (বা fallback) |
| $\nu(p)$ | AST-normalized patch (Python `ast` দিয়ে parse/unparse) |
| $\hat{\delta}$ | Final submitted patch |

**নোট:** Majority voting-এ tie হলে কোনটা নেওয়া হয়, এবং $r^{*}$ না থাকলে (reproduction test তৈরিই না হলে) ধাপ ২ কীভাবে চলে — এটা paper-এ স্পষ্ট নয়; যুক্তিসঙ্গত ধারণা হলো তখন সরাসরি fallback হয়। Implementation-এ যাচাই করতে হবে।

**সহজ কথায়:** এই ধাপে একটা fix-ও বাছাইয়ের জন্য যথেষ্ট নয়। আগে পুরনো কিছু ভাঙে কিনা দেখা হয়, তারপর নতুন test, তারপর ভোট। কেউ ভুল test-এর জন্য একা জিততে পারে না।

**Worked example (প্রক্রিয়া বোঝানোর জন্য — সংখ্যাগুলো কাল্পনিক, শুধু 40 সংখ্যাটা paper-এর):**
1. 40টা patch। Regression চালিয়ে দেখা গেল: 25টার $f(p) = 0$, বাকিগুলোর $f(p) \geq 1$ → $\mathcal{P}_1$ = 25টা।
2. $r^{*}$ চালিয়ে 25টার মধ্যে 12টা "Issue resolved" দিল → $\mathcal{P}_2$ = 12টা।
3. Normalize করার পর 12টা patch আসলে 3টা ভিন্ন রূপ: A (7বার), B (3বার), C (2বার) → $\hat{\delta}$ = A।
4. যদি 25টার কোনোটাই reproduction pass না করতো → $\mathcal{P}_2 = \mathcal{P}_1$ (25টা) থেকে voting।

### ৬.১০ Resolve Rate
Paper 01-এর $\text{Resolved}(\hat{\delta})$ সংজ্ঞা (F2P ও P2P সব pass) অপরিবর্তিত:
$$
\%\,\text{Resolved} = \frac{1}{N} \sum_{i=1}^{N} \text{Resolved}(\hat{\delta}_i) \times 100
$$

**সূত্রের মানে (কথায়):** মোট problem-এর মধ্যে কয়টা সম্পূর্ণ ঠিক হয়েছে, তার শতকরা হার। যেমন 300-এর 96 মানে ১০০-তে ৩২।

**Worked example:**
- SWE-bench Lite: $N = 300$, resolved = 96 → $96 / 300 = 32.00\%$
- SWE-bench Lite-S: $N = 249$, resolved = 84 → $84 / 249 \approx 33.73\%$
- SWE-bench Verified: $N = 500$, resolved = 194 → $194 / 500 = 38.80\%$
- **আমার derived observation:** Lite থেকে বাদ পড়া 51টা problem-এর মধ্যে Agentless solve করেছিল $96 - 84 = 12$টা → বাদ পড়া set-এ solve rate $12 / 51 \approx 23.5\%$, যা Lite-S-এর 33.73%-এর চেয়ে কম। অর্থাৎ বাদ পড়া problem-গুলো গড়ে Agentless-এর জন্য **কঠিন** ছিল (insufficient-info problem এর বড় অংশ — Section ৮.৯)।

### ৬.১১ Cost Metric
$$
\bar{\text{Cost}} = \frac{1}{N} \sum_{i=1}^{N} \text{Cost}_i, \qquad \text{Cost}_i = \sum_{\text{call}} \left( n_{\text{in}} \cdot c_{\text{in}} + n_{\text{out}} \cdot c_{\text{out}} \right)
$$

**সূত্রের মানে (কথায়):** প্রতি call-এ কত লেখা পাঠানো হলো ও কত ফেরত এলো, তার দাম যোগ করলে একটা issue-র খরচ। তারপর সব issue-র গড় নিলে গড় খরচ।

- $n_{\text{in}}, n_{\text{out}}$ = input ও output token সংখ্যা; $c_{\text{in}}, c_{\text{out}}$ = প্রতি token-এর API দাম।
- Paper শুধু $\bar{\text{Cost}}$ report করে (USD 0.70); per-token দাম লেখা নেই।

**Cost per resolved issue (আমার derived metric — paper-এ নেই):**
$$
\text{CPR} = \frac{\bar{\text{Cost}} \times N}{\text{resolved}}
$$
Agentless: $0.70 \times 300 / 96 = 2.1875$ → প্রতি সফল fix-এ প্রায় **USD 2.19**। পুরো Lite-এ মোট খরচ $0.70 \times 300 = 210$ USD। (অন্য tool-এর তুলনা Section ৮.২-এ।)

**সহজ কথায় (CPR):** প্রতি সফল fix-এ গড়ে কত টাকা যায়। সব খরচ যোগ করে সফল সংখ্যা দিয়ে ভাগ করলেই হয়।

**Cost decomposition (আমার reconstruction — Table 2, 3, 4-এর default row যোগ করে):**

| Stage | Default setting | Avg. Cost (USD) | উৎস |
|---|---|---|---|
| File localization | Combined (prompting 0.02 + embedding 0.04) | 0.06 | Table 2 |
| Element localization | Skeleton format | 0.02 | Table 2 |
| Edit location | Multi-samples (4) | 0.07 | Table 2 |
| Repair | Multi-samples (4 × 10) | 0.29 | Table 3 |
| Regression test selection | +Regression test | 0.01 | Table 4 |
| Reproduction test | +Reproduction test | 0.25 | Table 4 |
| **মোট** | | **0.70** | Table 1-এর সাথে হুবহু মেলে |

**Insight:** খরচের প্রায় $0.29 / 0.70 \approx 41\%$ repair-এ আর $0.25 / 0.70 \approx 36\%$ reproduction test-এ যায়; পুরো localization মাত্র $0.15 / 0.70 \approx 21\%$। (Table 4-এর cost "additional" ধরে নিলে এই যোগফল মেলে — paper নিজেও Table 4-কে "additional cost" বলেছে।)

### ৬.১২ Localization Accuracy Metrics
Paper দুই ধরনের localization metric ব্যবহার করে — **দুটো আলাদা জিনিস মাপে, গুলিয়ে ফেলো না।**

**(ক) Contains GT (Table 2 — localization step-এর output-এ):**
$$
\text{ContainsGT}_{\text{step}} = \frac{1}{N} \sum_{i=1}^{N} \mathbb{1}\left[ G_i \subseteq L_i^{\text{step}} \right] \times 100
$$

**সূত্রের মানে (কথায়):** Localization-এর ফল সত্যিকারের (gold) জায়গাকে ধরে রেখেছে কিনা, তা সব problem-এর উপর গুনে শতকরা হার।

- $G_i$ = gold patch যে location গুলো edit করেছে; $L_i^{\text{step}}$ = ঐ localization step যে location set দিয়েছে।
- **LoC** = location set-এর গড় line সংখ্যা (কত context যাচ্ছে)।

**(খ) % Correct Location (Table 1 — final submitted patch-এর উপর):** granularity $g \in \{\text{line}, \text{function}, \text{file}\}$:
$$
\text{CorrLoc}_g = \frac{1}{N} \sum_{i=1}^{N} \mathbb{1}\left[ G_i^{g} \subseteq \text{Edit}^{g}(\hat{\delta}_i) \right] \times 100
$$

**সূত্রের মানে (কথায়):** চূড়ান্ত patch আসল সমাধানের সব জায়গা ছুঁয়েছে কিনা, তা শতকরা হারে।

- Patch যদি gold patch-এর **সব** location-এর superset edit করে, তবেই "correct location"।
- Paper নিজেই বলে এটা **approximate** — অন্য জায়গায় edit করেও bug ঠিক করা সম্ভব।

**Worked example:**
- Table 2: file-level Combined = 81.67% → $0.8167 \times 300 = 245$টা problem-এ gold file top-3-এর মধ্যে আছে।
- Table 1: Agentless file-level CorrLoc = 69.7% → $0.697 \times 300 \approx 209$টা submitted patch সঠিক file(s) edit করেছে।
- পার্থক্য কেন: (ক) মাপে "candidate set-এ আছে কিনা", (খ) মাপে "final patch সত্যিই সেখানে edit করেছে কিনা" — পরেরটা স্বাভাবিকভাবেই কম।

### ৬.১৩ Upper Bound ও Selection Efficiency
Figure 6: 40টা patch-এর **যেকোনো একটা** সঠিক হলেই যদি গণনা করা হয় (oracle selection, অনেকটা pass@40-এর মতো):
$$
\text{UpperBound} = \frac{1}{N} \sum_{i=1}^{N} \max_{p \in \mathcal{P}_i} \text{Resolved}(p) = \frac{126}{300} = 42.0\%
$$

**সূত্রের মানে (কথায়):** ৪০টার যেকোনো একটা ঠিক হলেই গোনা হলে কতগুলো issue পাওয়া যেত (126), সেটাই সম্ভাব্য সর্বোচ্চ সীমা (upper bound)।

**Selection efficiency (আমার derived metric):**
$$
\eta = \frac{\text{Resolved by selection}}{\text{UpperBound count}} = \frac{96}{126} \approx 76.2\%
$$

**সূত্রের মানে (কথায়):** Selection efficiency মানে: যেখানে সঠিক patch ছিল, তার কত ভাগে সেটা বাছতে পেরেছে। এখানে 96 ÷ 126 ≈ 76%।

অর্থাৎ যেসব issue-তে অন্তত একটা সঠিক patch তৈরি হয়েছিল, তার প্রায় এক-চতুর্থাংশে (30টা issue) selection ভুল patch বেছেছে। **এটাই patch validation research-এর সুযোগ** (Section ১৩)।

### ৬.১৪ Reproduction Test Quality Funnel
$$
300 \;\to\; 213 \;(\text{"Issue reproduced" দেয়}) \;\to\; 94 \;(\text{gold patch-এর পরে "Issue resolved" দেয়})
$$

**সহজ কথায়:** 300-টা issue থেকে 213-টায় test বানানো গেল। কিন্তু সেই test-গুলোর মধ্যে মাত্র 94-টা সঠিক patch পাওয়ার পর সত্যিই "resolved" বলল। অর্থাৎ বেশিরভাগ বানানো test নিখুঁত নয়।

- Selected rate = $213 / 300 = 71.0\%$
- Plausible rate (সব problem-এর উপর) = $94 / 300 \approx 31.3\%$
- Precision of selected tests = $94 / 213 \approx 44.1\%$ (**আমার derived**) — অর্থাৎ selected test-এর অর্ধেকের বেশি gold patch-কেও "resolved" বলে না।
- তবুও reproduction filter যোগ করায় resolved 81 → 96 (+15)। কারণ: regression-first conservative design + fallback।

**সহজ কথায়:** এই funnel-এ প্রতিটা ধাপে সংখ্যা কমে: 300 থেকে 213, তারপর 94। প্রতিটা ধাপে কিছু test বাদ পড়ে।

### ৬.১৫ Benchmark Quality-র হিসাব
Figure 8-এর % গুলো 300-এর উপর:
$$
\text{Exact patch} = 4.3\% \approx 13, \quad \text{Misleading} = 5.0\% = 15, \quad \text{Not enough info} = 10.0\% = 30
$$
$$
13 + 15 + 30 = 58, \qquad 300 - 249 = 51 \;\Rightarrow\; \text{কমপক্ষে } 58 - 51 = 7 \text{টা problem একাধিক category-তে}
$$

**সূত্রের মানে (কথায়):** তিন ধরনের সমস্যাযুক্ত problem যোগ করলে 58 হয়। কিন্তু আসলে বাদ গেছে 51টা। তাই কিছু problem নিশ্চয়ই একসাথে একাধিক সমস্যায় পড়েছে।

(**আমার inference** — ধরে নিচ্ছি শুধু এই তিন category-ই বাদের কারণ; paper overlap সংখ্যা সরাসরি বলেনি।)

### ৬.১৬ সম্পর্কিত সূত্র: SBFL — Ochiai (তুলনার জন্য, paper ব্যবহার করেনি)
Paper-এর related work-এ SBFL উল্লেখ আছে। Statement $s$-এর suspiciousness:
$$
\text{Ochiai}(s) = \frac{e_f(s)}{\sqrt{F \cdot \left( e_f(s) + e_p(s) \right)}}
$$

**সূত্রের মানে (কথায়):** যে line বেশি fail-করা test-এ চলে এবং কম pass-করা test-এ চলে, তার সন্দেহের স্কোর বেশি।

- $e_f(s)$ = কতগুলো failing test $s$ execute করে; $e_p(s)$ = কতগুলো passing test; $F$ = মোট failing test।
- **কেন Agentless এটা ব্যবহার করতে পারে না:** শুরুতে কোনো failing (bug-triggering) test নেই, তাই $F = 0$। (তবে আমার মতে generated reproduction test দিয়ে $F > 0$ বানানো যায় → future idea, Section ১৪।)

---

**সহজ কথায়:** মাপার জন্য এই সংখ্যাগুলো বুঝলেই চলে: 300টা problem, GPT-4o, প্রতি issue-তে 40টা fix ও 40টা test, আর ফল তুলনা করা হয়েছে প্রায় ২৬টা agent-এর সাথে।

## ৭. Experimental Setup

| বিষয় | বিবরণ |
|---|---|
| **Main dataset** | SWE-bench Lite — 300 problem |
| **Extra datasets** | SWE-bench Lite-S (249, নিজেদের বানানো), SWE-bench Verified (500, OpenAI) |
| **LLM** | GPT-4o (`gpt-4o-2024-05-13`) |
| **Default decoding** | Greedy; sampling-এর সময় temperature **0.8** |
| **Embedding** | LlamaIndex + OpenAI `text-embedding-3-small`; chunk size 512, chunk overlap 0 |
| **File localization** | Top **3** file, greedy |
| **Element localization** | Unrestricted সংখ্যক class/function, greedy |
| **Edit location** | **4** sample → 4টা location set |
| **Repair context** | ±**10** line প্রতিটা edit location-এর চারপাশে |
| **Patches** | প্রতি location set-এ 10 (1 greedy + 9 sampled) → মোট **40/issue** |
| **Patch format** | Search/Replace (Aider থেকে) |
| **Normalization** | Python built-in `ast` library |
| **Reproduction tests** | **40/issue** (1 greedy + 39 sampled) |
| **Regression tests** | সব passing test − LLM-চিহ্নিত non-regression test (SWE-bench-এর P2P ব্যবহার করা হয়নি) |
| **Evaluation harness** | Official SWE-bench setup, modify করা যাতে arbitrary test চালানো যায় |
| **Baselines** | **26টা agent-based approach** (open-source + closed-source/commercial) + SWE-bench-এর **RAG** baseline (BM25 দিয়ে file retrieve করে সরাসরি patch) |
| **Baseline-এর সংখ্যা কোথা থেকে** | Official leaderboard বা tool-এর নিজস্ব paper/repository থেকে নেওয়া (নিজেরা চালায়নি) |
| **Metrics** | % Resolved, Avg. Cost (USD), Avg. # Tokens, % Correct Location (line/function/file) |

---

## ৮. Results — মূল ফলাফল

### ৮.১ Main Results on SWE-bench Lite (Table 1)
Paper-এর Table 1-এর row order অনুযায়ী। Paper closed-source tool-কে একটা তালা (lock) চিহ্ন দিয়ে চিহ্নিত করেছে; PDF-এর Table 1 (পৃষ্ঠা 10) দেখে নিশ্চিত হওয়া গেছে যে উপরের block-এর সব tool (CodeStory Aide থেকে RepoUnderstander পর্যন্ত, SpecRover, CodeR, MASAI সহ) closed-source, আর নিচের block (AutoCodeRover-v2 থেকে শুরু) open-source। "-" = তথ্য প্রকাশিত হয়নি।

**Block A — commercial/closed-source (paper-এর marker অনুযায়ী):**

| Tool | LLM | % Resolved | Avg. Cost (USD) | Avg. Tokens | Line | Function | File |
|---|---|---|---|---|---|---|---|
| CodeStory Aide | GPT-4o + Claude 3.5 S | **129 (43.00%)** | - | - | 41.7% | 58.7% | 72.0% |
| Bytedance MarsCode | NA | 118 (39.33%) | - | - | 42.7% | 58.0% | 79.7% |
| Honeycomb | NA | 115 (38.33%) | - | - | 44.3% | 57.0% | 69.3% |
| MentatBot | GPT-4o | 114 (38.00%) | - | - | 37.3% | 53.3% | 69.3% |
| Gru | NA | 107 (35.67%) | - | - | 38.3% | 54.3% | 75.0% |
| Isoform (Agentless-এর পুরনো version-এর উপর বানানো) | NA | 105 (35.00%) | - | 41,963 | 38.7% | 55.3% | 72.0% |
| SuperCoder2.0 | NA | 102 (34.00%) | - | - | 41.7% | 63.7% | 65.7% |
| Alibaba Lingma Agent | GPT-4o + Claude 3.5 S | 99 (33.00%) | - | - | 40.0% | 58.7% | 75.0% |
| Factory Code Droid | NA | 94 (31.33%) | - | - | 36.7% | 55.7% | 72.7% |
| Amazon Q Developer-v2 | NA | 89 (29.67%) | - | - | 40.3% | 52.0% | 74.3% |
| SpecRover | GPT-4o + Claude 3.5 S | 93 (31.00%) | 0.65 | - | - | - | - |
| CodeR | GPT-4 | 85 (28.33%) | 3.34 | 323,802 | 35.7% | 52.3% | 67.0% |
| MASAI | NA | 84 (28.00%) | - | - | 38.7% | 56.3% | 75.0% |
| SIMA | GPT-4o | 83 (27.67%) | 0.82 | - | 37.0% | 54.0% | 79.0% |
| IBM Research Agent-101 | NA | 80 (26.67%) | - | - | 39.7% | 56.7% | 73.3% |
| OpenCSG StarShip | GPT-4 | 71 (23.67%) | - | - | 39.0% | 61.7% | **90.7%** |
| Amazon Q Developer | NA | 61 (20.33%) | - | - | 34.0% | 43.7% | 71.7% |
| RepoUnderstander | GPT-4 | 64 (21.33%) | - | - | - | - | - |

**Block B — open-source + Agentless:**

| Tool | LLM | % Resolved | Avg. Cost (USD) | Avg. Tokens | Line | Function | File |
|---|---|---|---|---|---|---|---|
| AutoCodeRover-v2 | GPT-4o | 92 (30.67%) | - | - | 35.0% | 52.3% | 69.3% |
| RepoGraph (Agentless-এর পুরনো version-এর উপর) | GPT-4o | 89 (29.67%) | - | - | 36.7% | 51.3% | 71.0% |
| Moatless | Claude 3.5 S | 80 (26.67%) | 0.17 | - | 38.7% | 54.7% | 78.7% |
| Moatless | GPT-4o | 74 (24.67%) | 0.14 | - | 36.0% | 52.0% | 73.0% |
| OpenDevin + CodeAct v1.8 | Claude 3.5 S | 80 (26.67%) | 1.14 | - | 38.0% | 49.7% | 67.3% |
| Aider | GPT-4o + Claude 3.5 S | 79 (26.33%) | - | - | 35.3% | 50.0% | 69.7% |
| **SWE-agent** (Paper 02) | Claude 3.5 S | 69 (23.00%) | 1.62 | 521,208 | 40.7% | 54.3% | 72.0% |
| **SWE-agent** | GPT-4o | 55 (18.33%) | 2.53 | 498,346 | 29.3% | 42.3% | 58.3% |
| **SWE-agent** | GPT-4 | 54 (18.00%) | 2.51 | 245,008 | 30.7% | 45.3% | 61.0% |
| AppMap Navie | GPT-4o | 65 (21.67%) | - | - | 29.7% | 44.7% | 59.7% |
| **AutoCodeRover** (Paper 03) | GPT-4 | 57 (19.00%) | 0.45 | 38,663 | 29.0% | 42.3% | 62.3% |
| RAG (SWE-bench baseline) | Claude 3 Opus | 13 (4.33%) | 0.25 | - | 22.0% | 30.0% | 57.0% |
| RAG | GPT-4 | 8 (2.67%) | 0.13 | - | 12.7% | 23.3% | 47.3% |
| RAG | Claude-2 | 9 (3.00%) | - | - | 16.7% | 24.3% | 46.7% |
| RAG | GPT-3.5 | 1 (0.33%) | - | - | 6.3% | 11.3% | 27.3% |
| **AGENTLESS** | **GPT-4o** | **96 (32.00%)** | **0.70** | **78,166** | **35.3%** | **52.0%** | **69.7%** |

**সহজ কথায়:** Table 1-এ উপরে বন্ধ-source (commercial) tool, নিচে open-source। Agentless open-source-দের মধ্যে সবার উপরে (96টা)। কিছু commercial tool আরও বেশি করেছে (সর্বোচ্চ 129), কিন্তু তাদের code দেখা যায় না, তাই যাচাই করা যায় না। "-" মানে তথ্য প্রকাশ করা হয়নি।

**Authors-এর মূল দাবি:**
- Agentless সব open-source approach-এর মধ্যে সর্বোচ্চ: **96/300 = 32.00%**। পরের open-source AutoCodeRover-v2 = 92।
- সামগ্রিকভাবে সর্বোচ্চ নয় — CodeStory Aide 43.00% সহ কয়েকটা commercial tool উপরে, কিন্তু তাদের source code বা trajectory প্রকাশিত নয়, তাই যাচাই করা যায় না।
- RAG baseline-এর চেয়ে খরচ একটু বেশি, কিন্তু অনেক বেশি issue fix করে।

### ৮.২ Cost ও Token তুলনা (Table 1 + আমার derived cost per resolved)

| Tool (LLM) | Resolved | Avg. Cost (USD) | Avg. Tokens | Cost per resolved (USD, আমার হিসাব) |
|---|---|---|---|---|
| **Agentless (GPT-4o)** | 96 | 0.70 | 78,166 | 2.19 |
| SWE-agent (GPT-4o) | 55 | 2.53 | 498,346 | 13.80 |
| SWE-agent (Claude 3.5 S) | 69 | 1.62 | 521,208 | 7.04 |
| SWE-agent (GPT-4) | 54 | 2.51 | 245,008 | 13.94 |
| AutoCodeRover (GPT-4) | 57 | 0.45 | 38,663 | 2.37 |
| CodeR (GPT-4) | 85 | 3.34 | 323,802 | 11.79 |
| OpenDevin + CodeAct (Claude 3.5 S) | 80 | 1.14 | - | 4.28 |
| SIMA (GPT-4o) | 83 | 0.82 | - | 2.96 |
| SpecRover (GPT-4o + Claude 3.5 S) | 93 | 0.65 | - | 2.10 |
| Moatless (Claude 3.5 S) | 80 | 0.17 | - | 0.64 |
| Moatless (GPT-4o) | 74 | 0.14 | - | 0.57 |
| RAG (GPT-4) | 8 | 0.13 | - | 4.88 |

**সহজ কথায়:** একই GPT-4o ব্যবহার করলে Agentless SWE-agent-এর চেয়ে প্রায় ৩.৬ গুণ সস্তা, প্রায় ৬.৪ গুণ কম token খরচ করে, অথচ প্রায় ১.৭৫ গুণ বেশি issue ঠিক করে। কিন্তু সবচেয়ে সস্তা নয়: Moatless আরও সস্তা।

**পর্যবেক্ষণ:**
- একই LLM (GPT-4o)-তে Agentless বনাম SWE-agent: **$2.53 / 0.70 \approx 3.6$ গুণ সস্তা**, **$498{,}346 / 78{,}166 \approx 6.4$ গুণ কম token**, আর $96 / 55 \approx 1.75$ গুণ বেশি resolve।
- **আমার সৎ নোট:** Agentless সবচেয়ে সস্তা নয় — Moatless প্রতি issue ও প্রতি fix দুই হিসাবেই সস্তা; AutoCodeRover (GPT-4) প্রতি issue-তে সস্তা (0.45) ও কম token ব্যবহার করে। Paper-এর দাবিও সেটাই: "less than most prior agent-based approaches" — "সবার চেয়ে কম" নয়।
- Cost শুধু LLM API-র। Test execution (Docker মানে আলাদা বাক্সে test চালানোর ব্যবস্থা; CPU time মানে processor-এর সময়) এর খরচ কোনো tool-এর ক্ষেত্রেই গণনা হয়নি (Section ১২)।

### ৮.৩ Unique Issues Fixed (Figure 5 — Venn diagram)
- Open-source tool-গুলোর (AutoCodeRover-v2, RepoGraph, Moatless-Claude 3.5, Others) সাথে তুলনায় Agentless **2টা issue** fix করেছে যা অন্য কোনো open-source tool পারেনি।
- শীর্ষ commercial tool-গুলোর (CodeStory Aide, MarsCode, Honeycomb, Others) সাথে তুলনায়ও Agentless **1টা unique fix** দিয়েছে।
- Unique fix কম হওয়ার ব্যাখ্যা (authors): কয়েকটা tool Agentless-এর উপরেই বানানো (Isoform, RepoGraph) বা অনুপ্রাণিত (MarsCode)।

### ৮.৪ Localization Performance (Table 1-এর শেষ ৩ column)
- **Correct location-এর % আর solve rate-এর মধ্যে শক্ত সম্পর্ক** আছে (authors)।
- Agentless: line 35.3%, function 52.0%, file 69.7% — SWE-agent GPT-4o (29.3 / 42.3 / 58.3) ও AutoCodeRover GPT-4 (29.0 / 42.3 / 62.3)-এর চেয়ে প্রতিটা level-এ বেশি।
- সেরা line-level: Honeycomb 44.3%; সেরা function-level: SuperCoder2.0 63.7%; সেরা file-level: OpenCSG StarShip।
- **অস্বাভাবিক case:** OpenCSG StarShip-এর file-level localization খুব বেশি কিন্তু solve rate মাত্র 23.67% — closed-source হওয়ায় কারণ ব্যাখ্যা করা যায় না। **নোট:** paper-এর text-এ এই সংখ্যা 90.0% লেখা, কিন্তু Table 1-এ 90.7% — ছোট inconsistency।

### ৮.৫ Reproduction Test Results (Section 5.1.3)
| ধাপ | সংখ্যা (300-এর মধ্যে) |
|---|---|
| Original repo-তে "Issue reproduced" দেয় এমন test পাওয়া গেছে | **213** |
| Gold patch apply করার পর "Issue resolved" দেয় (সত্যিকারের ভালো test) | **94** |

**সহজ কথায়:** 300-এর মধ্যে 213-টায় bug-test বানানো গেছে। কিন্তু সেগুলোর মধ্যে মাত্র 94-টা সত্যিকারের সঠিক patch-এ "resolved" বলে। কারণ অনেক issue-র description-এ যাচাই করার মতো তথ্যই নেই।

- এই বড় পতনের কারণ (authors): অনেক issue description-এ সমাধান যাচাই করার মতো সম্পূর্ণ তথ্য থাকে না।
- Gold patch এখানে **শুধু test-এর মান মাপতে** ব্যবহার হয়েছে, Agentless-এর selection process-এ নয় (footnote 2)।
- Mitigation: regression-first filter + fallback।

### ৮.৬ Localization Ablation (Table 2)
Bold/default setting = তারকা (*) দিয়ে চিহ্নিত।

| Step | Method | Contains GT | LoC | Avg. Cost (USD) |
|---|---|---|---|---|
| File | Prompting-based | 78.67% | 3,221 | 0.02 |
| File | Embedding-based (w/o irrelevant filtering) | 67.67% | 3,388 | 0.05 |
| File | Embedding-based (w/ irrelevant filtering) | 70.33% | 3,622 | 0.04 |
| File | **Combined*** | **81.67%** | 3,424 | 0.06 |
| Element | Complete file | 53.67% | 778 | 0.15 |
| Element | **Skeleton format*** | **58.33%** | 698 | 0.02 |
| Edit location | Greedy | 50.67% | 189 | 0.06 |
| Edit location | Direct from file-level | 47.00% | 208 | 0.18 |
| Edit location | Multi-samples merged | 56.33% | 342 | 0.07 |
| Edit location | **Multi-samples*** (4টা set আলাদা) | 49.67% / 49.33% / 49.33% / 48.33% | 165 / 180 / 168 / 213 | 0.07 |

**সহজ কথায়:** এই table-এ দেখা যায়, bug খোঁজার ধাপ-ধাপ পদ্ধতি কাজ করে। প্রতি ধাপে code-এর পরিমাণ বহু কমে যায়, তবু সঠিক জায়গা ধরা পড়ার হার ভালোই থাকে। আর file-এর skeleton দেখানো পুরো file দেখানোর চেয়ে সস্তা ও বেশি নির্ভুল।

**Findings:**
1. **Irrelevant folder filtering জরুরি:** filter ছাড়া embedding retrieval-এ accuracy কম (67.67% বনাম 70.33%) আর খরচ বেশি (0.05 বনাম 0.04)।
2. **Prompting ও embedding পরস্পরের পরিপূরক:** আলাদাভাবে 78.67% ও 67.67–70.33%, একসাথে **81.67%**। (Text-এ embedding alone "67.7%" বলা — এটা w/o filtering row-এর সংখ্যা; default with-filtering row 70.33%। ছোট inconsistency।)
3. **Skeleton > Complete file:** skeleton-এ বেশি accuracy (58.33% বনাম 53.67%) আর খরচ সাত ভাগের এক ভাগেরও কম (0.02 বনাম 0.15)। কারণ: long context-এ LLM বিভ্রান্ত হয়।
4. **Context-এর নাটকীয় হ্রাস:** file level-এ ~3,424 line → element level-এ ~698 → edit location-এ ~165–213 line। অর্থাৎ ~3,000+ থেকে <800, তারপর ~200।
5. **Hierarchy দরকারি:** file থেকে সরাসরি edit location-এ গেলে accuracy কম (47.00%) আর খরচ বেশি (0.18)।
6. **Merge বনাম আলাদা রাখা:** merge করলে GT বেশি ধরা পড়ে (56.33%) কিন্তু context বেড়ে যায় (342 line)। Default-এ প্রতিটা sample-এর accuracy প্রায় সমান (~49%) কিন্তু context ছোট — তাই আলাদা আলাদা repair করা হয়।

### ৮.৭ Repair Ablation (Table 3 ও Figure 6)

| Method | Performance | Avg. Cost (USD) |
|---|---|---|
| Greedy location (40 samples) | 88 (29.33%) | 0.22 |
| Multi-samples merged (40 samples) | 85 (28.33%) | 0.24 |
| **Multi-samples (4 × 10 samples)*** | **96 (32.00%)** | 0.29 |

- একটা greedy location set থেকেই 40টা patch নিয়ে 88টা fix — ইতিমধ্যে খুব ভালো।
- 4টা location set আলাদাভাবে ব্যবহার করলে **96** — কারণ ভিন্ন location set ভিন্ন ground-truth location ও ভিন্ন context দেয়।

**সহজ কথায়:** একই জায়গা থেকে 40টা fix নিলেও ভালো ফল আসে (88)। কিন্তু ৪টা আলাদা জায়গার সেট থেকে আলাদা আলাদা fix নিলে আরও ভালো (96)। কারণ ভিন্ন জায়গার সেট ভিন্ন সম্ভাবনা খুলে দেয়।

**Figure 6 (sample সংখ্যা বাড়ালে):**
- X-axis 4-এর ধাপে বাড়ে (4টা location set)। প্রতি set-এ শুধু 1টা greedy (মোট 4টা patch) দিয়েই **80টা fix**।
- Sample বাড়ালে performance বাড়ে, কিন্তু **~40 sample-এ plateau** (মানে আর বাড়ে না, সমতল হয়ে যায়) — কারণ test filtering-এর পর majority voting; পরের sample-গুলো ইতিমধ্যে জেতা patch-কে ছাপিয়ে যেতে পারে না।
- **সব sample বিবেচনা করলে (কোনো একটা সঠিক হলেই) 126টা issue (42.0%)** solve সম্ভব — অর্থাৎ ভালো re-ranking (candidate-গুলোকে নতুন করে সাজিয়ে ভালোটাকে উপরে আনা) দিয়ে উন্নতির বড় সুযোগ।

### ৮.৮ Patch Validation Ablation (Table 4 ও Figure 7)

| Method | Performance | Additional Avg. Cost (USD) |
|---|---|---|
| Majority voting (শুধু) | 77 (25.67%) | 0.00 |
| + Regression test | 81 (27.00%) | 0.01 |
| **+ Reproduction test*** | **96 (32.00%)** | 0.25 |

- Majority voting একাই 77; regression যোগে +4; **reproduction test যোগে +15 — সবচেয়ে বড় উন্নতি**।
- তবে reproduction test-ই সবচেয়ে ব্যয়বহুল অংশ (+0.25)।

**সহজ কথায়:** শুধু ভোটে 77টা। পুরনো test যোগ করলে 81। বানানো bug-test যোগ করলে একলাফে 96। তাই এই test-ই সবচেয়ে বড় সুবিধা দিয়েছে, যদিও এটাই সবচেয়ে দামি অংশ।

**Figure 7 (reproduction test sample সংখ্যা বাড়ালে):**
| Reproduction test samples/issue | Selected tests (300-এর মধ্যে) | Plausible tests | Issues fixed |
|---|---|---|---|
| 1 (greedy) | 100 | (graph-এ; সঠিক সংখ্যা text-এ নেই) | 90 |
| 40 (default) | 213 | 94 | 96 |

- Sample বাড়ালে selected test অনেক বাড়ে, কিন্তু **plausible test খুব বেশি বাড়ে না** (1 থেকে 5-এ যাওয়া ছাড়া) — কারণ issue description-এর অস্পষ্টতা।
- তবুও repair performance 90 → 96।

### ৮.৯ SWE-bench Lite-এর Benchmark Quality Analysis (Figure 8) — আমাদের domain-এর জন্য সবচেয়ে গুরুত্বপূর্ণ

**(a) Description quality:**
| Category | % | আনুমানিক সংখ্যা (300-এর মধ্যে) |
|---|---|---|
| Contains reproducible example | 54.3% | 163 |
| Info in NL (ভাষায় যথেষ্ট তথ্য) | 27.0% | 81 |
| Contains partial reproducible example | 8.7% | 26 |
| **Not enough info** | **10.0%** | **30** |

- 10% problem-এ যথেষ্ট তথ্য নেই। উদাহরণ ধরন: (১) test একটা নির্দিষ্ট নামের নতুন function বা নির্দিষ্ট error message string চায় যা issue-তে নেই — functionality ঠিক হলেও নাম না মিললে fail; (২) issue-তে দুটো সমাধানের প্রস্তাব, test শুধু একটাকে মানে।
- **Footnote 3 (গুরুত্বপূর্ণ):** SWE-bench Lite-এর filtering process-এ এই ধরনের problem সম্পূর্ণ বাদ দেওয়ার দাবি থাকা সত্ত্বেও এগুলো এখনো আছে।

**(b) Solution in description:**
| Category | % | আনুমানিক সংখ্যা |
|---|---|---|
| No solution | 73.3% | 220 |
| Some steps in NL | 7.7% | 23 |
| Complete steps in NL | 9.7% | 29 |
| **Exact patch** (solution leakage) | **4.3%** | **13** |
| **Misleading** | **5.0%** | **15** |

- 4.3% + 9.7% = **14.0%** problem-এ সমাধান হয় হুবহু code-এ নয়তো সম্পূর্ণ ভাষায় দেওয়া — এগুলো অনেক সহজ।
- 5.0% problem-এর প্রস্তাবিত সমাধান developer-এর আসল patch-এর সাথে মেলে না → issue অনুসরণ করলে tool ভুল পথে যায়।

**(c) Location information (stacked bar, প্রতিটা granularity-তে):**
| Granularity | None (কোনো clue নেই) | Stack trace | Natural language | Keywords |
|---|---|---|---|---|
| Line | 90.3% | 3.0% | 6.7% | — |
| Function | 68.0% | 6.7% | 13.7% | 11.7% |
| File | 50.0% | 13.7% | 15.3% | 21.0% |
| Overall | 39.3% | 13.7% | 24.7% | 22.3% |

(**নোট:** "None" সংখ্যাগুলো paper-এর text-এর সাথে মেলে — <10% issue exact line দেয়, ~অর্ধেক issue file দেয়। বাকি segment-গুলো কোন category, তা আমি figure-এর legend order থেকে পড়েছি — supervisor-কে দেখানোর আগে PDF-এর Figure 8c একবার চোখে দেখে নিও।)

**সহজ কথায়:** Lite-এর প্রায় ১০% problem-এ তথ্য কম, প্রায় ১৪% problem-এ উত্তর হুবহু বা সম্পূর্ণ ধাপে দেওয়া, আর ৫% problem ভুল পথ দেখায়। বেশিরভাগ problem-এ bug-এর সঠিক line-এর কোনো ইঙ্গিত নেই।

**Authors-এর উপসংহার:** SWE-bench Lite-এ **অসমাধানযোগ্য প্রশ্ন, বিভ্রান্তিকর সমাধান, ও problem difficulty-তে বড় বৈষম্য** আছে — যা benchmark তৈরির সময় বা আগের approach-গুলোতে বিবেচনা করা হয়নি।

### ৮.১০ SWE-bench Lite-S Results (Table 5)

| Tool | LLM | Lite % Resolved | Lite Rank | Lite-S % Resolved | Lite-S Rank |
|---|---|---|---|---|---|
| CodeStory Aide | GPT-4o + Claude 3.5 S | 129 (43.00%) | 1 | 114 (45.78%) | 1 |
| Bytedance MarsCode | NA | 118 (39.33%) | 2 | 106 (42.57%) | 2 |
| Honeycomb | NA | 115 (38.33%) | 3 | 98 (39.36%) | 3 |
| MentatBot | GPT-4o | 114 (38.00%) | 4 | 96 (38.55%) | 4 |
| Gru | NA | 107 (35.67%) | 5 | 94 (37.75%) | 5 |
| Isoform | NA | 105 (35.00%) | 6 | 91 (36.55%) | 6 |
| SuperCoder2.0 | NA | 102 (34.00%) | 7 | 87 (34.94%) | 7 |
| Alibaba Lingma Agent | GPT-4o + Claude 3.5 S | 99 (33.00%) | 8 | 86 (34.54%) | 8 |
| **AGENTLESS** | **GPT-4o** | **96 (32.00%)** | **9** | **84 (33.73%)** | **9** |
| Factory Code Droid | NA | 94 (31.33%) | 10 | 82 (32.93%) | 10 |
| AutoCodeRover-v2 | GPT-4o | 92 (30.67%) | 11 | 79 (31.73%) | 11 |
| RepoGraph | GPT-4o | 89 (29.67%) | 12* | 77 (30.92%) | 12 |
| Amazon Q Developer-v2 | NA | 89 (29.67%) | 12* | 76 (30.52%) | 13 |
| CodeR | GPT-4 | 85 (28.33%) | 14 | 71 (28.51%) | 14* |
| MASAI | NA | 84 (28.00%) | 15 | 70 (28.11%) | 16 |
| SIMA | GPT-4o | 83 (27.67%) | 16 | 71 (28.51%) | 14* |
| Moatless | Claude 3.5 S | 80 (26.67%) | 17* | 67 (26.91%) | 17 |
| IBM Research Agent-101 | NA | 80 (26.67%) | 17* | 66 (26.51%) | 18* |
| OpenDevin + CodeAct v1.8 | Claude 3.5 S | 80 (26.67%) | 17* | 65 (26.10%) | 20 |
| Aider | GPT-4o + Claude 3.5 S | 79 (26.33%) | 20 | 66 (26.51%) | 18* |
| Moatless | GPT-4o | 74 (24.67%) | 21 | 62 (24.90%) | 21 |
| OpenCSG StarShip | GPT-4 | 71 (23.67%) | 22 | 56 (22.49%) | 23* |
| SWE-agent | Claude 3.5 S | 69 (23.00%) | 23 | 58 (23.29%) | 22 |
| AppMap Navie | GPT-4o | 65 (21.67%) | 24 | 56 (22.49%) | 23* |
| RepoUnderstander | GPT-4 | 64 (21.33%) | 25 | 51 (20.48%) | 25* |
| Amazon Q Developer | NA | 61 (20.33%) | 26 | 51 (20.48%) | 25* |
| AutoCodeRover | GPT-4 | 57 (19.00%) | 27 | 45 (18.07%) | 27* |
| SWE-agent | GPT-4o | 55 (18.33%) | 28 | 45 (18.07%) | 27* |
| SWE-agent | GPT-4 | 54 (18.00%) | 29 | 42 (16.87%) | 29 |
| RAG | Claude 3 Opus | 13 (4.33%) | 30 | 10 (4.02%) | 30 |
| RAG | Claude-2 | 9 (3.00%) | 31 | 6 (2.41%) | 31 |
| RAG | GPT-4 | 8 (2.67%) | 32 | 5 (2.01%) | 32 |
| RAG | GPT-3.5 | 1 (0.33%) | 33 | 0 (0.00%) | 33 |

**সহজ কথায়:** সমস্যাযুক্ত problem বাদ দিলেও tool-দের মোটামুটি একই ক্রম থাকে। শীর্ষ tool-দের score বাড়ে, কারণ বাদ পড়া problem-গুলো কঠিন ছিল। কয়েকটার score কমে, কারণ তারা বাদ পড়া সহজ problem থেকে বেশি নম্বর পাচ্ছিল (আমার অনুমান)।

(* = tie। Table 1-এর SpecRover Table 5-এ নেই।)

**Findings:**
- সামগ্রিক ranking **মোটামুটি একই**, কিন্তু কিছু ছোট পরিবর্তন: যেমন OpenDevin 17* → 20, Amazon Q Developer-v2 12* → 13, SIMA 16 → 14*, Aider 20 → 18*, SWE-agent (Claude 3.5 S) 23 → 22।
- প্রায় সব শীর্ষ tool-এর % Lite-S-এ **বেড়েছে** (যেমন CodeStory 43.00 → 45.78), কারণ বাদ পড়া problem-গুলোর বড় অংশ (insufficient info) কঠিন/অসম্ভব ছিল।
- **আমার observation:** কিছু tool-এর % কমেছে (যেমন SWE-agent GPT-4: 18.00 → 16.87, AutoCodeRover: 19.00 → 18.07, RAG সব model)। এর একটা সম্ভাব্য ব্যাখ্যা — এরা বাদ পড়া "সহজ" (exact patch থাকা) problem-গুলো থেকে তুলনামূলক বেশি score পাচ্ছিল। এটা আমার অনুমান; paper per-category breakdown tool অনুযায়ী দেয়নি।

### ৮.১১ Problem Category অনুযায়ী Solve Rate (Figure 9, Lite-S-এ)
Figure-এ selected tool: AutoCodeRover-v2, RepoGraph, Moatless (Claude 3.5) [open-source]; CodeStory Aide, MarsCode, Honeycomb [closed-source]; Agentless।
1. **Reproducible example থাকলে (Figure 9a):** আশ্চর্যজনকভাবে **আগের সব approach-এর solve rate কমে যায়**। অনেক agent (SWE-agent, OpenDevin, CodeR) আগে error reproduce করার চেষ্টা করে, কিন্তু example থাকলেও তাতে লাভ হয় না। **Agentless-এর solve rate এখানে উঁচুই থাকে** — কারণ এর reproduction test সরাসরি issue description থেকে বানানো, তাই example-টা কাজে লাগায় (MentatBot-ও একই রকম, এরও explicit test generation আছে)।
2. **Solution steps NL-এ থাকলে (Figure 9b):** প্রত্যাশিতভাবেই সব tool ভালো করে।
3. **Location information (Figure 9c):** সবচেয়ে সহজ — location NL-এ দেওয়া, তারপর stack trace; সবচেয়ে কঠিন — কোনো location clue নেই। Location NL/stack trace/keyword-এ থাকলে Agentless closed-source tool-এর সমান; কিন্তু **কোনো clue না থাকলে closed-source agent-রা Agentless-এর চেয়ে ভালো** — কারণ তারা জটিল code search tool ব্যবহার করতে পারে। **এটা agent-এর একটা আসল সুবিধা** (authors নিজেই স্বীকার করেছেন)।

### ৮.১২ SWE-bench Verified (Table 6)

| Tool | LLM | % Resolved (500-এর মধ্যে) |
|---|---|---|
| Tools (Anthropic) | Claude 3.5 Sonnet (20241022) | 245 (49.00%) |
| Tools (Anthropic) | Claude 3.5 Haiku | 203 (40.60%) |
| Solver | NA | 227 (45.40%) |
| Gru | NA | 226 (45.20%) |
| Honeycomb | NA | 203 (40.60%) |
| Amazon Q Developer-v2 | NA | 194 (38.80%) |
| Factory Code Droid | NA | 185 (37.00%) |
| Amazon Q Developer | NA | 128 (25.60%) |
| Composio SWEkit | Claude 3.5 Sonnet | 203 (40.60%) |
| AutoCodeRover-v2 | GPT-4o | 192 (38.40%) |
| SWE-agent | Claude 3.5 Sonnet | 168 (33.60%) |
| SWE-agent | GPT-4o | 116 (23.20%) |
| SWE-agent | GPT-4 | 112 (22.40%) |
| Alibaba Lingma Agent | Lingma SWE-GPT 72b | 144 (28.80%) |
| AppMap Navie | GPT-4o | 131 (26.20%) |
| **AGENTLESS** | **GPT-4o** | **194 (38.80%)** |

**সহজ কথায়:** মানুষ-যাচাই করা আরও পরিষ্কার সেটেও Agentless ভালো ফল করেছে: ১০০টার মধ্যে প্রায় ৩৯টা।

- Verified-এ Agentless **194/500 = 38.80%** — open-source-এর মধ্যে **দ্বিতীয়** (Composio SWEkit 40.60%-এর পরে), অনেক commercial tool-এর চেয়ে ভালো।
- **GPT-4o ব্যবহারকারী সব technique-এর মধ্যে সেরা** (AutoCodeRover-v2 GPT-4o = 38.40%, SWE-agent GPT-4o = 23.20%)।

### ৮.১৩ Adoption (Section 5.1.4)
- RepoGraph (open-source) ও Isoform (commercial) Agentless-এর আগের version-এর উপর বানানো।
- Bytedance MarsCode patch sampling/selection-এ আংশিক অনুপ্রাণিত; OpenDevin এটাকে নিজেদের ecosystem-এ integrate করছিল।
- OpenAI GPT-4o-র SWE-bench Verified showcase-এ এবং পরে o1 model family-র showcase-এ Agentless-কে default approach হিসেবে ব্যবহার করেছে (paper-এর দাবি)।

### ৮.১৪ একটা ছোট কিন্তু গুরুত্বপূর্ণ সংখ্যা (Footnote 1)
SWE-bench-এর PASS_TO_PASS list সরাসরি regression test হিসেবে ব্যবহার করলে Lite-এ score হতো **98** (96-এর বদলে)। অর্থাৎ benchmark-এর "oracle" তথ্য ব্যবহার করলে score কৃত্রিমভাবে বাড়ে — authors সচেতনভাবে তা এড়িয়েছেন। **Assurance-এর দৃষ্টিতে এটা একটা ভালো evaluation practice।**

---

## ৯. Key Findings / Insights (Supervisor-কে বলার মতো ৮টা পয়েন্ট)

1. **সরলতা জিতেছে:** Fixed ৩-phase pipeline দিয়ে GPT-4o-তে 96/300 (32.00%) — সব open-source agent-এর উপরে, SWE-agent (GPT-4o, 55)-এর প্রায় 1.75 গুণ।
2. **কম খরচ, কম token:** গড়ে USD 0.70 ও 78,166 token/issue; একই LLM-এ SWE-agent-এর চেয়ে ~3.6 গুণ সস্তা ও ~6.4 গুণ কম token।
3. **Hierarchical localization কার্যকর:** context ~3,400 → ~700 → ~200 line কমিয়েও accuracy ধরে রাখা; skeleton format পুরো file-এর চেয়ে বেশি accurate ও অনেক সস্তা।
4. **Diversity সাহায্য করে:** ৪টা ভিন্ন location set আলাদাভাবে ব্যবহার করে 88 → 96।
5. **Generated reproduction test সবচেয়ে বড় booster:** +15 fix (81 → 96), যদিও selected test-এর মাত্র 94/213 সত্যিই gold patch যাচাই করতে পারে।
6. **Selection-ই নতুন bottleneck:** 40টা patch-এর মধ্যে সঠিকটা থাকা 126 issue-তে (42.0%), কিন্তু বাছাই করা গেছে 96টায় — **30টা issue-তে সঠিক patch হাতে থেকেও হারিয়েছে**।
7. **Benchmark নিজেই ত্রুটিপূর্ণ:** SWE-bench Lite-এ 4.3% exact patch leak, 9.7% সম্পূর্ণ সমাধানের ধাপ, 5.0% misleading, 10.0% অপর্যাপ্ত তথ্য — তাই Lite-S (249)।
8. **Agent-এর আসল সুবিধা কোথায়:** যখন issue-তে কোনো location clue নেই, তখন search tool-সহ agent-রা ভালো করে — Agentless-এর দুর্বলতা।

---

## ১০. কেন এই Solution অন্যগুলোর থেকে ভালো?

| বৈশিষ্ট্য | RAG baseline (Paper 01) | SWE-agent (Paper 02) | AutoCodeRover (Paper 03) | **Agentless** |
|---|---|---|---|---|
| মূল ধারণা | BM25 file + একবারে patch | Custom ACI-তে LLM নিজে read/edit/bash চালায় | Code search API (যেমন class-এর method খোঁজা) দিয়ে iterative context retrieval | Fixed localize → repair → validate |
| কে সিদ্ধান্ত নেয় | কেউ না (one-shot) | LLM | LLM | মানুষের লেখা pipeline |
| Localization | BM25 (keyword) | Agent-এর search/navigation | Agent + AST-ভিত্তিক search API | LLM prompt + embedding, hierarchical |
| Patch format | Unified diff | Agent-এর edit command | Patch (agent) | Search/Replace |
| Candidate patch সংখ্যা | 1 | সাধারণত 1 trajectory | — | 40 |
| Validation | নেই | Agent নিজে test চালাতে পারে | — | Regression + generated reproduction + voting |
| Lite % Resolved | 2.67% (GPT-4) – 4.33% (Claude 3 Opus) | 18.33% (GPT-4o), 23.00% (Claude 3.5 S) | 19.00% (GPT-4); v2: 30.67% (GPT-4o) | **32.00% (GPT-4o)** |
| Avg. Cost (USD) | 0.13–0.25 | 1.62–2.53 | 0.45 (GPT-4) | 0.70 |
| Interpretability | উচ্চ | কম (30–40 turn) | মাঝারি | **উচ্চ — প্রতিটা phase আলাদা মাপা যায়** |
| Reproducibility | উচ্চ | কম-মাঝারি | মাঝারি | **উচ্চ** |

**সহজ কথায়:** নতুনত্ব হলো Agentless সরল, সস্তা, বোঝা যায় এমন ও আবার চালানো যায়। একই সাথে এর ফলও ভালো। তবে নিচের শর্ত আছে।

(SWE-agent ও AutoCodeRover-এর design বিবরণ এই paper-এর related work থেকে; বিস্তারিত Paper 02 ও 03 দেখো। "—" মানে এই paper-এ সেই তথ্য দেওয়া নেই।)

**মূল শক্তি:**
1. **Simplicity ও interpretability:** কোথায় ভুল হয়েছে সহজে বোঝা যায় — localization? repair? selection?
2. **Cost-efficiency:** অপ্রয়োজনীয় exploration নেই।
3. **Execution-grounded validation:** LLM-এর মতামতের বদলে test-এর আসল output।
4. **Strong, reproducible baseline:** open-source, fixed workflow — পরের গবেষণার "starting point"।
5. **Benchmark-এর প্রতি critical দৃষ্টি:** শুধু score নয়, score-এর বিশ্বাসযোগ্যতাও প্রশ্ন করেছে।

---

## ১১. কোন পরিস্থিতিতে এই Approach ভালো কাজ করে, কোথায় করে না

### ✅ ভালো কাজ করে যখন:
- Issue-তে **location-এর clue** আছে (file নাম, stack trace, keyword)।
- Issue-তে **reproducible example** আছে — reproduction test সহজে বানানো যায়।
- Bug-fix ছোট ও স্থানীয় (কয়েকটা function-এর মধ্যে)।
- Repository-র **existing test suite ভালো** — regression filter শক্তিশালী হয়।
- **Budget সীমিত** এবং process audit/debug করতে হবে।
- Python codebase (AST normalization Python `ast`-ভিত্তিক)।

### ❌ ভালো কাজ করে না / সীমিত যখন:
- Issue-তে **কোনো location clue নেই** — agent-রা search tool দিয়ে ভালো করে (Figure 9c)।
- Issue **অস্পষ্ট/underspecified** — reproduction test ভুল হয় (213 → 94)।
- Fix-এর জন্য **অনেক file জুড়ে বড় পরিবর্তন** লাগে — top-3 file-এর সীমা।
- **Interactive exploration** দরকার (যেমন environment debug, dependency install, runtime state দেখা)।
- নতুন **feature development** বা long-horizon task — pipeline bug-fix-কেন্দ্রিক।
- অন্য language — embedding অংশ চলবে, কিন্তু normalization ও test harness আবার বানাতে হবে।
- Test suite দুর্বল বা অনেক flaky (মানে কখনো pass, কখনো fail করা অস্থির test) — regression filter ভুল signal দেয়।

---

## ১২. Limitations — দুর্বলতা

### ১২.১ Authors যা নিজেরা স্বীকার করেছেন
1. **Data leakage / contamination (internal threat):** GPT-4o-র training data-তে SWE-bench Lite-এর gold patch থাকতে পারে; closed model হওয়ায় যাচাই অসম্ভব। যুক্তি: আগের কাজগুলোও একই ধরনের closed LLM ব্যবহার করেছে, আর SWE-bench authors GPT-4-এর cutoff-এর আগে/পরে পার্থক্য পাননি; পুরোপুরি সমাধানে GPT-4o নতুন করে train করতে হবে — academic project-এ অসম্ভব।
2. **Generalization (external threat):** মূলত SWE-bench Lite-এ evaluate; অন্য dataset-এ নাও মিলতে পারে। (Verified ও OpenAI-এর independent evaluation কিছুটা সমর্থন দেয়।)
3. **No-location-clue problem-এ agent-রা ভালো** — future work।
4. **Generated reproduction test অসম্পূর্ণ/ভুল হতে পারে** (213-এর মধ্যে মাত্র 94 plausible)।
5. **Correct-location metric approximate** — ভিন্ন জায়গায় fix সম্ভব।
6. Technique-গুলো আলাদাভাবে নতুন নয় — combination-ই contribution।

### ১২.২ আমার Critical Analysis (Professor-level observation)
1. **Single-run, কোনো variance নেই:** Pipeline-এ temperature 0.8-এ প্রচুর sampling আছে, অথচ প্রতিটা configuration একবার চালিয়ে একটা সংখ্যা report করা হয়েছে। 96 বনাম 92 (AutoCodeRover-v2) — এই 4টা issue-র পার্থক্য run-to-run noise-এর মধ্যে পড়ে কিনা জানা যায় না। কোনো confidence interval বা repeated trial নেই। **Reliability domain-এর জন্য এটা সবচেয়ে বড় gap।**
2. **Comparison-এর fairness:** Baseline-গুলোর সংখ্যা leaderboard/নিজস্ব report থেকে নেওয়া — ভিন্ন LLM, ভিন্ন সময়, ভিন্ন API দাম। অনেক closed-source tool-এর trajectory নেই। তাই "highest among open-source" দাবি সঠিক হলেও controlled comparison নয়। শুধু SWE-agent-এর সাথে একই LLM (GPT-4o)-তে সরাসরি তুলনা তুলনামূলক পরিষ্কার।
3. **"Agentless" কিন্তু "execution-less" নয়:** প্রতিটা issue-তে সব existing test চালানো, 40টা reproduction test চালানো, 40টা patch-এ regression ও reproduction test চালানো — এর **compute cost ও wall-clock time report করা হয়নি**। USD 0.70 শুধু LLM API খরচ। বড় repository-তে পুরো test suite বারবার চালানো ব্যয়বহুল।
4. **মানুষই planner:** Agent-এর "planning" সমস্যা এড়ানো হয়েছে মানুষের ডিজাইন করা pipeline দিয়ে — যা SWE-bench-ধরনের (Python, issue → patch, test আছে) task-এর জন্য tune করা। অন্য task type-এ এই pipeline আবার design করতে হবে; agent-এর সাধারণীকরণের প্রতিশ্রুতি এখানে নেই।
5. **Hyperparameter sensitivity অজানা:** N = 3 file, x = 10 line, 4টা location sample, 40টা patch — কেন এই মান? Patch ও reproduction test সংখ্যা ছাড়া (Figure 6, 7) N বা x-এর ablation নেই। আর এগুলো SWE-bench Lite-এই tune হলে Lite-এ evaluate করা একধরনের test-set tuning হতে পারে (paper-এ আলাদা dev set-এর উল্লেখ নেই)।
6. **Lite-S-এর manual classification-এর reliability:** কতজন annotator, কীভাবে মতভেদ মেটানো হয়েছে, inter-rater agreement (যেমন Cohen's kappa, মানে দুজন মানুষ কতটা একমত তার মাপ) — কিছুই report করা নেই। Benchmark-এর বিশ্বাসযোগ্যতা নিয়ে কাজ করা paper-এর নিজের label-এর reliability অজানা — এটা একটা irony।
7. **Lite-S test adequacy সমস্যা সমাধান করে না:** Problem description-এর সমস্যা বাদ দেওয়া হয়েছে, কিন্তু **দুর্বল F2P test-এর কারণে plausible-but-wrong patch "resolved" হওয়ার** (Paper 01, Section ১২ critique #1) সমস্যা থেকেই গেছে। Agentless-এর 96টা "resolved"-এর কতগুলো আসলে overfitted, তা যাচাই করা হয়নি।
8. **Majority voting-এর অনুমান:** "সবচেয়ে frequent = সঠিক" — কিন্তু LLM একটা systematic ভুল বারবার করলে ভুল patch-ই জিতবে। আর AST normalization শুধু surface পার্থক্য মুছে; অর্থে এক কিন্তু গঠনে ভিন্ন (যেমন `if not x` বনাম `if x is False`-ধরনের) patch-এর vote ভাগ হয়ে যায়।
9. **Reproduction test-এর oracle problem:** LLM-এর লেখা test-এর assertion LLM-এর নিজের বোঝার উপর নির্ভর — ভুল বুঝলে ভুল patch-কে "resolved" বলবে। 213-এর মধ্যে 119টা (213 − 94, আমার হিসাব) test gold patch-কেও resolved বলেনি — এই test-গুলো সঠিক patch-কে **বাদ** দিয়ে দিতে পারে (false rejection), শুধু fallback তখনই কাজ করে যখন **কোনো** patch pass করে না।
10. **Text–table inconsistency:** StarShip file-level 90.0% (text) বনাম 90.7% (Table 1); embedding alone 67.7% (text) বনাম default 70.33% (Table 2)। ছোট, কিন্তু supervisor ধরতে পারেন।
11. **Security/quality মাপা হয়নি:** Patch নতুন vulnerability বা code smell আনছে কিনা দেখা হয়নি — আমাদের Security sub-domain-এর gap।
12. **Python-নির্ভর normalization** ও SWE-bench-নির্ভর harness modification — অন্য language-এ port করা সহজ নয়।

---

## ১৩. Research Gaps — কোথায় কাজ করার সুযোগ আছে

| # | Gap | কেন গুরুত্বপূর্ণ | আমাদের কোন folder/paper-এ সম্পর্কিত কাজ |
|---|---|---|---|
| G1 | **Patch selection/re-ranking** — 126 সম্ভব, 96 বাছাই (η ≈ 76.2%) | সঠিক patch হাতে থেকেও হারানো; সবচেয়ে সরাসরি উন্নতির সুযোগ | Patch Validation (HITL LLM-as-a-Judge, Code Representation in APCA); LLM Test Generation (Oracle-Guided Program Selection) |
| G2 | **Reproduction test-এর মান** — 213 থেকে মাত্র 94 plausible | ভুল test ভুল patch বাছাই করে বা সঠিক patch বাদ দেয় | LLM Test Generation (CoverUp — এই paper-ও cite করেছে, UniTSyn, TestDecision); Patch Validation (Harden and Catch) |
| G3 | **Overfitted "resolved" patch** — Lite-S description ঠিক করেছে, test adequacy নয় | Score inflated; patch বিশ্বাসযোগ্য নয় | Patch Validation sub-domain; Coding-Agent Evaluation & Reliability (Engineering Reliable Coding Agents) |
| G4 | **Run-to-run reliability / variance** — single run | একই pipeline বারবার চালালে একই result? | Coding-Agent Evaluation & Reliability (Engineering Reliable Coding Agents) |
| G5 | **Benchmark contamination ও quality audit** — GPT-4o leakage অজানা; manual label-এর reliability নেই | Score আসল ability কিনা | Coding-Agent Evaluation & Reliability (SWE-rebench, SWE-Bench Pro / Long-Horizon) |
| G6 | **No-location-clue issue-তে localization** | Agentless-এর স্বীকৃত দুর্বলতা | Automated Program Repair (APR survey — FL অংশ); AutoCodeRover (Paper 03) |
| G7 | **Patch-এর security ও quality** | Test pass করেও vulnerable code | Security of AI-Generated Code (CWEval, Security and Quality in LLM-Generated Code, SecureVibeBench); APR (LLM Vulnerability Repair case study) |
| G8 | **Interpretable/assured pipeline-এর formal guarantee** | কোন ধাপে কতটা বিশ্বাস করা যায় তার মাপ নেই | Trustworthy AI for SE (Trustworthy AI Software Engineers, Proof-Carrying Code Completions, AI Assurance testing strategy) |
| G9 | **Test execution-এর compute cost reporting** | আসল খরচ লুকানো | Coding-Agent Evaluation & Reliability; LLM Test Generation (ExecutionAgent — test চালানোর infrastructure) |
| G10 | **Issue underspecification-এর automatic detection** | 10% problem অসম্ভব; manual classification scalable নয় | — (খোলা; Paper 01-এর G7-এর সাথে একই) |

**সহজ কথায়:** সবচেয়ে পরিষ্কার সুযোগ আছে সঠিক fix বাছাইয়ে (G1)। তারপর test-এর মান (G2), overfitting (G3), আর একই কাজ বারবার চালালে ফল একই আসে কিনা (G4)।

---

## ১৪. কী করলে আরও ভালো হবে — Improvement Ideas

(সবগুলো **আমার নিজের প্রস্তাব** — paper-এ নেই, যদি না উল্লেখ করা থাকে।)

1. **Better re-ranking:** Majority voting-এর বদলে একটা combined score:
   $$\text{Score}(p) = w_1 \cdot \text{vote}(p) + w_2 \cdot \text{repro}(p) - w_3 \cdot f(p) + w_4 \cdot \text{judge}(p)$$
   যেখানে $\text{judge}(p)$ = LLM-as-a-judge বা learned patch-correctness classifier-এর score। লক্ষ্য: 96 → 126-এর দিকে যাওয়া। (Paper নিজেও "better re-ranking" কে future work বলেছে।)
2. **Reproduction test-এর মান বাড়ানো:** একাধিক test রাখা (একটা নয়), test-গুলোর মধ্যে agreement দেখা; mutation testing দিয়ে test-এর শক্তি মাপা; issue-র example code সরাসরি test-এ রূপান্তর।
3. **Generated test দিয়ে SBFL:** Reproduction test fail হলে সেটাকে failing test ধরে Ochiai (Section ৬.১৬) চালিয়ে localization-কে execution-signal দেওয়া — বিশেষ করে no-location-clue issue-তে (G6)।
4. **Semantic patch clustering:** AST normalization-এর পরেও, generated test-এ একই behaviour দেখানো patch-গুলোকে এক cluster ধরে vote (behavioural equivalence) — vote split কমবে।
5. **Repeated-run reliability report:** প্রতিটা configuration k বার চালিয়ে mean ± std ও pass^k (সব k বার সফল) — Paper 01-এর improvement idea #3-এর সাথে মিলিয়ে।
6. **Assurance layer:** Selected patch-এ static security scan (Bandit/Semgrep) ও quality metric যোগ করে "resolved but risky" চিহ্নিত করা।
7. **Abstention:** Selection-এর confidence (যেমন vote share) কম হলে patch submit না করে মানুষকে জানানো — wrong patch-এর খরচ কমাতে।

---

## ১৫. কোন Gap-এ Research করলে ভালো Result ও Publication আসতে পারে

> ⚠️ এটা AI Coding Agents sub-domain-এর ৪টা paper পড়ার পর প্রাথমিক মত। বাকি sub-domain শেষ করে চূড়ান্ত বাছাই।

| Gap | SPL3-তে করা সম্ভব? | Novelty | Publication সম্ভাবনা |
|---|---|---|---|
| **G1: Patch re-ranking/selection** (Agentless-এর candidate patch-এর উপর নতুন selector) | ✅ হ্যাঁ — Agentless-এর output patch (40/issue) দিয়ে offline experiment, নতুন LLM call কম লাগবে | উচ্চ — paper নিজেই upper bound 42% দেখিয়েছে | ⭐⭐⭐⭐⭐ |
| **G2+G3: Reproduction test quality ও overfitting detection** | ✅ হ্যাঁ — ছোট subset (যেমন 50–100 issue) | উচ্চ, Patch Validation ও Test Generation দুই sub-domain-এর সংযোগ | ⭐⭐⭐⭐ |
| **G4: Run-to-run reliability of Agentless** | ✅ হ্যাঁ — সস্তা model দিয়ে কয়েকবার চালানো | মাঝারি-উচ্চ, domain-এর নামের সাথে সরাসরি মেলে | ⭐⭐⭐⭐ |
| **G7: Security-aware patch selection** | ✅ হ্যাঁ — static analyzer + selection | উচ্চ | ⭐⭐⭐⭐ |
| G6: No-clue localization | ⚠️ মাঝারি — বেশি engineering | মাঝারি | ⭐⭐⭐ |
| G5: নতুন contamination-free benchmark | ⚠️ কঠিন | মাঝারি (SWE-rebench আছে) | ⭐⭐ |

**সহজ কথায়:** SPL3-র জন্য সবচেয়ে সহজ ও সম্ভাবনাময় হলো G1: Agentless-এর সংরক্ষিত 40টা patch নিয়ে নতুন বাছাইকারী বানানো। এতে নতুন করে LLM চালাতে প্রায় কিছুই লাগে না।

**সম্ভাব্য venue (general guidance, Paper 01-এর মতো):**
- **Conference:** ICSE, FSE, ASE, ISSTA; workshop (যেমন LLM4Code, ICSE/FSE-এর AI-SE workshop) — student-এর জন্য শুরু করা সহজ।
- **Journal:** ACM TOSEM, IEEE TSE (খুব high), EMSE, JSS, IST।

---

## ১৬. SPL3 Implementation Perspective — Software-এ কীভাবে আনবো

### ১৬.১ কেন Agentless একজন student-এর জন্য সবচেয়ে reproducible baseline (আমার মূল্যায়ন)
1. **Open-source ও fixed workflow:** প্রতিটা phase একটা আলাদা script — agent-এর মতো unpredictable trajectory নেই।
2. **সস্তা:** paper-এর সময়ের দামে GPT-4o-তে গড়ে USD 0.70/issue → পুরো Lite প্রায় USD 210; 50-issue subset প্রায় USD 35 (আমার অনুমান; API দাম সময়ের সাথে বদলায়, নতুন সস্তা model দিয়ে আরও কম)।
3. **Modular — প্রতিটা ধাপ আলাদা মাপা যায়:** Contains GT, LoC, cost per stage — নিজের improvement কোন ধাপে কাজ করছে তা পরিষ্কার দেখানো যায়।
4. **LLM বদলানো সহজ:** প্রতিটা ধাপ একটা prompt — যেকোনো API বা open model বসানো যায়।
5. **Intermediate artifact সংরক্ষণ করা যায়:** 40টা patch ও 40টা test একবার generate করে রেখে দিলে, selection-এর নতুন algorithm বারবার **বিনা LLM খরচে** পরীক্ষা করা যায় — student budget-এর জন্য আদর্শ।
6. **Deterministic অংশ বেশি:** greedy step-গুলো reproducible; sampling step-এ seed/temperature নিয়ন্ত্রণ।

### ১৬.২ প্রস্তাবিত module
1. **Task Loader:** SWE-bench Lite / Verified (HuggingFace) + Lite-S problem list।
2. **Localization module:** repo structure builder, skeleton extractor (Python `ast`), embedding retriever (LlamaIndex বা নিজের cosine search), Contains-GT ও LoC হিসাব।
3. **Repair module:** context window builder (±x line), Search/Replace parser ও applier, multi-sampling।
4. **Test module:** reproduction test generator + runner (3টা output parse), regression test finder।
5. **Selection module:** regression filter → reproduction filter → AST normalization → majority voting (Section ৬.৯-এর rule হুবহু)।
6. **Evaluation harness wrapper:** official `swebench` Docker harness দিয়ে final F2P/P2P।
7. **Dashboard:** % Resolved, cost per stage, cost per resolved, upper bound vs selected (η), reproduction funnel (300 → selected → plausible)।
8. **(Gap অংশ) Assurance layer:** নতুন re-ranker, repeated-run variance, security scan।

### ১৬.৩ Practical সতর্কতা
- Windows-এ **WSL2 + Docker Desktop** লাগবে (Paper 01, Section ১৬-এর মতো); test চালানো সবচেয়ে বেশি সময় নেয়।
- Official repo paper প্রকাশের পরেও update হয়ে থাকতে পারে — **paper-এর version-এর সাথে মেলাতে নির্দিষ্ট commit/tag** ব্যবহার করো এবং report-এ লিখে রাখো।
- GPT-4o-র ঐ নির্দিষ্ট snapshot (`gpt-4o-2024-05-13`) ভবিষ্যতে না পাওয়া যেতে পারে — তাই 96 হুবহু reproduce না হলেও স্বাভাবিক; নিজের run-এর সংখ্যাই report করো।
- প্রতিটা LLM call-এর token ও cost log করো — cost per stage table (Section ৬.১১) নিজে বানাতে পারবে।

---

## ১৭. পরবর্তী গবেষণায় এই Paper-এর প্রভাব (Context)
- **Paper নিজে যা বলে:** OpenAI SWE-bench Verified-এ (একই দিকে — মানুষ দিয়ে problem যাচাই) Agentless-এর benchmark analysis-কে স্বীকৃতি দিয়েছে; GPT-4o ও o1-এর showcase-এ Agentless ব্যবহার; RepoGraph ও Isoform এর উপর বানানো; MarsCode অনুপ্রাণিত; OpenDevin integrate করছিল।
- **সাধারণ ধারা (আমার পর্যবেক্ষণ, hedged):** এই paper-এর পরে "agent বনাম fixed workflow" বিতর্ক SE-AI research-এ একটা স্থায়ী প্রশ্ন হয়ে উঠেছে; অনেক পরের কাজ multi-sample generation + test-based selection (যা Agentless জনপ্রিয় করেছে) এর উপর দাঁড়িয়েছে বলে মনে হয়। নির্দিষ্ট paper বা সংখ্যা উল্লেখ করার আগে আমাদের বাকি sub-domain paper থেকে যাচাই করবো।
- **আমাদের sub-domain-এর গল্প:** Paper 01 (benchmark) → Paper 02 (agent + ACI) → Paper 03 (agent + code search) → **Paper 04 (agent দরকারই কি? + benchmark নিজেই কতটা বিশ্বাসযোগ্য?)**। এই চতুর্থ paper-টাই আমাদের **"reliability and assurance"** প্রশ্নের দিকে সরাসরি সেতু।

---

## ১৮. Supervisor-এর সম্ভাব্য প্রশ্ন ও উত্তর (Viva Prep)

**Q1. Agent আর Agentless-এর মূল পার্থক্য কী?**
A: Agent-এ LLM নিজে ঠিক করে পরের action কী হবে ও কোন tool চালাবে (multi-turn, feedback-ভিত্তিক)। Agentless-এ workflow মানুষের ঠিক করা — localization → repair → validation; LLM প্রতিটা ধাপে শুধু নির্দিষ্ট ছোট কাজ করে, কোনো tool চালায় না, পরের ধাপও ঠিক করে না।

**Q2. Hierarchical localization কেন? প্রমাণ কী?**
A: Context ছোট রাখতে — long context-এ LLM বিভ্রান্ত হয়। Table 2: file থেকে সরাসরি edit location-এ গেলে Contains GT 47.00%, খরচ USD 0.18; hierarchy-তে (greedy) 50.67%, USD 0.06। Context ~3,424 → ~698 → ~200 line।

**Q3. Skeleton format কেন, পুরো file দিলে কী সমস্যা?**
A: Table 2: skeleton-এ 58.33% Contains GT ও USD 0.02; পুরো file-এ 53.67% ও USD 0.15 — অর্থাৎ পুরো file দিলে খরচ বেশি **এবং** accuracy কম।

**Q4. Search/Replace format-এর সুবিধা কী?**
A: Line number বা diff header লাগে না, শুধু মূল code-এর একটা অংশ ও তার বদলি — LLM-এর ভুল কম, token কম, পুরো file আবার লিখতে হয় না বলে hallucination কম (paper-এর দাবি)।

**Q5. Final patch কীভাবে বাছাই হয়?**
A: 40টা patch → সবচেয়ে কম regression failure-এর গুলো রাখো → তাদের মধ্যে যেগুলো reproduction test-এ "Issue resolved" দেয় রাখো (কেউ না দিলে fallback: শুধু regression) → AST দিয়ে normalize করে majority voting। Ablation: voting 77 → +regression 81 → +reproduction 96।

**Q6. SWE-bench-এর PASS_TO_PASS test কেন সরাসরি ব্যবহার করেনি?**
A: P2P gold patch দেখে বানানো — বাস্তবে আগে থেকে জানা যায় না; SWE-bench maintainer-রাও এটা ব্যবহার না করতে বলেছেন। ব্যবহার করলে score 98 হতো (footnote 1) — কিন্তু সেটা benchmark-এর "oracle" তথ্য leak করা হতো।

**Q7. Reproduction test-এর মাত্র 94/213 ঠিক, তবুও এত লাভ (+15) কেন?**
A: (১) Regression-first conservative design — ভুল test একা কোনো patch জেতাতে পারে না; (২) fallback — কোনো patch pass না করলে test উপেক্ষিত; (৩) 94টা ভালো test যেখানে আছে সেখানে সঠিক patch আলাদা করতে খুব কার্যকর। তবে আমার মতে ভুল test সঠিক patch-কে বাদ দেওয়ার ঝুঁকি থেকেই যায়।

**Q8. SWE-bench Lite-S কী, আর reliability-র জন্য কেন গুরুত্বপূর্ণ?**
A: Lite থেকে exact patch (4.3%), misleading solution (5.0%) ও not-enough-info (10.0%) problem বাদ দিয়ে 249টা problem। Exact patch থাকলে tool "copy" করে score পায়, info না থাকলে সঠিক কাজ করেও fail — দুটোই score-কে অবিশ্বাস্য করে। Assurance-এর প্রথম শর্ত হলো measurement instrument নিজে নির্ভরযোগ্য হওয়া।

**Q9. Agentless কি সত্যিই সবচেয়ে সস্তা?**
A: না। একই LLM-এ SWE-agent-এর চেয়ে ~3.6 গুণ সস্তা (0.70 বনাম 2.53), কিন্তু Moatless (0.14–0.17) ও AutoCodeRover GPT-4 (0.45) প্রতি issue-তে সস্তা। Paper-এর দাবি "বেশিরভাগ agent-এর চেয়ে সস্তা" এবং cost-performance balance ভালো। আর এই cost-এ test execution-এর compute ধরা নেই।

**Q10. কোথায় agent-রা Agentless-এর চেয়ে ভালো?**
A: যে issue-তে কোনো location clue নেই (Figure 9c) — closed-source agent-রা জটিল code search tool দিয়ে ভালো করে। Authors নিজেই এটাকে future work বলেছেন।

**Q11. 126 আর 96-এর পার্থক্য কী বোঝায়?**
A: 40টা patch-এর মধ্যে অন্তত একটা সঠিক — এমন issue 126টা (42.0%), কিন্তু selection মাত্র 96টায় সঠিক বেছেছে (η ≈ 76.2%)। অর্থাৎ generation-এর চেয়ে **selection/validation এখন বড় bottleneck** — এটাই আমাদের সম্ভাব্য research gap।

**Q12. Contamination নিয়ে কী বলেছেন authors? তুমি কি সন্তুষ্ট?**
A: GPT-4o-র training data দেখা যায় না; আগের কাজও closed LLM ব্যবহার করেছে, আর SWE-bench authors cutoff-এর আগে/পরে পার্থক্য পাননি। আমার মতে এটা দুর্বল প্রমাণ (Paper 01, Section ১২ critique #3) — বিশেষ করে 4.3% problem-এ exact patch issue-তেই থাকায় memorization ও copying আলাদা করা কঠিন।

**Q13. এই paper-এর সবচেয়ে বড় দুর্বলতা কী, তোমার মতে?**
A: Single-run result ও variance না থাকা — sampling-নির্ভর pipeline-এ 96 বনাম 92-এর পার্থক্য noise কিনা অজানা। দ্বিতীয়ত, Lite-S description-এর সমস্যা ঠিক করলেও দুর্বল test-এর কারণে overfitted patch "resolved" হওয়ার সমস্যা থেকে যায়।

**Q14. তুমি এখান থেকে কী implement করবে?**
A: Agentless pipeline একটা ছোট subset-এ reproduce করবো, প্রতিটা stage-এর metric (Contains GT, cost, reproduction funnel, η) মাপবো, তারপর saved candidate patch-এর উপর নতুন re-ranker/assurance layer (better test, security scan, repeated-run variance) যোগ করবো।

---

## ১৯. Glossary (দ্রুত মনে রাখার জন্য)

| Term | অর্থ |
|---|---|
| Agent (LLM agent) | LLM + tool + নিজে পরের action ঠিক করার loop |
| Agentless | মানুষের ঠিক করা fixed pipeline; LLM সিদ্ধান্ত নেয় না |
| ACI (Agent-Computer Interface) | SWE-agent-এর বানানো agent-এর জন্য বিশেষ command interface (Paper 02) |
| Hierarchical localization | File → class/function → edit location — ধাপে ধাপে zoom-in |
| Repository structure format | `tree`-এর মতো শুধু file/folder নামের representation |
| Skeleton format | File-এর শুধু class/function header ও signature |
| Embedding | Text/code-কে অর্থবহ vector-এ রূপান্তর |
| Cosine similarity | দুটো vector কতটা একই দিকে — মিলের মাপ |
| Chunk | বড় file-এর ছোট টুকরা (এখানে 512 size) |
| Search/Replace diff | মূল code-এর অংশ খুঁজে বদলি বসানোর সরল patch format |
| Temperature | Sampling-এ randomness-এর মাত্রা (এখানে 0.8) |
| Candidate patch | Selection-এর আগে তৈরি সম্ভাব্য patch (এখানে 40/issue) |
| Reproduction test | Issue-র bug পুনরায় ঘটায় ও fix যাচাই করে এমন generated test |
| Plausible test | যে selected reproduction test gold patch-এর পরে "Issue resolved" দেয় |
| Regression test set | Passing test − LLM-চিহ্নিত non-regression test |
| Majority voting | সবচেয়ে বেশিবার আসা (normalized) উত্তর বাছাই |
| AST normalization | Parse → canonical unparse → diff; surface পার্থক্য মুছে ফেলা |
| Contains GT | Localization output-এ gold location আছে কিনা |
| % Correct Location | Final patch gold location-এর superset edit করেছে কিনা |
| Solution leakage | Issue-তেই সমাধান (exact patch) লেখা |
| Misleading solution | Issue-র প্রস্তাবিত সমাধান আসল fix-এর সাথে মেলে না |
| SWE-bench Lite-S | Problematic problem বাদ দিয়ে Lite-এর 249-problem subset |
| SWE-bench Verified | OpenAI-এর মানুষ-যাচাই করা 500-problem subset |
| Upper bound (all samples) | যেকোনো একটা candidate সঠিক হলেই গণনা — 126 (42.0%) |

---

## ২০. এক নজরে সারাংশ (Summary Card)

| | |
|---|---|
| **Problem** | Autonomous agent জটিল, ব্যয়বহুল, debug করা কঠিন; আর SWE-bench Lite-এর problem-এর মান অজানা |
| **Solution** | Agentless — fixed ৩-phase pipeline (hierarchical localization → multi-sample Search/Replace repair → regression + generated reproduction test + majority voting) |
| **Setting** | GPT-4o; top-3 file; 4 location set × 10 patch = 40; 40 reproduction test; T = 0.8; ±10 line context |
| **Key result** | SWE-bench Lite 96/300 = **32.00%** (open-source-এ সর্বোচ্চ), USD **0.70**/issue, 78,166 token; Lite-S 84/249 = 33.73%; Verified 194/500 = 38.80% |
| **Key ablation** | Voting 77 → +regression 81 → +reproduction 96; upper bound 126 (42.0%) |
| **Benchmark insight** | Lite-এ 4.3% exact patch, 9.7% সম্পূর্ণ ধাপ, 5.0% misleading, 10.0% অপর্যাপ্ত তথ্য → Lite-S (249) |
| **Main limitation** | Single run, compute cost অজানা, no-clue issue-তে দুর্বল, generated test অনির্ভরযোগ্য (94/213), contamination অযাচাইকৃত |
| **আমাদের জন্য gap** | **Patch selection ও validation-এর assurance** — 96 থেকে 126-এর দিকে, overfitting detection, run-to-run reliability, security-aware selection |

---

## ২১. বর্তমান (2026) প্রেক্ষাপট — আজকের Model ও Agent-দের সাথে তুলনা

> **উৎস:** সব current-state তথ্য `00_Current_State_2026_Sources.md` (compiled 2026-10-28) থেকে; প্রতিটা সংখ্যা **vendor-reported (কোম্পানির নিজের দাবি)** নাকি **independent (স্বাধীনভাবে মাপা)** তা লেখা আছে, আর "search-snippet only" তথ্যও চিহ্নিত। Saturation (**Paper 01, Section ২১**), scaffold ও variance (**Paper 02, Section ২১**), plausible বনাম correct (**Paper 03, Section ২১**) আগেই আলোচিত। এখানে Agentless-এর নিজস্ব তিনটা প্রশ্ন: (১) simple workflow বনাম agent, (২) candidate selection (126 বনাম 96) ও pass@k, (৩) benchmark quality audit (Lite-S)।

### ২১.১ Paper-এর সময় বনাম এখন

| দিক | Paper-এ (2024, arXiv v2) | এখন, October 2026 | উৎস |
|---|---|---|---|
| সরল harness বনাম জটিল agent | Fixed ৩-phase pipeline, GPT-4o: Lite 32.00%, Verified 38.80% | Evaluator-দের standard harness এখন সরল, bash-only **mini-SWE-agent** (Scale, Vals.ai, Artificial Analysis); Verified-এ এর সাথে top 97.0% (Claude Opus 5, independent) | mini-SWE-agent GitHub; Vals.ai Sept 2026 |
| Agentless-এর নিজের বর্তমান অবস্থা | Open-source; OpenAI GPT-4o ও o1 showcase-এ ব্যবহার (paper-এর দাবি) | **বর্তমান model-এর জন্য তথ্য পাওয়া যায়নি** — fact sheet-এ Agentless-এর কোনো 2026 entry নেই | — |
| Harness / scaffold gap | Baseline সংখ্যা বিভিন্ন report থেকে নেওয়া, ভিন্ন LLM | একই model-এ scaffold বদলালে **29.8 point** পর্যন্ত পার্থক্য, top-30-এর spread মাত্র 8.8 (independent); GPT-5.2-Codex Scale harness-এ 41.0% বনাম OpenAI scaffold-এ 56.4% (search-snippet only) | arXiv 2609.17394; Morph |
| Vendor বনাম harness-normalised | Commercial tool-এর দাবি যাচাই করা যায় না (paper-এর critique) | SWE-Bench Pro: Opus 5.5 89.9% (**vendor**, harness detail নেই) বনাম Scale-এর mini-SWE-agent board-এ top Muse Spark 1.1 61.50 ± 3.10 (independent; Opus 5.5/GPT-6 entry নেই) | Opus 5.5 System Card; labs.scale.com |
| Candidate selection | 40 patch থেকে 96 বাছাই, upper bound 126 (η ≈ 76.2%) | SWE-rebench: Fable 5 pass@1 64.5%, pass@5 78.4%; GLM-5.2 62.9% বনাম 81.1% (independent) | swe-rebench.com |
| Benchmark quality audit | Lite-এ 4.3% exact patch, 5.0% misleading, 10.0% insufficient info → Lite-S (249) | Verified-এর audited hard subset-এ ≥59.4% flawed test (OpenAI, search-snippet only); SWE-Bench Pro-তে 27.4–34.1% task broken (OpenAI audit, secondary report); SWE-Bench Pro Verified 102টা task ঠিক করেছে (75 narrow test, 22 misleading description) | OpenAI 2026-02-23; the-decoder; arXiv 2609.08149 |
| Grader-এর মান | Generated reproduction test-এর মাত্র 94/213 plausible | DeepSWE: LLM-judge বনাম SWE-Bench Pro-র inherited test-এ disagreement 32.4%, DeepSWE-এর নিজের verifier-এ 1.4% (independent) | arXiv 2607.07946 |
| প্রতি issue খরচ | GPT-4o-তে USD 0.70 (শুধু LLM API) | Verified-এ USD 0.10–2.05 per test; Terminal-Bench 4.0-এ USD 1.72–17.64 per test (দুটোই independent) | Vals.ai |

**সহজ কথায়:** 2024-এর Agentless ও 2026-এর model দুই ক্ষেত্রেই দেখা যায়: সঠিক উত্তর তৈরি করার ক্ষমতা আছে, কিন্তু বাছাই ঠিকমতো হয় না।

**আমার পর্যবেক্ষণ:** Agentless-এর selection efficiency ছিল $\frac{96}{126} \approx 0.76$; SWE-rebench-এ GLM-5.2-এর $\frac{62.9}{81.1} \approx 0.78$ আর Fable 5-এর $\frac{64.5}{78.4} \approx 0.82$। এগুলো একই জিনিস নয় (Agentless-এ এক run-এর 40টা candidate; SWE-rebench-এ 5টা স্বাধীন run), তবু দুটোই বলে: **"কোনো একটা চেষ্টায় সঠিক" আর "যেটা জমা দিলাম সেটা সঠিক"-এর মধ্যে এখনো 15–20%-এর মতো ফাঁক।**

### ২১.২ কোন Finding এখনো সত্য, কোনটা পুরনো হয়ে গেছে

- **এখনো সত্য, আরও শক্তভাবে — "জটিল agent loop সবসময় দরকার নেই":** Benchmark চালানোর standard harness এখন bash-only mini-SWE-agent। **আমার পর্যবেক্ষণ:** এটা Agentless-এর fixed pipeline নয় (এটাও একটা agent loop), কিন্তু "সরল scaffold + শক্তিশালী model" যুক্তির পক্ষে; আর বড় vendor-রা নিজেদের product agent (Claude Code, Codex) চালায় — দুই ধারাই টিকে আছে।
- **এখনো সত্য — "Selection-ই নতুন bottleneck" (Key Finding ৬):** pass@1 ও pass@5-এর 12–18 point gap (SWE-rebench) দেখায় সঠিক সমাধান প্রায়ই model-এর নাগালে আছে, কিন্তু একবারে সেটা বাছাই হয় না।
- **এখনো সত্য, এখন industry-wide — "Benchmark নিজেই ত্রুটিপূর্ণ" (Key Finding ৭):** Agentless একা Lite audit করেছিল; 2026-এ OpenAI নিজেই Verified বাদ দিয়েছে (59.4% flawed test) আর নিজের আগের সুপারিশ SWE-Bench Pro থেকেও সরে এসেছে (secondary report)। Lite-S ছিল এই ধারার প্রথম দিকের উদাহরণ।
- **এখনো সত্য — "P2P/oracle তথ্য ব্যবহার করলে score কৃত্রিমভাবে বাড়ে" (footnote 1: 96 → 98):** 2026-এ এর চরম রূপ — agent নিজে `.git` history থেকে gold patch পড়ে; GLM-5.2 safeguard ছাড়া 78.80%, safeguard দিলে 57.32% (SWE-Bench Pro Verified, independent)। Agentless-এর "oracle এড়ানো" practice এখন evaluation-এর minimum standard হওয়া উচিত।
- **পুরনো — "Lite-এ 32% = open-source-এ সর্বোচ্চ":** Lite আর কেউ report করে না; official Lite-এর শেষ entry 2025-09-11 (top 60.33%)।
- **অজানা — "No-location-clue issue-তে agent ভালো" (Figure 9c):** বর্তমান model-এ issue-category অনুযায়ী breakdown fact sheet-এ **পাওয়া যায়নি**।
- **অজানা — generated reproduction test (94/213) বর্তমান model-এ কতটা ভালো:** SWT-bench/TDD-Bench-এ বর্তমান model-এর entry পাওয়া যায়নি। পাশের প্রমাণ: agent-এর লেখা test patch-এর 80.2%-এ দুর্বল বা কোনো oracle নেই ("All Smoke, No Alarm", independent)।

### ২১.৩ এই Paper-এর Gap-গুলো আজও খোলা কিনা

| Gap | 2026-এ অবস্থা | প্রমাণ |
|---|---|---|
| G1 / CG2: Patch selection ও re-ranking | **খোলা** | SWE-rebench pass@1–pass@5 gap 12–18 point; SWE Atlas-এ Pass@1 থেকে Pass^3-এ 30–50% পতন (search-snippet only) |
| G2 / CG3: Reproduction test-এর মান | **খোলা** | 80.2% weak-oracle agent test; agent commit-এ over-mocking 36% বনাম 26% (search-snippet only); বর্তমান model-এর SWT-bench/TDD-Bench result পাওয়া যায়নি |
| G3 / CG1: Overfitted "resolved" patch | **খোলা** | PatchDiff 29.6% (2025 model); SWE-Bench Pro Verified-এ 75টা overly narrow test |
| G4 / CG4: Run-to-run reliability | **খোলা, এখন report হচ্ছে** | Vendor SE ±2.6 (Terminal-Bench 4.0, Anthropic); Vals: top-3 model-এর পার্থক্য run-to-run spread-এর চেয়ে ছোট (independent) |
| G5 / CG6: Contamination ও benchmark audit | **আংশিক সমাধান** | OpenAI-এর Verified ও SWE-Bench Pro audit, SWE-Bench Pro Verified, DeepSWE (নতুন করে লেখা 113 task) — Lite-S-এর ধারা এখন বড় পরিসরে; কিন্তু নতুন benchmark-এ বর্তমান model-এর independent coverage কম |
| G6: No-location-clue localization | **বর্তমান model-এর জন্য তথ্য পাওয়া যায়নি** | — |
| G7 / CG5: Security-aware selection | **খোলা** | SecPass 7.8–17.3% যেখানে FuncPass 62–84% (Endor Labs, Opus 4.6/GPT-5.4 যুগ); বর্তমান model-এর তথ্য নেই |
| G9 / CG8: Test execution-এর compute cost | **আংশিক** | Vals এখন cost ও duration per test দেয় (Opus 5.5: USD 13.20, 1h04m, Terminal-Bench 4.0) — কিন্তু সেটা API ও run মিলিয়ে কিনা, আলাদা compute cost কিনা, fact sheet-এ স্পষ্ট নয় |
| G10: Underspecification-এর automatic detection | **খোলা** | OpenAI "underspecified prompts" ও "misleading prompts" কে failure category বলেছে; SWE-Bench Pro Verified ঠিক করেছে হাতে; অসম্ভব task-এ Opus 5.5-এর reward-hacking চেষ্টা 3–6 গুণ (vendor) — তাই অস্পষ্ট task এখন শুধু score নয়, **integrity-র ঝুঁকিও** |
| CG10: Assurance tool-এর নিজের validity (Lite-S-এর label reliability-র মতো) | **খোলা** | OpenAI audit-এ automated screen (27.4%) ও মানুষ (34.1%) মাত্র 74% ক্ষেত্রে একমত (secondary report) — task-quality label নিজেই noisy |

**সহজ কথায়:** এই paper-এর অনেক সমস্যা 2026-এও খোলা। Benchmark ভুল, patch বাছাই, বানানো test-এর মান, বারবার চালালে ফলের পার্থক্য।

### ২১.৪ বর্তমান Model দিয়ে আবার পরীক্ষা করলে — SPL3 Idea

1. **Agentless বনাম mini-SWE-agent, একই current model:** SWE-rebench-এর সর্বশেষ window-এর 30টা task, একটা সস্তা model (যেমন GPT-6.1 Terra, vendor API দাম USD 1 / USD 5 per million token)। দুটো harness একই model-এ। **যে gap দেখাবে:** CG8 — 29.8-point scaffold effect আমাদের ছোট sample-এ কতটা; আর fixed workflow 2026-এর model-এ এখনো প্রতিযোগী কিনা (fact sheet-এ এর কোনো তথ্য নেই)।
2. **Offline re-ranker on saved candidates:** প্রতিটা task-এ 10–20টা candidate patch একবার generate করে রেখে, তারপর selection rule বদলে বদলে (majority vote, reproduction test, LLM judge, security penalty) বিনা নতুন LLM খরচে তুলনা। **Gap:** CG2 — η (selected ÷ upper bound) বর্তমান model-এ কত।
3. **Reproduction-test audit:** Generated test-কে buggy ও gold version-এ চালিয়ে "plausible test" হার (paper-এর 94/213-এর মতো), আর mutation দিয়ে oracle-এর শক্তি। **Gap:** CG3 — বর্তমান model-এর reproduction test-এর মান কেউ মাপেনি।
4. **Mini "Lite-S 2026" audit:** 50টা fresh task হাতে classify (exact patch, misleading, insufficient info, narrow test) দুজন annotator দিয়ে, Cohen's kappa সহ — paper-এর নিজের দুর্বলতা (#6) এড়িয়ে। **Gap:** CG6 ও CG10 — fresh benchmark-ও কতটা পরিষ্কার, আর label কতটা নির্ভরযোগ্য।
5. **Leakage-safe validation phase:** Agentless-এর test-execution phase-এ `.git` ও network বন্ধ রেখে, আর regression test হিসেবে benchmark-এর P2P কখনো না দিয়ে (paper-এর practice) — pipeline-এর কোনো ধাপ answer file ছোঁয় কিনা log করা। **Gap:** CG12 — fixed pipeline কি agent-এর চেয়ে কম gaming-প্রবণ? **আমার পর্যবেক্ষণ:** LLM tool চালায় না বলে এমন হওয়ার কথা, কিন্তু এটা পরীক্ষিত নয়।

### ২১.৫ Supervisor-এর সম্ভাব্য প্রশ্ন (2026 প্রসঙ্গে)

**Q1. Agentless-এর "agent দরকার নেই" যুক্তি কি 2026-এ টিকে আছে?**
A: আংশিকভাবে। Benchmark-চালানোর standard এখন সরল bash-only mini-SWE-agent, আর scaffold-এর প্রভাব model-এর পার্থক্যের চেয়ে বড় (29.8 বনাম 8.8 point) — সরলতা ও controlled scaffold-এর পক্ষে। কিন্তু fact sheet-এ Agentless নিজে বর্তমান model দিয়ে চালানোর কোনো সংখ্যা নেই, আর industry product agent (Claude Code, Codex) দিকে গেছে। তাই "fixed workflow বনাম agent" 2026-এর model-এ একটা পরীক্ষা না-করা প্রশ্ন — আমার SPL3 idea #1।

**Q2. Lite-S-এর মতো benchmark audit কি এখন বেশি গুরুত্বপূর্ণ?**
A: হ্যাঁ। 2024-এ Agentless 300টা Lite problem থেকে exact patch, misleading ও insufficient-info problem বাদ দিয়ে 249টা রেখেছিল — অর্থাৎ 51টা (17%) বাদ। 2026-এ OpenAI Verified-এর audited hard subset-এ ≥59.4% flawed test আর SWE-Bench Pro-তে 27–34% broken task পেয়েছে — আর দুটো benchmark-ই কার্যত ছেড়ে দেওয়া হয়েছে। Measurement instrument নির্ভরযোগ্য না হলে assurance-এর কোনো দাবিই টেকে না।

**Q3. 126 বনাম 96 — এই selection gap বর্তমান model-এ কি বন্ধ হয়েছে?**
A: সরাসরি একই মাপ পাওয়া যায়নি, তবে কাছাকাছি প্রমাণ বলছে না: SWE-rebench-এ top model-দের pass@1 আর pass@5-এর মধ্যে 12–18 point ফাঁক (independent)। অর্থাৎ সঠিক patch তৈরি হওয়ার ক্ষমতা আছে, কিন্তু নির্ভরযোগ্যভাবে সেটা বেছে নেওয়ার ব্যবস্থা নেই — এটাই আমার assurance layer-এর মূল লক্ষ্য।
