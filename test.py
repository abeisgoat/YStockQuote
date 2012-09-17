#!/usr/bin/env python
import ystockquote as ysq
import datetime

#print ysq.get_historical_prices('GOOG', datetime.datetime(2012, 9, 1), datetime.datetime.now())
print ysq.get_price('GOOG')
print ysq.get_change('GOOG')
print ysq.get_all('GOOG')