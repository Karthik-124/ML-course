"""
build_presentation.py
Generates a professional 16-slide widescreen PowerPoint deck (ML_Course_Project_Presentation.pptx)
for the Machine Learning Course Project Presentation at IIIT Sri City.
Authors: Yashasvee Patel (S20240010266) & P Karthik (S20240010184)
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# ----------------- Color Palette -----------------
DARK_BG = RGBColor(15, 23, 42)        # Slate 900
DARK_CARD = RGBColor(30, 41, 59)      # Slate 800
LIGHT_BG = RGBColor(248, 250, 252)    # Slate 50
WHITE = RGBColor(255, 255, 255)
CARD_BG = RGBColor(255, 255, 255)
CARD_BORDER = RGBColor(226, 232, 240) # Slate 200
TEXT_MAIN = RGBColor(15, 23, 42)      # Slate 900
TEXT_MUTED = RGBColor(100, 116, 139)  # Slate 500
TEXT_LIGHT = RGBColor(241, 245, 249)  # Slate 100
TEXT_MUTED_LIGHT = RGBColor(148, 163, 184) # Slate 400

# Domain Accents
ACCENT_BLUE = RGBColor(37, 99, 235)   # Classification
ACCENT_GREEN = RGBColor(5, 150, 105)  # Regression
ACCENT_PURPLE = RGBColor(124, 58, 237)# Unsupervised & PCA
ACCENT_AMBER = RGBColor(217, 119, 6)   # Highlights / Warnings
ACCENT_SLATE = RGBColor(71, 85, 105)

FONT_HEADING = "Calibri"
FONT_BODY = "Calibri"

TOTAL_SLIDES = 16

def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    def set_slide_background(slide, color):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background()
        return bg

    def add_header(slide, breadcrumb, title, subtitle, accent_color=ACCENT_BLUE):
        # Breadcrumb badge
        crumb_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.5), Inches(0.3))
        tf_crumb = crumb_box.text_frame
        tf_crumb.word_wrap = True
        tf_crumb.margin_left = tf_crumb.margin_right = tf_crumb.margin_top = tf_crumb.margin_bottom = 0
        p_crumb = tf_crumb.paragraphs[0]
        p_crumb.text = breadcrumb.upper()
        p_crumb.font.name = FONT_HEADING
        p_crumb.font.size = Pt(10)
        p_crumb.font.bold = True
        p_crumb.font.color.rgb = accent_color

        # Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.68), Inches(11.5), Inches(0.55))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        tf_title.margin_left = tf_title.margin_right = tf_title.margin_top = tf_title.margin_bottom = 0
        p_title = tf_title.paragraphs[0]
        p_title.text = title
        p_title.font.name = FONT_HEADING
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_MAIN

        # Subtitle
        sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.25), Inches(11.5), Inches(0.35))
        tf_sub = sub_box.text_frame
        tf_sub.word_wrap = True
        tf_sub.margin_left = tf_sub.margin_right = tf_sub.margin_top = tf_sub.margin_bottom = 0
        p_sub = tf_sub.paragraphs[0]
        p_sub.text = subtitle
        p_sub.font.name = FONT_BODY
        p_sub.font.size = Pt(11)
        p_sub.font.color.rgb = TEXT_MUTED

    def add_footer(slide, slide_num):
        footer_line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(6.9), Inches(11.733), Inches(0.015))
        footer_line.fill.solid()
        footer_line.fill.fore_color.rgb = CARD_BORDER
        footer_line.line.fill.background()

        foot_box = slide.shapes.add_textbox(Inches(0.8), Inches(6.95), Inches(11.733), Inches(0.3))
        tf = foot_box.text_frame
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = f"IIIT Sri City  ·  Machine Learning Course Project  ·  Patel & Karthik                                                              Slide {slide_num} of {TOTAL_SLIDES}"
        p.font.name = FONT_BODY
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_MUTED

    def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=CARD_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        if border_color:
            card.line.color.rgb = border_color
            card.line.width = Pt(1)
        else:
            card.line.fill.background()
        return card

    def add_notes(slide, notes_text):
        notes_slide = slide.notes_slide
        tf = notes_slide.notes_text_frame
        tf.text = notes_text

    # ==========================================
    # SLIDE 1: Title Slide (Dark Theme)
    # ==========================================
    slide1 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide1, DARK_BG)

    # Accent decorative top bar
    bar = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.12))
    bar.fill.solid()
    bar.fill.fore_color.rgb = ACCENT_BLUE
    bar.line.fill.background()

    # Pill badge
    badge = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(1.2), Inches(3.8), Inches(0.38))
    badge.fill.solid()
    badge.fill.fore_color.rgb = DARK_CARD
    badge.line.color.rgb = ACCENT_BLUE
    badge.line.width = Pt(1)
    tf_b = badge.text_frame
    p_b = tf_b.paragraphs[0]
    p_b.alignment = PP_ALIGN.CENTER
    p_b.text = "CSE DEPT  ·  MACHINE LEARNING"
    p_b.font.name = FONT_HEADING
    p_b.font.size = Pt(10)
    p_b.font.bold = True
    p_b.font.color.rgb = RGBColor(147, 197, 253)

    # Title Box
    tbox = slide1.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(11.0), Inches(1.8))
    tf = tbox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Machine Learning Course Project"
    p.font.name = FONT_HEADING
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = WHITE

    p2 = tf.add_paragraph()
    p2.text = "Supervised Classification, Non-Linear Regularized Regression,\nand Unsupervised Clustering & Dimensionality Reduction"
    p2.font.name = FONT_BODY
    p2.font.size = Pt(18)
    p2.font.color.rgb = RGBColor(203, 213, 225)
    p2.space_before = Pt(10)

    # 3 domain badges
    domains = [
        ("1. Classification", "UCI Spambase · KNN, DT, SVM, CNN", ACCENT_BLUE, Inches(1.2)),
        ("2. Regression", "Superconductivity · SGD, Ridge, Lasso, Poly", ACCENT_GREEN, Inches(5.1)),
        ("3. Clustering & PCA", "HELP Country Data · K-Means & Covariance PCA", ACCENT_PURPLE, Inches(9.0))
    ]
    for d_title, d_sub, d_color, d_left in domains:
        c = add_card(slide1, d_left, 4.0, 3.6, 1.4, DARK_CARD, d_color)
        tb = slide1.shapes.add_textbox(Inches(d_left + 0.2), Inches(4.15), Inches(3.2), Inches(1.1))
        tf_c = tb.text_frame
        p_ct = tf_c.paragraphs[0]
        p_ct.text = d_title
        p_ct.font.bold = True
        p_ct.font.size = Pt(14)
        p_ct.font.color.rgb = WHITE
        p_cs = tf_c.add_paragraph()
        p_cs.text = d_sub
        p_cs.font.size = Pt(11)
        p_cs.font.color.rgb = TEXT_MUTED_LIGHT
        p_cs.space_before = Pt(6)

    # Authors and Institution box
    abox = slide1.shapes.add_textbox(Inches(1.2), Inches(5.8), Inches(11.0), Inches(1.0))
    tf_a = abox.text_frame
    p_a1 = tf_a.paragraphs[0]
    p_a1.text = "Submitted By:  Yashasvee Patel (S20240010266)  &  P Karthik (S20240010184)"
    p_a1.font.bold = True
    p_a1.font.size = Pt(13)
    p_a1.font.color.rgb = WHITE

    p_a2 = tf_a.add_paragraph()
    p_a2.text = "Department of Computer Science & Engineering  ·  Indian Institute of Information Technology, Sri City"
    p_a2.font.size = Pt(11.5)
    p_a2.font.color.rgb = TEXT_MUTED_LIGHT
    p_a2.space_before = Pt(4)

    add_notes(slide1,
        "Good morning/afternoon everyone. Today, Karthik and I are presenting our Machine Learning Course Project. "
        "Our work investigates three core paradigms of machine learning: supervised classification on UCI Spambase, "
        "non-linear regularized regression on superconducting critical temperatures, and unsupervised clustering with PCA "
        "on international socio-economic development data. We will walk through our mathematical foundations, pipeline designs, "
        "overfitting diagnostics, and key engineering takeaways.")

    # ==========================================
    # SLIDE 2: Project Architecture & Methodology
    # ==========================================
    slide2 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide2, LIGHT_BG)
    add_header(slide2, "Executive Overview", "Project Architecture & Experimental Rigor",
               "Three machine learning challenges unified by strict scientific validation and zero data leakage")
    add_footer(slide2, 2)

    # 3 Column Cards
    col_w = Inches(3.65)
    gap = Inches(0.39)
    start_x = Inches(0.8)

    cards_data = [
        ("Domain 1: Classification", ACCENT_BLUE,
         "UCI Spambase Dataset",
         "• Goal: Predict Spam vs. Ham (4,601 emails, 57 features)\n"
         "• Algorithms: KNN, Decision Tree, SVM (RBF), Deep 1D CNN\n"
         "• Core Focus: Class balance, Precision-Recall tradeoffs, False Positive minimization\n"
         "• Validation: 5-Fold Stratified CV & 1,000 bootstrap ROC-AUC confidence intervals"),

        ("Domain 2: Regression", ACCENT_GREEN,
         "Superconductivity Tc Prediction",
         "• Goal: Predict Critical Temp Tc (21,263 samples, 81 features)\n"
         "• Algorithms: SGD Linear Regression, Ridge (L2), Lasso (L1), Polynomial Expansion\n"
         "• Core Focus: High bias vs. variance, degree sweep (1 to 4), collinearity shrinkage\n"
         "• Validation: 5-Fold CV on alpha grids, Train/Test divergence analysis"),

        ("Domain 3: Clustering & PCA", ACCENT_PURPLE,
         "HELP International Socio-Economic",
         "• Goal: Cluster 167 nations for aid targeting & dimensionality reduction\n"
         "• Algorithms: K-Means (Lloyd's), PCA from Covariance Eigendecomposition\n"
         "• Core Focus: Elbow vs Silhouette, factor loadings, 2D/3D subspace projections\n"
         "• Validation: Eigendecomposition Sigma*v = lambda*v, 76.14% cumulative variance")
    ]

    for i, (title, color, dataset, bullets) in enumerate(cards_data):
        cx = start_x + i * (col_w + gap)
        c = add_card(slide2, cx, 1.7, col_w, 3.8)

        # Header bar on card
        top_bar = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx, Inches(1.7), col_w, Inches(0.45))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = color
        top_bar.line.fill.background()
        tf_tb = top_bar.text_frame
        p_tb = tf_tb.paragraphs[0]
        p_tb.text = title
        p_tb.font.bold = True
        p_tb.font.size = Pt(12)
        p_tb.font.color.rgb = WHITE
        p_tb.alignment = PP_ALIGN.CENTER

        # Content text
        tb = slide2.shapes.add_textbox(cx + Inches(0.2), Inches(2.25), col_w - Inches(0.4), Inches(3.1))
        tf = tb.text_frame
        tf.word_wrap = True
        p_ds = tf.paragraphs[0]
        p_ds.text = dataset
        p_ds.font.bold = True
        p_ds.font.size = Pt(12.5)
        p_ds.font.color.rgb = TEXT_MAIN

        p_b = tf.add_paragraph()
        p_b.text = bullets
        p_b.font.size = Pt(10)
        p_b.font.color.rgb = TEXT_MAIN
        p_b.space_before = Pt(8)

    # Bottom Banner: Scientific Protocol
    bot_card = add_card(slide2, 0.8, 5.7, 11.733, 1.0, WHITE, ACCENT_BLUE)
    bot_tb = slide2.shapes.add_textbox(Inches(1.0), Inches(5.75), Inches(11.333), Inches(0.9))
    tf_bot = bot_tb.text_frame
    tf_bot.word_wrap = True
    p_b1 = tf_bot.paragraphs[0]
    p_b1.text = "Strict Scientific Protocol & Zero Data Leakage Guarantee:"
    p_b1.font.bold = True
    p_b1.font.size = Pt(11)
    p_b1.font.color.rgb = ACCENT_BLUE

    p_b2 = tf_bot.add_paragraph()
    p_b2.text = "1. Strict 80/20 train/test split fixed before any modeling.  " \
                "2. All scalers (StandardScaler) placed strictly inside scikit-learn Pipelines so test distributions never contaminate training folds.  " \
                "3. Hyperparameter selection performed solely on 5-fold cross-validation training splits."
    p_b2.font.size = Pt(9.5)
    p_b2.font.color.rgb = TEXT_MAIN
    p_b2.space_before = Pt(3)

    add_notes(slide2,
        "Here is the high-level roadmap of our presentation. We tackle three diverse problems covering the machine learning spectrum. "
        "A foundational principle across all our experiments is scientific reproducibility and zero data leakage. In many student projects, "
        "StandardScaler is mistakenly applied to the full dataset before splitting, which artificially inflates validation accuracy. "
        "In our implementation, all feature transformations are encapsulated inside scikit-learn Pipelines, ensuring the test set remains completely unseen.")

    # ==========================================
    # SLIDE 3: Q1 - Classification: UCI Spambase & Setup
    # ==========================================
    slide3 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide3, LIGHT_BG)
    add_header(slide3, "Question 1 · Supervised Classification", "UCI Spambase Dataset & Problem Formulation",
               "Binary spam detection on 4,601 emails using 57 continuous lexical and punctuation features")
    add_footer(slide3, 3)

    # Left Column: Dataset Details
    add_card(slide3, 0.8, 1.7, 4.8, 4.9)
    tb_q1 = slide3.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(4.4), Inches(4.7))
    tf_q1 = tb_q1.text_frame
    tf_q1.word_wrap = True

    p = tf_q1.paragraphs[0]
    p.text = "Dataset Characteristics"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = ACCENT_BLUE

    p_body = tf_q1.add_paragraph()
    p_body.text = "• 4,601 Email Records: 80% Train (3,680) & 20% Test (921)\n" \
                  "• Class Distribution: 1,813 Spam (39.4%) vs. 2,788 Ham (60.6%)\n" \
                  "• Stratified train/test splitting preserves natural class ratio\n" \
                  "• 57 Continuous Features:\n" \
                  "   - 48 Word Frequencies (% occurrence of 'free', 'money', 'credit')\n" \
                  "   - 6 Character Frequencies (% of '!', '$', '#', etc.)\n" \
                  "   - 3 Capital Run-Length Statistics (average, max, total capital letters)"
    p_body.font.size = Pt(10)
    p_body.font.color.rgb = TEXT_MAIN
    p_body.space_before = Pt(4)

    p_asym = tf_q1.add_paragraph()
    p_asym.text = "The Asymmetric Cost of Spam Detection:"
    p_asym.font.bold = True
    p_asym.font.size = Pt(11)
    p_asym.font.color.rgb = ACCENT_AMBER
    p_asym.space_before = Pt(8)

    p_asym_b = tf_q1.add_paragraph()
    p_asym_b.text = "In spam filtering, False Positives (flagging an important college email or job offer as spam) " \
                    "are far more catastrophic than False Negatives (a junk email slipping into the inbox). " \
                    "Thus, Precision and ROC-AUC are paramount alongside pure accuracy."
    p_asym_b.font.size = Pt(9.5)
    p_asym_b.font.color.rgb = TEXT_MAIN
    p_asym_b.space_before = Pt(2)

    # Right Column: Embedded Figure 1
    add_card(slide3, 5.8, 1.7, 6.733, 4.9)
    tb_fig1_title = slide3.shapes.add_textbox(Inches(6.0), Inches(1.8), Inches(6.3), Inches(0.4))
    tf_f1 = tb_fig1_title.text_frame
    p_f1 = tf_f1.paragraphs[0]
    p_f1.text = "Figure 1: 5-Fold Cross-Validation Hyperparameter Sweeps"
    p_f1.font.bold = True
    p_f1.font.size = Pt(11.5)
    p_f1.font.color.rgb = TEXT_MAIN

    fig1_path = os.path.abspath("extracted_figures/fig1_classification_cv.png")
    if os.path.exists(fig1_path):
        slide3.shapes.add_picture(fig1_path, Inches(6.0), Inches(2.3), width=Inches(6.333))

    tb_fig1_cap = slide3.shapes.add_textbox(Inches(6.0), Inches(5.6), Inches(6.3), Inches(0.9))
    tf_f1c = tb_fig1_cap.text_frame
    tf_f1c.word_wrap = True
    p_cap = tf_f1c.paragraphs[0]
    p_cap.text = "Hyperparameter Selection on Training Folds:\n" \
                 "• Left (KNN): Swept k in [1..21]. Optimal k = 3 yields peak 5-fold CV accuracy (90.76%).\n" \
                 "• Right (Decision Tree): Swept max_depth in [2..25]. Optimal depth = 12 reaches peak CV accuracy (91.85%)."
    p_cap.font.size = Pt(9.5)
    p_cap.font.color.rgb = TEXT_MUTED

    add_notes(slide3,
        "Turning to Question 1, our task is classifying 4,601 emails from the UCI Spambase dataset. "
        "The feature space consists of 57 continuous variables. Notice that the class distribution is roughly 40% spam and 60% ham. "
        "Importantly, spam filtering has asymmetric misclassification costs. A false positive—marking a crucial email as spam—is unacceptable. "
        "On the right, Figure 1 illustrates our 5-fold cross-validation sweeps on the training data. For KNN, k=3 provided optimal balance between "
        "noise sensitivity and oversmoothing. For Decision Trees, depth 12 achieved peak cross-validation accuracy before pruning begins.")

    # ==========================================
    # SLIDE 4: Q1 - Classification: Model Suite & Architectures
    # ==========================================
    slide4 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide4, LIGHT_BG)
    add_header(slide4, "Question 1 · Supervised Classification", "Model Suite: Algorithms & Hyperparameter Tuning",
               "Evaluating instance-based, tree-based, maximum-margin, and deep convolutional paradigms")
    add_footer(slide4, 4)

    # Left Column: 4 Models
    add_card(slide4, 0.8, 1.7, 6.0, 4.9)
    tb_models = slide4.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.6), Inches(4.7))
    tf_m = tb_models.text_frame
    tf_m.word_wrap = True

    models_info = [
        ("1. K-Nearest Neighbour (KNN)", "Instance-based memory classifier using Euclidean distance. Optimal k=3 chosen via 5-fold CV. Highly sensitive to feature magnitude, mandating z-score normalization inside pipeline."),
        ("2. Decision Tree (CART)", "Axis-aligned recursive space partitioning optimizing Gini impurity drop: Gini = 1 - sum(p_c^2). Max depth = 12 chosen via CV to prevent unconstrained leaf memorization."),
        ("3. Support Vector Machine (RBF Kernel)", "Constructs maximum-margin hyperplane in infinite-dimensional RKHS using RBF kernel K(x, x') = exp(-gamma * ||x-x'||^2). Optimal C = 5.0 balances slack penalties xi_i against margin width."),
        ("4. Deep 1D CNN (Bonus PyTorch Model)", "3 Convolutional blocks (32 -> 64 -> 128 channels, kernel=3, stride=1), BatchNorm1d, ReLU, Dropout (0.3), and Global Average Pooling. Adam optimizer (lr=1e-3, 40 epochs).")
    ]

    for i, (m_title, m_desc) in enumerate(models_info):
        p_t = tf_m.paragraphs[0] if i == 0 else tf_m.add_paragraph()
        p_t.text = m_title
        p_t.font.bold = True
        p_t.font.size = Pt(11)
        p_t.font.color.rgb = ACCENT_BLUE
        if i > 0:
            p_t.space_before = Pt(6)

        p_d = tf_m.add_paragraph()
        p_d.text = m_desc
        p_d.font.size = Pt(9.5)
        p_d.font.color.rgb = TEXT_MAIN
        p_d.space_before = Pt(1)

    # Right Column: Figure 2 (SVM CV) & Architecture summary
    add_card(slide4, 7.0, 1.7, 5.533, 4.9)
    tb_fig2_title = slide4.shapes.add_textbox(Inches(7.2), Inches(1.8), Inches(5.1), Inches(0.4))
    tf_f2 = tb_fig2_title.text_frame
    p_f2 = tf_f2.paragraphs[0]
    p_f2.text = "Figure 2: SVM (RBF) 5-Fold Cross-Validation Curve"
    p_f2.font.bold = True
    p_f2.font.size = Pt(11.5)
    p_f2.font.color.rgb = TEXT_MAIN

    fig2_path = os.path.abspath("extracted_figures/fig2_svm_cv.png")
    if os.path.exists(fig2_path):
        slide4.shapes.add_picture(fig2_path, Inches(7.2), Inches(2.2), width=Inches(5.133))

    tb_fig2_cap = slide4.shapes.add_textbox(Inches(7.2), Inches(5.35), Inches(5.1), Inches(1.1))
    tf_f2c = tb_fig2_cap.text_frame
    tf_f2c.word_wrap = True
    p_cap2 = tf_f2c.paragraphs[0]
    p_cap2.text = "Cross-Validation Insights on SVM:\n" \
                  "• Regularization parameter C swept across logarithmic grid [0.1, 100].\n" \
                  "• C = 5.0 achieved the global maximum CV accuracy of 93.15%.\n" \
                  "• Below C = 1, the model underfits (too wide margin); above C = 10, variance increases due to strict penalty on training slack."
    p_cap2.font.size = Pt(9.5)
    p_cap2.font.color.rgb = TEXT_MUTED

    add_notes(slide4,
        "Here we summarize our four classifier architectures. Notice the diversity of inductive biases: "
        "KNN is instance-based, Decision Trees create orthogonal decision boundaries, SVM projects data into an infinite-dimensional feature space, "
        "and our bonus 1D CNN treats the 57 features as a 1D sequence to capture local interaction patterns. "
        "Figure 2 shows the cross-validation curve for SVM across the regularization parameter C. "
        "Notice the plateau between C=1 and C=10, with C=5.0 hitting our peak CV accuracy of 93.15%.")

    # ==========================================
    # SLIDE 5: Q1 - Classification: Confusion Matrices & Metrics
    # ==========================================
    slide5 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide5, LIGHT_BG)
    add_header(slide5, "Question 1 · Supervised Classification", "Model Performance & Confusion Matrix Analysis",
               "Quantitative evaluation on 921 test emails across 5 evaluation metrics and error distributions")
    add_footer(slide5, 5)

    # Left Column: Table 4
    add_card(slide5, 0.8, 1.7, 5.9, 4.9)
    tb_t4_title = slide5.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.5), Inches(0.4))
    tf_t4 = tb_t4_title.text_frame
    p_t4 = tf_t4.paragraphs[0]
    p_t4.text = "Table 4: Test Performance Metrics (N = 921 Emails)"
    p_t4.font.bold = True
    p_t4.font.size = Pt(11.5)
    p_t4.font.color.rgb = ACCENT_BLUE

    # Create Table on slide
    table_shape = slide5.shapes.add_table(5, 5, Inches(1.0), Inches(2.25), Inches(5.5), Inches(1.8))
    table = table_shape.table
    table.columns[0].width = Inches(1.6)
    table.columns[1].width = Inches(0.95)
    table.columns[2].width = Inches(0.95)
    table.columns[3].width = Inches(0.95)
    table.columns[4].width = Inches(1.05)

    headers = ["Model", "Accuracy", "Precision", "Recall", "F1-Score"]
    for j, h in enumerate(headers):
        cell = table.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = DARK_CARD
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.name = FONT_HEADING
        p.font.bold = True
        p.font.size = Pt(9.5)
        p.font.color.rgb = WHITE
        p.alignment = PP_ALIGN.CENTER

    data_t4 = [
        ["KNN (k=3)", "89.79%", "87.26%", "86.78%", "0.8702"],
        ["Decision Tree (d=12)", "91.97%", "90.70%", "88.71%", "0.8969"],
        ["SVM (RBF, C=5.0)", "92.40%", "92.22%", "88.15%", "0.9014"],
        ["Deep 1D CNN", "91.53%", "89.26%", "89.26%", "0.8926"]
    ]

    for i, row in enumerate(data_t4):
        for j, val in enumerate(row):
            cell = table.cell(i + 1, j)
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(238, 242, 255) if i == 2 else WHITE
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.name = FONT_BODY
            p.font.size = Pt(9)
            p.font.bold = (i == 2) # Highlight SVM
            p.font.color.rgb = ACCENT_BLUE if i == 2 else TEXT_MAIN
            p.alignment = PP_ALIGN.LEFT if j == 0 else PP_ALIGN.CENTER

    # Error analysis bullets below table
    tb_err = slide5.shapes.add_textbox(Inches(1.0), Inches(4.2), Inches(5.5), Inches(2.3))
    tf_err = tb_err.text_frame
    tf_err.word_wrap = True
    p_e1 = tf_err.paragraphs[0]
    p_e1.text = "Key Confusion Matrix Findings:"
    p_e1.font.bold = True
    p_e1.font.size = Pt(11)
    p_e1.font.color.rgb = TEXT_MAIN

    p_e2 = tf_err.add_paragraph()
    p_e2.text = "• SVM achieves Highest Precision (92.22%): Only 27 False Positives out of 558 legitimate emails. Minimizes risk of critical emails going to spam.\n" \
                "• Deep 1D CNN achieves Highest Recall (89.26%): Misses only 39 spam emails out of 363 total spam.\n" \
                "• Decision Tree performs remarkably well (91.97% accuracy), demonstrating that axis-aligned cuts on keyword frequency are highly effective for spam filtering."
    p_e2.font.size = Pt(9.5)
    p_e2.font.color.rgb = TEXT_MAIN
    p_e2.space_before = Pt(4)

    # Right Column: Figure 3 (Confusion Matrices)
    add_card(slide5, 6.9, 1.7, 5.633, 4.9)
    fig3_path = os.path.abspath("extracted_figures/fig3_confusion_matrices.png")
    if os.path.exists(fig3_path):
        slide5.shapes.add_picture(fig3_path, Inches(7.05), Inches(1.85), width=Inches(5.333))

    add_notes(slide5,
        "Here are the core classification test results on the 921 test emails. "
        "Looking at Table 4, SVM with RBF kernel achieves the highest overall accuracy at 92.40% and top F1-score of 0.9014. "
        "Most importantly, looking at the confusion matrices on the right (Figure 3), SVM generated only 27 False Positives, giving it the highest precision of 92.22%. "
        "In spam detection, high precision is essential. Meanwhile, our Deep CNN achieved the highest recall at 89.26%, catching the largest fraction of spam.")

    # ==========================================
    # SLIDE 6: Q1 - Classification: Complexity, Overfitting & ROC-AUC
    # ==========================================
    slide6 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide6, LIGHT_BG)
    add_header(slide6, "Question 1 · Supervised Classification", "Model Complexity, Overfitting & ROC-AUC Analysis",
               "Evaluating bias-variance tradeoffs and 1,000 bootstrap resamples on ranking discrimination")
    add_footer(slide6, 6)

    # Left: Figure 4 (Overfitting)
    add_card(slide6, 0.8, 1.7, 5.7, 4.9)
    tb_f4_t = slide6.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.3), Inches(0.35))
    tf_f4 = tb_f4_t.text_frame
    p_f4 = tf_f4.paragraphs[0]
    p_f4.text = "Figure 4: Complexity & Overfitting Dynamics"
    p_f4.font.bold = True
    p_f4.font.size = Pt(11)
    p_f4.font.color.rgb = TEXT_MAIN

    fig4_path = os.path.abspath("extracted_figures/fig4_complexity_overfitting.png")
    if os.path.exists(fig4_path):
        slide6.shapes.add_picture(fig4_path, Inches(0.95), Inches(2.2), width=Inches(5.4))

    tb_f4_c = slide6.shapes.add_textbox(Inches(1.0), Inches(5.6), Inches(5.3), Inches(0.9))
    tf_f4c = tb_f4_c.text_frame
    tf_f4c.word_wrap = True
    p_f4c = tf_f4c.paragraphs[0]
    p_f4c.text = "• KNN: k=1 memorizes training set (100% train acc), test drops due to noise.\n" \
                 "• Decision Tree: Depth > 15 reaches 99% train acc while test degrades (overfitting).\n" \
                 "• CNN: Dropout (0.3) prevents val loss divergence across 40 epochs."
    p_f4c.font.size = Pt(9)
    p_f4c.font.color.rgb = TEXT_MUTED

    # Right: Figure 5 (ROC Curves)
    add_card(slide6, 6.7, 1.7, 5.833, 4.9)
    tb_f5_t = slide6.shapes.add_textbox(Inches(6.9), Inches(1.8), Inches(5.4), Inches(0.35))
    tf_f5 = tb_f5_t.text_frame
    p_f5 = tf_f5.paragraphs[0]
    p_f5.text = "Figure 5: ROC Curves with 1,000 Bootstrap 95% CIs"
    p_f5.font.bold = True
    p_f5.font.size = Pt(11)
    p_f5.font.color.rgb = TEXT_MAIN

    fig5_path = os.path.abspath("extracted_figures/fig5_roc_curves.png")
    if os.path.exists(fig5_path):
        slide6.shapes.add_picture(fig5_path, Inches(7.1), Inches(2.2), width=Inches(5.0))

    tb_f5_c = slide6.shapes.add_textbox(Inches(6.9), Inches(5.35), Inches(5.4), Inches(1.1))
    tf_f5c = tb_f5_c.text_frame
    tf_f5c.word_wrap = True
    p_f5c = tf_f5c.paragraphs[0]
    p_f5c.text = "Bootstrap ROC-AUC Statistical Rigor (1,000 Resamples):\n" \
                 "• Deep 1D CNN: 0.9718 [95% CI: 0.961 – 0.981]\n" \
                 "• SVM (RBF): 0.9697 [95% CI: 0.959 – 0.979] (Statistical Tie with CNN)\n" \
                 "• KNN: 0.9360 [0.919 – 0.951]  |  Decision Tree: 0.9023 [0.876 – 0.925]\n" \
                 "Selection: SVM selected as champion model (highest precision, top F1, zero GPU need)."
    p_f5c.font.size = Pt(9)
    p_f5c.font.color.rgb = TEXT_MUTED

    add_notes(slide6,
        "Slide 6 provides critical scientific validation. On the left, Figure 4 demonstrates the classic bias-variance tradeoff across all four models. "
        "At k=1 for KNN or depth=25 for Decision Trees, training accuracy approaches 100%, but test accuracy drops as the models memorize noise. "
        "On the right, Figure 5 shows our ROC curves. Rather than relying on a single point estimate, we ran 1,000 bootstrap resamples to compute 95% confidence intervals. "
        "Notice that the intervals for SVM [0.959, 0.979] and Deep CNN [0.961, 0.981] overlap heavily. This proves they are in a statistical tie, "
        "justifying our selection of SVM based on its higher precision, lower latency, and simplicity.")

    # ==========================================
    # SLIDE 7: Q2 - Regression: Superconductivity Dataset & Formulation
    # ==========================================
    slide7 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide7, LIGHT_BG)
    add_header(slide7, "Question 2 · Non-Linear Regression & Regularization", "Superconductivity Critical Temperature (Tc) Prediction",
               "Predicting critical transition temperature from 81 elemental and chemical features across 21,263 superconductors")
    add_footer(slide7, 7)

    # 3 Summary Cards across top
    metrics_top = [
        ("Dataset Scale", "21,263 Superconductors", "80% Train (17,010) / 20% Test (4,253) split", ACCENT_GREEN),
        ("Input Features", "81 Continuous Features", "Derived from 8 fundamental atomic properties", ACCENT_BLUE),
        ("Target Variable Tc", "Range: 0.00021 K to 185 K", "Mean: 34.42 K · Heavily skewed distribution", ACCENT_AMBER)
    ]
    for i, (m_h, m_val, m_sub, m_col) in enumerate(metrics_top):
        cx = Inches(0.8 + i * 4.0)
        c = add_card(slide7, cx, 1.7, 3.733, 1.3)
        tb = slide7.shapes.add_textbox(cx + Inches(0.15), Inches(1.8), Inches(3.4), Inches(1.1))
        tf = tb.text_frame
        p1 = tf.paragraphs[0]
        p1.text = m_h.upper()
        p1.font.size = Pt(9.5)
        p1.font.bold = True
        p1.font.color.rgb = m_col
        p2 = tf.add_paragraph()
        p2.text = m_val
        p2.font.size = Pt(13)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_MAIN
        p3 = tf.add_paragraph()
        p3.text = m_sub
        p3.font.size = Pt(9.5)
        p3.font.color.rgb = TEXT_MUTED

    # Bottom Split Cards
    add_card(slide7, 0.8, 3.2, 5.7, 3.4)
    tb_b1 = slide7.shapes.add_textbox(Inches(1.0), Inches(3.3), Inches(5.3), Inches(3.1))
    tf_b1 = tb_b1.text_frame
    tf_b1.word_wrap = True

    p = tf_b1.paragraphs[0]
    p.text = "Elemental Feature Generation (8 Atomic Properties)"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = ACCENT_GREEN

    p_props = tf_b1.add_paragraph()
    p_props.text = "Features are statistical aggregates (mean, weighted mean, geometric mean, weighted geometric mean, min, max, range, and standard deviation) computed across 8 physical properties:\n" \
                   "1. Atomic Mass  ·  2. First Ionization Energy\n" \
                   "3. Atomic Radius  ·  4. Density\n" \
                   "5. Electron Affinity  ·  6. Heat of Fusion\n" \
                   "7. Thermal Conductivity  ·  8. Valence Electrons"
    p_props.font.size = Pt(9.5)
    p_props.font.color.rgb = TEXT_MAIN
    p_props.space_before = Pt(4)

    add_card(slide7, 6.8, 3.2, 5.733, 3.4)
    tb_b2 = slide7.shapes.add_textbox(Inches(7.0), Inches(3.3), Inches(5.3), Inches(3.1))
    tf_b2 = tb_b2.text_frame
    tf_b2.word_wrap = True

    p = tf_b2.paragraphs[0]
    p.text = "The Machine Learning Challenge"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = ACCENT_BLUE

    p_chal = tf_b2.add_paragraph()
    p_chal.text = "• Severe Collinearity: Multiple aggregate statistics derived from the same elemental properties exhibit high pairwise correlation (|r| > 0.85).\n" \
                  "• Non-Linear Cooper Pairing: Bardeen-Cooper-Schrieffer (BCS) quantum theory dictates that Tc depends exponentially on electron-phonon coupling and density of states.\n" \
                  "• Linear Hypothesis Failure: Plain linear models cannot capture multiplicative synergy between atomic radius, valence, and thermal conductivity."
    p_chal.font.size = Pt(9.5)
    p_chal.font.color.rgb = TEXT_MAIN
    p_chal.space_before = Pt(4)

    add_notes(slide7,
        "Moving to Question 2, we tackle a regression problem: predicting the critical temperature Tc of 21,263 superconductors. "
        "Tc is the temperature below which electrical resistance drops to zero. "
        "The dataset extracts 81 continuous features from 8 atomic properties. "
        "From a machine learning perspective, this presents two big challenges: severe multicollinearity among atomic statistics, "
        "and non-linear quantum physics where Tc is driven by multiplicative interactions rather than additive linear effects.")

    # ==========================================
    # SLIDE 8: Q2 - Regression: Linear SGD, Ridge & Lasso
    # ==========================================
    slide8 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide8, LIGHT_BG)
    add_header(slide8, "Question 2 · Non-Linear Regression & Regularization", "Linear SGD, Ridge (L2) & Lasso (L1) Regularization",
               "Evaluating linear baselines and regularized shrinkage across all 81 elemental features")
    add_footer(slide8, 8)

    # Left: Formulations & Findings
    add_card(slide8, 0.8, 1.7, 5.6, 4.9)
    tb_reg = slide8.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.2), Inches(4.7))
    tf_reg = tb_reg.text_frame
    tf_reg.word_wrap = True

    p = tf_reg.paragraphs[0]
    p.text = "Regularization Formulations & Objectives"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = ACCENT_GREEN

    p_reg = tf_reg.add_paragraph()
    p_reg.text = "• Linear Regression via SGD: Minimizes standard MSE without penalty. Iterative gradient descent converges to R^2 = 0.7332 (RMSE = 17.52 K).\n\n" \
                 "• Ridge Regression (L2 Penalty):\n" \
                 "  J(w) = sum(y_i - w^T x_i)^2 + alpha * ||w||_2^2\n" \
                 "  Shrinks collinear weights proportionally, mitigating ill-conditioned matrix inversion. Optimal alpha = 0.1 yields R^2 = 0.7375 (RMSE = 17.38 K).\n\n" \
                 "• Lasso Regression (L1 Penalty):\n" \
                 "  J(w) = sum(y_i - w^T x_i)^2 + alpha * ||w||_1\n" \
                 "  Enforces diamond-corner sparsity, setting irrelevant coefficients to zero. Optimal alpha = 1e-5 yields R^2 = 0.7375.\n\n" \
                 "• The Linear Ceiling: Both Ridge and Lasso plateau at R^2 ~ 0.738. Regularization prevents blowup but cannot break past linear underfitting."
    p_reg.font.size = Pt(9.5)
    p_reg.font.color.rgb = TEXT_MAIN
    p_reg.space_before = Pt(4)

    # Right: Figure 6 (Ridge & Lasso CV)
    add_card(slide8, 6.6, 1.7, 5.933, 4.9)
    tb_f6_t = slide8.shapes.add_textbox(Inches(6.8), Inches(1.8), Inches(5.5), Inches(0.4))
    tf_f6 = tb_f6_t.text_frame
    p_f6 = tf_f6.paragraphs[0]
    p_f6.text = "Figure 6: 5-Fold Cross-Validation for Ridge & Lasso"
    p_f6.font.bold = True
    p_f6.font.size = Pt(11.5)
    p_f6.font.color.rgb = TEXT_MAIN

    fig6_path = os.path.abspath("extracted_figures/fig6_ridge_lasso_cv.png")
    if os.path.exists(fig6_path):
        slide8.shapes.add_picture(fig6_path, Inches(6.75), Inches(2.3), width=Inches(5.6))

    tb_f6_c = slide8.shapes.add_textbox(Inches(6.8), Inches(5.35), Inches(5.5), Inches(1.1))
    tf_f6c = tb_f6_c.text_frame
    tf_f6c.word_wrap = True
    p_f6c = tf_f6c.paragraphs[0]
    p_f6c.text = "Alpha Grid Search Findings:\n" \
                 "• Left (Ridge): Stable performance for alpha < 10. Beyond alpha = 100, heavy L2 penalty causes excessive shrinkage and underfitting.\n" \
                 "• Right (Lasso): As alpha increases past 1e-3, sparsity aggressively eliminates valid predictors, causing CV R^2 to plummet."
    p_f6c.font.size = Pt(9)
    p_f6c.font.color.rgb = TEXT_MUTED

    add_notes(slide8,
        "To test linear modeling on this dataset, we implemented Linear SGD, Ridge, and Lasso. "
        "As seen in Figure 6, we ran 5-fold cross-validation across alpha grids. "
        "Ridge with alpha=0.1 and Lasso with alpha=1e-5 both reached an R^2 of 0.7375 and RMSE of 17.38 Kelvin. "
        "However, notice the fundamental limitation: all linear models hit a performance ceiling at R^2 ~ 0.738. "
        "Regularization successfully stabilizes collinearity, but it cannot overcome the high bias of assuming a linear physical relationship.")

    # ==========================================
    # SLIDE 9: Q2 - Regression: Polynomial Sweep & Overfitting
    # ==========================================
    slide9 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide9, LIGHT_BG)
    add_header(slide9, "Question 2 · Non-Linear Regression & Regularization", "Polynomial Expansion: Feature Selection & Degree Sweep",
               "Analyzing model capacity and generalization error from high bias (d=1) to catastrophic variance (d=4)")
    add_footer(slide9, 9)

    # Left: Top-15 Pearson Correlation Table
    add_card(slide9, 0.8, 1.7, 4.6, 4.9)
    tb_cor_t = slide9.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(4.2), Inches(0.4))
    tf_cor = tb_cor_t.text_frame
    p_cor = tf_cor.paragraphs[0]
    p_cor.text = "Top Features by Pearson Correlation (|r|)"
    p_cor.font.bold = True
    p_cor.font.size = Pt(11)
    p_cor.font.color.rgb = ACCENT_GREEN

    # Correlation mini table
    t_cor_s = slide9.shapes.add_table(6, 2, Inches(1.0), Inches(2.25), Inches(4.2), Inches(1.8))
    t_cor = t_cor_s.table
    t_cor.columns[0].width = Inches(2.9)
    t_cor.columns[1].width = Inches(1.3)

    t_cor.cell(0, 0).text = "Selected Feature"
    t_cor.cell(0, 1).text = "Corr (r)"
    for cell in [t_cor.cell(0, 0), t_cor.cell(0, 1)]:
        cell.fill.solid()
        cell.fill.fore_color.rgb = DARK_CARD
        cell.text_frame.paragraphs[0].font.bold = True
        cell.text_frame.paragraphs[0].font.size = Pt(9.5)
        cell.text_frame.paragraphs[0].font.color.rgb = WHITE

    rows_cor = [
        ["range_ThermalConductivity", "-0.6873"],
        ["w_mean_Valence", "-0.6324"],
        ["std_AtomicRadius", "+0.6133"],
        ["range_AtomicRadius", "+0.6133"],
        ["w_mean_ThermalConductivity", "-0.6121"]
    ]
    for i, (fn, r_val) in enumerate(rows_cor):
        c0 = t_cor.cell(i+1, 0)
        c1 = t_cor.cell(i+1, 1)
        c0.fill.solid()
        c1.fill.solid()
        c0.fill.fore_color.rgb = c1.fill.fore_color.rgb = WHITE
        c0.text_frame.paragraphs[0].text = fn
        c1.text_frame.paragraphs[0].text = r_val
        c0.text_frame.paragraphs[0].font.size = Pt(8.5)
        c1.text_frame.paragraphs[0].font.size = Pt(8.5)
        c1.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER

    tb_deg_notes = slide9.shapes.add_textbox(Inches(1.0), Inches(4.2), Inches(4.2), Inches(2.3))
    tf_dn = tb_deg_notes.text_frame
    tf_dn.word_wrap = True
    p_dn1 = tf_dn.paragraphs[0]
    p_dn1.text = "Degree Sweep on Top 15 Features:"
    p_dn1.font.bold = True
    p_dn1.font.size = Pt(10.5)
    p_dn1.font.color.rgb = TEXT_MAIN

    p_dn2 = tf_dn.add_paragraph()
    p_dn2.text = "• Degree 1 (15 terms): High Bias (R^2 = 0.735)\n" \
                 "• Degree 2 (135 terms): Balanced (R^2 = 0.735)\n" \
                 "• Degree 3 (815 terms): Overfitting begins (train R^2=0.81, test drops)\n" \
                 "• Degree 4 (3,875 terms): Catastrophic explosion! Test MSE explodes due to ill-conditioned Vandermonde matrix."
    p_dn2.font.size = Pt(9)
    p_dn2.font.color.rgb = TEXT_MAIN
    p_dn2.space_before = Pt(3)

    # Right: Figure 7 (Degree Sweep)
    add_card(slide9, 5.6, 1.7, 6.933, 4.9)
    tb_f7_t = slide9.shapes.add_textbox(Inches(5.8), Inches(1.8), Inches(6.5), Inches(0.4))
    tf_f7 = tb_f7_t.text_frame
    p_f7 = tf_f7.paragraphs[0]
    p_f7.text = "Figure 7: Polynomial Degree Sweep (Degrees 1 to 4)"
    p_f7.font.bold = True
    p_f7.font.size = Pt(11.5)
    p_f7.font.color.rgb = TEXT_MAIN

    fig7_path = os.path.abspath("extracted_figures/fig7_polynomial_sweep.png")
    if os.path.exists(fig7_path):
        slide9.shapes.add_picture(fig7_path, Inches(5.75), Inches(2.3), width=Inches(6.6))

    tb_f7_c = slide9.shapes.add_textbox(Inches(5.8), Inches(5.35), Inches(6.5), Inches(1.1))
    tf_f7c = tb_f7_c.text_frame
    tf_f7c.word_wrap = True
    p_f7c = tf_f7c.paragraphs[0]
    p_f7c.text = "Generalization Error Breakdown:\n" \
                 "• At d=1, train and test errors are identical but high (Underfitting / High Bias).\n" \
                 "• At d=4, train R^2 reaches 0.88, but unregularized test error diverges catastrophically (High Variance).\n" \
                 "• Conclusion: Polynomial expansion demands strict L2 regularization to control interaction variance."
    p_f7c.font.size = Pt(9)
    p_f7c.font.color.rgb = TEXT_MUTED

    add_notes(slide9,
        "To introduce non-linearity, we first selected the top 15 features by Pearson correlation and conducted a degree sweep from d=1 to d=4. "
        "Figure 7 demonstrates the textbook transition from underfitting to overfitting. "
        "At degree 1, we suffer from high bias. At degree 2, performance remains stable with 135 terms. "
        "At degree 3, we expand to 815 terms and training error pulls away from test error. "
        "Finally, at degree 4 with 3,875 terms, test error explodes completely. "
        "This proves that high-degree polynomial expansions without regularization suffer from severe variance and numerical instability.")

    # ==========================================
    # SLIDE 10: Q2 - Regression: The Breakthrough (Poly Ridge)
    # ==========================================
    slide10 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide10, LIGHT_BG)
    add_header(slide10, "Question 2 · Non-Linear Regression & Regularization", "The Breakthrough: Full 81-Feature Polynomial Ridge",
               "Capturing 3,402 cross-feature atomic interactions achieves R^2 = 0.8542 and reduces RMSE to 12.95 K")
    add_footer(slide10, 10)

    # Left: Table 6 and Breakthrough Insight
    add_card(slide10, 0.8, 1.7, 5.8, 4.9)
    tb_t6_t = slide10.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.4), Inches(0.4))
    tf_t6 = tb_t6_t.text_frame
    p_t6 = tf_t6.paragraphs[0]
    p_t6.text = "Table 6: Complete Regression Model Comparison"
    p_t6.font.bold = True
    p_t6.font.size = Pt(11.5)
    p_t6.font.color.rgb = ACCENT_GREEN

    # Regression table
    t6_s = slide10.shapes.add_table(6, 4, Inches(1.0), Inches(2.25), Inches(5.4), Inches(2.1))
    t6 = t6_s.table
    t6.columns[0].width = Inches(2.1)
    t6.columns[1].width = Inches(1.0)
    t6.columns[2].width = Inches(1.1)
    t6.columns[3].width = Inches(1.2)

    headers_t6 = ["Model", "Test MSE", "Test RMSE", "Test R^2"]
    for j, h in enumerate(headers_t6):
        c = t6.cell(0, j)
        c.fill.solid()
        c.fill.fore_color.rgb = DARK_CARD
        p = c.text_frame.paragraphs[0]
        p.text = h
        p.font.bold = True
        p.font.size = Pt(9)
        p.font.color.rgb = WHITE
        p.alignment = PP_ALIGN.CENTER

    data_t6 = [
        ["Linear Regression (SGD)", "307.09", "17.52 K", "0.7332"],
        ["Ridge Regression (a=0.1)", "302.15", "17.38 K", "0.7375"],
        ["Lasso Regression (a=1e-5)", "302.20", "17.38 K", "0.7375"],
        ["Poly Ridge (Top 15, d=2)", "305.24", "17.47 K", "0.7348"],
        ["Poly Ridge (All 81, d=2)", "167.79", "12.95 K", "0.8542"]
    ]

    for i, row in enumerate(data_t6):
        for j, val in enumerate(row):
            c = t6.cell(i+1, j)
            c.fill.solid()
            c.fill.fore_color.rgb = RGBColor(236, 253, 245) if i == 4 else WHITE
            p = c.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(8.5)
            p.font.bold = (i == 4)
            p.font.color.rgb = ACCENT_GREEN if i == 4 else TEXT_MAIN
            p.alignment = PP_ALIGN.LEFT if j == 0 else PP_ALIGN.CENTER

    # Breakthrough Callout Card
    tb_bt = slide10.shapes.add_textbox(Inches(1.0), Inches(4.5), Inches(5.4), Inches(2.0))
    tf_bt = tb_bt.text_frame
    tf_bt.word_wrap = True
    p_bth = tf_bt.paragraphs[0]
    p_bth.text = "Key Scientific Breakthrough:"
    p_bth.font.bold = True
    p_bth.font.size = Pt(11)
    p_bth.font.color.rgb = ACCENT_GREEN

    p_btb = tf_bt.add_paragraph()
    p_btb.text = "Expanding all 81 features to degree-2 generates 3,402 pairwise interaction terms. " \
                 "Regularized by Ridge (alpha = 10.0), Test R^2 surged from 0.7332 to 0.8542 (+16.5% relative gain) " \
                 "and RMSE plunged from 17.52 K to 12.95 K (-26.1% error reduction).\n" \
                 "Takeaway: Physical representation learning (multiplicative interaction between atomic properties) " \
                 "yields vastly greater returns than optimizing linear algorithms."
    p_btb.font.size = Pt(9)
    p_btb.font.color.rgb = TEXT_MAIN
    p_btb.space_before = Pt(3)

    # Right: Figure 8 (Bar Chart Comparison)
    add_card(slide10, 6.8, 1.7, 5.733, 4.9)
    tb_f8_t = slide10.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.3), Inches(0.4))
    tf_f8 = tb_f8_t.text_frame
    p_f8 = tf_f8.paragraphs[0]
    p_f8.text = "Figure 8: Performance Comparison on Test Set"
    p_f8.font.bold = True
    p_f8.font.size = Pt(11.5)
    p_f8.font.color.rgb = TEXT_MAIN

    fig8_path = os.path.abspath("extracted_figures/fig8_regression_comparison.png")
    if os.path.exists(fig8_path):
        slide10.shapes.add_picture(fig8_path, Inches(6.9), Inches(2.3), width=Inches(5.5))

    tb_f8_c = slide10.shapes.add_textbox(Inches(7.0), Inches(5.35), Inches(5.3), Inches(1.1))
    tf_f8c = tb_f8_c.text_frame
    tf_f8c.word_wrap = True
    p_f8c = tf_f8c.paragraphs[0]
    p_f8c.text = "Visualizing the Performance Jump:\n" \
                 "• Left plot: Polynomial Ridge (All 81) sharply outperforms all other models in R^2 (0.8542 vs ~0.737).\n" \
                 "• Right plot: RMSE drops from ~17.4 K down to 12.95 K, cutting prediction error by more than 4.5 Kelvin."
    p_f8c.font.size = Pt(9)
    p_f8c.font.color.rgb = TEXT_MUTED

    add_notes(slide10,
        "Slide 10 highlights the major engineering breakthrough in our regression task. "
        "When we expanded all 81 elemental features to degree-2, we created 3,402 pairwise interaction terms. "
        "By applying Ridge regularization with alpha=10.0, we prevented overfitting on this massive feature space. "
        "As seen in Table 6 and Figure 8, our Test R^2 surged from 0.7332 to 0.8542, and our RMSE dropped from 17.52 Kelvin down to 12.95 Kelvin. "
        "This proves that capturing non-linear physical interactions between atomic properties—like thermal conductivity times valence—is "
        "far more impactful than any hyperparameter tuning of linear models.")

    # ==========================================
    # SLIDE 11: Q3 - Unsupervised: HELP International Dataset & Formulation
    # ==========================================
    slide11 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide11, LIGHT_BG)
    add_header(slide11, "Question 3 · Unsupervised Learning & PCA", "HELP International Socio-Economic Dataset",
               "Discovering latent country clusters for equitable foreign aid allocation across 167 nations")
    add_footer(slide11, 11)

    # Left: Problem Context & Data Dictionary
    add_card(slide11, 0.8, 1.7, 5.8, 4.9)
    tb_q3 = slide11.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.4), Inches(4.7))
    tf_q3 = tb_q3.text_frame
    tf_q3.word_wrap = True

    p = tf_q3.paragraphs[0]
    p.text = "Socio-Economic Development Context"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = ACCENT_PURPLE

    p_q3b = tf_q3.add_paragraph()
    p_q3b.text = "• Objective: HELP International needs to categorize 167 nations to allocate humanitarian aid and development funds equitably.\n" \
                 "• Unsupervised Setting: No ground-truth labels exist; natural clusters must emerge from multivariate socio-economic patterns.\n" \
                 "• The 9 Indicators Evaluated:\n" \
                 "   1. child_mort: Deaths of children under 5 per 1,000 live births\n" \
                 "   2. exports: Exports of goods/services as % of GDP per capita\n" \
                 "   3. health: Total healthcare spending as % of GDP per capita\n" \
                 "   4. imports: Imports of goods/services as % of GDP per capita\n" \
                 "   5. income: Net income per person (USD)\n" \
                 "   6. inflation: Annual GDP growth rate (% inflation)\n" \
                 "   7. life_expec: Average life expectancy at birth (years)\n" \
                 "   8. total_fer: Children born per woman (fertility rate)\n" \
                 "   9. gdpp: Gross Domestic Product per capita (USD)"
    p_q3b.font.size = Pt(9.5)
    p_q3b.font.color.rgb = TEXT_MAIN
    p_q3b.space_before = Pt(4)

    # Right: Preprocessing & Formulation
    add_card(slide11, 6.8, 1.7, 5.733, 4.9)
    tb_pre = slide11.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.3), Inches(4.7))
    tf_pre = tb_pre.text_frame
    tf_pre.word_wrap = True

    p = tf_pre.paragraphs[0]
    p.text = "Preprocessing & Algorithmic Formulation"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = ACCENT_BLUE

    p_preb = tf_pre.add_paragraph()
    p_preb.text = "• Why Feature Scaling is Absolutely Essential:\n" \
                  "  GDP per capita ranges from $231 to $105,000, while fertility rate ranges from 1.15 to 7.49. " \
                  "  Without standardization, GDP would dominate Euclidean distance by a factor of 10,000x, " \
                  "  rendering health and mortality completely invisible to K-Means and PCA.\n\n" \
                  "• Standardization to Zero Mean & Unit Variance:\n" \
                  "  x_norm_ij = (x_ij - mu_j) / sigma_j\n\n" \
                  "• K-Means Optimization Problem (Lloyd's Algorithm):\n" \
                  "  min_{S} sum_{k=1}^K sum_{x in S_k} ||x - mu_k||_2^2\n" \
                  "  10 random restarts with K-Means++ initialization used to avoid local minima traps."
    p_preb.font.size = Pt(9.5)
    p_preb.font.color.rgb = TEXT_MAIN
    p_preb.space_before = Pt(4)

    add_notes(slide11,
        "Turning to Question 3, we analyze 167 nations evaluated on 9 socio-economic indicators from HELP International. "
        "The practical objective is determining which countries need urgent international aid. "
        "Because this is unsupervised learning, we have no predefined ground-truth labels. "
        "Notice the extreme difference in scales: GDP per capita runs up to $105,000, while fertility rate is under 8. "
        "Without z-score standardization, distance-based clustering would simply group countries by raw wealth, ignoring child mortality and healthcare.")

    # ==========================================
    # SLIDE 12: Q3 - K-Means: Elbow Method & Silhouette Analysis
    # ==========================================
    slide12 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide12, LIGHT_BG)
    add_header(slide12, "Question 3 · Unsupervised Learning & PCA", "K-Means Clustering: Elbow Method & Silhouette Scores",
               "Evaluating cluster cohesion and separation to select the optimal partition of 167 nations")
    add_footer(slide12, 12)

    # Left: Table 8 and Cluster Taxonomy
    add_card(slide12, 0.8, 1.7, 5.5, 4.9)
    tb_t8_t = slide12.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.1), Inches(0.4))
    tf_t8 = tb_t8_t.text_frame
    p_t8 = tf_t8.paragraphs[0]
    p_t8.text = "Table 8: WCSS & Silhouette Scores (K = 2 to 6)"
    p_t8.font.bold = True
    p_t8.font.size = Pt(11.5)
    p_t8.font.color.rgb = ACCENT_PURPLE

    # Table 8
    t8_s = slide12.shapes.add_table(6, 4, Inches(1.0), Inches(2.25), Inches(5.1), Inches(1.9))
    t8 = t8_s.table
    t8.columns[0].width = Inches(1.1)
    t8.columns[1].width = Inches(1.3)
    t8.columns[2].width = Inches(1.3)
    t8.columns[3].width = Inches(1.4)

    headers_t8 = ["Clusters", "WCSS", "% Drop", "Silhouette"]
    for j, h in enumerate(headers_t8):
        c = t8.cell(0, j)
        c.fill.solid()
        c.fill.fore_color.rgb = DARK_CARD
        p = c.text_frame.paragraphs[0]
        p.text = h
        p.font.bold = True
        p.font.size = Pt(9)
        p.font.color.rgb = WHITE
        p.alignment = PP_ALIGN.CENTER

    data_t8 = [
        ["K = 2", "1050.21", "-30.1%", "0.2874"],
        ["K = 3", "831.42", "-20.8%", "0.2833"],
        ["K = 4", "700.70", "-15.7%", "0.3037"],
        ["K = 5", "632.16", "-9.8%", "0.2180"],
        ["K = 6", "576.66", "-8.8%", "0.2224"]
    ]

    for i, row in enumerate(data_t8):
        for j, val in enumerate(row):
            c = t8.cell(i+1, j)
            c.fill.solid()
            c.fill.fore_color.rgb = RGBColor(245, 243, 255) if i == 1 else WHITE
            p = c.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(8.5)
            p.font.bold = (i == 1)
            p.font.color.rgb = ACCENT_PURPLE if i == 1 else TEXT_MAIN
            p.alignment = PP_ALIGN.CENTER

    tb_tax = slide12.shapes.add_textbox(Inches(1.0), Inches(4.3), Inches(5.1), Inches(2.2))
    tf_tax = tb_tax.text_frame
    tf_tax.word_wrap = True
    p_th = tf_tax.paragraphs[0]
    p_th.text = "Selected K = 3 Taxonomy (Actionable Aid Policy):"
    p_th.font.bold = True
    p_th.font.size = Pt(10.5)
    p_th.font.color.rgb = TEXT_MAIN

    p_tb = tf_tax.add_paragraph()
    p_tb.text = "• Cluster 0 (36 nations - Developed): High GDP ($42.5k), life exp 80.1 yr, child mort 5.0 (Germany, Japan, USA).\n" \
                "• Cluster 1 (47 nations - Underdeveloped / Priority): Severe poverty, low GDP ($1,909), life exp 56.6 yr, child mort 92.96 (Haiti, Afghanistan, Mali).\n" \
                "• Cluster 2 (84 nations - Developing): Intermediate income ($12.3k), GDP ($6.5k), life exp 73.1 yr (India, Brazil, Indonesia)."
    p_tb.font.size = Pt(8.5)
    p_tb.font.color.rgb = TEXT_MAIN
    p_tb.space_before = Pt(3)

    # Right: Figure 9 (Elbow and Silhouette)
    add_card(slide12, 6.5, 1.7, 6.033, 4.9)
    tb_f9_t = slide12.shapes.add_textbox(Inches(6.7), Inches(1.8), Inches(5.6), Inches(0.4))
    tf_f9 = tb_f9_t.text_frame
    p_f9 = tf_f9.paragraphs[0]
    p_f9.text = "Figure 9: K-Means Elbow Curve & Silhouette Profile"
    p_f9.font.bold = True
    p_f9.font.size = Pt(11.5)
    p_f9.font.color.rgb = TEXT_MAIN

    fig9_path = os.path.abspath("extracted_figures/fig9_kmeans_elbow_silhouette.png")
    if os.path.exists(fig9_path):
        slide12.shapes.add_picture(fig9_path, Inches(6.6), Inches(2.3), width=Inches(5.8))

    tb_f9_c = slide12.shapes.add_textbox(Inches(6.7), Inches(5.35), Inches(5.6), Inches(1.1))
    tf_f9c = tb_f9_c.text_frame
    tf_f9c.word_wrap = True
    p_f9c = tf_f9c.paragraphs[0]
    p_f9c.text = "Why K = 3 is Preferred over Mathematical Peak K = 4:\n" \
                 "• Elbow Criterion: WCSS drops sharply by 20.8% from K=2 to K=3 (down to 831.42). Beyond K=3, reductions diminish rapidly.\n" \
                 "• Domain Interpretability: K=4 simply fragments the intermediate developing group into two sub-tiers without offering new strategic insight."
    p_f9c.font.size = Pt(9)
    p_f9c.font.color.rgb = TEXT_MUTED

    add_notes(slide12,
        "Here we examine the cluster selection criteria. Table 8 and Figure 9 display our Elbow curve and Silhouette scores across K=2 to 6. "
        "Notice that while K=4 produces the mathematical peak in silhouette score (0.3037), we selected K=3 for international policy alignment. "
        "The WCSS elbow levels off significantly after K=3 with diminishing returns. "
        "Crucially, K=3 partitions the 167 countries into three meaningful tiers: 36 Developed nations, 84 Developing nations, "
        "and 47 Underdeveloped nations that require immediate humanitarian assistance.")

    # ==========================================
    # SLIDE 13: Q3 - PCA: Mathematical Derivation & Eigendecomposition
    # ==========================================
    slide13 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide13, LIGHT_BG)
    add_header(slide13, "Question 3 · Unsupervised Learning & PCA", "PCA: First-Principles Covariance Derivation & Scree Analysis",
               "Decomposing the 9x9 sample covariance matrix into orthogonal eigenvectors and eigenvalues")
    add_footer(slide13, 13)

    # Left: Mathematical Steps & Scree Table
    add_card(slide13, 0.8, 1.7, 5.5, 4.9)
    tb_pca_m = slide13.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.1), Inches(4.7))
    tf_pm = tb_pca_m.text_frame
    tf_pm.word_wrap = True

    p = tf_pm.paragraphs[0]
    p.text = "Mathematical Formulation from First Principles"
    p.font.bold = True
    p.font.size = Pt(11.5)
    p.font.color.rgb = ACCENT_PURPLE

    p_steps = tf_pm.add_paragraph()
    p_steps.text = "1. Standardize Features: Zero mean, unit variance X_norm in R^{167 x 9}\n" \
                   "2. Sample Covariance Matrix:\n" \
                   "   Sigma = (1 / (N - 1)) * X_norm^T * X_norm in R^{9 x 9}\n" \
                   "3. Symmetric Eigendecomposition:\n" \
                   "   Sigma * v_k = lambda_k * v_k,  ||v_k||_2 = 1\n" \
                   "4. Explained Variance Ratio (EVR):\n" \
                   "   EVR_k = lambda_k / sum_{j=1}^9 lambda_j"
    p_steps.font.size = Pt(9.5)
    p_steps.font.color.rgb = TEXT_MAIN
    p_steps.space_before = Pt(3)

    p_t10_h = tf_pm.add_paragraph()
    p_t10_h.text = "Table 10: Eigendecomposition Results"
    p_t10_h.font.bold = True
    p_t10_h.font.size = Pt(10.5)
    p_t10_h.font.color.rgb = TEXT_MAIN
    p_t10_h.space_before = Pt(6)

    # Mini Table for Top Components
    t_evr_s = slide13.shapes.add_table(4, 4, Inches(1.0), Inches(4.2), Inches(5.1), Inches(1.4))
    t_evr = t_evr_s.table
    t_evr.columns[0].width = Inches(1.1)
    t_evr.columns[1].width = Inches(1.3)
    t_evr.columns[2].width = Inches(1.3)
    t_evr.columns[3].width = Inches(1.4)

    t_evr.cell(0, 0).text = "Component"
    t_evr.cell(0, 1).text = "Eigenvalue (lambda)"
    t_evr.cell(0, 2).text = "Individual EVR"
    t_evr.cell(0, 3).text = "Cumulative EVR"
    for j in range(4):
        c = t_evr.cell(0, j)
        c.fill.solid()
        c.fill.fore_color.rgb = DARK_CARD
        c.text_frame.paragraphs[0].font.bold = True
        c.text_frame.paragraphs[0].font.size = Pt(8.5)
        c.text_frame.paragraphs[0].font.color.rgb = WHITE
        c.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER

    data_evr = [
        ["PC1", "4.1606", "45.95%", "45.95%"],
        ["PC2", "1.5557", "17.18%", "63.13%"],
        ["PC3", "1.1774", "13.00%", "76.14%"]
    ]
    for i, row in enumerate(data_evr):
        for j, val in enumerate(row):
            c = t_evr.cell(i+1, j)
            c.fill.solid()
            c.fill.fore_color.rgb = WHITE
            p = c.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(8.5)
            p.alignment = PP_ALIGN.CENTER

    tb_trunc = slide13.shapes.add_textbox(Inches(1.0), Inches(5.75), Inches(5.1), Inches(0.8))
    tf_tr = tb_trunc.text_frame
    tf_tr.word_wrap = True
    p_tr = tf_tr.paragraphs[0]
    p_tr.text = "Variance Truncation: Top 3 principal components retain over 76.14% of the total dataset spread while reducing dimensions from 9 to 3."
    p_tr.font.size = Pt(9)
    p_tr.font.bold = True
    p_tr.font.color.rgb = ACCENT_PURPLE

    # Right: Figures 10 and 11
    add_card(slide13, 6.5, 1.7, 6.033, 4.9)
    fig10_path = os.path.abspath("extracted_figures/fig10_covariance_heatmap.png")
    fig11_path = os.path.abspath("extracted_figures/fig11_pca_scree.png")

    if os.path.exists(fig10_path):
        slide13.shapes.add_picture(fig10_path, Inches(6.7), Inches(1.85), width=Inches(2.75))
    if os.path.exists(fig11_path):
        slide13.shapes.add_picture(fig11_path, Inches(9.6), Inches(1.85), width=Inches(2.75))

    tb_figs_c = slide13.shapes.add_textbox(Inches(6.7), Inches(5.3), Inches(5.6), Inches(1.1))
    tf_fc = tb_figs_c.text_frame
    tf_fc.word_wrap = True
    p_fc = tf_fc.paragraphs[0]
    p_fc.text = "Figure 10 & 11 Insights:\n" \
                 "• Left Heatmap (Fig 10): Shows strong collinear blocks (e.g., child mortality vs life expectancy r = -0.89), validating the need for PCA.\n" \
                 "• Right Scree Plot (Fig 11): Eigenvalues drop below Kaiser criterion (lambda < 1) after PC3 (lambda_4 = 1.0008, leveling into flat noise tail)."
    p_fc.font.size = Pt(9)
    p_fc.font.color.rgb = TEXT_MUTED

    add_notes(slide13,
        "In Slide 13, we derive Principal Component Analysis mathematically from first principles. "
        "We compute the sample covariance matrix Sigma on the standardized data, and solve the symmetric eigenvalue problem Sigma v = lambda v. "
        "As reported in Table 10, the first principal component alone accounts for 45.95% of total variance. "
        "Adding PC2 and PC3 brings cumulative explained variance to 76.14%. "
        "The Scree plot on the right (Figure 11) confirms that after PC3, eigenvalues drop to approximately 1.0, "
        "proving that a 3-dimensional subspace captures three-quarters of all information in the original 9 dimensions.")

    # ==========================================
    # SLIDE 14: Q3 - PCA: Factor Loadings & 2D/3D Projections
    # ==========================================
    slide14 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide14, LIGHT_BG)
    add_header(slide14, "Question 3 · Unsupervised Learning & PCA", "Factor Loadings & 2D / 3D Subspace Visualizations",
               "Interpreting principal component axes and projecting K-Means clusters into low-dimensional space")
    add_footer(slide14, 14)

    # Left: Factor Loadings Matrix Table 11
    add_card(slide14, 0.8, 1.7, 5.4, 4.9)
    tb_f_t = slide14.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.0), Inches(0.4))
    tf_ft = tb_f_t.text_frame
    p_ft = tf_ft.paragraphs[0]
    p_ft.text = "Table 11: Factor Loadings & Semantic Axes"
    p_ft.font.bold = True
    p_ft.font.size = Pt(11)
    p_ft.font.color.rgb = ACCENT_PURPLE

    # Loadings table
    t_load_s = slide14.shapes.add_table(4, 4, Inches(1.0), Inches(2.2), Inches(5.0), Inches(1.5))
    t_load = t_load_s.table
    t_load.columns[0].width = Inches(1.1)
    t_load.columns[1].width = Inches(0.9)
    t_load.columns[2].width = Inches(1.5)
    t_load.columns[3].width = Inches(1.5)

    t_load.cell(0, 0).text = "Axis"
    t_load.cell(0, 1).text = "EVR"
    t_load.cell(0, 2).text = "Top Positive"
    t_load.cell(0, 3).text = "Top Negative"
    for j in range(4):
        c = t_load.cell(0, j)
        c.fill.solid()
        c.fill.fore_color.rgb = DARK_CARD
        c.text_frame.paragraphs[0].font.bold = True
        c.text_frame.paragraphs[0].font.size = Pt(8.5)
        c.text_frame.paragraphs[0].font.color.rgb = WHITE
        c.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER

    data_load = [
        ["PC1", "45.95%", "life_expec (+0.43)\nincome (+0.40)", "child_mort (-0.42)\ntotal_fer (-0.40)"],
        ["PC2", "17.18%", "imports (+0.67)\nexports (+0.61)", "income (+0.02)\ngdpp (-0.05)"],
        ["PC3", "13.00%", "health (+0.60)\ntotal_fer (+0.03)", "inflation (-0.64)\nexports (-0.14)"]
    ]
    for i, row in enumerate(data_load):
        for j, val in enumerate(row):
            c = t_load.cell(i+1, j)
            c.fill.solid()
            c.fill.fore_color.rgb = WHITE
            p = c.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(8)
            p.alignment = PP_ALIGN.CENTER

    tb_load_notes = slide14.shapes.add_textbox(Inches(1.0), Inches(4.0), Inches(5.0), Inches(2.5))
    tf_ln = tb_load_notes.text_frame
    tf_ln.word_wrap = True
    p_ln1 = tf_ln.paragraphs[0]
    p_ln1.text = "Semantic Interpretation of Axes:"
    p_ln1.font.bold = True
    p_ln1.font.size = Pt(10.5)
    p_ln1.font.color.rgb = TEXT_MAIN

    p_ln2 = tf_ln.add_paragraph()
    p_ln2.text = "• PC1 (Socio-Economic Development): Separates wealthy, healthy nations from high-mortality, impoverished nations.\n" \
                 "• PC2 (Trade Openness): Isolates trade hubs and entrepôts (Singapore, Luxembourg, Malta) regardless of population size.\n" \
                 "• PC3 (Macroeconomic Stability): Contrasts health spending investment against inflation volatility."
    p_ln2.font.size = Pt(8.5)
    p_ln2.font.color.rgb = TEXT_MAIN
    p_ln2.space_before = Pt(3)

    # Right: Figures 12 and 13 (2D & 3D Projections)
    add_card(slide14, 6.4, 1.7, 6.133, 4.9)
    fig12_path = os.path.abspath("extracted_figures/fig12_pca_2d.png")
    fig13_path = os.path.abspath("extracted_figures/fig13_pca_3d.png")

    if os.path.exists(fig12_path):
        slide14.shapes.add_picture(fig12_path, Inches(6.55), Inches(1.85), width=Inches(2.85))
    if os.path.exists(fig13_path):
        slide14.shapes.add_picture(fig13_path, Inches(9.55), Inches(1.85), width=Inches(2.85))

    tb_proj_c = slide14.shapes.add_textbox(Inches(6.55), Inches(5.35), Inches(5.8), Inches(1.1))
    tf_pc = tb_proj_c.text_frame
    tf_pc.word_wrap = True
    p_pc = tf_pc.paragraphs[0]
    p_pc.text = "Harmonious Synthesis: K-Means Overlaid on PCA\n" \
                 "• The 2D (Fig 12) and 3D (Fig 13) projections show clean, non-overlapping cluster boundaries.\n" \
                 "• Why they agree: Both PCA and K-Means minimize squared Euclidean distances on standardized data. PCA identifies directions of maximal variance, where cluster centroids naturally spread."
    p_pc.font.size = Pt(9)
    p_pc.font.color.rgb = TEXT_MUTED

    add_notes(slide14,
        "Slide 14 reveals the semantic meaning of our principal components and connects PCA back to K-Means. "
        "By analyzing the factor loadings in Table 11, PC1 clearly represents Socio-Economic Development, contrasting life expectancy against child mortality. "
        "PC2 captures Trade Openness, separating international trading hubs like Singapore and Luxembourg. "
        "When we project our 167 nations into the 2D and 3D PCA subspaces and color them by their K-Means cluster (Figures 12 and 13), "
        "we observe clean, distinct cluster separations. This demonstrates complete geometrical harmony between unsupervised clustering and dimensionality reduction.")

    # ==========================================
    # SLIDE 15: Cross-Project Synthesis & Core Takeaways
    # ==========================================
    slide15 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide15, LIGHT_BG)
    add_header(slide15, "Conclusions & Synthesis", "Cross-Domain Summary & Fundamental ML Takeaways",
               "Synthesizing optimal models, hyperparameter configurations, and core engineering principles")
    add_footer(slide15, 15)

    # Table 12 Master Summary across top
    add_card(slide15, 0.8, 1.7, 11.733, 2.7)
    tb_t12_t = slide15.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(0.35))
    tf_t12 = tb_t12_t.text_frame
    p_t12 = tf_t12.paragraphs[0]
    p_t12.text = "Table 12: Final Synthesis of Champion Models across All Problems"
    p_t12.font.bold = True
    p_t12.font.size = Pt(11)
    p_t12.font.color.rgb = ACCENT_BLUE

    # Table 12
    t12_s = slide15.shapes.add_table(5, 5, Inches(1.0), Inches(2.2), Inches(11.333), Inches(2.0))
    t12 = t12_s.table
    t12.columns[0].width = Inches(2.3)
    t12.columns[1].width = Inches(2.5)
    t12.columns[2].width = Inches(2.1)
    t12.columns[3].width = Inches(2.2)
    t12.columns[4].width = Inches(2.233)

    headers_t12 = ["Problem Domain", "Evaluated Suite", "Selected Model", "Optimal Hyperparams", "Test Performance"]
    for j, h in enumerate(headers_t12):
        c = t12.cell(0, j)
        c.fill.solid()
        c.fill.fore_color.rgb = DARK_CARD
        p = c.text_frame.paragraphs[0]
        p.text = h
        p.font.bold = True
        p.font.size = Pt(9)
        p.font.color.rgb = WHITE
        p.alignment = PP_ALIGN.CENTER

    data_t12 = [
        ["Q1: Classification", "KNN, DT, SVM, CNN", "SVM (RBF Kernel)", "C = 5.0, gamma = 'scale'", "Acc: 92.40% · F1: 0.9014 · AUC: 0.9697"],
        ["Q1 Bonus: Deep Learning", "Deep 1D CNN", "Deep 1D CNN", "3 Conv Blocks, Adam 1e-3", "Acc: 91.53% · F1: 0.8926 · AUC: 0.9718"],
        ["Q2: Regression", "SGD, Ridge, Lasso, Poly", "Poly Ridge (All 81)", "Degree-2, Ridge alpha=10.0", "R^2: 0.8542 · RMSE: 12.95 K (vs 17.5 K)"],
        ["Q3: Unsupervised & PCA", "K-Means, Covariance PCA", "K-Means (K=3) & PCA", "K=3 clusters, Top 3 PCs", "WCSS: 831.42 · Cumul. Var: 76.14%"]
    ]

    for i, row in enumerate(data_t12):
        for j, val in enumerate(row):
            c = t12.cell(i+1, j)
            c.fill.solid()
            c.fill.fore_color.rgb = WHITE
            p = c.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(8.5)
            p.font.bold = (j == 2)
            p.alignment = PP_ALIGN.LEFT if j in [0, 1] else PP_ALIGN.CENTER

    # 4 Key Takeaways Cards across bottom
    takeaways = [
        ("1. Pipeline Integrity", "Encapsulating scalers inside pipelines completely eliminates data leakage across CV folds.", ACCENT_BLUE),
        ("2. Regularization", "Mandatory when scaling feature capacity (Tree pruning, SVM C, Ridge/Lasso alpha, Dropout).", ACCENT_GREEN),
        ("3. Non-Linear Synergy", "Capturing 3,402 atomic interactions outperformed all linear hyperparameter tuning (+16.5% R^2).", ACCENT_AMBER),
        ("4. Statistical Validation", "1,000 bootstrap resamples prevented false superiority claims between SVM and CNN.", ACCENT_PURPLE)
    ]

    for i, (tk_h, tk_b, tk_c) in enumerate(takeaways):
        left_pos = 0.8 + i * 3.0
        c = add_card(slide15, left_pos, 4.6, 2.733, 2.0, WHITE, tk_c)
        tb = slide15.shapes.add_textbox(Inches(left_pos + 0.15), Inches(4.7), Inches(2.433), Inches(1.8))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = tk_h
        p1.font.bold = True
        p1.font.size = Pt(10)
        p1.font.color.rgb = tk_c
        p2 = tf.add_paragraph()
        p2.text = tk_b
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = TEXT_MAIN
        p2.space_before = Pt(4)

    add_notes(slide15,
        "Slide 15 brings together our entire project findings into Table 12. "
        "Across all three domains, we observe consistent core principles: "
        "First, Pipeline encapsulation prevents subtle data leakage. "
        "Second, regularization is indispensable whenever model capacity is increased. "
        "Third, physical representation learning—such as polynomial interaction terms in regression—yields dramatically higher returns than tuning linear models. "
        "And fourth, bootstrap resampling provides the statistical rigor required to substantiate model comparisons.")

    # ==========================================
    # SLIDE 16: Conclusion & Audience Q&A (Dark Theme)
    # ==========================================
    slide16 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide16, DARK_BG)

    # Accent top bar
    bar16 = slide16.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.12))
    bar16.fill.solid()
    bar16.fill.fore_color.rgb = ACCENT_BLUE
    bar16.line.fill.background()

    # Title box
    tbox16 = slide16.shapes.add_textbox(Inches(1.2), Inches(1.3), Inches(11.0), Inches(1.6))
    tf16 = tbox16.text_frame
    tf16.word_wrap = True
    p16 = tf16.paragraphs[0]
    p16.text = "Thank You!"
    p16.font.name = FONT_HEADING
    p16.font.size = Pt(40)
    p16.font.bold = True
    p16.font.color.rgb = WHITE

    p16_sub = tf16.add_paragraph()
    p16_sub.text = "We welcome any questions, discussions, and feedback."
    p16_sub.font.name = FONT_BODY
    p16_sub.font.size = Pt(20)
    p16_sub.font.color.rgb = RGBColor(203, 213, 225)
    p16_sub.space_before = Pt(8)

    # 3 Summary Highlight Cards
    highlights = [
        ("Supervised Classification", "SVM (RBF) achieved 92.40% accuracy and 92.22% precision, backed by overlapping bootstrap ROC-AUC with 1D CNN.", ACCENT_BLUE),
        ("Non-Linear Regression", "Full 81-feature Polynomial Ridge achieved R^2 = 0.8542 and reduced RMSE to 12.95 K (+16.5% gain).", ACCENT_GREEN),
        ("Clustering & PCA", "K-Means (K=3) identified actionable humanitarian tiers; PCA captured 76.14% variance across 3 orthogonal axes.", ACCENT_PURPLE)
    ]
    for i, (hl_t, hl_b, hl_c) in enumerate(highlights):
        left_hl = 1.2 + i * 3.8
        c = add_card(slide16, left_hl, 3.4, 3.4, 1.8, DARK_CARD, hl_c)
        tb = slide16.shapes.add_textbox(Inches(left_hl + 0.2), Inches(3.55), Inches(3.0), Inches(1.5))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = hl_t
        p1.font.bold = True
        p1.font.size = Pt(12)
        p1.font.color.rgb = WHITE
        p2 = tf.add_paragraph()
        p2.text = hl_b
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = TEXT_MUTED_LIGHT
        p2.space_before = Pt(4)

    # Contact & Credits
    cbox = slide16.shapes.add_textbox(Inches(1.2), Inches(5.6), Inches(11.0), Inches(1.2))
    tf_c = cbox.text_frame
    p_c1 = tf_c.paragraphs[0]
    p_c1.text = "Project Team:  Yashasvee Patel (S20240010266)  &  P Karthik (S20240010184)"
    p_c1.font.bold = True
    p_c1.font.size = Pt(13)
    p_c1.font.color.rgb = WHITE

    p_c2 = tf_c.add_paragraph()
    p_c2.text = "Department of Computer Science & Engineering  ·  Indian Institute of Information Technology, Sri City\nCodebase & Full Technical Report available in repository."
    p_c2.font.size = Pt(11)
    p_c2.font.color.rgb = TEXT_MUTED_LIGHT
    p_c2.space_before = Pt(4)

    add_notes(slide16,
        "In conclusion, this project demonstrated practical and theoretical mastery across classification, regression, and unsupervised learning. "
        "We thank our professors and peers for their guidance, and we are now delighted to answer any questions. Thank you!")

    # Save presentation
    output_pptx = "ML_Course_Project_Presentation.pptx"
    prs.save(output_pptx)
    print(f"Presentation successfully saved to: {output_pptx}")

if __name__ == "__main__":
    create_presentation()

