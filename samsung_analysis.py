#!/usr/bin/env python3
"""
Samsung Electronics Stock Analysis
Downloads 1-year historical data and calculates moving averages
"""

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def download_stock_data(ticker, period="1y"):
    """Download stock data from Yahoo Finance"""
    print(f"Downloading data for {ticker}...")
    stock = yf.Ticker(ticker)
    df = stock.history(period=period)
    return df

def calculate_moving_averages(df):
    """Calculate 20-day and 50-day moving averages"""
    df['MA_20'] = df['Close'].rolling(window=20).mean()
    df['MA_50'] = df['Close'].rolling(window=50).mean()
    return df

def save_to_csv(df, filename):
    """Save dataframe to CSV file"""
    # Select relevant columns
    output_df = df[['Close', 'MA_20', 'MA_50']].copy()
    output_df.to_csv(filename)
    print(f"Data saved to {filename}")

def plot_chart(df, ticker, output_filename):
    """Create and save matplotlib chart"""
    plt.figure(figsize=(14, 7))

    # Plot closing price and moving averages
    plt.plot(df.index, df['Close'], label='Close Price', linewidth=2, color='#1f77b4')
    plt.plot(df.index, df['MA_20'], label='20-Day MA', linewidth=1.5, color='#ff7f0e', linestyle='--')
    plt.plot(df.index, df['MA_50'], label='50-Day MA', linewidth=1.5, color='#2ca02c', linestyle='--')

    plt.title(f'{ticker} - Stock Price with Moving Averages (1 Year)', fontsize=16, fontweight='bold')
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Price (KRW)', fontsize=12)
    plt.legend(loc='best', fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    plt.savefig(output_filename, dpi=300, bbox_inches='tight')
    print(f"Chart saved to {output_filename}")
    plt.close()

def main():
    # Configuration
    ticker = "005930.KS"  # Samsung Electronics
    csv_filename = "samsung_stock_data.csv"
    chart_filename = "samsung_stock_chart.png"

    # Download data
    df = download_stock_data(ticker, period="1y")

    # Calculate moving averages
    df = calculate_moving_averages(df)

    # Display summary statistics
    print("\n=== Summary Statistics ===")
    print(f"Data period: {df.index[0].date()} to {df.index[-1].date()}")
    print(f"Latest Close Price: {df['Close'].iloc[-1]:,.2f} KRW")
    print(f"Latest 20-Day MA: {df['MA_20'].iloc[-1]:,.2f} KRW")
    print(f"Latest 50-Day MA: {df['MA_50'].iloc[-1]:,.2f} KRW")
    print(f"1-Year High: {df['Close'].max():,.2f} KRW")
    print(f"1-Year Low: {df['Close'].min():,.2f} KRW")

    # Save to CSV
    save_to_csv(df, csv_filename)

    # Create chart
    plot_chart(df, ticker, chart_filename)

    print("\n✓ Analysis complete!")

if __name__ == "__main__":
    main()
