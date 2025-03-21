# news_scraper.py
import requests
import re

TOPIC_KEYWORDS = {
    'Finance': ['finance', 'stock', 'investment', 'market', 'bank', 'economy', 'profit', 'revenue', 'earnings'],
    'Technology': ['technology', 'tech', 'software', 'hardware', 'AI', 'machine learning', 'innovation', 'gadget'],
    'Science': ['science', 'research', 'study', 'discovery', 'biology', 'physics', 'chemistry'],
    'Healthcare': ['healthcare', 'medicine', 'medical', 'health', 'pharma', 'hospital'],
    'Energy': ['energy', 'oil', 'gas', 'renewable', 'solar', 'wind'],
    'Entertainment': ['entertainment', 'movie', 'music', 'streaming', 'tv'],
    'Automotive': ['automotive', 'car', 'vehicle', 'electric vehicle', 'EV'],
}

def identify_topics(text):
    """Identify topics from text based on predefined keywords."""
    text_lower = text.lower()
    identified_topics = set()
    for topic, keywords in TOPIC_KEYWORDS.items():
        for keyword in keywords:
            if re.search(r'\b' + re.escape(keyword.lower()) + r'\b', text_lower):
                identified_topics.add(topic)
                break
    return list(identified_topics) if identified_topics else ["General"]

def fetch_news(company_name, num_articles=15):
    
    api_key = "35754d0ba3fd47a88aa5aedd63dd57bb"
    url = f"https://newsapi.org/v2/everything?q={company_name}&pageSize={num_articles}&apiKey={api_key}"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to fetch news: HTTP {response.status_code}")
        return []

    data = response.json()
    articles = data.get("articles", [])
    
    results = []
    for article in articles[:num_articles]:
        title = article.get("title") or "No Title"
        summary = article.get("description") or "No Description"
        combined_text = f"{title} {summary}"
        topics = identify_topics(combined_text)

        results.append({
            "title": title,
            "summary": summary,
            "topics": topics,
        })
    
    return results
