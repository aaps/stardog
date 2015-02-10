from StringIO import StringIO
from zipfile import ZipFile
from urllib import urlopen
import os, sys, shutil
import imp


url = urlopen("https://github.com/aaps/stardog/archive/master.zip")
zipfile = ZipFile(StringIO(url.read()))


names = zipfile.namelist()
	
for name in names:

	newname = "/".join(name.split('/')[1:])
	if newname.endswith('/'):
		os.makedirs(os.path.normpath(newname))
	elif len(newname) > 0:
		file(os.path.normpath(newname), 'wb').write(zipfile.read(name))




# try:
#     imp.find_module('eggs')
#     found = True
# except ImportError:
#     found = False

