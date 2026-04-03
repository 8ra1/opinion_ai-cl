# =========================================
# OPINION.AI - Training Script
# هذا الملف مسؤول عن:
# 1) قراءة بيانات التدريب
# 2) تدريب مودل الفئة
# 3) تدريب مودل الرأي
# 4) حفظ المودلات والـ vectorizers
# =========================================

import pandas as pd
from pathlib import Path
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# -----------------------------------------
# تحديد مسارات المشروع
# -----------------------------------------
base_dir = Path(__file__).parent
data_path = base_dir / "data" / "training_reviews.csv"
models_dir = base_dir / "models"

# إنشاء مجلد models إذا لم يكن موجودًا
models_dir.mkdir(exist_ok=True)

# -----------------------------------------
# قراءة ملف البيانات
# encoding="utf-8-sig" مناسب غالبًا مع الملفات العربية
# -----------------------------------------
df = pd.read_csv(data_path, encoding="utf-8-sig")

# -----------------------------------------
# حذف الصفوف الناقصة احتياطًا
# -----------------------------------------
df = df.dropna(subset=["text", "category", "opinion"])

# -----------------------------------------
# تنظيف بسيط للنصوص والقيم
# strip() يزيل الفراغات الزائدة
# -----------------------------------------
df["text"] = df["text"].astype(str).str.strip()
df["category"] = df["category"].astype(str).str.strip()
df["opinion"] = df["opinion"].astype(str).str.strip()

# -----------------------------------------
# فصل النصوص عن الـ labels
# X = النصوص
# y_category = الفئات الصحيحة
# y_opinion = الآراء الصحيحة
# -----------------------------------------
X = df["text"]
y_category = df["category"]
y_opinion = df["opinion"]

# -----------------------------------------
# إنشاء أدوات تحويل النص إلى features رقمية
# استخدمنا TF-IDF لأنه بسيط ومناسب
# ngram_range=(1, 2) يعني:
# - كلمات مفردة
# - وكلمتين متجاورتين
# -----------------------------------------
category_vectorizer = TfidfVectorizer(ngram_range=(1, 2))
opinion_vectorizer = TfidfVectorizer(ngram_range=(1, 2))

# -----------------------------------------
# تحويل النصوص إلى صيغة رقمية
# fit_transform:
# - يتعلم من النصوص
# - ثم يحولها إلى features
# -----------------------------------------
X_category_vec = category_vectorizer.fit_transform(X)
X_opinion_vec = opinion_vectorizer.fit_transform(X)

# -----------------------------------------
# إنشاء المودلات
# اخترنا LogisticRegression لأنه:
# - بسيط
# - سريع
# - جيد لمشروعك الحالي
# max_iter=1000 لتقليل مشاكل convergence
# -----------------------------------------
category_model = LogisticRegression(max_iter=1000)
opinion_model = LogisticRegression(max_iter=1000)

# -----------------------------------------
# تدريب المودلين
# -----------------------------------------
category_model.fit(X_category_vec, y_category)
opinion_model.fit(X_opinion_vec, y_opinion)

# -----------------------------------------
# حفظ المودلات داخل مجلد models
# -----------------------------------------
joblib.dump(category_model, models_dir / "category_model.pkl")
joblib.dump(opinion_model, models_dir / "opinion_model.pkl")

# -----------------------------------------
# حفظ الـ vectorizers أيضًا
# لأن analysis.py يحتاجها لاحقًا
# -----------------------------------------
joblib.dump(category_vectorizer, models_dir / "category_vectorizer.pkl")
joblib.dump(opinion_vectorizer, models_dir / "opinion_vectorizer.pkl")

# -----------------------------------------
# رسالة نجاح
# -----------------------------------------
print("Training completed successfully.")
print("Models and vectorizers were saved in the models folder.")