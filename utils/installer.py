#!/usr/bin/python

from StringIO import StringIO
from zipfile import ZipFile
import urllib2
import json
import os
from time import localtime

logfile = "installer_log.txt"

# function that logs output to a logfile
# and applies a time stamp.
# it can be used to show the correct version
# is downloaded or not.


def log(logline, logfile):
    lt = localtime
    timestr = ("%d-%d-%d-%d" % (lt().tm_year, lt().tm_mon,
                                lt().tm_mday, lt().tm_hour))
    with open(logfile, 'a') as logfile:
        logfile.write("%s >> %s\n" % (timestr, logline))

# files that are to be ignored.
filterfiles = ['.gitignore', 'utils', '.git', 'todo-and-plans.md', 'ingredients_and_materials.txt', 'economic-simulation.txt']

# open a request for the data on this url
tag_url = "https://api.github.com/repos/aaps/stardog/tags"
tags = urllib2.urlopen(tag_url)
# returns list one element, get the first.
tags_text = tags.readlines()[0]
# the data on the newest version is always
# in the first element.
tags_json = json.loads(tags_text)[0]
ziplink = tags_json[u'zipball_url']
# log the version.
log(str(tags_json[u'name']), logfile)

url = urllib2.urlopen(ziplink)
zf = ZipFile(StringIO(url.read()))
names = zf.namelist()

for name in names:
    if name.split("/")[-1] not in filterfiles:
        newname = "/".join(name.split('/')[1:])
        if newname.endswith('/'):
            # try for if folder already exists
            try:
                os.makedirs(os.path.normpath(newname))
            except:
                pass
        elif len(newname) > 0:
            file(os.path.normpath(newname),
                 'wb').write(zf.read(name))
