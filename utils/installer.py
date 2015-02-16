from StringIO import StringIO
from zipfile import ZipFile
from urllib import urlopen
import os, sys, shutil

filterfiles = ['.gitignore','utils','.git','todo','ingredients']

url = urlopen("https://github.com/aaps/stardog/archive/v0.6.1.zip")
zipfile = ZipFile(StringIO(url.read()))
names = zipfile.namelist()
	

for name in names:
	
	for fil in filterfiles:
		if not fil in name:
			newname = "/".join(name.split('/')[1:])
			if newname.endswith('/'):
				os.makedirs(os.path.normpath(newname))
			elif len(newname) > 0:
				file(os.path.normpath(newname), 'wb').write(zipfile.read(name))

