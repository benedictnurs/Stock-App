import streamlit as st
import pandas as pd
import yfinance as yf
import datetime
import plotly.graph_objs as go
import plotly.express as px
from yahoo_fin import stock_info as si


st.set_page_config(
    page_title = "Stock Application",
    page_icon="📈",
    initial_sidebar_state="collapsed",
    )

#Sidebar of the dashboard and creates an empty container in the sidebar
window_sidebar = st.sidebar.container() 

#Date selections for the dashboard
sub_columns = window_sidebar.columns(2) 
start_date = sub_columns[0].date_input("Start", datetime.date(2010, 1, 1))
end_date = sub_columns[1].date_input("End", datetime.date.today())

#Market selections for the dashboard
market_select = window_sidebar.selectbox('Select Market',("S&P 500", "NASDAQ", "Dow Jones", "Other"))


class Stock():
	def __init__(self, stock):
		self.stock = stock

	#Grabs summarization data from the API
	def summary(self):
		return stock.info["longBusinessSummary"]

	def earnings(self): 
		return stock.earnings.head().style.format("{:,.0f}")

	#Grabs max price 
	def max_price(self): 
		return round(ticker_df["High"].max(),2)
	
	#Grabs current price
	def current_price(self): 
		price_current = round(ticker_df["Close"].iloc[-1],2)
		return price_current

	#Grabs starting price
	def starting_price(self): 
		price_start = round(ticker_df["Close"].iloc[0],2)
		return price_start


#To get the price change
def price_change(current ,start):  
	return round(current - start,2)


#To get the percent change
def percent_change(current ,start):  
	return round(((current - start)/start) * 100,2)


def market_selection():
        snp_500 = pd.DataFrame( si.tickers_sp500() )        
        nasdaq = pd.DataFrame( si.tickers_nasdaq() )
        dow = pd.DataFrame( si.tickers_dow() )
        other = pd.DataFrame( si.tickers_other() )

        if market_select == "S&P 500":
           market = snp_500
        elif market_select == "NASDAQ":
              market = nasdaq
        elif market_select == "Dow Jones":
                market = dow
        elif market_select == "Other":
                market = other
        return market


#Chart Visualization
def chart_candlestick():
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
                yaxis_title = "Price"

        )

        
        cs = fig.data[0]
        # Set line and fill colors
        cs.increasing.fillcolor = '#3D9970'
        cs.increasing.line.color = '#3D9970'
        cs.decreasing.fillcolor = '#FF4136'
        cs.decreasing.line.color = '#FF4136'
        return fig


def chart_line():
        fig = px.line(
                ticker_df,
                y = "Close" 
                )


        fig.update_layout(
                autosize=False,
                width = 800,
                height = 650,
                yaxis_title = "Price",
                #xaxis=dict(showgrid=False),
                #yaxis=dict(showgrid=False)
        )
        

        if ticker_df['Close'].iloc[-1] >= ticker_df['Close'].iloc[0]:
                fig.data[0].line.color = "#3D9970"
        else:
                fig.data[0].line.color = "#FF4136"

                


        return fig
        

#Stock selection for the dashboard
stock_select = window_sidebar.selectbox('Select Ticker',(market_selection()))

#Grabs data from the API
stock = yf.Ticker(stock_select) 
company_name = stock.info['longName']
ticker_df = stock.history(period= '1d',start = start_date, end = end_date) #get the historical prices for this ticker
ticker_df["Dates"] = ticker_df.index

#Creates an Object of Stock
stock_data = Stock(stock)

#Title of the stock
st.header(f"{company_name} ({stock_select})")

#The prices and deltas of the stock
window_page = st.container() # create an empty container in the page

#The prices with the deltas
sub_page = window_page.columns(4) 
sub_page[0].metric("Current Price", stock_data.current_price(), f"{percent_change(stock_data.current_price(),stock_data.starting_price()):,}%")
sub_page[1].metric("Start Price", stock_data.starting_price(), price_change(stock_data.current_price(),stock_data.starting_price()))
sub_page[2].metric("All-Time High", stock_data.max_price())

#Shows the chart 
chartCheck = st.checkbox("Candle Stick Chart")
chart = chart_line()

if chartCheck == True:
        chart = chart_candlestick()

st.plotly_chart(chart, use_container_width = True)


#Creating tabs 
tab1, tab2 = st.tabs(["Summarization", "Calculation"])


#Summarization of the stock 
tab1.caption(stock_data.summary())
#tab1.table(stock_data.earnings())

#Tab 2 
investedAmount = tab2.number_input("Initial Amount Invested")


def investment_changed():
        investedGrowth = round(percent_change(stock_data.current_price(),stock_data.starting_price())/100 * investedAmount,2) + investedAmount
        if investedGrowth >= investedAmount:
                investedChange = f""" <p style="font-family:sans-serif; 
                        color:Green;">
			${"{:,}".format(round(float(investedGrowth),2))}
			</p> """
        else:
                investedChange = f""" <p style="font-family:sans-serif; 
                        color:Red;">
			${"{:,}".format(round(float(investedGrowth),2))}
			</p> """
        return investedChange


def get_year():
        startYear = (str(ticker_df["Dates"].iloc[0])[0:4])
        endYear = (str(ticker_df["Dates"].iloc[-1])[0:4])
        year = int(endYear) - int(startYear)
        return year     


def gain_loss():
        gain = round(percent_change(stock_data.current_price(),stock_data.starting_price())/100 * investedAmount,2)
        change = ''
        if investedAmount == 0:
                gain = 0

        if gain >= investedAmount:
                change = f""" <p style="font-family:sans-serif; 
                        color:Green;">
			+${"{:,}".format(round(float(gain),2))}
			</p> """
        else:
                change = f""" <p style="font-family:sans-serif; 
                        color:Red;">
			-${"{:,}".format(round(float(abs(gain)),2))}
			</p> """
        return change


def gain_if():
        profit = round(percent_change(stock_data.current_price(),stock_data.starting_price())/100 * investedAmount,2)
        starting = investedAmount
        gain = profit - starting
        year = get_year()

        if gain >= starting:
                change = f'Total Gain After {year} Years'
        else:
                change = f'Total Loss After {year} Years'
        return change
        
        

sub_page2 = tab2.columns(2) 
sub_page2[0].markdown(f"Amount After {str(get_year())} Years", unsafe_allow_html=True)
sub_page2[0].markdown(investment_changed(), unsafe_allow_html=True)
sub_page2[1].markdown(gain_if(), unsafe_allow_html=True)
sub_page2[1].markdown(gain_loss(), unsafe_allow_html=True)