#!/usr/bin/env python

import urllib2
import json
import os

class Stock:

	def __init__(self, ticker):
		self.symbol = ticker
		self.filename = "{0}temp.png".format(self.symbol.replace(".", ""))
		self.info = None
		self.exists = True
		self.update()

	#Destructor, delete the file containing the chart image
	def __del__(self):
		os.remove(self.filename)

	#Load the info from Google Finance API
	def load_info(self):
		response = urllib2.urlopen(GOOGLE_FINANCE_BASE + "output=json&q=" + self.symbol)
		data = json.loads(response.read().replace("//", ""))

		try:
			self.info = data[0]

		except:
			self.exists = False

	#Load the chart from Google Finance API
	def load_chart(self):
		img = open("{0}temp.png".format(self.filename), wb)
		response = urllib2.urlopen(GOOGLE_FINANCE_BASE + "/getchart?q={0}&p=1d&i=150".format(self.symbol)).read()
		img.write(response)
		img.close()

	def update(self):
		self.load_info()
		self.load_chart()

	#Returns the price of the stock from the last trade
	def get_price(self):
		return int(self.info["l"])

	#Returns the percent change of the stock for the current day
	def get_percent_change(self):
		return int(self.info["cp"])

	#Returns a local path to the file containing the chart image
	def get_chart(self):
		return self.filename