# EchoLens

**EchoLens** is a project that:
1. Fetches recent news articles for a given company using [NewsAPI](https://newsapi.org/).
2. Performs sentiment analysis on those articles using a pre-trained Transformer model.
3. Converts English summaries to Hindi audio using Google Translate and gTTS.
4. Displays the results in a Streamlit web interface.

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Repository Contents](#repository-contents)
3. [How It Works](#how-it-works)
4. [Prerequisites](#prerequisites)
5. [Installation Guide](#installation-guide)
6. [Running Locally](#running-locally)
7. [Step-by-Step Usage](#step-by-step-usage)
8. [Deploying to Hugging Face Spaces](#deploying-to-hugging-face-spaces)
   - [Backend Deployment](#1-backend-deployment)
   - [Frontend Deployment](#2-frontend-deployment)
   - [Testing Your Deployment](#testing-your-deployment)
9. [Local Testing Procedures](#local-testing-procedures)
10. [Example Hugging Face Deployments](#example-hugging-face-deployments)
11. [Additional Notes](#additional-notes)
12. [License](#license)

---

## Project Overview

- **Goal**: Provide a simple pipeline to scrape and analyze news articles, determine their sentiment, and optionally convert the article summaries into Hindi audio.
- **Components**:
  - **Flask API** for backend tasks like scraping and sentiment analysis.
  - **Streamlit** app for a user-friendly frontend.
  - **Text-to-speech** functionality using Google Translate and gTTS.
- **Key Technologies**: Python, Flask, Streamlit, Transformers, NewsAPI, gTTS, Google Translate.

---

## Repository Contents

1. **`api.py`**  
   - **Flask** backend providing two main endpoints:
     - **`/fetch_articles`**: Takes a company name and returns scraped articles with sentiment analysis.
     - **`/convert_to_speech`**: Accepts text (JSON) and returns the path to a generated Hindi audio file.

2. **`app.py`**  
   - **Streamlit** frontend:
     - Allows user input of a company name.
     - Fetches corresponding articles from the Flask backend.
     - Displays article summaries, topics, and sentiment labels.
     - Offers local text-to-speech generation (by default).
     - Performs a comparative analysis of all fetched articles.

3. **`news_scraper.py`**  
   - Fetches news from the [NewsAPI](https://newsapi.org/) based on a search query (company name).
   - Identifies major topics (Finance, Technology, Healthcare, etc.) using keyword matching.

4. **`sentiment_analysis.py`**  
   - Uses the [`cardiffnlp/twitter-roberta-base-sentiment`](https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment) model to generate sentiment labels:
     - `LABEL_0`: Negative
     - `LABEL_1`: Neutral
     - `LABEL_2`: Positive

5. **`text2speech.py`**  
   - Translates English text to Hindi (using `googletrans`).
   - Converts Hindi text to speech and saves it as an MP3 file using `gTTS`.

6. **`requirements.txt`**  
   - Lists all the required Python dependencies.

---

## How It Works

1. **User enters a company name** in the **Streamlit** interface (`app.py`).
2. **Streamlit** sends a GET request to the Flask backend’s `/fetch_articles` endpoint with the company name as a parameter.
3. **Flask** uses `news_scraper.py` to fetch up to 15 news articles from **NewsAPI**.
4. **Flask** uses `sentiment_analysis.py` to analyze each article’s summary.
5. **Flask** returns the processed data (article title, summary, sentiment label, identified topics) back to **Streamlit**.
6. **Streamlit** displays each article, showing summary, sentiment, and topic. The user can click **“Convert to Speech”** to convert the summary to Hindi audio.

---

## Prerequisites

1. **Python 3.7+** (recommended Python 3.9 or later).
2. **[NewsAPI key](https://newsapi.org/)**: You need a valid API key to fetch news articles. Insert it in `news_scraper.py`.

---

## Installation Guide

1. **Clone or Download** this repository:
   ```bash
   git clone https://github.com/kumar00neelesh/echolens.git
   cd echolens
