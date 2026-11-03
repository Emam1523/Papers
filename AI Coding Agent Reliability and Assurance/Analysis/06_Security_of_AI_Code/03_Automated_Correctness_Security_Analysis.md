# Paper Analysis 03 (Security): Automating the Correctness Assessment of AI-Generated Code for Security Contexts

> Sub-domain: Security of AI-Generated Code
> PDF: Security of AI-Generated Code/Automating the correctness assessment of AI-generated code for security.pdf

## ০. Bibliographic info

| Field | তথ্য |
|---|---|
| Title | Automating the correctness assessment of AI-generated code for security contexts |
| Authors | Domenico Cotroneo, Alessio Foggia, Cristina Improta, Pietro Liguori, Roberto Natella (University of Naples Federico II, Italy) |
| Venue | The Journal of Systems and Software (JSS), volume 216 |
| Year / article no. | 2024, article 112113 |
| DOI | 10.1016/j.jss.2024.112113 |
| Dates (paper-এ আছে) | Received 21 October 2023; revised 10 March 2024; accepted 23 May 2024; online 24 May 2024; Editor: Burak Turhan |
| License | Open access, CC BY-NC-ND 4.0 |
| Tool name | ACCA (Assembly Code Correctness Assessment) |
| Code / data | github.com/dessertlab/ACCA এবং github.com/dessertlab/Shellcode_IA32 |
| Paper type | নতুন automated assessment method + empirical comparison (human evaluation vs baseline) |

## ★ সহজ ভাষায় পুরো Paper (প্রথমবার পড়ার জন্য)

### ক. Paper-টা কী নিয়ে?

- এটা একটা **নতুন tool + তার পরীক্ষা**-র paper। Tool-এর নাম ACCA।
- বানিয়েছেন ইতালির University of Naples Federico II-এর পাঁচজন গবেষক (Cotroneo, Foggia, Improta, Liguori, Natella)। ছাপা হয়েছে Journal of Systems and Software-এ, ২০২৪ সালে।
- AI আজকাল security-র কাজে ব্যবহৃত ছোট low-level code (assembly, যেটা প্রায় machine-এর ভাষা) লিখে দিতে পারে। প্রশ্ন হলো: AI-এর লেখা সেই code ঠিক কিনা, তা মানুষ না দেখে কম্পিউটার নিজে কীভাবে বলবে?
- Paper-এ tool বানানো হয়েছে, তারপর সেটা মানুষের রায়ের সাথে এবং পুরোনো পদ্ধতির সাথে মেলানো হয়েছে।

### খ. সমস্যাটা কী ছিল?

- AI-এর লেখা code ঠিক কিনা দেখার সবচেয়ে ভালো উপায় ছিল মানুষ দিয়ে পড়ানো। কিন্তু সেটা ধীর, ক্লান্তিকর, আর দরকার হয় expert।
- তাই লোকে BLEU বা Edit Distance-এর মতো metric ব্যবহার করত। এরা শুধু দুই code-এর **লেখা কতটা মেলে** সেটা দেখে। কোডটা কাজে কী করে, সেটা দেখে না।
- একটা উদাহরণ: `mov EDX, EAX` আর `push EAX; pop EDX` দেখতে আলাদা, কিন্তু দুটোর কাজ একই। Metric একে ভুল বলে নিচু নম্বর দেয়।
- উল্টোটাও হয়: `mov DL, 5` আর `mov BL, 5` প্রায় একই লেখা, কিন্তু আলাদা জায়গায় মান বসায়, তাই ভুল। Metric একে প্রায় ঠিক বলে দেয়।
- এটা অনেকটা পরীক্ষার খাতায় শুধু হুবহু উত্তর মেলানোর মতো। ছাত্র একই উত্তর অন্য ভাষায় লিখলে শূন্য পায়।

### গ. Paper কী solve করেছে?

- ACCA নামের একটা automatic checker বানিয়েছে। সে লেখা না মিলিয়ে code চালিয়ে **শেষ অবস্থা** (register, flag, stack) মেলায়।
- ৫টি generator থেকে মোট 2,950টি prediction এই tool দিয়ে যাচাই করেছে এবং মানুষের রায়ের সাথে তুলনা করেছে।
- ACCA মানুষের সাথে গড়ে 0.93 sample-এ একমত। মানে ১০০টার মধ্যে প্রায় ৯৩টিতে একই রায়।
- Correlation (দুই রায় কতটা একসাথে ওঠানামা করে) 0.84। সেরা পুরোনো metric Edit Distance-এর ছিল 0.69। মানে ACCA মানুষের চিন্তার অনেক কাছাকাছি।
- গড়ে একটি snippet যাচাইয়ে 0.20 সেকেন্ড লাগে, মানুষের লাগে প্রায় 20 সেকেন্ড। মানে প্রায় ১০০ গুণ দ্রুত।
- দুর্বলতা: ACCA একটু বেশি কড়া। মানুষ যেগুলো ঠিক বলে, তার কিছু সে ভুল বলে দেয় (ACCA 65% correct বনাম মানুষ 71%)।

### ঘ. কীভাবে solve করেছে?

1. আগে দেখে prediction আর সঠিক উত্তর (reference) হুবহু এক কিনা। এক হলে সঙ্গে সঙ্গে "ঠিক"। এতে সময় বাঁচে।
2. তারপর snippet-কে ছোট একটা পূর্ণ program বানিয়ে assemble করে। Assemble মানে assembly-কে machine code-এ বদলানো। এতে syntax ঠিক আছে কিনা বোঝা যায়।
3. কোনো label snippet-এ নেই বলে error এলে ACCA নিজে একটা বানানো label বসিয়ে আবার চেষ্টা করে।
4. Syntax ভুল হলে সঙ্গে সঙ্গে "ভুল"। বাকি ক্ষেত্রে reference আর prediction দুটোকেই angr নামের tool দিয়ে symbolic execution করে। মানে আসল সংখ্যার বদলে "যেকোনো মান" ধরে সব সম্ভাব্য পথ চালায়।
5. দুই program-এর প্রতিটি পথের শেষে register, flag, stack আর path-র শর্ত মেলায়। সব মিললে "semantically ঠিক"।
6. Loop থাকলে পথ খুব বেড়ে যায়। তাই 100 ধাপের বেশি গেলে থেমে "ভুল" ধরে নেয়।
7. এরপর 5টি AI generator-এর output-এ ACCA চালায় এবং ৩ জন মানুষ evaluator-এর রায়ের সাথে মেলায়।
8. তুলনায় Compilation, BLEU, Edit Distance, ChatGPT-judge ইত্যাদি baseline-ও চালায়। মাপে matching rate, offset আর Pearson correlation।

### ঙ. এরপর কী করা যায়?

- Authors বলেছেন: Python-এর মতো high-level ভাষায় নেওয়া, আর static analysis ও binary matching-এর সাথে জোড়া লাগানো।
- এখনও খোলা: ACCA বৈধ কিন্তু ভিন্ন ধরনের code-কে ভুল বলে দেয় (false negative)। আবার কিছু ভুল code-কে ঠিক বলে দেয় (false positive)।
- Paper-এ recall, precision, κ আর confidence interval নেই। এগুলো আমরা নিজেরা হিসাব করে বের করতে পারি।
- SPL3-তে আমরা ACCA-কে LLM judge-এর সাথে তুলনা করতে পারি। ACCA-র ভুল এক দিকে, LLM judge-এর ভুল উল্টো দিকে, তাই দুটো মিলিয়ে ভালো ফল হতে পারে।
- আমরা ACCA-কে ঠকানোর (gaming) পরীক্ষা করতে পারি, আর "could not verify" নামে তৃতীয় একটা ফলাফল যোগ করতে পারি।
- ধারণাটা ছোট Python patch-এও নেওয়া যায়: reference patch আর agent patch একই input-এ চালিয়ে output মেলানো।

> **মনে রাখো:**
> ACCA code-এর লেখা না মিলিয়ে চালিয়ে শেষ অবস্থা মেলায়, তাই মানুষের সাথে 0.93 একমত।
> সে নিশ্চিত ঠিক ধরায় ভালো, কিন্তু বৈধ বিকল্প code-কে ভুল বলে ফেলে এবং security মাপে না।
> আমাদের কাজের মূল প্রশ্ন: assurance tool নিজে কতটা বিশ্বাসযোগ্য?

## ১. TL;DR

- Paper-এর প্রশ্ন: AI যে security-oriented assembly code (shellcode) বানায়, সেটা correct কিনা মানুষ ছাড়া কীভাবে বলা যাবে? BLEU, Edit Distance-এর মতো text-similarity metric semantically equivalent কিন্তু আলাদা code-কে (যেমন `mov EDX, EAX` বনাম `push EAX; pop EDX`) ভুলভাবে নিচু score দেয়।
- সমাধান ACCA: (১) string compare, (২) assemble করে syntax check (Symbol-Not-Defined error সামলানো), (৩) angr দিয়ে reference ও prediction দুটোকে symbolic execution করে শেষ state (register, flag, stack, path constraint) মিলিয়ে দেখা।
- Dataset: extended Shellcode_IA32, মোট 5,900 NL-intent/assembly pair; test set 590 sample; 5টি generator (Seq2Seq, CodeBERT, CodeT5+, PLBart, ChatGPT) থেকে মোট 2,950 prediction।
- ফল: human evaluation-এর সাথে matching rate গড়ে 0.93 (min 0.90, max 0.95); Pearson ρ গড়ে 0.84 (সেরা baseline Edit Distance 0.69); গড় offset 0.06 (সেরা baseline Edit Distance 0.08)। ACCA correct-কে কম ধরে (65% বনাম human 71%) এবং 99% mismatch হলো "human correct, ACCA incorrect"।
- আমাদের জন্য মূল শিক্ষা: ACCA হলো high-precision, low-recall assurance tool (HITL judge-এর উল্টো error direction) এবং এর oracle হলো reference implementation, intent নয়। এটা Patch Validation ও RePaCA-র সাথে সরাসরি তুলনীয়।

**সহজ কথায়:** ACCA code-এর লেখা না দেখে চালিয়ে শেষ ফল মেলায়। তাই মানুষের সাথে প্রায় সবসময় একমত হয়। তবে সে একটু বেশি কড়া, কিছু ঠিক code-কেও ভুল বলে।

**Supervisor-কে ৩০ সেকেন্ডে:** "Sir, এই paper দেখায় যে code-এর correctness-কে text similarity দিয়ে না মেপে reference-এর সাথে execution-state equivalence দিয়ে মাপলে human judgement-এর সাথে correlation 0.56–0.69 থেকে 0.84-এ ওঠে। কিন্তু tool-টা reference-কে ground truth ধরে, human-কে ground truth ধরে validate করে, এবং শুধু একটি ছোট ধরনের (IA-32 shellcode) code-এ কাজ করে। আমাদের SPL3-এর জন্য এটা 'assurance tool নিজেই কতটা valid' (CG10, CG16, CG17)-এর একটি ভালো case study।"

## ২. Background (এই project-এর জন্য নতুন concept)

- **Shellcode:** vulnerable application-এ runtime-এ load করার মতো machine-code instruction-এর তালিকা; সাধারণত assembly লিখে assembler দিয়ে opcode বানানো হয়। লক্ষ্য: shell খোলা, process kill, fork bomb, secret leak ইত্যাদি।
- **IA-32 assembly:** 32-bit x86 instruction set। এই paper-এর সব উদাহরণ Linux + IA-32।
- **Offensive code generation:** NL description থেকে exploit-এর অংশ AI দিয়ে বানানো; proof-of-concept exploit দিয়ে vulnerability-র severity মাপতে ব্যবহার হয়।
- **NMT (Neural Machine Translation) code generator:** NL intent-কে target language-এ "translate" করা model (Seq2Seq, CodeBERT, CodeT5+, PLBart)।
- **Output similarity metrics:** generated code ও reference-এর text/token overlap মাপে: BLEU-4, SacreBLEU, Edit Distance, Exact Match। Semantic equivalence বোঝে না।
- **Semantic correctness বনাম syntactic correctness:** semantic correct হতে হলে syntax correctও হতে হয়; এই paper-এ human label 1/0।
- **Symbolic execution:** concrete input-এর বদলে symbolic value দিয়ে program চালিয়ে সব path ও তাদের output state বের করা। Path-গুলো constraint-এ রূপান্তরিত হয়ে SMT solver (z3) দিয়ে সমাধান হয়।
- **Basic block ও leaf node:** branch ছাড়া straight-line code; execution tree-র শেষ প্রান্তের state-কে leaf বলে। ACCA leaf-এর state set মেলায়।
- **Path explosion:** loop ও function call-এর কারণে path সংখ্যা exponentially বাড়ে; ACCA-তে max_steps = 100 দিয়ে সীমা।
- **Symbol-Not-Defined (SND) error:** snippet কোনো label/variable ব্যবহার করে যা snippet-এর বাইরে define করা। ACCA fictitious label বানিয়ে এটা সামলায়।
- **Oracle problem:** কোন output সঠিক তা নির্ধারণের কঠিনতা। এখানে reference snippet-ই oracle।
- **Matching rate ও offset:** ACCA/baseline-এর সাথে human-এর কত % sample-এ একই রায় (matching rate); অথবা মোট correctness-এর পার্থক্য (offset)।

**সহজ কথায়:** এই section-এর শব্দগুলো মনে রাখলেই পুরো paper বোঝা সহজ হবে: shellcode (ছোট exploit code), symbolic execution (সব সম্ভাব্য পথে "যেকোনো মান" ধরে চালানো), আর oracle (কোনটা সঠিক তা ঠিক করার মাপকাঠি)।

## ৩. Problem

- Human evaluation (manual code review) "gold standard" কিন্তু ধীর (গড়ে প্রায় 20 s/snippet), subjective, ক্লান্তিজনিত ভুলের সম্ভাবনা, এবং expert (assembly + cybersecurity) দরকার।
- Text-similarity metric দ্রুত ও reproducible, কিন্তু দুই ধরনের ভুল করে। (ক) equivalent কিন্তু আলাদা: `mov EDX, EAX` বনাম `push EAX; pop EDX`: BLEU-4 = 0.11, Edit Distance = 0.31। (খ) প্রায় একই কিন্তু ভুল: `mov DL, 5` বনাম `mov BL, 5`: Edit Distance = 0.96, BLEU-4 = 0.65, অথচ human একে incorrect বলবে।
- Static analyzer ও unit testing পুরো compilable program চায়; AI-generated snippet প্রায়ই অসম্পূর্ণ fragment।
- Code-oriented metric (CodeBLEU, RUBY) Java/C#-এর জন্য; assembly-র জন্য নেই এবং compilable code লাগে।
- Contrastive-learning embedding model-এ বড় compute ও training data লাগে, offensive code-এর corpus কম।
- সমস্যার সংক্ষিপ্ত রূপ: low-level security code-এর জন্য এমন automated oracle নেই যা human-এর মতো semantic correctness বলতে পারে।

**সহজ কথায়:** মানুষ ধীর, text-metric ভুল করে, আর বাকি পদ্ধতিগুলো অসম্পূর্ণ snippet-এ চলেই না। তাই এমন tool দরকার যা দ্রুত, আর মানুষের মতো বোঝে।

## ৪. Goal ও Research Question

- Goal: human effort ছাড়া AI-generated assembly (security context) code-এর syntactic (SYN) ও semantic (SEM) correctness automatically মাপা, human evaluation-এর কাছাকাছি।
- Paper আলাদা করে RQ1/RQ2 নম্বর দেয়নি; তিনটি প্রশ্ন Section 5-এর কাঠামো থেকে বোঝা যায় (আমার পুনর্গঠন)।
  1. ACCA-র সামগ্রিক correctness হিসাব human evaluation-এর কতটা কাছে ও baseline-এর চেয়ে ভালো কিনা (Section 5.1, offset ও matching rate)?
  2. Single-prediction level-এ human-এর সাথে correlation কেমন (Section 5.3, Pearson ρ)?
  3. Computational cost human-এর চেয়ে কম কিনা (Section 5.4)?
- আরেকটি qualitative প্রশ্ন: ACCA ও human কোথায় একমত নয় (Section 5.2, Table 5)।

**সহজ কথায়:** Paper তিনটি প্রশ্নের উত্তর খোঁজে: ACCA মানুষের কত কাছে? প্রতিটি আলাদা sample-এও কি মেলে? আর কত দ্রুত?

## ৫. Methodology (ধাপে ধাপে)

ACCA প্রতিটি prediction-এর জন্য জোড়া (SYN, SEM) ফেরত দেয়, 1 = verified, 0 = নয়।

1. **String comparison (Section 3.1):** prediction হুবহু reference-এর সমান হলে SYN = 1, SEM = 1 এবং শেষ। উদ্দেশ্য: symbolic execution এড়িয়ে গতি বাড়ানো।
2. **Assembling (Section 3.2):** snippet-কে সম্পূর্ণ program বানানো: `section .data` (exit address `db 0x56`), `section .text`, `global _start`, `_start:` এবং শেষে `jmp exit_addr`। NASM দিয়ে assemble।
   - No errors বা Warnings: SYN = 1 (warning গ্রহণযোগ্য, কারণ বেশিরভাগ warning ACCA-র নিজের যোগ করা লাইনের জন্য)।
   - Error: যদি SND হয়, assembler output থেকে missing symbol-এর নাম বের করে fictitious label (`loop: jmp myExitAddr`) যোগ করে আবার assemble। সফল হলে SYN = 1।
   - SND ছাড়া অন্য error (invalid opcode/operand combination, expression syntax error): SYN = 0, SEM = 0, শেষ।
3. **Linking:** assemble সফল হলে object file linker দিয়ে executable; reference ও prediction দুটির জন্যই আলাদা source file ও executable।
4. **Symbolic execution (Section 3.3):** angr (z3 backend) দিয়ে দুই executable চালানো। শুরুর register ও flag একই symbolic value; stack pointer ও memory blank। প্রতি ধাপে state ট্র্যাক; branch থেকে execution tree।
5. **State comparison:** প্রতিটি leaf-এর state: (ক) register, (খ) flag (carry, overflow, interrupt ইত্যাদি), (গ) stack value, (ঘ) path constraint। দুই program-এর leaf-সংখ্যা সমান হলে এক program-এর প্রতিটি leaf অন্যটির কোনো leaf-এর সাথে মিললে SEM = 1; না মিললে SEM = 0।
6. **Path explosion নিয়ন্ত্রণ:** max_steps = 100; এর বেশি চললে SEM = 0 (paper-এ 16/2,950 = 0.54% ক্ষেত্রে এমন হয়েছে)।
7. **Code generation (Section 4.1):**
   - Seq2Seq: bi-directional LSTM encoder, xnmt, Adam (β1 = 0.9, β2 = 0.999), learning rate 0.001, layer dimension 512, 1 layer, 200 epoch, beam size 5।
   - CodeBERT: encoder RoBERTa-style (12 layer, 12 head, hidden 768, position embedding 514), decoder 6 layer transformer; learning rate 0.00005, batch 32, beam 10।
   - CodeT5+ (220M variant): 12 decoder layer, 12 head, hidden 768, position embedding 512; learning rate 0.00005, batch 16, beam 10।
   - PLBart-large: 12 encoder + 12 decoder layer, 16 head; learning rate 0.00005, batch 16, beam 10।
   - ChatGPT-3.5 (free web interface, data up to April 2023): few-shot prompt (Fig. 3), temperature = default 1।
   - সব model validation set প্রতি 320 step-এ evaluate।
   - Pre-processing: stopword filtering, nltk tokenizer, spaCy named-entity tagger দিয়ে `var#` standardization; code-এর জন্য Python tokenize; post-processing-এ de-standardization।
8. **Dataset (Section 4.2):** 80/10/10 split: train 4,720, validation 590, test 590।
9. **Baseline assessors (Section 4.3):** Compilation Accuracy (NASM), BLEU-4 (NLTK), SacreBLEU, Exact Match, Edit Distance (pylcs), এবং ChatGPT-3.5 দুই ভাবে: ChatGPT-NL (NL intent-এর বিপরীতে 1/0) ও ChatGPT-GT (reference-এর বিপরীতে 1/0)। ChatGPT non-deterministic বলে তিনবার চালিয়ে 2-of-3 majority vote; 97% ক্ষেত্রে তিন রানে মতভেদ ছিল না।
10. **Human evaluation (Section 4.4):** 3 evaluator (2 PhD student with master's, 1 PhD researcher), প্রত্যেকে স্বাধীনভাবে প্রতি snippet দেখেছে; মতভেদ "human oversight" বলে সংশোধন করে 100% unanimous consensus। Inter-rater κ বা মতভেদের সংখ্যা paper-এ নেই।
11. **Hardware:** Debian, 8 vCPU, 16 GB RAM, একটি Nvidia T4 GPU। ACCA Linux ও Windows-এ চলে।

**সহজ কথায়:** ধাপগুলো একটা ছাঁকনির মতো। আগে সহজ পরীক্ষা (হুবহু মিল, syntax), তারপর ভারী পরীক্ষা (symbolic execution)। বেশিরভাগ ক্ষেত্রে ভারী কাজ লাগেই না, তাই tool দ্রুত।

## ৬. Math

**৬.১ ACCA-র সিদ্ধান্ত নিয়ম (paper-এর বর্ণনা থেকে আমার formal রূপ)**

$$
\text{SEM}(p, r) = \begin{cases} 1 & \text{if } p = r \\ 0 & \text{if } \text{SYN}(p) = 0 \\ 1 & \text{if } \mathcal{S}(p) = \mathcal{S}(r) \\ 0 & \text{otherwise} \end{cases}
$$

**কী হিসাব করে:** প্রথমে দেখে prediction আর reference হুবহু এক কিনা, এক হলে 1। না হলে syntax ভুল থাকলে 0। তারপর দুই program-এর শেষ অবস্থার set মিললে 1, নইলে 0।

- $p$ = model-এর prediction, $r$ = reference (ground truth) snippet।
- $\mathcal{S}(x)$ = $x$-এর symbolic execution-এর সব leaf state-এর set; প্রতিটি leaf state = (register, flag, stack, path constraint)।
- $\text{SYN}(p) = 1$ যদি assemble সফল হয় (warning সহ)।
- Max step 100 পেরোলে $\text{SEM} = 0$।
- দ্রষ্টব্য: $\mathcal{S}(p) = \mathcal{S}(r)$ মানে leaf-এর পারস্পরিক মিল; paper "constraint সহ state তুলনা" বলে, ঠিক কোন equivalence check (syntactic না SMT-based) তা বিস্তারিত দেয়নি।

**৬.২ Matching rate (Table 3)**

$$
\text{MR} = \frac{1}{N} \sum_{i=1}^{N} \mathbb{1}\left[ \text{ACCA}_i = \text{Human}_i \right]
$$

**কী হিসাব করে:** ACCA আর মানুষ কতগুলো sample-এ একই রায় দিয়েছে, সেটা মোট sample দিয়ে ভাগ করে।

- $N$ = test prediction সংখ্যা (প্রতি model 590); $\mathbb{1}[\cdot]$ = শর্ত সত্য হলে 1।
- Paper-এর যুক্তি: দুই পদ্ধতি 50% করে correct বললেও মতভেদ 100% হতে পারে, তাই MR দরকার।

**৬.৩ Offset (Table 4)**

$$
\text{Offset} = \left| \bar{c}_{\text{Human}} - \bar{c}_{\text{method}} \right|
$$

**কী হিসাব করে:** মানুষের মতে গড়ে কত শতাংশ code ঠিক আর tool-এর মতে কত শতাংশ, এই দুই সংখ্যার ফারাক।

- $\bar{c}$ = test set-এর গড় correctness (0 থেকে 1)। Paper "difference" বলেছে; absolute মান ধরা হয়েছে (আমার পাঠ), কারণ সব মান ধনাত্মক।
- সীমাবদ্ধতা: offset শুধু aggregate মাপে; দুই উল্টো ধরনের ভুল একে অপরকে বাতিল করে দিতে পারে।

**৬.৪ Pearson correlation (Table 6)**

$$
\rho = \frac{\text{cov}(X, Y)}{\sigma_X \, \sigma_Y}
$$

**কী হিসাব করে:** মানুষের রায় আর tool-এর মান একসাথে ওঠানামা করে কিনা। 1-এর কাছে মানে খুব মিল, 0 মানে কোনো সম্পর্ক নেই।

- $X$ = human label (0/1), $Y$ = ACCA বা baseline-এর মান। Binary দুই চলকে এটি phi coefficient-এর সমান। Continuous baseline (BLEU, ED)-এর সাথে এটি point-biserial। Paper কোনো threshold বা binarization উল্লেখ করেনি।

**৬.৫ Worked example (আমার হিসাব): Seq2Seq, Table 3 ও Table 6 থেকে**

- Table 3 (Seq2Seq): Matching 0.94, ACCA 0.60, Human 0.66। মতভেদ = 1 − 0.94 = 0.06 = Human − ACCA, অর্থাৎ সব মতভেদই "human 1, ACCA 0"।
- Confusion proportion: $p_{11} = 0.60$, $p_{10} = 0.06$ (human 1, ACCA 0), $p_{01} = 0$, $p_{00} = 0.34$।
- Phi:

$$
\phi = \frac{p_{11} p_{00} - p_{10} p_{01}}{\sqrt{0.66 \cdot 0.34 \cdot 0.60 \cdot 0.40}} = \frac{0.60 \cdot 0.34}{\sqrt{0.053856}} = \frac{0.204}{0.2321} \approx 0.88
$$

- Paper-এ 0.87; পার্থক্য rounding-এর (আমার হিসাব)। এটি দেখায় Table 3, 4, 6 internally সঙ্গত।

**সহজ কথায়:** Paper-এর দেওয়া তিনটি table থেকে আমরা নিজে হিসাব করে প্রায় একই ফল (0.88 বনাম 0.87) পেয়েছি। মানে সংখ্যাগুলো পরস্পরের সাথে মেলে।
- Recall (ACCA, human-কে ground truth ধরে) = 0.60 / 0.66 ≈ 0.91; precision = 1.00; specificity = 1.00 (আমার হিসাব, সব মতভেদ FN ধরে)।
- ChatGPT column: Matching 0.95, ACCA 0.71, Human 0.73; FN − FP = 0.02, FN + FP = 0.05 ⇒ FN = 0.035, FP = 0.015 ⇒ phi ≈ 0.88 (paper 0.87) (আমার হিসাব)।

**৬.৬ Time saving (আমার হিসাব)**

- ACCA: 2,950 × 0.20 s ≈ 590 s ≈ 9.8 মিনিট (Table 7 all-model average)।
- Human: 2,950 × 20 s = 59,000 s ≈ 16.4 ঘণ্টা (paper-এর "≈ 20 s" অভিজ্ঞতা-ভিত্তিক অনুমান)।
- অনুপাত প্রায় 100 গুণ। কিন্তু Table 7 অনুযায়ী Symbolic execution-এ যেসব prediction যায় (PR ≠ GT & SYN = 1) সেগুলোর গড় 0.43 s।

**সহজ কথায়:** ACCA সব মতভেদ সামলে human-এর 91% ঠিক code ধরে এবং যা ঠিক বলে তার সবই ঠিক। আর সময়ে মানুষের চেয়ে প্রায় ১০০ গুণ দ্রুত।

## ৭. Setup (table)

| Item | মান |
|---|---|
| Dataset | Extended Shellcode_IA32; 5,900 unique NL/assembly pair (প্রাথমিক 3,200 + enrichment) |
| Multi-line snippet | 1,374 intent (23%); 2 থেকে 18 instruction |
| Unique lines / tokens (Table 1) | NL: 5,740 lines, 2,855 tokens, গড় 9.18 token/line; Code: 3,316 lines, 1,770 tokens, গড় 5.83 |
| Split | train 4,720 / validation 590 / test 590 |
| Generators | Seq2Seq, CodeBERT, CodeT5+ (220M), PLBart-large, ChatGPT-3.5 |
| মোট prediction | 590 × 5 = 2,950; unique reference-prediction pair 1,369 |
| Assembler / SE engine | NASM; angr (z3 backend); max_steps = 100 |
| Human evaluators | 3 জন (2 PhD student, 1 PhD researcher); মতভেদ সংশোধিত, 100% consensus |
| Baselines | CA, BLEU-4, SacreBLEU, Edit Distance, Exact Match, ChatGPT-NL, ChatGPT-GT |
| ChatGPT repetition | 3 run, 2-of-3 majority; 97% ক্ষেত্রে মতভেদ নেই |
| Hardware | 8 vCPU, 16 GB RAM, 1× Nvidia T4 |
| Training seeds | একবারই training; একাধিক training run করা হয়নি (Section 6-এ যুক্তি) |

**সহজ কথায়:** মোট ৫,৯০০ জোড়া data, তার ৫৯০টি test। পাঁচটি AI প্রত্যেকে ৫৯০টি করে code লিখেছে, তাই মোট ২,৯৫০টি code যাচাই হয়েছে।

## ৮. Results

**৮.১ Table 3: ACCA বনাম human evaluation (average correctness ও matching)**

| Metric | Seq2Seq | CodeBERT | CodeT5+ | PLBart | ChatGPT | Average |
|---|---|---|---|---|---|---|
| Matching Rate | 0.94 | 0.90 | 0.93 | 0.92 | 0.95 | 0.93 |
| ACCA | 0.60 | 0.68 | 0.69 | 0.57 | 0.71 | 0.65 |
| Human Eval. | 0.66 | 0.78 | 0.76 | 0.64 | 0.73 | 0.71 |

(PDF text-layer-এ Table 3 এলোমেলো ছিল; `pdftotext -raw` দিয়ে page 9 পুনরায় নিয়ে সারি ঠিক করা হয়েছে।)

- ACCA সব model-এ human-এর চেয়ে কম বা প্রায় সমান: underestimation; 99% মতভেদ "human = 1, ACCA = 0"।

**সহজ কথায়:** ACCA আর মানুষ প্রতি ১০০টিতে ৯০ থেকে ৯৫টিতে একমত। যেখানে মতভেদ, প্রায় সবখানেই মানুষ বলেছে ঠিক আর ACCA বলেছে ভুল।

**৮.২ Table 4: Human-এর সাপেক্ষে offset (কম = ভালো)**

| Evaluation | Seq2Seq | CodeBERT | CodeT5+ | PLBart | ChatGPT | Average |
|---|---|---|---|---|---|---|
| Compilat. Acc. | 0.28 | 0.15 | 0.14 | 0.21 | 0.24 | 0.20 |
| BLEU-4 | 0.22 | 0.20 | 0.29 | 0.24 | 0.29 | 0.25 |
| SacreBLEU | 0.15 | 0.05 | 0.07 | 0.09 | 0.09 | 0.09 |
| Edit Distance | 0.15 | 0.07 | 0.07 | 0.09 | 0.05 | 0.08 |
| Exact Match | 0.25 | 0.17 | 0.27 | 0.24 | 0.28 | 0.24 |
| ChatGPT-NL | 0.08 | 0.02 | 0.07 | 0.17 | 0.24 | 0.12 |
| ChatGPT-GT | 0.06 | 0.13 | 0.10 | 0.10 | 0.05 | 0.09 |
| ACCA | 0.06 | 0.10 | 0.07 | 0.07 | 0.02 | 0.06 |

**সহজ কথায়:** Offset যত কম, তত ভালো। ACCA-র গড় 0.06, মানে মানুষের সাথে গড়ে মাত্র ৬ শতাংশ-পয়েন্ট ফারাক। কিন্তু প্রতি model-এ সে সবসময় একা সেরা নয়, নিচে §১২-এ দেখো।

**৮.৩ Table 6: Human-এর সাথে Pearson ρ (বেশি = ভালো)**

| Evaluation | Seq2Seq | CodeBERT | CodeT5+ | PLBart | ChatGPT | Average |
|---|---|---|---|---|---|---|
| Compilat. Acc. | 0.36 | 0.44 | 0.59 | 0.52 | 0.22 | 0.43 |
| BLEU-4 | 0.56 | 0.55 | 0.56 | 0.64 | 0.50 | 0.56 |
| SacreBLEU | 0.53 | 0.52 | 0.60 | 0.66 | 0.51 | 0.57 |
| Edit Distance | 0.67 | 0.61 | 0.75 | 0.76 | 0.64 | 0.69 |
| Exact Match | 0.60 | 0.67 | 0.55 | 0.61 | 0.55 | 0.59 |
| ChatGPT-NL | 0.42 | 0.42 | 0.37 | 0.44 | 0.07 | 0.34 |
| ChatGPT-GT | 0.67 | 0.61 | 0.70 | 0.68 | 0.56 | 0.64 |
| ACCA | 0.87 | 0.78 | 0.85 | 0.85 | 0.87 | 0.84 |

**সহজ কথায়:** এখানে বেশি মানে ভালো। ACCA-র 0.84 সব পদ্ধতির চেয়ে উপরে। Compilation পাস করা মানেই ঠিক নয়, তাই তার মান সবচেয়ে কম (0.43)।

**৮.৪ Table 7: ACCA-র সময় (সেকেন্ড/snippet; গড় ± SD, median)**

| Model | All predictions | PR ≠ GT | PR ≠ GT এবং SYN = 1 |
|---|---|---|---|
| Seq2Seq | 0.20 ± 1.22, 0.00 | 0.33 ± 1.58, 0.22 | 0.37 ± 1.67, 0.22 |
| CodeBERT | 0.14 ± 1.12, 0.00 | 0.29 ± 1.57, 0.20 | 0.33 ± 1.68, 0.21 |
| CodeT5+ | 0.11 ± 0.97, 0.00 | 0.22 ± 1.36, 0.08 | 0.27 ± 1.51, 0.20 |
| PLBart | 0.21 ± 1.56, 0.00 | 0.35 ± 1.99, 0.19 | 0.46 ± 2.30, 0.21 |
| ChatGPT | 0.32 ± 1.51, 0.00 | 0.67 ± 2.13, 0.28 | 0.70 ± 2.17, 0.29 |
| All Models | 0.20 ± 1.28, 0.00 | 0.37 ± 1.73, 0.21 | 0.43 ± 1.87, 0.22 |

(Table 7-ও PDF text-layer-এ এলোমেলো ছিল; raw extraction থেকে মেলানো।)

**সহজ কথায়:** গড়ে একটা snippet যাচাই করতে এক সেকেন্ডের পাঁচ ভাগের এক ভাগ লাগে। বেশিরভাগ হুবহু মিলে যায় বলে median 0.00 s। শুধু ভারী ক্ষেত্রে সময় বেশি।

**৮.৫ অন্যান্য সংখ্যা**

- Syntactically correct prediction (Section 5.4): Seq2Seq 553, CodeBERT 550, CodeT5+ 531, PLBart 499, ChatGPT 577 (প্রতিটি 590-এর মধ্যে)। শতাংশ (আমার হিসাব): 93.7%, 93.2%, 90.0%, 84.6%, 97.8%।
- max_step ছাড়িয়ে 0 score: 16/2,950 = 0.54%।
- সময়ের outlier: 17/2,950 = 0.58% (Seq2Seq 3, CodeBERT 2, CodeT5+ 1, PLBart 4, ChatGPT 7); Table 8-এর দুই উদাহরণ 23.92 s ও 11.98 s। কারণ: cmp, loop, jns জাতীয় conditional jump/compare-যুক্ত snippet ধীর; logic ও register op (and, xor, inc, mov) প্রায় ≤ 0.25 s।
- Baseline সময়: output similarity metric গড়ে ≈ 0.004 s (Exact Match 0.001 s থেকে SacreBLEU 0.01 s); ChatGPT-NL 0.003 s, ChatGPT-GT 0.001 s। তবে ChatGPT-এর জন্য prompt design ও মানুষের iteration লাগে, তাই paper একে "fully automated" মানে না।
- Human: ≈ 20 s/snippet (paper-এর অভিজ্ঞতা)। Abstract-এ ACCA = 0.17 s; Table 7-এ 0.20 s (§১২-এ inconsistency)।

**৮.৬ Table 5: মতভেদের উদাহরণ**

| NL intent | Ground truth | Prediction | Human | ACCA |
|---|---|---|---|---|
| Push zero into the stack | xor edx, edx; push edx | xor eax, eax; push eax | 1 | 0 |
| Save eax contents in esi contents | mov esi, eax | xchg esi, eax | 1 | 0 |
| In L1 jump short to esp | L1: jmp short esp | jmp short esp | 0 | 1 |
| Restore stack top into ecx, decrement ecx, jump to l1 if ecx not zero | pop ecx; loop l1 | pop ecx; dec ecx; jmp l1 | 0 | 1 |

- সারি ১-২ (false negative): অন্য register ব্যবহার করলে শেষ register state আলাদা, যদিও intent পূরণ হয়।
- সারি ৩ (false positive): label L1 register state বদলায় না, কিন্তু পুরো program-এর behaviour বদলায়।
- সারি ৪ (false positive): `loop` শর্তযুক্ত jump; prediction-এর `dec ecx; jmp` শর্তহীন; এই run-এ ecx শূন্য ছিল না বলে একই state, কিন্তু intent ভুল।

**সহজ কথায়:** ACCA-র ভুল দুই রকম। প্রথম দুই সারি: ঠিক code-কে ভুল বলেছে, কারণ আলাদা register ব্যবহার হয়েছে। শেষ দুই সারি: ভুল code-কে ঠিক বলেছে, কারণ শেষ অবস্থা দৈবাৎ মিলে গেছে।

## ৯. Key findings

1. Text-similarity metric-এর মধ্যে সেরা Edit Distance (ρ = 0.69, offset 0.08); সবচেয়ে দুর্বল Compilation Accuracy (ρ = 0.43): syntax-সঠিক হলেই semantic-সঠিক নয়।
2. ACCA human-এর সাথে 93% sample-এ একমত (min 0.90 CodeBERT, max 0.95 ChatGPT) এবং ρ = 0.84 গড়ে, সব model-এ সবচেয়ে বেশি (0.78 থেকে 0.87)।
3. ACCA correctness কম ধরে: গড় 0.65 বনাম 0.71; 99% মতভেদ false negative। কারণ: reference-এর ভিন্ন register/flag ব্যবহার করলে state মেলে না (`ADD EAX, 1` বনাম `INC EAX`: Carry flag আলাদা)।
4. ChatGPT-3.5 (aggregate-এ কাছাকাছি, offset 0.09 বা 0.12) per-sample correlation-এ দুর্বল: ChatGPT-GT 0.64, ChatGPT-NL 0.34; অর্থাৎ aggregate সংখ্যা কাছাকাছি হলেও কোন sample ঠিক তা ধরতে পারে না।
5. Offset ও correlation আলাদা তথ্য দেয়: ChatGPT-NL Seq2Seq-এ offset 0.08 কিন্তু ρ = 0.42; তাই paper-এর দুটি দিকই দেখার সিদ্ধান্ত যথার্থ।
6. খরচ: গড় 0.20 s (সব prediction), 0.43 s (পূর্ণ symbolic execution-এ যাওয়া ক্ষেত্র), outlier মাত্র 0.58%।
7. ACCA security বিশ্লেষণ নয়: এটি vulnerability খোঁজে না, শুধু reference-এর সাথে semantic equivalence মাপে (Section 6 "Relevance to Security")।
8. ChatGPT-3.5 নিজেও generator: ACCA ও human একই হারের কাছাকাছি (0.71 বনাম 0.73) এবং ChatGPT-এর output সবচেয়ে বেশি syntactically correct (577/590)।

**সহজ কথায়:** ACCA সবচেয়ে ভালো মেলে, দ্রুত চলে, কিন্তু কড়া। আর সে শুধু "ঠিক কাজ করে কিনা" দেখে, "নিরাপদ কিনা" দেখে না।

## ১০. কেন বিকল্পের চেয়ে ভালো

- **বনাম similarity metric:** token নয়, execution state মেলায়; তাই equivalent-কিন্তু-ভিন্ন (`jz` বনাম `je`, `mov` বনাম `push/pop`) গ্রহণ করে এবং এক character ভিন্ন কিন্তু ভুল (`DL` বনাম `BL`) প্রত্যাখ্যান করে।
- **বনাম unit test/pass@k:** snippet-এর জন্য test লিখতে হয় না; অসম্পূর্ণ snippet-ও চলে (fictitious label)। Pass@k লাগে test suite, যা বড় manual effort।
- **বনাম static analyzer / compiler-validation SE:** ওগুলো সম্পূর্ণ program চায়; ACCA fragment সামলায়।
- **বনাম code embedding (contrastive learning):** training data ও compute লাগে না; offensive assembly corpus কম, তাই embedding অপ্রয়োগযোগ্য।
- **বনাম ChatGPT judge:** deterministic (একই input একই output), repetition দরকার নেই, prompt engineering ও মানুষের iteration নেই, এবং correlation অনেক বেশি (0.84 বনাম 0.64 / 0.34)।
- **বনাম human:** প্রায় 100 গুণ দ্রুত (আমার হিসাব, §৬.৬), ক্লান্তি/subjectivity মুক্ত।

**সহজ কথায়:** বাকি পদ্ধতিগুলো হয় লেখা মেলায়, নয় পুরো program চায়, নয় ভারী training চায়। ACCA এই তিনটি ঝামেলাই এড়ায়।

## ১১. কখন কাজ করে / কখন ব্যর্থ হয়

**কাজ করে:**
- ছোট (কয়েক instruction), loop-হীন বা কম-branch snippet, যেখানে reference আছে এবং শেষ register/flag/stack state-ই behaviour-এর সংজ্ঞা।
- Syntax-ভুল দ্রুত ধরা (SYN = 0 হলে symbolic execution ছাড়াই শেষ)।
- Reference-এর সাথে হুবহু মিল থাকলে symbolic execution এড়ানো (median সময় 0.00 s)।

**ব্যর্থ হয়:**
- ভিন্ন কিন্তু বৈধ implementation (অন্য register ব্যবহার, ভিন্ন flag effect): false negative (Table 5 সারি ১-২)।
- যে ভুল শেষ state-এ দেখা যায় না (অব্যবহৃত label, শর্তযুক্ত বনাম শর্তহীন jump যখন শর্ত মিলে যায়): false positive (সারি ৩-৪)।
- Loop-সমৃদ্ধ বা দীর্ঘ snippet: max_steps = 100 পেরোলে স্বয়ংক্রিয়ভাবে 0; 16/2,950 ক্ষেত্রে।
- Compare/loop/conditional jump-এ ধীর (23.92 s ও 11.98 s উদাহরণ)।
- Reference না থাকলে ব্যবহার অসম্ভব; reference ভুল হলে ACCA-ও ভুল।

**সহজ কথায়:** ছোট, সরল, reference-ওয়ালা code-এ ACCA ভালো। লম্বা loop-ওয়ালা code, ভিন্ন কিন্তু বৈধ লেখা, আর reference না থাকা, এই তিন ক্ষেত্রে সে সমস্যায় পড়ে।

## ১২. Limitations

**Authors-এর স্বীকৃত:**
- ACCA শুধু semantic correctness মাপে, security বা vulnerability নয়।
- Oracle problem সমাধান করে না; reference implementation-কে নির্ভরযোগ্য ধরে নেয়।
- Reference-ভিত্তিক automation: reference লাগে (dataset থাকলেই test split থেকে পাওয়া যায়)।
- Model training একবার; একাধিক run করা হয়নি (ACCA deterministic, তাই generator-এর variance তাদের মূল বিষয় নয় বলে যুক্তি)।
- Dataset: শুধু offensive IA-32 assembly; Python ইত্যাদি high-level ভাষা ভবিষ্যৎ কাজ। Static analysis ও binary matching-এর সাথে সংযুক্তি ভবিষ্যৎ।
- Timing outlier কিছু আছে (0.58%)।

**আমার পর্যবেক্ষণ:**
- **Validation এক ধরনের "ground truth"-এর বিপরীতে:** human evaluation-কে ground truth ধরা হয়েছে; কিন্তু মতভেদ "human oversight" বলে সংশোধিত, কোনো κ বা মতভেদ-সংখ্যা নেই। আর human NL intent দেখে, ACCA reference দেখে: দুটি আলাদা oracle। এটি CG16 (label validity, rater circularity)-এর ক্ষেত্র।
- **Paper-internal inconsistency ১:** Abstract ও Conclusion-এ "0.17 s average"; Table 7-এ All Models গড় 0.20 s এবং text-ও "≈ 0.20 s"। 0.17 কোথা থেকে, paper-এ নেই।
- **Paper-internal inconsistency ২:** Section 5.1 text বলে ChatGPT-NL offset 0.09 এবং ChatGPT-GT 0.12; Table 4-এ ChatGPT-NL 0.12 ও ChatGPT-GT 0.09 (সারি গড় যাচাই: NL = 0.58/5 ≈ 0.12; GT = 0.44/5 ≈ 0.09, আমার হিসাব)। Text-এ দুটি উল্টে গেছে।
- **"4 out of 5 model-এ সর্বনিম্ন offset":** Table 4-এ CodeBERT-এ ACCA 0.10, অথচ ChatGPT-NL 0.02, SacreBLEU 0.05, Edit Distance 0.07; Seq2Seq-এ ChatGPT-GT-এর সাথে tie (0.06); CodeT5+-এ SacreBLEU, ED, ChatGPT-NL-এর সাথে tie (0.07)। কঠোরভাবে ACCA একা সর্বনিম্ন মাত্র PLBart ও ChatGPT-তে। তবে গড় 0.06 সত্যি সর্বনিম্ন।
- **"চারটি model" বনাম পাঁচটি:** Abstract "four state-of-the-art models"; পরীক্ষায় ChatGPT পঞ্চম generator হিসেবে গণ্য (Table 3-এ আলাদা কলাম)।
- **Offset-এর ছাপ:** ACCA-র offset (0.06) আসলে প্রায় পুরোটাই false-negative rate; ACCA-র recall প্রায় 0.91 (আমার হিসাব) কিন্তু paper recall/precision/specificity/κ/confusion matrix কখনো দেখায়নি। "Almost perfect assessment" দাবির জন্য precision (≈ 1.0) ভালো, কিন্তু 9% correct code অগ্রাহ্য হয়।
- **Pearson ও binary label:** ρ জেনেও binary-binary সম্পর্কে phi-এর সমান; prevalence (≈ 0.71 correct) ও baseline-এর threshold নিয়ে কিছু বলা নেই, কাজেই baseline-এর সাথে ρ-তুলনা threshold-নির্ভর হতে পারে।
- **Test set-এর দ্বৈততা:** 2,950 prediction-এর মধ্যে unique reference-prediction pair মাত্র 1,369 (46.4%, আমার হিসাব); অনেক model একই output দেয় বলে সংখ্যাটা কাছাকাছি, ফলে ACCA-র সংখ্যাগত confidence interval স্বাধীন 2,950 নমুনার মতো নয়। কোনো confidence interval বা significance test (যেমন McNemar) নেই।
- **Random split ও দ্বৈততা:** dataset-এ intent/code পুনরাবৃত্তি থাকলে random 80/10/10 split-এ test reference train-এ থাকতে পারে; এতে generator-এর কাছে Exact Match অনেক সহজ, ফলে baseline-এর তুলনা (Exact Match offset 0.24) প্রভাবিত হতে পারে। CG6/CG10 সংযোগ।
- **ChatGPT baseline দুর্বল সেট-আপ:** ChatGPT-3.5 web interface, কোনো chain-of-thought বা rubric নয়, temperature 1; আধুনিক reasoning model দিয়ে judge এর অবস্থা পাল্টাতে পারে (§২১)।
- **একক dataset ও একক architecture:** IA-32 Linux shellcode; 100-step cap-এর বৈধতা অন্য ধরনের code-এ অজানা।
- **Reference ও ground truth-এর পরিমাণগত অসম্পূর্ণতা:** reference-এর ভুল (dataset noise) গণনা হয়নি; paper স্পষ্টভাবে এই ধারণা "out of scope" বলেছে।

**সহজ কথায়:** Authors নিজেই স্বীকার করেছেন tool security মাপে না আর reference-কে সত্য ধরে। আমরা আরও দেখেছি: human label-এর বৈধতা অস্পষ্ট, কিছু সংখ্যায় অসঙ্গতি আছে, আর confidence interval নেই।

## ১৩. Research gaps

| G-id | Gap | Evidence (paper-এ) | Related CG / sub-domain folder |
|---|---|---|---|
| G1 | Reference-equivalence oracle বৈধ বিকল্প implementation-কে ভুল ঠেকায় (false negative ≈ সব মতভেদের 99%) | Table 3, §5.2, Table 5 সারি ১-২ | CG1, CG20 (নতুন); 02_APR, 05_Patch_Validation |
| G2 | Same-final-state ভুল আচরণ ঢাকে (false positive): label, শর্তযুক্ত jump | Table 5 সারি ৩-৪ | CG1, CG3 |
| G3 | Validity report অসম্পূর্ণ: κ, confusion matrix, precision/recall/specificity, CI, significance test নেই | §5.1, §5.3 | CG10, CG17 |
| G4 | Human ground truth-এর বৈধতা: মতভেদ "oversight" বলে সংশোধন, κ নেই, human intent দেখে কিন্তু ACCA reference দেখে | §4.4 | CG16 |
| G5 | Prevalence ও error direction: ACCA হলো high-precision low-recall; HITL judge উল্টো। মিলিয়ে ব্যবহারের নকশা নেই | Table 3 বনাম Sub-domain 5 | CG17 |
| G6 | মাত্র IA-32 shellcode; high-level language ও repository-level patch-এ প্রয়োগ অজানা | §6, Conclusion | CG9; 06_Security_of_AI_Code |
| G7 | Security assessment নেই: correctness ≠ safety; exploit code বা patch-এর vulnerability-closure যাচাই নেই | §6 "Relevance to Security" | CG5 |
| G8 | Gaming/robustness: model যদি ACCA-র state-equivalence-কে লক্ষ্য করে (যেমন extra dummy instruction, jump-to-exit) | কোনো adversarial test নেই | CG12, CG18 |
| G9 | Test split ও train data-র duplicate/leakage ও dataset reference noise-এর প্রভাব মাপা হয়নি | Table 1 বনাম 1,369 unique pair | CG6, CG16 |
| G10 | Path explosion সীমা (100 step) ও timeout কে "incorrect" গণনা করা: "could not verify" নামে আলাদা ফল নেই | §3.3, 16/2,950 | CG7, CG11 |

**সহজ কথায়:** Gap-গুলো মূলত তিন ভাগে পড়ে: tool-এর ভুল (G1, G2, G10), মাপার পদ্ধতির দুর্বলতা (G3, G4, G9), আর ব্যবহারের সীমা (G5 থেকে G8)।

## ১৪. Improvement ideas

1. **Intent-aware tri-state output:** SEM ∈ {equivalent, not equivalent, could not verify} (step-cap ও unsupported-instruction ক্ষেত্রে)। Context.md-র "could not verify" ধারণার সাথে সংযুক্ত।
2. **Observable-state projection:** শুধু আউটপুটে/ইন্টেন্টে প্রাসঙ্গিক register ও flag তুলনা (যেমন "zero EDX" এ EDX ও flag-এর কিছু অংশ), এবং "dead" register বা অব্যবহৃত flag উপেক্ষা; false negative কমাবে। তবে false positive বাড়ার ঝুঁকি; তাই intent থেকে projection বের করতে হবে।
3. **Hybrid pipeline:** ACCA (high precision) দিয়ে নিশ্চিত correct আলাদা করা; বাকি অনিশ্চিত অংশে rubric-driven LLM judge বা human। Error direction পরিপূরক (ACCA-র recall ≈ 0.91, precision ≈ 1.0 বনাম HITL judge-এর recall 0.93, precision 0.65, Sub-domain 5)।
4. **Statistical rigor:** bootstrap CI, McNemar, Cohen/Fleiss κ, prevalence-adjusted precision (CG17)।
5. **Differential/behavioural equivalence for Python/C patches:** ACCA-র ধারণা (reference-এর সাথে state equivalence) কে angr-এর বদলে KLEE/CrossHair বা differential test দিয়ে repository patch-এ আনা (PatchDiff-এর মতো, §২১)।
6. **Adversarial test:** ACCA-র বিরুদ্ধে gaming (CG12): generator-কে ACCA score-এ fine-tune করলে কী ঘটে।
7. **Security-aware layer:** correctness-এর পর sanitizer/CodeQL ধরনের check আলাদা signal হিসেবে (CG5); ACCA-র সাথে মিশিয়ে একক score নয়।
8. **Reference noise audit:** reference-ও ACCA-তে এক সংখ্যক sample-এ cross-check করে dataset label noise মাপা।

**সহজ কথায়:** সবচেয়ে কাজের ধারণা: ACCA-কে LLM judge-এর সাথে জোড়া লাগানো, কারণ দুজনের ভুল উল্টো দিকে। আর "যাচাই করা গেল না" নামে তৃতীয় ফলাফল রাখা।

## ১৫. Publication potential (SPL3-feasible)

- সম্ভাব্য contribution: "Reference-based equivalence judge বনাম rubric-based LLM judge: error-direction ও specificity-র তুলনামূলক বিশ্লেষণ" (workshop/short paper স্তর)।
- নতুনত্ব: ACCA-র assembly থেকে Python patch-এ রূপান্তর নয়; বরং **তিনটি assurance signal-এর (execution-equivalence, LLM judge, learned classifier) আলাদা error profile** একই labelled সেটে মাপা, CI ও κ সহ। Context.md-র CG10/CG17 ধারার বাস্তব প্রয়োগ।
- Feasibility: SPL3 ঘণ্টা ও compute সীমার মধ্যে 300–600 patch-এ labelled সেট ও কয়েকটি judge চালানো সম্ভব; ACCA নিজে খোলা কোড (github), Shellcode_IA32 খোলা ডেটা: Replication সহজ।
- ঝুঁকি: human label বানানো সবচেয়ে ব্যয়বহুল; সেজন্য প্রথম ধাপে paper-এর নিজস্ব ডেটার reproduction ও confusion matrix পুনর্গণনা (যেটা paper দেয়নি)।
- বাস্তব প্রকাশযোগ্য ছোট ফল: "ACCA-র reported 0.93 matching rate আসলে 0.91 recall ও ≈ 1.0 precision; error direction স্পষ্ট" ধরনের reproducibility note (আমার হিসাব, replication দিয়ে যাচাই সাপেক্ষ)।

**সহজ কথায়:** ছোট একটা paper-এর জন্য যথেষ্ট: ACCA-র confusion matrix আর error direction নতুন করে হিসাব করে দেখানো, যেটা original paper দেয়নি।

## ১৬. SPL3 implementation

1. **Reproduction (সপ্তাহ ১-২):** ACCA ও Shellcode_IA32 ক্লোন; NASM + angr (z3) ইনস্টল; test split-এর 590 sample ও কমপক্ষে দুটি model-এর (যেমন CodeT5+ ও একটি আধুনিক LLM) prediction তৈরি; ACCA চালানো; Table 3 ও 6 পুনরুৎপাদনের চেষ্টা।
2. **Confusion matrix ও কাঁচা label:** paper যা দেয়নি: human label-সহ TP/FP/FN/TN, recall, precision, specificity, κ, bootstrap CI।
3. **Judge তুলনা:** একই sample-এ (ক) ACCA, (খ) rubric-driven LLM judge (NL intent ও reference সহ ও ছাড়া), (গ) Edit Distance baseline; metric: R@P = 0.8 ও specificity (Sub-domain 5-এর অনুসরণ)।
4. **Gaming ও robustness test:** ACCA-র জন্য dummy-instruction/redundant-jump ধরনের adversarial prediction (CG12); judge-এর জন্য prompt-injection comment (CG18)।
5. **Patch-এর দিকে সেতু:** Python/C ছোট patch-এ একই ধারণা: reference patch ও agent patch-কে একই test input-এ চালিয়ে observable output তুলনা (differential execution)। ACCA-র state-set equivalence-এর সরল সংস্করণ।
6. **Output:** assurance report-এর একটি আলাদা signal: "behavioural equivalence to reference: equivalent / different / could not verify" + tool version + step cap।
7. **খরচ:** ACCA CPU-ভিত্তিক, ≈ 0.2 s/snippet; LLM judge-এর API খরচ আলাদা গণনা (USD)।

**সহজ কথায়:** পরিকল্পনা: আগে paper-এর ফল নিজে পুনরায় বের করো, তারপর judge তুলনা, তারপর gaming test, সবশেষে patch-এর দিকে ধারণাটা নিয়ে যাও।

## ১৭. Influence / link to earlier sub-domains

- **Sub-domain 1 (AutoCodeRover 51/78 = 65.4% প্রকৃত correct):** plausible ≠ correct সমস্যার "automated oracle" দিক; ACCA একটি reference-ভিত্তিক বিকল্প।
- **Sub-domain 2 (APR, RePaCA, VRpilot):** RePaCA low specificity (16/30 correct গ্রহণ) বনাম ACCA high precision low recall: উল্টো error profile; VRpilot-এর "sanitizer pass ≠ secure" এখানে "syntax/state pass ≠ intent-correct"-এর সাথে মেলে।
- **Sub-domain 3 (Evaluation):** SWE-rebench-এ কত run ও CI লাগে (CG8) তার বিপরীতে এই paper-এ CI ও significance test নেই।
- **Sub-domain 4 (Test generation):** Oracle strength (CG13); ACCA "reference state" কেই oracle ধরে, কিন্তু coverage-style নয়।
- **Sub-domain 5 (Patch Validation):** HITL judge (Fleiss κ 0.31 → 0.66; judge recall 0.93, precision 0.65, specificity ≈ 0.69) বনাম ACCA (recall ≈ 0.91, precision ≈ 1.0, আমার হিসাব); দুটো মিলিয়ে hybrid; APCA-র label confound (developer patch 82.5%) ও এখানে reference-label confound একই পরিবারের (CG16)।
- সরাসরি সম্পর্কিত CG: CG10 (assurance tool-এর নিজের বৈধতা), CG16, CG17, CG1, CG5 (security বনাম correctness আলাদা), CG12।

**সহজ কথায়:** আগের sub-domain-গুলোতে "plausible মানেই correct নয়" সমস্যা ছিল। ACCA সেই সমস্যার একটা স্বয়ংক্রিয় সমাধান, যার error direction অন্য judge-দের উল্টো।

## ১৮. Supervisor Q&A

1. **প্রশ্ন: ACCA কেন BLEU/Edit Distance-এর চেয়ে ভালো?**
   উত্তর: ওরা character/token মেলায়; ACCA execution-এর শেষ state মেলায়। `mov DL, 5` বনাম `mov BL, 5`-এ ED = 0.96, BLEU-4 = 0.65, অথচ code ভুল। Pearson ρ: ACCA 0.84 বনাম Edit Distance 0.69, BLEU-4 0.56।
2. **প্রশ্ন: "almost perfect" দাবি কতটা সঠিক?**
   উত্তর: Matching 0.93; কিন্তু 99% মতভেদ false negative, ফলে recall প্রায় 0.91 (আমার হিসাব); precision প্রায় 1.0। দাবিটা precision-এর ক্ষেত্রে সঠিক; recall-এ 9% correct code হারায়।
3. **প্রশ্ন: Human ground truth নির্ভরযোগ্য?**
   উত্তর: 3 expert, কিন্তু মতভেদ "oversight" বলে সংশোধন, κ নেই; human NL intent দেখে, ACCA reference দেখে। CG16-এর সমস্যা।
4. **প্রশ্ন: ACCA কি security মাপে?**
   উত্তর: না। Authors নিজে বলেছে এটা semantic correctness (reference-এর সাথে equivalence); vulnerability খোঁজে না।
5. **প্রশ্ন: ACCA-কে gaming করা যায়?**
   উত্তর: paper test করেনি। Reference-এর state মেলানোই লক্ষ্য হলে generator তা শিখতে পারে; CG12 হিসেবে আমাদের পরীক্ষা করতে হবে।
6. **প্রশ্ন: Patch/agent-এ প্রয়োগ হবে?**
   উত্তর: সরাসরি নয়; angr ও 100-step cap ছোট assembly-র জন্য। ধারণাটা (reference-এর সাথে behavioural equivalence) differential execution হিসেবে নেওয়া যায় (PatchDiff-এর মতো)।
7. **প্রশ্ন: ChatGPT-কে judge না ধরে কেন?**
   উত্তর: ρ = 0.64 (GT) ও 0.34 (NL), non-deterministic, prompt iteration লাগে; কিন্তু ChatGPT-3.5 পুরোনো; আধুনিক model-এর ক্ষেত্রে বর্তমান model-এর তথ্য পাওয়া যায়নি।
8. **প্রশ্ন: Paper-এ কোনো সংখ্যার অসঙ্গতি আছে?**
   উত্তর: হ্যাঁ: 0.17 s বনাম Table 7-এর 0.20 s; ChatGPT-NL/GT offset text-এ উল্টে গেছে (0.09/0.12 বনাম Table 4: 0.12/0.09); "চার model" বনাম পাঁচ কলাম।

**সহজ কথায়:** Supervisor-কে উত্তর দেওয়ার সময় সবসময় সংখ্যা সাথে রাখো: 0.84 বনাম 0.69, 99% false negative, 0.91 recall।

## ১৯. Glossary

| Term | অর্থ |
|---|---|
| ACCA | Assembly Code Correctness Assessment: symbolic-execution-ভিত্তিক tool |
| SYN / SEM | Syntactic / Semantic correctness বিট (1 বা 0) |
| Shellcode | exploit-এ ব্যবহৃত machine/assembly instruction-এর ক্রম |
| IA-32 | 32-bit x86 instruction set architecture |
| NASM | Netwide Assembler |
| angr | Binary analysis ও symbolic execution platform (z3 backend) |
| SMT solver | Constraint-এর satisfiability যাচাই করে (z3) |
| SND error | Symbol-Not-Defined: snippet-এর বাইরে define করা label/variable |
| Leaf node | Execution tree-র শেষ state |
| max_steps | Symbolic execution-এর step সীমা (100) |
| Matching rate | ACCA ও human-এর একমত হওয়া sample-এর শতাংশ |
| Offset | Human-এর সাথে গড় correctness-এর পার্থক্য |
| ρ (Pearson) | Linear correlation; binary-binary হলে phi |
| Edit Distance | Character-level পার্থক্য (এখানে 0 থেকে 1, বেশি = কাছাকাছি) |

## ২০. Summary card

| Item | মান |
|---|---|
| Paper | ACCA, JSS 216 (2024) 112113 |
| Idea | Reference-এর সাথে symbolic-execution state equivalence দিয়ে assembly code-এর correctness |
| Data | 5,900 pair; test 590 × 5 generator = 2,950 prediction |
| Human match | 0.93 (0.90 থেকে 0.95) |
| Pearson ρ | ACCA 0.84; Edit Distance 0.69; ChatGPT-GT 0.64; BLEU-4 0.56; ChatGPT-NL 0.34 |
| Offset | ACCA 0.06; Edit Distance 0.08 |
| Correct rate | ACCA 0.65 বনাম Human 0.71 |
| Time | 0.20 s গড় (Table 7); 0.43 s পূর্ণ SE; human ≈ 20 s |
| Error direction | 99% মতভেদ = human 1, ACCA 0 |
| মূল দুর্বলতা | reference = oracle; একক ভাষা; κ/CI/recall নেই; security নয় |
| আমাদের কাজে | CG10, CG16, CG17; hybrid judge; "could not verify" |

**সহজ কথায়:** পুরো paper এক নজরে: reference-এর সাথে শেষ অবস্থা মেলানো, মানুষের সাথে 0.93 একমত, কিন্তু একটু কড়া এবং security দেখে না।

## ২১. বর্তমান (2026) প্রেক্ষাপট

**২১.১ তখন বনাম এখন**

| দিক | Paper (2023–2024) | বর্তমান (2026, context.md) |
|---|---|---|
| Generator | Seq2Seq, CodeBERT, CodeT5+, PLBart, ChatGPT-3.5 | Claude Opus 5.5, GPT-6 family, Gemini 4, DeepSeek V4, Kimi K3.1 Pro ইত্যাদি; ACCA এদের উপর পরীক্ষিত নয় |
| Automated judge | ChatGPT-3.5 (ρ 0.64 / 0.34) | Rubric/LLM-judged mergeability-র দিকে শিল্প যাচ্ছে (FrontierCode); ComPass plain-LLM judge 62.14% overfitting detection (S); judge "over-fix" flag-এ 5–10% precision (S); Opus 5.5/GPT-6 patch-এ judge-এর কোনো study নেই |
| Behavioural equivalence | ACCA: reference-এর সাথে state | PatchDiff: plausible patch-এর 29.6% gold patch-এর থেকে ভিন্ন আচরণ করে (I, পুরোনো model) |
| Security | Correctness আলাদা, security নয় | SusVibes: FuncPass 62–84% কিন্তু SecPass 7.8–17.3% (I); Opus 5.5 prompt-injection success 54.61% safeguard ছাড়া / 11.13% সহ (V) |
| Gaming | বিবেচনায় নেই | METR: সফল long-task run-এর ≥ 16% cheat (I, আগের প্রজন্ম); Opus 5.5 card-এ "hidden tests" reasoning ও git concealment (V) |
| Benchmark | Shellcode_IA32 | SWE-bench Verified saturated (Vals.ai 97.0%, I); SWE-Bench Pro Verified-এ leakage বন্ধে 78.80% → 57.32% (I) |
| খরচ | ACCA ≈ 0.2 s CPU | Agent task খরচ (Vals Terminal-Bench 4.0, I): Opus 5.5 13.20 USD, Kimi K3.1 Pro 4.57, GPT-6.1 Sol 1.72; deterministic checker-এর খরচ এর তুলনায় নগণ্য (আমার হিসাব, paper-এর 0.2 s ও CPU-ভিত্তিক) |

**সহজ কথায়:** ২০২৪-এর পরে generator অনেক শক্তিশালী হয়েছে, কিন্তু ACCA ওদের উপর পরীক্ষিত নয়। Security আর gaming এখন বড় প্রশ্ন, যা এই paper ধরেনি।

**২১.২ এখনও সত্য / পুরোনো**

- এখনও সত্য: text similarity semantic correctness-এর বিকল্প নয়; automated judge-এর error direction ও prevalence বিবেচনা না করলে সংখ্যা বিভ্রান্তিকর; plausible/syntactically-valid ≠ correct (CG1)।
- এখনও সত্য: reference-ভিত্তিক oracle-এর বৈধতা মাপার দরকার (CG16); security আলাদা মাপতে হবে (SusVibes-এর FuncPass বনাম SecPass ফারাক ইঙ্গিত দেয়)।
- সম্ভবত পুরোনো: ChatGPT-3.5-কে baseline judge ধরা; আজকের reasoning judge বা rubric-সহ judge-এর ফল ভিন্ন হতে পারে, তবে সংখ্যাগত তথ্য: বর্তমান model-এর তথ্য পাওয়া যায়নি।
- পুরোনো/সীমিত: ছোট offensive-assembly dataset; আধুনিক agent patch-এর scale (repository-level) এর সাথে ACCA-র সরাসরি মিল নেই।

**২১.৩ আজ খোলা gap**

| Gap | অবস্থা (2026) |
|---|---|
| Reference-equivalence checker আধুনিক agent output-এ | কোনো ACCA-ধরনের study নেই; PatchDiff আংশিক (I) |
| Judge error profile (recall, specificity) আধুনিক model-এ | বর্তমান model-এর তথ্য পাওয়া যায়নি |
| Execution-equivalence + LLM judge-এর hybrid | পাওয়া যায়নি |
| Correctness বনাম security আলাদা assurance signal | SusVibes (I, Opus 4.6/GPT-5.4 যুগ) আংশিক; current-model SusVibes/BaxBench নেই |
| Equivalence checker-কে gaming | METR ও system card প্রসঙ্গ আছে (I/V); equivalence checker-এ নির্দিষ্ট study নেই |

**সহজ কথায়:** আজকের model-এ এই checker কেমন চলে, তার কোনো study এখনও নেই। এটাই আমাদের সুযোগ।

**২১.৪ আজকের model-সহ SPL3 idea (খরচ-সচেতন)**

- একটি ছোট labelled সেট (300–500 patch/snippet) ও দুই-তিনটি judge (deterministic equivalence checker, rubric LLM judge একটি সস্তা open model, একটি অগ্রগামী model ছোট subset-এ)।
- Deterministic checker CPU-তে চলে, প্রায় বিনা খরচে; LLM judge-এর খরচ আলাদা করে USD-তে রেকর্ড করা। সস্তা model দিয়ে প্রথমে স্ক্রিন, শুধু অনিশ্চিত অংশে ব্যয়বহুল model (Opus 5.5 ধরনের task-খরচ 13.20 USD প্রসঙ্গ, যদিও এটি agent task-এর খরচ, judge call-এর নয়)।
- ফলাফল: প্রতিটি signal-এর recall, precision, specificity, κ, CI; এবং "could not verify" হার।
- Fresh SWE-rebench task বা leakage-মুক্ত subset থেকে নমুনা, যাতে contamination (CG6) ঢোকে না।

**২১.৫ ৩টি Q&A**

1. **প্রশ্ন: আজকের model-এ ACCA চালালে কী হবে?**
   উত্তর: বর্তমান model-এর তথ্য পাওয়া যায়নি। সম্ভাবনা: model আরও বৈচিত্র্যময় বৈধ implementation দেবে, ফলে false negative বাড়তে পারে; এটি আমাদের পরীক্ষণীয় অনুমান, ফল নয়।
2. **প্রশ্ন: LLM judge এখন ACCA-কে প্রতিস্থাপন করবে?**
   উত্তর: প্রমাণ নেই। ComPass 62.14% (S) ও over-fix 5–10% precision (S) দেখায় plain judge দুর্বল হতে পারে; পরিপূরক হিসেবে ব্যবহার বেশি যুক্তিসঙ্গত।
3. **প্রশ্ন: Security-র জন্য ACCA যথেষ্ট?**
   উত্তর: না। SusVibes-এর FuncPass 62–84% বনাম SecPass 7.8–17.3% (I) দেখায় functional correctness নিরাপত্তার নিশ্চয়তা নয়।
