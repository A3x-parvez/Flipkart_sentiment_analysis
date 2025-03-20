import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

# Where the Main and sub Review are present
def fetch_reviews_multiple(url, start=1, end=20):
    reviews_list = []

    for i in range(start, end + 1):
        try:
            url_page = f"{url}&page={i}"
            response = requests.get(url_page, timeout=10)
            response.raise_for_status()  # Raise HTTPError for bad responses
            
            soup = BeautifulSoup(response.content, 'html.parser')
            reviews_container = soup.find_all("div", class_="cPHDOP col-12-12")
            if not reviews_container:
                continue  # Skip pages with no reviews

            review_divs = soup.find_all("div", class_="ZmyHeo")
            for div in review_divs:
                try:
                    review_text = div.div.text.strip()
                    review_text = review_text.replace("READ MORE", "")
                    reviews_list.append(review_text)
                except AttributeError:
                    continue  # Skip any malformed review elements

        except requests.exceptions.RequestException as e:
            print(f"Error fetching page {i}: {e}")
            continue  # Skip this page and move to the next

    return pd.DataFrame({'review': reviews_list})


# Where the Single Review is present
def fetch_reviews_single(url, start=1, end=20):
    reviews_list = []

    for i in range(start, end + 1):
        try:
            url_page = f"{url}&page={i}"
            response = requests.get(url_page, timeout=10)
            response.raise_for_status()  # Raise HTTPError for bad responses

            soup = BeautifulSoup(response.content, 'html.parser')
            reviews_container = soup.find_all("div", class_="ZmyHeo MDcJkH")
            if not reviews_container:
                continue  # Skip pages with no reviews

            review_divs = soup.find_all("div", class_="_11pzQk")
            for div in review_divs:
                try:
                    review_text = div.get_text(strip=True)
                    review_text = review_text.replace("READ MORE", "")
                    reviews_list.append(review_text)
                except AttributeError:
                    continue  # Skip any malformed review elements

        except requests.exceptions.RequestException as e:
            print(f"Error fetching page {i}: {e}")
            continue  # Skip this page and move to the next

    return pd.DataFrame({'review': reviews_list})


# Final function for fetch reviews of the product this function internally call fetch_reviews_multiple and fetch_reviews_single based on the parameters
def Fetch_Review(url, Type='multiple'):
    try:
        # Check if URL is a valid string and starts with Flipkart's domain
        if not isinstance(url, str) or not url.startswith("https://www.flipkart.com/"):
            return {"error": "Invalid URL: Must be a valid Flipkart link."}  # Changed: Returning error instead of printing

        # Ensure the URL follows the exact product review format
        pattern = r"^https://www\.flipkart\.com/[^/]+/product-reviews/[^/?]+(\?.*)?$"
        if not re.match(pattern, url):
            return {"error": "Invalid URL: Only Flipkart product review links are allowed."}  # Changed: Returning error instead of printing

        # Check if Type is valid
        if Type == 'single':
            df_final = fetch_reviews_single(url)
        elif Type == 'multiple':
            df_final = fetch_reviews_multiple(url)
        else:
            return {"error": "Invalid Type specified. Use 'single' or 'multiple'."}  # Changed: Returning error instead of printing

        return df_final  # No change: Returns the DataFrame normally if everything is correct

    except Exception as e:
        return {"error": f"An unexpected error occurred: {e}"}  # Changed: Returning error message instead of printing


# Check polarity
def sentiment_model(text):
    sia = SentimentIntensityAnalyzer()
    over_all_polarity = sia.polarity_scores(text)
    if over_all_polarity['compound'] >= 0.05:
        return "positive"
    elif over_all_polarity['compound'] <= -0.05:
        return "negative"
    else:
        return "neutral"


# Check sentimet of the comments
def Check_sentiment(df):
    try:
        if not isinstance(df, pd.DataFrame):  # Ensure input is a DataFrame
            return {"error": "Invalid input: Expected a pandas DataFrame."}
        
        if 'review' not in df.columns:  # Check if 'review' column exists
            return {"error": "Missing column: DataFrame must contain a 'review' column."}
        
        if df.empty:  # Handle empty DataFrame
            return {"error": "Empty DataFrame: No reviews available for sentiment analysis."}

        df_with_polarity = df.copy()
        df_with_polarity['sentiment'] = df_with_polarity['review'].apply(sentiment_model)  # Apply sentiment analysis

        return df_with_polarity

    except Exception as e:
        return {"error": f"An unexpected error occurred: {e}"}
    

# Return final positive negative and neutral reviews for product in list format for show in frontend
def get_review_text(final_df):
    try:
        if not isinstance(final_df, pd.DataFrame):  # Ensure input is a DataFrame
            return {"error": "Invalid input: Expected a pandas DataFrame."}
        
        required_columns = {'sentiment', 'review'}
        if not required_columns.issubset(final_df.columns):  # Check required columns
            return {"error": "Missing columns: DataFrame must contain 'review' and 'sentiment' columns."}
        
        if final_df.empty:  # Handle empty DataFrame
            return {"error": "Empty DataFrame: No reviews available."}

        # Extract reviews based on sentiment
        positive_reviews = final_df[final_df['sentiment'] == 'positive']['review'].tolist()
        negative_reviews = final_df[final_df['sentiment'] == 'negative']['review'].tolist()
        neutral_reviews = final_df[final_df['sentiment'] == 'neutral']['review'].tolist()  # Fixed typo "neural" → "neutral"

        return positive_reviews, negative_reviews, neutral_reviews

    except Exception as e:
        return{"error": f"An unexpected error occurred: {e}"}
    

# Final product report
def sentiment_report(df):
    try:
        if not isinstance(df, pd.DataFrame):  # Ensure input is a DataFrame
            return {"error": "Invalid input: Expected a pandas DataFrame."}
        
        required_columns = {'sentiment'}
        if not required_columns.issubset(df.columns):  # Check required columns
            return {"error": "Missing column: DataFrame must contain 'sentiment' column."}
        
        if df.empty:  # Handle empty DataFrame
            return {"error": "Empty DataFrame: No data available for sentiment analysis."}

        final_report = df.copy()
        total = final_report['sentiment'].shape[0]

        # Avoid division by zero
        if total == 0:
            return {"error": "No sentiment data found."}

        positive = final_report[final_report['sentiment'] == 'positive'].shape[0]
        negative = final_report[final_report['sentiment'] == 'negative'].shape[0]
        neutral = final_report[final_report['sentiment'] == 'neutral'].shape[0]

        # # Calculate percentages safely
        # positive_percentage = (positive / total) * 100
        # negative_percentage = (negative / total) * 100
        # neutral_percentage = (neutral / total) * 100

        # Calculate percentages safely with three decimal places
        positive_percentage = round((positive / total) * 100, 3)
        negative_percentage = round((negative / total) * 100, 3)
        neutral_percentage = round((neutral / total) * 100, 3)


        return positive_percentage, negative_percentage, neutral_percentage

    except Exception as e:
        return {"error": f"An unexpected error occurred: {e}"}
    


