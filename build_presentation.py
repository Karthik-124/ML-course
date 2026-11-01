"""
build_presentation.py
Generates a concise, high-impact 12-slide widescreen PowerPoint deck (ML_Course_Project_Presentation.pptx)
meeting the requirement of "approximately 10–15 slides".
Authors: Yashasvee Patel (S20240010266) & P Karthik (S20240010184)
Department of Computer Science & Engineering, IIIT Sri City
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

FONT_HEADING = "Calibri"
FONT_BODY = "Calibri"

TOTAL_SLIDES = 12

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

    bar = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.12))
    bar.fill.solid()
    bar.fill.fore_color.rgb = ACCENT_BLUE
    bar.line.fill.background()

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
    p2.text = "Supervised Classification, Regularized Non-Linear Regression,\nand Unsupervised Clustering & Dimensionality Reduction"
    p2.font.name = FONT_BODY
    p2.font.size = Pt(18)
    p2.font.color.rgb = RGBColor(203, 213, 225)
    p2.space_before = Pt(10)

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
        "regularized non-linear regression on superconducting critical temperatures, and unsupervised clustering with PCA "
        "on international socio-economic development data. We will walk you through our methodology, implementations, and empirical results.")

    # ==========================================
    # SLIDE 2: Project Architecture & Scientific Protocol
    # ==========================================
    slide2 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide2, LIGHT_BG)
    add_header(slide2, "Executive Overview", "Project Architecture & Experimental Rigor",
               "Three diverse machine learning challenges unified by strict scientific validation and zero data leakage")
    add_footer(slide2, 2)

    col_w = Inches(3.65)
    gap = Inches(0.39)
    start_x = Inches(0.8)

    cards_data = [
        ("Domain 1: Classification", ACCENT_BLUE, "UCI Spambase Dataset",
         "• 4,601 Email records, 57 continuous lexical features\n"
         "• Predict Spam (39.4%) vs Ham (60.6%)\n"
         "• Models: KNN (k=3), CART Tree (d=12), SVM RBF (C=5), Deep 1D CNN\n"
         "• Validation: 5-Fold Stratified CV, confusion matrices, 1,000 bootstrap CIs"),

        ("Domain 2: Regression", ACCENT_GREEN, "Superconductivity Tc Prediction",
         "• 21,263 Superconductors, 81 continuous elemental features\n"
         "• Predict Critical Transition Temp Tc in Kelvin\n"
         "• Models: Linear SGD, Ridge (L2), Lasso (L1), Degree-2 Poly Ridge\n"
         "• Validation: Degree sweeps (1 to 4) analyzing underfitting to variance blowup"),

        ("Domain 3: Clustering & PCA", ACCENT_PURPLE, "HELP International Country Data",
         "• 167 Nations evaluated across 9 socio-economic indicators\n"
         "• Unsupervised aid targeting & dimensionality reduction\n"
         "• Models: Lloyd's K-Means & Covariance Matrix PCA from first principles\n"
         "• Validation: WCSS Elbow drop, Silhouette profile, 76.14% variance in 2D/3D")
    ]

    for i, (title, color, dataset, bullets) in enumerate(cards_data):
        cx = start_x + i * (col_w + gap)
        c = add_card(slide2, cx, 1.7, col_w, 3.8)

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
                "2. All scalers (StandardScaler) encapsulated strictly inside scikit-learn Pipelines so test distributions never contaminate training folds.  " \
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
    # SLIDE 3: Q1 - Classification: Methodology & Implementation
    # ==========================================
    slide3 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide3, LIGHT_BG)
    add_header(slide3, "Question 1 · Supervised Classification", "Classification: Methodology & Model Implementation",
               "UCI Spambase dataset formulation, 4 classifier paradigms, and 5-fold cross-validation sweeps")
    add_footer(slide3, 3)

    # Left: Dataset & Architectures
    add_card(slide3, 0.8, 1.7, 5.6, 4.9)
    tb_q1_m = slide3.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.2), Inches(4.7))
    tf_q1m = tb_q1_m.text_frame
    tf_q1m.word_wrap = True

    p = tf_q1m.paragraphs[0]
    p.text = "UCI Spambase Dataset (N = 4,601)"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = ACCENT_BLUE

    p_body = tf_q1m.add_paragraph()
    p_body.text = "• 80% Train (3,680) / 20% Test (921) stratified split.\n" \
                  "• Class Balance: 1,813 Spam (39.4%) vs. 2,788 Ham (60.6%).\n" \
                  "• 57 Features: 48 word freqs, 6 char freqs, 3 capital run-length stats.\n" \
                  "• Asymmetric Cost: False Positives (important email to spam) are far more costly than False Negatives → Precision is prioritized."
    p_body.font.size = Pt(9.5)
    p_body.font.color.rgb = TEXT_MAIN
    p_body.space_before = Pt(4)

    p_arch = tf_q1m.add_paragraph()
    p_arch.text = "4 Evaluated Algorithmic Paradigms:"
    p_arch.font.bold = True
    p_arch.font.size = Pt(11)
    p_arch.font.color.rgb = TEXT_MAIN
    p_arch.space_before = Pt(8)

    p_arch_b = tf_q1m.add_paragraph()
    p_arch_b.text = "1. KNN (k=3 via CV): Euclidean metric, 90.76% CV accuracy.\n" \
                    "2. Decision Tree (CART, d=12 via CV): Gini impurity splits, 91.85% CV accuracy.\n" \
                    "3. SVM (RBF Kernel, C=5.0 via CV): Soft-margin RKHS boundary, 93.15% CV accuracy.\n" \
                    "4. Deep 1D CNN (Bonus PyTorch): 3 Conv1d blocks (32->64->128), BatchNorm, Dropout (0.3), Adam optimizer."
    p_arch_b.font.size = Pt(9.5)
    p_arch_b.font.color.rgb = TEXT_MAIN
    p_arch_b.space_before = Pt(2)

    # Right: Figures 1 & 2
    add_card(slide3, 6.6, 1.7, 5.933, 4.9)
    fig1_path = os.path.abspath("extracted_figures/fig1_classification_cv.png")
    fig2_path = os.path.abspath("extracted_figures/fig2_svm_cv.png")

    if os.path.exists(fig1_path):
        slide3.shapes.add_picture(fig1_path, Inches(6.75), Inches(1.85), width=Inches(5.6))
    if os.path.exists(fig2_path):
        slide3.shapes.add_picture(fig2_path, Inches(7.5), Inches(4.0), width=Inches(4.1))

    tb_cv_c = slide3.shapes.add_textbox(Inches(6.8), Inches(6.15), Inches(5.5), Inches(0.4))
    tf_cv = tb_cv_c.text_frame
    p_cv = tf_cv.paragraphs[0]
    p_cv.text = "Figure 1 & 2: 5-Fold CV tuning for KNN (k=3), Tree (depth=12), and SVM (C=5.0)."
    p_cv.font.size = Pt(9)
    p_cv.font.color.rgb = TEXT_MUTED

    add_notes(slide3,
        "In Question 1, we tackle binary classification on the UCI Spambase dataset of 4,601 emails. "
        "Notice the 57 features and asymmetric misclassification penalty: false alarms are unacceptable in email filtering. "
        "We evaluated four distinct paradigms: instance-based KNN, recursive CART Decision Trees, maximum-margin SVM with RBF kernel, "
        "and a Deep 1D CNN. Figures 1 and 2 show our 5-fold cross-validation sweeps on the training folds, establishing optimal hyperparameters.")

    # ==========================================
    # SLIDE 4: Q1 - Classification: Results & Model Selection
    # ==========================================
    slide4 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide4, LIGHT_BG)
    add_header(slide4, "Question 1 · Supervised Classification", "Classification: Experimental Results & Model Selection",
               "Test set evaluation on 921 emails, confusion matrices, and 1,000 bootstrap ROC-AUC confidence intervals")
    add_footer(slide4, 4)

    # Left: Table 4 & Insights
    add_card(slide4, 0.8, 1.7, 5.8, 4.9)
    tb_t4_t = slide4.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.4), Inches(0.35))
    tf_t4 = tb_t4_t.text_frame
    p_t4 = tf_t4.paragraphs[0]
    p_t4.text = "Table 4: Test Performance Metrics (N = 921 Emails)"
    p_t4.font.bold = True
    p_t4.font.size = Pt(11)
    p_t4.font.color.rgb = ACCENT_BLUE

    table_shape = slide4.shapes.add_table(5, 5, Inches(1.0), Inches(2.2), Inches(5.4), Inches(1.7))
    table = table_shape.table
    table.columns[0].width = Inches(1.5)
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
        p.font.size = Pt(9)
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
            p.font.size = Pt(8.5)
            p.font.bold = (i == 2)
            p.font.color.rgb = ACCENT_BLUE if i == 2 else TEXT_MAIN
            p.alignment = PP_ALIGN.LEFT if j == 0 else PP_ALIGN.CENTER

    tb_t4_notes = slide4.shapes.add_textbox(Inches(1.0), Inches(4.0), Inches(5.4), Inches(2.5))
    tf_t4n = tb_t4_notes.text_frame
    tf_t4n.word_wrap = True
    p_n1 = tf_t4n.paragraphs[0]
    p_n1.text = "Empirical Findings & Model Selection:"
    p_n1.font.bold = True
    p_n1.font.size = Pt(10.5)
    p_n1.font.color.rgb = TEXT_MAIN

    p_n2 = tf_t4n.add_paragraph()
    p_n2.text = "• SVM Champion: Highest accuracy (92.40%), top F1 (0.9014), and highest Precision (92.22%) with only 27 False Positives.\n" \
                 "• Deep 1D CNN: Highest Recall (89.26%), catching the most spam.\n" \
                 "• Bootstrap ROC-AUC Statistical Rigor (1,000 resamples):\n" \
                 "  - Deep CNN: 0.9718 [95% CI: 0.961 – 0.981]\n" \
                 "  - SVM (RBF): 0.9697 [95% CI: 0.959 – 0.979]\n" \
                 "  - Heavy overlap proves statistical tie; SVM selected for top precision and zero GPU overhead."
    p_n2.font.size = Pt(8.5)
    p_n2.font.color.rgb = TEXT_MAIN
    p_n2.space_before = Pt(3)

    # Right: Figures 3 & 5
    add_card(slide4, 6.8, 1.7, 5.733, 4.9)
    fig3_path = os.path.abspath("extracted_figures/fig3_confusion_matrices.png")
    fig5_path = os.path.abspath("extracted_figures/fig5_roc_curves.png")

    if os.path.exists(fig3_path):
        slide4.shapes.add_picture(fig3_path, Inches(6.95), Inches(1.85), width=Inches(2.75))
    if os.path.exists(fig5_path):
        slide4.shapes.add_picture(fig5_path, Inches(9.75), Inches(1.85), width=Inches(2.65))

    tb_figs_c = slide4.shapes.add_textbox(Inches(6.95), Inches(5.45), Inches(5.4), Inches(0.9))
    tf_fc = tb_figs_c.text_frame
    tf_fc.word_wrap = True
    p_fc = tf_fc.paragraphs[0]
    p_fc.text = "Left: Figure 3 (Confusion Matrices showing SVM's low False Positives).\n" \
                 "Right: Figure 5 (ROC curves with 1,000 bootstrap 95% confidence intervals)."
    p_fc.font.size = Pt(8.5)
    p_fc.font.color.rgb = TEXT_MUTED

    add_notes(slide4,
        "Here are the core classification test results on the 921 test emails. "
        "Looking at Table 4, SVM with RBF kernel achieves the highest overall accuracy at 92.40% and top F1-score of 0.9014. "
        "Most importantly, looking at the confusion matrices (Figure 3), SVM generated only 27 False Positives, giving it the highest precision of 92.22%. "
        "On ROC-AUC (Figure 5), 1,000 bootstrap resamples showed overlapping confidence intervals between SVM and CNN, proving a statistical tie. "
        "We selected SVM as champion based on precision, simplicity, and efficiency.")

    # ==========================================
    # SLIDE 5: Q2 - Regression: Methodology & Linear Models
    # ==========================================
    slide5 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide5, LIGHT_BG)
    add_header(slide5, "Question 2 · Non-Linear Regression & Regularization", "Regression: Methodology & Regularized Linear Models",
               "Superconductivity critical temperature (Tc) prediction, 81 atomic features, and linear performance ceilings")
    add_footer(slide5, 5)

    add_card(slide5, 0.8, 1.7, 5.6, 4.9)
    tb_reg_m = slide5.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.2), Inches(4.7))
    tf_rm = tb_reg_m.text_frame
    tf_rm.word_wrap = True

    p = tf_rm.paragraphs[0]
    p.text = "Superconductivity Dataset (N = 21,263)"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = ACCENT_GREEN

    p_body2 = tf_rm.add_paragraph()
    p_body2.text = "• 80% Train (17,010) / 20% Test (4,253) split.\n" \
                   "• Target Tc: Critical temp in Kelvin (0.00021 K to 185 K, Mean 34.42 K).\n" \
                   "• 81 Features: Statistics across 8 atomic properties (atomic mass, radius, valence, thermal conductivity, etc.).\n" \
                   "• Physical Challenge: High multicollinearity (|r| > 0.85) and non-linear quantum electron-phonon coupling."
    p_body2.font.size = Pt(9.5)
    p_body2.font.color.rgb = TEXT_MAIN
    p_body2.space_before = Pt(4)

    p_lin = tf_rm.add_paragraph()
    p_lin.text = "Linear Models & Regularization:"
    p_lin.font.bold = True
    p_lin.font.size = Pt(11)
    p_lin.font.color.rgb = TEXT_MAIN
    p_lin.space_before = Pt(8)

    p_lin_b = tf_rm.add_paragraph()
    p_lin_b.text = "• Linear SGD: Standard OLS MSE minimization (R^2 = 0.7332, RMSE = 17.52 K).\n" \
                   "• Ridge (L2): J(w) = MSE + alpha*||w||_2^2. Handles collinearity (optimal alpha=0.1, R^2 = 0.7375, RMSE = 17.38 K).\n" \
                   "• Lasso (L1): J(w) = MSE + alpha*||w||_1. Enforces sparsity (optimal alpha=1e-5, R^2 = 0.7375).\n" \
                   "• The Linear Ceiling: All linear models hit a hard cap at R^2 ~ 0.738. Regularization controls variance but cannot overcome linear high bias."
    p_lin_b.font.size = Pt(9)
    p_lin_b.font.color.rgb = TEXT_MAIN
    p_lin_b.space_before = Pt(2)

    add_card(slide5, 6.6, 1.7, 5.933, 4.9)
    tb_f6_t = slide5.shapes.add_textbox(Inches(6.8), Inches(1.8), Inches(5.5), Inches(0.4))
    tf_f6 = tb_f6_t.text_frame
    p_f6 = tf_f6.paragraphs[0]
    p_f6.text = "Figure 6: 5-Fold Cross-Validation for Ridge & Lasso"
    p_f6.font.bold = True
    p_f6.font.size = Pt(11)
    p_f6.font.color.rgb = TEXT_MAIN

    fig6_path = os.path.abspath("extracted_figures/fig6_ridge_lasso_cv.png")
    if os.path.exists(fig6_path):
        slide5.shapes.add_picture(fig6_path, Inches(6.75), Inches(2.3), width=Inches(5.6))

    tb_f6_c = slide5.shapes.add_textbox(Inches(6.8), Inches(5.35), Inches(5.5), Inches(1.1))
    tf_f6c = tb_f6_c.text_frame
    tf_f6c.word_wrap = True
    p_f6c = tf_f6c.paragraphs[0]
    p_f6c.text = "Alpha Grid Search Findings:\n" \
                 "• Left (Ridge): Stable for alpha < 10. Beyond alpha=100, heavy L2 penalty causes excessive shrinkage and underfitting.\n" \
                 "• Right (Lasso): Above alpha=1e-3, sparsity aggressively zeroes out useful predictors, causing CV R^2 to drop sharply."
    p_f6c.font.size = Pt(9)
    p_f6c.font.color.rgb = TEXT_MUTED

    add_notes(slide5,
        "Moving to Question 2, we predict the critical temperature Tc of 21,263 superconductors using 81 continuous features. "
        "As seen in Figure 6, we ran 5-fold cross-validation across alpha grids for Ridge and Lasso. "
        "Ridge with alpha=0.1 and Lasso with alpha=1e-5 both reached an R^2 of 0.7375 and RMSE of 17.38 Kelvin. "
        "However, notice the fundamental limitation: all linear models hit a performance ceiling at R^2 ~ 0.738. "
        "Regularization successfully stabilizes collinearity, but cannot overcome linear high bias on quantum phenomena.")

    # ==========================================
    # SLIDE 6: Q2 - Regression: Non-Linear Capacity & Overfitting Sweep
    # ==========================================
    slide6 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide6, LIGHT_BG)
    add_header(slide6, "Question 2 · Non-Linear Regression & Regularization", "Non-Linear Implementation & Overfitting Analysis",
               "Pearson correlation feature selection and degree sweep (1 to 4) illustrating capacity transitions")
    add_footer(slide6, 6)

    add_card(slide6, 0.8, 1.7, 4.6, 4.9)
    tb_cor_t = slide6.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(4.2), Inches(0.4))
    tf_cor = tb_cor_t.text_frame
    p_cor = tf_cor.paragraphs[0]
    p_cor.text = "Top Features by Pearson Correlation (|r|)"
    p_cor.font.bold = True
    p_cor.font.size = Pt(11)
    p_cor.font.color.rgb = ACCENT_GREEN

    t_cor_s = slide6.shapes.add_table(6, 2, Inches(1.0), Inches(2.25), Inches(4.2), Inches(1.8))
    t_cor = t_cor_s.table
    t_cor.columns[0].width = Inches(2.9)
    t_cor.columns[1].width = Inches(1.3)

    t_cor.cell(0, 0).text = "Selected Feature"
    t_cor.cell(0, 1).text = "Corr (r)"
    for cell in [t_cor.cell(0, 0), t_cor.cell(0, 1)]:
        cell.fill.solid()
        cell.fill.fore_color.rgb = DARK_CARD
        cell.text_frame.paragraphs[0].font.bold = True
        cell.text_frame.paragraphs[0].font.size = Pt(9)
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

    tb_deg_notes = slide6.shapes.add_textbox(Inches(1.0), Inches(4.2), Inches(4.2), Inches(2.3))
    tf_dn = tb_deg_notes.text_frame
    tf_dn.word_wrap = True
    p_dn1 = tf_dn.paragraphs[0]
    p_dn1.text = "Degree Sweep on Top 15 Features:"
    p_dn1.font.bold = True
    p_dn1.font.size = Pt(10.5)
    p_dn1.font.color.rgb = TEXT_MAIN

    p_dn2 = tf_dn.add_paragraph()
    p_dn2.text = "• Degree 1 (15 terms): High Bias (R^2 = 0.735)\n" \
                 "• Degree 2 (135 terms): Balanced non-linear baseline (R^2 = 0.735)\n" \
                 "• Degree 3 (815 terms): Overfitting begins (train R^2=0.81, test drops)\n" \
                 "• Degree 4 (3,875 terms): Catastrophic explosion! Test MSE explodes due to ill-conditioned Vandermonde matrix."
    p_dn2.font.size = Pt(9)
    p_dn2.font.color.rgb = TEXT_MAIN
    p_dn2.space_before = Pt(3)

    add_card(slide6, 5.6, 1.7, 6.933, 4.9)
    tb_f7_t = slide6.shapes.add_textbox(Inches(5.8), Inches(1.8), Inches(6.5), Inches(0.4))
    tf_f7 = tb_f7_t.text_frame
    p_f7 = tf_f7.paragraphs[0]
    p_f7.text = "Figure 7: Polynomial Degree Sweep (Degrees 1 to 4)"
    p_f7.font.bold = True
    p_f7.font.size = Pt(11.5)
    p_f7.font.color.rgb = TEXT_MAIN

    fig7_path = os.path.abspath("extracted_figures/fig7_polynomial_sweep.png")
    if os.path.exists(fig7_path):
        slide6.shapes.add_picture(fig7_path, Inches(5.75), Inches(2.3), width=Inches(6.6))

    tb_f7_c = slide6.shapes.add_textbox(Inches(5.8), Inches(5.35), Inches(6.5), Inches(1.1))
    tf_f7c = tb_f7_c.text_frame
    tf_f7c.word_wrap = True
    p_f7c = tf_f7c.paragraphs[0]
    p_f7c.text = "Generalization Error Breakdown:\n" \
                 "• At d=1, train and test errors are identical but high (Underfitting / High Bias).\n" \
                 "• At d=4, train R^2 reaches 0.88, but unregularized test error diverges catastrophically (High Variance).\n" \
                 "• Conclusion: Polynomial expansion demands strict L2 regularization to control interaction variance."
    p_f7c.font.size = Pt(9)
    p_f7c.font.color.rgb = TEXT_MUTED

    add_notes(slide6,
        "To introduce non-linearity, we first selected the top 15 features by Pearson correlation and conducted a degree sweep from d=1 to d=4. "
        "Figure 7 demonstrates the textbook transition from underfitting to overfitting. "
        "At degree 1, we suffer from high bias. At degree 2, performance remains stable with 135 terms. "
        "At degree 3, we expand to 815 terms and training error pulls away from test error. "
        "Finally, at degree 4 with 3,875 terms, test error explodes completely. "
        "This proves that high-degree polynomial expansions without regularization suffer from severe variance and numerical instability.")

    # ==========================================
    # SLIDE 7: Q2 - Regression: Results & The Breakthrough
    # ==========================================
    slide7 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide7, LIGHT_BG)
    add_header(slide7, "Question 2 · Non-Linear Regression & Regularization", "Regression: Results & The Polynomial Breakthrough",
               "Capturing 3,402 cross-feature atomic interactions achieves R^2 = 0.8542 and reduces RMSE to 12.95 K")
    add_footer(slide7, 7)

    add_card(slide7, 0.8, 1.7, 5.8, 4.9)
    tb_t6_t = slide7.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.4), Inches(0.4))
    tf_t6 = tb_t6_t.text_frame
    p_t6 = tf_t6.paragraphs[0]
    p_t6.text = "Table 6: Complete Regression Model Comparison"
    p_t6.font.bold = True
    p_t6.font.size = Pt(11.5)
    p_t6.font.color.rgb = ACCENT_GREEN

    t6_s = slide7.shapes.add_table(6, 4, Inches(1.0), Inches(2.25), Inches(5.4), Inches(2.1))
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

    tb_bt = slide7.shapes.add_textbox(Inches(1.0), Inches(4.5), Inches(5.4), Inches(2.0))
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

    add_card(slide7, 6.8, 1.7, 5.733, 4.9)
    tb_f8_t = slide7.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.3), Inches(0.4))
    tf_f8 = tb_f8_t.text_frame
    p_f8 = tf_f8.paragraphs[0]
    p_f8.text = "Figure 8: Performance Comparison on Test Set"
    p_f8.font.bold = True
    p_f8.font.size = Pt(11.5)
    p_f8.font.color.rgb = TEXT_MAIN

    fig8_path = os.path.abspath("extracted_figures/fig8_regression_comparison.png")
    if os.path.exists(fig8_path):
        slide7.shapes.add_picture(fig8_path, Inches(6.9), Inches(2.3), width=Inches(5.5))

    tb_f8_c = slide7.shapes.add_textbox(Inches(7.0), Inches(5.35), Inches(5.3), Inches(1.1))
    tf_f8c = tb_f8_c.text_frame
    tf_f8c.word_wrap = True
    p_f8c = tf_f8c.paragraphs[0]
    p_f8c.text = "Visualizing the Performance Jump:\n" \
                 "• Left plot: Polynomial Ridge (All 81) sharply outperforms all other models in R^2 (0.8542 vs ~0.737).\n" \
                 "• Right plot: RMSE drops from ~17.4 K down to 12.95 K, cutting prediction error by more than 4.5 Kelvin."
    p_f8c.font.size = Pt(9)
    p_f8c.font.color.rgb = TEXT_MUTED

    add_notes(slide7,
        "Slide 7 highlights the major engineering breakthrough in our regression task. "
        "When we expanded all 81 elemental features to degree-2, we created 3,402 pairwise interaction terms. "
        "By applying Ridge regularization with alpha=10.0, we prevented overfitting on this massive feature space. "
        "As seen in Table 6 and Figure 8, our Test R^2 surged from 0.7332 to 0.8542, and our RMSE dropped from 17.52 Kelvin down to 12.95 Kelvin. "
        "This proves that capturing non-linear physical interactions between atomic properties—like thermal conductivity times valence—is "
        "far more impactful than any hyperparameter tuning of linear models.")

    # ==========================================
    # SLIDE 8: Q3 - Unsupervised: Methodology & Formulations
    # ==========================================
    slide8 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide8, LIGHT_BG)
    add_header(slide8, "Question 3 · Unsupervised Learning & PCA", "Unsupervised: Methodology & Mathematical Formulations",
               "HELP International dataset, feature standardization necessity, and from-scratch algorithms")
    add_footer(slide8, 8)

    add_card(slide8, 0.8, 1.7, 5.8, 4.9)
    tb_q3_m = slide8.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.4), Inches(4.7))
    tf_q3m = tb_q3_m.text_frame
    tf_q3m.word_wrap = True

    p = tf_q3m.paragraphs[0]
    p.text = "HELP International Country Dataset"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = ACCENT_PURPLE

    p_q3b = tf_q3m.add_paragraph()
    p_q3b.text = "• Objective: Unsupervised categorization of 167 nations for equitable foreign aid allocation.\n" \
                 "• 9 Indicators: child_mort, exports, health, imports, income, inflation, life_expec, total_fer, gdpp.\n" \
                 "• Standardization to Zero Mean & Unit Variance:\n" \
                 "  x_norm_ij = (x_ij - mean_j) / std_j\n" \
                 "  Mandatory because GDP ranges up to $105,000 while fertility is < 8. Unscaled features would cause wealth to dominate distance by 10,000x."
    p_q3b.font.size = Pt(9.5)
    p_q3b.font.color.rgb = TEXT_MAIN
    p_q3b.space_before = Pt(4)

    p_form = tf_q3m.add_paragraph()
    p_form.text = "From-Scratch Mathematical Formulations:"
    p_form.font.bold = True
    p_form.font.size = Pt(11)
    p_form.font.color.rgb = TEXT_MAIN
    p_form.space_before = Pt(8)

    p_form_b = tf_q3m.add_paragraph()
    p_form_b.text = "1. K-Means (Lloyd's): min sum_{k} sum_{x in S_k} ||x - mu_k||_2^2 with 10 restarts & K-Means++ init.\n" \
                    "2. Sample Covariance Matrix: Sigma = (1 / (N - 1)) * X_norm^T X_norm in R^{9x9}.\n" \
                    "3. Eigendecomposition: Sigma * v_k = lambda_k * v_k, with ||v_k||_2 = 1.\n" \
                    "4. Explained Variance Ratio: EVR_k = lambda_k / sum(lambda)."
    p_form_b.font.size = Pt(9)
    p_form_b.font.color.rgb = TEXT_MAIN
    p_form_b.space_before = Pt(2)

    add_card(slide8, 6.8, 1.7, 5.733, 4.9)
    tb_f10_t = slide8.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.3), Inches(0.4))
    tf_f10 = tb_f10_t.text_frame
    p_f10 = tf_f10.paragraphs[0]
    p_f10.text = "Figure 10: Sample Covariance Heatmap (9x9)"
    p_f10.font.bold = True
    p_f10.font.size = Pt(11.5)
    p_f10.font.color.rgb = TEXT_MAIN

    fig10_path = os.path.abspath("extracted_figures/fig10_covariance_heatmap.png")
    if os.path.exists(fig10_path):
        slide8.shapes.add_picture(fig10_path, Inches(7.55), Inches(2.25), width=Inches(4.2))

    tb_f10_c = slide8.shapes.add_textbox(Inches(7.0), Inches(5.6), Inches(5.3), Inches(0.9))
    tf_f10c = tb_f10_c.text_frame
    tf_f10c.word_wrap = True
    p_f10c = tf_f10c.paragraphs[0]
    p_f10c.text = "Heatmap Insights:\n" \
                  "• Reveals strong collinear blocks (child mortality vs life expectancy r = -0.89; GDP vs income r = +0.90).\n" \
                  "• Validates the fundamental need for PCA dimensionality reduction."
    p_f10c.font.size = Pt(9)
    p_f10c.font.color.rgb = TEXT_MUTED

    add_notes(slide8,
        "In Question 3, we analyze 167 nations evaluated on 9 socio-economic indicators from HELP International. "
        "Because this is unsupervised learning, we have no predefined ground-truth labels. "
        "Standardization is critical: GDP per capita runs up to $105,000, while fertility rate is under 8. "
        "Without z-score standardization, distance-based clustering would simply group countries by raw wealth. "
        "Figure 10 shows our sample covariance heatmap, highlighting strong collinear blocks that PCA resolves.")

    # ==========================================
    # SLIDE 9: Q3 - Clustering: Elbow, Silhouette & Aid Taxonomy
    # ==========================================
    slide9 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide9, LIGHT_BG)
    add_header(slide9, "Question 3 · Unsupervised Learning & PCA", "K-Means: Elbow Method, Silhouette & Aid Taxonomy",
               "Evaluating cluster cohesion and separation to select the optimal partition of 167 nations")
    add_footer(slide9, 9)

    add_card(slide9, 0.8, 1.7, 5.5, 4.9)
    tb_t8_t = slide9.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.1), Inches(0.4))
    tf_t8 = tb_t8_t.text_frame
    p_t8 = tf_t8.paragraphs[0]
    p_t8.text = "Table 8: WCSS & Silhouette Scores (K = 2 to 6)"
    p_t8.font.bold = True
    p_t8.font.size = Pt(11.5)
    p_t8.font.color.rgb = ACCENT_PURPLE

    t8_s = slide9.shapes.add_table(6, 4, Inches(1.0), Inches(2.25), Inches(5.1), Inches(1.9))
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

    tb_tax = slide9.shapes.add_textbox(Inches(1.0), Inches(4.3), Inches(5.1), Inches(2.2))
    tf_tax = tb_tax.text_frame
    tf_tax.word_wrap = True
    p_th = tf_tax.paragraphs[0]
    p_th.text = "Selected K = 3 Taxonomy (Actionable Aid Policy):"
    p_th.font.bold = True
    p_th.font.size = Pt(10.5)
    p_th.font.color.rgb = TEXT_MAIN

    p_tb = tf_tax.add_paragraph()
    p_tb.text = "• Cluster 0 (36 nations - Developed): High GDP ($42.5k), life exp 80.1 yr, child mort 5.0 (Germany, Japan, USA).\n" \
                "• Cluster 1 (47 nations - Underdeveloped / High Priority): Severe poverty, low GDP ($1,909), life exp 56.6 yr, child mort 92.96 (Haiti, Afghanistan, Mali).\n" \
                "• Cluster 2 (84 nations - Developing): Intermediate income ($12.3k), GDP ($6.5k), life exp 73.1 yr (India, Brazil, Indonesia)."
    p_tb.font.size = Pt(8.5)
    p_tb.font.color.rgb = TEXT_MAIN
    p_tb.space_before = Pt(3)

    add_card(slide9, 6.5, 1.7, 6.033, 4.9)
    tb_f9_t = slide9.shapes.add_textbox(Inches(6.7), Inches(1.8), Inches(5.6), Inches(0.4))
    tf_f9 = tb_f9_t.text_frame
    p_f9 = tf_f9.paragraphs[0]
    p_f9.text = "Figure 9: K-Means Elbow Curve & Silhouette Profile"
    p_f9.font.bold = True
    p_f9.font.size = Pt(11.5)
    p_f9.font.color.rgb = TEXT_MAIN

    fig9_path = os.path.abspath("extracted_figures/fig9_kmeans_elbow_silhouette.png")
    if os.path.exists(fig9_path):
        slide9.shapes.add_picture(fig9_path, Inches(6.6), Inches(2.3), width=Inches(5.8))

    tb_f9_c = slide9.shapes.add_textbox(Inches(6.7), Inches(5.35), Inches(5.6), Inches(1.1))
    tf_f9c = tb_f9_c.text_frame
    tf_f9c.word_wrap = True
    p_f9c = tf_f9c.paragraphs[0]
    p_f9c.text = "Why K = 3 is Preferred over Mathematical Peak K = 4:\n" \
                 "• Elbow Criterion: WCSS drops sharply by 20.8% moving to K=3 (down to 831.42), with diminishing returns thereafter.\n" \
                 "• Domain Interpretability: K=4 simply fragments the intermediate developing group into two sub-tiers without offering new strategic insight."
    p_f9c.font.size = Pt(9)
    p_f9c.font.color.rgb = TEXT_MUTED

    add_notes(slide9,
        "Here we examine cluster selection. Table 8 and Figure 9 display our Elbow curve and Silhouette scores across K=2 to 6. "
        "Notice that while K=4 produces the mathematical peak in silhouette score (0.3037), we selected K=3 for international policy alignment. "
        "The WCSS elbow levels off significantly after K=3 with diminishing returns. "
        "Crucially, K=3 partitions the 167 countries into three meaningful tiers: 36 Developed nations, 84 Developing nations, "
        "and 47 Underdeveloped nations that require immediate humanitarian assistance.")

    # ==========================================
    # SLIDE 10: Q3 - PCA: Scree Analysis & 2D/3D Projections
    # ==========================================
    slide10 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide10, LIGHT_BG)
    add_header(slide10, "Question 3 · Unsupervised Learning & PCA", "PCA: Eigendecomposition, Scree & Subspace Projections",
               "Capturing 76.14% cumulative variance across 3 orthogonal axes and validating K-Means cluster harmony")
    add_footer(slide10, 10)

    add_card(slide10, 0.8, 1.7, 5.5, 4.9)
    tb_pca_t = slide10.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.1), Inches(0.35))
    tf_pt = tb_pca_t.text_frame
    p_pt = tf_pt.paragraphs[0]
    p_pt.text = "Table 10: Eigendecomposition & Factor Loadings"
    p_pt.font.bold = True
    p_pt.font.size = Pt(11)
    p_pt.font.color.rgb = ACCENT_PURPLE

    t_pca_s = slide10.shapes.add_table(4, 4, Inches(1.0), Inches(2.2), Inches(5.1), Inches(1.4))
    t_pca = t_pca_s.table
    t_pca.columns[0].width = Inches(1.1)
    t_pca.columns[1].width = Inches(1.2)
    t_pca.columns[2].width = Inches(1.2)
    t_pca.columns[3].width = Inches(1.6)

    t_pca.cell(0, 0).text = "Component"
    t_pca.cell(0, 1).text = "Eigenvalue"
    t_pca.cell(0, 2).text = "Cumul. EVR"
    t_pca.cell(0, 3).text = "Semantic Interpretation"
    for j in range(4):
        c = t_pca.cell(0, j)
        c.fill.solid()
        c.fill.fore_color.rgb = DARK_CARD
        c.text_frame.paragraphs[0].font.bold = True
        c.text_frame.paragraphs[0].font.size = Pt(8)
        c.text_frame.paragraphs[0].font.color.rgb = WHITE
        c.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER

    data_pca = [
        ["PC1", "4.1606", "45.95%", "Development (life_expec vs child_mort)"],
        ["PC2", "1.5557", "63.13%", "Trade Openness (imports & exports)"],
        ["PC3", "1.1774", "76.14%", "Macro Stability (health vs inflation)"]
    ]
    for i, row in enumerate(data_pca):
        for j, val in enumerate(row):
            c = t_pca.cell(i+1, j)
            c.fill.solid()
            c.fill.fore_color.rgb = WHITE
            p = c.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(8)
            p.alignment = PP_ALIGN.CENTER if j < 3 else PP_ALIGN.LEFT

    tb_pca_notes = slide10.shapes.add_textbox(Inches(1.0), Inches(3.8), Inches(5.1), Inches(2.7))
    tf_pn = tb_pca_notes.text_frame
    tf_pn.word_wrap = True
    p_pn1 = tf_pn.paragraphs[0]
    p_pn1.text = "Harmonious Synthesis: K-Means Overlaid on PCA:"
    p_pn1.font.bold = True
    p_pn1.font.size = Pt(10.5)
    p_pn1.font.color.rgb = TEXT_MAIN

    p_pn2 = tf_pn.add_paragraph()
    p_pn2.text = "• 76.14% Variance Truncation: Top 3 principal components retain over 3/4 of total spread while reducing dimensions from 9 to 3.\n" \
                 "• Geometrical Agreement: The 2D (Fig 12) and 3D (Fig 13) projections show clean, non-overlapping cluster boundaries.\n" \
                 "• Spectral Equivalence: Both PCA (variance maximization) and K-Means (WCSS minimization) are continuous and discrete spectral relaxations on the same standardized Euclidean geometry."
    p_pn2.font.size = Pt(8.5)
    p_pn2.font.color.rgb = TEXT_MAIN
    p_pn2.space_before = Pt(3)

    add_card(slide10, 6.5, 1.7, 6.033, 4.9)
    fig11_path = os.path.abspath("extracted_figures/fig11_pca_scree.png")
    fig12_path = os.path.abspath("extracted_figures/fig12_pca_2d.png")

    if os.path.exists(fig11_path):
        slide10.shapes.add_picture(fig11_path, Inches(6.65), Inches(1.85), width=Inches(2.75))
    if os.path.exists(fig12_path):
        slide10.shapes.add_picture(fig12_path, Inches(9.55), Inches(1.85), width=Inches(2.85))

    tb_pfigs_c = slide10.shapes.add_textbox(Inches(6.65), Inches(5.35), Inches(5.7), Inches(1.1))
    tf_pfc = tb_pfigs_c.text_frame
    tf_pfc.word_wrap = True
    p_pfc = tf_pfc.paragraphs[0]
    p_pfc.text = "Left: Figure 11 (PCA Scree plot showing sharp variance elbow after PC3).\n" \
                 "Right: Figure 12 (2D PCA projection colored by K-Means cluster K=3 showing clean partitions)."
    p_pfc.font.size = Pt(9)
    p_pfc.font.color.rgb = TEXT_MUTED

    add_notes(slide10,
        "Slide 10 reveals the semantic meaning of our principal components and connects PCA back to K-Means. "
        "PC1 represents Socio-Economic Development, PC2 captures Trade Openness, and PC3 reflects Macroeconomic Stability. "
        "Together, these 3 orthogonal components preserve 76.14% of the dataset variance. "
        "When we project our 167 nations into PCA subspace and color them by K-Means cluster (Figure 12), "
        "we observe clean, distinct cluster separations with zero boundary overlap, proving mathematical harmony between clustering and PCA.")

    # ==========================================
    # SLIDE 11: Cross-Domain Synthesis & ML Principles
    # ==========================================
    slide11 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide11, LIGHT_BG)
    add_header(slide11, "Conclusions & Synthesis", "Cross-Domain Summary & Fundamental ML Takeaways",
               "Synthesizing optimal models, hyperparameter configurations, and core engineering principles")
    add_footer(slide11, 11)

    add_card(slide11, 0.8, 1.7, 11.733, 2.7)
    tb_t12_t = slide11.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(0.35))
    tf_t12 = tb_t12_t.text_frame
    p_t12 = tf_t12.paragraphs[0]
    p_t12.text = "Table 12: Final Synthesis of Champion Models across All Problems"
    p_t12.font.bold = True
    p_t12.font.size = Pt(11)
    p_t12.font.color.rgb = ACCENT_BLUE

    t12_s = slide11.shapes.add_table(5, 5, Inches(1.0), Inches(2.2), Inches(11.333), Inches(2.0))
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

    takeaways = [
        ("1. Pipeline Integrity", "Encapsulating scalers inside pipelines completely eliminates data leakage across CV folds.", ACCENT_BLUE),
        ("2. Regularization", "Mandatory when scaling feature capacity (Tree pruning, SVM C, Ridge/Lasso alpha, Dropout).", ACCENT_GREEN),
        ("3. Non-Linear Synergy", "Capturing 3,402 atomic interactions outperformed all linear hyperparameter tuning (+16.5% R^2).", ACCENT_AMBER),
        ("4. Statistical Validation", "1,000 bootstrap resamples prevented false superiority claims between SVM and CNN.", ACCENT_PURPLE)
    ]

    for i, (tk_h, tk_b, tk_c) in enumerate(takeaways):
        left_pos = 0.8 + i * 3.0
        c = add_card(slide11, left_pos, 4.6, 2.733, 2.0, WHITE, tk_c)
        tb = slide11.shapes.add_textbox(Inches(left_pos + 0.15), Inches(4.7), Inches(2.433), Inches(1.8))
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

    add_notes(slide11,
        "Slide 11 brings together our entire project findings into Table 12. "
        "Across all three domains, we observe consistent core principles: "
        "Pipeline encapsulation prevents data leakage, regularization controls variance, "
        "physical representation learning delivers superior gains over linear tuning, and bootstrap resampling validates statistical significance.")

    # ==========================================
    # SLIDE 12: Conclusion & Audience Q&A (Dark Theme)
    # ==========================================
    slide12 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide12, DARK_BG)

    bar12 = slide12.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.12))
    bar12.fill.solid()
    bar12.fill.fore_color.rgb = ACCENT_BLUE
    bar12.line.fill.background()

    tbox12 = slide12.shapes.add_textbox(Inches(1.2), Inches(1.3), Inches(11.0), Inches(1.6))
    tf12 = tbox12.text_frame
    tf12.word_wrap = True
    p12 = tf12.paragraphs[0]
    p12.text = "Thank You!"
    p12.font.name = FONT_HEADING
    p12.font.size = Pt(40)
    p12.font.bold = True
    p12.font.color.rgb = WHITE

    p12_sub = tf12.add_paragraph()
    p12_sub.text = "We welcome any questions, discussions, and feedback."
    p12_sub.font.name = FONT_BODY
    p12_sub.font.size = Pt(20)
    p12_sub.font.color.rgb = RGBColor(203, 213, 225)
    p12_sub.space_before = Pt(8)

    highlights = [
        ("Supervised Classification", "SVM (RBF) achieved 92.40% accuracy and 92.22% precision, backed by overlapping bootstrap ROC-AUC with 1D CNN.", ACCENT_BLUE),
        ("Non-Linear Regression", "Full 81-feature Polynomial Ridge achieved R^2 = 0.8542 and reduced RMSE to 12.95 K (+16.5% gain).", ACCENT_GREEN),
        ("Clustering & PCA", "K-Means (K=3) identified actionable humanitarian tiers; PCA captured 76.14% variance across 3 orthogonal axes.", ACCENT_PURPLE)
    ]
    for i, (hl_t, hl_b, hl_c) in enumerate(highlights):
        left_hl = 1.2 + i * 3.8
        c = add_card(slide12, left_hl, 3.4, 3.4, 1.8, DARK_CARD, hl_c)
        tb = slide12.shapes.add_textbox(Inches(left_hl + 0.2), Inches(3.55), Inches(3.0), Inches(1.5))
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

    cbox = slide12.shapes.add_textbox(Inches(1.2), Inches(5.6), Inches(11.0), Inches(1.2))
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

    add_notes(slide12,
        "In conclusion, this project demonstrated practical and theoretical mastery across classification, regression, and unsupervised learning. "
        "We thank our professors and evaluators, and we are now delighted to answer any questions. Thank you!")

    output_pptx = "ML_Course_Project_Presentation.pptx"
    prs.save(output_pptx)
    print(f"Presentation successfully saved to: {output_pptx} (Total Slides: {len(prs.slides)})")

if __name__ == "__main__":
    create_presentation()
