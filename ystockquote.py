#!/usr/bin/env python
#
#  Copyright (c) 2012, Abraham Haskins (abeisgreat@abeisgreat.com)
#  Copyright (c) 2007-2008, Corey Goldberg (corey@goldb.org)
#
#  license: GNU LGPL
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2.1 of the License, or (at your option) any later version.


import urllib, datetime


"""
This is the "ystockquote" module.

This module provides a Python API for retrieving stock data from Yahoo Finance.

sample usage:
>>> import ystockquote
>>> print ystockquote.get_price('GOOG')
529.46
"""

yahoo_keys = {
    'price': 'l1',
    'change': 'c1',
    'volume': 'v',
    'average_daily_volume': 'a2',
    'stock_exchange': 'x',
    'market_cap': 'j1',
    'book_value': 'b4',
    'ebitda': 'j4',
    'dividend_per_share': 'd',
    'dividend_yield': 'y',
    'earnings_per_share': 'e',
    '52_week_high': 'k',
    '52_week_low': 'j',
    '50day_moving_average': 'm3',
    '200day_moving_average': 'm4',
    'price_earnings_ratio': 'r',
    'price_earnings_growth_ratio': 'r5',
    'get_price_sales_ratio': 'p5',
    'price_book_ratio': 'p6',
    'short_ratio': 's7'
}

for key in yahoo_keys:
    st = yahoo_keys[key]
    globals()['get_%s' % key] = lambda sy: __request(sy, st)

def __request(symbol, stat):
    url = 'http://finance.yahoo.com/d/quotes.csv?s=%s&f=%s' % (symbol, stat)
    return urllib.urlopen(url).read().strip().strip('"')


def get_all(symbol):
    """
    Get all available quote data for the given ticker symbol.
    
    Returns a dictionary.
    """
    values = __request(symbol, 'l1c1va2xj1b4j4dyekjm3m4rr5p5p6s7').split(',')
    data = {}
    data['price'] = values[0]
    data['change'] = values[1]
    data['volume'] = values[2]
    data['avg_daily_volume'] = values[3]
    data['stock_exchange'] = values[4]
    data['market_cap'] = values[5]
    data['book_value'] = values[6]
    data['ebitda'] = values[7]
    data['dividend_per_share'] = values[8]
    data['dividend_yield'] = values[9]
    data['earnings_per_share'] = values[10]
    data['52_week_high'] = values[11]
    data['52_week_low'] = values[12]
    data['50day_moving_avg'] = values[13]
    data['200day_moving_avg'] = values[14]
    data['price_earnings_ratio'] = values[15]
    data['price_earnings_growth_ratio'] = values[16]
    data['price_sales_ratio'] = values[17]
    data['price_book_ratio'] = values[18]
    data['short_ratio'] = values[19]
    return data
    
def get_historical_prices(symbol, start_datetime, end_datetime):

    start_date  = start_datetime.strftime("%Y%m%d") # Convert our nice Datetimes into Yahoo's date format
    end_date    = end_datetime.strftime("%Y%m%d")  # See above 

    request_data = {
        'a': str(int(start_date[4:6]) - 1),
        'b': start_date[6:8],
        'c': start_date[0:4],
        'd': str(int(end_date[4:6]) - 1),
        'e': end_date[6:8],
        'f': end_date[0:4],
    }

    url = 'http://ichart.yahoo.com/table.csv?s=%s&g=d&ignore=.csv' % symbol
    for key in request_data: 
        url += '&%s=%s' % (key, request_data[key])

    days = urllib.urlopen(url).readlines() # Load the CSV
    data = [day[:-2].split(',') for day in days] # Split the CSV sheet

    tdata = []  # Type'd Data version of Data
    for row in sorted(data[1:]): # Reverse and loop through our data
        tdata.append([ 
            datetime.datetime(int(row[0][0:4]), int(row[0][5:7]), int(row[0][8:10])), 
            float(row[1]), 
            float(row[2]), 
            float(row[3]), 
            float(row[4]), 
            int(row[5]), 
            float(row[6])
        ]) # Convert everything to the right types

    return tdata