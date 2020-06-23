#!/usr/bin/python
# -*- coding: utf-8 -*-

# insert_symbols.py

from __future__ import print_function

import datetime
from math import ceil

import bs4
import MySQLdb as mdb
import requests


def obtain_parse_wiki_snp500():
    """
    Download and parse the Wikipedia list of S&P500 
    constituents using requests and BeautifulSoup.

    Returns a list of tuples for to add to MySQL.
    """
    # Stores the current time, for the created_at record
    now = datetime.datetime.utcnow()

    # Use requests and BeautifulSoup to download the 
    # list of S&P500 companies and obtain the symbol table
    # 网址变动了，为：http://en.volupedia.org/wiki/List_of_S%26P_500_companies，这样才能打开网站。
    response = requests.get(
        "http://en.volupedia.org/wiki/List_of_S%26P_500_companies"
    )
    soup = bs4.BeautifulSoup(response.text)

    # This selects the first table, using CSS Selector syntax
    # and then ignores the header row ([1:])
    # symbolslist = soup.select('table')[0].select('tr')[1:]
    # 网站上CSS结构已经变了，只能通过tr标签来进行选择。可以通过查看网页源码来确定起始位置，由于
    # tr标签并不只是用作股票代码的（如最后面的tr，不是放股票信息的），故select选择器只选取前500支。
    symbolslist = soup.select('tr')[2:502]

    # Obtain the symbol information for each 
    # row in the S&P500 constituent table
    symbols = []
    for i, symbol in enumerate(symbolslist):
        tds = symbol.select('td')
        symbols.append(
            (
                tds[0].select('a')[0].text,  # Ticker
                'stock',  # instrument
                tds[1].select('a')[0].text,  # Name
                tds[3].text,  # Sector
                'USD', now, now
            ) 
        )
    return symbols


def insert_snp500_symbols(symbols):
    """
    Insert the S&P500 symbols into the MySQL database.
    """
    # Connect to the MySQL instance
    db_host = 'localhost'
    db_user = 'sec_user'
    db_pass = 'password'
    db_name = 'securities_master'
    con = mdb.connect(
        host=db_host, port=3306, user=db_user, passwd=db_pass, db=db_name
    )

    # Create the insert strings
    column_str = """ticker, instrument, name, sector, 
                 currency, created_date, last_updated_date
                 """
    # 生成7个%s加空格，由于最后是，和空格结尾，因此要从-2向前截取。
    insert_str = ("%s, " * 7)[:-2]
    final_str = "INSERT INTO symbol (%s) VALUES (%s)" % \
        (column_str, insert_str)

    # Using the MySQL connection, carry out 
    # an INSERT INTO for every symbol
    # with con:
    cur = con.cursor()
    try:
        cur.executemany(final_str, symbols)
        con.commit()
    except Exception as e:
        con.rollback()
    finally:
        cur.close()
        con.close()



if __name__ == "__main__":
    symbols = obtain_parse_wiki_snp500()
    insert_snp500_symbols(symbols)
    print("%s symbols were successfully added." % len(symbols))
