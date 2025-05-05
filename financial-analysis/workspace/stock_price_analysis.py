# filename: stock_price_analysis.py

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Define the stock ticker and time range
ticker = "NVDA"
end_date = datetime.today()
start_date = end_date - timedelta(days=365)

# Download the stock data
stock_data = yf.download(ticker, start=start_date, end=end_date)

# Convert index to datetime
stock_data.index = pd.to_datetime(stock_data.index)

# Ensure the stock data is not empty
if not stock_data.empty:
    # Calculate the price changes (using iloc for proper indexing)
    latest_close = stock_data["Close"].iloc[-1]
    first_close = stock_data["Close"].iloc[0]

    one_year_change = ((latest_close - first_close) / first_close) * 100

    monthly_close = stock_data["Close"].iloc[-min(30, len(stock_data))]
    monthly_change = ((latest_close - monthly_close) / monthly_close) * 100

    three_month_close = stock_data["Close"].iloc[-min(90, len(stock_data))]
    three_month_change = ((latest_close - three_month_close) / three_month_close) * 100

    # Get the first trading day of the year for YTD calculation
    first_trading_day_of_year = stock_data.index.get_loc(
        datetime(end_date.year, 1, 1), method="bfill"
    )
    ytd_close = stock_data["Close"].iloc[first_trading_day_of_year]
    ytd_change = ((latest_close - ytd_close) / ytd_close) * 100

    # Print the percentage changes
    print(f"Monthly Change: {monthly_change:.2f}%")
    print(f"3 Months Change: {three_month_change:.2f}%")
    print(f"Year-to-Date (YTD) Change: {ytd_change:.2f}%")
    print(f"One-Year Change: {one_year_change:.2f}%")

    # Plot the 1-year stock price change
    plt.figure(figsize=(10, 5))
    plt.plot(stock_data["Close"], label="Closing Price")
    plt.title("Nvidia 1-Year Stock Price Change")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.legend()
    plt.grid(True)

    # Save the plot
    plt.savefig("stock_price_change.png")
    plt.show()
else:
    print("No stock data available to perform analysis.")
