import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import yfinance as yf
import datetime
from yahoo_fin import stock_info as si
 

st.set_page_config(
    page_title = "Stock Application",
    page_icon="📈",
    initial_sidebar_state="collapsed",
    )

snp_500 = pd.DataFrame( si.tickers_sp500() )
nasdaq = pd.DataFrame( si.tickers_nasdaq() )
dow = pd.DataFrame( si.tickers_dow() )
other = pd.DataFrame( si.tickers_other() )

#Sidebar of the dashboard
window_sidebar = st.sidebar.container() # create an empty container in the sidebar
sub_columns = window_sidebar.columns(2) 

#Date selections for the dashboard
start_date = sub_columns[0].date_input("Start", datetime.date(2010, 1, 1))
end_date = sub_columns[1].date_input("End", datetime.date.today())
market_select = window_sidebar.selectbox('Select Market',("S&P 500", "NASDAQ", "Dow Jones", "Other"))

#Market selections for the dashboard
if market_select == "S&P 500":
        market = snp_500
elif market_select == "NASDAQ":
        market = nasdaq
elif market_select == "Dow Jones":
        market = dow
elif market_select == "Other":
        market = other

#Stock selection for the dashboard
stock_select = window_sidebar.selectbox('Select Ticker',(market))


#Grabs data from the API
ticker_stock = stock_select
stock = yf.Ticker(ticker_stock) 
company_name = stock.info['longName']
string_logo = '<img src=%s>' % stock.info['logo_url']
ticker_df = stock.history(period= '1d',start = start_date, end = end_date) #get the historical prices for this ticker
ticker_df["Dates"] = ticker_df.index

#Grabs summarization data from the API
summary = stock.info["longBusinessSummary"]
earnings = stock.earnings.head().style.format("{:,.0f}")

#Grabs prices 
max_price = round(ticker_df["High"].max(),2)
current_price = round(stock.info['regularMarketPrice'],2)
starting_price = round(ticker_df["Close"].iloc[0],2)


#Calculates change 
price_change = round(current_price - starting_price,2)
percent_change = round(((current_price - starting_price)/starting_price) * 100,2)




#Creates the candle chart
color_conditions = alt.condition("datum.Open <= datum.Close",
                                 alt.value("green"),
                                 alt.value("red"))
# build chart
chart = alt.Chart(ticker_df).encode(x = "Dates")
# set x axis label for chart
chart.encoding.x.title = "Time"
# construct a rule mark using mark_rule() method
rules = chart.mark_rule().encode(
    y = "Low",
    y2 = "High")
# adjust y axis label for rules
rules.encoding.y.title = "Close"
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

#Title of the stock
st.header(company_name + " ("+ticker_stock+")")

#The Prices and deltas of the stock
window_page = st.container() # create an empty container in the page
sub_page = window_page.columns(4) 
sub_page[0].metric("Current Price", current_price, price_change)
sub_page[1].metric("Start Price", starting_price, f"{percent_change}%")
sub_page[2].metric("All-Time High", max_price)


#st.markdown(string_logo, unsafe_allow_html=True)
agree = st.checkbox('Candle Chart')

if agree:
   st.altair_chart(candlestick, use_container_width = True)

else:
   st.altair_chart(chart, use_container_width = True)

#Summarization of the stock
st.caption(summary)
st.table(earnings)


