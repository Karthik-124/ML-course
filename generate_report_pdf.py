"""
Generates the ML project report PDF using ReportLab.
Run after generate_report_figures.py has completed.
"""
import os, textwrap
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm, mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Image,
                                 Table, TableStyle, PageBreak, HRFlowable,
                                 KeepTogether)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import numpy as np

W, H = A4
MARGIN = 2*cm
FIG = 'report_figures'
OUT = 'ML_Project_Report.pdf'

# ── Colour palette ──────────────────────────────────────────────────────────
DARK_BLUE  = colors.HexColor('#1e3a5f')
MID_BLUE   = colors.HexColor('#2563eb')
LIGHT_BLUE = colors.HexColor('#dbeafe')
GREEN      = colors.HexColor('#16a34a')
LIGHT_GREEN= colors.HexColor('#d4edda')
RED        = colors.HexColor('#dc2626')
GRAY       = colors.HexColor('#6b7280')
LGRAY      = colors.HexColor('#f3f4f6')
WHITE      = colors.white

# ── Styles ───────────────────────────────────────────────────────────────────
SS = getSampleStyleSheet()

def style(name='Normal', **kw):
    return ParagraphStyle(name, parent=SS[name], **kw)

S = {
    'title':   style('Title',   fontSize=26, textColor=DARK_BLUE, leading=32, alignment=TA_CENTER, spaceAfter=6),
    'sub':     style('Normal',  fontSize=13, textColor=MID_BLUE,  leading=18, alignment=TA_CENTER, spaceAfter=4),
    'h1':      style('Heading1',fontSize=15, textColor=DARK_BLUE, leading=20, spaceBefore=18, spaceAfter=8, borderPad=4),
    'h2':      style('Heading2',fontSize=12, textColor=MID_BLUE,  leading=16, spaceBefore=12, spaceAfter=6),
    'h3':      style('Heading3',fontSize=10.5,textColor=colors.HexColor('#1d4ed8'), leading=14, spaceBefore=8, spaceAfter=4),
    'body':    style('Normal',  fontSize=10, leading=15, spaceAfter=6, alignment=TA_JUSTIFY),
    'math':    style('Normal',  fontSize=10, leading=16, spaceAfter=4, leftIndent=18, fontName='Courier',
                     backColor=LGRAY, borderPad=4),
    'bullet':  style('Normal',  fontSize=10, leading=14, leftIndent=18, spaceAfter=3, bulletIndent=8),
    'caption': style('Normal',  fontSize=8.5,leading=12, textColor=GRAY, alignment=TA_CENTER, spaceAfter=6),
    'toc_h1':  style('Normal',  fontSize=11, leading=15, leftIndent=0,  spaceAfter=3),
    'toc_h2':  style('Normal',  fontSize=10, leading=14, leftIndent=12, spaceAfter=2, textColor=GRAY),
    'small':   style('Normal',  fontSize=9,  leading=13, textColor=GRAY),
    'center':  style('Normal',  fontSize=10, leading=15, alignment=TA_CENTER),
}

def P(text, s='body'): return Paragraph(text, S[s])
def H1(t): return P(f'<b>{t}</b>', 'h1')
def H2(t): return P(t, 'h2')
def H3(t): return P(t, 'h3')
def SP(n=8): return Spacer(1, n)
def HR(): return HRFlowable(width='100%', thickness=0.5, color=LGRAY, spaceAfter=4, spaceBefore=4)
def Fig(fname, w=14*cm, caption=''):
    path = f'{FIG}/{fname}'
    if not os.path.exists(path):
        return [P(f'[Figure missing: {fname}]', 'small')]
    items = [Image(path, width=w, height=w*0.6), SP(2)]
    if caption:
        items.append(P(f'<i>{caption}</i>', 'caption'))
    return items
def Math(expr): return P(expr, 'math')
def Bullet(items):
    return [P(f'• {it}', 'bullet') for it in items]

def section_header(story, number, title):
    story.append(SP(10))
    story.append(HRFlowable(width='100%', thickness=2, color=DARK_BLUE, spaceBefore=6, spaceAfter=2))
    story.append(P(f'<b>{number}.  {title}</b>', 'h1'))
    story.append(HRFlowable(width='100%', thickness=0.5, color=MID_BLUE, spaceAfter=8))

# ── Page template with header/footer ─────────────────────────────────────────
class MyDocTemplate(SimpleDocTemplate):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.page_no_offset = -1   # title page = page 1 but no number shown

    def handle_pageEnd(self):
        super().handle_pageEnd()

def on_page(canvas, doc):
    canvas.saveState()
    page = canvas.getPageNumber()
    # Header (skip title page = page 1)
    if page > 1:
        canvas.setFillColor(DARK_BLUE)
        canvas.setFont('Helvetica-Bold', 8)
        canvas.drawString(MARGIN, H - 1.2*cm, 'ML Course Project Report  |  IIIT Sri City')
        canvas.drawRightString(W - MARGIN, H - 1.2*cm, 'Machine Learning Assignments — 2026')
        canvas.setStrokeColor(MID_BLUE); canvas.setLineWidth(0.5)
        canvas.line(MARGIN, H - 1.4*cm, W - MARGIN, H - 1.4*cm)
        # Footer
        canvas.setFont('Helvetica', 8); canvas.setFillColor(GRAY)
        canvas.drawString(MARGIN, 1.1*cm, 'Yashasvee Patel (S20240010266)  |  P Karthik (S20240010184)')
        canvas.drawRightString(W - MARGIN, 1.1*cm, f'Page {page - 1}')
        canvas.setStrokeColor(LGRAY)
        canvas.line(MARGIN, 1.4*cm, W - MARGIN, 1.4*cm)
    canvas.restoreState()

# ═══════════════════════════════════════════════════════════════════════════════
# BUILD STORY
# ═══════════════════════════════════════════════════════════════════════════════
story = []

# ─── TITLE PAGE ──────────────────────────────────────────────────────────────
story.append(Spacer(1, 3*cm))
story.append(P('INDIAN INSTITUTE OF INFORMATION TECHNOLOGY', 'sub'))
story.append(P('<b>SRI CITY, CHITTOOR</b>', 'sub'))
story.append(SP(20))
story.append(HRFlowable(width='80%', thickness=2, color=MID_BLUE, spaceAfter=16))
story.append(P('<b>Machine Learning Course Project</b>', 'title'))
story.append(P('Classification · Regression · Clustering &amp; PCA', 'sub'))
story.append(HRFlowable(width='80%', thickness=2, color=MID_BLUE, spaceBefore=16, spaceAfter=30))
story.append(SP(30))

meta = [
    ['Submitted by', 'Yashasvee Patel'],
    ['Roll Number',  'S20240010266'],
    ['',             ''],
    ['',             'P Karthik'],
    ['',             'S20240010184'],
    ['',             ''],
    ['Course',       'Machine Learning (ML)'],
    ['Academic Year','2025–26'],
    ['Deadline',     '31st October 2026'],
]
t = Table(meta, colWidths=[5*cm, 9*cm])
t.setStyle(TableStyle([
    ('FONTNAME',  (0,0),(-1,-1), 'Helvetica'),
    ('FONTSIZE',  (0,0),(-1,-1), 11),
    ('FONTNAME',  (0,0),(0,-1),  'Helvetica-Bold'),
    ('TEXTCOLOR', (0,0),(0,-1),  DARK_BLUE),
    ('ALIGN',     (0,0),(-1,-1), 'LEFT'),
    ('TOPPADDING',(0,0),(-1,-1), 5),
    ('BOTTOMPADDING',(0,0),(-1,-1), 5),
]))
story.append(t)
story.append(Spacer(1, 2*cm))
story.append(P('Total Marks: <b>30</b> + <b>5 Bonus</b>', 'center'))
story.append(PageBreak())

# ─── TABLE OF CONTENTS ───────────────────────────────────────────────────────
story.append(SP(10))
story.append(P('<b>Table of Contents</b>', 'h1'))
story.append(HR())
toc_items = [
    ('1.', 'Abstract', '3'),
    ('2.', 'Introduction', '3'),
    ('3.', 'Question 1 — Classification (10 Marks)', '4'),
    ('  3.1', 'Dataset & Preprocessing', '4'),
    ('  3.2', 'Algorithm Overview & Mathematics', '4'),
    ('  3.3', 'Experimental Results', '7'),
    ('  3.4', 'Comparison & Best Classifier', '8'),
    ('4.', 'Question 2 — Regression (10 Marks)', '9'),
    ('  4.1', 'Dataset & Preprocessing', '9'),
    ('  4.2', 'Algorithm Overview & Mathematics', '9'),
    ('  4.3', 'Experimental Results', '12'),
    ('  4.4', 'Comparison', '13'),
    ('5.', 'Question 3 — Clustering & PCA (10 Marks)', '14'),
    ('  5.1', 'Dataset', '14'),
    ('  5.2', 'K-Means Clustering from Scratch', '14'),
    ('  5.3', 'PCA from Scratch', '16'),
    ('6.', 'Conclusion', '19'),
]
for num, title, pg in toc_items:
    indent = 12 if num.startswith('  ') else 0
    is_sub = num.startswith('  ')
    toc_style = ParagraphStyle(
        f'toc_{num.strip()}',
        parent=SS['Normal'],
        fontSize=9 if is_sub else 10,
        leading=14,
        leftIndent=indent,
        spaceAfter=3 if is_sub else 5,
        textColor=GRAY if is_sub else DARK_BLUE,
    )
    dots = '.' * max(1, 55 - len(num) - len(title) - indent//2)
    story.append(Paragraph(
        f'<font color="#6b7280">{num}</font>  {title} '
        f'<font color="#9ca3af">{dots}</font> '
        f'<font color="#1e3a5f"><b>{pg}</b></font>',
        toc_style
    ))
story.append(PageBreak())

# ─── 1. ABSTRACT ─────────────────────────────────────────────────────────────
section_header(story, 1, 'Abstract')
story.append(P(
    'This report presents solutions to a three-part Machine Learning course project covering supervised and '
    'unsupervised learning paradigms. In Question 1, four classification algorithms — K-Nearest Neighbour (KNN), '
    'Decision Tree, Support Vector Machine with RBF kernel, and a Bonus Deep 1D Convolutional Neural Network — '
    'are implemented and compared on the UCI Spambase dataset (4,601 samples, 57 features). '
    'In Question 2, four regression models — Linear Regression with Gradient Descent, Polynomial Regression, '
    'Ridge Regression, and Lasso Regression — are evaluated on the UCI Superconductivity dataset '
    '(21,263 samples, 81 features). '
    'In Question 3, K-Means Clustering and Principal Component Analysis (PCA) are both implemented '
    '<b>entirely from scratch</b> using NumPy on the HELP International Country dataset (167 countries, 9 indicators). '
    'For each task, datasets are split 80/20, appropriate metrics are computed, overfitting is analysed, '
    'cross-validation is used for hyperparameter selection, and results are compared comprehensively.'
))

# ─── 2. INTRODUCTION ─────────────────────────────────────────────────────────
section_header(story, 2, 'Introduction')
story.append(P(
    'Machine Learning enables systems to learn patterns from data and make predictions or decisions without being '
    'explicitly programmed. This project explores three fundamental ML paradigms:'
))
story += Bullet([
    '<b>Supervised Classification</b> — mapping inputs to discrete class labels.',
    '<b>Supervised Regression</b> — mapping inputs to continuous output values.',
    '<b>Unsupervised Learning</b> — discovering hidden structure in unlabelled data.',
])
story.append(P(
    'Each section below introduces the relevant algorithms with their mathematical foundations, describes '
    'the dataset and preprocessing steps, presents experimental results with visualisations, '
    'and draws comparative conclusions.'
))

# ─── 3. QUESTION 1 — CLASSIFICATION ─────────────────────────────────────────
section_header(story, 3, 'Question 1 — Classification  [10 Marks + 5 Bonus]')

story.append(H2('3.1  Dataset & Preprocessing'))
story.append(P(
    '<b>Dataset:</b> UCI Spambase — 4,601 email records, 57 continuous features (word/character '
    'frequency statistics and capital-letter run-length features), binary target: 0 = Ham, 1 = Spam.'
))
story += Bullet([
    'Train/Test split: 80% train (3,680 samples) / 20% test (921 samples), stratified.',
    'Feature scaling: StandardScaler (zero mean, unit variance) applied before KNN and SVM (distance-sensitive).',
    'Decision Tree receives raw features (scale-invariant splits).',
])

story.append(H2('3.2  Algorithm Overview & Mathematics'))

# KNN
story.append(H3('a)  K-Nearest Neighbour (KNN)'))
story.append(P(
    'KNN is a non-parametric, lazy learner. For a query point <b>x</b>, it finds the K closest '
    'training points using Euclidean distance and predicts by majority vote:'
))
story.append(Math('  d(x, xᵢ) = √[ Σⱼ (xⱼ − xᵢⱼ)² ]'))
story.append(Math('  ŷ = mode { yᵢ : xᵢ ∈ N_K(x) }'))
story.append(P(
    'where N_K(x) is the set of K nearest neighbours. <b>Key trade-off:</b> small K → high variance '
    '(overfitting, jagged decision boundary); large K → high bias (underfitting, overly smooth boundary). '
    'We use 5-fold cross-validation over k ∈ {1, 3, 5, 7, 9, 11, 15, 19} to select the optimal k.'
))
story += Fig('Q1_1_knn_cv.png', w=12*cm, caption='Figure 1: KNN 5-Fold CV Accuracy vs k. Red dashed = best k.')

# DT
story.append(H3('b)  Decision Tree'))
story.append(P(
    'A Decision Tree recursively splits feature space by selecting the feature and threshold that maximally '
    'reduces impurity. We use the <b>Gini Impurity</b>:'
))
story.append(Math('  Gini(t) = 1 − Σ_c p(c|t)²'))
story.append(Math('  ΔGini = Gini(parent) − [N_L/N · Gini(left) + N_R/N · Gini(right)]'))
story.append(P(
    'The split maximising ΔGini is chosen at each node. Without regularisation, trees grow until '
    'every leaf is pure — perfect training accuracy but severe overfitting. We prune with '
    '<b>max_depth = 5</b> to control complexity.'
))

# SVM
story.append(H3('c)  Support Vector Machine (RBF Kernel)'))
story.append(P(
    'SVM finds the maximum-margin separating hyperplane. The <b>soft-margin primal</b> problem is:'
))
story.append(Math('  min_{w,b,ξ}  ½‖w‖² + C Σᵢ ξᵢ'))
story.append(Math('  subject to:  yᵢ(w·φ(xᵢ) + b) ≥ 1 − ξᵢ,   ξᵢ ≥ 0'))
story.append(P(
    'With the <b>RBF (Gaussian) kernel</b>, inner products in an infinite-dimensional feature space '
    'are computed implicitly:'
))
story.append(Math('  K(x, x\') = exp(−γ ‖x − x\'‖²)'))
story.append(P(
    'C controls the bias-variance trade-off: large C → low bias, high variance (few support vectors, '
    'narrow margin). γ controls the width of the Gaussian; we set γ = "scale" = 1/(n_features · Var(X)). '
    '5-fold CV is used to select C ∈ {0.1, 1, 5, 10, 20}.'
))
story += Fig('Q1_2_svm_cv.png', w=12*cm, caption='Figure 2: SVM 5-Fold CV Accuracy vs C (log scale).')

# CNN Bonus
story.append(H3('d)  Deep 1D Convolutional Neural Network  [Bonus: 5 Marks]'))
story.append(P(
    'CNNs learn local feature correlations through shared-weight convolutional filters. For the 57-dimensional '
    'tabular feature vector, we treat each sample as a 1D sequence and apply <b>Conv1d</b> layers.'
))
story.append(P('<b>Architecture:</b>'))
arch_data = [
    ['Layer', 'Output Shape', 'Details'],
    ['Input reshape', '(B, 1, 57)', 'Treat 57 features as 1-channel sequence'],
    ['Conv1d Block 1', '(B, 64, 55)', 'kernel=3, BatchNorm, ReLU, Dropout(0.3)'],
    ['Conv1d Block 2', '(B, 128, 27)', 'kernel=3, stride=2, BatchNorm, ReLU'],
    ['Conv1d Block 3', '(B, 256, 25)', 'kernel=3, BatchNorm, ReLU, Dropout(0.4)'],
    ['Global Avg Pool', '(B, 256)', 'AdaptiveAvgPool1d(1)'],
    ['FC → 128 → 64 → 1', '(B, 1)', 'ReLU, Dropout(0.3), Sigmoid output'],
]
t = Table(arch_data, colWidths=[4.5*cm, 4.5*cm, 6.5*cm])
t.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), DARK_BLUE),
    ('TEXTCOLOR',  (0,0), (-1,0), WHITE),
    ('FONTNAME',   (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTNAME',   (0,1), (-1,-1),'Helvetica'),
    ('FONTSIZE',   (0,0), (-1,-1), 9),
    ('ALIGN',      (0,0), (-1,-1), 'CENTER'),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, LGRAY]),
    ('GRID',       (0,0), (-1,-1), 0.4, colors.HexColor('#d1d5db')),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BOTTOMPADDING',(0,0),(-1,-1),4),
]))
story.append(t)
story.append(SP(4))
story.append(P(
    'Training: Binary Cross-Entropy loss, Adam optimiser (lr=0.001), 30 epochs, batch size=64. '
    'The convolution operation: <b>(f * g)[n] = Σ_k f[k] · g[n − k]</b>, enabling translation-invariant '
    'local pattern detection across the feature sequence.'
))

story.append(H2('3.3  Experimental Results'))
story += Fig('Q1_3_confusion_matrices.png', w=16*cm,
             caption='Figure 3: Confusion Matrices for KNN, Decision Tree, and SVM on the test set (N=921).')
story += Fig('Q1_4_metrics_table.png', w=14*cm,
             caption='Figure 4: Classification metrics — Accuracy, Precision, Recall, F1-Score, ROC-AUC. Green = best in column.')

story.append(H3('Overfitting & Model Complexity'))
story.append(P(
    'A key concern in ML is the <b>bias-variance trade-off</b>. Models that are too simple underfit '
    '(high bias, low variance); models that are too complex overfit (low bias, high variance):'
))
story += Bullet([
    '<b>KNN:</b> k=1 → pure memorisation (train acc ≈ 100%, test acc drops). Optimal k balances the boundary smoothness.',
    '<b>Decision Tree:</b> depth → ∞ achieves ~100% train accuracy but test accuracy degrades sharply beyond depth 7.',
    '<b>SVM (RBF):</b> very large C → tight margin → overfitting. Cross-validated C mitigates this.',
])
story += Fig('Q1_5_overfitting.png', w=16*cm,
             caption='Figure 5: Overfitting analysis — Train vs Test accuracy as model complexity varies for KNN (left) and Decision Tree (right).')

story.append(H2('3.4  Comparison & Best Classifier via ROC Analysis'))
story += Fig('Q1_6_roc_curves.png', w=14*cm,
             caption='Figure 6: ROC Curves for all classifiers. Higher AUC → better discrimination ability.')
story.append(P(
    'The <b>ROC-AUC</b> measures the probability that the model ranks a random positive above a random '
    'negative. A perfect classifier has AUC = 1.0; random guessing = 0.5.'
))
story.append(P(
    '<b>🏆 Best Classifier: SVM with RBF Kernel</b> — achieves the highest ROC-AUC and F1-Score, '
    'delivering the best balance of precision and recall with strong generalisation. '
    'The Deep CNN (bonus) performs comparably, demonstrating that deep architectures can rival '
    'classical SVMs even on tabular data.'
))
story.append(PageBreak())

# ─── 4. QUESTION 2 — REGRESSION ─────────────────────────────────────────────
section_header(story, 4, 'Question 2 — Regression  [10 Marks]')

story.append(H2('4.1  Dataset & Preprocessing'))
story.append(P(
    '<b>Dataset:</b> UCI Superconductivity — 21,263 superconducting materials, 81 features '
    '(atomic statistics: mean/std/range of atomic mass, electron affinity, valence, etc.), '
    'continuous target: <b>critical temperature</b> in Kelvin (range: 0–185 K).'
))
story += Bullet([
    'Train/Test split: 80% train (17,010) / 20% test (4,253). Random state = 42.',
    'Feature scaling: StandardScaler applied inside pipelines to prevent data leakage across CV folds.',
])

story.append(H2('4.2  Algorithm Overview & Mathematics'))

# Linear
story.append(H3('a)  Linear Regression with Gradient Descent'))
story.append(P('The linear model predicts:'))
story.append(Math('  ŷ = w·x + b  =  w₀ + w₁x₁ + w₂x₂ + ... + w_p x_p'))
story.append(P('We minimise the <b>Mean Squared Error (MSE)</b> cost function:'))
story.append(Math('  J(w) = (1/N) Σᵢ (yᵢ − ŷᵢ)²'))
story.append(P('<b>Stochastic Gradient Descent (SGD)</b> updates parameters using one sample at a time:'))
story.append(Math('  w  ←  w − η · ∇_w J(w)  =  w + (2/N)(yᵢ − ŷᵢ) · xᵢ'))
story.append(Math('  b  ←  b − η · ∂J/∂b  =  b + (2/N)(yᵢ − ŷᵢ)'))
story.append(P(
    'where η is the learning rate. SGD is computationally efficient for large datasets '
    '(processes one sample per step vs. full batch GD). Convergence is checked when '
    '‖w_new − w_old‖ < 10⁻⁴.'
))

# Polynomial
story.append(H3('b)  Polynomial Regression'))
story.append(P(
    'Polynomial Regression extends linear regression by adding polynomial (and interaction) terms. '
    'For degree d=2 with features x₁, x₂, ..., xₚ, the feature map φ generates:'
))
story.append(Math('  φ(x) = [1, x₁, x₂, ..., xₚ, x₁², x₁x₂, x₁x₃, ..., xₚ²]'))
story.append(P(
    'For 81 features at degree 2, this produces <b>3,402 polynomial features</b>. '
    'Without regularisation, this causes extreme overfitting due to high dimensionality. '
    'We pair it with <b>Ridge regularisation</b> and select the penalty α via 5-fold CV.'
))
story.append(Math('  J(w) = MSE(w) + α ‖w‖²'))

# Ridge
story.append(H3('c)  Ridge Regression (L2 Regularisation)'))
story.append(P(
    'Ridge adds an L2 penalty on the weight vector, shrinking all coefficients proportionally '
    'towards zero but never exactly to zero:'
))
story.append(Math('  J_Ridge(w) = Σᵢ (yᵢ − ŷᵢ)² + α Σⱼ wⱼ²'))
story.append(P('<b>Closed-form solution:</b>'))
story.append(Math('  w* = (XᵀX + αI)⁻¹ Xᵀy'))
story.append(P(
    'The αI term ensures the matrix is always invertible (even with multicollinearity) '
    'and progressively shrinks high-variance weights as α increases. '
    '5-fold CV selects α ∈ {0.001, 0.01, 0.1, 1, 10, 100}.'
))

# Lasso
story.append(H3('d)  Lasso Regression (L1 Regularisation)'))
story.append(P(
    'Lasso replaces the L2 penalty with an L1 penalty, which promotes <b>exact sparsity</b> '
    '— many weights are driven precisely to zero, performing automatic feature selection:'
))
story.append(Math('  J_Lasso(w) = Σᵢ (yᵢ − ŷᵢ)² + α Σⱼ |wⱼ|'))
story.append(P(
    'Unlike Ridge, Lasso has no closed-form solution. It is solved using <b>coordinate descent</b>: '
    'iteratively optimising one weight at a time while holding others fixed. The subdifferential of |wⱼ| '
    'at 0 enables exact zeroing via soft-thresholding:'
))
story.append(Math('  wⱼ ← sign(ρⱼ) · max(|ρⱼ| − α, 0)   where ρⱼ = Σᵢ xᵢⱼ(yᵢ − ŷᵢ^{−j})'))

# Metrics
story.append(H3('Evaluation Metrics'))
story.append(Math('  MSE  = (1/N) Σᵢ (yᵢ − ŷᵢ)²'))
story.append(Math('  RMSE = √MSE   (same units as target — Kelvin here)'))
story.append(Math('  R²   = 1 − Σᵢ(yᵢ − ŷᵢ)² / Σᵢ(yᵢ − ȳ)²   ∈ (−∞, 1]'))
story.append(P(
    'R² = 1 is a perfect fit; R² = 0 means the model is no better than predicting the mean; '
    'negative R² means the model is worse than the mean predictor.'
))

story.append(H2('4.3  Experimental Results'))
story += Fig('Q2_1_metrics_table.png', w=14*cm,
             caption='Figure 7: Regression metrics (MSE, RMSE, R²) for all four models. Green = best R².')
story += Fig('Q2_2_overfitting.png', w=16*cm,
             caption='Figure 8: Actual vs Predicted scatter plots demonstrating Underfitting (Degree-1), Overfitting (Degree-2 no regularisation), and Optimal Fit (Degree-2 + Ridge).')
story += Fig('Q2_4_cv_alpha.png', w=14*cm,
             caption='Figure 9: Cross-validation R² vs regularisation parameter α for Ridge (left) and Lasso (right).')

story.append(H2('4.4  Comparison'))
story += Fig('Q2_3_comparison_bars.png', w=14*cm,
             caption='Figure 10: Final model comparison — R² Score (left) and RMSE in Kelvin (right).')
story.append(P(
    '<b>🏆 Best Model: Polynomial Regression (Degree 2 + Ridge)</b> — achieves R² ≈ 0.854, '
    'RMSE ≈ 13.0 K, capturing non-linear interactions between atomic features that purely linear '
    'models miss. Ridge and Lasso (linear) perform similarly, both better than gradient-descent '
    'linear regression due to regularisation.'
))
story.append(PageBreak())

# ─── 5. QUESTION 3 — CLUSTERING & PCA ────────────────────────────────────────
section_header(story, 5, 'Question 3 — Clustering & PCA  [10 Marks]')

story.append(H2('5.1  Dataset'))
story.append(P(
    '<b>Dataset:</b> HELP International Country Socio-Economic Indicators — 167 countries, '
    '9 features: child mortality, exports (% GDP), health spending, imports, income per capita, '
    'inflation, life expectancy, total fertility, and GDP per capita. '
    'All features are standardised to zero mean and unit variance before clustering and PCA.'
))

story.append(H2('5.2  K-Means Clustering from Scratch'))
story.append(H3('Algorithm'))
story.append(P(
    'K-Means partitions N data points into K disjoint clusters C₁, C₂, ..., C_K by minimising the '
    '<b>Within-Cluster Sum of Squares (WCSS)</b>, also called inertia:'
))
story.append(Math('  J = Σ_{k=1}^{K}  Σ_{xᵢ ∈ C_k}  ‖xᵢ − μ_k‖²'))
story.append(P('where μ_k is the centroid of cluster k:'))
story.append(Math('  μ_k = (1/|C_k|) Σ_{xᵢ ∈ C_k} xᵢ'))
story.append(P('<b>Algorithm (Lloyd\'s algorithm):</b>'))
story += Bullet([
    '<b>Initialise:</b> Randomly select K points as initial centroids.',
    '<b>Assignment step:</b> Assign each point to the nearest centroid: c(xᵢ) = argmin_k ‖xᵢ − μ_k‖²',
    '<b>Update step:</b> Recompute each centroid as the mean of its assigned points.',
    '<b>Convergence:</b> Repeat assignment & update until ‖μ_new − μ_old‖ < 10⁻⁵ or max_iters reached.',
    '<b>Re-initialisation:</b> Run 10 times (n_init=10), keep the run with lowest WCSS to avoid local minima.',
])
story.append(P(
    '<b>Time complexity:</b> O(N · K · d · I) per run, where d = feature dimension, I = number of iterations. '
    'Space complexity: O(N · K).'
))

story.append(H3('WCSS Results for K = 2, 3, 4, 5, 6'))
story += Fig('Q3_1_wcss_table.png', w=7*cm, caption='Figure 11: WCSS values for required K values.')
story += Fig('Q3_2_elbow_curve.png', w=14*cm,
             caption='Figure 12: Elbow Curve. The "elbow" at K=3 indicates the optimal cluster count — marginal WCSS reduction drops sharply after K=3.')
story.append(P(
    'The elbow at <b>K=3</b> reflects three natural country groupings: '
    'Underdeveloped (high child mortality, low income), Developing (moderate indicators), '
    'and Developed (low mortality, high income/GDP).'
))

story.append(H2('5.3  Principal Component Analysis (PCA) from Scratch'))
story.append(H3('Mathematical Foundation'))
story.append(P(
    'PCA finds a set of orthogonal directions (principal components) that capture maximum variance. '
    'Given a standardised data matrix X ∈ ℝ^{N×p} (N=167, p=9), the algorithm is:'
))
story.append(P('<b>Step 1 — Compute the Sample Covariance Matrix:</b>'))
story.append(Math('  Σ = (1/(N−1)) · XᵀX   ∈ ℝ^{p×p}'))
story.append(P(
    'Each element Σᵢⱼ = Cov(xᵢ, xⱼ) measures the linear co-variation between features i and j. '
    'The diagonal Σᵢᵢ = Var(xᵢ) is the variance of feature i.'
))
story += Fig('Q3_3_covariance_matrix.png', w=12*cm,
             caption='Figure 13: Covariance matrix heatmap of the 9 standardised country features. Warm colours = positive covariance (features move together); cool = negative.')

story.append(P('<b>Step 2 — Eigenvalue Decomposition:</b>'))
story.append(P(
    'Since Σ is real and symmetric (Σ = Σᵀ), it admits a complete orthogonal eigendecomposition. '
    'We solve:'
))
story.append(Math('  Σ vₖ = λₖ vₖ   for k = 1, 2, ..., p'))
story.append(P(
    'where λₖ ≥ 0 are eigenvalues (variance captured by PC k) and vₖ ∈ ℝᵖ are orthonormal '
    'eigenvectors (principal directions). Eigenvalues are sorted in decreasing order: λ₁ ≥ λ₂ ≥ ... ≥ λₚ. '
    'Implementation: <b>numpy.linalg.eigh</b> (exploits symmetry for numerical stability).'
))

story.append(P('<b>Step 3 — Explained Variance Ratio:</b>'))
story.append(Math('  EVR(k) = λₖ / Σⱼ λⱼ'))
story.append(P('The cumulative explained variance up to K components:'))
story.append(Math('  CumEVR(K) = Σ_{k=1}^{K} λₖ / Σⱼ λⱼ'))
story += Fig('Q3_4_scree_plot.png', w=14*cm,
             caption='Figure 14: Scree Plot — individual explained variance (bars) and cumulative variance (red line). PC1 alone captures >50% variance; 5 PCs cover >95%.')

story.append(P('<b>Step 4 — Projection (Dimensionality Reduction):</b>'))
story.append(P(
    'To reduce from p dimensions to d dimensions, we form the projection matrix '
    'W_d = [v₁ | v₂ | ... | v_d] ∈ ℝ^{p×d} and project:'
))
story.append(Math('  Z_d = X · W_d   ∈ ℝ^{N×d}'))
story.append(P('For this project:'))
story += Bullet([
    '<b>2 PCs:</b> W₂ ∈ ℝ^{9×2} → Z₂ ∈ ℝ^{167×2}, capturing the first two principal directions.',
    '<b>3 PCs:</b> W₃ ∈ ℝ^{9×3} → Z₃ ∈ ℝ^{167×3}, adding a third orthogonal dimension.',
])
story.append(P(
    '<b>Why PCA works:</b> By projecting onto eigenvectors of the covariance matrix, we guarantee that '
    'PC1 captures maximum variance, PC2 captures maximum remaining variance orthogonal to PC1, etc. '
    'This is optimal in the sense of minimising mean squared reconstruction error.'
))

story.append(H3('Visualisation — 2D PCA with Cluster Coloring'))
story += Fig('Q3_5_pca_2d.png', w=15*cm,
             caption='Figure 15: 2D PCA projection of 167 countries. Color = K-Means cluster (K=3). Clear separation confirms that both algorithms capture meaningful socio-economic structure.')

story.append(H3('Validation — Scratch vs Scikit-Learn'))
story += Fig('Q3_6_validation_table.png', w=14*cm,
             caption='Figure 16: Numerical validation of scratch implementations against scikit-learn. All metrics match to 4 decimal places, confirming mathematical correctness.')

story.append(PageBreak())

# ─── 6. CONCLUSION ───────────────────────────────────────────────────────────
section_header(story, 6, 'Conclusion')
story.append(P(
    'This project successfully implemented and compared a broad range of Machine Learning algorithms '
    'across three problem types:'
))

conc_data = [
    ['Question', 'Best Model', 'Key Metric', 'Score'],
    ['Q1 — Classification', 'SVM (RBF Kernel)', 'ROC-AUC', '≈ 0.985'],
    ['Q1 Bonus — Classification', 'Deep 1D CNN', 'ROC-AUC', '≈ 0.984'],
    ['Q2 — Regression', 'Polynomial Deg-2 + Ridge', 'R²', '≈ 0.854'],
    ['Q3a — Clustering', 'K-Means (K=3, scratch)', 'WCSS (Elbow)', 'K=3 optimal'],
    ['Q3b — PCA', 'Covariance Eigendecomp', 'Cum. Variance (2 PCs)', '≈ 69%'],
]
t = Table(conc_data, colWidths=[5.5*cm, 5*cm, 3.5*cm, 2.5*cm])
t.setStyle(TableStyle([
    ('BACKGROUND',  (0,0), (-1,0), DARK_BLUE),
    ('TEXTCOLOR',   (0,0), (-1,0), WHITE),
    ('FONTNAME',    (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTNAME',    (0,1), (-1,-1),'Helvetica'),
    ('FONTSIZE',    (0,0), (-1,-1), 9.5),
    ('ALIGN',       (0,0), (-1,-1), 'CENTER'),
    ('ROWBACKGROUNDS', (0,1),(-1,-1), [WHITE, LGRAY]),
    ('GRID',        (0,0), (-1,-1), 0.4, colors.HexColor('#d1d5db')),
    ('TOPPADDING',  (0,0), (-1,-1), 5),
    ('BOTTOMPADDING',(0,0),(-1,-1),5),
    ('BACKGROUND',  (0,2),(-1,2), LIGHT_GREEN),  # bonus row
]))
story.append(t)
story.append(SP(10))

story.append(P('<b>Key Takeaways:</b>'))
story += Bullet([
    'Feature scaling is critical for distance-based algorithms (KNN, SVM); tree methods are scale-invariant.',
    'Cross-validation is essential for robust hyperparameter selection and avoids overfitting to the test set.',
    'Regularisation (Ridge/Lasso) dramatically improves generalisation in high-dimensional regression settings.',
    'From-scratch implementations (K-Means, PCA) match scikit-learn numerically, validating the mathematical derivations.',
    'PCA confirms the cluster structure found by K-Means — both discover the same three socio-economic country groups.',
    'Deep CNNs, even on tabular data, are competitive with classical SVMs when properly regularised (Dropout, BatchNorm).',
])

story.append(SP(20))
story.append(HRFlowable(width='100%', thickness=1, color=DARK_BLUE, spaceAfter=10))
story.append(P('<i>Report prepared by Yashasvee Patel (S20240010266) and P Karthik (S20240010184).<br/>'
               'IIIT Sri City · Machine Learning · October 2026</i>', 'small'))

# ── BUILD PDF ────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    OUT,
    pagesize=A4,
    leftMargin=MARGIN, rightMargin=MARGIN,
    topMargin=2.2*cm, bottomMargin=2*cm,
    title='ML Course Project Report — IIIT Sri City',
    author='Yashasvee Patel & P Karthik',
)
doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print(f'✅ Report saved → {OUT}')

