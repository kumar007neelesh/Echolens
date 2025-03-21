# test_sentiment_analysis.py
import pytest
from sentiment_analysis import analyze_sentiment

def test_analyze_sentiment():
    texts = ["good product", "bad service"]
    results = analyze_sentiment(texts)
    print(results)
    assert len(results) == 2
    # Update this line to include the correct labels:
    assert results[0]['label'] in ['LABEL_0', 'LABEL_1', 'LABEL_2']
    assert results[1]['label'] in ['LABEL_0', 'LABEL_1', 'LABEL_2']
