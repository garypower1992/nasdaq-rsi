import yfinance as yf
import pandas as pd
import pandas_ta as ta
import json
from datetime import datetime

# List of Nasdaq-100 tickers
tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA", "AVGO", "PEP",
           "COST", "ADBE", "NFLX", "AMD", "CMCSA", "INTC", "CSCO", "TMUS", "TXN",
           "AMAT", "INTU", "QCOM", "BKNG", "ISRG", "VRTX", "ADI", "MU", "REGN", "GILD",
           "PDD", "LRCX", "MDLZ", "ADP", "KDP", "ATVI", "PANW", "MELI", "MAR", "AEP",
           "CTAS", "CDNS", "ADSK", "CHTR", "KLAC", "CSGP", "FTNT", "ORLY", "ROST", "MNST",
           "NXPI", "IDXX", "WDAY", "BIIB", "ASML", "PAYX", "ODFL", "MRVL", "EXC", "PCAR",
           "FAST", "WBD", "XEL", "SIRI", "EA", "CTSH", "ILMN", "VRSK", "ZM", "ANSS", "SGEN",
           "TEAM", "CRWD", "TTD", "ZS", "DDOG", "OKTA", "MDB", "FANG", "CEG", "LCID", "BKR",
           "ABNB", "JD", "BIDU", "KHC", "LULU", "DLTR", "ALGN", "MTCH", "DOCU", "VERI",
           "RIVN", "PDD", "SPLK", "CHKP", "INCY", "CDW", "NXGN", "ZS", "CGEN"]

rsi_period = 14
output_path = "nasdaq_rsi.json"

def fetch_rsi(ticker):
    data = yf.download(ticker, period="21d", interval="1d")
    if data.empty:
        return None
    data['RSI'] = ta.rsi(data['Close'], length=rsi_period)
    latest_rsi = data['RSI'].dropna().iloc[-1]
    return {"ticker": ticker, "rsi": round(latest_rsi, 2)}

results = [fetch_rsi(ticker) for ticker in tickers if fetch_rsi(ticker)]

output = {
    "last_updated": datetime.utcnow().isoformat() + "Z",
    "data": results
}

with open(output_path, "w") as f:
    json.dump(output, f, indent=2)
