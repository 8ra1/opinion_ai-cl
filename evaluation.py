# =========================================
# OPINION.AI - Evaluation Script
# هذا الملف مسؤول عن:
# 1) قراءة بيانات التدريب
# 2) تقسيمها إلى تدريب واختبار
# 3) تدريب مودل الفئة ومودل الرأي على جزء التدريب
# 4) قياس الأداء على جزء الاختبار
# =========================================

import pandas as pd
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, classification_report

# -----------------------------------------
# تحديد مسار ملف البيانات
# -----------------------------------------
base_dir = Path(__file__).parent
data_path = base_dir / "data" / "training_reviews.csv"

# -----------------------------------------
# قراءة ملف البيانات
# -----------------------------------------
df = pd.read_csv(data_path, encoding="utf-8-sig")

# حذف الصفوف الناقصة إن وجدت
df = df.dropna(subset=["text", "category", "opinion"])

# تنظيف بسيط للنصوص والقيم
df["text"] = df["text"].astype(str).str.strip()
df["category"] = df["category"].astype(str).str.strip()
df["opinion"] = df["opinion"].astype(str).str.strip()

# -----------------------------------------
# عرض معلومات سريعة عن البيانات
# -----------------------------------------
print("=== DATASET INFO ===")
print("Rows and Columns:", df.shape)

print("\nCategory Distribution:")
print(df["category"].value_counts())

print("\nOpinion Distribution:")
print(df["opinion"].value_counts())

# -----------------------------------------
# فصل النصوص عن الـ labels
# -----------------------------------------
X = df["text"]
y_category = df["category"]
y_opinion = df["opinion"]

# -----------------------------------------
# تقييم مودل الفئة
# -----------------------------------------

# تقسيم البيانات إلى تدريب واختبار
X_train_cat, X_test_cat, y_train_cat, y_test_cat = train_test_split(
    X,
    y_category,
    test_size=0.2,
    random_state=42,
    stratify=y_category
)

# تحويل النصوص إلى features رقمية
category_vectorizer = TfidfVectorizer(ngram_range=(1, 2))
X_train_cat_vec = category_vectorizer.fit_transform(X_train_cat)
X_test_cat_vec = category_vectorizer.transform(X_test_cat)

# إنشاء مودل الفئة
category_model = LogisticRegression(max_iter=1000)

# تدريب مودل الفئة
category_model.fit(X_train_cat_vec, y_train_cat)

# التنبؤ على بيانات الاختبار
y_pred_cat = category_model.predict(X_test_cat_vec)

# حساب النتائج
category_accuracy = accuracy_score(y_test_cat, y_pred_cat)
category_macro_f1 = f1_score(y_test_cat, y_pred_cat, average="macro")

# طباعة نتائج مودل الفئة
print("\n=== CATEGORY MODEL RESULTS ===")
print(f"Accuracy: {category_accuracy:.4f}")
print(f"Macro F1: {category_macro_f1:.4f}")

print("\nCategory Classification Report:")
print(classification_report(y_test_cat, y_pred_cat))

# -----------------------------------------
# تقييم مودل الرأي
# -----------------------------------------

# تقسيم البيانات إلى تدريب واختبار
X_train_op, X_test_op, y_train_op, y_test_op = train_test_split(
    X,
    y_opinion,
    test_size=0.2,
    random_state=42,
    stratify=y_opinion
)

# تحويل النصوص إلى features رقمية
opinion_vectorizer = TfidfVectorizer(ngram_range=(1, 2))
X_train_op_vec = opinion_vectorizer.fit_transform(X_train_op)
X_test_op_vec = opinion_vectorizer.transform(X_test_op)

# إنشاء مودل الرأي
opinion_model = LogisticRegression(max_iter=1000)

# تدريب مودل الرأي
opinion_model.fit(X_train_op_vec, y_train_op)

# التنبؤ على بيانات الاختبار
y_pred_op = opinion_model.predict(X_test_op_vec)

# حساب النتائج
opinion_accuracy = accuracy_score(y_test_op, y_pred_op)
opinion_macro_f1 = f1_score(y_test_op, y_pred_op, average="macro")

# طباعة نتائج مودل الرأي
print("\n=== OPINION MODEL RESULTS ===")
print(f"Accuracy: {opinion_accuracy:.4f}")
print(f"Macro F1: {opinion_macro_f1:.4f}")

print("\nOpinion Classification Report:")
print(classification_report(y_test_op, y_pred_op))