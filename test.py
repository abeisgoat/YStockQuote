#!/usr/bin/env python
import ystockquote as ysq
import datetime

#print ysq.get_historical_prices('GOOG', datetime.datetime(2012, 9, 1), datetime.datetime.now())
print ysq.get_moving_average('QIHU', 50)
print ysq.get_exponential_moving_average('QIHU', 50)