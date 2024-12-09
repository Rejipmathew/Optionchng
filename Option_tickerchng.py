import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

def main():
    st.title("Option Stock Ticker with Most Change")

    # Get list of stock tickers with default values
    tickers_input = st.text_input(
        "Enter stock tickers separated by commas (e.g., AAPL, MSFT, GOOG):",
        value="TSLA,AAPL,MSFT,NVDA,GOOG,AMZN,PLTR",
    )
    tickers = [ticker.strip() for ticker in tickers_input.split(",")]

    # Get options expiry dates for the first ticker (assuming all have similar expiry dates)
    try:
        stock = yf.Ticker(tickers[0])
        options_dates = stock.options
    except Exception as e:
        st.error(f"Error fetching options dates for {tickers[0]}: {e}")
        return

    # Expiry Date Input as dropdown
    expiry_date = st.selectbox("Select options expiry date:", options_dates)

    # Get options data for each ticker
    options_data = {}
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            options = stock.option_chain(expiry_date)
            options_data[ticker] = options
        except Exception as e:
            st.error(f"Error fetching data for {ticker}: {e}")

    # Create different pages for each ticker
    if options_data:
        for ticker, option_chain in options_data.items():
            with st.expander(f"{ticker} ({expiry_date})"):  # Use expander for each ticker
                for option_type in ["calls", "puts"]:
                    df = getattr(option_chain, option_type)
                    df["percentChange"] = df["percentChange"].abs()

                    fig = px.scatter(
                        df,
                        x="strike",
                        y="percentChange",
                        color="volume",
                        size="openInterest",
                        hover_data=["contractSymbol", "lastPrice", "bid", "ask", "change", "percentChange"],
                        title=f"{ticker} {option_type.upper()} - Percent Change vs Strike",
                        labels={"strike": "Strike Price", "percentChange": "Percent Change (%)", "volume": "Volume", "openInterest": "Open Interest"},
                    )
                    st.plotly_chart(fig)
    else:
        st.warning("No valid options data found for the given tickers.")

if __name__ == "__main__":
    main()