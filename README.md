# Machine Learning Course Project

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.0%2B-F7931E.svg?logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0%2B-EE4C2C.svg?logo=pytorch&logoColor=white)](https://pytorch.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebooks-orange.svg?logo=jupyter&logoColor=white)](https://jupyter.org/)
[![Institution](https://img.shields.io/badge/IIIT%20Sri%20City-CSE%20Department-003366.svg)](https://www.iiits.ac.in/)

> **Course:** Machine Learning (5th Semester)  
> **Department:** Computer Science & Engineering, Indian Institute of Information Technology, Sri City  
> **Authors:**
> - **Yashasvee Patel** — `S20240010266`
> - **P Karthik** — `S20240010184`

---

## 📌 Table of Contents
1. [Project Overview](#-project-overview)
2. [Project Report & Presentation Deliverables](#-project-report--presentation-deliverables)
3. [Question 1: Supervised Classification (UCI Spambase)](#-question-1-supervised-classification)
4. [Question 2: Non-Linear Regression & Regularization (Superconductivity)](#-question-2-non-linear-regression--regularization)
5. [Question 3: Unsupervised Clustering & PCA (HELP International)](#-question-3-unsupervised-clustering--pca)
6. [Master Synthesis & Key Takeaways](#-master-synthesis--key-takeaways)
7. [Repository Structure](#-repository-structure)
8. [Setup & Quickstart](#-setup--quickstart)

---

## 🌟 Project Overview

This repository contains our comprehensive, mathematically rigorous solutions to the Machine Learning Course Project. The study investigates three core paradigms of machine learning across distinct empirical domains:

1. **Supervised Binary Classification:** Predicting email spam using instance-based (KNN), tree-based (CART), maximum-margin (SVM RBF), and deep convolutional (1D CNN) models.
2. **Supervised Continuous Regression:** Predicting superconductor critical temperatures ($T_c$) using Linear SGD, Ridge ($L_2$), Lasso ($L_1$), polynomial degree sweeps (1 to 4), and high-dimensional interaction modeling.
3. **Unsupervised Clustering & Dimensionality Reduction:** Segmenting 167 nations for equitable foreign aid allocation using K-Means and deriving Principal Component Analysis (PCA) strictly from mathematical first principles (sample covariance eigendecomposition).

### 🛡️ Experimental Rigor & Zero Data Leakage Guarantee
Across all three problem sets:
- **Strict 80/20 Train-Test Splits:** Test sets are sequestered prior to any feature transformation or modeling.
- **Pipeline Encapsulation:** All scalers (`StandardScaler`) are encapsulated strictly inside `scikit-learn` `Pipeline` objects. This prevents validation fold statistics from contaminating training folds during cross-validation.
- **Statistical Significance:** Model comparisons are evaluated via 5-fold cross-validation and 1,000 bootstrap resamples for 95% confidence intervals on ROC-AUC.

---

## 📄 Project Report & Presentation Deliverables

| Deliverable | File Link | Description |
|:---|:---|:---|
| **Full Project Report (PDF)** | [**`ML_Project_Report.pdf`**](ML_Project_Report.pdf) | Complete 25-page formal technical report detailing mathematical formulations, cross-validation curves, confusion matrices, capacity analyses, factor loadings, and empirical conclusions. |
| **PowerPoint Presentation Deck** | [**`ML_Course_Project_Presentation.pptx`**](ML_Course_Project_Presentation.pptx) | Concise, high-impact 16:9 widescreen presentation deck (12 slides) with dark/light themes, clean metric cards, formatted benchmark tables, embedded figures, and integrated speaker notes on every slide. |

---

## 📧 Question 1: Supervised Classification

**Dataset:** UCI Spambase — 4,601 email records, 57 continuous features (48 word frequencies, 6 character frequencies, 3 capital run-length metrics).  
**Class Balance:** 1,813 Spam (39.4%) vs. 2,788 Ham (60.6%). Stratified 80/20 train/test split (3,680 train / 921 test).  
**Notebook:** [`Question1_Classification/Question1_Classification.ipynb`](Question1_Classification/Question1_Classification.ipynb)

### Evaluated Model Suite
1. **K-Nearest Neighbour (KNN):** Distance-based instance classifier. 5-fold CV swept $k \in [1, 21]$; optimal $k=3$ achieved 90.76% CV accuracy.
2. **Decision Tree (CART):** Recursive axis-aligned binary partitioning optimizing Gini impurity drops. Swept `max_depth` from 2 to 25; optimal depth $d=12$ selected (91.85% CV accuracy).
3. **Support Vector Machine (RBF Kernel):** Soft-margin hyperplane in infinite-dimensional RKHS with $K(x, x') = \exp(-\gamma ||x - x'||^2)$. Logarithmic grid sweep over $C \in [0.1, 100]$; optimal $C=5.0$, $\gamma=\text{'scale'}$ achieved 93.15% CV accuracy.
4. **Deep 1D CNN (Bonus PyTorch Architecture):** 3 Conv1d blocks (32 → 64 → 128 channels, kernel=3), BatchNorm1d, ReLU, Dropout (0.3), Global Average Pooling, Adam optimizer ($lr=10^{-3}$, 40 epochs).

### Quantitative Test Results (N = 921 Test Emails)

| Classifier | Accuracy | Precision | Recall | F1-Score | ROC-AUC | 95% Bootstrap CI |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **KNN ($k=3$)** | 89.79% | 87.26% | 86.78% | 0.8702 | 0.9360 | [0.919, 0.951] |
| **Decision Tree ($d=12$)** | 91.97% | 90.70% | 88.71% | 0.8969 | 0.9023 | [0.876, 0.925] |
| **SVM (RBF, $C=5.0$) 🏆** | **92.40%** | **92.22%** | 88.15% | **0.9014** | 0.9697 | [0.959, 0.979] |
| **Deep 1D CNN** | 91.53% | 89.26% | **89.26%** | 0.8926 | **0.9718** | [0.961, 0.981] |

### Key Classification Findings
- **Asymmetric Cost of Errors:** In email filtering, False Positives (legitimate email sent to spam) are far more harmful than False Negatives. SVM achieved the highest Precision (92.22%) with only 27 False Positives out of 558 legitimate emails.
- **Statistical Tie via Bootstrap Resampling:** While the Deep CNN had a higher point estimate for ROC-AUC (0.9718 vs 0.9697), their 1,000 bootstrap 95% confidence intervals heavily overlap ([0.961, 0.981] vs [0.959, 0.979]). SVM was chosen as the champion model due to higher precision, top F1, zero GPU requirements, and deterministic convex optimization.

---

## ⚡ Question 2: Non-Linear Regression & Regularization

**Dataset:** UCI Superconductivity — 21,263 superconductor samples, 81 continuous elemental features derived from 8 atomic properties (atomic mass, ionization energy, atomic radius, density, electron affinity, fusion heat, thermal conductivity, valence).  
**Target:** Critical transition temperature $T_c \in [0.00021\text{ K}, 185\text{ K}]$, Mean $34.42\text{ K}$. Stratified 80/20 train/test split (17,010 train / 4,253 test).  
**Notebook:** [`Question2_Regression/solution2.ipynb`](Question2_Regression/solution2.ipynb) *(consolidated solution containing all models, cross-validation, degree sweeps, and final evaluation)*

### Evaluated Model Suite & Regularization
- **Linear Regression via SGD:** Iterative gradient descent baseline without penalty. Converged in 62 iterations to $R^2 = 0.7332$ and $\text{RMSE} = 17.52\text{ K}$.
- **Ridge Regression ($L_2$):** Penalizes $\alpha ||w||_2^2$ to stabilize collinear atomic aggregates. Optimal $\alpha=0.1$ reached $R^2 = 0.7375$ ($\text{RMSE} = 17.38\text{ K}$).
- **Lasso Regression ($L_1$):** Enforces feature sparsity via $\alpha ||w||_1$. Optimal $\alpha=10^{-5}$ reached $R^2 = 0.7375$.
- **The Linear Ceiling:** All linear models hit a hard ceiling at $R^2 \approx 0.738$. Collinearity shrinkage prevents coefficient blowup but cannot overcome linear high bias on quantum phenomena.
- **Polynomial Degree Sweep (Degrees 1 to 4):**
  - *Degree 1 (15 terms):* High bias ($R^2 \approx 0.735$).
  - *Degree 2 (135 terms):* Balanced baseline ($R^2 = 0.7348$).
  - *Degree 3 (815 terms):* Train $R^2$ climbs to 0.81 while test error degrades.
  - *Degree 4 (3,875 terms):* Catastrophic variance explosion! Ill-conditioned Vandermonde matrix causes test MSE to explode to negative millions.

### The Breakthrough: Full 81-Feature Polynomial Ridge
Expanding all 81 elemental features to degree-2 generates **3,402 pairwise interaction terms**. Regularized by Ridge ($\alpha=10.0$):
- **Test $R^2$ surged from 0.7332 to 0.8542 (+16.5% relative gain)**
- **Test RMSE plunged from 17.52 K to 12.95 K (-26.1% error reduction)**

| Regression Model | Configuration | Test MSE ($K^2$) | Test RMSE ($K$) | Test $R^2$ Score |
|:---|:---|:---:|:---:|:---:|
| **Linear Regression (SGD)** | loss='squared_error', penalty=None | 307.09 | 17.52 K | 0.7332 |
| **Ridge Regression** | $\alpha=0.1$ (all 81 features) | 302.15 | 17.38 K | 0.7375 |
| **Lasso Regression** | $\alpha=10^{-5}$ (all 81 features) | 302.20 | 17.38 K | 0.7375 |
| **Polynomial Ridge (Top 15)** | Degree-2 (135 terms), Ridge $\alpha=0.01$ | 305.24 | 17.47 K | 0.7348 |
| **Polynomial Ridge (All 81) 🏆** | **Degree-2 (3,402 terms), Ridge $\alpha=10.0$** | **167.79** | **12.95 K** | **0.8542** |

---

## 🌍 Question 3: Unsupervised Clustering & PCA

**Dataset:** HELP International Country Socio-Economic Dataset — 167 nations evaluated on 9 development and health indicators (`child_mort`, `exports`, `health`, `imports`, `income`, `inflation`, `life_expec`, `total_fer`, `gdpp`).  
**Preprocessing:** Zero-mean unit-variance Standardization ($x_{ij}^{norm} = \frac{x_{ij} - \mu_j}{\sigma_j}$) to prevent raw GDP (up to \$105,000) from dominating Euclidean distances over child mortality and fertility.  
**Notebook:** [`Question3_Clustering_and_PCA/Question3_Clustering_and_PCA.ipynb`](Question3_Clustering_and_PCA/Question3_Clustering_and_PCA.ipynb)

### K-Means Clustering: Elbow Method & Silhouette Analysis
Lloyd's algorithm minimizing within-cluster sum of squares ($\text{WCSS}$) with 10 restarts:

| Clusters ($K$) | WCSS (Inertia) | Absolute Drop | % Reduction | Silhouette Score |
|:---:|:---:|:---:|:---:|:---:|
| $K = 2$ | 1050.21 | — | — | 0.2874 |
| **$K = 3$ 🏆** | **831.42** | **218.79** | **20.8%** | **0.2833** |
| $K = 4$ | 700.70 | 130.72 | 15.7% | 0.3037 |
| $K = 5$ | 632.16 | 68.54 | 9.8% | 0.2180 |
| $K = 6$ | 576.66 | 55.50 | 8.8% | 0.2224 |

*Selection Justification:* While $K=4$ reached a mathematical peak in silhouette score (0.3037), $K=3$ was selected based on the WCSS elbow drop (20.8% reduction with diminishing returns beyond) and actionable international policy alignment:
- **Cluster 0 (36 nations - Developed):** High GDP (\$42.5k), high life expectancy (80.1 yr), low child mortality (5.0).
- **Cluster 1 (47 nations - Underdeveloped / Urgent Aid Priority):** Severe poverty, low GDP (\$1,909), low life expectancy (56.6 yr), child mortality 92.96 (Haiti, Afghanistan, Mali).
- **Cluster 2 (84 nations - Developing):** Intermediate income (\$12.3k), GDP (\$6.5k), life expectancy 73.1 yr (India, Brazil, Indonesia).

### PCA from First Principles: Mathematical Eigendecomposition
Implemented strictly from scratch using the sample covariance matrix $\Sigma = \frac{1}{N-1} X_{norm}^T X_{norm} \in \mathbb{R}^{9 \times 9}$ and solving $\Sigma v_k = \lambda_k v_k$:

- **PC1 ($\lambda_1 = 4.1606$, EVR = 45.95%):** Represents *Socio-Economic Development & Health*. Loaded heavily by `life_expec` (+0.43), `income` (+0.40), `gdpp` (+0.39) vs `child_mort` (-0.42), `total_fer` (-0.40).
- **PC2 ($\lambda_2 = 1.5557$, EVR = 17.18%):** Represents *Trade Openness*. Dominated by `imports` (+0.67) and `exports` (+0.61). Isolates international trade hubs (Singapore, Luxembourg, Malta).
- **PC3 ($\lambda_3 = 1.1774$, EVR = 13.00%):** Represents *Macroeconomic Stability*. Contrasts public healthcare investment (`health` +0.60) against inflation volatility (`inflation` -0.64).
- **Variance Truncation:** Top 3 components capture **76.14% cumulative variance**, reducing dimensionality from 9 to 3 with minimal information loss.
- **Geometrical Harmony:** 2D and 3D PCA projections overlaid with K-Means clusters display clean, non-overlapping partitions, validating the continuous spectral equivalence between PCA and K-Means.

---

## 🏆 Master Synthesis & Key Takeaways

| Problem Domain | Evaluated Suite | Champion Model | Optimal Configuration | Test Performance |
|:---|:---|:---|:---|:---|
| **Q1: Classification** | KNN, CART DT, SVM RBF, 1D CNN | **SVM (RBF Kernel)** | $C=5.0$, $\gamma=\text{'scale'}$ | **Acc: 92.40%** · Prec: 92.22% · F1: 0.9014 · AUC: 0.9697 |
| **Q1 Bonus: Deep Learning** | Deep 1D Convolutional Net | **Deep 1D CNN** | 3 Conv Blocks, Adam $10^{-3}$ | Acc: 91.53% · Recall: 89.26% · **AUC: 0.9718** |
| **Q2: Regression** | SGD, Ridge, Lasso, Poly (1-4) | **Poly Ridge (All 81)** | Degree-2, Ridge $\alpha=10.0$ | **$R^2$: 0.8542** · **RMSE: 12.95 K** (-26.1% error) |
| **Q3: Clustering & PCA** | K-Means, Covariance PCA | **K-Means ($K=3$) & PCA** | Lloyd's, Top 3 PCs | **WCSS: 831.42** · **Cumul. Var: 76.14%** |

### Fundamental Machine Learning Lessons
1. **Feature Standardization is Mandatory:** Distance-based (KNN, K-Means) and margin-based (SVM) algorithms require scaling; otherwise high-magnitude features disproportionately skew decisions.
2. **Prevent Data Leakage:** Placing scalers within pipelines guarantees validation data remains strictly out-of-sample.
3. **Representation Learning Beats Linear Tuning:** Capturing 3,402 atomic interactions in regression delivered a 16.5% boost in $R^2$, far outpacing linear regularization tuning.
4. **Statistical Rigor:** 1,000 bootstrap resamples on ROC-AUC prevented false superiority claims between SVM and CNN.

---

## 📂 Repository Structure

```
ML-course/
├── README.md                                  # Comprehensive technical report & documentation
├── ML_Project_Report.pdf                      # Complete 25-page formal technical report (PDF)
├── ML_Course_Project_Presentation.pptx        # 12-slide widescreen PowerPoint presentation deck
├── .gitignore                                 # Git ignore patterns
│
├── Question1_Classification/
│   ├── Question1_Classification.ipynb         # Complete Classification solution & experiments
│   ├── Q1_(a)_.ipynb                          # Exploratory Question 1 notebook
│   └── Data/
│       └── spambase.csv                       # UCI Spambase dataset (4,601 records)
│
├── Question2_Regression/
│   ├── solution2.ipynb                        # Unified Regression solution (SGD, Ridge, Lasso, Poly)
│   └── superconductivty+data/
│       ├── train.csv                          # Superconductivity training dataset (21,263 samples)
│       └── unique_m.csv                       # Chemical composition formulas
│
└── Question3_Clustering_and_PCA/
    ├── Question3_Clustering_and_PCA.ipynb     # From-scratch K-Means & PCA implementations & validation
    └── archive/
        ├── Country-data.csv                   # HELP International country dataset (167 nations)
        └── data-dictionary.csv                # Socio-economic indicator descriptions
```

---

## ⚙️ Setup & Quickstart

### 1. Clone the Repository
```bash
git clone https://github.com/Karthik-124/ML-course.git
cd ML-course
```

### 2. Create and Activate Virtual Environment
```bash
python -m venv .venv

# Windows:
.venv\Scripts\activate

# macOS / Linux:
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install numpy pandas scikit-learn matplotlib seaborn torch python-pptx jupyter
```

### 4. Run Notebooks
```bash
jupyter lab
```

---

<p align="center">
  <b>Department of Computer Science & Engineering · Indian Institute of Information Technology, Sri City</b><br>
  <i>Submitted by Yashasvee Patel (S20240010266) & P Karthik (S20240010184)</i>
</p>
