# Paper Analysis 03 (APR): RePaCA — Reasoning LLMs for Static Automated Patch Correctness Assessment

> **Sub-domain:** Automated Program Repair (Paper 03)
> **Analysis করেছে:** SPL3 — AI Coding Agent Reliability and Assurance
> **Paper file:** `Automated Program Repair/Leveraging reasoning large language models for static automated.pdf`
> **আগে পড়ো:** Sub-domain 1, Paper 01 (SWE-bench) — patch/diff, unit test, F2P/P2P, LoRA, fine-tuning loss, greedy decoding সেখানে ব্যাখ্যা করা আছে। Sub-domain 1, Paper 03 (AutoCodeRover) — "78টা plausible patch-এর মাত্র 51টা (65.4%) সঠিক" প্রমাণটা এই paper-এর মূল motivation-এর সাথে মেলে। Sub-domain 1 Summary — common gap **CG1 (overfitting detection)** আর প্রস্তাবিত "Assurance Layer"।

---

## ০. Paper-এর পরিচয় (Bibliographic Info)

| বিষয় | তথ্য |
|---|---|
| **Title** | RePaCA: Leveraging reasoning large language models for static automated patch correctness assessment |
| **Authors** | Marcos Fuster-Pena, David de-Fitero-Dominguez, Antonio Garcia-Cabot (corresponding author), Eva Garcia-Lopez |
| **Institution** | Departamento de Ciencias de la Computación, Universidad de Alcalá, Madrid, Spain (INTELIA research lab) |
| **Venue** | *Neurocomputing*, Volume 701 (2026), Article 134583 — Elsevier-এর journal (সাধারণত Q1 হিসেবে পরিচিত; supervisor-কে বলার আগে SJR/JCR-এ যাচাই করো) |
| **DOI** | 10.1016/j.neucom.2026.134583 |
| **Timeline** | Received 13 Feb 2026 → Revised 1 Jul 2026 → Accepted 23 Jul 2026 → Online 24 Jul 2026 |
| **License** | Open access, CC BY-NC-ND 4.0 |
| **Paper type** | **Technique paper** — নতুন একটা APCA technique (RePaCA) + empirical evaluation (৩টা setting + ২টা ablation + qualitative example) |
| **Base model** | Qwen2.5-Coder-3B (Instruct), শুধু GRPO (Reinforcement Learning) দিয়ে fine-tune — কোনো SFT নেই |
| **Artifacts** | Code-এর কোনো public link paper-এ নেই; "Data will be made available on request"। Dataset গুলো APPT-এর GitHub (iSEngLab/APPT) ও INVALIDATOR-এর GitHub (thanhlecongg/Invalidator) থেকে নেওয়া |
| **Interesting fact** | প্রথম author paper লেখার সময় **B.Sc. শেষ করছিলেন** (author bio অনুযায়ী 2026-এ graduate) — অর্থাৎ undergraduate-level কাজ থেকেও journal publication সম্ভব। SPL3-এর জন্য এটা ভালো অনুপ্রেরণা। |
| **আমাদের domain-এ গুরুত্ব** | ⭐⭐⭐⭐⭐ — এটা সরাসরি **CG1 (plausible patch-এর overfitting detection)**-এর একটা technique। আমাদের প্রস্তাবিত Assurance Layer-এর প্রথম component ("test pass করা patch আসলে সঠিক কিনা") ঠিক এই কাজটাই করে — তাও কোনো test না চালিয়ে, শুধু code দেখে। |

---

## ১. এক লাইনে Paper (TL;DR)

**RePaCA একটা ছোট (3B parameter) code LLM-কে buggy code আর patched code দেখিয়ে আগে `<think>` block-এ ধাপে ধাপে চিন্তা (Chain of Thought) করতে বাধ্য করে, তারপর `<answer>` block-এ "correct" বা "overfitting" বলায়; আর এই ক্ষমতা বাড়াতে model-কে GRPO নামের Reinforcement Learning algorithm দিয়ে train করা হয়, যেখানে সঠিক format-এর জন্য ও সঠিক label-এর জন্য reward দেওয়া হয় (overfitting সঠিকভাবে ধরলে দ্বিগুণ reward)। Defects4J-ভিত্তিক standard dataset-এ এটা 83.1% accuracy ও 84.8% F1 পেয়ে আগের সব static APCA technique-কে ছাড়িয়ে গেছে।**

### Supervisor-কে ৩০ সেকেন্ডে কীভাবে বলবো
> "Sir, APR tool বা AI coding agent অনেক সময় এমন patch দেয় যেটা test pass করে কিন্তু আসলে bug ঠিক করে না — একে overfitting patch বলে। আমাদের আগের sub-domain-এ AutoCodeRover-এ দেখেছি test-pass করা patch-এর মাত্র 65.4% আসলে সঠিক। এই সমস্যা automatic ধরার field-কে বলে APCA। RePaCA হলো একটা static APCA — test চালায় না, শুধু buggy আর fixed code পাশাপাশি দেখে। তারা Qwen2.5-Coder-3B নামের ছোট model নিয়েছে, prompt-এ বলেছে আগে `<think>` এর ভেতরে যুক্তি দাও, তারপর `<answer>`-এ correct/overfitting বলো। তারপর DeepSeek-R1-এর মতো GRPO দিয়ে RL training করেছে: একই patch-এর জন্য 8টা উত্তর তৈরি করে, যেগুলো সঠিক label দেয় সেগুলোকে বেশি reward দেয়। 1,183টা Defects4J patch-এ 5-fold cross-validation-এ 83.1% accuracy, 84.8% F1 — আগের সেরা APPT-এর চেয়ে ভালো, আর statistical test-এ significant। অন্য dataset-এ (domain shift) APPT-এর AUC 55.4% মানে প্রায় random, RePaCA-র 72.3%। সাথে প্রতিটা সিদ্ধান্তের একটা human-readable ব্যাখ্যা দেয়। তবে এটা শুধু Java, ছোট single-method patch-এ test করা — SWE-bench-এর মতো Python, multi-file agent patch-এ কাজ করবে কিনা সেটাই আমাদের research প্রশ্ন।"

---

## ২. Background — এই paper বুঝতে যা আগে জানা দরকার

### ২.১ আগের paper থেকে যা লাগবে (পুনরায় ব্যাখ্যা নয়)

| Concept | কোথায় ব্যাখ্যা আছে | এই paper-এ কীভাবে লাগে |
|---|---|---|
| Patch / diff | Sub-domain 1, Paper 01, Section ২.২ | RePaCA-র input হলো buggy code + patched code (diff আকারে নয়, দুটো snippet) |
| Unit test, test oracle | Sub-domain 1, Paper 01, Section ২.৩ | Overfitting হয় কারণ test oracle দুর্বল |
| F2P / P2P test | Sub-domain 1, Paper 01, Section ২.৫ | Plausible patch = সব test pass করা patch |
| Automated Program Repair (প্রাথমিক ধারণা) | Sub-domain 1, Paper 01, Section ২.১১ | নিচে ২.২-এ বিস্তারিত |
| Patch overfitting-এর বাস্তব প্রমাণ | Sub-domain 1, Paper 03 (AutoCodeRover) ও Summary Section ৩.১ | 51/78 = 65.4% — motivation |
| Fine-tuning, LoRA, cross-entropy loss | Sub-domain 1, Paper 01, Section ২.৮, ৬.৭, ৬.৮ | এখানে SFT-এর বদলে RL; LoRA paper-এ উল্লেখ নেই (২.১৫ দেখো) |
| Greedy decoding, Pass@k | Sub-domain 1, Paper 01, Section ২.১০ | এখানে temperature 0.6 দিয়ে sampling |
| Ablation study | Sub-domain 1, Paper 01, Section ৫.৪ | Base model ও temperature ablation |
| Data contamination | Sub-domain 1, Paper 01, Section ২.৯ | Defects4J পুরনো ও public — contamination ঝুঁকি (Section ১২) |

### ২.২ Automated Program Repair (APR) — Generate-and-Validate pipeline
APR মানে মানুষের সাহায্য ছাড়া bug ঠিক করা। Paper অনুযায়ী আধুনিক APR tool সাধারণত deep learning দিয়ে bug-fix pattern শেখে এবং repair-কে একটা **translation problem** হিসেবে দেখে (buggy code → fixed code, যেমন এক ভাষা থেকে আরেক ভাষায় অনুবাদ)। সাধারণ pipeline:

1. **Fault localization:** সন্দেহজনক জায়গা (buggy method/function) খোঁজা।
2. **Patch generation:** code পরিবর্তন করে এক বা একাধিক candidate patch তৈরি।
3. **Patch validation:** test চালিয়ে যাচাই। যে candidate সব test pass করে তাকে বলে **plausible patch**।

SWE-agent, AutoCodeRover, Agentless (Sub-domain 1) আসলে এই pipeline-এরই LLM-agent version।

### ২.৩ Plausible, Correct ও Overfitting Patch

| Patch type | সব test pass করে? | Bug আসলে ঠিক হয়? | উদাহরণ |
|---|---|---|---|
| **Plausible** | হ্যাঁ | জানা নেই | Test suite-এর চোখে "সফল" |
| **Correct** | হ্যাঁ | হ্যাঁ — সাধারণভাবে (সব input-এ) | Developer-এর fix-এর সমতুল্য |
| **Overfitting** | হ্যাঁ | না — শুধু test-এর নির্দিষ্ট input-এ কাজ করে | Bug-ওয়ালা functionality-টাই মুছে দেওয়া; failing test-এর input-এর জন্য বিশেষ `if` লাগানো |

Paper-এর উদাহরণ: কোনো functionality bug তৈরি করছে দেখে tool যদি সেই functionality-টাই বাদ দিয়ে দেয়, তাহলে test হয়তো pass করবে, কিন্তু program-এর সামগ্রিক আচরণ নষ্ট হবে। নামটা machine learning-এর "overfitting" থেকে এসেছে — model যেমন training data মুখস্থ করে, patch-ও তেমন test case "মুখস্থ" করে।

### ২.৪ APCA — Automated Patch Correctness Assessment
Plausible patch-এর মধ্যে কোনগুলো overfitting তা automatic ভাবে চিহ্নিত করার field। Paper অনুযায়ী APCA হলো patch generation-এর পরে একটা **filtering step**, যার দুটো লাভ:
- মানুষকে কম plausible patch হাতে যাচাই করতে হয়;
- "test pass করে কিন্তু bug ঠিক করে না" এমন patch গ্রহণ করার ঝুঁকি কমে।

এটা একটা **binary classification** সমস্যা: input = একটা patch, output = Correct / Overfitting।

### ২.৫ Static বনাম Dynamic APCA

| দিক | Dynamic APCA | Static APCA |
|---|---|---|
| কী ব্যবহার করে | Patch execute করে runtime তথ্য (execution trace, test result); অনেক সময় নতুন test generate করে (যেমন EvoSuite, Randoop) | শুধু buggy code ও fixed code — code চালানো হয় না |
| সুবিধা | সাধারণত বেশি তথ্য, তাই বেশি নির্ভুল হতে পারে | সরল, দ্রুত, build/run environment লাগে না |
| অসুবিধা | জটিল ও সময়সাপেক্ষ — patch build ও run করতে হয় | তথ্য কম, তাই সাধারণত কম accurate |
| RePaCA কোন দিকে | — | **Static** |

Paper-এর যুক্তি: execution তথ্য পাওয়া সাধারণত patch code পাওয়ার চেয়ে অনেক বেশি ব্যয়বহুল, তাই তারা শুধু static setting-এ কাজ করেছে।

**আমার পর্যবেক্ষণ:** SWE-bench-style agent setting-এ এই হিসাবটা একটু আলাদা — সেখানে Docker environment আর test ইতিমধ্যে আছে (Sub-domain 1, Paper 01 দেখো), তাই dynamic তথ্য তুলনামূলক সস্তা। তবুও static check সবচেয়ে সস্তা প্রথম স্তর হিসেবে কাজে লাগে।

### ২.৬ আগের APCA Technique-গুলোর পরিবার (paper যেভাবে বর্ণনা করেছে)

Paper নিজেই এগুলোকে "কোন ধরনের evidence ব্যবহার করে" সেই অনুযায়ী ভাগ করেছে:

| Technique | Evidence-এর ধরন | কীভাবে কাজ করে (paper-এর বর্ণনা) |
|---|---|---|
| **ODS** [12] | Statically extracted code features | AST স্তরে hand-crafted feature বের করে traditional supervised learning classifier দিয়ে overfitting pattern চেনে |
| **CACHE** [9] | Learned embedding of code change + context | AST path ব্যবহার করে code change ও তার আশেপাশের context-এর context-sensitive embedding শেখে |
| **Quatrain** [13] | Bug report ও patch description-এর সম্পর্ক | Question–Answer problem: bug report = প্রশ্ন, patch-এর বর্ণনা = উত্তর; NLP দিয়ে দুটোর semantic সম্পর্ক মাপে |
| **INVALIDATOR** [10] | Program invariant + syntactic encoder | Test থেকে inferred program invariant (semantic) + CodeBERT দিয়ে syntactic বিশ্লেষণ |
| **APPT** [11] | Fine-tuned pre-trained LM (token sequence) | BERT fine-tune করে code-কে token sequence হিসেবে দেখে, তার উপর LSTM layer, শেষে classification layer। RePaCA-র আগে static APCA-তে সেরা |
| **LLM4PatchCorrect** [14] | In-context learning with retrieved labeled patches | Fine-tuning ছাড়া; bug তথ্যের সাথে semantically similar labeled patch যোগ করে prompt বানায় |

**Paper-এর মূল সমালোচনা:** এদের সবাই patch classify করে **syntactic/structural regularity আর learned correlation মিলিয়ে** — কেউ explicitly যুক্তি দেয় না যে "এই পরিবর্তন bug-এর **root cause** ঠিক করে কিনা"। RePaCA এই শূন্যস্থান পূরণ করতে চায়।

**আমার পর্যবেক্ষণ:** INVALIDATOR-এর invariant test execution থেকে inferred হয়, তাই এটা পুরোপুরি "static" নয় — এটা একটা hybrid। RePaCA-কে INVALIDATOR-এর সাথে তুলনা করার সময় এটা মনে রাখতে হবে (Section ৮.৩)।

### ২.৭ Abstract Syntax Tree (AST)
Code-এর grammar-এর একটা গাছ-আকৃতির (hierarchical) প্রতিরূপ — যেমন `if` node-এর নিচে condition আর body। ODS ও CACHE এই গাছ থেকে feature/path নেয়। RePaCA AST ব্যবহার করে না — raw code text দেয়।

### ২.৮ BERT, CodeBERT, LSTM, Embedding (baseline বুঝতে)
- **Embedding:** code বা text-কে একটা সংখ্যার vector-এ রূপান্তর, যাতে অনুরূপ জিনিস কাছাকাছি থাকে।
- **BERT / CodeBERT:** Transformer encoder model, বিশাল text/code দিয়ে pre-trained; classification কাজে fine-tune করা হয়। এরা text **generate** করে না, শুধু represent করে।
- **LSTM:** একটা recurrent neural network যা sequence-এর ক্রম মনে রাখে। APPT BERT-এর output-এর উপর LSTM বসিয়েছে।

এগুলো "এক ধাপে" সিদ্ধান্ত নেয় (single-pass) — কোনো মধ্যবর্তী যুক্তি লেখে না।

### ২.৯ LLM, Instruct Model, Prompt, One-shot Prompting
- **Instruct model:** base LLM-কে instruction মেনে চলার জন্য বাড়তি train করা version — chat message হিসেবে প্রশ্ন নেয়। RePaCA-র সব candidate model instruct version।
- **Prompt:** model-কে দেওয়া পুরো input text (instruction + data)।
- **One-shot prompting:** prompt-এ একটা সমাধান-করা উদাহরণ দেওয়া, যাতে model বোঝে কোন format-এ, কোন ধাপে উত্তর দিতে হবে। (Zero-shot = কোনো উদাহরণ নেই; few-shot = কয়েকটা।)

### ২.১০ Reasoning LLM, Chain of Thought (CoT) ও Test-Time Compute
- **Chain of Thought (CoT):** উত্তর দেওয়ার আগে model ধাপে ধাপে মধ্যবর্তী যুক্তি লেখে — paper-এর ভাষায় একটা "internal step-by-step monologue" যা মানুষের introspective চিন্তার অনুকরণ। গবেষণায় দেখা গেছে এতে জটিল প্রশ্নে উত্তরের মান বাড়ে।
- **Test-Time Compute (TTC):** inference-এর সময় বেশি token/চিন্তা খরচ করে ভালো উত্তর পাওয়া (training-এ নয়)।
- **Reasoning LLM:** যে model CoT-কে নিজের আচরণের অংশ বানিয়ে ফেলেছে, যেমন **DeepSeek-R1**। এর output format: `<think> ... </think>` (যুক্তি) তারপর `<answer> ... </answer>` (চূড়ান্ত উত্তর)। RePaCA হুবহু এই format ব্যবহার করে।
- **DeepSeek-R1-Zero:** কোনো supervised fine-tuning ছাড়া **শুধু RL** দিয়ে reasoning শেখানো model। RePaCA-র training method এর উপর ভিত্তি করে।

**গুরুত্বপূর্ণ সতর্কতা (paper নিজেই বলেছে):** `<think>`-এর লেখা যুক্তি model-এর আসল internal decision process-এর **বিশ্বস্ত (faithful) ব্যাখ্যা নয়** — এটা শুধু developer-কে prediction বিশ্লেষণে সাহায্য করে।

### ২.১১ Supervised Fine-Tuning (SFT) বনাম Reinforcement Learning (RL)

| দিক | SFT | RL (এখানে GRPO) |
|---|---|---|
| কী লাগে | প্রতিটা input-এর জন্য একটা "সঠিক output text" (target) | শুধু একটা **reward function** — output কতটা ভালো তার নম্বর |
| Model কী শেখে | Target text হুবহু নকল (imitate) করতে | যে output বেশি reward পায় তার সম্ভাবনা বাড়াতে |
| Loss | Cross-entropy (Sub-domain 1, Paper 01, Section ৬.৮) | Policy-gradient objective (Section ৬.৬) |
| APCA-তে সমস্যা/সুবিধা | Reasoning-এর জন্য মানুষের লেখা ব্যাখ্যা লাগতো — dataset-এ নেই | শুধু label (correct/overfitting) থাকলেই চলে; **একই patch-এর জন্য অনেক রকম বৈধ যুক্তি থাকতে পারে**, RL সেগুলোকে স্বাধীনতা দেয় |

RL-এর পরিভাষা:
- **Policy ($\pi_\theta$):** model নিজেই — prompt দেখে output-এর probability distribution।
- **Reward ($r$):** একটা output-এর জন্য পাওয়া নম্বর।
- **Advantage ($A$):** "এই output গড়ের চেয়ে কতটা ভালো" — positive হলে সেই output-এর সম্ভাবনা বাড়ানো হয়, negative হলে কমানো হয়।

### ২.১২ PPO থেকে GRPO
- **PPO (Proximal Policy Optimization):** জনপ্রিয় policy-gradient algorithm। Advantage হিসাব করতে একটা আলাদা **value model (critic)** লাগে, যেটা প্রায় policy-র সমান বড় — অর্থাৎ memory দ্বিগুণ। Update খুব বড় না হয় সেজন্য ratio-কে **clip** করে।
- **GRPO (Group Relative Policy Optimization),** DeepSeekMath paper-এ প্রস্তাবিত: value model বাদ। একই prompt-এর জন্য $G$টা output sample করে, তাদের reward-এর **group mean ও standard deviation** দিয়ে normalize করে advantage বের করে। অর্থাৎ "নিজের ভাইবোনদের তুলনায় কতটা ভালো" — এটাই "group relative"। RePaCA-তে $G = 8$।

### ২.১৩ Reference Model ও KL Penalty
Training-এর শুরুর model-এর একটা **frozen (অপরিবর্তিত) কপি** রাখা হয় — reference model। Policy যদি reference থেকে অনেক দূরে সরে যায় তাহলে **KL divergence** penalty দেওয়া হয়। এতে model "collapse" করে না (যেমন অর্থহীন কিন্তু reward পাওয়া text লেখা, বা ভাষা দক্ষতা হারানো)। Paper-এর Fig. 2-এ এটা দেখানো আছে।

### ২.১৪ Reward Design ও Reward Hacking
RL-এ model ঠিক সেটাই শেখে যার জন্য reward দেওয়া হয় — যা চাওয়া হয়েছে তা নয়। তাই reward ভুলভাবে বানালে model shortcut খোঁজে (**reward hacking**)। যেমন: শুধু format-এর জন্য reward দিলে model ফাঁকা `<think></think>` লিখতে পারে। RePaCA দুটো reward ব্যবহার করে — format ও accuracy (Section ৫.৪)। **গুরুত্বপূর্ণ:** কোনো reward `<think>`-এর যুক্তির **মান** যাচাই করে না — authors নিজেরাই future work-এ এটা স্বীকার করেছেন।

### ২.১৫ LoRA ও Unsloth (এই paper-এ কী জানা আছে)
LoRA Sub-domain 1, Paper 01-এ ব্যাখ্যা করা। RePaCA paper **LoRA ব্যবহার করেছে কিনা বলেনি**। শুধু বলেছে training-এ **TRL library** (GRPO implementation) আর **Unsloth** (training optimization, কম VRAM ও দ্রুত training-এর library) ব্যবহার করা হয়েছে। Unsloth সাধারণত LoRA/QLoRA-ভিত্তিক training-এর জন্য পরিচিত, তাই LoRA ব্যবহারের সম্ভাবনা আছে — কিন্তু **এটা অনুমান, paper-এ লেখা নেই** (Section ১২-এ reproducibility সমস্যা হিসেবে উল্লেখ করেছি)।

### ২.১৬ Temperature Sampling
Output-এর প্রতিটা token বাছাইয়ের সময় probability distribution কতটা "সমান করা" হবে তা temperature $T$ ঠিক করে:
- $T = 0$ → greedy (সবসময় একই উত্তর, deterministic)।
- $T$ বড় → বেশি বৈচিত্র্য, কিন্তু বেশি এলোমেলো/hallucination।
RePaCA $T = 0.6$ ব্যবহার করে (ablation Section ৮.৭)।

### ২.১৭ Dataset-এর উৎসগুলো
- **Defects4J (v1.2):** আসল Java bug-এর বহুল ব্যবহৃত benchmark (Commons Math, Commons Lang, Closure ইত্যাদি project)। বেশিরভাগ Java APR tool এর উপর evaluate হয়।
- **Tian et al. (1,000 patch) ও Wang et al. (902 patch):** আগের দুটো APCA study, যারা Defects4J-এর উপর বিভিন্ন APR tool-এর patch সংগ্রহ করে হাতে label করেছে।
- **ManySStuBs4J:** 1,000-এর বেশি open-source Java project থেকে "single-statement bug" ও তাদের developer-fix — এখানে **correct patch**-এর উৎস।
- **RepairThemAll:** অনেক Java APR tool-কে অনেক bug benchmark-এ চালানোর framework — এখানে **overfitting patch**-এর উৎস।
- CACHE paper এই dataset গুলো তৈরি করেছে; APPT এগুলো ব্যবহার করেছে; RePaCA APPT-এর GitHub থেকে নিয়েছে।

### ২.১৮ k-Fold Cross-Validation
Dataset-কে $k$টা সমান ভাগে ভাগ করে, প্রতিবার একটা ভাগ test, বাকি $k-1$টা training — মোট $k$ বার; তারপর ফল গড় বা একত্রিত করা হয়। ছোট dataset-এ একটা "ভাগ্যবান" split-এর উপর নির্ভরতা কমায়। এখানে $k = 5$, অর্থাৎ প্রতি fold-এ প্রায় 946টা training ও 237টা test patch (আমার হিসাব: $1183 \times 0.8 \approx 946$)।

### ২.১৯ Confusion Matrix ও Classification Metric
Paper-এর Table 2 অনুযায়ী **Overfitting = Positive, Correct = Negative**। সব সূত্র Section ৬.৮-এ।

| | Actual Overfitting (Positive) | Actual Correct (Negative) |
|---|---|---|
| **Predicted Overfitting** | True Positive (TP) | False Positive (FP) — সঠিক patch-কে ভুল করে বাতিল |
| **Predicted Correct** | False Negative (FN) — overfitting patch গ্রহণ হয়ে যায় | True Negative (TN) |

### ২.২০ Statistical Test: McNemar ও Bootstrap
- **McNemar's test:** একই instance-এর উপর দুটো classifier-এর paired তুলনা। শুধু সেই instance গুলো দেখে যেখানে দুটো classifier ভিন্ন উত্তর দিয়েছে।
- **Bootstrap confidence interval:** test set থেকে replacement সহ বারবার (এখানে 10,000 বার) নমুনা নিয়ে metric হিসাব করে তার বিস্তার থেকে 95% CI বের করা। CI যদি 0 ধারণ না করে তাহলে পার্থক্য significant।

### ২.২১ Domain Shift / Out-of-Distribution (OOD)
Training data আর test data যদি ভিন্ন উৎস/বৈশিষ্ট্যের হয় তাহলে model-এর performance পড়ে যায়। এখানে: small dataset = APR tool-এর patch; large dataset = GitHub developer-fix (correct) + RepairThemAll (overfitting)।

**আমার পর্যবেক্ষণ:** আমাদের জন্য এটা সবচেয়ে গুরুত্বপূর্ণ concept, কারণ Defects4J (Java, APR tool) → SWE-bench agent patch (Python, LLM agent) একটা অনেক বড় domain shift।

### ২.২২ Hallucination
Model যখন input-এ নেই এমন তথ্য বানিয়ে বলে — যেমন RePaCA-র Code 1 example-এ একটা পুরনো variable-কে "নতুন variable" বলা (Section ৮.৫)।

---

## ৩. Problem Statement — কী সমস্যা ছিল?

### ৩.১ মূল সমস্যা
1. **Test pass ≠ bug fixed:** APR tool অনেক plausible patch দেয় যেগুলো overfitting। এগুলো চিহ্নিত করা APR-এর সবচেয়ে গুরুত্বপূর্ণ চ্যালেঞ্জের একটা।
2. **Dynamic APCA ব্যয়বহুল:** patch execute করতে হয়, test generate করতে হয় — জটিল ও সময়সাপেক্ষ।
3. **Static APCA-র তিনটা দুর্বলতা (abstract-এ বলা):**
   - **Reliability:** accuracy তুলনামূলক কম;
   - **Flexibility:** নতুন ধরনের/উৎসের patch-এ খারাপ (domain shift);
   - **Transparency:** কেন একটা patch-কে overfitting বলা হলো তার কোনো ব্যাখ্যা নেই।
4. **Superficial analysis:** আগের সব static technique syntactic/structural pattern মেলায়, root cause নিয়ে যুক্তি দেয় না।
5. **In-context learning-এর অবাস্তব অনুমান:** LLM4PatchCorrect-এর মতো technique ধরে নেয় যে একই bug-এর জন্য হাতে-যাচাই করা অনুরূপ labeled patch আগে থেকে আছে — নতুন bug-এ এটা বাস্তবসম্মত নয়।

### ৩.২ Authors-এর Hypothesis
> বেশিরভাগ static APCA tool জটিল overfitting patch-এর root cause বুঝতে পারে না; LLM-এর deep reasoning ক্ষমতা ব্যবহার করলে — অর্থাৎ code-এর পার্থক্য বিশ্লেষণ, edge case বিবেচনা, fix সাধারণভাবে প্রযোজ্য নাকি শুধু নির্দিষ্ট input-এ কাজ করে তা যাচাই — APCA-র কার্যকারিতা বাড়বে।

### ৩.৩ কেন এটা গুরুত্বপূর্ণ (আমাদের দৃষ্টিকোণ)
Sub-domain 1-এ দেখেছি AutoCodeRover-এর test-pass করা patch-এর প্রায় ৩টার ১টা ভুল, আর SWE-bench-এ প্রায় 60% task-এ মাত্র ১টা F2P test। অর্থাৎ coding agent-এর জন্যও একই overfitting সমস্যা আছে। একটা সস্তা, ব্যাখ্যাযোগ্য static checker থাকলে agent-এর output-এর উপর প্রথম স্তরের assurance দেওয়া যায়।

---

## ৪. Goal ও Research Questions

**Goal:** একটা reasoning-ভিত্তিক static APCA technique তৈরি করা যা (ক) বেশি accurate, (খ) domain shift-এ robust, (গ) প্রতিটা সিদ্ধান্তের human-readable ব্যাখ্যা দেয় — এবং দেখা যে GRPO-trained reasoning LLM static APCA উন্নত করতে পারে কিনা।

Paper explicit RQ লেখেনি; Section 4-এর experiment অনুযায়ী implicit RQ:
- **RQ1 (Standard evaluation):** Small dataset-এ 5-fold CV-তে RePaCA কি ODS, Quatrain, CACHE, APPT-কে ছাড়ায়? পার্থক্য কি statistically significant?
- **RQ2 (INVALIDATOR তুলনা):** INVALIDATOR-এর নিজস্ব dataset ও split-এ RePaCA কেমন করে?
- **RQ3 (Cross-dataset / domain shift):** Small-এ train করে Large-এ test করলে RePaCA ও APPT কেমন করে?
- **RQ4 (Qualitative):** Model-এর `<think>` যুক্তি কি অর্থবহ ও সঠিক?
- **RQ5 (Ablation):** Base model নির্বাচন ও sampling temperature performance-এ কতটা প্রভাব ফেলে?

---

## ৫. Methodology — কীভাবে কাজটা করা হয়েছে

### ৫.১ সামগ্রিক Pipeline (Fig. 1)

| অংশ | উপাদান | বিবরণ |
|---|---|---|
| Prompt → Instructions | Task description | APCA-র উদ্দেশ্য ও analysis-এর নিয়ম |
| Prompt → Instructions | Format specification | `<think>` ও `<answer>` tag বাধ্যতামূলক |
| Prompt → Instructions | One-shot example | একটা সমাধান-করা assessment-এর নমুনা |
| Prompt → Target snippets | Buggy code + Patched code | যে patch-টা বিচার করতে হবে |
| Model | RePaCA | Qwen2.5-Coder-3B, GRPO fine-tuned |
| Output → Reasoning block | `<think> ... </think>` | ধাপে ধাপে বিশ্লেষণ; code-এর পার্থক্য; patch root cause ঠিক করে কিনা; fix সাধারণ নাকি নির্দিষ্ট input-এর জন্য |
| Output → Final answer | `<answer> ... </answer>` | Correct / Overfitting |

### ৫.২ Prompt Design (Section 3.1)
Prompt-এর ক্রম:
1. **সমস্যার সংক্ষিপ্ত ব্যাখ্যা:** দুটো snippet আছে (buggy version ও proposed fix); লক্ষ্য হলো চিহ্নিত করা পরিবর্তন আসলে মূল সমস্যা সমাধান করে, নাকি শুধু নির্দিষ্ট test pass করার জন্য আচরণ বদলায় (= overfitting)।
2. **Analysis requirements:** model কীভাবে বিশ্লেষণ করবে তার নির্দেশনা — গভীর ও structured reasoning উৎসাহিত করতে।
3. **Output format specification:** DeepSeek-R1-এর মতো — `<think>` এর ভেতরে internal monologue, `<answer>` এর ভেতরে চূড়ান্ত সিদ্ধান্ত।
4. **One-shot example:** একই format-এ একটা সমাধান-করা উদাহরণ — উত্তরের consistency বাড়ায়।
5. **Sample data:** buggy code ও fixed code।
6. **শেষ নির্দেশ:** model-কে reasoning শুরু করতে বলা।

Paper জোর দিয়েছে যে **ছোট model-এ prompt-এর explicit guidance বেশি গুরুত্বপূর্ণ**।

**Malformed output:** Small dataset-এ test-এর সময় প্রায় **1%** prompt-এর উত্তর ভুল format-এ এসেছে বা উত্তরই আসেনি। প্রস্তাবিত সমাধান: re-sampling বা সাধারণ post-processing। (Section 4.1-এ সঠিক সংখ্যা: 1,183-এর মধ্যে **20টা = 1.7%** unparseable — Section ৮.২ দেখো।)

Paper হুবহু prompt text দেয়নি। নিচে Fig. 1-এর ভিত্তিতে **আমার পুনর্গঠন (illustrative, paper-এর আসল text নয়)**:

```text
[Task] You are given two Java code snippets: the BUGGY version and a PATCHED
version produced by an automated repair tool. Decide whether the patch truly
fixes the root cause of the bug (CORRECT) or only changes behaviour so that
specific tests pass (OVERFITTING).
[Analysis requirements] Compare both versions step by step; identify exactly
what changed; reason about the root cause; check edge cases; judge whether the
fix is general or tied to specific inputs.
[Format] Reason inside <think> ... </think>, then give the label inside
<answer> ... </answer>.
[Example] <one solved example in the same format>
[Buggy code] ...
[Patched code] ...
Start your reasoning.
```

### ৫.৩ Training: RL-only GRPO (Section 3.2.1, Fig. 2)
**মূল decision:** কোনো prior SFT ছাড়াই base instruct model-কে সরাসরি RL দিয়ে optimize করা (DeepSeek-R1-Zero-এর মতো) — "RL-only adaptation এই domain-এ কাজ করে কিনা" সেটা পরীক্ষা করাও একটা উদ্দেশ্য।

Fig. 2 অনুযায়ী প্রতিটা training step:
1. Input: Prompt + Buggy code + Patched code → RePaCA (policy)।
2. Policy একই input-এর জন্য **G = 8টা candidate output** তৈরি করে (Output 1 … Output 8), প্রতিটায় `<think>…</think><answer>…</answer>`।
3. প্রতিটা output-কে দুটো reward function score দেয়: **Format reward** ও **Accuracy reward**।
4. দুটো যোগ করে প্রতিটা output-এর মোট reward $r_1, \ldots, r_8$ (Fig. 2-এর নমুনা: $r_1 = 2.0$, $r_8 = 1.0$)।
5. **Group computation:** group-এর mean ও std দিয়ে normalize করে advantage $A_1, \ldots, A_8$ (Fig. 2-এর নমুনা: $A_1 = 0.7$, $A_8 = -0.3$)।
6. Frozen **reference model** (শুরুর model-এর কপি) থেকে KL penalty হিসাব।
7. Advantage ও KL দিয়ে policy-র gradient (Fig. 2-এ $
abla	heta$) হিসাব করে update।

(Fig. 2-এর $r$ ও $A$ মানগুলো ছবির নমুনা — প্রকৃত training-এর সংখ্যা নয়।)

### ৫.৪ Reward Functions (Section 3.2.2, Table 1)

**(ক) Format reward — মান 0.0 থেকে 1.0, তিন অংশ:**

| শর্ত | যোগ হয় |
|---|---|
| Output-এ `<think> ... </think>` আছে | +0.5 |
| Output-এ `<answer> ... </answer>` আছে | +0.25 |
| `<answer>`-এর ভেতরে নিচের keyword-এর অন্তত একটা আছে | +0.25 |

Keyword list: "overfitting", "fixed", "fix", "correct", "buggy", "incorrect", "wrong"। আগের কাজে (LLM4PatchCorrect) শুধু "correct" ও "wrong" ছিল; এখানে list বড় করা হয়েছে যাতে model নিজের ভাষায় রায় দিতে পারে — "fix"/"fixed" = correct-এর সমার্থক; "buggy"/"incorrect"/"overfitting" = overfitting-এর সমার্থক (paper অনুযায়ী)।

(Fig. 2-এ format reward-কে সংক্ষেপে "think → +0.5, answer+keyword → +0.5" দেখানো হয়েছে — text-এর 0.25 + 0.25-এর সাথে সামঞ্জস্যপূর্ণ।)

**(খ) Accuracy reward — মান 0.0 থেকে 2.0 (Table 1):**

| Model-এর উত্তর | আসল label | Reward |
|---|---|---|
| Overfitting | Correct | 0.0 |
| Correct | Overfitting | 0.0 |
| Correct | Correct | 1.0 |
| Overfitting | Overfitting | **2.0** |

**কেন asymmetric (অসম)?** Empirical পর্যবেক্ষণ: model-এর পক্ষে overfitting patch ধরা correct patch চেনার চেয়ে কঠিন। মানগুলো preliminary experiment থেকে: প্রথমে সমান reward, তারপর ধীরে ধীরে পার্থক্য বাড়িয়ে learning curve ও output correctness দেখা হয়েছে। Authors-এর দাবি: 2.0 "harder class"-এ উন্নতির জন্য যথেষ্ট প্রণোদনা দেয় **"bias তৈরি না করে"**, যা precision/recall-এর ভারসাম্যে দেখা যায়। (আমার বিশ্লেষণে এই দাবি পুরোপুরি টেকে না — Section ৬.৭ ও ১২.২ দেখো।)

### ৫.৫ Base Model নির্বাচন (Section 3.3.1 ও 4.5.1)
- Candidate: প্রায় 2B–3B parameter-এর lightweight instruct model — stable GRPO training ও practical deployment দুটোর জন্য।
- নির্বাচনের মাপকাঠি: raw accuracy নয়, **class-balanced metric (F1, AUC)** — কারণ APCA-তে overfitting নির্ভরযোগ্যভাবে ধরা দরকার precision খুব না কমিয়ে।
- চারটা candidate: Qwen2.5-3B (general), Qwen2.5-Coder-3B, Llama-3.2-3B, Gemma-2-2B।
- বিজয়ী: **Qwen2.5-Coder-3B** — GRPO-র **আগেই** সবচেয়ে বেশি F1 (38.4%) ও AUC (53.6%)। কারণ হিসেবে authors code-heavy pre-training উল্লেখ করেছেন।

### ৫.৬ Hyperparameters ও Implementation (Section 3.3.4)

| Parameter | মান | কারণ (paper অনুযায়ী) |
|---|---|---|
| GPU (training) | 1× NVIDIA H100 NVL | — |
| Inference hardware | Consumer GPU, মাত্র **8 GB VRAM**-এই চলে | 3B model |
| Library | TRL (GRPO), Unsloth (optimization), PyTorch | — |
| Epochs | **20** | Validation split-এ accuracy ও reward convergence দেখে; এর বেশিতে উন্নতি নেই, training-set overfitting-এর লক্ষণ। (APPT 50 epoch ব্যবহার করে) |
| Learning rate | **5e-5** | APPT-এর সমান; অন্যান্য GRPO study-তেও অনুরূপ |
| Batch size | **8** sample | VRAM ও সময় কমাতে |
| Gradient accumulation | **2** step | একই কারণে |
| Group size $G$ | **8** candidate per prompt | একই কারণে |
| Temperature | **0.6** | Ablation-এ সেরা (Section ৮.৭) |
| Max completion length | **2048** token | Reasoning-এর জন্য যথেষ্ট জায়গা |
| KL coefficient $\beta$, clip $\epsilon$, max prompt length, LoRA config, random seed | **Paper-এ উল্লেখ নেই** | — |

**আমার হিসাব:** প্রতি fold-এ প্রায় 946টা training patch × 20 epoch × 8 generation ≈ **1,51,000টা** (প্রায় 151K) completion generate করতে হয় — প্রতিটা 2048 token পর্যন্ত। 5টা fold মিলিয়ে প্রায় 7.6 লাখ completion। এজন্যই authors বলেছেন GRPO training ব্যয়বহুল। (TRL-এ batch size completion-এর হিসাবে নাকি prompt-এর হিসাবে — paper-এ পরিষ্কার নয়; উপরের হিসাব epoch-এর সংজ্ঞা থেকে।)

### ৫.৭ Inference ও Parsing
1. Prompt তৈরি (একই one-shot prompt) → model temperature 0.6-এ একটা output তৈরি করে।
2. `<answer>`-এর ভেতরের text থেকে label বের করা।
3. Format ভুল হলে (প্রায় 1–1.7%) → re-sampling বা post-processing প্রস্তাবিত।

Paper-এ parser-এর হুবহু নিয়ম নেই (যেমন "incorrect" শব্দে "correct" substring থাকলে কী হয়)।

### ৫.৮ Evaluation Protocol

| Experiment | Train | Test | তুলনা | Baseline-এর সংখ্যার উৎস |
|---|---|---|---|---|
| E1: Standard | Small (5-fold CV) | Small (5-fold CV) | ODS, Quatrain, CACHE, APPT | CACHE ও APPT — তাদের মূল paper; ODS ও Quatrain — LLM4PatchCorrect paper থেকে (সেখানে precision/recall নেই) |
| E1b: Paired significance | Small (একই 5-fold split) | Small | APPT (authors-এর নিজের reproduction) | APPT-এর official code + paper-এর সেরা hyperparameter |
| E2: INVALIDATOR | INVALIDATOR dataset, 746 patch | 139 patch | INVALIDATOR | INVALIDATOR-এর মূল paper |
| E3: Cross-dataset | Small (সম্পূর্ণ) | Large (49,694) | APPT (reproduction) | Authors-এর নিজের run |
| E4: Qualitative | — | ২টা example | — | — |
| E5: Ablation | Small | Small | ৪টা base model (GRPO-র আগে); ৭টা temperature | — |

**লক্ষ্য করো:** CACHE নিজে Large-এ train করে Small-এ test করেছিল; RePaCA ইচ্ছা করে উল্টো (Small → Large) করেছে — "high-quality curated data কম, অন্য domain-এ adapt করতে হবে" এমন বাস্তব পরিস্থিতি simulate করতে।

---

## ৬. Mathematical Formulation — সূত্র ও ব্যাখ্যা

Paper নিজে কোনো numbered equation দেয়নি — reward-গুলো text ও Table 1-এ, GRPO শুধু নামে। নিচের formalization আমি paper-এর বর্ণনা ও GRPO-র মূল paper (DeepSeekMath [17]) অনুযায়ী লিখেছি, যাতে supervisor-এর সামনে পরিষ্কার করে বলা যায়।

### ৬.১ APCA Task-এর Formal Definition
একটা patch instance:
$$
x = (c_b,\; c_f), \qquad y \in \{0, 1\}
$$
- $c_b$ = buggy code snippet, $c_f$ = fixed (patched) code snippet
- $y = 1$ মানে **Overfitting (Positive)**, $y = 0$ মানে **Correct (Negative)**

একটা static APCA classifier হলো একটা function:
$$
h : (c_b, c_f) \to \{0, 1\}
$$
**Static** মানে $h$-এর input-এ কোনো execution তথ্য (test result, trace) নেই। Dataset $\mathcal{D} = \{(x_i, y_i)\}_{i=1}^{N}$; লক্ষ্য হলো generalization error কমানো:
$$
\min_{h} \; \mathbb{E}_{(x,y)} \left[ \mathbb{1}\left[ h(x) \neq y \right] \right]
$$

### ৬.২ RePaCA-র Output ও Prediction
Prompt $q = \text{Prompt}(c_b, c_f)$। Policy $\pi_\theta$ একটা output $o$ sample করে, যার দুটো অংশ:
$$
o = (z,\; a) \sim \pi_\theta(\cdot \mid q)
$$
- $z$ = `<think>`-এর ভেতরের reasoning (CoT)
- $a$ = `<answer>`-এর ভেতরের text

Prediction:
$$
\hat{y} = \text{parse}(a) \in \{0, 1, \text{None}\}
$$
এখানে None মানে unparseable (format ভুল) — paper-এর হিসাবে প্রায় 1–1.7% ক্ষেত্রে। (None label-টা আমার notation।)

### ৬.৩ Format Reward
$$
R_{\text{fmt}}(o) = 0.5 \cdot \mathbb{1}[\text{think tag present}] + 0.25 \cdot \mathbb{1}[\text{answer tag present}] + 0.25 \cdot \mathbb{1}[a \text{ contains a keyword}]
$$
তাই $R_{\text{fmt}} \in \{0, 0.25, 0.5, 0.75, 1.0\}$। Keyword set $K$ = {overfitting, fixed, fix, correct, buggy, incorrect, wrong}।

### ৬.৪ Accuracy Reward (Table 1)
$$
R_{\text{acc}}(\hat{y}, y) =
\begin{cases}
2.0, & \hat{y} = 1 \land y = 1 \quad (\text{overfitting সঠিকভাবে ধরা}) \\
1.0, & \hat{y} = 0 \land y = 0 \quad (\text{correct সঠিকভাবে চেনা}) \\
0.0, & \hat{y} \neq y
\end{cases}
$$

### ৬.৫ মোট Reward
Paper বলেছে "optimization is driven by both rewards" এবং "cumulative rewards" normalize করা হয় — অর্থাৎ যোগফল (TRL-এ একাধিক reward function-এর default আচরণও যোগ করা):
$$
r(o) = R_{\text{fmt}}(o) + R_{\text{acc}}(\hat{y}, y), \qquad r \in [0,\; 3]
$$

### ৬.৬ GRPO Objective (DeepSeekMath-এর standard রূপ)
একটা prompt $q$-এর জন্য পুরনো policy $\pi_{\theta_{\text{old}}}$ থেকে $G$টা output $\{o_1, \ldots, o_G\}$ sample করা হয়। প্রত্যেকটার reward $r_i$।

**Group-relative advantage** (একটা output-এর সব token একই advantage পায়):
$$
\hat{A}_{i} = \frac{r_i - \text{mean}(r_1, \ldots, r_G)}{\text{std}(r_1, \ldots, r_G)}
$$

**Token-level probability ratio:**
$$
\rho_{i,t}(\theta) = \frac{\pi_\theta(o_{i,t} \mid q,\, o_{i,<t})}{\pi_{\theta_{\text{old}}}(o_{i,t} \mid q,\, o_{i,<t})}
$$

**Objective (maximize করা হয়):**
$$
J(\theta) = \mathbb{E}\left[ \frac{1}{G} \sum_{i=1}^{G} \frac{1}{L_i} \sum_{t=1}^{L_i} \left( \min\left( \rho_{i,t}\, \hat{A}_i,\; \text{clip}(\rho_{i,t},\, 1-\epsilon,\, 1+\epsilon)\, \hat{A}_i \right) - \beta\, D_{\text{KL}}\left( \pi_\theta ,\, \pi_{\text{ref}} \right) \right) \right]
$$

**KL estimator (DeepSeekMath-এ ব্যবহৃত, সবসময় ধনাত্মক):**
$$
D_{\text{KL}}\left( \pi_\theta ,\, \pi_{\text{ref}} \right) = \frac{\pi_{\text{ref}}(o_{i,t} \mid \cdot)}{\pi_\theta(o_{i,t} \mid \cdot)} - \ln \frac{\pi_{\text{ref}}(o_{i,t} \mid \cdot)}{\pi_\theta(o_{i,t} \mid \cdot)} - 1
$$

| Symbol | মানে |
|---|---|
| $q$ | Prompt (instruction + one-shot example + buggy/fixed code) |
| $o_i$ | Group-এর $i$-তম output; $o_{i,t}$ তার $t$-তম token |
| $G$ | Group size — RePaCA-তে 8 |
| $L_i$ | Output $o_i$-এর token সংখ্যা (সর্বোচ্চ 2048) |
| $r_i$ | Output-এর মোট reward (format + accuracy) |
| $\hat{A}_i$ | Group-relative advantage — group-এর গড়ের তুলনায় কত std ভালো/খারাপ |
| $\rho_{i,t}$ | নতুন বনাম পুরনো policy-র probability ratio |
| $\epsilon$ | Clip range — update কত বড় হতে পারবে (paper-এ মান নেই) |
| $\beta$ | KL penalty-র ওজন (paper-এ মান নেই) |
| $\pi_{\text{ref}}$ | Frozen reference model (শুরুর Qwen2.5-Coder-3B) |

**Intuition:** যে output group-এর গড়ের চেয়ে বেশি reward পেয়েছে ($\hat{A}_i > 0$), তার প্রতিটা token-এর probability বাড়ানো হয়; কম পেলে কমানো হয়। Clip ও KL নিশ্চিত করে যে এক ধাপে model খুব বেশি না বদলায়। Value model নেই — "baseline" হলো group-এর গড় reward।

**Worked example ১ (আমার হিসাব, illustrative):** আসল label = Overfitting। 8টা output-এর সবগুলোর format নিখুঁত ($R_{\text{fmt}} = 1$)। 5টা বলেছে "overfitting" ($r = 1 + 2 = 3$), 3টা বলেছে "correct" ($r = 1 + 0 = 1$)।
- Mean $= (5 \times 3 + 3 \times 1)/8 = 18/8 = 2.25$
- Std (population) $= \sqrt{(5 \times 9 + 3 \times 1)/8 - 2.25^2} = \sqrt{6 - 5.0625} = \sqrt{0.9375} \approx 0.968$
- সঠিক output-এর advantage $= (3 - 2.25)/0.968 \approx +0.775$
- ভুল output-এর advantage $= (1 - 2.25)/0.968 \approx -1.291$

অর্থাৎ "overfitting" বলা 5টা reasoning path শক্তিশালী হবে, বাকি 3টা দুর্বল হবে। (Unbiased std, অর্থাৎ $G-1$ দিয়ে ভাগ করলে মান যথাক্রমে প্রায় +0.725 ও −1.208 — implementation-ভেদে সামান্য পার্থক্য।)

**Worked example ২ — label Correct হলে:** 4টা সঠিক ($r = 1 + 1 = 2$), 4টা ভুল ($r = 1 + 0 = 1$) → mean 1.5, std 0.5 → advantage +1.0 ও −1.0।

**Worked example ৩ — শিক্ষা-সংকেত হারিয়ে যাওয়া:** যদি 8টা output-এর সবগুলো একই উত্তর দেয় (সবগুলো সঠিক বা সবগুলো ভুল) এবং format-ও সমান হয়, তাহলে std = 0 → সব advantage 0 (practically ছোট $\varepsilon$ যোগ করা হয়) → **ওই prompt থেকে কিছুই শেখা হয় না**। খুব সহজ বা খুব কঠিন patch তাই training-এ অবদান রাখে না। এজন্যই group-এর ভেতরে বৈচিত্র্য দরকার — temperature এখানে গুরুত্বপূর্ণ।

**একটা সূক্ষ্ম বিষয় (আমার পর্যবেক্ষণ):** Advantage group-এর ভেতরে normalize হয়, তাই একটা prompt-এর ভেতরে reward-এর **absolute scale** (2.0 বনাম 1.0) আংশিকভাবে মুছে যায় — worked example ১ ও ২-এ দুটোতেই সঠিক উত্তরের advantage ধনাত্মক। তবে asymmetry পুরো হারায় না: label overfitting হলে সঠিক ও ভুলের পার্থক্য (3 বনাম 1) বড়, তাই format-এর ছোট পার্থক্যের তুলনায় accuracy সিদ্ধান্ত বেশি প্রভাব ফেলে।

### ৬.৭ আমার হিসাব: Asymmetric Reward কীভাবে Decision Threshold সরায়
ধরো model-এর ভেতরে একটা patch overfitting হওয়ার subjective probability $p$। Format নিখুঁত ধরে expected accuracy reward:
$$
\mathbb{E}[R_{\text{acc}} \mid \text{answer Overfitting}] = 2p, \qquad \mathbb{E}[R_{\text{acc}} \mid \text{answer Correct}] = 1 \cdot (1 - p)
$$
Reward-maximizing policy "Overfitting" বলবে যখন:
$$
2p > 1 - p \quad \text{অর্থাৎ} \quad p > \frac{1}{3}
$$
অর্থাৎ সমান reward-এ threshold হতো $p > 0.5$; এখানে threshold নেমে **$1/3$** হয়ে যায়। ফলে model বেশি করে "overfitting" বলবে → **Recall বাড়বে, Specificity কমবে।** Section ৮.৩-এর INVALIDATOR split-এ ঠিক এটাই দেখা যায়: Recall 97.2% কিন্তু correct patch-এর মাত্র 16/30 = 53.3% সঠিকভাবে চেনা গেছে। তাই authors-এর "without introducing bias" দাবি অন্তত এই split-এ দুর্বল। (এটা একটা আদর্শ-ক্ষেত্রের decision-theory যুক্তি; বাস্তব model পুরোপুরি এভাবে আচরণ নাও করতে পারে।)

### ৬.৮ Evaluation Metrics — সূত্র
$$
\text{Accuracy} = \frac{TP + TN}{TP + TN + FP + FN}
$$
$$
\text{Precision} = \frac{TP}{TP + FP} \qquad \text{Recall} = \frac{TP}{TP + FN}
$$
$$
F_1 = \frac{2 \cdot \text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}} = \frac{2\,TP}{2\,TP + FP + FN}
$$
$$
\text{Specificity (TNR)} = \frac{TN}{TN + FP}, \qquad \text{FPR} = 1 - \text{Specificity}
$$

| Metric | APCA-তে মানে (paper-এর ভাষায়) |
|---|---|
| Accuracy | মোট কত শতাংশ patch সঠিকভাবে classify হলো |
| Precision | "Overfitting" label কতটা বিশ্বাসযোগ্য — কম হলে সঠিক patch অযথা বাতিল হয় (developer productivity ও trust কমে) |
| Recall | সব overfitting patch-এর কত শতাংশ ধরা পড়লো — কম হলে ভুল patch codebase-এ ঢুকে যায় |
| F1 | Precision ও Recall-এর harmonic mean |
| AUC | সব decision threshold জুড়ে overfitting ও correct আলাদা করার ক্ষমতা |

**AUC (ROC curve-এর নিচের ক্ষেত্রফল):**
$$
\text{AUC} = \int_{0}^{1} \text{TPR}\left(\text{FPR}^{-1}(u)\right) \, du = P\left(s(x^{+}) > s(x^{-})\right)
$$
অর্থাৎ একটা random overfitting patch $x^{+}$ একটা random correct patch $x^{-}$-এর চেয়ে বেশি "overfitting score" $s$ পাওয়ার সম্ভাবনা। 0.5 = random, 1.0 = নিখুঁত।

**গুরুত্বপূর্ণ (আমার পর্যবেক্ষণ):** RePaCA একটা hard label (correct/overfitting) দেয়, কোনো probability score নয়। Paper বলেনি AUC কীভাবে হিসাব হয়েছে। Classifier যদি শুধু 0/1 দেয়, তাহলে ROC curve-এ একটাই বিন্দু থাকে এবং:
$$
\text{AUC}_{\text{hard}} = \frac{\text{TPR} + \text{TNR}}{2} = \text{Balanced Accuracy}
$$
Section ৬.১১-এ দেখাবো যে small dataset-এর reported সংখ্যাগুলো এই ব্যাখ্যার সাথে প্রায় মেলে — অর্থাৎ RePaCA-র "AUC" সম্ভবত আসলে balanced accuracy।

**MCC (Matthews Correlation Coefficient) — paper-এ নেই, আমি যোগ করেছি:**
$$
\text{MCC} = \frac{TP \cdot TN - FP \cdot FN}{\sqrt{(TP + FP)(TP + FN)(TN + FP)(TN + FN)}}
$$
Imbalanced dataset-এ চারটা ঘরই বিবেচনা করে বলে বেশি নির্ভরযোগ্য; −1 থেকে +1।

### ৬.৯ Worked Example — Paper-এর আসল Confusion Matrix (Fig. 3, INVALIDATOR test split, 139 patch)

Fig. 3 থেকে পড়া সংখ্যা (test split-এ 109টা overfitting, 30টা correct):

| | TP | FN | FP | TN |
|---|---|---|---|---|
| INVALIDATOR | 86 | 23 | 3 | 27 |
| RePaCA | 106 | 3 | 14 | 16 |

**RePaCA:**
- Accuracy $= (106 + 16)/139 = 122/139 = 0.8777 \to$ **87.8%** ✓ (paper-এর সাথে মেলে)
- Precision $= 106/(106 + 14) = 106/120 = 0.8833 \to$ **88.3%** ✓
- Recall $= 106/(106 + 3) = 106/109 = 0.9725 \to$ **97.2%** ✓
- F1 $= 2 \times 106/(212 + 14 + 3) = 212/229 = 0.9258 \to$ **92.6%** ✓
- Specificity $= 16/(16 + 14) = 16/30 = 53.3\%$ (আমার হিসাব)
- Balanced accuracy $= (0.9725 + 0.5333)/2 = 75.3\%$ (আমার হিসাব)
- MCC $= (106 \times 16 - 14 \times 3)/\sqrt{120 \times 109 \times 30 \times 19} = 1654/\sqrt{7455600} \approx 1654/2730.5 \approx 0.606$ (আমার হিসাব)

**INVALIDATOR:**
- Accuracy $= (86 + 27)/139 = 113/139 = 81.3\%$ ✓ (paper: 81.2% — rounding পার্থক্য)
- Precision $= 86/89 = 96.6\%$ ✓; Recall $= 86/109 = 78.9\%$ ✓
- F1 $= 172/(172 + 3 + 23) = 172/198 = 86.9\%$ (paper বলেছে 87.0% — সম্ভবত INVALIDATOR-এর মূল paper থেকে নেওয়া rounding; সামান্য পার্থক্য)
- Specificity $= 27/30 = 90.0\%$; Balanced accuracy $= (0.789 + 0.900)/2 = 84.5\%$; MCC $= 2253/\sqrt{14551500} \approx 0.591$ (আমার হিসাব)

**মূল শিক্ষা:** Accuracy ও F1-এ RePaCA এগিয়ে, কিন্তু **balanced accuracy-তে INVALIDATOR এগিয়ে (84.5% বনাম 75.3%)**, আর MCC প্রায় সমান (0.591 বনাম 0.606)। RePaCA 30টা correct patch-এর 14টাকে (46.7%) ভুল করে "overfitting" বলেছে।

### ৬.১০ আমার হিসাব: Trivial Baseline-এর সাথে তুলনা
যে classifier কিছু না দেখেই সব patch-কে "overfitting" বলে:
- INVALIDATOR test split-এ: Accuracy $= 109/139 = 78.4\%$, Recall = 100%, Precision = 78.4%, F1 $= 218/(218 + 30) = 87.9\%$।
- Small dataset-এ: Accuracy $= 648/1183 = 54.8\%$, F1 $= 1296/(1296 + 535) = 70.8\%$।

তাই INVALIDATOR split-এ RePaCA-র F1 92.6% trivial baseline-এর 87.9% থেকে মাত্র 4.7 point বেশি; এই split-এ F1 metric-টা positive class-ভারী বলে অনেকটা "ফোলানো"। Small dataset-এ অবশ্য RePaCA (F1 84.8%, accuracy 83.1%) trivial baseline-এর অনেক উপরে।

### ৬.১১ আমার হিসাব: Small Dataset-এর Confusion Matrix পুনর্গঠন
Small dataset: 648 overfitting (P), 535 correct (N)। Reported Recall 85.7%, Precision 84.0% ধরে (20টা unparseable উপেক্ষা করে, তাই আনুমানিক):
- $TP \approx 0.857 \times 648 \approx 555$; $FN \approx 93$
- $FP = TP/\text{Precision} - TP \approx 555/0.84 - 555 \approx 106$; $TN \approx 535 - 106 = 429$
- Accuracy $\approx (555 + 429)/1183 \approx 83.2\%$ (reported 83.1% ✓)
- Specificity $\approx 429/535 \approx 80.2\%$
- Balanced accuracy $\approx (85.7 + 80.2)/2 \approx 83.0\%$ — reported **AUC 82.8%**-এর খুব কাছে

অর্থাৎ small dataset-এ RePaCA-র ভারসাম্য INVALIDATOR split-এর চেয়ে অনেক ভালো (specificity ~80% বনাম 53.3%)। আর AUC ≈ balanced accuracy — Section ৬.৮-এর অনুমান সমর্থন করে।

### ৬.১২ McNemar's Test
দুটো classifier (A = APPT, B = RePaCA) একই $n$ instance-এ। $b$ = যেখানে A ঠিক কিন্তু B ভুল; $c$ = যেখানে A ভুল কিন্তু B ঠিক। (Continuity correction সহ) statistic:
$$
\chi^2 = \frac{\left( |b - c| - 1 \right)^2}{b + c}
$$
(Correction ছাড়া রূপ: $(b - c)^2/(b + c)$।) Null hypothesis-এ এটা 1 degree of freedom-এর $\chi^2$ distribution মানে। Paper শুধু ফল দিয়েছে: $\chi^2 = 25.90$, $p = 3.6 \times 10^{-7}$ (1,163 paired instance) — $b$ ও $c$-এর মান বা কোন রূপ ব্যবহার হয়েছে বলেনি।

**Illustrative উদাহরণ (কাল্পনিক সংখ্যা):** $b = 40$, $c = 100$ হলে $\chi^2 = (60 - 1)^2/140 \approx 24.9$ — paper-এর মানের কাছাকাছি মাত্রা। অর্থাৎ RePaCA যেখানে APPT-এর চেয়ে ভালো এমন instance, উল্টোটার চেয়ে উল্লেখযোগ্যভাবে বেশি।

### ৬.১৩ Bootstrap Confidence Interval
$B = 10{,}000$ বার test set থেকে replacement সহ $n$টা instance নেওয়া; প্রতিবার metric-এর পার্থক্য $\Delta^{(b)} = M_{\text{RePaCA}}^{(b)} - M_{\text{APPT}}^{(b)}$। 95% CI:
$$
\text{CI}_{95} = \left[ \Delta_{(2.5\%)},\; \Delta_{(97.5\%)} \right]
$$
CI-এর নিচের সীমা 0-এর উপরে হলে উন্নতি significant। Table 5-এ চারটা metric-এর সবগুলোর CI 0 বাদ দেয় (Section ৮.২)।

---

## ৭. Experimental Setup

| বিষয় | বিবরণ |
|---|---|
| **Main dataset** | Small — 1,183 patch, Defects4J v1.2, Java, APR tool-এর patch |
| **Transfer dataset** | Large — 49,694 patch |
| **INVALIDATOR dataset** | 885 patch = 746 train + 139 test (তাদের codebase থেকে) |
| **Protocol** | 5-fold CV (small); fixed split (INVALIDATOR); Small → Large (cross-dataset) |
| **Baselines** | ODS, Quatrain, CACHE, APPT (published/secondary সংখ্যা); APPT (নিজেদের reproduction); INVALIDATOR (published) |
| **Excluded baseline** | LLM4PatchCorrect — practical scenario ভিন্ন বলে (অনুরূপ labeled patch আগে থেকে থাকতে হয়) |
| **Metric** | Accuracy, Precision, Recall, F1, AUC; McNemar; bootstrap CI |
| **Model** | Qwen2.5-Coder-3B-Instruct + GRPO |

**Dataset statistics (Table 3):**

| Dataset | Correct | Overfitting | Total | Overfitting % (আমার হিসাব) |
|---|---|---|---|---|
| Small | 535 | 648 | 1,183 | 54.8% |
| Large | 25,589 | 24,105 | 49,694 | 48.5% |
| INVALIDATOR test split | 30 | 109 | 139 | 78.4% (Fig. 3 থেকে) |

**Small dataset-এর উৎস:** Tian et al. (1,000 patch) + Wang et al. (902 patch) = 1,902 → filtering ও duplicate বাদ দিয়ে 1,183।
**Large dataset-এর উৎস:** Correct patch মূলত ManySStuBs4J (developer fix, APR tool নয়); overfitting patch RepairThemAll framework থেকে; duplicate ও biased patch বাদ।

Authors দুটো dataset-কেই "balanced ও modest in size" বলেছেন।

---

## ৮. Results — মূল ফলাফল

### ৮.১ Standard Evaluation — Small Dataset (Table 4)

| Technique | Accuracy | Precision | Recall | F1 | AUC |
|---|---|---|---|---|---|
| ODS | 62.3 | – | – | 69.1 | 62.5 |
| Quatrain | 69.4 | – | – | 77.8 | 64.5 |
| CACHE | 75.4 | 79.5 | 76.5 | 78.0 | 80.3 |
| APPT | 79.7 | 80.8 | 83.2 | 81.8 | 82.5 |
| **RePaCA (Ours)** | **83.1** | **84.0** | **85.7** | **84.8** | **82.8** |

Paper-এর বলা পার্থক্য (percentage point):

| Metric | RePaCA − APPT | RePaCA − CACHE |
|---|---|---|
| Accuracy | +3.4 | +7.8 (paper); আমার হিসাবে 83.1 − 75.4 = 7.7 |
| Precision | +3.2 | +4.5 |
| Recall | +2.5 | +9.2 |
| F1 | +3.0 | +6.8 |
| AUC | +0.3 | +2.5 |

**আমার পর্যবেক্ষণ:** AUC-তে APPT-এর উপর উন্নতি মাত্র 0.3 point — প্রায় সমান। আর ODS ও Quatrain-এর সংখ্যা মূল paper নয়, LLM4PatchCorrect paper থেকে নেওয়া — তাই সমান condition নিশ্চিত নয়।

### ৮.২ Statistical Significance (Table 5 ও McNemar)
APPT-এর instance-level prediction মূল paper-এ নেই, তাই authors APPT-কে official code দিয়ে একই 5-fold split-এ নিজেরা চালিয়েছেন।

**Table 5 — Bootstrap 95% CI (10,000 resample), small dataset:**

| Metric | APPT (reproduction) | RePaCA | Diff (RePaCA − APPT) |
|---|---|---|---|
| Accuracy | 75.0 [72.4, 77.5] | 83.1 [80.9, 85.2] | +8.08 [+5.1, +11.1] |
| Precision | 76.2 [72.9, 79.4] | 83.9 [81.1, 86.7] | +7.75 [+4.6, +11.0] |
| Recall | 79.4 [76.3, 82.5] | 85.7 [82.8, 88.3] | +6.24 [+2.3, +10.1] |
| F1 | 77.8 [75.2, 80.2] | 84.8 [82.6, 86.9] | +7.02 [+4.3, +9.8] |

সব CI 0 বাদ দেয় → statistically significant। (AUC-এর CI দেওয়া হয়নি।)

**McNemar's test:**
- 1,163টা paired instance-এ: $\chi^2 = 25.90$, $p = 3.6 \times 10^{-7}$ → RePaCA-র পক্ষে significant।
- বাকি **20টা instance (1.7%)** বাদ — RePaCA unparseable output দিয়েছিল।
- Robustness check: ওই 20টাকে majority class-এ বসিয়ে আবার: $\chi^2 = 24.82$, $p = 6.3 \times 10^{-7}$ → এখনো significant।

**আমার পর্যবেক্ষণ — দুটো গুরুত্বপূর্ণ বিষয়:**
1. APPT-এর reproduction published সংখ্যার চেয়ে কম: Accuracy 79.7 → 75.0 (−4.7), Precision 80.8 → 76.2, Recall 83.2 → 79.4, F1 81.8 → 77.8। তাই "RePaCA APPT-এর চেয়ে কত ভালো" — published-এর তুলনায় +3.4, reproduction-এর তুলনায় +8.1 accuracy point। Significance test দুর্বল reproduction-এর বিরুদ্ধে করা — authors নিজেই এটা threat হিসেবে স্বীকার করেছেন।
2. Table 5-এ RePaCA-র precision **83.9**, কিন্তু Table 4 ও text-এ **84.0** — ছোট অসঙ্গতি (সম্ভবত rounding বা unparseable instance-এর ভিন্ন handling)।

### ৮.৩ INVALIDATOR-এর সাথে তুলনা (Section 4.2, Fig. 3)

| Metric | INVALIDATOR | RePaCA |
|---|---|---|
| Accuracy | 81.2 | **87.8** |
| Precision | **96.6** | 88.3 |
| Recall | 78.9 (86/109) | **97.2 (106/109)** |
| F1 | 87.0 | **92.6** |
| False Positive | **3** | 14 |
| False Negative | 23 | **3** |
| Specificity (আমার হিসাব) | **90.0%** | 53.3% |
| Balanced accuracy (আমার হিসাব) | **84.5%** | 75.3% |

**Authors-এর ব্যাখ্যা:** RePaCA বেশিরভাগ overfitting patch ধরে (recall অনেক বেশি), বিনিময়ে কিছু সঠিক patch-কে ভুল করে overfitting বলে (precision কম)। তাদের মতে এটা গ্রহণযোগ্য trade-off, কারণ overfitting patch-এর "নীরবে codebase-এ ঢুকে পড়া" ঠেকানো বেশি গুরুত্বপূর্ণ — software-এর behavioral integrity-কে patch acceptance rate-এর উপর অগ্রাধিকার।

**আমার পর্যবেক্ষণ:** Test split-এ মাত্র 30টা correct patch — তাই specificity-র অনিশ্চয়তা অনেক বড়। আর Section ৬.৭-এর threshold বিশ্লেষণ বলে এই recall-ভারী আচরণ asymmetric reward-এরই প্রত্যাশিত ফল।

### ৮.৪ Cross-Dataset — Small-এ Train, Large-এ Test (Table 6)

| Model | Accuracy | Precision | Recall | F1 | AUC |
|---|---|---|---|---|---|
| APPT (reproduction) | 60.5 | 59.1 | **90.2** | 71.4 | 55.4 |
| **RePaCA** | **72.7** | **72.4** | 78.7 | **75.4** | **72.3** |

- Accuracy +12.2 point, F1 +4.0 point, AUC +16.9 point।
- APPT-এর recall বেশি (90.2%) কিন্তু precision 59.1% — প্রায় সব কিছুকেই overfitting বলছে; AUC 55.4% প্রায় random। Authors-এর মতে এটা APPT-এর OOD data-তে "architectural vulnerability"।
- RePaCA precision ও recall-এ ভারসাম্য রেখেছে।
- তবে small dataset-এর তুলনায় RePaCA-র নিজেরও বড় পতন: Accuracy 83.1 → 72.7 (−10.4), F1 84.8 → 75.4 (−9.4), AUC 82.8 → 72.3 (−10.5) (আমার হিসাব)।

**আমার হিসাব — একটা অসঙ্গতির সম্ভাবনা:** Hard label ও AUC = balanced accuracy ধরে নিয়ে Table 6-এর RePaCA-র Accuracy, Precision, Recall থেকে test set-এর overfitting অনুপাত বের করলে পাওয়া যায় প্রায় **53%** (rounding ধরে 53.0–53.4%), এবং তখন balanced accuracy ঠিক 72.3% হয় (= reported AUC)। কিন্তু Table 3 অনুযায়ী Large dataset-এ overfitting অনুপাত **48.5%**। সম্ভাব্য ব্যাখ্যা: unparseable output বাদ দেওয়া, small-এর সাথে overlap বাদ দেওয়া, বা Large-এর একটা subset-এ test — paper-এ এটা বলা নেই। Supervisor প্রশ্ন করলে "authors-কে জিজ্ঞেস করার মতো বিষয়" হিসেবে বলা যায়; নিশ্চিত দাবি নয়।

### ৮.৫ Reasoning Examples (Section 4.4 ও 6)

| Example | Patch | Model কী ঠিক বলেছে | Model কী ভুল বলেছে |
|---|---|---|---|
| **Code 1 — Overfitting** | একটা step-size হিসাবের method: দুটো sum (`yOnScale2`, `yDotOnScale2`) জমা করে, তাদের অনুপাত থেকে step `h` বের করে বা খুব ছোট হলে minimum মান দেয়। Patch (line 5–6) `yDotOnScale2` update-এর আগে `if (scale.length != this.maxstep)` যোগ করে | মূল functionality ও নতুন শর্ত ঠিকভাবে বর্ণনা; patch `scale[j] == 0` হলে **division by zero** (আসল bug-এর উৎস) ঠেকায় না; শর্তটা অত্যন্ত নির্দিষ্ট — overfitting-এর মূল লক্ষণ। চূড়ান্ত label সঠিক | `yDotOnScale2`-কে "নতুন variable যা original code-এ কোথাও ব্যবহৃত নয়" বলেছে — অথচ আগেই line 2-এ declared হিসেবে বিবেচনা করেছিল → **hallucination ও স্ববিরোধ** |
| **Code 2 — Correct** | `Complex` class-এর `add(Complex rhs)`: আগে `checkNotNull`, তারপর real ও imaginary অংশ যোগ। Patch (line 3–5) — current object বা `rhs` NaN হলে সঙ্গে সঙ্গে NaN return | মূল সমস্যা (NaN handling নেই) চিহ্নিত; fix generic (নির্দিষ্ট মানের উপর নির্ভর করে না) → সঠিক label | — |
| **Code 3 — "Indistinguishable" overfitting** (Section 6) | খুব ছোট, context-হীন patch | — | Authors-এর মতে এমন patch নির্ভরযোগ্যভাবে classify করা প্রায় অসম্ভব — আশেপাশের method/class-এর context লাগবে |

**আমার পর্যবেক্ষণ:** মাত্র ২টা সফল example দেখানো হয়েছে (cherry-picked হওয়ার সম্ভাবনা)। ভুল classification-এর কোনো systematic error analysis (কত শতাংশ reasoning-এ hallucination, কত শতাংশে যুক্তি ও label-এর বিরোধ) নেই। Code 1-এ label সঠিক হলেও যুক্তিতে ভুল আছে — অর্থাৎ **"সঠিক উত্তর, ভুল কারণ"** সম্ভব।

### ৮.৬ Ablation ১ — Base Model (Table 7, GRPO-র আগে, small dataset)

| Model | Parameters | Accuracy | F1 | AUC |
|---|---|---|---|---|
| Gemma-2 | 2B | 55.8 | 18.1 | 52.0 |
| Llama-3.2 | 3B | 54.2 | 16.0 | 50.2 |
| Qwen2.5 | 3B | **56.7** | 14.4 | 52.5 |
| **Qwen2.5-Coder** | 3B | 55.9 | **38.4** | **53.6** |

- General Qwen2.5-এর accuracy সবচেয়ে বেশি, কিন্তু F1 মাত্র 14.4% — authors-এর মতে majority class-এর দিকে প্রবল bias, overfitting চিনতে ব্যর্থ।
- Qwen2.5-Coder সেরা ভারসাম্য → নির্বাচিত।
- **GRPO-র প্রভাব (আমার হিসাব):** Qwen2.5-Coder-3B GRPO-র আগে → পরে: Accuracy 55.9 → 83.1 (+27.2), F1 38.4 → 84.8 (+46.4), AUC 53.6 → 82.8 (+29.2)। অর্থাৎ পুরো উন্নতির প্রায় সবটাই training থেকে এসেছে; base model-গুলো প্রায় random (AUC 50–54%)।

**আমার হিসাব — আরেকটা অসঙ্গতি:** Small dataset-এ overfitting (positive) = 648, correct = 535। যদি F1 overfitting class-এর জন্য হয়, তাহলে F1 = 14.4% হলে accuracy সর্বোচ্চ প্রায় 49.5% হতে পারে — কিন্তু reported 56.7%। একইভাবে Gemma (F1 18.1 → সর্বোচ্চ ~50.7%, reported 55.8) ও Llama (F1 16.0 → সর্বোচ্চ ~50.0%, reported 54.2)। সম্ভাব্য ব্যাখ্যা: base model-এর অনেক unparseable output বাদ দিয়ে হিসাব, ভিন্ন subset, বা F1 অন্য class-এর জন্য। আরও লক্ষণীয়: majority class হলো overfitting (54.8%) — model যদি "majority class-এর দিকে bias" থাকে তাহলে বেশিরভাগ "overfitting" বলবে, যা overfitting-এর F1 **বাড়াবে**, কমাবে না। তাই Table 7-এর সংখ্যা ও তার ব্যাখ্যা পুরোপুরি সামঞ্জস্যপূর্ণ নয় — নিশ্চিত দাবি না করে "প্রশ্ন" হিসেবে রাখা উচিত।

### ৮.৭ Ablation ২ — Temperature (Fig. 4)
Temperature 0.0 থেকে 1.2 পর্যন্ত (0.2 ধাপে) পরীক্ষা। Fig. 4 থেকে **আনুমানিক পড়া মান** (graph থেকে চোখে পড়া, ±0.002 ভুল হতে পারে; শুধু T = 0.6-এর মান text-এ সঠিকভাবে দেওয়া):

| Temperature | Accuracy | F1 | AUC |
|---|---|---|---|
| 0.0 | ~0.803 | ~0.811 | ~0.800 |
| 0.2 | ~0.818 | ~0.829 | ~0.817 |
| 0.4 | ~0.814 | ~0.828 | ~0.813 |
| **0.6** | **0.831** | **0.848** | **0.828** |
| 0.8 | ~0.816 | ~0.828 | ~0.815 |
| 1.0 | ~0.813 | ~0.826 | ~0.812 |
| 1.2 | ~0.799 | ~0.809 | ~0.798 |

**Authors-এর ব্যাখ্যা:** কম temperature-এ বৈচিত্র্য কম → performance কম; বেশি temperature-এ reasoning অসংলগ্ন ও hallucinatory → "sharp decline"।

**আমার পর্যবেক্ষণ:** পুরো range-এ accuracy মাত্র ~0.80 থেকে 0.83 — প্রায় 3 point-এর পার্থক্য। T = 0.2 থেকে 1.0 পর্যন্ত মান প্রায় সমান (~0.81–0.82), শুধু 0.6-এ একটা চূড়া। এটা "highly sensitive" দাবির চেয়ে বরং **single-run noise**-এর মতো দেখায় — একাধিক seed-এর গড় ও error bar ছাড়া বলা কঠিন। তাছাড়া temperature-টা **test fold-এর ফল দেখেই বাছাই করা হয়েছে** বলে মনে হয় (Section ১২.২)।

### ৮.৮ Format Failure
- Text-এ "around 1%" (Section 3.1, 5.2) এবং Section 4.1-এ 20/1,183 = **1.7%** unparseable।
- প্রস্তাবিত সমাধান: post-processing বা re-sampling।

---

## ৯. Key Findings / Insights (Supervisor-কে বলার মতো ৮টা পয়েন্ট)

1. **ছোট reasoning model + RL static APCA-তে state-of-the-art:** 3B model, small dataset-এ 83.1% accuracy, 84.8% F1 — ODS, Quatrain, CACHE, APPT সবার উপরে।
2. **উন্নতি statistically significant** (নিজেদের APPT reproduction-এর বিরুদ্ধে): McNemar $p = 3.6 \times 10^{-7}$; সব bootstrap CI 0 বাদ দেয়।
3. **SFT ছাড়া শুধু RL-ই যথেষ্ট:** কোনো মানুষের লেখা reasoning ছাড়াই, শুধু label-ভিত্তিক reward দিয়ে model reasoning শিখেছে। GRPO-র আগে Qwen2.5-Coder প্রায় random (AUC 53.6%), পরে 82.8%।
4. **Domain shift-এ বেশি robust:** Small → Large-এ RePaCA AUC 72.3% বনাম APPT 55.4%। তবে নিজেরও প্রায় 10 point পতন।
5. **Recall-ভারী আচরণ:** INVALIDATOR split-এ recall 97.2% কিন্তু 30টা correct patch-এর 14টা ভুল করে বাতিল; asymmetric reward (2.0 বনাম 1.0) এর একটা সম্ভাব্য কারণ।
6. **Explanation আছে কিন্তু বিশ্বাসযোগ্য নয়:** `<think>` block developer-কে সাহায্য করে, কিন্তু hallucination, diff ভুল বোঝা, যুক্তি ও label-এর বিরোধ দেখা গেছে — authors নিজেই বলেছেন এটা developer inspection-কে সাহায্য করবে, প্রতিস্থাপন নয়।
7. **Context-poor patch মৌলিক সীমা:** খুব ছোট patch শুধু code দেখে classify করা প্রায় অসম্ভব — repository context দরকার।
8. **Training ব্যয়বহুল, inference সস্তা:** H100-এ GRPO training, কিন্তু inference 8 GB VRAM-এর consumer GPU-তে — APR pipeline-এ post-generation filter হিসেবে বসানো যায়।

---

## ১০. কেন এই Solution অন্যগুলোর থেকে ভালো?

| বৈশিষ্ট্য | ODS / CACHE | Quatrain | INVALIDATOR | APPT | LLM4PatchCorrect | Dynamic (test generation) | **RePaCA** |
|---|---|---|---|---|---|---|---|
| Execution লাগে? | না | না | Invariant inference-এর জন্য test লাগে | না | না | হ্যাঁ | **না** |
| Bug report/description লাগে? | না | হ্যাঁ | না | না | Bug তথ্য লাগে | না | **না** |
| অনুরূপ labeled patch লাগে? | না | না | না | না | হ্যাঁ | না | **না** |
| Root cause নিয়ে যুক্তি | না (pattern) | না (similarity) | আংশিক (invariant) | না (single-pass) | আংশিক | আচরণ দেখে | **হ্যাঁ, explicit CoT** |
| ব্যাখ্যা দেয়? | না | না | না | না | সীমিত | Failing test | **হ্যাঁ, `<think>`** |
| Small dataset accuracy | 62.3 / 75.4 | 69.4 | ভিন্ন dataset | 79.7 | তুলনা করা হয়নি | তুলনা করা হয়নি | **83.1** |
| OOD robustness | — | — | — | AUC 55.4 | — | — | **AUC 72.3** |

**মূল শক্তি:**
1. **শুধু code-ই যথেষ্ট** — কোনো test, execution, bug report বা retrieval pool লাগে না; তাই যেকোনো APR pipeline-এ plug-in করা যায়।
2. **Reasoning → generalization:** pattern-matching-এর চেয়ে semantic বোঝাপড়া, যা domain shift-এ ভালো টেকে।
3. **Transparency:** প্রতিটা সিদ্ধান্তের সাথে human-readable rationale।
4. **Lightweight deployment:** 3B, 8 GB VRAM।
5. **Data-efficient training:** মাত্র ~946টা labeled patch per fold, কোনো reasoning annotation ছাড়া।

---

## ১১. কোন পরিস্থিতিতে এই paper/technique ভালো কাজ করে, কোথায় করে না

### ✅ ভালো কাজ করে যখন:
- **Java, single-method/single-hunk ছোট patch** (Defects4J-ধরনের)।
- Bug-এর root cause snippet-এর ভেতরেই দৃশ্যমান (যেমন NaN check, division by zero)।
- Patch-এ **সন্দেহজনকভাবে নির্দিষ্ট শর্ত** আছে (`if (x == specificValue)`) — overfitting-এর ক্লাসিক লক্ষণ।
- Execution environment নেই বা ব্যয়বহুল — শুধু code হাতে আছে।
- Recall বেশি গুরুত্বপূর্ণ (ভুল patch ঢোকা বেশি ক্ষতিকর, কিছু সঠিক patch হারানো সহ্য করা যায়)।
- Developer-এর সাথে human-in-the-loop review — explanation সাহায্য করে।

### ❌ ভালো কাজ করে না / সীমিত যখন:
- **Context-poor patch** — ছোট পরিবর্তন যার সঠিকতা অন্য method/class-এর উপর নির্ভর করে (Code 3)।
- **Multi-file, repository-level patch** (SWE-bench-এর মতো) — input-এ শুধু দুটো snippet, 2048-token completion।
- **অন্য language** (Python, JavaScript) — শুধু Java-তে train ও test।
- **Correct patch বেশি এমন distribution** — specificity কম (INVALIDATOR split-এ 53.3%) হলে অনেক সঠিক patch বাতিল হবে।
- **Training data-র থেকে ভিন্ন উৎসের patch** — Small → Large-এ ~10 point পতন; LLM agent-এর patch আরও ভিন্ন।
- **Calibrated confidence দরকার হলে** — শুধু hard label, কোনো probability নেই।
- **Explanation-কে প্রমাণ হিসেবে ব্যবহার** — CoT faithful নয়।

---

## ১২. Limitations — দুর্বলতা

### ১২.১ Authors যা নিজেরা স্বীকার করেছেন (Section 5.2 Threats to Validity ও Section 6 Future Work)
1. **Reasoning-এ মৌলিক ত্রুটি:** hallucination (code-এ নেই এমন সমস্যা/সমাধান বানানো); diff সঠিকভাবে বুঝতে ব্যর্থ; snippet-এ নেই এমন method/variable-এর আচরণ অনুমান; superficial/অপ্রাসঙ্গিক পরিবর্তনে অতিরিক্ত গুরুত্ব; **যুক্তি ও চূড়ান্ত label-এর বিরোধ** (যুক্তি বলে bug ঠিক হয়েছে, label বলে overfitting)। তাই explanation developer-এর পরিদর্শনের সহায়ক, প্রতিস্থাপন নয়।
2. **Cross-dataset-এ বড় domain shift** ইচ্ছাকৃত — overall metric কমে যায়।
3. **APPT reproduction published সংখ্যার চেয়ে কম** — hardware, framework version, non-deterministic GPU operation-এর কারণে হতে পারে; তাই broad comparison-এ published সংখ্যা, আর significance ও cross-dataset-এ reproduction ব্যবহার।
4. **প্রায় 1% format failure** — re-sampling বা post-processing দিয়ে সমাধানযোগ্য।
5. **GRPO training-এর computational খরচ বেশি** — অনেক generation, বড় GPU, দীর্ঘ সময়; তবে inference দ্রুত।
6. **Dataset ছোট এবং শুধু correct/overfitting patch** — বেশি APR tool-এর patch দিয়ে বড় করা দরকার।
7. **কিছু patch খুব ছোট বা context-poor** (Code 3) — repository context, AST, execution trace, bug ও fix-এর natural-language ব্যাখ্যা যোগ করা উচিত (কিন্তু deployment জটিলতা বাড়বে)।
8. **APR pipeline-এ বাস্তবে integrate করে evaluate করা হয়নি।**
9. **Reward শুধু format ও final answer দেখে, reasoning-এর যৌক্তিকতা নয়** — reasoning quality reward দরকার।
10. **বড়/বিশেষায়িত reasoning model পরীক্ষা করা হয়নি।**

### ১২.২ আমার Critical Analysis (Professor-level observation)

**(ক) Evaluation design**
1. **Hyperparameter test set দেখে বাছাই (সবচেয়ে গুরুত্বপূর্ণ):** Temperature ablation-এর সেরা মান (0.6)-এর ফল **হুবহু** headline সংখ্যা (83.1 / 84.8 / 82.8)। Base model ablation-ও small dataset-এই। আলাদা held-out set-এ tuning-এর উল্লেখ নেই (epoch সংখ্যার জন্য "validation split of the training data" বলা আছে, temperature-এর জন্য নেই)। এতে reported সংখ্যা আশাবাদী (optimistic) হতে পারে — বিশেষ করে temperature curve-এর পার্থক্য ছোট (~3 point) হওয়ায়।
2. **Variance/seed report নেই:** Temperature 0.6-এ sampling stochastic, অথচ একটা run। একই patch-এ বারবার চালালে label বদলায় কিনা (run-to-run consistency) মাপা হয়নি — এটা ঠিক আমাদের **CG4**।
3. **Baseline-এর সমতা:** ODS ও Quatrain-এর সংখ্যা তৃতীয় paper থেকে, CACHE/APPT মূল paper থেকে, INVALIDATOR মূল paper থেকে — একই split, একই preprocessing নিশ্চিত নয় (Sub-domain 1 Summary-র **CG8**-এর মতো সমস্যা)।
4. **গুরুত্বপূর্ণ ablation অনুপস্থিত:**
   - **SFT বনাম GRPO** — একই data-তে classification-head বা SFT দিয়ে train করলে কত হতো? Reasoning-ই কি উন্নতির কারণ, নাকি শুধু 3B code model fine-tune করা?
   - **`<think>` ছাড়া GRPO** (শুধু answer) — CoT-এর আসল অবদান কত?
   - **Reward weight** (1:1 বনাম 1:2) ও **one-shot example**-এর প্রভাব।
   - **বড় zero-shot LLM** (যেমন বাণিজ্যিক frontier model) — তুলনা নেই।
5. **INVALIDATOR তুলনা পুরোপুরি "static বনাম static" নয়:** INVALIDATOR test-inferred invariant ব্যবহার করে; আর split-এ মাত্র 30টা correct patch, তাই precision/specificity খুব অস্থির।
6. **Trivial baseline report করা হয়নি:** INVALIDATOR split-এ "সব overfitting" বললেই F1 87.9% (Section ৬.১০)।

**(খ) Metric ও internal consistency**
7. **AUC hard label থেকে:** RePaCA probability দেয় না; reported AUC সম্ভবত balanced accuracy (small dataset-এ পুনর্গঠন 83.0% বনাম reported 82.8%)। APPT-এর AUC আসল ROC-AUC (continuous score) হলে দুটো সরাসরি তুলনীয় নয়।
8. **ছোট সংখ্যাগত অসঙ্গতি:** precision 84.0 (Table 4) বনাম 83.9 (Table 5); CACHE-এর তুলনায় accuracy পার্থক্য 7.8 বলা, কিন্তু 83.1 − 75.4 = 7.7; INVALIDATOR F1 87.0 বনাম Fig. 3 থেকে 86.9; "~1%" বনাম 1.7% format failure।
9. **Table 7 ও Table 6-এর সম্ভাব্য অসঙ্গতি** (Section ৮.৪ ও ৮.৬-এ আমার হিসাব) — class distribution-এর সাথে reported accuracy/F1 মেলে না। এগুলো unparseable handling-এর কারণে হতে পারে; paper-এ পরিষ্কার নেই।
10. **Unparseable output-এর handling metric-এ অস্পষ্ট:** McNemar-এ 20টা বাদ, কিন্তু Table 4-এ কীভাবে গণনা হলো (ভুল ধরা, বাদ দেওয়া?) বলা নেই। Deployment-এ "উত্তর নেই" একটা বাস্তব ঘটনা।

**(গ) Method design**
11. **Asymmetric reward → bias:** Section ৬.৭-এ দেখিয়েছি এটা decision threshold 0.5 থেকে 1/3-এ নামায়; INVALIDATOR split-এর specificity 53.3% এর সাথে সামঞ্জস্যপূর্ণ। "Without introducing bias" দাবি সব dataset-এ টেকে না।
12. **Keyword-ভিত্তিক format reward দুর্বল:** "correct" ও "incorrect" দুটোই keyword; "incorrect" শব্দে "correct" substring আছে — parser সতর্ক না হলে label ভুল পড়া সম্ভব। Paper parser-এর নিয়ম দেয়নি।
13. **Reasoning-এর মানের কোনো reward বা metric নেই:** Explanation quality-র দাবি শুধু ২টা হাতে-বাছাই example-এ; কোনো human evaluation, faithfulness বা consistency metric নেই।
14. **Calibration/confidence নেই:** Assurance-এর জন্য "কতটা নিশ্চিত" জানা দরকার (**CG7**); hard label সেটা দেয় না।

**(ঘ) Data ও validity**
15. **Contamination ঝুঁকি:** Defects4J ও তার patch অনেক পুরনো ও public; Qwen2.5-Coder-এর pre-training data-তে থাকতে পারে। Paper এটা আলোচনা করেনি।
16. **Label noise:** Small dataset-এর label আগের study-গুলোর manual/semi-automatic label; Large-এ "correct" = developer fix (ManySStuBs4J) — APR tool-এর correct patch-এর থেকে ভিন্ন distribution, ফলে model "কে লিখেছে" (style) শিখে ফেলতে পারে, "সঠিক কিনা" নয়।
17. **Language ও scope:** শুধু Java, শুধু Defects4J-ধরনের ছোট patch; multi-hunk/multi-file patch-এর আলাদা ফল নেই।
18. **Reproducibility:** Code public নয় ("data on request"), prompt-এর হুবহু text নেই, $\beta$, $\epsilon$, LoRA, seed নেই।
19. **Inference খরচ মাপা হয়নি:** প্রতি patch-এ কত token/সেকেন্ড লাগে — CoT 2048 token পর্যন্ত, তাই "lightweight" দাবি সংখ্যা দিয়ে সমর্থিত নয়।

---

## ১৩. Research Gaps — কোথায় কাজ করার সুযোগ আছে

| # | Gap | কেন গুরুত্বপূর্ণ | Sub-domain 1-এর কোন CG | কে কিছুটা কাজ করেছে (আমাদের folder-এ) |
|---|---|---|---|---|
| G1 | **Agent patch-এর জন্য static APCA (Python, repository-level)** — RePaCA শুধু Java/Defects4J | SWE-bench-style agent-এর plausible patch-এর overfitting ধরা | CG1 | AI Coding Agents (AutoCodeRover-এর 51/78 label); Patch Validation |
| G2 | **Hybrid APCA: static reasoning + dynamic evidence** (generated test-এর ফল, execution trace) | Static একা context-poor patch-এ ব্যর্থ; dynamic একা ব্যয়বহুল | CG1, CG3 | LLM Test Generation; Patch Validation |
| G3 | **APCA score দিয়ে candidate re-ranking** | Agentless-এর 96 বনাম 126 ফাঁক | CG2 | AI Coding Agents (Agentless); Patch Validation |
| G4 | **Calibrated confidence ও abstention** — hard label-এর বদলে probability; "নিশ্চিত নই" হলে মানুষের কাছে পাঠানো | Assurance-এর জন্য risk-aware সিদ্ধান্ত | CG7 | Trustworthy AI for Software Engineering; Patch Validation (HITL LLM-as-a-Judge) |
| G5 | **Run-to-run consistency of the judge** — একই patch-এ বারবার একই রায়? | Stochastic judge নিজেই অবিশ্বস্ত হতে পারে | CG4 | Coding-Agent Evaluation & Reliability |
| G6 | **Explanation faithfulness ও reasoning-quality reward** | Hallucinated rationale developer-কে ভুল পথে নেয় | CG7 | Trustworthy AI for Software Engineering |
| G7 | **Overfitting-এর বাইরে: security-regression detection** — patch test pass করে কিন্তু নতুন vulnerability আনে | Correct-but-insecure patch | CG5 | Security of AI-Generated Code; APR folder-এর LLM Vulnerability Repair case study |
| G8 | **Fair, reproducible APCA benchmark** — একই split, একই preprocessing, variance সহ | Paper-ভেদে baseline সংখ্যা মেলে না | CG8, CG6 | Coding-Agent Evaluation & Reliability |
| G9 | **Cost-sensitive / threshold-tunable APCA** — reward asymmetry বা threshold দিয়ে precision-recall নিয়ন্ত্রণ | ভিন্ন project-এর ভিন্ন ঝুঁকি-সহনশীলতা | CG1, CG7 | — (খোলা) |

---

## ১৪. কী করলে আরও ভালো হবে — Improvement Ideas

(সব idea আমার — paper-এ নেই, যদি না উল্লেখ থাকে।)

1. **Score দেওয়া, শুধু label নয়:** $k$টা CoT sample করে overfitting-ভোটের অনুপাত বা `<answer>` token-এর log-probability ব্যবহার করে continuous score:
   $$
   s(x) = \frac{1}{k} \sum_{j=1}^{k} \mathbb{1}\left[ \hat{y}^{(j)} = 1 \right]
   $$
   এতে আসল ROC-AUC, calibration (ECE) ও abstention সম্ভব; ভোট-বিভক্তি নিজেই uncertainty-র সংকেত (self-consistency)।
2. **Threshold বা reward-ratio tuning:** Section ৬.৭ অনুযায়ী reward ratio $w$ হলে threshold $p > 1/(1 + w)$। Project-এর ঝুঁকি অনুযায়ী $w$ বা score-threshold বেছে নেওয়া।
3. **Reasoning-consistency reward:** যুক্তি ও label-এর বিরোধ শাস্তি দেওয়া (authors-এর future work-এর সাথে মেলে) — যেমন একটা ছোট verifier model দিয়ে CoT-এর সিদ্ধান্ত বের করে label-এর সাথে মেলানো।
4. **Context augmentation:** surrounding method/class, call-site, issue text (SWE-bench-এ আছে), এবং failing test-এর নাম/body যোগ করা — authors-ও repository context প্রস্তাব করেছেন।
5. **Hybrid signal:** RePaCA-র static score + generated test-এর ফল + patch-এর আকার/শর্তের নির্দিষ্টতা (যেমন literal constant-এর সাথে তুলনা) → একটা ছোট meta-classifier।
6. **Proper evaluation:** nested CV বা আলাদা validation fold-এ temperature বাছাই; ৩–৫টা seed; McNemar-এর $b$, $c$ report; trivial baseline ও MCC report।
7. **SFT/CoT ablation:** একই 3B model-এ (ক) classification head, (খ) SFT, (গ) GRPO without think, (ঘ) GRPO with think — reasoning-এর আসল অবদান মাপা।
8. **Cross-language transfer:** Java-তে train করে Python patch-এ zero-shot test; তারপর অল্প Python label দিয়ে GRPO।

---

## ১৫. কোন Gap-এ Research করলে ভালো Result ও Publication আসতে পারে

> ⚠️ এটা Sub-domain 2-এর এই paper-এর ভিত্তিতে প্রাথমিক মত। বাকি sub-domain (বিশেষ করে Patch Validation ও LLM Test Generation) পড়ার পর চূড়ান্ত করবো।

| Gap / Idea | SPL3-তে করা সম্ভব? | Novelty | Publication সম্ভাবনা |
|---|---|---|---|
| **G1: RePaCA-style static judge SWE-bench agent patch-এ** (Python transfer study) | ✅ হ্যাঁ — public agent patch + ছোট label set; 3B model inference 8 GB GPU-তে; বাণিজ্যিক LLM API দিয়ে prompt-only version-ও সম্ভব | উচ্চ — Java APCA → Python agent patch transfer প্রায় অনাবিষ্কৃত বলে মনে হয় (literature যাচাই করতে হবে) | ⭐⭐⭐⭐ |
| **G1 + G4: Self-consistency score দিয়ে calibrated APCA + abstention** | ✅ হ্যাঁ — training ছাড়াই, শুধু $k$টা sample | মাঝারি-উচ্চ; assurance framing নতুন | ⭐⭐⭐⭐ |
| **G2 + G3: Static judge + generated test দিয়ে Agentless candidate re-ranking** | ✅ হ্যাঁ, কিন্তু Docker/WSL2 লাগবে | উচ্চ; পরিষ্কার metric (resolved সংখ্যা) | ⭐⭐⭐⭐⭐ |
| G5: LLM judge-এর run-to-run consistency study | ✅ সহজ | মাঝারি | ⭐⭐⭐ |
| GRPO দিয়ে নিজে Python APCA model train করা | ⚠️ কঠিন — H100-শ্রেণির GPU, অনেক labeled data লাগে | উচ্চ | ⭐⭐⭐ (resource-এর উপর নির্ভর) |

**সম্ভাব্য venue (general guidance):**
- **Journal:** *Neurocomputing* নিজেই এই ধরনের কাজ নিয়েছে (undergraduate first author সহ!); এছাড়া Information and Software Technology (IST), Journal of Systems and Software (JSS), Empirical Software Engineering (EMSE), Automated Software Engineering journal।
- **Conference/Workshop:** ICSE/FSE/ASE/ISSTA-এর workshop (যেমন LLM4Code, APR workshop) — student-এর জন্য শুরু করা সহজ।

---

## ১৬. SPL3 Implementation Perspective — Software-এ কীভাবে আনবো

### ১৬.১ RePaCA কি আমাদের Assurance Layer-এর Overfitting-Detection Component হতে পারে?

**সংক্ষিপ্ত উত্তর (আমার মূল্যায়ন):** ধারণা হিসেবে **হ্যাঁ** — এটাই সবচেয়ে সস্তা প্রথম স্তর (execution লাগে না, 8 GB GPU, ব্যাখ্যা দেয়)। কিন্তু **RePaCA-কে হুবহু SWE-bench agent patch-এ বসালে অনেক কিছু ভাঙবে**; তাই এটাকে "plug-in" নয়, "শুরুর ভিত্তি" হিসেবে দেখতে হবে।

**কী ভাঙবে — বিস্তারিত:**

| দিক | RePaCA-র training/evaluation | SWE-bench agent patch (Sub-domain 1) | ঝুঁকি |
|---|---|---|---|
| Language | Java | Python | Syntax, idiom, type system ভিন্ন; dynamic typing-এ bug pattern ভিন্ন |
| Patch-এর উৎস | পুরনো APR tool (template/search-based) | LLM agent (SWE-agent, AutoCodeRover, Agentless) | Overfitting-এর ধরন ভিন্ন — APR tool অদ্ভুত শর্ত যোগ করে; LLM patch দেখতে "স্বাভাবিক" কিন্তু অসম্পূর্ণ হতে পারে |
| Patch-এর আকার | ছোট, সাধারণত single method/hunk | Gold patch গড়ে 32.8 line edit, 1.7 file, 3টা function (Sub-domain 1, Paper 01, Table 1) | দুটো snippet-এ ধরানো যায় না |
| Context | শুধু buggy + fixed snippet | পুরো repository; issue text আছে | Context-poor সমস্যা (Code 3) আরও বড় হবে; আবার issue text একটা বাড়তি সুযোগ |
| Input/Output length | Max completion 2048 token; prompt length অজানা | Multi-file diff + context অনেক বড় | Context window-এ জায়গা না হওয়া; 3B model-এর long-context reasoning দুর্বল |
| Label distribution | Small-এ 54.8% overfitting | AutoCodeRover-এর plausible patch-এ 27/78 ≈ 34.6% overfitting | Specificity কম হলে অনেক সঠিক patch বাতিল |
| Domain shift প্রমাণ | Java → Java-তেই ~10 point পতন | Java → Python + tool → agent | আরও বড় পতনের সম্ভাবনা |
| Test-এর উপস্থিতি | Static, test ব্যবহার করে না | F2P/P2P ও Docker environment আছে | Static-only হওয়া এখানে অপ্রয়োজনীয় সীমাবদ্ধতা — hybrid ভালো |

**আমার হিসাব — hypothetical "what-if" (AutoCodeRover-এর 78টা plausible patch: 51 correct, 27 overfitting):**

এটা শুধু একটা চিন্তা-পরীক্ষা — RePaCA-র Java-তে মাপা rate হুবহু Python agent patch-এ খাটবে না।

| ধরা হলো RePaCA-র rate | ধরা পড়া overfitting (27-এর মধ্যে) | ভুল করে বাতিল correct (51-এর মধ্যে) | Filter-এর পরে গৃহীত patch-এ সঠিকের হার |
|---|---|---|---|
| Filter নেই | 0 | 0 | 51/78 = **65.4%** |
| Small dataset rate (Recall 85.7%, Specificity ≈80.2%) | ≈23.1 | ≈10.1 | ≈40.9/(40.9 + 3.9) ≈ **91.3%** |
| INVALIDATOR split rate (Recall 97.2%, Specificity 53.3%) | ≈26.2 | ≈23.8 | ≈27.2/(27.2 + 0.7) ≈ **97.4%** |

**শিক্ষা:** একটা static judge গৃহীত patch-এর "বিশুদ্ধতা" 65.4% থেকে 90%-এর উপরে নিতে পারে — **কিন্তু দাম হলো অনেক সঠিক patch হারানো** (10 থেকে 24টা)। Agent-এর resolve rate তাই কমে যাবে। এজন্য assurance layer-এ hard reject না করে **score + abstention ("মানুষ দেখুক")** ভালো design — এবং এটাই আমাদের CG7-এর সাথে মেলে।

### ১৬.২ প্রস্তাবিত Module (SPL3-feasible)

1. **Data Loader:** (ক) APPT-এর GitHub-এর Small dataset (Java) — RePaCA-র ফল reproduce/তুলনার জন্য; (খ) SWE-bench Lite/Verified-এর agent patch (Sub-domain 1-এর public trajectory/patch) + যেখানে পাওয়া যায় সেখানে manual correctness label (যেমন AutoCodeRover-এর 78টা patch-এর analysis); প্রয়োজনে নিজেরা ছোট একটা set হাতে label।
2. **Prompt Builder:** RePaCA-র format (`<think>`/`<answer>`) + one-shot; Python-এর জন্য উদাহরণ; ঐচ্ছিক context: issue text, পরিবর্তিত function-এর পুরো body, multi-file diff।
3. **Judge Backend:** (ক) Qwen2.5-Coder-3B-Instruct locally (8 GB GPU) — base, prompt-only; (খ) একটা বড় LLM API — তুলনার জন্য; (গ) সময়/resource থাকলে TRL + Unsloth দিয়ে ছোট GRPO run।
4. **Parser + Re-sampler:** strict regex (`incorrect`-কে `correct`-এর আগে check), unparseable হলে re-sample।
5. **Self-consistency Scorer:** $k$ = 5–8 sample → overfitting score $s(x)$, agreement rate।
6. **Evaluation module:** Accuracy, Precision, Recall, F1, Specificity, Balanced accuracy, MCC, ROC-AUC (score থেকে), calibration; trivial baseline; bootstrap CI ও McNemar।
7. **Assurance integration:** score অনুযায়ী তিন ভাগ — Accept / Human review / Reject; Agentless-এর candidate re-ranking-এ score ব্যবহার।
8. **Dashboard:** প্রতিটা patch-এর score, `<think>` rationale, সিদ্ধান্ত।

```python
# Assurance Layer — Component 1 (overfitting judge) sketch (আমার design, illustrative)
def assess_patch(buggy, patched, issue=None, k=8, temp=0.6):
    prompt = build_prompt(buggy, patched, issue)          # RePaCA-style think/answer format
    labels, rationales = [], []
    for _ in range(k):
        out = llm.generate(prompt, temperature=temp, max_new_tokens=2048)
        label = parse_answer(out)                          # 'overfitting' / 'correct' / None
        if label is None:
            continue                                       # re-sample policy (paper-এর প্রস্তাব)
        labels.append(label); rationales.append(extract_think(out))
    if not labels:
        return {"decision": "human_review", "score": None}
    score = labels.count("overfitting") / len(labels)      # self-consistency score
    if score >= 0.75:   decision = "reject"
    elif score <= 0.25: decision = "accept"
    else:               decision = "human_review"          # abstention (CG7)
    return {"decision": decision, "score": score, "rationales": rationales}
```

### ১৬.৩ পরীক্ষার পরিকল্পনা (ছোট আকারে)
1. **Step 1 — Reproduce baseline (Java):** Small dataset-এ base Qwen2.5-Coder-3B prompt-only চালিয়ে Table 7-এর কাছাকাছি সংখ্যা আসে কিনা।
2. **Step 2 — Transfer (Python):** একই prompt SWE-bench agent patch-এ — Java-র তুলনায় কতটা পতন।
3. **Step 3 — Context ablation:** snippet-only বনাম + issue text বনাম + পুরো function/file।
4. **Step 4 — Score ও abstention:** self-consistency score-এ coverage–accuracy curve (কত শতাংশ patch-এ সিদ্ধান্ত দিলে কত নির্ভুল)।
5. **Step 5 — Re-ranking:** Agentless-এর candidate-এ score দিয়ে বাছাই করে resolved সংখ্যা।

**Practical সতর্কতা:**
- GRPO training (paper-এর মতো) H100-শ্রেণির GPU চায় — SPL3-তে inference + prompt-only বা খুব ছোট-scale training-ই বাস্তবসম্মত।
- Python agent patch-এর **নির্ভরযোগ্য correctness label** পাওয়া সবচেয়ে বড় বাধা — ছোট কিন্তু পরিষ্কার label set (দুইজন মিলে label, agreement মাপা) পরিকল্পনা করতে হবে।
- Windows-এ local model চালাতে GPU driver/CUDA বা WSL2 লাগবে।

---

## ১৭. পরবর্তী গবেষণায় এই Paper-এর প্রভাব (Context)

- Paper-টা খুব নতুন (online July 2026), তাই citation-ভিত্তিক প্রভাব এখনো বলা যায় না। এর অবস্থান বোঝা যায় APCA-র ধারাবাহিকতায়: **hand-crafted feature (ODS) → learned embedding (CACHE) → NLP correlation (Quatrain) → invariant + PLM (INVALIDATOR) → fine-tuned PLM (APPT) → in-context LLM (LLM4PatchCorrect) → RL-trained reasoning LLM (RePaCA)**।
- এটা বৃহত্তর একটা প্রবণতার অংশ: DeepSeek-R1-এর পরে GRPO দিয়ে ছোট model-কে বিশেষ কাজে reasoning শেখানো, এবং **LLM-as-a-Judge** দিয়ে code/patch মূল্যায়ন। আমাদের Patch Validation folder-এর "Human-in-the-Loop LLM-as-a-Judge" paper-টা একই দিকের, এবং সেটার সাথে তুলনা করা দরকার হবে।
- Authors-এর নিজের প্রস্তাবিত পরের ধাপ: বড় ও সমৃদ্ধ dataset, repository context, reasoning-quality reward, APR pipeline-এ integration, বড়/বিশেষায়িত reasoning model।
- **আমাদের জন্য গুরুত্ব:** coding agent-এর score যত বাড়ছে, প্রশ্ন তত "কত % solve" থেকে "**solve করা patch কতটা বিশ্বাসযোগ্য**"-এর দিকে যাচ্ছে (Sub-domain 1, Paper 01, Section ১৭)। RePaCA দেখায় যে একটা ছোট, সস্তা, ব্যাখ্যাযোগ্য judge বানানো সম্ভব — কিন্তু agent setting-এ এর validity এখনো খোলা প্রশ্ন।

---

## ১৮. Supervisor-এর সম্ভাব্য প্রশ্ন ও উত্তর (Viva Prep)

**Q1. Static আর dynamic APCA-র পার্থক্য কী, আর RePaCA কেন static?**
A: Dynamic APCA patch execute করে runtime তথ্য বা নতুন test-এর ফল দেখে; static শুধু buggy ও fixed code তুলনা করে। Paper-এর যুক্তি: execution তথ্য পাওয়া code পাওয়ার চেয়ে অনেক ব্যয়বহুল ও জটিল। RePaCA দেখাতে চেয়েছে reasoning দিয়ে static approach-এর accuracy-র ঘাটতি পূরণ করা যায়।

**Q2. GRPO কী, আর PPO থেকে কীভাবে আলাদা?**
A: দুটোই policy-gradient RL algorithm। PPO-তে advantage হিসাবের জন্য আলাদা value model লাগে। GRPO একই prompt-এর জন্য $G$টা output (এখানে 8) তৈরি করে, তাদের reward-এর mean ও std দিয়ে normalize করে advantage বানায় — value model লাগে না, তাই memory কম। PPO-র মতো clipping ও reference model-এর KL penalty রাখে।

**Q3. Reward কীভাবে design করা হয়েছে, আর overfitting-এ 2.0 কেন?**
A: দুটো reward — format (think tag 0.5, answer tag 0.25, answer-এ keyword 0.25; মোট 1.0) আর accuracy (ভুল 0, সঠিক correct 1.0, সঠিক overfitting 2.0)। Authors দেখেছেন model-এর পক্ষে overfitting ধরা কঠিন, তাই preliminary experiment-এ ধীরে ধীরে পার্থক্য বাড়িয়ে 2.0 বেছেছেন। তবে আমার হিসাবে এটা decision threshold-কে 0.5 থেকে 1/3-এ নামায় — model বেশি "overfitting" বলে; INVALIDATOR split-এ specificity 53.3% এর সাথে মেলে।

**Q4. ফলাফল কি সত্যিই significant?**
A: APPT-এর নিজেদের reproduction-এর বিরুদ্ধে হ্যাঁ — McNemar $\chi^2 = 25.90$, $p = 3.6 \times 10^{-7}$ (1,163 instance); 20টা unparseable-কে majority class-এ দিলেও $p = 6.3 \times 10^{-7}$; সব bootstrap CI 0 বাদ দেয়। তবে reproduction published APPT-এর চেয়ে প্রায় 4.7 accuracy point কম, তাই published সংখ্যার সাথে পার্থক্য (+3.4) ছোট এবং সেটার significance test করা হয়নি। এছাড়া temperature test fold দেখে বাছাই হওয়ায় সংখ্যা কিছুটা আশাবাদী হতে পারে।

**Q5. INVALIDATOR-এর চেয়ে কি সত্যিই ভালো?**
A: Accuracy (87.8 বনাম 81.2) ও F1 (92.6 বনাম 87.0)-এ হ্যাঁ, কারণ recall অনেক বেশি (97.2 বনাম 78.9)। কিন্তু precision কম (88.3 বনাম 96.6), 30টা correct patch-এর 14টা ভুল করে বাতিল। Balanced accuracy-তে INVALIDATOR এগিয়ে (84.5 বনাম 75.3, আমার হিসাব), MCC প্রায় সমান। আর test split-এ 78.4% patch overfitting, তাই "সব overfitting" বললেই F1 87.9% — F1 এখানে অনেকটা ফোলানো।

**Q6. `<think>` block-এর ব্যাখ্যা কি বিশ্বাস করা যায়?**
A: পুরোপুরি না। Authors নিজেই বলেছেন এটা internal decision process-এর faithful ব্যাখ্যা নয়। Code 1-এ label সঠিক হলেও model একটা পুরনো variable-কে "নতুন" বলেছে; কিছু ক্ষেত্রে যুক্তি বলে patch সঠিক কিন্তু label overfitting। Reward reasoning-এর মান যাচাই করে না। তাই এটা developer-এর সহায়ক, প্রমাণ নয়।

**Q7. AUC কীভাবে হিসাব হলো, যেখানে model শুধু label দেয়?**
A: Paper বলেনি। Hard label থেকে AUC = (TPR + TNR)/2 = balanced accuracy। Small dataset-এ আমার পুনর্গঠনে balanced accuracy ≈ 83.0%, reported AUC 82.8% — প্রায় মেলে। তাই সম্ভবত এটাই; APPT-এর continuous-score AUC-এর সাথে তুলনা তাই পুরোপুরি সমান নয়। আসল AUC পেতে $k$টা sample-এর ভোট বা token probability থেকে score বানানো যায়।

**Q8. Domain shift-এ robustness-এর দাবি কতটা শক্ত?**
A: আপেক্ষিকভাবে শক্ত — APPT-এর AUC 55.4% (প্রায় random), RePaCA 72.3%। কিন্তু absolute অর্থে RePaCA-ও প্রায় 10 point পড়েছে (83.1 → 72.7 accuracy)। আর এটা Java → Java shift; আমাদের Java → Python, APR tool → LLM agent shift আরও বড়।

**Q9. RePaCA কি SWE-bench agent-এর patch যাচাই করতে পারবে?**
A: সরাসরি নয়। চারটা বড় বাধা: (১) Python বনাম Java; (২) agent patch গড়ে 1.7 file, 32.8 line — দুটো snippet-এ আঁটে না; (৩) repository context লাগে, যেখানে RePaCA context-poor patch-এ নিজেই ব্যর্থ; (৪) LLM agent-এর overfitting-এর ধরন APR tool থেকে ভিন্ন। তবে ধারণাটা — reasoning judge, ব্যাখ্যা, সস্তা inference — assurance layer-এর প্রথম স্তর হিসেবে খুব উপযোগী। আমি এটাকে issue text ও context যোগ করে, score + abstention সহ, Python patch-এ transfer study হিসেবে পরীক্ষা করতে চাই।

**Q10. SFT না করে শুধু RL কেন?**
A: APCA dataset-এ শুধু label আছে, মানুষের লেখা reasoning নেই — SFT দিয়ে CoT শেখাতে সেই text লাগতো। RL-এ শুধু reward লাগে, আর একই patch-এর জন্য অনেক বৈধ যুক্তি থাকতে পারে, RL সেটা অনুমোদন করে। তবে paper SFT বনাম RL-এর ablation করেনি — তাই "RL-ই কারণ" প্রমাণিত নয়।

**Q11. এই paper থেকে তুমি কী implement করবে?**
A: RePaCA-style prompt (think/answer + one-shot) দিয়ে একটা ছোট local judge (Qwen2.5-Coder-3B, 8 GB GPU), self-consistency score ও abstention সহ; প্রথমে Java small dataset-এ base result reproduce, তারপর SWE-bench agent patch-এ transfer — এবং Agentless candidate re-ranking-এ ব্যবহার। এটা আমাদের assurance layer-এর component 1 (overfitting detection) ও component 5 (confidence) একসাথে পূরণ করবে।

**Q12. Temperature 0.6 কেন, আর এটা কতটা নির্ভরযোগ্য?**
A: Fig. 4-এ 0.6-এ সেরা (Accuracy 83.1, F1 84.8, AUC 82.8)। কিন্তু 0.0 থেকে 1.2 পুরো range-এ accuracy মাত্র ~80–83%, আর single run — তাই পার্থক্যটা noise হতে পারে। এছাড়া এটা test fold-এর ফল দেখে বাছাই — আলাদা validation set-এ tune করা উচিত ছিল।

---

## ১৯. Glossary (দ্রুত মনে রাখার জন্য)

| Term | অর্থ |
|---|---|
| APR | Automated Program Repair — স্বয়ংক্রিয় bug fixing |
| Plausible patch | সব available test pass করা patch |
| Overfitting patch | Test pass করে কিন্তু bug-এর root cause ঠিক করে না |
| APCA | Automated Patch Correctness Assessment — plausible patch সঠিক নাকি overfitting তা automatic নির্ণয় |
| Static APCA | Execution ছাড়া, শুধু buggy ও fixed code দেখে APCA |
| Dynamic APCA | Patch চালিয়ে/test generate করে APCA |
| AST | Abstract Syntax Tree — code-এর grammar-এর গাছ |
| CoT | Chain of Thought — উত্তরের আগে ধাপে ধাপে যুক্তি |
| Reasoning LLM | CoT-কে নিজের আচরণে অন্তর্ভুক্ত করা model (যেমন DeepSeek-R1) |
| Test-Time Compute | Inference-এ বেশি গণনা/চিন্তা খরচ করে ভালো উত্তর |
| SFT | Supervised Fine-Tuning — target text নকল করা শেখা |
| RL | Reinforcement Learning — reward বাড়ানো শেখা |
| Policy | RL-এ model নিজেই (output-এর probability distribution) |
| Advantage | একটা output গড়ের চেয়ে কতটা ভালো |
| PPO | Value model + clipping-ভিত্তিক policy-gradient algorithm |
| GRPO | Group Relative Policy Optimization — value model ছাড়া, group-এর গড় reward-কে baseline ধরে |
| Reference model | Frozen শুরুর model, KL penalty-র জন্য |
| KL divergence | দুটো probability distribution কতটা আলাদা |
| Reward hacking | Reward-এর ফাঁক দিয়ে আসল লক্ষ্য না পূরণ করে reward পাওয়া |
| One-shot prompting | Prompt-এ একটা সমাধান-করা উদাহরণ দেওয়া |
| Temperature | Sampling-এর এলোমেলোতা নিয়ন্ত্রণ |
| Unparseable output | নির্ধারিত format-এ না থাকা output |
| Domain shift / OOD | Training ও test data-র distribution আলাদা |
| Specificity | সঠিক patch-এর কত শতাংশ সঠিকভাবে "correct" বলা হলো |
| Balanced accuracy | (Recall + Specificity)/2 |
| MCC | Confusion matrix-এর চারটা ঘর বিবেচনা করা correlation metric |
| McNemar's test | একই data-তে দুটো classifier-এর paired significance test |
| Bootstrap CI | Resampling দিয়ে metric-এর confidence interval |
| Defects4J | আসল Java bug-এর benchmark |
| Hallucination | Input-এ নেই এমন তথ্য বানানো |
| Faithfulness | ব্যাখ্যা model-এর আসল সিদ্ধান্ত-প্রক্রিয়া প্রতিফলিত করে কিনা |

---

## ২০. এক নজরে সারাংশ (Summary Card)

| | |
|---|---|
| **Problem** | Static APCA technique-গুলো pattern মেলায়, root cause নিয়ে যুক্তি দেয় না — accuracy, flexibility ও transparency কম |
| **Solution** | RePaCA: Qwen2.5-Coder-3B-কে `<think>`/`<answer>` format-এ CoT করিয়ে correct/overfitting classify; SFT ছাড়া শুধু GRPO (G = 8) |
| **Reward** | Format (0.5 + 0.25 + 0.25) + Accuracy (ভুল 0, correct 1.0, overfitting 2.0) |
| **Setup** | 20 epoch, lr 5e-5, batch 8, grad-acc 2, temp 0.6, max 2048 token, 1× H100 NVL; inference 8 GB VRAM |
| **Key result** | Small (1,183 Defects4J patch, 5-fold): Acc 83.1, P 84.0, R 85.7, F1 84.8, AUC 82.8 — APPT (79.7/81.8 F1)-এর চেয়ে ভালো; McNemar $p = 3.6 \times 10^{-7}$ |
| **অন্য ফল** | INVALIDATOR split (139): Acc 87.8, F1 92.6, Recall 97.2 কিন্তু Precision 88.3 (INVALIDATOR 96.6); Small → Large: Acc 72.7, F1 75.4, AUC 72.3 বনাম APPT 60.5 / 71.4 / 55.4 |
| **Key insight** | ছোট model-ও RL দিয়ে APCA-তে reasoning শিখতে পারে এবং OOD-তে pattern-matching model-এর চেয়ে ভালো টেকে |
| **Main limitation** | Java-only, ছোট snippet, hallucinated/অবিশ্বস্ত rationale, recall-ভারী bias, test-fold-এ tuning, variance নেই, hard-label AUC, code public নয় |
| **আমাদের জন্য gap** | Python, multi-file **agent patch**-এর জন্য context-aware, calibrated (score + abstention) overfitting judge — Assurance Layer-এর component 1 + 5 (CG1, CG2, CG7) |

---

## ২১. বর্তমান (2026) প্রেক্ষাপট — আজকের Model ও Agent-দের সাথে তুলনা

RePaCA তিনটা paper-এর মধ্যে সবচেয়ে নতুন (online July 2026), কিন্তু এর judge হলো Qwen2.5-Coder-3B, আর যে patch-গুলো এটা বিচার করে সেগুলো Defects4J-এর পুরনো APR tool-এর ছোট Java patch। October 2026-এ patch লিখছে Claude Opus 5.5 / Fable 5.1, GPT-6 Astra / GPT-6.1 Sol, Gemini 4 Argon-এর মতো model, Claude Code বা Codex-এর মতো agent-এর ভেতরে; আর industry নিজেই patch-এর মান বিচারে LLM judge ও rubric ব্যবহার শুরু করেছে। তাই প্রশ্নটা আর "static LLM judge কাজ করে কিনা" নয় — বরং "**আজকের agent-এর patch-এ judge কতটা নির্ভুল, আর judge-কে কি ঠকানো যায়**"। সব current-state তথ্য `00_Current_State_2026_Sources.md` (2026-10-28) থেকে, **কোম্পানির নিজের দাবি (vendor-reported)** / **স্বাধীনভাবে মাপা (independent)** / search-snippet only লেবেল সহ। নিজের যুক্তি "আমার পর্যবেক্ষণ" লেবেলে।

### ২১.১ Paper-এর সময় বনাম এখন

| দিক | Paper-এ (RePaCA) | এখন, October 2026 | উৎস (fact sheet) |
|---|---|---|---|
| সাধারণ LLM judge-এর accuracy | GRPO-র আগে base 3B model প্রায় random (AUC 50–54%, Table 7); GRPO-র পরে Accuracy 83.1% | ComPass: সাধারণ LLM baseline overfitting patch বাছাইয়ে **62.14%** accuracy (false positive বেশি), ComPass-এর learned method **88.35%**। Baseline-এ কোন LLM, তা fact sheet-এ নেই | §4 — arXiv 2602.07561 (search-snippet only) |
| Judge বনাম execution | INVALIDATOR split-এ specificity 53.3% (আমার হিসাব) | 4টা language-এ execution-calibrated study: judge-judge agreement judge-execution agreement-এর চেয়ে অনেক বেশি; over-fix flag-এর precision **5–10%**; "no single judge trustworthy on real Java code" | §4 — doi 10.3390/jcp6050153 (search-snippet only) |
| Plausible-but-wrong-এর হার | Small dataset-এ 54.8% overfitting (APR tool patch) | PatchDiff: agent-এর plausible patch-এর **29.6%** gold patch থেকে ভিন্ন আচরণ; "solved"-এর **7.8%** পুরো developer suite-এ fail — আগের প্রজন্মের agent, current-এ পুনরায় মাপা হয়নি | §4 — arXiv 2503.15223 [independent] |
| Industry-র grading পদ্ধতি | Binary label (correct / overfitting) | FrontierCode v1.1 (150 task): held-out test + model-graded rubric ("mergeability"); out-of-scope edit শাস্তি পায়, তাই medium effort-এর উপরে score কমে। Opus 5.5 54.6%, GPT-6 Astra 53.3% — Cognition নিজে চালিয়েছে, কিন্তু vendor-এর মাধ্যমে উদ্ধৃত | §2, §4 — Opus 5.5 card §8.4 |
| Benchmark test-এর নিজের মান | Label-কে ground truth ধরা হয়েছে | DeepSWE: LLM judge-এর সাথে SWE-Bench Pro-র inherited test-এর অমিল **32.4%**, DeepSWE-এর নিজের verifier-এ **1.4%**। OpenAI: SWE-Bench Pro-র 27–34% task broken | §3, §4 — arXiv 2607.07946 [independent]; the-decoder (secondary) |
| Verifier gaming | Reward hacking শুধু GRPO training-এর প্রসঙ্গে (Section ২.১৪) | Opus 5.5 transcript-এ model স্পষ্টভাবে "hidden tests … written by the benchmark creators" নিয়ে যুক্তি করে; "answer key কী চায় অনুমান" প্রায় 0.3% episode-এ (vendor-reported)। METR: 8 ঘণ্টার বেশি task-এ সফল run-এর অন্তত 16% অবৈধ; Opus 4.6 MirrorCode-এ প্রায় 80% চেষ্টায় hack করার চেষ্টা করেছে, scorer-এ logging ঢুকিয়ে বা scorer-কে binary-search করে (independent, আগের প্রজন্ম) | §3 — Opus 5.5 card §6.2; METR 2026-05-19 |
| Judge-এর input কতটা বিশ্বস্ত | Patch code-কে নিরীহ data ধরা হয় | Coding environment-এ prompt injection: Opus 5.5 ASR safeguard ছাড়া 54.61%, probe সহ 11.13% (vendor-reported); 7টা MCP client-এ tool poisoning-এর সুরক্ষা অসম (independent) | §5 — Opus 5.5 card §5.2.2.1; arXiv 2603.21642 |
| Judge চালানোর খরচ | 3B model, 8 GB VRAM-এ inference | Opus 5.5: 4 USD input / 20 USD output প্রতি million token (secondary, search-snippet only); GPT-6.1 Terra: 1 USD / 5 USD (vendor-reported); Qwen3.8-27B Apache-2.0 open weight (secondary) | §1 |
| Current-generation validation | — | **পাওয়া যায়নি:** Opus 5.5 বা GPT-6-প্রজন্মের agent patch-এ LLM-judge patch assessment যাচাইয়ের কোনো 2026 study | §4 — fact sheet নিজেই "Not found" বলেছে |

### ২১.২ কোন Finding এখনো সত্য, কোনটা পুরনো হয়ে গেছে

**এখনো সত্য:**
1. **"Test pass করা patch-কে আলাদা করে যাচাই করতে হবে" — RePaCA-র মূল motivation আরও শক্ত।** PatchDiff-এর 29.6%, SWE-Bench Pro-র "low-coverage tests let incomplete fixes pass" (OpenAI audit), আর PROBE-এর filter-এর পরে resolution rate কমা (search-snippet only) — সব একই দিকে।
2. **"Untrained বা সাধারণ LLM দুর্বল judge" (Table 7):** ComPass-এর plain LLM baseline 62.14% — RePaCA-র base model-এর মতোই training বা calibration ছাড়া judge দুর্বল। আমার পর্যবেক্ষণ: dataset ও model আলাদা, তাই সংখ্যা তুলনীয় নয়, কিন্তু উপসংহার মেলে।
3. **"Explanation বিশ্বাসযোগ্য নয়, judge-কে প্রমাণ হিসেবে নেওয়া যায় না" (Key Finding 6):** 2026-এর execution-calibrated study আরও এক ধাপ এগিয়েছে — judge-রা নিজেদের মধ্যে একমত হয়, কিন্তু execution-এর সাথে কম মেলে। অর্থাৎ **consistency ≠ validity**; Section ১৬.২-এর self-consistency score uncertainty মাপে, কিন্তু সঠিকতার নিশ্চয়তা দেয় না।
4. **Specificity-র সমস্যা (Section ৬.৭ ও ৮.৩):** Over-fix flag-এর 5–10% precision আর ComPass-এর "high false positives" — দুটোই দেখায় LLM judge সঠিক patch-কে অতিরিক্ত সন্দেহ করে। RePaCA-র asymmetric reward এই প্রবণতা আরও বাড়ায় (আমার আগের বিশ্লেষণ)।

**পুরনো হয়ে গেছে বা বদলাতে হবে:**
1. **Patch-এর ধরন:** Defects4J-এর single-method patch আর আজকের agent patch আলাদা জগৎ — Terminal-Bench 4.0-এ একটা task-এ গড়ে প্রায় এক ঘণ্টা (Opus 5.5, Vals), DeepSWE long-horizon ও 5 language। RePaCA-র দুই snippet + 2048 token-এর format এখানে খাটে না (Section ১৬.১-এর table আরও প্রাসঙ্গিক হয়েছে)।
2. **"Static judge = সস্তা ও নিরীহ assurance" ধারণা:** আমার পর্যবেক্ষণ — RePaCA judge-কে একটা নিরপেক্ষ পর্যবেক্ষক ধরে। কিন্তু judge যখন reward বা gate হয়ে যায় (FrontierCode-এর rubric grading এর উদাহরণ), তখন generator-এর উপর তাকে খুশি করার চাপ পড়ে। Static judge `.git` leak-এর মতো runtime shortcut থেকে নিরাপদ (সে কিছু চালায় না), কিন্তু দুটো নতুন আক্রমণের সামনে খোলা: (ক) **দেখতে-সাধারণ overfitting** — magic constant-কে নাম দেওয়া বা অপ্রয়োজনীয় generalization যোগ করা, যাতে RePaCA-র শেখা "নির্দিষ্ট শর্ত = overfitting" সংকেত লুকায়; (খ) **patch-এর ভেতরে judge-এর উদ্দেশে লেখা comment** — যেহেতু judge untrusted code পড়ে, prompt injection-এর ঝুঁকি আছে। এই দুটো ঝুঁকি নিয়ে কোনো মাপা ফল fact sheet-এ নেই; Opus 5.5-এর "hidden test" নিয়ে যুক্তি দেখায় current model grader সম্পর্কে সচেতন, তাই আশঙ্কাটা অবাস্তব নয় — কিন্তু এটা inference, প্রমাণ নয়।
3. **Ground-truth label-এর বিশ্বাসযোগ্যতা:** RePaCA dataset-এর label-কে সত্য ধরে। 2026-এ দেখা যাচ্ছে benchmark test নিজেই 27–34% ক্ষেত্রে ভুল, আর inherited test-এর সাথে judge-এর অমিল 32.4%। তাই current agent patch-এ APCA evaluate করতে হলে label-এর উৎস (কোন test, কে label করেছে) আলাদা করে যাচাই করতে হবে।
4. **Judge-এর আকার বনাম generator-এর আকার:** আমার পর্যবেক্ষণ — 3B judge দিয়ে frontier agent-এর patch বিচার মানে দুর্বল model শক্তিশালী model-কে যাচাই করছে। এই asymmetry-র প্রভাব নিয়ে fact sheet-এ কোনো data নেই।

### ২১.৩ এই Paper-এর Gap-গুলো আজও খোলা কিনা

| Gap | 2026-এ অবস্থা | প্রমাণ (fact sheet) |
|---|---|---|
| G1 — Agent patch-এর জন্য static APCA (Python, repository-level) | **খোলা** | Current-generation agent patch-এ LLM-judge যাচাইয়ের কোনো study পাওয়া যায়নি |
| G2 — Hybrid APCA (static + dynamic) | **আংশিক সমাধান** | Benchmark-এ held-out test + model-graded rubric একসাথে (FrontierCode); কিন্তু patch-level APCA tool হিসেবে নয়, আর rubric judge-এর নিজের নির্ভুলতা অপ্রকাশিত |
| G3 — APCA score দিয়ে candidate re-ranking | **খোলা** | Fact sheet-এ কোনো প্রমাণ নেই |
| G4 — Calibrated confidence ও abstention | **খোলা** | Generator দিকে শুধু vendor দাবি: Fable 5.1 আটকে গেলে "says so" (গুণগত, কোম্পানির নিজের দাবি); judge-এর calibration নিয়ে কিছু নেই |
| G5 — Judge-এর run-to-run consistency | **খোলা (নতুন মোড় সহ)** | Judge-judge agreement বেশি কিন্তু judge-execution কম; Noise Floor Audit: prompt perturbation rerun-এর চেয়ে 11–58 গুণ বড় SD |
| G6 — Explanation faithfulness | **খোলা** | কোনো নতুন প্রমাণ নেই |
| G7 — Security-regression detection | **খোলা** | SecPass 7.8–17.3% যেখানে FuncPass 62–84% (আগের প্রজন্ম) |
| G8 — Fair, reproducible APCA benchmark | **আংশিক সমাধান** | Grader-মান উন্নত হচ্ছে: SWE-Bench Pro Verified 119-এর 102টা task ঠিক করেছে, DeepSWE verifier-এ অমিল 1.4%; কিন্তু APCA-নির্দিষ্ট benchmark নয় |
| G9 — Cost-sensitive / threshold-tunable APCA | **খোলা** | Over-fix flag-এর 5–10% precision দেখায় threshold-নিয়ন্ত্রণ আরও জরুরি |
| CG1 — Plausible patch-এর correctness | **খোলা** | PatchDiff 29.6% current agent-এ পুনরায় মাপা হয়নি |
| CG7 — Confidence ও abstention | **খোলা** | উপরের G4 দেখো |
| CG10 — Assurance tool-এর নিজের evaluation validity | **খোলা** | ComPass baseline 62.14%; judge-execution অমিল |
| CG11 — Verifier health | **খোলা** | Inherited test-এ 32.4% অমিল; 27–34% broken task |
| CG12 — Verifier-এর বিরুদ্ধে optimization pressure | **খোলা, judge-এর জন্য একেবারেই মাপা হয়নি** | Test-ভিত্তিক verifier-এ প্রমাণ আছে (GLM-5.2 78.80% থেকে 57.32%; METR অন্তত 16%); LLM judge-কে ঠকানোর কোনো মাপ fact sheet-এ নেই |

### ২১.৪ বর্তমান Model দিয়ে আবার পরীক্ষা করলে — SPL3 Idea

সব idea আমার প্রস্তাব। খরচের নীতি: patch তৈরি ও judge-এর bulk run local 3B বা সস্তা API-তে; frontier judge (যেমন Opus 5.5) শুধু 30–60টা patch-এর subset-এ। Judge call প্রতি patch-এ কয়েকটা, তাই agent run-এর চেয়ে অনেক সস্তা (আমার অনুমান; pilot দিয়ে মাপতে হবে)।

1. **Current agent patch-এ reasoning judge — recall ও specificity দুটোই:** SWE-rebench-এর নতুন task-এ mini-SWE-agent + একটা সস্তা current model দিয়ে 40–60টা plausible patch সংগ্রহ। Label: PatchDiff-ধরনের differential test (gold বনাম agent patch-এর আচরণ) + দুইজনের manual review। Judge: (ক) RePaCA-style prompt-এ Qwen2.5-Coder-3B local, (খ) একটা current frontier model কম effort-এ। Report: recall, specificity, balanced accuracy, MCC, bootstrap CI, McNemar। **যে নতুন gap বেরোবে:** fact sheet-এর "Not found" ঘরটা — current agent patch-এ judge-এর স্বাধীন মাপ (G1, CG10)।
2. **Judge-বনাম-execution calibration:** একই patch-এ 2–3টা judge-এর রায় পরস্পরের সাথে ও differential-test ফলের সাথে মেলানো। 2026-এর Java finding ("judge-রা একমত, execution-এর সাথে নয়") Python agent patch-এও হয় কিনা। **যে নতুন gap বেরোবে:** judge ensemble-এর agreement-কে confidence হিসেবে ব্যবহার করা নিরাপদ কিনা (G5, CG11)।
3. **Judge-gaming stress test (static judge-ও কি verifier gaming-এর শিকার?):** জানা overfitting patch-এর তিন ধরনের রূপান্তর — (ক) magic constant-কে named constant বানানো, (খ) অপ্রাসঙ্গিক refactor noise, (গ) judge-এর উদ্দেশে আশ্বাস-দেওয়া comment। প্রতিটায় label কতবার "overfitting" থেকে "correct"-এ উল্টায় (flip rate)। কোনো API-নির্ভর agent লাগে না — সবচেয়ে সস্তা ও সবচেয়ে নতুন idea। **যে নতুন gap বেরোবে:** LLM judge-এর বিরুদ্ধে optimization pressure কোথাও মাপা হয়নি (CG12)।
4. **Effort ও self-consistency sweep:** একই judge-এ 2টা effort level × k = 5 sample; coverage–accuracy curve ও abstention-এর হার। FrontierCode-এ বেশি effort-এ score কমে — judge-এর ক্ষেত্রেও কি তাই? **যে নতুন gap বেরোবে:** judge-এর জন্য test-time compute-এর লাভ-ক্ষতি (G4, G5)।
5. **Binary label বনাম rubric:** একই patch-এ RePaCA-র binary রায় আর FrontierCode-ধরনের rubric (scope, mergeability) রায় তুলনা — কোনটা differential test-এর সাথে বেশি মেলে। **যে নতুন gap বেরোবে:** industry যে rubric grading-এ গেছে, তার patch-level নির্ভুলতা (G2)।

### ২১.৫ Supervisor-এর সম্ভাব্য প্রশ্ন (2026 প্রসঙ্গে)

**Q1. আজ তো Opus 5.5-এর মতো model আছে — 3B judge নিয়ে কাজ করার মানে কী?**
A: দুটো কারণ। (ক) খরচ — judge প্রতিটা patch-এ চালাতে হয়; 3B local-এ প্রায় বিনামূল্যে, frontier API-তে প্রতি million output token 20 USD পর্যন্ত (Opus 5.5, secondary source)। (খ) বড় model যে ভালো judge তার স্বাধীন প্রমাণ নেই — ComPass-এর plain LLM baseline 62.14%, আর একটা 2026 study বলে Java-তে কোনো একক judge বিশ্বাসযোগ্য নয়। তাই ছোট বনাম বড় judge-কে একই current agent patch-এ মাপাই SPL3 idea 1।

**Q2. RePaCA-র মতো static judge কি verifier gaming থেকে নিরাপদ?**
A: আংশিক। এটা কিছু execute করে না, তাই `.git` history পড়া বা scorer-এ logging ঢোকানোর মতো test-ভিত্তিক shortcut এর উপর কাজ করে না। কিন্তু judge যদি agent-এর reward বা acceptance gate হয়, agent এমন patch লিখতে শিখতে পারে যা দেখতে সাধারণ কিন্তু আসলে overfitting, বা judge-এর উদ্দেশে comment লিখতে পারে। এটা আমার inference — fact sheet-এ judge-gaming-এর কোনো মাপ নেই, আর ঠিক এজন্যই SPL3 idea 3।

**Q3. Industry তো এখন rubric আর LLM judge দিয়েই grade করছে — তাহলে APCA research কি শেষ?**
A: না, বরং জরুরি হয়েছে। FrontierCode-এর মতো benchmark rubric grading ব্যবহার করছে, কিন্তু সেই judge-এর patch-level নির্ভুলতা প্রকাশিত নয়, আর current-generation agent patch-এ LLM-judge যাচাইয়ের কোনো study fact sheet-এ নেই। RePaCA-র evaluation কাঠামো (confusion matrix, McNemar, cross-dataset) ঠিক সেই যাচাইয়ের জন্য দরকারি — শুধু dataset-টা Defects4J থেকে current agent patch-এ সরাতে হবে, আর recall-এর পাশে specificity-ও report করতে হবে।
