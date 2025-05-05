# filename: stock_analysis.py

import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime

# Step 1: Fetch stock data for "Hey"
# Assuming the ticker symbol is "HEY" (please replace if it's different)
ticker = "HEY"
stock = yf.Ticker(ticker)

# Get historical data for the past year
historical_data = stock.history(period="1y")

# Step 2: Calculate Price Changes
current_price = historical_data["Close"][-1]
one_month_data = historical_data.tail(21)  # Approx. 21 trading days in a month
three_months_data = historical_data.tail(63)  # Approx. 63 trading days in 3 months
ytd_data = historical_data[historical_data.index.year == datetime.now().year]
one_year_data = historical_data

# Calculate percent changes
one_month_change = (
    (current_price - one_month_data["Close"].iloc[0]) / one_month_data["Close"].iloc[0]
) * 100
three_months_change = (
    (current_price - three_months_data["Close"].iloc[0])
    / three_months_data["Close"].iloc[0]
) * 100
ytd_change = (
    (current_price - ytd_data["Close"].iloc[0]) / ytd_data["Close"].iloc[0]
) * 100
one_year_change = (
    (current_price - one_year_data["Close"].iloc[0]) / one_year_data["Close"].iloc[0]
) * 100

# Output the changes
print(f"1 Month Change: {one_month_change:.2f}%")
print(f"3 Months Change: {three_months_change:.2f}%")
print(f"YTD Change: {ytd_change:.2f}%")
print(f"1 Year Change: {one_year_change:.2f}%")

# Step 3: Plot the 1-year stock price change graph
plt.figure(figsize=(10, 5))
plt.plot(
    one_year_data.index,
    one_year_data["Close"],
    label=f"1-Year Price Change for {ticker}",
)
plt.xlabel("Date")
plt.ylabel("Price (USD)")
plt.title("1-Year Stock Price Change")
plt.legend()
plt.grid(True)

# Step 4: Save the Plot
plt.savefig("stock_price_change.png")
plt.show()
