import yfinance as yf
import pandas as pd
import pandas_ta as ta
import json
import requests
from bs4 import BeautifulSoup

# Function to get the list of tickers from the Nasdaq-100 Wikipedia page
def get_nasdaq_100_tickers():
    url = "https://en.wikipedia.org/wiki/NASDAQ-100"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Find the table that contains the tickers
    table = soup.find_all("table", {"class": "wikitable"})[3]
    
    # Extract tickers from the table
    tickers = []
    for row in table.find_all("tr")[1:]:
        cells = row.find_all("td")
        if len(cells) > 1:
            ticker = cells[1].get_text(strip=True)
            tickers.append(ticker)
    
    return tickers

# Fetch RSI for a given ticker
def fetch_rsi(ticker):
    try:
        # Download the stock data
        data = yf.download(ticker, period="1y", interval="15m")  # 1-year of 15-minute data
        
        if data.empty:
            print(f"No data for {ticker}")
            return None

        # Calculate RSI using pandas_ta
        data['RSI'] = ta.rsi(data['Close'], length=14)
        
        # Check if RSI is valid and return the last value
        if 'RSI' in data and not data['RSI'].isnull().all():
            latest_rsi = data['RSI'].dropna().iloc[-1]
            return {"ticker": ticker, "rsi": latest_rsi}
        else:
            print(f"RSI not available for {ticker}")
            return None
    except Exception as e:
        print(f"Error fetching RSI for {ticker}: {e}")
        return None

# Get the list of Nasdaq-100 tickers
tickers = get_nasdaq_100_tickers()

# Store the results for all tickers
results = [fetch_rsi(ticker) for ticker in tickers if fetch_rsi(ticker)]

# Filter out None results
results = [result for result in results if result is not None]

# Save the results to a JSON file
output_path = "nasdaq_rsi.json"
with open(output_path, "w") as f:
    json.dump(results, f, indent=2)

print(f"RSI data saved to {output_path}")

