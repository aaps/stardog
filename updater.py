#!/usr/bin/python

from StringIO import StringIO
from zipfile import ZipFile
import urllib2
import json
import os
from time import localtime
import fnmatch
import os.path


logfile = "installer_log.txt"


def log(logline, logfile):
    """
    function that logs output to a logfile
    and applies a time stamp.
    it can be used to show the correct version
    is downloaded or not.
    """
    lt = localtime
    timestr = ("%d-%d-%d-%d" % (lt().tm_year, lt().tm_mon,
                                lt().tm_mday, lt().tm_hour))
    with open(logfile, 'a') as logfile:
        logfile.write("%s >> %s\n" % (timestr, logline))


def getGitVersion(tag_url="https://api.github.com/repos/aaps/stardog/tags"):
    """ returns a string that is the latest version reported on git tags."""
    import urllib2
    import json
    # open a request for the github repo tags.
    try:
        tags = urllib2.urlopen(tag_url, timeout = 5)
    except:
        return "timeout"
    # returns a list one element get that element.
    tag_text = tags.readlines()[0]
    # the newest version is always in the first jason structure.
    tag_json = json.loads(tag_text)[0]
    return str(tag_json[u'name'])

def getCredits(tag_url="https://raw.githubusercontent.com/aaps/stardog/master/texts/Credits.txt"):
    """ returns a string that is the latest version reported on git tags."""
    import urllib2
    # import json
    # open a request for the github repo tags.
    try:
        urlobject = urllib2.urlopen(tag_url, timeout = 5)
    except:
        return "timeout"
    contents = urlobject.readlines()
    return str('\n'.join(contents))


def getLogVersion(logfile="installer_log.txt"):
    """
    returns a string that is the latest version
    reported in the log file.
    """
    lines = []
    if not os.path.isfile(logfile):
        return lines
    else:
        with open(logfile, 'r') as log:
            lines = log.readlines()
        # get the last element
        version = lines[-1]
        # get version
        version = version.split(' ')[-1]
        # remove newline
        version = version[0:-1]
        return version


def checkVersion():
    """ return True if current version """
    return(getLogVersion() == getGitVersion())

if __name__ == "__main__":
    # files that are to be ignored.
    filterfiles = ['.gitignore', 'installer-utils', '.git', 'todo-and-plans.md',
                   'ingredients_and_materials.txt', 'economic-simulation.txt','texts']
    print("Get zip link and downloading.")
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
    print("Done")
    print("Unzipping and copying files.")
    zf = ZipFile(StringIO(url.read()))
    names = zf.namelist()

    for name in names:
        thename = name.split("/")
        useit = True
        for aname in filterfiles:
            if fnmatch.fnmatch(name, '*' + aname + '*'):
                useit = False
        if useit:
            newname = "/".join(thename[1:])
            if newname.endswith('/'):
                # try for if folder already exists
                try:
                    os.makedirs(os.path.normpath(newname))
                except:
                    pass
            elif len(newname) > 0:
                print newname
                file(os.path.normpath(newname), 'wb').write(zf.read(name))
    print("Done")
