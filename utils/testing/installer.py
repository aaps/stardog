from StringIO import StringIO
from zipfile import ZipFile
from urllib import urlopen
import urllib2
import json
import os, sys, shutil

filterfiles = ['.gitignore', 'utils', '.git', 'todo', 'ingredients']

tag_url = "https://api.github.com/repos/aaps/stardog/tags"
tags = urllib2.urlopen(tag_url)
# returns list one element, get the first.
tags_text = tags.readlines()[0]
# the data on the newest version is always
# in the first element.
tags_json = json.loads(tags_text)[0]
ziplink = tags_json[u'zipball_url']

url = urllib2.urlopen(ziplink)
with ZipFile(StringIO(url.read())) as zf:
    zf.printdir()
    sys.exit()
    for member in zf.infolist():
        zf.extract(member)

# names = zip_file.namelist()

# for name in names:
#     for fil in filterfiles:
#         if fil not in name:
#             newname = "/".join(name.split('/')[1:])
#             if newname.endswith('/'):
#                 os.makedirs(os.path.normpath(newname))
#             elif len(newname) > 0:
#                 file(os.path.normpath(newname), 'wb').write(zip_file.read(name))
