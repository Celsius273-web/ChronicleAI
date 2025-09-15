ChronicleAI 

ChronicleAI is a smart news bot that scrapes articles from RSS feeds, processes them into searchable chunks, and uses AI to answer your questions based on current news. Think of it as your personal news research assistant that can pull insights from multiple sources and give you comprehensive, up-to-date answers. The idea is to make current events research faster and smarter for anyone who needs it.

How it works:

Ingests news articles from RSS feeds (BBC, Reuters, NPR, etc.)

Processes them into searchable chunks using vector embeddings

Answers your questions by finding relevant chunks and synthesizing responses with AI

When you ask a question, ChronicleAI searches through all the news content, finds the most relevant pieces, summarizes them, and then uses Google’s Gemini AI to give you a detailed answer.

What each file does:

config.yaml — all the RSS feed URLs

ingest.py — downloads and parses articles

process.py — breaks articles into chunks and creates vector embeddings

main.py — the main interface where you interact with the bot

requirements.txt — dependencies

Setup:
Clone the repo and install dependencies in a Python 3.11 or 3.12 environment.
git clone https://github.com/Celsius273-web/ChronicleAI

pip install -r requirements.txt

LLM setup: the project uses Google’s Gemini API by default, but you can swap in other API keys or even local models.

Get a Google AI API key and add it to a .env file as MY_KEY=your_api_key_here

Install Playwright browsers with: playwright install

Create a data/ folder in your project directory

Run:
python main.py

p — ask the bot a question about current news

n — refresh the news sources (scrape new articles)

any other key — quit

A few notes:

ChronicleAI maintains session memory to give context-aware answers

Articles are scraped once only (no duplicates)

The vector search finds the 5 most relevant chunks per question (adjustable)

Summaries are created before sending to the main AI to reduce API costs


Customization options:

RSS feeds: edit config.yaml to add or remove feeds.

Chunking: in process.py you can adjust chunk size (600 chars by default), overlap (100 chars), and separators.

RSS feeds: these are publicly available feeds from BBC, Reuters, NPR, etc. Fine for personal use, but CHECK each outlet’s terms of service for commercial use.

Summarization: You can alter or the summarization as needed, I simply wanted to reduce API usage.


Troubleshooting:

Check your API key or local model setup

Make sure the data/ folder exists

Some feeds may be temporarily down

If Playwright fails, try playwright install again


License: MIT License
