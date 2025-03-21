# api.py
from flask import Flask, request, jsonify
import news_scraper
import sentiment_analysis
import text2speech

app = Flask(__name__)

@app.route('/fetch_articles', methods=['GET'])
def fetch_articles():
    """
    API endpoint to fetch news articles based on the company name.
    Returns JSON with articles, including sentiment analysis.
    """
    company_name = request.args.get('company', default='', type=str)
    if not company_name:
        return jsonify({"error": "Company name is required"}), 400

    # 1) Scrape/fetch the news articles
    articles = news_scraper.fetch_news(company_name)
    if not articles:
        return jsonify({"error": "No articles found"}), 404

    # 2) Perform sentiment analysis on each article
    #    (The pipeline returns a list of results like [{"label": "LABEL_2", "score": ...}, ...])
    for article in articles:
        summary_text = article.get('summary', '')
        # analyze_sentiment expects a list of strings
        sentiment_result = sentiment_analysis.analyze_sentiment([summary_text])
        if sentiment_result:
            # Store the first sentiment result in the article dict
            article['sentiment'] = sentiment_result[0]
        else:
            article['sentiment'] = {"label": "Unknown", "score": 0.0}

    return jsonify(articles), 200


@app.route('/convert_to_speech', methods=['POST'])
def convert_to_speech():
    """
    API endpoint to convert given text to Hindi speech.
    (Optional – if you want TTS done by the backend instead of Streamlit side)
    Expects a JSON body with {"text": "some text here"}
    Returns a JSON with a message and a path to the generated file.
    """
    data = request.get_json() or {}
    text = data.get('text', '')
    if not text:
        return jsonify({"error": "Text is required for speech conversion"}), 400

    file_path = text2speech.text_to_speech(text, lang='hi')
    return jsonify({"message": "Speech generated successfully", "file_path": file_path}), 200


if __name__ == '__main__':
    app.run(debug=True)
