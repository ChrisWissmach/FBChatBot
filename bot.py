#!/usr/bin/env python

from rtstock.stock import Stock
from fbchat import log, Client
from helpers import *
import os
import urllib

class StockBot(Client):

	def send_info(self, ticker, info, thread_id, thread_type):
		msg = "${0}\n==================\nCurrent Price: ${1}\nDaily change: {2}".format(ticker, info["LastTradePriceOnly"], info["ChangeinPercent"])
		chart_url = "https://finance.google.com/finance/getchart?q={0}&p=1d&i=150".format(ticker)
		ticker_file_name = ticker.replace('.', '')

		#Get the chart image, write to local file so it can be sent in a message
		img = open('{0}temp.png'.format(ticker_file_name), 'wb')
		img.write(urllib.urlopen(chart_url).read())
		img.close()

		#Send chart with msg
		self.sendLocalImage('{0}temp.png'.format(ticker_file_name), msg, thread_id=thread_id, thread_type=thread_type)

		#Remove the local copy of the chart image
		os.remove('{0}temp.png'.format(ticker_file_name))

	def onMessage(self, author_id, message, thread_id, thread_type, **kwargs):
		self.markAsDelivered(author_id, thread_id)
		self.markAsRead(author_id)

		if author_id != self.uid:
			if "$" in message:

				ticker = parse_ticker(message).upper()

				#Not an actual ticker, maybe entered a dollar amount (i.e. $30)
				if (ticker  == ''):
					return

				ticker, info = get_stock_info(ticker)

				if info != None:
					log.info("Found ticker symbol {0} in last message".format(ticker))
					self.send_info(ticker, info, thread_id, thread_type)
					
				else:
					msg = "Can't find ticker ${0}".format(ticker.upper())
					self.sendMessage(msg, thread_id=thread_id, thread_type=thread_type)


client = StockBot("fbchatstockbot@gmail.com", "botpassword123")
client.listen()