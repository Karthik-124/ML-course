"""
generate_html_presentation.py
Generates an interactive HTML5 presentation deck (presentation.html)
with keyboard controls, fullscreen mode, slide drawer, speaker notes, and embedded high-res figures.
"""

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Machine Learning Course Project Presentation · IIIT Sri City</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-dark: #0f172a;
            --bg-dark-card: #1e293b;
            --bg-light: #f8fafc;
            --bg-card: #ffffff;
            --border-light: #e2e8f0;
            --border-dark: #334155;
            --text-dark: #0f172a;
            --text-muted: #64748b;
            --text-light: #f1f5f9;
            --text-muted-light: #94a3b8;
            --accent-blue: #2563eb;
            --accent-green: #059669;
            --accent-purple: #7c3aed;
            --accent-amber: #d97706;
            --font-main: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
            --font-mono: 'JetBrains Mono', monospace;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: var(--font-main);
            background: #020617;
            color: var(--text-dark);
            height: 100vh;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            user-select: none;
        }

        /* Top Progress Bar */
        .progress-bar-container {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 4px;
            background: rgba(255, 255, 255, 0.1);
            z-index: 100;
        }
        .progress-bar {
            height: 100%;
            width: 0%;
            background: linear-gradient(90deg, #2563eb, #7c3aed, #059669);
            transition: width 0.3s ease;
        }

        /* Deck Viewport */
        .deck-container {
            flex: 1;
            position: relative;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 16px;
        }

        .slide {
            display: none;
            width: 100%;
            max-width: 1400px;
            height: 90vh;
            max-height: 820px;
            background: var(--bg-light);
            border-radius: 16px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5), 0 0 0 1px rgba(255, 255, 255, 0.1);
            position: relative;
            overflow: hidden;
            flex-direction: column;
            padding: 32px 48px 24px 48px;
            animation: fadeIn 0.3s ease-out;
        }

        .slide.active {
            display: flex;
        }

        .slide.dark-theme {
            background: var(--bg-dark);
            color: var(--text-light);
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: scale(0.985); }
            to { opacity: 1; transform: scale(1); }
        }

        /* Slide Header */
        .slide-header {
            margin-bottom: 20px;
            position: relative;
        }
        .breadcrumb-badge {
            display: inline-block;
            font-size: 0.75rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            padding: 4px 10px;
            border-radius: 6px;
            margin-bottom: 8px;
        }
        .badge-blue { background: #dbeafe; color: #1e40af; }
        .badge-green { background: #d1fae5; color: #065f46; }
        .badge-purple { background: #ede9fe; color: #5b21b6; }
        .badge-amber { background: #fef3c7; color: #92400e; }
        .badge-dark { background: #334155; color: #93c5fd; }

        .slide-title {
            font-size: 1.85rem;
            font-weight: 800;
            line-height: 1.2;
            color: var(--text-dark);
        }
        .dark-theme .slide-title {
            color: #ffffff;
        }

        .slide-subtitle {
            font-size: 0.95rem;
            color: var(--text-muted);
            margin-top: 4px;
        }
        .dark-theme .slide-subtitle {
            color: var(--text-muted-light);
        }

        /* Slide Content Area */
        .slide-body {
            flex: 1;
            display: grid;
            grid-gap: 24px;
            overflow: hidden;
        }

        .grid-2col {
            grid-template-columns: 1fr 1fr;
        }
        .grid-2col-wide-right {
            grid-template-columns: 0.9fr 1.1fr;
        }
        .grid-2col-wide-left {
            grid-template-columns: 1.1fr 0.9fr;
        }
        .grid-3col {
            grid-template-columns: repeat(3, 1fr);
        }
        .grid-4col {
            grid-template-columns: repeat(4, 1fr);
        }

        /* UI Cards */
        .card {
            background: var(--bg-card);
            border: 1px solid var(--border-light);
            border-radius: 12px;
            padding: 20px;
            display: flex;
            flex-direction: column;
            overflow: hidden;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        }
        .card-dark {
            background: var(--bg-dark-card);
            border: 1px solid var(--border-dark);
            color: var(--text-light);
        }
        .card-header-bar {
            padding: 8px 12px;
            border-radius: 6px;
            font-weight: 700;
            font-size: 0.85rem;
            text-align: center;
            color: white;
            margin-bottom: 12px;
        }

        .card h3 {
            font-size: 1.05rem;
            font-weight: 700;
            margin-bottom: 8px;
            color: var(--text-dark);
        }
        .card-dark h3 {
            color: #ffffff;
        }

        .card p, .card li {
            font-size: 0.88rem;
            line-height: 1.5;
            color: #334155;
        }
        .card-dark p, .card-dark li {
            color: #cbd5e1;
        }

        .card ul {
            padding-left: 18px;
            margin-top: 6px;
        }
        .card li {
            margin-bottom: 4px;
        }

        /* Images in slide */
        .figure-box {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            background: #ffffff;
            border: 1px solid var(--border-light);
            border-radius: 12px;
            padding: 12px;
            overflow: hidden;
        }
        .figure-box img {
            max-width: 100%;
            max-height: 380px;
            object-fit: contain;
            border-radius: 6px;
        }
        .figure-caption {
            font-size: 0.78rem;
            color: var(--text-muted);
            margin-top: 8px;
            text-align: center;
            line-height: 1.35;
        }

        /* Tables */
        .styled-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.82rem;
            margin-top: 8px;
        }
        .styled-table th {
            background: #1e293b;
            color: #ffffff;
            padding: 8px 10px;
            text-align: center;
            font-weight: 600;
        }
        .styled-table td {
            padding: 7px 10px;
            border-bottom: 1px solid #e2e8f0;
            text-align: center;
            color: #1e293b;
        }
        .styled-table tr:hover {
            background: #f1f5f9;
        }
        .styled-table .highlight-row {
            background: #eff6ff;
            font-weight: 700;
            color: #1d4ed8;
        }
        .styled-table .highlight-green {
            background: #ecfdf5;
            font-weight: 700;
            color: #047857;
        }

        /* Callout Box */
        .callout {
            border-left: 4px solid var(--accent-blue);
            background: #eff6ff;
            padding: 10px 14px;
            border-radius: 0 8px 8px 0;
            margin-top: 10px;
        }
        .callout-amber {
            border-left-color: var(--accent-amber);
            background: #fffbeb;
        }
        .callout-green {
            border-left-color: var(--accent-green);
            background: #ecfdf5;
        }
        .callout-purple {
            border-left-color: var(--accent-purple);
            background: #f5f3ff;
        }
        .callout h4 {
            font-size: 0.88rem;
            font-weight: 700;
            margin-bottom: 3px;
        }
        .callout p {
            font-size: 0.82rem;
            line-height: 1.4;
            color: #334155;
        }

        /* Slide Footer */
        .slide-footer {
            margin-top: 16px;
            padding-top: 12px;
            border-top: 1px solid var(--border-light);
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.78rem;
            color: var(--text-muted);
        }
        .dark-theme .slide-footer {
            border-top-color: var(--border-dark);
            color: var(--text-muted-light);
        }

        /* Floating Controls */
        .controls {
            position: fixed;
            bottom: 16px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            align-items: center;
            gap: 12px;
            background: rgba(15, 23, 42, 0.85);
            backdrop-filter: blur(12px);
            padding: 8px 20px;
            border-radius: 9999px;
            border: 1px solid rgba(255, 255, 255, 0.15);
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
            z-index: 1000;
        }
        .btn-ctrl {
            background: transparent;
            border: none;
            color: #ffffff;
            cursor: pointer;
            padding: 6px 12px;
            border-radius: 6px;
            font-size: 0.85rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 6px;
            transition: all 0.2s;
        }
        .btn-ctrl:hover {
            background: rgba(255, 255, 255, 0.15);
        }
        .slide-indicator {
            color: #94a3b8;
            font-size: 0.85rem;
            font-family: var(--font-mono);
            min-width: 60px;
            text-align: center;
        }

        /* Speaker Notes Panel */
        .notes-panel {
            position: fixed;
            right: 0;
            top: 0;
            width: 380px;
            height: 100vh;
            background: #0f172a;
            border-left: 1px solid #334155;
            color: #e2e8f0;
            padding: 24px;
            overflow-y: auto;
            transform: translateX(100%);
            transition: transform 0.3s ease;
            z-index: 999;
            box-shadow: -10px 0 30px rgba(0, 0, 0, 0.5);
        }
        .notes-panel.open {
            transform: translateX(0);
        }
        .notes-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-bottom: 12px;
            border-bottom: 1px solid #334155;
            margin-bottom: 16px;
        }
        .notes-header h3 {
            font-size: 1rem;
            font-weight: 700;
            color: #93c5fd;
        }
        .notes-content {
            font-size: 0.9rem;
            line-height: 1.6;
            color: #cbd5e1;
        }

        /* Thumbnail Grid Drawer */
        .overview-modal {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(15, 23, 42, 0.95);
            backdrop-filter: blur(16px);
            z-index: 2000;
            display: none;
            padding: 40px;
            overflow-y: auto;
        }
        .overview-modal.open {
            display: block;
        }
        .overview-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
            gap: 20px;
            max-width: 1400px;
            margin: 0 auto;
        }
        .overview-card {
            background: #1e293b;
            border: 1px solid #334155;
            border-radius: 10px;
            padding: 16px;
            cursor: pointer;
            transition: all 0.2s;
            color: #f1f5f9;
        }
        .overview-card:hover {
            border-color: #3b82f6;
            transform: translateY(-4px);
        }
        .overview-card.active-card {
            border-color: #3b82f6;
            background: #1e3a8a;
        }
        .overview-card h4 {
            font-size: 0.9rem;
            margin-bottom: 6px;
        }
        .overview-card p {
            font-size: 0.75rem;
            color: #94a3b8;
        }
    </style>
</head>
<body>

    <div class="progress-bar-container">
        <div class="progress-bar" id="progressBar"></div>
    </div>

    <div class="deck-container">

        <!-- SLIDE 1: Title Slide -->
        <section class="slide dark-theme active" data-notes="Good morning/afternoon everyone. Today, Karthik and I are presenting our Machine Learning Course Project. Our work investigates three core paradigms of machine learning: supervised classification on UCI Spambase, non-linear regularized regression on superconducting critical temperatures, and unsupervised clustering with PCA on international socio-economic development data. We will walk through our mathematical foundations, pipeline designs, overfitting diagnostics, and key engineering takeaways.">
            <div style="height: 4px; background: #2563eb; width: 100%; border-radius: 2px; margin-bottom: 24px;"></div>
            <div class="breadcrumb-badge badge-dark">CSE DEPT · MACHINE LEARNING</div>
            <h1 class="slide-title" style="font-size: 2.5rem; margin-top: 8px;">Machine Learning Course Project</h1>
            <p class="slide-subtitle" style="font-size: 1.25rem; color: #94a3b8; margin-top: 8px;">
                Supervised Classification, Non-Linear Regularized Regression, and Unsupervised Clustering & Dimensionality Reduction
            </p>

            <div class="slide-body grid-3col" style="margin-top: 36px; max-height: 220px;">
                <div class="card card-dark" style="border-top: 3px solid #2563eb;">
                    <div style="font-size: 0.75rem; font-weight: 700; color: #60a5fa; text-transform: uppercase;">Question 1 · Classification</div>
                    <h3 style="margin-top: 6px;">UCI Spambase</h3>
                    <p>KNN, Decision Tree, SVM (RBF), and Deep 1D CNN evaluated on 4,601 emails.</p>
                </div>
                <div class="card card-dark" style="border-top: 3px solid #059669;">
                    <div style="font-size: 0.75rem; font-weight: 700; color: #34d399; text-transform: uppercase;">Question 2 · Regression</div>
                    <h3 style="margin-top: 6px;">Superconductivity Tc</h3>
                    <p>SGD Linear, Ridge, Lasso, and Polynomial Regression on 21,263 superconductor samples.</p>
                </div>
                <div class="card card-dark" style="border-top: 3px solid #7c3aed;">
                    <div style="font-size: 0.75rem; font-weight: 700; color: #c084fc; text-transform: uppercase;">Question 3 · Unsupervised</div>
                    <h3 style="margin-top: 6px;">HELP International</h3>
                    <p>K-Means Clustering and First-Principles Covariance PCA across 167 nations.</p>
                </div>
            </div>

            <div style="margin-top: 40px;">
                <p style="font-weight: 700; font-size: 1.05rem; color: #ffffff;">Submitted By: Yashasvee Patel (S20240010266) & P Karthik (S20240010184)</p>
                <p style="font-size: 0.9rem; color: #94a3b8; margin-top: 4px;">Department of Computer Science & Engineering · Indian Institute of Information Technology, Sri City · Nov 4, 2026</p>
            </div>
            <div class="slide-footer">
                <span>IIIT Sri City · Machine Learning</span>
                <span>Slide 1 of 16</span>
            </div>
        </section>

        <!-- SLIDE 2: Project Architecture & Methodology -->
        <section class="slide" data-notes="Here is the high-level roadmap of our presentation. We tackle three diverse problems covering the machine learning spectrum. A foundational principle across all our experiments is scientific reproducibility and zero data leakage. In many student projects, StandardScaler is mistakenly applied to the full dataset before splitting, which artificially inflates validation accuracy. In our implementation, all feature transformations are encapsulated inside scikit-learn Pipelines, ensuring the test set remains completely unseen.">
            <div class="slide-header">
                <span class="breadcrumb-badge badge-blue">Executive Overview</span>
                <h2 class="slide-title">Project Architecture & Experimental Rigor</h2>
                <p class="slide-subtitle">Three machine learning challenges unified by strict scientific validation and zero data leakage</p>
            </div>
            <div class="slide-body grid-3col">
                <div class="card">
                    <div class="card-header-bar" style="background: #2563eb;">Domain 1: Classification</div>
                    <h3>UCI Spambase Dataset</h3>
                    <ul>
                        <li><strong>Goal:</strong> Binary spam vs ham classification (4,601 emails, 57 continuous features)</li>
                        <li><strong>Models:</strong> KNN (k=3), CART Decision Tree (d=12), SVM (RBF, C=5.0), Deep 1D CNN</li>
                        <li><strong>Validation:</strong> 5-Fold Stratified CV, confusion matrices, and 1,000 bootstrap ROC-AUC CIs</li>
                    </ul>
                </div>
                <div class="card">
                    <div class="card-header-bar" style="background: #059669;">Domain 2: Regression</div>
                    <h3>Superconductivity Tc</h3>
                    <ul>
                        <li><strong>Goal:</strong> Predict critical temperature Tc in Kelvin (21,263 samples, 81 features)</li>
                        <li><strong>Models:</strong> SGD Linear, Ridge (L2), Lasso (L1), Degree-2 Polynomial Expansion</li>
                        <li><strong>Validation:</strong> Degree sweep (1 to 4) under/overfitting analysis, 5-fold CV alpha grids</li>
                    </ul>
                </div>
                <div class="card">
                    <div class="card-header-bar" style="background: #7c3aed;">Domain 3: Clustering & PCA</div>
                    <h3>HELP Socio-Economic Data</h3>
                    <ul>
                        <li><strong>Goal:</strong> Unsupervised country clustering for aid allocation & dimensionality reduction</li>
                        <li><strong>Models:</strong> K-Means (Lloyd's), PCA via sample covariance matrix eigendecomposition</li>
                        <li><strong>Validation:</strong> Elbow WCSS drop, Silhouette analysis, 76.14% variance in 2D/3D</li>
                    </ul>
                </div>
            </div>
            <div class="callout callout-blue" style="margin-top: 14px;">
                <h4>Strict Scientific Protocol & Zero Data Leakage Guarantee:</h4>
                <p>1. Fixed 80/20 train/test split. 2. All scalers (StandardScaler) placed strictly inside scikit-learn Pipelines so test distributions never contaminate training folds. 3. Hyperparameter selection performed solely on training folds.</p>
            </div>
            <div class="slide-footer">
                <span>IIIT Sri City · Machine Learning</span>
                <span>Slide 2 of 16</span>
            </div>
        </section>

        <!-- SLIDE 3: Q1 - Classification Setup & Spambase -->
        <section class="slide" data-notes="Turning to Question 1, our task is classifying 4,601 emails from the UCI Spambase dataset. The feature space consists of 57 continuous variables. Notice that the class distribution is roughly 40% spam and 60% ham. Importantly, spam filtering has asymmetric misclassification costs. A false positive—marking a crucial email as spam—is unacceptable. On the right, Figure 1 illustrates our 5-fold cross-validation sweeps on the training data. For KNN, k=3 provided optimal balance between noise sensitivity and oversmoothing. For Decision Trees, depth 12 achieved peak cross-validation accuracy before pruning begins.">
            <div class="slide-header">
                <span class="breadcrumb-badge badge-blue">Question 1 · Supervised Classification</span>
                <h2 class="slide-title">UCI Spambase Dataset & Problem Formulation</h2>
                <p class="slide-subtitle">Binary spam detection on 4,601 emails using 57 continuous lexical and punctuation features</p>
            </div>
            <div class="slide-body grid-2col-wide-right">
                <div class="card">
                    <h3>Dataset Characteristics</h3>
                    <ul>
                        <li><strong>Scale:</strong> 4,601 Email records split into 80% Train (3,680) and 20% Test (921).</li>
                        <li><strong>Class Balance:</strong> 1,813 Spam (39.4%) vs. 2,788 Legitimate Ham (60.6%).</li>
                        <li><strong>57 Continuous Features:</strong>
                            <ul style="margin-top: 4px;">
                                <li>48 Word Frequencies (% of 'free', 'money', 'credit')</li>
                                <li>6 Character Frequencies (% of '!', '$', '#', etc.)</li>
                                <li>3 Capital Run-Length Statistics (average, max, total)</li>
                            </ul>
                        </li>
                    </ul>
                    <div class="callout callout-amber" style="margin-top: 14px;">
                        <h4>The Asymmetric Cost of Spam Detection:</h4>
                        <p>False Positives (flagging an important college email as spam) are far more harmful than False Negatives. Thus, Precision and ROC-AUC are prioritized alongside pure Accuracy.</p>
                    </div>
                </div>
                <div class="figure-box">
                    <img src="extracted_figures/fig1_classification_cv.png" alt="Figure 1: CV Curves for KNN and Decision Tree">
                    <p class="figure-caption">
                        <strong>Figure 1: 5-Fold Cross-Validation Hyperparameter Sweeps</strong><br>
                        Left (KNN): Swept k in [1..21]. Optimal k = 3 yields peak 5-fold CV accuracy (90.76%).<br>
                        Right (Decision Tree): Swept max_depth in [2..25]. Optimal depth = 12 reaches peak CV accuracy (91.85%).
                    </p>
                </div>
            </div>
            <div class="slide-footer">
                <span>IIIT Sri City · Machine Learning</span>
                <span>Slide 3 of 16</span>
            </div>
        </section>

        <!-- SLIDE 4: Q1 - Classification Suite -->
        <section class="slide" data-notes="Here we summarize our four classifier architectures. Notice the diversity of inductive biases: KNN is instance-based, Decision Trees create orthogonal decision boundaries, SVM projects data into an infinite-dimensional feature space, and our bonus 1D CNN treats the 57 features as a 1D sequence to capture local interaction patterns. Figure 2 shows the cross-validation curve for SVM across the regularization parameter C. Notice the plateau between C=1 and C=10, with C=5.0 hitting our peak CV accuracy of 93.15%.">
            <div class="slide-header">
                <span class="breadcrumb-badge badge-blue">Question 1 · Supervised Classification</span>
                <h2 class="slide-title">Model Suite: Algorithms & Hyperparameter Tuning</h2>
                <p class="slide-subtitle">Evaluating instance-based, tree-based, maximum-margin, and deep convolutional paradigms</p>
            </div>
            <div class="slide-body grid-2col">
                <div class="card">
                    <h3>Evaluated Architectures</h3>
                    <ul>
                        <li><strong>1. K-Nearest Neighbour (KNN):</strong> Instance-based Euclidean metric. Optimal k=3 chosen via 5-fold CV (90.76% CV accuracy). Mandates z-score normalization inside pipeline.</li>
                        <li><strong>2. Decision Tree (CART):</strong> Axis-aligned recursive partitioning minimizing Gini impurity: Gini = 1 - sum(p_c^2). Max depth = 12 chosen via CV (91.85% CV accuracy).</li>
                        <li><strong>3. SVM (RBF Kernel):</strong> Soft-margin hyperplane in infinite-dimensional RKHS with RBF kernel exp(-gamma*||x-x'||^2). Optimal C = 5.0 (93.15% CV accuracy).</li>
                        <li><strong>4. Deep 1D CNN (Bonus PyTorch):</strong> 3 Conv1d blocks (32->64->128 filters), BatchNorm, Dropout (0.3), Global Average Pooling, Adam lr=1e-3.</li>
                    </ul>
                </div>
                <div class="figure-box">
                    <img src="extracted_figures/fig2_svm_cv.png" alt="Figure 2: SVM CV Curve">
                    <p class="figure-caption">
                        <strong>Figure 2: 5-Fold Cross-Validation Curve for SVM (RBF) across C</strong><br>
                        Regularization parameter C swept across [0.1, 100]. C = 5.0 achieved global maximum CV accuracy (93.15%). Below C=1 the model underfits; above C=10 variance increases.
                    </p>
                </div>
            </div>
            <div class="slide-footer">
                <span>IIIT Sri City · Machine Learning</span>
                <span>Slide 4 of 16</span>
            </div>
        </section>

        <!-- SLIDE 5: Q1 - Confusion Matrices & Metrics -->
        <section class="slide" data-notes="Here are the core classification test results on the 921 test emails. Looking at Table 4, SVM with RBF kernel achieves the highest overall accuracy at 92.40% and top F1-score of 0.9014. Most importantly, looking at the confusion matrices on the right (Figure 3), SVM generated only 27 False Positives, giving it the highest precision of 92.22%. In spam detection, high precision is essential. Meanwhile, our Deep CNN achieved the highest recall at 89.26%, catching the largest fraction of spam.">
            <div class="slide-header">
                <span class="breadcrumb-badge badge-blue">Question 1 · Supervised Classification</span>
                <h2 class="slide-title">Model Performance & Confusion Matrix Analysis</h2>
                <p class="slide-subtitle">Quantitative evaluation on 921 test emails across 5 evaluation metrics and error distributions</p>
            </div>
            <div class="slide-body grid-2col-wide-left">
                <div>
                    <div class="card" style="margin-bottom: 12px;">
                        <h3>Table 4: Test Performance Metrics (N = 921 Emails)</h3>
                        <table class="styled-table">
                            <thead>
                                <tr>
                                    <th>Classifier</th>
                                    <th>Accuracy</th>
                                    <th>Precision</th>
                                    <th>Recall</th>
                                    <th>F1-Score</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>KNN (k=3)</td>
                                    <td>89.79%</td>
                                    <td>87.26%</td>
                                    <td>86.78%</td>
                                    <td>0.8702</td>
                                </tr>
                                <tr>
                                    <td>Decision Tree (d=12)</td>
                                    <td>91.97%</td>
                                    <td>90.70%</td>
                                    <td>88.71%</td>
                                    <td>0.8969</td>
                                </tr>
                                <tr class="highlight-row">
                                    <td>SVM (RBF, C=5.0)</td>
                                    <td>92.40%</td>
                                    <td>92.22%</td>
                                    <td>88.15%</td>
                                    <td>0.9014</td>
                                </tr>
                                <tr>
                                    <td>Deep 1D CNN</td>
                                    <td>91.53%</td>
                                    <td>89.26%</td>
                                    <td>89.26%</td>
                                    <td>0.8926</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                    <div class="callout callout-blue">
                        <h4>Key Confusion Matrix Insights:</h4>
                        <p>• <strong>SVM achieves Highest Precision (92.22%):</strong> Only 27 False Positives out of 558 legitimate emails. Minimizes the risk of critical communications landing in spam.<br>
                        • <strong>Deep 1D CNN achieves Highest Recall (89.26%):</strong> Catches the most spam (misses only 39 out of 363 spam emails).<br>
                        • <strong>Decision Tree:</strong> Highly competitive 91.97% accuracy via orthogonal lexical thresholds.</p>
                    </div>
                </div>
                <div class="figure-box">
                    <img src="extracted_figures/fig3_confusion_matrices.png" alt="Figure 3: Confusion Matrices">
                    <p class="figure-caption">
                        <strong>Figure 3: Confusion Matrices for All 4 Classifiers (921 Test Emails)</strong><br>
                        Comparing True Negatives, False Positives (FP), False Negatives (FN), and True Positives (TP). Notice SVM has the fewest false alarms (FP = 27).
                    </p>
                </div>
            </div>
            <div class="slide-footer">
                <span>IIIT Sri City · Machine Learning</span>
                <span>Slide 5 of 16</span>
            </div>
        </section>

        <!-- SLIDE 6: Q1 - Overfitting & ROC-AUC -->
        <section class="slide" data-notes="Slide 6 provides critical scientific validation. On the left, Figure 4 demonstrates the classic bias-variance tradeoff across all four models. At k=1 for KNN or depth=25 for Decision Trees, training accuracy approaches 100%, but test accuracy drops as the models memorize noise. On the right, Figure 5 shows our ROC curves. Rather than relying on a single point estimate, we ran 1,000 bootstrap resamples to compute 95% confidence intervals. Notice that the intervals for SVM [0.959, 0.979] and Deep CNN [0.961, 0.981] overlap heavily. This proves they are in a statistical tie, justifying our selection of SVM based on its higher precision, lower latency, and simplicity.">
            <div class="slide-header">
                <span class="breadcrumb-badge badge-blue">Question 1 · Supervised Classification</span>
                <h2 class="slide-title">Model Complexity, Overfitting & ROC-AUC Analysis</h2>
                <p class="slide-subtitle">Evaluating bias-variance tradeoffs and 1,000 bootstrap resamples on ranking discrimination</p>
            </div>
            <div class="slide-body grid-2col">
                <div class="figure-box">
                    <img src="extracted_figures/fig4_complexity_overfitting.png" alt="Figure 4: Complexity & Overfitting Dynamics">
                    <p class="figure-caption">
                        <strong>Figure 4: Complexity Dynamics Across All Models</strong><br>
                        • KNN: k=1 reaches 100% train accuracy but fails on test data due to noise sensitivity.<br>
                        • Decision Tree: Depth > 15 memorizes training noise without test gains.<br>
                        • CNN: Dropout (0.3) prevents val loss divergence across 40 epochs.
                    </p>
                </div>
                <div class="figure-box">
                    <img src="extracted_figures/fig5_roc_curves.png" alt="Figure 5: ROC Curves">
                    <p class="figure-caption">
                        <strong>Figure 5: ROC Curves with 1,000 Bootstrap 95% CIs</strong><br>
                        • Deep 1D CNN: 0.9718 [95% CI: 0.961 – 0.981]<br>
                        • SVM (RBF): 0.9697 [95% CI: 0.959 – 0.979] (Statistical Tie with CNN)<br>
                        • KNN: 0.9360 [0.919 – 0.951] | Decision Tree: 0.9023 [0.876 – 0.925]<br>
                        <strong>Selection:</strong> SVM selected for highest precision, top F1, and deterministic reproducibility.
                    </p>
                </div>
            </div>
            <div class="slide-footer">
                <span>IIIT Sri City · Machine Learning</span>
                <span>Slide 6 of 16</span>
            </div>
        </section>

        <!-- SLIDE 7: Q2 - Regression Setup -->
        <section class="slide" data-notes="Moving to Question 2, we tackle a regression problem: predicting the critical temperature Tc of 21,263 superconductors. Tc is the temperature below which electrical resistance drops to zero. The dataset extracts 81 continuous features from 8 atomic properties. From a machine learning perspective, this presents two big challenges: severe multicollinearity among atomic statistics, and non-linear quantum physics where Tc is driven by multiplicative interactions rather than additive linear effects.">
            <div class="slide-header">
                <span class="breadcrumb-badge badge-green">Question 2 · Non-Linear Regression & Regularization</span>
                <h2 class="slide-title">Superconductivity Critical Temperature (Tc) Prediction</h2>
                <p class="slide-subtitle">Predicting critical transition temperature from 81 elemental and chemical features across 21,263 superconductors</p>
            </div>
            <div class="slide-body grid-3col" style="max-height: 140px; margin-bottom: 16px;">
                <div class="card" style="border-left: 4px solid #059669;">
                    <div style="font-size: 0.75rem; font-weight: 700; color: #059669; text-transform: uppercase;">Dataset Scale</div>
                    <div style="font-size: 1.25rem; font-weight: 800; color: #0f172a; margin-top: 4px;">21,263 Superconductors</div>
                    <p style="font-size: 0.8rem; color: #64748b;">80% Train (17,010) / 20% Test (4,253)</p>
                </div>
                <div class="card" style="border-left: 4px solid #2563eb;">
                    <div style="font-size: 0.75rem; font-weight: 700; color: #2563eb; text-transform: uppercase;">Input Features</div>
                    <div style="font-size: 1.25rem; font-weight: 800; color: #0f172a; margin-top: 4px;">81 Continuous Features</div>
                    <p style="font-size: 0.8rem; color: #64748b;">Derived from 8 fundamental atomic properties</p>
                </div>
                <div class="card" style="border-left: 4px solid #d97706;">
                    <div style="font-size: 0.75rem; font-weight: 700; color: #d97706; text-transform: uppercase;">Target Variable Tc</div>
                    <div style="font-size: 1.25rem; font-weight: 800; color: #0f172a; margin-top: 4px;">Range: 0.00021 K to 185 K</div>
                    <p style="font-size: 0.8rem; color: #64748b;">Mean: 34.42 K · Heavily skewed distribution</p>
                </div>
            </div>
            <div class="slide-body grid-2col">
                <div class="card">
                    <h3>Elemental Feature Generation (8 Atomic Properties)</h3>
                    <p>Features are 8 statistical aggregates (mean, weighted mean, geometric mean, weighted geometric mean, min, max, range, std) computed over:</p>
                    <ul style="margin-top: 6px;">
                        <li>1. Atomic Mass · 2. First Ionization Energy</li>
                        <li>3. Atomic Radius · 4. Density</li>
                        <li>5. Electron Affinity · 6. Heat of Fusion</li>
                        <li>7. Thermal Conductivity · 8. Valence Electrons</li>
                    </ul>
                </div>
                <div class="card">
                    <h3>The Machine Learning Challenge</h3>
                    <ul>
                        <li><strong>High Multicollinearity:</strong> Correlated aggregate statistics (|r| > 0.85) cause ill-conditioned matrix inversion in standard OLS.</li>
                        <li><strong>Non-Linear Quantum Mechanics:</strong> BCS superconductivity theory states Tc depends exponentially on electron-phonon coupling and density of states.</li>
                        <li><strong>Linear Hypothesis Failure:</strong> Plain linear models cannot capture multiplicative synergies between valence, atomic radius, and conductivity.</li>
                    </ul>
                </div>
            </div>
            <div class="slide-footer">
                <span>IIIT Sri City · Machine Learning</span>
                <span>Slide 7 of 16</span>
            </div>
        </section>

        <!-- SLIDE 8: Q2 - Linear SGD, Ridge & Lasso -->
        <section class="slide" data-notes="To test linear modeling on this dataset, we implemented Linear SGD, Ridge, and Lasso. As seen in Figure 6, we ran 5-fold cross-validation across alpha grids. Ridge with alpha=0.1 and Lasso with alpha=1e-5 both reached an R^2 of 0.7375 and RMSE of 17.38 Kelvin. However, notice the fundamental limitation: all linear models hit a performance ceiling at R^2 ~ 0.738. Regularization successfully stabilizes collinearity, but it cannot overcome the high bias of assuming a linear physical relationship.">
            <div class="slide-header">
                <span class="breadcrumb-badge badge-green">Question 2 · Non-Linear Regression & Regularization</span>
                <h2 class="slide-title">Linear SGD, Ridge (L2) & Lasso (L1) Regularization</h2>
                <p class="slide-subtitle">Evaluating linear baselines and regularized shrinkage across all 81 elemental features</p>
            </div>
            <div class="slide-body grid-2col-wide-left">
                <div class="card">
                    <h3>Formulations & Empirical Findings</h3>
                    <ul>
                        <li><strong>Linear Regression via SGD:</strong> Minimizes standard MSE without penalty. Iterative SGD converges to R^2 = 0.7332 and RMSE = 17.52 K.</li>
                        <li><strong>Ridge Regression (L2 Penalty):</strong>
                            <div style="font-family: var(--font-mono); font-size: 0.8rem; background: #f1f5f9; padding: 4px 8px; border-radius: 4px; margin: 4px 0;">
                                J(w) = sum(y_i - w^T x_i)^2 + alpha * ||w||_2^2
                            </div>
                            Shrinks collinear weights proportionally, mitigating ill-conditioned inversion. Optimal alpha = 0.1 yields R^2 = 0.7375 (RMSE = 17.38 K).
                        </li>
                        <li><strong>Lasso Regression (L1 Penalty):</strong>
                            <div style="font-family: var(--font-mono); font-size: 0.8rem; background: #f1f5f9; padding: 4px 8px; border-radius: 4px; margin: 4px 0;">
                                J(w) = sum(y_i - w^T x_i)^2 + alpha * ||w||_1
                            </div>
                            Enforces sparsity. Optimal alpha = 1e-5 yields R^2 = 0.7375.
                        </li>
                    </ul>
                    <div class="callout callout-amber" style="margin-top: 10px;">
                        <h4>The Linear Ceiling:</h4>
                        <p>All linear models hit a hard ceiling at R^2 ≈ 0.738. Regularization prevents blowup but cannot break past high linear bias.</p>
                    </div>
                </div>
                <div class="figure-box">
                    <img src="extracted_figures/fig6_ridge_lasso_cv.png" alt="Figure 6: Ridge & Lasso CV">
                    <p class="figure-caption">
                        <strong>Figure 6: 5-Fold Cross-Validation for Ridge & Lasso across Alpha</strong><br>
                        Left (Ridge): Stable performance for alpha < 10. Beyond alpha=100, heavy L2 penalty causes excessive shrinkage and underfitting.<br>
                        Right (Lasso): Above alpha=1e-3, sparsity aggressively zeroes out useful predictors, causing CV R^2 to drop sharply.
                    </p>
                </div>
            </div>
            <div class="slide-footer">
                <span>IIIT Sri City · Machine Learning</span>
                <span>Slide 8 of 16</span>
            </div>
        </section>

        <!-- SLIDE 9: Q2 - Polynomial Sweep & Overfitting -->
        <section class="slide" data-notes="To introduce non-linearity, we first selected the top 15 features by Pearson correlation and conducted a degree sweep from d=1 to d=4. Figure 7 demonstrates the textbook transition from underfitting to overfitting. At degree 1, we suffer from high bias. At degree 2, performance remains stable with 135 terms. At degree 3, we expand to 815 terms and training error pulls away from test error. Finally, at degree 4 with 3,875 terms, test error explodes completely. This proves that high-degree polynomial expansions without regularization suffer from severe variance and numerical instability.">
            <div class="slide-header">
                <span class="breadcrumb-badge badge-green">Question 2 · Non-Linear Regression & Regularization</span>
                <h2 class="slide-title">Polynomial Expansion: Feature Selection & Degree Sweep</h2>
                <p class="slide-subtitle">Analyzing model capacity and generalization error from high bias (d=1) to catastrophic variance (d=4)</p>
            </div>
            <div class="slide-body grid-2col-wide-right">
                <div>
                    <div class="card" style="margin-bottom: 12px;">
                        <h3>Top Features by Pearson Correlation (|r|)</h3>
                        <table class="styled-table">
                            <thead>
                                <tr>
                                    <th>Selected Feature</th>
                                    <th>Pearson Correlation (r)</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr><td>range_ThermalConductivity</td><td>-0.6873</td></tr>
                                <tr><td>w_mean_Valence</td><td>-0.6324</td></tr>
                                <tr><td>std_AtomicRadius</td><td>+0.6133</td></tr>
                                <tr><td>range_AtomicRadius</td><td>+0.6133</td></tr>
                                <tr><td>w_mean_ThermalConductivity</td><td>-0.6121</td></tr>
                            </tbody>
                        </table>
                    </div>
                    <div class="callout callout-green">
                        <h4>Degree Sweep on Top 15 Features:</h4>
                        <p>• <strong>Degree 1 (15 terms):</strong> High Bias (R^2 = 0.735)<br>
                        • <strong>Degree 2 (135 terms):</strong> Balanced baseline (R^2 = 0.735)<br>
                        • <strong>Degree 3 (815 terms):</strong> Overfitting begins (train R^2 = 0.81, test R^2 drops)<br>
                        • <strong>Degree 4 (3,875 terms):</strong> Catastrophic variance explosion! Test MSE diverges due to ill-conditioned Vandermonde matrix.</p>
                    </div>
                </div>
                <div class="figure-box">
                    <img src="extracted_figures/fig7_polynomial_sweep.png" alt="Figure 7: Polynomial Degree Sweep">
                    <p class="figure-caption">
                        <strong>Figure 7: Polynomial Degree Sweep (Degrees 1 to 4)</strong><br>
                        At d=1, train and test errors are identical but high (Underfitting). At d=4, train R^2 reaches 0.88, but unregularized test error diverges catastrophically (High Variance).
                    </p>
                </div>
            </div>
            <div class="slide-footer">
                <span>IIIT Sri City · Machine Learning</span>
                <span>Slide 9 of 16</span>
            </div>
        </section>

        <!-- SLIDE 10: Q2 - Breakthrough Poly Ridge -->
        <section class="slide" data-notes="Slide 10 highlights the major engineering breakthrough in our regression task. When we expanded all 81 elemental features to degree-2, we created 3,402 pairwise interaction terms. By applying Ridge regularization with alpha=10.0, we prevented overfitting on this massive feature space. As seen in Table 6 and Figure 8, our Test R^2 surged from 0.7332 to 0.8542, and our RMSE dropped from 17.52 Kelvin down to 12.95 Kelvin. This proves that capturing non-linear physical interactions between atomic properties—like thermal conductivity times valence—is far more impactful than any hyperparameter tuning of linear models.">
            <div class="slide-header">
                <span class="breadcrumb-badge badge-green">Question 2 · Non-Linear Regression & Regularization</span>
                <h2 class="slide-title">The Breakthrough: Full 81-Feature Polynomial Ridge</h2>
                <p class="slide-subtitle">Capturing 3,402 cross-feature atomic interactions achieves R^2 = 0.8542 and reduces RMSE to 12.95 K</p>
            </div>
            <div class="slide-body grid-2col-wide-left">
                <div>
                    <div class="card" style="margin-bottom: 12px;">
                        <h3>Table 6: Complete Regression Model Comparison</h3>
                        <table class="styled-table">
                            <thead>
                                <tr>
                                    <th>Regression Model</th>
                                    <th>Test MSE</th>
                                    <th>Test RMSE</th>
                                    <th>Test R^2</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr><td>Linear Regression (SGD)</td><td>307.09</td><td>17.52 K</td><td>0.7332</td></tr>
                                <tr><td>Ridge Regression (a=0.1)</td><td>302.15</td><td>17.38 K</td><td>0.7375</td></tr>
                                <tr><td>Lasso Regression (a=1e-5)</td><td>302.20</td><td>17.38 K</td><td>0.7375</td></tr>
                                <tr><td>Poly Ridge (Top 15, d=2)</td><td>305.24</td><td>17.47 K</td><td>0.7348</td></tr>
                                <tr class="highlight-green"><td>Poly Ridge (All 81, d=2)</td><td>167.79</td><td>12.95 K</td><td>0.8542</td></tr>
                            </tbody>
                        </table>
                    </div>
                    <div class="callout callout-green">
                        <h4>Key Scientific Breakthrough:</h4>
                        <p>Expanding all 81 features to degree-2 generates 3,402 pairwise interaction terms. Regularized by Ridge (alpha = 10.0), Test R^2 surged from 0.7332 to <strong>0.8542 (+16.5% relative gain)</strong> and RMSE plunged from 17.52 K to <strong>12.95 K (-26.1% error reduction)</strong>.<br>
                        <em>Takeaway:</em> Physical representation learning (atomic interactions) yields vastly greater returns than optimizing linear algorithms.</p>
                    </div>
                </div>
                <div class="figure-box">
                    <img src="extracted_figures/fig8_regression_comparison.png" alt="Figure 8: Bar Chart Comparison">
                    <p class="figure-caption">
                        <strong>Figure 8: Test Set Performance Comparison</strong><br>
                        Left: Full 81-feature Polynomial Ridge achieves massive R^2 lead (0.8542 vs ~0.737).<br>
                        Right: RMSE drops from ~17.4 K down to 12.95 K, cutting prediction error by > 4.5 Kelvin.
                    </p>
                </div>
            </div>
            <div class="slide-footer">
                <span>IIIT Sri City · Machine Learning</span>
                <span>Slide 10 of 16</span>
            </div>
        </section>

        <!-- SLIDE 11: Q3 - Unsupervised Setup -->
        <section class="slide" data-notes="Turning to Question 3, we analyze 167 nations evaluated on 9 socio-economic indicators from HELP International. The practical objective is determining which countries need urgent international aid. Because this is unsupervised learning, we have no predefined ground-truth labels. Notice the extreme difference in scales: GDP per capita runs up to $105,000, while fertility rate is under 8. Without z-score standardization, distance-based clustering would simply group countries by raw wealth, ignoring child mortality and healthcare.">
            <div class="slide-header">
                <span class="breadcrumb-badge badge-purple">Question 3 · Unsupervised Learning & PCA</span>
                <h2 class="slide-title">HELP International Socio-Economic Dataset</h2>
                <p class="slide-subtitle">Discovering latent country clusters for equitable foreign aid allocation across 167 nations</p>
            </div>
            <div class="slide-body grid-2col">
                <div class="card">
                    <h3>Socio-Economic Development Context</h3>
                    <ul>
                        <li><strong>Objective:</strong> HELP International needs to categorize 167 nations to allocate humanitarian aid and development funds equitably.</li>
                        <li><strong>Unsupervised Setting:</strong> No ground-truth labels exist; natural clusters must emerge from multivariate socio-economic patterns.</li>
                        <li><strong>The 9 Indicators Evaluated:</strong>
                            <ul style="margin-top: 4px;">
                                <li>1. child_mort (deaths under 5 per 1,000 live births)</li>
                                <li>2. exports (% GDP) &nbsp;|&nbsp; 3. health spending (% GDP)</li>
                                <li>4. imports (% GDP) &nbsp;|&nbsp; 5. income per person (USD)</li>
                                <li>6. inflation (annual GDP %) &nbsp;|&nbsp; 7. life_expec (years)</li>
                                <li>8. total_fer (children per woman) &nbsp;|&nbsp; 9. gdpp (USD)</li>
                            </ul>
                        </li>
                    </ul>
                </div>
                <div class="card">
                    <h3>Preprocessing & Algorithmic Formulation</h3>
                    <ul>
                        <li><strong>Why Feature Scaling is Absolutely Mandatory:</strong>
                            <p style="margin-top: 4px;">GDP per capita ranges from $231 to $105,000, while fertility rate ranges from 1.15 to 7.49. Without standardization, GDP would dominate Euclidean distance by 10,000x, rendering health and mortality completely invisible to K-Means and PCA.</p>
                        </li>
                        <li style="margin-top: 8px;"><strong>Standardization to Zero Mean & Unit Variance:</strong>
                            <div style="font-family: var(--font-mono); font-size: 0.8rem; background: #f1f5f9; padding: 4px 8px; border-radius: 4px; margin: 4px 0;">
                                x_norm_ij = (x_ij - mean_j) / std_j
                            </div>
                        </li>
                        <li style="margin-top: 8px;"><strong>K-Means Optimization (Lloyd's Algorithm):</strong>
                            <p style="margin-top: 2px;">Minimizes WCSS across K clusters with 10 random restarts using K-Means++ initialization.</p>
                        </li>
                    </ul>
                </div>
            </div>
            <div class="slide-footer">
                <span>IIIT Sri City · Machine Learning</span>
                <span>Slide 11 of 16</span>
            </div>
        </section>

        <!-- SLIDE 12: Q3 - K-Means Elbow & Silhouette -->
        <section class="slide" data-notes="Here we examine the cluster selection criteria. Table 8 and Figure 9 display our Elbow curve and Silhouette scores across K=2 to 6. Notice that while K=4 produces the mathematical peak in silhouette score (0.3037), we selected K=3 for international policy alignment. The WCSS elbow levels off significantly after K=3 with diminishing returns. Crucially, K=3 partitions the 167 countries into three meaningful tiers: 36 Developed nations, 84 Developing nations, and 47 Underdeveloped nations that require immediate humanitarian assistance.">
            <div class="slide-header">
                <span class="breadcrumb-badge badge-purple">Question 3 · Unsupervised Learning & PCA</span>
                <h2 class="slide-title">K-Means Clustering: Elbow Method & Silhouette Scores</h2>
                <p class="slide-subtitle">Evaluating cluster cohesion and separation to select the optimal partition of 167 nations</p>
            </div>
            <div class="slide-body grid-2col-wide-left">
                <div>
                    <div class="card" style="margin-bottom: 12px;">
                        <h3>Table 8: WCSS & Silhouette Scores (K = 2 to 6)</h3>
                        <table class="styled-table">
                            <thead>
                                <tr>
                                    <th>Clusters (K)</th>
                                    <th>WCSS</th>
                                    <th>% Drop</th>
                                    <th>Silhouette</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr><td>K = 2</td><td>1050.21</td><td>-30.1%</td><td>0.2874</td></tr>
                                <tr class="highlight-row" style="background: #f5f3ff; color: #6d28d9;"><td>K = 3</td><td>831.42</td><td>-20.8%</td><td>0.2833</td></tr>
                                <tr><td>K = 4</td><td>700.70</td><td>-15.7%</td><td>0.3037</td></tr>
                                <tr><td>K = 5</td><td>632.16</td><td>-9.8%</td><td>0.2180</td></tr>
                                <tr><td>K = 6</td><td>576.66</td><td>-8.8%</td><td>0.2224</td></tr>
                            </tbody>
                        </table>
                    </div>
                    <div class="callout callout-purple">
                        <h4>Selected K = 3 Taxonomy (Actionable Aid Policy):</h4>
                        <p>• <strong>Cluster 0 (36 nations - Developed):</strong> High GDP ($42.5k), life exp 80.1 yr, child mort 5.0 (Germany, Japan, USA).<br>
                        • <strong>Cluster 1 (47 nations - Underdeveloped / High Priority):</strong> Severe poverty, low GDP ($1,909), life exp 56.6 yr, child mort 92.96 (Haiti, Afghanistan, Mali).<br>
                        • <strong>Cluster 2 (84 nations - Developing):</strong> Intermediate income ($12.3k), GDP ($6.5k), life exp 73.1 yr (India, Brazil, Indonesia).</p>
                    </div>
                </div>
                <div class="figure-box">
                    <img src="extracted_figures/fig9_kmeans_elbow_silhouette.png" alt="Figure 9: Elbow & Silhouette">
                    <p class="figure-caption">
                        <strong>Figure 9: K-Means Elbow Curve & Silhouette Profile</strong><br>
                        Why K=3 over mathematical peak K=4? Elbow criterion: WCSS drops sharply by 20.8% moving to K=3 (down to 831.42), with diminishing returns thereafter. K=4 merely fragments developing nations.
                    </p>
                </div>
            </div>
            <div class="slide-footer">
                <span>IIIT Sri City · Machine Learning</span>
                <span>Slide 12 of 16</span>
            </div>
        </section>

        <!-- SLIDE 13: Q3 - PCA Derivation & Eigendecomposition -->
        <section class="slide" data-notes="In Slide 13, we derive Principal Component Analysis mathematically from first principles. We compute the sample covariance matrix Sigma on the standardized data, and solve the symmetric eigenvalue problem Sigma v = lambda v. As reported in Table 10, the first principal component alone accounts for 45.95% of total variance. Adding PC2 and PC3 brings cumulative explained variance to 76.14%. The Scree plot on the right (Figure 11) confirms that after PC3, eigenvalues drop to approximately 1.0, proving that a 3-dimensional subspace captures three-quarters of all information in the original 9 dimensions.">
            <div class="slide-header">
                <span class="breadcrumb-badge badge-purple">Question 3 · Unsupervised Learning & PCA</span>
                <h2 class="slide-title">PCA: First-Principles Covariance Derivation & Scree Analysis</h2>
                <p class="slide-subtitle">Decomposing the 9x9 sample covariance matrix into orthogonal eigenvectors and eigenvalues</p>
            </div>
            <div class="slide-body grid-2col-wide-left">
                <div>
                    <div class="card" style="margin-bottom: 12px;">
                        <h3>Mathematical Formulation from Scratch</h3>
                        <p>1. Standardize features: X_norm with zero mean, unit variance.<br>
                        2. Sample Covariance Matrix: <strong>Sigma = (1 / (N - 1)) * X_norm^T * X_norm</strong> in R^(9x9)<br>
                        3. Symmetric Eigendecomposition: <strong>Sigma * v_k = lambda_k * v_k</strong>, ||v_k|| = 1<br>
                        4. Explained Variance Ratio: <strong>EVR_k = lambda_k / sum(lambda)</strong></p>

                        <table class="styled-table" style="margin-top: 10px;">
                            <thead>
                                <tr>
                                    <th>Component</th>
                                    <th>Eigenvalue (lambda)</th>
                                    <th>Individual EVR</th>
                                    <th>Cumulative EVR</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr><td>PC1</td><td>4.1606</td><td>45.95%</td><td>45.95%</td></tr>
                                <tr><td>PC2</td><td>1.5557</td><td>17.18%</td><td>63.13%</td></tr>
                                <tr><td>PC3</td><td>1.1774</td><td>13.00%</td><td><strong>76.14%</strong></td></tr>
                            </tbody>
                        </table>
                    </div>
                    <div class="callout callout-purple">
                        <h4>Variance Truncation:</h4>
                        <p>The top 3 principal components capture <strong>76.14% of the total dataset variance</strong>. Beyond PC3, eigenvalues drop below 1.0 (Kaiser criterion), confirming that 3 dimensions preserve 3/4 of the information.</p>
                    </div>
                </div>
                <div class="figure-box" style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px;">
                    <div>
                        <img src="extracted_figures/fig10_covariance_heatmap.png" alt="Figure 10: Covariance Heatmap" style="max-height: 240px;">
                        <p class="figure-caption"><strong>Fig 10: Covariance Heatmap</strong><br>Reveals collinear blocks (|r| > 0.85).</p>
                    </div>
                    <div>
                        <img src="extracted_figures/fig11_pca_scree.png" alt="Figure 11: Scree Plot" style="max-height: 240px;">
                        <p class="figure-caption"><strong>Fig 11: Scree Plot</strong><br>Elbow after PC3; tail flattens.</p>
                    </div>
                </div>
            </div>
            <div class="slide-footer">
                <span>IIIT Sri City · Machine Learning</span>
                <span>Slide 13 of 16</span>
            </div>
        </section>

        <!-- SLIDE 14: Q3 - Factor Loadings & 2D/3D Projections -->
        <section class="slide" data-notes="Slide 14 reveals the semantic meaning of our principal components and connects PCA back to K-Means. By analyzing the factor loadings in Table 11, PC1 clearly represents Socio-Economic Development, contrasting life expectancy against child mortality. PC2 captures Trade Openness, separating international trading hubs like Singapore and Luxembourg. When we project our 167 nations into the 2D and 3D PCA subspaces and color them by their K-Means cluster (Figures 12 and 13), we observe clean, distinct cluster separations. This demonstrates complete geometrical harmony between unsupervised clustering and dimensionality reduction.">
            <div class="slide-header">
                <span class="breadcrumb-badge badge-purple">Question 3 · Unsupervised Learning & PCA</span>
                <h2 class="slide-title">Factor Loadings & 2D / 3D Subspace Visualizations</h2>
                <p class="slide-subtitle">Interpreting principal component axes and projecting K-Means clusters into low-dimensional space</p>
            </div>
            <div class="slide-body grid-2col-wide-left">
                <div>
                    <div class="card" style="margin-bottom: 12px;">
                        <h3>Table 11: Factor Loadings & Semantic Interpretation</h3>
                        <table class="styled-table">
                            <thead>
                                <tr>
                                    <th>Axis</th>
                                    <th>EVR</th>
                                    <th>Top Positive Loading</th>
                                    <th>Top Negative Loading</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr><td>PC1</td><td>45.95%</td><td>life_expec (+0.43), income (+0.40)</td><td>child_mort (-0.42), total_fer (-0.40)</td></tr>
                                <tr><td>PC2</td><td>17.18%</td><td>imports (+0.67), exports (+0.61)</td><td>income (+0.02), gdpp (-0.05)</td></tr>
                                <tr><td>PC3</td><td>13.00%</td><td>health (+0.60), total_fer (+0.03)</td><td>inflation (-0.64), exports (-0.14)</td></tr>
                            </tbody>
                        </table>
                    </div>
                    <div class="callout callout-purple">
                        <h4>Semantic Axes:</h4>
                        <p>• <strong>PC1 (Development & Health):</strong> Contrasts prosperity & longevity vs childhood poverty.<br>
                        • <strong>PC2 (Trade Openness):</strong> Isolates trade hubs (Singapore, Luxembourg, Malta).<br>
                        • <strong>PC3 (Macro Stability):</strong> Contrasts public healthcare investment against inflation volatility.</p>
                    </div>
                </div>
                <div class="figure-box" style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px;">
                    <div>
                        <img src="extracted_figures/fig12_pca_2d.png" alt="Figure 12: 2D PCA Projection" style="max-height: 240px;">
                        <p class="figure-caption"><strong>Fig 12: 2D PCA Projection</strong><br>Colored by K-Means cluster (K=3).</p>
                    </div>
                    <div>
                        <img src="extracted_figures/fig13_pca_3d.png" alt="Figure 13: 3D PCA Projection" style="max-height: 240px;">
                        <p class="figure-caption"><strong>Fig 13: 3D PCA Projection</strong><br>Captures 76.14% cumulative variance.</p>
                    </div>
                </div>
            </div>
            <div class="slide-footer">
                <span>IIIT Sri City · Machine Learning</span>
                <span>Slide 14 of 16</span>
            </div>
        </section>

        <!-- SLIDE 15: Cross-Project Synthesis & Key Takeaways -->
        <section class="slide" data-notes="Slide 15 brings together our entire project findings into Table 12. Across all three domains, we observe consistent core principles: First, Pipeline encapsulation prevents subtle data leakage. Second, regularization is indispensable whenever model capacity is increased. Third, physical representation learning—such as polynomial interaction terms in regression—yields dramatically higher returns than tuning linear models. And fourth, bootstrap resampling provides the statistical rigor required to substantiate model comparisons.">
            <div class="slide-header">
                <span class="breadcrumb-badge badge-blue">Conclusions & Synthesis</span>
                <h2 class="slide-title">Cross-Domain Summary & Fundamental ML Takeaways</h2>
                <p class="slide-subtitle">Synthesizing optimal models, hyperparameter configurations, and core engineering principles</p>
            </div>
            <div class="card" style="margin-bottom: 16px;">
                <h3>Table 12: Master Synthesis of Champion Models across All Problems</h3>
                <table class="styled-table">
                    <thead>
                        <tr>
                            <th>Problem Domain</th>
                            <th>Evaluated Suite</th>
                            <th>Selected Model</th>
                            <th>Optimal Hyperparameters</th>
                            <th>Test Performance</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr><td>Q1: Classification</td><td>KNN, DT, SVM, CNN</td><td><strong>SVM (RBF Kernel)</strong></td><td>C = 5.0, gamma = 'scale'</td><td>Acc: 92.40% · F1: 0.9014 · AUC: 0.9697</td></tr>
                        <tr><td>Q1 Bonus: Deep Learning</td><td>Deep 1D CNN</td><td><strong>Deep 1D CNN</strong></td><td>3 Conv Blocks, Adam 1e-3</td><td>Acc: 91.53% · F1: 0.8926 · AUC: 0.9718</td></tr>
                        <tr class="highlight-green"><td>Q2: Regression</td><td>SGD, Ridge, Lasso, Poly</td><td><strong>Poly Ridge (All 81)</strong></td><td>Degree-2, Ridge alpha=10.0</td><td>R^2: 0.8542 · RMSE: 12.95 K (vs 17.5 K)</td></tr>
                        <tr style="background: #f5f3ff;"><td>Q3: Unsupervised & PCA</td><td>K-Means, Covariance PCA</td><td><strong>K-Means (K=3) & PCA</strong></td><td>K=3 clusters, Top 3 PCs</td><td>WCSS: 831.42 · Cumul. Var: 76.14%</td></tr>
                    </tbody>
                </table>
            </div>
            <div class="slide-body grid-4col">
                <div class="card" style="border-top: 3px solid #2563eb;">
                    <h3 style="font-size: 0.95rem; color: #2563eb;">1. Pipeline Integrity</h3>
                    <p style="font-size: 0.8rem;">Encapsulating scalers inside pipelines completely eliminates data leakage across CV folds.</p>
                </div>
                <div class="card" style="border-top: 3px solid #059669;">
                    <h3 style="font-size: 0.95rem; color: #059669;">2. Regularization</h3>
                    <p style="font-size: 0.8rem;">Mandatory when scaling feature capacity (Tree pruning, SVM C, Ridge/Lasso alpha, Dropout).</p>
                </div>
                <div class="card" style="border-top: 3px solid #d97706;">
                    <h3 style="font-size: 0.95rem; color: #d97706;">3. Non-Linear Synergy</h3>
                    <p style="font-size: 0.8rem;">Capturing 3,402 atomic interactions outperformed all linear hyperparameter tuning (+16.5% R^2).</p>
                </div>
                <div class="card" style="border-top: 3px solid #7c3aed;">
                    <h3 style="font-size: 0.95rem; color: #7c3aed;">4. Statistical Rigor</h3>
                    <p style="font-size: 0.8rem;">1,000 bootstrap resamples prevented false superiority claims between SVM and CNN.</p>
                </div>
            </div>
            <div class="slide-footer">
                <span>IIIT Sri City · Machine Learning</span>
                <span>Slide 15 of 16</span>
            </div>
        </section>

        <!-- SLIDE 16: Conclusion & Audience Q&A -->
        <section class="slide dark-theme" data-notes="In conclusion, this project demonstrated practical and theoretical mastery across classification, regression, and unsupervised learning. We thank our professors and peers for their guidance, and we are now delighted to answer any questions. Thank you!">
            <div style="height: 4px; background: #2563eb; width: 100%; border-radius: 2px; margin-bottom: 24px;"></div>
            <h1 class="slide-title" style="font-size: 2.8rem;">Thank You!</h1>
            <p class="slide-subtitle" style="font-size: 1.35rem; color: #94a3b8; margin-top: 8px;">
                We welcome any questions, discussions, and feedback.
            </p>

            <div class="slide-body grid-3col" style="margin-top: 36px; max-height: 220px;">
                <div class="card card-dark" style="border-top: 3px solid #2563eb;">
                    <div style="font-size: 0.75rem; font-weight: 700; color: #60a5fa; text-transform: uppercase;">Classification</div>
                    <h3 style="margin-top: 6px;">SVM (RBF) Champion</h3>
                    <p>92.40% accuracy, 92.22% precision, and overlapping bootstrap ROC-AUC with deep 1D CNN.</p>
                </div>
                <div class="card card-dark" style="border-top: 3px solid #059669;">
                    <div style="font-size: 0.75rem; font-weight: 700; color: #34d399; text-transform: uppercase;">Regression</div>
                    <h3 style="margin-top: 6px;">Poly Ridge Breakthrough</h3>
                    <p>Surged R^2 to 0.8542 and slashed RMSE to 12.95 K by capturing atomic interaction terms.</p>
                </div>
                <div class="card card-dark" style="border-top: 3px solid #7c3aed;">
                    <div style="font-size: 0.75rem; font-weight: 700; color: #c084fc; text-transform: uppercase;">Clustering & PCA</div>
                    <h3 style="margin-top: 6px;">Unified Harmony</h3>
                    <p>K=3 actionable development tiers; PCA explains 76.14% variance across 3 orthogonal dimensions.</p>
                </div>
            </div>

            <div style="margin-top: 40px;">
                <p style="font-weight: 700; font-size: 1.05rem; color: #ffffff;">Project Team: Yashasvee Patel (S20240010266) & P Karthik (S20240010184)</p>
                <p style="font-size: 0.9rem; color: #94a3b8; margin-top: 4px;">Department of Computer Science & Engineering · Indian Institute of Information Technology, Sri City</p>
                <p style="font-size: 0.85rem; color: #64748b; margin-top: 2px;">Codebase, trained models & full 25-page technical report available in repository.</p>
            </div>
            <div class="slide-footer">
                <span>IIIT Sri City · Machine Learning</span>
                <span>Slide 16 of 16</span>
            </div>
        </section>

    </div>

    <!-- Floating Navigation Controls -->
    <div class="controls">
        <button class="btn-ctrl" id="btnPrev" title="Previous Slide (Left Arrow)">◀ Prev</button>
        <span class="slide-indicator" id="slideIndicator">1 / 16</span>
        <button class="btn-ctrl" id="btnNext" title="Next Slide (Right Arrow or Space)">Next ▶</button>
        <div style="width: 1px; height: 18px; background: rgba(255,255,255,0.2);"></div>
        <button class="btn-ctrl" id="btnNotes" title="Toggle Speaker Notes (S)">🎙 Notes</button>
        <button class="btn-ctrl" id="btnOverview" title="Slide Overview Grid (G)">⊞ Grid</button>
        <button class="btn-ctrl" id="btnFullscreen" title="Toggle Fullscreen (F)">⛶ Fullscreen</button>
    </div>

    <!-- Speaker Notes Panel -->
    <aside class="notes-panel" id="notesPanel">
        <div class="notes-header">
            <h3>Speaker Notes & Talking Points</h3>
            <button class="btn-ctrl" id="btnCloseNotes" style="padding: 2px 8px;">✕</button>
        </div>
        <div class="notes-content" id="notesContent">
            Loading speaker notes...
        </div>
    </aside>

    <!-- Slide Overview Modal -->
    <div class="overview-modal" id="overviewModal">
        <div style="display: flex; justify-content: space-between; align-items: center; max-width: 1400px; margin: 0 auto 24px auto;">
            <h2 style="color: #ffffff; font-size: 1.5rem;">Slide Overview (Press ESC to exit)</h2>
            <button class="btn-ctrl" id="btnCloseOverview" style="font-size: 1.1rem;">✕ Close</button>
        </div>
        <div class="overview-grid" id="overviewGrid"></div>
    </div>

    <script>
        const slides = document.querySelectorAll('.slide');
        const progressBar = document.getElementById('progressBar');
        const slideIndicator = document.getElementById('slideIndicator');
        const btnPrev = document.getElementById('btnPrev');
        const btnNext = document.getElementById('btnNext');
        const btnNotes = document.getElementById('btnNotes');
        const btnCloseNotes = document.getElementById('btnCloseNotes');
        const notesPanel = document.getElementById('notesPanel');
        const notesContent = document.getElementById('notesContent');
        const btnOverview = document.getElementById('btnOverview');
        const btnCloseOverview = document.getElementById('btnCloseOverview');
        const overviewModal = document.getElementById('overviewModal');
        const overviewGrid = document.getElementById('overviewGrid');
        const btnFullscreen = document.getElementById('btnFullscreen');

        let currentSlide = 0;
        const totalSlides = slides.length;

        function updateSlide(index) {
            if (index < 0) index = 0;
            if (index >= totalSlides) index = totalSlides - 1;
            currentSlide = index;

            slides.forEach((slide, i) => {
                slide.classList.toggle('active', i === currentSlide);
            });

            const progress = ((currentSlide + 1) / totalSlides) * 100;
            progressBar.style.width = `${progress}%`;
            slideIndicator.textContent = `${currentSlide + 1} / ${totalSlides}`;

            // Update notes
            const activeSlide = slides[currentSlide];
            const notes = activeSlide.getAttribute('data-notes') || 'No speaker notes for this slide.';
            notesContent.innerHTML = `<p>${notes}</p>`;

            // Update overview cards active state
            document.querySelectorAll('.overview-card').forEach((card, i) => {
                card.classList.toggle('active-card', i === currentSlide);
            });
        }

        btnPrev.addEventListener('click', () => updateSlide(currentSlide - 1));
        btnNext.addEventListener('click', () => updateSlide(currentSlide + 1));

        btnNotes.addEventListener('click', () => notesPanel.classList.toggle('open'));
        btnCloseNotes.addEventListener('click', () => notesPanel.classList.remove('open'));

        btnOverview.addEventListener('click', () => overviewModal.classList.add('open'));
        btnCloseOverview.addEventListener('click', () => overviewModal.classList.remove('open'));

        btnFullscreen.addEventListener('click', () => {
            if (!document.fullscreenElement) {
                document.documentElement.requestFullscreen().catch(err => alert(err.message));
            } else {
                document.exitFullscreen();
            }
        });

        // Populate Overview Grid
        slides.forEach((slide, i) => {
            const titleEl = slide.querySelector('.slide-title');
            const title = titleEl ? titleEl.textContent : `Slide ${i + 1}`;
            const subEl = slide.querySelector('.slide-subtitle');
            const sub = subEl ? subEl.textContent : '';

            const card = document.createElement('div');
            card.className = `overview-card ${i === 0 ? 'active-card' : ''}`;
            card.innerHTML = `<h4>Slide ${i + 1}: ${title}</h4><p>${sub.substring(0, 80)}...</p>`;
            card.addEventListener('click', () => {
                updateSlide(i);
                overviewModal.classList.remove('open');
            });
            overviewGrid.appendChild(card);
        });

        // Keyboard Controls
        window.addEventListener('keydown', (e) => {
            if (overviewModal.classList.contains('open')) {
                if (e.key === 'Escape') overviewModal.classList.remove('open');
                return;
            }

            if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {
                e.preventDefault();
                updateSlide(currentSlide + 1);
            } else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
                e.preventDefault();
                updateSlide(currentSlide - 1);
            } else if (e.key === 's' || e.key === 'S') {
                notesPanel.classList.toggle('open');
            } else if (e.key === 'g' || e.key === 'G') {
                overviewModal.classList.toggle('open');
            } else if (e.key === 'f' || e.key === 'F') {
                if (!document.fullscreenElement) {
                    document.documentElement.requestFullscreen();
                } else {
                    document.exitFullscreen();
                }
            } else if (e.key === 'Home') {
                updateSlide(0);
            } else if (e.key === 'End') {
                updateSlide(totalSlides - 1);
            }
        });

        // Initial setup
        updateSlide(0);
    </script>
</body>
</html>
"""

with open("presentation.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Interactive presentation generated successfully: presentation.html ({len(html_content)} bytes)")

