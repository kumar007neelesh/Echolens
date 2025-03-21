# sentiment_analysis.py
from transformers import pipeline

# Load the pre-trained sentiment analysis pipeline.
# The cardiffnlp/twitter-roberta-base-sentiment model
# returns LABEL_0 (negative), LABEL_1 (neutral), LABEL_2 (positive)
sentiment_pipeline = pipeline(
    'sentiment-analysis', 
    model='cardiffnlp/twitter-roberta-base-sentiment'
)

def analyze_sentiment(texts):
    """
    Analyzes the sentiment of given texts.
    :param texts: List of strings to analyze.
    :return: List of dicts, e.g. [{"label": "LABEL_2", "score": 0.99}, ...]
    """
    if not texts:
        return []
    results = sentiment_pipeline(texts)
    return results
