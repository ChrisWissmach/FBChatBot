#!/usr/bin/env python

from fbchat import log, Client
from helpers import parse_ticker
from stock import Stock
import os

class StockBot(Client):

	def send_info(self, s, thread_id, thread_type):
		price = s.get_price()
		if price == "-1":
			msg = "Error with ticker. Google's fault though, not mine..."
			self.sendMessage(msg, thread_id=thread_id, thread_type=thread_type)
			return

		msg = "${0} ({1})\n==================\nCurrent Price: ${2}\nDaily change: {3}%".format(s.symbol, s.duration.upper(), price, s.get_percent_change())

		#Send chart with msg
		self.sendLocalImage(s.get_chart(), msg, thread_id=thread_id, thread_type=thread_type)


	def onMessage(self, author_id, message, thread_id, thread_type, **kwargs):
		self.markAsDelivered(author_id, thread_id)
		self.markAsRead(author_id)

		if author_id != self.uid:

			if "$" in message:
				ticker, duration, i = parse_ticker(message)

				#Not an actual ticker, maybe entered a dollar amount (i.e. $30)
				if (ticker  == ''):
					return

				s = Stock(ticker, duration, i)

				if s.exists:
					log.info("Found ticker symbol {0} in last message".format(s.symbol))
					self.send_info(s, thread_id, thread_type)
					
				else:
					msg = "Can't find ticker ${0}".format(ticker.upper())
					self.sendMessage(msg, thread_id=thread_id, thread_type=thread_type)


client = StockBot("<EMAIL>", "<PASSWORD>")
client.listen()
