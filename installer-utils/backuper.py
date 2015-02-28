#!/usr/bin/python

import os
import time
import urllib2
import datetime
import glob

files = []
formatstring = "%A-%d-%B-%Y"
now = datetime.datetime.now()
timestampmax = now + datetime.timedelta(days=64)

for filename in os.listdir("."):
	if filename[-4:] == ".zip":
		if datetime.datetime.strptime(filename.split("_")[1], formatstring) > timestampmax:
			os.remove("./" + filename)


response = urllib2.urlopen('https://github.com/aaps/stardog/archive/master.zip')
afile = response.read()
open("stardog_" + now.strftime(formatstring)  + "_.zip", "w").write(afile)