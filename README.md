# 📰 News Summarizer & Entity Context Viewer

Fetch the latest news articles, generate smart summaries, and interactively explore entities with context using **spaCy**, **Streamlit**, and **NewsAPI**.

---

## ✨ Features
- 🔎 **Search and Fetch News** from top sources like BBC, CNN, Reuters using **NewsAPI**.
- 📝 **Automatic Summarization** using custom NLP techniques.
- 🧠 **Named Entity Recognition (NER)** visualization using **spaCy**.
- 📋 **Entity Table**: View and **download extracted entities** as a table (CSV export available).
- 🎯 **Clickable Entity Labels**: View all sentences where an entity appears by selecting a label.
- 📚 **Full and Summary NER Visualization**.
- ⚡ **Optimized User Experience**: Single point selection — no repetitive dropdowns or clutter.


---

## 🛠 Tech Stack
- [Streamlit](https://streamlit.io/) — for fast UI building
- [spaCy](https://spacy.io/) — for NLP tasks (NER, tokenization, sentence segmentation)
- [NewsAPI](https://newsapi.org/) — for fetching real-world news
- [newspaper3k](https://github.com/codelucas/newspaper) — for article scraping
- Python libraries — `requests`, `heapq`, `json`, etc.

---

## 🚀 Quick Setup Instructions

1. **Clone this repo**:
    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Add your `config.json`**:
    Create a file named `config.json` inside the root folder:
    ```json
    {
      "NEWS_API_KEY": "your_newsapi_key_here"
    }
    ```

4. **Run the app**:
    ```bash
    streamlit run app.py
    ```

---

## 📸 Demo 


> 🎥 Also check the [Demo Video](#) for a full walkthrough!

---

## ⚡ How It Works

- 🔍 Enter a keyword or leave empty to fetch trending news.
- 📑 Select an article to read full content and summarized version.
- 🧠 Entity Labels (like PERSON, DATE, GPE) are extracted automatically.
- 📋 View extracted entities in a table and **download** them as CSV.
- 👆 **Click any Entity Label** to view exactly where it's mentioned — seamless experience.
- 🎯 Smooth experience by combining **NER visualization** and **context browsing** in one view.


