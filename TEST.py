


# import pandas as pd
# import numpy as np
# from pandas_datareader import data,wb
# import datetime
# import matplotlib.pylot as plt
# import matplotlib
# matplotlib.style.use('ggplot')
# %

from __future__ import print_function

import numpy as np
import datetime
from pandas_datareader import data
import pandas_datareader.data as web

import yfinance as yf
yf.pdr_override()

import warnings

import MySQLdb as mdb

db_host = 'localhost'
db_user = 'sec_user'
db_pass = 'password'
db_name = 'securities_master'
con = mdb.connect(db_host, db_user, db_pass, db_name)

if __name__ == "__main__":
    # start = datetime.datetime(2000, 1, 2)
    # end = datetime.datetime(2020, 6, 19)
    start = datetime.datetime(2001, 9, 5)
    end = datetime.datetime(2001, 9, 30)
    # sh = web.DataReader("EMN", 'yahoo', start, end)
    sh = web.get_data_yahoo("EMN", start, end)
    print(sh)
    # print(sh[sh['Open'] is np.nan])
    # print(sh[sh.isnull().T.any().T])

    # now = datetime.datetime.utcnow()
    #
    # cur = con.cursor()
    #
    # # Create the insert strings
    # column_str = """data_vendor_id, symbol_id, price_date, created_date,
    #                      last_updated_date, open_price, high_price, low_price,
    #                      close_price, volume, adj_close_price"""
    # insert_str = ("%s, " * 11)[:-2]
    # final_str = "INSERT INTO daily_price (%s) VALUES (%s)" % \
    #             (column_str, insert_str)

    # daily_datas = [
    #     ('1', 'AAPL', datetime.datetime.strftime(index.to_pydatetime(), "%Y-%m-%d %H:%M:%S"),
    #      datetime.datetime.strftime(now, "%Y-%m-%d %H:%M:%S"), datetime.datetime.strftime(now, "%Y-%m-%d %H:%M:%S"),
    #      '%.4f' % row['Open'], '%.4f' % row['High'], '%.4f' % row['Low'],
    #      '%.4f' % row['Close'], '%.4f' % row['Volume'], '%.4f' % row['Adj Close'])
    #     for index, row in sh.iterrows()
    # ]
    # print(daily_datas)

    # cur = con.cursor()
    # try:
    #     cur.executemany(final_str, daily_datas)
    #
    # except Exception as e:
    #     print("执行Mysql: %s 时出错：%s" % (final_str, e))
    # finally:
    #     con.commit()









