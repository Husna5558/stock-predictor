import yfinance as yf
import pandas as pd
import numpy as np
import datetime
import time
stocks = [
    # US Tech
    'AAPL', 'MSFT', 'GOOG', 'AMZN', 'META', 'TSLA', 'NVDA', 'NFLX', 'AMD', 'INTC',
    'ADBE', 'CRM', 'ORCL', 'CSCO', 'QCOM', 'AVGO', 'TXN', 'IBM', 'MU', 'NOW',
    # US Finance
    'JPM', 'BAC', 'C', 'GS', 'MS', 'WFC', 'BLK', 'AXP', 'SCHW', 'PNC',
    'USB', 'TFC', 'COF', 'BK', 'AIG', 'CB', 'MMC', 'MET', 'PRU', 'TRV',
    # US Energy
    'XOM', 'CVX', 'COP', 'PSX', 'MPC', 'OXY', 'VLO', 'HAL', 'SLB', 'KMI',
    'EOG', 'PXD', 'DVN', 'APA', 'BKR', 'HES', 'MRO', 'FANG', 'OKE', 'WMB',
    # US Healthcare
    'JNJ', 'PFE', 'MRK', 'ABT', 'TMO', 'DHR', 'BMY', 'AMGN', 'GILD', 'LLY',
    'CVS', 'CI', 'UNH', 'HCA', 'ISRG', 'MDT', 'SYK', 'REGN', 'VRTX', 'BSX',
    # US Consumer & Retail
    'PG', 'KO', 'PEP', 'WMT', 'COST', 'HD', 'LOW', 'TGT', 'MCD', 'SBUX',
    'NKE', 'DIS', 'CMG', 'BKNG', 'MAR', 'EBAY', 'ROST', 'TJX', 'DG', 'DLTR',
    # US Industrials
    'CAT', 'BA', 'GE', 'HON', 'UPS', 'FDX', 'LMT', 'NOC', 'RTX', 'DE',
    'EMR', 'ETN', 'GD', 'CMI', 'MMM', 'PCAR', 'PH', 'DOV', 'ITW', 'AME',
    # US Utilities & REITs
    'NEE', 'DUK', 'SO', 'AEP', 'D', 'EXC', 'SRE', 'PEG', 'ED', 'XEL',
    'PLD', 'AMT', 'CCI', 'SPG', 'O', 'EQIX', 'PSA', 'WELL', 'VTR', 'DLR',
    # Indian IT & Finance
    'TCS.NS', 'INFY.NS', 'WIPRO.NS', 'TECHM.NS', 'HCLTECH.NS', 'LTIM.NS', 'MPHASIS.NS', 'COFORGE.NS', 'LTTS.NS', 'PERSISTENT.NS',
    'HDFCBANK.NS', 'ICICIBANK.NS', 'KOTAKBANK.NS', 'AXISBANK.NS', 'SBIN.NS', 'PNB.NS', 'BANKBARODA.NS', 'FEDERALBNK.NS', 'IDFCFIRSTB.NS', 'INDUSINDBK.NS',
    # Indian Energy & Infra
    'RELIANCE.NS', 'ONGC.NS', 'BPCL.NS', 'IOC.NS', 'GAIL.NS', 'NTPC.NS', 'POWERGRID.NS', 'TATAPOWER.NS', 'ADANIGREEN.NS', 'ADANITRANS.NS',
    'ADANIPORTS.NS', 'LT.NS', 'ULTRACEMCO.NS', 'SHREECEM.NS', 'AMBUJACEM.NS', 'JSWSTEEL.NS', 'TATASTEEL.NS', 'HINDALCO.NS', 'COALINDIA.NS', 'VEDL.NS',
    # Indian Consumer & Auto
    'ITC.NS', 'HINDUNILVR.NS', 'BRITANNIA.NS', 'NESTLEIND.NS', 'MARICO.NS', 'GODREJCP.NS', 'DABUR.NS', 'COLPAL.NS', 'TITAN.NS', 'PAGEIND.NS',
    'MARUTI.NS', 'TATAMOTORS.NS', 'M&M.NS', 'BAJAJ-AUTO.NS', 'HEROMOTOCO.NS', 'EICHERMOT.NS', 'TVSMOTOR.NS', 'ASHOKLEY.NS', 'BOSCHLTD.NS', 'MRF.NS'
]
print(f"Total tickers loaded: {len(stocks)}")
print("Fetching historical data...")
hist = yf.download(stocks, period='6d', interval='1d', progress=False)
predictions = {}
for stock in stocks:
    try:
        last_5 = hist['Close'][stock].iloc[-6:-1].values
        today_open = hist['Open'][stock].iloc[-1]
        avg_last_5 = np.mean(last_5)
        direction = "UP" if today_open < avg_last_5 else "DOWN"
        predictions[stock] = {
            'predicted': direction,
            'open': today_open,
            'avg_last_5': avg_last_5
        }
    except Exception as e:
        print(f"Skipping {stock}: {e}")

print("\nPredictions made for the day:")
for s, d in predictions.items():
    print(f"{s}: Predicted {d['predicted']} (Open={d['open']:.2f}, 5-day avg={d['avg_last_5']:.2f})")
print("\nWaiting until market close... (simulating 10 seconds for demo)")
time.sleep(10)
print("Fetching today's closing prices...")
closing_data = yf.download(stocks, period='1d', interval='1d', progress=False)
closing_prices = closing_data['Close'].iloc[-1]
correct = 0
total = 0
results = []
for stock in predictions:
    try:
        open_price = predictions[stock]['open']
        close_price = closing_prices[stock]
        predicted = predictions[stock]['predicted']
        actual = "UP" if close_price > open_price else "DOWN"
        is_correct = (predicted == actual)
        results.append([stock, open_price, close_price, predicted, actual, "✅" if is_correct else "❌"])
        total += 1
        if is_correct:
            correct += 1
    except:
        continue
accuracy = (correct / total) * 100 if total > 0 else 0
df = pd.DataFrame(results, columns=["Stock", "Open", "Close", "Predicted", "Actual", "Result"])
print("\nFinal Prediction Report:")
print(df)
print(f"\nOverall Prediction Accuracy: {accuracy:.2f}%")
