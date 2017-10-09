#!/usr/bin/env python

import re

GOOGLE_FINANCE_BASE = "https://finance.google.com/finance"

"""
Parses the message for the ticker name and also returns a date
range if a valid one is given (else '1d') along with an extra 
parameter `i` used to obtain the correct image of the chart.
"""
def parse_ticker(msg):
	valid_ranges = ['d', 'm', 'y']
	ranges = {
    '1d': 60,
    '5d': 240,
    '1M': 86400,
    '3M': 86400,
    '6M': 86400,
    '1Y': 86400,
    '5Y': 604800,
    '40Y': 604800,
  }
	after_dollar = (msg.split("$")[1]).split(" ")[:2]
	ticker = re.split('[^a-zA-Z\.\-]', after_dollar[0])[0].upper()
	# if the ticker is entered as a dollar amount
	if ticker.isnumeric():
		ticker = ''
		return (ticker, None, None)

	duration = "1d"
	if len(after_dollar) > 1:
		if after_dollar[1] == "max":
			duration = "40Y"
		else:
	  	if after_dollar[1][0].isnumeric() and (after_dollar[1][1].lower() in valid_ranges):
	    	duration = after_dollar[1][0] + after_dollar[1][1]
	    	if after_dollar[1][1].lower() != 'd':
	    		duration = after_dollar[1][0] + after_dollar[1][1].upper()
	i = 60
	if duration in ranges:
		i = ranges[duration]
	else:
		duration = "1d"
	
	return (ticker, duration, i)
