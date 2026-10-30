# Paper Analysis 02 (PatchVal): On the Effectiveness of Code Representation in Deep Learning-Based APCA

> Sub-domain: Patch Validation
> PDF: Patch Validation/On the Effectiveness of Code Representation in Deep.pdf

## ০. Bibliographic info

| ক্ষেত্র | তথ্য |
|---|---|
| Title | On the Effectiveness of Code Representation in Deep Learning-Based Automated Patch Correctness Assessment |
| Authors | Quanjun Zhang (Nanjing Univ. of Science and Technology), Haichuan Hu, Chunrong Fang, Ye Shang, Tao Zheng, Zhenyu Chen (Nanjing University), Yun Yang (Swinburne Univ. of Technology, Australia), Liang Xiao (NJUST) |
| Identifier | arXiv:2603.07520v2 [cs.SE], 5 April 2026 |
| Venue | paper-এ কোনো নির্দিষ্ট journal/conference লেখা নেই; ACM format-এর placeholder আছে ("ACM XXXX-XXXX/2026/4-ART", DOI nnnnnnn), "Vol. 1, No. 1, Article ., April 2026", 27 pages। তাই venue "উল্লেখ নেই" |
| Type | Empirical study (প্রথম systematic study — authors-দের দাবি) |
| Domain | Automated Patch Correctness Assessment (APCA), learning-based, static |
| Dataset | Defects4J v2.0 (835 bugs, 17 project) থেকে 2,274 plausible patch, 39 APR tool (Table 1) |
| Scale | 15 representation, 11 classifier, 5-fold CV; গণনা অনুযায়ী (45+1+22+51)×5 = 595 trained model (§৫.৩-এ "nearly 600"; abstract-এ "more than 500") |
| Artifact | Replication package anonymous.4open.science/r/APCARepresentation (paper-এ দেওয়া) |
| Funding | NSFC (61932012, 62141215, 62372228) |

## ১. TL;DR

**এক কথায়:** Patch-এর code-কে কীভাবে "represent" করলে overfitting patch সবচেয়ে ভালো ধরা যায়, তার প্রথম বড় তুলনামূলক পরীক্ষা। Graph-based (CPG + GGNN) সবচেয়ে ভালো, কিন্তু পার্থক্য ছোট।

- চার ধরনের representation: heuristic (TF-IDF, ODS-এর hand-crafted feature), sequence (subword token), tree (AST), graph (CFG, CDG, DDG, PDG, CPG)।
- Best-of-type accuracy (Table 6): TF-IDF+XGBoost 80.41%, Transformer 82.48%, TreeLSTM+AST 82.94%, GGNN+CPG 83.73%।
- Best single cell: DDG+GGNN accuracy 83.95% (Table 5)।
- দুটো representation fuse করলে উপকার: Heu-Seq backend fusion average 85.95% (Table 7); তিনটি-চারটি fuse করলে উন্নতি নেই।
- Node-এর textual info, type info-র চেয়ে বেশি দরকারি: 85-টি scenario-র মধ্যে 79-টিতে (§৫.১)।
- Pre-trained CodeBERT/CodeT5 সামান্য ভালো (average 83.98% / 83.61%), কিন্তু modest (§৫.২)।

**Supervisor-কে ৩০ সেকেন্ডে:**
1. Static patch-correctness classifier-এ representation বদলালে accuracy প্রায় 80–84%-এর মধ্যে ঘোরে; সবচেয়ে ভালো ও সবচেয়ে খারাপ "ভালো" representation-এর ফারাক মাত্র কয়েক pp।
2. সব পরীক্ষা শুধু Defects4J (Java, একটি benchmark), random 5-fold CV; cross-project / cross-dataset test নেই — authors নিজেরাই স্বীকার করেছেন (§৫.৩)।
3. Correct class-এর 1,169-এর মধ্যে 965-টি (82.5%, আমার হিসাব) developer-এর লেখা patch — তাই classifier "developer-style vs tool-style" শিখছে কি না, প্রশ্ন থাকে।
4. Specificity paper-এ report হয়নি; recall-heavy (recall 87.09%, precision 81.00%)। আমার হিসাবে specificity প্রায় 80.7%।
5. আমাদের জন্য: এটি RePaCA (Sub-domain 2)-এর "learned-classifier বিকল্প" baseline; কিন্তু leakage-সংক্রান্ত evaluation design আমাদের CG10 আরও জোরালো করে।

## ২. Background (এই project-এ নতুন concept)

- **Patch overfitting:** test-suite pass করে (plausible) কিন্তু developer-এর patch-এর সাথে semantically সমান নয় (correct নয়)। CG1-এর সাথে সরাসরি যুক্ত।
- **APCA:** একটি plausible patch correct না overfitting, তা automatic ঠিক করা। তিন শ্রেণি: static (code pattern/similarity), dynamic (নতুন test generate করে execute; যেমন PATCH-SIM), learning-based (classifier)।
- **PATCH-SIM:** Randoop দিয়ে extra test generate করে execution trace তুলনা করে; paper বলছে 139 patch classify করতে প্রায় 70 ঘণ্টা লাগে (§৪.২)।
- **Code representation চার প্রকার:**
  - Heuristic: TF-IDF অথবা হাতে বানানো feature (ODS-এর 202 feature = code 50 + context + pattern 26)।
  - Sequence: subword token-এর ক্রম (যেমন getUserName → get, user, name)।
  - Tree: AST।
  - Graph: CFG (execution flow), CDG (control dependency), DDG (data dependency), PDG (CDG+DDG), CPG (CFG+CDG+DDG একত্রে)। Joern দিয়ে তৈরি, DGL দিয়ে চালানো।
- **Models:** classic ML (SVM, Naive Bayes, XGBoost); sequence (LSTM, BiLSTM, Transformer encoder); tree (TreeLSTM, TBCNN); graph (GCN, GAT, GGNN)।
- **Fusion:** intermediate (vector concatenate করে একটি classifier train) বনাম backend (আলাদা trained model-এর softmax probability-র গড়)।
- **k-fold cross-validation:** data 5 ভাগ করে ঘুরিয়ে test করা; এখানে random split (bug বা project অনুযায়ী নয়)।

## ৩. Problem

- APR-এর generate-and-validate ধাপে test-suite দুর্বল হলে plausible but incorrect (overfitting) patch আসে; developer-কে হাতে filter করতে সময় লাগে।
- Static APCA-তে precision কম হওয়ার ঝুঁকি; dynamic APCA-তে runtime তথ্যের জন্য অনেক সময় লাগে।
- Learning-based APCA-তে অনেক আলাদা representation আছে (ODS heuristic, Tian et al. sequence/BERT, CACHE AST-path), কিন্তু কোনটি কেন ভালো — তার systematic তুলনা ছিল না। বিশেষ করে graph-based representation APCA-তে প্রায় অনাবিষ্কৃত।
- তিনটি অমীমাংসিত প্রশ্ন: (১) কোন representation optimal; (২) graph কেমন; (৩) একাধিক representation মেলানো যায় কি।

## ৪. Goal & RQ

**Goal:** APCA-র জন্য code representation-এর কার্যকারিতা, সীমা ও fusion-সম্ভাবনা মাপা, এবং future research-এর guideline দেওয়া।

| RQ | প্রশ্ন |
|---|---|
| RQ1 | চার ধরনের representation কেমন perform করে ও কীভাবে তুলনীয়? |
| RQ2 | Best representation-গুলো state-of-the-art APCA (PATCH-SIM, ODS, Tian et al., CACHE)-র তুলনায় কেমন? |
| RQ3 | একাধিক representation মেলালে prediction ভালো হয় কি? |
| Extra | §৫.১ node embedding (type vs textual vs hybrid); §৫.২ pre-trained code model |

**Contributions (paper অনুযায়ী):** 2,274-patch benchmark; 500+ model-এর empirical study; 22 fusion scenario (11 combination × 2 strategy); practical guideline।

## ৫. Methodology

**ধাপ ১ — Preprocessing (§৩.১):** plausible patch থেকে buggy code snippet ও patched code snippet বের করা।

**ধাপ ২ — Representation (§৩.৩), মোট 15টি:**
1. Heuristic (8টি): TF-IDF; Code (Coming দিয়ে 50 feature: operator, variable, statement, AST operation); Context; Pattern (ADD দিয়ে 26 repair pattern, Sobreira-র 395 Defects4J patch-ভিত্তিক taxonomy, 5 category); এবং pairwise ও triple combination (Code&Context, Code&Pattern, Context&Pattern, Code&Context&Pattern)।
2. Sequence (1টি): subword tokenizer।
3. Tree (1টি): AST।
4. Graph (5টি): CFG, CDG, DDG, PDG, CPG।

**ধাপ ৩ — Classifier (§৩.৪), 11টি:** Naive Bayes, SVM, XGBoost; LSTM, BiLSTM, Transformer; TreeLSTM, TBCNN; GCN, GAT, GGNN। TBCNN নিজেরা PyTorch-এ re-implement; max tree node 5000, max children 200।

**ধাপ ৪ — Training (§৩.৭):**
- Learning rate 0.001 (Transformer 0.0005); max epoch 100; batch size 128 (TBCNN-এ 16); word embedding dim 128; dropout 0.2।
- Random split → train/validation/test; 5-fold CV-তে report।
- Hardware: Ubuntu 18.04.3, দুটি Tesla V100-SXM2-32GB।
- Default hyper-parameter (prior work [49] অনুসরণ); কোনো আলাদা hyper-parameter tuning বর্ণিত নেই।

**ধাপ ৫ — Dataset (§৩.৬):** Liu et al., Xiong et al., Ali et al., Tian et al., Lin et al. ইত্যাদির release থেকে patch সংগ্রহ; developer-এর correct patch যোগ (imbalance কমাতে, Tian et al. অনুসরণ); whitespace ও comment সরিয়ে buggy ও patched snippet হুবহু সমান হলে duplicate বাদ।

**ধাপ ৬ — RQ2 baseline:** ODS, Tian et al. (BERT embedding + LR/DT/NB/SVM), CACHE (AST path), PATCH-SIM। PATCH-SIM-এর জন্য Xiong et al.-এর 139 test patch ব্যবহার, বাকি সব training; শুধু tree-based model train (page limit ও training সময়ের কারণে)।

**ধাপ ৭ — Fusion (§৪.৩):** প্রতি type-এর best (TF-IDF+XGBoost, Transformer, TreeLSTM, GGNN) নিয়ে 11 combination। Intermediate = vector concatenate + softmax classifier; Backend = চারটি trained model-এর softmax probability-র গড় (paper একে stacking বলেছে, কিন্তু বর্ণনা আসলে simple averaging)।

**ধাপ ৮ — Node embedding (§৫.১):** type embedding (linear layer), textual embedding (node-এর প্রথম লাইন → BiLSTM-এর last hidden state), hybrid (concatenate → linear)।

**ধাপ ৯ — Pre-trained (§৫.২):** CodeBERT (encoder-only), CodeT5 (encoder-decoder) token sequence-এ।

## ৬. Math

Positive class = **overfitting** (আমাদের ধারণার "reject করা patch")। TP = overfitting ধরা পড়েছে; FP = correct patch-কে overfitting বলা; FN = overfitting patch-কে correct বলা; TN = correct patch correct বলা।

$$\text{Accuracy} = \frac{TP + TN}{TP + FP + FN + TN}$$

$$\text{Recall} = \frac{TP}{TP + FN}, \qquad \text{Precision} = \frac{TP}{TP + FP}$$

$$F1 = 2 \cdot \frac{\text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}}$$

$$AUC = \frac{\sum_{i=1}^{M} \text{rank}_i - \frac{M(M+1)}{2}}{M \times N}$$

- $\text{rank}_i$ = $i$-তম positive sample-এর predicted rank; $M$ = positive সংখ্যা; $N$ = negative সংখ্যা।
- "Average" column = পাঁচ metric-এর গড় (Table 2–5, 7, 8, 9); Table 6-এ চার metric (AUC বাদ)।

**Paper-এ নেই, কিন্তু আমাদের জন্য জরুরি (আমার হিসাব):** Specificity (correct patch গ্রহণের হার)।

$$\text{Specificity} = \frac{TN}{TN + FP}$$

**Worked example — GGNN+CPG (Table 6 / Table 5):** Table 1 অনুযায়ী correct = 1169, overfitting = 1105 (সূত্র: Table 1 total row; §৩.৬-এর লেখায় সংখ্যা উল্টো আছে, নিচে §১২ দেখো)। Recall = 87.09%, Precision = 81.00%।

1. TP = 0.8709 × 1105 = 962.3 (প্রায়)।
2. Predicted positive = TP / Precision = 962.3 / 0.8100 = 1188.0 (প্রায়)।
3. FP = 1188.0 − 962.3 = 225.7; TN = 1169 − 225.7 = 943.3।
4. Specificity = 943.3 / 1169 = **80.7%** (আমার হিসাব)।
5. Cross-check: Accuracy = (962.3 + 943.3) / 2274 = 83.8% (paper 83.73%) — মিলছে, তাই Table 1-এর class orientation সঠিক ধরা হলো।
6. F1 = 2 × 0.81 × 0.8709 / (0.81 + 0.8709) = 83.9% (paper 83.90%) — মিলছে।

একই পদ্ধতিতে (আমার হিসাব, পুরো dataset-এর আনুমানিক pooled সংখ্যা; 5-fold average-এর কারণে সামান্য ভুল সম্ভব):

| Approach | Recall | Precision | আনুমানিক Specificity |
|---|---|---|---|
| TF-IDF + XGBoost | 83.21% | 78.07% | প্রায় 77.9% |
| Transformer (sequence) | 87.27% | 78.97% | প্রায় 78.0% |
| TreeLSTM + AST | 86.73% | 80.01% | প্রায় 79.5% |
| GGNN + CPG | 87.09% | 81.00% | প্রায় 80.7% |

**PATCH-SIM-এর 139-patch test set (আমার হিসাব, অনুমান-ভিত্তিক):** PATCH-SIM precision 100%, accuracy 66%, recall 57% থেকে সমীকরণ $0.57P + (139-P) = 0.66 \times 139$ সমাধান করলে $P \approx 110$ (overfitting), $N \approx 29$ (correct) আসে; RePaCA-র reported 109/30 split-এর সাথে মেলে (Sub-domain 2-এর RePaCA দেখো)। এই অনুমানে Tree model (recall 91%, precision 84%): TP ≈ 99.2, FP ≈ 18.9, TN ≈ 11.1, specificity ≈ 37% — অর্থাৎ correct patch-এর মাত্র প্রায় 37% গ্রহণ। এটি paper-এ নেই; split-টি আমার অনুমান।

**"X% improvement" কীভাবে পড়তে হবে:** Paper-এর বেশিরভাগ "improvement" relative শতাংশ। উদাহরণ: TF-IDF বনাম ODS accuracy: (80.41 − 71.00) / 71.00 = 13.25% ✓ (আমার যাচাই)। কিন্তু §৫.২-এ AUC "5.20%" absolute pp (87.80 − 82.60)। মিশ্র ব্যবহার, পাঠককে সাবধান থাকতে হবে।

## ৭. Setup

| বিষয় | মান |
|---|---|
| Benchmark | Defects4J v2.0, 835 bug, 17 project |
| Patch সংখ্যা | 2,274 (Table 1: 1,169 correct, 1,105 overfitting) |
| Patch-এর উৎস | 39 row (Developer সহ) = 38 APR tool + developer; §১-এ "more than 30 repair tools", §৫.৩-এ "39 APR tools" |
| Developer-এর correct patch | 965 (সব correct class-এর 82.5%, আমার হিসাব) |
| Tool-এর correct patch | 204 (আমার হিসাব) বনাম 1,105 overfitting |
| Positive class | Overfitting |
| Evaluation | 5-fold CV, random split |
| Metrics | Accuracy, Precision, Recall, F1, AUC (মাত্র এই পাঁচটি) |
| Baseline | ODS, Tian et al. (LR, DT, SVM, NB), CACHE, PATCH-SIM |
| Language | শুধু Java |
| Tool | Joern, DGL, Coming, ADD, PyTorch |
| Seed / run | একাধিক seed বা variance (std, CI) report করা হয়নি; significance test নেই |

## ৮. Results

### ৮.১ Heuristic (Table 2)

| Model + Feature | Accuracy | Recall | F1 | Average |
|---|---|---|---|---|
| XGBoost + TF-IDF | 80.41% | 83.21% | 80.50% | 80.53% |
| XGBoost + Code&Context&Pattern | 75.85% | 76.63% | 75.53% | 75.67% |
| NaiveBayes + TF-IDF | 79.23% | 82.22% | 79.39% | 79.38% |
| SVM + TF-IDF | 61.09% | 93.95% | 70.20% | 68.67% |
| SVM + Code&Pattern | 50.02% | 98.83% | 65.82% | 63.06% |

- TF-IDF তিন classifier-এর গড়ে: accuracy 73.58%, precision 70.33%, recall 86.46%, F1 76.70%, AUC 73.91%।
- SVM প্রায় সব feature-এ recall 90%+ কিন্তু accuracy প্রায় 50–61% — প্রায় সবকিছুকে overfitting বলছে (high recall, কম specificity-র চরম উদাহরণ)। Paper এটি আলাদাভাবে বিশ্লেষণ করেনি।
- XGBoost সব feature গড়ে accuracy 73.03%, F1 72.61%।

### ৮.২ Sequence (Table 3)

| Model | Accuracy | Precision | Recall | F1 | AUC | Average |
|---|---|---|---|---|---|---|
| LSTM | 81.60% | 79.04% | 84.66% | 81.74% | 81.68% | 81.74% |
| BiLSTM | 82.04% | 78.48% | 86.91% | 82.45% | 82.16% | 82.41% |
| Transformer | 82.48% | 78.97% | 87.27% | 82.87% | 82.60% | 82.84% |

### ৮.৩ Tree (Table 4)

| Model | Accuracy | Precision | Recall | F1 | AUC | Average |
|---|---|---|---|---|---|---|
| TreeLSTM | 82.94% | 80.01% | 86.73% | 83.18% | 83.03% | 83.18% |
| TBCNN | 81.72% | 79.24% | 84.62% | 81.84% | 81.79% | 81.84% |

### ৮.৪ Graph (Table 5, প্রতি graph-এর average ও সেরা model)

| Graph | GAT avg | GCN avg | GGNN avg | Graph average accuracy | Graph average (5 metric) |
|---|---|---|---|---|---|
| CFG | 81.44% | 75.56% | 83.44% | 79.87% | 80.15% |
| DDG | 82.43% | 75.69% | 84.05% | 80.77% | 80.72% |
| PDG | 81.62% | 75.61% | 82.76% | 80.08% | 80.00% |
| CDG | 76.33% | 73.04% | 82.38% | 76.52% | 77.25% |
| CPG | 82.83% | 82.47% | 83.91% | 82.69% | 83.07% |

- Best single cell: DDG+GGNN accuracy 83.95%, recall 86.73%, F1 84.04% (Table 5)।
- CPG+GGNN: accuracy 83.73%, precision 81.00%, recall 87.09%, F1 83.90%, AUC 83.81%।
- GCN সবচেয়ে দুর্বল (CFG-তে 75.59%) কিন্তু CPG-তে 81.80% ও সর্বোচ্চ recall 88.63% (সব graph model-এর মধ্যে সর্বোচ্চ)।
- CFG-তে accuracy 75.59% থেকে 83.15% — একই representation, model বদলে 7.6 pp ফারাক (§৫.৪ guideline-এ উল্লেখ)।
- Cross-type: graph-এর সব graph ও classifier মিলিয়ে average accuracy 79.99%, precision 78.36%, recall 82.54%, F1 80.31%, AUC 80.00% (§৪.১)।

### ৮.৫ Best-of-type বনাম SOTA (Table 6, 5-fold CV, নিজের dataset-এ)

| Approach | Accuracy | Precision | Recall | F1 | Average |
|---|---|---|---|---|---|
| ODS | 71.00% | 72.00% | 71.00% | 71.00% | 71.25% |
| Tian et al. (LR) | 75.00% | 77.78% | 74.00% | 75.00% | 75.45% |
| Tian et al. (DT) | 63.74% | 65.09% | 65.37% | 65.23% | 64.86% |
| Tian et al. (SVM) | 76.58% | 78.48% | 75.76% | 77.09% | 76.98% |
| Tian et al. (NB) | 61.00% | 64.00% | 55.00% | 59.00% | 59.75% |
| CACHE | 74.00% | 74.00% | 87.00% | 79.00% | 78.50% |
| Heuristic (TF-IDF+XGBoost) | 80.41% | 78.07% | 83.21% | 80.50% | 80.55% |
| Sequence (Transformer) | 82.48% | 78.97% | 87.27% | 82.87% | 82.90% |
| Tree (TreeLSTM) | 82.94% | 80.01% | 86.73% | 83.18% | 83.03% |
| Graph (GGNN+CPG) | 83.73% | 81.00% | 87.09% | 83.90% | 83.81% |

**PATCH-SIM-এর 139 patch-এ (Table 6, শেষ দুই row):**

| Approach | Accuracy | Precision | Recall | F1 | Average |
|---|---|---|---|---|---|
| PATCH-SIM | 66.00% | 100.00% | 57.00% | 73.00% | 74.00% |
| Tree-based | 80.00% | 84.00% | 91.00% | 88.00% | 85.75% |

- Graph-এর average (83.81) বনাম Tian-SVM (76.98): 6.83 pp absolute; বনাম CACHE (78.50): 5.31 pp। Introduction-এ "CPG+GGNN, Tian et al. (BERT+SVM)-কে accuracy-তে 9.34% ইত্যাদি" লেখা আছে: (83.73−76.58)/76.58 = 9.34% ✓ (আমার যাচাই, relative)।
- Baseline-এর অনেক সংখ্যা integer % (71.00, 75.00, 61.00 …) — CACHE/ODS মূল paper থেকে নেওয়া নাকি এই dataset-এ re-run, §৪.২ বলছে "executing them on our datasets" কিন্তু integer precision অন্য ইঙ্গিত দেয়।

### ৮.৬ Fusion (Table 7, Average column)

| Combination | Intermediate avg | Backend avg |
|---|---|---|
| Heu-Seq | 84.73% | 85.95% |
| Heu-Tre | 83.85% | 82.31% |
| Heu-Gra | 84.60% | 83.45% |
| Seq-Tre | 82.53% | 81.25% |
| Seq-Gra | 83.49% | 82.80% |
| Tre-Gra | 84.66% | 83.88% |
| Heu-Seq-Tre | 82.72% | 83.08% |
| Heu-Seq-Gra | 84.24% | 83.85% |
| Heu-Tre-Gra | 84.37% | 84.16% |
| Seq-Tre-Gra | 83.30% | 83.14% |
| Heu-Seq-Tre-Gra | 83.81% | 84.52% |

- সর্বোচ্চ Heu-Seq backend: accuracy 85.42%, precision 84.00%, recall 88.75%, F1 86.29%, AUC 85.30%।
- তুলনা: single best (GGNN+CPG) average 83.81% (Table 6) — Heu-Seq backend 85.95% মাত্র 2.14 pp (absolute, আমার হিসাব) ভালো।
- Heu-Tre intermediate accuracy 83.04%; Heu-Tre-Gra 83.54% ইত্যাদি — চারটি মেলালে (83.81%) best pair-এর (84.73%) নিচে।

### ৮.৭ Node embedding (Table 8, নির্বাচিত row)

| Model + Graph | Textual avg | Type avg | Hybrid avg |
|---|---|---|---|
| TreeLSTM + AST | 83.62% | 82.50% | 83.18% |
| GGNN + CPG | 83.01% | 82.49% | 83.91% |
| GAT + PDG | 81.34% | 72.07% | 81.62% |
| GAT + CFG (row label সন্দেহজনক, §১২) | 81.44% | 63.72% | 80.93% |

- Textual > type: 85 scenario-র মধ্যে 79-টিতে, গড় improvement 5.24% (§৫.১)।
- PDG+GAT-এ textual, type-কে 12.62% (accuracy) ছাড়িয়েছে (আমার যাচাই: (81.14−72.05)/72.05 = 12.62% ✓)।
- Hybrid আরও ভালো GGNN+CPG-তে (+0.88% accuracy), কিন্তু TreeLSTM+AST-এ গড়ে 0.53% কমেছে।
- Type-only অনেক model-এ খুব খারাপ: CFG+GAT 63.32% accuracy (Table 8)।

### ৮.৮ Pre-trained (Table 9)

| Model | Accuracy | Precision | Recall | F1 | AUC | Average |
|---|---|---|---|---|---|---|
| CodeBERT | 83.22% | 82.48% | 83.48% | 82.93% | 87.80% | 83.98% |
| CodeT5 | 82.96% | 81.86% | 83.67% | 82.69% | 86.88% | 83.61% |
| Transformer | 82.48% | 78.97% | 87.27% | 82.87% | 82.60% | 82.84% |

- CodeBERT-এর precision 82.48% (Transformer-এর চেয়ে 3.51 pp বেশি) কিন্তু recall 83.48% (3.79 pp কম, আমার হিসাব)। অর্থাৎ pre-trained model বেশি "সাবধানী"; trade-off ভিন্ন।

## ৯. Key findings

1. **Representation-গুলোর মধ্যে ব্যবধান ছোট:** best-of-type accuracy 80.41–83.73%। সবচেয়ে ভালো (graph) ও সবচেয়ে দুর্বল (heuristic) best model-এর ফারাক মাত্র 3.32 pp (আমার হিসাব)।
2. **Graph সবচেয়ে ভালো গড়ে:** CPG+GGNN accuracy 83.73%, CPG তিন GNN-এর গড় accuracy 82.69%।
3. **CPG বহু-তথ্য একত্র করে বলে ভালো:** CDG একা সবচেয়ে দুর্বল (average 77.25%)।
4. **Model-নির্বাচন representation-এর মতোই গুরুত্বপূর্ণ:** GGNN সব graph-এ সেরা, GCN CFG-তে 75.59% — একই graph-এ 7.6 pp ফারাক।
5. **TF-IDF একটি শক্ত, সস্তা baseline:** XGBoost+TF-IDF 80.41% accuracy, ODS-এর হাতে-বানানো 202 feature-কে হারিয়েছে।
6. **দুটির fusion কাজ করে, বেশির fusion করে না:** Heu-Seq backend 85.95% (average); চারটি মেলালে 83.81% (intermediate) / 84.52% (backend)। কারণ হিসেবে naive fusion (concatenate/average) অনুমান করা হয়েছে, পরীক্ষা করা হয়নি।
7. **Static classifier dynamic technique-কে recall-এ ছাড়ায়, precision-এ নয়:** PATCH-SIM precision 100%, recall 57%; Tree model precision 84%, recall 91%।
8. **Node-এর textual info বেশি মূল্যবান:** type-only embedding কিছু ক্ষেত্রে ভয়াবহ দুর্বল (63.32%)।

## ১০. Why better than alternatives

- ODS (hand-crafted): graph/tree/sequence সবাই ODS (average 71.25%) ছাড়িয়েছে, কারণ representation automatic শেখা হয়, hand-crafted feature-এর সীমা নেই।
- Tian et al. (BERT embedding + classic classifier): task-specific end-to-end train করা model embedding-কে "frozen" না রেখে সরাসরি শেখে; Transformer 82.48% বনাম Tian-SVM 76.58%।
- CACHE: AST path-এর বদলে full tree/graph মডেল; graph 83.81% বনাম 78.50% (average)।
- PATCH-SIM: execution ছাড়াই (static) দ্রুত; ঘণ্টার বদলে ইনফারেন্স — তবে precision-এ পিছিয়ে (84% বনাম 100%)।
- Graph বনাম sequence: control/data-flow সরাসরি encode হয়, তবে লাভ মাত্র প্রায় 1.25 pp (accuracy 83.73 বনাম 82.48, আমার হিসাব)।

## ১১. When it works / fails

**ভালো কাজ করে:**
- Defects4J-জাতীয় Java benchmark, যেখানে training-এ একই bug বা একই APR tool-এর patch আছে।
- Patch ছোট, localised (এক-দুই statement) হলে — তবে paper patch-size অনুযায়ী ভাঙেনি।

**সমস্যা ও failure (paper ও আমার পর্যবেক্ষণ):**
- Representation-model mismatch: GCN-এ CFG/DDG/PDG দুর্বল।
- SVM-জাতীয় classifier সব patch-কে overfitting বলে (accuracy ~50%)।
- Fusion-এ তিনটির বেশি মেলালে অবনতি।
- Cross-project, cross-language, cross-tool, বা LLM-generated patch-এ কী হয়, তা অপরীক্ষিত।

## ১২. Limitations

**Authors-দের স্বীকৃত (§৫.৩):**
- Baseline নির্বাচন সীমিত (অন্য APCA technique বাদ)।
- শুধু Defects4J; অন্য dataset-এ generalise অজানা।
- Cross-validation: একই bug-এর ভিন্ন tool-এর patch train ও test-এ ভাগ হতে পারে; বাস্তবে এটা সম্ভব নয়।
- Cross-project evaluation ও correct-patch-identification setting ভবিষ্যৎ কাজ।
- আরও representation ও model বাদ পড়েছে।

**আমার পর্যবেক্ষণ:**
1. **Label/source confound:** Correct class-এর 82.5% (965/1169) developer patch, overfitting class-এ developer patch 0। Tool-generated correct মাত্র 204 বনাম 1,105 overfitting (সবই আমার হিসাব, Table 1 থেকে)। Model "কোন patch developer-style" শিখেও accuracy পেতে পারে। Paper-এ tool-split বা tool-held-out test নেই। এটি CG10-র সরাসরি উদাহরণ।
2. **Class balance কৃত্রিম:** Test set-এ প্রায় 51% correct; বাস্তবে tool-generated plausible patch-এর মধ্যে correct অনেক কম (এই dataset-এ tool-generated-এর মধ্যে 204/1309 = 15.6%, আমার হিসাব)। Accuracy/AUC বাস্তব deployment-এর precision সম্পর্কে ভুল ধারণা দেয়।
3. **Specificity report হয়নি।** আমার হিসাবে CPG+GGNN প্রায় 80.7% (§৬)। PATCH-SIM-এর subset-এ Tree model-এর আনুমানিক 37% (অনুমান-ভিত্তিক)।
4. **Variance নেই:** 5-fold-এর std, seed, significance test দেওয়া হয়নি; best-of-type-এর 1 pp ফারাক (Transformer 82.48 বনাম TreeLSTM 82.94) noise-এর মধ্যে হতে পারে। "Graph consistently outperforms" বলার statistical ভিত্তি নেই।
4. **Hyper-parameter tuning নেই (default):** model-wise ন্যায্যতা অনিশ্চিত; GCN-এর দুর্বলতা under-tuning হতে পারে।
5. **LLM যুগের patch নেই:** সব patch পুরনো 39 APR tool-এর; agent/LLM-generated patch-এর distribution ভিন্ন।
6. **Baseline re-run অস্পষ্ট:** ODS/CACHE-এর সংখ্যা integer-ধরনের (71, 74, 87…), "own dataset-এ run" দাবির সাথে সন্দেহজনক।
7. **Paper-internal অসংগতি (যাচাই করা):**
   - §৩.৬ লেখা "2274 (1169 overfitting and 1105 correct)"; Table 1 header বলছে 1169 correct / 1105 overfitting। Table 1 ও Developer row (965 correct, 0 overfitting) এবং আমার accuracy cross-check Table 1-এর পক্ষে — লেখাটাই উল্টো।
   - Abstract: "TreeLSTM trained with AST 87.09% overfitting patches filter"; Table 4-এ TreeLSTM recall 86.73%; 87.09% আসলে GGNN+CPG-র recall।
   - RQ2 summary/§৪.২ কোথাও "DDG+GGNN", Table 6/RQ1 "CPG+GGNN"।
   - Table 2: SVM-এর "Context & Pattern" ও "Code & Context & Pattern" row হুবহু এক (54.46/51.99/91.86/66.12/55.44) — copy-paste সন্দেহ।
   - RQ1 "45 models": আমার গণনায় 24+3+2+15 = 44।
   - Table 5-এর CPG average-এর লেখায় পাঁচ metric-এর জায়গায় ছয়টি সংখ্যা (শেষটি সম্ভবত গড়)।
   - Table 8-এর row label: কিছু default (hybrid) মান "Textual" row-তে বসেছে (যেমন GAT+CFG 80.86%, GGNN+CFG 83.15% যা Table 5-এ default), অন্যগুলোতে "Hybrid" row-তে — label সম্ভবত গোলমেলে।
   - §৪.৩/Intro: "13.58% improvement of Heu-Seq" — Table 7 ও Table 6 থেকে TF-IDF+XGBoost (80.55%) বনাম Heu-Seq backend (85.95%) relative 6.7%; তাই 13.58% সম্ভবত সব heuristic variant-এর গড় ভিত্তি; paper-এ স্পষ্ট নয়।
   - "Backend fusion"-কে stacking বলা হয়েছে, বর্ণনায় simple averaging।
   - Table 9: CodeBERT AUC 87.80% অন্য সব metric (প্রায় 83%) থেকে অনেক বেশি; অন্য model-এ AUC ≈ accuracy — আলাদা গণনা সন্দেহ।
   - §৪.৩ ও §৫.৪-এ "accuracy 13.58% / 82.21% for heu-seq-tre" — Table 7-এ Heu-Seq-Tre backend accuracy 82.21% ✓, কিন্তু §৪.৩ "82.10%" (intermediate)। দুই fusion-এর সংখ্যা মিশে আছে।

## ১৩. Research gaps

| ID | Gap | Evidence | Related CG / folder |
|---|---|---|---|
| G-PV2-1 | Random 5-fold CV-তে leakage (একই bug-এর ভিন্ন patch train/test-এ), cross-project/cross-bug test নেই | §৫.৩ authors-রা নিজেরা বলেছেন | CG10 / 05_Patch_Validation |
| G-PV2-2 | Developer patch দিয়ে correct class ভরা (82.5%) — source-confound | Table 1 | CG10, CG1 |
| G-PV2-3 | Specificity ও balanced/realistic prevalence-এ precision report হয়নি | Table 2–9 শুধু 5 metric | CG1, CG10 |
| G-PV2-4 | কোনো variance/significance (std, McNemar) নেই | Table 3–6 single number | CG8, CG4 |
| G-PV2-5 | Cross-language/repository-level/agent-generated patch-এ অপরীক্ষিত | §৩.৬ (Defects4J Java only) | CG9 |
| G-PV2-6 | LLM/reasoning-model judge-এর সাথে সরাসরি তুলনা নেই; paper নিজে LLM-কে future work বলেছে | §৫.৪ | CG1, Sub-domain 2 (RePaCA) |
| G-PV2-7 | Fusion naive (concatenate/average); learned fusion অপরীক্ষিত | §৪.৩ | CG2 |
| G-PV2-8 | Abstain/uncertainty নেই — classifier সব patch-এ হ্যাঁ/না বলে | §৩.৫ binary only | CG7 |
| G-PV2-9 | Adversarial/gaming robustness (patch-এ TF-IDF-মতো surface token বদলে classifier ঠকানো) পরীক্ষিত নয় | সম্পূর্ণ অনুপস্থিত | CG12 |
| G-PV2-10 | Classifier-এর version-bound validity (নতুন tool/model-এর patch distribution-এ drift) | §৫.৩ নতুন tool-এর patch ভবিষ্যৎ কাজ | CG11 |

## ১৪. Improvement ideas

1. **Leakage-মুক্ত split:** bug-grouped ও tool-held-out split; ফলাফল random-CV-র সাথে পাশাপাশি দেখানো।
2. **Developer-patch confound সরানো:** শুধু tool-generated patch-এ train/test, অথবা developer patch আলাদা control হিসেবে।
3. **Specificity ও prevalence-adjusted precision:** বাস্তব অনুপাত (প্রায় 15% correct) অনুযায়ী reweight।
4. **Representation + LLM:** CPG/AST-কে LLM-এর prompt-এ structured context হিসেবে দেওয়া; RePaCA-র reasoning-এর সাথে classifier-এর score মিলিয়ে ensemble।
5. **Learned fusion:** gating/attention, meta-classifier (বর্তমান averaging-এর বদলে)।
6. **Abstention:** দুই classifier (graph, sequence)-এর disagreement হলে "could not verify"।
7. **Repeat runs + paired test:** McNemar, bootstrap CI।

## ১৫. Publication potential (SPL3-feasible)

- **সম্ভাব্য শিরোনাম:** "Do Code-Representation APCA Classifiers Generalise? A Leakage-Free, Specificity-Aware Re-evaluation" — workshop/short paper (বাস্তবসম্মত)।
- **Novelty:** paper-এর replication package ব্যবহার করে (১) bug-grouped split, (২) tool-held-out split, (৩) developer-patch ablation, (৪) specificity ও prevalence-adjusted precision, (৫) paired significance test।
- **Feasible কারণ:** dataset ছোট (2,274), model ছোট (V100-এ train হয়েছে), artifact open।
- **Risk:** replication package-এ আমরা নিশ্চিত নই 2,274-patch ও split ID সবই আছে কি না; Joern-এর build ঝামেলা হতে পারে। প্রথমে sequence (CodeBERT) ও TF-IDF দিয়ে শুরু করা নিরাপদ।
- **Strong claim:** যদি tool-held-out-এ accuracy উল্লেখযোগ্য কমে (যেমন 83% → ~65%), সেটাই মূল ফলাফল। কমার পূর্বানুমান আমার অনুমান, প্রমাণ নয়।

## ১৬. SPL3 implementation

**Static overfitting detector-এর জন্য representation সুপারিশ (আমার মত):**
1. **Baseline ১ (সস্তা):** TF-IDF + XGBoost (80.41%; CPU-তে সেকেন্ডে train)।
2. **Baseline ২:** CodeBERT sequence classifier (83.22% accuracy; precision 82.48% বেশি, recall 83.48% কম) — GPU লাগলে ছোট।
3. **Baseline ৩ (গবেষণা):** CPG+GGNN (83.73%) — তবে Joern pipeline ও Java-only; ফারাক sequence-এর চেয়ে মাত্র 0.5–1.25 pp, তাই খরচ-লাভ সন্দেহজনক।
4. **Fusion:** Heu-Seq backend (85.95%) সস্তা ও সেরা fusion — probability average, নতুন architecture লাগে না।
5. **আমাদের নতুন কাজ:** একই pipeline RePaCA-style LLM judge-এর পাশে চালিয়ে দুটোর signal আলাদা রাখা (single weighted score নয়)।

**Pipeline:**
- Dataset: Defects4J patch (paper-এর artifact) + SWE-bench-জাতীয় agent patch (CG9 পরীক্ষা, যদি label পাওয়া যায়)।
- Split: (ক) random 5-fold (paper-এর পুনরাবৃত্তি), (খ) bug-grouped, (গ) tool-held-out।
- Metric: recall, specificity, precision at realistic prevalence, F1, AUC; প্রতিটির bootstrap CI; paired McNemar।
- Output: probability + "uncertain" band।

**সময় ও খরচ:** TF-IDF/XGBoost ও CodeBERT ছোট GPU-তে ঘণ্টার মধ্যে; Joern+GNN সবচেয়ে ভারী। আমার অনুমান — paper-এ খরচ/training সময় দেওয়া নেই।

## ১৭. Influence / link to our earlier sub-domains

- **Sub-domain 2, RePaCA:** RePaCA (reasoning LLM + GRPO) Defects4J-তে 83.1% accuracy, 106/109 overfitting ধরেছিল কিন্তু 16/30 correct গ্রহণ করেছিল। এই paper-এর graph/sequence classifier-এর accuracy (83.73%/82.48%) প্রায় একই স্তরে — অর্থাৎ বিশাল reasoning model-এর accuracy সস্তা 128-dim embedding model-এর মতোই। (সতর্কতা: dataset ও split ভিন্ন হতে পারে; সরাসরি তুলনা নয়।) আমার হিসাবে PATCH-SIM subset-এ Tree model-এর specificity প্রায় 37%, RePaCA-র 16/30 = 53%; দুটোই কম specificity-র সমস্যা দেখায়, কিন্তু অনুমান-ভিত্তিক।
- **Sub-domain 2, APR survey:** inconsistent correctness definition ও leakage-র সমস্যা এখানেও (random CV, developer patch confound)।
- **Sub-domain 1, AutoCodeRover/Agentless:** agent patch-এর plausible ≠ correct (CG1) সমস্যা; এই paper দেখায় static classifier কী পারে (ও কী পারে না)।
- **Sub-domain 3, SWE-rebench/Pro:** fresh task ও contamination-মুক্ত evaluation-এর ধারণা এই paper-এ নেই; আমরা সেটি আনতে পারি।
- **Sub-domain 4, Oracle-Guided Selection:** distinguishing test (dynamic) এই paper-এর static score-এর পরিপূরক; একটি static, একটি dynamic signal আলাদা রাখা আমাদের assurance report-এর কাঠামোর সাথে মেলে।

## ১৮. Supervisor Q&A

**প্রশ্ন ১: সেরা representation কোনটি?**
উত্তর: গড়ে graph (CPG+GGNN accuracy 83.73%, average 83.81%), কিন্তু TreeLSTM+AST (82.94%) ও Transformer (82.48%) খুব কাছে; ফারাক 1 pp-এর কাছাকাছি, significance test নেই, তাই "consistently" দাবি শক্ত নয়।

**প্রশ্ন ২: Static classifier কি RePaCA-র চেয়ে ভালো?**
উত্তর: সরাসরি তুলনা করা যায় না (dataset/split ভিন্ন)। RePaCA-র 83.1% Defects4J-তে, এখানে random 5-fold-এ 83.73%। অনুপাত প্রায় সমান; আমাদের নতুন কাজ হলো একই dataset ও split-এ দুটোকে তুলনা করা।

**প্রশ্ন ৩: Generalisation (CG9, CG10) সম্পর্কে এই paper কী বলে?**
উত্তর: প্রায় কিছুই না। শুধু Defects4J Java; random split; authors নিজেরাই cross-project evaluation-কে future work বলেছে (§৫.৩)।

**প্রশ্ন ৪: Precision/recall/specificity trade-off কেমন?**
উত্তর: Recall ~87% ও precision ~81% (CPG+GGNN)। Specificity report নেই; আমার হিসাবে প্রায় 80.7% (Table 1 অনুপাত ধরে)। SVM-এ ধস: recall 90%+ কিন্তু accuracy ~50%।

**প্রশ্ন ৫: Dataset-এর সবচেয়ে বড় ঝুঁকি কী?**
উত্তর: Correct class-এর 965/1169 developer patch — model "কে লিখেছে" শিখতে পারে; এবং class প্রায় 51/49, বাস্তবে correct অনেক কম।

**প্রশ্ন ৬: Fusion থেকে আমরা কী শিখি?**
উত্তর: দুটি মেলানো ভালো (Heu-Seq backend average 85.95%), বেশি মেলালে ভালো হয় না; naive fusion-এর কারণে। Learned fusion ভবিষ্যৎ কাজ।

**প্রশ্ন ৭: Pre-trained model ছাড়া কেন এই study?**
উত্তর: Authors representation-এর প্রভাব আলাদা করতে চেয়েছেন (controlled setting); পরে CodeBERT/CodeT5 modest উন্নতি (83.98%/83.61% average) দেখিয়েছে।

**প্রশ্ন ৮: Paper-এ কোনো সংখ্যার গরমিল আছে?**
উত্তর: হ্যাঁ — class label উল্টো লেখা (§৩.৬ বনাম Table 1), abstract-এর 87.09% (TreeLSTM বলা, আসলে CPG+GGNN-এর recall), Table 2-এর duplicate row, model-সংখ্যা 45 বনাম আমার গণনা 44 (বিস্তারিত §১২)।

## ১৯. Glossary

| শব্দ | অর্থ |
|---|---|
| APCA | Automated Patch Correctness Assessment |
| Plausible patch | Test pass করা patch |
| Overfitting patch | Test pass করে কিন্তু incorrect |
| AST | Abstract Syntax Tree |
| CFG/CDG/DDG/PDG/CPG | Control-flow, control-dependency, data-dependency, program-dependency, code property graph |
| GGNN | Gated Graph Neural Network (GRU দিয়ে node update) |
| TreeLSTM | Tree-structured LSTM |
| TF-IDF | Term frequency–inverse document frequency |
| Intermediate/backend fusion | Feature concatenate / model probability গড় |
| Specificity | Correct patch-কে correct বলার হার |
| PCM | Pre-trained code model |

## ২০. Summary card

| বিষয় | মান |
|---|---|
| Paper | Zhang et al., arXiv 2603.07520v2, April 2026 |
| Data | 2,274 patches (1,169 correct, 1,105 overfitting), Defects4J, 39 rows |
| Best single | DDG+GGNN accuracy 83.95%; CPG+GGNN 83.73% (Table 5/6) |
| Best fusion | Heu-Seq backend average 85.95% (Table 7) |
| Pre-trained | CodeBERT average 83.98% (Table 9) |
| Sequence vs graph | 82.48% vs 83.73% accuracy |
| PATCH-SIM (139) | Tree: acc 80, prec 84, rec 91, F1 88; PATCH-SIM: 66/100/57/73 |
| Specificity (আমার হিসাব) | CPG+GGNN ≈ 80.7%; Tree on PATCH-SIM set ≈ 37% (অনুমান) |
| Main weakness | Random CV, developer-patch confound (82.5% of correct), no variance, Java-only |
| আমাদের ব্যবহার | Cheap static signal; leakage-free re-evaluation = SPL3 publication angle |

## ২১. বর্তমান (2026) প্রেক্ষাপট

### ২১.১ তখন বনাম এখন

| বিষয় | Paper-এর সময় (Defects4J, 39 পুরনো APR tool) | এখন (context.md থেকে) |
|---|---|---|
| Patch source | Genetic/template/NMT-ভিত্তিক tool | Agent/LLM (Claude Opus 5.5, GPT-6 family ইত্যাদি) patch লেখে; এই distribution-এ APCA classifier পরীক্ষিত নয় — "বর্তমান model-এর তথ্য পাওয়া যায়নি" |
| Patch-correctness judge | Trained classifier (representation) | Plain-LLM judge ComPass 62.14% overfitting detection (S, search-snippet); judge "over-fix" flag-এ precision 5–10% (S) |
| Overfitting মাত্রা | Defects4J label | PatchDiff: 29.6% plausible patch gold-এর থেকে ভিন্ন আচরণ করে (I, পুরনো model) |
| Benchmark | Defects4J | SWE-bench Verified saturated (Vals.ai 97.0%, I); SWE-Bench Pro Verified-এ leakage বন্ধ করলে GLM-5.2 78.80% → 57.32% (I) |
| Test quality | Developer test-suite | 80.2% agent-লেখা test patch-এ weak/no oracle (I) |

### ২১.২ কী এখনও সত্য / কী পুরনো

**এখনও সত্য:**
- Plausible ≠ correct (CG1): PatchDiff-এর 29.6% (I) একই সমস্যা নিশ্চিত করে।
- Random split ও label-source confound সমস্যা পুরনো হয়নি; বরং agent-patch-এ আরও বড় (leakage-এ 78.80% → 57.32%, I)।
- Recall/specificity trade-off: judge-দের নিম্ন precision (5–10%, S) একই শ্রেণির সমস্যা।

**পুরনো/সীমিত:**
- 39 পুরনো APR tool-এর patch; আজকের agent-patch-এ এই 83.73% প্রযোজ্য কি না অজানা।
- "LLM-কে future work" বলা — এখন LLM judge বাস্তব (ComPass 62.14%, S), অর্থাৎ ছোট classifier-এর 83% সংখ্যার সাথে সরাসরি তুলনা অনুপযুক্ত (ভিন্ন dataset)।
- Defects4J-এর contamination ঝুঁকি আজকের LLM-এ বেশি (CG6)।

### ২১.৩ আজ খোলা gap

| Gap | অবস্থা (2026) | CG |
|---|---|---|
| Agent-generated patch-এ representation-based classifier-এর সংখ্যা | কোনো সংখ্যা পাওয়া যায়নি | CG1, CG9 |
| Classifier বনাম reasoning judge একই split-এ | তথ্য পাওয়া যায়নি | CG1, CG10 |
| Gaming: agent hidden test বা git ইতিহাস লুকায় (V) — classifier এটি ধরতে পারে কি | অজানা | CG12 |
| Version-bound validity (নতুন model-এর patch drift) | অজানা | CG11 |
| Security-sensitive patch-এ correctness classifier (SusVibes FuncPass 62–84% বনাম SecPass 7.8–17.3%, I) | কোনো APCA study নেই | CG5 |

### ২১.৪ SPL3 idea (বর্তমান model, cost-aware)

- **Cheap static triage:** TF-IDF+XGBoost বা CodeBERT classifier আগে চালানো (প্রায় শূন্য খরচ); যেগুলো "অনিশ্চিত", শুধু সেগুলোর জন্য LLM judge ডাকা। Cost reference: Vals Terminal-Bench 4.0-এ per-task খরচ Opus 5.5 13.20 USD, Kimi K3.1 Pro 4.57 USD, GPT-6.1 Sol 1.72 USD (I) — অর্থাৎ বড় model দিয়ে প্রতিটি patch judge করা ব্যয়বহুল।
- **Evaluation:** fresh SWE-rebench task ও SWE-Bench Pro Verified subset-এ agent patch; bug-grouped ও model-held-out split; recall ও specificity দুটোই; multiple run (pass@1 বনাম pass@5-এর 12–18 pt ফারাক, I)।
- **Report:** static score, LLM-judge score ও dynamic test-সংকেত আলাদা ও version-সহ; "could not verify" স্পষ্ট ফলাফল।
- সতর্কতা: এই idea-র কোনো সংখ্যা আমরা এখনও মাপিনি; উপরের সব current-model সংখ্যা context.md-এর (V/I/S লেবেল সহ)।

### ২১.৫ তিনটি Q&A

**প্রশ্ন ১: আজকের Opus 5.5-এর patch-এ এই classifier কেমন কাজ করবে?**
উত্তর: বর্তমান model-এর তথ্য পাওয়া যায়নি। Training data পুরনো tool-এর, তাই distribution shift প্রত্যাশিত; আমাদের প্রথম পরীক্ষা এটিই।

**প্রশ্ন ২: LLM judge থাকতে ছোট classifier কেন?**
উত্তর: খরচ ও সংকেতের আলাদা ধরন। Judge-এর কিছু ক্ষেত্রে precision কম (5–10% over-fix flag, S) এবং ব্যয়বহুল; classifier সস্তা triage দেয়। তবে classifier-এর নিজের generalisation অপরীক্ষিত।

**প্রশ্ন ৩: এই paper-এর কোন অংশ আজও অবিতর্কিত?**
উত্তর: "একটি representation সব সময় সেরা নয়, model-নির্বাচন গুরুত্বপূর্ণ" এবং "দুটির সরল fusion সস্তা উপকার দেয়" — তবে দুটোই Defects4J-random-CV-তে প্রমাণিত, নতুন প্রেক্ষাপটে নয়।
