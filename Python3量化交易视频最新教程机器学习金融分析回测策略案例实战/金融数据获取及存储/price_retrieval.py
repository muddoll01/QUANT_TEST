#!/usr/bin/python
# -*- coding: utf-8 -*-

# price_retrieval.py

from __future__ import print_function

import warnings

import MySQLdb as mdb
import requests
import yfinance as yf
yf.pdr_override()

import datetime
# from pandas_datareader import data
import pandas_datareader.data as web

# Obtain a database connection to the MySQL instance
db_host = 'localhost'
db_user = 'sec_user'
db_pass = 'password'
db_name = 'securities_master'
con = mdb.connect(db_host, db_user, db_pass, db_name)


def obtain_list_of_db_tickers():
    """
    Obtains a list of the ticker symbols in the database.
    """
    # with con:
    cur = con.cursor()
    try:
        # cur.execute("SELECT id, ticker FROM symbol")
        # 只用前两条数据来进行测试
        # cur.execute("SELECT id, ticker FROM symbol LIMIT 0, 2")
        # 如果全部一次性插入会失败，可以考虑每次插入50支股票的数据，分10次完成。
        cur.execute("SELECT id, ticker FROM symbol WHERE id >= 199 AND id <= 200")
        data = cur.fetchall()
    except(Exception):
        con.rollback()
        raise Exception("Execute QUERY err.")
    finally:
        pass
        # cur.close()
        # con.close()
    return [(d[0], d[1]) for d in data]

# 说明：由于yahoo不再提供API服务，前面方法中的程序无法运行获取股票历史数据，改为pandas获取
def get_daily_historic_data_yahoo_ZY(
        ticker, start_date=datetime.datetime(2000, 1, 1),
        end_date=datetime.date.today()
    ):
    # start_date = datetime.datetime(2020, 5, 1)
    # end_date = datetime.datetime(2020, 6, 3)
    # prices = web.DataReader(ticker, 'yahoo', start_date, end_date)

    # 网速很慢时，获取数据速度会很慢，可能一直卡在这。
    prices = web.get_data_yahoo(ticker, start_date, end_date)

    return prices

def insert_daily_data_into_db_ZY(
        data_vendor_id, symbol_id, daily_data
    ):
    now = datetime.datetime.utcnow()

    # Create the insert strings
    column_str = """data_vendor_id, symbol_id, price_date, created_date, 
                     last_updated_date, open_price, high_price, low_price, 
                     close_price, volume, adj_close_price"""
    insert_str = ("%s, " * 11)[:-2]
    final_str = "INSERT INTO daily_price (%s) VALUES (%s)" % \
                (column_str, insert_str)

    """
    测试daily_data构建，由于数据库表是保留4位小数，从yahoo获取的float数据是14位小数，需要截取后存入数据库。
    另外，Python里面的datetime和mysql数据库里面的datetime不能通过，不能直接把python里面的datetime对象直接插入到
    数据库中，会失败，需要按数据库格式进行转换后插入。
    """
    daily_datas = [
        (data_vendor_id, symbol_id, datetime.datetime.strftime(index.to_pydatetime(), "%Y-%m-%d %H:%M:%S"),
         datetime.datetime.strftime(now, "%Y-%m-%d %H:%M:%S"), datetime.datetime.strftime(now, "%Y-%m-%d %H:%M:%S"),
         '%.4f' % row['Open'], '%.4f' % row['High'], '%.4f' % row['Low'],
         '%.4f' % row['Close'], '%.4f' % row['Volume'], '%.4f' % row['Adj Close'])
        for index, row in daily_data.iterrows()
    ]
    # print(daily_datas)

    cur = con.cursor()
    try:
        cur.executemany(final_str, daily_datas)
    except Exception as e:
        print("执行Mysql: %s 时出错：%s" % (final_str, e))
        # con.rollback()
    finally:
        # 一定要commit，否则无法写入数据库
        con.commit()
        print('commit 成功')
        # cur.close()
        # con.close() // con是定义在main函数中的，不能关闭

if __name__ == "__main__":
    # This ignores the warnings regarding Data Truncation
    # from the Yahoo precision to Decimal(19,4) datatypes
    warnings.filterwarnings('ignore')

    # Loop over the tickers and insert the daily historical
    # data into the database
    tickers = obtain_list_of_db_tickers()
    lentickers = len(tickers)
    for i, t in enumerate(tickers):
        print(
            "Adding data for %s: %s out of %s" % 
            (t[1], i+1, lentickers)
        )
        yf_data = get_daily_historic_data_yahoo_ZY(t[1])
        # print(yf_data)
        # print(str(t[0]))
        insert_daily_data_into_db_ZY(1, int(t[0]), yf_data)
    print("Successfully added Yahoo Finance pricing data to DB.")
