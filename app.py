# app.py (frontend)
import streamlit as st
import requests
import os
import tempfile
import pandas as pd

# Optional: if you want TTS done locally in the frontend:
from text2speech import text_to_speech  

# Replace with the public URL of your backend on Hugging Face
# e.g. "https://your-username-your-backend.hf.space"
API_URL = "https://neeleshk21-echolens-backend.hf.space"  # For local testing, or update to your actual backend URL

def fetch_articles(company_name):
    """
    Calls the backend's /fetch_articles endpoint to retrieve news articles.
    """
    try:
        response = requests.get(f"{API_URL}/fetch_articles", params={'company': company_name})
        response.raise_for_status()
        return response.json()  # Should be a list of articles
    except requests.RequestException as e:
        st.error(f"Failed to retrieve articles: {e}")
        return []

def text_to_audio_file(text, index):
    """
    Perform text-to-speech locally in the Streamlit app. 
    If you want TTS in the backend, remove this and call the backend's /convert_to_speech.
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
        file_path = temp_file.name
        text_to_speech(
            text=text,
            file_name=file_path,
            lang='hi'
        )
    return file_path

def comparative_analysis(articles):
    if not articles:
        st.warning("No articles available for comparative analysis.")
        return None

    data = []
    for article in articles:
        title = article.get("title", "N/A")
        summary = article.get("summary", "N/A")
        topics = ", ".join(article.get("topics", []))
        
        # The backend returns e.g. {"label": "LABEL_2", "score": 0.99}
        sentiment = article.get("sentiment", {})
        label = sentiment.get("label", "Unknown")  # 'LABEL_0', 'LABEL_1', 'LABEL_2'
        # Optionally map them to Negative/Neutral/Positive if you like:
        sentiment_map = {"LABEL_0": "Negative", "LABEL_1": "Neutral", "LABEL_2": "Positive"}
        sentiment_str = sentiment_map.get(label, "Unknown")

        data.append({
            "Title": title,
            "Summary": summary,
            "Topics": topics,
            "Sentiment": sentiment_str
        })

    df = pd.DataFrame(data)
    st.subheader("Comparative Analysis of News Coverage")
    st.write(df)

    st.write("### Insights:")
    sentiments = df["Sentiment"].value_counts()
    st.write(f"Sentiment Distribution: {sentiments.to_dict()}")
    unique_topics = df["Topics"].unique()
    st.write(f"Unique Topics Covered: {unique_topics}")
    return df

def main():
    st.markdown("""
    <h1 style='text-align: center; font-size: 60px; margin-bottom: -20px;'>EchoLens</h1>
    <h3 style='text-align: center; font-size: 20px; color: gray;'>News Insights You Can Hear</h3>
    <hr style='margin: 20px 0;'>
    """, unsafe_allow_html=True)
    
    if "articles" not in st.session_state:
        st.session_state.articles = []
    if "audio_files" not in st.session_state:
        st.session_state.audio_files = {}

    company_name = st.text_input("Enter the company name:")

    if st.button("Fetch News"):
        st.session_state.articles = fetch_articles(company_name)
        st.session_state.audio_files.clear()

    # Display each article
    for index, article in enumerate(st.session_state.articles):
        st.subheader(article.get("title", "No Title"))
        st.write("**Summary:**", article.get("summary", "No Summary"))
        topics = article.get("topics", [])
        st.write("**Topic(s):**", ", ".join(topics))

        # Sentiment label
        sentiment = article.get("sentiment", {})
        label = sentiment.get("label", "Unknown")
        sentiment_map = {"LABEL_0": "Negative", "LABEL_1": "Neutral", "LABEL_2": "Positive"}
        sentiment_label = sentiment_map.get(label, "Unknown sentiment")
        st.write("**Sentiment:**", sentiment_label)

        # Button to convert to speech (locally)
        if st.button("Convert to Speech", key=f"convert-btn-{index}"):
            audio_file_path = text_to_audio_file(article["summary"], index)
            st.session_state.audio_files[index] = audio_file_path
            with open(audio_file_path, "rb") as audio_file:
                audio_bytes = audio_file.read()
            st.audio(audio_bytes, format="audio/mp3")

    # Button to do comparative analysis
    if st.button("Perform Comparative Analysis"):
        comparative_analysis(st.session_state.articles)

if __name__ == "__main__":
    main()
