# Using QuantSoftwareToolKit and concommitant libraries
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math

# vol, avg_ret, sharpe, cum_ret = simulate(..)
def simulate(ls_symbols, weights):
	dt_timeofday = dt.timedelta(hours=16)
	dt_start = dt.datetime(2006, 1, 1)
	dt_end = dt.datetime(2010, 12, 31)
	ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)

	c_dataobj = da.DataAccess('Yahoo')
	ls_keys = ['close']
	key_data = c_dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
	data = dict(zip(ls_keys, key_data))
	prices = np.array(data.values()[0])

	prices_norm = prices / prices[0, : ]

	# get 0 column without clunky np array syntax
	weighted_price = 0

	# assume number of symbols == number of weights
	for i in range(len(weights)):
    weighted_price += weights[i] * prices_norm[ : , i]

	# get daily returns
	daily_returns = weighted_price.copy()
	tsu.returnize0(daily_returns)

	# get return parameters
	avg_ret = daily_returns.mean()
	vol = daily_returns.std()
	sharpe = avg_ret / vol * math.sqrt(252) # 252 is the number of trading days
	cum_ret = list(weighted_price)[len(list(weighted_price)) - 1] - 1

	return vol, avg_ret, sharpe, cum_ret, weighted_price
