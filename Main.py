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
    start_date = st.sidebar.date_input("Start date", dt.date(2000, 1, 1))
    end_date = st.sidebar.date_input("End date", dt.date.today())
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



#Grabs data from the API
ticker_stock = st.sidebar.stock_select
ticker_data = yf.Ticker(ticker_stock) 
company_name = ticker_data.info['longName']
string_logo = '<img src=%s>' % ticker_data.info['logo_url']
ticker_df = ticker_data = yf.Ticker(ticker_stock).history(start = start_date, end = end_date) #get the historical prices for this ticker
ticker_df["Dates"] = ticker_df.index


#Creates the candle chart
color_conditions = alt.condition("datum.Open <= datum.Close",
                                 alt.value("green"),
                                 alt.value("red"))# build chart
chart = alt.Chart(ticker_df).encode(x = "Dates")
# set title of chart
chart.title = "Candle-stick Chart of "+ company_name
# set x axis label for chart
chart.encoding.x.title = "Time"
# construct a rule mark using mark_rule() method
rules = chart.mark_rule().encode(
    y = "Low",
    y2 = "High")
# adjust y axis label for rules
rules.encoding.y.title = "Price"
# construct bars
bars = chart.mark_bar().encode(
    y="Open",
    y2="Close",
    color = color_conditions)
candlestick = rules + bars

#Creates the regular chart 
chart = alt.Chart(ticker_df).mark_area(line={'color':'darkgreen'},color=alt.Gradient(
        gradient='linear',
        stops=[alt.GradientStop(color='white', offset=0),
               alt.GradientStop(color='darkgreen', offset=1)])).encode(x="Dates",y="Close")
chart.title = "Chart of "+ company_name
# display altair chart






# display rules and bars (both based on the same basic chart


st.header(company_name)
#st.markdown(string_logo, unsafe_allow_html=True)
agree = st.checkbox('Candle Chart')

if agree:
   st.altair_chart(candlestick, use_container_width=True)
else:
   st.altair_chart(chart, use_container_width=True)

