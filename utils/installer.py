from StringIO import StringIO
from zipfile import ZipFile
from urllib import urlopen
import os, sys, shutil
import imp



url = urlopen("https://github.com/aaps/stardog/archive/master.zip")
zipfile = ZipFile(StringIO(url.read()))
zipfile.extractall("..")

for filename in os.listdir(".."):
	if filename.startswith("stardog"):
		os.rename(filename, "stardog")


try:
    imp.find_module('eggs')
    found = True
except ImportError:
    found = False

