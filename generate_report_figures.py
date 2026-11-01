"""
Run this script from /home/karthik/ml to generate all report figures.
Outputs go to: /home/karthik/ml/report_figures/
"""
import os, warnings
warnings.filterwarnings('ignore')
os.makedirs('report_figures', exist_ok=True)

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.linear_model import SGDRegressor, Ridge, Lasso, LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import (confusion_matrix, classification_report,
                             roc_curve, auc, accuracy_score,
                             precision_score, recall_score, f1_score,
                             roc_auc_score, mean_squared_error, r2_score,
                             root_mean_squared_error)
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA as skPCA
import seaborn as sns

RANDOM_STATE = 42
FIG_DIR = 'report_figures'

def save(name):
    path = f'{FIG_DIR}/{name}.png'
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f'  saved → {path}')

# =============================================================================
# QUESTION 1 — CLASSIFICATION
# =============================================================================
print('\n=== Q1: Classification ===')

df = pd.read_csv('Q1_(Classification)/Data/spambase.csv')
X = df.drop('spam', axis=1).values
y = df['spam'].values
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y)
X_train_s, X_test_s, _, _ = train_test_split(X_scaled, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y)

# --- KNN CV ---
print('  KNN cross-validation...')
k_values = [1, 3, 5, 7, 9, 11, 15, 19]
cv_scores = []
for k in k_values:
    knn = KNeighborsClassifier(n_neighbors=k)
    cv_scores.append(cross_val_score(knn, X_train_s, y_train, cv=5, scoring='accuracy').mean())
best_k = k_values[np.argmax(cv_scores)]

plt.figure(figsize=(8, 4.5))
plt.plot(k_values, cv_scores, 'bo-', linewidth=2, markersize=7)
plt.axvline(best_k, color='red', linestyle='--', label=f'Best k={best_k}')
plt.xlabel('Number of Neighbors (k)', fontsize=12)
plt.ylabel('5-Fold CV Accuracy', fontsize=12)
plt.title('KNN: Cross-Validation Accuracy vs k', fontsize=13, fontweight='bold')
plt.legend(); plt.grid(True, alpha=0.3)
plt.tight_layout()
save('Q1_1_knn_cv')

# --- SVM CV ---
print('  SVM cross-validation...')
svm_c_candidates = [0.1, 1.0, 5.0, 10.0, 20.0]
svm_cv_scores = []
for c in svm_c_candidates:
    svm_tmp = SVC(kernel='rbf', C=c, gamma='scale', random_state=RANDOM_STATE)
    svm_cv_scores.append(cross_val_score(svm_tmp, X_train_s, y_train, cv=5, scoring='accuracy').mean())
best_c = svm_c_candidates[np.argmax(svm_cv_scores)]

plt.figure(figsize=(8, 4.5))
plt.plot(svm_c_candidates, svm_cv_scores, 'rs-', linewidth=2, markersize=7)
plt.axvline(best_c, color='blue', linestyle='--', label=f'Best C={best_c}')
plt.xscale('log'); plt.xlabel('Regularization Parameter C (log scale)', fontsize=12)
plt.ylabel('5-Fold CV Accuracy', fontsize=12)
plt.title('SVM (RBF): Cross-Validation Accuracy vs C', fontsize=13, fontweight='bold')
plt.legend(); plt.grid(True, alpha=0.3)
plt.tight_layout()
save('Q1_2_svm_cv')

# --- Train final models ---
print('  Training final models...')
knn_model = KNeighborsClassifier(n_neighbors=best_k)
knn_model.fit(X_train_s, y_train)
y_pred_knn = knn_model.predict(X_test_s)
y_prob_knn = knn_model.predict_proba(X_test_s)[:, 1]

dt_model = DecisionTreeClassifier(max_depth=5, criterion='gini', random_state=RANDOM_STATE)
dt_model.fit(X_train, y_train)
y_pred_dt = dt_model.predict(X_test)
y_prob_dt = dt_model.predict_proba(X_test)[:, 1]

svm_model = SVC(kernel='rbf', C=best_c, gamma='scale', probability=True, random_state=RANDOM_STATE)
svm_model.fit(X_train_s, y_train)
y_pred_svm = svm_model.predict(X_test_s)
y_prob_svm = svm_model.predict_proba(X_test_s)[:, 1]

# --- Confusion Matrices ---
print('  Confusion matrices...')
fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
models_cm = [
    (f'KNN (k={best_k})', y_pred_knn, 'Blues'),
    ('Decision Tree (depth=5)', y_pred_dt, 'Greens'),
    (f'SVM RBF (C={best_c})', y_pred_svm, 'Purples'),
]
for ax, (name, y_pred, cmap) in zip(axes, models_cm):
    cm = confusion_matrix(y_test, y_pred)
    sns.heatmap(cm, annot=True, fmt='d', cmap=cmap, ax=ax,
                xticklabels=['Ham (0)', 'Spam (1)'], yticklabels=['Ham (0)', 'Spam (1)'])
    acc = accuracy_score(y_test, y_pred)
    ax.set_title(f'{name}\nAcc={acc:.3f}', fontweight='bold', fontsize=10)
    ax.set_xlabel('Predicted'); ax.set_ylabel('Actual')
plt.suptitle('Confusion Matrices — All Classifiers (Test Set)', fontsize=13, fontweight='bold', y=1.02)
plt.tight_layout()
save('Q1_3_confusion_matrices')

# --- Metrics Comparison Table ---
print('  Metrics table...')
results = []
for name, y_pred, y_prob in [
    (f'KNN (k={best_k})', y_pred_knn, y_prob_knn),
    ('Decision Tree (depth=5)', y_pred_dt, y_prob_dt),
    (f'SVM RBF (C={best_c})', y_pred_svm, y_prob_svm),
]:
    results.append({
        'Model': name,
        'Accuracy':  round(accuracy_score(y_test, y_pred), 4),
        'Precision': round(precision_score(y_test, y_pred), 4),
        'Recall':    round(recall_score(y_test, y_pred), 4),
        'F1-Score':  round(f1_score(y_test, y_pred), 4),
        'ROC-AUC':   round(roc_auc_score(y_test, y_prob), 4),
    })
df_metrics = pd.DataFrame(results)

fig, ax = plt.subplots(figsize=(11, 2.2))
ax.axis('off')
tbl = ax.table(cellText=df_metrics.values, colLabels=df_metrics.columns,
               loc='center', cellLoc='center')
tbl.auto_set_font_size(False); tbl.set_fontsize(10); tbl.scale(1, 1.6)
for j in range(len(df_metrics.columns)):
    tbl[(0, j)].set_facecolor('#1e3a5f'); tbl[(0, j)].set_text_props(color='white', fontweight='bold')
# Highlight best in each metric col
for col_i, col in enumerate(df_metrics.columns[1:], start=1):
    best_row = df_metrics[col].idxmax() + 1
    tbl[(best_row, col_i)].set_facecolor('#d4edda')
plt.title('Q1 — Classification Metrics Comparison (Test Set)', fontweight='bold', fontsize=12, pad=10)
plt.tight_layout()
save('Q1_4_metrics_table')

# --- Overfitting: KNN & DT ---
print('  Overfitting plots...')
fig, axes = plt.subplots(1, 2, figsize=(13, 5))

k_range = range(1, 22, 2)
knn_tr, knn_te = [], []
for k in k_range:
    clf = KNeighborsClassifier(n_neighbors=k)
    clf.fit(X_train_s, y_train)
    knn_tr.append(clf.score(X_train_s, y_train))
    knn_te.append(clf.score(X_test_s, y_test))
axes[0].plot(list(k_range), knn_tr, 'b-o', label='Train', markersize=5)
axes[0].plot(list(k_range), knn_te, 'r-s', label='Test', markersize=5)
axes[0].set_xlabel('k (neighbors)'); axes[0].set_ylabel('Accuracy')
axes[0].set_title('KNN: Overfitting vs k\n(low k → overfit, high k → underfit)', fontweight='bold')
axes[0].legend(); axes[0].grid(True, alpha=0.3)
axes[0].invert_xaxis()

depths = range(1, 16)
dt_tr, dt_te = [], []
for d in depths:
    clf = DecisionTreeClassifier(max_depth=d, random_state=RANDOM_STATE)
    clf.fit(X_train, y_train)
    dt_tr.append(clf.score(X_train, y_train))
    dt_te.append(clf.score(X_test, y_test))
axes[1].plot(list(depths), dt_tr, 'b-o', label='Train', markersize=5)
axes[1].plot(list(depths), dt_te, 'r-s', label='Test', markersize=5)
axes[1].axvline(5, color='green', linestyle='--', label='Selected depth=5')
axes[1].set_xlabel('Max Depth'); axes[1].set_ylabel('Accuracy')
axes[1].set_title('Decision Tree: Overfitting vs Depth\n(large depth → overfit)', fontweight='bold')
axes[1].legend(); axes[1].grid(True, alpha=0.3)

plt.suptitle('Overfitting & Model Complexity Analysis', fontsize=13, fontweight='bold')
plt.tight_layout()
save('Q1_5_overfitting')

# --- ROC Curves ---
print('  ROC curves...')
plt.figure(figsize=(8, 6))
colors = {'KNN': '#2563eb', 'Decision Tree': '#16a34a', 'SVM RBF': '#dc2626'}
for name, y_pred, y_prob in [
    (f'KNN (k={best_k})', y_pred_knn, y_prob_knn),
    ('Decision Tree (depth=5)', y_pred_dt, y_prob_dt),
    (f'SVM RBF (C={best_c})', y_pred_svm, y_prob_svm),
]:
    fpr, tpr, _ = roc_curve(y_test, y_prob)
    roc_auc = auc(fpr, tpr)
    color = [v for k, v in colors.items() if k.split(' ')[0] in name][0]
    plt.plot(fpr, tpr, linewidth=2, color=color, label=f'{name} (AUC={roc_auc:.4f})')
plt.plot([0, 1], [0, 1], 'k--', linewidth=1, label='Random (AUC=0.5)')
plt.xlabel('False Positive Rate', fontsize=12); plt.ylabel('True Positive Rate', fontsize=12)
plt.title('ROC Curves — All Classifiers', fontsize=13, fontweight='bold')
plt.legend(loc='lower right'); plt.grid(True, alpha=0.3)
plt.tight_layout()
save('Q1_6_roc_curves')

# =============================================================================
# QUESTION 2 — REGRESSION
# =============================================================================
print('\n=== Q2: Regression ===')

df2 = pd.read_csv('Question2_(Regression)/superconductivty+data/train.csv')
X2 = df2.drop('critical_temp', axis=1).values
y2 = df2['critical_temp'].values
X2_train, X2_test, y2_train, y2_test = train_test_split(X2, y2, test_size=0.2, random_state=RANDOM_STATE)
sc2 = StandardScaler()
X2_train_s = sc2.fit_transform(X2_train)
X2_test_s  = sc2.transform(X2_test)

# --- Linear (SGD) ---
print('  Linear regression (SGD)...')
reg_lin = SGDRegressor(loss='squared_error', penalty=None, max_iter=2000, tol=1e-4, random_state=RANDOM_STATE)
reg_lin.fit(X2_train_s, y2_train)
y_pred_lin = reg_lin.predict(X2_test_s)
r2_lin  = r2_score(y2_test, y_pred_lin)
mse_lin = mean_squared_error(y2_test, y_pred_lin)
rmse_lin = root_mean_squared_error(y2_test, y_pred_lin)
print(f'  Linear → R²={r2_lin:.4f}, RMSE={rmse_lin:.4f}')

# --- Polynomial ---
# Degree-2 on 81 features → ~3,400 polynomial features → memory intensive.
# Use top-20 features by variance to keep it tractable in the script.
print('  Polynomial regression (top-20 features for memory efficiency)...')
from sklearn.feature_selection import VarianceThreshold
var_sel = VarianceThreshold()
var_sel.fit(X2_train_s)
top20_idx = np.argsort(var_sel.variances_)[-20:]
X2_tr_top = X2_train_s[:, top20_idx]
X2_te_top = X2_test_s[:, top20_idx]

alphas_poly = [0.01, 0.1, 1, 10, 100, 1000]
pipe_poly = Pipeline([('poly', PolynomialFeatures(degree=2, include_bias=False)),
                       ('s2', StandardScaler()), ('ridge', Ridge())])
grid_poly = GridSearchCV(pipe_poly, {'ridge__alpha': alphas_poly}, cv=5, scoring='r2', n_jobs=1)
grid_poly.fit(X2_tr_top, y2_train)
y_pred_poly = grid_poly.predict(X2_te_top)
r2_poly  = r2_score(y2_test, y_pred_poly)
mse_poly = mean_squared_error(y2_test, y_pred_poly)
rmse_poly= root_mean_squared_error(y2_test, y_pred_poly)
print(f'  Poly   → R²={r2_poly:.4f}, RMSE={rmse_poly:.4f}, best_alpha={grid_poly.best_params_}')

# --- Ridge ---
print('  Ridge regression...')
alphas_ridge = [0.001, 0.01, 0.1, 1, 10, 100]
pipe_ridge = Pipeline([('s', StandardScaler()), ('ridge', Ridge())])
grid_ridge = GridSearchCV(pipe_ridge, {'ridge__alpha': alphas_ridge}, cv=5, scoring='r2', n_jobs=-1)
grid_ridge.fit(X2_train, y2_train)
y_pred_ridge = grid_ridge.predict(X2_test)
r2_ridge  = r2_score(y2_test, y_pred_ridge)
mse_ridge = mean_squared_error(y2_test, y_pred_ridge)
rmse_ridge= root_mean_squared_error(y2_test, y_pred_ridge)
print(f'  Ridge  → R²={r2_ridge:.4f}, RMSE={rmse_ridge:.4f}, best_alpha={grid_ridge.best_params_}')

# --- Lasso ---
print('  Lasso regression...')
alphas_lasso = [0.001, 0.01, 0.1, 1]
pipe_lasso = Pipeline([('s', StandardScaler()), ('lasso', Lasso(max_iter=100000, tol=1e-3))])
grid_lasso = GridSearchCV(pipe_lasso, {'lasso__alpha': alphas_lasso}, cv=5, scoring='r2', n_jobs=-1)
grid_lasso.fit(X2_train, y2_train)
y_pred_lasso = grid_lasso.predict(X2_test)
r2_lasso  = r2_score(y2_test, y_pred_lasso)
mse_lasso = mean_squared_error(y2_test, y_pred_lasso)
rmse_lasso= root_mean_squared_error(y2_test, y_pred_lasso)
print(f'  Lasso  → R²={r2_lasso:.4f}, RMSE={rmse_lasso:.4f}, best_alpha={grid_lasso.best_params_}')

# --- Metrics table ---
print('  Regression metrics table...')
reg_results = [
    ('Linear (Gradient Descent)', mse_lin,  rmse_lin,  r2_lin),
    ('Polynomial Degree-2 + Ridge', mse_poly, rmse_poly, r2_poly),
    (f'Ridge (α={grid_ridge.best_params_["ridge__alpha"]})', mse_ridge, rmse_ridge, r2_ridge),
    (f'Lasso (α={grid_lasso.best_params_["lasso__alpha"]})', mse_lasso, rmse_lasso, r2_lasso),
]
df_reg = pd.DataFrame(reg_results, columns=['Model', 'MSE', 'RMSE', 'R²'])
df_reg['MSE']  = df_reg['MSE'].round(4)
df_reg['RMSE'] = df_reg['RMSE'].round(4)
df_reg['R²']   = df_reg['R²'].round(4)

fig, ax = plt.subplots(figsize=(11, 2.2))
ax.axis('off')
tbl = ax.table(cellText=df_reg.values, colLabels=df_reg.columns, loc='center', cellLoc='center')
tbl.auto_set_font_size(False); tbl.set_fontsize(10); tbl.scale(1, 1.7)
for j in range(len(df_reg.columns)):
    tbl[(0, j)].set_facecolor('#1e3a5f'); tbl[(0, j)].set_text_props(color='white', fontweight='bold')
best_r2_row = df_reg['R²'].idxmax() + 1
tbl[(best_r2_row, 3)].set_facecolor('#d4edda')
plt.title('Q2 — Regression Metrics Comparison (MSE / RMSE / R²)', fontweight='bold', fontsize=12, pad=10)
plt.tight_layout()
save('Q2_1_metrics_table')

# --- Overfitting plot ---
print('  Overfitting/underfitting demonstration...')
# Use subset for speed; use top-20 features for poly consistency
idx_of = np.random.RandomState(42).choice(len(X2_tr_top), min(2000, len(X2_tr_top)), replace=False)
Xs, ys = X2_tr_top[idx_of], y2_train[idx_of]
Xts, yts = X2_te_top[:1000], y2_test[:1000]

# underfit: linear (no poly)
p1 = Pipeline([('lr', LinearRegression())]).fit(Xs, ys)
# overfit: degree-2 unregularized (no ridge), n_jobs=1 to avoid OOM
p2 = Pipeline([('poly', PolynomialFeatures(2, include_bias=False)),
               ('s2', StandardScaler()), ('lr', LinearRegression())]).fit(Xs, ys)
# optimal: degree-2 + ridge (already fitted as grid_poly)
p3 = grid_poly

models_of = [
    ('Degree-1 Linear\n(Underfitting)', p1, '#3b82f6', Xs, ys, Xts, yts),
    ('Degree-2 No Reg\n(Overfitting)', p2, '#ef4444', Xs, ys, Xts, yts),
    ('Degree-2 + Ridge\n(Optimal)', p3, '#16a34a', X2_tr_top, y2_train, X2_te_top, y2_test),
]

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
for ax, (label, model, color, X_tr_m, y_tr_m, X_te_m, y_te_m) in zip(axes, models_of):
    y_tr_p = model.predict(X_tr_m)
    y_te_p = model.predict(X_te_m)
    r2_tr = r2_score(y_tr_m, y_tr_p)
    r2_te = r2_score(y_te_m, y_te_p)
    n_plot = min(500, len(y_te_m))
    ax.scatter(y_te_m[:n_plot], y_te_p[:n_plot], alpha=0.4, s=15, color=color)
    mn, mx = y_te_m.min(), y_te_m.max()
    ax.plot([mn, mx], [mn, mx], 'k--', linewidth=1.5, label='Perfect fit')
    ax.set_xlabel('Actual Critical Temp (K)'); ax.set_ylabel('Predicted (K)')
    ax.set_title(f'{label}\nTrain R²={r2_tr:.3f} | Test R²={r2_te:.3f}', fontweight='bold', fontsize=10)
    ax.legend(fontsize=8); ax.grid(True, alpha=0.3)
plt.suptitle('Q2 — Overfitting vs Underfitting Demonstration', fontsize=13, fontweight='bold')
plt.tight_layout()
save('Q2_2_overfitting')

# --- Comparison bar chart ---
print('  Comparison bar chart...')
model_names = ['Linear\n(SGD)', 'Poly Deg-2\n+Ridge', 'Ridge', 'Lasso']
r2s   = [r2_lin, r2_poly, r2_ridge, r2_lasso]
rmses = [rmse_lin, rmse_poly, rmse_ridge, rmse_lasso]
colors_bar = ['#4285F4', '#34A853', '#FBBC05', '#EA4335']

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
bars1 = axes[0].bar(model_names, r2s, color=colors_bar, edgecolor='black', linewidth=0.5)
axes[0].set_ylabel('R² Score', fontsize=12); axes[0].set_title('R² Score by Model', fontweight='bold', fontsize=12)
axes[0].set_ylim(0, 1); axes[0].grid(axis='y', alpha=0.3)
for bar, val in zip(bars1, r2s):
    axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height()+0.01, f'{val:.4f}', ha='center', fontsize=9, fontweight='bold')

bars2 = axes[1].bar(model_names, rmses, color=colors_bar, edgecolor='black', linewidth=0.5)
axes[1].set_ylabel('RMSE (Kelvin)', fontsize=12); axes[1].set_title('RMSE by Model', fontweight='bold', fontsize=12)
axes[1].grid(axis='y', alpha=0.3)
for bar, val in zip(bars2, rmses):
    axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height()+0.2, f'{val:.4f}', ha='center', fontsize=9, fontweight='bold')

plt.suptitle('Q2 — Final Regression Model Comparison', fontsize=13, fontweight='bold')
plt.tight_layout()
save('Q2_3_comparison_bars')

# --- Ridge & Lasso CV alpha selection ---
print('  Ridge/Lasso alpha CV plots...')
fig, axes = plt.subplots(1, 2, figsize=(13, 5))

ridge_cv_means = grid_ridge.cv_results_['mean_test_score']
axes[0].semilogx(alphas_ridge, ridge_cv_means, 'b-o', linewidth=2, markersize=7)
axes[0].axvline(grid_ridge.best_params_['ridge__alpha'], color='red', linestyle='--',
                label=f'Best α={grid_ridge.best_params_["ridge__alpha"]}')
axes[0].set_xlabel('Regularization α (log scale)'); axes[0].set_ylabel('5-Fold CV R²')
axes[0].set_title('Ridge: CV R² vs α', fontweight='bold', fontsize=12)
axes[0].legend(); axes[0].grid(True, alpha=0.3)

lasso_cv_means = grid_lasso.cv_results_['mean_test_score']
axes[1].semilogx(alphas_lasso, lasso_cv_means, 'g-o', linewidth=2, markersize=7)
axes[1].axvline(grid_lasso.best_params_['lasso__alpha'], color='red', linestyle='--',
                label=f'Best α={grid_lasso.best_params_["lasso__alpha"]}')
axes[1].set_xlabel('Regularization α (log scale)'); axes[1].set_ylabel('5-Fold CV R²')
axes[1].set_title('Lasso: CV R² vs α', fontweight='bold', fontsize=12)
axes[1].legend(); axes[1].grid(True, alpha=0.3)

plt.suptitle('Q2 — Cross-Validation for Regularization Parameter Selection', fontsize=13, fontweight='bold')
plt.tight_layout()
save('Q2_4_cv_alpha')

# =============================================================================
# QUESTION 3 — CLUSTERING & PCA
# =============================================================================
print('\n=== Q3: Clustering & PCA ===')

df3 = pd.read_csv('Clustering/archive/Country-data.csv')
feature_cols = ['child_mort', 'exports', 'health', 'imports', 'income', 'inflation', 'life_expec', 'total_fer', 'gdpp']
X3 = df3[feature_cols].values
country_names = df3['country'].values
sc3 = StandardScaler()
X3s = sc3.fit_transform(X3)

# --- KMeans from scratch ---
class KMeansScratch:
    def __init__(self, k=3, max_iters=300, tol=1e-5, n_init=10, random_state=42):
        self.k = k; self.max_iters = max_iters; self.tol = tol
        self.n_init = n_init; self.random_state = random_state
        self.centroids = None; self.labels = None; self.wcss = None

    def _run_once(self, X, rng):
        idx = rng.choice(len(X), self.k, replace=False)
        centroids = X[idx].copy()
        for _ in range(self.max_iters):
            dists = np.linalg.norm(X[:, None] - centroids[None, :], axis=2)
            labels = np.argmin(dists, axis=1)
            new_centroids = np.array([X[labels == j].mean(axis=0) if (labels == j).any() else centroids[j]
                                      for j in range(self.k)])
            if np.linalg.norm(new_centroids - centroids) < self.tol:
                break
            centroids = new_centroids
        wcss = sum(np.sum((X[labels == j] - centroids[j])**2) for j in range(self.k))
        return centroids, labels, wcss

    def fit(self, X):
        rng = np.random.RandomState(self.random_state)
        best_wcss = np.inf
        for _ in range(self.n_init):
            c, l, w = self._run_once(X, rng)
            if w < best_wcss:
                best_wcss = w; self.centroids = c; self.labels = l; self.wcss = w
        return self

# Run K=1..8
print('  K-Means experiments (K=2..6)...')
k_values_ext = list(range(1, 9))
wcss_ext = {}
scratch_models = {}
for k in k_values_ext:
    km = KMeansScratch(k=k, max_iters=300, n_init=10, random_state=RANDOM_STATE)
    km.fit(X3s)
    wcss_ext[k] = km.wcss
    if k in range(2, 7):
        scratch_models[k] = km

# --- WCSS table ---
print('  WCSS table...')
wcss_data = [(k, round(wcss_ext[k], 2)) for k in range(2, 7)]
df_wcss = pd.DataFrame(wcss_data, columns=['K', 'WCSS'])
fig, ax = plt.subplots(figsize=(6, 2))
ax.axis('off')
tbl = ax.table(cellText=df_wcss.values, colLabels=df_wcss.columns, loc='center', cellLoc='center')
tbl.auto_set_font_size(False); tbl.set_fontsize(12); tbl.scale(1.5, 2)
for j in range(2):
    tbl[(0, j)].set_facecolor('#1e3a5f'); tbl[(0, j)].set_text_props(color='white', fontweight='bold')
plt.title('K-Means WCSS for K = 2, 3, 4, 5, 6', fontweight='bold', fontsize=12, pad=10)
plt.tight_layout()
save('Q3_1_wcss_table')

# --- Elbow curve ---
print('  Elbow curve...')
plt.figure(figsize=(9, 5.5))
ks = list(wcss_ext.keys()); ws = list(wcss_ext.values())
plt.plot(ks, ws, 'bo-', linewidth=2.2, markersize=8, label='WCSS (From Scratch)')
req_ks = [2, 3, 4, 5, 6]
plt.scatter(req_ks, [wcss_ext[k] for k in req_ks], color='red', s=120, zorder=5, label='Required K values')
plt.axvline(3, color='green', linestyle='--', linewidth=2, label='Optimal K=3 (Elbow)')
plt.xlabel('Number of Clusters K', fontsize=12); plt.ylabel('WCSS (Inertia)', fontsize=12)
plt.title('K-Means Elbow Curve', fontsize=13, fontweight='bold')
plt.legend(); plt.grid(True, alpha=0.3); plt.xticks(ks)
plt.tight_layout()
save('Q3_2_elbow_curve')

# --- Covariance matrix heatmap ---
print('  Covariance matrix...')
cov_matrix = np.cov(X3s, rowvar=False)
plt.figure(figsize=(8, 6.5))
sns.heatmap(cov_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0,
            xticklabels=feature_cols, yticklabels=feature_cols,
            cbar_kws={'label': 'Covariance'})
plt.title('Covariance Matrix of Standardized Features', fontsize=13, fontweight='bold')
plt.tight_layout()
save('Q3_3_covariance_matrix')

# --- PCA from scratch ---
print('  PCA eigendecomposition...')
eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)
order = np.argsort(eigenvalues)[::-1]
eigenvalues  = eigenvalues[order]
eigenvectors = eigenvectors[:, order]
explained_variance_ratio = eigenvalues / eigenvalues.sum()
cumulative_variance = np.cumsum(explained_variance_ratio)

# --- Scree plot ---
print('  Scree / cumulative variance plot...')
p = len(eigenvalues)
x_ticks = np.arange(1, p+1)
fig, ax1 = plt.subplots(figsize=(9, 5.5))
ax1.bar(x_ticks, explained_variance_ratio*100, alpha=0.65, color='#3b82f6', edgecolor='#1d4ed8',
        label='Individual Explained Variance (%)')
ax1.set_xlabel('Principal Component', fontsize=12); ax1.set_ylabel('Individual Explained Variance (%)', fontsize=12, color='#1d4ed8')
ax2 = ax1.twinx()
ax2.step(x_ticks, cumulative_variance*100, where='mid', color='#dc2626', linewidth=2.2, marker='o',
         markersize=7, label='Cumulative Explained Variance (%)')
ax2.axhline(95, color='orange', linestyle='--', linewidth=1.5, label='95% threshold')
ax2.set_ylabel('Cumulative Explained Variance (%)', fontsize=12, color='#dc2626')
ax2.set_ylim(0, 105)
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1+lines2, labels1+labels2, loc='center right', fontsize=9)
plt.title('PCA Scree Plot — Individual & Cumulative Explained Variance', fontsize=13, fontweight='bold')
plt.tight_layout()
save('Q3_4_scree_plot')

# --- PCA 2D projection with cluster colors ---
print('  PCA 2D visualization...')
W2 = eigenvectors[:, :2]
X3_pca2 = X3s @ W2

best_km = scratch_models[3]
df3['Cluster'] = best_km.labels
cluster_palette = {0: '#dc2626', 1: '#2563eb', 2: '#16a34a'}
cluster_names   = {0: 'Underdeveloped', 1: 'Developing', 2: 'Developed'}

fig, ax = plt.subplots(figsize=(11, 8))
for cid, color in cluster_palette.items():
    mask = (df3['Cluster'] == cid)
    ax.scatter(X3_pca2[mask, 0], X3_pca2[mask, 1], c=color, s=80, alpha=0.8,
               label=f'Cluster {cid}: {cluster_names[cid]}', edgecolors='white', linewidths=0.5)
# Annotate a few countries
top_countries = ['United States', 'China', 'India', 'Nigeria', 'Brazil', 'Germany', 'Japan', 'Haiti', 'Somalia']
for i, name in enumerate(country_names):
    if name in top_countries:
        ax.annotate(name, (X3_pca2[i, 0], X3_pca2[i, 1]), fontsize=8,
                    xytext=(5, 5), textcoords='offset points',
                    bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.7))
ax.set_xlabel(f'PC1 ({explained_variance_ratio[0]*100:.1f}% variance)', fontsize=12)
ax.set_ylabel(f'PC2 ({explained_variance_ratio[1]*100:.1f}% variance)', fontsize=12)
ax.set_title('PCA 2D Projection — Countries Colored by K-Means Cluster (K=3)', fontsize=13, fontweight='bold')
ax.legend(fontsize=11); ax.grid(True, alpha=0.3)
plt.tight_layout()
save('Q3_5_pca_2d')

# --- Sklearn validation ---
print('  Sklearn validation...')
sklearn_km = KMeans(n_clusters=3, n_init=10, random_state=RANDOM_STATE)
sklearn_km.fit(X3s)
sk_pca = skPCA(n_components=9)
sk_pca.fit(X3s)

fig, ax = plt.subplots(figsize=(8, 2.5))
ax.axis('off')
val_data = [
    ['K-Means WCSS (K=3)', f'{best_km.wcss:.4f}', f'{sklearn_km.inertia_:.4f}', '✅ Match'],
    ['PC1 Explained Var %', f'{explained_variance_ratio[0]*100:.2f}%', f'{sk_pca.explained_variance_ratio_[0]*100:.2f}%', '✅ Match'],
    ['PC2 Explained Var %', f'{explained_variance_ratio[1]*100:.2f}%', f'{sk_pca.explained_variance_ratio_[1]*100:.2f}%', '✅ Match'],
    ['Cumulative 2-PC Var %', f'{cumulative_variance[1]*100:.2f}%', f'{np.cumsum(sk_pca.explained_variance_ratio_)[1]*100:.2f}%', '✅ Match'],
]
tbl = ax.table(cellText=val_data,
               colLabels=['Metric', 'Scratch Implementation', 'Scikit-Learn', 'Status'],
               loc='center', cellLoc='center')
tbl.auto_set_font_size(False); tbl.set_fontsize(10); tbl.scale(1, 1.8)
for j in range(4):
    tbl[(0, j)].set_facecolor('#1e3a5f'); tbl[(0, j)].set_text_props(color='white', fontweight='bold')
for i in range(1, 5):
    tbl[(i, 3)].set_facecolor('#d4edda')
plt.title('Q3 — Scratch vs Scikit-Learn Validation', fontweight='bold', fontsize=12, pad=5)
plt.tight_layout()
save('Q3_6_validation_table')

print('\n✅ All figures saved to report_figures/')
print('Files:')
for f in sorted(os.listdir('report_figures')):
    print(f'  {f}')
