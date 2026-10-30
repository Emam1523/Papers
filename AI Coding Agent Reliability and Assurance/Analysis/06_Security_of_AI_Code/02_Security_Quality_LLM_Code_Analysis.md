# Paper Analysis 02 (Security): Security and Quality in LLM-Generated Code — A Multi-Language, Multi-Model Analysis

> Sub-domain: Security of AI-Generated Code
> PDF: Security of AI-Generated Code/Security and Quality in LLM-Generated Code.pdf

## ০. Bibliographic info

| বিষয় | তথ্য |
|---|---|
| Title | Security and Quality in LLM-Generated Code: A Multi-Language, Multi-Model Analysis |
| Authors | Mohammed F. Kharma, Soohyeon Choi, Mohammad Alkhanafseh, David Mohaisen (corresponding) |
| Affiliation | University of Central Florida (Mohaisen, Choi); Birzeit University, Palestine (Kharma, Alkhanafseh) |
| Venue (paper-এর header) | IEEE Transactions on Dependable and Secure Computing, Vol. 14, No. 8, August 2015 — এটি template-এর placeholder, কারণ paper-এর reference-এ 2025 সালের source ও "accessed 12/2025" আছে |
| আসল অবস্থান | arXiv:2502.01853v2 [cs.CR], 9 March 2026। কোনো journal-এ accepted কি না, paper-এ বলা নেই |
| Paper type | Measurement study (empirical); নতুন vulnerability class বা নতুন analysis technique দাবি করে না |
| Code/data | GitHub-এ replication package (dataset, prompts, unit tests, analysis scripts) |
| Models (সবই 2024-এর) | GPT-4o-202407, claude-3-5-sonnet-20240620, gemini-1.5-pro-001, codestral-2405, llama-3-sonar-large-32k-chat (Perplexity) |
| Languages | Python, Java, C++, C |
| মূল সংখ্যা | 200 tasks × 4 languages × 5 models = 4,000 programs; 4,000 unit test files; মোট 97,412 LoC |

## ১. TL;DR

এই paper 200টি language-neutral programming task নিয়ে 5টি LLM-কে 4টি language-এ code লিখতে বলে (মোট 4,000 program)। তারপর তিনটি অক্ষে মাপে: (ক) compile সফল কি না, (খ) unit test-এ semantic correctness, (গ) SonarQube ও CodeQL দিয়ে security ও quality (reliability, maintainability, security hotspot, clean code)।

- Python-এ compile সবচেয়ে ভালো (5টির মধ্যে 4টি model 100.0%, claude-3.5 99.5%), C++ সবচেয়ে খারাপ (77.0%–89.0%)।
- Semantic correctness: Python গড় 90.12%, C গড় 77.78% (আমার হিসাব, পাঁচ model-এর unweighted গড়)।
- মোট security finding 284টি: Java 69, Python 40, C++ 53, C 122। C-তে 122-এর মধ্যে 66টি CWE-120 (buffer copy)।
- Java ও Python-এ সবচেয়ে বেশি CWE-780 (RSA without OAEP): Java 29টি, Python 18টি।
- দুর্বলতা: প্রতিটি task-এর জন্য একবারই generation (temperature 0.9), কোনো confidence interval নেই, SAST-এর false positive rate দেওয়া নেই, এবং কয়েকটি table-এ paper-এর নিজের লেখার সাথে অসঙ্গতি আছে (বিভাগ ১২)।

**Supervisor-কে ৩০ সেকেন্ডে:** "এটি security-র একটি বড় measurement study, patch-এর নয়, single-turn function/file-level code-এর। আমাদের assurance report-এর জন্য তিনটি জিনিস নেওয়ার আছে: (১) কোন CWE ও কোন tool (SonarQube + CodeQL, আর Semgrep পরামর্শ) চালাতে হবে, (২) correctness আর security আলাদা signal, কারণ claude-3.5 সবচেয়ে বেশি correct হয়েও সবচেয়ে বেশি LoC ও maintainability issue তৈরি করে, আর gemini-1.5 correctness-এ মাঝামাঝি হয়েও সবচেয়ে বেশি vulnerability (75টি) দেয়, (৩) language-ভেদে ফলাফল আলাদা, তাই tool ও threshold language-অনুযায়ী ঠিক করতে হবে। তবে raw count LoC-এর সাথে জড়িত, তাই আমরা density ও before/after diff ব্যবহার করব।"

## ২. Background (শুধু আমাদের project-এ নতুন concept)

- **CWE (Common Weakness Enumeration):** MITRE-র weakness-এর তালিকা। paper-এ 86টি আলাদা CWE ID task-এ tag করা হয়েছে। প্রতিটি CWE-র একটি নম্বর আছে, যেমন CWE-120 (buffer copy without checking size), CWE-259 (hard-coded password), CWE-780 (RSA without OAEP padding)।
- **SAST (Static Application Security Testing):** code না চালিয়ে source বিশ্লেষণ করে weakness খোঁজা। এখানে দুটি tool: SonarQube (quality ও security rule, নিজস্ব "security hotspot" ধারণা সহ) এবং CodeQL (query-ভিত্তিক, CWE-aligned)।
- **Security hotspot:** SonarQube-এর শব্দ। এটি নিশ্চিত vulnerability নয়, বরং security-sensitive code-এর জায়গা যা মানুষকে দেখে সিদ্ধান্ত নিতে হয় (authentication, input validation ইত্যাদি)। তাই hotspot সংখ্যা vulnerability-র সমান নয়।
- **Quality attribute (SonarQube):** reliability (bug), maintainability (code smell), security (vulnerability), security hotspot। Clean code-এর চারটি dimension: consistency, intentionality, adaptability, responsibility।
- **Complexity metric:** LoC, Cyclomatic Complexity (CyC), Cyclomatic Complexity Density (CCD), Cognitive Complexity (CoC)।
- **Language-neutral specification:** একই task-এর বর্ণনা কোনো language-এর নাম বা library ছাড়া লেখা, যাতে একই prompt চারটি language-এ চলে।
- **Security-relevant legacy API:** Java 17-এ SecureRandom-এর মতো আধুনিক ব্যবস্থা থাকলেও model পুরনো পথ নেয়; C++-এ rand() ও srand() ব্যবহার (Appendix C.4)।

## ৩. Problem

- LLM-generated code-এর security নিয়ে আগের কাজ বেশিরভাগ এক language (Python বা C) বা এক model (Copilot, ChatGPT) নিয়ে।
- Language বদলালে একই task-এ security কেমন বদলায়, তা পরিষ্কার নয়। paper বলে, security quality "identical scenarios"-এও language-ভেদে আলাদা হতে পারে।
- Correctness, quality ও security প্রায়ই আলাদা করে মাপা হয়; একসাথে মাপলে trade-off বোঝা যায়।
- আগের কাজে dataset প্রায়ই single-language (SecurityEval শুধু Python, 130 prompt) বা function signature দেওয়া, যা বাস্তব ব্যবহারের চেয়ে সহজ।

## ৪. Goal ও Research Questions

- **RQ1:** Programming language-এর পছন্দ LLM-generated code-এর security-কে কীভাবে প্রভাবিত করে?
- **RQ2:** বিভিন্ন LLM syntactically valid ও semantically correct code বানানোয় কেমন তুলনীয়, একাধিক language-এ?
- **RQ3:** কোন security vulnerability সবচেয়ে বেশি, এবং model ও language-ভেদে কীভাবে বদলায়?
- **Contribution:** (১) 200 task-এর manually vetted dataset, সাত category-তে; (২) unified setup-এ cross-language ও cross-model তুলনা; (৩) CWE ভিত্তিক গভীর security বিশ্লেষণ।
- paper নিজেই বলে এটি "quantitative measurement study"। তাই কারণ-নির্ণয় (কেন Python ভালো) অনুমান-নির্ভর (training data, model size), পরীক্ষা করা নয়।

## ৫. Methodology (ধাপে ধাপে)

1. **Model নির্বাচন:** eligibility criteria: ব্যাপক ব্যবহার, program synthesis/reasoning/security কাজে প্রদর্শিত ক্ষমতা, চার language-এ code generation support, stable API, এবং architecture-র বৈচিত্র্য। ফল: Table 3-এর পাঁচটি model।
2. **Generation settings (Table 4):** সব model-এ temperature 0.9, max tokens 4,096, top-p 0.9। Context window: GPT-4o 128k, llama-3 32k, claude-3.5 200k, codestral 32k, gemini-1.5 128k।
3. **Language নির্বাচন:** C, C++, Java, Python; static বনাম dynamic typing এবং manual বনাম automatic memory management-এর পার্থক্য কাজে লাগাতে।
4. **Prompt:** মূল task description, কোনো prompt engineering নেই, function signature নেই। একটি Python script prompt পাঠায়; দ্বিতীয় script output গুছিয়ে file বানায় (file name-এ task, model, language)।
5. **Environment:** Debian 12, OpenJDK 17.0.8, Python 3.11.9, CMake 3.28.6 (C++17), Lenovo ThinkPad E570 (i7 7th gen, 16 GB)। একই hardware।
6. **Compilation:** compiled language-এ compile; Python-এ built-in syntax checker। ফল 200 row × 20 column binary matrix। ছোট, সঙ্গত fix (import/include) প্রয়োগ ও log করা হয়েছে।
7. **Semantic correctness:** চার phase। (ক) প্রতি task-এ language-agnostic spec (normal, boundary, edge, invalid); (খ) প্রতিটি generated program-এর interface বিশ্লেষণ (কারণ function name, parameter, return, I/O আলাদা); (গ) প্রতি program-এর জন্য আলাদা unit test, একই input ও expected output; (ঘ) দুজন professional test review করেন। ফল: 4,000 unit test file। প্রতি program 0%–100% score (পাস করা case-এর অনুপাত)। প্রতি task-এ সর্বোচ্চ 10টি test।
8. **Coverage:** representative subset-এ JaCoCo (Java) ও সমতুল্য tool; গড় line coverage 75%-এর বেশি।
9. **Complexity:** LoC, CyC, CCD, CoC (বিভাগ ৬)।
10. **Static analysis:** SonarQube (reliability, security, maintainability, hotspot) এবং CodeQL (query pack)। প্রতিটি SonarQube-reported vulnerability manual যাচাই এবং CodeQL-এর সাথে একই file/location-এ cross-check; stratified 20% sample যাচাই (বিভাগ ১২-এ অসঙ্গতি দেখো)।
11. **Human effort:** দুজন software engineer (4 ও 10 বছরের অভিজ্ঞতা); test তৈরি ও চালাতে 800 person-hour-এর বেশি, পাঁচ মাসে।
12. **Dataset নির্মাণ:** category অনুযায়ী ভাগ, উৎস (LeetCode, Edabit, Codewars, Exercism, SecurityEval, CodeQL, MITRE CWE), peer review, tagging ও similarity analysis দিয়ে redundancy সরানো।

### ৫.১ Dataset

| Category (Table 6) | Task count |
|---|---|
| Secure Coding (CWEs) | 102 |
| Data Structures and Algorithms | 86 |
| Parsing and Validation | 54 |
| Networking | 48 |
| Mathematics and Logic | 26 |
| Programming Systems and Utilities | 18 |
| Concurrency and Synchronization | 6 |

একটি task একাধিক category-তে পড়তে পারে, তাই যোগফল (340) 200-র বেশি। Table 5 অনুযায়ী উৎস: Manual (first author-এর লেখা) 123, coding challenge site 64, security dataset 13; মোট 200। Difficulty (garbled table পড়ে আমার ব্যাখ্যা): Easy 17, Medium 173, Hard 10। CWE group (Table 7): Input Validation (CWE-20, 707, 642), Injection (89, 78, 74), Buffer Errors (119, 787, 125), Access Control (285, 639, 287), Cryptographic (321, 326, 327), Information Exposure (209, 532), Resource Management (400, 770), Memory Errors (416)।

## ৬. Math

### ৬.১ Compilation success rate

$$
S_P = \frac{C_P}{T_P} \times 100, \qquad C_P = \sum_{i=1}^{n} C_i, \quad C_i \in \{0, 1\}
$$

- $P$: programming language; $T_P$: ওই language-এর মোট file; $C_i = 1$ যদি file $i$ সফলভাবে compile হয়।
- **Worked example (paper-এর সংখ্যা):** Java, claude-3.5: $S_P = 95.0\%$ (Table 8)। প্রতি model-language-এ $T = 200$, তাই $C = 190$ file compile হয়েছে (আমার হিসাব)।

### ৬.২ Semantic score

paper প্রতি program-এর জন্য 0%–100% score বলে (পাস করা test case ÷ মোট test case)। আমার formalisation:

$$
s_i = \frac{\text{passed}_i}{\text{total}_i}\times 100, \qquad \bar{s}_{m,P} = \frac{1}{200}\sum_{i=1}^{200} s_i
$$

- $m$: model; $P$: language। Table 8-এর "Semantic error-free" শতাংশ সম্ভবত $\bar{s}_{m,P}$। paper স্পষ্ট বলেনি এটি গড় score, না সব test পাস করা program-এর অনুপাত (বিভাগ ১২)।

### ৬.৩ Complexity metric

$$
M = E + 2Q - N, \qquad M_d = \frac{E + 2Q - N}{cl}, \qquad C = C_{\text{base}} + \sum_{i=1}^{n} n_c
$$

- $E$: control flow graph-এর edge; $N$: node; $Q$: connected component (সাধারণ লেখায় $P$); $cl$: মোট code line। $M$ = Cyclomatic Complexity (CyC), $M_d$ = CCD, $C$ = Cognitive Complexity (CoC), যেখানে $n_c$ nesting ও conditional থেকে বাড়া মান।
- **Worked example (Table 10, Java, claude-3.5):** CyC = 1,097, LoC = 6,480, তাই CCD = $1{,}097 / 6{,}480 = 0.169 \approx 0.17$, যা table-এর 0.17-এর সাথে মেলে।
- **অসঙ্গতি পরীক্ষা (আমার হিসাব):** gemini-1.5-এর Java row: $965/5{,}606 = 0.172$, কিন্তু table-এ 0.23। যদি gemini ও codestral-এর LoC অদলবদল করা হয়, তাহলে $965/4{,}143 = 0.233$ মেলে এবং codestral-এ $730/5{,}606 = 0.130$ মেলে। চারটি language-এই একই অদলবদল সব সংখ্যা মেলায় (Python: $765/2{,}077=0.368$; C++: $1{,}084/4{,}293=0.253$; C: $1{,}256/4{,}532=0.277$)। তাই Table 10-এর LoC কলাম বা CCD কলাম দুটির একটিতে gemini-1.5 ও codestral-এর সারি উল্টে গেছে।

### ৬.৪ আমার তৈরি normalised metric (paper-এ নেই)

$$
D_{\text{vuln}}(P) = \frac{\text{findings}_P}{\text{LoC}_P/1000}, \qquad R_{\text{prog}}(P) = \frac{\text{findings}_P}{\text{programs}_P}
$$

- $D_{\text{vuln}}$: প্রতি 1000 line-এ finding; $R_{\text{prog}}$: প্রতি program-এ finding (প্রতি language-এ 1,000 program)।
- **Worked example (আমার হিসাব):** C: $122/29.528 = 4.13$ per KLoC; $122/1000 = 0.122$ per program। Python: $40/14.154 = 2.83$ per KLoC; $0.040$ per program। Java: $69/26.55 = 2.60$; $0.069$। C++: $53/27.18 = 1.95$; $0.053$।

### ৬.৫ Sampling error (আমার হিসাব)

প্রতি model-language cell-এ $n=200$। যদি score-কে binary ধরা হয়, standard error $\sqrt{p(1-p)/n}$:

$$
\mathrm{SE} = \sqrt{\frac{0.95 \times 0.05}{200}} = 0.0154 \;(\approx \pm 3.0\ \text{pp at 95\%}), \qquad \sqrt{\frac{0.80\times 0.20}{200}} = 0.0283 \;(\approx \pm 5.5\ \text{pp})
$$

অর্থাৎ C-তে GPT-4o (81.1%) ও gemini-1.5 (77.0%)-এর 4.1 pp পার্থক্য এই আন্দাজে noise-এর সীমার ভেতরে। paper কোনো CI বা significance test দেয়নি।

## ৭. Setup (table)

| উপাদান | মান |
|---|---|
| Tasks | 200 (language-neutral, 86 unique CWE ID tag) |
| Languages | Python 3.11.9, Java (OpenJDK 17.0.8), C++ (C++17, CMake 3.28.6), C |
| Models | GPT-4o-202407, claude-3-5-sonnet-20240620, gemini-1.5-pro-001, codestral-2405, llama-3-sonar-large-32k-chat |
| Decoding | temperature 0.9, top-p 0.9, max tokens 4,096; একবার generation |
| Programs | 4,000 (200 per language per model) |
| Unit tests | 4,000 per-program test file; প্রতি task-এ সর্বোচ্চ 10 case |
| Static analysis | SonarQube, CodeQL (manual review সহ) |
| Coverage | নমুনা subset-এ গড় line coverage 75%-এর বেশি |
| Analysed LoC | 97,412 |
| Human effort | 800+ person-hour, পাঁচ মাস |
| Hardware/OS | Lenovo ThinkPad E570, i7 7th gen, 16 GB, Debian 12 |
| Prompt | মূল description, কোনো prompt engineering নেই, function signature নেই |

## ৮. Results

### ৮.১ Compilation-error-free rate (Table 8, বাম অর্ধেক, %)

| Model | Java | Python | C++ | C | গড় (আমার হিসাব) |
|---|---|---|---|---|---|
| claude-3.5 | 95.0 | 99.5 | 81.5 | 96.0 | 93.00 |
| gemini-1.5 | 88.5 | 100.0 | 77.5 | 90.5 | 89.13 |
| codestral | 88.5 | 100.0 | 80.0 | 91.5 | 90.00 |
| GPT-4o | 94.0 | 100.0 | 89.0 | 91.5 | 93.63 |
| llama-3 | 88.0 | 100.0 | 77.0 | 88.0 | 88.25 |
| Language গড় (আমার হিসাব) | 90.80 | 99.90 | 81.00 | 91.50 | |

(Table 8 pdftotext-এ কলাম গুলিয়ে ছিল; সারির ক্রম paper-এর টেক্সটের সংখ্যার সাথে মিলিয়ে নিশ্চিত করেছি: claude C 96%, GPT-4o C++ 89%, llama Java 88%, C++ 77%।)

### ৮.২ Semantic error-free rate (Table 8, ডান অর্ধেক, %)

| Model | Java | Python | C++ | C | গড় (আমার হিসাব) |
|---|---|---|---|---|---|
| claude-3.5 | 91.8 | 92.1 | 91.2 | 84.2 | 89.83 |
| gemini-1.5 | 89.5 | 90.5 | 81.0 | 77.0 | 84.50 |
| codestral | 82.9 | 88.6 | 83.7 | 73.7 | 82.23 |
| GPT-4o | 88.3 | 90.9 | 88.0 | 81.1 | 87.08 |
| llama-3 | 81.6 | 88.5 | 79.3 | 72.9 | 80.58 |
| Language গড় (আমার হিসাব) | 86.82 | 90.12 | 84.64 | 77.78 | |

### ৮.৩ Complexity (Table 10)

| Language | Model | LoC | CyC | CCD | CoC |
|---|---|---|---|---|---|
| Java | claude-3.5 | 6,480 | 1,097 | 0.17 | 891 |
| Java | gemini-1.5 | 5,606 | 965 | 0.23 | 902 |
| Java | codestral | 4,143 | 730 | 0.13 | 585 |
| Java | GPT-4o | 5,328 | 908 | 0.17 | 670 |
| Java | llama-3 | 4,993 | 913 | 0.18 | 809 |
| Java | Summary | 26,550 | 4,613 | 0.17 | 3,857 |
| Python | claude-3.5 | 3,474 | 895 | 0.26 | 881 |
| Python | gemini-1.5 | 3,064 | 765 | 0.37 | 881 |
| Python | codestral | 2,077 | 553 | 0.18 | 491 |
| Python | GPT-4o | 2,906 | 665 | 0.23 | 610 |
| Python | llama-3 | 2,633 | 677 | 0.26 | 631 |
| Python | Summary | 14,154 | 3,555 | 0.25 | 3,494 |
| C++ | claude-3.5 | 6,725 | 1,261 | 0.19 | 1,096 |
| C++ | gemini-1.5 | 5,822 | 1,084 | 0.25 | 1,044 |
| C++ | codestral | 4,293 | 825 | 0.14 | 732 |
| C++ | GPT-4o | 5,263 | 676 | 0.13 | 510 |
| C++ | llama-3 | 5,077 | 979 | 0.19 | 884 |
| C++ | Summary | 27,180 | 4,825 | 0.18 | 4,266 |
| C | claude-3.5 | 7,509 | 1,464 | 0.19 | 1,463 |
| C | gemini-1.5 | 6,555 | 1,256 | 0.28 | 1,331 |
| C | codestral | 4,532 | 894 | 0.14 | 869 |
| C | GPT-4o | 5,926 | 1,133 | 0.19 | 994 |
| C | llama-3 | 5,006 | 1,004 | 0.20 | 1,012 |
| C | Summary | 29,528 | 5,751 | 0.19 | 5,669 |

Total LoC = 26,550 + 14,154 + 27,180 + 29,528 = 97,412 (paper-এর সংখ্যার সাথে মেলে)। Python code সবচেয়ে ছোট (প্রতি program-এ গড় প্রায় 14.2 line, আমার হিসাব)। gemini/codestral সারির সমস্যা বিভাগ ৬.৩ ও ১২-তে।

### ৮.৪ Quality attribute (Table 11): S = security vulnerability, R = reliability, M = maintainability, SH = security hotspot

| Language | Model | S | R | M | SH |
|---|---|---|---|---|---|
| Java | claude-3.5 | 15 | 51 | 810 | 61 |
| Java | gemini-1.5 | 16 | 46 | 694 | 33 |
| Java | codestral | 12 | 37 | 535 | 40 |
| Java | GPT-4o | 13 | 52 | 925 | 76 |
| Java | llama-3 | 13 | 46 | 932 | 27 |
| Java | Summary | 69 | 232 | 3,896 | 237 |
| Python | claude-3.5 | 5 | 0 | 82 | 44 |
| Python | gemini-1.5 | 9 | 1 | 83 | 36 |
| Python | codestral | 9 | 1 | 50 | 39 |
| Python | GPT-4o | 8 | 0 | 75 | 43 |
| Python | llama-3 | 9 | 1 | 63 | 34 |
| Python | Summary | 40 | 3 | 353 | 196 |
| C++ | claude-3.5 | 9 | 6 | 590 | 36 |
| C++ | gemini-1.5 | 17 | 8 | 587 | 18 |
| C++ | codestral | 10 | 5 | 470 | 20 |
| C++ | GPT-4o | 7 | 6 | 459 | 17 |
| C++ | llama-3 | 10 | 10 | 565 | 18 |
| C++ | Summary | 53 | 35 | 2,671 | 109 |
| C | claude-3.5 | 19 | 60 | 449 | 186 |
| C | gemini-1.5 | 33 | 50 | 352 | 146 |
| C | codestral | 21 | 39 | 314 | 115 |
| C | GPT-4o | 27 | 37 | 380 | 133 |
| C | llama-3 | 22 | 54 | 322 | 182 |
| C | Summary | 122 | 240 | 1,817 | 762 |

(Table 11-ও গুলিয়ে ছিল; `pdftotext -raw` দিয়ে পুনরায় বের করেছি। প্রতিটি কলামের যোগফল Summary সারির সাথে মেলে: যেমন Java S 15+16+12+13+13 = 69।)

### ৮.৫ Language ও model অনুযায়ী normalised তুলনা (আমার হিসাব)

| Language | S মোট | LoC | S per KLoC | S per program | R per KLoC | M per KLoC | SH per KLoC |
|---|---|---|---|---|---|---|---|
| Java | 69 | 26,550 | 2.60 | 0.069 | 8.74 | 146.7 | 8.93 |
| Python | 40 | 14,154 | 2.83 | 0.040 | 0.21 | 24.9 | 13.85 |
| C++ | 53 | 27,180 | 1.95 | 0.053 | 1.29 | 98.3 | 4.01 |
| C | 122 | 29,528 | 4.13 | 0.122 | 8.13 | 61.5 | 25.80 |

| Model | S মোট (4 language) | LoC মোট | S per KLoC | M মোট | M per KLoC | R মোট | SH মোট |
|---|---|---|---|---|---|---|---|
| claude-3.5 | 48 | 24,188 | 1.98 | 1,931 | 79.8 | 117 | 327 |
| gemini-1.5 | 75 | 21,047 | 3.56 | 1,716 | 81.5 | 105 | 233 |
| codestral | 52 | 15,045 | 3.46 | 1,369 | 91.0 | 82 | 214 |
| GPT-4o | 55 | 19,423 | 2.83 | 1,839 | 94.7 | 95 | 269 |
| llama-3 | 54 | 17,709 | 3.05 | 1,882 | 106.3 | 111 | 261 |
| মোট | 284 | 97,412 | 2.92 | 8,737 | 89.7 | 510 | 1,304 |

প্রতি program 284 / 4,000 = 0.071 finding (আমার হিসাব)। এটি finding-এর সংখ্যা, vulnerable program-এর সংখ্যা নয়; paper দ্বিতীয়টি দেয়নি।

### ৮.৬ CWE breakdown (Table 12, কলাম ক্রম: claude, gemini, codestral, GPT-4o, llama)

| CWE | Java | Python | C++ | C |
|---|---|---|---|---|
| 780 (RSA without OAEP) | 6 7 4 8 4 (29) | 3 4 5 3 3 (18) | 0 7 3 1 0 (11) | 0 6 3 3 0 (12) |
| 259 (hard-coded password) | 2 2 2 1 4 (11) | 2 2 2 2 3 (11) | তালিকায় নেই | তালিকায় নেই |
| 22 (path traversal) | 3 3 2 2 3 (13) | 0 | | |
| 611 (XXE) | 2 2 2 2 1 (9) | 0 | 0 0 0 0 1 (1) | |
| 502 (deserialization) | 0 1 1 0 0 (2) | 0 | | |
| 295 (certificate validation) | 2 0 0 0 0 (2) | 0 | | |
| 79 (XSS) | 0 1 1 0 0 (2) | 0 0 1 1 2 (4) | | |
| 521 (weak password requirement) | 0 0 0 0 1 (1) | 0 1 1 2 1 (5) | | |
| 918 / 759 | 0 | 918: 1; 759: 1 | | |
| 295, 326, 327 (cert/crypto) | | | 9 8 6 5 7 (35) | 9 5 3 8 7 (32) |
| 297 (cert host mismatch) | | | 0 2 1 1 2 (6) | 1 2 1 2 3 (9) |
| 120 (buffer copy) | | | 0 0 0 0 0 (0) | 9 19 14 13 11 (66) |
| 131, 788 (buffer size/after end) | | | | 0 1 0 1 1 (3) |

প্রতি language-এর CWE যোগফল Table 11-এর S-এর সাথে মেলে (Java 69, Python 40, C++ 53, C 122; আমার যাচাই)। C-তে CWE-120 = 66/122 = 54.1%; C-তে crypto/certificate group = 32/122 = 26.2%; Java-তে CWE-780 = 29/69 = 42.0% (আমার হিসাব)।

### ৮.৭ Clean code (Table 13): C = consistency, I = intentionality, A = adaptability, R = responsibility

| Language | Model | C | I | A | R |
|---|---|---|---|---|---|
| Java | claude-3.5 | 0 | 203 | 532 | 10 |
| Java | gemini-1.5 | 0 | 244 | 387 | 9 |
| Java | codestral | 0 | 181 | 182 | 6 |
| Java | GPT-4o | 8 | 148 | 392 | 9 |
| Java | llama-3 | 61 | 200 | 360 | 9 |
| Java | Summary | 69 | 976 | 1,853 | 43 |
| Python | claude-3.5 | 54 | 23 | 5 | 5 |
| Python | gemini-1.5 | 47 | 34 | 5 | 7 |
| Python | codestral | 35 | 17 | 1 | 7 |
| Python | GPT-4o | 47 | 27 | 4 | 5 |
| Python | llama-3 | 51 | 15 | 1 | 6 |
| Python | Summary | 234 | 116 | 16 | 30 |
| C++ | claude-3.5 | 116 | 438 | 42 | 9 |
| C++ | gemini-1.5 | 136 | 421 | 40 | 15 |
| C++ | codestral | 117 | 335 | 24 | 9 |
| C++ | GPT-4o | 93 | 334 | 39 | 6 |
| C++ | llama-3 | 121 | 408 | 49 | 7 |
| C++ | Summary | 583 | 1,936 | 194 | 46 |
| C | claude-3.5 | 162 | 321 | 36 | 9 |
| C | gemini-1.5 | 188 | 197 | 38 | 11 |
| C | codestral | 155 | 186 | 27 | 6 |
| C | GPT-4o | 197 | 210 | 25 | 11 |
| C | llama-3 | 160 | 205 | 25 | 7 |
| C | Summary | 862 | 1,119 | 151 | 44 |

### ৮.৮ Compile error ধরন (Table 9, গুণগত)

- সবচেয়ে সাধারণ: library/import error ("cannot find symbol", যেমন java.util.∗ ভুলে যাওয়া)।
- Java: exception handling (gemini, codestral, llama-3 বেশি), missing class/member (codestral), syntax (প্রধানত codestral), type compatibility।
- C++: missing include, type handling, STL ও C++11 বনাম C++17 পার্থক্য, binding/qualifier error (সংখ্যা: claude 20, gemini 8, codestral 4, GPT-4o 11, llama-3 22 — table garbled, আমার পড়া)।
- C: undeclared type (bool), missing header (cgi/cgi.h), function argument ভুল; llama-3 সবচেয়ে খারাপ (88.0%)।
- Table 9 pdftotext-এ ঠিকভাবে বের হয়নি, তাই এর অন্য সংখ্যা এখানে দিচ্ছি না।

## ৯. Key findings

1. **Python-এ compile সবচেয়ে ভালো:** Python-এ 4টি model 100.0%, claude-3.5 99.5%। C++ সবচেয়ে কঠিন: 77.0% (llama-3) থেকে 89.0% (GPT-4o)।
2. **Semantic correctness language-এর উপর নির্ভর করে:** Python গড় 90.12%, Java 86.82%, C++ 84.64%, C 77.78% (আমার হিসাব)। C-তে সর্বোচ্চ 84.2% (claude-3.5), সর্বনিম্ন 72.9% (llama-3)।
3. **C-তে security সবচেয়ে খারাপ:** 122 finding (প্রতি program 0.122, Java-র 1.77 গুণ, Python-এর 3.05 গুণ, আমার হিসাব)। এর 66টি CWE-120।
4. **Crypto misuse সব language-এ আছে:** CWE-780 Java 29, Python 18, C++ 11, C 12; certificate/crypto (CWE-295/326/327) C++ 35, C 32।
5. **gemini-1.5 সবচেয়ে বেশি vulnerability দেয়:** 75 (মোট 284-র 26.4%), বিশেষ করে C-তে 33 ও C++-এ 17। claude-3.5 সর্বনিম্ন: 48 (আমার যোগ)।
6. **Correctness ও security আলাদা:** claude-3.5 correctness-এ প্রথম (89.83% গড়) এবং vulnerability-তেও সবচেয়ে কম (48), কিন্তু সবচেয়ে বেশি LoC (24,188), maintainability issue (1,931) ও সবচেয়ে বেশি security hotspot (327)। gemini-1.5 correctness-এ দ্বিতীয় (84.50%) অথচ vulnerability-তে সর্বাধিক (75)।
7. **Raw count LoC-এ প্রভাবিত:** codestral সবচেয়ে কম maintainability issue (1,369) দেখায় কারণ সবচেয়ে কম code (15,045 line) লিখে; per-KLoC ধরলে claude-3.5 (79.8) সবচেয়ে ভালো, codestral 91.0 (আমার হিসাব)।
8. **Modern feature অব্যবহৃত:** Java 17 থাকা সত্ত্বেও model পুরনো random number generation ব্যবহার করে; C++ এ srand/rand (paper-এর Conclusion ও Appendix C.4)।

## ১০. Alternatives-এর চেয়ে কেন ভালো

- **Multi-language, multi-model, একই prompt:** আগের কাজ (Pearce, Copilot, SecurityEval Python-only) এক model বা এক language। এখানে same task, same environment তাই পার্থক্য language ও model-এর কারণে।
- **Function signature ছাড়া prompt:** বাস্তব ব্যবহারের মতো; তবে এর দাম হলো প্রতি program-এর জন্য আলাদা test (800+ person-hour)।
- **Correctness + quality + security একসাথে:** আগের কাজ প্রায়ই একটি অক্ষ মাপে (Table 2)। এখানে trade-off দেখা যায়।
- **Tool cross-check ও manual review:** একক SAST-এর false positive-এর সমস্যা (Lenarduzzi et al.: ছয়টি tool-এর overlap কম) মোকাবিলা করতে SonarQube + CodeQL।
- **Open data:** dataset, prompt, test, script প্রকাশিত; model-agnostic adapter-এর মাধ্যমে নতুন model-এ পুনরায় চালানো যায়।
- আমার মন্তব্য: এই সুবিধাগুলো "বিস্তার"-এর; গভীরতা (কারণ-বিশ্লেষণ, statistical test) কম।

## ১১. কখন কাজ করে / কখন ব্যর্থ

**কাজ করে:**
- ছোট, self-contained, single-file task-এ cross-language তুলনা।
- Crypto misuse, hard-coded secret, buffer copy-র মতো pattern-ভিত্তিক weakness ধরতে (SAST-এর শক্তির জায়গা)।
- নতুন model-এ ঢুকিয়ে baseline হিসেবে।

**ব্যর্থ বা অনিশ্চিত:**
- Multi-file, repository-level, বা agent-লেখা patch (paper নিজেই বলে system-level security মাপা হয়নি)।
- Business-logic ও authentication flow-এর মতো semantic vulnerability, যা pattern-ভিত্তিক SAST ধরে না।
- Runtime vulnerability (dynamic analysis ও fuzzing নেই; paper future work বলেছে)।
- Multi-turn, IDE-ভিত্তিক, prompt-refinement সহ ব্যবহার।
- Model আপডেট হলে সংখ্যা বদলে যাবে (paper নিজে "time-stamped snapshot" বলে)।

## ১২. Limitations

### ১২.১ Authors-এর স্বীকৃত

- SonarQube-এর false positive ও semantic বোঝার অভাব; unit test অসম্পূর্ণ হলে defect ধরা পড়ে না।
- Non-deterministic decoding (temperature 0.9) stochasticity আনে।
- Per-sample test তৈরিতে manual adaptation-এর subjectivity।
- Task ছোট ও self-contained; system-level security নয়।
- Single-turn generation; multi-turn বা collaborative নয়।
- Model version ঠিক করা; ভবিষ্যৎ আপডেটে reproducibility ক্ষুণ্ন হতে পারে।
- Semantic similarity automated নয়, manual; dynamic analysis ও fuzzing নেই।

### ১২.২ আমার পর্যবেক্ষণ (paper-internal অসঙ্গতিসহ)

1. **Header:** "IEEE TDSC Vol. 14, No. 8, August 2015" template placeholder; আসল status arXiv v2 (March 2026)।
2. **Abstract বনাম Table 11/12:** abstract বলে "Python and Java ... fewer security findings than C and C++"। কিন্তু raw count-এ Java 69 > C++ 53। প্রতি KLoC-তে Python (2.83) > Java (2.60) > C++ (1.95)। শুধু C স্পষ্টভাবে খারাপ (4.13)। সুতরাং claim আংশিক সত্য।
3. **Abstract বনাম Table 12:** abstract বলে C ও C++-এ "memory safety issues, hard-coded secrets" বেশি। কিন্তু Table 12-এ C++-এ CWE-120 = 0 এবং CWE-259 (hard-coded) শুধু Java ও Python-এর তালিকায়; C ও C++ এ নেই। C++-এর প্রধান finding crypto/certificate (35)।
4. **Manual review-র পরিমাণ:** বিভাগ ৩.৫.৩ বলে সব reported vulnerability manual যাচাই এবং stratified 20% sample; বিভাগ ৬ ও ৫.৫ বলে "approximately 20% of tasks"। কোনটি সঠিক স্পষ্ট নয়।
5. **LoC বনাম CCD অসঙ্গতি:** Table 10-এ gemini-1.5 ও codestral সারি চারটি language-এই CCD = CyC / LoC মেলে না (বিভাগ ৬.৩)। এছাড়া বিভাগ ৫.২ Python-এ gemini LoC 2,077 বলে, অথচ বিভাগ ৫.৩ ও Table 10 codestral-কে 2,077 দেয়।
6. **Text বনাম Table (C++):** বিভাগ ৫.৩ বলে claude-3.5 C++-এ "few security hotspots (36)" ও "strong security"; কিন্তু 36 C++-এ সর্বোচ্চ (বাকি 18, 20, 17, 18)। আবার "codestral fewest maintainability (470) and hotspots (20)" বলে, অথচ GPT-4o-র 459 ও 17 আরও কম।
7. **Text বনাম Table (C, reliability):** "codestral scores lower in reliability (39)" লেখা আছে; R একটি issue-গণনা, তাই 39 কম issue মানে ভালো; ভাষা বিভ্রান্তিকর।
8. **Conclusion বনাম Table 13:** Conclusion বলে Python ও C++ "gaps in adaptability and responsibility"। কিন্তু Python-এ adaptability issue সবচেয়ে কম (16), Java-তে সবচেয়ে বেশি (1,853)। Java-কে "stronger intentionality" বলাও টেবিলের (976 issue) সাথে মেলে না।
9. **Python compile:** টেক্সট "three LLMs achieve 100%" বলে, Table 8-এ চারটি model 100.0%।
10. **Semantic > compile:** কয়েকটি cell-এ semantic rate compile rate-এর চেয়ে বেশি (llama-3 C++: 79.3 > 77.0; gemini C++: 81.0 > 77.5; codestral C++: 83.7 > 80.0)। compile ব্যর্থ file যদি 0 গণ্য হতো, তা সম্ভব হতো না। তাই compile ব্যর্থ file ঠিক করে/বাদ দিয়ে test চালানো হয়েছে ("limited manual fixes")। এতে semantic rate-এর denominator ও manual বাড়তি সাহায্যের প্রভাব অস্পষ্ট।
11. **"Semantic error-free" সংজ্ঞা অস্পষ্ট:** গড় test score, না সব test পাস করা program-এর শতাংশ।
12. **Statistics নেই:** প্রতি cell-এ 200 sample, একবার generation, CI বা paired test নেই। Java-তে claude 15 বনাম gemini 16 vulnerability আলাদা করা যায় না।
13. **SAST validity:** SonarQube-এর কত finding CodeQL নিশ্চিত করেছে, false positive রেট কত, তার সংখ্যা নেই। CodeQL-এর আলাদা count-ও নেই।
14. **Per-category ফল নেই:** 7টি category ও 86 CWE tag করা হলেও ফল category-অনুযায়ী (বা CWE-লক্ষ্য task-এ hit rate) দেওয়া হয়নি। 102 secure-coding task-এ কত শতাংশ vulnerable, জানা যায় না।
15. **Contamination:** LeetCode, Codewars, Edabit থেকে 64টি public task; model training data-য় থাকতে পারে; paper এ কথা বলেনি।
16. **Model ও API অস্পষ্টতা:** Table 3-এর source link web chat page (claude.ai, gemini.google.com), যদিও "stable API" বলা; llama-3 Perplexity-র sonar model, মূল Llama 3 নয়।
17. **Prompt-এ security নির্দেশ নেই:** model-কে "secure" করতে বলা হয়নি; তাই "default behaviour" মাপা হয়েছে, secure-prompt-এর সাথে তুলনা নেই।
18. **Reference-এ "Asare et al. [?]"** (Table 1) — একটি অমীমাংসিত citation।

## ১৩. Research gaps

| G-id | Gap | Evidence | Related CG / folder |
|---|---|---|---|
| G1 | Function/file-level code, agent patch নয়; patch-এ নতুন করে আনা finding (before/after diff) মাপা হয়নি | Section 6 external validity; tasks self-contained | CG5, CG1 / 06_Security_of_AI_Code |
| G2 | SAST-এর precision/recall ও tool-agreement সংখ্যা নেই | Section 3.5.3 (20% বনাম সব); CodeQL-এর আলাদা count নেই | CG10, নতুন CG20 |
| G3 | Raw count বনাম density; vulnerable-program rate নেই | Table 11 (S মোট 284, program-ভিত্তিক rate নেই) | CG8, নতুন CG21 |
| G4 | Single sample, temperature 0.9, CI/ significance test নেই | Table 4, 200 sample per cell | CG4, CG8 |
| G5 | Language-নির্ভরতা শুধু 4 language, কারণ-নির্ণয় নেই | Section 5.1 (তত্ত্ব, পরীক্ষা নয়) | CG9 / 06_Security_of_AI_Code |
| G6 | Correctness ও security-র সম্পর্ক পরিমাণগতভাবে বিশ্লেষিত নয় | claude বনাম gemini (বিভাগ ৯, ৬) | CG5 |
| G7 | Dynamic analysis, fuzzing, sanitizer নেই | Future Work | CG5, CG15 |
| G8 | Dataset contamination ও per-category/CWE ফল নেই | 64 public-site task; Table 6 শুধু distribution | CG6 |
| G9 | Multi-turn, prompt-এ security নির্দেশ, ও self-repair ফলাফল অপরীক্ষিত | Section 6 conclusion validity | CG1, CG7 |
| G10 | Quality metric-এর মান (SonarQube smell) কতটা maintainability-র প্রকৃত সূচক, তার validation নেই | Section 3.5.4 (definition-ই tool-এর rule) | CG10 |

## ১৪. Improvement ideas

- Finding-কে LoC, program ও task-সংখ্যার সাথে normalise করা এবং CI সহ report করা।
- Per-task paired analysis: একই task-এ model/language-এর পার্থক্য McNemar বা bootstrap দিয়ে।
- Temperature 0 বা একাধিক seed (pass@k-এর মতো) দিয়ে variance মাপা।
- SAST triage: Semgrep যোগ (paper নিজেই বলেছে), tool-ভিত্তিক agreement ও manual label-এর precision/recall।
- Dynamic oracle: sanitizer (ASan/UBSan) ও fuzzing C/C++ এর জন্য, যা CWE-120 ঠিক ধরবে।
- Patch-mode: agent-এর patch-এর আগে ও পরে scan করে "নতুন finding" গণনা।
- Secure prompt ও self-repair তুলনা (paper-এর future work + আগের কাজে পাওয়া "follow-up prompt-এ উন্নতি")।
- Per-CWE hit rate: নির্দিষ্ট CWE-লক্ষ্য task-এ কত শতাংশ vulnerable।

## ১৫. Publication potential (SPL3-feasible)

- **সম্ভাব্য কাজ:** "Security and quality of AI-agent patches" — SWE-bench-জাতীয় patch-এ before/after SAST diff, correctness-এর সাথে তুলনা। এটি এই paper-এর function-level সীমাবদ্ধতা সরায়।
- **Venue ধরন:** workshop বা student track (MSR challenge, ICSE/ASE workshop, SANER short); journal-এ যেতে হলে statistical rigor ও একাধিক model দরকার।
- **SPL3-feasible অংশ:** Python (এবং সম্ভব হলে Java) patch-এ Semgrep + CodeQL চালানো; ছোট sample (পঞ্চাশ থেকে একশ patch); per-patch finding-delta ও CWE ম্যাপিং।
- **Novelty:** patch-level security delta ও "plausible ≠ secure" (Sub-domain 2-এর VRpilot-এর ধারণা) যুক্ত।
- **ঝুঁকি:** SAST noise; correct label-এর অভাব; model API খরচ।

## ১৬. SPL3 implementation

**Assurance report-এর security/quality অংশ (প্রস্তাব, আমার ডিজাইন):**

1. **Input:** repository + patch (agent output)।
2. **Baseline scan ও patched scan:** একই tool, একই rule-version; শুধু patch-এ নতুন finding গণনা করে ("introduced")। আগে থেকে থাকা finding আলাদা।
3. **Tool (paper থেকে):** CodeQL (C/C++, Java, Python সমর্থিত), SonarQube (সব চার language; ভারী, CI-ভিত্তিক), এবং Semgrep (paper future work; হালকা)। প্রতিটির নাম ও version report-এ।
4. **CWE checklist (Table 12 থেকে অগ্রাধিকার):**
   - Crypto: CWE-780 (RSA without OAEP), 295/297/326/327, 521, 759।
   - Secret: CWE-259 (hard-coded password)।
   - Input/Injection: CWE-22, 79, 611 (XXE), 502, 918, 89, 78।
   - Memory (C/C++): CWE-120, 131, 788, 416, 787, 125।
   - Deprecated API: non-secure random (rand/srand, java.util.Random) — paper-এর C.4।
5. **Language-অনুযায়ী profile (CG9):** C/C++ → memory + sanitizer; Java/Python → crypto, XXE, path traversal, secret। Threshold language-ভেদে আলাদা, কারণ C-তে baseline density 4.13/KLoC এবং C++-এ 1.95/KLoC (আমার হিসাব)।
6. **Quality signal আলাদা (CG5):** reliability, maintainability, cognitive complexity delta, clean code — কোনো single weighted score ছাড়া। correctness (test pass) আলাদা কলামে।
7. **Normalisation:** finding per KLoC-changed, এবং delta। Count একা দেখানো যাবে না।
8. **Uncertainty:** প্রতিটি tool-finding-এর জন্য "confirmed / unconfirmed / hotspot"; "could not scan" একটি স্পষ্ট ফলাফল।
9. **Manual audit:** একটি ছোট stratified নমুনা (paper-এর 20% ধারণা) হাতে যাচাই করে SAST precision মাপা।
10. **Cost:** SAST চালানো সস্তা (LLM খরচ নেই); paper-এ test লেখার 800+ person-hour দেখায় manual test scale হয় না, তাই আমরা existing repo test ব্যবহার করব, নতুন per-program test নয়।

## ১৭. পূর্ববর্তী sub-domain-এর সাথে সম্পর্ক

- **Sub-domain 1 (SWE-bench, SWE-agent, AutoCodeRover, Agentless):** সেখানে patch "resolved" শুধু test দিয়ে; এই paper দেখায় test-pass-এর পাশে security ও quality আলাদা মাপতে হয় (CG5)।
- **Sub-domain 2 (APR: VRpilot, RePaCA):** VRpilot-এর "sanitizer pass ≠ secure" এবং এই paper-এর "high semantic correctness ≠ secure" একই দিকে। এখানে SAST-এর নির্দিষ্ট CWE তালিকা পাওয়া যায়।
- **Sub-domain 3 (Evaluation):** SWE-rebench-এর variance ও contamination সমস্যা এই paper-এও আছে (single run, public site task)। CG4, CG6, CG8-এর সাথে মেলে।
- **Sub-domain 4 (Test generation):** coverage ≠ oracle; এই paper-এর 75%+ coverage একই সীমা বহন করে (CG13)।
- **Sub-domain 5 (Patch validation):** HITL LLM-as-a-Judge ও Harden and Catch-এর মতো, SAST-ও একটি আলাদা signal যার precision মাপতে হয় (CG10, CG17)।
- **Direction update:** assurance report-এর "security scan" মডিউল এই paper থেকে CWE ও tool-list পায়।

## ১৮. Supervisor Q&A

**প্র১: Paper-এর venue কী?**
উ: Header-এ "IEEE TDSC Vol. 14 No. 8 Aug 2015" আছে, কিন্তু reference-এ 2025 তারিখ থাকায় এটি template। প্রকৃত অবস্থান arXiv:2502.01853v2 (9 March 2026)। journal-এ গৃহীত কি না paper বলেনি।

**প্র২: কোন model ও কোন language?**
উ: GPT-4o-202407, claude-3-5-sonnet-20240620, gemini-1.5-pro-001, codestral-2405, llama-3-sonar-large-32k-chat; Python, Java, C++, C। সব 2024-এর model।

**প্র৩: কোন language সবচেয়ে ঝুঁকিপূর্ণ?**
উ: C: 122 finding, প্রতি program 0.122; Java 0.069, C++ 0.053, Python 0.040 (আমার হিসাব)। তবে প্রতি KLoC-তে Python (2.83) Java (2.60) ও C++ (1.95)-এর চেয়ে বেশি; তাই "Python ও Java নিরাপদ" দাবিটি normalisation-এর উপর নির্ভর করে।

**প্র৪: কোন CWE সবচেয়ে বেশি?**
উ: C-তে CWE-120 (66টি); Java ও Python-এ CWE-780 (29 ও 18); C/C++ এ crypto/certificate group (35 ও 32)।

**প্র৫: Correctness বেশি মানে কি security বেশি?**
উ: না। claude-3.5 দুটিতেই ভালো, কিন্তু gemini-1.5 correctness-এ দ্বিতীয় (84.50% গড়) অথচ vulnerability-তে প্রথম (75)। তাই আমরা দুটি আলাদা signal রাখব।

**প্র৬: সংখ্যাগুলো কতটা নির্ভরযোগ্য?**
উ: প্রতি cell 200 sample, একবার generation (temperature 0.9), CI নেই। আমার হিসাবে $n=200$-এ 80% rate-এ প্রায় ±5.5 pp। কয়েকটি table-সংখ্যা paper-এর লেখার সাথে মেলে না (বিভাগ ১২)।

**প্র৭: SAST কতটা সঠিক?**
উ: paper false positive rate দেয়নি। SonarQube vulnerability CodeQL-এর সাথে cross-check করা হয়েছে বলা হলেও agreement-এর সংখ্যা নেই। আমাদের project-এ নিজেদের নমুনা যাচাই দরকার (CG20)।

**প্র৮: আমাদের project-এ কীভাবে কাজে লাগবে?**
উ: assurance report-এর security ও quality অংশে CWE চেকলিস্ট, tool-list (CodeQL, SonarQube, Semgrep), language profile এবং "correctness আলাদা" নীতি; কিন্তু file-level নয়, patch-diff-ভিত্তিক scan।

## ১৯. Glossary

| শব্দ | অর্থ |
|---|---|
| CWE | Common Weakness Enumeration, weakness-এর শ্রেণি |
| SAST | Static code scan |
| SonarQube | Quality ও security rule engine, hotspot ধারণা সহ |
| CodeQL | Query-ভিত্তিক code analysis |
| Security hotspot | মানুষের দেখার মতো sensitive code অংশ, নিশ্চিত vulnerability নয় |
| CyC | Cyclomatic complexity |
| CCD | CyC ÷ code line |
| CoC | Cognitive complexity |
| OAEP | RSA-এর নিরাপদ padding |
| XXE | XML External Entity attack (CWE-611) |
| ReDoS | Regex-ভিত্তিক denial of service (Appendix C.5) |
| KLoC | হাজার line of code |
| pp | percentage point |

## ২০. Summary card

| বিষয় | সারাংশ |
|---|---|
| Paper | Security and Quality in LLM-Generated Code (Kharma et al.; arXiv 2502.01853v2, March 2026) |
| ধরন | Measurement study; 200 task × 4 language × 5 model = 4,000 program |
| Tool | SonarQube, CodeQL, unit test (4,000 file), JaCoCo coverage |
| Compile | Python 99.9% গড়, C++ 81.0% গড় (আমার হিসাব) |
| Semantic | Python 90.12%, C 77.78% গড় (আমার হিসাব) |
| Security | মোট 284: Java 69, Python 40, C++ 53, C 122 |
| শীর্ষ CWE | C: CWE-120 (66); Java: CWE-780 (29) |
| Model | gemini-1.5 সবচেয়ে বেশি vulnerability (75); claude-3.5 কম (48) কিন্তু সবচেয়ে বেশি LoC |
| দুর্বলতা | একবার generation, CI নেই, SAST precision নেই, table অসঙ্গতি, file-level only |
| আমাদের জন্য | CWE ও tool তালিকা, language profile, quality আলাদা signal, patch-diff scan |

## ২১. বর্তমান (2026) প্রেক্ষাপট

### ২১.১ তখন বনাম এখন

| বিষয় | Paper (2024 model) | এখন (context.md থেকে) |
|---|---|---|
| Model | GPT-4o, claude-3.5, gemini-1.5, codestral, llama-3 | Claude Opus 5.5, Fable 5.1, Sonnet 5.5, GPT-6 পরিবার, Gemini 4 Argon, Kimi K3.1 Pro, GLM-5.x, DeepSeek V4 |
| Functional বনাম security | Functional 72.9%–92.1%; security finding প্রতি program 0.04–0.122 (আমার হিসাব) | SusVibes: FuncPass 62%–84%, SecPass 7.8%–17.3% (independent, Opus 4.6/GPT-5.4 যুগ) |
| Task ধরন | ছোট, self-contained | repository-level, agent patch (SWE-bench Pro ইত্যাদি) |
| Prompt injection | আলোচিত নয় | Opus 5.5: 54.61% (safeguard ছাড়া) বনাম 11.13% (safeguard সহ), vendor-reported |
| Cheat/gaming | আলোচিত নয় | METR: সফল long-task run-এর ≥16% cheat (independent, আগের generation); Opus 5.5 card-এ "hidden tests" reasoning (vendor) |
| Current model-এ এই ধরনের multi-language SAST study | — | বর্তমান model-এর তথ্য পাওয়া যায়নি |

### ২১.২ এখনও সত্য / পুরনো

**এখনও সত্য (paper নিজেও বলে):** Python/Java-তে compile ও correctness বেশি, C/C++ কঠিন; crypto misuse ও hard-coded secret-এর মতো pattern সহজে টিকে থাকে; "functional correctness ≠ security" (SusVibes-এ আরও বড় ব্যবধান: independent)।

**সম্ভবত পুরনো:** নির্দিষ্ট সংখ্যা ও model র‍্যাংকিং (paper নিজেই বলে snapshot); 4,096 token, single-turn, ছোট task; SWE-bench Verified-ধরনের পুরনো benchmark এখন saturated (Vals.ai 97.0%, independent) তাই এই ছোট-task পরিমাপ এখন সহজ হতে পারে। 2026 model-এ এই paper-এর সংখ্যা বসানো যাবে না (বর্তমান model-এর তথ্য পাওয়া যায়নি)।

### ২১.৩ আজও খোলা gap

| Gap | বর্তমান অবস্থা (context.md অনুযায়ী) | Related |
|---|---|---|
| Current model-এর multi-language SAST ফল | SusVibes/BaxBench-এ current model-এর ডেটা নেই | G1, G5 |
| Patch-level security delta | SWE-bench-এ প্রচলিত resolve rate কোনো security signal দেয় না | CG5 |
| SAST validity (precision) | কোনো সংখ্যা নেই; judge "over-fix" flags 5–10% precision (search-snippet only) আলাদা বিষয় | CG10, CG20 |
| Variance | pass@1 বনাম pass@5 gap 12–18 pts (SWE-rebench, independent) | G4 |
| Gaming of the signal | agent scanner/test-কে ফাঁকি দিতে পারে (METR, vendor card) | CG12 |

### ২১.৪ SPL3 idea (current model-এ, cost-aware)

- **Idea:** 2–3টি current model (দাম অনুযায়ী) দিয়ে ছোট patch set তৈরি; প্রতিটি patch-এ Semgrep + CodeQL before/after scan; correctness test আলাদা; ফল language-ভেদে।
- **খরচ:** SAST-এ LLM খরচ নেই, খরচ শুধু patch generation। দামের একমাত্র সূত্র context.md-এ Vals Terminal-Bench 4.0: Opus 5.5 প্রতি task 13.20 USD, Kimi K3.1 Pro 4.57 USD, GPT-6.1 Sol 1.72 USD (independent)। এটি অন্য benchmark, তাই এই paper-এর task-এর খরচ সরাসরি অনুমান করা যাবে না (আমার সতর্কতা)।
- **পরিকল্পনা:** প্রথমে সস্তা model দিয়ে pilot (ত্রিশ-চল্লিশ task), তারপর ছোট নমুনায় ব্যয়বহুল model; সব run-এর tool ও rule version লিখে রাখা।
- **Variance:** প্রতি task-এ একাধিক run (SWE-rebench-এর 5-run পদ্ধতির মতো), CI সহ।

### ২১.৫ তিনটি Q&A

**প্র১: এই 2024-এর paper কি এখনও প্রাসঙ্গিক?**
উ: পদ্ধতি ও CWE তালিকা হ্যাঁ; সংখ্যা ও র‍্যাংকিং না। বর্তমান model-এর তথ্য পাওয়া যায়নি, তাই আমরা নতুন করে চালাব।

**প্র২: Current model-এ কি security ভালো হয়েছে?**
উ: context.md-তে সবচেয়ে কাছের তথ্য SusVibes (independent): FuncPass 62%–84%, SecPass 7.8%–17.3% (Opus 4.6/GPT-5.4 যুগ)। Opus 5.5 বা GPT-6-এ SusVibes/BaxBench-এর ডেটা নেই; তাই দাবি করা যাবে না।

**প্র৩: SPL3-তে সবচেয়ে বড় ঝুঁকি কী?**
উ: SAST noise ও label-এর অভাব। সমাধান: নমুনা manual audit, tool-version লেখা, এবং "নিশ্চিত নয়" একটি আলাদা ফলাফল রাখা।
