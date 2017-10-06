#!/usr/bin/env python

import urllib2
import json
import os
from helpers import *

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
		response = urllib2.urlopen(GOOGLE_FINANCE_BASE + "?output=json&q=" + self.symbol)
		data = json.loads(response.read().replace("//", ""))

		#If it can't find a stock with ticker=self.symbol, add NYSE: to the front
		#	-If it can't find that, remove NYSE: and add .TO to the end
		#	-If it can't find that, you're out of luck because those are the only one's I've programmed in so far
		#I'll improve this later...
		try:
			self.info = data[0]
			random_check = self.info["symbol"]

		except:
			response = urllib2.urlopen(GOOGLE_FINANCE_BASE + "?output=json&q=NYSE:" + self.symbol)
			data = json.loads(response.read().replace("//", ""))

			try:
				self.info = data[0]
				random_check = self.info["symbol"]
			except:
				self.symbol = self.symbol + ".TO"
				response = urllib2.urlopen(GOOGLE_FINANCE_BASE + "?output=json&q=" + self.symbol)
				data = json.loads(response.read().replace("//", ""))

				try:
					self.info = data[0]
					random_check = self.info["symbol"]
				except:
					self.exists = False


	#Load the chart from Google Finance API
	def load_chart(self):
		img = open(self.filename, "wb")
		response = urllib2.urlopen(GOOGLE_FINANCE_BASE + "/getchart?q={0}&p=1d&i=150".format(self.symbol)).read()
		img.write(response)
		img.close()

	def update(self):
		self.load_info()
		self.load_chart()

	#Returns the price of the stock from the last trade
	def get_price(self):
		return self.info["l"]

	#Returns the percent change of the stock for the current day
	def get_percent_change(self):
		return self.info["cp"]

	#Returns a local path to the file containing the chart image
	def get_chart(self):
		return self.filename
