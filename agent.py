import anthropic
import os
from dotenv import load_dotenv
from binance_client import get_funding_rate, get_open_interest, get_price
from news_client import get_news
from rag import retrieve

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

COIN_TO_SYMBOL = {
    "BTC": "BTCUSDT",
    "ETH": "ETHUSDT",
    "SOL": "SOLUSDT",
    "BNB": "BNBUSDT",
}

COIN_TO_NAME = {
    "BTC": "Bitcoin",
    "ETH": "Ethereum",
    "SOL": "Solana",
    "BNB": "Binance Coin",
}

def analyse(coin: str) -> dict:
    """Run the full agent pipeline for a given coin ticker e.g. 'ETH'"""
    # Normalise input — handle full names and lowercase
    NAME_TO_TICKER = {
        "bitcoin": "BTC",
        "ethereum": "ETH",
        "solana": "SOL",
        "bnb": "BNB",
        "binance coin": "BNB",
    }
    coin = coin.upper().strip()
    coin = NAME_TO_TICKER.get(coin.lower(), coin)
    symbol = COIN_TO_SYMBOL.get(coin)
    name = COIN_TO_NAME.get(coin, coin)

    if not symbol:
        return {"error": f"Unsupported coin: {coin}. Supported: {list(COIN_TO_SYMBOL.keys())}"}

    # Step 1: Fetch live market data
    funding = get_funding_rate(symbol)
    oi = get_open_interest(symbol)
    price = get_price(symbol)

    # Step 2: Fetch news
    articles = get_news(name, max_articles=5)
    news_text = "\n".join([f"- [{a['source']}] {a['title']}" for a in articles])

    # Step 3: Retrieve relevant knowledge
    knowledge_chunks = retrieve(f"{name} crypto analysis", n_results=3)
    knowledge_text = "\n".join([f"- {chunk}" for chunk in knowledge_chunks])

    # Step 4: Assemble prompt
    prompt = f"""You are a professional crypto analyst. Analyse {name} ({coin}) using the data below and produce a structured research report.

## Live Market Data
- Mark Price: ${price['mark_price']:,.4f}
- Funding Rate: {funding['funding_rate']:.4f}%
- Open Interest: {oi['open_interest']:,.2f} contracts

## Recent News
{news_text}

## Retrieved Knowledge (from research documents)
{knowledge_text}

## Instructions
Produce a concise research report with exactly these sections:
1. Summary (2-3 sentences)
2. Risks
3. Bullish Factors
4. Bearish Factors
5. Conclusion (1-2 sentences with a directional bias: Bullish / Neutral / Bearish)

Be specific. Reference the actual numbers from the market data. Keep each section to 2-4 bullet points."""

   # Step 5: Call LLM
    try:
        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        report_text = message.content[0].text
    except anthropic.BadRequestError as e:
        if "credit balance is too low" in str(e):
            return {"error": "Anthropic API credit balance is too low. Please top up at https://console.anthropic.com/settings/billing"}
        raise
    except anthropic.APIConnectionError:
        return {"error": "Could not connect to Anthropic API. Please check your internet connection."}
    except anthropic.AuthenticationError:
        return {"error": "Invalid Anthropic API key. Please check your .env file."}

    return {
        "coin": coin,
        "name": name,
        "mark_price": price["mark_price"],
        "funding_rate": funding["funding_rate"],
        "open_interest": oi["open_interest"],
        "news": articles,
        "knowledge": knowledge_chunks,
        "report": report_text
    }

if __name__ == "__main__":
    result = analyse("eth")
    if "error" in result:
        print(result["error"])
    else:
        print(f"\n{'='*50}")
        print(f"ANALYSIS: {result['name']} ({result['coin']})")
        print(f"{'='*50}")
        print(f"Price: ${result['mark_price']:,.4f}")
        print(f"Funding Rate: {result['funding_rate']:.4f}%")
        print(f"Open Interest: {result['open_interest']:,.2f}")
        print(f"\n--- REPORT ---\n")
        print(result["report"])
