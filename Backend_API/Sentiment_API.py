from flask import Flask, request, jsonify
import pandas as pd
import json
from flask_cors import CORS

# Import your original functions exactly as defined in Main_functions.py
from Main_functions import Fetch_Review, Check_sentiment, get_review_text, sentiment_report


app = Flask(__name__)
CORS(app)


@app.route('/Fetch_Product_reviews', methods=['GET'])
def Fetch_Product_reviews():
    try:
        url = request.args.get('url')
        review_type = request.args.get('type', 'multiple')

        if not url:
            return jsonify({"error": "URL parameter is required"}), 400

        print("Fetching reviews...")  # Debugging
        reviews_df = Fetch_Review(url, review_type)
        print("Fetched reviews:completed")  # Debugging

        if isinstance(reviews_df, dict) and "error" in reviews_df:
            return jsonify(reviews_df), 400

        print("Classifying sentiment...")  # Debugging
        sentiment_df = Check_sentiment(reviews_df)
        print("Classified sentiment:Completed")  # Debugging

        print("Extracting review lists...")  # Debugging
        positive_reviews, negative_reviews, neutral_reviews = get_review_text(sentiment_df)
        print("Extracted lists:Completed")  # Debugging

        print("Calculating sentiment percentages...")  # Debugging
        sentiment_percentages = sentiment_report(sentiment_df)

        # Ensure percentages are returned as a dictionary
        if isinstance(sentiment_percentages, tuple):  
            sentiment_percentages = {
                "positive_percentage": sentiment_percentages[0],
                "negative_percentage": sentiment_percentages[1],
                "neutral_percentage": sentiment_percentages[2]
            }

        print("Sentiment percentages:Completed")  # Debugging

        # Final API response
        response = {
            "reviews": {
                "positive_reviews": positive_reviews,
                "negative_reviews": negative_reviews,
                "neutral_reviews": neutral_reviews
            },
            "percentages": sentiment_percentages
        }

        # Use json.dumps() with ensure_ascii=False to display emojis correctly
        return app.response_class(
            response=json.dumps(response, ensure_ascii=False),
            status=200,
            mimetype="application/json"
        )

    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
