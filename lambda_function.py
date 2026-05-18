import json
from analysis import analysis.py
from db import db.py

def lambda_handler(event, context):
    try:
        body = json.loads(event["body"])
        review = body.get("review")

        if not review:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Review is required"})
            }

        # ✅ Run your AI model
        result = analyze_text(review)

        category = result["category"]
        sentiment = result["sentiment"]

        # ✅ Save to database
        save_feedback(review, category, sentiment)

        return {
            "statusCode": 200,
            "body": json.dumps({
                "review": review,
                "category": category,
                "sentiment": sentiment
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": str(e)
        }
