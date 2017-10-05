#!/usr/bin/env python

import re
from rtstock.stock import Stock

#Parses the message to check if there is a ticker in it, returns the symbol or ''
def parse_ticker(msg):
	after_dollar = msg.split("$")[1]
	ticker = re.split('[^a-zA-Z\.\-]', after_dollar)[0]
	return ticker

#Gets the info for a given ticker, if it gives bad info, try with .TO at the end (Toronto stock exchange)
#	If no info can be found, return None
def get_stock_info(ticker):
	stock = Stock(ticker)
	info = stock.get_info()[0]
	if info["LastTradePriceOnly"] != None:
		return (ticker, info)
	else:
		stock = Stock(ticker+".TO")
		info = stock.get_info()[0]
		if info["LastTradePriceOnly"] != None:
			return (ticker+".TO", info)

