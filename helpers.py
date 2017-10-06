#!/usr/bin/env python

import re

GOOGLE_FINANCE_BASE = "https://finance.google.com/finance"

#Parses the message to check if there is a ticker in it, returns the symbol or ''
def parse_ticker(msg):
	after_dollar = msg.split("$")[1]
	ticker = re.split('[^a-zA-Z\.\-]', after_dollar)[0]
	return ticker