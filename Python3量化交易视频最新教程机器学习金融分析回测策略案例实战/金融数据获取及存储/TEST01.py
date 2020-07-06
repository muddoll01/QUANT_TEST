from __future__ import print_function

import yfinance as yf
yf.pdr_override()
import datetime
# from pandas_datareader import data
import pandas_datareader.data as web

if __name__ == '__main__':
    # print(datetime.date.today().timetuple()[0:3])
    # print(datetime.datetime.today())

    # amzn = web.DataReader('AMZN', 'yahoo', datetime(2000, 1, 1), datetime(2015, 1, 1))

    amzn = web.get_data_yahoo('AREX', datetime.datetime(2000, 1, 1), datetime.datetime(2015, 1, 1))
    # print(amzn.head(5))





