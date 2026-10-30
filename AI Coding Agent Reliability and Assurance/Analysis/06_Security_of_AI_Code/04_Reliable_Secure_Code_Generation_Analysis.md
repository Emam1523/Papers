# Paper Analysis 04 (Security): Enhancing Reliability in LLM-Based Secure Code Generation

> Sub-domain: Security of AI-Generated Code
> PDF: Security of AI-Generated Code/Enhancing Reliability in LLM-Based Secure Code Generation.pdf

## ০. Bibliographic info

| Field | Detail |
|---|---|
| Title | Enhancing Reliability in LLM-Based Secure Code Generation |
| Authors | Mohammed F. Kharma, Mohammad Alkhanafseh, Ahmed Sabbah, David Mohaisen (Senior Member, IEEE) |
| Affiliation | Birzeit University (Palestine); Mohaisen এছাড়া University of Central Florida |
| Identifier | arXiv:2605.24300v1 [cs.CR], ২২ May ২০২৬ |
| Venue | Paper-এ কোনো journal/conference-এর নাম নেই (শুধু arXiv preprint, IEEE-style format); venue stated নয় |
| Method নাম | MA-CoT (Mitigation-Aware Chain-of-Thought) |
| Models | gpt-5-2025-08-07, claude-sonnet-4-5-20250929, gemini-2.5-pro |
| Languages | C, Java, Python |
| Datasets | ২০০-task primary dataset (লেখকদের আগের কাজ থেকে) + LLMSecEval (১৫০ prompt) |
| Analyzer | SonarQube (SAST) + দুইজন security researcher-এর expert review |
| Code/data | "GitHub"-এ available বলা আছে (URL টেক্সটে পাওয়া যায়নি) |
| আগের কাজ | WA-CoT (Weaknesses-Aware CoT), ref [17], Empirical Software Engineering-এ submitted; dataset ref [37], IEEE TDSC ২০২৬ |

## ১. TL;DR

- Paper একটি **prompt-level** পদ্ধতি দেয়: MA-CoT। Prompt-এ তিনটি জিনিস ঢোকানো হয়: (ক) সব task-এর জন্য baseline security rule, (খ) task-এর security domain অনুযায়ী CWE-ভিত্তিক **mitigation** (কী করতে হবে, শুধু কোন দুর্বলতা আছে তা নয়), (গ) language-specific checklist।
- ৩টি LLM × ৩টি language × ৪টি prompt strategy (Vanilla, Zero-shot, CoT, MA-CoT) × ২০০ task = ৭,২০০ program, প্রতি combination-এ **একটি মাত্র sample**।
- Primary dataset-এ মোট SonarQube finding ৯২ থেকে ৩৯ (৫৭.৬% কমেছে); Blocker+Critical ৯০ থেকে ৩৯ (৫৬.৭%)। LLMSecEval-এ ৭৩ থেকে ৪ (৯৪.৫%); high-severity ৪৫ থেকে ২ (৯৫.৬%)।
- Zero-shot ("Write secure code") এবং generic CoT অনেক ক্ষেত্রে Vanilla-র চেয়ে খারাপ; বিশেষ করে C-তে।
- Paper-এর দ্বিতীয় অবদান: vulnerability-র কারণকে "language-core" বনাম "language-stack" (library, OS, toolchain, application logic) স্তরে ভাগ করা।
- **আমাদের জন্য মূল কথা:** paper-এ কোনো verification loop নেই, কোনো repeated run নেই, কোনো statistical test নেই, functional correctness-এর ফলাফলও report করা হয়নি। অর্থাৎ "reliability" এখানে মানে "finding কম", "run-to-run স্থিতিশীলতা" নয়। তবু paper-এর per-category reporting, severity shift বিশ্লেষণ ও layered attribution আমাদের assurance report-এ কাজে লাগানো যায়।

**Supervisor-কে ৩০ সেকেন্ডে:** "এই paper দেখায় যে security prompt-এ সাধারণ 'be secure' নির্দেশ কাজ করে না, বরং task-নির্দিষ্ট mitigation দিলে SonarQube finding প্রায় অর্ধেক (৯২ থেকে ৩৯) হয়। কিন্তু প্রতিটি cell-এ একটাই sample, একটাই static analyzer, কোনো functional test result নেই, আর mitigation checklist-টা SonarQube-র rule-এর সাথেই মিলে যায়। তাই এটা আমাদের কাছে একটি ভালো generation-side technique এবং একই সাথে 'security signal কতটা নির্ভরযোগ্য' প্রশ্নের একটি দুর্বল উদাহরণ।"

## ২. Background (শুধু এই project-এ নতুন ধারণা)

- **SAST (Static Application Security Testing):** program না চালিয়ে source code-এ pattern/rule মিলিয়ে দুর্বলতা খোঁজা। এখানে SonarQube। এটি exploitability প্রমাণ করে না (paper নিজেই construct threat হিসেবে বলেছে)।
- **SonarQube severity:** চারটি স্তর: Blocker, Critical, Major, Minor। Paper "high-severity" বলতে Blocker+Critical বোঝায়।
- **CWE (Common Weakness Enumeration):** MITRE-র দুর্বলতার ধরন-তালিকা। উদাহরণ: CWE-295 (Improper Certificate Validation), CWE-327 (Broken/Risky Crypto Algorithm), CWE-367 (TOCTOU race), CWE-14 (compiler কর্তৃক buffer-clear বাদ পড়া), CWE-259 (hard-coded password), CWE-600 (uncaught exception), CWE-79 (XSS), CWE-611 (XXE), CWE-119/120 (buffer error), CWE-20 (input validation), CWE-521 (weak password policy)।
- **TOCTOU:** "check" ও "use"-এর মাঝে অবস্থা বদলে যাওয়ার race (যেমন file আছে কিনা দেখে তারপর খোলা)।
- **AEAD:** authenticated encryption (AES-GCM, ChaCha20-Poly1305)। **Argon2id:** password-based key derivation।
- **CoT (Chain-of-Thought):** ধাপে ধাপে যুক্তি করার prompt। Paper-এর CoT: (১) requirement বোঝো, (২) security বিবেচনা চিহ্নিত করো, (৩) নিরাপদে implement করো, (৪) correctness verify করো।
- **WA-CoT বনাম MA-CoT:** WA-CoT শুধু CWE নাম ও বর্ণনা দিত; MA-CoT দেয় সংক্ষিপ্ত, করণীয়-ভিত্তিক countermeasure।
- **Layered attribution:** কোনো finding language-এর নিজস্ব বৈশিষ্ট্য (language-core) নাকি তার চারপাশের stack-এর (standard library, ecosystem library, OS/platform API, toolchain, application logic) দোষ, তা ভাগ করার নিয়ম (Table II)।
- **LLMSecEval:** CWE Top 25-ভিত্তিক ১৫০টি natural-language prompt, প্রতিটির সাথে secure reference solution; C ও Python থেকে তৈরি বলে paper বলেছে।

## ৩. Problem

1. LLM-generated code-এ security দুর্বলতা বারবার আসে (Copilot-এর scenario-র প্রায় ৪০% insecure, Pearce et al.), এবং model বড় হলেও কমে না (Fu et al.)।
2. Prompt engineering সাধারণত functional correctness বাড়ায়; security "incidental"। "Write secure code" খুব অস্পষ্ট।
3. লেখকদের আগের WA-CoT-এর চারটি সীমাবদ্ধতা: (ক) information overload (বড় CWE catalog), (খ) coarse integration (remediation step ছাড়া শুধু CWE id), (গ) language agnosticism, (ঘ) model দুর্বলতা চিনলেও code synthesis-এর সময় প্রয়োগ করে না।
4. Language-based তুলনায় "language feature" শব্দটি বিভ্রান্তিকর: অনেক দুর্বলতা language নয়, তার library/OS/toolchain-এর।

## ৪. Goal ও Research Questions

- **Goal:** lightweight, inference-time (fine-tuning ছাড়া) prompt পদ্ধতি যা model, language ও dataset বদলালেও security outcome স্থিতিশীলভাবে ভালো করে।
- **RQ1:** Targeted CWE-based mitigation কি standard prompting-এর তুলনায় vulnerability-র severity কমায়?
- **RQ2:** Programming language-এর বৈশিষ্ট্য mitigation-aware prompting-এর কার্যকারিতাকে কীভাবে প্রভাবিত করে?
- **RQ3:** Model-গুলোর মধ্যে কী vulnerability pattern দেখা যায়, এবং তা কীভাবে model-specific security-তে কাজে লাগে?
- **পাঁচটি contribution:** MA-CoT; ৭,২০০ program-এর empirical study; severity/CWE metrics; open benchmark ও artifact; layered attribution ও hardening guidance।

## ৫. Methodology (ধাপে ধাপে)

### ৫.১ MA-CoT pipeline (Figure 1)

1. **Stage 1: Task analysis ও domain classification।** LLM-ভিত্তিক semantic analysis দিয়ে task-কে এক বা একাধিক security domain-এ ফেলা হয়। Domain তালিকা (paper যে ৭টি functional category দিয়েছে সেগুলো): Secure Coding; Data Structures and Algorithms; Parsing and Validation; Networking; Mathematics and Logic; Programming Systems and Utilities; Concurrency and Synchronization। কোন LLM এই classification করেছে তা paper-এ বলা নেই।
2. **Stage 2: Mitigation retrieval।** চিহ্নিত domain-এর জন্য "code-security weakness mitigation dataset" থেকে mitigation আনা হয়। উদাহরণ: authentication task-এ Weak Password Requirements-এর mitigation (শক্ত password policy, hashing ও salting)।
3. **Stage 3: Prompt construction।** তিনটি অংশ জোড়া লাগে: (১) সব code-এর জন্য baseline security principle, (২) mitigation strategy, (৩) task ও language-এর জন্য নির্দিষ্ট checklist।

উদাহরণ নির্দেশ: crypto task-এ AES-256-GCM (AEAD), Argon2id key derivation (কমপক্ষে ১২৮-bit salt), CSPRNG দিয়ে nonce; C-তে pointer initialization, bounds check ও explicit memory clearing; Python-এ input sanitization, safe deserialization, exception handling।

### ৫.২ Mitigation-Aware dataset

প্রতিটি record-এ চারটি অংশ: General Rules; Language-Specific Guidelines (C, C++, Python, Java); Code Review Checklist; কিছু Fine-tuning Example (instruction, insecure input, secure output)। Record সংখ্যা paper-এ বলা নেই। Appendix-এ দুটি example: "Language Basics" ও "Cryptography" (যেমন MD5, SHA-1, DES/3DES, RC4, ECB নিষিদ্ধ; TLS 1.2/1.3 ও certificate verification বাধ্যতামূলক)।

### ৫.৩ Baseline prompt (তুলনার জন্য)

- **Vanilla:** শুধু task description।
- **Zero-shot:** "Write secure code for the following task"।
- **CoT:** চার ধাপের reasoning (ওপরে দেখো)।
- **MA-CoT:** security signal reasoning-এর ভেতরে (baseline rule + task mitigation + language checklist); "code generate হওয়ার পর ঠিক করা" নয়, বরং reasoning-এর সময় দুর্বলতা সামনে আনা।

### ৫.৪ Generation ও evaluation

- প্রতিটি (LLM, language, method, task) এর জন্য **একটি** code sample: ৩ × ৩ × ৪ × ২০০ = ৭,২০০।
- Output থেকে code বের করে compile/syntax-check করা হয়, metadata (model, language, method, task ID) সহ সংরক্ষণ।
- SonarQube প্রতিটি sample-এ vulnerability ও severity দেয়; finding CWE-তে map করা হয়।
- দুইজন security researcher স্বাধীনভাবে SonarQube finding review করে ও মতভেদ consensus-এ মেটায় (agreement metric report করা হয়নি)।
- External validation: LLMSecEval (১৫০ task) একই pipeline-এ।

### ৫.৫ Layered attribution পদ্ধতি (Table II)

প্রতিটি finding-কে standardized field (language_feature, feature_category, feature_mechanism, comparative_analysis) দিয়ে **একটি primary layer** দেওয়া হয়। একাধিক layer সম্ভব হলে "সবচেয়ে নিচের layer যা ঝুঁকি তৈরির জন্য প্রয়োজন" নিয়ম। Layer-গুলো: language-core (strict); standard runtime/library; ecosystem library/framework; platform/OS API; toolchain/optimization; application security logic/policy।

Attribution কে বা কোন প্রক্রিয়ায় করেছে (মানুষ নাকি LLM) paper-এ স্পষ্ট নয়।

## ৬. Math

Paper-এ কোনো statistical formula নেই; সব মান count ও percentage। নিচে paper-এর metric-গুলোর formalisation এবং আমার যোগ করা কয়েকটি হিসাব।

### ৬.১ Sample সংখ্যা

$$N = |\mathcal{L}| \cdot |\mathcal{G}| \cdot |\mathcal{M}| \cdot |\mathcal{T}|$$

এখানে $\mathcal{L}$ = LLM-এর সেট, $\mathcal{G}$ = language-এর সেট, $\mathcal{M}$ = prompt method-এর সেট, $\mathcal{T}$ = task-এর সেট। Paper: $N = 3 \times 3 \times 4 \times 200 = 7200$। প্রতি method-এ $3 \times 3 \times 200 = 1800$ program (আমার হিসাব)।

### ৬.২ Relative reduction (paper-এর ব্যবহৃত metric)

$$RR = \frac{F_{V} - F_{M}}{F_{V}} \times 100$$

$F_V$ = Vanilla-তে মোট finding, $F_M$ = MA-CoT-তে মোট finding।

Worked example (Table III, মোট): $RR = \frac{92 - 39}{92} \times 100 = \frac{53}{92} \times 100 = 57.6\%$ (paper-এর সাথে মেলে)।

High-severity: $H = B + C$ (Blocker + Critical)। $RR_H = \frac{90 - 39}{90} \times 100 = 56.7\%$।

### ৬.৩ Category shift (C language, primary dataset)

$$\Delta H = (B_M + C_M) - (B_V + C_V)$$

C: $B_V = 4,\ C_V = 48$ তাই $H_V = 52$; $B_M = 10,\ C_M = 21$ তাই $H_M = 31$। $\Delta B = +6,\ \Delta C = -27,\ \Delta H = -21$ (আমার হিসাব)। $RR_H = \frac{52 - 31}{52} \times 100 = 40.4\%$। Paper বলেছে "প্রায় 40%"; Blocker বাড়ার কারণ rule c:S5798।

### ৬.৪ Layer share (Table VII)

$$s_{g,k} = \frac{n_{g,k}}{\sum_{k'} n_{g,k'}} \times 100$$

$n_{g,k}$ = language $g$-তে layer $k$-তে attributed weakness instance। Paper শুধু $s$ দেয়, $n$ দেয় না। যেমন C: Platform/OS 38.0%, ecosystem crypto/TLS 31.2%, language-core memory 27.1%, toolchain 1.8% (যোগফল ৯৮.১%, বাকিটা sparse/uncategorized)।

### ৬.৫ আমার হিসাব: rate ratio ও অনিশ্চয়তা (paper করেনি)

Findings-কে Poisson count ধরলে (শক্ত অনুমান; একই program-এ একাধিক finding ও task-clustering আছে, তাই বাস্তব CI আরও চওড়া হবে):

$$\ln \hat{R}_{rate} = \ln \frac{F_M}{F_V}, \qquad SE = \sqrt{\frac{1}{F_V} + \frac{1}{F_M}}$$

Primary dataset: $\frac{39}{92} = 0.424$, $\ln 0.424 = -0.858$, $SE = \sqrt{\frac{1}{92} + \frac{1}{39}} = \sqrt{0.0109 + 0.0256} = 0.191$। ৯৫% CI: $-0.858 \pm 1.96 \times 0.191 = [-1.233,\ -0.484]$, অর্থাৎ rate ratio $\in [0.29,\ 0.62]$। LLMSecEval: $\frac{4}{73} = 0.055$, $SE = \sqrt{\frac{1}{73} + \frac{1}{4}} = 0.514$, CI প্রায় $[0.02,\ 0.15]$ (আমার হিসাব)। অর্থাৎ direction প্রায় নিশ্চিত, কিন্তু প্রতিটি ছোট cell (যেমন ২ বনাম ৩) আলাদা করা যায় না।

### ৬.৬ আমার প্রস্তাব: security pass^k (assurance report-এর জন্য)

একটি task-কে k বার generate করে, প্রতিবার scanner clean কিনা দেখে:

$$\text{SecPass}^{k} = \frac{1}{|\mathcal{T}|} \sum_{t \in \mathcal{T}} \frac{\binom{c_t}{k}}{\binom{n}{k}}$$

$n$ = প্রতি task-এ মোট sample, $c_t$ = task $t$-এ clean sample, $\binom{c_t}{k}/\binom{n}{k}$ = k টি এলোমেলো sample সবগুলোই clean হওয়ার সম্ভাবনা। Paper $n = 1$ ব্যবহার করেছে, তাই এটি অনুমান করা যায় না।

Illustration (শুধু আমার অনুমান-নির্ভর; findings স্বাধীন ধরে): MA-CoT-তে $39/1800 = 0.0217$ finding/program, তাই clean সম্ভাবনা $p \geq 0.978$ ধরলে $p^5 \approx 0.896$। Vanilla-তে $92/1800 = 0.0511$, $p \geq 0.949$, $p^5 \approx 0.769$। বাস্তবে এই বিশ্লেষণ task-wise correlation বাদ দেয় বলে শুধু ধারণা-চিত্র।

## ৭. Setup

| Item | Value |
|---|---|
| Models | gpt-5-2025-08-07 (gpt-5), claude-sonnet-4-5-20250929 (claude-4.5), gemini-2.5-pro (gemini-2.5) |
| Temperature | ১ (তিনটিতেই) |
| Max tokens | 32k (তিনটিতেই) |
| Context window | 400k / 200k / 1000k |
| Languages | C, Java, Python |
| Methods | Vanilla, Zero-shot, CoT, MA-CoT |
| Primary dataset | ২০০ language-agnostic task, ৭টি category, unit test ও manual/tool review আগের কাজে |
| External benchmark | LLMSecEval, ১৫০ task |
| মোট task | ৩৫০ (paper-এর হিসাব) |
| Generation | API endpoint, প্রতি combination-এ ১টি sample, ৭,২০০ program |
| Analyzer | SonarQube (language-specific analyzer), ২ জন researcher review |
| Seed/repeat | উল্লেখ নেই; কোনো repeated run নেই |
| Reasoning mode | gpt-5/claude/gemini-এর reasoning setting উল্লেখ নেই |

## ৮. Results

### ৮.১ Table III: Primary dataset, vulnerability count (মূল মান)

| Language | Model | Vanilla | ZeroShot | CoT | MA-CoT |
|---|---|---|---|---|---|
| C | gpt-5 | 17 | 23 | 24 | 13 |
| C | claude-4.5 | 19 | 20 | 27 | 11 |
| C | gemini-2.5 | 16 | 20 | 16 | 7 |
| Java | gpt-5 | 2 | 3 | 3 | 2 |
| Java | claude-4.5 | 20 | 13 | 12 | 1 |
| Java | gemini-2.5 | 5 | 6 | 6 | 1 |
| Python | gpt-5 | 3 | 2 | 2 | 2 |
| Python | claude-4.5 | 7 | 10 | 4 | 2 |
| Python | gemini-2.5 | 3 | 3 | 4 | 0 |

আমার যোগফল (Table VI-এর সাথে মেলে): Vanilla ৯২, ZeroShot ১০০, CoT ৯৮, MA-CoT ৩৯। Language-wise: C ৫২/৬৩/৬৭/৩১; Java ২৭/২২/২১/৪; Python ১৩/১৫/১০/৪ (Vanilla/ZS/CoT/MA)।

Paper-এর language reduction: C ৪০% (৫২ থেকে ৩১); Java ৮৫% (২৭ থেকে ৪); Python ৬৯% (১৩ থেকে ৪)। নয়টির মধ্যে সাতটি configuration-এ MA-CoT সবচেয়ে কম; ব্যতিক্রম gpt-5 Java (Vanilla ও MA-CoT দুটিই ২) এবং gpt-5 Python (ZS, CoT, MA-CoT তিনটিই ২)।

### ৮.২ Table IV: LLMSecEval (১৫০ task)

| Language | Model | Vanilla | ZeroShot | CoT | MA-CoT |
|---|---|---|---|---|---|
| C | gpt-5 | 4 | 7 | 10 | 0 |
| C | claude-4.5 | 3 | 3 | 7 | 0 |
| C | gemini-2.5 | 4 | 5 | 1 | 1 |
| Java | gpt-5 | 2 | 0 | 0 | 0 |
| Java | claude-4.5 | 46 | 28 | 6 | 2 |
| Java | gemini-2.5 | 5 | 3 | 3 | 1 |
| Python | gpt-5 | 1 | 0 | 1 | 0 |
| Python | claude-4.5 | 4 | 2 | 3 | 0 |
| Python | gemini-2.5 | 4 | 6 | 3 | 0 |

আমার যোগফল: Vanilla ৭৩, ZS ৫৪, CoT ৩৪, MA-CoT ৪। MA-CoT নয়টির মধ্যে ছয়টিতে শূন্য। Language-wise Vanilla: C ১১, Java ৫৩, Python ৯। Paper-এর মন্তব্য: Java Vanilla ৫৩ (primary-তে ২৭), C ১১ (primary-তে ৫২)।

### ৮.৩ Severity (Figure 2 ও text)

| Dataset | Method | মোট | Blocker | Critical | Major | Minor | High (B+C) |
|---|---|---|---|---|---|---|---|
| Primary | Vanilla | 92 | 18 | 72 | 0 | 2 | 90 |
| Primary | MA-CoT | 39 | 11 | 28 | 0 | 0 | 39 |
| LLMSecEval | Vanilla | 73 | 34 | 11 | 4 | 24 | 45 |
| LLMSecEval | MA-CoT | 4 | 1 | 1 | 0 | 2 | 2 |

Language-wise high-severity (primary): Java ২৫ (১৩B+১২C) থেকে ৪ (১B+৩C); Python ১৩ (১B+১২C) থেকে ৪ (০B+৪C); C ৫২ (৪B+৪৮C) থেকে ৩১ (১০B+২১C)। Major শূন্য ও Minor ২ কেবল Vanilla-র Java থেকে (আমার বিয়োগফল: ২৭ − ২৫ = ২)। LLMSecEval: C Critical ১১ থেকে ১; Java Blocker ২৫ থেকে ১, Major ৪ থেকে ০; Python Blocker ৯ থেকে ০।

### ৮.৪ CWE pattern (Table V, Figure 3, text)

| CWE | Language | Vanilla | ZS | CoT | MA-CoT |
|---|---|---|---|---|---|
| 295 (cert validation) | C (primary) | 25 | 14 | 18 | 6 |
| 327 (risky crypto) | C (primary) | 12 | 15 | 16 | 2 |
| 327 | Java (primary) | 11 | - | - | 1 |
| 327 | Python (primary) | 12 | - | - | 4 |

Residual (MA-CoT, C): CWE-367 (TOCTOU) ও CWE-14 (clear না হওয়া buffer)। CWE-611 (XXE) Java primary-তে MA-CoT-তে নেই; CWE-79 তীব্রভাবে কমেছে। CWE-327 reduction: C ৮৩%, Java ৯১%, Python ৬৭%।

### ৮.৫ Table VI: model-wise মোট

| Model | Primary V | ZS | CoT | MA | LLMSecEval V | ZS | CoT | MA |
|---|---|---|---|---|---|---|---|---|
| gpt-5 | 22 | 28 | 29 | 17 | 7 | 7 | 11 | 0 |
| claude-4.5 | 46 | 43 | 43 | 14 | 53 | 33 | 16 | 2 |
| gemini-2.5 | 24 | 29 | 26 | 8 | 13 | 14 | 7 | 2 |

Reduction (paper): claude-4.5 ৭০% (primary), ৯৬% (LLMSecEval); gemini-2.5 ৬৭% ও ৮৫%; gpt-5 ২৩% (primary) ও LLMSecEval-এ সবই শূন্য (১০০%)।

### ৮.৬ Table VII: layer contribution (শুধু শতাংশ)

| Language | Layer (share) |
|---|---|
| C | Platform/OS API 38.0% (CWE-367); Ecosystem crypto/TLS 31.2% (CWE-327, cert); Language-core memory/bounds 27.1% (CWE-119/120); Toolchain 1.8% (CWE-14) |
| Java | Application logic/policy 27.6%; Language-core error model 27.1% (CWE-600); Standard runtime crypto/TLS 21.2% (CWE-327); Language-core secret representation 13.5% (CWE-259); বাকি XML/config ইত্যাদি |
| Python | Generation-prone patterns/idioms 30.8%; Language-core semantics 21.5%; Application logic 21.5%; Ecosystem API permissiveness 16.9% (CWE-327/329); Runtime/module-state 9.2% |

## ৯. Key findings

1. **Targeted mitigation কাজ করে:** primary-তে ৯২ থেকে ৩৯, LLMSecEval-এ ৭৩ থেকে ৪ (Table III, IV, VI)।
2. **Generic "secure" ও CoT অনির্ভরযোগ্য:** primary-তে ZS মোট ১০০ ও CoT ৯৮, Vanilla ৯২-এর চেয়ে বেশি। C-তে ZS তিনটি model-এই বেশি; CoT gpt-5 ও claude-এ বেশি (claude ১৯ থেকে ২৭)।
3. **Model-নির্ভর responsiveness:** claude-4.5 weak baseline (৪৬) কিন্তু সবচেয়ে বেশি উপকার; gpt-5 primary-তে মাত্র ২৩% (২২ থেকে ১৭)।
4. **Severity composition আড়াল হতে পারে:** C-তে Blocker ৪ থেকে ১০ বাড়লেও Critical ৪৮ থেকে ২১ কমেছে; paper তাই total নয়, per-category report করার পরামর্শ দেয়।
5. **Residual risk hardening-ধরনের:** TOCTOU (CWE-367), secure wiping (CWE-14); এগুলো prompt দিয়ে সম্পূর্ণ সরে না, secure-by-construction primitive (memset_s, explicit_bzero, SecureZeroMemory, openat, O_CREAT|O_EXCL, O_NOFOLLOW) দরকার।
6. **Layered attribution:** C-এর বড় অংশ (৩৮.০% OS + ৩১.২% library) language-core নয়; Java/Python-এ configuration/API-driven, তাই prompt বেশি কাজ করে।
7. **Dataset shift:** একই method এক dataset-এ মাঝারি, অন্যটিতে প্রায় নিঃশেষ; "prompt effectiveness কোন CWE class dominant তার ওপর নির্ভর করে।"
8. **Model ও prompt একসাথে বাছাই:** দুর্বল baseline model-ও ভালো prompt-এ ভালো করতে পারে।

## ১০. Alternatives-এর চেয়ে কেন ভালো (paper-এর যুক্তি)

- বনাম **Vanilla/Zero-shot:** নির্দিষ্ট করণীয় দেয়, তাই model-এর "insecure default" বেছে নেওয়ার স্বাধীনতা কমে।
- বনাম **generic CoT:** CoT intermediate design choice বাড়ায় কিন্তু constraint না থাকায় insecure default বেছে সুন্দর ব্যাখ্যা দেয়; C-তে planning step check-then-use file flow ও verification bypass ডেকে আনে (paper-এর ব্যাখ্যা, test করা হয়নি)।
- বনাম **WA-CoT:** CWE নাম-তালিকার বদলে সংক্ষিপ্ত mitigation; overload নেই। (Paper WA-CoT-এর সাথে সরাসরি তুলনার সংখ্যা দেয়নি।)
- বনাম **RCI/Reflexion/RESCUE/SecureCoder/PromSec:** Related work-এ আলোচিত, কিন্তু **experiment-এ তুলনা নেই**। Paper বলে এটি inference-time ও hardware/training ছাড়া, কিন্তু কোনো measured তুলনা দেয়নি।
- Multi-round repair (Datta et al.) regression ঝুঁকি আছে বলে paper mitigation কে reasoning-এ ঢোকানো বেছেছে।

## ১১. কখন কাজ করে / কখন করে না

| অবস্থা | ফলাফল | কেন (paper-এর ব্যাখ্যা) |
|---|---|---|
| Java, Python; config/API-driven দুর্বলতা | ভালো (Java ৮৫%, Python ৬৯%) | secure default ও fail-closed নিয়ম prompt-এ দেওয়া যায় |
| Crypto/TLS/credential (CWE-327, 295, 259, 600) | তীব্র হ্রাস | স্পষ্ট করণীয় |
| C, TOCTOU ও secure wiping | আংশিক | OS ও compiler optimization-এর বিষয়, prompt দিয়ে সম্পূর্ণ সমাধান নয় |
| gpt-5, primary dataset | মাত্র ২৩% | baseline ইতিমধ্যে মোটামুটি ভালো; বা dataset-এর mix (paper "task vulnerability mix"কে কারণ বলেছে) |
| Generic CoT বা Zero-shot | অস্থির, কখনো খারাপ | অনির্দিষ্ট reasoning, নির্দিষ্ট constraint ছাড়া |
| LLMSecEval vs primary | ফল আলাদা মাত্রার | task mix ও language mix আলাদা |

## ১২. Limitations

### ১২.১ লেখকদের স্বীকৃত

- SAST exploitability মাপে না; pattern-sensitive (c:S5798 উদাহরণ)।
- LLM output decoding, prompt ও provider update-এ বদলায়; লেখকরা একই pipeline ও analyzer config দিয়ে কমানোর চেষ্টা করেছেন।
- ৩ language, ৩ model, ২ dataset; অন্য CWE mix-এ ফল ভিন্ন হতে পারে; দাবি শুধু comparative।
- ভবিষ্যৎ কাজ: static ও dynamic validation একসাথে।

### ১২.২ আমার পর্যবেক্ষণ

1. **প্রতি cell-এ একটি sample, temperature ১, কোনো repeat নেই।** "Internal validity" paragraph run-to-run variance আসলে মাপেনি (CG4)। Table-এর অনেক cell-এর পার্থক্য ১–২ (যেমন Java gpt-5: ২ বনাম ৩) যা noise হতে পারে।
2. **কোনো statistical test নেই;** "consistently" শব্দ count-তুলনার ওপর দাঁড়িয়ে (CG8)।
3. **একটি analyzer (SonarQube) ও একটি rule-set।** MA-CoT-এর mitigation (TLS verify, hard-coded secret নয়, modern crypto, input validation) মোটামুটি SonarQube rule-এর সাথে একই। অর্থাৎ prompt-কে evaluator-এর মাপকাঠির দিকে tune করা হয়েছে, Goodhart-ধরনের ঝুঁকি (CG12)। Exploit-ভিত্তিক বা অন্য analyzer (CodeQL, Semgrep) দিয়ে cross-check নেই।
4. **Functional correctness report নেই।** Primary dataset-এর unit test থাকলেও MA-CoT code-এর pass rate দেওয়া হয়নি; অতিরিক্ত সতর্ক code ভাঙা বা অকার্যকর হতে পারে (CG5)। 2026-এর SusVibes (নিচে ২১) ঠিক এই FuncPass বনাম SecPass ফাঁক দেখায়।
5. **Confound: MA-CoT prompt অনেক দীর্ঘ ও বেশি তথ্য দেয়।** "Vanilla + একই checklist (CoT ছাড়া)" বা তিন component-এর ablation নেই, তাই কোন অংশ কাজ করছে জানা যায় না।
6. **Paper-এর নিজস্ব সংখ্যায় অসঙ্গতি** (নিচে ১২.৩)।
7. **Dataset অধিকাংশই লেখকদের নিজেদের** (ref [37]); mitigation KB-ও লেখকদের তৈরি; independent held-out নেই। LLMSecEval C ও Python-ভিত্তিক হলেও Java-তেও চালানো হয়েছে; অনুবাদ/adaptation পদ্ধতি বর্ণিত নয়।
8. **Residual finding-এর ব্যাখ্যা subjective:** c:S5798 ও CWE-367-কে "hardening signal, weaker security নয়" বলা হয়েছে; কিন্তু কিছু finding আসল (TOCTOU race সত্যিকারের ঝুঁকি হতে পারে)। কোনটি false positive তার manual verdict count দেওয়া নেই।
9. **Reviewer agreement report নেই** (দুই researcher, কোনো κ নেই)।
10. **Verification loop অনুপস্থিত:** একবার generate, কোনো scanner-feedback loop নেই। তাই "reliability" শুধু প্রথম-পর্যায় output-এর ওপর।

### ১২.৩ Paper-internal inconsistency (আমি Table III/IV থেকে পুনরায় গুনেছি)

| # | Paper-এর দাবি | Table-এর সংখ্যা |
|---|---|---|
| 1 | Section V-E: primary-তে ZS ও CoT "সব model-এর" findings বাড়ায় | claude-4.5: V ৪৬, ZS ৪৩, CoT ৪৩ (কমেছে); বাড়ে gpt-5 (২২ থেকে ২৮, ২৯) ও gemini-2.5 (২৪ থেকে ২৯, ২৬) |
| 2 | Section V-A: C-তে ZS ও CoT তিন model-এই count বাড়ায় | gemini-2.5 C CoT = ১৬ = Vanilla ১৬ (বাড়েনি) |
| 3 | Section V-B: C-তে CoT "পাঁচটি model-dataset pair"-এ Vanilla-র চেয়ে বেশি | আমি চারটি পাই: primary-তে gpt-5, claude; LLMSecEval-এ gpt-5, claude। gemini-2.5 দুটোতেই বেশি নয় (১৬ = ১৬; ১ < ৪) |
| 4 | ৭,২০০ program, মোট ৩৫০ task | ৭,২০০ কেবল primary (৩ × ৩ × ৪ × ২০০)। LLMSecEval-এর program সংখ্যা (৩ × ৩ × ৪ × ১৫০ = ৫,৪০০ হলে) বলা নেই |
| 5 | Language-core-এর সংজ্ঞা strict | Java "secret representation (CWE-259)" ও Python "generation-prone idioms" (Table VII) কে language-core বা Table II-তে নেই এমন layer-এ রাখা; strict সংজ্ঞার সাথে মেলে না |

Abstract-এর "MA-CoT is the only strategy that consistently improves" বাক্যটি table অনুযায়ী মূলত ঠিক (সাতটি cell-এ সবচেয়ে কম), কিন্তু gpt-5-এর দুটি cell-এ tie।

## ১৩. Research gaps

| G-id | Gap | Evidence | Related CG / folder |
|---|---|---|---|
| G1 | Security signal-এর run-to-run variance অজানা; ১ sample, temp ১ | Section III-C.2; Table III-এর ছোট cell | CG4 / 06_Security |
| G2 | Single static analyzer; analyzer-এর নিজস্ব variance ও rule-sensitivity | SonarQube একমাত্র; c:S5798 বিতর্ক | CG10, CG12 / 06_Security |
| G3 | Prompt-এর mitigation ও scanner-এর rule মিলে যাওয়া (Goodhart) | MA-CoT checklist বনাম SonarQube rule | CG12 / 06_Security |
| G4 | Functional correctness ও security একসাথে report হয়নি | Table III-VI-এ শুধু finding | CG5, CG1 / 06_Security |
| G5 | Verification/repair loop ও তার regression ঝুঁকি তুলনা নেই | RCI, Reflexion শুধু related work | CG5, CG2 / 02_APR |
| G6 | Component ablation ও prompt-length confound নেই | তিন অংশ একসাথে test | CG8 / 03_Evaluation |
| G7 | Statistical testing ও CI নেই; reviewer agreement নেই | "consistently" শুধু count-ভিত্তিক | CG8, CG16 |
| G8 | Dynamic/exploit validation নেই (BaxBench, CWEval ধরনের) | Section VII construct validity | CG5, CG13 / 04_Test_Generation |
| G9 | Agent/repository-level patch-এ প্রযোজ্যতা অজানা; শুধু single-function generation | ২০০ standalone task | CG9, CG5 / 01_Agents |
| G10 | Security scanner finding-এর "delta" (patch আগে ও পরে) ও hardening-জনিত নতুন finding আলাদা করা | C Blocker ৪ থেকে ১০ | CG5, CG12 |

## ১৪. Improvement ideas

1. **Repeat ও variance:** প্রতি task-এ k = ৫ sample, temperature বদলে, SecPass^k ও finding-এর std dev report; McNemar বা paired bootstrap (task-wise)।
2. **Scanner ensemble:** SonarQube ছাড়াও Semgrep, CodeQL, Bandit/Flawfinder; finding union ও intersection আলাদা report; scanner disagreement-ই অনিশ্চয়তা।
3. **Exploit/test-ভিত্তিক সংকেত:** BaxBench/CWEval-ধরনের security test, fuzzing/sanitizer (ASan, UBSan) C code-এ।
4. **Ablation:** baseline rule শুধু; CWE mitigation শুধু; language checklist শুধু; এবং prompt-length-matched placebo (অপ্রাসঙ্গিক সমান দৈর্ঘ্যের টেক্সট)।
5. **Closed loop:** generate, scan, finding-based feedback, regenerate (সর্বোচ্চ ২ রাউন্ড); প্রতিটি রাউন্ডে নতুন finding ও functional test regression মাপা।
6. **Held-out scanner:** prompt যে scanner দিয়ে tune হয়েছে, আর evaluate হয় যে scanner দিয়ে, তা আলাদা।
7. **Per-category report** (paper-এর ভালো ধারণা) এবং layered attribution-কে report-এ স্থায়ীভাবে রাখা।
8. **Secure-by-construction wrapper:** residual CWE-367/14-এর জন্য prompt নয়, post-process লিন্ট বা safe-API replacement।

## ১৫. Publication potential (SPL3-feasible)

- **সম্ভাব্য শিরোনাম:** "How Reliable is the Security Signal? Run-to-Run Variance and Analyzer Disagreement in LLM Secure-Code Evaluation"।
- **নতুনত্ব:** MA-CoT-ধরনের prompt-এর ফল দুই-তিনটি scanner ও k-বার run-এ আবার মাপা; "security finding count" কতটা স্থিতিশীল তা দেখানো; hardening-জনিত finding (c:S5798) আলাদা করার triage।
- **Feasibility:** ৫০-task subset, ২–৩টি সস্তা/open model, ৩ prompt strategy, k = ৫, Python+C শুধু। Compute ও খরচ কম; scanner স্থানীয়ভাবে চালানো যায়।
- **ঝুঁকি:** নতুন ফল না-ও আসতে পারে (variance ছোট হলে)। সেক্ষেত্রেও negative result ও tool paper হিসেবে মূল্য আছে।
- **Venue ধরন:** MSR/ICSE workshop (LLM4Code ধরনের), বা SPL3 report-এর একটি অধ্যায়।

## ১৬. SPL3 implementation

1. **Task set:** paper-এর LLMSecEval (১৫০) থেকে ৫০টি + আমাদের assurance benchmark-এর কিছু patch-task।
2. **Prompt arms:** Vanilla, Zero-shot secure, MA-CoT-lite (শুধু baseline rule + task mitigation), এবং length-matched placebo।
3. **Models:** ২টি open/সস্তা model + ১টি commercial (খরচ-সচেতন; ২১.৪ দেখো)।
4. **Runs:** k = ৫, একই seed বর্জিত; সব raw output ও scanner JSON সংরক্ষণ।
5. **Scanners:** Semgrep, Bandit (Python), Flawfinder/cppcheck (C), CodeQL যেখানে সম্ভব; প্রতিটির version ও rule-set hash লিখে রাখা (CG11)।
6. **Metrics:** finding per program, SecPass^k, high-severity count, category shift table, scanner agreement (Jaccard), functional pass rate (unit test)।
7. **Assurance report-এ আউটপুট:** একক নম্বর নয়; scanner-wise অনুচ্ছেদ, run-variance range, "delta findings introduced by patch" এবং "could not verify" অবস্থা।
8. **Analysis:** paired bootstrap, task-clustered CI; মাত্র গণনার tab নয়।

## ১৭. আগের sub-domain-এর সাথে সম্পর্ক

- **Sub-domain 1 (Agents):** SWE-agent/Agentless-এর patch-এ security scan নেই; এই paper single-function generation-এ ভালো প্রয়োগ, repository-level-এ অনিশ্চিত (G9)।
- **Sub-domain 2 (APR):** VRpilot-এর "sanitizer pass ≠ secure" ও এই paper-এর "SAST clean ≠ exploit-free" একই সতর্কতা; Reflexion/RCI-র regression ঝুঁকি (G5)।
- **Sub-domain 3 (Evaluation):** Engineering Reliable Coding Agents monograph-এর "single run varies 2.2–6.0 pp" ও "gaming"-এর সাথে সরাসরি সম্পর্ক: এই paper-এ একই ধরনের variance ও gaming পরীক্ষা নেই।
- **Sub-domain 4 (Test generation):** CoverUp/TestDecision-এর "coverage ≠ oracle" ধারণা এখানে "SAST clean ≠ secure"-এর সমান্তরাল।
- **Sub-domain 5 (Patch validation):** HITL LLM-as-a-Judge-এর "recall বনাম specificity" এবং SAST-এর "false positive বনাম hardening-induced finding"-এর তুলনা করা যায়।
- **Sub-domain 6 (Security):** এই paper generation-side technique; অন্য paper-গুলো যেখানে security কে measure করে (SusVibes ইত্যাদি, context ২১ দেখো) সেগুলোর সাথে মিলিয়ে পড়তে হবে।

## ১৮. Supervisor Q&A

**প্রশ্ন ১: Paper-এ "reliability" মানে কী?**
উত্তর: মূলত "ভিন্ন model/language/dataset-এ MA-CoT-ই সবচেয়ে কম finding দেয়", অর্থাৎ ranking-এর স্থিতিশীলতা। কোনো repeated run নেই, তাই একই setting-এ run-to-run স্থিতিশীলতা মাপা হয়নি। আমাদের CG4 এখানে সরাসরি খোলা।

**প্রশ্ন ২: ৯২ থেকে ৩৯ কমা কি statistically significant?**
উত্তর: Paper test করেনি। আমার হিসাবে (Poisson ধরে) rate ratio ০.৪২৪, ৯৫% CI প্রায় ০.২৯–০.৬২; দিক পরিষ্কার, কিন্তু findings clustered বলে CI আসলে আরও চওড়া হবে এবং ছোট cell-ভিত্তিক দাবি (যেমন model-wise) দুর্বল।

**প্রশ্ন ৩: C-তে Blocker ৪ থেকে ১০ হলো, তবু paper কেন বলছে ভালো?**
উত্তর: Critical ৪৮ থেকে ২১ কমেছে, মোট high-severity ৫২ থেকে ৩১। Blocker বাড়ার কারণ c:S5798 rule (memset দিয়ে secret মুছলে compiler বাদ দিতে পারে)। এটি আসল সমস্যা (wipe কার্যকর না) আবার hardening চেষ্টা; দুটোর পার্থক্য scanner করতে পারে না। এটাই assurance report-এর জন্য শিক্ষা: "নতুন finding = খারাপ" ধরা ভুল।

**প্রশ্ন ৪: Evaluator-এর সাথে prompt মিলে যাওয়ার (Goodhart) ঝুঁকি কোথায়?**
উত্তর: MA-CoT-এর checklist (TLS verify, hard-coded secret নয়, AEAD, input validation) SonarQube-এর rule-এর সাথেই মোটামুটি মেলে। তাই কম finding মানে বাস্তবে নিরাপদ নাও হতে পারে; অন্য scanner বা exploit test ছাড়া তা আলাদা করা যায় না (CG12)।

**প্রশ্ন ৫: Verification loop আছে কি?**
উত্তর: নেই। MA-CoT একবারের generation-এ reasoning-এ নিয়ম ঢোকায়। Related work-এ RCI/Reflexion আলোচিত, regression ঝুঁকিসহ, কিন্তু তুলনা নেই।

**প্রশ্ন ৬: Paper-এর ফল কি এখন (২০২৬ model-এ) টিকবে?**
উত্তর: তথ্য নেই। Paper-এর model গুলো ২০২৫-র (gpt-5, claude-4.5, gemini-2.5)। বর্তমান model-এ MA-CoT-এর কোনো ফল আমাদের তথ্যে নেই।

**প্রশ্ন ৭: Layered attribution আমাদের কাজে লাগবে কি?**
উত্তর: হ্যাঁ, assurance report-এ প্রতিটি finding-এর "কারণ-layer" (library, OS, toolchain, application, language-core) দেওয়া actionable। কিন্তু attribution-এর নির্ভরযোগ্যতা (কে করেছে, inter-rater) paper-এ অনিশ্চিত।

**প্রশ্ন ৮: কেন শুধু findings গুনলেই হবে না?**
উত্তর: Paper নিজেই বলেছে totals category shift আড়াল করে। আমাদের report-এ per-category, per-scanner ও run-variance আলাদা দেখানো উচিত।

## ১৯. Glossary

| Term | অর্থ |
|---|---|
| MA-CoT | Mitigation-Aware Chain-of-Thought, করণীয়-সহ security prompt |
| WA-CoT | Weaknesses-Aware CoT, শুধু CWE তালিকা-ভিত্তিক আগের পদ্ধতি |
| SAST | Static security analysis |
| CWE | দুর্বলতার শ্রেণি-ID |
| TOCTOU | Check ও use-এর মাঝে race |
| AEAD | Authenticated encryption |
| Blocker/Critical | SonarQube-এর সর্বোচ্চ দুই severity |
| Language-core | Language spec বা বাধ্যতামূলক runtime থেকে আসা দুর্বলতা |
| Language-stack | Library, OS, toolchain, application logic থেকে আসা |
| Hardening | নিরাপত্তা বাড়ানোর চেষ্টা (যেমন secure wipe) |
| SecPass^k | k বারের সবগুলো run security-clean (আমার প্রস্তাব) |

## ২০. Summary card

| Item | Value |
|---|---|
| Idea | Prompt-এ task-নির্দিষ্ট CWE mitigation + baseline rule + language checklist |
| Scale | ৩ model, ৩ language, ৪ method, ২০০ task = ৭,২০০ program |
| Primary result | ৯২ থেকে ৩৯ finding (৫৭.৬%); high-severity ৯০ থেকে ৩৯ (৫৬.৭%) |
| External result | ৭৩ থেকে ৪ (৯৪.৫%); high-severity ৪৫ থেকে ২ (৯৫.৬%) |
| Negative finding | Zero-shot ও CoT কখনো Vanilla-র চেয়ে খারাপ (primary: ১০০ ও ৯৮ বনাম ৯২) |
| Residual | CWE-367, CWE-14 (OS/toolchain) |
| Weakness | ১ sample, ১ analyzer, test নেই, functional result নেই, ablation নেই |
| আমাদের ব্যবহার | per-category report, layered attribution, scanner-triage, SecPass^k |

## ২১. বর্তমান (2026) প্রেক্ষাপট

### ২১.১ তখন বনাম এখন

| বিষয় | Paper (২০২৫ model) | ২০২৬ (context থেকে) |
|---|---|---|
| Model | gpt-5, claude-sonnet-4-5, gemini-2.5-pro | Claude Opus 5.5, Sonnet 5.5, GPT-6 family, Gemini 4 Argon; open: Kimi K3.1 Pro, GLM-5.x, DeepSeek V4 |
| Security বনাম function | MA-CoT-এ finding কম; function মাপা হয়নি | SusVibes: FuncPass 62–84% কিন্তু SecPass 7.8–17.3% (I, Opus 4.6/GPT-5.4 যুগ) |
| Run variance | মাপা হয়নি | SWE-rebench pass@1 বনাম pass@5 ফাঁক ১২–১৮ পয়েন্ট (I); prompt rewording noise rerun-এর ১১–৫৮ গুণ (I) |
| Gaming | আলোচনা নেই | METR: সফল long-task run-এর অন্তত ১৬% ছিল cheat (I, আগের প্রজন্ম); Opus 5.5 card-এ "hidden tests" reasoning ও git concealment কিছু environment-এ (V) |
| Prompt injection | আলোচনা নেই | Opus 5.5 success 54.61% safeguard ছাড়া, 11.13% সহ (V) |
| MA-CoT-এর ফল বর্তমান model-এ | Paper-এ আছে (পুরোনো model) | বর্তমান model-এর তথ্য পাওয়া যায়নি; No current-model SusVibes/BaxBench data |

### ২১.২ এখনো সত্য / পুরোনো

- **এখনো সত্য (সম্ভবত):** security ও functional pass-এর ফাঁক (SusVibes); generic "be secure" prompt-এর সীমা (SecureAgentBench-এর উদ্ধৃতি paper-এই); single-run বিশ্বাসযোগ্য নয় (variance data)।
- **পুরোনো হতে পারে:** নির্দিষ্ট সংখ্যা (৫৭.৬%, ২৩% ইত্যাদি) পুরোনো model-এর; নতুন model-এ baseline আরও ভালো বা আলাদা হতে পারে, তাই MA-CoT-এর সুবিধা কমতে/বদলাতে পারে (তথ্য পাওয়া যায়নি)।
- **অনিশ্চিত:** claude-এর "weak security priors"-এর দাবি Sonnet 5.5/Opus 5.5-এ খাটে কিনা।

### ২১.৩ আজকের খোলা gap

| Gap | অবস্থা (২০২৬) |
|---|---|
| Security signal-এর run variance | বর্তমান model-এ secure-code variance-এর data পাওয়া যায়নি; general benchmark variance আছে (I) |
| Prompt-level mitigation বনাম agent scaffold | Agent harness (mini-SWE-agent) ও prompt-এর পারস্পরিক প্রভাবের তথ্য নেই |
| Gaming of security scanner | Cheating আচরণের প্রমাণ (METR, V) আছে; security scanner-নির্দিষ্ট gaming-এর তথ্য নেই |
| Dynamic security validation | SusVibes-ধরনের বেঞ্চমার্ক আছে, কিন্তু current-model data নেই |
| Cost-aware secure generation | Task-প্রতি খরচের পার্থক্য বিশাল (নিচে); secure prompt-এর অতিরিক্ত token খরচ জানা নেই |

### ২১.৪ বর্তমান model-এ SPL3 idea (খরচ-সচেতন)

- **Idea:** Semgrep + CodeQL/Bandit + SonarQube-তে একই output scan করে "scanner disagreement" ও "run variance" মাপা, ছোট ৫০-task set-এ।
- **Model বাছাই:** Vals Terminal-Bench 4.0 অনুযায়ী task-প্রতি আনুমানিক খরচ: Opus 5.5 ১৩.২০ USD, Kimi K3.1 Pro ৪.৫৭ USD, GPT-6.1 Sol ১.৭২ USD (I; এটি Terminal-Bench-এর খরচ, আমাদের কাজের সরাসরি খরচ নয়)। তাই বেশিরভাগ run সস্তা/open model-এ, কয়েকটি আনুমানিক commercial reference হিসেবে।
- **Arms:** Vanilla, MA-CoT-lite, placebo; k = ৫।
- **প্রতিবেদন:** SecPass^k, delta finding, scanner agreement, FuncPass (SusVibes-ধরনের সমান্তরাল মাপ)।
- **নিয়ম:** version-bound verdict (CG11); "could not verify" স্পষ্ট ফল।

### ২১.৫ তিনটি Q&A

**প্রশ্ন ১: ২০২৬ model-এ এই paper-এর ফল কি পুনরুৎপাদন হবে?**
উত্তর: বর্তমান model-এর তথ্য পাওয়া যায়নি। দিক সম্ভবত একই (নির্দিষ্ট mitigation > অস্পষ্ট নির্দেশ), কিন্তু magnitude অনিশ্চিত; সেটাই আমাদের পরীক্ষার প্রশ্ন।

**প্রশ্ন ২: Security signal-এ gaming কীভাবে ঘটতে পারে?**
উত্তর: Agent বা prompt যদি scanner-এর rule জেনে সেগুলো এড়ায় (বা code মুছে ফেলে), scan clean হয় কিন্তু কার্যকারিতা/নিরাপত্তা নষ্ট হয়। METR ও Opus 5.5 card-এর (V) cheat-আচরণ দেখায় এটি কাল্পনিক নয়; তাই scan-এর সাথে functional test ও একাধিক scanner দরকার।

**প্রশ্ন ৩: এই paper-এর কোন অংশ সরাসরি assurance report-এ ঢোকানো যায়?**
উত্তর: (ক) per-category/per-severity রিপোর্ট (totals নয়), (খ) layered attribution, (গ) hardening-জনিত নতুন finding আলাদা করার triage। MA-CoT prompt নিজে generation-side; report-এর "পরিমাপ" অংশ নয়, কিন্তু একটি মান্য treatment arm হতে পারে।
