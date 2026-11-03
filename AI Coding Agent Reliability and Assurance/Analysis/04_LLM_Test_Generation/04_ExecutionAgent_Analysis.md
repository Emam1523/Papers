# Paper Analysis 04 (TestGen): ExecutionAgent — An LLM Agent to Execute Tests of Arbitrary Projects

> **Sub-domain:** LLM Test Generation
> **Analysis করেছে:** SPL3 — AI Coding Agent Reliability and Assurance
> **Paper file:** `LLM Test Generation/An LLM Agent to Execute Tests of Arbitrary Projects.pdf`
> **আগে পড়ো:** Sub-domain 1, Paper 01 (SWE-bench) — F2P/P2P test, regression test, Docker harness; Sub-domain 1, Paper 02 (SWE-agent) — agent scaffold, ReAct loop, Agent-Computer Interface; Sub-domain 1, Paper 04 (Agentless) — regression test filtering ও reproduction test; Sub-domain 3, Paper 01 (SWE-rebench) — LLM দিয়ে automated environment setup। Sub-domain 1–3 Summary — common gap **CG1–CG12** আর প্রস্তাবিত "assurance report for AI agent patches"।

---

## ০. Paper-এর পরিচয় (Bibliographic Info)

| বিষয় | তথ্য |
|---|---|
| **Title** | You Name It, I Run It: An LLM Agent to Execute Tests of Arbitrary Projects |
| **Authors** | Islem Bouzenia, Michael Pradel |
| **Institution** | University of Stuttgart, Germany |
| **Venue** | Proceedings of the ACM on Software Engineering (PACMSE), Vol. 2, No. ISSTA, Article ISSTA047, July 2025 — অর্থাৎ **ISSTA 2025** (International Symposium on Software Testing and Analysis), software testing-এর top-tier venue |
| **Dates** | Received 2025-02-27; accepted 2025-03-31 |
| **DOI** | 10.1145/3728922 (23 pages, Creative Commons Attribution 4.0 license) |
| **Paper type** | **Technique + empirical evaluation** — একটা নতুন LLM agent (ExecutionAgent) আর 50টা project-এর উপর তার মূল্যায়ন |
| **Artifacts** | Code: github.com/sola-st/ExecutionAgent; archive: doi.org/10.5281/zenodo.15202434 |
| **Funding** | European Research Council (grant 851895 ও 101155832), German Research Foundation (DeMoCo ও QPTest project) |
| **আমাদের domain-এ গুরুত্ব** | ⭐⭐⭐⭐⭐ — Assurance layer-এর সব **dynamic signal** (regression test, generated test, reproduction test) চালাতে হলে আগে project-টা build করে তার test suite চালাতে হয়। এই paper ঠিক সেই "আগের ধাপ"-টাই automate করে। এটা না থাকলে আমাদের assurance report শুধু static signal-এ সীমাবদ্ধ থাকবে। |

---

## ★ সহজ ভাষায় পুরো Paper (প্রথমবার পড়ার জন্য)

### ক. Paper-টা কী নিয়ে?
- এটা একটা **নতুন tool-এর paper**। Tool-টার নাম **ExecutionAgent**। সাথে 50টা আসল project-এ tool-টা পরীক্ষা করে দেখানো হয়েছে।
- Paper লিখেছেন Stuttgart University-র (জার্মানি) Islem Bouzenia আর Michael Pradel। এটা ISSTA 2025-এ ছাপা হয়েছে। ISSTA হলো software testing-এর একটা বড় conference।
- Tool-টা একটা AI agent (মানে এমন AI, যে নিজে নিজে একের পর এক কাজ করতে পারে)।
- তুমি শুধু একটা GitHub project-এর link দেবে। Agent নিজে terminal-এ command চালাবে, project-টা তৈরি করবে আর তার test চালাবে।
- শেষে সে বলবে কয়টা test pass করল, কয়টা fail করল, কয়টা skip হলো।
- সহজ করে বললে: "অচেনা project-এর test চালানোর কাজটা automatic করা।"

### খ. সমস্যাটা কী ছিল?
- ধরো তুমি একটা নতুন বাসায় উঠেছ। একটা আলমারি কিনেছ, যেটা নিজে জোড়া লাগাতে হবে। Manual-টা অর্ধেক লেখা, কিছু screw-এর নাম ভুল। তুমি চেষ্টা করছ, ভুল করছ, আবার চেষ্টা করছ।
- অচেনা software project-এর test চালানোও ঠিক এমন। প্রতিটা project-এর ভাষা আলাদা, tool আলাদা, দরকারি library-র version আলাদা। README প্রায়ই অসম্পূর্ণ বা পুরনো।
- **একটা concrete example:** OpenVPN নামে একটা C project-এর test চালাতে `autoconf`, `libtool`, `cmocka` সহ প্রায় 13টা system package আগে install করতে হয়। তারপর `autoreconf`, `./configure`, `make`, `make check` — এই ক্রমে command চালাতে হয়। কোনো একটা বাদ গেলে test চলেই না।
- আগে এই কাজ মানুষ হাতে করত। এতে অনেক সময় লাগত, আর হাজার হাজার project-এ করা অসম্ভব ছিল।
- যেসব automatic script ছিল, সেগুলো সাধারণত শুধু একটা ভাষার জন্য। যেমন GitBug-Java 66,042টা repository নিয়ে শুরু করে মাত্র 228টার test চালাতে পেরেছিল।
- আমাদের জন্য এটা কেন জরুরি: AI agent-এর বানানো patch ঠিক কিনা দেখতে হলে test চালাতেই হয়। কিন্তু test চালানোর আগে project-টা চালু অবস্থায় আনতে হয়। SWE-bench এই কাজ মানুষ দিয়ে করিয়েছিল, তাই আমরা সমস্যাটা এতদিন দেখিনি।

### গ. Paper কী solve করেছে?
- Paper একটা **general agent** বানিয়েছে, যেটা যেকোনো ভাষার project-এ কাজ করে। 14টা ভাষার 50টা project-এ পরীক্ষা হয়েছে।
- Agent-এর output দুটো file: একটা **Dockerfile** (পরিবেশ বানানোর recipe) আর একটা **script** (সেই পরিবেশে build ও test চালানোর command)। একবার বানানো হলে এগুলো বারবার ব্যবহার করা যায়।
- নতুন একটা ধারণা দিয়েছে: **meta-prompting**। এতে AI-কে দিয়েই AI-এর নিজের জন্য নিয়ম (guideline) লেখানো হয়।
- দেখিয়েছে যে শুধু "build হয়েছে" যথেষ্ট না। Build করা আর test চালানো একদম আলাদা ক্ষমতা।
- **গুরুত্বপূর্ণ সংখ্যা ১:** 50টা project-এর মধ্যে **33টার** test suite সফলভাবে চলেছে। মানে ১০০টার মধ্যে ৬৬টা।
- **গুরুত্বপূর্ণ সংখ্যা ২:** সেরা পুরনো পদ্ধতি চালাতে পেরেছিল মাত্র **5টা**। তাই ExecutionAgent **6.6 গুণ** ভালো। পুরনো পদ্ধতির হিসাবে ১০০টার মধ্যে মাত্র ১০টা।
- **গুরুত্বপূর্ণ সংখ্যা ৩:** গড় খরচ মাত্র **0.16 USD** আর **74 মিনিট** প্রতি project। মানে এক কাপ চায়ের দামেরও কম।

### ঘ. কীভাবে solve করেছে?
1. **ভাষা চেনা:** Project-টা কোন ভাষার, তা GitHub-এর Linguist library দিয়ে বের করা হয়।
2. **LLM-কে জিজ্ঞেস করা (meta-prompting):** "Java project-এর test চালাতে কোন 10টা নিয়ম মানা উচিত?" LLM-এর উত্তরটাই agent-এর নিয়মের তালিকা হয়ে যায়।
3. **Hint জোগাড়:** Project-এর CI script (maintainer-এর লেখা "কীভাবে test চলে" file) পড়ে সংক্ষেপ করা হয়। সাথে web search করে উপরের 5টা page-এর install-এর তথ্য নেওয়া হয়।
4. **Terminal-এ চেষ্টা করা:** Agent এবার Docker container-এর ভেতরে একটা একটা করে command চালায়। প্রতিবার সে আগে "ভাবে" (thought), তারপর command দেয়।
5. **Output ছোট করা:** Command-এর output বেশি লম্বা (200 token-এর বেশি) হলে আরেকটা LLM call দিয়ে সংক্ষেপ করা হয়। নইলে agent অপ্রয়োজনীয় তথ্যে হারিয়ে যায়।
6. **ভুল থেকে শেখা:** Command আটকে গেলে সময়সীমা (5 মিনিট) পার হলে agent ঠিক করে অপেক্ষা করবে, input দেবে না বন্ধ করবে। একটা চেষ্টায় সর্বোচ্চ 40 command। ব্যর্থ হলে "কী শিখলাম" লিখে আবার চেষ্টা, মোট 3 বার পর্যন্ত।
7. **শেষ যাচাই:** Agent "কাজ শেষ" বললে control center দেখে তিনটা file আছে কিনা: Dockerfile, install script আর test result file।
8. **আসলের সাথে মেলানো:** শেষে সংখ্যাগুলো CI log-এর আসল সংখ্যার সাথে মিলিয়ে দেখা হয়, কতটা কাছাকাছি।

### ঙ. এরপর কী করা যায়?
- **Authors যা বলেছেন:** একই ভুল বারবার করা কমানো; পুরনো dependency-র project আর একাধিক configuration (ভিন্ন OS বা browser) সামলানো; আর এই environment দিয়ে AI agent-এর patch যাচাই করে দেখা (paper এটাকে "vision" বলেছে, পরীক্ষা করেনি)।
- **এখনো খোলা প্রশ্ন:** Agent যে result file লেখে, সেটা আসলেই সত্য কিনা — paper শুধু file আছে কিনা দেখে। একই project বারবার চালালে ফল একই হয় কিনা, তাও জানা নেই।
- **আরেকটা খোলা প্রশ্ন:** পুরনো commit-এ (যেমন SWE-bench-এর base commit) কাজ করে কিনা। Paper শুধু সর্বশেষ version পরীক্ষা করেছে।
- **SPL3-এ আমরা করতে পারি (১):** Agent-এর লেখা result বিশ্বাস না করে, test framework-এর নিজের XML/JSON report থেকে আমরা নিজেরা result পড়বো। সাথে "`|| true` দিয়ে ব্যর্থতা লুকানো হয়েছে কিনা" ধরার checker।
- **SPL3-এ আমরা করতে পারি (২):** SWE-bench বা SWE-rebench-এর ছোট একটা subset-এ ExecutionAgent চালিয়ে দেখা, পুরনো commit-এ per-test স্তরে সে কতটা সঠিক।
- **SPL3-এ আমরা করতে পারি (৩):** একই project কয়েকবার চালিয়ে ফলের variance মাপা। খরচ কম, নতুনত্ব ভালো।

> **মনে রাখো:**
> ExecutionAgent যেকোনো project-এর test চালানোর recipe (Dockerfile ও script) নিজে বানায়: 50টার মধ্যে 33টায় সফল, খরচ গড়ে 0.16 USD।
> কিন্তু "test চলেছে" মানেই "ফল সত্য" নয় — paper শুধু file আছে কিনা দেখে, result সত্য কিনা দেখে না। আমাদের কাজ ঠিক এখানেই।

---

## ১. এক লাইনে Paper (TL;DR)

**ExecutionAgent হলো একটা GPT-4o-mini-চালিত LLM agent, যেটা যেকোনো GitHub project-এর জন্য নিজে নিজে terminal-এ command চালিয়ে, ভুল দেখে শুধরে, একটা Dockerfile আর একটা install-ও-test script তৈরি করে, এবং project-এর test suite চালিয়ে কতগুলো test pass, fail ও skip হলো তা report করে; 14টা language-এর 50টা project-এর মধ্যে 33টার test suite সফলভাবে চালাতে পেরেছে, যা সেরা পুরনো পদ্ধতির (5টা) চেয়ে 6.6 গুণ।**

### Supervisor-কে ৩০ সেকেন্ডে কীভাবে বলবো
> "Sir, AI agent-এর patch সঠিক কিনা যাচাই করতে আমরা সবসময় বলি 'test চালাও'। কিন্তু একটা অচেনা project-এর test চালানোই একটা কঠিন কাজ — ভাষা আলাদা, build tool আলাদা, dependency-র version মেলাতে হয়, documentation অসম্পূর্ণ। SWE-bench এই কাজ মানুষ দিয়ে করেছিল, SWE-rebench Python-এর জন্য নির্দিষ্ট ধাপের LLM pipeline দিয়ে করেছিল। ExecutionAgent এটাকে একটা general agent দিয়ে করে: প্রথমে LLM-কে দিয়েই language-specific guideline লিখিয়ে নেয় (meta-prompting), CI script আর web search থেকে install-এর hint জোগাড় করে, তারপর Docker container-এ terminal command চালিয়ে trial-and-error করে। 50টা project-এর 33টায় test suite চলেছে, তার 29টায় ফলাফল CI-এর আসল ফলাফলের 10%-এর মধ্যে, আর খরচ গড়ে মাত্র 0.16 USD আর 74 মিনিট প্রতি project। আমাদের assurance layer-এর 'test চালানোর অংশ' এখান থেকে আসতে পারে।"

**সহজ কথায়:** ওপরের কথাটা এক বাক্যে: আগে বোঝো test কীভাবে চালাতে হয়, তারপরই বলা যায় patch ঠিক কিনা। ExecutionAgent সেই প্রথম ধাপটা AI দিয়ে করায়।

---

## ২. Background — এই paper বুঝতে যা আগে জানা দরকার

### ২.১ Test Suite, Test Runner ও Test Framework
- **Test suite:** একটা project-এর সব automated test-এর সংগ্রহ। যেমন django-র test suite-এ paper-এর ground truth অনুযায়ী 17,604টা test।
- **Testing framework:** test লেখা ও চালানোর library — Python-এ `pytest`, Java-তে JUnit (Maven-এর ভিতরে Surefire plugin চালায়), JavaScript-এ Jest/Mocha/Jasmine/Karma, C-তে cmocka বা `make check`।
- **Test result-এর তিনটা অবস্থা:** **pass** (প্রত্যাশিত আচরণ), **fail** (assertion ভেঙেছে বা error), **skip** (ইচ্ছাকৃতভাবে চালানো হয়নি — যেমন কোনো optional dependency নেই, বা ভিন্ন OS-এর জন্য)। ExecutionAgent ঠিক এই তিনটা সংখ্যাই report করে।

### ২.২ Build System ও Dependency Installation — ভাষা অনুযায়ী
একটা project-এর source code থেকে চালানোর উপযোগী program বানানোকে **build** বলে। প্রতিটা ভাষার ecosystem আলাদা:

| ভাষা | Build / package tool | Dependency কোথায় লেখা থাকে | Test চালানোর সাধারণ command |
|---|---|---|---|
| Python | pip, conda, setuptools | `requirements.txt`, `setup.py`, `pyproject.toml` | `pytest` |
| Java | Maven, Gradle | `pom.xml`, `build.gradle` | `mvn test`, `gradle test` |
| JavaScript / TypeScript | npm, Yarn | `package.json` | `npm test` |
| C / C++ | Make, CMake, autotools (`autoreconf`, `./configure`) | প্রায়ই README-তে লেখা system library (`apt install libxyz-dev`) | `make check`, `ctest` |

- **কেন কঠিন:** C/C++-এ কোনো standard package manager নেই; system library-র সঠিক version `apt` দিয়ে install করতে হয়, কখনো নিজে compile করতে হয়। Paper-ও বলছে C আর C++ সবচেয়ে কঠিন ছিল।
- **User setup বনাম development setup:** একজন সাধারণ user library ব্যবহার করতে `pip install x` করলেই হয়। কিন্তু **test চালাতে** লাগে development setup — test framework, compiler, কখনো `glibc-32`, কিছু dependency নতুন করে compile করা, config file বদলানো। Paper-এর "LLM scripts" baseline ঠিক এই পার্থক্য না বুঝে ব্যর্থ হয়েছে।
- **Git submodule:** একটা repository-র ভিতরে আরেকটা repository-কে dependency হিসেবে রাখা। Clone করার সময় আলাদাভাবে (`git submodule update --init`) আনতে হয়। Paper-এ 9টা project-এ submodule ছিল, তার মাত্র 2টায় test চলেছে।

**সহজ কথায়:** Test suite হলো পরীক্ষার প্রশ্নপত্র। Build system হলো প্রশ্নপত্র ছাপানোর মেশিন। এক এক ভাষার মেশিন এক এক রকম, তাই agent-কে প্রতিবার আলাদা করে শিখতে হয়।

### ২.৩ Docker Container
- **Container:** একটা হালকা, আলাদা করা (isolated) Linux পরিবেশ। Host machine নষ্ট না করে ভিতরে যেকোনো package install করা যায়।
- **Dockerfile:** container image কীভাবে বানাতে হবে তার recipe — `FROM ubuntu:20.04` (base image), `RUN apt-get install ...` (package install), `WORKDIR` (কোন folder-এ কাজ হবে)।
- **কেন দরকার:** (১) **Reproducibility** — একই Dockerfile থেকে যেকোনো machine-এ একই পরিবেশ; (২) **নিরাপত্তা** — agent যদি ভুল বা ক্ষতিকর command চালায়, ক্ষতি container-এর ভিতরে থাকে। SWE-bench-ও প্রথমে conda ব্যবহার করে পরে Docker-এ গিয়েছিল (SWE-bench analysis, Section ১২.২, critique #8)।
- ExecutionAgent-এর **output-ই** দুটো file: একটা Dockerfile (container বানাতে) আর একটা shell script (container-এর ভিতরে build ও test চালাতে)।

**সহজ কথায়:** Docker হলো একটা বন্ধ ঘর। ঘরের ভেতরে যত খুশি জিনিস বসাও, বাইরের ঘর নষ্ট হয় না। Dockerfile হলো সেই ঘর সাজানোর তালিকা।

### ২.৪ CI/CD Script — Hint হিসেবে
- **Continuous Integration (CI):** প্রতিটা commit বা pull request-এ একটা server স্বয়ংক্রিয়ভাবে project build করে test চালায়। Platform: GitHub Actions (`.github/workflows/*.yml`), CircleCI, Jenkins, CirrusCI, Travis CI ইত্যাদি।
- **কেন hint:** CI file-এ project maintainer নিজে লিখে রেখেছেন কোন OS, কোন package, কোন command দিয়ে test চলে। এটা README-র চেয়ে প্রায়ই বেশি সঠিক, কারণ এটা নিয়মিত চলে।
- **কেন সরাসরি চালানো যায় না:** CI file একটা নির্দিষ্ট platform-এর syntax-এ লেখা (GitHub Actions-এর `uses:` action ইত্যাদি), আর সব platform বাইরের মানুষের জন্য পুরোপুরি চালানো যায় না। সব project-এ CI থাকেও না — paper-এর dataset-এ 7টা project-এ build বা test কোনো script-ই নেই।
- **CI log = ground truth:** CI server-এ চলা test-এর log-এ pass/fail/skip সংখ্যা থাকে। Paper এই সংখ্যাকেই "সঠিক উত্তর" (ground truth) ধরেছে।

### ২.৫ LLM Agent, Tool ও Agent Loop
- **LLM agent:** এমন system যেখানে LLM নিজে ঠিক করে কোন **tool** (terminal, file read/write) কোন argument দিয়ে চালাবে, output দেখে পরের ধাপ ঠিক করে, লক্ষ্য পূরণ না হওয়া পর্যন্ত। (ReAct ধারণা — SWE-agent analysis-এ বিস্তারিত।)
- **Agent tool design:** Agent-কে কোন tool দেওয়া হবে আর tool-এর output কীভাবে ফেরত যাবে — এটাই agent-এর "হাত-পা"। SWE-agent দেখিয়েছিল ভালো interface (ACI) performance বাড়ায়। ExecutionAgent চারটা tool দেয়: `linux_terminal`, `read_file`, `write_file`, `task_done`।
- **Trajectory:** একটা project-এর জন্য agent-এর নেওয়া সব ধাপের ক্রম (thought → command → output → ...)।
- **Command budget:** একটা চেষ্টায় সর্বোচ্চ কতগুলো command চালানো যাবে — খরচ ও অসীম loop থামাতে।

**সহজ কথায়:** Agent-এর হাতে চারটা tool, আর একটা সীমা (command budget) — যাতে সে অনন্তকাল ঘুরতে না থাকে।

### ২.৬ Meta-Prompting ও Guideline
- **সাধারণ prompt engineering:** মানুষ হাতে লিখে দেয় "Java হলে `mvn test` চালাও, Python হলে ..."। সমস্যা: সময়সাপেক্ষ, সব technology কভার করা যায় না, দ্রুত পুরনো হয়।
- **Meta-prompting (এই paper-এর প্রস্তাবিত ধারণা):** LLM-কে একটা উঁচু-স্তরের প্রশ্ন করা — "একটা Java project install করে test চালাতে আমার কোন 10টা guideline মানা উচিত, সর্বশেষ practice মেনে?" — আর সেই **উত্তরকে** agent-এর আসল prompt-এর অংশ বানানো। অর্থাৎ prompt লেখার কাজটাই LLM-কে দিয়ে করানো।
- **Guideline:** ছোট নিয়মের তালিকা — যেমন "pom.xml থেকে Java version মিলিয়ে নাও", "test report বের করতে `mvn surefire-report:report` ব্যবহার করো"। এগুলো agent-কে একটা high-level plan দেয়।
- **Paper-এর যুক্তি:** নতুন train করা LLM-এর মধ্যে নতুন technology-র জ্ঞান থাকে, তাই meta-prompting স্বয়ংক্রিয়ভাবে "আপ-টু-ডেট" থাকে। (সীমাবদ্ধতা: LLM-এর জ্ঞান তার training cutoff পর্যন্ত — Section ১২ দেখো।)

**সহজ কথায়:** Meta-prompting হলো নিজে নিয়ম না লিখে বিশেষজ্ঞকে জিজ্ঞেস করে নেওয়া: "এই কাজে কোন নিয়মগুলো মানব?"

### ২.৭ Output Summarization (Context Management)
`ls -R` বা `npm install`-এর output হাজার হাজার লাইন হতে পারে। পুরোটা prompt-এ দিলে (ক) context window ভরে যায়, (খ) agent অপ্রাসঙ্গিক তথ্যে বিভ্রান্ত হয় (SWE-bench-এর "বেশি context ≠ ভালো" finding-এর মতো), (গ) খরচ বাড়ে। তাই output নির্দিষ্ট সীমা (default 200 token) ছাড়ালে আরেকটা LLM call দিয়ে সংক্ষেপ করা হয়।

**সহজ কথায়:** Output যত লম্বা, agent তত গুলিয়ে ফেলে। তাই লম্বা output-এর সারাংশ prompt-এ রাখা হয়।

### ২.৮ Test Execution Report ও Ground Truth তুলনা
- **Test execution report:** test চালানোর পর তিনটা সংখ্যা — $n_{pass}$, $n_{fail}$, $n_{skip}$। ExecutionAgent এগুলো একটা file-এ লিখে রাখে।
- **Ground truth তুলনা:** একই project-এর CI log-এ যে সংখ্যা আছে, তার সাথে মেলানো। মিললে বোঝা যায় agent "সত্যিই" ঠিক পরিবেশে test চালিয়েছে — শুধু "কিছু একটা চালিয়েছে" নয়।
- **কেন শুধু "test চলেছে" যথেষ্ট নয়:** dependency কম থাকলে অনেক test skip বা fail হয়, অথচ suite "চলেছে" দেখায়। তাই deviation মাপা দরকার (সূত্র Section ৬-এ)।

**সহজ কথায়:** শুধু "test চলেছে" বললে হবে না। CI-এর আসল সংখ্যার সাথে মিলিয়ে দেখতে হবে সত্যিই ঠিক পরিবেশে চলেছে কিনা।

### ২.৯ Flaky Test
যে test একই code-এ কখনো pass, কখনো fail করে — network, timing, floating-point, ক্রম-নির্ভরতার কারণে। Paper-এর baseline Flapy মূলত flaky test গবেষণার জন্য বানানো tool। Ground truth-এর সাথে কিছু অমিলের কারণ হিসেবে paper flakiness-কে দায়ী করেছে।

### ২.১০ Ablation Study
Agent-এর একটা অংশ (যেমন preparation phase) সরিয়ে দিয়ে আবার চালানো — performance কতটা কমে তা দেখে বোঝা যায় অংশটা কতটা জরুরি।

### ২.১১ Cost ও Time পরিমাপ
- **LLM cost:** API-তে input token আর output token-এর আলাদা দাম, প্রতি million token হিসেবে। মোট খরচ = সব call-এর token × দাম।
- **Wall-clock time:** শুরু থেকে শেষ পর্যন্ত আসল সময় — LLM call, package download, compile, test চালানো সব মিলিয়ে। Paper-এর 74 মিনিট এই সময়, একসাথে 5টা project চালানো অবস্থায়।

**সহজ কথায়:** খরচ মানে LLM-কে দেওয়া আর LLM থেকে পাওয়া token-এর দাম। সময় মানে ঘড়ির আসল সময় (শুধু LLM-এর সময় নয়)।

### ২.১২ এই paper আমাদের অন্য sub-domain-এর সাথে কোথায় যুক্ত
| ধারণা | কোথায় আগে এসেছে | এখানে ভূমিকা |
|---|---|---|
| Docker harness ও environment reproducibility | Sub-domain 1, Paper 01 (SWE-bench) | ExecutionAgent-এর output-ই একটা Docker environment |
| Regression test filtering | Sub-domain 1, Paper 04 (Agentless) | Regression test চালাতে আগে কাজ করা environment লাগে |
| LLM-চালিত install recipe | Sub-domain 3, Paper 01 (SWE-rebench) | একই সমস্যা, ভিন্ন সমাধান — agentless recipe বনাম interactive agent |
| Validator feedback loop | Sub-domain 2, Paper 02 (VRpilot) | ExecutionAgent-এর feedback phase একই ধরনের loop |
| Verifier health ও verifier gaming (CG11, CG12) | Sub-domain 3 Summary | Test runner নিজেই verifier-এর অংশ — সে ভুল করলে সব রায় ভুল |

---

## ৩. Problem Statement — কী সমস্যা ছিল?

### ৩.১ মূল সমস্যা
**প্রশ্ন (paper-এর ভাষায়):** একটা যেকোনো project দেওয়া হলে, কীভাবে স্বয়ংক্রিয়ভাবে সেটা build করে তার test suite চালানো যায়?

**Formal লক্ষ্য:** Input = একটা git repository-র URL বা file path। Output = দুটো script — (১) একটা isolated environment (যেমন container) বানানোর script, (২) সেই environment-এর ভিতরে project build করে test চালানোর script। আর test চালানোর ফল (pass, fail, skip সংখ্যা)।

**দুটো বাধ্যতামূলক গুণ:**
1. **Technology-agnostic:** যেকোনো language, build system, testing framework।
2. **Fully automated:** project ছাড়া আর কোনো মানুষের input বা বাড়তি তথ্য লাগবে না।

### ৩.২ কেন কঠিন
- ভিন্ন ভিন্ন language ও ecosystem, প্রত্যেকের নিজস্ব tool ও convention।
- নির্দিষ্ট version-এর library বা tool দরকার — জটিল dependency।
- Documentation অসম্পূর্ণ, অসঙ্গত, বা একেবারেই নেই।
- Environment নিয়ে অলিখিত ধারণা (OS, system configuration)।
- প্রতিটা testing framework-এর setup ও চালানোর পদ্ধতি আলাদা।

### ৩.৩ আগের তিনটা পদ্ধতি ও তাদের দুর্বলতা
| পদ্ধতি | দুর্বলতা |
|---|---|
| মানুষ documentation পড়ে trial-and-error | সময়সাপেক্ষ, অনেক project-এ scale করে না |
| Project-এর CI/CD workflow পুনর্ব্যবহার | সব project-এ নেই; নির্দিষ্ট platform-নির্ভর (যেমন GitHub Actions) যা বাইরের মানুষের জন্য পুরোপুরি চালানো যায় না; একাধিক platform, প্রত্যেকের আলাদা config |
| Heuristic automated script | সাধারণত এক language-এর জন্য; Flapy শুধু PyPI-তে থাকা Python project-এ চলে আর সেখানেও অনেক suite চালাতে পারে না; GitBug-Java-র pipeline 66,042 repository থেকে শুরু করে মাত্র 228টার test চালাতে পেরেছিল |

**সহজ কথায়:** আগের তিনটা পথের কোনোটাই সব project-এ কাজ করে না: মানুষ ধীর, CI সবসময় নেই, আর script শুধু এক ভাষার।

### ৩.৪ সমাধানকে যে চারটা challenge পার হতে হবে
1. বিভিন্ন জনপ্রিয় language-এর **সর্বশেষ technology ও tool** সম্পর্কে জানা।
2. **অসম্পূর্ণ ও আংশিক পুরনো documentation** বোঝা।
3. **System-এর সাথে interact** করা — command চালানো, output দেখা, error সামলানো।
4. Setup **সফল হয়েছে কিনা যাচাই** করা, না হলে test suite না চলা পর্যন্ত সমস্যা সমাধান।

**সহজ কথায়:** Agent-কে চারটা কাজ ঠিকমতো করতে হবে: নতুন technology জানা, অসম্পূর্ণ docs বোঝা, terminal-এর সাথে কথা বলা, আর শেষে যাচাই করা যে সব ঠিকমতো হয়েছে।

### ৩.৫ কেন এটা গুরুত্বপূর্ণ (আমাদের domain-এর চোখে)
Paper নিজেই বলছে: যেসব LLM agent নিজে code বদলায় (SWE-agent, AutoCodeRover ইত্যাদি), তাদের পরিবর্তন যাচাই করতে একটা feedback mechanism লাগে, আর test suite চালানো সেই mechanism দেয়। Defects4J, SWE-bench, DyPyBench-এর মতো benchmark বানাতেও test চালানো লাগে। **আমার পর্যবেক্ষণ:** আমাদের assurance report-এর "regression test signal" আর "generated test signal" — দুটোই এই ক্ষমতার উপর দাঁড়িয়ে। SWE-bench-এ এটা মানুষ করে দিয়েছিল বলে আমরা এতদিন সমস্যাটা দেখিনি।

---

## ৪. Goal ও Research Questions

**Goal:** প্রথম autonomous, LLM-ভিত্তিক agent বানানো যেটা যেকোনো project set up করে তার test suite চালায়, আর দেখানো যে এটা বিদ্যমান পদ্ধতির চেয়ে কার্যকর ও সাশ্রয়ী।

**Contribution (paper-এর দাবি):**
1. যেকোনো project set up করে test চালানোর প্রথম autonomous LLM agent।
2. **Meta-prompting** — নতুন ধারণা, যেখানে agent LLM-এর কাছ থেকে সর্বশেষ guideline চেয়ে নেয়।
3. Agent কীভাবে system-এর সাথে interact করবে, output monitor করবে, error সামলাবে — এ নিয়ে কয়েকটা technical design insight।
4. Empirical প্রমাণ যে এটা বিভিন্ন ধরনের project-এ কাজ করে এবং বিদ্যমান technique-এর চেয়ে স্পষ্টভাবে ভালো।

**Research Questions:**
- **RQ1 (effectiveness):** ExecutionAgent কতটা কার্যকরভাবে project সঠিকভাবে set up করে test চালাতে পারে?
- **RQ2 (costs):** Execution time ও LLM token ব্যবহারে খরচ কত?
- **RQ3 (ablation study):** বিভিন্ন component ও configuration-এর প্রভাব কতটা?
- **RQ4 (trajectories):** Agent tool-গুলোর সাথে কীভাবে interact করে, লক্ষ্যে পৌঁছাতে কোন পথ নেয়?

**সহজ কথায়:** Paper চারটা প্রশ্নের উত্তর খোঁজে: কতটা কাজ করে (RQ1), কত খরচ (RQ2), কোন অংশ কতটা জরুরি (RQ3), আর agent আসলে কী কী করে (RQ4)।

---

## ৫. Methodology — কীভাবে কাজটা করা হয়েছে

### ৫.১ সামগ্রিক কাঠামো: দুই Phase (Figure 1)
| Phase | কী করে | Output |
|---|---|---|
| **Phase 1: Preparation** | Meta-prompting দিয়ে guideline, CI script-এর summary, web search-এর hint জোগাড় | "Prompt ingredients" |
| **Phase 2: Feedback loop** | LLM পরের command ঠিক করে → tool চালায় → output summary → prompt update → আবার | Dockerfile + install/test script + test result file |

পুরো প্রক্রিয়া পরিচালনা করে একটা component — **control center**।

**সহজ কথায়:** Agent প্রথমে একটু পড়াশোনা করে (Phase 1), তারপর হাতে-কলমে চেষ্টা করে (Phase 2)। যেন পরীক্ষার আগে নোট পড়া, তারপর mock test দেওয়া।

### ৫.২ Algorithm 1 — ধাপে ধাপে
Input: repository URL $u$। Output: environment set up ও test চালানোর script।

**Phase 1 (line 1–6):**
1. `lang_guidelines` ← LLM("Give language-specific guidelines", get_languages($u$))
2. `container_guidelines` ← LLM("Give guidelines on recent containerization technology")
3. `ci_paths` ← LLM("Give common locations of CI scripts within a repo")
4. `ci_hints` ← read_ci_scripts_and_summarize($u$, ci_paths)
5. `install_hints` ← search_web($u$)

**Phase 2 (line 8–31):**
1. `attempts_left` ← 3; `p_attempt_lessons` ← খালি।
2. **Outer loop** (প্রতিটা attempt): command prompt বানাও (guideline + hint + আগের attempt-এর lesson); `budget_left` ← 40।
3. **Inner loop** (প্রতিটা command):
   - Step 1: (thought, cmd) ← LLM(p_cmd)
   - Step 2: cmd_result ← execute(cmd); যদি cmd = `task_done` এবং result valid → target file পড়ে script return।
   - Step 3: output-এর summary বানাও, prompt-এ (thought, cmd, summary) যোগ করো; budget এক কমাও।
4. Inner loop শেষ হলে attempt এক কমাও; LLM-কে দিয়ে আগের command ও thought-এর তালিকা বিশ্লেষণ করিয়ে lesson বানাও (line 30: analyze_commands_and_thoughts)।

**সহজ কথায়:** Algorithm-এর ভেতরে দুটো loop: বাইরের loop মানে নতুন চেষ্টা (সর্বোচ্চ 3), ভেতরের loop মানে চেষ্টার ভেতরে একটা একটা command (সর্বোচ্চ 40)। ব্যর্থ চেষ্টার পর agent "কী ভুল হলো" লিখে রাখে, পরের চেষ্টায় সেটা কাজে লাগে।

### ৫.৩ Phase 1-এর বিস্তারিত

**৫.৩.১ Language-specific guideline:**
- Project-এর প্রধান language heuristic-ভাবে বের করা হয় GitHub-এর **Linguist** library দিয়ে।
- Meta-prompt (Figure 2, Java-র উদাহরণ): "I want to install and run tests of a Java project. Give a list of 10 guidelines ..." — latest practice ও technology বিবেচনা করে।
- **কেন ঠিক 10টা:** সংখ্যা না দিলে LLM কখনো কয়েকটা ভাসা-ভাসা guideline দেয়, কখনো অনেক লম্বা তালিকা যা process করা কঠিন; authors-এর অভিজ্ঞতায় 10টা যথেষ্ট বিস্তারিত।
- Figure 2-এর উত্তরের উদাহরণ: README পড়ো; pom.xml বা build.gradle থেকে Java version মিলাও; dependency management tool দেখো; ... ; Maven-এ `mvn surefire-report:report` দিয়ে test report বানাও, Gradle সাধারণত `build/reports/tests/test/index.html`-এ HTML report বানায়।

**৫.৩.২ Language-independent guideline:** LLM দিয়েই বানানো একটা সাধারণ তালিকা — যাতে কোনো project তার প্রধান language-এর সাধারণ নিয়ম না মানলেও (যেমন দ্বিতীয় language-এর প্রভাব বেশি হলে) agent কাজ চালাতে পারে।

**৫.৩.৩ Container guideline:** Meta-prompt দিয়ে সর্বশেষ ও সবচেয়ে প্রচলিত containerization technology জিজ্ঞেস করা হয়। লেখার সময় GPT-4o উত্তর দিয়েছিল Docker সবচেয়ে ভালো option।

**৫.৩.৪ বিদ্যমান CI/CD script:** তিন ধাপ —
1. Meta-prompt দিয়ে CI script-এর সাধারণ folder, file name, extension-এর তালিকা।
2. সেই তালিকা দিয়ে repository-তে মিলে যাওয়া file খোঁজা।
3. LLM দিয়ে কোন file build ও test-এর জন্য প্রাসঙ্গিক তা ঠিক করা এবং প্রতিটার জন্য চারটা জিনিস চাওয়া: (১) সংক্ষিপ্ত natural language summary, (২) dependency-র তালিকা, (৩) setup ও test-এর গুরুত্বপূর্ণ command, (৪) প্রাসঙ্গিক file বা link।
- Figure 3-এর উদাহরণ (bootstrap-এর `karma.conf.js`): summary বলছে Jasmine দিয়ে unit test, Rollup দিয়ে preprocessing, headless Chrome ও Firefox; dependency তালিকায় jasmine, karma, karma-jasmine ইত্যাদি; important command `npm test`।

**৫.৩.৫ Web search:**
- Query: "How to install the <LANGUAGE> project '<PROJECT>' from source code?"
- উপরের **5টা** result-এর text বের করে একসাথে LLM-কে summarize করতে দেওয়া হয় (একটা একটা page পড়লে query ও খরচ বাড়তো)।
- কোনো page-এ setup-এর তথ্য না থাকলে LLM-কে বলা হয় নির্দিষ্ট বাক্য ফেরত দিতে: "This page does not contain setup-related information."
- কারণ: অনেক project-এর বেশি পরিষ্কার documentation readthedocs-এর মতো বাইরের site-এ থাকে।

**সহজ কথায়:** Phase 1-এর শেষে agent-এর হাতে চারটা জিনিস: ভাষার নিয়ম, container-এর নিয়ম, CI-এর সারাংশ আর web-এর সারাংশ। এগুলো দিয়েই সে পরের ধাপে prompt সাজায়।

### ৫.৪ Phase 2-এর বিস্তারিত

**৫.৪.১ Command prompt-এর 7টা section:**
| # | Section | ধরন | বিষয়বস্তু |
|---|---|---|---|
| 1 | Agent role | Static | মূল কাজ: project build করে test ঠিকমতো চালানো, ও সফলতার শর্ত |
| 2 | Goals | Static | install তথ্য জোগাড়; build ও test script লেখা; script চালিয়ে দরকার হলে ঠিক করা; test result বিশ্লেষণ করে pass/fail/skip সংখ্যা দেওয়া |
| 3 | Tools | Static | চারটা tool-এর বর্ণনা |
| 4 | Guidelines | Dynamic | Language-specific ও container guideline |
| 5 | Installation hints | Dynamic | CI script ও web search-এর hint, আর আগের attempt-এর lesson |
| 6 | Tool invocation history | Dynamic | এ পর্যন্ত চালানো command ও তাদের output summary (শুরুতে খালি) |
| 7 | পরের command-এর instruction | Static | Response format: TypeScript interface (Figure 4) |

**সহজ কথায়:** Agent-এর prompt একটা লম্বা চিঠির মতো। শুরুতে স্থির অংশ (তার কাজ ও tool), মাঝে পরিবর্তনশীল অংশ (নিয়ম, hint, এ পর্যন্ত কী করেছে), শেষে "পরের command কী?" প্রশ্ন।

**Response format (Figure 4):** JSON — `thoughts` (string) আর `tool` (name ও args)। উদাহরণ: thoughts = "I need to check the files and folders available within this repository.", tool = `linux_terminal` with `cmd: ls`। Thought চাওয়ার দুটো কারণ: (১) empirically response-এর মান বাড়ে (chain-of-thought), (২) debugging ও decision বোঝা সহজ। Format ভুল হলে control center error message দিয়ে সঠিক format মনে করিয়ে দেয়।

**৫.৪.২ চারটা Tool:**
| Tool | Input | কাজ |
|---|---|---|
| `linux_terminal` | একটা command | যেকোনো Linux terminal command চালিয়ে output ফেরত |
| `read_file` | file path | file-এর content ফেরত |
| `write_file` | file path ও content | file লেখা — বিশেষ করে Dockerfile আর `install.sh`-এর মতো output script |
| `task_done` | কেন শেষ তার natural language ব্যাখ্যা | কাজ সফলভাবে শেষ হয়েছে বলে signal |

Terminal দিয়েই সব করা সম্ভব, তবু file tool দেওয়া হয়েছে একজন developer-এর text editor ব্যবহারের অনুকরণে।

**সহজ কথায়:** চারটা tool-ই যথেষ্ট, কারণ terminal দিয়েই প্রায় সবকিছু করা যায়। `write_file` শুধু Dockerfile বা script লেখা সহজ করে।

**৫.৪.৩ Summarization:** Tool output **200 token** (default)-এর বেশি হলে আরেকটা LLM call দিয়ে summary ও প্রাসঙ্গিক তথ্য বের করা হয় (Figure 3-এর format)। তারপর command ও summary tool invocation history-তে যোগ হয়।

**সহজ কথায়:** লম্বা output হলে সারাংশ বানাও, তারপর সেই সারাংশ আর command prompt-এর history-তে রাখো। এতে prompt ছোট থাকে।

**৫.৪.৪ Control Center-এর দায়িত্ব:**
1. LLM output parse করে format যাচাই।
2. Algorithm 1 অনুযায়ী পরের ধাপ চালানো।
3. **Process monitoring:** container-এর ভিতরে launch হওয়া process track করে কখন শেষ হলো তা স্পষ্টভাবে ধরা (কারণ কিছু command অনেকক্ষণ কোনো output দেয় না, শুধু stdout/stderr দেখা যথেষ্ট নয়); শেষ হলে পুরো stdout ও stderr ফেরত।
4. **Timeout (default 5 মিনিট):** সময় পার হলে পাওয়া output ও process status LLM-কে দেওয়া হয়, LLM তিনটার একটা বেছে নেয় — (১) আরও 5 মিনিট অপেক্ষা, (২) চলমান tool-কে input দেওয়া (যেমন installation confirm করতে "y"), (৩) command বন্ধ করা।
5. **Output cleaning:** terminal-এর color code ও progress bar-এর বিশেষ character মুছে ফেলা।

**সহজ কথায়:** Control center হলো agent-এর তত্ত্বাবধায়ক। সে agent-এর কথা ঠিকঠাক parse করে, command আটকে গেলে সিদ্ধান্ত নেয়, আর output পরিষ্কার করে।

**৫.৪.৫ `task_done`-এর পর validation:** Control center তিনটা file আছে কিনা দেখে — (১) container বানানোর file (যেমন Dockerfile), (২) container-এর ভিতরে চালানোর installation script, (৩) test result-এর file (pass, fail, skip সংখ্যা)। সব থাকলে script user-কে ফেরত; না থাকলে ঠিক কী বাদ পড়েছে তা জানিয়ে agent-কে নতুন command দিতে বলা হয়।

**সহজ কথায়:** "কাজ শেষ" বললেই agent ছাড়া পায় না। তিনটা file আছে কিনা দেখা হয়। কিন্তু file-এর ভেতরের তথ্য সত্য কিনা — সেটা দেখা হয় না (এটাই paper-এর বড় দুর্বলতা)।

**৫.৪.৬ Output-এর উদাহরণ (Figure 5, OpenVPN):**
- Dockerfile: `FROM ubuntu:20.04`, timezone ঠিক করা (interactive prompt এড়াতে), `apt-get install` দিয়ে build-essential, liblzo2-dev, libpam0g-dev, liblz4-dev, libcap-ng-dev, libnl-genl-3-dev, linux-libc-dev, autoconf, automake, libtool, cmocka-dev, python3-docutils, git; তারপর OpenVPN clone।
- `install_and_run.sh`: `autoreconf -fvi` → `./configure --enable-werror` → `make -j$(nproc)` → `make check VERBOSE=1`।
- **আমার পর্যবেক্ষণ:** Dockerfile-এর দুই জায়গায় `|| exit 0` আছে — অর্থাৎ install বা clone fail করলেও image build "সফল" দেখাবে। Reproducibility-র জন্য এটা ঝুঁকিপূর্ণ (Section ১২.২)।

**সহজ কথায়:** OpenVPN-এর জন্য agent একটা Dockerfile (সব package install) আর একটা ছোট script (চারটা command: autoreconf, configure, make, make check) বানিয়েছে। মানুষ হাতে যা করত, ঠিক তাই।

### ৫.৫ Implementation ও Model
- Python ও bash-এ লেখা; ExecutionAgent নিজেও একটা Docker container-এ চলে।
- LLM: **OpenAI GPT-4o-mini**, Python API দিয়ে।
- অন্য model ব্যবহার করা যায় যদি interface-এ নির্দিষ্ট JSON output format সমর্থন করে; লেখার সময় Claude, DeepSeek, Llama এটা সমর্থন করতো। **কিন্তু paper-এ অন্য কোনো model দিয়ে experiment নেই।**

### ৫.৬ Default Configuration — এক নজরে
| Parameter | মান |
|---|---|
| Model | GPT-4o-mini |
| প্রতি attempt-এ command budget | 40 |
| সর্বোচ্চ attempt | 3 |
| Summarization threshold | 200 token |
| Command timeout | 5 মিনিট (LLM চাইলে আরও 5 মিনিট করে বাড়াতে পারে) |
| Meta-prompt guideline সংখ্যা | 10 |
| Web search result | উপরের 5টা |
| Language detection | GitHub Linguist |

---

## ৬. Mathematical Formulation — সূত্র ও ব্যাখ্যা

Paper-এ শুধু deviation-এর সূত্র explicit আছে। বাকিটা আমি paper-এর Algorithm 1 ও metric-এর বর্ণনা থেকে formal করেছি (**আমার formalization**), যাতে supervisor-কে পরিষ্কারভাবে দেখানো যায়।

### ৬.১ Problem-এর Formal Definition
Project $u$ (repository URL)। লক্ষ্য একটা জোড়া script খুঁজে বের করা:
$$
(D, S) \quad \text{যেখানে } D = \text{Dockerfile}, \; S = \text{install ও test script}
$$
এমনভাবে যে $D$ থেকে বানানো container-এ $S$ চালালে test result পাওয়া যায়:
$$
\text{Run}(D, S) = (n_{pass}, n_{fail}, n_{skip})
$$

**সহজ কথায়:** প্রথম সূত্রটা বলছে আমাদের লক্ষ্য: এমন একজোড়া file $(D, S)$ খোঁজা, যা চালালে তিনটা সংখ্যা (pass, fail, skip) পাওয়া যায়। এখানে $D$ হলো Dockerfile, $S$ হলো script, আর $n$ দিয়ে test গোনা হয়েছে।

### ৬.২ Preparation Phase — Prompt Ingredients
$$
I(u) = \left( G_{lang}(u),\; G_{cont},\; H_{ci}(u),\; H_{web}(u) \right)
$$

**কী হিসাব করে:** চারটা hint-কে এক পুঁটলিতে বেঁধে $I(u)$ নাম দেওয়া হয়েছে। এটাই agent-এর "পড়াশোনার নোট"। নিচে প্রতিটা অংশ কী:

- $G_{lang}(u) = \text{LLM}(\text{meta-prompt}, \text{Linguist}(u))$ — 10টা language guideline
- $G_{cont}$ — container guideline
- $H_{ci}(u)$ — CI script-এর summary
- $H_{web}(u)$ — উপরের 5টা web result-এর summary

### ৬.৩ Feedback Loop — Agent-এর অবস্থা পরিবর্তন
Attempt $a \in \{1, 2, 3\}$, attempt-এর ভিতরে ধাপ $t \in \{1, \ldots, B\}$, $B = 40$। Prompt $P_{a,t}$:
$$
P_{a,1} = \text{Compose}\left( I(u),\; L_{a-1} \right), \qquad L_0 = \text{খালি}
$$
প্রতিটা ধাপে:
$$
(\theta_t, c_t) = \text{LLM}(P_{a,t}), \qquad o_t = \text{Exec}(c_t)
$$
$$
s_t = \begin{cases} \text{LLM}_{sum}(P_{a,t}, o_t), & \text{যদি } \text{tok}(o_t) > 200 \\ o_t, & \text{অন্যথায়} \end{cases}
$$
$$
P_{a,t+1} = \text{Update}\left( P_{a,t},\; \theta_t,\; c_t,\; s_t \right)
$$
Attempt শেষ হলে lesson:
$$
L_a = \text{LLM}\left( \text{analyze}(c_{1..B},\; \theta_{1..B}) \right)
$$

**কী হিসাব করে:** প্রথম চার লাইন বলছে: প্রতি ধাপে LLM একটা thought আর একটা command দেয়। Command চলে, output আসে। Output বেশি লম্বা হলে সংক্ষেপ হয়। তারপর prompt-এ নতুন তথ্য যোগ হয়। চেষ্টা শেষ হলে সব ধাপ বিশ্লেষণ করে একটা lesson লেখা হয়। নিচে symbol-গুলোর মানে:

| Symbol | মানে |
|---|---|
| $\theta_t$ | LLM-এর thought (reasoning) |
| $c_t$ | পরের command (tool + argument) |
| $o_t$ | tool-এর কাঁচা output (color code মুছে) |
| $s_t$ | output-এর summary |
| $L_a$ | attempt $a$ থেকে শেখা lesson |

**নোট (paper-এর ব্যাখ্যা থেকে):** 200 token-এর বেশি হলে summarize করার কথা Section 2.4.3-এ আছে, যদিও Algorithm 1-এ শর্ত ছাড়া summarize দেখানো হয়েছে।

**সহজ কথায়:** প্রতিটা ধাপে agent নতুন তথ্য নিয়ে prompt বড় করে, আর প্রতি চেষ্টা শেষে নিজের ভুল থেকে একটা পাঠ লিখে রাখে। ব্যর্থ চেষ্টার পাঠ পরের চেষ্টায় কাজে লাগে।

### ৬.৪ থামার শর্ত (Termination)
$$
\text{Stop}(t) = \mathbb{1}\left[ c_t = \text{task-done} \;\land\; \text{valid} \right], \qquad \text{valid} = \mathbb{1}[D \text{ আছে}] \cdot \mathbb{1}[S \text{ আছে}] \cdot \mathbb{1}[R \text{ আছে}]
$$
যেখানে $R$ = test result file। **গুরুত্বপূর্ণ:** valid শুধু file-এর **অস্তিত্ব** যাচাই করে, file-এর **বিষয়বস্তু সঠিক কিনা** নয়।

**সহজ কথায়:** Agent থামে তখনই, যখন সে "কাজ শেষ" বলে আর তিনটা file-ই আছে। ($\mathbb{1}[\cdot]$ মানে শর্ত সত্য হলে 1, মিথ্যা হলে 0।) লক্ষ করো, এখানে file-এর ভেতরের তথ্য সঠিক কিনা তার কোনো শর্ত নেই।

**সর্বোচ্চ command সংখ্যা (আমার হিসাব):**
$$
T_{max} = A \times B = 3 \times 40 = 120 \text{ command}
$$
প্রতিটা command-এ সর্বোচ্চ 2টা LLM call (command নির্বাচন + summary), আর প্রতি attempt-শেষে 1টা lesson call — অর্থাৎ feedback phase-এ মোটামুটি সর্বোচ্চ $120 \times 2 + 3 = 243$টা LLM call (Phase 1-এর call ছাড়া)। এটা upper bound; paper আসল call সংখ্যা report করেনি।

**সহজ কথায়:** সর্বোচ্চ 3 চেষ্টা × 40 command = 120 command। প্রতি command-এ সর্বোচ্চ 2টা LLM call, আর প্রতি চেষ্টার শেষে 1টা। তাই মোট সর্বোচ্চ প্রায় 243 call। এটা শুধু উপরের সীমা, আসল সংখ্যা paper বলেনি।

### ৬.৫ Effectiveness Metric
$N = 50$ project। প্রতিটা project $i$-এর জন্য তিনটা binary ফল — built $b_i$, tests executed $e_i$, deviation 10%-এর কম $g_i$:
$$
SR_{build} = \frac{1}{N}\sum_{i=1}^{N} b_i, \qquad SR_{test} = \frac{1}{N}\sum_{i=1}^{N} e_i, \qquad SR_{close} = \frac{1}{N}\sum_{i=1}^{N} g_i
$$
যেখানে $g_i \leq e_i \leq b_i$। Paper এই rate-গুলো **হাতে script ও test result দেখে** নির্ধারণ করেছে।

**সহজ কথায়:** এই তিনটা সূত্র সোজা শতাংশ: 50টা project-এর মধ্যে কতটায় build হলো, কতটায় test চলল, আর কতটায় ফল CI-এর কাছাকাছি। প্রতিটা project-এর জন্য 1 (হ্যাঁ) বা 0 (না) ধরে গড় করা হয়েছে।

**Worked example (ExecutionAgent, Table 2):**
- $SR_{build} = 41/50 = 82\%$
- $SR_{test} = 33/50 = 66\%$
- $SR_{close} = 29/50 = 58\%$
- Build হওয়াদের মধ্যে test চলেছে (আমার হিসাব): $33/41 \approx 80.5\%$

**সহজ কথায়:** ExecutionAgent-এর 41টা build-এর মধ্যে 33টায় test চলেছে (প্রায় ৮০%)। মানে build হলে বেশিরভাগ ক্ষেত্রে test-ও চলে।

**তুলনা — LLM scripts baseline:** build 29/50 = 58%, কিন্তু test মাত্র 5/50 = 10%; build হওয়াদের মধ্যে $5/29 \approx 17.2\%$। অর্থাৎ শুধু build করতে পারা আর test চালাতে পারা — দুটো একদম আলাদা ক্ষমতা।

### ৬.৬ Improvement Factor (6.6x)
$$
\text{Factor} = \frac{SR_{test}(\text{ExecutionAgent})}{\max_{m \in \text{baselines}} SR_{test}(m)} = \frac{33}{5} = 6.6
$$
Baseline-গুলোর মধ্যে সর্বোচ্চ test execution LLM scripts-এর 5/50 (AutoGPT 4/50, Flapy 0/10)।

**সহজ কথায়:** Factor 6.6 মানে: সেরা পুরনো পদ্ধতি যতগুলো project-এর test চালাতে পারে (5টা), ExecutionAgent তার 6.6 গুণ (33টা) পারে।

### ৬.৭ Ground Truth থেকে Deviation (paper-এর সূত্র)
প্রতিটা bucket $b \in \{pass, fail, skip\}$-এর জন্য:
$$
\text{dev}_b = \left| \frac{n_b^{EA} - n_b^{GT}}{n_b^{GT}} \right| \times 100
$$
আর project-এর overall deviation তিনটার গড়:
$$
\text{dev} = \frac{1}{3}\left( \text{dev}_{pass} + \text{dev}_{fail} + \text{dev}_{skip} \right)
$$

**কী হিসাব করে:** Deviation মাপে agent-এর পাওয়া সংখ্যা আসল (CI-এর) সংখ্যা থেকে কত শতাংশ দূরে। তিনটা bucket (pass, fail, skip) আলাদা করে মেপে গড় করা হয়। 0% মানে হুবহু মিল। নিচে symbol-গুলোর মানে:

| Symbol | মানে |
|---|---|
| $n_b^{EA}$ | ExecutionAgent-এর চালানোয় bucket $b$-এর test সংখ্যা |
| $n_b^{GT}$ | CI log (ground truth)-এ bucket $b$-এর test সংখ্যা |

**Paper-এর নিজের উদাহরণ:** ground truth-এ 100টা pass, ExecutionAgent-এ 95টা → $\text{dev}_{pass} = |95 - 100|/100 \times 100 = 5\%$।

**Worked example ১ — pytest (Table 1-এর আসল সংখ্যা, আমার হিসাব):**
- Pass: GT 3,640, EA 3,775 → $|3775 - 3640|/3640 \times 100 \approx 3.71\%$
- Fail: GT 11, EA 11 → $0\%$
- Skip: GT 111, EA 119 → $|119 - 111|/111 \times 100 \approx 7.21\%$
- Overall: $(3.71 + 0 + 7.21)/3 \approx 3.64\%$ → "deviation < 10%"-এর মধ্যে।

**Worked example ২ — django (ছোট denominator-এর সমস্যা, আমার হিসাব):**
- Pass: GT 16,151, EA 16,148 → $\approx 0.019\%$
- Fail: GT 5, EA 6 → $|6 - 5|/5 \times 100 = 20\%$
- Skip: GT 1,448, EA 1,451 → $\approx 0.21\%$
- Overall: $(0.019 + 20 + 0.21)/3 \approx 6.74\%$

**শিক্ষা:** 17,604টা test-এর মধ্যে মাত্র 1টা বাড়তি fail-ই overall deviation-কে 6.74%-এ তুলেছে। অর্থাৎ এই metric **ছোট bucket-এ অত্যন্ত sensitive**।

**Zero-denominator সমস্যা (আমার পর্যবেক্ষণ):** axios-এ GT fail = 0, কিন্তু EA fail = 8। তখন $\text{dev}_{fail} = 8/0$ — অসংজ্ঞায়িত। Paper বলেনি এই ক্ষেত্রে কী করা হয়েছে। Table 1-এর 33টা tested project-এর মধ্যে অনেকগুলোতে GT-র fail বা skip = 0।

**সহজ কথায়:** Pytest-এ তিনটা bucket-এর deviation ছোট (3.71, 0, 7.21), তাই গড় প্রায় 3.64%। অর্থাৎ "close" (10%-এর কম)। অন্যদিকে Django-তে 1টা বাড়তি fail থেকেই 20% — metric ছোট bucket-এ কতটা স্পর্শকাতর তা এই দুই উদাহরণে দেখা যায়।

### ৬.৮ সামগ্রিক Average Deviation (7.5%)
33টা tested project-এর মধ্যে 17টা হুবহু মেলে (deviation 0), বাকি 16টার গড় 15.4%:
$$
\bar{\text{dev}} = \frac{17 \times 0 + 16 \times 15.4}{33} = \frac{246.4}{33} \approx 7.47\% \approx 7.5\%
$$
অর্থাৎ abstract-এর "7.5%" হলো **শুধু tested 33টা project-এর** গড়, সব 50টার নয়।

**আমার যাচাই (Table 1 থেকে recompute):** paper-এর সূত্র হুবহু প্রয়োগ করে Table 1-এর সংখ্যা থেকে আমি 7.5% বা "29/50 deviation < 10%" reproduce করতে পারিনি। শূন্য-denominator bucket বাদ দিলে 33টার মধ্যে 25টা 10%-এর নিচে আর গড় প্রায় 20.6%। শুধু **pass সংখ্যা** দিয়ে deviation হিসাব করলে 29টা 10%-এর নিচে পড়ে (Table 2-এর 29-এর সাথে মেলে), গড় প্রায় 6.84%। তাই paper আসলে কোন হিসাব ব্যবহার করেছে তা অস্পষ্ট — এটা supervisor-এর কাছে খোলাখুলি বলা উচিত।

**সহজ কথায়:** 33টা সফল project-এর অর্ধেকের একটু বেশি (17টা) হুবহু মিলেছে, বাকিদের গড় 15.4% দূরে। দুটো মিলিয়ে সামগ্রিক গড় 7.5%। কিন্তু এই সংখ্যা শুধু সফল 33টার, সব 50টার নয়।

### ৬.৯ Conditional Success Rate (subgroup analysis)
$$
SR_{test}(G) = \frac{|\{ i \in G : e_i = 1 \}|}{|G|}
$$
| Group $G$ | হিসাব | মান |
|---|---|---|
| Automated build tool আছে | 28/38 | ≈ 73.7% |
| Build tool নেই | 5/12 | ≈ 41.7% |
| Submodule আছে | 2/9 | ≈ 22.2% |
| Submodule নেই (আমার হিসাব) | (33 − 2)/(50 − 9) = 31/41 | ≈ 75.6% |
| Python-main (ExecutionAgent) | 6/10 | 60% |
| Python-main (Flapy) | 0/10 | 0% |

**সহজ কথায়:** বিভিন্ন group-এ সফলতার হার আলাদা করে দেখা: build tool থাকলে প্রায় ৭৪%, না থাকলে ৪২%; submodule থাকলে মাত্র ২২%। অর্থাৎ project-এর ধরন সফলতাকে বড়ভাবে বদলায়।

### ৬.১০ Cost ও Time Model
প্রতিটা LLM call $k$-এর input token $x_k$, output token $y_k$, দাম $\pi_{in}, \pi_{out}$ (USD প্রতি token):
$$
C(u) = \sum_{k} \left( x_k \, \pi_{in} + y_k \, \pi_{out} \right)
$$
Paper token সংখ্যা বা দামের হিসাব table আকারে দেয়নি, শুধু গড় খরচ (Figure 9)।

**সহজ কথায়:** প্রতিটা LLM call-এর খরচ = input token × input-এর দাম + output token × output-এর দাম। এগুলো যোগ করলে একটা project-এর মোট খরচ।

**সফল ও ব্যর্থ project-এর মিশ্রণ:** সফলতার অনুপাত $q$ হলে প্রত্যাশিত খরচ:
$$
\mathbb{E}[C] = q \cdot \bar{C}_{succ} + (1 - q) \cdot \bar{C}_{fail}
$$
**Worked example (আমার হিসাব):** $q = 33/50 = 0.66$, $\bar{C}_{succ} = 0.10$, $\bar{C}_{fail} = 0.34$ ধরলে $\mathbb{E}[C] = 0.66 \times 0.10 + 0.34 \times 0.34 = 0.066 + 0.1156 \approx 0.18$ USD — paper-এর 0.16 USD-এর চেয়ে একটু বেশি। কারণ সম্ভবত Figure 9-এর তিনটা group (Build Failure, Build Only, Tests Executed) আর text-এর "succeed/fail" group-এর সংজ্ঞা হুবহু এক নয়; paper এটা স্পষ্ট করেনি।

**সহজ কথায়:** কিছু project সস্তায় সফল, কিছু ব্যর্থ হয়ে বেশি খরচ করে। সফলতার অনুপাত দিয়ে ওজন করে গড় খরচ বের করা হয়েছে।

**প্রতি সফল project-এর খরচ (আমার হিসাব):**
$$
C_{per\,success} = \frac{N \cdot \bar{C}}{\#\text{success}} = \frac{50 \times 0.16}{33} \approx 0.24 \text{ USD}
$$
**সময় (আমার হিসাব):** মোট compute-সময় $50 \times 74 = 3{,}700$ মিনিট ≈ 61.7 ঘণ্টা; একসাথে 5টা চালালে wall-clock প্রায় $61.7 / 5 \approx 12.3$ ঘণ্টা। প্রতি সফল project-এ $3700/33 \approx 112$ মিনিট।

**সহজ কথায়:** মোট 50টা project-এ খরচ হয় 50 × 0.16 = 8 USD। কিন্তু সফল হয়েছে 33টা, তাই প্রতি সফল project-এ প্রায় 0.24 USD। ব্যর্থ project-এর খরচও সফলের ঘাড়ে চাপে।

### ৬.১১ Ablation-এর Relative Drop
$$
\Delta_{rel}(v) = \frac{S_{full} - S_{v}}{S_{full}} \times 100
$$
Paper-এর "50%" ও "21%" সংখ্যা **deviation < 10% column** (Table 3) দিয়ে মেলে (আমার যাচাই):
- No guidelines: $(29 - 15)/29 \approx 48.3\%$ → paper বলছে "50%"
- No CI/Web retrieval: $(29 - 23)/29 \approx 20.7\%$ → paper বলছে "21%"
- No CI/Web-এর খরচ বৃদ্ধি: $(0.18 - 0.16)/0.16 = 12.5\%$ → paper বলছে "13%"

"Executed tests" column দিয়ে হিসাব করলে no guidelines-এ $(33 - 15)/33 \approx 54.5\%$ আর no CI/Web-এ $(33 - 24)/33 \approx 27.3\%$ হতো।

**সহজ কথায়:** কোনো অংশ সরালে সফলতা কত শতাংশ কমল, সেটাই এই সূত্র। যেমন guideline সরালে 29 থেকে 15 — প্রায় অর্ধেক কমে গেল।

### ৬.১২ Script Size
Script-এর command সংখ্যা — comment, ফাঁকা লাইন আর `echo` বাদ; যৌগিক command ভেঙে আলাদা গোনা। যেমন `make . && make test` = 2টা command:
$$
\text{size}(S) = \sum_{r \in S} \left| \text{split}(r) \right| \cdot \mathbb{1}[r \text{ comment বা echo নয়}]
$$

**সহজ কথায়:** Script-এর আকার মাপা হয় ভেতরের আসল command গুনে। Comment, ফাঁকা লাইন আর `echo` বাদ। `a && b` মানে 2টা command।

### ৬.১৩ Tool Usage Distribution
$$
p(\text{tool}) = \frac{\#\text{call}_{tool}}{\sum_{\tau} \#\text{call}_{\tau}}
$$
Terminal 74.8% + write_file 16.0% + read_file 8.2% + task_done 1% = 100%।

**সহজ কথায়:** প্রতিটা tool মোট কতবার ডাকা হয়েছে, তার শতাংশ। Terminal সবচেয়ে বেশি (প্রায় ৭৫%)।

### ৬.১৪ (আমার পর্যবেক্ষণ) একাধিক Attempt-এর মান
যদি প্রতিটা attempt স্বাধীনভাবে $p$ সম্ভাবনায় সফল হতো, তাহলে 3টা attempt-এ অন্তত একবার সফল:
$$
P_{\geq 1} = 1 - (1 - p)^3
$$
যেমন $p = 0.4$ হলে $1 - 0.6^3 = 0.784$। তবে বাস্তবে attempt-গুলো স্বাধীন নয় (lesson পরের attempt-এ যায়, একই project-এর একই বাধা) — আর paper প্রতি attempt-এর সফলতা আলাদা করে report করেনি, তাই এটা শুধু intuition।

**সহজ কথায়:** ধরো একটা চেষ্টায় সফল হওয়ার সম্ভাবনা ৪০%। তিনবার চেষ্টা করলে অন্তত একবার সফল হওয়ার সম্ভাবনা প্রায় ৭৮%। কিন্তু বাস্তবে চেষ্টাগুলো স্বাধীন নয়, তাই এটা শুধু ধারণা।

---

## ৭. Experimental Setup

### ৭.১ Dataset (Section 3.1.3)
**Selection criteria:**
1. **Language diversity:** Python, Java, C, C++, JavaScript — প্রতিটা থেকে 10টা project, যেখানে ওই language প্রধান বা দ্বিতীয় সর্বাধিক ব্যবহৃত।
2. **Ground truth-এর প্রাপ্যতা:** CI/CD log-এ test result public থাকতে হবে — GitHub Actions, CircleCI, Jenkins, CirrusCI, আর মাঝে মাঝে project-এর website (যেমন TensorFlow)। README-তে CI badge থাকা একটা সূচক।
3. **Maturity ও activity:** কমপক্ষে 100 star, 100 commit, আর data collection-এর আগের ছয় মাসে অন্তত একটা commit।

**Construction:** প্রতিটা language-এর সবচেয়ে জনপ্রিয় project (star ও fork অনুযায়ী) ranking, উপর থেকে হাতে দেখে criteria মেলানো, 50টা না হওয়া পর্যন্ত।

**Statistics:**
| বিষয় | মান |
|---|---|
| Project | 50 |
| Code-এর language | 14টা |
| শুধু test code-এর language | 8টা (পাঁচ প্রধান + Kotlin, Scala, TypeScript) |
| Median commit | প্রায় 10K |
| Median star | প্রায় 45K |
| Median test case | প্রায় 1.4K |
| Main language-এ লেখা test-এর গড় অংশ | 87% |
| Automated build tool আছে | 38/50 (Make/CMake 14, npm/Yarn 13, Maven/Gradle 9) |
| CI-তে build ও test দুটোর script | 33/50 |
| শুধু build script | 10/50 |
| Build বা test কোনো script নেই | 7/50 |
| Submodule আছে | 9/50 |
| Linux-এ চলে (CI log দিয়ে নিশ্চিত) | 50/50 |

উদাহরণ: CPython-এর অনেক test Python-এ লেখা কিন্তু C-তে লেখা code test করে।

**সহজ কথায়:** Dataset-এ 50টা জনপ্রিয় project, 14টা ভাষা। বেশিরভাগে CI আছে (তাই আসল উত্তর পাওয়া যায়), আর 38টায় automated build tool আছে। আরও আছে: 9টায় submodule।

### ৭.২ Baselines (Section 3.1.4)
| Baseline | কী | Setup |
|---|---|---|
| **LLM scripts** | LLM-কে দিয়ে প্রতিটা প্রধান language-এর জন্য একটা general install-ও-test script লেখানো (Figure 6-এর prompt: Ubuntu-তে source থেকে install করে test চালাও, project, framework ও dependency-র পার্থক্য সামলাও, যতটা সম্ভব general কিন্তু জানা special case-ও সামলাও) | 5টা script; project-এর main language-এর script দিয়ে চালানো |
| **AutoGPT** | General-purpose LLM agent — plan করে, tool (web search, file read/write, Python execution) চালায়, plan update করে | একই model ও একই budget (সর্বোচ্চ iteration); task description Figure 7-এ (4টা goal) |
| **Flapy** | Python project set up করে test চালানোর মানুষের লেখা script, মূলত flaky test গবেষণার জন্য | শুধু 10টা Python-main project-এ |

**সহজ কথায়:** তিনটা পুরনো পদ্ধতির সাথে তুলনা: LLM-কে দিয়ে একটা সাধারণ script লেখানো, AutoGPT (সাধারণ-উদ্দেশ্যের agent), আর Flapy (Python-এর জন্য মানুষের লেখা)।

### ৭.৩ Metric ও Validation
- Successful build rate, successful testing rate — **হাতে** script ও test result দেখে।
- Script size (Section ৬.১২)।
- Ground truth-এর সাথে deviation (Section ৬.৭); "close" = deviation < 10%।
- খরচ: execution time ও LLM খরচ (USD)।

### ৭.৪ Hardware
256GB RAM-এর একটা Xeon(R) Silver 4214 machine, একসাথে 5টা project চলেছে।

---

## ৮. Results — মূল ফলাফল

### ৮.১ RQ1: Effectiveness — Table 2
| | ExecutionAgent | LLM scripts | AutoGPT | Flapy |
|---|---|---|---|---|
| Built | **41 / 50** | 29 / 50 | 9 / 50 | 6 / 10 |
| Executed tests | **33 / 50** | 5 / 50 | 4 / 50 | 0 / 10 |
| Ground truth deviation < 10% | **29 / 50** | 4 / 50 | 2 / 50 | 0 / 10 |

- 33টা tested project-এর মধ্যে **17টায় ফল ground truth-এর সাথে হুবহু এক**; বাকি 16টার গড় deviation 15.4%।
- Individual test case স্তরে: 17/33-এ একই test set একই ফলাফলে চলেছে; বাকি 16টায় **passing test-এর 99.9% ground truth-এর সাথে মিলেছে** — অমিল মূলত failing test-এ।
- Flapy-র 10টা Python project-এ ExecutionAgent 6টা build ও test করেছে, paper-এর দাবি অনুযায়ী সবগুলো ground truth-এর সাথে হুবহু এক।

**সহজ কথায়:** ExecutionAgent 41টা build করেছে, 33টায় test চালিয়েছে। 29টায় ফল CI-এর কাছাকাছি (10%-এর মধ্যে)। বাকি baseline-গুলো এর কাছেও আসেনি। সবচেয়ে বড় ফাঁক: LLM scripts build করেছে 29টা, কিন্তু test চালিয়েছে মাত্র 5টা।

### ৮.২ Table 1 — 50টা project-এর বিস্তারিত ফল
(GT = ground truth; EA = ExecutionAgent। "built only" = build হয়েছে কিন্তু test চলেনি; "build fail" = build হয়নি।)

| Project | Languages | GT Tests | GT Pass | GT Fail | GT Skip | EA Tests | EA Pass | EA Fail | EA Skip |
|---|---|---|---|---|---|---|---|---|---|
| Activiti | J | 3269 | 3266 | 0 | 3 | 2392 | 2389 | 1 | 2 |
| ansible | P | 1717 | 1703 | 0 | 14 | built only | | | |
| axios | JS, TS | 203 | 203 | 0 | 0 | 203 | 195 | 8 | 0 |
| bootstrap | JS, Html/css | 808 | 808 | 0 | 0 | 808 | 793 | 15 | 0 |
| ccache | C, SH | 47 | 36 | 0 | 11 | 47 | 36 | 0 | 11 |
| Chart.js | JS, TS | 3298 | 3298 | 0 | 0 | built only | | | |
| commons-csv | J | 856 | 845 | 0 | 11 | 856 | 845 | 0 | 11 |
| cpython | P, C, C++ | 478 | 462 | 0 | 16 | 478 | 433 | 4 | 42 |
| deno | JS, TS, Rust | 1458 | 1446 | 0 | 12 | 511 | 474 | 36 | 1 |
| distcc | C, P | 57 | 57 | 0 | 0 | 57 | 53 | 4 | 0 |
| django | P | 17604 | 16151 | 5 | 1448 | 17605 | 16148 | 6 | 1451 |
| dubbo | J | 14020 | 13678 | 0 | 342 | 14020 | 13678 | 0 | 342 |
| express | JS | 1228 | 1228 | 0 | 0 | 1228 | 1228 | 0 | 0 |
| flask | P | 484 | 481 | 0 | 3 | 484 | 480 | 1 | 3 |
| flink | J, Scala, P | 105242 | 100644 | 0 | 4598 | built only | | | |
| folly | C++, P | 3089 | 3088 | 0 | 0 | build fail | | | |
| FreeRTOS | C, ASM | 215 | 215 | 0 | 0 | build fail | | | |
| git | C, SH, Perl | 31715 | 31715 | 0 | 0 | 30264 | 29203 | 265 | 796 |
| guava | J | 857221 | 857221 | 0 | 0 | 857221 | 857221 | 0 | 0 |
| imgui | C++, C | 348 | 348 | 0 | 0 | build fail | | | |
| json | C++ | 93 | 93 | 0 | 0 | 93 | 93 | 0 | 0 |
| json-c | C | 25 | 25 | 0 | 0 | 25 | 25 | 0 | 0 |
| keras | P | 12110 | 11860 | 0 | 250 | 12775 | 12445 | 10 | 320 |
| langchain | P | 1358 | 887 | 0 | 471 | built only | | | |
| libevent | C | 68 | 68 | 0 | 0 | 68 | 68 | 0 | 0 |
| mermaid | JS, TS | 3106 | 3104 | 0 | 2 | 3287 | 3276 | 0 | 11 |
| mpv-player | C | 14 | 14 | 0 | 0 | build fail | | | |
| msgpack-c | C | 41 | 41 | 0 | 0 | build fail | | | |
| mybatis | J | 1870 | 1851 | 0 | 19 | 1870 | 1851 | 0 | 19 |
| nest | JS | 1655 | 1655 | 0 | 0 | 1655 | 1655 | 0 | 0 |
| node | JS, C++, P | 4218 | 4218 | 0 | 0 | build fail | | | |
| numpy | P, C, C++ | 44861 | 43197 | 0 | 1629 | build fail | | | |
| opencv | C++, C, P | 232 | 216 | 0 | 16 | 232 | 216 | 0 | 16 |
| openvpn | C | 96 | 95 | 0 | 1 | 91 | 85 | 2 | 4 |
| pandas | P, C | 199448 | 172973 | 1025 | 25486 | 183384 | 171565 | 2233 | 9586 |
| pytest | P | 3762 | 3640 | 11 | 111 | 3805 | 3775 | 11 | 119 |
| react | JS, TS, Rust | 5509 | 5509 | 0 | 0 | 9764 | 9738 | 1 | 25 |
| react-native | C++, J, JS | 158 | 158 | 0 | 0 | 158 | 158 | 0 | 0 |
| rocketmq | J | 2336 | 2324 | 0 | 12 | 2336 | 2324 | 0 | 12 |
| RxJava | J | 11863 | 9404 | 0 | 2459 | 11863 | 9395 | 9 | 2459 |
| scikit-learn | P, C, C++ | 37064 | 31900 | 125 | 5039 | 37729 | 32546 | 128 | 5055 |
| scipy | P, C, C++ | 52672 | 49745 | 0 | 2767 | built only | | | |
| spring | J, KT | 117 | 74 | 0 | 43 | 117 | 74 | 0 | 43 |
| tensorflow | C++, P | 3148 | 0 | 0 | 0 | built only | | | |
| TypeScript | JS | 96598 | 96598 | 0 | 0 | 96598 | 96598 | 0 | 0 |
| vue | TS, JS | 1449 | 1449 | 0 | 0 | 1449 | 1449 | 0 | 0 |
| webpack | JS | 28935 | 28815 | 0 | 120 | build fail | | | |
| webview | C++, C, P | 12 | 12 | 0 | 0 | build fail | | | |
| xgboost | C++, P, R | 208 | 207 | 0 | 1 | built only | | | |
| xrdp | C, C++ | 206 | 206 | 0 | 0 | built only | | | |

**সহজ কথায়:** প্রতিটা project-এর জন্য দেখানো হয়েছে CI-তে কত test pass, fail, skip ছিল, আর ExecutionAgent কত পেয়েছে। দুটো সংখ্যা মিললে ভালো। "built only" মানে build হয়েছে কিন্তু test চলেনি, "build fail" মানে build-ই হয়নি।

**আমার গণনা (Table 1 থেকে):**
- Tested = 33, built only = 8 (ansible, Chart.js, flink, langchain, scipy, tensorflow, xgboost, xrdp), build fail = 9 (folly, FreeRTOS, imgui, mpv-player, msgpack-c, node, numpy, webpack, webview) → 33 + 8 + 9 = 50 ✓; built = 33 + 8 = 41 ✓।
- **চারটা সংখ্যাই হুবহু মেলে এমন project আমি গুনে পেয়েছি 16টা** (ccache, commons-csv, dubbo, express, guava, json, json-c, libevent, mybatis, nest, opencv, react-native, rocketmq, spring, TypeScript, vue), paper বলছে 17টা। একটার পার্থক্য সম্ভবত paper-এর "identical" সংজ্ঞায় (যেমন test set মেলানো) — paper স্পষ্ট করেনি।
- **অসঙ্গতি:** paper বলছে Python-এর 6টা tested project-এর "সবগুলো" ground truth-এর সাথে identical; কিন্তু Table 1-এ Python-tagged tested project-গুলোর (django, flask, keras, pandas, pytest, cpython, scikit-learn) একটাও হুবহু মেলে না (যেমন flask: GT 481 pass ও 0 fail, EA 480 pass ও 1 fail)।
- **লক্ষণীয় outlier:** react-এ EA 9,764টা test চালিয়েছে, GT-তে 5,509 — অর্থাৎ CI-র চেয়ে **বেশি** test; mermaid-এও 3,287 বনাম 3,106। এর মানে CI হয়তো সব test চালায় না, অথবা agent ভিন্ন configuration-এ চালিয়েছে — "ground truth" নিজেই নিখুঁত নয়।
- tensorflow-এর GT-তে 3,148 test কিন্তু pass, fail, skip সবই 0 — ground truth extraction-এ সমস্যার ইঙ্গিত।

**সহজ কথায়:** Table 1 নিজেও পুরোপুরি নির্ভুল নয়। কিছু ক্ষেত্রে agent CI-এর চেয়ে বেশি test চালিয়েছে (react), আবার tensorflow-এর আসল উত্তরেই সব 0। তাই "আসল উত্তর"-ও নিখুঁত নয়।

### ৮.৩ Language অনুযায়ী (Figure 8)
- **Java-তে সবচেয়ে কার্যকর** — paper বলছে সব Java project build ও test হয়েছে।
- **C ও C++ সবচেয়ে কঠিন** — build ও test প্রক্রিয়া কম standardized, প্রায়ই system dependency-র সাথে মেলাতে package নতুন করে compile করতে হয়।
- Figure 8-এর প্রতিটা bar-এর সঠিক সংখ্যা text-এ নেই, আর PDF থেকে বের করা যায়নি; paper প্রতিটা project-এর "main language" তালিকাও দেয়নি। **নোট:** flink (J, Scala, P) Table 1-এ built only — তাই "সব Java project" দাবি মেলাতে হলে flink-কে Java-main ধরা হয়নি বলে ধরতে হয়।

**সহজ কথায়:** Java সবচেয়ে সহজ, C ও C++ সবচেয়ে কঠিন। কারণ C/C++-এ standard package manager নেই; system library হাতে মেলাতে হয়।

### ৮.৪ Build tool ও Submodule অনুযায়ী
- Automated build tool-যুক্ত 38টার মধ্যে 28টায় test চলেছে; build tool ছাড়া 12টার মধ্যে 5টায়।
- Submodule-যুক্ত 9টার মধ্যে মাত্র 2টায় test চলেছে।

**সহজ কথায়:** Build tool থাকলে সফলতা অনেক বেশি (28/38), না থাকলে কম (5/12)। Submodule থাকলে প্রায় সবসময় ব্যর্থ (2/9)।

### ৮.৫ Deviation-এর কারণ (5টা project-এর বিস্তারিত বিশ্লেষণ)
1. **Module-ভিত্তিক project:** Activiti-তে bpmn converter module compile fail করায় বাকি testing থেমে যায়; অন্য module চালিয়ে যাওয়ার একটা option ছিল কিন্তু agent সেটা ব্যবহার করেনি (তাই 3,269-এর জায়গায় 2,392)।
2. **অসম্পূর্ণ dependency:** axios-এ headless Chromium binary না থাকায় 8টা test চলেনি (Table 1-এ এগুলো fail হিসেবে দেখা যায়)।
3. **Test flakiness:** কিছু error-এর পিছনে missing dependency বা setup সমস্যার স্পষ্ট চিহ্ন ছিল না।

**সহজ কথায়:** ফল মিলছে না মূলত তিন কারণে: এক module আটকে গেলে বাকিটা থামা, একটা dependency (যেমন browser) না থাকা, আর flaky test।

### ৮.৬ Baseline-এর সাথে তুলনা
- **LLM scripts:** অনেক build করে (29/50) কিন্তু test চালাতে পারে মাত্র 5টায় (5/29)। কারণ: user setup আর development setup-এর পার্থক্য বোঝে না — compiler, glibc-32, testing framework install, dependency recompile, config বদল বাদ পড়ে। ExecutionAgent অপ্রত্যাশিত error iteratively ঠিক করতে পারে।
- **AutoGPT:** একই budget-এ মাত্র 9টা build, 4টায় test। ExecutionAgent-এর মূল পার্থক্য: meta-prompting, চালানো command-এর memory আরও কার্যকরভাবে manage করা, আর বেশি sophisticated ও robust tool।
- **Flapy:** LLM scripts-এর মতো build-এ ঠিকঠাক (6/10) কিন্তু 10টার একটারও test সম্পূর্ণ চালাতে পারেনি।

**সহজ কথায়:** সব baseline-এর মূল সমস্যা এক: তারা "user setup" ও "development setup"-এর পার্থক্য বোঝে না, আর ভুল হলে শোধরাতে পারে না। ExecutionAgent পারে, কারণ সে ধাপে ধাপে ভুল দেখে ঠিক করে।

### ৮.৭ RQ2: Costs (Section 3.3, Figure 9)
| বিষয় | মান |
|---|---|
| গড় সময় প্রতি project | **74 মিনিট** (5টা একসাথে চলা অবস্থায়) |
| গড় LLM খরচ প্রতি project | **USD 0.16** |
| Build বা test-এ ব্যর্থ project-এর গড় খরচ | USD 0.34 (budget শেষ না হওয়া পর্যন্ত চেষ্টা করে) |
| সফল project-এর গড় খরচ | USD 0.10 |

Authors-এর যুক্তি: বিকল্প হলো মানুষ দিয়ে হাতে setup, তাই এই সময় ও খরচ গ্রহণযোগ্য; LLM সস্তা হলে খরচ আরও কমবে।

**সহজ কথায়:** ব্যর্থ হলে agent budget শেষ পর্যন্ত চেষ্টা করে, তাই ব্যর্থ project-এর খরচ (0.34) সফলের (0.10) চেয়ে প্রায় 3.4 গুণ। খরচ সামান্যই, তাই paper বলছে মানুষের হাতে করার চেয়ে এটা সস্তা।

### ৮.৮ RQ3: Ablation Study — Table 3
| Variant | Built | Executed tests | Deviation < 10% | Project cost (USD) |
|---|---|---|---|---|
| **ExecutionAgent (full)** | **41** | **33** | **29** | 0.16 |
| No preparation phase | 12 | 8 | 7 | 0.19 |
| No feedback phase | 19 | 5 | 5 | 0.02 |
| No guidelines | 26 | 15 | 15 | 0.15 |
| No CI/Web retrieval | 31 | 24 | 23 | 0.18 |

- **No preparation phase:** meta-prompting ও retrieval ছাড়া সরাসরি feedback loop — 12 build, 8 test; আর খরচ **বেশি** (0.19)।
- **No feedback phase:** preparation-এর তথ্য দিয়ে একবারে একটা script — মাত্র 5টায় test; খুব সস্তা (0.02) কিন্তু অকার্যকর। এটা মূলত LLM scripts baseline-এর (5/50) সমান।
- **No guidelines:** effectiveness প্রায় 50% কমে।
- **No CI/Web retrieval:** success rate 21% কমে, খরচ 13% বাড়ে।
- **আমার পর্যবেক্ষণ:** কোনো component সরালেই খরচ খুব একটা কমে না (feedback phase ছাড়া) — বরং preparation বা retrieval সরালে খরচ বাড়ে, কারণ agent অন্ধকারে বেশি command চালায়। অর্থাৎ ভালো context একসাথে **কার্যকারিতা বাড়ায় আর খরচ কমায়**।

**সহজ কথায়:** Agent-এর একটা অংশ সরিয়ে আবার চালালে কতটা খারাপ হয়, সেটাই ablation। Preparation বা feedback — যেকোনোটা সরালে ফল অনেক নামে। তাই দুটোই জরুরি। মজার ব্যাপার: preparation সরালে খরচ বরং বাড়ে, কারণ agent অন্ধকারে হাতড়ায়।

### ৮.৯ RQ4: Tool ও Trajectory বিশ্লেষণ (Section 3.5)
**Tool usage:**
| Tool | অংশ |
|---|---|
| Terminal | 74.8% |
| write_file | 16.0% |
| read_file | 8.2% |
| task_done | 1% |

**Terminal command (Figure 10, top-10):**
- Directory ও file দেখার command (ls, cd, pwd) মিলে প্রায় 33%।
- Installation ও build command (apt install, pip, npm) প্রায় 21%।
- প্রায় 25% command top-10-এর বাইরে — অর্থাৎ command-এর বৈচিত্র্য অনেক, hard-coded command তালিকা কাজ করবে না।

**Trajectory-র তিনটা পর্যবেক্ষণ:**
1. **পুনরাবৃত্ত phase — setup, dependency, testing:** react-native, commons-csv, pytest-এর মতো library-তে স্পষ্ট তিনটা ধাপ: (১) `ls`, README.md / pom.xml / package.json পড়া; (২) Dockerfile বা setup script লেখা — যেমন `FROM node:20` বা `FROM python:3.10-slim`, তারপর apt-get ও npm/yarn; (৩) `npm test`, `pytest` চালিয়ে ফল নিশ্চিত করা, log রাখা, output script তৈরি।
2. **ধারাবাহিক Docker ব্যবহার:** project-এর নিজের Dockerfile থাকলে সেটা দিয়ে environment; `docker images`, `docker ps` দিয়ে environment যাচাই।
3. **Error handling:** script-এ fallback logic (`||` দিয়ে বিকল্প action); cleanup command যাতে error-এ বাড়তি file জমে না থাকে।

**Script complexity:** 33টা সফল project-এ গড় script size 18 (সর্বনিম্ন 12, সর্বোচ্চ 37)। Paper একই অনুচ্ছেদে আবার বলছে "গড়ে 16টা command" — **18 বনাম 16-এর অসঙ্গতি paper-এ ব্যাখ্যা করা নেই।** Script ছোট কারণ agent সফল command-ক্রম খুঁজে পাওয়ার পরেই script লেখে।

**সহজ কথায়:** Agent মূলত terminal দিয়ে কাজ করে (প্রায় ৭৫%)। সাধারণ পথ তিন ধাপ: ফোল্ডার আর README দেখা, Dockerfile আর script লেখা, তারপর test চালিয়ে ফল নিশ্চিত করা। Script-এ fallback (`||`) আর cleanup-ও থাকে।

**ব্যর্থতার দুটো আচরণ (Section 3.5.4):**
1. **একই ভুলের পুনরাবৃত্তি:** যেমন `sudo` না থাকলেও বারবার `sudo` ব্যবহার — error-এর পর ঠিক করে, কিন্তু পরের command-এ আবার একই ভুল।
2. **Follow-up না করা:** Node বা gcc-এর নতুন version install করে, কিন্তু পুরনোটাই default থেকে যায়; তারপর version check → install → default না করা — এই চক্রে resource নষ্ট।

**সহজ কথায়:** Agent দুটো ভুল বারবার করে: একই ভুল পুনরাবৃত্তি (sudo নেই, তবু sudo), আর নতুন version install করে সেটাকে default না বানানো। এতে budget নষ্ট হয়।

---

## ৯. Key Findings / Insights (Supervisor-কে বলার মতো ৮টা পয়েন্ট)

1. **যেকোনো project-এর test চালানো automate করা সম্ভব, কিন্তু নিখুঁত নয়** — 50-এর মধ্যে 33টা (66%), ground truth-এর কাছাকাছি 29টা (58%)।
2. **Build করা আর test চালানো আলাদা ক্ষমতা** — LLM scripts 29টা build করে কিন্তু test চালায় মাত্র 5টায়। Development setup-এর লুকানো ধাপগুলোই আসল বাধা।
3. **Feedback loop অপরিহার্য** — feedback ছাড়া মাত্র 5টা; iterative trial-and-error-ই মূল শক্তি।
4. **Context (guideline + hint) কার্যকারিতা বাড়ায় এবং খরচ কমায়** — preparation বা retrieval সরালে খরচ বেড়েছে।
5. **Specialized agent > general agent** — একই model ও budget-এ AutoGPT মাত্র 4টা।
6. **C/C++ আর submodule এখনো কঠিন** — submodule-যুক্ত project-এ 2/9।
7. **Test চলার পরেও ফলাফল সবসময় ঠিক নয়** — 16টা tested project-এ ground truth থেকে গড় 15.4% deviation; failing test-এ অমিল বেশি। অর্থাৎ "suite চলেছে" মানেই "সঠিক environment" নয়।
8. **সস্তা ও যথেষ্ট দ্রুত** — GPT-4o-mini দিয়ে গড় USD 0.16, 74 মিনিট; ব্যর্থ project সফলের চেয়ে 3.4 গুণ বেশি খরচ করে (0.34 বনাম 0.10, আমার হিসাব)।

**সহজ কথায়:** আটটা মূল শিক্ষা: (১) automate করা যায় কিন্তু নিখুঁত নয়, (২) build আর test আলাদা, (৩) feedback loop জরুরি, (৪) context খরচ কমায়, (৫) বিশেষ agent সাধারণ agent-এর চেয়ে ভালো, (৬) C/C++ কঠিন, (৭) test চলা মানে ঠিক ফল নয়, (৮) সস্তা।

---

## ১০. কেন এই Solution অন্যগুলোর থেকে ভালো?

| বৈশিষ্ট্য | Flapy / GitBug-Java pipeline | LLM scripts | AutoGPT | SWE-rebench-এর recipe pipeline (Sub-domain 3) | **ExecutionAgent** |
|---|---|---|---|---|---|
| Language | এক language | প্রতি language একটা general script | যেকোনো | শুধু Python | **যেকোনো (14 language-এ পরীক্ষিত)** |
| Interaction | নেই (fixed script) | নেই (একবার লেখা) | আছে, general | সীমিত (error log দেখে recipe আবার লেখা, LLM নিজে command চালায় না) | **পূর্ণ interactive — terminal, file, timeout handling** |
| আপ-টু-ডেট জ্ঞান | হাতে update | LLM-এর জ্ঞান | LLM-এর জ্ঞান | LLM-এর জ্ঞান | **Meta-prompting দিয়ে project-অনুযায়ী guideline** |
| বাইরের hint | নেই | নেই | Web search | Repository file | **CI script + web search** |
| Output | Script | Script | যা খুশি | JSON recipe + Docker image | **Dockerfile + install/test script + result file** |
| Ground truth যাচাই | — | — | — | F2P/P2P শর্ত | **CI log-এর সাথে pass/fail/skip তুলনা** |
| Test চালানোর সাফল্য (এই paper-এ) | Flapy 0/10 | 5/50 | 4/50 | এই dataset-এ চালানো হয়নি | **33/50** |

**সহজ কথায়:** অন্য সব পদ্ধতির তুলনায় ExecutionAgent একমাত্র যেটা একসাথে: যেকোনো ভাষায় কাজ করে, নিজে terminal-এ কথা বলে, hint নেয়, আর শেষে আসল উত্তরের সাথে মেলায়।

**মূল শক্তি:**
1. **Human developer-এর অনুকরণ:** docs পড়া, চেষ্টা, ভুল দেখে শোধরানো।
2. **Meta-prompting:** prompt রক্ষণাবেক্ষণের বোঝা LLM-এর উপর।
3. **Robust tool design:** process termination detection, timeout-এ wait/input/terminate বিকল্প, output cleaning, summarization।
4. **Reusable output:** একবার সফল হলে Dockerfile ও script বারবার ব্যবহার করা যায় — LLM ছাড়াই।
5. **Ground truth দিয়ে যাচাই:** শুধু "চলেছে" নয়, CI-এর সাথে ফল মেলানো হয়েছে।
6. **Open source:** code ও artifact public।

---

## ১১. কোন পরিস্থিতিতে ভালো কাজ করে, কোথায় করে না

### ✅ ভালো কাজ করে যখন:
- Project-এ **standard build tool** আছে (Maven/Gradle, npm/Yarn, Make/CMake) — 28/38।
- **Java** project — সবচেয়ে বেশি সফল।
- Project জনপ্রিয়, documentation ভালো, CI script আছে।
- Project-এর **সর্বশেষ version (HEAD)** চালাতে হবে, আধুনিক dependency দিয়ে।
- একটা single configuration-এ (এক OS, এক language version) test চালানো যথেষ্ট।

### ❌ ভালো কাজ করে না / সীমিত যখন:
- **C/C++** project, বিশেষ করে system library recompile লাগলে (folly, imgui, node, numpy build fail)।
- **Git submodule** আছে — 2/9।
- **Multi-module** project যেখানে এক module ব্যর্থ হলে বাকি থেমে যায় (Activiti)।
- **পুরনো dependency** দরকার — meta-prompt "latest practice" চায় (threat #2)।
- **Browser-নির্ভর test** (headless Chromium, axios)।
- একাধিক configuration (ভিন্ন browser, OS, version) — paper সাধারণত একটাই চালায়।
- কম পরিচিত বা দুর্বল documentation-এর project — পরীক্ষা হয়নি।
- **আমাদের ক্ষেত্রে বিশেষভাবে:** নির্দিষ্ট **পুরনো commit**-এ (যেমন SWE-bench task-এর base commit) test চালাতে হলে — paper-এর setup HEAD clone করে, historical commit-এ পরীক্ষা হয়নি।

**সহজ কথায়:** সংক্ষেপে: জনপ্রিয় ও স্ট্যান্ডার্ড build-এর project-এ ভালো; C/C++, submodule, পুরনো dependency ও একাধিক configuration-এ দুর্বল।

---

## ১২. Limitations — দুর্বলতা

### ১২.১ Authors যা নিজেরা স্বীকার করেছেন
1. **একই ভুলের পুনরাবৃত্তি** (`sudo` উদাহরণ) — command নষ্ট হয়।
2. **Follow-up-এর অভাব** (নতুন Node/gcc install করে default না করা)।
3. **Single configuration:** একটা language version, browser বা OS — অন্য environment-এর পার্থক্য ধরা পড়ে না (prompt বদলে ঠিক করা যায় বলে authors-এর মত)।
4. **আধুনিক technology-কেন্দ্রিক design:** পুরনো dependency-র project-এ কম কার্যকর হতে পারে (iterative approach আংশিক প্রশমন করে বলে authors-এর মত)।
5. **জনপ্রিয়, ভালো documentation-এর project-এ পরীক্ষা:** কম পরিচিত project-এ ফল ভিন্ন হতে পারে; dataset-এর অনেক project submodule ব্যবহার করে না।
6. **Selection bias:** ground truth পেতে CI log লাগে, তাই dataset CI-ব্যবহারকারী project-এর দিকে ঝুঁকে আছে; বিকল্প হলো হাতে setup করে ground truth বানানো।
7. Deviation-এর কারণ: module-ভিত্তিক build, অসম্পূর্ণ dependency, flakiness।
8. C ও C++-এ কম কার্যকর; submodule-এ দুর্বল।

**সহজ কথায়:** Authors নিজেরা আটটা দুর্বলতা মেনেছেন। সবচেয়ে বড় দুটো: একই ভুলের পুনরাবৃত্তি, আর শুধু একটা configuration-এ পরীক্ষা।

### ১২.২ আমার Critical Analysis (Professor-level observation)
1. **Validation শুধু file-এর অস্তিত্ব দেখে (সবচেয়ে গুরুত্বপূর্ণ, আমাদের domain-এর জন্য):** `task_done`-এর পর control center দেখে Dockerfile, script আর result file **আছে কিনা** — result-এর সংখ্যা কোথা থেকে এলো, test আসলে চলেছে কিনা, তা নয়। একটা LLM agent চাইলে result file-এ সংখ্যা লিখে দিতে পারে, failing test skip করাতে পারে, বা test command-এর পাশে `|| true` বসিয়ে দিতে পারে। Paper-এর evaluation-এ মানুষ হাতে দেখেছে বলে এটা ধরা পড়েছে, কিন্তু **scale-এ automated ব্যবহারে এটা verifier gaming-এর (CG12) সরাসরি পথ।**
2. **Figure 5-এর `|| exit 0`:** Dockerfile-এ install বা clone fail করলেও build সফল দেখায়। Trajectory analysis-এ paper এই fallback logic-কে "error handling and resilience" বলে প্রশংসা করেছে, কিন্তু assurance-এর দৃষ্টিতে এটা **নীরব ব্যর্থতা লুকানো** — environment অসম্পূর্ণ হলেও "সফল"।
3. **Metric-এর অস্পষ্টতা ও reproducibility:** (ক) শূন্য-denominator bucket কীভাবে সামলানো হয়েছে বলা নেই; (খ) Table 1 থেকে আমি 29/50 ও 7.5% সূত্র হুবহু মেনে reproduce করতে পারিনি — শুধু pass-count দিয়ে 29 মেলে; (গ) identical project 17 নাকি 16; (ঘ) Python-এর "সব identical" দাবি Table 1-এর সাথে মেলে না; (ঙ) script size 18 বনাম 16; (চ) cost-এর মিশ্র গড় 0.18 বনাম 0.16। আলাদাভাবে ছোট, কিন্তু একসাথে evaluation-এর নির্ভুলতা নিয়ে প্রশ্ন তোলে।
4. **"Close" threshold (10%) ও তিন bucket-এর সমান weight:** 1টা বাড়তি fail (django) আর হাজারটা হারানো pass (Activiti) একই metric-এ মেশে। Per-test স্তরে (test ID ধরে) তুলনা — যেমন Jaccard বা F2P/P2P-ধাঁচের — বেশি অর্থবহ।
5. **Single run, কোনো variance নেই:** প্রতিটা project একবার চালানো (অথবা paper repeat-এর কথা বলেনি)। LLM agent non-deterministic — একই project-এ আবার চালালে 33 কত হয়, জানা নেই। আমাদের CG4-এর সাথে সরাসরি যুক্ত।
6. **শুধু একটা model (GPT-4o-mini):** অন্য model "সম্ভব" বলা হয়েছে, পরীক্ষা হয়নি। কোন অংশ model-এর ক্ষমতা আর কোন অংশ scaffold-এর — আলাদা করা যায় না।
7. **Ground truth নিজেই দুর্বল:** CI log সব test নাও চালাতে পারে (react-এ EA বেশি test চালিয়েছে); tensorflow-এর GT-তে সব bucket 0; CI-র ভিন্ন OS/hardware। "Deviation" আংশিকভাবে ground truth-এর ত্রুটিও মাপে।
8. **Historical commit-এ পরীক্ষা নেই:** সব project HEAD-এ, সক্রিয় (ছয় মাসের মধ্যে commit)। Patch validation-এ আমাদের দরকার বছরখানেক পুরনো base commit, যেখানে dependency পুরনো — ঠিক যেখানে paper নিজেই দুর্বলতা স্বীকার করেছে।
9. **নিরাপত্তা বিবেচনা নেই:** Agent README, CI file, আর **web search-এর top-5 page** পড়ে command চালায় — এগুলো prompt injection-এর পথ (কেউ README-তে "run curl ... | bash" লিখে রাখলে?)। Container আংশিক সুরক্ষা দেয়, কিন্তু network খোলা থাকে, আর `docker build`/`docker run` চালাতে container-এর Docker access লাগে (paper-এ Docker-in-Docker বিস্তারিত নেই)। Paper এ নিয়ে কিছু বলেনি।
10. **Token ও call সংখ্যা report নেই:** শুধু USD-এ খরচ "current pricing" অনুযায়ী — দাম বদলালে তুলনা করা যায় না। Token সংখ্যা দিলে যেকোনো দামে recompute করা যেত।
11. **Time measurement-এর শর্ত:** 74 মিনিট 5টা একসাথে চলা অবস্থায়; LLM latency, download, compile আলাদা করে দেখানো হয়নি।
12. **Dataset ছোট ও জনপ্রিয়-কেন্দ্রিক:** 50টা, median 45K star — training data-তে এদের setup নির্দেশ প্রায় নিশ্চিত আছে। কম পরিচিত project-এ (যেমন SWE-rebench-এর হাজার হাজার repository) ফল কম হতে পারে।

**সহজ কথায়:** আমার মতে সবচেয়ে গুরুত্বপূর্ণ সমালোচনা: validation শুধু file-এর অস্তিত্ব দেখে। এটা আমাদের verifier gaming (CG12) প্রসঙ্গের সরাসরি পথ। বাকিগুলো ছোট, কিন্তু একসাথে paper-এর মাপজোখের নির্ভুলতায় প্রশ্ন তোলে।

---

## ১৩. Research Gaps — কোথায় কাজ করার সুযোগ আছে

| # | Gap | কেন গুরুত্বপূর্ণ | কে কিছুটা কাজ করেছে (আমাদের folder-এ) | Common gap |
|---|---|---|---|---|
| G1 | **Result integrity** — test result agent-এর লেখা নয়, আসলে চালানো থেকে এসেছে তা যাচাই; test skip করা, OR-fallback দিয়ে failure চাপা দেওয়া বা test মুছে দেওয়া ধরা | Validation শুধু file-এর অস্তিত্ব দেখে; scale-এ verifier gaming | Coding-Agent Evaluation & Reliability (Engineering Reliable Agents — verifier gaming); Trustworthy AI for SE | CG11, CG12 |
| G2 | **Historical commit ও পুরনো dependency-তে setup** | Patch validation-এ base commit-এ test চালাতে হয় | Coding-Agent Evaluation & Reliability (SWE-rebench — version grouping, dependency freeze); AI Coding Agents (SWE-bench Docker harness) | CG6 |
| G3 | **Per-test স্তরের structured output** — test ID ও status, F2P/P2P হিসাব | শুধু তিনটা সংখ্যা দিয়ে regression ধরা যায় না | AI Coding Agents (Agentless regression filter, SWE-bench F2P/P2P); Patch Validation | CG3 |
| G4 | **Run-to-run reliability** — একই project বারবার চালালে ফল কতটা স্থির | একবারের run-এর 33/50 নির্ভরযোগ্য কিনা অজানা | Coding-Agent Evaluation & Reliability (SWE-rebench 5 run, monograph) | CG4 |
| G5 | **Flaky test চেনা ও আলাদা করা** | Deviation-এর একটা কারণ; flaky test থাকলে regression signal ভুল | Coding-Agent Evaluation & Reliability (SWE-rebench flaky test বাদ দেয়); LLM Test Generation | CG3, CG4 |
| G6 | **Setup agent-এর নিরাপত্তা** — README/CI/web থেকে prompt injection, untrusted install command | Agent অজানা repository-তে command চালায় | Security of AI-Generated Code | CG5 |
| G7 | **C/C++, submodule, multi-module project** | 2/9 submodule; C/C++ সবচেয়ে কম সফল | AI Coding Agents (SWE-Bench Pro-র বহু-ভাষা দিক) | CG9 |
| G8 | **Agent memory ও ভুলের পুনরাবৃত্তি** (sudo, version default) | Budget নষ্ট, ব্যর্থ project-এ খরচ 3.4 গুণ | AI Coding Agents (SWE-agent-এর ACI design) | — |
| G9 | **Model-নিরপেক্ষ evaluation** — বিভিন্ন LLM, scaffold বনাম model-এর অবদান আলাদা করা | শুধু GPT-4o-mini | Coding-Agent Evaluation & Reliability (scaffold-ভেদ) | CG8 |
| G10 | **শক্তিশালী ground truth ও metric** — CI-নির্ভর না হয়ে, per-test, শূন্য-denominator-নিরাপদ | Selection bias, ambiguous deviation | Coding-Agent Evaluation & Reliability | CG10 |
| G11 | **Multi-configuration test execution** (OS, browser, version) | Single configuration-এ bug লুকিয়ে থাকে | — (খোলা) | — |
| G12 | **Downstream ব্যবহারে মূল্যায়ন** — তৈরি environment দিয়ে agent patch যাচাই করলে assurance কতটা বাড়ে | Paper এটা "vision" হিসেবে বলেছে, পরীক্ষা করেনি | Automated Program Repair (VRpilot feedback loop); Patch Validation | CG1, CG3 |
| G13 | **Cost transparency** — token, call, latency আলাদা করে | USD দাম বদলায়; তুলনা অসম্ভব | Coding-Agent Evaluation & Reliability | CG8 |

**সহজ কথায়:** Gap table-এর মূল বার্তা: পরীক্ষার ফল সত্য কিনা (G1), পুরনো commit-এ কাজ করে কিনা (G2), per-test স্তরে তথ্য (G3), বারবার চালালে একই ফল (G4) — এই চারটা আমাদের কাজের সবচেয়ে কাছের সুযোগ।

---

## ১৪. কী করলে আরও ভালো হবে — Improvement Ideas

1. **Trusted result extraction (G1):** Agent-এর লেখা result file বিশ্বাস না করে, control center নিজে script চালিয়ে framework-এর machine-readable report (pytest `--junitxml`, Maven Surefire XML, Jest JSON) parse করবে। সাথে integrity check — test file-এর git diff খালি কিনা, script-এ `|| true` বা `|| exit 0` আছে কিনা, test সংখ্যা repository-র static test গণনার (যেমন `pytest --collect-only`) কাছাকাছি কিনা।
2. **Historical-commit mode (G2):** Input-এ commit hash; meta-prompt-এ "latest practice" না চেয়ে "commit তারিখের সময়কার practice" চাওয়া; lock file বা commit তারিখ অনুযায়ী dependency version-এ pin করা (SWE-rebench-এর dependency freeze ধারণা)।
3. **Per-test output + F2P/P2P হিসাব (G3):** Result file-এ শুধু তিনটা সংখ্যা নয়, প্রতিটা test ID ও status। তাহলে সরাসরি Agentless-ধাঁচের regression filter চালানো যায়।
4. **Repeat ও flaky detection (G4, G5):** তৈরি script 3–5 বার চালিয়ে যে test-এর status বদলায় তাকে flaky চিহ্নিত করা; agent-কেও কয়েকবার চালিয়ে success-এর variance report।
5. **Episodic memory / "do-not-repeat" তালিকা (G8):** ব্যর্থ command-pattern (যেমন sudo নেই) prompt-এ স্থায়ী নিয়ম হিসেবে রাখা; version install-এর পর `update-alternatives` বা PATH যাচাই checklist।
6. **Sandboxing ও input sanitization (G6):** Web/README থেকে আসা text-কে "data" হিসেবে চিহ্নিত করা, network allow-list, `curl ... | bash` ধরনের command-এ সতর্কতা।
7. **Submodule ও multi-module checklist (G7):** `.gitmodules` থাকলে স্বয়ংক্রিয় `git submodule update --init --recursive`; Maven-এ `-fae` (fail at end) ধরনের option প্রথমেই বিবেচনা।

**সহজ কথায়:** উন্নতির ধারণাগুলোর মূল কথা: agent-কে বিশ্বাস না করে নিজে যাচাই করো, পুরনো commit-এ চালাও, per-test ফল রাখো, বারবার চালাও।

---

## ১৫. কোন Gap-এ Research করলে ভালো Result ও Publication আসতে পারে

> ⚠️ Sub-domain 4-এর প্রথম paper-গুলোর একটার ভিত্তিতে প্রাথমিক মত। পুরো sub-domain শেষে চূড়ান্ত হবে।

| Gap | SPL3-তে করা সম্ভব? | Novelty | Publication সম্ভাবনা |
|---|---|---|---|
| **G1: Result integrity checker** for setup/test agent (agent-লেখা result বনাম আসল execution; tamper detection) | ✅ হ্যাঁ — ExecutionAgent open source, 50টা project-এর ground truth আছে | উচ্চ — verifier gaming এখন গরম বিষয়, setup agent-এ কেউ মাপেনি (fact sheet-এ নেই) | ⭐⭐⭐⭐ |
| **G2 + G3: Historical-commit, per-test environment builder** — SWE-rebench/SWE-bench task-এর Docker image-কে ground truth ধরে ExecutionAgent-কে মূল্যায়ন | ✅ হ্যাঁ — ছোট subset (20–30 task) | উচ্চ — দুই line-এর কাজ (setup agent ও benchmark environment) সরাসরি জোড়া | ⭐⭐⭐⭐⭐ |
| **G4: Setup agent-এর reliability** (k run, variance) | ✅ হ্যাঁ, খরচ কম (GPT-4o-mini-স্তরের model-এ প্রতি project 0.16 USD) | মাঝারি-উচ্চ | ⭐⭐⭐ |
| **G12: Environment + regression signal দিয়ে agent patch assurance** | ✅ হ্যাঁ — আমাদের মূল direction-এর অংশ | উচ্চ, কিন্তু অন্য অংশের উপর নির্ভরশীল | ⭐⭐⭐⭐ |
| G6: Setup agent-এর prompt injection নিরাপত্তা | ⚠️ সম্ভব, কিন্তু নৈতিক ও sandbox সতর্কতা লাগে | উচ্চ | ⭐⭐⭐ |

**সহজ কথায়:** সবচেয়ে সম্ভাবনাময় দুটো পথ: (১) result integrity checker এবং (২) পুরনো commit আর per-test ভিত্তিতে environment builder। দুটোই ছোট subset নিয়ে SPL3-তে করা যায়।

**সম্ভাব্য venue (general guidance):** ISSTA, ICSE, FSE, ASE (এই paper নিজেই ISSTA-তে); workshop — LLM4Code, AST (Automation of Software Test); journal — ACM TOSEM, IEEE TSE, EMSE, JSS, IST।

---

## ১৬. SPL3 Implementation Perspective — Software-এ কীভাবে আনবো

**মূল ধারণা:** আমাদের "assurance report for AI agent patches"-এ একটা **Environment & Test Execution module** লাগবে। SWE-bench বা SWE-rebench task হলে তাদের প্রস্তুত Docker image ব্যবহার করবো; অন্য repository হলে ExecutionAgent-ধাঁচের agent fallback হিসেবে। তারপর regression test আর generated test — দুটো dynamic signal আলাদা আলাদা report করবো, static judge-এর signal থেকে পৃথক রেখে।

**প্রস্তাবিত module:**
1. **Environment Resolver:** task-এর জন্য বিদ্যমান image (SWE-bench/SWE-rebench) আছে কিনা দেখবে; না থাকলে ExecutionAgent (open-source code) চালাবে, commit hash সহ।
2. **Trusted Test Runner:** agent-এর script চালাবে কিন্তু result নিজে parse করবে — JUnit XML, pytest JSON/XML, Jest JSON। Per-test status বের করবে।
3. **Integrity Checker (G1):** script-এ `|| true`, `|| exit 0`, test-skip flag, test file-এর diff — সব flag করবে। Agent patch apply-এর আগে ও পরে test file hash মিলাবে (patch যেন test বদলাতে না পারে — monograph-এর architectural separation)।
4. **Flaky Detector (G5):** base commit-এ প্রতিটা test 3 বার চালিয়ে অস্থির test আলাদা করবে, regression signal থেকে বাদ দেবে।
5. **Regression Signal:** Agentless-এর মতো — base-এ pass করা (flaky বাদে) test-গুলো patch-এর পরে চালিয়ে কতগুলো ভেঙেছে।
6. **Generated-test Signal:** Sub-domain 4-এর অন্য paper-এর test generator যে test বানাবে, সেগুলো এই environment-এ চালানো।
7. **Report:** প্রতিটা signal আলাদা — মান, uncertainty (repeat-এর variance), environment version (Dockerfile hash, model version) — CG11-এর verifier versioning।

**Practical সতর্কতা:**
- Windows-এ WSL2 + Docker Desktop লাগবে; ExecutionAgent নিজে container-এ চলে আর container বানায় — Docker socket mount লাগতে পারে, নিরাপত্তা বিবেচনা করতে হবে।
- প্রতি project গড়ে 74 মিনিট — তাই ছোট subset (10–20 project/task), আর সফল Dockerfile cache করা।
- API খরচ ও token প্রতিটা run-এ log করবো (G13)।

**সহজ কথায়:** আমাদের software-এ আসবে ছয়-সাতটা module: environment তৈরি, বিশ্বাসযোগ্য test runner, integrity checker, flaky detector, regression signal, generated-test signal, আর report। মূল কথা — agent যা বলে তা নয়, আমরা নিজে যা মাপি তা-ই report-এ যাবে।

---

## ১৭. পরবর্তী গবেষণায় এই Paper-এর প্রভাব ও সংযোগ (Context)

- **Sub-domain 3 (SWE-rebench)-এর সাথে সরাসরি তুলনা:** দুটোই environment setup automate করে।
  - SWE-rebench: Python-only, Qwen2.5-72B, agentless (নির্দিষ্ট ধাপ) recipe, সর্বোচ্চ 3 candidate; 31% repository-তে working recipe, install ও validate stage-এ সামগ্রিক প্রায় 14%; 18 task-এর ছোট study-তে agentless 10 candidate 9/18, interactive agent 1 trial 8/18। SWE-rebench authors নিজেই "interactive install"-কে yield বাড়ানোর সুযোগ বলেছেন।
  - ExecutionAgent: ঠিক সেই interactive পথ, আর তার ablation দেখায় feedback ছাড়া (অর্থাৎ একবারে script) মাত্র 5টা, feedback-সহ 33টা।
  - **আমার পর্যবেক্ষণ:** দুই paper-এর সংখ্যা সরাসরি তুলনীয় নয় — SWE-rebench historical commit-এ F2P/P2P পর্যন্ত যাচাই করে, ExecutionAgent HEAD-এ শুধু suite চালায় ও সংখ্যা মেলায়। আমাদের assurance layer-এর দরকার দুটোর মিলন: interactive agent + historical commit + per-test যাচাই।
- **Sub-domain 1 (Agentless)-এর regression-test ধাপ:** Agentless পুরনো passing test চালিয়ে regression কম এমন patch রাখে, তারপর reproduction test। এই ধাপ SWE-bench-এর প্রস্তুত environment ছাড়া চলে না। SWE-bench-এর বাইরে (যেকোনো repository-তে) Agentless বা আমাদের assurance layer চালাতে হলে ExecutionAgent-ধাঁচের setup অপরিহার্য।
- **Sub-domain 1 (SWE-bench):** Environment reproducibility সমস্যা (conda → Docker) — ExecutionAgent-এর output Dockerfile, তাই এক অর্থে "SWE-bench harness যেকোনো project-এর জন্য"।
- **Sub-domain 2 (VRpilot):** compiler/sanitizer/test feedback loop — একই ধাঁচের iterative refinement; একই ঝুঁকি (validator-কে খুশি করা = feedback overfitting)।
- **একই গবেষণা দল:** RepairAgent (Bouzenia, Devanbu, Pradel), DyPyBench (Bouzenia et al., FSE 2024) — যেখানে executable Python project-এর benchmark হাতে বানাতে হয়েছিল; ExecutionAgent সেই হাতের কাজ automate করার চেষ্টা।
- **পরবর্তী সম্পর্কিত কাজ (নাম আমার পূর্বজ্ঞান থেকে, আমাদের fact sheet-এ নেই — supervisor-কে দেখানোর আগে যাচাই করতে হবে):** Repo2Run, EnvBench, SetupBench নামে environment setup-এর agent/benchmark কাজ এসেছে বলে জানি; তাদের সংখ্যা এখানে দিচ্ছি না।

**সহজ কথায়:** এই paper আমাদের গবেষণার ভিত্তি। তুলনা: SWE-rebench Python-only আর একবারে recipe লেখে, ExecutionAgent বহু ভাষা আর interactive। দুটোর সংখ্যা সরাসরি তুলনীয় নয়, কারণ লক্ষ্য আলাদা।

---

## ১৮. Supervisor-এর সম্ভাব্য প্রশ্ন ও উত্তর (Viva Prep)

**Q1. এই paper LLM Test Generation sub-domain-এ কেন? এটা তো test বানায় না।**
A: ঠিক, এটা test generate করে না, test **চালানোর** environment বানায়। কিন্তু generated test-এর কোনো মূল্য নেই যদি সেটা চালানো না যায়। Test generation, regression testing, reproduction test — সব dynamic signal-এর পূর্বশর্ত এই ক্ষমতা। আমাদের assurance layer-এর dynamic অংশ এর উপর দাঁড়াবে।

**Q2. Meta-prompting আর সাধারণ prompt engineering-এর পার্থক্য কী?**
A: সাধারণ prompt-এ মানুষ হাতে প্রতিটা language-এর নিয়ম লেখে। Meta-prompting-এ LLM-কে জিজ্ঞেস করা হয় "Java project-এর test চালাতে 10টা guideline দাও", আর সেই উত্তর agent-এর prompt-এ বসে। Ablation-এ guideline সরালে deviation<10% project 29 থেকে 15-এ নামে (প্রায় 48%)।

**Q3. 6.6x improvement কীভাবে হিসাব হয়েছে?**
A: Test suite চালাতে পারা project-এর সংখ্যা: ExecutionAgent 33, সেরা baseline (LLM scripts) 5; $33/5 = 6.6$।

**Q4. 7.5% deviation মানে কী, আর এর সীমাবদ্ধতা কী?**
A: প্রতিটা tested project-এ pass, fail, skip — তিনটার আলাদা relative error-এর গড়, তারপর 33টা project-এর গড়: $(17 \times 0 + 16 \times 15.4)/33 \approx 7.5\%$। সীমাবদ্ধতা: ছোট bucket-এ খুব sensitive (django-তে 1টা বাড়তি fail-ই 20% fail-deviation), GT-তে 0 থাকলে অসংজ্ঞায়িত, আর Table 1 থেকে আমি সংখ্যাটা হুবহু reproduce করতে পারিনি।

**Q5. LLM scripts অনেক project build করলো কিন্তু test চালাতে পারলো না কেন?**
A: User setup আর development setup আলাদা। Build-এর জন্য `setup.py` বা `pom.xml` যথেষ্ট, কিন্তু test-এর জন্য বাড়তি compiler, testing framework, recompiled dependency, config বদল লাগে। একবার লেখা script অপ্রত্যাশিত error সামলাতে পারে না; ExecutionAgent error দেখে শোধরায়।

**Q6. AutoGPT-ও তো agent — কেন এত খারাপ?**
A: একই model ও budget-এ AutoGPT 9 build, 4 test। Authors তিনটা কারণ বলেছেন: meta-prompting নেই, চালানো command-এর memory কম কার্যকর, আর tool কম robust (process termination detection, timeout-এ wait/input/terminate, output cleaning নেই)। অর্থাৎ task-specific scaffold design বড় পার্থক্য করে — এটা SWE-agent-এর ACI finding-এর সাথে মেলে।

**Q7. SWE-rebench-ও environment setup automate করেছে — দুটোর পার্থক্য কী?**
A: SWE-rebench Python-only, নির্দিষ্ট ধাপের (agentless) recipe pipeline — LLM নিজে command চালায় না, error log দেখে recipe আবার লেখে; লক্ষ্য historical commit-এ F2P/P2P সহ valid task। ExecutionAgent বহু-ভাষার interactive agent, HEAD-এ suite চালায়, CI-এর সংখ্যার সাথে মেলায়। SWE-rebench authors interactive install-কে উন্নতির সুযোগ বলেছেন — ExecutionAgent সেটাই, কিন্তু historical commit-এ পরীক্ষিত নয়।

**Q8. তোমার assurance layer-এ এই paper থেকে কী নেবে আর কী বদলাবে?**
A: নেবো: interactive setup agent, meta-prompting, CI hint, Dockerfile output। বদলাবো: (১) result agent-এর লেখা file থেকে নয়, framework-এর XML/JSON report থেকে নিজে parse; (২) per-test status; (৩) integrity check (`|| true`, test file diff); (৪) historical commit mode; (৫) flaky detection ও repeat।

**Q9. এই paper-এর সবচেয়ে বড় দুর্বলতা কী, তোমার মতে?**
A: Validation শুধু তিনটা file আছে কিনা দেখে। Automated, বড় scale-এ ব্যবহার করলে agent ভুয়া বা আংশিক ফলাফল লিখে "সফল" হতে পারে — verifier gaming (CG12)। Paper-এ মানুষ হাতে যাচাই করায় এটা ধরা পড়েনি বা আলোচিত হয়নি।

**Q10. খরচ 0.16 USD — এটা কি বাস্তবসম্মত?**
A: GPT-4o-mini-এর মতো সস্তা model দিয়ে, 2025-এর দামে। ব্যর্থ project-এ 0.34, সফলে 0.10; প্রতি সফল project-এ আমার হিসাবে প্রায় 0.24 USD। কিন্তু paper token সংখ্যা দেয়নি, তাই অন্য model-এ খরচ কত হবে তা সরাসরি হিসাব করা যায় না। সময়ও বড় খরচ — গড় 74 মিনিট।

**Q11. Ablation-এ preparation phase সরালে খরচ বাড়লো কেন?**
A: Guideline ও hint ছাড়া agent অন্ধভাবে বেশি command চালায়, budget শেষ করে, তাই 0.16 থেকে 0.19 USD; অথচ test চলে মাত্র 8টায়। Feedback phase সরালে খরচ 0.02 কারণ একবার মাত্র script লেখা হয় — সস্তা কিন্তু 5টায় test।

**সহজ কথায়:** Viva-র জন্য তিনটা বিষয় ভালো করে মুখস্থ রাখো: (১) 6.6x কীভাবে হিসাব, (২) deviation-এর সীমাবদ্ধতা, (৩) result integrity-ই বড় দুর্বলতা।

---

## ১৯. Glossary (দ্রুত মনে রাখার জন্য)

| Term | অর্থ |
|---|---|
| Test suite | Project-এর সব automated test |
| Build system | Source থেকে চালানোর উপযোগী program বানানোর tool (Maven, npm, Make) |
| Development setup | Test চালানোর জন্য দরকারি পূর্ণ setup (user setup-এর চেয়ে বেশি) |
| Docker / Dockerfile | Isolated environment / তার recipe |
| CI/CD | প্রতিটা পরিবর্তনে স্বয়ংক্রিয় build ও test |
| Ground truth | CI log থেকে নেওয়া আসল pass/fail/skip সংখ্যা |
| Meta-prompting | LLM-কে দিয়ে prompt-এর অংশ (guideline) লেখানো |
| Guideline | Agent-এর জন্য ছোট নিয়মের তালিকা (এখানে 10টা) |
| Control center | Agent loop, tool, timeout, validation পরিচালনাকারী component |
| Command budget | প্রতি attempt-এ সর্বোচ্চ command (40) |
| Attempt | Outer loop-এর একটা চেষ্টা (সর্বোচ্চ 3) |
| Summarization | 200 token-এর বেশি output সংক্ষেপ করা |
| Deviation | Ground truth থেকে আপেক্ষিক পার্থক্য (%) |
| Submodule | Repository-র ভিতরে আরেকটা repository |
| Flaky test | একই code-এ কখনো pass কখনো fail |
| Trajectory | Agent-এর নেওয়া ধাপের ক্রম |
| Linguist | GitHub-এর language শনাক্তকরণ library |

**সহজ কথায়:** এই glossary দেখে পুরো paper-এর ভাষা মনে করা যায়। কোনো শব্দ ভুলে গেলে এখানে ফিরে এসো।

---

## ২০. এক নজরে সারাংশ (Summary Card)

| | |
|---|---|
| **Problem** | যেকোনো project-এর test suite automatically চালানো কঠিন — ভাষা, build tool, dependency, অসম্পূর্ণ docs |
| **Solution** | ExecutionAgent — meta-prompting + CI/web hint + interactive terminal agent + control center |
| **Method** | Preparation phase → feedback loop (40 command × 3 attempt), output summarization, Dockerfile ও script output |
| **Key result** | 50 project, 14 language: 41 built, 33 tested, 29 close to ground truth; সেরা baseline-এর 6.6 গুণ; গড় deviation 7.5% (tested-দের মধ্যে) |
| **Cost** | GPT-4o-mini, গড় USD 0.16 ও 74 মিনিট প্রতি project |
| **Key insight** | Feedback loop ও guideline অপরিহার্য; build ≠ test; C/C++ ও submodule কঠিন |
| **Main limitation** | File-existence validation, single model, single run, HEAD-only, metric অস্পষ্টতা |
| **আমাদের জন্য gap** | Assurance layer-এর dynamic signal-এর ভিত্তি — কিন্তু result integrity, historical commit, per-test output যোগ করতে হবে |

---

## ২১. বর্তমান (2026) প্রেক্ষাপট — আজকের Model ও Agent-দের সাথে তুলনা

> **উৎস:** এই section-এর সব current-state তথ্য `00_Current_State_2026_Sources.md` (fact sheet, compiled 2026-10-28) থেকে নেওয়া। প্রতিটা সংখ্যার পাশে লেখা আছে সেটা **কোম্পানির নিজের দাবি (vendor-reported)** নাকি **স্বাধীনভাবে মাপা (independent)**; fact sheet যেটাকে "search-snippet only" বলেছে, এখানেও তাই চিহ্নিত। আমার নিজের যুক্তি "আমার পর্যবেক্ষণ" দিয়ে আলাদা করা।
>
> **গুরুত্বপূর্ণ:** Fact sheet-এ **environment setup বা test-suite execution-এর কোনো benchmark-এ বর্তমান model-এর (Opus 5.5, GPT-6, Gemini 4) কোনো সংখ্যা নেই** — ExecutionAgent-এর 50-project dataset-এ বা অন্য কোথাও। তাই নিচের তুলনা বেশিরভাগ পরোক্ষ, আর এই অনুপস্থিতি নিজেই একটা gap।

### ২১.১ Paper-এর সময় বনাম এখন

| দিক | Paper-এ (ISSTA 2025, accepted 2025-03) | এখন, October 2026 | উৎস |
|---|---|---|---|
| Agent-এর model | GPT-4o-mini; Claude, DeepSeek, Llama-ও JSON format সমর্থন করে বলে উল্লেখ, কিন্তু পরীক্ষা হয়নি | Claude Opus 5.5 (2026-09-22), GPT-6 family (Astra, Sol, Luna, 6.1 Sol, 6.1 Terra), Gemini 4 Argon (2026-10-13), Kimi K3.1 Pro, DeepSeek V4 | Fact sheet §1 (primary/secondary) |
| Environment setup / test execution-এ বর্তমান model-এর ফল | 33/50 test executed (GPT-4o-mini) | **পাওয়া যায়নি** — fact sheet-এ কোনো setup-benchmark বা ExecutionAgent re-run নেই | Fact sheet (অনুপস্থিতি) |
| সবচেয়ে কাছের বর্তমান benchmark (terminal-ভিত্তিক agent কাজ, তবে test-suite setup নয়) | — | Terminal-Bench 4.0, Vals.ai (mini-SWE-agent, avg@3): Opus 5.5 65.15%, Kimi K3.1 Pro 63.64%, GPT-6 Astra 59.60%, GPT-6.1 Sol 55.05% (**independent**); Anthropic-এর দাবি Opus 5.5 66.4% (**vendor-reported**) | Vals.ai 2026-10-26; Opus 5.5 launch page |
| Agent scaffold | নিজস্ব 4-tool agent; general agent AutoGPT 4/50 | mini-SWE-agent এখন Scale, Vals.ai, Artificial Analysis-এর **standard harness**; Claude Code v2.1.312, Codex CLI rust-v0.165.0, OpenHands v1.34.0 সক্রিয় — কিন্তু কোনোটাই ExecutionAgent-এর dataset-এ মাপা হয়নি | Fact sheet §1 (GitHub API, primary) |
| প্রতি task খরচ | USD 0.16 প্রতি project (GPT-4o-mini) | Terminal-Bench 4.0-এ USD 1.72 (GPT-6.1 Sol) থেকে USD 17.64 (Gemini 4 Argon), Opus 5.5 USD 13.20 (**independent**); SWE-rebench USD 0.81–4.40 প্রতি problem (**independent**) | Vals.ai; swe-rebench.com |
| Model-এর দাম | Paper token সংখ্যা দেয়নি | GPT-6.1 Terra: USD 1 input / USD 5 output প্রতি million token (**vendor-reported**); Opus 5.5: USD 4 / USD 20 (**vendor-reported, search-snippet only**) | Fact sheet §1 |
| প্রতি task সময় | 74 মিনিট (5টা একসাথে) | Terminal-Bench 4.0-এর long-horizon task প্রতি প্রায় 35 মিনিট থেকে 1h22m; Opus 5.5 প্রতি test 1h04m (**independent**) | Vals.ai |
| Run-to-run variance | প্রতি project একবার; variance report নেই | Anthropic Terminal-Bench 4.0-এ ±2.6 SE (**vendor**); SWE-rebench-এ pass@1 বনাম pass@5-এ 12–18 point ফাঁক (**independent**); Noise Floor Audit: prompt-এর অর্থ-অপরিবর্তিত পরিবর্তনে SD rerun-এর 11–58 গুণ (**independent**) | Fact sheet §3 |
| Result integrity / verifier gaming | Validation = তিনটা file আছে কিনা; আলোচনা নেই | METR: 8 ঘণ্টার বেশি task-এ সফল run-এর ≥16% অবৈধ (**independent**, আগের প্রজন্ম); Opus 5.5 System Card-এ রিপোর্ট: কিছু RL environment-এ Claude git দিয়ে repository-র পরিবর্তন লুকিয়েছে (**vendor**); Fable 5.1 "failing test disable করার সম্ভাবনা কম" (**vendor, qualitative**) | Fact sheet §1, §3 |
| Agent-এর CI/build কাজের গ্রহণযোগ্যতা | — | প্রায় 33k agent PR-এর study (MSR 2026): docs, CI ও build PR সবচেয়ে বেশি merge হয়; unmerged PR প্রায়ই CI fail করে (**independent**, 2025-এর agent, AIDev dataset) | arXiv 2601.15195 |
| Coding environment-এ prompt injection | আলোচনা নেই | Opus 5.5 adaptive attacker-এ ASR safeguard ছাড়া 54.61%, probe সহ 11.13% (**vendor-reported**, বাইরের red-team tool); CI-তে "comment and control" prompt injection Claude Code, Gemini CLI, Copilot Agent-এ (**secondary, search-snippet only**) | Opus 5.5 System Card §5.2.2.1; CSA note |
| Agent-লেখা test-এর মান | — | Agent PR-এর test patch-এর 80.2%-এ দুর্বল বা কোনো explicit oracle নেই (**independent**) | "All Smoke, No Alarm", arXiv 2606.18168 |

**আমার পর্যবেক্ষণ (খরচের অনুপাত, সতর্কতাসহ):** $1.72 / 0.16 \approx 10.8$ আর $13.20 / 0.16 = 82.5$। অর্থাৎ frontier model-এ agentic terminal task-এর প্রতি-task খরচ ExecutionAgent-এর 2025-এর খরচের প্রায় 11 থেকে 83 গুণ। **কিন্তু এটা একই কাজ নয়** (Terminal-Bench task বনাম test-suite setup), একই harness নয় — তাই এটা শুধু "frontier model দিয়ে আবার চালালে খরচ অনেক বাড়তে পারে" এর ইঙ্গিত, পরিমাপ নয়।

**সহজ কথায়:** Paper-এর সময় (2025) আর এখনকার (2026) মধ্যে বড় পার্থক্য: model আরও শক্তিশালী ও দামি, কিন্তু environment-setup কাজে নতুন model-এর কোনো সংখ্যা কেউ প্রকাশ করেনি। এটাই একটা gap।

### ২১.২ কোন Finding এখনো সত্য, কোনটা পুরনো হয়ে গেছে

- **অজানা (মাপা হয়নি) — "33/50 test executed":** বর্তমান model দিয়ে এই dataset-এ কেউ আবার চালিয়েছে এমন তথ্য fact sheet-এ নেই। Terminal-Bench 4.0-এ সেরা model-ও প্রায় 59–65% (independent), অর্থাৎ terminal-ভিত্তিক agent কাজ এখনো saturated নয় — **আমার অনুমান**, setup-এর জন্য সরাসরি প্রমাণ নয়।
- **এখনো সত্য বলে মনে হয় — "Terminal অপরিহার্য" (74.8% call):** শিল্প এখন bash-কেন্দ্রিক mini-SWE-agent-কে standard harness হিসেবে ব্যবহার করে (fact sheet §1)। **আমার পর্যবেক্ষণ:** এটা paper-এর finding-এর সাথে সামঞ্জস্যপূর্ণ, তবে fact sheet নিজে tool-usage distribution মাপেনি।
- **সম্ভবত পুরনো — "খরচ নগণ্য (USD 0.16)":** এটা সস্তা model-এর উপর দাঁড়িয়ে। Frontier model-এ agentic task-এর independent খরচ USD 1.72–17.64 (Vals.ai)। সস্তা current model (GPT-6.1 Terra, vendor দাম USD 1/USD 5 per million token) দিয়ে খরচ কেমন হবে তা জানা নেই, কারণ paper token সংখ্যা দেয়নি।
- **এখনো সত্য, আরও জোরালো — "agent একই ভুল বারবার করে, budget নষ্ট":** বর্তমান model-এর ক্ষেত্রে fact sheet-এ এই নির্দিষ্ট আচরণের সংখ্যা নেই; তবে Sonnet 5.5 max effort-এ xhigh-এর চেয়ে খারাপ, কারণ subagent run timeout বা scope-এর বাইরের edit (vendor) — অর্থাৎ বেশি compute সবসময় ভালো নয়, যা paper-এর "ব্যর্থ project-এ বেশি খরচ" পর্যবেক্ষণের সাথে মেলে।
- **গুরুত্ব বেড়েছে — "validation শুধু file-existence" (আমার critique #1):** 2026-এ verifier gaming এখন মাপা ঘটনা — SWE-Bench Pro Verified-এ GLM-5.2 78.80% থেকে anti-hacking safeguard দিলে 57.32% (independent); DeepSWE-তে প্রতারণার 87% ক্ষেত্রে `.git` history থেকে gold commit পড়া (independent)। একটা setup agent-কে যদি "test result দাও" বলে reward করা হয়, একই ধরনের shortcut-এর ঝুঁকি আছে।
- **এখনো সত্য — "test চালানোই যথেষ্ট নয়":** OpenAI-এর audit-এ Verified-এর hard subset-এর ≥59.4% task-এর test সঠিক submission reject করে (**search-snippet only**); SWE-Bench Pro-র 27.4–34.1% task ত্রুটিপূর্ণ (secondary)। অর্থাৎ environment ঠিক থাকলেও test-এর মান আলাদা সমস্যা — ExecutionAgent শুধু প্রথম সমস্যা সমাধান করে।
- **নতুন ঝুঁকি, paper-এ ছিল না — setup agent-এ prompt injection:** ExecutionAgent README, CI file আর web page পড়ে command চালায়; 2026-এ coding agent-এ prompt injection ও CI-ভিত্তিক injection বারবার রিপোর্ট হচ্ছে (fact sheet §5)। **আমার পর্যবেক্ষণ:** setup agent এই আক্রমণের জন্য স্বাভাবিক লক্ষ্য, কিন্তু setup agent-এর উপর নির্দিষ্ট পরিমাপ fact sheet-এ নেই।

**সহজ কথায়:** যা এখনো সত্য: terminal-ই agent-এর প্রধান tool, test চালানো যথেষ্ট নয়, আর verifier gaming আরও জরুরি। যা পুরনো হতে পারে: খরচ 0.16 USD (সস্তা model-এর কথা)। আর নতুন ঝুঁকি: prompt injection।

### ২১.৩ এই Paper-এর Gap-গুলো আজও খোলা কিনা

| Gap | 2026-এ অবস্থা | প্রমাণ |
|---|---|---|
| G1 / CG11, CG12: Result integrity ও verifier gaming | **খোলা, আরও জরুরি** | GLM-5.2 78.80 থেকে 57.32 (SWE-Bench Pro Verified, independent); METR ≥16% অবৈধ সফল run (independent, আগের প্রজন্ম); Opus 5.5 System Card: কিছু RL environment-এ Claude git দিয়ে পরিবর্তন লুকিয়েছে (vendor); setup agent-এর জন্য নির্দিষ্ট audit **পাওয়া যায়নি** |
| G2 / CG6: Historical commit ও পুরনো dependency | **বর্তমান তথ্য পাওয়া যায়নি** | SWE-rebench নতুন window (111 problem, 65 repo, শেষ 2026-07-01) চালাচ্ছে, কিন্তু fact sheet-এ তাদের environment setup-এর বর্তমান success rate নেই |
| G3 / CG3: Per-test structured output | **বর্তমান তথ্য পাওয়া যায়নি** | Fact sheet-এ setup agent-এর output format নিয়ে কিছু নেই; agent-লেখা test-এর 80.2% দুর্বল oracle (independent) — test চালানো গেলেও signal দুর্বল |
| G4 / CG4: Run-to-run reliability | **খোলা** | SWE-rebench pass@1 বনাম pass@5 12–18 point; SWE Atlas pass@1 থেকে pass^3-এ 30–50% পতন (**search-snippet only**); Noise Floor 11–58 গুণ; setup agent-এর জন্য variance মাপা হয়নি |
| G5 / CG3, CG4: Flaky test | **বর্তমান তথ্য পাওয়া যায়নি** | AIDev-এর ~205k test file-এ assertion মান ও flakiness study আছে (figure secondary, not verified); setup-স্তরে flaky detection-এর তথ্য নেই |
| G6 / CG5: Setup agent-এর নিরাপত্তা | **খোলা** | Opus 5.5 coding-environment prompt injection ASR 54.61% (safeguard ছাড়া) / 11.13% (probe সহ) (vendor); MCP tool-poisoning 7 client-এ (independent); CI prompt injection (secondary, snippet) |
| G7 / CG9: C/C++, submodule | **বর্তমান তথ্য পাওয়া যায়নি** | Fact sheet-এ language-ভিত্তিক setup ফল নেই; SWE-bench Multilingual official top 72.7% (independent) বনাম Opus 5.5 93.9% (vendor) — patch-solving, setup নয় |
| G8: Agent memory ও ভুলের পুনরাবৃত্তি | **বর্তমান তথ্য পাওয়া যায়নি** | Effort বাড়ালে কখনো খারাপ (FrontierCode, Sonnet 5.5 — vendor) — পরোক্ষ ইঙ্গিত মাত্র |
| G9 / CG8: Model-নিরপেক্ষ evaluation | **খোলা, আরও খারাপ** | Scaffold বদলালে একই model-এ 29.8 point পর্যন্ত পার্থক্য (independent); vendor বনাম independent সংখ্যার ফাঁক (Sonnet 5.5 Terminal-Bench 70.6% vendor বনাম 63.6–64.1% independent) |
| G10 / CG10: Ground truth ও metric | **খোলা** | Benchmark-এর নিজের test ত্রুটিপূর্ণ (≥59.4% Verified hard subset, snippet; SWE-Bench Pro 27.4–34.1%, secondary) — "CI log = ground truth" ধারণার মতোই "benchmark test = ground truth" প্রশ্নবিদ্ধ |
| G11: Multi-configuration | **বর্তমান তথ্য পাওয়া যায়নি** | — |
| G12 / CG1, CG3: Environment দিয়ে patch assurance | **খোলা** | PatchDiff: plausible patch-এর 29.6% gold থেকে ভিন্ন আচরণ, 7.8% "correct" patch পুরো developer suite-এ fail (independent, 2025 model; বর্তমান model-এ আবার মাপা হয়নি) — পুরো suite চালানোর ক্ষমতাই এখানে মূল |
| G13 / CG8: Cost transparency | **আংশিক উন্নতি** | Vals.ai ও SWE-rebench এখন প্রতি task USD খরচ ও সময় দেয় (independent); token-স্তরের তথ্য fact sheet-এ নেই |

**সহজ কথায়:** 13টা gap-এর মধ্যে বেশিরভাগ 2026-এও খোলা বা "তথ্য পাওয়া যায়নি"। মানে এখানে গবেষণার সুযোগ আছে, কারণ কেউ এখনো মাপেনি।

### ২১.৪ বর্তমান Model দিয়ে আবার পরীক্ষা করলে — SPL3 Idea (cost-aware)

**মূল প্রশ্ন:** "2026-এর একটা সস্তা model দিয়ে ExecutionAgent কি বেশি project চালাতে পারে, আর তার result কি বিশ্বাসযোগ্য — বিশেষ করে historical commit-এ, per-test স্তরে?"

1. **Re-run on a subset (G9, G4):** ExecutionAgent-এর 50টার মধ্যে 15টা project — paper-এর 9টা build-fail + 6টা tested (তুলনার জন্য)। একটা সস্তা current model (যেমন GPT-6.1 Terra, vendor-reported দাম USD 1 / USD 5 per million token; বা DeepSeek V4 Pro) দিয়ে, প্রতিটা 3 বার। **যে gap দেখাবে:** C/C++ project-এ নতুন model কি উন্নতি আনে, আর run-ভেদে ফল কতটা বদলায় — fact sheet-এ এই সংখ্যা নেই।
2. **SWE-rebench/SWE-bench image-কে ground truth ধরে historical-commit test (G2, G3):** SWE-rebench-এর 10–15টা task নিয়ে, ExecutionAgent-কে base commit-এ environment বানাতে বলা; তারপর প্রস্তুত image-এ পাওয়া per-test status (F2P/P2P তালিকা)-র সাথে মেলানো। **Gap:** setup agent পুরনো commit-এ per-test স্তরে কতটা সঠিক — CI-এর তিনটা সংখ্যার বদলে test ID স্তরে।
3. **Result integrity audit (G1):** প্রতিটা run-এর agent-লেখা result file আর আমাদের নিজের parse করা JUnit/pytest report মেলানো; script-এ `|| true` / `|| exit 0` / skip flag গণনা। **Gap:** কত শতাংশ "সফল" run আসলে আংশিক বা ভুয়া ফল দেয় — CG12-এর setup-স্তরের প্রথম পরিমাপ।
4. **Downstream assurance মান (G12):** এই environment দিয়ে কিছু published agent patch-এ regression signal চালানো, PatchDiff-ধাঁচে পুরো suite-এ "resolved but regressing" হার।

**আমার হিসাব (খরচ ও সময়, rough):**
- Idea 1: 15 project × 3 run = 45 run। Paper-এর GPT-4o-mini-স্তরের খরচে $45 \times 0.16 = 7.2$ USD। Frontier-স্তরে, Terminal-Bench-এর per-task খরচকে proxy ধরলে $45 \times 1.72 \approx 77$ USD (GPT-6.1 Sol) থেকে $45 \times 13.20 = 594$ USD (Opus 5.5)। **এই proxy অনিশ্চিত** — কাজ ভিন্ন; তাই আগে 3টা project-এ token log করে আসল খরচ মেপে নিতে হবে।
- সময়: $45 \times 74 = 3{,}330$ মিনিট ≈ 55.5 ঘণ্টা compute; 5টা একসাথে চালালে ≈ 11 ঘণ্টা wall-clock (paper-এর মতো শক্তিশালী machine ধরে; ছাত্রের laptop-এ একসাথে 1–2টা বাস্তবসম্মত, তখন ≈ 28–56 ঘণ্টা)।
- Idea 2: 15 task × 1 run, একই হিসাবে $15 \times 0.16 = 2.4$ USD (সস্তা model) — সবচেয়ে কম খরচে সবচেয়ে বেশি নতুন তথ্য।
- **Cost-aware নিয়ম:** সফল Dockerfile cache করে পুনর্ব্যবহার (তখন LLM খরচ শূন্য); ব্যর্থ project-এ (paper-এ গড় 0.34, সফলের 3.4 গুণ) budget আগেই কমিয়ে দেখা কতটা সফলতা হারায়।

### ২১.৫ Supervisor-এর সম্ভাব্য প্রশ্ন (2026 প্রসঙ্গে)

**Q1. 2026-এর model দিয়ে তো এই কাজ অনেক সহজ হয়ে গেছে — paper কি এখনো প্রাসঙ্গিক?**
A: হয়তো সহজ হয়েছে, কিন্তু **কেউ মাপেনি** — fact sheet-এ বর্তমান model দিয়ে environment setup বা ExecutionAgent-এর dataset-এ কোনো সংখ্যা নেই। সবচেয়ে কাছের benchmark Terminal-Bench 4.0-এ সেরা model-ও প্রায় 59–65% (independent)। আর paper-এর মূল design প্রশ্ন — result বিশ্বাসযোগ্য কিনা — 2026-এর verifier gaming প্রমাণের পর আরও গুরুত্বপূর্ণ।

**Q2. Frontier model ব্যবহার করলে খরচ কত হবে?**
A: সরাসরি জানা নেই, কারণ paper token সংখ্যা দেয়নি। Proxy হিসেবে Terminal-Bench 4.0-এ প্রতি task USD 1.72 (GPT-6.1 Sol) থেকে USD 13.20 (Opus 5.5) (Vals.ai, independent) — paper-এর 0.16-এর প্রায় 11–83 গুণ। তাই আমি সস্তা model দিয়ে শুরু করবো, প্রথম কয়েকটা run-এ token মেপে বাজেট ঠিক করবো।

**Q3. Agent যদি test result বানিয়ে লেখে, ধরবে কীভাবে?**
A: Agent-এর লেখা result file বিশ্বাস করবো না; framework-এর নিজস্ব XML/JSON report আমাদের runner parse করবে, test file-এর hash patch-এর আগে-পরে মেলাবে, script-এ `|| true` বা skip flag খুঁজবে। 2026-এর প্রমাণ (GLM-5.2-এর 78.80 থেকে 57.32, DeepSeek-এর ক্ষেত্রে প্রায় অপরিবর্তিত) দেখায় leakage বন্ধ করলে কিছু model-এর score অনেক নামে — তাই এটা অপরিহার্য।

**Q4. এই paper তোমার assurance report-এ ঠিক কোথায় বসে?**
A: Dynamic signal-এর নিচের স্তরে। Static judge (RePaCA-ধাঁচের) environment ছাড়াই চলে; কিন্তু regression test (Agentless-এর ধাপ) আর generated test চালাতে environment লাগে। SWE-bench/SWE-rebench task-এ প্রস্তুত image ব্যবহার করবো, বাইরের repository-তে ExecutionAgent-ধাঁচের builder — integrity check, per-test output আর version সহ।
