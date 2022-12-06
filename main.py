import streamlit as st
import pandas as pd
import yfinance as yf
import datetime
import plotly.graph_objs as go
from yahoo_fin import stock_info as si
 

st.set_page_config(
    page_title = "Stock Application",
    page_icon="📈",
    initial_sidebar_state="collapsed",
    )


class Stock():
	def __init__(self, stock):
		self.stock = stock

	#Grabs summarization data from the API
	def summary(self):
		return stock.info["longBusinessSummary"]

	def earnings(self): 
		return stock.earnings.head().style.format("{:,.0f}")

	#Grabs prices 
	def max_price(self): 
		return round(ticker_df["High"].max(),2)
	
	def current_price(self): 
		return round(stock.info['regularMarketPrice'],2)
	
	def starting_price(self):
		return round(ticker_df["Close"].iloc[0],2)


snp_500 = pd.DataFrame( si.tickers_sp500() )
nasdaq = pd.DataFrame( si.tickers_nasdaq() )
dow = pd.DataFrame( si.tickers_dow() )
other = pd.DataFrame( si.tickers_other() )

#Sidebar of the dashboard
window_sidebar = st.sidebar.container() 
#Create an empty container in the sidebar

#Date selections for the dashboard
sub_columns = window_sidebar.columns(2) 
start_date = sub_columns[0].date_input("Start", datetime.date(2010, 1, 1))
end_date = sub_columns[1].date_input("End", datetime.date.today())


#Market selections for the dashboard
market_select = window_sidebar.selectbox('Select Market',("S&P 500", "NASDAQ", "Dow Jones", "Other"))
def market_selection():
        if market_select == "S&P 500":
           market = snp_500
        elif market_select == "NASDAQ":
              market = nasdaq
        elif market_select == "Dow Jones":
                market = dow
        elif market_select == "Other":
                market = other
        return market

#Stock selection for the dashboard
stock_select = window_sidebar.selectbox('Select Ticker',(market_selection()))


#Grabs data from the API
stock = yf.Ticker(stock_select) 
company_name = stock.info['longName']
ticker_df = stock.history(period= '1d',start = start_date, end = end_date) #get the historical prices for this ticker
ticker_df["Dates"] = ticker_df.index

#Creates an Object of Stock
stock_data = Stock(stock)


#Grabs prices 
max_price = round(ticker_df["High"].max(),2)
current_price = round(stock.info['regularMarketPrice'],2)
starting_price = round(ticker_df["Close"].iloc[0],2)


#Calculates change 
price_change = round(current_price - starting_price,2)
percent_change = round(((current_price - starting_price)/starting_price) * 100,2)


#Chart Visualization
def chart():
        fig = go.Figure()
        fig.add_trace(go.Candlestick(
                x = ticker_df.index,
                open = ticker_df['Open'],
                high = ticker_df['High'],
                low = ticker_df['Low'],
                close = ticker_df['Close'], 
                name = 'market data',))

        fig.update_layout(
                autosize=False,
                width = 800,
                height = 650,
        )

        # Add titles
        fig.update_layout(
                #title= f"{company_name} Live Chart",
                yaxis_title = "Price")
        return fig

#Title of the stock
st.header(f"{company_name} ({stock_select})")




#The Prices and deltas of the stock
window_page = st.container() # create an empty container in the page
sub_page = window_page.columns(4) 
sub_page[0].metric("Current Price", current_price, f"{percent_change:,}%")
sub_page[1].metric("Start Price", starting_price, price_change)
sub_page[2].metric("All-Time High", max_price)

#Shows the chart 
st.plotly_chart(chart(), use_container_width=True)



#Summarization of the stock
st.caption(stock_data.summary())
st.table(stock_data.earnings())


