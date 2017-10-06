#!/usr/bin/env python

from fbchat import log, Client
from helpers import parse_ticker
from stock import Stock
import os

class StockBot(Client):

	def send_info(self, s, thread_id, thread_type):
		msg = "${0}\n==================\nCurrent Price: ${1}\nDaily change: {2}".format(s.symbol, s.get_price(), s.get_percent_change())

		#Send chart with msg
		self.sendLocalImage(s.get_chart(), msg, thread_id=thread_id, thread_type=thread_type)

		#Remove the local copy of the chart image
		os.remove(format(ticker_file_name))

	def onMessage(self, author_id, message, thread_id, thread_type, **kwargs):
		self.markAsDelivered(author_id, thread_id)
		self.markAsRead(author_id)

		if author_id != self.uid:

			if "$" in message:
				ticker = parse_ticker(message).upper()

				#Not an actual ticker, maybe entered a dollar amount (i.e. $30)
				if (ticker  == ''):
					return

				s = Stock(ticker)

				if s.exists:
					log.info("Found ticker symbol {0} in last message".format(s.symbol))
					self.send_info(s, thread_id, thread_type)
					
				else:
					msg = "Can't find ticker ${0}".format(ticker.upper())
					self.sendMessage(msg, thread_id=thread_id, thread_type=thread_type)


client = StockBot("fbchatstockbot@gmail.com", "botpassword123")
client.listen()