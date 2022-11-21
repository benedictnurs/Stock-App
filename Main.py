import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import yfinance as yf
import datetime as dt
from yahoo_fin import stock_info as si
 

snp_500 = pd.DataFrame( si.tickers_sp500() )
nasdaq = pd.DataFrame( si.tickers_nasdaq() )
dow = pd.DataFrame( si.tickers_dow() )
other = pd.DataFrame( si.tickers_other() )


with st.sidebar:
    st.sidebar.market_select = st.selectbox('Pick a Market',("S&P 500", "NASDAQ", "Dow Jones", "Other"))
    if st.sidebar.market_select == "S&P 500":
        market = snp_500
    elif st.sidebar.market_select == "NASDAQ":
        market = nasdaq
    elif st.sidebar.market_select == "Dow Jones":
        market = dow
    elif st.sidebar.market_select == "Other":
        market = other
    st.sidebar.stock_select = st.selectbox('Pick a Ticker',(market))




stock = st.sidebar.stock_select
ticker_data = yf.Ticker(stock) 
company_name = ticker_data.info['longName']
string_logo = '<img src=%s>' % ticker_data.info['logo_url']

st.header(company_name)
st.markdown(string_logo, unsafe_allow_html=True)

