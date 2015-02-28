#!/usr/bin/python

import os
import time
import urllib2
import datetime
import glob

files = []
formatstring = "%A-%d-%B-%Y"

timestampmax = datetime.datetime.now() + datetime.timedelta(days=64)

# print datetime.datetime.now()

for filename in os.listdir("."):
	if filename[-4:] == ".zip":
		if datetime.datetime.strptime(filename.split("_")[1], formatstring) > timestampmax:
			os.remove("./" + filename)

