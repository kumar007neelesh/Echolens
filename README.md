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
   conda create --name myenv python=3.9 -y
   pip install -r requirements.txt
   ```
## Running Locally
```bash
   python api.py
   streamlit run app.py
```
## Deployment on Huggingface Space
### 1. Backend Deployment

1. **Create a new Hugging Face Space**  
   - Go to [Hugging Face Spaces](https://huggingface.co/spaces) and create a new Space.  
   - Select **“Blank”**, **“Docker”**, or **“Flask”** template, whichever suits your preference.

2. **Upload Your Backend Files**  
   - Typical backend files might include:
     - `api.py` (or `app.py`, if you renamed it to match Hugging Face’s entry-point expectations)
     - `news_scraper.py`
     - `sentiment_analysis.py`
     - `text2speech.py`
     - `requirements.txt`
   - Make sure you include all dependencies in `requirements.txt`.

3. **Set the Entrypoint**  
   - If you’re using a **Flask** template, rename `api.py` to `app.py` if needed.
   - At the bottom of your main file (`api.py` or `app.py`), ensure you have something like:
     ```python
     if __name__ == '__main__':
         app.run(host='0.0.0.0', port=7860)
     ```
     so the server can start on the expected port.

4. **Commit and Push**  
   - Once uploaded, commit your changes. 
   - Wait for the Space to build.  
   - The resulting URL might look like `https://<your-backend>.hf.space`.

5. **Test the Backend**  
   - Open your backend Space URL in the browser to ensure the server starts.
   - For example, if your backend has an endpoint `/fetch_articles`, you can visit:
     ```
     https://<your-backend>.hf.space/fetch_articles?company=Google
     ```
     and check if you receive JSON data.

---

### 2. Frontend Deployment

1. **Create another Hugging Face Space** for the **frontend**.  
   - This time, select **“Streamlit”** as the template.

2. **Upload Your Frontend Files**  
   - Common frontend files might include:
     - `app.py` (Streamlit code)
     - `requirements.txt`
   - Update `requirements.txt` to include everything you need for Streamlit (and any additional libraries used in `app.py`).

3. **Update Backend URL**  
   - In your frontend code (e.g., `app.py`), ensure you point to your newly created backend Space:
     ```python
     API_URL = "https://<your-backend>.hf.space"
     ```
     Replace `<your-backend>.hf.space` with your actual backend URL.

4. **Commit and Push**  
   - After uploading your code, commit and wait for the build.
   - The frontend Space URL might look like `https://<your-frontend>.hf.space`.

5. **Access Your Streamlit App**  
   - Open `https://<your-frontend>.hf.space` in your browser.
   - Enter a company name or perform any other actions to confirm your app is working correctly and fetching data from the backend.

---

### 3. Testing Your Deployment

After both Spaces have deployed successfully, verify they are communicating properly:

1. **Backend Check**  
   - Directly visit an endpoint (e.g., `https://<your-backend>.hf.space/fetch_articles?company=Netflix`) to see JSON output.

2. **Frontend Check**  
   - Go to `https://<your-frontend>.hf.space`.
   - Enter a company name (e.g., “Amazon”) and click **Fetch News**.  
   - Confirm the articles are displayed with sentiment.  
   - If you have text-to-speech, test that functionality too.

3. **Common Issues**  
   - **CORS or networking** issues: Make sure your backend doesn’t restrict cross-origin requests.  
   - **Mismatched URLs**: Ensure `API_URL` in your frontend is correct.  
   - **Requirements**: If your code fails to load or import certain libraries, verify `requirements.txt`.

---

**Congratulations!** You have now deployed both backend and frontend to Hugging Face Spaces. If you encounter any issues, check the Space logs or open an issue on your repository.

