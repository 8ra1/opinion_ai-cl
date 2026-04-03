from pathlib import Path
import joblib

base_dir = Path(__file__).parent
models_dir = base_dir / "models"

category_model = joblib.load(models_dir / "category_model.pkl")
opinion_model = joblib.load(models_dir / "opinion_model.pkl")
category_vectorizer = joblib.load(models_dir / "category_vectorizer.pkl")
opinion_vectorizer = joblib.load(models_dir / "opinion_vectorizer.pkl")


def predict_category(text):
    text_vectorized = category_vectorizer.transform([text])
    prediction = category_model.predict(text_vectorized)[0]
    return prediction


def predict_opinion(text):
    text_vectorized = opinion_vectorizer.transform([text])
    prediction = opinion_model.predict(text_vectorized)[0]
    return prediction


def analyze_review(text):
    category = predict_category(text)
    opinion = predict_opinion(text)

    return {
        "category": category,
        "opinion": opinion
    }


if __name__ == "__main__":
    sample_text = "الأكل كان لذيذا جدا والخدمة ممتازة"
    result = analyze_review(sample_text)

    print("Text:", sample_text)
    print("Predicted Category:", result["category"])
    print("Predicted Opinion:", result["opinion"])