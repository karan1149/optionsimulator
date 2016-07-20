# Using QuantSoftwareToolKit and concommitant libraries
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math

def simulate(ls_symbols, weights, dt_start, dt_end):
	dt_timeofday = dt.timedelta(hours=16)
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

	return sharpe

def find_weights(ls_symbols):
	dt_start = dt.datetime(2011, 1, 1)
	dt_end = dt.datetime(2011, 12, 31)

	max_sharpe = 0
	max_weights = [0, 0, 0, 0]

	# assuming number of symbols will be 4 for simplicity
	for w1 in np.arange(0, 1, .1):
    	for w2 in np.arange(0, 1, .1):
        	for w3 in np.arange(0, 1, .1):
            	for w4 in np.arange(0, 1, .1):
            	if (w1 + w2 + w3 + w4 == 1):
   		 curr_weights = [w1, w2, w3, w4]
   		 curr = simulate(ls_symbols, curr_weights, dt_start, dt_end)
   		 if (curr > max_sharpe):
   		 	max_sharpe = curr
   		 	max_weights = curr_weights
	return max_weights, max_sharpe
