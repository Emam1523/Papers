# Paper Analysis 01 (TestGen): UniTSyn — A Large-Scale Dataset for LLM-based Program Testing

> **Sub-domain:** LLM Test Generation (৪র্থ sub-domain-এর প্রথম paper)
> **Analysis করেছে:** SPL3 — AI Coding Agent Reliability and Assurance
> **Paper file:** `LLM Test Generation/A Large-Scale Dataset Capable of Enhancing the Prowess of Large.pdf`
> **কেন এই sub-domain:** আমাদের assurance layer-এর **dynamic signal** হলো generated test (CG1, CG3)। তাই এই paper পড়ার সময় মূল প্রশ্ন: "LLM-এর লেখা test কতটা সঠিক, কতটা চলে, আর কতটা bug ধরতে পারে?"

---

## ০. Paper-এর পরিচয় (Bibliographic Info)

| বিষয় | তথ্য |
|---|---|
| **Title** | UniTSyn: A Large-Scale Dataset Capable of Enhancing the Prowess of Large Language Models for Program Testing |
| **Authors** | Yifeng He, Jiabo Huang, Yuyang Rong, Yiwen Guo, Ethan Wang, Hao Chen |
| **Institution** | UC Davis (He, Rong, Wang, Chen); Tencent Security Big Data Lab (Huang); Independent Researcher (Guo — corresponding author) |
| **Version / Venue** | arXiv:2402.03396v1 [cs.SE], 4 February 2024। PDF-টা ICML 2024-এর LaTeX template-এ লেখা (PDF metadata-তে keyword "Machine Learning, ICML", আর একটা "Impact Statements" অংশ আছে), এবং paper বলছে code ও data "upon acceptance" release হবে — অর্থাৎ এই version-টা **under-review preprint**। কোন venue-তে শেষ পর্যন্ত গৃহীত হয়েছে তা **এই PDF থেকে নির্ধারণ করা যায় না** — supervisor-কে দেখানোর আগে arXiv/DBLP-তে যাচাই করতে হবে |
| **Paper type** | **Dataset paper + dataset-building framework** (সাথে dataset-এর মান প্রমাণের জন্য একটা model, UniTester) |
| **Artifacts (দাবি)** | 2.7M focal-test pair (5টা language), tree-sitter + LSP-ভিত্তিক collection framework, UniTester (1.1B) model। v1-এ "Code and data will be publicly available" — তখনো release হয়নি |
| **আমাদের domain-এ গুরুত্ব** | ⭐⭐⭐ — সরাসরি patch assurance নিয়ে নয়, কিন্তু (১) **test-to-code linking** (কোন test কোন function-কে test করে) LSP দিয়ে করার পদ্ধতি আমাদের "patch-এর সাথে প্রাসঙ্গিক test খোঁজা" কাজে লাগবে; (২) এর evaluation দেখায় LLM-generated test-এর **accuracy ও executability কত কম** — এটাই আমাদের dynamic signal-এর সীমা |

---

## ১. এক লাইনে Paper (TL;DR)

**UniTSyn হলো GitHub-এর 5টা language (Python, Java, Go, C++, JavaScript)-এর প্রায় 1.45 লাখ project থেকে tree-sitter (parsing) আর Language Server Protocol (definition খোঁজা) ব্যবহার করে, কোনো project execute না করেই, 2.7 million "test function ↔ যে function-কে test করছে (focal function)" জোড়া সংগ্রহ করা একটা dataset; এর উপর 1.1B SantaCoder-কে আরও train করে বানানো UniTester HumanEval-X-এ test-এর assertion accuracy 33.9% থেকে 51.5%-এ তুলেছে।**

### Supervisor-কে ৩০ সেকেন্ডে কীভাবে বলবো
> "Sir, LLM দিয়ে unit test লেখাতে গেলে model-কে জানতে হয় কোন function-কে test করছে আর তার সঠিক output কী। কিন্তু সাধারণ code LLM-এর training data-তে test আর তার target function আলাদা আলাদা snippet হিসেবে থাকে — জোড়া বাঁধা থাকে না। আগের কাজগুলো এই জোড়া বাঁধতো হয় project চালিয়ে (dynamic analysis — scale করে না, যেমন TeCo মাত্র 1,270টা Java project), নয়তো file-level-এ (দুর্বল জোড়া, যেমন CAT-LM)। UniTSyn editor-এর 'Go to Definition' feature-এর পেছনের protocol — LSP — ব্যবহার করে function-level জোড়া বানায়, কোনো project build বা run না করেই, আর নতুন language যোগ করতে প্রায় শুধু language server চালু করার command লাগে। 2.7M জোড়ায় train করা 1.1B model HumanEval-X-এ test accuracy-তে 2.7B CAT-LM-কেও ছাড়িয়েছে। তবে আমাদের জন্য সবচেয়ে গুরুত্বপূর্ণ খবর হলো সতর্কবার্তা: সেরা model-এরও অর্ধেকের মতো assertion ভুল, আর গড়ে মাত্র ~32% test error ছাড়া চলে।"

---

## ২. Background — এই paper বুঝতে যা আগে জানা দরকার

### ২.১ Unit Test
একটা ছোট function, যেটা আরেকটা function-কে নির্দিষ্ট input দিয়ে call করে দেখে output ঠিক আছে কিনা। Paper-এর Listing 1-এর Java উদাহরণ:
```java
@Test
public void testAdd() {
  int x = 500;  int offsetX = 100;
  int y = 700;  int offsetY = 200;
  Position mp = new Position(x, y);
  Position result = mp.add(offsetX, offsetY);
  assertEquals(mp.x + offsetX, result.x);
}
```
একটা unit test-এর তিনটা অংশ: **setup** (variable ও object বানানো), **call** (যে function test করা হচ্ছে তাকে ডাকা), **check** (assertion)।

### ২.২ Focal Function
যে function-টাকে test আসলে পরীক্ষা করছে, তাকে **focal function** বলে (Tufano et al.-এর শব্দ)। উপরের উদাহরণে `new Position(...)` setup-এর জন্য, কিন্তু focal function হলো `add` (line 6)। **Focal-test pair** = (focal function-এর code, test function-এর code)।

### ২.৩ Test Oracle ও Assertion
- **Test oracle:** "সঠিক output কী হওয়া উচিত" — এই সিদ্ধান্ত। Oracle ছাড়া test শুধু code চালায়, ভুল ধরে না।
- **Assertion:** oracle-কে code-এ লেখার উপায় — `assert f(2) == 4`, `assertEquals(...)`, `assert.Equal(...)`, `console.assert(...)`।
- **কেন test generation, code generation-এর চেয়ে কঠিন (paper-এর যুক্তি):** test লিখতে শুধু চলমান code নয়, input-এর জন্য **একদম সঠিক output-এর prediction** লাগে। ভুল expected value দিলে সঠিক code-ও "fail" দেখাবে।
- **Weak oracle:** এমন assertion যা প্রায় কিছুই যাচাই করে না (যেমন শুধু "output None নয়")। আমাদের fact sheet অনুযায়ী আজকের agent-দের লেখা test patch-এর 80.2%-এ weak বা কোনো স্পষ্ট oracle নেই (Section ২১ দেখো)।

### ২.৪ Test-to-Code Linking (Focal-Test Alignment)
একটা test কোন production function-কে test করছে, তা স্বয়ংক্রিয়ভাবে বের করা। তিনটা পদ্ধতি paper-এ আলোচিত:
| পদ্ধতি | কীভাবে | সমস্যা | উদাহরণ |
|---|---|---|---|
| Dynamic analysis | Test চালিয়ে দেখা কোন function call হলো | প্রতিটা project build ও run করতে হয় — scale করে না | TeCo (1,270 Java project) |
| Heuristic | নামের মিল (`testAdd` → `add`), language-specific নিয়ম | প্রতি language-এ আলাদা, ভঙ্গুর | AthenaTest, TOGA, A3Test |
| File-level | `test_foo.py` ↔ `foo.py` | জোড়া দুর্বল — কোন function তা জানা যায় না | CAT-LM |
| **Static + LSP (এই paper)** | AST থেকে focal call খুঁজে LSP দিয়ে তার definition বের করা | Language server লাগে; call heuristic ভুল হতে পারে | UniTSyn |

### ২.৫ Abstract Syntax Tree (AST) ও tree-sitter
- **AST:** source code-কে গাছের মতো structure-এ রূপান্তর — function, variable declaration, call, assertion সব আলাদা node।
- **tree-sitter:** একটা parser generator, যেটা formal grammar থাকা যেকোনো language parse করতে পারে। একই interface দিয়ে 5টা language-এর AST পাওয়া যায় — তাই UniTSyn-এর parsing অংশ language-নিরপেক্ষ।
- **Postorder traversal:** গাছের আগে সব child, তারপর parent visit করা। UniTSyn এভাবে traverse করে **প্রথম যে assertion node পায়** সেটাকে ধরে (paper-এর Figure 3-এ লাল node)।

### ২.৬ Language Server Protocol (LSP)
- VS Code-এ কোনো function-এর উপর "Go to Definition" চাপলে editor নিজে code বিশ্লেষণ করে না — একটা আলাদা **language server** process-কে JSON-RPC message পাঠায়: "এই file-এর এই line, এই column-এ যে নাম, তার definition কোথায়?" Server উত্তর দেয় file path + line।
- **LSP** হলো Microsoft-এর এই standard protocol — editor আর language-এর বুদ্ধিমত্তা আলাদা করে। ফলে যেকোনো language-এর server (Python-এর জন্য যেমন pylsp/jedi, Java-র জন্য jdtls, C++-এর জন্য clangd, Go-র জন্য gopls) একই ধরনের request বোঝে।
- **UniTSyn-এর কৌশল:** নিজেকে একটা "editor client" বানিয়ে language server-কে প্রশ্ন করা — তাই প্রতিটা language-এর জন্য নিজস্ব dependency analysis লিখতে হয় না, project execute-ও করতে হয় না।

### ২.৭ Static বনাম Dynamic Analysis
- **Static:** code না চালিয়ে বিশ্লেষণ (AST, call graph, LSP)। দ্রুত, scale করে, কিন্তু runtime-এ আসলে কী call হলো তা নিশ্চিত নয় (যেমন polymorphism, dynamic dispatch)।
- **Dynamic:** code চালিয়ে দেখা। নিখুঁত, কিন্তু প্রতিটা project-এর environment setup লাগে।
- **আমাদের জন্য:** আমাদের assurance layer-এ "static judge + dynamic test" — এই paper-এর linking static, কিন্তু এর evaluation (accuracy, coverage) dynamic।

### ২.৮ Multilingual Dataset ও Transfer
একাধিক programming language-এর data একসাথে train করা। প্রশ্ন: Python শিখে কি Java-র test লেখা ভালো হয় (positive transfer), নাকি খারাপ হয় (negative transfer)? Paper-এর RQ4 এটাই দেখে।

### ২.৯ Pre-training, Continual Training ও Fine-tuning
- **Pre-training:** বিশাল সাধারণ corpus-এ শূন্য থেকে model train করা (যেমন SantaCoder)।
- **Continual training (continued pre-training):** আগে train করা model-কে একই objective (next-token prediction) দিয়ে নতুন domain-এর data-তে আরও train করা। **UniTester এটাই** — instruction বা prompt-response জোড়া নয়, শুধু "focal function + newline + test function" টানা text।
- **Instruction tuning / fine-tuning:** (instruction, answer) জোড়ায় train করা — WizardCoder এই ধরনের model; paper এদের জন্য prompt আলাদাভাবে বানিয়েছে।
- **Autoregressive model:** বাম থেকে ডানে একটা একটা token predict করে (GPT-ধরনের, decoder-only)। Encoder-decoder (যেমন CodeT5+) আলাদা architecture।
- **Catastrophic forgetting:** নতুন data-তে train করতে গিয়ে পুরনো জ্ঞান ভুলে যাওয়া — paper weight decay 0.05 দিয়ে এটা কমাতে চেয়েছে।

### ২.১০ Sequence Packing
বিভিন্ন দৈর্ঘ্যের sample-কে padding দিয়ে সমান না করে, সব sample টানা জুড়ে নির্দিষ্ট দৈর্ঘ্যের (এখানে 2048 token) টুকরো কেটে নেওয়া — GPU-র কোনো অংশ খালি padding-এ নষ্ট হয় না।

### ২.১১ Temperature Sampling
Model-এর পরবর্তী token-এর probability distribution-কে temperature $T$ দিয়ে তীক্ষ্ণ বা চ্যাপ্টা করা। $T = 0.2$ মানে প্রায় deterministic, অল্প বৈচিত্র্য। Paper প্রতি task-এ এভাবে 10টা output নেয়।

### ২.১২ Code Coverage — Line, Statement, Branch
- **Line coverage:** focal function-এর কত % executable line test চালানোর সময় অন্তত একবার চলেছে।
- **Statement coverage:** একই ধারণা, line-এর বদলে statement (Go-র tool statement গোনে)।
- **Branch coverage:** প্রতিটা `if`/loop-এর প্রতিটা দিক (true/false) কত % চলেছে। Line coverage-এর চেয়ে কঠোর — `if x > 0: y = 1` line-টা চললেও false দিকটা না চলতে পারে।
- **গুরুত্বপূর্ণ সীমা:** code চলা bug ধরার **প্রয়োজনীয় শর্ত, যথেষ্ট নয়** (paper নিজেও "necessary condition" বলেছে)। Assertion না থাকলে 100% coverage-ও কোনো bug ধরে না।

### ২.১৩ Test Pass Rate / Executability
Generated test-টা compile হয়ে error ছাড়া শেষ পর্যন্ত চলে কিনা। Paper-এ "#Pass" = 164টা task-এর মধ্যে কতগুলোর test কোনো error ছাড়া চলেছে (10 trial-এর গড়)।

### ২.১৪ Mutation Testing ও Mutation Score (paper ব্যবহার করেনি — কিন্তু আমাদের জন্য জরুরি)
- Code-এ ছোট ছোট কৃত্রিম bug (mutant) ঢোকানো — যেমন `<` কে `<=`, `+` কে `-`। তারপর test suite চালানো।
- কোনো test fail করলে mutant "killed"। **Mutation score** = killed mutant-এর অনুপাত — test আসলে কতটা bug **ধরতে পারে** তার সরাসরি মাপ।
- **এই paper mutation score মাপেনি** — accuracy (assertion সঠিক কিনা) আর coverage (code চলেছে কিনা) মেপেছে। এই দুটো মিলেও "test bug ধরে কিনা" প্রমাণ করে না। এটা Section ১২-১৩-এর একটা বড় gap।

### ২.১৫ HumanEval ও HumanEval-X
- **HumanEval (Chen et al., 2021):** 164টা Python programming problem, প্রতিটায় function signature, docstring, canonical solution ও hidden test।
- **HumanEval-X (Zheng et al., 2023):** একই 164টা problem C++, Java, JavaScript, Go-তেও। UniTSyn-এর 5টা language-ই এখানে আছে — তাই evaluation-এর জন্য বেছে নেওয়া।
- **লক্ষ্য করো:** এখানে model code লেখে না — **canonical solution দেওয়া হয়, model শুধু তার test লেখে**।

### ২.১৬ Data Leakage / Contamination
Evaluation data যদি training data-তে থাকে, model মুখস্থ থেকে উত্তর দিতে পারে। Paper দাবি করে HumanEval-X ব্যবহারের কারণে evaluation-এর focal ও test function কোনো model দেখেনি — এই দাবি কতটা শক্ত, তা Section ১২-তে আলোচনা।

---

## ৩. Problem Statement — কী সমস্যা ছিল?

### ৩.১ মূল সমস্যা
1. **Code LLM-এর test লেখার ক্ষমতা দুর্বল:** এরা এমন code snippet-এ train হয় যেখানে test code আর সাধারণ code আলাদা করা হয়নি; তাই "accurate and complete" test লেখে না।
2. **Test আর focal function-এর সংযোগ training data-তে নেই:** সংযোগ ছাড়া model বুঝতে পারে না test-টা কোন আচরণ ও কোন logic path যাচাই করছে।
3. **জোড়া সংগ্রহের বিদ্যমান পদ্ধতি scale করে না:**
   - Dynamic/heuristic (TeCo, TOGA, A3Test, AthenaTest) — প্রতি project-এ execution setup, প্রতি language-এ নতুন heuristic। TeCo-র execution-based সংগ্রহ মাত্র 1,270টা Java project-এ — আর Java (JVM + Maven) চালানোর জন্য সবচেয়ে সহজ language-গুলোর একটা।
   - File-level (CAT-LM) — scale করে, কিন্তু জোড়া দুর্বল।
4. **Multilingual testing model-এর অভাব:** CAT-LM শুধু Python ও Java-তে train হয়েছে; নতুন language যোগ করা কঠিন।

### ৩.২ দুটো technical চ্যালেঞ্জ (Section 3.1)
1. প্রতিটা language-এর grammar ও unit test-এর syntax আলাদা — focal call খুঁজতে language-specific নিয়ম লাগে।
2. Dependency graph থেকে focal function-এর সঠিক definition বের করা প্রতি language-এ আলাদা ও শ্রমসাধ্য।

### ৩.৩ কেন গুরুত্বপূর্ণ
Software testing শ্রমসাধ্য অথচ জরুরি; LLM দিয়ে test লেখানো গেলে খরচ কমে। কিন্তু model ভালো test লিখতে হলে ভালো, বড়, জোড়া-বাঁধা training data লাগে।

---

## ৪. Goal ও Research Questions

**Goal:** একটা বড়, multilingual, function-level focal-test pair dataset ও তা সংগ্রহের একটা সহজে-বর্ধনযোগ্য framework বানানো; তারপর এই data দিয়ে train করা model-এর মাধ্যমে data-র মান প্রমাণ করা।

Paper-এর explicit RQ (Section 4.2):
- **RQ1 (Accuracy):** LLM-এর generated test case কতটা সঠিক? — generated assertion আলাদা আলাদা করে সঠিক solution-এর উপর চালিয়ে।
- **RQ2 (Completeness):** Generated test কতটা complete? — দুইভাবে: executability (#Pass) এবং focal function-এর line/statement/branch coverage।
- **RQ3 (Pairing প্রয়োজন কি?):** Focal-test জোড়া ভেঙে আলাদা snippet হিসেবে train করলে কী হয়? (Paired বনাম Unpaired)
- **RQ4 (Multilingual-এর প্রভাব):** শুধু Python-এ train (Mono) বনাম 5 language-এ train (Multi)।

**Contribution (paper-এর ভাষায় ৩টা):** (১) 2.7M focal-test pair, 5 language; (২) LSP-ভিত্তিক generic, extendable dataset-building approach; (৩) UniTester train করে dataset-এর মান যাচাই।

---

## ৫. Methodology — কীভাবে কাজটা করা হয়েছে

### ৫.১ Repository সংগ্রহ (Section 3.2)
- CAT-LM-এর পদ্ধতি অনুসরণ করে GitHub-এ "active development"-এ থাকা repository খোঁজা, CodeSearchNet-কে বাড়ানোর উদ্দেশ্যে।
- শর্ত: **10-এর বেশি star**, এবং **1 January 2020-এর পরে নতুন commit**।
- বাদ: archived, forked, mirrored repository।
- Language: Python, Java, Go, C++, JavaScript।

### ৫.২ Pipeline (Figure 1): GitHub → test extraction → focal call → LSP → pair

| ধাপ | অংশ | কী করা হয় | Language-ভেদে কী বদলাতে হয় |
|---|---|---|---|
| 1 | Download | GitHub API দিয়ে repository নামানো | কিছু না |
| 2 | Parsing (frontend) | tree-sitter দিয়ে প্রতিটা file-এর AST | Grammar (tree-sitter-এ আগেই আছে) |
| 3 | Test function identification (frontend) | AST traverse করে test function চেনা — "hook" call-back দিয়ে | Hook: নাম-ভিত্তিক heuristic, বা framework feature (যেমন JUnit-এর `@Test`) |
| 4 | Focal call analysis (frontend) | Test-এর ভেতরে প্রথম assertion-এর **আগের শেষ** এমন call যেটা repository-র ভেতরের কোনো definition-কে ডাকে | মাত্র **একটা extra function** implement করতে হয় |
| 5 | Focal extraction via LSP (backend) | Language server-কে JSON-RPC request: ঐ call-এর definition কোথায়? উত্তর থেকে focal function-এর source code কাটা | শুধু language server চালু করার command |
| 6 | Store | Function-level focal-test pair সংরক্ষণ | কিছু না |

**ধাপ 3 — Test identification-এর দুই রকম implementation:** (ক) function-এর নাম দেখে heuristic; (খ) language feature — যেমন Java JUnit-এ প্রতিটা test-এ `@Test` modifier থাকতে হয়। নতুন test framework যোগ করতে নতুন hook লিখলেই হয়।

**ধাপ 4 — Focal call heuristic (TeCo থেকে নেওয়া):** একটা test সাধারণত setup-এর জন্য অনেক function call করে; আসল focal call চেনা কঠিন। নিয়ম: postorder traversal-এ প্রথম assertion node খুঁজে, **তার আগের শেষ call যেটা repository-তে defined function-কে ডাকে**। Listing 1-এ: `new Position(x, y)` (line 5) ও `mp.add(...)` (line 6) দুটোই assertion (line 7)-এর আগে; শেষেরটা `add` → focal।

**ধাপ 5 — কেন LSP:** project build বা run করতে হয় না, প্রতি language-এ dependency analysis লিখতে হয় না; language server-এর "definition খোঁজা" ক্ষমতা ধার নেওয়া হয়।

### ৫.৩ Dataset Statistics (Table 1)

| Language | Framework (test extraction-এর ভিত্তি) | #proj | #pairs |
|---|---|---|---|
| Python | unittest, pytest | 43,848 | 1,218,311 |
| Java | JUnit | 25,488 | 1,097,518 |
| Go | testing | 38,097 | 361,075 |
| C++ | GoogleTest | 20,090 | 25,513 |
| JavaScript | MochaJS | 17,621 | 13,293 |
| **মোট (আমার হিসাব)** | — | **145,144** | **2,715,710** (≈ paper-এর "2.7M") |

> নোট: সাধারণ `pdftotext` layout mode-এ এই table-এর Go/C++/JS-এর #pairs কলাম এলোমেলো দেখায়; `pdftotext -raw` দিয়ে আবার বের করে উপরের মানগুলো নিশ্চিত করা হয়েছে, আর যোগফল paper-এর 2.7M-এর সাথে মেলে।

### ৫.৪ UniTester Model (Section 4.1)

| বিষয় | মান |
|---|---|
| Base model | SantaCoder, **1.1B** parameter (decoder-only) |
| Objective | Autoregressive next-token prediction (continual training) |
| Training sample | focal function + newline + test function (একসাথে জোড়া) |
| Packing | Constant sequence length **2048** |
| Batch size | **32** |
| Learning rate | **5e-5**; প্রথম **500 step** logarithmic warmup, তারপর cosine annealing |
| Weight decay | **0.05** (overfitting ও catastrophic forgetting কমাতে) |
| Optimizer | Adam |
| Steps | **36,000** |
| Data size | প্রায় **এক billion token** |
| Hardware / সময় | **8 × Nvidia V100**, প্রায় **24 ঘণ্টা** |

### ৫.৫ Evaluation Setup (Section 4.2)

| বিষয় | মান |
|---|---|
| Benchmark | HumanEval-X: 164 task × 5 language (Python, C++, Java, JavaScript, Go) |
| কাজ | Canonical solution (focal function) দেওয়া, model তার test লেখে |
| Prompt | CodeT-এর ধাঁচে language-specific assert keyword দিয়ে শুরু (Figure 4) — যেমন Python-এ `def test_has_close_elements(): assert has_close_elements(`; C++-এ `#undef NDEBUG`, `#include <assert.h>`, `int main(){ assert(...`; JavaScript-এ `console.assert(...`; Go-তে `assert.Equal(...)`; Java-তে `main`-এর ভেতরে `assert s.hasCloseElements(...` |
| Instruction-tuned model-এর জন্য | Focal function + "Check the correctness of ..." hint-কে instruction বানিয়ে test complete করতে বলা |
| Max input / output | 800 token input, সর্বোচ্চ 256 token output |
| Temperature | 0.2 (Xiong et al. ও Rao et al. অনুসারে, সব model-এ একই) |
| Samples | প্রতি task-এ 10টা output |
| Accuracy-র জন্য | Generated test থেকে **প্রথম 10টা assertion** parse করে প্রতিটা আলাদা করে যাচাই (Chen et al. — CodeT অনুসারে) |
| Completeness-এর জন্য | প্রতিটা output আলাদা test হিসেবে চালানো; শুধু Java-তে test class-এর closing bracket যোগ করা হয়েছে, অন্য কোনো জটিল post-processing নেই; 10 trial-এর গড় coverage |

**তুলনার model:**
| Model | ধরন | Parameter |
|---|---|---|
| CodeT5p (CodeT5+) | Code, encoder-decoder | 770M |
| CodeGen2 | Code, decoder-only | 1.0B |
| WizardCoder | Code, instruction-tuned | 1.0B |
| InCoder | Code, decoder-only | 1.3B |
| SantaCoder | Code, decoder-only (UniTester-এর base) | 1.1B |
| CAT-LM | **Test generation**, Python+Java, file-level aligned, 60B token-এ trained | 2.7B |
| UniTester | **Test generation**, UniTSyn, ~1B token | 1.1B |

> Paper-এর যুক্তি: CAT-LM বেশি data (60B বনাম 1B token) ও দ্বিগুণের বেশি বড় model — তবুও হারানো গেলে data-র মান প্রমাণ হয়।

### ৫.৬ Ablation Variant (RQ3, RQ4)
- **Baseline:** SantaCoder, UniTSyn-এ train হয়নি।
- **Unpaired:** একই data, কিন্তু test ও focal function আলাদা snippet হিসেবে।
- **Paired:** UniTester (Multi)।
- **Mono:** শুধু UniTSyn-এর Python অংশে train।
- **Multi:** 5 language-এ train (= UniTester)।

---

## ৬. Mathematical Formulation — সূত্র ও ব্যাখ্যা

Paper-এ কোনো explicit equation নেই। নিচের formalization **আমার** — paper-এর লেখা বর্ণনাকে গাণিতিকভাবে লেখা, যাতে supervisor-কে exact সংজ্ঞা দেখানো যায়। যেখানে paper কোনো detail বলেনি, তা আলাদা করে বলা আছে।

### ৬.১ Repository Filter
$R_q$ = language $q$-এর GitHub repository-র set। একটা repository $r$ নেওয়া হবে যদি:
$$
\text{keep}(r) = \mathbb{1}\left[\text{stars}(r) > 10 \;\land\; \text{lastCommit}(r) > \text{2020-01-01} \;\land\; \neg\,\text{archived}(r) \;\land\; \neg\,\text{fork}(r) \;\land\; \neg\,\text{mirror}(r)\right]
$$

### ৬.২ Test Function Identification (Hook)
Repository-র প্রতিটা function $g$-এর জন্য একটা hook $h_q(g) \in \{0, 1\}$। Test set:
$$
T_r = \{\, g \in \text{Functions}(r) \;:\; h_q(g) = 1 \,\}
$$
উদাহরণ: Java-তে $h_{\text{Java}}(g) = 1$ যদি $g$-এর `@Test` modifier থাকে; নাম-ভিত্তিক hook-এ $h(g) = 1$ যদি নাম "test" দিয়ে শুরু হয়।

### ৬.৩ Focal Call Selection
Test $t$-এর AST-কে postorder-এ traverse করলে node-গুলোর ক্রম $\text{pos}(\cdot)$। প্রথম assertion node:
$$
a^{\star} = \arg\min_{a \in \text{Asserts}(t)} \text{pos}(a)
$$
Candidate call: যেসব call $c$ assertion-এর আগে এবং যাদের definition repository-র ভেতরে:
$$
C(t) = \{\, c \in \text{Calls}(t) \;:\; \text{pos}(c) < \text{pos}(a^{\star}) \;\land\; \text{def}(c) \in r \,\}
$$
Focal call হলো এদের মধ্যে **শেষেরটা**:
$$
c^{\star}(t) = \arg\max_{c \in C(t)} \text{pos}(c)
$$
**Worked example (Listing 1):** Assertion line 7। Line 5-এ `Position(...)` আর line 6-এ `add(...)` — দুটোই repository-তে defined, দুটোই line 7-এর আগে। $\arg\max$ = line 6 → $c^{\star}$ = `add`।

**আমার পর্যবেক্ষণ:** যদি test-এ কোনো assertion না থাকে (যেমন শুধু exception না হওয়া পরীক্ষা করে) বা $C(t)$ খালি হয়, তাহলে কী হয় — paper বলেনি। সম্ভবত ঐ test বাদ যায়, যার মানে dataset assertion-ওয়ালা test-এর দিকে ঝুঁকে আছে।

### ৬.৪ LSP দিয়ে Focal Function বের করা
$\text{LSP}_q$ = language $q$-এর server-এর "definition" request। Call $c^{\star}$-এর অবস্থান (file, line, column) দিলে:
$$
\text{loc}(f) = \text{LSP}_q\big(\text{file}(c^{\star}),\, \text{line}(c^{\star}),\, \text{col}(c^{\star})\big), \qquad f = \text{extract}(\text{loc}(f))
$$
Dataset:
$$
\mathcal{D} = \cup_{q} \; \cup_{r \in R_q,\, \text{keep}(r)} \; \{\, (f(t),\, t) \;:\; t \in T_r,\; C(t) \text{ খালি নয়} \,\}
$$
**আমার হিসাব:** $\sum_q$ #pairs = 1,218,311 + 1,097,518 + 361,075 + 25,513 + 13,293 = **2,715,710**।

**প্রতি project-এ গড় pair (আমার হিসাব):**
| Language | #pairs ÷ #proj |
|---|---|
| Python | 1,218,311 ÷ 43,848 ≈ 27.8 |
| Java | 1,097,518 ÷ 25,488 ≈ 43.1 |
| Go | 361,075 ÷ 38,097 ≈ 9.5 |
| C++ | 25,513 ÷ 20,090 ≈ 1.27 |
| JavaScript | 13,293 ÷ 17,621 ≈ 0.75 |

C++ ও JavaScript-এ project প্রতি 1-এর কাছাকাছি বা তারও কম pair — authors-এর limitation-এর সাথে মেলে (শুধু GoogleTest ও MochaJS hook লেখা হয়েছে)।

### ৬.৫ Training Objective
Training sample $x = f \oplus \text{newline} \oplus t$ (এখানে $\oplus$ = string জোড়া)। সব sample টানা জুড়ে $L = 2048$ দৈর্ঘ্যের sequence $s = (s_1, \ldots, s_L)$ কাটা হয় (packing)। Loss:
$$
\mathcal{L}(\theta) = -\frac{1}{L} \sum_{i=1}^{L} \log p_\theta(s_i \mid s_{<i})
$$
**গুরুত্বপূর্ণ:** loss focal ও test দুই অংশের token-এর উপরই — অর্থাৎ model focal function লেখাও শেখে, শুধু test নয়। Inference-এ focal দেওয়া থাকে, model test অংশ complete করে।

Weight decay সহ Adam update (paper-এ শুধু "Adam" + "weight decay 0.05" বলা; decoupled নাকি L2 তা বলা নেই):
$$
\theta \leftarrow \theta - \eta_k \left( \frac{\hat{m}_k}{\sqrt{\hat{v}_k} + \epsilon} + \lambda\, \theta \right), \qquad \lambda = 0.05
$$

### ৬.৬ Learning-rate Schedule
প্রথম 500 step "logarithmic warmup" (paper সঠিক সূত্র দেয়নি)। তারপর cosine annealing (Loshchilov & Hutter):
$$
\eta_k = \eta_{\min} + \frac{1}{2}\left(\eta_{\max} - \eta_{\min}\right)\left(1 + \cos\left(\frac{(k - 500)\,\pi}{36000 - 500}\right)\right), \quad 500 \leq k \leq 36000
$$
$\eta_{\max} = 5 \times 10^{-5}$। $\eta_{\min}$ paper-এ বলা নেই।
**Worked example:** ধরো $\eta_{\min} = 0$ (আমার অনুমান)। মাঝামাঝি $k = 18250$-এ cosine-এর argument $\pi/2$, তাই $\eta = \frac{1}{2} \times 5 \times 10^{-5} \times 1 = 2.5 \times 10^{-5}$।

### ৬.৭ কত token আসলে দেখা হয়েছে (আমার হিসাব)
$$
\text{Tokens}_{\text{seen}} = \text{steps} \times \text{batch} \times L = 36000 \times 32 \times 2048 = 2{,}359{,}296{,}000 \approx 2.36\text{B}
$$
Data "around one billion tokens" হলে $\frac{2.36}{1} \approx 2.4$ epoch-এর মতো। (Paper epoch সংখ্যা বলেনি; "around" শব্দের কারণে এটা মোটামুটি হিসাব।)

### ৬.৮ Temperature Sampling
Logit $z_v$ থেকে token $v$-এর probability:
$$
p_T(v) = \frac{\exp(z_v / T)}{\sum_{u \in V} \exp(z_u / T)}, \qquad T = 0.2
$$
**Worked example (আমার উদাহরণ):** দুটো token-এর logit 2.0 ও 1.0। $T = 1$-এ probability অনুপাত $e^{1} \approx 2.72$; $T = 0.2$-এ $e^{1/0.2} = e^{5} \approx 148$ — অর্থাৎ বড় logit-ওয়ালা token প্রায় নিশ্চিতভাবে বাছাই হয়। তাই 10টা sample-এর মধ্যে বৈচিত্র্য কম।

### ৬.৯ RQ1: Assertion Accuracy
Task $j$-এর (মোট $N = 164$) জন্য 10টা generated output থেকে প্রথম 10টা assertion $a_{j,1}, \ldots, a_{j,m_j}$ ($m_j \leq 10$)। প্রতিটা assertion আলাদাভাবে canonical solution $f_j^{\star}$-এর উপর চালানো হয়:
$$
\text{ok}(a) = \begin{cases} 1, & \text{যদি } a \text{ চালালে } f_j^{\star} \text{-এর উপর error ছাড়া true হয়} \\ 0, & \text{অন্যথায় (false, exception, compile error)} \end{cases}
$$
$$
\text{Acc}_q = \frac{\sum_{j=1}^{N} \sum_{i=1}^{m_j} \text{ok}(a_{j,i})}{\sum_{j=1}^{N} m_j} \times 100
$$
**সতর্কতা:** paper সূত্রটা লেখেনি; "parse the assertions … examine their standalone correctness" বর্ণনা থেকে আমার formalization। Task-ভিত্তিক গড় (প্রতি task-এর accuracy, তারপর গড়) নাকি assertion-ভিত্তিক মোট — paper স্পষ্ট নয়।

**আসলে কী মাপে:** assertion-টা **সঠিক code-এর আচরণের সাথে মিলছে কিনা** (oracle correctness)। এটা মাপে না assertion-টা **ভুল code ধরতে পারে কিনা** (fault-detection strength)। যেমন `assert f([1.0, 2.0], 0.5) == f([1.0, 2.0], 0.5)` সবসময় "accurate", কিন্তু কোনো bug ধরে না।

**Worked example:** UniTester Python-এ 52.5%। যদি প্রতি task-এ পুরো 10টা assertion পাওয়া যায়, তাহলে $164 \times 10 = 1{,}640$ assertion-এর মধ্যে প্রায় $0.525 \times 1640 \approx 861$টা সঠিক, ~779টা ভুল (আমার হিসাব, $m_j = 10$ ধরে)।

**Average (Avg) কলাম:** 5 language-এর সরল গড়:
$$
\bar{\text{Acc}} = \frac{1}{5} \sum_{q} \text{Acc}_q
$$
**যাচাই (আমার হিসাব):** WizardCoder: (36.8 + 43.9 + 28.7 + 31.3 + 47.7) ÷ 5 = 188.4 ÷ 5 = 37.68 → paper 37.7 ✓। UniTester: (52.5 + 55.1 + 48.8 + 41.7 + 59.7) ÷ 5 = 257.8 ÷ 5 = 51.56 → paper লিখেছে **51.5** (সাধারণ rounding-এ 51.6 হওয়ার কথা; সম্ভবত unrounded মান থেকে গড় করা — ছোট অসঙ্গতি, ফলাফলে প্রভাব নেই)।

### ৬.১০ Relative Improvement
$$
\Delta_{\text{rel}} = \frac{\text{Acc}_{\text{UniTester}} - \text{Acc}_{\text{other}}}{\text{Acc}_{\text{other}}} \times 100\%
$$
**Paper-এর দুই দাবি যাচাই (আমার হিসাব):**
- Python, CAT-LM-এর বিপরীতে: $\frac{52.5 - 37.5}{37.5} = 0.40$ → **40%** ✓ ("up to a 40% relative margin")।
- গড়ে WizardCoder-এর বিপরীতে: $\frac{51.5 - 37.7}{37.7} = 0.366$ → **36.6%** ✓।

### ৬.১১ RQ2: Executability (#Pass ও Pass Rate)
Task $j$, trial $k$ ($K = 10$)-এর generated test $t_{j,k}$:
$$
\text{Pass}_q = \frac{1}{K} \sum_{k=1}^{K} \sum_{j=1}^{N} \mathbb{1}\left[t_{j,k} \text{ error ছাড়া চলে}\right], \qquad \text{PassRate}_q = \frac{\text{Pass}_q}{N}
$$
**Worked example (আমার হিসাব):** UniTester Python #Pass = 41.2 → $41.2 / 164 = 25.1\%$। Java #Pass = 103.1 → $103.1 / 164 = 62.9\%$।

**Paper-এর "2% থেকে 32%" দাবি কোথা থেকে (আমার হিসাব):** প্রতি model-এর 5 language-এর #Pass-এর গড় ÷ 164:
- UniTester: (41.2 + 28.1 + 103.1 + 53.3 + 36.0) ÷ 5 = 52.34 → 52.34 ÷ 164 = **31.9%** (≈ 32%)
- CodeGen2: (4.1 + 11.6 + 52.3 + 48.5 + 19.2) ÷ 5 = 27.14 → **16.5%**
- InCoder: (3.0 + 0.0 + 15.0 + 0.5 + 1.3) ÷ 5 = 3.96 → **2.4%** (≈ 2%)
- "Nearly twice that of CodeGen2": $52.34 / 27.14 \approx 1.93$ ✓

অর্থাৎ "2%–32%" প্রতিটা language-এর জন্য নয়, **model-ভিত্তিক 5-language গড়**। একক language-এ UniTester Java 62.9% পর্যন্ত যায়।

### ৬.১২ RQ2: Coverage
Focal function $f_j$-এর executable line set $\mathcal{L}_j$, branch set $B_j$; test $t$ চালালে যেসব line/branch চলে: $\text{Exec}_L(t)$, $\text{Exec}_B(t)$।
$$
\text{LineCov}(t, f_j) = \frac{|\text{Exec}_L(t) \cap \mathcal{L}_j|}{|\mathcal{L}_j|} \times 100, \qquad \text{BranchCov}(t, f_j) = \frac{|\text{Exec}_B(t) \cap B_j|}{|B_j|} \times 100
$$
Reported মান (আমার formalization; paper "average coverage rates from ten trials" বলেছে):
$$
\bar{\text{LineCov}}_q = \frac{1}{K N} \sum_{k=1}^{K} \sum_{j=1}^{N} \text{LineCov}(t_{j,k}, f_j)
$$
**Worked example 1 (Listing 1):** focal `add`-এর executable line মাত্র 1টা (`return new Position(...)`)। Test সেটা call করে → $\text{LineCov} = 1/1 = 100\%$। Branch নেই, তাই branch coverage সংজ্ঞায়িত নয় (tool-ভেদে 100% বা বাদ)।

**Worked example 2 (আমার উদাহরণ, কাল্পনিক):** focal-এ 10টা executable line, 4টা branch outcome। Test 7টা line আর 2টা branch outcome চালায় → LineCov = 70%, BranchCov = 50%।

**আমার পর্যবেক্ষণ — কম coverage-এর মানে কী:** Table 3-এর coverage মান pass rate-এর প্রায় সমানুপাতিক। UniTester Python: LineCov 20.71, PassRate 25.1% → $20.71 / 25.1 \approx 0.82$। CAT-LM Python: $19.51 / (35.9/164 = 21.9) \approx 0.89$। এটা মিলে যায় যদি **error-ওয়ালা test-এর coverage 0 ধরা হয়** আর চলমান test focal function-এর বেশিরভাগ line চালায়। Paper এটা স্পষ্ট বলেনি, তাই এটা অনুমান। কিন্তু Java-তে UniTester-এর PassRate 62.9% অথচ LineCov মাত্র 10.78% ($10.78/62.9 \approx 0.17$) — অর্থাৎ Java-তে "error ছাড়া চলা" অনেক test focal function-কে প্রায় চালায়ই না। Section ১২-তে এর একটা সম্ভাব্য কারণ (Java-র `assert` default-এ বন্ধ) আলোচনা করেছি।

### ৬.১৩ Coverage Improvement ("up to 6.32%, average 2.8%") — যাচাই
Paper বলে UniTester line coverage-এ সর্বোচ্চ 6.32% ও গড়ে 2.8% absolute উন্নতি করেছে। প্রতি language-এ **সেরা অন্য model**-এর সাথে পার্থক্য (আমার হিসাব):
| Language | UniTester Line/Stmt | সেরা অন্য model | পার্থক্য |
|---|---|---|---|
| Python | 20.71 | CAT-LM 19.51 | +1.20 |
| C++ | 13.39 | CodeGen2 7.07 | **+6.32** |
| Java | 10.78 | WizardCoder 5.62 | +5.16 |
| JavaScript | 27.59 | CodeGen2 27.65 | **−0.06** |
| Go (Stmt) | 12.39 | CodeGen2 10.99 | +1.40 |
| **গড়** | — | — | (1.20 + 6.32 + 5.16 − 0.06 + 1.40) ÷ 5 = **2.80** ✓ |

দাবি দুটোই মেলে — কিন্তু লক্ষ্য করো **JavaScript-এ UniTester line (27.59 বনাম 27.65) ও branch (23.34 বনাম 23.87) দুটোতেই CodeGen2-এর চেয়ে সামান্য পিছিয়ে** — paper এটা আলাদা করে বলেনি।

### ৬.১৪ Mutation Score (paper-এ নেই — আমাদের প্রস্তাবিত পরিপূরক metric)
$M$ = focal function-এর non-equivalent mutant-এর set (equivalent mutant — যা আচরণ বদলায় না — আগেই বাদ); test suite $S$:
$$
	ext{MS}(S) = rac{|\{\, \mu \in M \;:\; \exists\, t \in S,\; t(\mu) = 	ext{FAIL} \,\}|}{|M|} = rac{	ext{killed}}{	ext{total} - 	ext{equivalent}}
$$
**Worked example (কাল্পনিক, আমার উদাহরণ):** HumanEval-এর `has_close_elements`-এর জন্য 20টা mutant, 2টা equivalent। Generated test 9টা kill করে → $\text{MS} = 9 / 18 = 50\%$। Coverage 100% হলেও MS 50% হতে পারে — কারণ assertion দুর্বল।

**কেন জরুরি:** RQ1-এর accuracy বলে "assertion সঠিক code-এ pass করে"; MS বলে "assertion ভুল code-এ fail করে"। আমাদের patch assurance-এর জন্য দ্বিতীয়টাই আসল — ভুল patch ধরতে হবে।

---

## ৭. Experimental Setup (সংক্ষেপে)

| বিষয় | বিবরণ |
|---|---|
| Training data | UniTSyn (Table 1), ~1B token |
| Model | UniTester = SantaCoder 1.1B + continual training |
| Evaluation benchmark | HumanEval-X, 164 task × 5 language |
| মোট generated output প্রতি model (আমার হিসাব) | 164 × 5 × 10 = 8,200 |
| Metric | Accuracy (RQ1), #Pass + Line/Stmt/Branch coverage (RQ2), Paired/Unpaired (RQ3), Mono/Multi (RQ4) |
| Branch coverage | C++ ও Go-তে নেই (tool-এর সীমা); Go-তে line-এর বদলে statement |
| Statistical test | **নেই** — কোনো confidence interval, standard deviation বা significance test report করা হয়নি |

---

## ৮. Results — মূল ফলাফল

### ৮.১ RQ1: Accuracy (Table 2)

| Model | #Params | Py | C++ | Java | JS | Go | Avg |
|---|---|---|---|---|---|---|---|
| CodeT5p | 770M | 30.6 | 33.7 | 26.9 | **37.1**† | 32.9 | 32.2 |
| CodeGen2 | 1.0B | 34.0 | 40.7 | 24.1 | 30.5 | 36.1 | 33.1 |
| WizardCoder | 1.0B | 36.8 | 43.9 | 28.7 | 31.3 | 47.7 | 37.7 |
| InCoder | 1.3B | 34.2 | 33.5 | 22.6 | 24.4 | 31.5 | 29.2 |
| SantaCoder | 1.1B | 36.2 | 34.7 | 36.5 | 30.6 | 31.5 | 33.9 |
| CAT-LM (test gen) | 2.7B | 37.5 | 31.6 | 34.4 | 29.2 | 36.9 | 33.9 |
| **UniTester** (test gen) | 1.1B | **52.5** | **55.1** | **48.8** | **41.7** | **59.7** | **51.5** |

† UniTester ছাড়া JS-এ সেরা।
> নোট: সাধারণ text extraction-এ CAT-LM ও UniTester-এর row এলোমেলো দেখায়; `pdftotext -raw` দিয়ে নিশ্চিত করা হয়েছে CAT-LM = 2.7B ও UniTester = 1.1B।

**প্রতি language-এ সেরা অন্য model-এর তুলনায় UniTester (আমার হিসাব):**
| Language | সেরা অন্য | UniTester | Absolute | Relative |
|---|---|---|---|---|
| Python | CAT-LM 37.5 | 52.5 | +15.0 | +40.0% |
| C++ | WizardCoder 43.9 | 55.1 | +11.2 | +25.5% |
| Java | SantaCoder 36.5 | 48.8 | +12.3 | +33.7% |
| JavaScript | CodeT5p 37.1 | 41.7 | +4.6 | +12.4% |
| Go | WizardCoder 47.7 | 59.7 | +12.0 | +25.2% |

Paper-এর পর্যবেক্ষণ: উন্নতি সবচেয়ে বেশি Python-এ (সবচেয়ে বেশি data), সবচেয়ে কম JavaScript-এ (সবচেয়ে কম data, 13,293 pair) — data-র পরিমাণের সাথে সম্পর্কিত।

**Base SantaCoder-এর তুলনায় উন্নতি (আমার হিসাব):** Py +16.3, C++ +20.4, Java +12.3, JS +11.1, Go +28.2 percentage point। SantaCoder C++ ও Go-তে train হয়নি, তবুও ঐ দুই language-এ উন্নতি সবচেয়ে বড় — paper-এর দাবি "on par with the rest" এর চেয়েও শক্তিশালী ফল। (তবে JS নিয়ে paper-এর বক্তব্যে একটা অসঙ্গতি আছে — Section ১২ দেখো।)

### ৮.২ RQ2: Completeness (Table 3)

| Model | Params | Py #Pass | Py Line | Py Branch | C++ #Pass | C++ Line | Java #Pass | Java Line | Java Branch | JS #Pass | JS Line | JS Branch | Go #Pass | Go Stmt |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CodeT5p | 770M | 10.0 | 5.72 | 5.41 | 0.7 | 0.43 | 40.3 | 4.22 | 2.01 | 4.9 | 2.07 | 1.01 | 1.7 | 0.73 |
| CodeGen2 | 1B | 4.1 | 2.41 | 2.34 | 11.6 | 7.07 | 52.3 | 5.12 | 3.29 | 48.5 | **27.65** | **23.87** | 19.2 | 10.99 |
| WizardCoder | 1B | 16.1 | 9.39 | 8.95 | 3.7 | 2.24 | 47.7 | 5.62 | 4.09 | 9.2 | 5.50 | 5.32 | 0.7 | 0.42 |
| InCoder | 1.3B | 3.0 | 1.76 | 1.60 | 0.0 | 0.00 | 15.0 | 1.54 | 0.91 | 0.5 | 0.29 | 0.26 | 1.3 | 0.78 |
| SantaCoder | 1.1B | 4.5 | 2.62 | 2.59 | 4.9 | 2.99 | 50.1 | 4.74 | 1.83 | 5.9 | 3.53 | 3.23 | 0.7 | 0.43 |
| CAT-LM | 2.7B | 35.9 | 19.51 | 18.03 | 0.0 | 0.00 | 0.9 | 0.07 | 0.00 | 9.2 | 4.53 | 3.49 | 0.0 | 0.00 |
| **UniTester** | 1.1B | **41.2** | **20.71** | **18.27** | **28.1** | **13.39** | **103.1** | **10.78** | **4.57** | **53.3** | 27.59 | 23.34 | **36.0** | **12.39** |

#Pass = 164টা task-এর মধ্যে কতগুলোর test error ছাড়া চলেছে (10 trial-এর গড়); Line/Branch/Stmt = %।

**মূল পর্যবেক্ষণ:**
- Model-ভিত্তিক গড় pass rate 2%–32% (UniTester ~32%, CodeGen2 ~16.5%) — **বেশিরভাগ generated test চলেই না**।
- CAT-LM (Python+Java-তে trained) C++ ও Go-তে **একটাও** চলমান test লেখেনি (#Pass 0.0), Java-তেও মাত্র 0.9 — paper-এর "multilingual দরকার" যুক্তির পক্ষে শক্ত প্রমাণ।
- C++ সবচেয়ে কঠিন (paper-এর মতে C++ readability কম, মানুষের জন্যও লেখা কঠিন) — UniTester ছাড়া সবার C++ #Pass ≤ 11.6।
- Coverage absolute মান খুব কম (সর্বোচ্চ ~28%) — কারণ error-ওয়ালা test-ও গড়ে ধরা হয়েছে বলে মনে হয় (Section ৬.১২)।

### ৮.৩ RQ3: Paired বনাম Unpaired (Figure 5)
Paper সংখ্যা দেয়নি, শুধু bar chart। আমি PDF-এর vector graphics থেকে bar-এর উচ্চতা পড়ে মান বের করেছি (**আমার হিসাব, প্রায় ±0.1 নির্ভুল**; Baseline ও Paired bar Table 2-এর SantaCoder ও UniTester-এর সাথে হুবহু মিলেছে, তাই পদ্ধতিটা নির্ভরযোগ্য):

| Language | Baseline (SantaCoder) | Unpaired | Paired (UniTester) |
|---|---|---|---|
| Python | 36.2 | ≈ 44.8 | 52.5 |
| C++ | 34.7 | ≈ 40.1 | 55.1 |
| Java | 36.5 | ≈ **34.8** | 48.7 |
| JavaScript | 30.7 | ≈ 33.7 | 41.7 |
| Go | 31.6 | ≈ 39.7 | 59.7 |
| Overall | 33.9 | ≈ 38.6 | 51.6 |

- **Paper-এর দাবি:** Unpaired baseline-এর চেয়ে ভালো (সম্ভবত UniTSyn-এ test ও focal-এর ভারসাম্যপূর্ণ মিশ্রণের কারণে), আর Paired অনেক বেশি ভালো → **জোড়া বাঁধাই মূল কারণ**।
- **আমার পর্যবেক্ষণ:** Overall-এ উন্নতির ভাগ — Baseline → Unpaired ≈ +4.7, Unpaired → Paired ≈ +13.0। অর্থাৎ মোট উন্নতির প্রায় তিন-চতুর্থাংশ জোড়া বাঁধার কারণে। তবে **Java-তে Unpaired baseline-এর চেয়ে সামান্য খারাপ** (≈34.8 বনাম 36.5) — paper-এর "unpaired more accurate than baseline" সব language-এ সত্য নয়।
- Paper-এর ব্যাখ্যা: focal function context-এ থাকলে model "expected usage and behavior" বোঝে; না থাকলে সব সম্ভাব্য focal function মুখস্থ করে predict করতে হয়, reasoning দিয়ে নয়।

### ৮.৪ RQ4: Mono বনাম Multi (Figure 6)
আবার vector data থেকে পড়া (**আমার হিসাব**):

| Language | Baseline | Mono (শুধু Python) | Multi (UniTester) |
|---|---|---|---|
| Python | 36.2 | ≈ **55.2** | 52.5 |
| C++ | 34.7 | ≈ 31.0 | 55.1 |
| Java | 36.5 | ≈ 30.7 | 48.7 |
| JavaScript | 30.7 | ≈ 35.0 | 41.7 |
| Go | 31.6 | ≈ 36.6 | 59.7 |
| Overall | 33.9 | ≈ 37.7 | 51.6 |

- **Python-এ Mono, Multi-এর চেয়ে ভালো** (≈55.2 বনাম 52.5) — একটা language-এ বিশেষজ্ঞ model সেই language-এ ভালো।
- Python থেকে JavaScript ও Go-তে **positive transfer** (baseline-এর উপরে), কিন্তু C++ ও Java-তে **negative transfer** (baseline-এর নিচে: C++ ≈31.0 বনাম 34.7, Java ≈30.7 বনাম 36.5)।
- Paper-এর উপসংহার: syntax-এ কাছাকাছি language-এর মধ্যে সীমিত transfer, অন্যত্র ক্ষতি — তাই language-specific বা universal যেকোনো model-এর জন্যই বহু-ভাষার test সংগ্রহের flexible framework দরকার।

---

## ৯. Key Findings / Insights (Supervisor-কে বলার মতো ৮টা পয়েন্ট)

1. **Static analysis + LSP দিয়ে execution ছাড়াই function-level test-to-code linking scale করা যায়** — 145,144 project, 2.7M pair, 5 language।
2. **Test-specific data-র মান আকারের চেয়ে গুরুত্বপূর্ণ:** 1B token-এ trained 1.1B UniTester, 60B token-এ trained 2.7B CAT-LM-কে সব 5 language-এ accuracy-তে হারিয়েছে (গড় 51.5 বনাম 33.9)।
3. **জোড়া বাঁধা (pairing) মূল চাবিকাঠি:** Unpaired-এর তুলনায় Paired-এর বড় লাফ (Figure 5)।
4. **Multilingual training সামগ্রিকভাবে ভালো, কিন্তু transfer অসম:** Mono Python-এ সেরা, কিন্তু C++/Java-তে baseline-এর নিচে নামে (Figure 6)।
5. **LLM-generated test-এর বেশিরভাগ চলেই না:** model-ভিত্তিক গড় pass rate 2%–32% — **সেরা model-এরও প্রায় 68% test error দেয়** (আমার হিসাব: 100 − 31.9)।
6. **চললেও assertion-এর প্রায় অর্ধেক ভুল:** সেরা গড় accuracy 51.5% — অর্থাৎ assertion-গুলোর প্রায় অর্ধেক সঠিক code-কেই "ভুল" বলবে।
7. **Coverage কম:** সর্বোচ্চ গড় line coverage ~28% (JavaScript); coverage উন্নতি গড়ে মাত্র 2.8 point।
8. **(আমাদের lens) Generated test সরাসরি patch-এর রায় দেওয়ার মতো নির্ভরযোগ্য নয়:** ~50% ভুল assertion মানে generated test-এ fail করা মানেই patch ভুল নয় — test-টাই ভুল হতে পারে। তাই dynamic signal-কে **filter** করে (যেমন gold/reference আচরণে pass করা test-ই রাখা) এবং **uncertainty-সহ** report করতে হবে।

---

## ১০. কেন এই Solution অন্যগুলোর থেকে ভালো?

| বৈশিষ্ট্য | TeCo / dynamic | AthenaTest, TOGA, A3Test (heuristic) | CAT-LM (file-level) | **UniTSyn** |
|---|---|---|---|---|
| Alignment granularity | Function | Function | **File** | **Function** |
| Project execute করতে হয়? | হ্যাঁ | সাধারণত না | না | **না** |
| নতুন language যোগ | কঠিন (build system) | নতুন heuristic | নতুন file-matching নিয়ম | **Language server command + এক function + hook** |
| Language | Java (1,270 project) | মূলত Java | Python, Java | **Python, Java, Go, C++, JS** |
| Scale | ছোট | মাঝারি | বড় (60B token) | বড় (2.7M pair, ~1B token) |

**মূল শক্তি:**
1. **Language-agnostic design:** tree-sitter (parsing) + LSP (definition) — দুটোই বহু-ভাষার standard tool।
2. **Execution-free:** environment setup-এর ঝামেলা নেই — scalability-র মূল কারণ।
3. **Data efficiency প্রমাণ:** ছোট model + কম token দিয়ে বড় test model-কে হারানো।
4. **Ablation দিয়ে design choice যাচাই:** pairing (RQ3) ও multilinguality (RQ4) দুটোই আলাদা করে পরীক্ষা।
5. **Leakage নিয়ে সচেতনতা:** নিজেদের সংগ্রহ করা data-তে test না করে public benchmark (HumanEval-X) বেছে নেওয়া — যদিও এর কার্যকারিতা প্রশ্নসাপেক্ষ (Section ১২)।

---

## ১১. কোন পরিস্থিতিতে ভালো কাজ করে, কোথায় করে না

### ✅ ভালো কাজ করে যখন:
- বড় পরিসরে test-generation **training data** বানাতে হবে, বিশেষ করে বহু-ভাষায়।
- Language-এর ভালো language server আছে (Python, Java, Go, C++-এর জন্য mature server আছে)।
- Test-গুলো "setup → focal call → assertion" ধাঁচের সরল unit test।
- একটা **repository-তে কোন test কোন function-কে ছোঁয় তার static map** দরকার (আমাদের patch → প্রাসঙ্গিক test খোঁজার কাজে)।

### ❌ ভালো কাজ করে না / সীমিত যখন:
- Test-এ একাধিক focal function, বা assertion-এর আগে helper/utility call শেষে থাকে — "শেষ call" heuristic ভুল function বাছবে।
- Parameterized test, fixture-ভিত্তিক test, assertion ছাড়া test (exception test), property-based test।
- Dynamic language-এর runtime dispatch (Python-এ duck typing, JS-এ prototype) — static LSP সঠিক definition না-ও পেতে পারে।
- Framework hook নেই এমন language/framework — C++ ও JS-এ মাত্র একটা করে framework (GoogleTest, MochaJS) সমর্থিত।
- Repository-level, বহু-file context দরকার এমন test (integration test) — HumanEval-X-এর একক function দিয়ে এটা মাপা হয়নি।
- **Patch validation-এর মতো fault-detection কাজ** — paper accuracy ও coverage মাপে, bug ধরার ক্ষমতা মাপে না।

---

## ১২. Limitations — দুর্বলতা

### ১২.১ Authors যা নিজেরা স্বীকার করেছেন
1. সম্পূর্ণ স্বয়ংক্রিয় নয় — কিছু manual setting অনিবার্য।
2. C++ ও JavaScript-এ সর্বজনীন testing framework নেই — প্রতিটা framework-এর জন্য developer-কে hook লিখতে হয়। শুধু GoogleTest-এর hook লেখায় C++-এ repository সংখ্যা (pair সংখ্যা) কম।
3. আরও নিখুঁত hook দিলে আরও pair বের করা সম্ভব; তাদের লক্ষ্য extensible framework, প্রতিটা testing suite-এ গভীরে যাওয়া নয়।
4. (Section 4.2-তে) Branch coverage C++ ও Go-তে মাপা যায়নি — tool-এর সীমা।

### ১২.২ আমার Critical Analysis (Professor-level observation)
1. **Pairing-এর নির্ভুলতা কখনো মাপা হয়নি (সবচেয়ে বড় method gap):** Dataset paper হলেও কোনো manual sample audit নেই — কত % pair-এ LSP সঠিক focal function পেয়েছে, "শেষ call before first assertion" heuristic কত % ক্ষেত্রে ভুল (যেমন `assertEquals(expected, helper.compute(x))`-এ আসল call assertion-এর **ভেতরে**; বা শেষ call একটা getter/builder) — জানা যায় না। Dataset-এর label noise অজানা। আমাদের CG10/CG11 ("assurance tool-এর নিজের validity, verifier health")-এর ঠিক উদাহরণ।
2. **Accuracy মাপে oracle-এর সঠিকতা, fault-detection নয়:** একটা assertion canonical solution-এ pass করলেই "accurate"। `assert f(x) == f(x)` বা খুব সাধারণ assertion-ও accurate। **Mutation score বা আসল bug ধরার পরীক্ষা নেই।** Patch assurance-এর জন্য দরকার উল্টোটা — ভুল code-এ fail করা।
3. **"Pass" মানে error ছাড়া চলা — কিন্তু কিছু language-এ assertion fail-ও error দেয় না (আমার hypothesis, যাচাই দরকার):**
   - JavaScript prompt-এ `console.assert` ব্যবহার — Node.js-এ `console.assert` false হলে শুধু message print করে, exception throw করে না। তাহলে ভুল assertion-ওয়ালা JS test-ও "#Pass"-এ গোনা হতে পারে।
   - Java prompt-এ `assert` keyword — JVM-এ assertion default-এ বন্ধ থাকে (`-ea` flag ছাড়া)। বন্ধ থাকলে assert-এর ভেতরের expression **চলেই না** — তাহলে test "error ছাড়া চলে" কিন্তু focal function call-ই হয় না। এটা Java-তে উচ্চ #Pass (103.1, ~62.9%) অথচ কম line coverage (10.78%)-এর অসঙ্গতি ব্যাখ্যা করতে পারে।
   - C++ prompt-এ authors নিজেরা `#undef NDEBUG` দিয়েছেন — অর্থাৎ এই ঝুঁকি সম্পর্কে তারা অন্তত C++-এ সচেতন ছিলেন। Java-তে `-ea` ব্যবহার হয়েছে কিনা paper বলেনি।
   - **আমাদের জন্য শিক্ষা:** generated test-কে dynamic signal বানালে test runner-এর configuration (assertion enabled কিনা) নিজেই verifier health-এর অংশ।
4. **Contamination দাবি দুর্বল:** Paper বলে HumanEval-X-এর focal ও test function "had never been seen by any of the models"। কিন্তু HumanEval (2021) ও HumanEval-X-এর solution ও test GitHub-এ বহুল প্রচারিত; UniTSyn নিজেই 2020-এর পরের GitHub repository mine করেছে, আর baseline model-গুলোর training corpus-ও GitHub-ভিত্তিক। কোনো **decontamination (n-gram/duplicate) check** report করা হয়নি। (CG6)
5. **Toy benchmark — repository-level নয়:** HumanEval-X-এর প্রতিটা focal function একক, ছোট, dependency-মুক্ত। অথচ dataset বাস্তব project থেকে — train/eval distribution আলাদা। বাস্তব repository-তে (mock, fixture, import, class state) generated test কেমন করে, তা মাপা হয়নি।
6. **কোনো variance বা significance নেই:** 10 trial-এর শুধু গড়; standard deviation, confidence interval বা paired test নেই। JavaScript-এ UniTester ও CodeGen2-এর coverage পার্থক্য 0.06 — noise-এর ভেতরে কিনা বলা যায় না। (CG4, CG8)
7. **Text ও result-এ ছোট অসঙ্গতি:**
   - JavaScript নিয়ে paper একই অনুচ্ছেদে বলে উন্নতি "even more significant on languages with insufficient training data, e.g., JavaScript", আবার বলে "the least improvement being in JavaScript"। Table 2 অনুযায়ী (আমার হিসাব) JS-এ base SantaCoder-এর উপর উন্নতি +11.1 point (সবচেয়ে কম) আর সেরা অন্য model-এর উপর +4.6 (সবচেয়ে কম) — দ্বিতীয় বক্তব্য data-র সাথে মেলে, প্রথমটা নয়।
   - "C++ composing executable tests was the most challenging" — #Pass-এ সত্য, কিন্তু accuracy-তে UniTester-এর C++ (55.1) দ্বিতীয় সর্বোচ্চ।
   - UniTester Avg 51.56 → reported 51.5।
   - Unpaired-এর Java-তে baseline-এর নিচে থাকা (Figure 5) text-এ উল্লেখ নেই।
8. **Comparison fairness:** UniTester-এর prompt format (focal + newline + test) ঠিক তার training format-এর মতো; অন্য model-দের জন্য prompt সেভাবে tuned কিনা — instruction-tuned model-এর জন্য আলাদা prompt থাকলেও — prompt sensitivity মাপা হয়নি। আর Java-র closing bracket post-processing "most models"-কে সাহায্য করে বলা হয়েছে — সব model-এ একইভাবে প্রয়োগ হয়েছে কিনা স্পষ্ট নয়। (CG8)
9. **ছোট model-এ সীমাবদ্ধ:** তুলনা শুধু ≤2.7B model-এর মধ্যে। বড় general LLM (সেই সময়ের GPT-4 ইত্যাদি) কেমন করে, বা UniTSyn দিয়ে বড় model train করলে লাভ থাকে কিনা — অজানা।
10. **Loss focal অংশেও:** Training-এ focal function-এর token-এর উপরও loss — model-এর capacity-র একটা অংশ test-এর বদলে production code লেখায় যায়। Test অংশে loss mask করলে কী হতো — ablation নেই।
11. **Dataset-এর অন্যান্য অজানা দিক:** deduplication, license filtering, test-এর মান (flaky/trivial test বাদ দেওয়া), focal function-এর দৈর্ঘ্য বা test-এ assertion সংখ্যার বণ্টন — কিছুই report করা হয়নি।
12. **Release:** v1-এ code ও data "upon acceptance" — reproducibility তখন যাচাই করা সম্ভব ছিল না।

---

## ১৩. Research Gaps — কোথায় কাজ করার সুযোগ আছে

| # | Gap | কেন গুরুত্বপূর্ণ | আমাদের CG | কে কিছুটা কাজ করেছে (আমাদের folder-এ) |
|---|---|---|---|---|
| TG1-G1 | **Generated test-এর fault-detection ক্ষমতা (mutation score, real bug) মাপা হয়নি** | Accuracy ও coverage দিয়ে test ভুল code ধরবে কিনা বোঝা যায় না | CG3, CG1 | Patch Validation (overfitting detection); LLM Test Generation-এর পরের paper-গুলো (CoverUp, TestDecision) — এখনো পড়া বাকি |
| TG1-G2 | **Generated test-এর ~50% assertion ভুল — oracle filtering/calibration** | ভুল test দিয়ে patch বিচার করলে সঠিক patch বাতিল হবে | CG3, CG7, CG11 | LLM Test Generation: Oracle-Guided Program Selection (পড়া বাকি); Trustworthy AI for SE |
| TG1-G3 | **Executability কম (2%–32%)** — চালানোর পরিবেশ ও repair | না চললে কোনো signal নেই | CG3 | LLM Test Generation: ExecutionAgent ("You Name It, I Run It") — পড়া বাকি |
| TG1-G4 | **Repository-level evaluation নেই** (শুধু HumanEval-X) | আমাদের agent patch বাস্তব repository-তে | CG3, CG9 | AI Coding Agents (Agentless-এর reproduction test 213 → 94); Coding-Agent Evaluation & Reliability (SWE-rebench, SWE-Bench Pro) |
| TG1-G5 | **Focal-test linking-এর নির্ভুলতা যাচাই হয়নি** | Dataset label noise; আমরা linking দিয়ে "patch-এর প্রাসঙ্গিক test" খুঁজলে ভুল হবে | CG10, CG11 | Coding-Agent Evaluation & Reliability (monograph-এর verifier versioning) |
| TG1-G6 | **Contamination check নেই** | Score-এর একটা অংশ মুখস্থ হতে পারে | CG6 | Coding-Agent Evaluation & Reliability (SWE-rebench) |
| TG1-G7 | **Variance/significance নেই** | ছোট পার্থক্য (যেমন JS coverage 0.06) অর্থহীন হতে পারে | CG4, CG8 | Coding-Agent Evaluation & Reliability (SWE-rebench SEM, monograph) |
| TG1-G8 | **Test runner configuration-এর validity** (`console.assert`, Java `-ea`) | Verifier নিজেই ভুল "pass" দিতে পারে | CG11, CG12 | Coding-Agent Evaluation & Reliability (verifier health) |
| TG1-G9 | **Generated test-কে patch assessment-এর signal হিসেবে ব্যবহার** — paper-এর scope-এর বাইরে | আমাদের মূল research direction-এর dynamic অংশ | CG1, CG2 | Automated Program Repair (RePaCA — static judge); Patch Validation; AI Coding Agents (Agentless re-ranking) |
| TG1-G10 | **Security-oriented test নেই** | Test functional আচরণ দেখে, vulnerability নয় | CG5 | Security of AI-Generated Code |
| TG1-G11 | **C++/JS-এ কম data (hook-নির্ভরতা)** | বহু-ভাষার assurance-এ এই language-গুলোতে signal দুর্বল | CG9 | Coding-Agent Evaluation & Reliability (SWE-Bench Pro-তে JS/TS/Go) |
| TG1-G12 | **Buggy focal function-এর test** — focal function নিজেই ভুল হলে generated test ভুল আচরণকে "সঠিক" হিসেবে assert করবে | Patch-এর জন্য test লিখলে patch-এর ভুলও test-এ ঢুকে যায় (circularity) | CG1, CG12 | Patch Validation; Trustworthy AI for SE |

**আমার পর্যবেক্ষণ — TG1-G12 কেন বিশেষ গুরুত্বপূর্ণ:** UniTSyn-এর setup-এ focal function (canonical solution) সঠিক ধরে নেওয়া হয় আর test তার আচরণ অনুসরণ করে। কিন্তু আমাদের ক্ষেত্রে focal function = agent-এর **patched code**, যেটা ভুল হতে পারে। Model যদি patched code দেখে test লেখে, তাহলে ভুল আচরণকেই assert করবে — test "pass" করবে, কিন্তু কিছু প্রমাণ করবে না। তাই dynamic signal-এর জন্য test-কে **patch দেখে নয়, issue/specification দেখে** লেখাতে হবে, অথবা original ও patched দুই version-এ চালিয়ে **differential** তুলনা করতে হবে।

---

## ১৪. কী করলে আরও ভালো হবে — Improvement Ideas

1. **Linking audit:** প্রতি language-এ 200টা random pair manually দেখে precision মাপা; "শেষ call" বনাম "assertion-এর ভেতরের call" বনাম "নাম-মিল" heuristic তুলনা।
2. **Mutation score যোগ:** HumanEval-X-এর প্রতিটা canonical solution-এর mutant বানিয়ে generated test-এর kill rate মাপা। Accuracy ও MS-এর মধ্যে correlation দেখা।
3. **Assertion-strength classification:** প্রতিটা assertion-কে strong (নির্দিষ্ট মান তুলনা), weak (type/None check), trivial (tautology) ভাগ করা — "All Smoke, No Alarm"-এর oracle taxonomy-র মতো।
4. **Runner hardening:** Java-তে `-ea`, JavaScript-এ `console.assert`-এর বদলে `assert` module বা throw-করা wrapper, সব language-এ "focal function আসলে call হয়েছে কিনা" check।
5. **Repository-level evaluation:** SWE-bench-ধাঁচের task-এ generated test-কে **reproduction test** হিসেবে মাপা (patch-এর আগে fail, পরে pass)।
6. **Variance report:** 10 sample-এর SD ও bootstrap CI; model-গুলোর paired comparison।
7. **Loss masking ablation:** শুধু test অংশে loss — data efficiency বাড়ে কিনা।
8. **Decontamination:** HumanEval-X-এর solution/test-এর সাথে UniTSyn-এর n-gram overlap check।

---

## ১৫. কোন Gap-এ Research করলে ভালো Result ও Publication আসতে পারে

> ⚠️ ৪র্থ sub-domain-এর প্রথম paper-এর ভিত্তিতে প্রাথমিক মত। এই sub-domain-এর বাকি ৪টা paper পড়ে চূড়ান্ত করবো।

| Gap | SPL3-তে করা সম্ভব? | Novelty | Publication সম্ভাবনা |
|---|---|---|---|
| **TG1-G9 + G2: Filtered generated test-কে agent patch assessment-এর dynamic signal হিসেবে** (static judge-এর পাশে আলাদা signal) | ✅ হ্যাঁ — SWE-bench/SWE-rebench-এর ছোট subset, API model | উচ্চ — আমাদের research direction-এর কেন্দ্র | ⭐⭐⭐⭐⭐ |
| **TG1-G1: Accuracy বনাম mutation score — "accurate" test কি bug ধরে?** (বর্তমান LLM দিয়ে) | ✅ হ্যাঁ — HumanEval-X Python অংশ + mutmut | মাঝারি-উচ্চ; empirical study হিসেবে পরিষ্কার | ⭐⭐⭐⭐ |
| **TG1-G8: Test-runner validity audit** (assertion আসলে enforce হচ্ছে কিনা) | ✅ হ্যাঁ, সস্তা | ছোট কিন্তু তীক্ষ্ণ finding; workshop paper | ⭐⭐⭐ |
| TG1-G5: LSP linking-এর precision audit | ✅ হ্যাঁ, manual কাজ বেশি | মাঝারি | ⭐⭐⭐ |
| নতুন বড় multilingual dataset বানানো | ⚠️ infra ও compute বেশি | কম (UniTSyn আছে) | ⭐⭐ |

**সম্ভাব্য venue (general guidance):** ICSE, FSE, ASE, ISSTA (testing-এর জন্য বিশেষভাবে ISSTA ও ICST); workshop — LLM4Code, AST (Automation of Software Test)। Journal — ACM TOSEM, IEEE TSE, EMSE, STVR (Software Testing, Verification and Reliability), JSS, IST।

---

## ১৬. SPL3 Implementation Perspective — Software-এ কীভাবে আনবো

**Paper implement করা মানে কী?** পুরো 2.7M dataset বানানো বা model train করা নয় (8 × V100, 24 ঘণ্টা — student budget-এর বাইরে)। বরং paper-এর **দুটো উপযোগী অংশ** আমাদের assurance tool-এ নেওয়া:
1. **LSP-ভিত্তিক test-to-code linker** — patch যে function বদলেছে, repository-র কোন কোন test তাকে ছোঁয়।
2. **Generated test-এর evaluation harness** — accuracy, executability, coverage, এবং paper-এ না থাকা mutation score।

**প্রস্তাবিত module:**
| Module | কাজ | Tool (প্রস্তাব) |
|---|---|---|
| 1. Parser | Python file → AST, test function চেনা (pytest/unittest hook) | tree-sitter (Python binding) বা Python-এর `ast` |
| 2. Focal linker | Test-এর focal call (paper-এর heuristic) → LSP দিয়ে definition | একটা Python language server (যেমন jedi-language-server বা pylsp) + LSP client library |
| 3. Patch mapper | Agent-এর diff → পরিবর্তিত function → module 2 দিয়ে সংশ্লিষ্ট বিদ্যমান test | `unidiff` + module 2 |
| 4. Test generator | Issue/spec থেকে focal function-এর জন্য test (patch দেখে নয় — TG1-G12) | যেকোনো LLM API |
| 5. Oracle filter | Generated test original ও patched code-এ চালিয়ে differential; reference থাকলে reference-এ fail করা assertion বাদ | pytest |
| 6. Metrics | #Pass, line/branch coverage, mutation score, assertion-strength | coverage.py (`--branch`), mutmut |
| 7. Assurance report | প্রতিটা signal আলাদা, uncertainty (k sample-এর SD), tool ও model version সহ | JSON + HTML |

**Practical সতর্কতা:**
- Language server চালানো ও JSON-RPC handle করা প্রথমবার ঝামেলার — প্রথমে শুধু Python, একটা server।
- Mutation testing ধীর — প্রতি focal function-এ mutant সংখ্যা সীমিত রাখতে হবে; Windows-এ কিছু Python mutation tool-এর সীমাবদ্ধতা থাকতে পারে, তাই WSL2-এ চালানো নিরাপদ বিকল্প।
- Test runner validity (TG1-G8) প্রথম দিন থেকেই: assertion আসলে enforce হচ্ছে কিনা একটা "sanity mutant" (জোর করে ভুল output) দিয়ে পরীক্ষা।

---

## ১৭. পরবর্তী গবেষণায় এই Paper-এর প্রভাব (Context)

- এই paper **2024-এর শুরুর** — তখন test generation-এর প্রশ্ন ছিল "ছোট model-কে ভালো test data দিয়ে কীভাবে train করবো"। 2026-এ প্রশ্ন বদলে "frontier agent-রা নিজেরাই test লেখে — সেই test কতটা বিশ্বাসযোগ্য?" (Section ২১)।
- আমাদের folder-এর এই sub-domain-এর পরের paper-গুলো (CoverUp — coverage-guided generation; TestDecision; ExecutionAgent — যেকোনো project-এর test চালানো; Oracle-Guided Program Selection) এই paper-এর খোলা প্রশ্নগুলোর (coverage কম, executability কম, oracle অনিশ্চিত) দিকেই কাজ করছে বলে নাম থেকে মনে হয় — পড়ার পর নিশ্চিত করবো।
- UniTSyn-এর citation সংখ্যা বা পরবর্তী version-এর তথ্য আমার কাছে থাকা উৎসে নেই — তাই এখানে দাবি করছি না।

---

## ১৮. Supervisor-এর সম্ভাব্য প্রশ্ন ও উত্তর (Viva Prep)

**Q1. Focal function কী, আর focal-test pair কেন দরকার?**
A: যে function-কে test আসলে পরীক্ষা করে সেটাই focal function। জোড়া থাকলে model test লেখার সময় function-এর code দেখে তার আচরণ ও logic path বুঝতে পারে; না থাকলে সম্ভাব্য সব function মুখস্থ করে অনুমান করতে হয়। RQ3-এর ablation দেখায় Unpaired থেকে Paired-এ বড় লাফ (vector data থেকে আমার পড়া হিসাবে Overall ≈38.6 থেকে 51.5)।

**Q2. LSP কেন ব্যবহার করলো, dynamic analysis কেন নয়?**
A: Dynamic analysis-এ প্রতিটা project build ও run করতে হয় — TeCo সহজতম language Java-তেও মাত্র 1,270 project পেরেছে। LSP static: editor-এর "Go to Definition"-এর মতো language server-কে প্রশ্ন করে definition পাওয়া যায়, project চালাতে হয় না, আর নতুন language-এ শুধু server-এর command লাগে। ফলে 145,144 project-এ scale করা গেছে।

**Q3. Focal call কীভাবে চেনে? এর দুর্বলতা কী?**
A: TeCo-র নিয়ম — postorder-এ প্রথম assertion-এর আগের শেষ call যেটা repository-র কোনো function-কে ডাকে। দুর্বলতা: focal call assertion-এর ভেতরে থাকলে (`assertEquals(3, add(1,2))`), বা শেষ call একটা helper হলে ভুল function বাছবে। আর paper এর নির্ভুলতা কখনো মাপেনি।

**Q4. UniTester কি fine-tuned model?**
A: Instruction fine-tuning নয় — continual (autoregressive) training। SantaCoder 1.1B-কে focal + newline + test টানা text-এ next-token prediction দিয়ে 36,000 step, batch 32, sequence 2048, LR 5e-5, 8 V100-এ ~24 ঘণ্টা train করা।

**Q5. Accuracy 51.5% মানে কী? এটা কি ভালো?**
A: Generated assertion-গুলোর মধ্যে 51.5% সঠিক solution-এ সত্য হয় (5 language-এর গড়)। অন্যদের (29.2–37.7) চেয়ে অনেক ভালো, কিন্তু absolute অর্থে প্রায় অর্ধেক assertion ভুল। আর এটা bug ধরার ক্ষমতা মাপে না — mutation score নেই।

**Q6. "#Pass 103.1" কীভাবে 164-এর মধ্যে, আর তবুও coverage মাত্র 10.78% কেন?**
A: #Pass = 164 task-এর মধ্যে কতগুলোর test error ছাড়া চলে, 10 trial-এর গড় → Java-তে ~62.9%। Coverage কম হওয়ার একটা সম্ভাব্য কারণ (আমার hypothesis): Java-র `assert` default-এ বন্ধ, তাই assert-এর ভেতরের focal call চলেই না, অথচ test "error ছাড়া" শেষ হয়। Paper `-ea` ব্যবহার করেছে কিনা বলেনি — যাচাই দরকার।

**Q7. Multilingual training কি সবসময় ভালো?**
A: সামগ্রিকভাবে হ্যাঁ (Overall ≈37.7 Mono বনাম 51.5 Multi), কিন্তু Python-এ শুধু-Python model (≈55.2) ভালো। Python থেকে JS/Go-তে transfer হয়, C++/Java-তে baseline-এর নিচে নামে — negative transfer।

**Q8. HumanEval-X ব্যবহার করে কি contamination এড়ানো গেছে?**
A: Paper তাই দাবি করে, কিন্তু কোনো decontamination check নেই। HumanEval 2021 থেকে public, আর dataset ও baseline model দুটোই GitHub-ভিত্তিক — তাই দাবিটা দুর্বল। তাছাড়া HumanEval-X ছোট একক function — বাস্তব repository-র মতো নয়।

**Q9. এই paper তোমার assurance research-এ কীভাবে কাজে লাগবে?**
A: দুইভাবে। (১) LSP-ভিত্তিক linking দিয়ে agent patch-এর পরিবর্তিত function-এর সাথে সম্পর্কিত test খুঁজে বের করা। (২) এর ফলাফল সতর্ক করে যে generated test-এর অর্ধেক assertion ভুল ও বেশিরভাগ test চলে না — তাই generated test-কে সরাসরি রায় না বানিয়ে, filter করে, uncertainty-সহ, আলাদা dynamic signal হিসেবে assurance report-এ রাখবো।

**Q10. এই paper-এর সবচেয়ে বড় দুর্বলতা কী?**
A: Dataset paper হয়েও dataset-এর label (focal-test pairing)-এর নির্ভুলতা মাপা হয়নি, আর test-এর মান মাপা হয়েছে এমন metric দিয়ে (accuracy, coverage) যা bug ধরার ক্ষমতা প্রমাণ করে না।

---

## ১৯. Glossary (দ্রুত মনে রাখার জন্য)

| Term | অর্থ |
|---|---|
| Unit test | একটা function-কে নির্দিষ্ট input দিয়ে চালিয়ে output যাচাই করা ছোট code |
| Focal function | যে function-কে test আসলে পরীক্ষা করছে |
| Focal-test pair | (focal function, test function) জোড়া |
| Test oracle | সঠিক output কী হওয়া উচিত তার সিদ্ধান্ত |
| Assertion | Oracle-কে code-এ প্রকাশ (`assert ...`) |
| Test-to-code linking | কোন test কোন function-কে test করে তা বের করা |
| AST | Code-এর গাছ-আকৃতির structure |
| tree-sitter | বহু-ভাষার parser generator |
| LSP | Editor ও language server-এর মধ্যে standard protocol (definition খোঁজা ইত্যাদি) |
| Hook | নতুন language/framework-এ test চেনার জন্য plug-in function |
| Continual training | Train করা model-কে নতুন domain-এর data-তে একই objective-এ আরও train |
| Packing | বিভিন্ন sample জুড়ে নির্দিষ্ট দৈর্ঘ্যের sequence বানানো |
| Temperature | Sampling-এর randomness নিয়ন্ত্রণ |
| Line / Branch coverage | কত % line / branch outcome চলেছে |
| #Pass | Error ছাড়া চলা test-এর সংখ্যা (164-এর মধ্যে) |
| Mutation score | কৃত্রিম bug-এর কত % test ধরতে পারে |
| Positive / negative transfer | এক language-এর শিক্ষা অন্যটায় সাহায্য / ক্ষতি করা |
| HumanEval-X | 164 problem × 5 language-এর benchmark |

---

## ২০. এক নজরে সারাংশ (Summary Card)

| | |
|---|---|
| **Problem** | Code LLM ভালো test লেখে না; test ও focal function-এর জোড়া-বাঁধা বড় multilingual data নেই; বিদ্যমান সংগ্রহ পদ্ধতি scale করে না |
| **Solution** | tree-sitter + LSP দিয়ে execution-ছাড়া function-level focal-test pairing; 2.7M pair, 5 language, 145,144 project |
| **Validation model** | UniTester: SantaCoder 1.1B, ~1B token, 36k step, 8 V100, ~24h |
| **Key result** | Accuracy গড় 51.5% (পরের সেরা WizardCoder 37.7; CAT-LM 33.9); গড় pass rate ~32% (CodeGen2 ~16.5%); line coverage গড়ে +2.8 point |
| **Key insight** | Pairing-ই মূল লাভ; multilingual সামগ্রিকভাবে ভালো কিন্তু transfer অসম |
| **Main limitation** | Pairing নির্ভুলতা অমাপা; mutation score নেই; HumanEval-X toy benchmark; variance নেই; test runner validity প্রশ্নসাপেক্ষ |
| **আমাদের জন্য** | LSP linking → patch-প্রাসঙ্গিক test খোঁজা; generated test = দুর্বল কিন্তু দরকারি dynamic signal — filter ও uncertainty-সহ ব্যবহার করতে হবে (CG1, CG3) |

---

## ২১. বর্তমান (2026) প্রেক্ষাপট — আজকের Model ও Agent-দের সাথে তুলনা

> **উৎস:** এই section-এর সব current-state তথ্য `00_Current_State_2026_Sources.md` (fact sheet, compiled 2026-10-28) থেকে নেওয়া। প্রতিটা সংখ্যার পাশে লেখা আছে সেটা **কোম্পানির নিজের দাবি (vendor-reported)** নাকি **স্বাধীনভাবে মাপা (independent)**। Fact sheet যেটাকে "search-snippet only" বলেছে, সেটা এখানেও তাই চিহ্নিত — supervisor-কে দেখানোর আগে মূল উৎস খুলে যাচাই করা উচিত। আমার নিজের যুক্তি "আমার পর্যবেক্ষণ" দিয়ে আলাদা করা।
>
> **গুরুত্বপূর্ণ সীমা:** fact sheet-এ **unit test generation-এর benchmark (HumanEval-X test accuracy, coverage, mutation score) নিয়ে বর্তমান model-এর কোনো সংখ্যা নেই**। Reproduction-test benchmark (SWT-bench, TDD-Bench)-এও Opus 5.5, GPT-6 বা Gemini 4-এর কোনো 2026 entry পাওয়া যায়নি। তাই এই paper-এর Table 2/3-এর সাথে আজকের model-এর সরাসরি তুলনা **সম্ভব নয়** — এটা নিজেই একটা gap।

### ২১.১ Paper-এর সময় বনাম এখন

| দিক | Paper-এ (arXiv v1, Feb 2024) | এখন, October 2026 | উৎস |
|---|---|---|---|
| Test লেখে কে | ছোট (≤2.7B) model, prompt-এ assert keyword দিয়ে শুরু করানো | Frontier coding agent (Codex, Copilot, Devin, Cursor, Claude Code) নিজেরাই PR-এ test যোগ করে; AI test-adding commit-এর 16.4% লিখেছে (**independent**, search-snippet only) | Fact sheet §6, MSR 2026 Mining Challenge (arXiv 2603.13724) |
| Oracle-এর মান | Assertion accuracy সর্বোচ্চ গড় 51.5% (HumanEval-X) | Agent-দের 86,156 test-file patch-এর **80.2%**-এ weak বা কোনো স্পষ্ট oracle নেই; strong oracle থাকলে merge-এর odds বাড়ে (OR 1.28, p<0.001) (**independent**) | "All Smoke, No Alarm", arXiv 2606.18168, 2026-06-16 |
| Weak assertion হার | মাপা হয়নি | Agent test-এ weak assertion ~14.3% বনাম মানুষের ~11.9% (figure secondary summary থেকে, **যাচাই করা নয়**) | arXiv 2607.12068 |
| Mocking | আলোচিত নয় (HumanEval-X-এ mock লাগে না) | Agent commit-এর 36% test-এ mock যোগ করে, non-agent-এর 26%; agent commit-এর 23% test file ছোঁয়, non-agent-এর 13% (**independent**, search-snippet only) | arXiv 2602.00409, MSR 2026 |
| Coverage | গড় line coverage সর্বোচ্চ ~28%, উন্নতি +2.8 point | AI-এর test বেশি লম্বা, বেশি assertion; coverage gain মানুষের test-এর সাথে তুলনীয় (**independent**, search-snippet only) — কিন্তু HumanEval-X-ধাঁচের সংখ্যা নেই | arXiv 2603.13724 |
| Test-এর উপযোগিতা | ধরে নেওয়া হয়েছে ভালো test = ভালো | "Rethinking the Value of Agent-Generated Tests": issue resolution-এ test লেখার উন্নতি সীমিত, প্রায়ই observation-based debugging দিয়ে প্রতিস্থাপিত (**independent**, search-snippet only) | HF papers 2602.07900 |
| Vendor দাবি | — | Fable 5.1 "can write its own tests to check its work"; "less likely to disable a failing test to pass" (**vendor-reported, qualitative**, কোনো সংখ্যা নেই) | Anthropic Fable page; AWS blog, 2026-09-01 |
| Reproduction test benchmark | — | SWT-bench, TDD-Bench-এ বর্তমান model-এর ফল **পাওয়া যায়নি** | Fact sheet §6 |
| Benchmark-এর test-এর মান | HumanEval-X-এর test ধরে নেওয়া হয়েছে নির্ভুল | SWE-bench Verified-এর audited hard subset-এর অন্তত 59.4%-এ flawed test (OpenAI, search-snippet only); SWE-Bench Pro-র public task-এর 27.4% (automated + Codex review) থেকে 34.1% (5 জন মানুষ) broken (secondary report) | Fact sheet §3 |

**আমার পর্যবেক্ষণ:** দুটো সংখ্যা সরাসরি তুলনীয় নয় — paper-এর 51.5% হলো "assertion সঠিক code-এ সত্য কিনা", আর 80.2% হলো "test patch-এ শক্ত oracle আছে কিনা"। কিন্তু দুটো একই দিকে ইঙ্গিত করে: **2024-এর ছোট model থেকে 2026-এর agent পর্যন্ত, generated test-এর oracle-ই দুর্বলতম অংশ**। আর এই paper accuracy মাপলেও oracle **শক্তি** মাপেনি — 2026-এর গবেষণা ঠিক সেই মাত্রাটাই মাপছে।

### ২১.২ কোন Finding এখনো সত্য, কোনটা পুরনো হয়ে গেছে

- **এখনো সত্য, আরও বড় পরিসরে — "LLM-এর test-এর oracle দুর্বল" (Key Finding ৬):** 2026-এ 33,596 agent PR-এর test patch-এর 80.2%-এ weak/no oracle (independent)। Paper-এর ~50% ভুল assertion থেকে সমস্যার রূপ বদলেছে — "ভুল oracle" থেকে "দুর্বল বা অনুপস্থিত oracle" — কিন্তু সমস্যা রয়ে গেছে।
- **সম্ভবত পুরনো (কিন্তু প্রমাণ নেই) — "বেশিরভাগ generated test চলেই না (2%–32%)" (Key Finding ৫):** আজকের agent নিজে test চালিয়ে দেখে ঠিক করতে পারে, আর তাদের test PR-এ merge হচ্ছে — তাই executability-র সমস্যা অনেক কমেছে বলে মনে হয়। **কিন্তু fact sheet-এ বর্তমান model-এর test executability-র কোনো সরাসরি সংখ্যা নেই** — এটা অনুমান, মাপা তথ্য নয়।
- **পুরনো — "ছোট test-specific model + ভালো data বড় general model-কে হারায়":** Paper-এর তুলনা শুধু ≤2.7B model-এর মধ্যে। 2026-এ test লেখা হয় frontier general agent দিয়ে; ছোট test-specific model-এর সাথে তুলনার কোনো তথ্য fact sheet-এ নেই।
- **এখনো সত্য — "coverage ≠ quality":** 2026-এর MSR গবেষণা বলছে AI test-এর coverage gain মানুষের সাথে তুলনীয় (search-snippet), অথচ একই সময়ে 80.2% weak oracle — অর্থাৎ coverage ভালো হলেও bug ধরার ক্ষমতা নিশ্চিত নয়। এটা paper-এর নিজের "coverage is necessary, not sufficient" বক্তব্যকে শক্ত করে।
- **নতুন সমস্যা, paper-এ ছিল না — over-mocking ও test tampering:** Agent-রা বেশি mock যোগ করে (36% বনাম 26%), আর vendor নিজেই "less likely to disable a failing test" দাবি করছে — অর্থাৎ failing test বন্ধ করে দেওয়া একটা বাস্তব আচরণ ছিল। Paper-এর setting-এ (model শুধু test লেখে, code নয়) এই সমস্যা উঠতো না। (CG12)
- **এখনো প্রাসঙ্গিক — test-to-code linking:** বর্তমান agent-ও repository-তে কোন test কোন function ছোঁয় তা খুঁজতে হয়; LSP-ভিত্তিক linking-এর ধারণা পুরনো হয়নি। তবে বর্তমান agent-এর linking accuracy-র কোনো সংখ্যা fact sheet-এ **নেই**।

### ২১.৩ Gap-গুলো আজও খোলা কিনা

| Gap | 2026-এ অবস্থা | প্রমাণ |
|---|---|---|
| TG1-G1 / CG3: Fault-detection (mutation score) মাপা হয়নি | **খোলা** | Fact sheet-এ বর্তমান model-এর generated test-এর mutation score-এর কোনো সংখ্যা নেই; শুধু oracle-strength (80.2% weak/no) মাপা হয়েছে |
| TG1-G2 / CG3, CG7: Oracle-এর নির্ভুলতা ও calibration | **খোলা, বড় পরিসরে নিশ্চিত** | 80.2% weak/no oracle (independent); weak assertion 14.3% বনাম 11.9% (unverified) |
| TG1-G3 / CG3: Executability | **বর্তমান model-এর তথ্য পাওয়া যায়নি** | SWT-bench/TDD-Bench-এ কোনো 2026 entry নেই |
| TG1-G4 / CG9: Repository-level evaluation | **আংশিক** | এখন AIDev-ধরনের বাস্তব PR dataset-এ test মাপা হচ্ছে (independent), কিন্তু এগুলো মূলত 2025-এর agent; Opus 5.5/GPT-6-generation-এর জন্য নয় |
| TG1-G5 / CG10, CG11: Linking-এর নির্ভুলতা | **খোলা — তথ্য নেই** | Fact sheet-এ কিছু নেই |
| TG1-G6 / CG6: Contamination | **খোলা, আরও তীব্র** | OpenAI SWE-bench Verified-কে "increasingly contaminated" বলে ছেড়েছে (search-snippet only); HumanEval-ধাঁচের পুরনো benchmark-এ ঝুঁকি আরও বেশি (আমার পর্যবেক্ষণ) |
| TG1-G7 / CG4, CG8: Variance ও significance | **খোলা (মাপা শুরু হয়েছে)** | Noise Floor Audit: prompt-এর অর্থ-অপরিবর্তিত পরিবর্তনে SD rerun-এর চেয়ে 11–58 গুণ বেশি (independent); test generation-specific variance-এর তথ্য নেই |
| TG1-G8 / CG11, CG12: Test runner/verifier validity | **খোলা, নতুন রূপে** | Fable 5.1-এর "less likely to disable a failing test" দাবি (vendor) দেখায় test বন্ধ করা বাস্তব সমস্যা; SWE-Bench Pro Verified-এ GLM-5.2 78.80% থেকে safeguard দিলে 57.32% (independent) |
| TG1-G9 / CG1, CG2: Generated test দিয়ে patch assessment | **খোলা** | PatchDiff: plausible patch-এর 29.6% gold থেকে ভিন্ন আচরণ (independent, 2025 model); বর্তমান model-এ পুনরায় মাপা হয়নি। PROBE: program variant দিয়ে দুর্বল test ধরা যায় (search-snippet only) |
| TG1-G10 / CG5: Security-oriented test | **খোলা** | SusVibes/Endor: FuncPass 62.6–84.4% কিন্তু SecPass 7.8–17.3% (independent, পুরনো agent); বর্তমান model-এর ফল নেই |
| TG1-G11 / CG9: C++/JS-এ কম data | **তথ্য পাওয়া যায়নি** | Fact sheet-এ language-ভিত্তিক test generation-এর তথ্য নেই |
| TG1-G12 / CG1, CG12: Buggy code দেখে test লেখা (circularity) | **খোলা** | "Rethinking the Value of Agent-Generated Tests" (search-snippet only) — agent-এর test-এর মূল্য সীমিত; সরাসরি circularity মাপা কোনো গবেষণা fact sheet-এ নেই |

### ২১.৪ বর্তমান Model দিয়ে আবার পরীক্ষা করলে — SPL3 Idea (cost-aware)

1. **UniTSyn-এর RQ1/RQ2 + mutation score, একটা সস্তা current model দিয়ে:** HumanEval-X-এর Python অংশ (164 task), paper-এর হুবহু setting (input ≤800 token, output ≤256, T = 0.2, 10 sample)। Metric: accuracy, #Pass, line/branch coverage, **আর mutation score (নতুন)**।
   - **আমার হিসাব (খরচ):** 164 × 10 = 1,640 call; input সর্বোচ্চ 1,640 × 800 = 1.31M token, output সর্বোচ্চ 1,640 × 256 = 0.42M token। GPT-6.1 Terra-র vendor-reported দাম (USD 1 input / USD 5 output per million) ধরলে ≈ 1.31 + 2.10 = **USD 3.4-এর মতো**। পুরো 5 language (8,200 call) করলে ≈ 6.56 + 10.50 = **USD 17-এর মতো**। Opus 5.5 (USD 4 / USD 20, price search-snippet only) দিয়ে 5 language ≈ 26.2 + 42.0 = **USD 68-এর মতো**। (Reasoning token বা দীর্ঘ output হলে খরচ বাড়বে; এটা upper-bound-ধাঁচের মোটামুটি হিসাব।)
   - **যে gap দেখাবে:** TG1-G1 — accuracy উঁচু হলেও mutation score কম কিনা; আর 2024-এর 52.5% (Python) থেকে বর্তমান model কতদূর এগিয়েছে — fact sheet অনুযায়ী এই সংখ্যা **কেউ মাপেনি**।
   - **সতর্কতা:** HumanEval-X contamination-এর ঝুঁকি আজ আরও বেশি — ফলাফলকে "upper bound" হিসেবে report করতে হবে।
2. **Runner validity sanity check:** একই generated Java ও JavaScript test `-ea` সহ/ছাড়া এবং `console.assert` বনাম throw-করা assert দিয়ে চালিয়ে #Pass কতটা বদলায়। খরচ প্রায় শূন্য (শুধু execution)। **Gap:** TG1-G8 — paper-এর Java #Pass 103.1 বনাম coverage 10.78-এর অসঙ্গতির ব্যাখ্যা।
3. **Patch-assessment-এর dynamic signal (মূল idea):** SWE-rebench-এর সর্বশেষ window থেকে ~30টা task, প্রতিটায় agent patch (প্রকাশিত trajectory থেকে, বা সস্তা model দিয়ে)। (ক) LSP linker দিয়ে পরিবর্তিত function-এর বিদ্যমান test খোঁজা; (খ) **issue text থেকে** (patch দেখে নয়) 5টা test generate; (গ) original, agent-patched ও gold-patched code-এ চালিয়ে differential। **Gap:** TG1-G9 + TG1-G12 + CG1 — generated test কত % ভুল patch ধরে, আর কত % সঠিক patch ভুলভাবে বাতিল করে।
   - **আমার হিসাব (খরচ):** 30 task × 5 test × 3 run (variance-এর জন্য) = 450 generation; প্রতিটা ~3k input + ~1k output token ধরলে (আমার অনুমান) 1.35M input + 0.45M output → GPT-6.1 Terra-তে ≈ 1.35 + 2.25 = **USD 3.6-এর মতো**।
4. **Oracle-strength audit:** উপরের generated test-গুলোকে "All Smoke, No Alarm"-এর মতো weak/strong oracle-এ ভাগ করে, oracle strength আর ভুল-patch ধরার হারের সম্পর্ক দেখা। **Gap:** TG1-G2 — 80.2% weak oracle-এর পরিসংখ্যান কি আমাদের patch-assessment setting-এ প্রযোজ্য?

### ২১.৫ Supervisor-এর সম্ভাব্য প্রশ্ন (2026 প্রসঙ্গে)

**Q1. এখন frontier agent-রাই test লেখে — তাহলে 1.1B model-এর এই paper কি আর প্রাসঙ্গিক?**
A: Model অংশটা পুরনো, কিন্তু দুটো জিনিস প্রাসঙ্গিক। (১) LSP-ভিত্তিক test-to-code linking — আমাদের tool-এ patch-এর সাথে প্রাসঙ্গিক test খুঁজতে কাজে লাগবে। (২) এর মূল সতর্কবার্তা — generated test-এর oracle দুর্বল — 2026-এ বড় পরিসরে নিশ্চিত হয়েছে: agent-দের test patch-এর 80.2%-এ weak বা কোনো oracle নেই (independent)।

**Q2. Opus 5.5 বা GPT-6 HumanEval-X-এ test accuracy কত পায়?**
A: জানা নেই — fact sheet-এ বর্তমান model-এর unit-test-generation benchmark-এর কোনো সংখ্যা নেই, এমনকি SWT-bench/TDD-Bench-এও 2026 entry নেই। এই অনুপস্থিতিটাই আমাদের SPL3-এর একটা ছোট, সস্তা contribution-এর সুযোগ (২১.৪-এর idea 1)।

**Q3. Agent-এর লেখা test দিয়ে কি agent-এর patch যাচাই করা যায়?**
A: সরাসরি নয়। Agent patch দেখে test লিখলে নিজের ভুলকেই assert করতে পারে (TG1-G12), oracle দুর্বল হতে পারে (80.2%), আর vendor-রাও failing test বন্ধ করার প্রবণতা স্বীকার করছে। তাই আমাদের design-এ test generate হবে issue থেকে, চালানো হবে original/patched/gold-এ differential-ভাবে, আর assurance report-এ এটা static judge-এর পাশে **আলাদা signal** হিসেবে uncertainty ও version সহ থাকবে — একক weighted score-এ মিশিয়ে নয়।
