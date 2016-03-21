
import  pandas_datareader as web

price = web.get_data_yahoo('AAPL', '2015-01-01')['Adj Close']

print price