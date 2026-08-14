"""
HR Employee Attrition - Multi-Algorithm Training & Evaluation
Trains many classification algorithms, evaluates with multiple metrics,
picks the best model, and exports everything needed for the dashboard.
"""
import json
import warnings
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    RandomForestClassifier, GradientBoostingClassifier,
    AdaBoostClassifier, ExtraTreesClassifier, VotingClassifier
)
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, roc_curve, confusion_matrix, classification_report
)
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier

warnings.filterwarnings("ignore")
RANDOM_STATE = 42

# ---------------------------------------------------------------
# 1. Load data
# ---------------------------------------------------------------
df = pd.read_csv("data/WA_Fn-UseC_-HR-Employee-Attrition.csv")

drop_cols = ["EmployeeCount", "EmployeeNumber", "Over18", "StandardHours"]
df = df.drop(columns=[c for c in drop_cols if c in df.columns])

target_col = "Attrition"
y_raw = df[target_col].map({"Yes": 1, "No": 0})
X = df.drop(columns=[target_col])

cat_cols = X.select_dtypes(include="object").columns.tolist()
num_cols = X.select_dtypes(exclude="object").columns.tolist()

encoders = {}
for c in cat_cols:
    le = LabelEncoder()
    X[c] = le.fit_transform(X[c])
    encoders[c] = le

X_train, X_test, y_train, y_test = train_test_split(
    X, y_raw, test_size=0.2, random_state=RANDOM_STATE, stratify=y_raw
)

scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s = scaler.transform(X_test)
X_train_s = pd.DataFrame(X_train_s, columns=X.columns)
X_test_s = pd.DataFrame(X_test_s, columns=X.columns)

# models needing scaled input
scaled_models = {"Logistic Regression", "Support Vector Machine (SVM)",
                  "K-Nearest Neighbors", "Neural Network (MLP)",
                  "Naive Bayes", "Linear Discriminant Analysis"}

models = {
    "Logistic Regression": LogisticRegression(max_iter=2000, random_state=RANDOM_STATE),
    "Decision Tree": DecisionTreeClassifier(random_state=RANDOM_STATE, max_depth=6),
    "Random Forest": RandomForestClassifier(n_estimators=300, random_state=RANDOM_STATE),
    "Extra Trees": ExtraTreesClassifier(n_estimators=300, random_state=RANDOM_STATE),
    "Gradient Boosting": GradientBoostingClassifier(random_state=RANDOM_STATE),
    "AdaBoost": AdaBoostClassifier(random_state=RANDOM_STATE, n_estimators=200),
    "XGBoost": XGBClassifier(
        random_state=RANDOM_STATE, eval_metric="logloss",
        n_estimators=300, max_depth=4, learning_rate=0.05, verbosity=0
    ),
    "LightGBM": LGBMClassifier(random_state=RANDOM_STATE, n_estimators=300, verbosity=-1),
    "Support Vector Machine (SVM)": SVC(probability=True, random_state=RANDOM_STATE),
    "K-Nearest Neighbors": KNeighborsClassifier(n_neighbors=9),
    "Naive Bayes": GaussianNB(),
    "Neural Network (MLP)": MLPClassifier(
        random_state=RANDOM_STATE, max_iter=800, hidden_layer_sizes=(64, 32)
    ),
    "Linear Discriminant Analysis": LinearDiscriminantAnalysis(),
}

results = {}
roc_data = {}
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)

for name, model in models.items():
    use_scaled = name in scaled_models
    xtr, xte = (X_train_s, X_test_s) if use_scaled else (X_train, X_test)

    model.fit(xtr, y_train)
    y_pred = model.predict(xte)
    y_proba = model.predict_proba(xte)[:, 1] if hasattr(model, "predict_proba") else y_pred

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, zero_division=0)
    rec = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    try:
        auc = roc_auc_score(y_test, y_proba)
    except Exception:
        auc = None

    cv_scores = cross_val_score(model, xtr, y_train, cv=cv, scoring="accuracy")
    cm = confusion_matrix(y_test, y_pred).tolist()

    fpr, tpr, _ = roc_curve(y_test, y_proba)
    roc_data[name] = {
        "fpr": fpr[::max(1, len(fpr)//30)].tolist(),
        "tpr": tpr[::max(1, len(tpr)//30)].tolist(),
    }

    results[name] = {
        "accuracy": round(acc * 100, 2),
        "precision": round(prec * 100, 2),
        "recall": round(rec * 100, 2),
        "f1_score": round(f1 * 100, 2),
        "roc_auc": round(auc * 100, 2) if auc is not None else None,
        "cv_mean_accuracy": round(cv_scores.mean() * 100, 2),
        "cv_std_accuracy": round(cv_scores.std() * 100, 2),
        "confusion_matrix": cm,
        "scaled_input": use_scaled,
    }
    print(f"{name:32s} | Acc: {acc*100:6.2f}% | F1: {f1*100:6.2f}% | AUC: {(auc*100 if auc else 0):6.2f}%")

# ---------------------------------------------------------------
# 2. Ensemble - Voting Classifier of top 3 tree-based models
# ---------------------------------------------------------------
top3_names = sorted(results, key=lambda n: results[n]["f1_score"], reverse=True)[:3]
estimators = [(n.replace(" ", "_"), models[n]) for n in top3_names]
voting = VotingClassifier(estimators=estimators, voting="soft")
voting.fit(X_train, y_train)
y_pred_v = voting.predict(X_test)
y_proba_v = voting.predict_proba(X_test)[:, 1]

acc = accuracy_score(y_test, y_pred_v)
prec = precision_score(y_test, y_pred_v, zero_division=0)
rec = recall_score(y_test, y_pred_v, zero_division=0)
f1 = f1_score(y_test, y_pred_v, zero_division=0)
auc = roc_auc_score(y_test, y_proba_v)
cv_scores = cross_val_score(voting, X_train, y_train, cv=cv, scoring="accuracy")
cm = confusion_matrix(y_test, y_pred_v).tolist()
fpr, tpr, _ = roc_curve(y_test, y_proba_v)
roc_data["Voting Ensemble (Top 3)"] = {
    "fpr": fpr[::max(1, len(fpr)//30)].tolist(),
    "tpr": tpr[::max(1, len(tpr)//30)].tolist(),
}
results["Voting Ensemble (Top 3)"] = {
    "accuracy": round(acc * 100, 2),
    "precision": round(prec * 100, 2),
    "recall": round(rec * 100, 2),
    "f1_score": round(f1 * 100, 2),
    "roc_auc": round(auc * 100, 2),
    "cv_mean_accuracy": round(cv_scores.mean() * 100, 2),
    "cv_std_accuracy": round(cv_scores.std() * 100, 2),
    "confusion_matrix": cm,
    "scaled_input": False,
    "note": f"Soft-voting ensemble of: {', '.join(top3_names)}",
}
print(f"{'Voting Ensemble (Top 3)':32s} | Acc: {acc*100:6.2f}% | F1: {f1*100:6.2f}% | AUC: {auc*100:6.2f}%")

# ---------------------------------------------------------------
# 3. Best model selection (ranked by F1, tie-break Accuracy then AUC)
# ---------------------------------------------------------------
best_model_name = sorted(
    results,
    key=lambda n: (results[n]["f1_score"], results[n]["accuracy"], results[n]["roc_auc"] or 0),
    reverse=True,
)[0]
print("\nBEST MODEL:", best_model_name, results[best_model_name])

# ---------------------------------------------------------------
# 4. Feature importance (from Random Forest, always available)
# ---------------------------------------------------------------
rf_model = models["Random Forest"]
importances = rf_model.feature_importances_
feat_imp = sorted(
    zip(X.columns.tolist(), importances.tolist()), key=lambda t: t[1], reverse=True
)
feat_imp = [{"feature": f, "importance": round(v * 100, 3)} for f, v in feat_imp[:15]]

# ---------------------------------------------------------------
# 5. Dataset-level stats for dashboard visuals
# ---------------------------------------------------------------
dataset_stats = {
    "total_records": int(len(df)),
    "total_features": int(X.shape[1]),
    "attrition_yes": int((y_raw == 1).sum()),
    "attrition_no": int((y_raw == 0).sum()),
    "attrition_rate": round(float((y_raw == 1).mean()) * 100, 2),
    "train_size": int(len(X_train)),
    "test_size": int(len(X_test)),
}

dept_attrition = (
    df.groupby("Department")[target_col]
    .apply(lambda s: round((s == "Yes").mean() * 100, 2))
    .reset_index()
    .rename(columns={target_col: "attrition_rate"})
    .to_dict(orient="records")
)

jobrole_attrition = (
    df.groupby("JobRole")[target_col]
    .apply(lambda s: round((s == "Yes").mean() * 100, 2))
    .reset_index()
    .rename(columns={target_col: "attrition_rate"})
    .sort_values("attrition_rate", ascending=False)
    .to_dict(orient="records")
)

overtime_attrition = (
    df.groupby("OverTime")[target_col]
    .apply(lambda s: round((s == "Yes").mean() * 100, 2))
    .reset_index()
    .rename(columns={target_col: "attrition_rate"})
    .to_dict(orient="records")
)

age_bins = pd.cut(df["Age"], bins=[17, 25, 30, 35, 40, 45, 50, 61],
                   labels=["18-25", "26-30", "31-35", "36-40", "41-45", "46-50", "51-60"])
age_attrition = (
    df.assign(AgeGroup=age_bins)
    .groupby("AgeGroup", observed=True)[target_col]
    .apply(lambda s: round((s == "Yes").mean() * 100, 2))
    .reset_index()
    .rename(columns={target_col: "attrition_rate"})
    .to_dict(orient="records")
)

income_by_attrition = (
    df.groupby(target_col)["MonthlyIncome"]
    .mean()
    .round(2)
    .reset_index()
    .to_dict(orient="records")
)

satisfaction_cols = ["JobSatisfaction", "EnvironmentSatisfaction", "RelationshipSatisfaction", "WorkLifeBalance"]
satisfaction_avg = {
    c: {
        "Yes": round(df.loc[y_raw == 1, c].mean(), 2),
        "No": round(df.loc[y_raw == 0, c].mean(), 2),
    }
    for c in satisfaction_cols
}

# ---------------------------------------------------------------
# 6. Export everything to JSON for the dashboard
# ---------------------------------------------------------------
output = {
    "best_model": best_model_name,
    "results": results,
    "roc_data": roc_data,
    "feature_importance": feat_imp,
    "dataset_stats": dataset_stats,
    "dept_attrition": dept_attrition,
    "jobrole_attrition": jobrole_attrition,
    "overtime_attrition": overtime_attrition,
    "age_attrition": age_attrition,
    "income_by_attrition": income_by_attrition,
    "satisfaction_avg": satisfaction_avg,
}

with open("output/results.json", "w") as f:
    json.dump(output, f, indent=2)

print("\nSaved output/results.json")
print("\nRanking (by F1 score):")
for i, name in enumerate(sorted(results, key=lambda n: results[n]["f1_score"], reverse=True), 1):
    r = results[name]
    print(f"{i:2d}. {name:32s} Acc={r['accuracy']}%  F1={r['f1_score']}%  AUC={r['roc_auc']}%")
