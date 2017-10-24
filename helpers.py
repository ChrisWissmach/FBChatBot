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
	after_dollar = (msg.split("$", 1)[1]).split(" ")[:2]
	ticker = re.split('[^a-zA-Z\.\-]', after_dollar[0])[0].upper()
	# if the ticker is entered as a dollar amount
	if ticker.isnumeric() or ticker == '':
		ticker = ''
		return (ticker, None, None)

	duration = "1d"
	if len(after_dollar) > 1 and len(after_dollar[1]) > 1:
		if after_dollar[1] == "max":
			duration = "40Y"
		else:
			if after_dollar[1][0].isnumeric() and (after_dollar[1][1].lower() in valid_ranges):
				duration = after_dollar[1][0] + after_dollar[1][1]
			if after_dollar[1][1].lower() != 'd' and after_dollar[1][1].lower() in ['m','y']:
				duration = after_dollar[1][0] + after_dollar[1][1].upper()
	i = 60
	if duration in ranges:
		i = ranges[duration]
	else:
		num = int(duration[0])
		letter = duration[1]
		if letter == 'd':
			if num > 1 and num < 5:
				num = 5
			elif num > 5:
				num = 1
				letter = 'M'
		elif letter == 'M':
			if num > 1 and num < 3:
				num = 3
			elif num > 3 and num < 6:
				num = 6
			elif num > 6:
				num = 1
				letter = 'Y'
		elif letter == 'Y':
			if num > 1 and num < 5:
				num = 5		
			elif num > 5 and num < 40:
				num = 40

		duration = str(num) + letter
	
	return (ticker, duration, i)
