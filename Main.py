import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import yfinance as yf
import datetime as dt
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


window_sidebar = st.sidebar.container() # create an empty container in the sidebar
sub_columns = window_sidebar.columns(2) 


start_date = sub_columns[0].date_input("Start date", dt.date(2000, 1, 1))
end_date = sub_columns[1].date_input("End date", dt.date.today())
market_select = window_sidebar.selectbox('Pick a Market',("S&P 500", "NASDAQ", "Dow Jones", "Other"))
    

st.markdown(f'''
    <style>
        section[data-testid="stSidebar"] .css-ng1t4o {{width: 10rem;}}
        section[data-testid="stSidebar"] .css-1d391kg {{width: 10rem;}}
    </style>
''',unsafe_allow_html=True)

if st.sidebar.market_select == "S&P 500":
        market = snp_500
elif st.sidebar.market_select == "NASDAQ":
        market = nasdaq
elif st.sidebar.market_select == "Dow Jones":
        market = dow
elif st.sidebar.market_select == "Other":
        market = other
stock_select = window_sidebar.selectbox('Pick a Ticker',(market))



#Grabs data from the API
ticker_stock = stock_select
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


st.header(company_name)
#st.markdown(string_logo, unsafe_allow_html=True)
chart_plot = st.empty()
agree = st.checkbox('Candle Chart')

if agree:
   chart_plot.altair_chart(candlestick, use_container_width = True)

else:
   chart_plot.altair_chart(chart, use_container_width = True)

