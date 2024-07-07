import json
from flask import Flask, request, jsonify
from transformers import pipeline
import psycopg2
import requests

app = Flask(__name__)

sentiment_model = pipeline("sentiment-analysis")

db_settings = {
    "host": "localhost",
    "database": "sentiment_analysis",
    "user": "postgres",
    "password": "your_password"
}

external_api_url = "http://example.com/sentiment_analysis_api"

@app.route('/analyze_sentiment', methods=['POST'])
def analyze_sentiment():
    try:
        text_data = request.json['text']
        
        sentiment_result_local = sentiment_model(text_data)
        local_sentiment = sentiment_result_local[0]['label']
        
        save_to_database(text_data, local_sentiment)
        
        response = requests.post(external_api_url, json={"text": text_data})
        
        if response.status_code == 200:
            api_sentiment = response.json()['sentiment']
            save_to_database(text_data, api_sentiment)
            
            return jsonify({"local_sentiment": local_sentiment, "api_sentiment": api_sentiment}), 200
        else:
            return jsonify({"error": "External API request failed"}), 500
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def save_to_database(text_data, sentiment):
    try:
        conn = psycopg2.connect(**db_settings)
        cursor = conn.cursor()
        
        cursor.execute("INSERT INTO sentiment_data (text, sentiment) VALUES (%s, %s)", (text_data, sentiment))
        
        conn.commit()
        cursor.close()
        conn.close()
        
    except Exception as e:
        print("Error:", e)

if __name__ == '__main__':
    app.run(debug=True)
