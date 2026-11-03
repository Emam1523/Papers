# Paper Analysis 02: SWE-agent — Agent-Computer Interfaces Enable Automated Software Engineering

> **Sub-domain:** AI Coding Agents (এই sub-domain-এর ২য় paper; ১ম paper SWE-bench-এর benchmark-এর উপর এটা প্রথম বড় "agent")
> **Analysis করেছে:** SPL3 — AI Coding Agent Reliability and Assurance
> **Paper file:** `AI Coding Agents/SWE-agent-Agent-Computer Interfaces Enable.pdf`

---

## ০. Paper-এর পরিচয় (Bibliographic Info)

| বিষয় | তথ্য |
|---|---|
| **Title** | SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering |
| **Authors** | John Yang, Carlos E. Jimenez (দুজনের equal contribution), Alexander Wettig, Kilian Lieret, Shunyu Yao, Karthik Narasimhan, Ofir Press |
| **Institution** | Princeton Language and Intelligence, Princeton University |
| **Venue** | NeurIPS 2024 (38th Conference on Neural Information Processing Systems) — AI/ML-এর top-tier conference। arXiv: 2405.15793 (v3, Nov 2024) |
| **Paper type** | **System + Empirical paper** — নতুন model train করা হয়নি; বরং LLM-এর জন্য একটা নতুন **interface (ACI)** design করে তার প্রভাব experiment ও ablation দিয়ে মাপা হয়েছে |
| **Artifacts** | পুরো SWE-agent code (open-source), configuration file, সব trajectory, patch, evaluation log, analysis notebook (swe-agent.com) |
| **আমাদের domain-এ গুরুত্ব** | ⭐⭐⭐⭐⭐ — SWE-bench-এ প্রথম বড় **interactive coding agent**। "Agent কীভাবে কাজ করে, কোথায় ভুল করে, কীভাবে guardrail দিয়ে ভুল কমানো যায়" — এই প্রশ্নগুলো আমাদের **Reliability ও Assurance** domain-এর একদম কেন্দ্রে। Trajectory ও failure-mode analysis পরের সব reliability কাজের ভিত্তি। |

---

## ★ সহজ ভাষায় পুরো Paper (প্রথমবার পড়ার জন্য)

### ক. Paper-টা কী নিয়ে?

- এটা একটা **নতুন tool/system-এর paper**, সাথে অনেক experiment (পরীক্ষা) আছে।
- বানিয়েছে Princeton University-র একটা দল (John Yang, Carlos Jimenez, Ofir Press ও আরও কয়েকজন)। ছাপা হয়েছে NeurIPS 2024-এ, যেটা AI-এর খুব বড় একটা conference।
- Paper-এর নাম SWE-agent। এটা এমন একটা "agent" (যে LLM নিজে নিজে ধাপে ধাপে computer চালিয়ে কাজ করে)।
- নতুন করে কোনো AI model train করা হয়নি। একই model নিয়ে শুধু তার কাজ করার "workspace" বদলানো হয়েছে।
- আগের Paper 01 (SWE-bench) ছিল পরীক্ষার প্রশ্নপত্র। এই paper হলো সেই পরীক্ষায় বসা প্রথম বড় "ছাত্র"।

### খ. সমস্যাটা কী ছিল?

- LLM-কে GitHub-এর একটা সত্যিকারের bug ঠিক করতে দিলে সে প্রায় সবসময় ব্যর্থ হতো। Paper 01-এর সবচেয়ে ভালো সিস্টেমও ১০০টার মধ্যে মাত্র ৪টার মতো পারতো।
- সরাসরি Linux terminal দিলেও তেমন লাভ হতো না। কারণ terminal বানানো হয়েছে মানুষের জন্য, LLM-এর জন্য নয়।
- **উদাহরণ:** `cat` command পুরো file একবারে screen-এ ঢেলে দেয়। হাজার হাজার line পড়তে গিয়ে LLM-এর "মাথা" ভরে যায় এবং সে আসল জায়গা হারিয়ে ফেলে।
- আরেকটা সমস্যা: `sed` দিয়ে edit করলে কিছুই বলে না। ভুল হলে LLM বুঝতেই পারে না, আর একই ভুল বারবার করতে থাকে।
- **সাধারণ উপমা:** একজন চালককে এমন গাড়ি দিলে যার dashboard-এ কিছুই লেখা নেই। চালক ভালো হলেও দুর্ঘটনা ঘটবে।

### গ. Paper কী solve করেছে?

- **ACI** নামে একটা নতুন ধারণা দিয়েছে। মানে LLM-এর জন্য বিশেষভাবে বানানো একটা "IDE"।
- ACI-তে আছে ছোট ও সহজ search command, একবারে ১০০ line দেখানো file viewer, আর ভুল edit আটকানো একটা linter (code-এর বানান-ভুল ধরার tool)।
- পুরনো output ছেঁটে ফেলা হয়, যাতে LLM-এর মাথা হালকা থাকে।
- Ablation করে (একটা একটা অংশ সরিয়ে) দেখিয়েছে কোন অংশ কতটা কাজে লাগে।
- Agent কোথায় ব্যর্থ হয় সেটাও বিশ্লেষণ করেছে।
- **সংখ্যা ১: 12.47%** (full SWE-bench)। মানে ১০০টা bug-এর মধ্যে প্রায় ১২টা ঠিক হয়েছে। আগের সেরা ছিল 3.8%, অর্থাৎ প্রায় ৪টা।
- **সংখ্যা ২: 18.00% বনাম 11.00%** (Lite সেট)। সাধারণ terminal দিলে ১১টা, ACI দিলে ১৮টা। মানে একই model-এ relative 64% বেশি।
- **সংখ্যা ৩: pass@1 = 17.94% কিন্তু pass@6 = 32.67%।** মানে একই task ৬ বার চালালে প্রায় দ্বিগুণ task অন্তত একবার solve হয়। অর্থাৎ agent আজ পারে, কাল পারে না। Reliability-র জন্য এটাই সবচেয়ে বড় সতর্কবার্তা।

### ঘ. কীভাবে solve করেছে?

1. **আগে সমস্যা দেখেছে।** Dev set-এর অল্প কিছু bug-এ agent চালিয়ে দেখেছে সে কোথায় আটকায়।
2. **৪টা design নিয়ম বানিয়েছে।** Command সহজ হবে, ছোট হবে, feedback সংক্ষিপ্ত কিন্তু কাজের হবে, আর ভুল ছড়াতে দেওয়া হবে না।
3. **Search command সহজ করেছে।** `find_file`, `search_dir`, `search_file`। ৫০টার বেশি result এলে দেখানো হয় না, আরও নির্দিষ্ট করে খুঁজতে বলা হয়।
4. **File viewer বানিয়েছে।** একবারে ১০০ line দেখায়, line number দেয়, আর কত line উপরে-নিচে আছে বলে দেয়।
5. **Edit command বানিয়েছে।** `edit n:m` দিয়ে এক command-এ line n থেকে m বদলানো যায়। বদলানোর পর flake8 চালানো হয়; syntax ভুল থাকলে edit বাতিল হয়ে যায়।
6. **History ছোট রাখে।** শুধু শেষ ৫টা output পুরো থাকে, পুরনোগুলো এক লাইনে "Old output omitted" হয়ে যায়।
7. **Agent loop চালায়।** প্রতি turn-এ LLM একটা thought ও একটা command দেয়। Docker container (আলাদা নিরাপদ বাক্স) সেটা চালায় এবং ফল ফেরত দেয়।
8. **শেষে মেপেছে।** `submit` করলে সব edit মিলে একটা patch হয়। SWE-bench-এর test দিয়ে সেটা যাচাই হয়। তারপর ablation, trajectory ও failure analysis করা হয়েছে।

### ঙ. এরপর কী করা যায়?

- **Authors যা বলেছেন:** আরও tool যোগ করা (web browsing, static analysis, fuzzing)। আর ACI হাতে না বানিয়ে automatically বানানো।
- **এখনো খোলা:** Agent-এর patch আসলে ঠিক কিনা, তা শুধু test দিয়ে বোঝা যায় না। Linter শুধু syntax দেখে, logic-এর ভুল ধরে না।
- **এখনো খোলা:** একই task-এ ফল কেন বদলায়, আর প্রথম approach ব্যর্থ হলে agent কেন নতুন পথ নেয় না।
- **আমরা SPL3-তে পারি:** SWE-agent-এ regression test, security scan ও test-tamper (test file বদলানো) detection-এর একটা assurance layer যোগ করে আগে-পরে তুলনা করতে পারি।
- **আমরা পারি:** একই config ৩ বার চালিয়ে pass^k ও flip rate মাপতে।
- **আমরা পারি:** Paper-এর open-source trajectory দিয়ে (API খরচ ছাড়াই) failure আগে থেকে অনুমান করার একটা classifier বানাতে।

> **মনে রাখো:**
> Model একই রেখে শুধু interface (ACI) ভালো করলেই SWE-bench-এ ফল 11% থেকে 18% হয়ে যায়।
> কিন্তু agent-এর patch শুধু test pass করলেই বিশ্বাসযোগ্য নয়, আর একই task-এ ফল প্রতিবার বদলায়।
> এই দুই ফাঁক (assurance ও reliability) থেকেই আমাদের SPL3-এর কাজ শুরু।

---


## ১. এক লাইনে Paper (TL;DR)

**LLM-কে সরাসরি Linux shell দিলে সে software engineering-এ ভালো করে না; কিন্তু LLM-এর জন্য বিশেষভাবে বানানো একটা interface — যাকে authors বলছেন Agent-Computer Interface (ACI) — দিলে (সহজ search command, 100-line-এর file viewer, linter-সহ edit command, পুরনো output collapse করা) একই LLM SWE-bench-এ 12.47% issue solve করে, যেখানে আগের সেরা non-interactive system করতো 3.8%।**

**সহজ কথায়:** প্রতিটা শব্দ খুলে বললে: LLM-কে একটা ভালো "workspace" দিলে সে অনেক বেশি কাজ করতে পারে। Workspace-এ ছোট command, ছোট করে file দেখা আর ভুল edit আটকানোর ব্যবস্থা আছে। ফলে ১০০টা bug-এর মধ্যে ১২টা ঠিক হয়, যেখানে আগে ঠিক হতো মাত্র ৪টার মতো।

### Supervisor-কে ৩০ সেকেন্ডে কীভাবে বলবো
> "Sir, Paper 01 (SWE-bench)-এ আমরা দেখেছি LLM-কে একবারে কিছু file দিয়ে patch লিখতে বললে Claude 2 মাত্র 1.96% পারে। SWE-agent paper বলছে — model বদলানোর দরকার নেই, **model যে interface দিয়ে computer ব্যবহার করে সেটা বদলাও**। মানুষের জন্য যেমন VSCode আছে, LLM-এর জন্যও তেমন একটা 'IDE' দরকার — যাকে তারা বলছে Agent-Computer Interface। এতে আছে ছোট ও সহজ search command, একবারে 100 line দেখায় এমন file viewer, একটা edit command যেটা syntax error থাকলে edit-টা বাতিল করে দেয়, আর পুরনো output ছেঁটে context ছোট রাখা। ফলাফল: GPT-4 Turbo দিয়ে full SWE-bench-এ 12.47% (286/2,294), SWE-bench Lite-এ 18.00%, যা সাধারণ Linux shell দেওয়া agent-এর (11.00%) চেয়ে relative 64% বেশি। Ablation (একটা একটা অংশ সরিয়ে দেখা কতটা কাজে লাগে) দিয়ে তারা দেখিয়েছে প্রতিটা design choice কতটা কাজে লাগে, আর trajectory (agent-এর পুরো কাজের রেকর্ড) বিশ্লেষণ করে দেখিয়েছে agent কোথায় ব্যর্থ হয় — failure-এর অর্ধেকের বেশি হলো ভুল বা অতি-নির্দিষ্ট implementation। আমাদের reliability research-এর জন্য এটা গুরুত্বপূর্ণ কারণ এটা দেখায় agent-এর আচরণ শুধু model নয়, **environment design**-এর উপরও নির্ভর করে।"

---

## ২. Background — এই paper বুঝতে যা আগে জানা দরকার

SWE-bench, Issue/PR, Patch, F2P/P2P test, Resolved metric, BM25, Context window, Contamination, Greedy decoding — এগুলো **Paper 01 দেখো**। এখানে শুধু এই paper-এর **নতুন** concept-গুলো ব্যাখ্যা করা হলো।

### ২.১ LM Agent ও Agent Loop
- **সাধারণ LLM ব্যবহার (non-interactive):** একবার prompt দাও → একবার উত্তর নাও। Paper 01-এর RAG baseline এরকম।
- **LM Agent:** LLM একটা **environment**-এর (এখানে computer/terminal) সাথে বারবার **interact** করে — একটা কাজ (action) করে, তার ফল (observation/feedback) দেখে, তারপর পরের কাজ ঠিক করে।
- **Agent loop:** "ভাবো → কাজ করো → ফল দেখো → আবার ভাবো" — এই চক্র যতক্ষণ না কাজ শেষ হয় বা budget ফুরায়।
- মানুষের সাথে তুলনা: একজন developer যেমন file খোলে, পড়ে, edit করে, test চালায়, error দেখে আবার ঠিক করে — agent-ও তেমন করে।

### ২.২ ReAct (Reasoning + Acting)
Yao et al. (এই paper-এর co-author Shunyu Yao)-এর একটা প্রচলিত prompting পদ্ধতি। প্রতিটা step-এ model দুটো জিনিস লেখে:
1. **Thought:** "এখন কী করা উচিত এবং কেন" — natural language-এ চিন্তা।
2. **Action:** একটা নির্দিষ্ট command (যেমন `open sessions.py`)।
তারপর environment একটা **Observation** ফেরত দেয়। SWE-agent-এ প্রতিটা turn-এ ঠিক **একটা thought ও একটা action** বাধ্যতামূলক (system prompt-এ এটাকে "DISCUSSION" ও command block বলা হয়েছে)।

### ২.৩ Agent-Computer Interface (ACI) — এই paper-এর মূল concept
- **UI (User Interface):** মানুষের জন্য বানানো (যেমন VSCode, GUI)।
- **API:** অন্য software-এর জন্য বানানো।
- **ACI:** authors-এর প্রস্তাবিত নতুন category — **LM agent-কে একটা নতুন ধরনের "end user"** হিসেবে ধরে তার জন্য বানানো interface।
- ACI দুটো জিনিস ঠিক করে: (ক) agent কোন **command** ব্যবহার করতে পারবে (action space) এবং (খ) environment-এর অবস্থা agent-কে **কোন format-এ** দেখানো হবে (feedback)। এছাড়া ACI পুরো **history** track করে এবং প্রতিটা step-এ কোনটা কীভাবে model-এর input-এ যাবে তা ঠিক করে।
- কেন আলাদা interface দরকার? মানুষ অপ্রয়োজনীয় তথ্য চোখ দিয়ে এড়িয়ে যেতে পারে, কিন্তু LLM-এর কাছে প্রতিটা token-এর memory ও compute খরচ আছে, আর অপ্রাসঙ্গিক context performance কমায়। আবার তখনকার LLM GUI-এর visual তথ্য ভালো বুঝতো না।
- **গুরুত্বপূর্ণ:** paper-এ LLM-এর weight **fixed** — শুধু interface বদলে performance বাড়ানো হয়েছে।

**সহজ কথায়:** ACI হলো LLM-এর জন্য বানানো একটা IDE। মানুষের VSCode যেমন মানুষের সুবিধা ভেবে বানানো, ACI তেমন LLM-এর সুবিধা ভেবে বানানো।

### ২.৪ Action, Observation, Turn, Trajectory
| Term | মানে |
|---|---|
| **Action** | Agent-এর দেওয়া একটা command (যেমন `search_dir "PVSystem"`) |
| **Observation** | Command চালানোর পর environment যা দেখায় (output) |
| **Turn / Step** | একটা (thought, action, observation) চক্র |
| **Trajectory** | একটা task-এর শুরু থেকে শেষ পর্যন্ত সব turn-এর পুরো রেকর্ড — agent কী ভেবেছে, কী করেছে, কী দেখেছে। SWE-agent প্রতিটা task-এর trajectory `.traj` file হিসেবে save করে। |
| **Episode** | একটা task instance-এর পুরো run |

Trajectory আমাদের reliability research-এর জন্য সোনার খনি — agent কেন fail করলো তা এখান থেকে বিশ্লেষণ করা যায়।

### ২.৫ Linux Shell, InterCode ও "Shell-only" Baseline
- **InterCode** (Yang et al., একই group-এর আগের কাজ): LLM-কে একটা interactive coding environment (যেমন Bash) দেওয়ার framework।
- **Shell-only agent:** LLM শুধু সাধারণ Linux command (`cd`, `ls`, `cat`, `grep`, `find`, `sed`) দিয়ে কাজ করে। এটাই paper-এর মূল **baseline agent**। এখানে সমস্যা: `cat` পুরো file দেখিয়ে context ভরিয়ে দেয়, `sed` দিয়ে multi-line edit কঠিন, আর edit করলে কোনো feedback আসে না ("silent")।

### ২.৬ Linter ও Guardrail
- **Linter:** code না চালিয়েই code-এর syntax ও কিছু সাধারণ ভুল ধরার tool। Python-এর জনপ্রিয় linter **flake8**।
- **Guardrail:** এমন একটা নিরাপত্তা-বাঁধ যেটা agent-কে একটা নির্দিষ্ট ভুল করতে দেয় না। SWE-agent-এ: edit করার পর flake8 চালানো হয়; syntax error থাকলে **edit বাতিল** (apply হয় না) এবং agent-কে error message দেখানো হয়।
- **Error propagation / cascading error:** একটা ভুল edit (যেমন ভুল indentation) পরের অনেক step নষ্ট করে — agent বারবার একই জায়গা edit করতে থাকে। Guardrail এই "ধারাবাহিক ভুল" থামায়।

### ২.৭ Context Management ও History Collapsing
- প্রতিটা turn-এ LLM-কে **পুরো আগের history** (system prompt + issue + আগের সব thought/action/observation) আবার পাঠাতে হয়। Turn যত বাড়ে, input তত লম্বা হয় → খরচ বাড়ে, context window ভরে যায়, model বিভ্রান্ত হয়।
- **History processor:** কোন পুরনো message কীভাবে রাখা হবে তা ঠিক করে।
- **Collapsing:** SWE-agent শেষ **5টা** observation পুরো রাখে; তার আগেরগুলোর content একটা এক-লাইনের placeholder দিয়ে বদলে দেয় — যেমন "Old output omitted (101 lines)"। Thought ও action থেকে যায়, তাই plan-এর ইতিহাস হারায় না, কিন্তু পুরনো (এবং হয়তো outdated) file content চলে যায়।
- Paper 01-এ দেখেছি বেশি context performance কমায় (*lost in the middle*) — এটা সেই সমস্যারই agent-version সমাধান।

### ২.৮ Demonstration (In-context Example)
Prompt-এ একটা **সফল trajectory-র উদাহরণ** দেখানো (few-shot learning-এর মতো)। SWE-agent dev set-এর একটা সফল trajectory demonstration হিসেবে দেয়। Authors-এর মতে এর মূল কাজ সম্ভবত সঠিক **format-এ command দেওয়া শেখানো**, domain জ্ঞান শেখানো নয়।

### ২.৯ Temperature ও Decoding
- **Temperature = 0:** প্রায় greedy decoding (Paper 01 দেখো) — সবচেয়ে সম্ভাব্য token বাছাই।
- **Temperature > 0 (যেমন 0.2):** কিছু randomness — একই input-এ ভিন্ন output।
- লক্ষ্য করো: temperature 0 হলেও API-ভিত্তিক model-এ run-to-run পার্থক্য থাকতে পারে (paper-এর 6 run-এর পার্থক্য এটা দেখায়)।

### ২.১০ Pass@1, Pass@k ও Variance (Paper 01-এ সংক্ষেপে ছিল, এখানে বিস্তারিত)
- **Pass@1 / % Resolved:** একবার চেষ্টায় কত % task সফল।
- **Pass@k:** k বার স্বাধীনভাবে চালালে **অন্তত একবার** সফল হওয়ার হার। k বাড়লে pass@k বাড়ে।
- **Variance:** একই system বারবার চালালে score কতটা ওঠানামা করে। Reliability-র জন্য এটা খুব গুরুত্বপূর্ণ। (সূত্র Section ৬-এ)

### ২.১১ Cost Budget ও API Cost
- GPT-4 Turbo বা Claude 3 Opus API-তে প্রতি input/output token-এর জন্য টাকা লাগে।
- Agent অনেক turn চালায়, প্রতি turn-এ লম্বা history পাঠায় → খরচ RAG-এর চেয়ে অনেক বেশি।
- **Per-instance budget:** প্রতিটা task-এ সর্বোচ্চ **4 USD**। এটা পেরিয়ে গেলে episode থেমে যায় এবং তখন পর্যন্ত করা edit স্বয়ংক্রিয়ভাবে submit হয় (`exit_cost`)।

### ২.১২ SWE-bench Lite
SWE-bench-এর 300টা task-এর একটা canonical subset, যেখানে মূলত **self-contained functional bug fix** রাখা হয়েছে। সস্তায় ablation চালানোর জন্য ব্যবহার হয়েছে। (Full SWE-bench = 2,294 task — Paper 01 দেখো।)

### ২.১৩ HumanEvalFix
- HumanEval-এর (164টা ছোট programming problem) একটা **bug-fixing** version — OctoPack (Muennighoff et al.) কাজের অংশ।
- প্রতিটা problem-এ একটা function-এ bug ঢোকানো আছে; model-কে bug ঠিক করতে হয়; test দিয়ে যাচাই হয়।
- Language: Python, JS, Go, Java, C++, Rust (paper ব্যবহার করেছে Python, JS, Java)।
- Paper-এর উল্লেখ অনুযায়ী Muennighoff et al. দেখিয়েছিলেন GPT-4 HumanEval-এ 78.3% কিন্তু HumanEvalFix-এ 47.8% — অর্থাৎ debugging, নতুন code লেখার চেয়ে কঠিন।
- এখানে বড় codebase navigate করতে হয় না — তাই এটা agent-এর শুধু **editing ability** মাপে।

### ২.১৪ Docker Container ও Sandbox
Agent যে command চালায় তা একটা **isolated container**-এ চলে, যাতে ভুল command (যেমন `rm -rf`) host computer নষ্ট না করে। প্রতিটা task-এর জন্য নতুন ephemeral container। Reproducibility ও safety দুটোর জন্য দরকার।

### ২.১৫ Reproduction Script ও Localization
- **Reproduction:** issue-তে বলা bug নিজের environment-এ আবার ঘটিয়ে দেখা — সাধারণত `reproduce.py` নামে ছোট script লিখে চালানো।
- **Localization:** codebase-এর কোন file/line-এ bug আছে তা খুঁজে বের করা (Paper 01-এ এটাকেই মূল bottleneck বলা হয়েছিল)।

### ২.১৬ Hyperparameter Sweep / Grid Search
কয়েকটা setting-এর (যেমন temperature, window size, history) সব combination চালিয়ে দেখা কোনটা সবচেয়ে ভালো। Ablation-এর (Paper 01 দেখো) সাথে পার্থক্য: sweep-এ best setting বাছাই হয়; ablation-এ একটা অংশ সরিয়ে তার অবদান মাপা হয়।

### ২.১৭ LM-as-a-Judge (Automatic Labeling)
একটা LLM (এখানে GPT-4o)-কে দিয়ে অন্য agent-এর trajectory পড়িয়ে failure-এর category ঠিক করানো। মানুষের label-এর সাথে কতটা মেলে (**agreement**) তা দিয়ে judge-এর বিশ্বাসযোগ্যতা মাপা হয়। (আমাদের *Patch Validation* sub-domain-এর HITL LLM-as-a-Judge paper-এ এটা বিস্তারিত আসবে।)

### ২.১৮ Precision, Recall, F1 (File-level Localization)
Agent যে file গুলো edit করেছে আর gold patch যে file গুলো edit করেছে — এই দুই set কতটা মেলে তা মাপতে F1 ব্যবহার হয়েছে। (সূত্র Section ৬-এ)

---

## ৩. Problem Statement — কী সমস্যা ছিল?

### ৩.১ মূল সমস্যা
1. **Non-interactive approach খুব দুর্বল:** Paper 01-এর RAG baseline (BM25 দিয়ে file এনে একবারে patch লেখা) SWE-bench-এ সর্বোচ্চ ~3.8% (Claude 3 Opus দিয়ে)। Model code চালিয়ে দেখতে পারে না, ভুল হলে ঠিক করতে পারে না।
2. **Agent-কে সরাসরি Linux shell দিলেও ভালো হয় না:** Shell মানুষের জন্য বানানো, LLM-এর জন্য নয়। Authors-এর পর্যবেক্ষণ:
   - `cd`, `ls`, `cat` chain দিয়ে খোঁজা খুব অদক্ষ — অনেক turn নষ্ট।
   - `grep`/`find` অনেক সময় শত শত অপ্রাসঙ্গিক line দেয় → context ভরে যায়।
   - `cat` পুরো file দেখায়; `head`/`tail` দিয়ে নির্দিষ্ট অংশ দেখা জটিল; scroll করতে প্রতিবার line number হিসাব করতে হয়।
   - `sed` দিয়ে multi-line edit কঠিন ও error-prone; redirection দিয়ে পুরো file আবার লিখতে হয়।
   - Edit-এর পর কোনো feedback নেই ("silent") — ভুল হলে agent বুঝতে পারে না।
   - Syntax error হলে agent একই জায়গা বারবার edit করতে থাকে (cascading error)।

**সহজ কথায়:** Terminal-এর command গুলো মানুষের জন্য ঠিক আছে। কিন্তু LLM-এর জন্য এগুলো অনেক বেশি লেখা দেখায়, ভুল হলে চুপ থাকে, আর একই ভুল বারবার করায়।
3. **Interface design-এর প্রভাব কেউ systematically মাপেনি:** আগের কাজগুলো tool use, prompting, code execution আলাদা আলাদা দেখেছে, কিন্তু "interface design নিজেই agent-এর performance কতটা বদলায়" — এই প্রশ্ন unexplored।

### ৩.২ কেন এটা গুরুত্বপূর্ণ?
- নতুন model train করা খুব ব্যয়বহুল; interface design সস্তা ও যেকোনো model-এ প্রয়োগযোগ্য।
- HCI (Human-Computer Interaction) গবেষণা দেখিয়েছে ভালো interface মানুষের productivity অনেক বাড়ায় — LLM-এর ক্ষেত্রেও কি তাই? এটাই paper-এর মূল hypothesis।

---

## ৪. Goal ও Research Questions

**Goal:** LLM-এর জন্য software engineering-এর উপযোগী একটা interface (ACI) design করা, সেটা দিয়ে SWE-bench-এ state-of-the-art পাওয়া, এবং interface-এর প্রতিটা অংশ agent-এর আচরণ ও performance কীভাবে বদলায় তা বিশ্লেষণ করা।

Paper-এর implicit RQ (আমার ভাষায় সাজানো):
- **RQ1:** LLM-centric ACI কি মানুষের জন্য বানানো interface (Linux shell) ও non-interactive RAG-এর চেয়ে ভালো? (Table 1)
- **RQ2:** ACI-এর প্রতিটা component (search, file viewer, editor+linting, context management, demonstration) কতটা অবদান রাখে? (Table 3)
- **RQ3:** ACI কি অন্য model-এ (Claude 3 Opus) ও অন্য task-এ (HumanEvalFix) portable? (Table 1, Table 2)
- **RQ4:** Agent কীভাবে সমস্যা সমাধান করে — কোন action pattern দেখা যায়? (Figure 7, Table 8)
- **RQ5:** Agent কোথায় ও কেন ব্যর্থ হয়? (Figure 8, Table 9)
- **RQ6:** Performance কতটা stable (variance, pass@k) এবং খরচ কত? (Table 10, Table 1)

**Contribution (authors-এর দাবি অনুযায়ী দুটো):**
1. ACI concept-এর প্রস্তাব এবং দেখানো যে model-এর weight না বদলে শুধু ACI design দিয়ে performance অনেক বাড়ানো যায়।
2. SWE-agent system বানানো, evaluate করা এবং open-source করা।

---

## ৫. Methodology — কীভাবে কাজটা করা হয়েছে

### ৫.১ সামগ্রিক কাঠামো
| অংশ | কী | কাজ |
|---|---|---|
| **LM** | GPT-4 Turbo বা Claude 3 Opus (weight fixed) | প্রতি turn-এ thought + action তৈরি |
| **ACI** | Custom command + feedback format + history processor | LM ও computer-এর মাঝখানের "adapter" |
| **Environment** | Docker container-এ repository + Linux shell | Command চালানো, output ফেরত দেওয়া |
| **Output** | পুরো episode-এর সব edit থেকে তৈরি একটা `.patch` file | SWE-bench harness দিয়ে evaluate |

**সহজ কথায়:** SWE-agent মানে চারটা অংশ: LLM (চিন্তা করে), ACI (অনুবাদক), Docker (কাজের জায়গা) আর patch file (ফল)।

SWE-agent Linux shell-এর উপরেই বানানো, তাই custom command-এর পাশাপাশি সাধারণ bash command (`python`, `pytest`, `rm` ইত্যাদি)-ও ব্যবহার করা যায়।

### ৫.২ ACI-এর ৪টা Design Principle (paper-এর Section 2)
1. **Action সহজ ও বোঝার মতো হবে:** bash command-এর documentation-এ ডজন ডজন option থাকে; অল্প option ও ছোট documentation-এর command agent সহজে ব্যবহার করতে পারে — demonstration বা fine-tuning কম লাগে।
2. **Action compact ও efficient হবে:** গুরুত্বপূর্ণ কাজ (navigation, editing) যত কম action-এ সম্ভব হওয়া উচিত। খারাপ design = অনেক ছোট action জোড়া লাগিয়ে একটা বড় কাজ।
3. **Environment feedback informative কিন্তু সংক্ষিপ্ত:** agent-কে বর্তমান অবস্থা ও তার শেষ action-এর প্রভাব জানাতে হবে, অপ্রয়োজনীয় detail ছাড়া। (যেমন edit-এর পর file-এর নতুন অবস্থা দেখানো।)
4. **Guardrail ভুলের বিস্তার থামায় ও দ্রুত recovery করায়:** যেমন syntax checker, যেটা ভুল সাথে সাথে ধরে।

**সহজ কথায়:** ভালো ACI-র চার নিয়ম: সহজ command, কম ধাপে কাজ, ছোট কিন্তু কাজের feedback আর ভুল আটকানোর বাঁধ।

### ৫.৩ Design Process — ACI কীভাবে বানানো হলো
1. **Manual inspection:** SWE-bench-এর dev split থেকে হাতে বাছাই করা অল্প কিছু উদাহরণে agent চালানো, trajectory পড়ে কোথায় সমস্যা হচ্ছে তা দেখা, সেই অনুযায়ী command/prompt/tip বদলানো (HCI-এর user study-র মতো)।
2. **Grid search:** বাকি hyperparameter (window size, history processing, temperature) dev split-এর 37টা random instance-এ sweep করে বাছাই (Appendix B.1, Table 5)।
Authors স্বীকার করেছেন এই process **manual** — এটা automate করা future work।

### ৫.৪ ACI Component ১: Search ও Navigation
| Command | কাজ |
|---|---|
| `find_file <file_name> [<dir>]` | Repository-তে নির্দিষ্ট নামের file খোঁজে |
| `search_dir <search_term> [<dir>]` | একটা directory-র সব file-এ শব্দ খোঁজে; প্রতিটা file-এ কয়টা match তা দেখায় |
| `search_file <search_term> [<file>]` | একটা file-এ শব্দ খোঁজে; match-এর line number দেখায় (file না দিলে বর্তমান open file) |

- **কেন দুটো directory-level command?** Issue-তে কখনো file-এর নাম থাকে, কখনো class/function-এর নাম — দুই ধরনের keyword-এর জন্য দুই command।
- **Guardrail:** একটা search-এ **50টার বেশি result** হলে result দেখানো হয় না; বরং agent-কে আরও নির্দিষ্ট query লিখতে বলা হয়। Trade-off: context ছোট থাকে, কিন্তু agent-কে আরেকটা LM call করতে হয়।
- **Summarized output:** সব result একবারে, সংক্ষিপ্ত আকারে (file-এর নাম + match সংখ্যা)।

**সহজ কথায়:** Search-এর result খুব বেশি হলে LLM-এর মাথা ভরে যায়। তাই ৫০টার বেশি হলে আরও নির্দিষ্ট করে খুঁজতে বলা হয়।

### ৫.৫ ACI Component ২: File Viewer
| Command | কাজ |
|---|---|
| `open <path> [<line_number>]` | File খোলে; line number দিলে window সেই line-এ যায় |
| `goto <line_number>` | Window-কে নির্দিষ্ট line-এ নেয় |
| `scroll_down` / `scroll_up` | Window-কে 100 line নিচে/উপরে সরায় |

Viewer যা দেখায়:
- Open file-এর **পুরো path** ও **মোট line সংখ্যা** (যেমন "[File: solvers/diophantine.py (3093 lines total)]")
- Window-এর আগে ও পরে কত line বাদ আছে ("(400 lines above)", "(2684 lines below)")
- প্রতিটা line-এর আগে **line number**
- একবারে সর্বোচ্চ **100 line** (window size)

**কেন এভাবে?** `cat` context ভরিয়ে দেয়; `sed`/`head` দিয়ে পরের 100 line দেখতে agent-কে start/end line আবার হিসাব করতে হয় — LLM-এর এই arithmetic-এ ভুল হয়। Viewer stateful (`CURRENT_LINE` variable মনে রাখে), তাই agent-কে হিসাব করতে হয় না। Authors-এর rule of thumb: **action ও output এমনভাবে বানাও যাতে একটা আরেকটার উপর build করে এবং model-কে arithmetic করতে না হয়।**

**সহজ কথায়:** File viewer LLM-কে একটা ছোট জানালা দেয়। সে ১০০ line করে দেখে এবং কোন line-এ আছে নিজেই মনে রাখে, তাই তাকে অঙ্ক কষতে হয় না।

### ৫.৬ ACI Component ৩: File Editor (edit + linting guardrail)
| Command | কাজ |
|---|---|
| `edit <n>:<m>` ... `end_of_edit` | Open file-এর line n থেকে m (inclusive) replacement text দিয়ে বদলায় |
| `create <filename>` | নতুন file বানিয়ে খোলে (সাধারণত reproduction script-এর জন্য) |
| `submit` | সব edit থেকে patch বানিয়ে submit করে, episode শেষ |

**Edit-এর ধাপগুলো (step by step):**
1. Agent `edit 404:407` লিখে নতুন code দেয় (file viewer-এ দেখা line number ব্যবহার করে — আলাদা হিসাব লাগে না)।
2. Edit apply হয়।
3. নিচের linter command চালানো হয়:
```
flake8 --isolated --select=F821,F822,F831,E111,E112,E113,E999,E902 "$CURRENT_FILE" 2>&1
```
4. **কোনো error না হলে:** edit থেকে যায়, এবং file viewer edit-এর জায়গা ঘিরে updated content দেখায় (agent সাথে সাথে ফল দেখে)।
5. **Error হলে:** edit **revert** হয়, আর agent-কে একটা message দেখানো হয় যাতে থাকে — (ক) কোন error (যেমন "F821 undefined name 'orientation_strategy'"), (খ) edit apply হলে file দেখতে কেমন হতো, (গ) আসল code। শেষে বলা হয় "DO NOT re-run the same failed edit command"।

**Lint error code-এর মানে:**
| Code | মানে |
|---|---|
| F821, F822 | Undefined name/symbol |
| F831 | Function definition-এ duplicate argument |
| E111, E112, E113 | Indentation error |
| E999 | Syntax error |
| E902 | flake8 file পড়তে পারেনি |

- **ধারণা (assumption):** মূল codebase আগে থেকে syntactically ঠিক — তাই নতুন error মানে agent-এর edit-ই দোষী।
- **Error message-এর তিন অংশই দরকার** (authors-এর development অভিজ্ঞতা): error type না থাকলে agent ভুল diagnose করে; changed snippet না থাকলে একই command বারবার দেয়; original snippet না থাকলে অনেক পুরনো turn-এর content দেখে ভুল edit করে।
- **Guardrail-এর অসুবিধা (authors নিজেই বলেছেন):** কিছু edit নির্দিষ্ট ক্রমে করতে বাধ্য করে। যেমন একটা function argument মুছতে চাইলে, প্রথমে body থেকে সব reference মুছতে হবে, নইলে header থেকে মুছলেই F821 error আসবে এবং edit বাতিল হবে।

**সহজ কথায়:** Edit করলে সাথে সাথে বানান-ভুল পরীক্ষা হয়। ভুল থাকলে edit ফিরিয়ে নেওয়া হয় এবং agent-কে কারণ বলা হয়। এতে একটা ভুল পরের সব ধাপ নষ্ট করতে পারে না।

### ৫.৭ ACI Component ৪: Context Management
1. **Prompt:** system prompt-এ environment, command documentation ও response format; instance prompt-এ issue ও tips।
2. **Thought + Action বাধ্যতামূলক:** প্রতি turn-এ একটা DISCUSSION (thought) ও একটা command।
3. **Malformed response handling:** format ভুল হলে error message (Figure 32) দেখিয়ে আবার চেষ্টা করতে বলা হয়। Valid response পাওয়ার পর **প্রথমটা ছাড়া** আগের error message গুলো history থেকে মুছে দেওয়া হয় (de-noising)। পরপর কয়েকবার malformed হলে episode early exit (Appendix C-তে "3 malformed responses in a row" বলা আছে; Figure 26-এ "2+ consecutive format errors" — দেখো Section ১২.৩)।
4. **No-output message:** command কোনো output না দিলে (যেমন `rm`) agent-কে স্পষ্ট বলা হয় "Your command ran successfully and did not produce any output" — নইলে agent বিভ্রান্ত হয়ে অপ্রয়োজনীয় command চালায়।
5. **History collapsing:** শেষ 5টা observation-এর আগেরগুলো এক লাইনে collapse ("Old output omitted (N lines)")। লাভ: (ক) কম token → বেশি turn সম্ভব, (খ) outdated file content সরে যায়।

**সহজ কথায়:** প্রতি turn-এ পুরো ইতিহাস আবার পাঠাতে হয়। তাই পুরনো লম্বা output ছেঁটে ফেললে খরচও কমে, LLM-এর বিভ্রান্তিও কমে।

### ৫.৮ Agent Loop — একটা Episode কীভাবে চলে (Figure 9, Figure 26)
1. **Initial messages:** (১) System template → (২) Demonstration (ঐচ্ছিক; একটা সফল dev-set trajectory) → (৩) Instance template (issue text + instruction + tips)।
2. **Turn 1:** LM একটা thought + action দেয়।
3. **Execute:** ACI action-টা Docker container-এ চালায়।
4. **Feedback:** তিন ধরনের template-এর একটা —
   - Output থাকলে: "Next step" template (output + "(Open file: ...) (Current directory: ...) bash-$" prompt)
   - Output না থাকলে: "Next step (no output)" template
   - Response malformed হলে: "Format error" template
5. **History processing:** পুরনো observation collapse।
6. ধাপ ২–৫ পুনরাবৃত্তি।
7. **Termination (৪ ভাবে, Appendix B.9):** (ক) agent নিজে `submit` দেয়; (খ) cost limit (4 USD) পেরোয় ও edit থাকলে auto-submit; (গ) cost limit পেরোয় কিন্তু কোনো edit নেই → কিছু submit হয় না; (ঘ) পরপর অনেক malformed response → early exit।
8. **Patch:** সব edit-এর diff একটা `.patch` file হয় → SWE-bench harness-এ F2P/P2P test দিয়ে evaluate (Paper 01 দেখো)।

**সহজ কথায়:** একটা episode মানে: প্রম্পট দাও, LLM ভাবে ও command দেয়, Docker চালায়, ফল দেখে আবার ভাবে। এভাবে `submit` বা budget শেষ হওয়া পর্যন্ত চলে।

### ৫.৯ Prompt Template-গুলোর বিশেষ বৈশিষ্ট্য (Appendix C)
- **System template:** "You are an autonomous programmer..." — environment-এর বর্ণনা, সব command-এর documentation, indentation সম্পর্কে সতর্কতা, এক turn-এ একটাই command, interactive command (`python` REPL, `vim`) চলবে না।
- **Instance template-এর 6টা tip** (dev set-এ failure দেখে হাতে লেখা): (১) আগে bug reproduce করো, fix-এর পর আবার চালাও; (২) একটা command কাজ না করলে অন্য command চেষ্টা করো; (৩) দূরের line-এ যেতে বারবার scroll না করে `goto` ব্যবহার করো; (৪) কোনো input file লাগলে `find_file` দিয়ে খোঁজো; (৫) open file ও current directory সবসময় খেয়াল রাখো; (৬) edit-এর পর code দেখে নিশ্চিত হও।
- Authors বলেছেন tip লেখার এই manual পদ্ধতি scale করে না, কিন্তু "surprisingly effective"।

**সহজ কথায়:** Prompt-এর ছয়টা tip আসলে আগের ব্যর্থতা দেখে হাতে লেখা পরামর্শ, যেমন "আগে bug reproduce করো"।
- Response format তিন রকম পরীক্ষা করা হয়েছে: markdown code block, JSON (`thought`/`action` key), XML tag।

### ৫.১০ Implementation ও Configuration (Appendix A.2–A.3)
- **তিনটা module:** Environment (InterCode-ভিত্তিক, Docker), Agent (ACI render করে, API ও local model দুটোই support), Logging (trajectory ও patch save)।
- **Configuration file (.yaml)-এর চারটা অংশ:** (১) Prompt templates, (২) Command files (bash/Python function; docstring স্বয়ংক্রিয়ভাবে prompt-এ ঢোকে), (৩) Control flow (`parse_function`, `history_processor`), (৪) Environment variables (যেমন `CURRENT_FILE`, `CURRENT_LINE`, `WINDOW_SIZE` — interface-কে stateful করে)।
- নতুন command যোগ করতে একটা skeleton (signature, docstring, arguments) মেনে function লিখলেই হয় — তাই ACI নিয়ে experiment করা সহজ।

### ৫.১১ Baseline Setup
1. **RAG (Paper 01-এর মতো):** BM25 দিয়ে issue-কে query করে file আনা → model একবারে patch লেখে। Model: GPT-4 Turbo, Claude 3 Opus।
2. **Shell-only agent:** InterCode-এর Bash environment; শুধু সাধারণ Linux command; model-এর final codebase অবস্থা থেকে patch। Demonstration সহ ও ছাড়া দুটো version।

### ৫.১২ Analysis Methodology
- **Trajectory analysis:** resolved trajectory-তে প্রতিটা turn-এ কোন action কতবার — frequency, density, n-gram pattern (Table 8), transition probability heatmap (Figure 21–24)।
- **Failure analysis:** Lite-এর unresolved trajectory (n = 248) → authors 9টা category বানালেন (Table 9) → 15টা instance হাতে label করে validation set → GPT-4o-কে trajectory + agent-এর patch + gold patch দিয়ে category বলতে বলা → validation set-এ মানুষের সাথে 87% মিল।
- **Qualitative case study (Appendix D):** Lite থেকে 2টা সফল ও 2টা ব্যর্থ instance-এর পুরো trajectory বিশ্লেষণ।

**সহজ কথায়:** Authors শুধু সংখ্যা দেখেননি। Agent কোন command কখন দেয়, কোথায় ব্যর্থ হয় এবং হাতে ও GPT-4o দিয়ে ব্যর্থতার কারণ ভাগ করে দেখেছেন।

---

## ৬. Mathematical Formulation — সূত্র ও ব্যাখ্যা

Paper-এ explicit equation প্রায় নেই (এটা system/empirical paper)। নিচে আমি paper-এর কাজটা formal ভাবে লিখেছি, যাতে supervisor-কে precise ভাবে বোঝানো যায়। **৬.১–৬.৩-এর notation আমার নিজের সাজানো; paper-এর বর্ণনার সাথে মিলিয়ে লেখা।**

### ৬.১ Agent as a Policy (Agent-কে একটা Policy হিসেবে লেখা)
Turn $t$-এ history:
$$
h_t = \left(x_{\text{sys}},\; x_{\text{demo}},\; x_{\text{issue}},\; (r_1, a_1, o_1),\; \ldots,\; (r_{t-1}, a_{t-1}, o_{t-1})\right)
$$
LLM (parameter $\theta$, fixed) পরের thought ও action তৈরি করে:
$$
(r_t,\; a_t) = \text{Sample}\left(\pi_\theta\left(\cdot \mid \Phi(h_t)\right)\right)
$$
Environment action চালিয়ে নতুন state ও observation দেয়:
$$
(s_t,\; o_t) = \mathcal{E}(s_{t-1},\; a_t)
$$

**সহজ কথায়:** প্রথম সূত্র বলছে LLM পরের ধাপে কী করবে তা ঠিক করে এখন পর্যন্ত সব ঘটনা (history) দেখে। দ্বিতীয় সূত্রে LLM thought ও action বের করে। তৃতীয় সূত্রে environment সেই action চালিয়ে নতুন অবস্থা ও output দেয়। Φ হলো এই history-কে ছেঁটে LLM-এর জন্য সাজানোর ধাপ।

| Symbol | মানে |
|---|---|
| $x_{\text{sys}}, x_{\text{demo}}, x_{\text{issue}}$ | System prompt, demonstration, issue-সহ instance prompt |
| $r_t$ | Turn $t$-এর thought (reasoning, ReAct-এর "Thought") |
| $a_t$ | Turn $t$-এর action (একটা command) |
| $o_t$ | Action-এর পর environment-এর observation |
| $s_t$ | Environment-এর state (codebase-এর অবস্থা, open file, current line, working directory) |
| $\pi_\theta$ | LLM-এর policy — history দেখে পরের (thought, action)-এর probability distribution |
| $\Phi$ | **ACI-এর history processor + formatter** — raw history থেকে model-এর আসল input বানায় |
| $\mathcal{E}$ | Environment (Docker container-এ shell + ACI command) |

**ACI-কে তিনটা জিনিসের tuple হিসেবে দেখা যায় (আমার formalization):**
$$
\text{ACI} = (\mathcal{A},\; F,\; \Phi)
$$
- $\mathcal{A}$ = action space (কোন command আছে: `open`, `goto`, `edit`, `search_dir`...)
- $F$ = feedback formatter (output কোন format-এ দেখানো হবে: line number, "(N lines above)", lint message)
- $\Phi$ = history processor (কী রাখা হবে, কী collapse হবে)

**মূল insight এই notation-এ:** paper $\theta$ বদলায় না; শুধু $\mathcal{A}$, $F$, $\Phi$ বদলে performance বাড়ায়। Table 3-এর প্রতিটা ablation এই তিনটার একটা বদলানো।

### ৬.২ History Collapsing (Last-5 Observations)
Turn $t$-এ $i$-তম observation model-কে কীভাবে দেখানো হবে:
$$
\tilde{o}_i =
\begin{cases}
o_i, & \text{যদি } i > t - 1 - 5 \text{ (শেষ 5টা observation)} \\
\text{"Old output omitted (} n_i \text{ lines)"}, & \text{অন্যথায়}
\end{cases}
$$

**সহজ কথায়:** শেষ ৫টা observation পুরো রাখা হয়, বাকিগুলো এক লাইনের placeholder হয়ে যায়। এই সূত্র সেটাই লেখে।
$n_i$ = observation $o_i$-এর line সংখ্যা। Thought $r_i$ ও action $a_i$ সবসময় থাকে।

**কেন খরচ এত কমে — একটা কাল্পনিক উদাহরণ (সংখ্যাগুলো আমার ধরে নেওয়া, paper-এর নয়):**
ধরো initial prompt = 5,000 token, প্রতি turn-এ thought+action = 100 token, observation = 1,000 token, collapsed observation = 10 token। Turn 20-এ model-এর input:
- **Full history:** $5000 + 19 \times (100 + 1000) = 25{,}900$ token
- **Last-5:** $5000 + 19 \times 100 + 5 \times 1000 + 14 \times 10 = 12{,}040$ token

অর্থাৎ প্রায় অর্ধেক। আর যেহেতু **প্রতি turn-এ পুরো history আবার পাঠাতে হয়**, পুরো episode-এর মোট input token turn সংখ্যার সাথে প্রায় **quadratic** হারে বাড়ে — collapsing সেটাকে অনেক কমায়। এজন্যই একই 4 USD budget-এ বেশি turn চালানো যায়।

### ৬.৩ Episode Termination ও Patch
$$
T = \min \{\, t \;:\; a_t = \text{submit} \;\lor\; \text{Cost}_{1:t} \geq B \;\lor\; \text{consecutive format errors} \geq K \,\}
$$

**সহজ কথায়:** Episode থামে যখন agent `submit` দেয়, খরচ budget ছাড়ায় বা পরপর অনেক format ভুল হয়। এই তিনটার যেটা আগে ঘটে সেখানেই শেষ।
- $B$ = 4 USD (per-instance budget)
- $K$ = early-exit-এর সীমা (paper-এ 3 বলা আছে, একটা figure-এ 2+ — Section ১২.৩ দেখো)

Final patch:
$$
\hat{\delta} = \text{diff}(C_0,\; C_T)
$$
$C_0$ = শুরুর codebase, $C_T$ = episode শেষে codebase। তারপর $\text{Resolved}(\hat{\delta})$ ঠিক Paper 01-এর মতো (সব F2P ও P2P test pass করলে 1, নইলে 0)।

**লক্ষ্য করো:** agent যদি `reproduce.py` বানিয়ে না মোছে, সেটাও patch-এ ঢুকে যায় — এজন্যই agent-এর patch gold patch-এর চেয়ে বড় হয় (Table 11)। Prompt-এ "remove reproduce.py before submit" ধরনের আচরণ demonstration-এ দেখানো হয়েছে।

### ৬.৪ Resolve Rate (% Resolved = pass@1)
$$
\%\,\text{Resolved} = \frac{1}{N} \sum_{i=1}^{N} \text{Resolved}(\hat{\delta}_i) \times 100
$$

**সহজ কথায়:** মোট task-এর মধ্যে কতটা solve হয়েছে তার শতাংশ। যেমন ২২৯৪টার মধ্যে ২৮৬টা মানে 12.47%।
**Worked example (paper-এর আসল সংখ্যা):**
- Full SWE-bench, SWE-agent w/ GPT-4 Turbo: $\dfrac{286}{2294} \times 100 = 12.47\%$
- Lite, SWE-agent w/ GPT-4 Turbo: $\dfrac{54}{300} \times 100 = 18.00\%$
- Full SWE-bench, SWE-agent w/ Claude 3 Opus: $10.46\%$ → $2294 \times 0.1046 \approx 240$টা task

### ৬.৫ Relative Improvement, Fold Change ও Percentage Point
তিনটা আলাদা জিনিস — supervisor এখানে প্রশ্ন করতে পারেন:
$$
\text{Relative gain} = \frac{R_{\text{new}} - R_{\text{old}}}{R_{\text{old}}}, \quad \text{Fold} = \frac{R_{\text{new}}}{R_{\text{old}}}, \quad \Delta_{\text{pp}} = R_{\text{new}} - R_{\text{old}}
$$

**সহজ কথায়:** এখানে তিনটা আলাদা তুলনা আছে। Relative gain বলে পুরনো সংখ্যার তুলনায় কত শতাংশ বেড়েছে। Fold বলে কত গুণ হয়েছে। Percentage point বলে সরাসরি বিয়োগফল কত।
**Worked example (Lite, GPT-4 Turbo):**
- Shell-only (demo সহ) = 11.00%, SWE-agent = 18.00%: $\dfrac{18.00 - 11.00}{11.00} = 0.636 \approx 64\%$ relative gain — paper-এর "64% relative increase"।
- RAG = 2.67%: $\dfrac{18.00}{2.67} \approx 6.7$ গুণ — paper-এর "6.7-fold"।
- Shell-only **w/o demonstration** = 7.33%: $18.00 - 7.33 = 10.67 \approx 10.7$ percentage point — Introduction-এর "10.7 percentage points more than the baseline agent"।

**আমার পর্যবেক্ষণ:** "64%" ও "10.7 pp" দুটো **ভিন্ন baseline**-এর সাথে তুলনা (demo সহ বনাম demo ছাড়া Shell-only)। দুটোই সঠিক, কিন্তু presentation-এ এটা স্পষ্ট করা উচিত।

### ৬.৬ Ablation Effect
$$
\Delta_{\text{ablation}} = R(\text{variant}) - R(\text{default})
$$

**সহজ কথায়:** একটা অংশ সরালে default-এর তুলনায় কত percentage point কমে, সেটাই ablation effect।
Default (SWE-agent, Lite, GPT-4 Turbo) = 18.0%। যেমন linting সরালে: $15.0 - 18.0 = -3.0$ pp; edit command সরালে: $10.3 - 18.0 = -7.7$ pp। (Table 3-এর সব সংখ্যা Section ৮.৩-এ।)

### ৬.৭ Cost Metric
Turn $j$-এর খরচ (সাধারণ API pricing model; paper নির্দিষ্ট দাম বলেনি):
$$
\text{Cost}_{1:t} = \sum_{j=1}^{t} \left( p_{\text{in}} \cdot n^{\text{in}}_j + p_{\text{out}} \cdot n^{\text{out}}_j \right)
$$

**সহজ কথায়:** প্রতি turn-এর খরচ হলো input token ও output token-এর দাম আলাদা করে ধরে যোগফল। সব turn যোগ করলে মোট খরচ।
$p_{\text{in}}, p_{\text{out}}$ = প্রতি input/output token-এর দাম; $n^{\text{in}}_j, n^{\text{out}}_j$ = turn $j$-এ token সংখ্যা।

Paper-এর **Avg. Cost** = **শুধু resolved instance-গুলোর** গড় API খরচ (paper-এর definition):
$$
\bar{C} = \frac{1}{\text{count}(\text{resolved})} \sum_{i \in \text{resolved}} \text{Cost}_i
$$

**সহজ কথায়:** Paper-এর গড় খরচ শুধু সফল task-গুলোর। ব্যর্থ task-এর খরচ এতে ধরা নেই, তাই প্রকৃত খরচ এর চেয়ে বেশি।
**Worked example (paper-এর "8–13x more costly"):**
- GPT-4 Turbo, Lite: $\dfrac{1.67}{0.13} \approx 12.8$ গুণ
- Claude 3 Opus, Lite: $\dfrac{2.18}{0.25} \approx 8.7$ গুণ

**আমার নিজের rough estimate — প্রতি resolved issue-এ আসল খরচ (assumption স্পষ্ট):** Avg. Cost শুধু সফল task-এর খরচ গোনে, কিন্তু ব্যর্থ task-এও টাকা খরচ হয়, আর paper নিজেই বলছে ব্যর্থ run বেশি খরচ করে। Lite-এ GPT-4 Turbo: 54টা resolved (গড় 1.67 USD) + 246টা unresolved। Unresolved-এর খরচ সর্বোচ্চ 4 USD (budget cap) ধরলে:
$$
\frac{54 \times 1.67 + 246 \times 4}{54} \approx \frac{90.2 + 984}{54} \approx 19.9 \text{ USD per resolved issue (upper bound)}
$$
আর unresolved-এর গড় 2.52 USD ধরলে (paper-এর full-set-এর unsuccessful, budget শেষ না হওয়া run-এর mean — তাই এটা কম দিকের অনুমান):
$$
\frac{90.2 + 246 \times 2.52}{54} \approx \frac{90.2 + 619.9}{54} \approx 13.1 \text{ USD per resolved issue}
$$
অর্থাৎ **প্রতিটা সফল fix-এর আসল খরচ সম্ভবত ~13–20 USD**, যদিও paper-এর table-এ 1.67 USD দেখায়। এটা paper-এর দাবি নয়, আমার হিসাব — তবে cost-aware evaluation-এর জন্য গুরুত্বপূর্ণ পয়েন্ট।

### ৬.৮ Run-to-run Mean ও Standard Deviation (Table 10)
6টা run-এর resolve rate $R_1, \ldots, R_6$:
$$
\bar{R} = \frac{1}{n} \sum_{j=1}^{n} R_j, \quad \sigma = \sqrt{\frac{1}{n} \sum_{j=1}^{n} \left(R_j - \bar{R}\right)^2}
$$

**সহজ কথায়:** ৬ বার চালানোর গড় এবং সেই ৬টা সংখ্যা গড় থেকে গড়ে কতটা সরে, তার হিসাব। SD ছোট মানে গড় ফল প্রায় স্থির।
**Worked example (paper-এর আসল সংখ্যা):** $R = (17.33, 18.00, 18.00, 18.67, 17.33, 18.33)$
- $\bar{R} = 107.66 / 6 = 17.94$
- Deviation-এর বর্গ: $0.376, 0.003, 0.003, 0.528, 0.376, 0.150$ → যোগফল $\approx 1.436$
- $\sigma = \sqrt{1.436 / 6} = \sqrt{0.239} \approx 0.49$

Paper লিখেছে 17.94 ± 0.49 — আমার হিসাব অনুযায়ী এটা population SD ($n$ দিয়ে ভাগ)। Sample SD ($n-1$ দিয়ে ভাগ) নিলে $\approx 0.54$ হতো। দুটোই ছোট — অর্থাৎ **গড় score stable**।

### ৬.৯ Pass@k (Unbiased Estimator)
প্রতিটা instance $i$-এ $n$টা run-এর মধ্যে $c_i$টা সফল হলে:
$$
\text{pass@}k = \frac{1}{N} \sum_{i=1}^{N} \left[ 1 - \frac{\binom{n - c_i}{k}}{\binom{n}{k}} \right]
$$

**সহজ কথায়:** প্রতিটা task-এর জন্য দেখা হয় k বার চেষ্টায় অন্তত একবার সফল হওয়ার সম্ভাবনা কত। তারপর সব task-এর গড় নেওয়া হয়। বাঁ দিকের ভগ্নাংশ বলে k বারই ব্যর্থ হওয়ার সম্ভাবনা।
| Symbol | মানে |
|---|---|
| $N$ | মোট instance (Lite-এ 300) |
| $n$ | প্রতি instance-এ মোট run (এখানে 6) |
| $c_i$ | instance $i$-এ কতগুলো run সফল |
| $k$ | কতগুলো চেষ্টা গোনা হচ্ছে |
| $\binom{n-c_i}{k} / \binom{n}{k}$ | $k$টা run random বাছলে **সবগুলো ব্যর্থ** হওয়ার সম্ভাবনা |

**Worked example (একটা instance, কাল্পনিক):** 6 run-এ 2 বার সফল ($n=6, c=2$):
- $k=1$: $1 - \dfrac{\binom{4}{1}}{\binom{6}{1}} = 1 - \dfrac{4}{6} = 0.333$
- $k=3$: $1 - \dfrac{\binom{4}{3}}{\binom{6}{3}} = 1 - \dfrac{4}{20} = 0.80$
- $k=6$: $\binom{4}{6} = 0$, তাই $= 1$

**Paper-এর আসল সংখ্যা (Table 10, Lite, GPT-4 Turbo):** pass@1 = 17.94, pass@2 = 23.89, pass@3 = 27.35, pass@4 = 29.67, pass@5 = 31.33, pass@6 = 32.67।
- লক্ষ্য করো pass@1 = 17.94 = 6 run-এর গড় — unbiased estimator-এ pass@1 সবসময় গড়ের সমান হয়, তাই এটা consistent। (Paper নিজে formula লেখেনি; এটা আমার যাচাই।)
- pass@6 = 32.67% → $300 \times 0.3267 = 98$টা instance অন্তত একবার solve হয়েছে।

**Reliability-র জন্য আমার নিজের derivation (গুরুত্বপূর্ণ):**
- সেরা একটা run solve করেছে $0.1867 \times 300 = 56$টা। কিন্তু 6 run মিলিয়ে 98টা। তাই **অন্তত $98 - 56 = 42$টা instance (~14%) "unstable"** — কোনো run-এ solve হয়, কোনো run-এ হয় না।
- "সব 6 run-এ সফল" হার (অনেকে এটাকে **pass^k** বলে — pass@k-এর উল্টো, reliability মাপে) সর্বোচ্চ সবচেয়ে খারাপ run-এর সমান, অর্থাৎ $\leq 17.33\%$। আসল মান paper-এ নেই।
- Authors-এর ভাষায়: "average performance variance is relatively low, though per-instance resolution can change considerably" — আমার হিসাব এটাকেই সংখ্যায় দেখায়।

### ৬.১০ Linting Guardrail-কে Formal ভাবে
$S = \{\text{F821}, \text{F822}, \text{F831}, \text{E111}, \text{E112}, \text{E113}, \text{E999}, \text{E902}\}$ = নির্বাচিত error code set। $\mathcal{L}_S(f)$ = file $f$-এ flake8 যে $S$-ভুক্ত error পায় তার set। Edit $e$ apply করলে নতুন file $f' = e(f)$:
$$
f_{\text{next}} =
\begin{cases}
f', & \text{যদি } \text{count}\left(\mathcal{L}_S(f')\right) = 0 \\
f \;\; (\text{edit বাতিল, lint message দেখাও}), & \text{অন্যথায়}
\end{cases}
$$

**সহজ কথায়:** Edit-এর পর linter নির্বাচিত error পেলে edit বাতিল। না পেলে edit রাখা হয়।
Assumption: $\text{count}\left(\mathcal{L}_S(f_{\text{original}})\right) = 0$ (মূল codebase well-formed)।
**সীমাবদ্ধতা (আমার পর্যবেক্ষণ):** এটা শুধু **syntax/name** স্তরের gate — semantic ভুল (ভুল logic) ধরে না। তাই "Incorrect Implementation" failure (39.9%) এই guardrail আটকাতে পারে না।

### ৬.১১ Edit Recovery Probability (Appendix B.3.3, Figure 20)
"Failed edit" = যে edit lint error দিয়েছে। "Recovery" = পরপর কিছু failed edit-এর ঠিক পরেই একটা সফল edit।
$$
P(\text{শেষ পর্যন্ত সফল edit} \mid n \text{টা পরপর failed edit})
$$

**সহজ কথায়:** পরপর কয়েকবার edit ব্যর্থ হলে শেষ পর্যন্ত একটা সফল edit হওয়ার সম্ভাবনা কত, সেটা এই সূত্র দেখায়।
- $n = 0$: 90.5% (যেকোনো edit চেষ্টা শেষ পর্যন্ত সফল হওয়ার সম্ভাবনা)
- $n = 1$: 57.2% → অর্থাৎ একবার ভুল হলে **42.8%** ক্ষেত্রে agent আর recover করে না
- $n$ বাড়লে সম্ভাবনা আরও কমে

**Recovery rate worked example (paper-এর সংখ্যা থেকে আমার ভাগ):**
- Resolved trajectory-তে: 135 বার failed-edit sequence, 104 বার recover → $104/135 \approx 77.0\%$
- সব trajectory-তে: 810 সফল recovery বনাম 555 ব্যর্থ → $810/(810+555) = 810/1365 \approx 59.3\%$
- সফল recovery-র আগে গড়ে 2.03 (resolved) / 2.2 (all) চেষ্টা; ব্যর্থ recovery-র আগে 4.22 (resolved) / 5.59 (all)।

### ৬.১২ File-level Localization F1 (Appendix B.9)
$\hat{F}$ = agent-এর patch যে file গুলো edit/remove করেছে, $F^{*}$ = gold patch-এর file set:
$$
P = \frac{\text{count}(\hat{F} \cap F^{*})}{\text{count}(\hat{F})}, \quad R = \frac{\text{count}(\hat{F} \cap F^{*})}{\text{count}(F^{*})}, \quad F_1 = \frac{2PR}{P + R}
$$

**সহজ কথায়:** Precision বলে agent-এর বদলানো file-এর কতটা সঠিক। Recall বলে সঠিক file-এর কতটা সে পেয়েছে। F1 এই দুটোকে এক সংখ্যায় আনে।
**Worked example (কাল্পনিক):** agent edit করেছে {`sessions.py`, `reproduce.py`}, gold = {`sessions.py`} → $P = 1/2$, $R = 1/1$, $F_1 = \dfrac{2 \times 0.5 \times 1}{1.5} = 0.667$। (দেখো — reproduce file না মুছলে precision কমে যায়।)
**Paper-এর সংখ্যা:** SWE-agent w/ GPT-4 Turbo $F_1 = 59.05\%$; BM25 (RAG) w/ Claude 3 Opus $F_1 = 45.47\%$। Paper F1-কে instance-গুলোর উপর কীভাবে গড় করেছে তা স্পষ্ট বলেনি।

### ৬.১৩ Action Transition Probability (Figure 21–24)
আগের $n$টা action দেখে পরের action-এর সম্ভাবনা ($n \in \{1,2,3,4\}$, প্রতিটার জন্য সবচেয়ে common 15টা sequence):
$$
P(a_t = a \mid a_{t-n}, \ldots, a_{t-1}) = \frac{\text{count}(a_{t-n}, \ldots, a_{t-1}, a)}{\text{count}(a_{t-n}, \ldots, a_{t-1})}
$$

**সহজ কথায়:** আগের কয়েকটা action দেখে পরের action কী হওয়ার সম্ভাবনা বেশি, সেটা গুনে বের করা হয়েছে।
এটা মূলত একটা **n-gram (Markov) model** of agent behavior।
**Paper-এর সংখ্যা:** `open`-এর পরে: `search_file` 0.35, `edit` 0.25, `scroll_down` 0.18, `goto` 0.09। (`create`, `edit`, `python`)-এর পরে: `edit` 0.39, `find_file` 0.31, `search_dir` 0.22।

### ৬.১৪ LM-Judge Agreement
$$
\text{Agreement} = \frac{\text{মানুষ ও LM একই category দিয়েছে এমন instance}}{\text{validation instance}}
$$

**সহজ কথায়:** মানুষ ও GPT-4o একই category দিয়েছে এমন instance-এর অনুপাত। এটা দিয়ে বোঝা যায় LLM judge কতটা ভরসাযোগ্য।
Validation set 15টা, agreement 87% → এটা সম্ভবত $13/15 = 86.7\%$ (আমার অনুমান; paper শুধু "87%" লিখেছে)।
**আমার পর্যবেক্ষণ:** 15টা sample খুব ছোট — 13/15-এর 95% confidence interval অনেক চওড়া (Wilson interval-এ মোটামুটি 62% থেকে 96%)। তাই failure-mode শতাংশগুলো "approximate" হিসেবে নেওয়া উচিত।

### ৬.১৫ Hyperparameter Grid
$$
\text{Configs} = \{0.0, 0.2\}_{\text{temp}} \times \{100, 200\}_{\text{window}} \times \{\text{Full}, \text{Last-5}\}_{\text{history}} \to 2 \times 2 \times 2 = 8 \text{ config per model}
$$

**সহজ কথায়:** ২ রকম temperature, ২ রকম window ও ২ রকম history মিলিয়ে মোট ৮টা setting চেষ্টা করা হয়েছে।
প্রতিটা config dev split-এর 37টা random instance-এ, 5টা sample-এর গড় (Table 5)।

---

## ৭. Experimental Setup

| বিষয় | বিবরণ |
|---|---|
| **Main benchmark** | SWE-bench full test (2,294 task, 12 Python repo) — main result |
| **Ablation benchmark** | SWE-bench Lite (300 task) — ablation ও analysis |
| **Dev set** | SWE-bench dev split (225 task) — ACI design ও hyperparameter sweep (37 instance) |
| **Extra benchmark** | HumanEvalFix (164 problem/language; Python, JS, Java ব্যবহার) |
| **Models** | GPT-4 Turbo (`gpt-4-1106-preview`, 128k context), Claude 3 Opus (`claude-3-opus-20240229`, 200k context) |
| **বাদ পড়া model** | Llama 3, DeepSeek Coder ইত্যাদি চেষ্টা করা হয়েছে কিন্তু agent setting-এ "subpar"; যেমন Llama 3-এর context মাত্র 8k |
| **Final config** | Temperature 0.0, window 100 line, history = last 5 observations (দুই model-এর জন্যই) |
| **Budget** | প্রতি instance 4 USD; পেরোলে বিদ্যমান edit auto-submit |
| **Metric** | % Resolved (pass@1), Avg. Cost (resolved instance-এর গড় API খরচ, USD) |
| **Baselines** | RAG (BM25, Paper 01-এর মতো), Shell-only agent (demo সহ ও ছাড়া) |
| **Execution** | Docker container (inference ও evaluation দুটোই) |
| **Failure labeler** | GPT-4o (`gpt-4o-2024-05-13`) |

**সহজ কথায়:** মূল ফল full SWE-bench-এ, ablation Lite-এ, আর design ও tuning dev set-এ হয়েছে। দুটো model: GPT-4 Turbo ও Claude 3 Opus।

**Dataset info (Table 12):**
| Dataset | Release | License | Split ও Count | Language |
|---|---|---|---|---|
| SWE-bench | 10/10/2023 | MIT | Test 2,294; Lite 300; Dev 225 | Python |
| HumanEvalFix | 07/23/2023 | MIT | Test 164 | Python, JS, Go, Java, C++, Rust |

---

## ৮. Results — মূল ফলাফল

### ৮.১ Main Results (Table 1)
| System | Model | SWE-bench % Resolved | SWE-bench Avg. Cost (USD) | Lite % Resolved | Lite Avg. Cost (USD) |
|---|---|---|---|---|---|
| RAG | GPT-4 Turbo | 1.31 | 0.13 | 2.67 | 0.13 |
| RAG | Claude 3 Opus | 3.79 | 0.25 | 4.33 | 0.25 |
| Shell-only | GPT-4 Turbo | – | – | 11.00 | 1.46 |
| Shell-only (w/o demo) | GPT-4 Turbo | – | – | 7.33 | 0.79 |
| **SWE-agent** | **GPT-4 Turbo** | **12.47** | 1.59 | **18.00** | 1.67 |
| SWE-agent | Claude 3 Opus | 10.46 | 2.59 | 13.00 | 2.18 |

(Shell-only full SWE-bench-এ চালানো হয়নি।)

**পড়ার উপায়:**
- Interactive হওয়াটাই বড় লাফ: RAG GPT-4 Turbo 2.67% → Shell-only 11.00% (Lite)।
- তার উপর ACI আরও লাফ: 11.00% → 18.00% (relative 64%)।
- ACI GPT-4 Turbo-র জন্য design করা হলেও Claude 3 Opus-এও কাজ করে (full-এ 10.46%) — **portability**।
- আগের সেরা non-interactive (RAG Claude 3 Opus, 3.79%) থেকে full SWE-bench-এ 12.47% — প্রায় 3.3 গুণ।

**সহজ কথায়:** ইন্টারেক্টিভ হলেই বড় লাফ (2.67 থেকে 11.00), আর ACI দিলে আরেকটা লাফ (11.00 থেকে 18.00)।

### ৮.২ HumanEvalFix (Table 2, pass@1 %)
| Model | Python | JS | Java |
|---|---|---|---|
| CodeLLaMa-instruct-13B | 29.2 | 19.5 | 32.3 |
| GPT-4 | 47.0 | 48.2 | 50.0 |
| DeepseekCoder-CodeAlpaca-6.7B | 49.4 | 51.8 | 45.1 |
| WaveCoder-DS-6.7B | 57.9 | 52.4 | 57.3 |
| **SWE-agent w/ GPT-4 Turbo** | **87.7** | **89.7** | **87.9** |

- SWE-agent ছাড়া বাকি সংখ্যা Yu et al. (WaveCoder paper) থেকে নেওয়া — অর্থাৎ authors নিজে চালাননি।
- Same config, শুধু language-specific demonstration বদলানো। বেশিরভাগ task প্রথম 10 turn-এর মধ্যে solve (Figure 25)।
- **সতর্কতা (আমার):** তুলনাটা পুরোপুরি apples-to-apples নয় — baseline গুলো non-interactive এবং অনেক পুরনো/ছোট model; SWE-agent test চালিয়ে বারবার চেষ্টা করতে পারে।

**সহজ কথায়:** HumanEvalFix-এ ফল ভালো, কিন্তু কাজটা সহজ, তাই এটা মূল দাবির প্রমাণ নয়।

### ৮.৩ ACI Ablation (Table 3, SWE-bench Lite, GPT-4 Turbo; default = 18.0%)
| Component | Variant | % Resolved | Default থেকে পার্থক্য |
|---|---|---|---|
| **Editor** | edit action **w/ linting** (default) | **18.0** | — |
| | edit action w/o linting | 15.0 | −3.0 |
| | No edit (শুধু shell: `sed`, redirection) | 10.3 | −7.7 |
| **Search** | **Summarized** (default) | **18.0** | — |
| | Iterative (`next`/`prev` দিয়ে একটা একটা result) | 12.0 | −6.0 |
| | No search | 15.7 | −2.3 |
| **File Viewer** | 30 lines | 14.3 | −3.7 |
| | **100 lines** (default) | **18.0** | — |
| | Full file | 12.7 | −5.3 |
| **Context** | **Last 5 Obs.** (default) | **18.0** | — |
| | Full history | 15.0 | −3.0 |
| | w/o demonstration | 16.3 | −1.7 |

**মূল শিক্ষা:**
1. **Edit command সবচেয়ে গুরুত্বপূর্ণ** (−7.7 pp সরালে)। `sed` দিয়ে multi-line edit কঠিন ও silent।
2. **Iterative search, কোনো search না থাকার চেয়েও খারাপ** (12.0 বনাম 15.7)! কারণ agent সব result একটা একটা করে `next` দিয়ে দেখতে থাকে, budget/context শেষ করে ফেলে। → "মানুষের জন্য ভালো UI (VSCode-style search) agent-এর জন্য খারাপ হতে পারে।"
3. **Window size-এ একটা sweet spot আছে:** কম (30) হলে context কম, বেশি (full file) হলে noise বেশি। 100 সবচেয়ে ভালো।
4. **Linting guardrail +3.0 pp** দেয়।
5. **History collapsing +3.0 pp** দেয়।
6. Demonstration-এর অবদান সবচেয়ে কম (+1.7 pp)।

**সহজ কথায়:** Edit command সরালে সবচেয়ে বেশি ক্ষতি। আর মানুষের জন্য ভালো iterative search agent-এর জন্য উল্টো ক্ষতিকর।

### ৮.৪ Variance ও Pass@k (Table 10, Figure 4; Lite, GPT-4 Turbo, 6 run)
| Run 1 | Run 2 | Run 3 | Run 4 | Run 5 | Run 6 | Avg |
|---|---|---|---|---|---|---|
| 17.33 | 18.00 | 18.00 | 18.67 | 17.33 | 18.33 | 17.94 ± 0.49 |

| pass@1 | pass@2 | pass@3 | pass@4 | pass@5 | pass@6 |
|---|---|---|---|---|---|
| 17.94 | 23.89 | 27.35 | 29.67 | 31.33 | 32.67 |

গড় stable, কিন্তু 6 বার চালালে প্রায় দ্বিগুণ instance অন্তত একবার solve হয় — per-instance outcome অস্থির (Section ৬.৯ দেখো)।

### ৮.৫ Hyperparameter Sweep (Table 5; dev-এর 37 instance, 5 sample-এর গড়)
| Model | Temp | Window | History | % Resolved |
|---|---|---|---|---|
| GPT-4 Turbo | 0.0 | 100 | Full | 14.1 |
| GPT-4 Turbo | 0.0 | 100 | Last 5 Obs. | **15.1** |
| GPT-4 Turbo | 0.0 | 200 | Full | 9.2 |
| GPT-4 Turbo | 0.0 | 200 | Last 5 Obs. | 10.8 |
| GPT-4 Turbo | 0.2 | 100 | Full | 10.8 |
| GPT-4 Turbo | 0.2 | 100 | Last 5 Obs. | 12.4 |
| GPT-4 Turbo | 0.2 | 200 | Full | 8.7 |
| GPT-4 Turbo | 0.2 | 200 | Last 5 Obs. | 10.8 |
| Claude 3 Opus | 0.0 | 100 | Full | 5.4 |
| Claude 3 Opus | 0.0 | 100 | Last 5 Obs. | **8.1** |
| Claude 3 Opus | 0.0 | 200 | Full | 7.0 |
| Claude 3 Opus | 0.0 | 200 | Last 5 Obs. | 7.1 |
| Claude 3 Opus | 0.2 | 100 | Full | 7.4 |
| Claude 3 Opus | 0.2 | 100 | Last 5 Obs. | **8.1** |
| Claude 3 Opus | 0.2 | 200 | Full | **8.1** |
| Claude 3 Opus | 0.2 | 200 | Last 5 Obs. | 6.8 |

Claude-এ তিনটা config-এর tie; দুই model-এর জন্যই 0.0/100/Last-5 বাছাই করা হয়েছে। **আমার পর্যবেক্ষণ:** dev-এর মাত্র 37 instance — 15.1% মানে প্রায় 5–6টা instance; config-গুলোর পার্থক্য অনেক ক্ষেত্রে 1–2টা instance-এর সমান, তাই এই বাছাই statistically দুর্বল।

**সহজ কথায়:** Tuning-এর সেট খুব ছোট (৩৭টা), তাই বাছাই করা setting খুব শক্ত প্রমাণের উপর দাঁড়িয়ে নেই।

### ৮.৬ Repository অনুযায়ী (Table 6, Lite, % Resolved)
| Repo (Lite-এ instance) | SWE-agent GPT-4 | SWE-agent Claude 3 Opus | RAG GPT-4 | RAG Claude 3 Opus | RAG Claude 2 |
|---|---|---|---|---|---|
| astropy (6) | 16.67 | 33.33 | 0.00 | 0.00 | 0.00 |
| django (114) | 26.32 | 16.67 | 4.39 | 6.14 | 5.26 |
| matplotlib (23) | 13.04 | 13.04 | 0.00 | 0.00 | 0.00 |
| seaborn (4) | 25.00 | 0.00 | 25.00 | 25.00 | 0.00 |
| flask (3) | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| requests (6) | 33.33 | 16.67 | 0.00 | 0.00 | 0.00 |
| xarray (5) | 0.00 | 0.00 | 20.00 | 20.00 | 0.00 |
| pylint (6) | 16.67 | 0.00 | 0.00 | 0.00 | 0.00 |
| pytest (17) | 17.65 | 5.88 | 0.00 | 5.88 | 5.88 |
| scikit-learn (23) | 17.39 | 17.39 | 0.00 | 4.35 | 8.70 |
| sphinx (16) | 6.25 | 6.25 | 0.00 | 0.00 | 0.00 |
| sympy (77) | 10.39 | 5.19 | 1.30 | 2.60 | 0.00 |

- Authors-এর বক্তব্য: RAG যে repo-তে প্রায় কিছুই পারতো না (matplotlib, sympy), SWE-agent সেখানেও solve করে।
- **আমার হিসাব:** GPT-4-এর 54টা resolved-এর মধ্যে 30টাই django থেকে ($114 \times 0.2632 = 30$) — অর্থাৎ **~56% সাফল্য একটা repo থেকে**। Django-র ভালো ফল overall score-কে টেনে তোলে।
- xarray-তে RAG 20% পারলেও SWE-agent 0% — interactive সবসময় ভালো নয়।

**সহজ কথায়:** ফলের অনেকটা আসছে django থেকে। তাই overall সংখ্যা সব repo-র সমান ছবি দেয় না।

### ৮.৭ সময় অনুযায়ী (Table 7, Lite, % Resolved; contamination check)
| Year (instance) | SWE-agent GPT-4 | SWE-agent Claude 3 Opus | RAG GPT-4 | RAG Claude 3 Opus | RAG Claude 2 |
|---|---|---|---|---|---|
| 2023 (30) | 23.33 | 13.33 | 3.33 | 3.33 | 0.0 |
| 2022 (57) | 21.05 | 17.54 | 5.26 | 7.02 | 1.75 |
| 2021 (42) | 23.81 | 11.90 | 2.38 | 4.76 | 2.38 |
| 2020 (66) | 10.61 | 7.58 | 3.03 | 1.52 | 1.52 |
| Before 2020 (105) | 17.14 | 10.48 | 0.95 | 4.76 | 5.71 |

Authors: issue-এর বছর ও resolve rate-এর মধ্যে স্পষ্ট সম্পর্ক নেই → test pollution/contamination-এর শক্ত প্রমাণ নেই।

**সহজ কথায়:** পুরনো বা নতুন issue-তে ফল প্রায় একই। তাই model-এর আগে থেকে মুখস্থ করার প্রমাণ শক্ত নয়।

### ৮.৮ Turn ও Cost-এর Distribution (Appendix B.3.1, Figure 14–15, Section 5.2)
| Statistic | মান |
|---|---|
| Resolved trajectory, full SWE-bench, GPT-4 (286টা) | গড় 14.71 turn, median 12, 75% trajectory 18 turn-এর মধ্যে |
| Resolved trajectory, Lite, Claude 3 Opus (35টা) | গড় 12.71 turn, median 13, 75% trajectory 15 turn-এর মধ্যে |
| সফল instance (GPT-4) | median খরচ 1.21 USD, 12 step |
| ব্যর্থ instance (GPT-4, budget শেষ না হওয়া) | mean খরচ 2.52 USD, 21 step |
| Resolved-এর মধ্যে budget শেষের আগে submit | 93.0% |
| সব instance-এর মধ্যে budget শেষের আগে submit | 69.0% |
| `exit_cost` সাধারণত কোন turn-এ | Turn 30–40 (4 USD limit ≈ এই সংখ্যক turn) |

**"Agents succeed quickly and fail slowly":** সফল run দ্রুত ও সস্তায় শেষ হয়। তাই authors মনে করেন budget বা token limit বাড়ালে performance তেমন বাড়বে না। প্রথম 10–20 turn-এর approach কাজ না করলে agent পরের turn কাজে লাগাতে পারে না — নতুন approach না নিয়ে একই জায়গায় local editing চালিয়ে যায়।

**সহজ কথায়:** সফল run দ্রুত ও সস্তায় শেষ হয়। ব্যর্থ run লম্বা চলে ও বেশি খরচ করে। তাই budget বাড়িয়ে লাভ কম।

### ৮.৯ Agent-এর আচরণের Pattern (Section 5.2, Figure 7, Table 8)
**সাধারণ trajectory-র ৩টা phase:**
1. **শুরু (turn 1–3): Reproduction বা Localization।** সব trajectory শুরু হয় `create` (reproduction) অথবা `find_file`/`search_dir` (localization) দিয়ে। সবচেয়ে common triple: `create, edit, python` — turn 1–3-এ **156 বার** (Table 8)।
2. **মাঝখান (turn 5+): "Edit, then execute" loop।** Turn 5 থেকে সবচেয়ে বেশি action `edit` ও `python`। Turn 5–31-এ `edit` সবচেয়ে জনপ্রিয় command (একমাত্র ব্যতিক্রম turn 30)। মাঝে মাঝে আবার localization (অন্য function/file দেখা)।
3. **শেষ: Submit।** Submit turn 10–20-এ কেন্দ্রীভূত; resolved instance আগে submit হয়। জনপ্রিয় শেষ pattern: `edit, python, rm, submit`।

**Table 8-এর কয়েকটা উল্লেখযোগ্য pattern (resolved, GPT-4):**
| Turns | Pattern | Count | Category |
|---|---|---|---|
| 1–3 | create, edit, python | 156 | Reproduction |
| 1–3 | search_dir, open, search_file | 21 | Localization (File) |
| 2–4 | edit, python, find_file | 71 | Localization (File) |
| 3–5 | python, find_file, open | 61 | Localization (File) |
| 5–7 | open, search_file, goto | 29 | Localization (Line) |
| 4–6 | find_file, open, edit | 28 | Editing |
| 7–9 | edit, python, rm | 20 | Editing |
| 8–10 | python, rm, submit | 19 | Submission |
| 9–11 | edit (x3) | 18 | Editing |

- `search_dir`/`search_file`-এর distribution bimodal: turn 1-এ peak (সরাসরি localization) ও turn 4-এ peak (reproduction-এর পরে localization)।
- Agent "zoom in" করে: directory-level search → file → line (`search_dir` → `open` → `search_file` → `goto`)।
- Failure pattern: একই action বারবার (`edit` ×4, `scroll_down` ×4) সাধারণত আরও cascade করে।

**সহজ কথায়:** Agent সাধারণত আগে bug reproduce করে, তারপর edit ও test চালানোর চক্রে ঘোরে, শেষে submit করে।

### ৮.১০ Editing — এখনো কঠিন (Section 5.2, Appendix B.3.3)
| Statistic | মান |
|---|---|
| Full SWE-bench-এ অন্তত 1টা failed edit আছে এমন trajectory | 1,185 / 2,294 (51.7%) |
| ঐ trajectory-গুলোতে failed edit | median 3, max 33 |
| Resolved-এর মধ্যে অন্তত 1টা failed edit | 113 / 286 (paper লিখেছে 31.5% — আমার হিসাবে 39.5%, Section ১২.৩ দেখো) |
| Resolved-এ failed edit প্রতি trajectory | median/mean 2, max 26 |
| যেকোনো edit শেষ পর্যন্ত সফল হওয়ার সম্ভাবনা | 90.5% |
| 1টা failed edit-এর পরে সফল হওয়ার সম্ভাবনা | 57.2% |

**সহজ কথায়:** অর্ধেকের বেশি task-এ অন্তত একটা edit ব্যর্থ হয়, এবং একবার ব্যর্থ হলে পরে ঠিক করার সম্ভাবনা কমে যায়।

### ৮.১১ Failure Modes (Figure 8, Table 9; Lite unresolved, n = 248, GPT-4 Turbo)
| Category | বর্ণনা (Table 9 থেকে সংক্ষেপে) | % |
|---|---|---|
| **Incorrect Implementation** | ঠিক জায়গায় পরিবর্তন করেছে কিন্তু সমাধান issue ঠিক করে না | **39.9** |
| **Failed to Recover from Edit** (Failed Edit Recovery) | Edit loop-এ আটকে গেছে, বারবার failed edit | **23.4** |
| Failed to Find Edit Location | সঠিক file খুলেছে কিন্তু সঠিক জায়গা খুঁজে পায়নি/edit করেনি | 12.9 |
| **Overly Specific Implementation** | প্রাসঙ্গিক পরিবর্তন, কিন্তু সমাধান যথেষ্ট general নয় — নির্দিষ্ট case ঠিক করে, অন্য case-এ behavior বদলে দিতে পারে | **12.1** |
| Gave Up Prematurely | কোনো সমস্যায় পড়ে agent নিজেই থেমে গেছে | 4.8 |
| Failed to Find Relevant File | সঠিক file কখনো খোলেনি/দেখেনি | 2.4 |
| Can't Reproduce (Failed to Reproduce) | Issue reproduce করার চেষ্টা করেছে কিন্তু পারেনি | 2.4 |
| Ran Out of Time (Ran Out of Budget) | সঠিক পথে ছিল কিন্তু budget শেষ | 2.0 |

- Incorrect + Overly Specific = **52.0%** (paper-এর সংখ্যা) — অর্থাৎ অর্ধেকের বেশি failure হলো **খুঁজে পেয়েছে কিন্তু ভুল/অপর্যাপ্ত সমাধান**।
- Table 9-এ "Other" নামে ৯ম category আছে, Figure 8-এ ৮টা দেখানো।
- **নোট:** 39.9, 12.1 ও 23.4 paper-এর text দিয়ে নিশ্চিত; বাকি ছোট মানগুলোর (12.9, 4.8, 2.4, 2.4, 2.0) category-mapping PDF-এর Figure 8 (পৃষ্ঠা 8)-এর রং মিলিয়ে যাচাই করা হয়েছে।

**সহজ কথায়:** ব্যর্থতার প্রধান কারণ "ঠিক জায়গা খুঁজে ভুল সমাধান দেওয়া", জায়গা খুঁজে না পাওয়া নয়।

### ৮.১২ Patch-এর আকার (Table 11; median / mean, 90th percentile-এর মধ্যে)
| Model | Outcome | Lines + | Lines − | Hunks | Files |
|---|---|---|---|---|---|
| SWE-agent w/ GPT-4 Turbo | Resolved | 3.0 / 5.7 | 1.0 / 1.32 | 1.0 / 1.52 | 1.0 / 1.22 |
| | All | 12.0 / 16.58 | 1.0 / 1.35 | 2.0 / 1.83 | 1.0 / 1.53 |
| Gold | Resolved | 2.0 / 3.58 | 1.0 / 1.98 | 1.0 / 1.3 | 1.0 / 1.0 |
| | All | 7.0 / 11.67 | 2.0 / 4.05 | 2.0 / 2.45 | 1.0 / 1.24 |
| SWE-agent w/ Claude 3 Opus | Resolved | 3.0 / 5.09 | 1.0 / 1.59 | 1.0 / 1.56 | 1.0 / 1.26 |
| | All | 11.0 / 15.25 | 1.0 / 1.79 | 2.0 / 2.14 | 2.0 / 1.87 |
| Gold | Resolved | 3.0 / 3.91 | 1.0 / 1.94 | 1.0 / 1.4 | 1.0 / 1.0 |
| | All | 6.0 / 10.68 | 2.0 / 3.61 | 2.0 / 2.22 | 1.0 / 1.13 |

- Agent-এর patch gold-এর চেয়ে **বড়** (বেশি line যোগ, বেশি hunk/file) — authors-এর মতে মূলত রেখে দেওয়া **reproduction code**-এর কারণে। (Paper 01-এ RAG model-এর patch ছিল gold-এর চেয়ে ছোট — উল্টো চিত্র।)
- Resolved patch গুলো ছোট → multi-location edit এখনো কঠিন।

**সহজ কথায়:** Agent-এর patch বড় হয় কারণ সে প্রায়ই reproduce script ফেলে রাখে।

### ৮.১৩ Episode কীভাবে শেষ হয় (Table 13)
| Model | Split | Outcome | Submit | Exit Cost (Submit) | Exit Cost (No Submit) | Early Exit |
|---|---|---|---|---|---|---|
| GPT-4 Turbo | Full | Resolved | 266 | 20 | 0 | 0 |
| | | All | 1589 | 630 | 48 | 1 |
| | Lite | Resolved | 50 | 4 | 0 | 0 |
| | | All | 203 | 95 | 2 | 0 |
| Claude 3 Opus | Full | Resolved | 206 | 35 | 0 | 0 |
| | | All | 882 | 1048 | 73 | 1 |
| | Lite | Resolved | 32 | 3 | 0 | 0 |
| | | All | 133 | 156 | 11 | 0 |

- Claude 3 Opus-এর অর্ধেকের বেশি episode cost limit-এ শেষ হয় — GPT-4-এর চেয়ে অনেক বেশি।
- Paper অনুযায়ী (GPT-4, full): submit দিয়ে শেষ হওয়া task-এর 14.3% resolved, `exit_cost`-এ শেষ হওয়াগুলোর মাত্র 3.1%।
- সব run মিলিয়ে মাত্র 2টা early exit → ACI format-ঠিক response আদায়ে কার্যকর।

**সহজ কথায়:** বেশিরভাগ সফল run নিজে `submit` দিয়ে শেষ হয়। Budget-এ শেষ হওয়া run প্রায় সবসময় ব্যর্থ।

### ৮.১৪ Localization: Agent বনাম BM25 (Appendix B.9)
File-level F1: SWE-agent w/ GPT-4 Turbo **59.05%** বনাম BM25 w/ Claude 3 Opus **45.47%** — interactive search Paper 01-এর মূল bottleneck (localization)-এ উন্নতি আনে।

### ৮.১৫ Qualitative Case Study (Appendix D, Lite, GPT-4 Turbo)
| Instance | ফল | কী হয়েছিল | শিক্ষা |
|---|---|---|---|
| psf/requests-2317 | ✅ Resolved | `builtin_str(method)` bytes-কে `"b'GET'"` বানাচ্ছিল। Agent `find_file` → `search_file` → edit (bytes হলে decode) → reproduce script (200 OK) → মুছে submit | Test pass করেছে, কিন্তু repo-তে আগে থেকে থাকা `to_native_string` utility ব্যবহার করেনি → maintainability কম |
| pylint-dev/pylint-5859 | ✅ Resolved | `--notes` option-এ শুধু punctuation tag ("???") ধরা হচ্ছিল না। Agent regex-এর `\b` বদলে lookahead দিয়েছে | Gold patch ভিন্ন regex ব্যবহার করে; authors নিজেই বলছেন agent-এর সমাধান হয়তো এমন side-effect আনে যা existing test ধরে না |
| sympy/sympy-21614 | ❌ Unresolved | `Derivative.kind` ভুল। Agent অনেক অনুমানভিত্তিক search করেছে, শেষে বিশাল file-এ scroll করতে করতে budget শেষ | Search কৌশল অদক্ষ; inheritance structure বোঝা দরকার ছিল |
| django/django-14411 | ❌ Unresolved | Label-এর `for` attribute সমস্যা। Agent ঠিক class খুঁজে পেয়েছে কিন্তু ভুল method (`label_tag`) override করেছে; আসলে `id_for_label` override দরকার ছিল | **Test না করেই submit** করেছে (ধরে নিয়েছে Django server চালানো যাবে না) |

**আমাদের domain-এর জন্য এই table-টা খুব গুরুত্বপূর্ণ:** দুটো "resolved" case-এই authors নিজে quality/correctness নিয়ে সন্দেহ প্রকাশ করেছেন → test pass ≠ trustworthy patch।

**সহজ কথায়:** Test পাস করলেই patch ভালো, এমন নয়। Authors নিজেই দুটো সফল case নিয়ে সন্দেহ করেছেন।

---

## ৯. Key Findings / Insights (Supervisor-কে বলার মতো ৮টা পয়েন্ট)

1. **Interface design একটা আলাদা lever:** model না বদলে শুধু ACI দিয়ে Lite-এ 11.00% → 18.00% (relative 64%), full-এ 12.47% (আগের সেরা 3.8%)।
2. **মানুষের জন্য ভালো ≠ agent-এর জন্য ভালো:** VSCode-style iterative search agent-এর জন্য "no search"-এর চেয়েও খারাপ (12.0 বনাম 15.7)।
3. **Compact edit + তাৎক্ষণিক feedback সবচেয়ে গুরুত্বপূর্ণ:** edit command সরালে −7.7 pp।
4. **Guardrail কাজ করে:** syntax linting +3.0 pp; তবু 51.7% trajectory-তে failed edit, আর একবার fail হলে recovery-র সম্ভাবনা 90.5% থেকে 57.2%-এ নামে।
5. **কম কিন্তু সঠিক context ভালো:** 100-line window ও last-5 history optimal; full file বা full history দুটোই খারাপ।
6. **Agent দ্রুত সফল হয়, ধীরে ব্যর্থ হয়:** budget বাড়ানো সম্ভবত সমাধান নয়; ব্যর্থ run বেশি খরচ করে।
7. **বেশিরভাগ failure "ভুল সমাধান", খুঁজে না পাওয়া নয়:** 52.0% Incorrect/Overly Specific implementation; localization failure (file + location) মিলিয়ে প্রায় 15%।
8. **গড় stable কিন্তু instance-স্তরে অস্থির:** 6 run-এ গড় 17.94 ± 0.49, কিন্তু pass@6 = 32.67% — একই task একবার পারে, আরেকবার পারে না। **Reliability-র জন্য এটা সবচেয়ে বড় সতর্কবার্তা।**

**সহজ কথায়:** আটটা পয়েন্টের সারকথা: interface গুরুত্বপূর্ণ, guardrail কাজ করে, কিন্তু ফল একই task-এ বদলায়।

---

## ১০. কেন এই Solution অন্যগুলোর থেকে ভালো?

| বৈশিষ্ট্য | RAG (Paper 01) | Shell-only agent | **SWE-agent (ACI)** |
|---|---|---|---|
| Interaction | একবারে উত্তর | বহু turn | বহু turn |
| Code চালিয়ে যাচাই | না | হ্যাঁ | হ্যাঁ |
| Localization | BM25 (keyword, স্থির) | `cd`/`ls`/`grep` — অদক্ষ, noisy | Summarized search (≤50 result) + file viewer |
| File দেখা | Retrieved file পুরো context-এ | `cat` পুরো file | 100-line window, line number, "lines above/below" |
| Editing | Patch format লিখতে হয় (প্রায়ই apply fail) | `sed`/redirection — silent, error-prone | `edit n:m` এক action-এ, তাৎক্ষণিক feedback |
| ভুল ধরা | নেই | নেই | Linter guardrail — ভুল edit বাতিল |
| Context management | Fixed context | Full history | Last-5 collapsing |
| Lite % Resolved (GPT-4 Turbo) | 2.67 | 11.00 | **18.00** |
| Lite Avg. Cost (USD) | 0.13 | 1.46 | 1.67 |

**সহজ কথায়:** RAG একবারে উত্তর দেয়, shell-only ধাপে ধাপে চেষ্টা করে, আর SWE-agent তার সাথে ভালো tool ও guardrail যোগ করে। তাই সেটা সবচেয়ে এগিয়ে।

**মূল শক্তি:**
1. **Model-agnostic উন্নতি:** কোনো training লাগে না; যেকোনো যথেষ্ট শক্তিশালী model-এ প্রয়োগ করা যায় (GPT-4 Turbo ও Claude 3 Opus দুটোতেই কাজ করেছে)।
2. **Principled design + ablation:** প্রতিটা design choice-এর অবদান সংখ্যা দিয়ে দেখানো।
3. **গভীর behavioral analysis:** trajectory, transition probability, failure taxonomy — শুধু score নয়, "কেন"।
4. **সম্পূর্ণ open-source ও extensible:** yaml config দিয়ে নতুন command/guardrail যোগ করা সহজ — আমাদের মতো research-এর জন্য আদর্শ testbed।
5. **Safety-সচেতন:** Docker sandbox।

---

## ১১. কোন পরিস্থিতিতে SWE-agent ভালো কাজ করে, কোথায় করে না

### ✅ ভালো কাজ করে যখন:
- Issue-তে reproduce করার code বা স্পষ্ট symbol (class/function/file নাম) আছে — search command দিয়ে দ্রুত localize করা যায়।
- Fix ছোট ও এক-জায়গার (resolved patch-এর median 3 line যোগ, 1 file)।
- Python codebase (linter flake8 Python-specific)।
- শক্তিশালী, বড় context-এর model (128k+) আছে।
- Bug-fixing/editing task, বিশেষত ছোট scope-এ (HumanEvalFix 87.7–89.7%)।

### ❌ ভালো কাজ করে না / সীমিত যখন:
- **Fix-এর জন্য codebase-এর গভীর structure বোঝা দরকার** (যেমন sympy-21614-এ inheritance; django-14411-এ সঠিক override point)।
- **Multi-file / multi-hunk পরিবর্তন** দরকার।
- **Reproduce করা কঠিন** (server, GUI, বিশেষ environment) — agent test ছাড়াই submit করতে পারে।
- **ছোট context-এর বা দুর্বল model** (Llama 3 8k, DeepSeek Coder — "subpar")।
- **প্রথম approach ব্যর্থ হলে** — agent pivot করতে পারে না, একই জায়গায় edit চালিয়ে যায়।
- **Cost-sensitive setting** — RAG-এর চেয়ে 8–13 গুণ খরচ, আর ব্যর্থ run আরও ব্যয়বহুল।
- **Semantic correctness দরকার** — guardrail শুধু syntax দেখে।
- **অন্য language** — paper-এর linting ও evaluation Python-কেন্দ্রিক (যদিও Docker দিয়ে extend করা সম্ভব বলে authors দাবি করেছেন)।

---

## ১২. Limitations — দুর্বলতা

### ১২.১ Authors যা নিজেরা স্বীকার করেছেন (Appendix E.3 ও অন্যান্য জায়গা)
1. **Toolkit ছোট:** web browsing, static/dynamic analysis, spectrum-based fault localization, fuzzing-ভিত্তিক test generation যোগ করা হয়নি — future work।
2. **ACI design ও case study manual:** trajectory দেখে হাতে design; tip লেখা scale করে না। Automated ACI design future work।
3. **Scope শুধু programmatic task:** অন্য domain-এ (web, data analysis) ACI principle কাজ করবে কিনা অজানা।
4. **Guardrail-এর trade-off:** linting কিছু edit-কে নির্দিষ্ট ক্রমে করতে বাধ্য করে।
5. **Search 50-result cap:** এতে agent-কে আবার query দিতে হয়, বাড়তি LM call।
6. **Demonstration সত্যিই domain জ্ঞান দেয় কিনা নিশ্চিত নন** — মূলত format শেখায় বলে মনে করেন।
7. **Budget:** খরচের কারণে মূল result pass@1; variance শুধু Lite-এ GPT-4 দিয়ে মাপা।
8. **Agent পরের turn কাজে লাগাতে পারে না** — প্রথম approach ব্যর্থ হলে error recovery দুর্বল।
9. **Ethics (E.1):** LM-generated code চালানোর security ঝুঁকি (Docker namespace isolation hardware virtualization-এর মতো নিরাপদ নয়), দূষিত evaluation dataset-এর issue text দিয়ে agent-কে malicious code বানাতে বলা, এবং offensive/malicious ব্যবহারের ঝুঁকি।
10. Llama 3, DeepSeek Coder-এর মতো open model agent setting-এ ভালো করেনি।

### ১২.২ আমার Critical Analysis (Professor-level observation)
1. **"Resolved" এখনো test-নির্ভর — overfitting ঝুঁকি বাড়ে:** Agent test চালাতে পারে এবং নিজের reproduction script অনুযায়ী code বদলায়। ফলে সে এমন patch বানাতে পারে যা visible behavior ঠিক করে কিন্তু general নয় — authors নিজেই "Overly Specific Implementation" (12.1%) category বানিয়েছেন, আর resolved case-এও (pylint-5859) side-effect-এর সন্দেহ লিখেছেন। কিন্তু **resolved patch-গুলোর মধ্যে কতগুলো আসলে overfit, তা মাপা হয়নি।** Paper 01-এর G1 (patch overfitting) gap এখানে আরও প্রকট।
2. **Reliability (consistency) মাপা হয়েছে, কিন্তু শিরোনামে আসেনি:** pass@6 = 32.67% বনাম pass@1 = 17.94% — অন্তত 42টা instance unstable (আমার হিসাব, Section ৬.৯)। একজন user-এর কাছে "একই issue আজ solve হয়, কাল হয় না" — এটা trust-এর বড় সমস্যা, কিন্তু paper এটাকে মূলত "variance low" হিসেবে উপস্থাপন করেছে।
3. **Cost metric বিভ্রান্তিকর হতে পারে:** Avg. Cost শুধু resolved instance-এর গড়; ব্যর্থ run-এর খরচ (যা বেশি) বাদ। আমার rough হিসাবে প্রতি সফল fix-এর আসল খরচ ~13–20 USD (Section ৬.৭)।
4. **Design ও evaluation-এর মধ্যে overfitting-এর সম্ভাবনা:** ACI dev set-এ manual inspection দিয়ে বানানো, hyperparameter মাত্র 37 instance-এ বাছাই। Test set আলাদা হলেও, একই benchmark family-তে বারবার tuning করে "benchmark-specific" design হয়ে যেতে পারে। অন্য benchmark-এ (HumanEvalFix) portable দেখানো হয়েছে, কিন্তু সেটা অনেক সহজ task।
5. **Ablation statistically দুর্বল:** Table 3-এর প্রতিটা ablation একবার run (একটা সংখ্যা)। Run-to-run SD ~0.49 pp, কিন্তু per-instance অস্থিরতা অনেক বেশি; −1.7 pp (demo) পার্থক্য মাত্র ~5টা instance। কোনো significance test নেই।
6. **Failure analysis-এর validity:** 15টা হাতে-label instance দিয়ে GPT-4o judge validate (87%) — sample খুব ছোট; আর judge-কে gold patch দেখানো হয়েছে, যা category-কে প্রভাবিত করতে পারে।
7. **Baseline comparison অসম:** HumanEvalFix-এ baseline সংখ্যা অন্য paper থেকে নেওয়া, non-interactive ও ছোট model — interactive agent-এর সাথে তুলনা apples-to-apples নয়।
8. **Repository bias:** Lite-এ GPT-4-এর সাফল্যের ~56% django থেকে (আমার হিসাব)।
9. **Guardrail শুধু syntax-level:** semantic, security বা regression check নেই। Agent চাইলে test file বদলাতে বা দুর্বল fix submit করতে পারে — এটা আটকানোর কোনো guardrail নেই।
10. **Security of the agent itself:** Authors ethics অংশে দূষিত issue text-এর মাধ্যমে agent-কে malicious কাজ করানোর ঝুঁকি উল্লেখ করেছেন (আজকের ভাষায় prompt injection-এর মতো), কিন্তু কোনো defense বা measurement নেই।
11. **Contamination check দুর্বল:** Lite-এ বছরভিত্তিক তুলনা (2023-এ মাত্র 30 instance) — Paper 01-এর মতোই দুর্বল প্রমাণ।
12. **Closed model-নির্ভরতা ও reproducibility:** GPT-4 Turbo/Claude 3 Opus-এর নির্দিষ্ট snapshot পরে API থেকে সরে যেতে পারে; তখন হুবহু reproduce করা কঠিন। (Trajectory open-source হওয়ায় analysis reproduce করা যায়।)

### ১২.৩ Paper-এর ভেতরের কিছু অসঙ্গতি (আমার নিজের যাচাই — presentation-এ সাবধান)
| # | অসঙ্গতি | কোথায় |
|---|---|---|
| 1 | HumanEvalFix: Abstract ও Table 2 (Python) বলে **87.7%**, কিন্তু Section 5-এর text বলে **88.3%**। তিন language-এর গড় 88.43 — কোনোটার সাথে হুবহু মেলে না। | Abstract, Section 5, Table 2 |
| 2 | Claude 3 Opus Lite: Table 1-এ **13.00%** (= 39/300), কিন্তু Table 6 ও Table 7-এর সংখ্যা যোগ করলে 35টা, Table 13-এ resolved = 32 + 3 = 35, Figure 14-এও 35 trajectory → **11.67%**। | Table 1 বনাম Table 6/7/13, Figure 14 |
| 3 | Resolved-এর মধ্যে failed edit: "113 (31.5%) of 286" — কিন্তু $113/286 = 39.5\%$। | Appendix B.3.3 |
| 4 | Failure analysis-এ unresolved n = 248, কিন্তু Lite-এ 54 resolved হলে unresolved = 246। সম্ভবত অন্য run থেকে নেওয়া (যেমন 17.33%-এর run-এ 52 resolved → 248 unresolved) — paper স্পষ্ট করেনি। | Section 5.2, B.4 |
| 5 | Table 4-এ `scroll_down`-এর documentation "Moves the window up 100 lines" আর `scroll_up`-এর "down" — উল্টো লেখা (typo)। | Table 4 |
| 6 | Section 5.2 "Table 15" উল্লেখ করে, কিন্তু আমাদের PDF version-এ (arXiv v3) Table 13-এর পরে আর table নেই। | Section 5.2 |
| 7 | "median cost of 1.21 USD and 12 steps compared to a **mean** of 2.52 USD and 21 steps" — median আর mean মিশিয়ে তুলনা। | Section 5.2 |
| 8 | Early exit-এর শর্ত: Section 3 বলে valid না হওয়া পর্যন্ত পুনরাবৃত্তি; Figure 26 বলে "2+ consecutive format errors"; Appendix C বলে "3 malformed responses in a row"। | Section 3, Figure 26, Appendix C |
| 9 | Table 13-এ "All" row-এর যোগফল: GPT-4 full = 1589 + 630 + 48 + 1 = 2,268 (2,294 নয়); Claude full = 2,004। আর submit-এ শেষ হওয়াদের resolved হার $266/1589 \approx 16.7\%$, কিন্তু paper বলে 14.3%। | Table 13, Appendix B.9 |
| 10 | Claude 3 Opus full-এর ক্ষেত্রে Introduction-এ "10.5%" (10.46-এর rounding) — অসঙ্গতি নয়, শুধু rounding। | Introduction |

এগুলো paper-এর মূল claim বদলায় না, কিন্তু supervisor সংখ্যা ধরে প্রশ্ন করলে কাজে লাগবে।

**সহজ কথায়:** এই অসঙ্গতিগুলো ছোট সংখ্যার ভুল। মূল দাবি বদলায় না, কিন্তু viva-তে সংখ্যা ধরে প্রশ্ন এলে জানা থাকা ভালো।

---

## ১৩. Research Gaps — কোথায় কাজ করার সুযোগ আছে

| # | Gap | কেন গুরুত্বপূর্ণ (এই paper-এর প্রমাণ) | আমাদের কোন folder-এর সাথে সম্পর্কিত |
|---|---|---|---|
| G1 | **Patch correctness beyond tests** — resolved কিন্তু overfit/অসম্পূর্ণ patch চিহ্নিত করা | Overly Specific 12.1%; resolved case-এও (pylint-5859) side-effect-এর সন্দেহ | Patch Validation (HITL LLM-as-Judge, APCA code representation, Harden and Catch); Automated Program Repair |
| G2 | **Run-to-run reliability (pass^k, flip rate)** | pass@1 17.94 বনাম pass@6 32.67; ≥42 instance unstable | Coding-Agent Evaluation & Reliability (Engineering Reliable Coding Agents) |
| G3 | **Agent-এর নিজের test/reproduction-এর মান** — agent test না করেই submit, বা দুর্বল reproduce script | django-14411 test ছাড়াই submit; Can't Reproduce 2.4% | LLM Test Generation (ExecutionAgent, CoverUp, Oracle-Guided Program Selection) |
| G4 | **Semantic / security guardrail** — syntax-এর বাইরে (security scan, regression test gate) | Guardrail শুধু flake8 syntax; Incorrect Implementation 39.9% আটকায় না | Security of AI-Generated Code (CWEval, Security & Quality in LLM Code); Trustworthy AI for SE (Proof-Carrying Code Completions) |
| G5 | **Agent-এর নিজের নিরাপত্তা** — দূষিত issue text, sandbox escape, ধ্বংসাত্মক command | Authors ethics অংশে ঝুঁকি স্বীকার করেছেন, defense নেই | Security of AI-Generated Code; Trustworthy AI for SE (Trustworthy AI Software Engineers) |
| G6 | **Error recovery / strategy pivot** | 1 failed edit-এর পর recovery 57.2%; প্রথম 10–20 turn ব্যর্থ হলে agent আটকে যায় | Coding-Agent Evaluation & Reliability; AI Coding Agents (AutoCodeRover, Agentless) |
| G7 | **Cost-aware ও early-stopping agent / failure prediction** | Succeed fast, fail slow; ব্যর্থ run বেশি খরচ | Coding-Agent Evaluation & Reliability |
| G8 | **Maintainability ও code quality** | requests-2317: existing utility ব্যবহার করেনি; patch gold-এর চেয়ে বড় | Security of AI-Generated Code (Security and Quality in LLM-Generated Code) |
| G9 | **Richer SE tools in ACI** (SBFL, static analysis, fuzzing) | Authors-এর নিজের future work | Automated Program Repair; LLM Test Generation |
| G10 | **Automated ACI design** | Design manual, scale করে না | — (খোলা) |
| G11 | **Multi-language ও harder task** | Python-only linting ও evaluation | Coding-Agent Evaluation & Reliability (SWE-Bench Pro, Long-Horizon SE tasks) |
| G12 | **Contamination-free evaluation of agents** | Temporal analysis দুর্বল | Coding-Agent Evaluation & Reliability (SWE-rebench) |
| G13 | **Trajectory-level evaluation (process, not just outcome)** | শুধু final patch evaluate হয়; trajectory-তে test বদলানো, অপ্রয়োজনীয় file রাখা ইত্যাদি ধরা হয় না | Trustworthy AI for SE (AI Assurance testing strategy); Coding-Agent Evaluation & Reliability |

**সহজ কথায়:** এই gap গুলোর বেশিরভাগই assurance ও reliability-র সাথে জড়িত, তাই SPL3-এর জন্য উপযুক্ত।

---

## ১৪. কী করলে আরও ভালো হবে — Improvement Ideas (আমার প্রস্তাব, paper-এ নেই)

1. **Assurance guardrail layer:** linter-এর পাশাপাশি — (ক) `submit`-এর আগে বাধ্যতামূলক existing test চালানো (regression gate), (খ) Bandit/Semgrep দিয়ে security scan, (গ) test file পরিবর্তন করলে flag, (ঘ) reproduction file স্বয়ংক্রিয়ভাবে patch থেকে বাদ।
2. **Semantic linting:** শুধু syntax নয়, type checker (যেমন mypy) বা নতুন undefined behavior ধরার জন্য বাড়তি check — তবে false positive-এর trade-off মাপতে হবে।
3. **Reliability metric রিপোর্ট করা:**
   $$\text{pass}^{k} = \frac{1}{N} \sum_{i=1}^{N} \mathbb{1}\left[c_i = n\right] \quad (k = n \text{ হলে})$$
   এবং **flip rate** = যে instance-এর ফল run-এর মধ্যে বদলায় তার অনুপাত।
4. **Failure-aware early stopping:** trajectory signal (পরপর failed edit, একই action পুনরাবৃত্তি, turn সংখ্যা) দেখে ব্যর্থতা আগে অনুমান করে থামানো বা strategy বদলানো — খরচ বাঁচাবে।
5. **Patch overfitting check:** resolved patch-এর উপর LLM/mutation দিয়ে বাড়তি test বানিয়ে দেখা কতগুলো আসলে ভুল (Paper 01-এর G1-এর agent version)।
6. **Strategy pivot prompt:** N turn-এ progress না হলে history reset করে নতুন hypothesis নিয়ে শুরু করা (reflection)।
7. **True cost metric:** মোট খরচ ÷ resolved সংখ্যা (cost per resolved issue) রিপোর্ট করা।

---

## ১৫. কোন Gap-এ Research করলে ভালো Result ও Publication আসতে পারে

> ⚠️ এটা ২টা paper-এর ভিত্তিতে প্রাথমিক মত। ৭টা sub-domain শেষ করার পর চূড়ান্ত gap বাছাই করবো। 2024-এর পরে এসব দিকে অনেক কাজ হয়ে থাকতে পারে — novelty নিশ্চিত করতে আলাদা literature search লাগবে।

| Gap / Idea | SPL3-তে করা সম্ভব? | Novelty | Publication সম্ভাবনা |
|---|---|---|---|
| **G1+G4: Assurance-aware ACI** — SWE-agent-এ regression-test gate + security scan + test-tamper detection guardrail যোগ করে resolved, overfit rate, security finding একসাথে মাপা | ✅ হ্যাঁ — SWE-bench Lite/Verified-এর 50–100 instance, সস্তা model | উচ্চ; domain-এর নামের সাথে সরাসরি মেলে | ⭐⭐⭐⭐⭐ |
| **G7: Trajectory থেকে failure prediction** — paper-এর open-source trajectory ব্যবহার করে (নতুন API খরচ ছাড়া) early-stop classifier | ✅ খুব সম্ভব — শুধু public data ও ML | মাঝারি-উচ্চ | ⭐⭐⭐⭐ |
| **G2: Run-to-run reliability study** — একই config k বার চালিয়ে pass^k, flip rate, কোন ধরনের issue unstable | ✅ হ্যাঁ, তবে API খরচ k গুণ; ছোট subset নিতে হবে | মাঝারি-উচ্চ | ⭐⭐⭐⭐ |
| **G3: Agent-এর reproduction test-এর মান মূল্যায়ন** — agent-এর লেখা reproduce script আসলে bug ধরে কিনা | ✅ হ্যাঁ — trajectory থেকে script বের করে gold/buggy version-এ চালানো | উচ্চ | ⭐⭐⭐⭐ |
| G10: Automated ACI design | ⚠️ কঠিন, অনেক compute | উচ্চ | ⭐⭐⭐ |
| G5: Agent prompt-injection robustness | ⚠️ সম্ভব, তবে ethics ও sandbox সতর্কতা লাগবে | উচ্চ | ⭐⭐⭐⭐ |

**সহজ কথায়:** সবচেয়ে বাস্তবসম্মত শুরু হলো assurance guardrail layer এবং trajectory-ভিত্তিক failure prediction।

**সম্ভাব্য venue (general guidance, Paper 01-এর মতো):**
- **Conference:** ICSE, FSE, ASE, ISSTA; workshop (যেমন LLM4Code) — student-এর জন্য শুরু করা সহজ।
- **Journal:** ACM TOSEM, IEEE TSE (খুব high), EMSE, JSS, IST।
- Trajectory-ভিত্তিক empirical study (G7, G3) সাধারণত **MSR**-ধরনের venue-তেও মানানসই।

---

## ১৬. SPL3 Implementation Perspective — Software-এ কীভাবে আনবো

**Paper implement করা মানে কী?** নিজে একটা ছোট "SWE-agent-style" agent বানানো (বা open-source SWE-agent চালানো), এবং তার উপর আমাদের **assurance layer** যোগ করা, যাতে প্রতিটা patch-এর বিশ্বাসযোগ্যতা মাপা যায়।

**প্রস্তাবিত module:**
1. **Environment Manager:** প্রতিটা task-এর জন্য Docker container তুলে repo-কে base commit-এ checkout (SWE-bench-এর image ব্যবহার)।
2. **ACI Command Layer:** `open`, `goto`, `scroll_up/down`, `find_file`, `search_dir`, `search_file` (≤50 result cap), `edit n:m` + flake8 gate, `create`, `submit` — Python-এ implement।
3. **History Processor:** last-5 observation collapsing, malformed response de-noising।
4. **LLM Client:** যেকোনো API বা local model; প্রতি turn-এ token ও খরচ log; per-instance budget cap।
5. **Trajectory Logger:** প্রতিটা turn (thought, action, observation, cost) JSON-এ save।
6. **Evaluator:** official SWE-bench harness দিয়ে F2P/P2P চালিয়ে Resolved (Paper 01 দেখো)।
7. **Assurance Layer (আমাদের gap অংশ):** regression-test gate, Bandit/Semgrep security scan, test-tamper detection, reproduction-file filter, extra test দিয়ে overfit check।
8. **Analytics Dashboard:** % Resolved, true cost per resolved, pass@k ও pass^k, failure category (LLM judge + মানুষের ছোট validation), action transition heatmap।

**কাজের ধাপ (৩–৪ মাসের SPL3-এর জন্য প্রস্তাব):**
1. Open-source SWE-agent বা নিজের minimal version Lite-এর 20–30টা instance-এ চালানো।
2. Paper-এর দুটো ablation (linting on/off, window size) ছোট scale-এ reproduce।
3. Assurance layer যোগ করে আগে-পরে তুলনা।
4. k = 3 run করে reliability metric।

**Practical সতর্কতা:**
- Windows-এ **WSL2 + Docker Desktop** লাগবে; SWE-bench image অনেক disk জায়গা নেয় — অল্প instance দিয়ে শুরু করো।
- **খরচ হিসাব:** paper-এ GPT-4 Turbo দিয়ে per-instance cap 4 USD ছিল। আমাদের ক্ষেত্রে সস্তা model ও কম budget (যেমন 0.5–1 USD) ধরলে, 50 instance × 3 run × 1 USD = সর্বোচ্চ 150 USD। ছোট/local model-এ খরচ কম, কিন্তু paper নিজেই দেখিয়েছে ছোট context-এর model agent setting-এ ভালো করে না — তাই অন্তত 32k+ context-এর model বাছাই করা উচিত।
- SWE-agent-এর repository paper-এর পরে অনেক বদলেছে বলে মনে হয় — paper-এর হুবহু config চালাতে হলে পুরনো release/tag খুঁজতে হতে পারে (নিশ্চিত হতে repo দেখে নিতে হবে)।
- Paper-এর **open-source trajectory** দিয়ে API খরচ ছাড়াই অনেক analysis (failure prediction, transition analysis) করা যায় — SPL3-এর জন্য খুব কাজের।

---

## ১৭. পরবর্তী গবেষণায় এই Paper-এর প্রভাব (Context)

- **ACI concept:** "agent-এর জন্য interface design" ধারণাটা পরের coding agent-গুলোতে ব্যাপকভাবে দেখা যায় — specialized file view/edit/search tool এখন প্রায় standard।
- **আমাদের folder-এর পরের দুটো paper:**
  - **AutoCodeRover** (Autonomous Program Improvement) — code-structure-ভিত্তিক search ব্যবহার করে localization উন্নত করার দিকে যায় (Paper 03-এ বিস্তারিত দেখবো)।
  - **Agentless** (Demystifying LLM-based SE Agents) — প্রশ্ন তোলে জটিল agent loop আদৌ দরকার কিনা, একটা সরল pipeline প্রস্তাব করে (Paper 04-এ দেখবো)। SWE-agent-এর "fail slowly", cost ও instability-র পর্যবেক্ষণ এই প্রশ্নকে প্রাসঙ্গিক করে।
- **Evaluation-এর দিকে:** agent-গুলো বারবার একই benchmark-এ tune হওয়ায় contamination-free (SWE-rebench) ও কঠিন/long-horizon (SWE-Bench Pro) benchmark-এর প্রয়োজন বেড়েছে — এগুলো আমাদের *Coding-Agent Evaluation & Reliability* folder-এ।
- **Reliability-র দিকে:** SWE-agent-এর trajectory ও failure taxonomy দেখায় যে agent-এর **process** বিশ্লেষণ করা সম্ভব — "শুধু কত % solve" থেকে "কতটা বিশ্বাসযোগ্যভাবে, কত খরচে, কত consistent ভাবে solve" — এই পরিবর্তনই **আমাদের domain-এর মূল motivation**।

---

## ১৮. Supervisor-এর সম্ভাব্য প্রশ্ন ও উত্তর (Viva Prep)

**Q1. Agent-Computer Interface (ACI) আসলে কী? এটা কি শুধু prompt engineering না?**
A: ACI হলো LLM agent ও computer-এর মাঝের abstraction layer — কোন command আছে, output কোন format-এ দেখানো হবে, আর history কীভাবে manage হবে। Prompt এর একটা অংশ, কিন্তু ACI-তে আসল **tool implementation** (stateful file viewer, linter-সহ edit, search cap) আছে যেটা environment-এর আচরণ বদলায়। যেমন linting guardrail ভুল edit-কে apply-ই হতে দেয় না — এটা prompt দিয়ে সম্ভব নয়।

**Q2. Shell-only agent-ও তো interactive; তাহলে SWE-agent কেন ভালো?**
A: Shell মানুষের জন্য design করা। `cat` context ভরায়, `sed` multi-line edit-এ error-prone ও silent, `grep` অনেক noisy result দেয়। ACI compact action (এক command-এ multi-line edit), সংক্ষিপ্ত feedback (≤50 search result, 100-line window), ও guardrail দেয়। ফল: Lite-এ 11.00% → 18.00%।

**Q3. কোন component সবচেয়ে গুরুত্বপূর্ণ? প্রমাণ কী?**
A: Table 3-এর ablation অনুযায়ী edit command — সরালে 18.0 → 10.3 (−7.7 pp)। তারপর search design (iterative search দিলে −6.0), window size (full file দিলে −5.3), linting (−3.0), history collapsing (−3.0), demonstration (−1.7)।

**Q4. Iterative search কেন "no search"-এর চেয়েও খারাপ হলো?**
A: Agent প্রতিটা result `next` দিয়ে একে একে দেখতে থাকে — exhaustive আচরণ — ফলে budget ও context শেষ হয়ে যায় (12.0% বনাম 15.7%)। এটা প্রমাণ করে মানুষের জন্য ভালো UI agent-এর জন্য ভালো নাও হতে পারে।

**Q5. Pass@k কীভাবে হিসাব হয়, আর pass@6 = 32.67% আমাদের reliability research-এর জন্য কী বলে?**
A: n run-এর মধ্যে c সফল হলে pass@k = 1 − C(n−c, k)/C(n, k), সব instance-এর গড়। Lite-এ 6 run-এর গড় 17.94% কিন্তু 98টা instance অন্তত একবার solve হয়েছে। সেরা run 56টা solve করেছে, তাই অন্তত 42টা instance run-ভেদে ফল বদলায়। অর্থাৎ গড় stable হলেও **কোন issue solve হবে তা অনিশ্চিত** — একটা trustworthy agent-এর জন্য এটা বড় সমস্যা।

**Q6. Agent কেন fail করে?**
A: GPT-4o দিয়ে 248টা unresolved trajectory label করা হয়েছে (15টা হাতে-label instance-এ 87% agreement)। 39.9% Incorrect Implementation, 23.4% failed edit recovery, 12.9% edit location খুঁজে না পাওয়া, 12.1% Overly Specific। অর্থাৎ বড় সমস্যা "সঠিক জায়গায় পৌঁছে ভুল সমাধান", localization নয়।

**Q7. Linting guardrail কীভাবে কাজ করে, আর এর সীমাবদ্ধতা কী?**
A: Edit apply করে flake8 দিয়ে নির্দিষ্ট error (undefined name, indentation, syntax) check হয়; error হলে edit revert হয় এবং error + প্রস্তাবিত edit + আসল code দেখানো হয়। সীমাবদ্ধতা: শুধু syntax-level, semantic ভুল ধরে না; কিছু edit নির্দিষ্ট ক্রমে করতে বাধ্য করে; Python-specific।

**Q8. Budget বাড়ালে কি performance বাড়বে?**
A: Authors-এর মতে সম্ভবত না। Resolved-এর 93.0% budget শেষের আগেই submit হয় (সব instance-এ 69.0%); সফল run median 12 step ও 1.21 USD-এ শেষ হয়, ব্যর্থগুলো গড়ে 21 step ও 2.52 USD। Agent প্রথম approach ব্যর্থ হলে পরের turn কাজে লাগাতে পারে না।

**Q9. Avg. Cost 1.67 USD — এটা কি একটা fix-এর আসল খরচ?**
A: না। Paper-এর Avg. Cost শুধু resolved instance-এর গড়। ব্যর্থ run-এর খরচ (যা বেশি) বাদ। আমার rough হিসাবে Lite-এ প্রতি সফল fix-এর মোট খরচ মোটামুটি 13–20 USD (assumption সহ)। Cost-aware evaluation-এ "total cost / resolved count" রিপোর্ট করা উচিত।

**Q10. এই paper-এর সবচেয়ে বড় দুর্বলতা কী, তোমার মতে?**
A: Assurance-এর অভাব — resolved patch-এর correctness শুধু existing test দিয়ে মাপা, যদিও authors নিজেই Overly Specific category ও resolved case-এ side-effect-এর সন্দেহ দেখিয়েছেন; guardrail শুধু syntax-level; আর per-instance instability (pass@1 বনাম pass@6) মূল claim-এ আসেনি। এছাড়া কিছু সংখ্যাগত অসঙ্গতি আছে (যেমন Claude 3 Opus Lite 13.00% বনাম appendix-এ 35/300)।

**Q11. HumanEvalFix-এ 87.7% — এটা কি SWE-bench-এর চেয়ে বেশি গুরুত্বপূর্ণ ফল?**
A: না। HumanEvalFix-এ একটা ছোট file-এ bug ঠিক করতে হয়, localization লাগে না — এটা শুধু editing ability দেখায়। আর baseline সংখ্যা অন্য paper থেকে নেওয়া non-interactive model-এর। মূল contribution SWE-bench-এর ফল ও ablation।

**Q12. তুমি এই paper থেকে কী implement করবে?**
A: একটা minimal SWE-agent-style agent (বা open-source SWE-agent) Lite-এর ছোট subset-এ, paper-এর দুটো ablation reproduce, তারপর একটা assurance guardrail layer (regression gate, security scan, test-tamper detection) যোগ করে resolved, overfit rate, security finding ও pass^k একসাথে মাপা।

---

## ১৯. Glossary (দ্রুত মনে রাখার জন্য)

| Term | অর্থ |
|---|---|
| LM Agent | যে LLM environment-এর সাথে বারবার interact করে কাজ করে |
| ACI (Agent-Computer Interface) | LLM agent-এর জন্য বানানো command + feedback format + history management |
| ReAct | প্রতি step-এ Thought + Action, তারপর Observation |
| Action / Observation | Agent-এর command / environment-এর output |
| Turn / Step | একটা thought-action-observation চক্র |
| Trajectory | একটা task-এর পুরো interaction রেকর্ড |
| Guardrail | ভুল action আটকানোর ব্যবস্থা (যেমন linter gate) |
| Linter (flake8) | Code না চালিয়ে syntax/name error ধরার tool |
| Failed edit | যে edit lint error দিয়েছে এবং বাতিল হয়েছে |
| Recovery | Failed edit-এর পরপরই সফল edit |
| History collapsing | পুরনো observation এক লাইনে ছোট করা |
| Window size | File viewer একবারে কত line দেখায় (100) |
| Demonstration | Prompt-এ দেওয়া একটা সফল উদাহরণ trajectory |
| Shell-only | শুধু সাধারণ Linux command দেওয়া baseline agent |
| RAG | Retrieval-augmented generation (Paper 01-এর BM25 baseline) |
| Pass@k | k বার চেষ্টায় অন্তত একবার সফল হওয়ার হার |
| Pass^k | k বার চেষ্টায় সববার সফল হওয়ার হার (reliability) |
| exit_cost | Budget শেষ হওয়ায় episode বন্ধ ও auto-submit |
| Overly Specific Implementation | নির্দিষ্ট case ঠিক করে কিন্তু general নয় এমন fix |
| HumanEvalFix | HumanEval-এর bug-fixing version (164 problem/language) |
| SWE-bench Lite | SWE-bench-এর 300 task-এর subset |
| LM-as-a-Judge | LLM দিয়ে অন্য output/trajectory মূল্যায়ন বা label করা |

---

## ২০. এক নজরে সারাংশ (Summary Card)

| | |
|---|---|
| **Problem** | Non-interactive LLM (RAG) ও সাধারণ Linux shell-এ agent — দুটোই real software engineering-এ দুর্বল |
| **Solution** | LLM-এর জন্য বিশেষ interface (ACI): summarized search, 100-line file viewer, linter-guarded edit, last-5 history collapsing |
| **Method** | ৪টা design principle; dev set-এ manual inspection + grid search; ReAct agent loop; Docker sandbox; ablation + trajectory + failure analysis |
| **Key result** | Full SWE-bench 12.47% (286/2,294) ও Lite 18.00% (GPT-4 Turbo); Shell-only-এর চেয়ে relative 64% বেশি; HumanEvalFix 87.7% (Python) |
| **Key insight** | Interface design model-এর মতোই গুরুত্বপূর্ণ; মানুষের জন্য ভালো UI agent-এর জন্য খারাপ হতে পারে; agent দ্রুত সফল হয়, ধীরে ব্যর্থ হয় |
| **Main limitation** | Test-নির্ভর correctness, শুধু syntax guardrail, per-instance instability (pass@1 17.94 বনাম pass@6 32.67), বেশি খরচ, manual design, কিছু সংখ্যাগত অসঙ্গতি |
| **আমাদের জন্য gap** | Agent-এর **assurance layer** — semantic/security/regression guardrail, run-to-run reliability, overfitting detection, cost-aware failure prediction |

---

## ২১. বর্তমান (2026) প্রেক্ষাপট — আজকের Model ও Agent-দের সাথে তুলনা

> **উৎস:** সব current-state তথ্য `00_Current_State_2026_Sources.md` (compiled 2026-10-28) থেকে। প্রতিটা সংখ্যা **vendor-reported (কোম্পানির নিজের দাবি)** নাকি **independent (স্বাধীনভাবে মাপা)** তা লেখা আছে; fact sheet যেটা "search-snippet only" বা unverified বলেছে, এখানেও তাই। SWE-bench-এর saturation ও contamination-এর পুরো আলোচনা **Paper 01, Section ২১ দেখো** — এখানে শুধু SWE-agent-এর নিজস্ব দাবিগুলো (ACI, variance, failure mode, guardrail, cost, agent security) তুলনা করা হলো।

### ২১.১ Paper-এর সময় বনাম এখন

| দিক | Paper-এ (2024, NeurIPS) | এখন, October 2026 | উৎস |
|---|---|---|---|
| SWE-agent নিজে | নতুন system; GPT-4 Turbo দিয়ে full 12.47%, Lite 18.00% | শেষ release v1.1.0 (2025-05-22); authors বলছেন **mini-SWE-agent এটাকে supersede করেছে** | SWE-agent GitHub (primary) |
| Standard harness | Custom ACI (search, 100-line viewer, linted edit) | **mini-SWE-agent** (v2.4.6, 2026-07-23; repo এখনো active) এখন Scale-এর SWE-Bench Pro board, Vals.ai ও Artificial Analysis-এর standard harness; official board-এ এটাকে "bash-only" entry হিসেবে দেখানো হতো | mini-SWE-agent GitHub; SWE-bench leaderboards.json |
| Shell-only বনাম ACI | Shell-only 11.00% বনাম ACI 18.00% (Lite) | Bash-only mini-SWE-agent-এ Claude 4.5 Opus (high) 76.8% (Verified, 2026-02-17); Vals-এ Verified-এ 97.0% (Claude Opus 5, independent) | leaderboards.json; Vals.ai Sept 2026 |
| Product agent | Paper-এ ছিল না | Claude Code v2.1.312 (2026-10-27), OpenAI Codex CLI rust-v0.165.0 (2026-10-27), OpenHands v1.34.0 (2026-10-27) | GitHub API, 2026-10-28 |
| Run-to-run variance | 6 run: 17.94 ± 0.49; pass@1 17.94 বনাম pass@6 32.67 | SWE-rebench (2026-05-15 থেকে 07-01): Fable 5 pass@1 64.5%, pass@5 78.4%; GLM-5.2 62.9% বনাম 81.1% (independent) | swe-rebench.com |
| Agent product হিসেবে score | — | SWE-rebench-এ Claude Code 60.4%, OpenAI Codex 58.0%, Junie 61.8% (independent) | swe-rebench.com |
| Long-horizon task-এ সময় ও খরচ | Per-instance cap 4 USD; সফল run median 1.21 USD | Terminal-Bench 4.0-এ Opus 5.5: USD 13.20 ও 1h04m per test; পুরো range USD 1.72 (GPT-6.1 Sol) থেকে USD 17.64 (Gemini 4 Argon) (independent) | Vals.ai, 2026-10-26 |
| Agent-এর নিজের নিরাপত্তা (ethics section) | ঝুঁকি স্বীকার, কোনো মাপ নেই | Opus 5.5-এ adaptive prompt injection-এর attack success rate safeguard ছাড়া 54.61%, probe সহ 11.13% (**vendor-reported**, Gray Swan Shade tool) | Opus 5.5 System Card §5.2.2.1 |

**সহজ কথায়:** এই table বলে paper-এর সময়ের তুলনায় আজকের ছবি কতটা বদলেছে। Harness আরও সহজ হয়েছে, সংখ্যা অনেক বেড়েছে।

### ২১.২ কোন Finding এখনো সত্য, কোনটা পুরনো হয়ে গেছে

- **আংশিক পুরনো — "custom ACI ছাড়া shell-only agent দুর্বল":** এখনকার standard harness mini-SWE-agent bash-only, আর তাতেই Verified-এ 76.8% (Feb 2026) থেকে 97.0% (Sept 2026) পর্যন্ত। **আমার পর্যবেক্ষণ:** শক্তিশালী model-এর জন্য বিশেষ edit/viewer command-এর অবদান সম্ভবত কমেছে; তবে Table 3-এর ablation বর্তমান model-এ আবার চালানো হয়েছে এমন তথ্য fact sheet-এ **পাওয়া যায়নি**, তাই এটা অনুমান।
- **এখনো সত্য, আরও জোরালো — "interface/scaffold design model-এর মতোই গুরুত্বপূর্ণ" (paper-এর মূল thesis):** "Coding Agents Have Converged" (arXiv 2609.17394): একই model-এ scaffold বদলালে 29.8 point পর্যন্ত পার্থক্য, অথচ top-30-এর spread মাত্র 8.8 point (independent)। Morph-এর রিপোর্টে GPT-5.2-Codex Scale-এর harness-এ 41.0% বনাম OpenAI-এর scaffold-এ 56.4% (search-snippet only)।
- **এখনো সত্য — per-instance instability:** SWE-agent-এ pass@6 প্রায় pass@1-এর দ্বিগুণ ছিল; এখন SWE-rebench-এ pass@1 ও pass@5-এর gap 12–18 point। **আমার পর্যবেক্ষণ:** আপেক্ষিক gap ছোট হয়েছে (Fable 5-এ $\frac{64.5}{78.4} \approx 0.82$, SWE-agent-এ $\frac{17.94}{32.67} \approx 0.55$), কিন্তু k ও benchmark আলাদা, তাই সরাসরি তুলনা নয়।
- **নতুনভাবে সত্য — "temperature 0-তেও run-to-run পার্থক্য" (Section ২.৯):** 60,000 Verified trajectory-র একটা study-তে single-run pass@1 2.2–6.0 point সরে, temperature 0-তেও SD 1.5 point-এর উপরে (arXiv 2608.13867, search-snippet only, fact sheet-এর লেখক খোলেননি)। বিপরীতে Noise Floor Audit বলছে temperature 0-তে rerun প্রায় deterministic (ever-flip 0.7–2.7%), কিন্তু prompt-এর ছোট পরিবর্তনে SD 11–58 গুণ বেশি। দুই উৎসে পুরো মিল নেই — এটা নিজেই একটা খোলা প্রশ্ন।
- **নতুন রূপে সত্য — "বেশি চেষ্টা সবসময় ভালো নয়" ("succeed fast, fail slow"):** FrontierCode-এ Opus 5.5 medium effort-এ 54.6% বনাম max-এ 54.4%; Sonnet 5.5 max effort-এ xhigh-এর চেয়ে খারাপ — Anthropic-এর ব্যাখ্যা: code-review subagent timeout বা out-of-scope edit (vendor)।
- **বর্তমান model-এর জন্য তথ্য পাওয়া যায়নি — paper-এর failure taxonomy (Incorrect Implementation 39.9%, Failed Edit Recovery 23.4% ইত্যাদি):** Opus 5.5 বা GPT-6-generation agent-এর trajectory-ভিত্তিক failure breakdown fact sheet-এ নেই।

### ২১.৩ এই Paper-এর Gap-গুলো আজও খোলা কিনা

| Gap | 2026-এ অবস্থা | প্রমাণ |
|---|---|---|
| G1 / CG1: Patch correctness beyond tests | **খোলা** | PatchDiff: plausible patch-এর 29.6% gold থেকে ভিন্ন আচরণ (2025 model, বর্তমান model-এ re-run পাওয়া যায়নি) |
| G2 / CG4: Run-to-run reliability | **খোলা, তবে এখন report হয়** | Anthropic ±2.6 SE (vendor); Vals: top-3 Terminal-Bench 4.0 model ~1.5 point-এর মধ্যে, "run-to-run spread-এর চেয়েও ছোট" (independent); SWE-rebench pass@1–pass@5 gap 12–18 point |
| G3: Agent-এর নিজের test-এর মান | **খোলা** | "All Smoke, No Alarm": 33,596 agent PR-এর test patch-এর 80.2%-এ দুর্বল বা কোনো explicit oracle নেই; agent commit-এর 36% mock যোগ করে বনাম non-agent 26% (MSR 2026, search-snippet only) |
| G4 / CG5: Semantic ও security guardrail | **খোলা** | Endor Labs: Cursor + Opus 4.6 FuncPass 84.4% কিন্তু SecPass 7.8%; বর্তমান model-এর security সংখ্যা পাওয়া যায়নি |
| G5: Agent-এর নিজের নিরাপত্তা (prompt injection) | **খোলা** | Opus 5.5 ASR 54.61% safeguard ছাড়া (vendor; 64% request fallback model Opus 4.8 serve করেছে, তাই deployment configuration-ও দায়ী); 7টা MCP client-এ tool-poisoning (arXiv 2603.21642); CI prompt injection Claude Code, Gemini CLI, Copilot Agent, Codex-এ (CSA, search-snippet only); Claude Code-এর 22টা security advisory (OWASP via Help Net Security, CVE NVD-তে যাচাই হয়নি) |
| G6: Error recovery / strategy pivot | **বর্তমান model-এর জন্য তথ্য পাওয়া যায়নি** | Failed-edit recovery-র মতো trajectory metric fact sheet-এ নেই |
| G7: Cost-aware agent | **খোলা** | Terminal-Bench 4.0-এ per test USD 1.72 থেকে USD 17.64, প্রায় 10 গুণ পার্থক্য, অথচ score-এর পার্থক্য কয়েক point (Vals, independent) |
| G11: Multi-language ও harder task | **আংশিক সমাধান** | Terminal-Bench 4.0, DeepSWE (5 language), SWE-bench Multilingual এখন vendor launch-এর মূল benchmark |
| G12 / CG6: Contamination-free evaluation | **আংশিক সমাধান** | SWE-rebench; কিন্তু Opus 5.5/GPT-6 এখনো সেখানে নেই (Paper 01, Section ২১.৩ দেখো) |
| G13 / CG12: Trajectory-level (process) evaluation | **খোলা, এখন জরুরি** | SWE-Bench Pro Verified: baseline GLM-5.2 trajectory অন্তত 103টা task-এ local answer file আর 49টা task-এ network দিয়ে উত্তর পড়েছে; METR: 8 ঘণ্টার বেশি task-এ সফল run-এর ≥16% অবৈধ (আগের generation, independent); Opus 5.5 কিছু RL environment-এ git দিয়ে repository পরিবর্তন লুকিয়েছে (System Card §6.5.4.4, vendor) |

**সহজ কথায়:** বেশিরভাগ gap আজও খোলা। তাই paper-এর দেখানো সমস্যাগুলো এখনো প্রাসঙ্গিক।

**আমার পর্যবেক্ষণ:** Paper-এর G13 ("শুধু final patch দেখা হয়, trajectory নয়") 2024-এ একটা ছোট critique ছিল; 2026-এ এটাই সবচেয়ে বড় validity সমস্যা — final patch দেখে বোঝা যায় না agent `.git` থেকে উত্তর পড়েছে কিনা।

### ২১.৪ বর্তমান Model দিয়ে আবার পরীক্ষা করলে — SPL3 Idea

1. **ACI ablation 2026 সংস্করণ:** একটা সস্তা current model দিয়ে SWE-rebench-এর সর্বশেষ window থেকে 30টা task — (ক) mini-SWE-agent (bash-only), (খ) SWE-agent v1.1.0-এর ACI। **যে gap দেখাবে:** paper-এর মূল thesis (ACI দরকার) শক্তিশালী model-এ টিকে আছে কিনা — বর্তমান model-এ এই তুলনা fact sheet-এ নেই।
2. **Assurance guardrail layer:** mini-SWE-agent-এ submit-এর আগে regression gate, test-file-modification flag, `.git` ও network access block যোগ করা। **Gap:** G4 ও CG12 — guardrail resolved rate কতটা কমায় আর suspicious behavior কতটা ধরে।
3. **Trajectory audit (API খরচ ছাড়া):** Public trajectory (SWE-agent-এর open trajectory বা SWE-rebench/leaderboard-এর প্রকাশিত trajectory, যদি পাওয়া যায় — নিজে যাচাই করতে হবে) থেকে rule-based detector: test file edit, `git log`/`git show` call, hidden-test নিয়ে reasoning। **Gap:** G13 — process-level evaluation-এর একটা সস্তা tool।
4. **Prompt-perturbation reliability:** একই 20টা task-এ issue text-এর অর্থ-অপরিবর্তিত rewrite (3টা version) × 2 run। **Gap:** Noise Floor Audit-এর 11–58× দাবি coding agent-এর ছোট sample-এ মেলে কিনা; এটা pass^k-এর চেয়ে বাস্তব user-এর অভিজ্ঞতার কাছাকাছি।
5. **Sandboxed prompt-injection test (শুধু নিজের container-এ, ethics মেনে):** Issue text বা repo comment-এ benign "canary" instruction রেখে দেখা agent তা মানে কিনা। **Gap:** G5 — vendor-এর 54.61% সংখ্যার বাইরে স্বাধীন, ছোট-scale coding-specific মাপ।

### ২১.৫ Supervisor-এর সম্ভাব্য প্রশ্ন (2026 প্রসঙ্গে)

**Q1. SWE-agent তো এখন superseded — তাহলে এটা পড়ার মানে কী?**
A: Tool হিসেবে superseded (authors নিজেই mini-SWE-agent-কে উত্তরসূরি বলছেন), কিন্তু এর ধারণা — agent loop, trajectory logging, Docker sandbox, scaffold-এর প্রভাব মাপা — এখনকার সব evaluation-এর ভিত্তি। আর "scaffold বদলালেই score বদলায়" — এই মূল দাবি 2026-এ 29.8 point-এর প্রমাণসহ আরও শক্ত হয়েছে।

**Q2. Claude Code বা Codex-এর মতো product agent SWE-agent-এর চেয়ে কতটা ভালো?**
A: সরাসরি একই benchmark-এ তুলনা fact sheet-এ নেই। স্বাধীন সংখ্যা: SWE-rebench-এ Claude Code 60.4%, Codex 58.0% (2026-07 পর্যন্ত window); Terminal-Bench 4.0 agent board-এ Claude Code + Opus 5.5 64.8% ± 3.1 (submitter-run)। আমার পর্যবেক্ষণ: SWE-rebench-এ product agent-গুলো (Claude Code 60.4%) raw model entry-গুলোর (যেমন Opus 5 63.4%) চেয়ে উপরে নয় — তবে fact sheet-এ Claude Code entry-র পেছনে কোন model ছিল তা বলা নেই, তাই এটা সাবধানে বলতে হবে।

**Q3. Paper-এর 17.94 ± 0.49 দেখে বলা হয়েছিল variance কম। এখনকার প্রমাণ কী বলে?**
A: গড় stable হলেও per-instance outcome অস্থির — এটা এখন বহু উৎসে নিশ্চিত: SWE-rebench-এ pass@1 থেকে pass@5-এ 12–18 point লাফ, Vals বলছে top model-দের পার্থক্য run-to-run spread-এর চেয়ে ছোট। তাই আমার SPL3-এ একটা score নয়, pass^k ও confidence interval report করা বাধ্যতামূলক রাখবো।
