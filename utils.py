import os

def getTempDir():
	import tempfile
	return tempfile.gettempdir()+os.sep
