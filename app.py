import streamlit as st
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
import en_core_web_sm
from string import punctuation
from heapq import nlargest
import spacy_streamlit
import requests
import json
import random
from newspaper import Article

# Load spaCy model
nlp = en_core_web_sm.load()

# Stopwords and punctuation
stopwords = list(STOP_WORDS)
punctuation = punctuation + "\n"

# Load the configuration file
with open('config.json', 'r') as file:
    config = json.load(file)

# Access the API key
news_api_key = config.get("NEWS_API_KEY")

# Function to visualize Named Entity Recognition (NER) using spacy_streamlit
def spacy_rander(summary, text=None, unique_key=None):
    summ = nlp(summary)
    if text == "Yes":
        # Visualize the full article with NER
        rend = spacy_streamlit.visualize_ner(
            summ, labels=nlp.get_pipe("ner").labels, title="Full Article Visualization", 
            show_table=True, key=f"full_article_{unique_key}")  # Use unique key
    else:
        # Visualize the summary with NER
        rend = spacy_streamlit.visualize_ner(
            summ, labels=nlp.get_pipe("ner").labels, title="Summary Visualization", 
            show_table=True, key=f"summary_{unique_key}")  # Use unique key
    return rend

# Function to calculate word frequencies (used for sentence scoring)
def word_frequency(doc):
    word_frequencies = {}
    for word in doc:
        if word.text.lower() not in stopwords:
            if word.text.lower() not in punctuation:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1
    return word_frequencies

# Function to calculate sentence scores based on word frequencies
def sentence_score(sentence_tokens, word_frequencies):
    sentence_score = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_score.keys():
                    sentence_score[sent] = word_frequencies[word.text.lower()] 
                else:
                    sentence_score[sent] += word_frequencies[word.text.lower()]
    return sentence_score

# Function to fetch news links from NewsAPI based on query
@st.cache_data
def fetch_news_links(query):
    link_list = []
    title_list = []
    thumbnail_list = []

    # List of reliable sources
    sources = "bbc-news,cnn,bbc-sport,google-news,reuters,the-new-york-times,the-guardian,wired"

    if query == "":
        # Query with predefined reliable sources
        reqUrl = f"https://newsapi.org/v2/everything?sources={sources}&language=en&apiKey={news_api_key}"
    else:
        # Query for specific keyword (e.g., "sports") from the reliable sources
        reqUrl = f"https://newsapi.org/v2/everything?q={query}&sources={sources}&language=en&apiKey={news_api_key}"

    headersList = {
        "Accept": "*/*",
        "User-Agent": "Thunder Client (https://www.thunderclient.com)"
    }

    response = requests.request("GET", reqUrl, headers=headersList).text
    response_data = json.loads(response)

    # Check if "articles" is in the response
    if "articles" in response_data:
        for article in response_data["articles"]:
            if article.get("url"):
                link_list.append(article["url"])
                title_list.append(article["title"])
                thumbnail_list.append(article.get("urlToImage", ""))

    if not link_list:
        st.error(f"No articles found for the query '{query}'. Try using a different term or check your API key.")

    return link_list, title_list, thumbnail_list

# Function to fetch the full news articles based on links
@st.cache_data
def fetch_news(link_list):
    news_list = []

    for link in link_list:
        try:
            article = Article(link)
            article.download()
            article.parse()  # Parse the article
            news_list.append(article.text)  # Extracted text from the article
        except Exception as e:
            news_list.append(f"Error fetching article: {e}")

    return news_list

# Function to generate the summary of the given text
def get_summary(text):
    # Process the text with spaCy
    doc = nlp(text)

    # Check if the article is long enough to summarize
    if len(text.split()) < 50:
        return text  # Return the original text if it's very short

    # Generate word frequencies
    word_frequencies = word_frequency(doc)
    
    # Normalize word frequencies to range between 0 and 1
    max_freq = max(word_frequencies.values())
    if max_freq > 0:
        word_frequencies = {word: freq / max_freq for word, freq in word_frequencies.items()}

    # Tokenize sentences
    sentence_tokens = [sent for sent in doc.sents]

    # Calculate sentence scores based on word frequencies
    sentence_scores = sentence_score(sentence_tokens, word_frequencies)

    # Select top 20% of sentences based on their scores for longer articles
    select_length = int(len(sentence_tokens) * 0.25)  # Select top 25% of sentences for more comprehensive summary
    if select_length == 0:  # Handle edge case where no sentences are selected
        select_length = 1  # At least one sentence should be selected
    
    # Select the sentences with the highest scores
    selected_sentences = nlargest(select_length, sentence_scores, key=sentence_scores.get)
    
    # Join the selected sentences into a summary
    summary = [sent.text.strip() for sent in selected_sentences]
    summary = " ".join(summary)

    return summary

# Streamlit UI
# Apply custom CSS to set the background color to black
st.markdown(
    """
    <style>
    body {
        background-color: #121212;
        color: black;
    }
    .css-ffhzg2 {
        color: white;
    }
    .css-2trqyp {
        color: white;
    }
    .css-10trblm {
        color: white;
    }
    .css-2h1d69d {
        color: white;
    }
    .stButton>button {
        background-color: #000000;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# Title
st.title("📰 News Summarizer (Using NewsAPI and spaCy)")
st.write("Fetch and summarize the latest News articles using advanced NLP techniques.")

# Search query input for fetching news
query = st.text_input("Enter a topic to search (optional)", "")

# Fetch BBC news articles based on search query
link_list, title_list, thumbnail_list = fetch_news_links(query)
if title_list:
    selected_article = st.selectbox("Select an article to summarize", title_list)

    # Fetch the full article content
    article = fetch_news([link_list[title_list.index(selected_article)]])[0]

    # Display full article content
    st.subheader("Full Article")
    st.write(article)

    # Generate and display the summary
    summary = get_summary(article)
    st.subheader("Summary")
    st.success(summary)

    # Visualize the full article with NER
    spacy_rander(article, text="Yes", unique_key=random.randint(0, 100))

    # Visualize the summary with NER
    spacy_rander(summary, unique_key=random.randint(0, 100))

else:
    st.error("No articles found. Please try a different query or check your API key.")
