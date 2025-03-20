from flask import Flask, request, jsonify
import json
import requests

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    product_url = data.get('product_url')
    review_type = data.get('review_type')

    if not product_url or not review_type:
        return jsonify({"error": "Missing product URL or review type"}), 400

    # Mock API call (Replace with actual API URL)
    response = requests.get(f"https://api.example.com/reviews?url={product_url}&type={review_type}")
    
    if response.status_code == 200:
        review_data = response.json()

        # Save response to a JSON file
        with open("reviews.json", "w") as file:
            json.dump(review_data, file, indent=4)

        return jsonify(review_data)
    else:
        return jsonify({"error": "Failed to fetch reviews"}), 500

if __name__ == '__main__':
    app.run(debug=True)
