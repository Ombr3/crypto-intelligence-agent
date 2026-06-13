# 🤖 Crypto Intelligence Agent

An AI-powered research assistant that analyses cryptocurrencies by combining
live market data with retrieved knowledge and LLM reasoning to produce
structured research reports.

## Architecture

```
User Input (coin ticker)
        │
        ▼
Crypto Intelligence Agent
        │
   ┌────┴─────┬──────────┐
   ▼          ▼          ▼
Binance API  RAG DB   News API
(funding     (vector  (recent
rate, OI,    search)  headlines)
price)
   └────┬─────┴──────────┘
        ▼
 Context Assembly
        ▼
    LLM Prompt
  (Claude Sonnet)
        ▼
 Structured Report
        ▼
  Streamlit UI
```

## Features

- 📈 **Live market data** — funding rate, open interest, mark price via Binance API
- 📰 **Recent news** — top headlines via NewsAPI
- 📚 **RAG pipeline** — retrieves relevant context from your own research documents
- 🤖 **LLM analysis** — Claude generates a structured report with bullish/bearish factors
- ⚠️ **Error handling** — graceful messages for API failures, low credits, bad input

## Supported Coins

BTC, ETH, SOL, BNB (easily extendable)

## Tech Stack

- Python 3.11
- Anthropic Claude API (claude-sonnet-4-6)
- ChromaDB (vector store)
- Binance Futures API (public endpoints)
- NewsAPI
- Streamlit

## Setup

1. Clone the repo

2. Install dependencies:
```
uv venv
uv add requests python-dotenv streamlit anthropic chromadb sentence-transformers
```

3. Create a `.env` file:
```
ANTHROPIC_API_KEY=your_key
NEWS_API_KEY=your_key
```

4. Add research documents (`.txt` or `.pdf`) to the `data/` folder

5. Run:
```
streamlit run app.py
```

## Project Structure

```
crypto-agent/
├── app.py              # Streamlit UI
├── agent.py            # Main orchestration logic
├── binance_client.py   # Binance API integration
├── news_client.py      # NewsAPI integration
├── rag.py              # Vector store + retrieval pipeline
├── data/               # Your research documents go here
└── .env                # API keys (not committed)
```
