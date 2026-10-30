# Paper Analysis 03: AutoCodeRover — Autonomous Program Improvement

> **Sub-domain:** AI Coding Agents (sub-domain-এর ৩ নম্বর paper; আগে Paper 01 = SWE-bench, Paper 02 = SWE-agent)
> **Analysis করেছে:** SPL3 — AI Coding Agent Reliability and Assurance
> **Paper file:** `AI Coding Agents/Autonomous Program Improvement.pdf`
> **পূর্ণ path:** `E:\Course Book and Slide\4th Year\SPL3\Papers\AI Coding Agent Reliability and Assurance\AI Coding Agents\Autonomous Program Improvement.pdf`

---

## ০. Paper-এর পরিচয় (Bibliographic Info)

| বিষয় | তথ্য |
|---|---|
| **Title** | AutoCodeRover: Autonomous Program Improvement |
| **Authors** | Yuntong Zhang, Haifeng Ruan, Zhiyu Fan, Abhik Roychoudhury |
| **Institution** | National University of Singapore (NUS) |
| **Venue** | ISSTA 2024 (33rd ACM SIGSOFT International Symposium on Software Testing and Analysis), Vienna, Austria, 16–20 September 2024 — Software Testing/Analysis-এর top-tier conference |
| **DOI / arXiv** | 10.1145/3650212.3680384 · arXiv:2404.05427 (v3, 25 Jul 2024) |
| **Paper type** | **Technique / Tool paper** (নতুন agent system + empirical evaluation) |
| **Artifacts** | Open-source tool, সব generated patch, LLM conversation history, replication script — github.com/nus-apr/auto-code-rover |
| **Funding** | Singapore Ministry of Education Tier 3 grant "Automated Program Repair" (MOE-MOET32021-0001) |
| **আমাদের domain-এ গুরুত্ব** | ⭐⭐⭐⭐⭐ — এটা প্রথম দিকের paper যেটা LLM agent-কে **software engineering-এর পুরনো tool (AST, fault localization, test-based validation)**-এর সাথে জোড়া দিয়েছে, এবং **plausible patch-এর মধ্যে কতগুলো আসলে correct** তা manually যাচাই করে report করেছে — এটা সরাসরি আমাদের "Reliability and Assurance" domain-এর প্রশ্ন। |

---

## ১. এক লাইনে Paper (TL;DR)

**AutoCodeRover হলো একটা দুই-ধাপের LLM agent: প্রথম ধাপে LLM codebase-এর AST-এর উপর class/method/code search API ডেকে ধাপে ধাপে (stratified, iterative) প্রাসঙ্গিক code খুঁজে bug-এর জায়গা ঠিক করে; দ্বিতীয় ধাপে আরেকটা LLM agent সেই জায়গায় patch লেখে এবং patch apply না হলে আবার চেষ্টা করে। Test থাকলে SBFL (spectrum-based fault localization) দিয়ে আরও ভালো জায়গা দেখায়। GPT-4 দিয়ে SWE-bench Lite-এ 19% (pass@1) resolve করে, প্রতি task-এ গড়ে মাত্র 0.43 USD খরচে।**

### Supervisor-কে ৩০ সেকেন্ডে কীভাবে বলবো
> "Sir, SWE-bench (Paper 01) দেখিয়েছিল যে LLM-এর মূল সমস্যা হলো বড় codebase-এ bug-এর জায়গা খুঁজে পাওয়া। SWE-agent (Paper 02) LLM-কে shell-এর মতো file command দিয়ে সমাধান করতে চেয়েছে। AutoCodeRover বলছে — codebase-কে শুধু file-এর গাদা না ভেবে program structure (AST: class, method) হিসেবে দেখো। এরা LLM-কে ৭টা search API দিয়েছে (যেমন `search_class`, `search_method_in_class`), LLM ধাপে ধাপে search করে context জোগাড় করে, তারপর আলাদা agent patch লেখে। Test-suite থাকলে SBFL দিয়ে suspicious method দেখানো হয়। ফলাফল: SWE-bench Lite-এ 19% (SWE-agent 18%), কিন্তু খরচ 0.43 USD বনাম 2.51 USD — প্রায় ছয় গুণ সস্তা। সবচেয়ে গুরুত্বপূর্ণ — তারা নিজেরা manually দেখেছে যে test pass করা 78টা patch-এর মধ্যে মাত্র 51টা (65.4%) আসলে সঠিক। অর্থাৎ 'resolved' মানেই 'correct' নয় — এটা আমাদের assurance research-এর মূল motivation।"

---

## ২. Background — এই paper বুঝতে যা আগে জানা দরকার

Paper 01-এ যা ইতিমধ্যে ব্যাখ্যা করা হয়েছে (আবার লিখছি না, **Paper 01 দেখো**): GitHub issue/PR/commit (২.১), patch/diff (২.২), unit test ও test oracle (২.৩), regression testing (২.৪), **FAIL_TO_PASS / PASS_TO_PASS** (২.৫), context window (২.৬), BM25 (২.৭, সূত্র ৬.৫), contamination (২.৯), greedy decoding ও **pass@k** (২.১০, সূত্র ৬.১০), APR-এর পরিচয় (২.১১), Resolved metric (৬.৩–৬.৪)। SWE-agent-এর Agent-Computer Interface (ACI) **Paper 02 দেখো**।

এই paper-এ যে **নতুন** concept গুলো এসেছে, সেগুলো নিচে।

### ২.১ SWE-bench Lite
SWE-bench-এর একটা ছোট, সস্তা subset — **300টা task, 11টা Python project** থেকে (paper Section 2.2 অনুযায়ী)। পুরো SWE-bench-এ 2,294টা task, 12টা repository (Paper 01)। এই paper মূলত Lite-এ, সাথে full SWE-bench ও "Devin subset" (570 task)-এ পরীক্ষা করেছে।

### ২.২ Program Repair বনাম Program Improvement
- **Program repair:** শুধু bug ঠিক করা (software **maintenance**)।
- **Program improvement (এই paper-এর শব্দ):** bug fix **এবং** নতুন feature যোগ করা (software **evolution**) — দুটোই। Authors বলছেন একটা development team existing project maintain করতে গেলে এই দুই ধরনের কাজই প্রধান।
- উদাহরণ: paper-এর motivating example django-13933 আসলে issue tracker-এ **"New feature"** হিসেবে চিহ্নিত — অর্থাৎ শুধু bug নয়।
- **কেন নামটা গুরুত্বপূর্ণ:** Authors-এর vision হলো "autonomous software engineering" — ভবিষ্যতে LLM-এর লেখা code-কেও আরেকটা autonomous process improve করবে, যাতে সেটা trust করা যায়।

### ২.৩ Abstract Syntax Tree (AST) ও Program Structure
- **AST** হলো source code-এর একটা গাছ-আকৃতির (tree) representation, যেখানে প্রতিটা node একটা syntactic জিনিস: module → class → method (function) → statement → expression।
- উদাহরণ (সরল):
```python
class ModelChoiceField(ChoiceField):      # ClassDef node
    def to_python(self, value):           # FunctionDef node (class-এর child)
        raise ValidationError(...)        # Raise statement node
```
- এর AST-তে `ModelChoiceField` নামের একটা ClassDef node আছে, তার child হলো `to_python` নামের FunctionDef node। তাই "ModelChoiceField class-এর ভেতরে to_python method কোথায়?" — এই প্রশ্নের উত্তর text search ছাড়াই, নির্ভুলভাবে দেওয়া যায়।
- **Text/file দৃষ্টিভঙ্গি বনাম AST দৃষ্টিভঙ্গি:** `grep` দিয়ে "to_python" খুঁজলে comment, string, অন্য class-এর একই নামের method — সব চলে আসে। AST দিয়ে খুঁজলে ঠিক যেই class-এর method, শুধু সেটাই আসে।
- **Class signature:** class-এর নাম, parent class, আর ভেতরের method-গুলোর শুধু নাম/parameter (body ছাড়া)। লম্বা class-এর পুরোটা না দিয়ে signature দিলে context ছোট থাকে।
- Python-এ built-in `ast` module দিয়ে খুব সহজে AST বানানো যায় (Section ১৬-তে কাজে লাগবে)।

### ২.৪ Code Search API
- LLM নিজে hard disk-এ file খুঁজতে পারে না; তাকে কিছু **function/tool** দেওয়া হয়, যা সে নাম ও argument দিয়ে "ডাকতে" পারে। AutoCodeRover-এ এমন **৭টা API** আছে (Table 1, Section ৫.৩-এ পুরো list)।
- **"Hints" ধারণা:** Issue-তে user প্রায়ই class/method/file-এর নাম বা ছোট code snippet লিখে দেয়। LLM এই hint-গুলো থেকে keyword বের করে API-এর argument বানায়।
- **SWE-agent (Paper 02)-এর সাথে পার্থক্য:** SWE-agent LLM-কে file open/scroll/search/edit-এর মতো shell-ধরনের command দেয় (file-level)। AutoCodeRover দেয় program-structure-level command (class/method-level)।

### ২.৫ LLM Agent, Tool Call ও Multi-agent Design
- **LLM agent:** LLM যে নিজে সিদ্ধান্ত নেয় পরের কাজ কী, tool ডাকে, ফল দেখে আবার সিদ্ধান্ত নেয় — একটা loop।
- AutoCodeRover-এ **দুটো আলাদা agent** (আসলে একই GPT-4, আলাদা prompt/role): (১) **context retrieval agent**, (২) **patch generation agent**।

### ২.৬ Context Retrieval, Iterative Search ও Stratified Search
- **Context retrieval:** patch লেখার আগে কোন code LLM-কে দেখাতে হবে তা জোগাড় করা। Paper 01-এ এটা BM25 দিয়ে একবারে (one-shot) করা হয়েছিল।
- **Iterative search:** একবার search-এর ফল থেকে নতুন নাম পাওয়া যায় (যেমন class signature-এ নতুন method-এর নাম), সেটা দিয়ে আবার search — ধাপে ধাপে।
- **Stratified search:** search-কে "স্তরে" (stratum, বহুবচন strata) ভাগ করা। প্রতিটা স্তরে LLM **একসাথে একাধিক, কিন্তু শুধু দরকারি** API call বাছাই করে; ফল context-এ যোগ হয়; তারপর LLM বলে context যথেষ্ট কিনা। যথেষ্ট না হলে পরের স্তর।
- **কেন দরকার (paper-এর দুই observation):** (ক) একটা মাত্র API call যথেষ্ট নয় — অসম্পূর্ণ context; (খ) সব call একসাথে করলে context বিশাল হয়ে LLM বিভ্রান্ত হয় বা context window ছাড়িয়ে যায়। Stratified search এই দুইয়ের মাঝামাঝি।

### ২.৭ Fault Localization (FL)
Program-এর **কোথায়** bug আছে তা খুঁজে বের করা। SWE-bench-এর ভাষায় একে localization বলা হয়েছিল (Paper 01: "localization-ই মূল bottleneck")। FL অনেক রকম: spectrum-based, mutation-based, learning-based, LLM-based ইত্যাদি। এই paper শুধু spectrum-based ব্যবহার করেছে।

### ২.৮ Spectrum-Based Fault Localization (SBFL)
- **Program spectrum / coverage:** একটা test চালালে program-এর কোন কোন অংশ (statement/method) execute হলো তার হিসাব।
- **মূল intuition:** যে method **fail করা test-এ বেশি** চলে আর **pass করা test-এ কম** চলে, সেটা বেশি সন্দেহজনক (suspicious)।
- প্রতিটা program element-কে একটা **suspiciousness score** দেওয়া হয়; সবচেয়ে বেশি score-এর গুলো সম্ভাব্য bug location।
- Score হিসাবের জনপ্রিয় সূত্র: **Tarantula** ও **Ochiai** (paper এই দুটোর নাম উল্লেখ করেছে)। পুরো সূত্র ও worked example Section ৬.৩-এ।
- **Granularity:** statement-level, basic block-level, method-level। AutoCodeRover **method-level SBFL** ব্যবহার করে, কারণ LLM লম্বা code snippet পড়তে পারে।
- **দুর্বলতা:** SBFL-এর accuracy test-suite-এর quality-র উপর অনেক নির্ভর করে। দরকার অন্তত একটা failing test।

### ২.৯ Test-suite based APR-এর তিন ধারা
Paper-এর Related Work (Section 2.1) অনুযায়ী:
| ধারা | কীভাবে কাজ করে | উদাহরণ (paper-এ cited) |
|---|---|---|
| **Search-based** | পূর্বনির্ধারিত mutation operator দিয়ে অনেক patch বানিয়ে test pass করে এমনটা খোঁজা | GenProg |
| **Semantics-based** | Test থেকে একটা "repair constraint" বানিয়ে constraint solver দিয়ে patch synthesize | SemFix, Angelix |
| **Learning-based** | Deep learning model-কে code-এ train করে পরের সঠিক token predict | CoCoNuT, ইত্যাদি |
| **LLM-based APR** | LLM-কে buggy statement দিয়ে বারবার patch চাওয়া যতক্ষণ না test pass করে | — |
- **Authors-এর critique:** LLM-based APR সাধারণত **perfect fault localization ধরে নেয়** (bug-এর line আগে থেকে জানা)। বাস্তবে বড় project-এ এটা জানাই সবচেয়ে কঠিন। আবার traditional APR-এর ভালো test-suite লাগে, যা সবসময় থাকে না, আর তারা issue-র natural language description ব্যবহার করে না। AutoCodeRover এই দুই ফাঁক পূরণ করতে চায়।

### ২.১০ Generate-and-Validate, Retry Loop ও Linter
- **Generate-and-validate:** patch বানাও → যাচাই করো → fail হলে আবার বানাও।
- AutoCodeRover-এ যাচাই দুই স্তরে: (১) **syntactic** — patch নির্দিষ্ট format মানছে কি, original code-এ apply হয় কি, linter-এ Python syntax error (যেমন indentation) আছে কি; (২) **semantic (ঐচ্ছিক)** — test থাকলে test-suite চালিয়ে দেখা।
- **Linter:** code না চালিয়ে syntax/style ভুল ধরার tool (যেমন pyflakes, flake8)। Paper নির্দিষ্ট linter-এর নাম বলেনি।

### ২.১১ Plausible, Correct ও Overfitting Patch (খুব গুরুত্বপূর্ণ)
| Patch type | সংজ্ঞা (paper Section 6.1) |
|---|---|
| **Plausible** | দেওয়া test-suite pass করে |
| **Correct** | Plausible **এবং** developer-এর intent মেনে চলে — এই paper-এ: developer patch-এর সাথে **semantically equivalent** |
| **Overfitting** | Plausible কিন্তু developer-এর intent মানে না — test pass করে কিন্তু আসলে ভুল |
- **Correctness বনাম Plausibility:** SWE-bench-এর "Resolved" আসলে **plausibility** মাপে, correctness নয়। Test দুর্বল হলে overfitting patch-ও resolved হয়ে যায়।
- **Semantically equivalent:** code হুবহু এক না হলেও আচরণ (behavior) এক। যেমন Figure 3-এ AutoCodeRover `%`-formatting দিয়ে value বসিয়েছে, developer `params={'value': value}` দিয়েছে — লেখা আলাদা, প্রভাব একই।
- APR community-তে এটা পুরনো সমস্যা — paper Smith et al. (FSE 2015, "Is the cure worse than the disease?")-কে cite করে।

### ২.১২ Bug Reproduction / Issue Reproducer
Issue-র বর্ণনা থেকে এমন একটা test বানানো যেটা bug-টা ঘটিয়ে দেখায় (fail করে)। এটা পেলে SBFL চালানো ও patch যাচাই — দুটোই করা যায়। Paper এটা future work হিসেবে প্রস্তাব করেছে (*LLM Test Generation* sub-domain-এ বিস্তারিত আসবে)।

### ২.১৩ Temperature
LLM output-এর randomness নিয়ন্ত্রণের parameter। 0 = প্রায় deterministic; বেশি = বেশি বৈচিত্র্য। এই paper temperature = 0.2 ব্যবহার করেছে — তবু output পুরোপুরি deterministic নয়, তাই ৩ বার চালানো হয়েছে।

### ২.১৪ Static Call Graph, Language Server, Data Dependence (Discussion-এ উল্লেখিত)
- **Call graph:** কোন method কোন method-কে ডাকে তার graph।
- **Language server (LSP):** IDE-তে "jump to definition"-এর মতো সুবিধা যে দেয়।
- **Forward data dependence:** একটা variable-এর মান পরে কোথায় কোথায় ব্যবহৃত হয়।
- Authors এগুলোকে ভবিষ্যতে context retrieval আরও শক্তিশালী করার উপায় বলেছেন।

### ২.১৫ Devin
Cognition Labs-এর closed-source commercial "AI software engineer"। এর details public নয়, তাই paper শুধু Devin-এর technical report-এর সংখ্যা নিয়েছে (নিজে চালায়নি)।

---

## ৩. Problem Statement — কী সমস্যা ছিল?

### ৩.১ মূল সমস্যা
1. **Automatic programming ≠ software engineering:** Copilot-এর মতো tool code লিখতে পারে, কিন্তু বাস্তবে বেশিরভাগ কাজ হলো existing program-কে **improve** করা (bug fix, feature add)। LLM-এর লেখা code-ও ভুল বা vulnerable হতে পারে — তাকেও improve করতে হবে।
2. **Localization কঠিন:** Paper 01 দেখিয়েছিল বড় codebase-এ সঠিক জায়গা খুঁজে পাওয়াই মূল bottleneck। LLM-based APR কাজগুলো এটাকে এড়িয়ে যায় (perfect FL ধরে নেয়)।
3. **Traditional APR-এর সীমা:** ভালো test-suite লাগে (বাস্তবে প্রায়ই থাকে না), আর issue-র natural language বর্ণনা কাজে লাগায় না।
4. **তখনকার LLM agent-গুলো "AI flavor"-এর:** Devin, SWE-agent codebase-কে file-এর collection হিসেবে দেখে; software engineering-এর structure ও analysis tool (AST, FL, test) কাজে লাগায় না — authors-এর দাবি।
5. **খরচ:** GPT-4-এর মতো model ব্যয়বহুল; SWE-agent প্রতি task-এ ~2.5 USD খরচ করছিল।
6. **Patch-এর গুণমান report হচ্ছিল না:** Devin ও SWE-agent কতগুলো patch সত্যি সঠিক তা report করেনি (authors-এর দাবি, Section 1)।

### ৩.২ কেন এটা গুরুত্বপূর্ণ?
Developer-রা bug fix-এ অনেক সময় দেয় (paper অনুযায়ী, যে issue-গুলো ACR solve করেছে তার developer-দের গড়ে 2.68 দিন লেগেছে)। যদি একটা tool অল্প খরচে, অল্প সময়ে কিছু শতাংশ issue নিজে থেকে সমাধান করতে পারে, এবং সেই patch-গুলো **বিশ্বাসযোগ্য** হয়, তাহলে developer-এর কাজ কমে।

---

## ৪. Goal ও Research Questions

**Goal:** একটা software-engineering-oriented, সস্তা ও কার্যকর LLM agent বানানো যেটা শুধু issue description ও codebase থেকে GitHub issue (bug fix + feature) autonomous-ভাবে সমাধান করে; test থাকলে debugging technique দিয়ে আরও ভালো করে।

Paper-এর **explicit RQ** (Section 5):
- **RQ1:** AutoCodeRover কতটা মানুষের মতো software issue automate করতে পারে? (efficacy, time, cost, SWE-agent/Devin-এর সাথে তুলনা, patch correctness)
- **RQ2:** বিদ্যমান debugging/analysis technique (এখানে SBFL) কি AutoCodeRover-কে সাহায্য করে?
- **RQ3:** AutoCodeRover ও fully automated program improvement-এর সামনে চ্যালেঞ্জ কী? (failure taxonomy)

**Authors-এর ঘোষিত "software engineering outlook" (Section 1-এর পাঁচটা dimension):**
1. File-এর collection নয়, **program representation (AST)**-এর উপর কাজ।
2. মানুষ engineer-এর মতো **program structure (class, method, snippet) ধরে code search**।
3. সময়ের চেয়ে **efficacy বেশি গুরুত্বপূর্ণ**, যদি সময় একটা সীমার মধ্যে থাকে (developer survey অনুযায়ী automated repair-এর জন্য 30–60 মিনিট গ্রহণযোগ্য)।
4. **Test-based fault localization** দিয়ে code search guide করা।
5. Solve করা issue-গুলোর patch সত্যি **acceptable** কিনা পরীক্ষা করা (≈2/3 correct)।

---

## ৫. Methodology — কীভাবে কাজটা করা হয়েছে

### ৫.১ Overall Workflow (Figure 2)
Input: problem statement $P$ (issue title + description) ও codebase $C$। (Test-suite $T$ ঐচ্ছিক।) Output: একটা patch।

| ধাপ | Stage | কে করে | কী হয় |
|---|---|---|---|
| 1 | Context retrieval | Retrieval agent | Issue পড়ে keyword/hint বের করে, search API বাছাই করে |
| 2 | Context retrieval | Local AST engine | API গুলো locally চালিয়ে ফল (signature/code) ফেরত দেয় |
| 3 | Context retrieval | Retrieval agent | ফল analyze করে: context যথেষ্ট? না হলে ধাপ 1-এ ফেরত (পরের stratum) |
| 4 | Context retrieval | Retrieval agent | যথেষ্ট হলে **buggy location**-এর list দেয় (file, class, method) |
| 5 | Patch generation | Patch agent | Buggy location-এর সঠিক code আনে, আগের সব context + analysis দেখে patch লেখে |
| 6 | Patch generation | System | Patch format ঠিক আছে? apply হয়? linter OK? না হলে "Patch cannot be applied… try again" বলে retry |
| 7 | Output | System | Final patch (retry limit শেষ হলে "best patch so far") |

### ৫.২ Motivating Example: django-13933 (Figure 1, Figure 3)
Issue: `ModelChoiceField` validation error দেওয়ার সময় ভুল choice-এর **value** দেখায় না (যেখানে `ModelMultipleChoiceField` দেখায়)। এটা "New feature" ticket।
1. **Step 1:** Agent issue থেকে বোঝে `ModelChoiceField` ও `ModelMultipleChoiceField` প্রাসঙ্গিক; Django field-এ validation সাধারণত `clean` method-এ হয় — তাই ৪টা call: `search_class` ×2, `search_method_in_class("clean", …)` ×2।
2. **Step 2:** ফল: দুই class-এর signature পাওয়া গেল; `ModelChoiceField`-এ **`clean` নেই** (call #3 ব্যর্থ) — এটা নিজেই তথ্য, agent-এর ধারণা ঠিক করে দেয়। Signature থেকে নতুন দুটো method দেখা গেল: `to_python` ও `validate` (issue-তে উল্লেখ ছিল না)। Agent লক্ষ করে `ModelMultipleChoiceField`-এর error message-এ `%(value)s` আছে, কিন্তু `ModelChoiceField`-এ নেই — সম্ভাব্য root cause।
3. **Step 3:** নতুন পাওয়া নাম দিয়ে আবার search (**iterative**): `search_method_in_class("validate", "ModelChoiceField")`, `search_method_in_class("to_python", "ModelChoiceField")`। দেখা গেল `validate` শুধু parent-কে ডাকে; `to_python` আসলে `ValidationError` raise করে কিন্তু value দেয় না → এটাই buggy location। Agent context "sufficient" বলে।
4. **Step 4:** Patch agent `django/forms/models.py`-এর `ModelChoiceField.to_python`-এ patch লেখে: error message-এ `% {'value': value}` যোগ করে।
5. **Figure 3:** Developer `params={'value': value}` argument দিয়ে করেছে — লেখা আলাদা, কিন্তু প্রভাব একই, এবং developer-এর test pass করে।

### ৫.৩ Context Retrieval API (Table 1)
| API | কী খোঁজে | Output |
|---|---|---|
| `search_class(cls)` | পুরো codebase-এ class `cls` | Class-এর **signature** |
| `search_class_in_file(cls, f)` | File `f`-এ class `cls` | Class-এর signature |
| `search_method(m)` | পুরো codebase-এ method `m` | Method-এর **পূর্ণ implementation** |
| `search_method_in_class(m, cls)` | Class `cls`-এ method `m` | Method-এর implementation |
| `search_method_in_file(m, f)` | File `f`-এ method `m` | Method-এর implementation |
| `search_code(c)` | পুরো codebase-এ code snippet `c` | Snippet-এর আগে-পরে **±3 line** |
| `search_code_in_file(c, f)` | File `f`-এ snippet `c` | Snippet-এর ±3 line |

**Design decision ও কারণ:**
- Class-এর জন্য পুরো body নয়, **শুধু signature** — বড় project-এ class অনেক লম্বা হয়। Authors-এর মতে, একটা নির্দিষ্ট সীমায় context কেটে ফেলার চেয়ে signature দেওয়া ভালো। Signature দেখে agent পরে দরকারি method আলাদা করে চাইতে পারে।
- **LLM-এর সাথে interface:** API-গুলোর বর্ণনা ও expected output prompt-এ দেওয়া থাকে; LLM API-এর নাম ও argument-এর list লিখে উত্তর দেয়; system local codebase-কে AST-তে parse করে search চালায় এবং ফল LLM-কে ফেরত দেয়।
- **Hint-এর উদাহরণ (Figure 4):** sympy-12481-এ `Permutation` class দুবার উল্লেখ; django-13230-এ `feed.add_item()` snippet, `syndication.views` package path, `item_extra_kwargs` method name ইত্যাদি।

### ৫.৪ Stratified Context Search (Section 4.3, Figure 5)
1. **Stratum 1:** Context-এ শুধু problem statement। LLM hint থেকে দরকারি API call-এর একটা **set** বাছাই করে (একাধিক হতে পারে, কিন্তু "only necessary")।
2. Call-গুলো locally চলে; ফল context-এ যোগ হয় → "Project context 1"।
3. LLM-কে জিজ্ঞাসা: context যথেষ্ট? (ক) না → পরের stratum, যেখানে context = problem statement + এ পর্যন্ত পাওয়া code; (খ) হ্যাঁ → buggy location-এর list (যেমন `ClassA.methodB`, `ClassB.methodC`)।
4. Stratum 2, …, k — আগের ফল থেকে পাওয়া নতুন নাম পরের call-এর argument হয়।

**কেন কাজ করে (paper-এর যুক্তি):** django-13230-এ শুধু `search_method("add_item")` দিয়ে শুরু করলে LLM মনে করতে পারে এটাই যথেষ্ট — অসম্পূর্ণ। আবার সব hint একসাথে search করলে বিশাল context। Stratified search "best use of context" — authors-এর ভাষায় "optimal context" (এটা authors-এর দাবি; কোনো ablation দিয়ে প্রমাণ করা হয়নি — Section ১২ দেখো)।

### ৫.৫ Analysis-Augmented Context Retrieval: SBFL (Section 4.4)
- **কখন:** যদি test-suite $T$ পাওয়া যায় (developer-এর দেওয়া বা অন্য tool-এর তৈরি)।
- **কীভাবে:** Context retrieval শুরুর **আগেই** SBFL চালিয়ে **top-5 suspicious method** বের করা হয় (method-level)। এগুলো agent-কে দেওয়া হয় এই বলে: "results from an external analysis tool that identifies suspicious code"।
- **SBFL-কে বদলে দেওয়া হয়নি, augment করা হয়েছে:** SBFL-এর output সরাসরি patch location হিসেবে ব্যবহার করা হয়নি, কারণ SBFL-এর accuracy test quality-র উপর নির্ভর করে। বরং SBFL-এর method-গুলো **অতিরিক্ত hint** — agent issue-র বর্ণনা আর SBFL-এর list মিলিয়ে (cross-reference) সিদ্ধান্ত নেয়।
- **Patch validation (ACR-sbfl setting):** Patch তৈরি হলে পুরো test-suite চালানো হয়; fail করলে patch agent-কে আবার ডাকা হয়। এই validation loop **৩ বার** পর্যন্ত চলে।
- **RQ2-তে ব্যবহৃত test-suite:** SWE-bench Lite-এ দেওয়া **developer-written test case** (অর্থাৎ PR-এর test) — এটা গুরুত্বপূর্ণ, Section ১২-তে আলোচনা।

### ৫.৬ Patch Generation (Section 4.5)
1. Patch agent পায়: problem statement, buggy location/method-এর list, এবং পুরো retrieval history (কোন API ডাকা হয়েছিল, কী ফল এসেছিল, retrieval agent-এর analysis)।
2. প্রথমে buggy location-এর **সঠিক code snippet** codebase থেকে আনে।
3. নির্দিষ্ট format-এ patch লেখে (Figure 1 Step 4-এ দেখানো: `<file>…</file>` tag-এ file ও line, আর `<patched>…</patched>` tag-এ নতুন code)।
4. **Retry loop:** patch format না মানলে, codebase-এ syntactically apply না হলে, বা linter Python syntax সমস্যা (যেমন indentation error) পেলে — আবার চেষ্টা।
5. **Retry limit = ৩**। তারপর "best patch so far" output।

### ৫.৭ Stopping / Termination
- Retrieval loop থামে যখন LLM নিজে বলে context যথেষ্ট ও buggy location ঠিক করে।
- পুরো tool থামে যখন **একটা patch তৈরি হয়, অথবা context retrieval stage দশবার repeat হয়** (Section 5)।
- Patch agent-এর retry সর্বোচ্চ ৩ বার; ACR-sbfl-এ test validation loop সর্বোচ্চ ৩ বার।
- (আমার পর্যবেক্ষণ: "context retrieval stage repeats ten times" — এটা ১০টা stratum, নাকি পুরো retrieval stage ১০ বার নতুন করে শুরু — paper-এ পরিষ্কার নয়।)

### ৫.৮ দুই Scenario
| Scenario | Input | কী ব্যবহার হয় | Table 2-এ নাম |
|---|---|---|---|
| Issue-only (বাস্তবসম্মত) | $P$, $C$ | Stratified search + patch retry (format/apply/lint) | ACR @1, ACR @3 |
| Test-suite available | $P$, $C$, $T$ | উপরের সব + SBFL top-5 hint + test-based patch validation (৩ বার) | ACR-sbfl |

### ৫.৯ পুরো Algorithm ধাপে ধাপে (আমার সারাংশ)
1. Codebase-কে AST-তে parse করে class/method index তৈরি।
2. (ঐচ্ছিক) Test-suite চালিয়ে method-level SBFL → top-5 suspicious method।
3. Stratum $i = 1$: context = issue (+ SBFL list)।
4. LLM দরকারি API call-এর set বাছাই করে।
5. Local AST search চালিয়ে ফল context-এ যোগ।
6. LLM analysis: যথেষ্ট? না হলে $i$ এক বাড়িয়ে ধাপ 4-এ ফেরত।
7. যথেষ্ট হলে buggy location list।
8. Patch agent location-এর code এনে patch লেখে।
9. Format/apply/lint check; fail হলে retry (≤3)।
10. (ঐচ্ছিক) Test চালাও; fail হলে নতুন patch (≤3)।
11. Patch না এলে retrieval আবার (মোট ≤10 বার); তারপর output।

---

## ৬. Mathematical Formulation — সূত্র ও ব্যাখ্যা

Paper-এ explicit equation প্রায় নেই (tool paper হওয়ায়)। নিচে paper-এর বর্ণনা ও সংখ্যা থেকে formal রূপ দেওয়া হলো। **যেখানে formalization বা হিসাব আমার নিজের, সেখানে তা উল্লেখ করা আছে।**

### ৬.১ Task ও Output-এর Formal Definition (আমার formalization)
Paper 01-এর মতো notation:
$$
\hat{\delta} = \text{ACR}(P,\; C) \quad \text{বা} \quad \hat{\delta} = \text{ACR}(P,\; C,\; T)
$$
- $P$ = problem statement (issue title + description)
- $C$ = buggy version-এ checkout করা codebase
- $T$ = test-suite (শুধু ACR-sbfl setting-এ)
- $\hat{\delta}$ = তৈরি হওয়া patch

দুই stage-কে আলাদা function হিসেবে লেখা যায়:
$$
(K,\; L) = \mathcal{R}(P,\; C), \qquad \hat{\delta} = \mathcal{G}(P,\; K,\; L)
$$
$\mathcal{R}$ = context retrieval agent, $K$ = জোগাড় হওয়া context (API call ও তাদের ফল), $L$ = buggy location-এর list, $\mathcal{G}$ = patch generation agent।

### ৬.২ Stratified Search-এর Formal রূপ (আমার formalization)
$$
K_0 = \{P\}, \qquad A_i = \text{LLM}_{\text{select}}(K_{i-1}), \qquad K_i = K_{i-1} \cup \{\, \text{exec}(a,\; \text{AST}(C)) \;:\; a \in A_i \,\}
$$
$$
\text{stop at stratum } i \quad \text{যদি} \quad \text{LLM}_{\text{sufficient}}(K_i) = \text{true}
$$
- $A_i$ = stratum $i$-এ LLM-এর বাছাই করা API call-এর set (একাধিক হতে পারে)
- $\text{exec}(a, \text{AST}(C))$ = AST-এর উপর call $a$ locally চালানোর ফল
- $\text{LLM}_{\text{sufficient}}$ = LLM-এর নিজের "context যথেষ্ট" সিদ্ধান্ত

**Worked example (django-13933, Figure 1):**
- $K_0$ = issue text
- $A_1$ = { search_class(ModelChoiceField), search_class(ModelMultipleChoiceField), search_method_in_class(clean, ModelChoiceField), search_method_in_class(clean, ModelMultipleChoiceField) } → $\text{size}(A_1) = 4$
- $K_1$ = issue + 2টা signature + "clean পাওয়া যায়নি" + ১টা clean implementation → insufficient
- $A_2$ = { search_method_in_class(validate, ModelChoiceField), search_method_in_class(to_python, ModelChoiceField) } → $\text{size}(A_2) = 2$
- $K_2$ যথেষ্ট → $L$ = { django/forms/models.py :: ModelChoiceField.to_python }
- মোট ২টা stratum-এ ৬টা API call। (Figure 1-এর "Step 1–3" এখানে দুই round search + একটা analysis-এর সমান।)

### ৬.৩ SBFL Suspiciousness Score

**গুরুত্বপূর্ণ সতর্কতা:** Paper শুধু বলেছে score "Tarantula ও Ochiai-এর মতো metric দিয়ে হিসাব করা যায়" এবং তারা **method-level SBFL, top-5** ব্যবহার করেছে; **ঠিক কোন formula ব্যবহার করেছে তা paper-এ লেখা নেই।** (Public code-এ কোনটা আছে তা নিজে যাচাই করে নিতে হবে — আমি paper থেকে নিশ্চিত হতে পারিনি।) তাই দুটো standard সূত্রই দিচ্ছি।

প্রতিটা program element (এখানে method) $m$-এর জন্য:

| Symbol | মানে |
|---|---|
| $e_f(m)$ | কতগুলো **failing** test $m$-কে execute করেছে |
| $e_p(m)$ | কতগুলো **passing** test $m$-কে execute করেছে |
| $n_f(m)$ | কতগুলো failing test $m$-কে execute **করেনি** |
| $n_p(m)$ | কতগুলো passing test $m$-কে execute করেনি |
| $N_F$ | মোট failing test $= e_f + n_f$ |
| $N_P$ | মোট passing test $= e_p + n_p$ |

**Ochiai (Abreu et al., 2007 — paper-এ cited [3]):**
$$
\text{Ochiai}(m) = \frac{e_f(m)}{\sqrt{N_F \cdot \left(e_f(m) + e_p(m)\right)}} = \frac{e_f(m)}{\sqrt{\left(e_f(m) + n_f(m)\right) \cdot \left(e_f(m) + e_p(m)\right)}}
$$

**Tarantula (Jones et al., 2002 — paper-এ cited [21]):**
$$
\text{Tarantula}(m) = \frac{\dfrac{e_f(m)}{N_F}}{\dfrac{e_f(m)}{N_F} + \dfrac{e_p(m)}{N_P}}
$$

**Intuition:**
- Numerator-এ $e_f$: যত বেশি failing test method-টা ছুঁয়েছে, তত সন্দেহ।
- Denominator-এ $e_p$: যত বেশি passing test-ও ছুঁয়েছে, তত সন্দেহ কমে (কারণ ঠিকঠাক চলার সময়ও এটা চলে)।
- কোনো failing test না ছুঁলে ($e_f = 0$) score = 0।

**Worked example (hypothetical — paper-এ কোনো SBFL সংখ্যা নেই, এটা বোঝানোর জন্য বানানো):** ধরো ৫টা test: ২টা fail ($N_F = 2$), ৩টা pass ($N_P = 3$)। চারটা method-এর coverage:

| Method | $e_f$ | $e_p$ | Ochiai | Tarantula |
|---|---|---|---|---|
| `Model._prepare_related_fields_for_save` | 2 | 0 | 1.000 | 1.000 |
| `ForeignKey.resolve_related_fields` | 2 | 1 | 0.816 | 0.750 |
| `Model._do_update` | 1 | 3 | 0.354 | 0.333 |
| `Product.__init__` | 0 | 2 | 0 | 0 |

হিসাব:
- প্রথমটা: Ochiai $= 2/\sqrt{2 \times 2} = 2/2 = 1.0$; Tarantula $= (2/2)/((2/2) + (0/3)) = 1/1 = 1.0$
- দ্বিতীয়টা: Ochiai $= 2/\sqrt{2 \times 3} = 2/2.449 = 0.816$; Tarantula $= 1/(1 + 1/3) = 1/1.333 = 0.75$
- তৃতীয়টা: Ochiai $= 1/\sqrt{2 \times 4} = 1/2.828 = 0.354$; Tarantula $= 0.5/(0.5 + 1) = 0.333$
- চতুর্থটা: $e_f = 0$ → দুটোই 0

Ranking: প্রথম > দ্বিতীয় > তৃতীয় > চতুর্থ। AutoCodeRover-এ এভাবে top-5 method agent-কে দেওয়া হয়। (Method-এর নাম django-13964 case study থেকে ধার করা, কিন্তু সংখ্যাগুলো কাল্পনিক।)

**Paper-এর আসল উদাহরণ (Figure 9, django-13964):** SBFL top-5 ছিল — (1) `DatabaseOperations.convert_uuidfield_value`, (2) `Model._do_update`, (3) `Model._prepare_related_fields_for_save`, (4) `Value._resolve_output_field`, (5) `ForeignKey.resolve_related_fields`। Agent top-1 নয়, বরং **3rd ও 5th** method search করেছে, কারণ এগুলো issue-র text-এর সাথে বেশি মেলে। 3rd-টাতেই developer আসলে fix করেছিল। → SBFL score একা যথেষ্ট নয়; LLM-এর language understanding + SBFL মিলিয়ে ভালো ফল।

### ৬.৪ Resolve Rate
Paper 01-এর Resolved সংজ্ঞা (F2P + P2P সব pass) একই:
$$
\text{Resolve rate} = \frac{\text{number of resolved tasks}}{N} \times 100\%
$$
**Worked example (Table 2):**
- SWE-bench Lite: $57/300 = 0.19 = 19.00\%$ (ACR @1); $54/300 = 18.00\%$ (SWE-agent)
- Full SWE-bench: $285/2294 = 0.1242 = 12.42\%$ (ACR @1); $286/2294 = 12.47\%$ (SWE-agent)
- ACR-sbfl: $66/300 = 22.00\%$

### ৬.৫ pass@1 ও pass@3 (ACR @1, ACR @3)
প্রতিটা task ৩ বার ($n = 3$) চালানো হয়েছে। Task $i$-এর run $r$-এর ফল $s_{i,r} \in \{0, 1\}$।
$$
\text{ACR@3} = \frac{1}{N} \sum_{i=1}^{N} \mathbb{1}\left[\max_{r \in \{1,2,3\}} s_{i,r} = 1\right]
$$
অর্থাৎ তিনবারের **যেকোনো একবার** resolve হলেই গণ্য।
$$
\text{ACR@1} = \frac{1}{3N} \sum_{r=1}^{3} \sum_{i=1}^{N} s_{i,r}
$$
অর্থাৎ এক run-এর গড় সাফল্য। (**সতর্কতা:** paper "pass@1" বলেছে এবং Devin subset-এ "12.63% … on average in pass@1" লিখেছে — তাই আমি ধরে নিচ্ছি @1 = তিন run-এর গড়; কিন্তু paper এটা স্পষ্টভাবে সংজ্ঞায়িত করেনি।) Paper 01-এর unbiased pass@k estimator-এ $n = k = 3$ বসালে $1 - \binom{n-c}{3}/\binom{3}{3}$ = "অন্তত একবার সফল" — ACR@3-এর সাথে একই।

**Worked example:** Lite-এ @1 = 57 task, @3 = 78 task → ৩ বার চালালে আরও $78 - 57 = 21$টা task resolve হয় (relative বৃদ্ধি $21/57 \approx 36.8\%$, আমার হিসাব)। Full SWE-bench-এ $422 - 285 = 137$টা বেশি।

### ৬.৬ Time ও Cost Metric
Paper-এর তিনটা metric: (১) % resolved, (২) average time cost (seconds), (৩) average token cost (token ও USD)।
$$
\bar{t} = \frac{1}{N}\sum_{i=1}^{N} t_i, \qquad \bar{c} = \frac{1}{N}\sum_{i=1}^{N} c_i
$$
$t_i$ = task $i$-তে মোট সময় (seconds), $c_i$ = task $i$-তে মোট token (বা USD), $N$ = task সংখ্যা।
**গুরুত্বপূর্ণ:** @3-এর time ও cost = **তিনবার চালানোর মোট** (প্রতি task)।

**Worked example (Table 2, Lite):**
- ACR @1: 195 s ≈ 3.25 মিনিট; 37k token = 0.43 USD
- ACR @3: 520 s ≈ 8.67 মিনিট (paper-এর হিসাব); 112k token = 1.30 USD (≈ $3 \times 37$k = 111k, মিলে যায়)
- SWE-agent: 245k token = 2.51 USD → ACR @1-এর চেয়ে $2.51/0.43 \approx 5.8$ গুণ বেশি খরচ (আমার হিসাব)

**Implied price per million token (আমার হিসাব):** ACR: $0.43/37{,}000 \times 10^6 \approx 11.6$ USD; SWE-agent: $2.51/245{,}000 \times 10^6 \approx 10.2$ USD। দুটো প্রায় কাছাকাছি, তাই খরচের পার্থক্য মূলত **token সংখ্যার** পার্থক্য থেকে।

**Cost per resolved task (আমার derived metric — paper-এ নেই, কিন্তু assurance-এর জন্য বেশি অর্থবহ):**
$$
\text{CPR} = \frac{N \times \bar{c}}{\text{number resolved}}
$$
| System (Lite) | মোট খরচ | Resolved | CPR |
|---|---|---|---|
| ACR @1 | $300 \times 0.43 = 129$ USD | 57 | ≈ 2.26 USD |
| ACR @3 | $300 \times 1.30 = 390$ USD | 78 | = 5.00 USD |
| ACR-sbfl | $300 \times 0.47 = 141$ USD | 66 | ≈ 2.14 USD |
| SWE-agent | $300 \times 2.51 = 753$ USD | 54 | ≈ 13.94 USD |

(ACR-sbfl-এর খরচে test চালানোর compute ধরা হয়নি — শুধু token।)

**Developer time-এর সাথে তুলনা (paper-এর দাবি + আমার হিসাব):** ACR @3 যে 78টা issue solve করেছে, তার 66টার জন্য developer-দের PR বানাতে গড়ে ~2.68 দিন লেগেছে (বাকি 12টা 34–4023 দিন)। $2.68 \text{ দিন} = 2.68 \times 24 \times 60 \approx 3859$ মিনিট; $3859/8.67 \approx 445$ গুণ দ্রুত। কিন্তু এটা **calendar time বনাম compute time** — developer পুরো 2.68 দিন এই issue-তে কাজ করেনি। তাই এই তুলনা সাবধানে ব্যবহার করতে হবে (Section ১২)।

### ৬.৭ Correctness Rate (Plausible → Correct)
$$
\text{Correctness rate} = \frac{N_{\text{correct}}}{N_{\text{plausible}}}, \qquad N_{\text{overfit}} = N_{\text{plausible}} - N_{\text{correct}}
$$
- $N_{\text{plausible}}$ = test pass করা (resolved) task — এখানে ACR @3-এর 78
- $N_{\text{correct}}$ = যেগুলো developer patch-এর সাথে semantically equivalent (৩ run-এর যেকোনোটায় correct patch থাকলেই)

**Worked example (Section 6.1):** $51/78 = 0.6538 \approx 65.4\%$। Overfitting $= 78 - 51 = 27$টা। এর মধ্যে "all but 2" = **25টা** developer-এর একই method modify করেছে (location ঠিক, content ভুল)।

**আমার derived সংখ্যা:** সত্যিকারের correct fix-এর হার $= 51/300 = 17.0\%$ — অর্থাৎ "26% resolved" থেকে assurance-এর দৃষ্টিতে সংখ্যাটা 17%-এ নেমে আসে। Location-level useful patch (correct + same-method overfitting) $= 51 + 25 = 76$টা = $76/78 \approx 97.4\%$ plausible patch অন্তত সঠিক জায়গায় হাত দিয়েছে।

### ৬.৮ Overlap ও Unique Fix (Figure 6 Venn Diagram)
$A$ = ACR @1-এর resolved set (57), $S$ = SWE-agent-এর resolved set (54):
$$
|A \cap S| = 31, \qquad |A| - |A \cap S| = 57 - 31 = 26, \qquad |S| - |A \cap S| = 54 - 31 = 23
$$
$$
|A \cup S| = |A| + |S| - |A \cap S| = 57 + 54 - 31 = 80
$$
**আমার হিসাব:**
- দুটো মিলিয়ে (oracle ensemble) $80/300 \approx 26.7\%$ — কোনোটার একার চেয়ে অনেক বেশি।
- Jaccard similarity $= |A \cap S|/|A \cup S| = 31/80 \approx 0.39$ — দুই tool অনেকটাই ভিন্ন task solve করে।
- ACR-এর resolved-এর $26/57 \approx 45.6\%$ SWE-agent পারেনি।

### ৬.৯ SBFL-এর প্রভাব (RQ2)
$$
\Delta = 66 - 57 = 9 \text{ task}, \qquad \frac{9}{300} = 3 \text{ percentage point}, \qquad \frac{9}{57} \approx 15.8\% \text{ relative বৃদ্ধি}
$$
(Relative বৃদ্ধি আমার হিসাব।) তাছাড়া ACR-sbfl এমন **7টা** task solve করেছে যা অন্য কোনো run পারেনি।

### ৬.১০ Failure Taxonomy-এর বণ্টন (Figure 10)
৩০০ task, প্রতিটা task-এর ৩ run-এর মধ্যে **best run** ধরে:
$$
\sum_{k} \text{share}_k = 26.0 + 29.3 + 20.0 + 18.0 + 6.7 = 100\%
$$
সংখ্যায় (আমার রূপান্তর, $300 \times$ শতাংশ): Success ≈ 78, Wrong patch ≈ 88, Wrong location in correct file = 60, Wrong file = 54, No patch ≈ 20 → মোট 300।

---

## ৭. Experimental Setup

| বিষয় | বিবরণ |
|---|---|
| **Benchmark** | SWE-bench Lite (300 task, 11 project), full SWE-bench (2,294), SWE-bench Devin subset (570 = full-এর random 25%) |
| **Input** | শুধু issue-র natural language description + buggy version-এর local repository (RQ1); RQ2-তে সাথে developer test-suite |
| **Foundation model** | OpenAI GPT-4 (`gpt-4-0125-preview`) — API বাছাই, issue refine, patch লেখা সব কাজে |
| **LLM parameter** | temperature = 0.2, max_tokens = 1024, বাকি default |
| **Patch retry limit** | 3 |
| **Test validation loop (ACR-sbfl)** | 3 বার |
| **SBFL** | Method-level, top-5 suspicious method, developer-written test ব্যবহার করে |
| **Termination** | Patch তৈরি হলে, বা context retrieval stage 10 বার repeat হলে |
| **Repetition** | পুরো experiment ৩ বার (randomness এড়াতে) → @1 ও @3 |
| **Baselines** | SWE-agent (GitHub-এ public result সরাসরি নেওয়া), Devin (technical report-এর সংখ্যা; tool access নেই) |
| **Metric** | % resolved, average time (s), average token ও USD cost; অতিরিক্ত manual correctness check |
| **Machine** | x86_64 Linux, Ubuntu 20.04 |
| **Patch evaluation** | Official SWE-bench Docker environment |
| **Correctness check পদ্ধতি** | কমপক্ষে ২ জন author প্রতিটা patch cross-validate; মতভেদ হলে আরেকজন author সিদ্ধান্ত দেন |

---

## ৮. Results — মূল ফলাফল

### ৮.১ Overall Result (Table 2)

**SWE-bench Lite (size = 300):**
| Tool | Resolved | Avg Time (s) | Avg Tokens (Cost) |
|---|---|---|---|
| SWE-agent | 18.00% (54) | — | 245k (2.51 USD) |
| **ACR @1** | **19.00% (57)** | 195 | **37k (0.43 USD)** |
| ACR @3 | 26.00% (78) | 520 | 112k (1.30 USD) |
| ACR-sbfl | 22.00% (66) | 250 | 40k (0.47 USD) |

**Full SWE-bench (size = 2294):**
| Tool | Resolved | Avg Time (s) | Avg Tokens (Cost) |
|---|---|---|---|
| SWE-agent | 12.47% (286) | — | 240k (2.46 USD) |
| ACR @1 | 12.42% (285) | 248 | 39k (0.45 USD) |
| ACR @3 | 17.96% (422) | 701 | 120k (1.39 USD) |

**SWE-bench Devin subset (size = 570):**
| Tool | Resolved | Avg Time (s) | Avg Tokens (Cost) |
|---|---|---|---|
| SWE-agent | 13.51% (77) | — | 234k (2.40 USD) |
| Devin | 13.86% (79) | > 600 | — |
| ACR @1 | 12.63% (72) | 238 | 37k (0.42 USD) |
| ACR @3 | 18.77% (107) | 692 | 117k (1.36 USD) |

("—" = data নেই। SWE-agent-এর time public নয়; Devin-এর cost public নয়।)

**Authors-এর ব্যাখ্যা:**
- Full SWE-bench-এ ACR @1 (12.42%) SWE-agent (12.47%)-এর "at par"।
- Lite-এ ACR @1 19% বনাম SWE-agent 18%।
- @3-এ বড় লাফ → ভবিষ্যতে program specification থাকলে "iterated generate-and-validate" দিয়ে উন্নতির সুযোগ।
- Devin subset-এ ACR @3 (18.77%) Devin-এর (13.86%) চেয়ে বেশি, এবং সময় অনেক কম।

**আমার পর্যবেক্ষণ:** Devin subset-এ **ACR @1 (12.63%) আসলে Devin (13.86%) ও SWE-agent (13.51%) দুটোর চেয়েই কম।** "Devin-এর চেয়ে ভালো" দাবি শুধু @3 (তিনবার চেষ্টা) দিয়ে — যা সমান শর্তে তুলনা নয়। Full SWE-bench-এও @1-এ SWE-agent এক task এগিয়ে (286 বনাম 285)।

### ৮.২ Time ও Token Cost (Figure 7, Figure 8)
- **Figure 7:** success rate বনাম গড় cost (USD) — ACR কম খরচে সমান বা বেশি success দেখায়।
- ACR @1 Lite-এ গড়ে 195 s ও 37k token (0.43 USD); SWE-agent 245k token (2.51 USD)।
- ACR @3 (তিন run মিলিয়ে) 520 s (~8.67 মিনিট) — developer survey অনুযায়ী automated repair-এর গ্রহণযোগ্য 30–60 মিনিটের অনেক নিচে।
- ACR @3-এর 78টা solved issue-এর 66টায় developer-দের PR তৈরিতে গড়ে ~2.68 দিন; বাকি 12টা close হতে 34 থেকে 4023 দিন লেগেছে।
- **Figure 8 (resolved task-এর token distribution):** ACR **19টা** task 10k-এর কম token-এ (~0.1 USD) এবং **31টা** task 10k–30k token-এ resolve করেছে; অন্যদিকে SWE-agent-এর resolved task-এর **66.7%**-এ 100k-এর বেশি token লেগেছে। Authors-এর ব্যাখ্যা: stratified retrieval দ্রুত error location ধরে ফেলে।

### ৮.৩ AutoCodeRover বনাম SWE-agent — Overlap (Figure 6)
| | সংখ্যা |
|---|---|
| শুধু ACR পেরেছে (unique) | 26 |
| দুটোই পেরেছে (common) | 31 |
| শুধু SWE-agent পেরেছে (unique) | 23 |
| মিলিত (union) | 80 (আমার হিসাব) |

- **ACR-এর unique 26-এর কারণ (authors):** AST-level fine-grained search দিয়ে bug location নির্ভুলভাবে ধরা — যেমন django-13401-এ একসাথে তিনটা দরকারি method search।
- **SWE-agent-এর unique 23-এ ACR কেন ব্যর্থ (authors):** মূলত **unimplemented search API** — যেমন django-12286-এ LLM `search_file` ডেকেছে, যা ACR-এ নেই। Error message ফেরত দিলেও LLM পরে valid API ডাকতে পারেনি। → আরও robust search API দরকার।
- **Conclusion:** দুই tool একে অপরের **complement**।

### ৮.৪ Plausible বনাম Correct Patch (Section 6.1)
| Metric | মান |
|---|---|
| Plausible (ACR @3, Lite) | 78 |
| Manually correct (semantically equivalent to developer patch) | 51 |
| **Correctness rate** | **65.4%** (≈ 2/3) |
| Overfitting | 27 (আমার বিয়োগ) |
| Overfitting কিন্তু developer-এর একই method modify করেছে | সবগুলো, শুধু 2টা বাদে (= 25) |

**Overfitting-এর কারণ (authors):**
1. LLM-এর ক্ষমতার সীমা বা অপর্যাপ্ত context (মূল কারণ)।
2. **Issue-তে reporter একটা preliminary patch দিয়েছিল** যা final developer patch থেকে আলাদা — LLM সেটা অনুসরণ করে ভুল করেছে।
3. **Issue-তে একটা নির্দিষ্ট case উল্লেখ ছিল** — LLM শুধু সেটাই ঠিক করেছে, কিন্তু developer অনুরূপ অন্য case-ও ঠিক করেছে।
- **Authors-এর উপসংহার:** test-suite-এর মতো **issue description-ও একটা incomplete specification**। আর overfitting patch-ও developer-এর কাজে লাগে, কারণ সেটা সঠিক location দেখিয়ে দেয়।
- **গুরুত্বপূর্ণ:** Authors বলেছেন Devin ও SWE-agent এই ধরনের correctness report করেনি।

### ৮.৫ RQ2: SBFL-এর প্রভাব
| | ACR @1 | ACR-sbfl |
|---|---|---|
| Resolved (Lite) | 57 (19%) | **66 (22%)** |
| Avg time | 195 s | 250 s |
| Avg tokens (cost) | 37k (0.43 USD) | 40k (0.47 USD) |
| অন্য কোনো run পারেনি এমন unique task | — | **7** |

**Case study — django-13964 (Figure 9):** Issue: non-numeric primary key-ওয়ালা parent model-এ child set করে save করলে data loss। Issue-তে `Product` ও `Order` class-এর নাম আছে — কিন্তু এগুলো শুধু bug reproduce করার উদাহরণ, bug-এর কারণ নয় (বিভ্রান্তিকর hint)।
- **SBFL ছাড়া:** Stratum 1: `search_class(Product)`, `search_class(Order)`…; Stratum 2: `search_code_in_file("class Product(models.Model):", "tests/queries/models.py")` — অকাজের দিকে চলে যায়।
- **SBFL সহ:** Top-5 list পেয়ে agent `search_method_in_class(resolve_related_fields, ForeignKey)` ও `search_method_in_class(_prepare_related_fields_for_save, Model)` ডাকে — দ্বিতীয়টাতেই developer fix করেছিল।
- Agent SBFL-এর top-1 অন্ধভাবে নেয়নি, 3rd ও 5th নিয়েছে কারণ সেগুলো issue-র অন্য hint-এর সাথে মেলে → **execution-based analysis issue-তে না থাকা তথ্য যোগ করে, আর LLM দুই উৎস মিলিয়ে নেয়।**

### ৮.৬ RQ3: Failure Taxonomy (Figure 10)
৩০০ task-এর প্রতিটার best run (৩ run থেকে) ধরে, SBFL ছাড়া। (Paper text-এ এটাকে "ACR-all in Table 2" বলা হয়েছে, কিন্তু Table 2-এ এই নাম নেই — আমার ধারণা এটা ACR @3-এর সমতুল্য, কারণ Success = 26.0% = @3।)

| Category | মানে | শতাংশ | ≈ Task (আমার রূপান্তর) |
|---|---|---|---|
| Success | Issue resolve হয়েছে | 26.0% | 78 |
| Wrong patch | Developer যত method বদলেছে সবগুলোই বদলেছে, কিন্তু content ভুল (location ঠিক) | 29.3% | 88 |
| Wrong location in correct file | সঠিক file, কিন্তু ভুল method/class (বা একাধিক method-এর সবগুলো ধরেনি) | 20.0% | 60 |
| Wrong file | ভুল file-এ patch | 18.0% | 54 |
| No patch | কোনো applicable patch তৈরি হয়নি | 6.7% | 20 |

**Authors-এর বিশ্লেষণ:**
- **Wrong patch (29.3%)** — location ঠিক, তাই উন্নতির পথ: আরও fine-grained **intra-procedural analysis** ও **specification inference** দিয়ে method-level repair guidance।
- **Wrong location/file/no patch** (মোট 44.7%) — fault localization ব্যর্থ। "Wrong file" ও "No patch" task-গুলোর issue-তে কম class/method/file-এর নাম থাকে; কিছুতে শুধু reproduce করার ছোট example আছে → সেখান থেকে **test-suite generate করে SBFL** চালানো যায়। আর যেগুলোতে reproducible example নেই, শুধু natural language — সেখানে **human involvement** দরকার।

### ৮.৭ Leaderboard Context (Section 7, Figure 11)
- April 2024-এর পর থেকে SWE-bench-এ academia ও industry মিলিয়ে **17-এর বেশি** attempt।
- 12 July 2024-এ full SWE-bench leaderboard-এ সর্বোচ্চ: Factory Code Droid **19.27%**।
- একই সময়ে AutoCodeRover-এর নতুন version: **18.83%** (full SWE-bench)।
- Authors বলেছেন ফলাফল "right spirit"-এ দেখতে হবে — ACR-এর আসল গুরুত্ব হলো **program specification থেকে patching guide করার** পদ্ধতি।

---

## ৯. Key Findings / Insights (Supervisor-কে বলার মতো ৮টা পয়েন্ট)

1. **Program structure-aware search কাজ করে ও সস্তা:** Lite-এ 19% (SWE-agent 18%), কিন্তু খরচ ~5.8 গুণ কম (0.43 বনাম 2.51 USD)।
2. **Localization-ই আসল খেলা:** Resolved patch-এর বেশিরভাগ token-সাশ্রয়ী — 19টা task 10k token-এর কম লেগেছে; দ্রুত সঠিক জায়গা খুঁজে পাওয়াই efficiency আনে।
3. **Repetition-এ বড় লাভ:** ৩ বার চালালে 19% → 26% — LLM output-এর বৈচিত্র্য কাজে লাগানো যায়, কিন্তু এটা একই সাথে **non-determinism**-এর প্রমাণ (reliability concern)।
4. **Test-based analysis (SBFL) সাহায্য করে:** 19% → 22%, এবং 7টা unique task — issue-তে না থাকা তথ্য দেয়।
5. **LLM + SBFL > SBFL একা:** Agent SBFL ranking অন্ধভাবে নেয় না, issue text-এর সাথে মিলিয়ে নেয়।
6. **Plausible ≠ Correct:** 78টা plausible-এর মাত্র 51টা (65.4%) correct — প্রায় ১/৩ overfitting। Issue description-ও incomplete specification।
7. **Tools are complementary:** ACR ও SWE-agent-এর common মাত্র 31; union 80 (26.7%)।
8. **Failure-এর বড় অংশ localization:** 44.7% task-এ সঠিক location-ই পাওয়া যায়নি; 29.3%-এ location ঠিক কিন্তু patch ভুল।

---

## ১০. কেন এই Solution অন্যগুলোর থেকে ভালো?

| বৈশিষ্ট্য | Paper 01 RAG baseline (BM25 + one-shot) | SWE-agent (Paper 02) | Devin | Traditional test-based APR | **AutoCodeRover** |
|---|---|---|---|---|---|
| Codebase-কে কীভাবে দেখে | File (keyword match) | File + shell-ধরনের command | অজানা (closed) | Statement-level | **AST: class/method** |
| Context retrieval | একবারে | Agent নিজে file navigate | অজানা | FL output | **Stratified, iterative API search** |
| Fault localization | নেই | LLM নিজে | অজানা | SBFL ইত্যাদি | **LLM + (ঐচ্ছিক) SBFL** |
| Issue text ব্যবহার | হ্যাঁ | হ্যাঁ | হ্যাঁ | সাধারণত না | **হ্যাঁ** |
| Test-suite লাগে? | না | না | না | **হ্যাঁ** | না (থাকলে কাজে লাগায়) |
| Cost/task (Lite) | — | 2.51 USD | — | — | **0.43 USD** |
| Correctness manually যাচাই | না | না (authors-এর দাবি) | না (authors-এর দাবি) | APR-এ প্রচলিত | **হ্যাঁ (65.4%)** |
| Open-source | হ্যাঁ | হ্যাঁ | না | বিভিন্ন | **হ্যাঁ** |

(Paper 01-এর baseline অন্য model ও অন্য setup-এ চলেছিল, তাই সংখ্যার সরাসরি তুলনা অর্থবহ নয় — শুধু design পার্থক্য দেখানো হলো।)

**মূল শক্তি:**
1. **Software engineering knowledge + LLM:** AST, FL, linter, test — পুরনো SE tool-কে LLM-এর সাথে জুড়েছে।
2. **Context efficiency:** Signature-only output, ±3 line snippet, শুধু দরকারি call — কম token, কম বিভ্রান্তি।
3. **Modular:** Retrieval ও patching আলাদা — প্রতিটা আলাদাভাবে উন্নত/মাপা যায়।
4. **Flexible:** Test না থাকলেও চলে; থাকলে SBFL ও validation যোগ হয়।
5. **Honest evaluation dimension:** Plausible বনাম correct আলাদা করে report।
6. **Fully reproducible artifacts:** Patch, conversation, script সব public।

---

## ১১. কোন পরিস্থিতিতে এই paper/approach ভালো কাজ করে, কোথায় করে না

### ✅ ভালো কাজ করে যখন:
- Issue-তে **class/method/file-এর নাম বা code snippet** (hint) আছে।
- Codebase **object-oriented ও well-structured** (class/method দিয়ে ভাগ করা)।
- Bug এক বা অল্প কয়েকটা method-এ সীমাবদ্ধ।
- **Test-suite আছে** এবং অন্তত একটা failing test আছে (SBFL কাজ করে)।
- **খরচ সীমিত** — অল্প token-এ কাজ করতে হবে।

### ❌ ভালো কাজ করে না / সীমিত যখন:
- Issue-তে code entity-র নাম কম, শুধু natural language বা শুধু reproduction example (Wrong file / No patch category)।
- Issue-তে **বিভ্রান্তিকর hint** (যেমন django-13964-এর `Product`/`Order`) বা reporter-এর ভুল preliminary patch।
- Fix-এ **একাধিক method/file** বদলাতে হয় (Wrong location in correct file-এর একটা কারণ)।
- LLM এমন search চায় যা implement করা নেই (যেমন `search_file`)।
- **Python ছাড়া** অন্য language — AST search, linter Python-specific (আমার পর্যবেক্ষণ; architecture অন্য language-এ নেওয়া সম্ভব কিন্তু evaluate করা হয়নি)।
- Module-level code, config file, non-code file (যেমন documentation, setup file)-এ পরিবর্তন লাগলে — class/method-কেন্দ্রিক API দিয়ে ধরা কঠিন (আমার পর্যবেক্ষণ)।

---

## ১২. Limitations — দুর্বলতা

### ১২.১ Authors যা নিজেরা স্বীকার করেছেন
1. **LLM randomness** — ভিন্ন run-এ ভিন্ন ফল; সমাধান হিসেবে ৩ বার চালানো ও replication package।
2. **Overfitting** — "resolved" মানে শুধু PR-এর test pass; সমাধান হিসেবে manual semantic equivalence check।
3. **Test-suite সবসময় পাওয়া যায় না** — SBFL scenario "not always practical"।
4. **Unimplemented search API** (যেমন `search_file`) — আরও robust API দরকার।
5. **Issue description incomplete specification** — preliminary patch বা নির্দিষ্ট case উল্লেখের কারণে overfitting।
6. **সব সিদ্ধান্ত LLM-এর হাতে** (কোথায় search, কখন থামা) — সবসময় যথেষ্ট নয়; human involvement-এর interface দরকার।
7. Wrong patch-এর জন্য আরও fine-grained analysis ও specification inference দরকার।

### ১২.২ আমার Critical Analysis (Professor-level observation)
1. **ACR-sbfl-এ evaluation test-এর leakage (সবচেয়ে গুরুত্বপূর্ণ):** RQ2-তে SBFL ও patch validation-এর জন্য "developer-written test cases … provided in SWE-bench lite" ব্যবহার করা হয়েছে। SWE-bench-এর evaluation-ও এই PR test (F2P) দিয়েই হয় (Paper 01)। যদি ঐ test-গুলোই SBFL ও ৩-বার validation loop-এ ব্যবহৃত হয়, তাহলে tool কার্যত **evaluation oracle দেখে** patch বাছাই করছে — 22% সংখ্যাটা issue-only setting-এর সাথে তুলনীয় নয়। Paper এটা "common scenario in program repair" বলেছে, কিন্তু PR-এর নতুন test বাস্তবে fix-এর আগে থাকে না। (Paper-এর text থেকে ঠিক কোন test set ব্যবহৃত হয়েছে — test patch সহ কিনা — সম্পূর্ণ স্পষ্ট নয়; তবে "developer-written test cases for each task instance" বাক্য থেকে এটাই মনে হয়।)
2. **অসম তুলনা (pass@3 বনাম pass@1):** Devin-কে ছাড়িয়ে যাওয়ার দাবি শুধু @3-এ; @1-এ ACR Devin ও SWE-agent দুটোর নিচে (Devin subset)। @3-এর cost ও time-ও তিনগুণ।
3. **Statistical significance নেই:** Lite-এ 57 বনাম 54 — মাত্র ৩টা task-এর পার্থক্য; ৩ run-এর মধ্যে variance বা confidence interval report হয়নি। এত ছোট পার্থক্যে "higher than SWE-agent" বলা দুর্বল।
4. **Baseline নিজেরা চালানো হয়নি:** SWE-agent-এর GitHub result ও Devin-এর report-এর সংখ্যা নেওয়া; একই model version, একই environment, একই সময়ে চালানো নয়।
5. **Correctness check শুধু নিজের tool-এর:** Section 6.1-এ "patch quality of AutoCodeRover and baselines" বোঝার কথা বলা হলেও text-এ শুধু ACR-এর 65.4% report হয়েছে; SWE-agent-এর correctness rate দেওয়া নেই — তাই "ACR-এর patch বেশি বিশ্বাসযোগ্য" এমন তুলনা করা যায় না।
6. **Manual check-এর bias ও leniency:** Judge হলেন authors নিজেরা (নিজের tool); inter-rater agreement (যেমন Cohen's kappa) report হয়নি; আর "৩ run-এর যেকোনো একটায় correct হলেই correct" — এটা উদার নিয়ম। কোন run-এর patch আসলে developer পেতো, তা নির্দিষ্ট নয়।
7. **Developer time তুলনা বিভ্রান্তিকর:** 2.68 দিন হলো issue খোলা থেকে PR পর্যন্ত **calendar time** (triage, অপেক্ষা, review সহ), developer-এর আসল effort নয়।
8. **Ablation অসম্পূর্ণ:** শুধু SBFL-এর ablation আছে। Stratified search বনাম single-shot/সব-একসাথে search, signature বনাম full class, retry limit, প্রতিটা API-এর অবদান — কোনোটার ablation নেই। তাই "stratified search-ই সাফল্যের কারণ" দাবিটা পরীক্ষিত নয়।
9. **একটাই LLM:** শুধু GPT-4 (0125-preview)। অন্য model বা open-source model-এ কাজ করে কিনা জানা নেই; framework-এর অবদান বনাম GPT-4-এর অবদান আলাদা করা যায় না।
10. **"Context sufficient" সিদ্ধান্তের calibration নেই:** LLM কখন থামবে তা LLM-এর আত্মবিশ্বাস-নির্ভর; কোনো confidence score, abstention ("এই issue আমি পারবো না") mechanism নেই। Reliability-র দৃষ্টিতে এটা বড় gap।
11. **Localization accuracy quantitatively মাপা হয়নি:** Taxonomy আছে, কিন্তু retrieved location-এর precision/recall (gold patch-এর method-এর তুলনায়) প্রতি run-এ মাপা নেই — অথচ paper-এর মূল দাবি localization।
12. **Contamination আলোচনা নেই:** GPT-4-এর training data-তে django/sympy-এর fix থাকতে পারে; Paper 01-এর মতো কোনো date-based check নেই।
13. **Inherited SWE-bench weakness:** দুর্বল test, underspecified issue, solution leakage (Paper 01, Section ১২.২) — সবই এখানেও প্রযোজ্য। Correctness check আংশিকভাবে এটা ধরে।
14. **Security ও code quality দেখা হয়নি:** Patch নতুন vulnerability আনছে কিনা, maintainability কেমন — মাপা হয়নি, যদিও Perspectives section-এ authors নিজেই বলেছেন LLM code "vulnerable" হতে পারে।
15. **Cost-এ hidden compute বাদ:** শুধু LLM token-এর USD; AST parsing, Docker-এ test চালানো (ACR-sbfl) ইত্যাদির খরচ ধরা হয়নি।
16. **Abstract-এর "about 4 minutes" ও Table-এর সংখ্যা:** Lite-এ @1 = 195 s (≈3.25 মিনিট), full-এ 248 s (≈4.1 মিনিট) — ছোট অসামঞ্জস্য, তবে বড় সমস্যা নয়।

---

## ১৩. Research Gaps — কোথায় কাজ করার সুযোগ আছে

| # | Gap | কেন গুরুত্বপূর্ণ | কোন folder/sub-domain-এর সাথে যুক্ত |
|---|---|---|---|
| G1 | **Automatic overfitting detection** — 27/78 plausible patch ভুল; manual check scale হয় না | Resolved ≠ correct; agent-কে বিশ্বাস করা যায় না | Patch Validation (HITL LLM-as-Judge, APCA code representation, Harden and Catch); Automated Program Repair |
| G2 | **Issue থেকে reproduction test generation** — test ছাড়া SBFL/validation সম্ভব নয় (authors-এর future work) | Leakage ছাড়া realistic SBFL ও validation | LLM Test Generation (ExecutionAgent, CoverUp, UniTSyn) |
| G3 | **Localization confidence ও abstention** — agent কখন জানে সে ভুল জায়গায় আছে? | 44.7% task-এ ভুল location; ভুল patch দেওয়ার চেয়ে "পারবো না" বলা ভালো | Trustworthy AI for SE; Coding-Agent Evaluation & Reliability (Engineering Reliable Coding Agents) |
| G4 | **Run-to-run consistency** — @1 vs @3-এর বড় পার্থক্য | Non-determinism = unreliability | Coding-Agent Evaluation & Reliability |
| G5 | **Leakage-free comparison protocol** — same model, same tests, pass@1, significance test | ছোট পার্থক্যে বড় দাবি | Coding-Agent Evaluation & Reliability (SWE-rebench) |
| G6 | **Patch-এর security/quality assurance** | Plausible patch vulnerable হতে পারে | Security of AI-Generated Code (CWEval, SecureVibeBench ইত্যাদি) |
| G7 | **Semantic program analysis দিয়ে retrieval** — call graph, data dependence, LSP (authors-এর future work) | Wrong file/location কমানো | AI Coding Agents (Paper 04 Agentless-এর সাথে তুলনা) |
| G8 | **Specification inference** — wrong patch (29.3%) কমাতে method-level intent বোঝা | Location ঠিক কিন্তু content ভুল | Trustworthy AI for SE (Proof-Carrying Code Completions); Automated Program Repair |
| G9 | **Human-in-the-loop interface** — কখন agent developer-কে জিজ্ঞাসা করবে | Authors নিজেই বলেছেন দরকার | Patch Validation (HITL); Trustworthy AI for SE |
| G10 | **Robust tool/API design** — unimplemented API-তে agent আটকে যায় | SWE-agent-এর 23 unique-এর মূল কারণ | AI Coding Agents (Paper 02 ACI-এর সাথে তুলনা) |

---

## ১৪. কী করলে আরও ভালো হবে — Improvement Ideas

(এই section-এর সব idea আমার নিজের প্রস্তাব, paper-এ নেই — শুধু যেখানে "authors-এর future work" লেখা আছে সেগুলো paper থেকে।)

1. **Leakage-free SBFL:** PR-এর test-এর বদলে LLM দিয়ে issue থেকে reproduction test বানিয়ে SBFL ও validation (authors-এর future work-এর বাস্তবায়ন), তারপর PR-এর test দিয়ে শুধু final evaluation।
2. **Overfitting detector:** Plausible patch-এর উপর (ক) অতিরিক্ত generated test, (খ) developer-patch ছাড়া LLM-as-judge, (গ) একাধিক run-এর patch-এর মধ্যে behavioral agreement — মিলিয়ে একটা "correctness confidence" score।
3. **Localization confidence:** Retrieval agent-এর প্রস্তাবিত location-এর উপর SBFL score, issue-text similarity ও multi-run agreement মিলিয়ে একটা score; threshold-এর নিচে হলে abstain বা human-কে জিজ্ঞাসা।
4. **Consistency metric:** pass@3-এর পাশাপাশি **pass^3** (তিনবারই সফল) report করা — reliability-র সরাসরি মাপ।
5. **API fallback:** Unimplemented API চাইলে কাছাকাছি valid API-তে auto-map (যেমন `search_file` → file-এর class list)।
6. **Static analysis augmentation (authors-এর future work):** Call graph (যেমন PyCG), data dependence, language server।
7. **Multi-dimensional assurance score (Paper 01-এর idea-র ধারাবাহিকতা):**
   $$\text{AssuranceScore} = w_1 \cdot \text{Plausible} + w_2 \cdot \text{CorrectnessConf} + w_3 \cdot \text{Security} + w_4 \cdot \text{Consistency}$$
8. **Ablation suite:** Stratified বনাম flat search, signature বনাম full body — framework-এর আসল অবদান মাপা।

---

## ১৫. কোন Gap-এ Research করলে ভালো Result ও Publication আসতে পারে

> ⚠️ এটা ৩টা paper-এর ভিত্তিতে প্রাথমিক মত। সব sub-domain শেষ করার পর চূড়ান্ত gap বাছাই করবো।

| Gap | SPL3-তে করা সম্ভব? | Novelty | Publication সম্ভাবনা |
|---|---|---|---|
| **G1: Overfitting/correctness detection for agent patches** (ACR-এর public patch + manual label-এর উপর) | ✅ হ্যাঁ — ACR repo-তে patch public; নিজে ছোট subset label করা যায় | উচ্চ | ⭐⭐⭐⭐⭐ |
| **G2+G1: Reproduction-test-based validation** (issue → test → validate, PR test ছাড়া) | ✅ হ্যাঁ — Lite-এর 30–50 task-এ | উচ্চ, authors নিজেই future work বলেছেন | ⭐⭐⭐⭐ |
| **G3: Localization confidence / abstention** | ✅ হ্যাঁ — mini-ACR retrieval-এর উপর | মাঝারি-উচ্চ | ⭐⭐⭐⭐ |
| **G4: Run-to-run consistency study** (pass@k বনাম pass^k) | ✅ হ্যাঁ, ছোট subset ও সস্তা model দিয়ে | মাঝারি | ⭐⭐⭐ |
| **G6: Security scan of agent patches** | ✅ হ্যাঁ — Bandit/Semgrep দিয়ে | মাঝারি-উচ্চ (Security sub-domain-এর সাথে মিলে) | ⭐⭐⭐⭐ |
| G7: Call-graph-augmented retrieval | ⚠️ সম্ভব, কিন্তু full SWE-bench-এ evaluate করা ব্যয়বহুল | মাঝারি (অনেকে কাজ করছে) | ⭐⭐ |

**সবচেয়ে ভালো combination (আমার মত):** "Plausible-to-correct gap" — ACR-এর 65.4% সংখ্যাটা একটা পরিষ্কার motivation। একটা automatic assurance layer বানানো যেটা agent-এর plausible patch-কে correct/overfitting হিসেবে classify করে, এবং ACR-এর manually-যাচাই করা patch (যদি public artifact-এ label থাকে — নিজে যাচাই করতে হবে) বা নিজেদের ছোট labeled set দিয়ে evaluate করে।

**সম্ভাব্য venue (general guidance):**
- **Conference:** ICSE, FSE, ASE, ISSTA (এই paper যেখানে published); workshop: LLM4Code, APR workshop (International Workshop on Automated Program Repair) — student-এর জন্য শুরু করার ভালো জায়গা।
- **Journal:** ACM TOSEM, IEEE TSE, EMSE, JSS, IST।

---

## ১৬. SPL3 Implementation Perspective — Software-এ কীভাবে আনবো

**Paper implement করা মানে কী?** AutoCodeRover-এর একটা ছোট, বোঝার মতো **re-implementation ("mini-ACR")** বানানো, যেটা SWE-bench Lite-এর ছোট subset-এ চলে, এবং তার উপর একটা **assurance layer** যোগ করা। (ACR-এর original code open-source — তুলনা ও reference-এর জন্য ব্যবহার করা যায়।)

**প্রস্তাবিত module:**
1. **AST Indexer:** Python-এর built-in `ast` module দিয়ে repository parse → class, method, file, line range-এর index (JSON/SQLite)।
2. **Search API layer:** Table 1-এর ৭টা API (signature output, method body, ±3 line snippet); সাথে `search_file`-এর মতো fallback (G10)।
3. **Retrieval agent:** Stratified loop — LLM-কে function calling দিয়ে API set বাছাই করতে দেওয়া; "sufficient?" প্রশ্ন; সর্বোচ্চ stratum সীমা; সব call log করা।
4. **SBFL module (ঐচ্ছিক):** `coverage.py`-এর dynamic context দিয়ে প্রতিটা test-এ কোন method চলেছে তা বের করা → Ochiai/Tarantula → top-5। (Leakage এড়াতে PR test নয়, generated reproduction test ব্যবহার — G2।)
5. **Patch agent:** Location-এর code + context → patch; `git apply --check` + linter (pyflakes/ruff) → retry ≤3।
6. **Evaluation:** Official `swebench` harness (Docker) দিয়ে F2P/P2P (Paper 01 দেখো)।
7. **Assurance layer (gap অংশ):** (ক) multi-run consistency (pass^k), (খ) generated extra test দিয়ে overfitting check, (গ) Bandit/Semgrep security scan, (ঘ) localization confidence।
8. **Dashboard:** % resolved, cost/task, cost per resolved, localization accuracy (gold patch-এর method-এর তুলনায়), taxonomy (Figure 10-এর ৫ category)।

**Practical সতর্কতা:**
- পুরো 300 task না চালিয়ে 30–50 task দিয়ে শুরু; সস্তা model দিয়ে development, শেষে শক্তিশালী model দিয়ে final run।
- Windows-এ Docker harness-এর জন্য WSL2 + Docker Desktop লাগবে (Paper 01 দেখো)।
- প্রতিটা run-এর token ও খরচ log করা — paper-এর মতো cost metric report করতে হবে।
- ৩ বার চালিয়ে variance দেখানো উচিত (paper-এর randomness threat)।

---

## ১৭. পরবর্তী গবেষণায় এই Paper-এর প্রভাব (Context)

- এই paper দেখিয়েছে যে **structured code search + সস্তা pipeline** দিয়ে SWE-agent-এর সমান ফল পাওয়া যায় — এটা "agent কতটা জটিল হওয়া দরকার" প্রশ্ন তুলেছে। **Paper 04 (Agentless)** এই প্রশ্নকে আরও এগিয়ে নিয়েছে বলে ধারণা — বিস্তারিত সেই analysis-এ দেখবো।
- Paper নিজেই জানিয়েছে ACR দ্রুত উন্নত হচ্ছিল (July 2024-এ full SWE-bench-এ 18.83%), এবং leaderboard-এ তখন 17-এর বেশি entry।
- **Plausible বনাম correct** আলাদা করে report করার প্রথা — পরে SWE-bench Verified (Paper 01, Section ১৭) ও patch validation-এর কাজগুলো (আমাদের Patch Validation folder) একই সমস্যার দিকে নজর দিয়েছে।
- Issue reproduction test generation — authors-এর future work — পরের agent ও test-generation কাজে গুরুত্বপূর্ণ দিক হয়েছে বলে সাধারণভাবে দেখা যায়; আমাদের *LLM Test Generation* folder-এর paper পড়ে নিশ্চিত হবো।
- Authors-এর Perspectives: ভবিষ্যতে focus **"scale" থেকে "trust"**-এর দিকে সরবে — এটা হুবহু আমাদের domain-এর (Reliability and Assurance) motivation।

---

## ১৮. Supervisor-এর সম্ভাব্য প্রশ্ন ও উত্তর (Viva Prep)

**Q1. AutoCodeRover আর SWE-agent-এর মূল পার্থক্য কী?**
A: SWE-agent LLM-কে shell-ধরনের file command (open, scroll, edit) দেয় — codebase-কে file-এর collection হিসেবে দেখে। AutoCodeRover AST-ভিত্তিক class/method-level search API দেয়, stratified iterative search করে, retrieval ও patch generation আলাদা agent-এ রাখে, এবং test থাকলে SBFL ব্যবহার করে। ফলে কম token খরচ (37k বনাম 245k) এবং Lite-এ সমান/সামান্য ভালো ফল (19% বনাম 18%)।

**Q2. Stratified search কেন? সব API একসাথে বা একটা একটা করে ডাকলে সমস্যা কী?**
A: একটা call অসম্পূর্ণ context দেয় (django-13230-এ শুধু `add_item` দেখে LLM থেমে যেতে পারে); সব একসাথে ডাকলে context বিশাল হয়ে LLM বিভ্রান্ত হয় বা context window ছাড়ায়। Stratified search প্রতিটা স্তরে শুধু দরকারি একাধিক call করে, আর আগের ফল থেকে নতুন নাম নিয়ে পরের স্তরে যায়। তবে এটার আলাদা ablation paper-এ নেই।

**Q3. SBFL কীভাবে কাজ করে? সূত্রটা বলো।**
A: Failing test-এ বেশি আর passing test-এ কম execute হওয়া method বেশি suspicious। Ochiai $= e_f/\sqrt{N_F (e_f + e_p)}$। যেমন ২টা failing test-এর দুটোই একটা method-কে ছোঁয়, আর ৩টা passing-এর ১টা ছোঁয় → $2/\sqrt{2 \times 3} \approx 0.816$। Paper কোন formula ব্যবহার করেছে তা লেখেনি — শুধু Tarantula/Ochiai উদাহরণ দিয়েছে, method-level, top-5।

**Q4. SBFL-এর ফল সরাসরি patch location হিসেবে নেয়নি কেন?**
A: SBFL-এর accuracy test-suite-এর quality-র উপর নির্ভর করে। তাই এটা শুধু অতিরিক্ত hint — LLM issue text-এর সাথে মিলিয়ে নেয়। django-13964-এ agent top-1 নয়, 3rd ও 5th বেছেছে, আর 3rd-টাই ছিল developer-এর fix location।

**Q5. 19% → 22% (SBFL) উন্নতিটা কি পুরোপুরি বিশ্বাসযোগ্য?**
A: পুরোপুরি নয়। RQ2-তে SWE-bench-এর developer-written test ব্যবহার হয়েছে, এবং সেই test দিয়ে patch validation loop-ও চালানো হয়েছে। Evaluation-ও একই ধরনের test দিয়ে হয় — তাই এটা প্রায় oracle access; বাস্তবে fix-এর আগে এই test থাকে না। Authors নিজেও বলেছেন scenario-টা "not always practical"। ন্যায্য তুলনার জন্য issue থেকে generated reproduction test দিয়ে SBFL চালানো উচিত।

**Q6. "Plausible" আর "correct" patch-এর পার্থক্য কী, আর paper-এ সংখ্যা কত?**
A: Plausible = test pass করে; correct = developer patch-এর সাথে semantically equivalent। ACR @3-এর 78টা plausible-এর 51টা correct (65.4%), 27টা overfitting — যার 25টা সঠিক method-এই পরিবর্তন করেছে। অর্থাৎ সত্যিকারের correct fix-এর হার 51/300 = 17%, 26% নয়।

**Q7. Devin-এর চেয়ে ভালো — এই দাবি কতটা শক্ত?**
A: দুর্বল। Devin subset-এ ACR @1 = 12.63%, Devin = 13.86%, SWE-agent = 13.51% — @1-এ ACR পিছিয়ে। শুধু @3-এ (তিনবার চেষ্টা, তিনগুণ খরচ) ACR 18.77%। তাছাড়া Devin-এর সংখ্যা তাদের report থেকে নেওয়া, ACR team নিজে চালায়নি।

**Q8. ACR কোথায় সবচেয়ে বেশি ব্যর্থ হয়?**
A: Figure 10: 29.3% wrong patch (location ঠিক, content ভুল), 20.0% সঠিক file-এ ভুল location, 18.0% ভুল file, 6.7% no patch। অর্থাৎ 44.7% task-এ localization ব্যর্থ। যেসব issue-তে code entity-র নাম কম, সেখানে বেশি ব্যর্থ।

**Q9. 2.68 দিন বনাম 4 মিনিট — এই তুলনা কি ঠিক?**
A: সাবধানে নিতে হবে। 2.68 দিন issue খোলা থেকে PR তৈরি পর্যন্ত calendar time (78-এর মধ্যে 66টার গড়), developer-এর আসল কাজের সময় নয়। আর tool-এর মাত্র ~65% plausible patch correct — তাই developer-কে তবু review করতে হবে।

**Q10. ACR আর SWE-agent-এর overlap থেকে কী শেখা যায়?**
A: Common মাত্র 31; ACR-এর unique 26, SWE-agent-এর 23; union 80 (26.7%)। দুটো design আলাদা ধরনের task-এ ভালো — ensemble বা কোন task-এ কোন agent, সেই routing-এর সুযোগ আছে।

**Q11. এই paper তোমার SPL3-তে কীভাবে কাজে লাগবে?**
A: (১) mini-ACR (AST index + ৭ API + stratified loop + patch retry) বানিয়ে Lite-এর ছোট subset-এ চালানো; (২) assurance layer — reproduction test দিয়ে leakage-free validation, overfitting detection, consistency (pass^k), security scan; (৩) plausible-to-correct gap মাপা।

**Q12. Temperature 0.2 দিলেও ৩ বার চালাতে হলো কেন?**
A: Temperature 0.2-তেও GPT-4-এর output পুরো deterministic নয়, আর agent loop-এ ছোট পার্থক্য পরের সিদ্ধান্তে বড় হয়ে যায়। 19% (@1) বনাম 26% (@3)-এর পার্থক্যই দেখায় non-determinism অনেক — reliability-র জন্য এটা একটা মূল সমস্যা।

---

## ১৯. Glossary (দ্রুত মনে রাখার জন্য)

| Term | অর্থ |
|---|---|
| AST | Source code-এর tree representation (class → method → statement) |
| Class signature | Class-এর নাম ও method-এর নাম/parameter, body ছাড়া |
| Code search API | LLM যে function ডেকে codebase থেকে class/method/snippet আনে |
| Hint | Issue-তে উল্লেখিত class/method/file নাম বা code snippet |
| Stratum / Strata | Stratified search-এর একেকটা স্তর |
| Stratified search | স্তরে স্তরে, প্রতিবার শুধু দরকারি একাধিক API call |
| Iterative search | আগের ফল থেকে পাওয়া নাম দিয়ে পরের search |
| Buggy location | Retrieval agent-এর ঠিক করা fix-এর জায়গা (file, class, method) |
| Fault localization (FL) | Bug কোথায় তা খোঁজা |
| SBFL | Test coverage-এর পার্থক্য দিয়ে suspiciousness score |
| Ochiai / Tarantula | দুটো জনপ্রিয় SBFL formula |
| Program spectrum | কোন test-এ program-এর কোন অংশ চলেছে তার হিসাব |
| Plausible patch | Test pass করে |
| Correct patch | Developer patch-এর সাথে semantically equivalent |
| Overfitting patch | Test pass করে কিন্তু intent মানে না |
| Program improvement | Bug fix + feature addition |
| Retry loop | Patch format/apply/lint/test fail হলে আবার patch লেখা |
| Linter | Code না চালিয়ে syntax/style ভুল ধরার tool |
| ACR @1 / @3 | এক run-এর ফল / তিন run-এর যেকোনোটায় সফল |
| ACR-sbfl | SBFL hint + test validation সহ setting |
| Issue reproducer | Issue থেকে bug-দেখানো test তৈরি |
| Devin | Cognition Labs-এর closed-source AI software engineer |

---

## ২০. এক নজরে সারাংশ (Summary Card)

| | |
|---|---|
| **Problem** | LLM agent-রা codebase-কে file-এর গাদা হিসেবে দেখে; localization কঠিন; খরচ বেশি; patch correctness report হয় না |
| **Solution** | AutoCodeRover — AST-ভিত্তিক ৭টা code search API + stratified iterative context retrieval + আলাদা patch agent (retry ≤3) + ঐচ্ছিক SBFL (top-5) ও test validation |
| **Model** | GPT-4 (gpt-4-0125-preview), temperature 0.2, ৩ বার run |
| **Key result** | Lite: 19% (@1), 26% (@3), 22% (sbfl); SWE-agent 18%। Full: 12.42% (@1), 17.96% (@3); SWE-agent 12.47% |
| **Cost** | 0.43 USD ও 195 s প্রতি task (Lite @1) বনাম SWE-agent 2.51 USD |
| **Correctness** | 78 plausible-এর 51 correct = 65.4%; 25/27 overfitting সঠিক method-এ |
| **Failure** | Wrong patch 29.3%, wrong location 20.0%, wrong file 18.0%, no patch 6.7% |
| **Key insight** | Program structure + SE analysis tool + LLM = সস্তা ও কার্যকর; কিন্তু plausible ≠ correct |
| **Main limitation** | SBFL-এ evaluation test leakage-এর ঝুঁকি, pass@3 দিয়ে তুলনা, statistical test নেই, শুধু GPT-4, নিজের tool-এর manual check |
| **আমাদের জন্য gap** | Automatic overfitting detection, leakage-free reproduction-test validation, localization confidence, run-to-run consistency |

---

## ২১. বর্তমান (2026) প্রেক্ষাপট — আজকের Model ও Agent-দের সাথে তুলনা

> **উৎস:** সব current-state তথ্য `00_Current_State_2026_Sources.md` (compiled 2026-10-28) থেকে; প্রতিটা সংখ্যা **vendor-reported** নাকি **independent** তা লেখা আছে, আর fact sheet-এ "search-snippet only" চিহ্নিত তথ্য এখানেও চিহ্নিত। Benchmark saturation-এর সাধারণ আলোচনা **Paper 01, Section ২১**-এ, scaffold ও variance-এর আলোচনা **Paper 02, Section ২১**-এ। এখানে AutoCodeRover-এর তিনটা নিজস্ব প্রশ্নে focus: (১) localization, (২) plausible বনাম correct (65.4%), (৩) test/oracle access ও খরচ।

### ২১.১ Paper-এর সময় বনাম এখন

| দিক | Paper-এ (2024, ISSTA) | এখন, October 2026 | উৎস |
|---|---|---|---|
| Resolve rate | GPT-4 দিয়ে Lite 19% (@1), 26% (@3); full 12.42% | Lite আর কেউ report করে না (শেষ official Lite entry 2025-09-11, top 60.33%); Verified-এ top 97.0% (independent) | SWE-bench leaderboards.json; Vals.ai Sept 2026 |
| AutoCodeRover-এর নিজের বর্তমান অবস্থা | Open-source, active | **বর্তমান model-এর জন্য তথ্য পাওয়া যায়নি** — fact sheet-এ ACR-এর কোনো 2026 entry বা release নেই | — |
| Plausible বনাম correct | 78 plausible-এর 51 correct = 65.4% (manual, authors নিজে) | PatchDiff (ICSE 2026): plausible patch-এর **29.6%** gold patch থেকে ভিন্ন আচরণ করে; "correct" patch-এর 7.8% পুরো developer test suite-এ fail (independent, 2025 model) | arXiv 2503.15223 |
| Test-এর দুর্বলতার মাত্রা | Paper: issue description ও test দুটোই incomplete specification | SWE-Bench Pro-তে OpenAI-এর audit: 27.4% (automated + Codex review) থেকে 34.1% (5 জন মানুষ) task broken, যার একটা category "low-coverage tests let incomplete fixes pass" | the-decoder (secondary; OpenAI-এর মূল post fact sheet-এ পৌঁছানো যায়নি) |
| Oracle/test access | ACR-sbfl developer test দিয়ে SBFL ও validation চালায় (Section ১২.২ critique #1) | SWE-Bench Pro Verified: agent `.git` history, local file, network ও metadata — চার channel দিয়ে উত্তর পায়; GLM-5.2 78.80% থেকে safeguard দিলে 57.32% (independent) | arXiv 2609.08149 |
| প্রতি task খরচ | ACR @1 USD 0.43, SWE-agent USD 2.51 (Lite) | SWE-rebench-এ USD 0.81–4.40 per problem; Verified-এ USD 0.10–2.05 per test (দুটোই independent) | swe-rebench.com; Vals.ai |
| Model-এর দাম | GPT-4 (paper-এর implied ≈ 11.6 USD per million token, আমার হিসাব) | Opus 5.5: USD 4 input / USD 20 output per million (search-snippet only); GPT-6.1 Terra: USD 1 / USD 5 (vendor) | llm-stats (snippet); OpenAI X post |
| Patch-এর বাস্তব গ্রহণযোগ্যতা | Developer-এর 2.68 দিনের সাথে তুলনা | ~33k agent PR-এ (Codex, Copilot, Devin, Cursor, Claude Code) bug-fix PR সবচেয়ে কম merge হয় (MSR 2026, independent); fix-related PR-এ Claude Code 57.4% (n=115), Codex 81.6% (search-snippet only) | arXiv 2601.15195; arXiv 2602.00164 |

**আমার পর্যবেক্ষণ:** ACR-এর 65.4% আর PatchDiff-এর 29.6% একই জিনিস মাপে না — ACR "semantically equivalent to developer patch" হাতে যাচাই করেছে; PatchDiff differential testing দিয়ে "আচরণ ভিন্ন" মেপেছে। তবু দিক একই: test-pass করা patch-এর মোটামুটি এক-তৃতীয়াংশ নিয়ে সন্দেহ থেকে যায় ($1 - 0.654 = 0.346$ বনাম $0.296$)।

### ২১.২ কোন Finding এখনো সত্য, কোনটা পুরনো হয়ে গেছে

- **এখনো সত্য — "Plausible ≠ Correct" (Key Finding ৬, paper-এর সবচেয়ে গুরুত্বপূর্ণ অবদান):** PatchDiff 29.6%; OpenAI-এর audit-এ low-coverage test; agent PR-এ bug-fix PR সবচেয়ে কম merge হয়। কিন্তু এই সব প্রমাণ 2025-এর model বা AIDev dataset-এর 2025 agent-এর উপর — **Opus 5.5 বা GPT-6-generation agent-এর patch-এ plausible-to-correct হার কেউ মাপেনি** (fact sheet স্পষ্টভাবে বলছে)।
- **এখনো সত্য, অন্য নামে — "Issue description-ও incomplete specification":** SWE-Bench Pro Verified 102টা task ঠিক করেছে, তার 22টা misleading description আর 75টা overly narrow test (independent)। ACR-এর overfitting কারণ #2–#3 (reporter-এর preliminary patch, একটা নির্দিষ্ট case) ঠিক এই ধরনের।
- **উল্টো দিকে আরও সত্য — ACR-sbfl-এর "oracle access" নিয়ে আমার critique (Section ১২.২ #1):** 2024-এ এটা ছিল design-এর প্রশ্ন; 2026-এ agent নিজেই oracle খুঁজে নেয় — DeepSWE-এর cheating trial-এর 87% (38-এর মধ্যে 33) `.git` history থেকে gold commit পড়েছে (search-snippet only); Opus 5.5 transcript-এ "hidden tests … written by the benchmark creators" নিয়ে reasoning (vendor)। অর্থাৎ evaluation test-কে agent থেকে আলাদা রাখা এখন আরও জরুরি।
- **সম্ভবত পুরনো — "খরচ কমানোই বড় সুবিধা" (USD 0.43 বনাম 2.51):** এখন cheapest model-এ Verified-এ USD 0.10 per test (DeepSeek V4 Pro, Vals); আর vendor-রা দাম কমাচ্ছে (Opus 5.5 "40% less to run than Opus 5", vendor)। **আমার পর্যবেক্ষণ:** token-সাশ্রয়ী design-এর সুবিধা এখন model বাছাইয়ের তুলনায় ছোট; তবে long-horizon task-এ খরচ আবার বেড়েছে (Terminal-Bench 4.0-এ Opus 5.5 USD 13.20 per test, Vals)।
- **অজানা — "Localization-ই আসল খেলা" (44.7% task-এ ভুল location):** বর্তমান agent-এর file/function-level localization accuracy-র কোনো সংখ্যা fact sheet-এ **পাওয়া যায়নি**। Saturated benchmark-এ localization আর bottleneck না হলেও, কঠিন benchmark-এ (SWE-Bench Pro public board-এ top 61.50%, Scale, independent) failure-এর কারণ বিশ্লেষণ পাওয়া যায়নি।
- **অজানা — SBFL বা program-analysis tool বর্তমান agent-এ কাজে লাগে কিনা:** Fact sheet-এ এ নিয়ে কোনো তথ্য নেই।

### ২১.৩ এই Paper-এর Gap-গুলো আজও খোলা কিনা

| Gap | 2026-এ অবস্থা | প্রমাণ |
|---|---|---|
| G1 / CG1: Automatic overfitting detection | **খোলা** | LLM judge-এর plain baseline overfitting filter-এ মাত্র 62.14% accuracy, learned method ComPass 88.35% (search-snippet only); execution-calibrated study-তে over-fix flag-এর precision 5–10%, "no single judge trustworthy on real Java code" (search-snippet only); বর্তমান-generation agent patch-এ LLM-judge validation **পাওয়া যায়নি** |
| G2 / CG3: Issue থেকে reproduction test | **খোলা** | SWT-bench ও TDD-Bench-এ Opus 5.5, GPT-6, Gemini 4-এর result **পাওয়া যায়নি**; "Rethinking the Value of Agent-Generated Tests": test লেখা issue resolution-এ সামান্যই সাহায্য করে (search-snippet only); Fable 5.1 "নিজের test লিখে কাজ যাচাই করতে পারে" — শুধু vendor-এর qualitative দাবি |
| G3 / CG7: Localization confidence ও abstention | **আংশিক (শুধু vendor দাবি)** | Fable 5.1 আটকে গেলে "says so when stuck" (AWS blog, vendor, qualitative); কোনো independent abstention metric পাওয়া যায়নি |
| G4 / CG4: Run-to-run consistency | **খোলা** | SWE-rebench pass@1–pass@5 gap 12–18 point (independent); ACR-এর @1–@3 gap ছিল 7 point (19 → 26) |
| G5 / CG8: Leakage-free, fair comparison protocol | **খোলা, তবে পদ্ধতি এসেছে** | SWE-Bench Pro Verified-এর anti-hacking safeguard; "Coding Agents Have Converged": McNemar test-এ 29টা adjacent pair-এর 0টা আলাদা; vendor (Opus 5.5 SWE-bench Pro 89.9%) বনাম Scale-এর harness-normalised board (top 61.50%) — বড় ফাঁক |
| G6 / CG5: Security/quality assurance | **খোলা** | SusVibes: SWE-agent + Claude 4 Sonnet secure মাত্র 11.8%; বর্তমান model-এর তথ্য পাওয়া যায়নি; "Merged, Not Measured": performance fix measurement ছাড়াই merge হয় (title only) |
| G7: Semantic program analysis দিয়ে retrieval | **বর্তমান model-এর জন্য তথ্য পাওয়া যায়নি** | — |
| G8: Specification inference | **বর্তমান model-এর জন্য তথ্য পাওয়া যায়নি** | — |
| G9: Human-in-the-loop interface | **আংশিক** | Agent PR-এর rejection কারণে "lack of reviewer engagement" ও "agent misalignment" (MSR 2026, independent) — মানুষ-agent যোগাযোগ এখনো দুর্বল |
| CG12: Assurance signal-এর gaming | **খোলা, নতুন প্রমাণ** | ACR-sbfl-এর মতো test-feedback loop এখন reward-hacking-এর পথ: Opus 5.5 successful hack 0.046% (training-time, vendor, self-measured); GPT-6.1 Sol-এ GPT-6 Astra-র চেয়ে বেশি reward-hacking flag (vendor); কোনো independent audit পাওয়া যায়নি |

### ২১.৪ বর্তমান Model দিয়ে আবার পরীক্ষা করলে — SPL3 Idea

1. **"65.4% in 2026" — plausible-to-correct re-measurement:** একটা current cheap model + mini-SWE-agent দিয়ে SWE-rebench-এর সর্বশেষ window-এর 30–40টা task; resolved patch-গুলো ACR-এর মতো দুজন মিলে manually label (semantic equivalence) + PatchDiff-ধাঁচের differential test। Inter-rater agreement (Cohen's kappa) report করবো — ACR-এর যে দুর্বলতা ছিল। **Gap:** CG1 — বর্তমান model-এ এই সংখ্যা fact sheet অনুযায়ী কেউ মাপেনি; ছোট sample হলেও এটা নতুন তথ্য।
2. **Leakage-free SBFL:** ACR-এর Section ১৪-এর idea #1 — PR test-এর বদলে agent-generated reproduction test দিয়ে SBFL, container-এ `.git` history সরিয়ে। **Gap:** CG3 + CG12 — oracle access ছাড়া SBFL আদৌ সাহায্য করে কিনা।
3. **Localization probe (প্রায় বিনা খরচে):** Current agent-এর trajectory থেকে প্রথম কোন file/method খোলা হয়েছে তা gold patch-এর method-এর সাথে মিলিয়ে precision/recall; ACR-এর Figure 10-এর ৫ category-তে ভাগ করা। **Gap:** বর্তমান agent-এর localization accuracy-র কোনো public সংখ্যা নেই।
4. **LLM-judge-এর calibration on agent patches:** Idea 1-এর manual label-কে ground truth ধরে একটা LLM judge-এর accuracy মাপা। **Gap:** CG10 — fact sheet স্পষ্ট বলছে Opus 5.5/GPT-6-generation agent patch-এ LLM-judge validation study পাওয়া যায়নি; ComPass-এর 62.14% (snippet) baseline-এর সাথে তুলনা করা যাবে।
5. **Cost per correct fix:** Section ৬.৬-এর CPR metric-কে "cost per **correct** fix"-এ বাড়ানো: মোট খরচ ÷ manually-correct patch। **আমার পর্যবেক্ষণ:** ACR-এর সংখ্যায় এটা $\frac{390}{51} \approx 7.6$ USD (@3); 2026-এর সংখ্যা নিজের run থেকে বের করতে হবে। **Gap:** CG8 — resolved-ভিত্তিক cost metric patch quality লুকায়।

### ২১.৫ Supervisor-এর সম্ভাব্য প্রশ্ন (2026 প্রসঙ্গে)

**Q1. 65.4% correctness 2024-এর GPT-4-এর সংখ্যা। এখনকার model কি এই সমস্যা সমাধান করে ফেলেছে?**
A: জানা নেই — আর সেটাই gap। সর্বশেষ independent প্রমাণ PatchDiff (29.6% plausible patch ভিন্ন আচরণ করে), কিন্তু সেটা 2025-এর model-এ। Fact sheet স্পষ্ট বলছে বর্তমান model-এ re-run পাওয়া যায়নি। তার উপর benchmark-এর test নিজেই দুর্বল (SWE-Bench Pro-তে 27–34% task broken), তাই resolved rate বাড়লেও correctness বেড়েছে কিনা বলা যায় না।

**Q2. ACR-sbfl-এ evaluation test ব্যবহার নিয়ে তোমার আপত্তি কি এখনো প্রাসঙ্গিক?**
A: আরও বেশি প্রাসঙ্গিক। এখন agent নিজেই oracle খুঁজে নেয় — `.git` history থেকে gold patch পড়া, scorer-এ logging inject করা (METR, আগের generation)। SWE-Bench Pro Verified দেখিয়েছে leakage বন্ধ করলে GLM-5.2-এর score 78.80% থেকে 57.32%-এ নামে। তাই যেকোনো test-feedback design-এ evaluation oracle আলাদা রাখা আর leakage channel বন্ধ করা এখন minimum requirement।

**Q3. Structured, AST-ভিত্তিক search এর idea কি এখনো কাজের?**
A: সম্ভবত, কিন্তু প্রমাণ নেই। এখনকার standard harness mini-SWE-agent bash-only, আর fact sheet-এ program-analysis-augmented retrieval বা localization accuracy নিয়ে বর্তমান model-এর কোনো তথ্য নেই। আমার SPL3-এ trajectory থেকে localization মাপার idea (২১.৪-এর #3) দিয়ে এই প্রশ্নের একটা ছোট উত্তর দেওয়া যায়।
