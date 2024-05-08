from datetime import datetime, timedelta
import yfinance as yf

def fetchPrice(ticker_symbol, days):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    data = yf.download(ticker_symbol, start=start_date, end=end_date)
    return data
