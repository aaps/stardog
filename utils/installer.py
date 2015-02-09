import zipfile, os, sys

zfile = zipfile.ZipFile(sys.argv[1])
zfile.extractall()