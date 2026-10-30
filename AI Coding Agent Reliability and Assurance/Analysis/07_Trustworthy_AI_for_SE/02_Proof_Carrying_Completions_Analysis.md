# Paper Analysis 02 (Trust): Proof-Carrying Code Completions

> Sub-domain: Trustworthy AI for Software Engineering
> PDF: Trustworthy AI for Software Engineering/Proof-Carrying Code Completions.pdf

## ০. Bibliographic info

| ক্ষেত্র | তথ্য |
|---|---|
| Title | Vision Paper: Proof-Carrying Code Completions |
| Authors | Parnian Kamran, Premkumar Devanbu, Caleb Stanford (University of California, Davis, USA) |
| Venue | 39th IEEE/ACM International Conference on Automated Software Engineering Workshops (ASEW 2024), 27 Oct – 1 Nov 2024, Sacramento, CA, USA |
| Pages | 8 pages (প্রকাশিত পৃষ্ঠা 35–42) |
| DOI | 10.1145/3691621.3694932 |
| Paper type | Vision paper + ছোট prototype + একটি preliminary case study (full empirical paper নয়) |
| Tool / code | PC³ (paper-এ লেখা "PC³", PDF text-এ ঘন (superscript) অক্ষর হারিয়ে "3" দেখায়); open source: github.com/DavisPL/PCCC (MIT License) |
| Verifier / language | Dafny 4.6.0 (Hoare-logic ভিত্তিক program verifier) |
| LLM | GPT-4 API (gpt-4-0613), temperature 0.75, LangChain 0.2.7 |
| Funding | US National Science Foundation, award CCF #2403762 |
| License | Creative Commons Attribution 4.0 International |
| আমাদের lens | LLM-এর কোড যদি machine-checkable proof সহ আসে, তাহলে assurance report-এর সবচেয়ে শক্ত signal কী হতে পারে |

## ১. TL;DR

- মূল idea: LLM (শক্তিশালী server, "high-resourced entity") কোড দেবে **এবং** সেই কোডের safety proof দেবে। user (দুর্বল machine, "low-resourced entity") শুধু একটি ছোট, trusted verifier চালিয়ে proof যাচাই করবে। এটাই "proof-carrying code completion" (PC³)।
- user-কে নিজে pre/post-condition লিখতে হয় না। user একবার একটি **global safety property** বাছে (যেমন "কোনো file path-এ `..` থাকবে না")। একটি VC generator (VCGen) সেই property-কে "effectful interface" (file open/read/write ইত্যাদি) -এর precondition-এ বদলে দেয়। LLM-কে প্রমাণ করতে হয় যে তার কোড প্রতিটি interface call-এর precondition মানে।
- Prototype Dafny-তে; interface-এ ৭টি method (Open, Join, Read, Write, Copy, Flush, Seek); Dafny verifier-এর ব্যর্থতা LLM-এ feedback দেয়; সর্বোচ্চ T = 5 attempt।
- Case study মাত্র **একটি task** (predetermined directory-তে filename জুড়ে full path বানানো), CWE-35 (path traversal) -এর বিপরীতে। GPT-4 Python baseline (os.path.join) নিরাপত্তা-guard ছাড়া; PC³ Dafny কোড **প্রথম attempt-এ (k = 1)**, প্রায় 3,350 token ও গড়ে 0.109 USD per query-তে verify হয়েছে।
- সীমা: n = 1 task, correctness হাতে দেখা, VCGen manual, Dafny LLM-এর কাছে out-of-distribution, কোনো কোড-বিশাল benchmark নেই।

**Supervisor-কে ৩০ সেকেন্ডে:**

- Paper একটি "দিকনির্দেশনা" (vision), সংখ্যাগত প্রমাণ নয়। এর মূল অবদান হলো একটি architecture: safety property → precondition on effectful interface → LLM proof → verifier check।
- আমাদের assurance report-এর জন্য এটি "সবচেয়ে শক্ত সম্ভাব্য signal" এর উদাহরণ: test pass না, বরং proof। কিন্তু proof শুধু **নির্বাচিত safety property**-র জন্য, "patch সঠিক" এর জন্য নয়।
- এটি CG1 (plausible ≠ correct) আংশিক সমাধান করে একটি সংকীর্ণ property-র জন্য, CG19 (author oracle নেই) -এ spec-কে oracle বানায়, কিন্তু spec কে লিখবে সে প্রশ্ন সরিয়ে দেয়, মেটায় না (নতুন gap, নিচে CG23)।
- SWE-bench-ধরনের Python repository patch-এ সরাসরি প্রযোজ্য নয়; আমরা একটি "proof-or-abstain" lane ছোট, নির্বাচিত সাবসেটে রাখতে পারি।

## ২. Background (শুধু এই project-এ নতুন concept)

### ২.১ Specification, precondition, postcondition

Specification মানে "কোড কী করবে" তার যান্ত্রিকভাবে-পড়া যায় এমন বিবরণ। দুটি অংশ:

- **Precondition** (`requires`): function ডাকার আগে কী সত্য থাকতে হবে। ডাকার দায়িত্ব caller-এর।
- **Postcondition** (`ensures`): function শেষে কী সত্য থাকবে। দায়িত্ব function-এর।

সহজ উদাহরণ (Dafny):

```
method Divide(a: int, b: int) returns (q: int)
  requires b != 0
  ensures q * b <= a < q * b + b
{ q := a / b; }
```

এখানে `requires b != 0` মানে "শূন্য দিয়ে ভাগ কোরো না"। caller `Divide(5, 0)` লিখলে verifier **কোড চালানোর আগেই** লাল flag দেখায়। এটি test-এর মতো "একটি input-এ চালিয়ে দেখা" নয়; এটি "সব সম্ভাব্য input-এর জন্য" যুক্তি।

### ২.২ Hoare triple

একটি Hoare triple লেখা হয় $\{P\}\ C\ \{Q\}$: "P সত্য অবস্থায় C চালালে শেষে Q সত্য"। Dafny verifier প্রতিটি method-কে এই ধরনের verification condition (VC)-এ ভেঙে SMT solver (Z3)-কে দেয়। solver "সব input-এ সত্য" প্রমাণ করতে পারলে verified; না পারলে error।

### ২.৩ Proof-Carrying Code (PCC)

Necula (1997)-এর classic idea: কোড-producer কোডের সাথে একটি **proof** পাঠায়; consumer একটি ছোট proof-checker দিয়ে যাচাই করে, producer-কে বিশ্বাস না করেই। মূল asymmetry: **proof খুঁজে বের করা কঠিন, proof যাচাই করা সহজ**। বাস্তব উপমা: sudoku-র সমাধান পাওয়া কঠিন, কিন্তু পূরণ-করা grid ঠিক কিনা দেখা সহজ।

- Producer = LLM server (untrusted, শক্তিশালী)।
- Consumer = user machine (trusted checker, দুর্বল)।
- সুবিধা: LLM provider কোড বদলালে proof-ও বদলাতে হবে; না বদলালে validation-এ ধরা পড়বে।

### ২.৪ Safety property বনাম functional correctness

- **Safety property** (Lamport): "কোনো খারাপ কিছু কখনো ঘটবে না" (যেমন path traversal হবে না)। এটি সব প্রোগ্রামের জন্য একই রকম, task-নির্ভর নয়, তাই একবার লিখে বারবার ব্যবহার করা যায়।
- **Functional correctness**: "প্রোগ্রাম ঠিক কাজটি করে" (যেমন sort ঠিক sort করে)। এর জন্য প্রতিটি task-এর নিজস্ব spec দরকার, যা লেখা কঠিন।

Paper ইচ্ছাকৃতভাবে প্রথমটি বেছেছে, কারণ user proof-expert নয়।

### ২.৫ Effectful interface

প্রোগ্রামের সব side effect (file খোলা, লেখা, network, raw memory) যদি একটি নির্দিষ্ট API-র মধ্য দিয়েই যেতে বাধ্য হয়, তাহলে শুধু সেই API-র কলগুলোয় precondition বসিয়ে পুরো প্রোগ্রামের safety নিশ্চিত করা যায়। এটি একটি "চোকপয়েন্ট" মডেল। Dafny-তে এই বাধ্যবাধকতা বলবৎ করা সহজ।

### ২.৬ Verifier feedback loop এবং verify@K

LLM কোড দেয় → Dafny compile + verify → ব্যর্থ হলে error message prompt-এ ফিরিয়ে আবার চেষ্টা। **verify@K** (Misu et al.-এর metric) = K-তম attempt-এর মধ্যে verify হওয়া। এটি আমাদের Sub-domain 2-এর VRpilot-এর compiler-feedback loop-এর সমগোত্রীয়, কিন্তু oracle এখানে test নয়, verifier।

### ২.৭ CWE-35 কী

CWE-35: "Path Traversal: `.../...//`"। CWE-22-এর একটি variant। আক্রমণ: input-এ `../../etc/passwd` দিয়ে নির্দিষ্ট directory (`/home/user/documents/`) থেকে বেরিয়ে সংবেদনশীল file পড়া।

## ৩. Problem

Paper যে সমস্যাগুলো বলছে:

- LLM-এর কোডে কোনো formal guarantee নেই (Figure 1: GitHub Copilot, Sept. 2023, public key-র বদলে private key return করেছে)।
- User কখনো কখনো সন্দেহজনক suggestion accept করে; বিশেষত যারা task-এ অনিশ্চিত তারা বড় block না দেখেই নেয়।
- LLM cloud-এ চলে, তাই provider-ও একটি failure point: provider-কে বিশ্বাস করতে হয় যে সে ঠিক model ঠিকভাবে চালাচ্ছে এবং output "দূষিত" করছে না।
- Paper-এর উল্লেখ: ৬৩% developer LLM tool ব্যবহার করে (Stack Overflow Developer Survey 2024, ref [35])।

এই সমস্যাকে paper abstract স্তরে বলে: শক্তিশালী entity $S$ (provider) কোড $c$ বানায়; দুর্বল entity $U$ (user) চায় $c$ একটি safety property $\varphi$ মানুক। $U$ কীভাবে নিজে $c$-এর সব behavior পরীক্ষা না করেই আত্মবিশ্বাস পাবে?

তিনটি challenge (paper-এ):

1. user proof-বিশেষজ্ঞ নয়, তাই proof পর্দার আড়ালে হতে হবে।
2. LLM-ও Dafny-র মতো proof language-এ অভ্যস্ত নয় (Dafny syntax training corpus-এ বিরল)।
3. code completion আংশিক (incomplete) program; প্রতিটি completion আলাদাভাবে verifiable হতে হবে।

## ৪. Goal & RQ

Goal: "proof-carrying code completions" paradigm প্রস্তাব করা, Dafny-তে একটি prototype বানিয়ে feasibility দেখানো।

Case study-র তিনটি RQ (paper-এর শব্দে সারাংশ):

- RQ1: generated কোড কি নির্বাচিত safety property মানে?
- RQ2: chain-of-thought prompt ও few-shot উদাহরণ কতটা কার্যকরভাবে verify-হওয়া কোড দেয়?
- RQ3: generated কোড কি "correct" (অর্থাৎ ঠিক operation বাস্তবায়ন করে)?

Paper-এর উত্তর: RQ1 হ্যাঁ; RQ2 "modest সংখ্যক token ও একটি মাত্র verification attempt"; RQ3 হ্যাঁ, **manual inspection** দ্বারা।

## ৫. Methodology (ধাপে ধাপে)

### ৫.১ Overall workflow (Figure 2)

1. User একটি task দেয় (task description + method signature)।
2. PC³ prompt বানায়: (ক) task বর্ণনা (user-এর), (খ) effectful interface-এর method তালিকা, সব pre/post-condition সহ (VCGen-এর), (গ) few-shot উদাহরণ (dataset থেকে, চাইলে RAG দিয়ে semantically similar)।
3. User safety property তালিকা থেকে বাছে (বা team/project policy ঠিক করে দেয়)।
4. VCGen property-কে formal VC-তে বদলে interface-এর precondition-এ বসায়।
5. LLM কোড + proof (precondition, assertion) বানায়।
6. Compile + Dafny verify। সফল হলে "Success"; ব্যর্থ হলে error + chat history prompt-এ যুক্ত করে আবার, যতক্ষণ $K \le T$।
7. $K > T$ হলে "Fail"।

Figure 2-এ trusted অংশ (low-resourced entity): compilation, validation, verifier। Untrusted অংশ (high-resourced): LLM, prompt সংযোজন ও retrieval।

### ৫.২ Prompt design

- Chain-of-Thought template (Misu et al. অনুসরণে): SYSTEM message বলে "শুধু দেওয়া Safe API ব্যবহার করো; safety property মানতে প্রয়োজনীয় precondition লিখো; শুধু দেওয়া method signature ও precondition-এর মধ্যে থাকো"।
- Step 1: প্রয়োজনীয় API ও তাদের precondition বাছাই। Step 2: Dafny কোড লেখা।
- Template-এ **৫টি** few-shot উদাহরণ (প্রতি ধাপে expected response সহ)।
- বিকল্প: RAG-ভিত্তিক উদাহরণ নির্বাচন (user query + method signature + safety property spec দিয়ে semantic search)।

### ৫.৩ Effectful interface

- Dafny standard library-র file-system function ও একটি open-source FileIO interface থেকে adapt করা।
- Method: Open, Join, Read, Write, Copy, Flush, Seek।
- অনুমান: OS-এর সাথে সব মিথস্ক্রিয়া এই interface দিয়ে হবে; Dafny-তে এটি বলবৎ করা সহজ।

### ৫.৪ Safety properties ও VCGen

- Safety property: file-system-সম্পর্কিত CWE (Mitre CWE-1219 "File Handling Issues") থেকে অনুপ্রাণিত: path traversal নিষেধ, sensitive file access নিষেধ, home directory access নিষেধ, filename/pathname-এ অবৈধ অক্ষর, path-এ reserved name, অবৈধ file extension।
- VCGen-এর দায়িত্ব (soundness): property $\varphi$ হলে, interface-এর যেকোনো function $f$ ও input $x$-এর জন্য, $x$ VCGen-এর precondition মানলে $f$-এর যেকোনো execution-এর যেকোনো বিন্দুতে program state $\varphi$ মানবে। অর্থাৎ **VCGen-এর ভুল হলে পুরো গ্যারান্টি ভেঙে যায়**; এটি trusted computing base-এর অংশ।
- **বর্তমান implementation-এ VCGen manual**: property থেকে precondition হাতে লেখা।

### ৫.৫ Validation

- Verifier (Dafny; Coq/Idris/Agda/Lean-ও সম্ভাব্য) compile ও verify করে।
- Compiler error (যেমন অজানা function/method name) feedback-এ ফিরে যায়; অতিরিক্ত diagnostic (ভুল API ব্যবহার, method signature hint, error-কে নির্দিষ্ট line-এর সাথে link) যুক্ত হতে পারে।
- সর্বোচ্চ attempt: **T = 5** (verify@K ধারণা)।

### ৫.৬ Case study প্রণালী

- Task: predetermined directory (`/home/user/documents/`)-তে external filename জুড়ে full path বানানো।
- Baseline: GPT-4, Python, safety property ছাড়া (Figure 4 উপরের prompt, Figure 5 response: `os.path.join`)।
- PC³: Dafny, নির্বাচিত safety property তিনটি: path traversal প্রতিরোধ, empty string নিষেধ, invalid character নিষেধ। `Join` method-এ manual precondition (Figure 4 নিচের অংশ)।
- Sanity check (লেখকদের): precondition-গুলো পরস্পর-বিরোধী নয় তা নিশ্চিত করতে method body-তে `assert false` দিয়ে দেখা যে body unreachable কিনা। (অর্থাৎ vacuous proof এড়ানো।)
- Correctness: লেখকরা output হাতে দেখেছেন।

## ৬. Math

Paper-এ কোনো গাণিতিক সমীকরণ নেই। নিচে paper যে ধারণাগুলো ব্যবহার করে সেগুলোর আনুষ্ঠানিক রূপ (আমার formalisation, paper-এর বাক্যের উপর ভিত্তি করে); প্রতিটি symbol ব্যাখ্যা সহ।

### ৬.১ Hoare triple

$$
\{P\}\ C\ \{Q\}
$$

- $P$ = precondition, $C$ = কোড, $Q$ = postcondition। অর্থ: যেকোনো state $s \text{ satisfies } P$ থেকে $C$ চালালে শেষ state $s' \text{ satisfies } Q$।

### ৬.২ VCGen soundness (paper §২.৪-এর বাক্যের আনুষ্ঠানিক রূপ)

$$
\forall f \in \mathcal{I},\ \forall x:\ \big(x \text{ satisfies } \mathrm{Pre}_{\varphi}(f)\big) \Rightarrow \forall \text{ execution } e \text{ of } f(x),\ \forall t:\ \mathrm{state}_e(t) \text{ satisfies } \varphi
$$

- $\mathcal{I}$ = effectful interface-এর method-সমষ্টি; $\varphi$ = নির্বাচিত safety property; $\mathrm{Pre}_{\varphi}(f)$ = VCGen-এর বানানো precondition; $t$ = execution-এর যেকোনো বিন্দু।
- অর্থ: precondition মানলে পুরো execution জুড়ে property সত্য।

### ৬.৩ Program-level safety (আমার সংযোজন, paper-এর "key contract" থেকে)

$$
\Big(\forall\, \text{call } f(x) \text{ in } c:\ \text{verifier proves } \mathrm{Pre}_{\varphi}(f)(x)\Big) \land \Big(\text{effects only via } \mathcal{I}\Big) \Rightarrow c \text{ satisfies } \varphi
$$

- $c$ = LLM-এর কোড। দুটি শর্ত: (১) প্রতিটি interface call-এর VC প্রমাণিত, (২) side effect **শুধু** $\mathcal{I}$ দিয়ে। দ্বিতীয় শর্ত ভাঙলে (interface এড়িয়ে গেলে) গ্যারান্টি নেই; "weird machines" (Vanegue) এই ধরনের লুকানো ফাঁক।

### ৬.৪ verify@K

$$
\text{Success} \iff \exists K \le T:\ \mathrm{Verify}(c_K) = \text{true}
$$

- $c_K$ = $K$-তম attempt-এর কোড, $T$ = সর্বোচ্চ attempt (paper-এ $T = 5$)। Figure 2-এ শর্তগুলো: "$K \le T$ ও verified" → Success; "$K > T$" → Fail।
- Paper-এ aggregate metric (যেমন task-এর উপর গড়) নেই, কারণ মাত্র একটি task।

### ৬.৫ Worked example: Figure 6-এর verification obligation

Join-এর precondition (Figure 4) থেকে filename $f$-এর জন্য প্রাসঙ্গিক শর্ত:

$$
\mathrm{non\_empty}(f) \land \neg\,\mathrm{dangerous}(f) \land \mathrm{valid\_name}(f) \land \mathrm{valid\_len}(f)
$$

GPT-4-র Figure 6 কোড নিজের `requires`-এ এই চারটি শর্তই (non_empty_string, is_valid_file_name, !has_dangerous_pattern, has_valid_file_length) তুলে ধরে এবং directory constant `/home/user/documents/` দিয়ে Join ডাকে। ফলে Join-এর precondition caller-precondition থেকে অনুসরণ করে; verifier সম্ভুষ্ট। **মূল কৌশল:** "বিপজ্জনক input প্রতিরোধ" দায়িত্বটা caller-এর precondition-এ ঠেলে দেওয়া হয়েছে; অর্থাৎ প্রোগ্রাম নিরাপদ **ঐ চুক্তির অধীনে** (যে কেউ `CreateFullPath` ডাকবে তাকে filename ভালো রাখতে হবে)।

### ৬.৬ আমার হিসাব: token cost

- Paper: প্রায় 3,350 token, গড়ে 0.109 USD per query।
- আমার হিসাব: $0.109 / 3{,}350 \approx 0.0000325$ USD per token $\approx 32.5$ USD per million token (blended)।
- আমার হিসাব (অনুমান; paper-এ মূল্যতালিকা নেই): gpt-4-0613 (8k)-এর তৎকালীন list মূল্য ধরলে input 0.03 USD ও output 0.06 USD per 1,000 token। $x$ = input token, $y$ = output token হলে $x + y = 3350$ এবং $0.00003x + 0.00006y = 0.109$। প্রথম সমীকরণ থেকে $0.00003 	imes 3350 = 0.1005$, তাই $0.00003y = 0.0085$, অর্থাৎ $y \approx 283$ token ও $x \approx 3067$ token। মানে খরচের বেশিরভাগ prompt (few-shot ও API list), output ছোট। এই মূল্য আমি paper-এর বাইরে থেকে ধরেছি, তাই নিশ্চিত নয়।

## ৭. Setup (table)

| উপাদান | মান |
|---|---|
| LLM | GPT-4 API, gpt-4-0613 (paper-এ "released March 14, 2023", "175 billion parameters", "8192 token context" লেখা) |
| Temperature | 0.75 |
| Framework | LangChain 0.2.7 |
| Verifier | Dafny 4.6.0 |
| Machine | Apple M1 Pro, 10 core, 16 GB, macOS 14.5 |
| পরীক্ষার তারিখ | 10 August 2024 |
| Task সংখ্যা | 1 |
| Attempt | k = 1 (সফল); T = 5 (সর্বোচ্চ) |
| Few-shot | 5টি Dafny উদাহরণ |
| Safety property (case study) | path traversal নিষেধ; empty string নিষেধ; invalid character নিষেধ |
| Baseline | GPT-4 Python, property ছাড়া |
| Correctness যাচাই | লেখকদের manual inspection |
| Consistency যাচাই | `assert false` দিয়ে body unreachable দেখা |

## ৮. Results

কোনো মূল result table নেই; সব তথ্য §৩ (Case study) ও Figure 4–6 থেকে।

| বিষয় | ফলাফল | উৎস |
|---|---|---|
| Baseline (Python, os.path.join) | কার্যকরী, কিন্তু `../../etc/passwd` ধরনের input আটকানোর কোনো guard নেই | §৩, Figure 5 |
| PC³ (Dafny), প্রথম attempt | CWE-35 এড়ানোর precondition ঠিকভাবে তৈরি | §৩, Figure 6 |
| Attempt সংখ্যা | k = 1 | §৩ |
| Token ব্যবহার | প্রায় 3,350 | §৩ |
| Cost | গড় 0.109 USD per query (CoT template) | §৩ |
| RQ1 (safe?) | হ্যাঁ | §৩ Conclusions |
| RQ2 (efficient?) | হ্যাঁ, modest token, এক attempt | §৩ Conclusions |
| RQ3 (correct?) | হ্যাঁ, manual inspection; precondition সামঞ্জস্যপূর্ণ | §৩ Conclusions |

Figure 6-এর কোডের গঠন: `CreateFullPath(filename: seq<char>)` method; `requires` চারটি (non_empty_string, is_valid_file_name, !has_dangerous_pattern, has_valid_file_length); body-তে `directory := "/home/user/documents/"` ও `fullPath := Join(directory, filename)`।

লক্ষ্য করুন: কোনো success rate, কোনো ব্যর্থ উদাহরণ, কোনো একাধিক-task বা একাধিক-run তথ্য নেই।

## ৯. Key findings

1. **Architecture-level**: global safety property → effectful interface precondition → LLM proof → verifier, এই pipeline user-কে spec লেখা থেকে অব্যাহতি দেয়।
2. প্রতিটি dangerous call-এর নিজস্ব verification query থাকে; কোডের body অসম্পূর্ণ হলেও কিছু call আলাদা যাচাই করা যায় (partial completion সমস্যার সমাধান)।
3. Case study-তে GPT-4 একটি task-এ প্রথম attempt-এ সঠিক precondition-সহ Dafny কোড দিয়েছে (3,350 token, 0.109 USD)।
4. Baseline Python কোড functionally ঠিক হলেও path traversal-এ অরক্ষিত; PC³ কোডে ঝুঁকি যান্ত্রিকভাবে (verifier দ্বারা) বাদ।
5. Proof-এর অসঙ্গতি এড়াতে `assert false` (vacuity) পরীক্ষা ব্যবহার করা হয়েছে, এটি ছোট কিন্তু গুরুত্বপূর্ণ নকশা-সচেতনতা।
6. লেখকদের নিজস্ব অভিজ্ঞতা: Dafny-তে LLM দিয়ে কোড বানানো মূলধারার ভাষার তুলনায় "অনেক কঠিন"; তাই মূলধারার ভাষায় PC³ বা fine-tuning ভবিষ্যৎ কাজ।
7. Related work-এ নিজেদের অবস্থান: Misu et al. (Dafny + user-supplied pre/post + tests, safety property নয়) ও Laurel (helper assertion) থেকে আলাদা।

## ১০. Why better than alternatives

| বিকল্প | সমস্যা | PC³-এর সুবিধা |
|---|---|---|
| শুধু test | কিছু input দেখে; absence-of-bug প্রমাণ করে না | verifier সব input-এ যুক্তি করে (নির্বাচিত property-র জন্য) |
| Static analyzer / SAST (Sub-domain 6) | false positive/negative, ভিন্ন tool ভিন্ন মত | সফল হলে sound proof (verifier ও VCGen ঠিক থাকলে) |
| LLM-as-judge (Sub-domain 5) | ভুল দিক ও persuasion-এ দুর্বল | judge নয়, যান্ত্রিক checker; persuade করা যায় না |
| মানুষ review | ক্লান্তি, অসঙ্গতি | স্বয়ংক্রিয়, user-কে proof পড়তে হয় না |
| Full functional verification (Misu et al.) | user-কে spec/test লিখতে হয় | property একবার বাছলেই চলে |

কিন্তু "better" কেবল সংকীর্ণ অর্থে: paper কোনো সংখ্যাগত তুলনা করেনি।

## ১১. When it works / fails

**কাজ করে যখন:**

- property সহজ ও task-নিরপেক্ষ (path traversal, bounds, empty string)।
- সব side effect একটি ছোট interface দিয়ে যায়।
- ভাষায় verifier আছে (Dafny/Lean/Coq/F∗/Verus)।
- কোড ছোট, একটি function-স্কেলের।

**ব্যর্থ হয় যখন:**

- property functional correctness (যেমন "ঠিক sort")। তখন spec লিখতে হবে।
- ভাষা mainstream (Python/C/Rust) এবং verifier নেই বা দুর্বল; paper নিজেই বলে Dafny কোড বানানো কঠিন।
- interface সম্পূর্ণ নয় (network, database, raw memory interface এখনো নেই)।
- VCGen ভুল বা অসম্পূর্ণ।
- LLM অসামঞ্জস্যপূর্ণ (contradictory) precondition লিখে vacuous proof বানায়।
- "weird machines": spec-এ অদৃশ্য side effect (Vanegue)।

## ১২. Limitations

**লেখকদের স্বীকৃত:**

- VCGen আপাতত manual; সাধারণ treatment ভবিষ্যৎ কাজ।
- শুধু file system interface; network/database/memory/system call interface পরে।
- Safety property description-এর জন্য user-friendly configuration language (যেমন access control policy ভিত্তিক) দরকার।
- Dafny কোড বানানো মূলধারার ভাষার চেয়ে অনেক কঠিন; prompt engineering ও fine-tuning দরকার।
- LLM proof-এ ব্যর্থতার উদাহরণ আছে (ref [68]); paper নিজেই এটি উল্লেখ করেছে।

**আমার পর্যবেক্ষণ:**

- n = 1 task, একটি model, একটি attempt: কোনো সাধারণীকরণ বা variance (CG4) নেই। Temperature 0.75-এ অন্য run-এ ফল ভিন্ন হতে পারত।
- Correctness manual inspection; RQ3-এর "yes" যান্ত্রিক নয়, তাই লেখকদের নিজস্ব ধারণার উপর নির্ভরশীল।
- "Safe" মানে "precondition মানে"; কিন্তু precondition-গুলো **caller-এর দায়িত্বে** ঠেলে দেওয়া। `CreateFullPath` নিজে filename sanitize করে না; সে শুধু বলে "আমাকে ভালো filename দাও"। প্রকৃত system-এ ঐ method-কে কেউ খারাপ input দিয়ে ডাকলে একই verifier সেই caller-এ আপত্তি তুলবে কিনা তা নির্ভর করে পুরো প্রোগ্রাম verify হওয়ার উপর। Completion-in-isolation মডেলে এটি অমীমাংসিত।
- Figure 4-এর Join precondition-এ `has_absoloute_path(f)` (বানান paper-এই এমন) আছে, অথচ Figure 6-এর `CreateFullPath` সেই শর্ত তার `requires`-এ তোলে না। এটি পর্যবেক্ষণযোগ্য অসঙ্গতি: কীভাবে Join-এর সব precondition (বিশেষ করে `has_valid_path_length(p+f)` ও `has_absoloute_path(f)`) discharge হলো তা paper দেখায়নি; সম্ভবত Dafny-র `path`/`file` type বা helper predicate-এর সংজ্ঞায় লুকানো, কিন্তু সংজ্ঞা paper-এ নেই।
- "CWE-35" খুব নির্দিষ্ট variant (`.../...//`); সাধারণ path traversal সাধারণত CWE-22। Safety property সংজ্ঞায়িত `has_dangerous_pattern` কীভাবে সব encoding (percent-encoding, backslash, symlink) ধরে তা বলা নেই।
- Paper-এর "GPT-4: 175 billion parameters" তথ্যটি OpenAI কখনো প্রকাশ করেনি বলে আমার জানা; এই দাবি যাচাইযোগ্য নয় (প্রাসঙ্গিক নয়, কিন্তু সতর্কতা)।
- Baseline unfair: Python baseline-এ safety prompt/spec নেই, PC³-তে আছে; একটি fair baseline হতো "Python + একই safety instruction" বা "Dafny + কোনো interface precondition ছাড়া"। কোনো ablation নেই (CoT বনাম few-shot বনাম RAG)।
- Cost 0.109 USD একটি সফল attempt-এর; ব্যর্থ/পুনরাবৃত্ত attempt-এর খরচ জানা নেই।

## ১৩. Research gaps

| G-id | Gap | Evidence | Related CG / our folder |
|---|---|---|---|
| G1 | একাধিক task, একাধিক model, একাধিক run-এ verify@K ও success rate নেই | §৩: মাত্র একটি task, k = 1 | CG4, CG8 / 03 Evaluation |
| G2 | Specification কে লিখবে ও সেই spec যথেষ্ট কিনা কীভাবে যাচাই হবে | §১: safety property পূর্বনির্বাচিত; §৫: VCGen manual | নতুন CG23 (spec adequacy) / 07 |
| G3 | VCGen ও effectful interface trusted base; তাদের সঠিকতা যাচাইয়ের উপায় নেই | §২.৪ "up to VCGen to do this correctly" | নতুন CG24 / 06 Security |
| G4 | Repository-level patch ও mainstream language-এ প্রয়োগ | §৫ Discussion: Python/C/Rust-এ কঠিন | CG9 / 01 Agents |
| G5 | Functional correctness-এর proof (issue-resolution) এই paper-এর বাইরে | §১: global safety property ইচ্ছাকৃত | CG1, CG19 / 01, 05 |
| G6 | Verifier-কে "ঠকানো" (vacuity, `assume false`, `{:verify false}`) থেকে রক্ষা শুধু একটি `assert false` check | §৩ | CG12 / 03 |
| G7 | Proof-সহ কোড বনাম Python কোডের সম্পর্ক: কোড Dafny থেকে অন্য ভাষায় compile হলে গ্যারান্টি কতটা থাকে | paper আলোচনা করেনি | CG9 / 07 |
| G8 | Safe property বনাম বাস্তব vulnerability: precondition-এর recall কত (কত CWE ধরে) | §৩: ছয় ধরনের property তালিকাভুক্ত, মাপা নয় | CG21 / 06 |
| G9 | "প্রমাণ ব্যর্থ" হলে কী: abstain নাকি বিকল্প signal | Figure 2: শুধু "Fail" | CG7 / 03 |

## ১৪. Improvement ideas

1. **Spec-lite agent patch check**: agent patch-এর diff-এ নতুন dangerous call (file, network, eval, subprocess) যান্ত্রিকভাবে খুঁজে প্রতিটির জন্য precondition-অবশ্যই-মানা property (যেমন "path বাইরে যাবে না") ছোট Dafny/Verus/Lean-এ নয় বরং Python runtime-contract (icontract/deal)-এ রেখে একটি **hybrid signal** বানানো; proof নয়, "contract-checked" লেবেল।
2. **VCGen স্বয়ংক্রিয়করণ**: CWE → precondition catalog (property library) তৈরি; প্রতিটির সঙ্গে test-suite যা precondition-কে adversarial input দিয়ে পরীক্ষা করে (VCGen soundness-এর যান্ত্রিক sanity check)।
3. **Vacuity ও spec-strength audit**: `assert false`-ছাড়াও mutation testing: precondition দুর্বল করলে কোড কি আর verify হয়? প্রতিটি `requires` দরকারি কিনা (CG13-এর proof-জগতের সংস্করণ)।
4. **Tri-state verdict**: Verified / Counterexample or Failed / Unverifiable (spec নেই বা ভাষা সমর্থিত নয়)। CG22-এর সমাধানের সঙ্গে মেলে।
5. **Proof repair loop-এ distinct feedback**: error-কে line-এর সাথে link করার আইডিয়া RePaCA/VRpilot-এর feedback loop-এর সঙ্গে তুলনীয়; ablation চালানো (compiler error only vs counterexample vs assertion hint)।
6. **Fair baseline**: একই safety instruction সহ Python/Dafny/Verus, একই model, একাধিক run, McNemar paired test।

## ১৫. Publication potential (SPL3-feasible)

- পুরো PC³ পুনর্নির্মাণ বা পুনরুৎপাদন SPL3-র সাধ্যের মধ্যে ছোট পরিসরে সম্ভব, কিন্তু নতুন formal-verification প্রযুক্তি বানানো কঠিন।
- বাস্তবসম্মত অবদান: **"Proof-or-abstain" লেনের সম্ভাব্যতা-অধ্যয়ন**: agent-patch-এর কত শতাংশ (নির্দিষ্ট ছোট class: file path, bounds, null) সরল property-তে mechanical checking-এর যোগ্য? এটি একটি empirical measurement paper (workshop/short paper স্তরের)।
- Venue-ধরন: ASE/ICSE workshop (যেমন LLM4Code, Dafny workshop, FORGE)। আমি নির্দিষ্ট venue-র সময়সীমা নিয়ে নিশ্চিত নই।
- ঝুঁকি: LLM-কে Dafny/Verus লেখাতে গিয়ে সময় চলে যেতে পারে (paper নিজেই বলে কঠিন)।

## ১৬. SPL3 implementation

ছোট, নিয়ন্ত্রিত পরিকল্পনা (assurance report-এর একটি optional "formal lane"):

1. **Property catalog (সপ্তাহ ১)**: ৪-৫টি সরল, task-নিরপেক্ষ property: path traversal নিষেধ; array index bound; null/None dereference নেই; subprocess-এ shell injection নেই; hard-coded secret নেই।
2. **Applicability scanner (সপ্তাহ ২)**: SWE-rebench বা SWE-Bench Pro Verified subset-এর gold/agent patch-এ diff পড়ে (AST) বের করা: কতটা patch-এ ঐ dangerous call আছে? আমার ধারণা অধিকাংশ patch-এ থাকে না; তাই coverage-ই প্রথম ফলাফল।
3. **Checker (সপ্তাহ ৩-৪)**: Python-এর জন্য verifier নেই বলে দুটি সম্ভাবনা: (ক) CrossHair/Nagini ধরনের Python verifier (আমি নির্দিষ্ট করে যাচাই করিনি), (খ) PC³-এর মূল ছোট C/Rust/Dafny উদাহরণ নিয়ে pilot। বাস্তবসম্মত: ছোট function-স্কেল (HumanEval-ধরনের) task-এ Dafny/Verus-এ GPT/Claude দিয়ে verify@K মাপা।
4. **Metrics**: verify@K (K = 1, 3, 5), vacuity-fail হার (`assert false`/mutation), cost per verified completion (USD), run-to-run variance (≥ ৫ run)।
5. **Report format**: প্রতিটি patch-এ তিনমুখী "Proof: verified / failed / not-applicable", আলাদা signal হিসেবে, weighted score-এ মেশানো নয়।
6. **Environment**: Dafny 4.x / Verus; verifier version ও solver (Z3) version log (CG11)।

## ১৭. Influence / link to our earlier sub-domains

- **Sub-domain 1 (Agents)**: Agentless/SWE-agent-এর patch যাচাই test-ভিত্তিক; PC³ বিকল্প oracle দেয়, কিন্তু function-scale।
- **Sub-domain 2 (APR)**: VRpilot-এর compiler/sanitizer feedback loop-এর সঙ্গে PC³-এর verifier feedback loop কাঠামোগতভাবে সমান; পার্থক্য: oracle এখানে sound (নির্দিষ্ট property-র জন্য)। RePaCA-র overfitting detection-এর low specificity সমস্যা এখানে নেই (verifier মিথ্যা "verified" দেয় না, ধরে নিলে VCGen ঠিক), কিন্তু "failed" মানে "ভুল" নয় (LLM প্রমাণ খুঁজে পায়নি)।
- **Sub-domain 3 (Evaluation)**: SWE-rebench/SWE-Bench Pro-তে task-সংখ্যা ও variance; PC³ case study-তে ঠিক উল্টো (n = 1), তাই CG4/CG8 এখানে সরাসরি প্রযোজ্য।
- **Sub-domain 4 (Test generation)**: test-এর oracle strength (CG13) vs spec-এর strength: পরেরটি একই সমস্যা, শুধু বেশি যান্ত্রিক।
- **Sub-domain 5 (Patch validation)**: LLM judge-এর ভুল দিক ও persuasion (CG17, CG18)। Proof-checker persuade করা যায় না; সেটা প্রধান সুবিধা।
- **Sub-domain 6 (Security)**: CWEval/SusVibes-এর func-sec gap; PC³ ঠিক ঐ gap (functional ঠিক, security নেই) পূরণ করতে চায়: Figure 5 baseline ঠিক সেই উদাহরণ।
- **এই sub-domain (Trust)**: Proof-carrying completions হলো trust-এর "সবচেয়ে শক্ত" প্রান্ত; বাকি paper সম্ভবত confidence/calibration-ধরনের নরম signal।

আমাদের CG-র সাথে সরাসরি সংযোগ:

| CG | PC³ কীভাবে সম্পর্কিত | সীমা |
|---|---|---|
| CG1 (plausible ≠ correct) | নির্বাচিত property-র জন্য "plausible" নয়, "প্রমাণিত"। | শুধু property-র জন্য; অন্য আচরণ অজানা |
| CG13 (test oracle strength) | spec হলো oracle; precondition দুর্বল হলে প্রমাণও দুর্বল | spec strength মাপার উপায় paper-এ নেই |
| CG19 (author oracle নেই) | user লেখে না; property catalog + VCGen oracle-এর কাজ করে | catalog কে লিখল? trusted base |
| CG22 (reference-anchored oracle valid বিকল্প বাতিল করে) | spec-ভিত্তিক oracle gold patch-এর উপর নির্ভর করে না; যেকোনো সঠিক বাস্তবায়ন মানা হয় | spec অতিরিক্ত সংকীর্ণ হলে বৈধ কোডও ব্যর্থ |
| CG12 (gaming) | যান্ত্রিক checker persuasion-প্রতিরোধী, কিন্তু vacuity/`assume` দিয়ে ঠকানো সম্ভব | `assert false` ছাড়া আর কিছু নেই |

## ১৮. Supervisor Q&A

**প্র১. Proof-carrying code বলতে কী বোঝায়, এক বাক্যে?**
উত্তর: কোডের সাথে এমন একটি যান্ত্রিকভাবে-যাচাইযোগ্য proof আসে, যা consumer একটি ছোট checker দিয়ে যাচাই করে producer-কে বিশ্বাস না করেই। অসমমিতি: proof বানানো কঠিন, যাচাই সহজ।

**প্র২. Test pass করা আর proof verified হওয়ার পার্থক্য কী?**
উত্তর: test কিছু নির্বাচিত input দেখে; verifier নির্ধারিত property-র জন্য সব input-এ যুক্তি করে। উদাহরণ: `Divide(a, b)`-এ test `b = 1, 2, 3` দিলে পাশ করে, কিন্তু `requires b != 0` না থাকলে verifier call-site-এ `Divide(x, y)` (y অজানা) আটকে দেয়। তবে proof শুধু spec যা বলে তা-ই প্রমাণ করে; spec ভুল বা দুর্বল হলে proof অর্থহীন।

**প্র৩. Paper-এর সবচেয়ে বড় সংখ্যাগত ফলাফল কী?**
উত্তর: একটি task, k = 1, প্রায় 3,350 token, গড়ে 0.109 USD per query (§৩)। এর বেশি কোনো সংখ্যা নেই; তাই আমরা এটিকে feasibility-র ইঙ্গিত হিসেবে পড়ি, প্রমাণ হিসেবে নয়।

**প্র৪. এই পদ্ধতিতে spec কে লেখে? এটি কি CG19 সমাধান করে?**
উত্তর: আংশিক। user লেখে না; safety property তালিকা থেকে বাছা হয় এবং VCGen (আপাতত manual) precondition বানায়। অর্থাৎ spec-লেখার দায়িত্ব গেছে property-catalog ও VCGen-এর লেখকের কাছে। তাই CG19 "author oracle নেই" সমস্যা spec-এর trusted base-এ পরিণত হয়; আমি এটিকে নতুন CG23/CG24 বলছি।

**প্র৫. Agent-এর SWE-bench patch-এ এটি কি প্রয়োগযোগ্য?**
উত্তর: আজকের অবস্থায় সরাসরি নয়। (ক) Python-এ Dafny-মতো যাচাইকারী নেই, (খ) issue-fix-এর spec "bug ঠিক হয়েছে", যা property নয় functional spec, (গ) repository-level কোডে effectful interface আলাদা করা কঠিন। সম্ভাব্য: ছোট class-এর patch-এ (file path, bounds) সীমিত formal lane।

**প্র৬. Verified হলে কি কোড নিরাপদ?**
উত্তর: না, শর্তসাপেক্ষে: (১) VCGen সঠিক হতে হবে; (২) side effect সব interface দিয়ে যেতে হবে; (৩) property সত্যিই বিপদটি ধরে (যেমন `has_dangerous_pattern` সব encoding ধরে); (৪) verifier ও solver bug-মুক্ত; (৫) precondition vacuous নয়। Paper শুধু (৫)-এর জন্য `assert false` check করেছে।

**প্র৭. Verification failed হলে কী ধরে নেব?**
উত্তর: "কোড ভুল" নয়; "LLM প্রমাণ খুঁজে পায়নি"। এই ফল কোডের দোষ নয়, LLM-এর proof-synthesis দক্ষতার সীমা হতে পারে। তাই report-এ "Unverified" আলাদা অবস্থা (tri-state) রাখা দরকার।

**প্র৮. কেন Dafny, আর এতে সমস্যা কী?**
উত্তর: Dafny industrial-standard Hoare-logic verifier, inline pre/post-condition-এর সুবিধা, এবং Z3 backend। সমস্যা: LLM-এর training data-তে বিরল (paper নিজেই বলে out-of-distribution), তাই কোড-লেখা mainstream ভাষার তুলনায় কঠিন।

## ১৯. Glossary

| শব্দ | সংক্ষিপ্ত অর্থ |
|---|---|
| Proof-carrying code | কোডের সাথে যান্ত্রিকভাবে যাচাইযোগ্য proof |
| Specification | কোডের প্রত্যাশিত আচরণের formal বিবরণ |
| Precondition (`requires`) | call-এর আগে সত্য হতে হবে এমন শর্ত |
| Postcondition (`ensures`) | call-এর পরে সত্য থাকবে এমন শর্ত |
| Hoare logic | $\{P\}\,C\,\{Q\}$ ধরনের কোড-যুক্তি পদ্ধতি |
| Verification condition (VC) | verifier-কে প্রমাণ করতে হবে এমন logical formula |
| VCGen | safety property থেকে VC/precondition বানানোর উপাদান |
| Effectful interface | সব side effect যে API দিয়ে যায় |
| Safety property | "খারাপ কিছু ঘটবে না" ধরনের property |
| Dafny | verification-সমর্থিত ভাষা ও verifier |
| verify@K | K attempt-এর মধ্যে verify হওয়া |
| CWE-35 | Path traversal variant (`.../...//`) |
| Vacuous proof | অসম্ভব precondition-এর কারণে অর্থহীন proof |
| Weird machine | spec-এ অদৃশ্য অনাকাঙ্ক্ষিত আচরণ |

## ২০. Summary card

| বিষয় | সংক্ষেপ |
|---|---|
| Idea | LLM কোড + safety proof দেয়, user verifier দিয়ে যাচাই করে |
| Spec কীভাবে | global safety property → VCGen → effectful interface precondition |
| Prototype | Dafny 4.6.0, GPT-4 (gpt-4-0613), T = 5 |
| Evidence | ১টি task, k = 1, ~3,350 token, 0.109 USD, manual correctness |
| শক্তি | persuasion-প্রতিরোধী, sound signal (শর্তসাপেক্ষে), user-কে spec লিখতে হয় না |
| দুর্বলতা | n = 1, VCGen manual, Dafny কঠিন, শুধু safety, trusted base |
| আমাদের কাজে | assurance report-এ ঐচ্ছিক "Proof: verified / failed / n.a." signal; নতুন CG23, CG24 |

## ২১. বর্তমান (2026) প্রেক্ষাপট

প্রাপ্ত 2026 তথ্য শুধু context.md থেকে (V = vendor-reported, I = independent, S = search-snippet)। Formal verification-এর (Dafny/Verus/Lean) সরাসরি current-model তথ্য context-এ **নেই**: বর্তমান model-এর তথ্য পাওয়া যায়নি।

### ২১.১ Then vs now

| বিষয় | Paper (2024) | 2026 তথ্য (context.md) |
|---|---|---|
| Model | GPT-4 (gpt-4-0613) | Claude Opus 5.5, Fable 5.1, Sonnet 5.5; GPT-6 family; Gemini 4 Argon; open: Kimi K3.1 Pro, GLM-5.x, DeepSeek V4 |
| Proof-generation ক্ষমতা | একটি task, k = 1 | বর্তমান model-এর তথ্য পাওয়া যায়নি |
| কোড-সুরক্ষা অবস্থা | Copilot-এর ভুল key উদাহরণ | SusVibes: FuncPass 62–84% কিন্তু SecPass 7.8–17.3% (I, Opus 4.6/GPT-5.4 যুগ) |
| Test oracle মান | paper আলোচনা করেনি | agent-লেখা test patch-এর 80.2% এ দুর্বল/কোনো oracle নেই (I) |
| Benchmark | নেই | SWE-bench Verified saturated: Vals.ai 97.0% (I); OpenAI ব্যবহার বন্ধ করেছে, audited subset-এর ≥ 59.4% এ ত্রুটিপূর্ণ test (S) |
| Gaming | উল্লেখ নেই | METR: সফল long-task run-এর ≥ 16% cheat (I, আগের প্রজন্ম); Opus 5.5 card-এ "hidden tests" reasoning ও git concealment কিছু environment-এ (V) |
| Cost per task | 0.109 USD per query (এক মুহূর্তের) | Vals Terminal-Bench 4.0 (I): Opus 5.5 13.20 USD, Kimi K3.1 Pro 4.57, GPT-6.1 Sol 1.72 (কাজের ধরন ভিন্ন, তুলনীয় নয়) |

### ২১.২ এখনও সত্য / পুরনো

**এখনও সত্য (context-এর আলোকে):**

- Test-ভিত্তিক signal দুর্বল: 80.2% দুর্বল oracle (I) ও SWE-bench Verified-এর সমস্যা paper-এর "tests are not enough" মনোভাবকে সমর্থন করে।
- Functional ঠিক কিন্তু security দুর্বল: SusVibes-এর 62–84% বনাম 7.8–17.3% gap ঠিক সেই সমস্যা যা Figure 5 ছোট আকারে দেখায়।
- Gaming ঝুঁকি: ≥ 16% cheat (I) দেখায় কেন persuasion-মুক্ত যান্ত্রিক checker আকর্ষণীয়, তবে একটি checker-ও gaming-এর লক্ষ্য হতে পারে (আমার পর্যবেক্ষণ)।

**পুরনো / যাচাই দরকার:**

- GPT-4-ভিত্তিক proof-সংশ্লেষণ ক্ষমতা আজকের model-এর ক্ষমতা নির্দেশ করে না; বর্তমান model-এর তথ্য পাওয়া যায়নি।
- "Dafny কঠিন" মন্তব্য নতুন model-এ বদলাতে পারে; context-এ প্রমাণ নেই।
- 0.109 USD এখনকার agentic task-এর খরচের সাথে তুলনীয় নয়।

### ২১.৩ আজও খোলা gap

| Gap | কেন এখনও খোলা (context.md থেকে) | সংযোগ |
|---|---|---|
| বর্তমান model-এর formal proof ক্ষমতা (verify@K) | context-এ কোনো তথ্য নেই | G1 |
| Agent patch-এ spec/precondition-ভিত্তিক security gate | SecPass 7.8–17.3% (I) দেখায় প্রয়োজন; কিন্তু current-model SusVibes/BaxBench তথ্য নেই | CG5, CG20 |
| Oracle শক্তি | 80.2% দুর্বল oracle (I); proof-oracle-এর spec শক্তি মাপা হয়নি | CG13, CG23 |
| Verifier/checker gaming | METR ≥ 16% cheat (I); verifier-লক্ষ্যিত gaming-এর তথ্য নেই | CG12 |
| Version-bound verdict | verifier/solver version নথিভুক্ত করার প্রমাণ নেই | CG11 |

### ২১.৪ SPL3 idea (বর্তমান model, cost-aware)

- Model-স্তর: একটি সস্তা open model (যেমন Kimi K3.1 Pro 4.57 USD per task, GPT-6.1 Sol 1.72 USD per task, Vals Terminal-Bench 4.0, I) ও একটি বড় model-এর তুলনা; কিন্তু ঐ খরচ Terminal-Bench কাজের, proof-কাজের নয়; আমি আলাদা মাপব।
- Pilot: ১০০টি ছোট function-স্কেল task (file path, bounds), প্রতি task ৫ run, K ≤ 5; মাপব verify@K, vacuity হার, USD per verified completion।
- Budget নিয়ম: আগে সস্তা model-এ চালিয়ে ব্যর্থদের শুধু বড় model-এ পুনরায়; "Unverified" আলাদা গণনা।
- Report-এ আলাদা signal হিসেবে রাখব, weighted score-এ নয়।
- বাস্তবতা: Python repository patch-এ coverage হয়তো কম; তাই প্রথম ফল coverage-ই।

### ২১.৫ তিনটি Q&A

**প্র১. 2026-এ প্রমাণ-সহ কোড কি আর সম্ভব?**
উত্তর: Context-এ current-model formal-proof তথ্য নেই; তাই বর্তমান model-এর তথ্য পাওয়া যায়নি। আমরা নিজেরা ছোট pilot-এ মাপব, দাবি করব না।

**প্র২. Benchmark saturated হলে proof কেন গুরুত্বপূর্ণ?**
উত্তর: Verified 97.0% (I) পেরিয়ে গেছে ও test ত্রুটিপূর্ণ হিসেবে অভিযুক্ত (S); তাই test-pass আর আলাদা করে না। Proof শুধু নির্বাচিত property-র জন্য, তবে test-এর বাইরের একটি স্বতন্ত্র সংকেত।

**প্র৩. Agent যদি verifier-ই ঠকায়?**
উত্তর: METR ≥ 16% cheat (I, আগের প্রজন্ম) ও Opus 5.5 card-এর "hidden tests" আচরণ (V) থেকে ধরে নেওয়া নিরাপদ নয়। তাই checker-কে agent-এর নাগালের বাইরে, নির্দিষ্ট version-এ, আলাদা environment-এ চালাতে হবে (CG11, CG12); proof-এর spec ও `assume`/`verify false` ধরনের বাইপাস লগ-অডিট করতে হবে (আমার পরামর্শ)।
