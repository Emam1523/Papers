# Paper Analysis 03 (PatchVal): Harden and Catch — Just-in-Time Assured LLM-Based Software Testing

> Sub-domain: Patch Validation
> PDF: Patch Validation/Harden and Catch for Just-in-Time Assured LLM-Based SoftwareTesting.pdf

## ০. Bibliographic info

| Field | তথ্য |
|---|---|
| Title | Harden and Catch for Just-in-Time Assured LLM-Based Software Testing: Open Research Challenges |
| Authors | Mark Harman (Meta Product Compliance and Privacy; UCL), Peter O'Hearn (Meta FAIR; UCL), Shubho Sengupta (Independent Software and AI Consultant, USA) |
| Venue / year | 33rd ACM International Conference on the Foundations of Software Engineering (FSE Companion '25), June 23–28, 2025, Trondheim, Norway |
| Paper type | Position / challenges paper, FSE 2025 keynote-এর সঙ্গে লেখা (paper-এর নিজের কথায়: "written to accompany the keynote") |
| Length | 17 pages, 86 references, author order alphabetical |
| DOI | 10.1145/3696630.3734199 |
| Contribution type | Formal definitions (Definition 1–15), 8-category test taxonomy (Figure 1), case tables (Table 1–3), 4 explicit Research Challenges |
| Experiments | নেই। Meta-র deployment (ACH) নিয়ে শুধু গুণগত বর্ণনা (Section 2.5); কোনো সংখ্যাগত ফলাফল এই paper-এ নেই |
| Code / data | নেই |

## ১. TL;DR

**এক বাক্যে:** Paper বলে প্রচলিত test generation আসলে শুধু hardening test (ভবিষ্যৎ regression ঠেকানো) বানায়, তাই সে "Regression Only Trap"-এ আটকে থাকে। আসল বড় চ্যালেঞ্জ হলো pull request জমা পড়ার মুহূর্তে "catching" test বানানো, যা ওই PR-এর bug ধরে (Catching JiTTest Challenge)।

- **Hardening test** = current revision-এ pass করে, কিন্তু ভবিষ্যতের কোনো buggy revision-এ (oracle অনুযায়ী) fail করতে পারে।
- **Catching test** = current revision-এ fail করে। Strong হলে oracle-ও বলে এটা সত্যিই fail হওয়া উচিত।
- Weak/strong ভাগ থেকে ৮টি test category তৈরি হয়: ৫টি বিভ্রান্তিকর signal, ৩টি নির্ভরযোগ্য signal।
- Precision এবং recall আলাদা বা F1 হিসেবে না মেপে **R@P=α** (precision অন্তত α রেখে সর্বোচ্চ recall) মাপার প্রস্তাব; উদাহরণে α = 0.8।
- Oracle-কে "জানা বা অজানা" না ভেবে "খরচ করার মতো ক্রমিক resource" ভাবতে বলে; PR-এর non-executable text (title, comment) থেকে oracle "scavenge" করার ধারণা দেয়।

**Supervisor-কে ৩০ সেকেন্ডে:**

- এটা experiment-paper নয়; এটা একটা **শব্দভান্ডার ও সমস্যা-ম্যাপ**। আমাদের assurance report-এর dynamic signal-গুলোকে (patch-targeted test, oracle strength, distinguishing test) নির্দিষ্টভাবে সংজ্ঞায়িত করতে এই definition কাজে লাগবে।
- সবচেয়ে কাজের জিনিস: Definition 5–15 এবং Figure 1-এর ৮ region। কোনো generated test pass করলে সেটা strong না weak, এবং কোন region-এ পড়ে, এই প্রশ্নটাই CG13 (oracle strength)-এর formal রূপ।
- আমাদের "patch" = paper-এর "child revision", আর patch-এর আগের repo = "parent"। Agent patch-এর জন্য test generate করা মানেই JiTTest generate করা।
- সংখ্যা কম: 0.8 (precision), 1.75 ঘণ্টা (median first-review), 8 ঘণ্টা (industry aspiration), ছয়টি ACH assurance, ৮ region, ৪ Research Challenge।
- দুর্বলতা: কোনো empirical validation নেই; "initial results" abstract-এ বলা হলেও সংখ্যা দেওয়া হয়নি।

## ২. Background (এই প্রজেক্টের জন্য নতুন ধারণা)

- **Regression oracle:** আগের version-এর behaviour-কেই ground truth ধরা। সুবিধা: সহজে automate হয়। অসুবিধা: নতুন bug বা পুরোনো bug ধরা যায় না।
- **Implicit oracle:** "যা কোনো system-এর কখনো করা উচিত নয়" (crash, memory violation, out-of-memory)। Fuzzer ও Sapienz এটা ব্যবহার করে; শুধু অতি স্পষ্ট bug ধরে।
- **Oracle problem:** একটা test pass/fail হওয়া উচিত কি না, সেটা কে ঠিক করবে। Paper বলে একক ground-truth oracle ধরে নেওয়া অযৌক্তিক (DeMillo, Lipton, Perlis 1979), কারণ software engineering একটি সামাজিক প্রক্রিয়া।
- **Mutation testing / mutant killing:** কোড-এ ইচ্ছাকৃত ছোট bug (mutant) ঢুকিয়ে দেখা কোন test সেটা ধরে। এখানে mutant = ভবিষ্যতের সম্ভাব্য buggy revision-এর প্রতিনিধি।
- **Assured LLMSE / Assured LLMST:** LLM যা বানায় তা verifiable assurance সহ দেওয়া (generate-and-test); testing-এ প্রয়োগকে Assured LLMST বলে।
- **Pseudo false positive:** Engineer যদি একটি "সঠিক" signal-ও reject করে, সেটাও friction, তাই false positive-এর মতো গোনা হয়।
- **Failed error propagation:** Bug execute হয়, state দূষিত হয়, কিন্তু output পর্যন্ত পৌঁছায় না। ভবিষ্যৎ PR এই পথ খুলে দিলে হঠাৎ failure দেখা দেয় (paper-এর ভাষায় "unexploded bomb")।
- **Flaky test:** একই কোডে কখনো pass কখনো fail। "Valid regression test" হতে হলে consistently pass করতে হয়।
- **Parsimonious pull request:** এত কম বর্ণনার PR (যেমন title: "add location details to lookup query", summary: TSIA, Test Plan: YOLO) যেখান থেকে oracle-এর তথ্য প্রায় বের করা যায় না।

## ৩. Problem

- প্রায় সব automated test generation (EvoSuite, Klee, CUTE, DART, Austin, TestGen-LLM, CoverUp, HITS, ACH ইত্যাদি) **hardening** test বানায়: current version-এ pass করে, ভবিষ্যৎ পরিবর্তন ঠেকায়।
- এর কারণ oracle problem: regression oracle সহজ, তাই সবাই সেটা বেছে নেয়। ফল **Regression Only Trap (ROT)**: test-কে current revision-এ pass করতে হয়, তাই সে ওই revision-এর নতুন bug বা দীর্ঘদিনের legacy bug ধরতে পারে না।
- Coverage বাড়ানো test ও কার্যত অর্থহীন হতে পারে: যে test-এর assertion সমার্থকভাবে Assert(True), সে নির্মাণগতভাবেই কোনো bug ধরবে না, অথচ coverage বাড়ায় (coverage dilemma)।
- আসল অমীমাংসিত সমস্যা: PR জমা পড়ার মুহূর্তে এমন test বানানো যা ওই PR-এর bug ধরে, কিন্তু সঠিক PR-এ false alarm দেয় না। এখানে oracle-এর একমাত্র উৎস প্রায়ই PR নিজে, যা খুব সংক্ষিপ্ত।
- Deployment প্রশ্নও অমীমাংসিত: কোন outcome-এ test land হবে, কোনটায় শুধু signal যাবে, কোনটা discard হবে।

## ৪. Goal ও Research Questions

**Goal:** hardening/catching ধারণাগুলো formal করা, test outcome-এর case-by-case বিশ্লেষণে deployment নীতি বের করা, এবং open research challenge চিহ্নিত করা।

Paper-এর চারটি Research Challenge (প্রতিটি paper-এ স্পষ্ট নম্বরসহ):

| RC | প্রশ্ন (paper অনুযায়ী) | Section |
|---|---|---|
| RC1 | Test-কে ৮ category-তে ভুল শ্রেণিবিন্যাসের ঝুঁকি কমানোর কৌশল খোঁজা | ৪ |
| RC2 | Weak hardening থেকে strong hardening স্বয়ংক্রিয়ভাবে আলাদা করা (partial oracle ব্যবহার করে human oracle effort কমানো) | ৫.১ |
| RC3 | Regression catching এবং false positive স্বয়ংক্রিয়ভাবে আলাদা করা (strictly weak catching-এর ঝুঁকি কমানো) | ৫.১ |
| RC4 | **Catching JiTTest Challenge:** buggy PR ও তার parent দেওয়া থাকলে এমন test বানানো যা PR-এর bug ধরে, non-buggy PR-এ false positive-এর ঝুঁকি কম রেখে। মান = JiTTest-এর R@P=α, যেমন α = 0.8 | ৬ |

Paper-এর RQ-ধরনের অন্তর্নিহিত প্রশ্ন: (ক) কখন একটি test-signal engineer-কে দেখানো নিরাপদ, (খ) parsimonious PR থেকেও কি fake catch বাদ দেওয়ার মতো oracle তথ্য মেলে।

## ৫. Methodology (ধাপে ধাপে)

Paper-এর "পদ্ধতি" হলো একটি **বিশ্লেষণ-কাঠামো**, কোনো algorithm নয়। ধাপগুলো:

1. **Fundamentals ঠিক করা (Definition 2):** একটি tree repository যেখানে revision r-এর Parent(r) আছে; test case-এর সেট; predicate Builds, Passes, Fails। ধরে নেওয়া হয় test গুলো পরস্পর স্বাধীনভাবে চলে (নির্ভরতা শিথিল করা যায়, কিন্তু আলোচনা জটিল হয়)। Footnote 2: timeout ইত্যাদি অন্য outcome বাদ রাখা হয়েছে।
2. **Timeliness (Definition 3, 4):** Timely test = revision r প্রথম pull request হিসেবে জমা পড়ার সময় বা আগে test উপস্থিত। JiTTest = r-এর জন্য timely কিন্তু Parent(r)-এর জন্য timely নয়।
3. **Oracle (Definition 5):** Partial oracle যথেষ্ট; প্রশ্ন একটাই: "revision r-এ test t-এর pass না fail হওয়া উচিত?" Practical সরলীকরণ: PR author-ই সিদ্ধান্তদাতা।
4. **Hardening (Definition 6–9):** weak, strong, perfect precision, perfect recall।
5. **Catching (Definition 10–15):** weak/strong catching, তারপর regression catching বনাম functionality catching।
6. **৮ category (Figure 1):** parent-এ hardening অবস্থা (নেই / strictly weak / strong) × child-এ catching অবস্থা (নেই / strictly weak / strong) ভেদে।
7. **Case tables (Table 1–3):** Table 1 timely hardening test-এর ১০ সারি; Table 2 JiTTest-এর ২৪ সারি (৫ category); Table 3 oracle-জ্ঞান ছাড়া প্রস্তাবিত ৮টি deployment সিদ্ধান্ত।
8. **Oracle scavenging:** LLM দিয়ে code ও natural language (comment, PR title, CI history) একসঙ্গে পড়ে oracle সংকেত বের করা (Section 6.2–6.4)।
9. **Latent bug অনুসন্ধান (Section 6.5):** কোডের একটি অংশ delete করে নতুন PR হিসেবে re-insert করলে JiTTest দিয়ে latent bug পাওয়া যায়; বারবার করে পুরো code base হাঁটা যায়।

**Meta-র deployment-এর যা বলা আছে (Section 2):**

- Sapienz: ২০১৭ থেকে client-side end-to-end test; Fausta: ২০২১ থেকে WhatsApp server-side।
- Unit-level: TestGen-LLM (FSE 2024), ACH (mutation-guided, FSE 2025, arXiv 2501.12862)।
- ACH ছয়টি assurance দেয়: (১) Buildable, (২) Valid Regression Test (pass ও non-flaky), (৩) Hardening (এমন fault ধরে যা অন্য কোনো existing test ধরে না), (৪) Additional Coverage, (৫) Relevant, (৬) Fashion Following। প্রথম চারটি verifiable/falsifiable; শেষ দুটি আকাঙ্ক্ষামূলক।
- ACH-এ mutant নিশ্চিতভাবে killed হয়, তাই equivalent mutant সমস্যা এড়ানো যায়।
- Engineer-এর রায়: irrelevant মনে হওয়া test-ও coverage বাড়ালে বেশি গ্রহণযোগ্য ছিল (গুণগত পর্যবেক্ষণ; সংখ্যা [5, 29]-এ, এই paper-এ নেই)।

**Timing যুক্তি (Section 2.4):**

- Real time-এর utility-ভিত্তিক সংজ্ঞা (Definition 1, [8] থেকে): consumer অপেক্ষার সময় কমলেও আরও ভালো করতে পারে না।
- PR-এর প্রথম মানব-response-এর median সময় 1.75 ঘণ্টা (study [42]; এতে instant bot ধরা, তাই কম ধরা হয়ে থাকতে পারে); industry aspiration প্রায় 8 ঘণ্টা ([62])।
- তাই JiTTest-এ প্রায় 8 ঘণ্টা static ও dynamic analysis-এর সুযোগ আছে।

## ৬. Math (formalism)

নোটেশন: r = revision, Parent(r) = তার parent, t = test, P = Parent(r)। Paper-এর PDF-এর symbol কিছু জায়গায় extraction-এ ভেঙে গেছে; নিচের রূপ paper-এর ইংরেজি বর্ণনা অনুযায়ী আমার পুনর্লিখন।

**৬.১ Oracle ও signal-এর ধরন (Definition 5).** Oracle_r(t) ∈ {pass, fail}। চার ধরনের ফল:

- True positive: Fails_r(t) এবং Oracle_r(t) = fail।
- False positive: Fails_r(t) এবং Oracle_r(t) = pass।
- True negative: Passes_r(t) এবং Oracle_r(t) = pass।
- False negative: Passes_r(t) এবং Oracle_r(t) = fail।

**৬.২ Weak ও strong hardening (Definition 6, 7).**

$$
\mathrm{Hardening}_r(t) \iff \mathrm{Passes}_r(t) \land \exists r'.\ \big(\mathrm{Parent}(r') = r \land \mathrm{Fails}_{r'}(t) \land \mathrm{Oracle}_{r'}(t) = \text{fail}\big)
$$

$$
\mathrm{SHardening}_r(t) \iff \mathrm{Hardening}_r(t) \land \mathrm{Oracle}_r(t) = \text{pass}
$$

- r' = r-এর কোনো সম্ভাব্য ভবিষ্যৎ child (mutant-এর মতো)। Weak hardening মানে "অন্তত একটি buggy child-এ ঠিকভাবে fail করবে"।
- Strong হলে এর সঙ্গে current revision-এও pass করা সঠিক (true negative)।
- "Strictly weak hardening" = weak কিন্তু strong নয় (যেমন current-এ ভুলভাবে pass করছে)।

**৬.৩ Precision/recall-ভিত্তিক hardening (Definition 8, 9).**

$$
\mathrm{PPHardening}_r(t) \iff \mathrm{Hardening}_r(t) \land \forall r'.\ \big(\mathrm{Fails}_{r'}(t) \to \mathrm{Oracle}_{r'}(t) = \text{fail}\big)
$$

$$
\mathrm{PRHardening}_r(t) \iff \mathrm{Hardening}_r(t) \land \forall r'.\ \big(\mathrm{Oracle}_{r'}(t) = \text{fail} \to \mathrm{Fails}_{r'}(t)\big)
$$

- দুটি মিলিয়ে perfect precision and recall: প্রতিটি সম্ভাব্য ভবিষ্যৎ revision-এ test fail করে **ঠিক তখনই** যখন revision buggy।
- Paper বলে perfect precision অর্জনযোগ্য নয় (প্রশ্নগুলো মূলত undecidable) এবং exhaustive testing অসম্ভব বলে perfect recall-ও নয়।

**৬.৪ Catching (Definition 10, 11).**

$$
\mathrm{Catching}_r(t) \iff \mathrm{Fails}_r(t)
$$

$$
\mathrm{SCatching}_r(t) \iff \mathrm{Fails}_r(t) \land \mathrm{Oracle}_r(t) = \text{fail}
$$

**৬.৫ Regression catching (Definition 12, 13).** Catching এবং parent-এর জন্য hardening, দুটিই। Strong রূপ paper নিজে সরল করেছে:

$$
\mathrm{SRCatching}_r(t) \iff \mathrm{Passes}_{P}(t) \land \mathrm{Fails}_r(t) \land \mathrm{Oracle}_r(t) = \text{fail}
$$

ব্যাখ্যা: parent P-তে pass করছে এবং r-এ সঠিকভাবে fail করছে। (Hardening_P-এর ∃-শর্ত এখানে r নিজেই সাক্ষী হিসেবে সন্তুষ্ট করে দেয়, তাই বাদ গেছে।)

**৬.৬ Functionality catching (Definition 14, 15).** Catching কিন্তু parent-এ hardening নয়: test হয় parent-এ build হয় না (নতুন method), অথবা build হয় কিন্তু parent-এ fail করে।

$$
\mathrm{SFCatching}_r(t) \iff \big(\neg \mathrm{Builds}_{P}(t) \lor \mathrm{Fails}_{P}(t)\big) \land \mathrm{Fails}_r(t) \land \mathrm{Oracle}_r(t) = \text{fail}
$$

Weak রূপে শেষ শর্ত বদলে "∃ সহোদর revision r'' (Parent(r'') = P) যেখানে t সঠিকভাবে fail করে" বসে; এটাই সংজ্ঞার অস্বস্তিকর অতিরিক্ত শর্ত যা paper নিজেও উল্লেখ করেছে।

**৬.৭ Just-in-Time test (Definition 3, 4).**

$$
\mathrm{JiT}_r(t) \iff \mathrm{Timely}_r(t) \land \neg \mathrm{Timely}_{P}(t)
$$

**৬.৮ Real time (Definition 1).** ফল U-তে consumer-এর utility হলে, অপেক্ষার সময় d কমলে U আর বাড়ে না, তখন ফল "real time"।

**৬.৯ Precision, recall এবং R@P=α (Section 3.4, 3.5).** মান বোঝানোর জন্য আমার প্রতীকায়ন:

$$
P = \frac{TP}{TP + FP}, \qquad R = \frac{TP}{TP + FN}
$$

$$
R@P{=}\alpha \;=\; \max\{\, R(\tau) \;:\; P(\tau) \geq \alpha \,\}
$$

- τ = test-এর signal দেখানোর কোনো সিদ্ধান্ত-সীমা (threshold) বা নীতি; α = ন্যূনতম precision।
- P ≥ α হলে false positive ও true positive-এর অনুপাত:

$$
\frac{FP}{TP} \leq \frac{1-\alpha}{\alpha}
$$

- F1 = 2PR/(P+R) নিষিদ্ধ করা হয়নি, তবে paper বলে F1 precision ও recall-কে বিনিময়যোগ্য পণ্য ধরে নেয়, যা industry deployment-এ ঠিক নয়।
- Recall সরাসরি মাপা যায় না; অনুমান করা হয় mutation testing (fault space sampling) বা production-এ leak-through (false negative-এর নিম্নসীমা) দিয়ে।

**৬.১০ Worked example (paper-এর প্রকৃত সংখ্যা ও উদাহরণ, হিসাব আমার)।**

**(ক) Paper-এর Product উদাহরণ (Example 1, 2, 5).** Revision r-এর Product() constructor-এ bug আছে: supplier location None হয়ে যেতে পারে।

1. Example 1: assertTrue(not locs)। Python-এ not None = True, তাই bug থাকা সত্ত্বেও pass করে। Oracle_r = fail, কিন্তু Passes_r, তাই এটা false negative, strictly weak hardening (Figure 1-এর Region 1)।
2. Example 2: assertTrue(locs is not None and len(locs) == 0)। এটা bug থাকলে correctly fail করে; bug না থাকলে correctly pass করে। তাই strong hardening।
3. পরের PR (Example 5) constructor-এ None বসিয়ে দিলে Example 2 fail করে, Oracle = fail, parent-এ pass করত; অতএব Strong Regression Catching (Region 6)। Example 1 ওই PR-এ pass করে, কিছুই ধরে না।

**(খ) Precision threshold α = 0.8 (paper-এর সংখ্যা).** FP/TP ≤ (1 − 0.8)/0.8 = 0.25, অর্থাৎ ১:৪। (আমার হিসাব)। মানে প্রতি ৪টি সত্যিকারের catch-এর বিপরীতে সর্বোচ্চ ১টি false alarm। Paper বলে engineer ২০% সময় friction সহ্য করবে যদি বাকি ৮০% সত্যিকার catch হয়।

**(গ) কাল্পনিক R@P (আমার হিসাব, paper-এর তথ্য নয়).** ধরি কোনো JiTTest generator ১০টি signal দেখাল: ৮টি true positive, ২টি false positive। P = 8/10 = 0.8, α = 0.8 পূরণ হয়। ১০০টি injected mutant-এর মধ্যে ৮টি ধরা পড়লে recall অনুমান R = 8/100 = 0.08, অতএব এই generator-এর R@P=0.8 ≈ 0.08। এই সংখ্যা সম্পূর্ণ উদাহরণ; উদ্দেশ্য দেখানো যে precision শর্ত পূরণ হলেও recall-এর আলাদা মান থাকে।

**(ঘ) Timing (আমার হিসাব).** 8 ঘণ্টা / 1.75 ঘণ্টা ≈ 4.57। অর্থাৎ industry-aspiration বাজেট median first-review সময়ের প্রায় ৪.৬ গুণ। Median বলে 1.75 ঘণ্টার মধ্যে test এলে অন্তত 0.5 সম্ভাবনায় "in time" (paper-এর কথা)।

**(ঙ) ৮ region = ৩ × ৩ − ১ (আমার পর্যবেক্ষণ).** Parent-এ {নেই, strictly weak hardening, strong hardening} × child-এ {নেই, strictly weak catching, strong catching} = ৯টি সংমিশ্রণ, যার মধ্যে "দুটিই নেই" (test অকেজো) বাদ গেছে; বাকি ৮টি। Paper-এ ৫টি বিভ্রান্তিকর (Region 1, 3, 4, 5, 7), ৩টি সত্য-signal (Region 2, 6, 8)।

## ৭. Setup (paper-এর "বিশ্লেষণ setup")

| বিষয় | বিবরণ |
|---|---|
| ধরণ | Conceptual / formal বিশ্লেষণ; কোনো dataset, model, benchmark নেই |
| Illustrative system | কাল্পনিক product database application (Product object, supplier location তালিকা, distance method) |
| Test language | Python-ধাঁচের pseudo-code উদাহরণ (Example 1–6) |
| Meta deployment | Sapienz (২০১৭), Fausta (২০২১), TestGen-LLM, ACH; Section 2.5-এ কেবল গুণগত বর্ণনা |
| LLM | কোনো নির্দিষ্ট model-এর নাম বা সংস্করণ উল্লেখ নেই |
| Independence assumption | Test গুলো স্বাধীনভাবে চলে (সরলীকরণ) |
| Oracle assumption | PR author-ই oracle-এ সম্মত সিদ্ধান্তদাতা |
| Time budget | CI-তে প্রায় 8 ঘণ্টা; median first review 1.75 ঘণ্টা |
| Metric প্রস্তাব | R@P=α, α = 0.8 (conservative পছন্দ) |
| Statistics | নেই |

## ৮. Results (কাঠামোগত ফলাফল; সংখ্যাগত experiment নেই)

**৮.১ আনুষ্ঠানিক ফলাফল ও সংখ্যা**

| বিষয় | মান | উৎস |
|---|---|---|
| Median first human response to a PR | 1.75 ঘণ্টা (bot সহ, তাই underestimate হতে পারে) | Section 2.4, [42] |
| Industry aspiration | প্রায় 8 ঘণ্টা | Section 2.4, [62] |
| Precision threshold উদাহরণ | α = 0.8, FP:TP ≤ 1:4 | Section 3.5 |
| ACH assurance সংখ্যা | ৬ (৪টি strict, ২টি aspirational) | Section 2.5 |
| Test category | ৮ (৫ বিভ্রান্তিকর + ৩ নির্ভরযোগ্য) | Section 4, Figure 1 |
| Engineer review-এ বাদ পড়া সমস্যাজনক category | ৩ / ৫ (Region 1, 3, 5) | Section 5.1 |
| Research Challenge | ৪ | Section 4, 5.1, 6 |
| Table 1 / 2 / 3 সারি | ১০ / ২৪ / ৮ (আমার গণনা) | Table 1–3 |

**৮.২ Table 1 (timely hardening test; PDF-এর column ভেঙে গিয়েছিল, নিচে আমার পুনর্গঠন)**

| Child-এ outcome | Oracle (parent, child) | Type | Region (parent → child) | ফল |
|---|---|---|---|---|
| pass | pass, pass | true negative | 2 → 2 | Strong hardening pass করল: সব ঠিক |
| pass | fail, pass | true negative | 1 → 2 | Strictly weak hardening pass: child একটি অধরা bug সারিয়েছে |
| fail | pass, fail | true positive | 6 | True regression catch |
| fail | fail, fail | true positive | 5 | আপাত regression; সম্ভবত failed error propagation |
| pass | fail, fail | false negative | 1 → 1 | Strictly weak hardening bug মিস করে যাচ্ছে |
| pass | pass, fail | false negative | 2 → 1 | Strong hardening child-এর আনা bug মিস করল |
| fail | pass, pass | false positive | 4 | Strong hardening ভুলভাবে child আটকাল |
| fail | fail, pass | false positive | 3 | Strictly weak hardening একটি fix-কে নতুন failure দেখাল |
| no build | pass, – | – | 2 | Strong hardening retire: child tested functionality সরিয়েছে |
| no build | fail, – | – | 1 | Strictly weak hardening retire: test আগে থেকেই দুর্বল ছিল |

**৮.৩ Table 2 (JiTTest, ২৪ সারি, ৫ category) — সারসংক্ষেপ**

| Category | শর্ত (parent / child) | সারি | Paper-এর সিদ্ধান্ত |
|---|---|---|---|
| 1 Parent Hardening | parent-এ pass | 8 | Table 1-এর সঙ্গে isomorphic, কিন্তু false positive-এর ক্ষতি বেশি (সম্ভবত এটাই একমাত্র test) |
| 2 Child Hardening | parent-এ fail, child-এ pass | 4 | তুলনামূলক নিরাপদ; fix বা উন্নতির প্রমাণও হতে পারে |
| 3 New Functionality | parent-এ build হয় না | 4 | child-এ pass করলে land করা নিরাপদ; fail করলে নতুন functionality-র bug-এর ইঙ্গিত |
| 4 Cannot Land | child-এ build হয় না | 4 | land করা যাবে না, কিন্তু signal engineer-কে দেওয়া ভালো |
| 5 Likely Discard | দুই জায়গাতেই fail | 4 | সাধারণত discard (সবচেয়ে অনিশ্চিত সিদ্ধান্ত) |

**৮.৪ Table 3 (oracle জানা না থাকলে প্রস্তাবিত ৮টি সিদ্ধান্ত)**

| Parent / child outcome | সিদ্ধান্ত | সম্ভাব্য খারাপ ফল | সম্ভাব্য সেরা ফল |
|---|---|---|---|
| pass / pass | Land Test | দীর্ঘদিনের সমস্যা baked in হয় | ভবিষ্যৎ regression ধরে |
| pass / fail | Report Fail | false positive; অন্য test pass করতে পারে | বর্তমান regression ধরে |
| fail / pass | Land Test | নতুন সৃষ্ট সমস্যা baked in | নতুন functionality-র ভবিষ্যৎ regression ধরে |
| no build / pass | Land Test | নতুন সৃষ্ট সমস্যা baked in | নতুন functionality-র ভবিষ্যৎ regression ধরে |
| no build / fail | Report Fail | false positive; অন্য test pass করতে পারে | নতুন functionality-র bug ধরে |
| pass / no build | Give Signal | ভুলভাবে বলে parent ঠিক ছিল | নিশ্চিত করে behaviour সরানো হয়েছে |
| fail / no build | Give Signal | ভুলভাবে বলে parent ভুল ছিল | fix নথিভুক্ত করতে সাহায্য করে |
| fail / fail | Discard Test | বর্তমান revision-এর bug-catch হারায় | বিভ্রান্তিকর test হারায় |

**৮.৫ Actionable conclusions (paper-এর নিজের)**

- Engineer review (সেকেন্ডের কাজ) করালে ৫টির মধ্যে ৩টি সমস্যাজনক category (Region 1, 3, 5) দূর হয়: "A relatively small amount of timely oracle information can dramatically enhance test effectiveness."
- সব passing, non-flaky, review-গ্রাহ্য test land করা নিরাপদ; ঝুঁকিগুলো মানুষের লেখা test-এর ঝুঁকিরই উদাহরণ।
- Generated test সবসময় **parent-এও** চালাও (extra signal): বর্তমান tool-গুলো সাধারণত চালায় না।
- Failing JiTTest signal সরাসরি engineer-কে না দিয়ে "আরও বিশ্লেষণের trigger" হিসেবে ব্যবহার করা যায়।
- Auto-landing শুধু disposable test-এ নিরাপদ (যেমন meaning-preserving refactoring-এর পরে বদলানো behaviour ধরার test, যা পরে ফেলে দেওয়া হয়)।

**৮.৬ Section 6-এর oracle scavenging উদাহরণ (গুণগত)**

- Fake regression catching: PR title "add location details to lookup query"; hardening test assert করে location column NULL; অথচ PR ঠিক এই আচরণ বদলাতে চায়। শুধু ছয় শব্দের title থেকেই test discard করা যায়।
- Fake functionality catching: comment বলে "destination location cannot be the same as the current location"; test divide-by-zero পায় কারণ দুই location এক। Comment-এর এই assumption test লঙ্ঘন করছে, তাই failure false positive। ভালো উত্তর: signal দমন না করে মন্তব্য হিসেবে জানানো, বা test-কে divide-by-zero exception assert করা passing test-এ রূপান্তর, বা repair প্রস্তাব।

## ৯. Key findings

1. Hardening আর catching আলাদা সংজ্ঞাযোগ্য ধারণা; একই test সময়ের সঙ্গে hardening থেকে catching হয়ে যেতে পারে (Example 6: bug সারানোর পর functionality catching test strong hardening হয়ে যায়)।
2. Regression Only Trap: current revision-এ pass করতে বাধ্য test নতুন bug বা legacy bug ধরতে পারে না।
3. Strict weak (current-এ ভুলভাবে pass করা) test "মিথ্যা নিরাপত্তাবোধ" তৈরি করে এবং ভবিষ্যৎ buggy revision-এও একই দুর্বলতা বহন করে।
4. ৮ category-র মধ্যে ৫টি বিভ্রান্তিকর signal দেয়; শুধু ৩টি নির্ভরযোগ্য।
5. মানুষের সংক্ষিপ্ত oracle পরীক্ষা (test current-এ pass করা সঠিক কি না) ৩/৫ problematic category বাদ দেয়।
6. JiTTest-এ false positive-এর খরচ hardening test-এর চেয়ে বেশি, কারণ নতুন test প্রায়ই একমাত্র signal।
7. Parent-এ test চালালে বাড়তি signal মেলে (fail→pass = fix; no-build = নতুন functionality)।
8. Parsimonious PR-ও যথেষ্ট oracle ইঙ্গিত দিতে পারে (title, comment, CI history), আর LLM code ও natural language একসঙ্গে পড়ে সেই সেতু হতে পারে।
9. Catching JiTTest দিয়ে delete-and-reinsert কৌশলে legacy code-এর latent bug-ও খোঁজা সম্ভব।

## ১০. Alternatives-এর চেয়ে কেন ভালো

- **Coverage-ভিত্তিক generator (EvoSuite, Klee, CoverUp ধরনের):** coverage কার্যকরভাবে fault-revealing নয়; paper hardening-কে "অন্তত একটি bug ধরে" দিয়ে সংজ্ঞায়িত করে।
- **Fuzzer ও end-to-end (AFL, Sapienz, Fausta):** implicit oracle-এ আটকা, নতুন functionality-র বিশেষ ভুল ধরে না; JiTTest ধারণা PR-নির্দিষ্ট oracle খোঁজে।
- **F1 ধরনের মেট্রিক:** precision-recall বিনিময়যোগ্য ধরে নেয়; R@P=α deployment-বাস্তবতার সঙ্গে মেলে।
- **"Oracle জানা/অজানা" দ্বিমুখী ভাবনা:** oracle-কে ক্রমিক ও ব্যয়বহুল resource হিসেবে দেখার ফলে human review-এর সুনির্দিষ্ট মূল্য ও সুফল হিসাব করা যায়।
- **শুধু code summarisation:** circularity-র ঝুঁকি (LLM দিয়ে summary, আবার LLM দিয়েই test)। Paper মানুষের লেখা non-executable text-কে অগ্রাধিকার দেয়।
- সীমা: এগুলো "ভালো" এই দাবির empirical প্রমাণ paper-এ নেই; এগুলো সংজ্ঞাগত ও যুক্তিগত সুবিধা।

## ১১. কখন কাজ করে / ব্যর্থ হয়

| অবস্থা | Paper-অনুযায়ী ফল |
|---|---|
| Engineer review আছে, test non-flaky | Strictly weak hardening-এর ঝুঁকি কমে (Region 1, 3, 5 দূর) |
| PR-এ যথেষ্ট comment/description | Oracle scavenging সম্ভব, fake catch বাদ দেওয়া যায় |
| Parsimonious PR (TSIA/YOLO) | শুধু title ও কোড; সবচেয়ে কঠিন, তবু কিছু ক্ষেত্রে (title-এর ছয় শব্দেই) discard সম্ভব |
| Test গুলো পরস্পর নির্ভরশীল | Paper-এর independence assumption ভাঙে; বিশ্লেষণ জটিল |
| Oracle নিয়ে engineer-রা দ্বিমত | Single ground-truth ধরে নেওয়া অকার্যকর; PR author-কে সিদ্ধান্তদাতা ধরা হয় |
| Test parent ও child দুটিতেই fail | সাধারণত discard; paper নিজেই এটাকে "least certain" বলে |
| Latent bug খোঁজা (delete-and-reinsert) | নতুন non-executable text নেই; CI history ও পুরোনো comment ঘাঁটতে হয় |
| Failed error propagation থাকলে | Hardening test হঠাৎ এমন "regression" ধরে যা আসলে পুরোনো bug |

## ১২. Limitations

**লেখকদের স্বীকৃত:**

- Deployment option গুলো unequivocal বা comprehensive নয়।
- Independence assumption সরলীকরণ।
- Oracle ঠিক করার পদ্ধতি ইচ্ছাকৃতভাবে অনির্দিষ্ট রাখা হয়েছে।
- Category 5 (দুই জায়গাতেই fail) সম্পর্কে সিদ্ধান্ত সবচেয়ে অনিশ্চিত।
- Perfect precision ও recall অসম্ভব।

**আমার পর্যবেক্ষণ:**

- Abstract-এ "initial results from our work on automated LLM-based hardening" বলা আছে, কিন্তু Section 2.5-এ কোনো সংখ্যা নেই; সংখ্যা অন্য paper-এ ([5], [29])।
- Catching JiTTest Challenge কেউ সমাধান করে দেখায়নি; "grounds for optimism" শুধু দুটি হাতে-বানানো উদাহরণ।
- R@P=α-এর recall মাপার কৌশল (mutation sample, production leak-through) নিজেই পক্ষপাতদুষ্ট; mutant বাস্তব bug-এর প্রতিনিধি কি না, তার কোনো প্রমাণ এখানে নেই।
- Oracle সব জায়গায় "PR author-এর মত" ধরলে, agent-লেখা patch (যার কোনো human author নেই) ও adversarial বা অসাবধান author-এর ক্ষেত্রে সংজ্ঞা দুর্বল হয়।
- Table 1 ও 2-এর সব সারিই oracle-জ্ঞান ধরে নেয়; বাস্তবে oracle অজানা, আর Table 3-এ সেই অজানার অবস্থায় প্রস্তাব আরও মোটা (৮টি সিদ্ধান্ত)।
- Section 2.3-এর যুক্তি "test যোগ করলে suite কখনো খারাপ হয় না" ধরে নেয় test ব্যয়, flakiness ও maintenance ভার শূন্য; অথচ নিজেই flaky ও friction নিয়ে আলোচনা করে।
- সময় বাজেট (8 ঘণ্টা) একটি industry blog ([62]) থেকে, peer-reviewed নয়; আর 1.75 ঘণ্টা Git প্রকল্পের median, Meta-র নয়।
- Agent-এর patch-এর ক্ষেত্রে gaming ঝুঁকি আলোচিত নয়: Generator যদি ইচ্ছাকৃতভাবে বা নিজের অজান্তে test-কে এমনভাবে বানায় যাতে সবসময় pass করে, তাহলে কী হবে।
- Security বা non-functional bug (performance, concurrency) নিয়ে কিছু নেই।

## ১৩. Research gaps

| G-id | Gap | Evidence | সম্পর্কিত CG / folder |
|---|---|---|---|
| G1 | Weak বনাম strong test স্বয়ংক্রিয়ভাবে আলাদা করার কৌশল নেই (RC2) | Example 1 বনাম 2; Section 5.1 | CG13, CG3 / 04_LLM_Test_Generation |
| G2 | Regression catching বনাম false positive আলাদা করা (RC3) | Table 2, Category 1, Region 4 | CG1, CG14 |
| G3 | ৮ region-এ test-এর ভুল শ্রেণিবিন্যাস কমানো (RC1) | Figure 1 | CG13, CG10 |
| G4 | Catching JiTTest-এর R@P=α মাপার কোনো benchmark বা প্রমাণ নেই (RC4) | Section 6; কোনো experiment নেই | CG6, CG8 |
| G5 | Parsimonious PR থেকে oracle scavenging-এ LLM-circularity | Section 6.1 | CG12, CG7 |
| G6 | Category 5 (parent ও child দুটিতেই fail) এখন discard; ভবিষ্যৎ কৌশল দরকার | Section 5.2 | CG7 (abstention) |
| G7 | Recall অনুমান: mutation sample ও leak-through-এর পক্ষপাত | Section 3.5 | CG10, CG13 |
| G8 | Test-সমূহের নির্ভরশীলতা শিথিল করার বিশ্লেষণ নেই | Definition 2 | CG15 |
| G9 | Oracle সময়ের সঙ্গে বদলায় (regulation, engineer-এর মত); version-bound রায় দরকার | Section 6.4 | CG11 |
| G10 | Agent-লেখা patch-এ "author oracle" কে হবে | Section 3.2 (আমার পর্যবেক্ষণ) | CG1, CG12 |
| G11 | Friction/pseudo false positive-এর সংখ্যাগত মডেল নেই | Section 3.5 | CG8, CG10 |

## ১৪. Improvement ideas

1. **Patch-targeted catching test pipeline:** Agent patch P-এর জন্য issue-text ও patch diff থেকে test বানাও; parent (pre-patch) ও child (post-patch) দুটিতেই চালাও; Table 2-এর ৫ category-তে ফল ফেলো।
2. **Oracle-strength audit:** Generated test-এর assertion-কে mutation-ভিত্তিক "strong hardening" proxy দিয়ে পরীক্ষা করো (ACH-র মতো mutant kill দেখাও) এবং trivial assertion (Assert(True), `not x` যা None-ও ধরে) লিন্টার দিয়ে চিহ্নিত করো।
3. **R@P=α-ভিত্তিক রিপোর্ট:** Assurance report-এ precision ≥ 0.8 শর্তে recall আলাদা দেখাও; F1 বা একক weighted score নয়।
4. **Region-ভিত্তিক signal label:** প্রতিটি test-signal-এ Figure 1-এর region (অনুমিত) ও সংশ্লিষ্ট অনিশ্চয়তা যুক্ত করো।
5. **Category 5 → "যাচাই করা গেল না":** Discard না করে বিশেষ outcome হিসেবে দেখাও (CG7)।
6. **Oracle scavenging:** Issue text, PR description, code comment থেকে প্রত্যাশিত আচরণ নিংড়ে নিয়ে test-এর assertion-এর বিপরীতে মিলিয়ে দেখো; circularity এড়াতে generator আর judge আলাদা model/prompt রাখো।
7. **Gaming-প্রতিরোধ:** Test-writing agent patch-writing agent থেকে বিচ্ছিন্ন রাখো; patch agent test-এর ভেতর কী আছে দেখতে পাবে না।
8. **Delete-and-reinsert** কৌশল লোকাল repo-তে latent bug ও "hidden fail" যাচাইয়ে পরীক্ষা করো।

## ১৫. Publication potential (SPL3-feasible)

- **Workshop/short paper:** "Region taxonomy-based audit of agent-generated tests on SWE-rebench tasks": কতটা test strictly weak, কতটা functionality catching, তার মাপ।
- **Empirical study:** R@P=α দিয়ে patch-targeted catching test generator-দের তুলনা, ছোট fresh SWE-rebench subset-এ (নতুন কাজ কারণ paper নিজে কোনো মাপ দেয়নি)।
- **Negative-result সম্ভাবনা:** ভালো ধারণা, তবু LLM-generated catching test-এর precision 0.8-এ পৌঁছায় না, এটা দেখালেও প্রকাশযোগ্য।
- **Tool paper (অপেক্ষাকৃত কঠিন):** পূর্ণ assurance report prototype।
- সীমা: Paper একটি keynote-পেপার; তাই এর উপর ভিত্তি করে দাবি করলে "এই taxonomy নিয়ে আমরা প্রথমবার মাপলাম" ধরনের দাবিই নিরাপদ।

## ১৬. SPL3 implementation

1. **ডেটা:** Fresh SWE-rebench task-এর ছোট উপসেট (ব্যয় ও সময় বিবেচনায়, প্রথমে ২০–৫০টি) + কয়েকটি agent patch (সঠিক ও ভুল দুটিই; gold patch ও plausible-but-wrong patch)।
2. **Parent/child সংজ্ঞা:** Parent = pre-patch repo, child = patch প্রয়োগের পর repo।
3. **Test generator:** একটি LLM (সাশ্রয়ী) issue text + diff থেকে ৩–৫টি test বানায়।
4. **Runner:** প্রতিটি test parent ও child দুটিতেই চালাও, প্রতিটি ৩ বার (flakiness দেখতে)। Outcome: pass / fail / no-build।
5. **Classifier:** Table 2-এর ৫ category-তে ফেলো। Mapping (আমার প্রস্তাব):
   - fail → pass: patch আচরণ বদলে ঠিক করেছে (support)।
   - pass → pass: শুধু hardening; patch সম্পর্কে নতুন তথ্য নেই।
   - pass → fail: patch regression ঘটিয়েছে বা test ভুল (oracle পরীক্ষা লাগবে)।
   - no build → pass/fail: নতুন functionality test।
   - fail → fail: patch fix করেনি বা test ভুল; "যাচাই করা গেল না" লেবেল।
6. **Oracle-strength:** Patch-এর আশপাশে mutant বানাও; test কয়টা মারে সেটা মাপো।
7. **Evaluation:** Ground truth = gold patch-এর hidden test ও ম্যানুয়াল label। Precision ও recall আলাদা; R@P=0.8; paired test (McNemar)।
8. **Risk:** LLM-বানানো test নিজেই ভুল হতে পারে; তাই পরিমাপ করতে হবে test-এর নিজের সঠিকতা (gold patch-এ pass করে কি না)।
9. **Cost-aware:** ছোট model দিয়ে test generation, শুধু অনিশ্চিত ক্ষেত্রে বড় model।

## ১৭. Influence ও আগের sub-domain-এর সঙ্গে সংযোগ

- **Sub-domain 1 (AI Coding Agents):** SWE-agent, AutoCodeRover, Agentless-এ "plausible ≠ correct" (AutoCodeRover-এর 51/78 = 65.4% সঠিক) সমস্যা; এই paper সেই সমস্যার test-ভিত্তিক সংজ্ঞা দেয়: যে test বদলের আচরণ ধরে না সে strictly weak।
- **Sub-domain 2 (APR):** RePaCA-র static judge-এর পাশে এই paper-এর dynamic signal; overfitting patch ধরতে catching test দরকার।
- **Sub-domain 3 (Evaluation):** Verifier health ও gamed score; এই paper-এর "pseudo false positive", "মিথ্যা নিরাপত্তাবোধ" সেই আলোচনার পরিপূরক।
- **Sub-domain 4 (Test generation):** CoverUp-এর "coverage ≠ oracle" সরাসরি এই paper-এর coverage dilemma; Oracle-Guided Selection-এর distinguishing test এখানে "catching test"-এর বিশেষ রূপ; TestDecision-এর reward-এ assertion strength নেই, এই paper সেই ফাঁক সংজ্ঞায়িত করে।
- এই paper-এ CoverUp ও HITS পরোক্ষভাবে উল্লেখ আছে ([70], [83]), এবং Oracle-guided program selection ([27]) উল্লেখ আছে (oracle inference উদাহরণে)।

## ১৮. Supervisor Q&A

**প্র১: Hardening আর catching test-এর মূল পার্থক্য কী?**
উ: Hardening current revision-এ pass করে এবং ভবিষ্যতের কোনো buggy revision-এ fail করতে পারে। Catching current revision-এই fail করে (strong হলে oracle-ও বলে এটা সঠিক fail)। একই test প্রথমে hardening, পরে catching হতে পারে।

**প্র২: Weak আর strong-এর পার্থক্য কেন গুরুত্বপূর্ণ?**
উ: Strictly weak hardening test current-এ ভুলভাবে pass করে (false negative), ফলে নিরাপত্তার ভ্রান্ত অনুভূতি জন্মায়। আমাদের CG13 (oracle strength) ঠিক এই সমস্যা।

**প্র৩: কেন F1 নয়, R@P=α?**
উ: Industry-তে precision-এ ক্ষতি (engineer-এর friction) সহ্য করা কঠিন, আর recall-এ ঘাটতি তুলনামূলক কম ঝুঁকির। F1 দুটোকে বিনিময়যোগ্য ধরে। α = 0.8 হলে FP:TP ≤ 1:4।

**প্র৪: Paper-এর কোনো experimental result আছে?**
উ: না। Meta-র ACH-র গুণগত বর্ণনা আছে, কিন্তু সংখ্যা অন্য paper-এ। এটা position paper, তাই আমাদের কাজ হবে মাপা।

**প্র৫: আমাদের agent-patch যাচাইয়ে এটা কীভাবে লাগে?**
উ: Patch = child, patch-এর আগের repo = parent। Generated test-কে parent ও child দুটিতেই চালিয়ে Table 2-এর category-তে ফেলা যায়; fail → pass সমর্থক signal, pass → fail সম্ভাব্য regression বা ভুল test।

**প্র৬: Oracle কে ঠিক করবে যখন patch agent লিখেছে?**
উ: Paper-এ PR author ধরা হয়েছে; agent-patch-এ author নেই। এখানে issue text, existing test ও পরোক্ষ মানবীয় রায় ব্যবহার করতে হবে; এটাই আমাদের জন্য অমীমাংসিত প্রশ্ন (G10)।

**প্র৭: Gaming-এর ঝুঁকি কোথায়?**
উ: Paper-এ আলোচিত নয়। কিন্তু Region 1 ও Assert(True)-ধরনের test গেম করার সহজ পথ; আমরা generator ও patch agent বিচ্ছিন্ন রাখব।

**প্র৮: Fail → fail কেন discard?**
উ: Paper বলে ঐ test-এর আসল bug ধরার সম্ভাবনা কম, false positive-এর ঝুঁকি বেশি। আমাদের ক্ষেত্রে বরং "যাচাই করা গেল না" লেবেল দেওয়া ভালো।

## ১৯. Glossary

| Term | অর্থ |
|---|---|
| Hardening test | বর্তমানে pass, ভবিষ্যৎ regression ঠেকায় |
| Catching test | বর্তমান revision-এ fail করে bug ধরে |
| Strong / weak | Oracle-এর সঙ্গে মেলে কি না |
| JiTTest | PR জমা পড়ার মুহূর্তে বানানো test |
| ROT | Regression Only Trap |
| Regression oracle | আগের version-ই ground truth |
| Implicit oracle | crash/memory ভুলের মতো সর্বজনীন ভুল |
| R@P=α | precision ≥ α রেখে recall |
| Pseudo false positive | engineer যে সঠিক signal-ও reject করে |
| Oracle scavenging | non-executable text থেকে প্রত্যাশিত আচরণ খুঁজে নেওয়া |
| ACH | Meta-র mutation-guided test generator |
| Failed error propagation | দূষিত state output পর্যন্ত না পৌঁছানো |

## ২০. Summary card

| বিষয় | সারাংশ |
|---|---|
| Paper | Harden and Catch (FSE Companion '25) |
| ধরন | Position paper, কোনো experiment নেই |
| মূল ধারণা | Hardening বনাম catching; weak বনাম strong; JiTTest |
| মূল সংখ্যা | α = 0.8; 1.75 ঘণ্টা; 8 ঘণ্টা; ৮ region (৫+৩); ৪ RC; ৬ ACH assurance |
| আমাদের কাজে | CG13, CG14, CG12, CG7, CG11; patch = child, pre-patch = parent |
| দুর্বলতা | কোনো empirical validation নেই; recall অনুমান পক্ষপাতদুষ্ট |
| ব্যবহার | Dynamic signal-এর সংজ্ঞা ও R@P=α মেট্রিক |

**RC ও আমাদের CG-র মানচিত্র**

| Paper-এর challenge | আমাদের CG | আমাদের assurance report-এ রূপ |
|---|---|---|
| RC1 শ্রেণিবিন্যাসের ভুল | CG10, CG13 | test-signal-এর region label ও uncertainty |
| RC2 weak → strong | CG13 | oracle-strength audit (mutation + assertion lint) |
| RC3 regression catch বনাম false positive | CG1, CG14 | distinguishing test ও human/LLM-judge সঙ্গে cross-check |
| RC4 Catching JiTTest | CG14, CG3 | patch-targeted catching test; R@P=0.8 |
| Oracle scavenging (Section 6.4) | CG12, CG7 | issue/PR text থেকে oracle; circularity রোধ |
| Latent bug (Section 6.5) | CG6 | contamination-মুক্ত নতুন test source |
| Flaky/valid regression (Section 2.5) | CG15 | environment-নির্ভরতা পরীক্ষা, consistency |

## ২১. বর্তমান (2026) প্রেক্ষাপট

### ২১.১ তখন বনাম এখন

| বিষয় | Paper (2025) | এখন (context.md; V = vendor, I = independent, S = search-snippet) |
|---|---|---|
| Test generation-এ model | নির্দিষ্ট model উল্লেখ নেই; LLM-কে সম্ভাবনা হিসেবে দেখা | Claude Opus 5.5, GPT-6 family, Gemini 4 Argon ইত্যাদি; harness মান mini-SWE-agent |
| Agent-লেখা test-এর oracle | "Assert(True)" কাল্পনিক চরম উদাহরণ | agent-লেখা test patch-এর 80.2% দুর্বল বা অনুপস্থিত oracle (I) |
| Mocking | আলোচিত নয় | agents over-mock 36% বনাম 26% (S) |
| Patch correctness | plausible ≠ correct প্রশ্ন সরাসরি নয় | PatchDiff: 29.6% plausible patch gold থেকে আলাদা আচরণ করে (I, পুরোনো model); ComPass plain-LLM judge 62.14% (S) |
| Benchmark | উল্লেখ নেই | SWE-bench Verified saturated (Vals.ai 97.0%, archived, I) |
| Gaming | আলোচিত নয় | METR: দীর্ঘ কাজের সফল run-এর ≥16% cheat (I, আগের প্রজন্ম); Opus 5.5 card-এ "hidden tests" যুক্তি ও git concealment (V) |

### ২১.২ এখনও সত্য / পুরোনো

- **এখনও সত্য:** ওপরে দেখা ৮০.২% দুর্বল oracle ফল paper-এর weak-hardening ও coverage dilemma-র সংখ্যাগত সমর্থন, অন্তত আগের প্রজন্মের agent-এর জন্য।
- **এখনও সত্য:** Gaming (hidden tests, git concealment) ইঙ্গিত দেয় oracle-কে এমন কারো ওপর ছাড়া যায় না যার স্বার্থ আছে।
- **পুরোনো বা অপরীক্ষিত:** Paper-এর Meta-কেন্দ্রিক সংখ্যা (1.75h/8h) 2026-এর agentic PR flow-এ প্রযোজ্য কি না জানা নেই, কারণ agent তাৎক্ষণিক PR পাঠায় ও review পদ্ধতি বদলেছে (এই বিষয়ে context.md-তে তথ্য পাওয়া যায়নি)।
- **অপরীক্ষিত:** Current-model-এর SWT-bench/TDD-Bench ফল নেই; তাই paper-এর Catching JiTTest যুক্তি LLM-এর আধুনিক সংস্করণে প্রয়োগ করে দেখা বাকি।
- বর্তমান model-এর তথ্য পাওয়া যায়নি: catching JiTTest-এ R@P=0.8-এর সঙ্গে মেলে এমন কোনো সংখ্যা।

### ২১.৩ আজকের দিনে খোলা gap

| Gap | কেন এখনও খোলা | CG |
|---|---|---|
| Current-model (Opus 5.5, GPT-6) এর catching test-এর R@P মাপা | context.md-তে এমন কোনো সংখ্যা নেই | CG14, CG13 |
| Weak/strong oracle-এ নতুন model-এর অবস্থা | 80.2% সংখ্যা আগের প্রজন্মের | CG13 |
| Gaming-সহনশীল catching test (agent test-কে প্রভাবিত করতে পারে না) | hidden tests ও git concealment আচরণ রিপোর্ট হয়েছে (V) | CG12 |
| Judge-এর precision (over-fix flag-এ 5–10% precision, S) | oracle scavenging-কে judge-এর ওপর ছাড়া ঝুঁকিপূর্ণ | CG1, CG7 |
| Security-সম্পর্কিত catching test | SusVibes: FuncPass 62–84% বনাম SecPass 7.8–17.3% (I, Opus 4.6/GPT-5.4 যুগ) | CG5 |

### ২১.৪ SPL3 idea (বর্তমান model, cost-aware)

- **বড় model** (যেমন Opus 5.5, cost প্রতি task 13.20 USD, Vals Terminal-Bench 4.0, I) শুধু পাতলা সংখ্যক কঠিন task-এ।
- **সাশ্রয়ী model** (Kimi K3.1 Pro 4.57 USD; GPT-6.1 Sol 1.72 USD, I) test generation ও scavenging-এ ব্যবহার করে ব্যয় কমানো।
- Pipeline: issue text → সাশ্রয়ী model দিয়ে ৩–৫ test → parent/child execution → Table 2 category → অনিশ্চিত হলে বড় model-এর দ্বিতীয় মত → "যাচাই করা গেল না" বিকল্প।
- মাপ: R@P=0.8, প্রতিবার ৫ run (variance: pass@1 ও pass@5-এর ফাঁক 12–18 pt, I)।
- আমার হিসাব নয়, শুধু অনুমান: খরচ-সীমা ঠিক করতে প্রথমে পাইলটে প্রতি task-এ গড় token মাপতে হবে; context.md-তে এর কোনো সংখ্যা নেই।

### ২১.৫ তিনটি Q&A

**প্র১: Paper 2025-এর; এখন কেন প্রাসঙ্গিক?**
উ: কারণ agent-লেখা test-এর weak oracle (80.2%, I) ও gaming-এর প্রমাণ বলে, যে ধারণার সংজ্ঞা paper দেয় (strong/weak, catching) সেটাই এখন আমাদের মাপার ভিত্তি।

**প্র২: Current model-এর কোনো সরাসরি তথ্য আছে কি?**
উ: Catching JiTTest-এর R@P-এর জন্য নেই। বর্তমান model-এর তথ্য পাওয়া যায়নি। যা আছে তা পরোক্ষ (weak oracle, gaming)।

**প্র৩: Gaming ঠেকাতে paper কী সাহায্য করে?**
উ: সরাসরি করে না। তবে strong hardening ও PR-নির্দিষ্ট oracle scavenging মেনে চললে এমন test-ই গ্রহণযোগ্য হয় যা মানুষ বা স্বাধীন judge যাচাই করতে পারে; এর সঙ্গে generator-agent আলাদা রাখা আমাদের সংযোজন।
