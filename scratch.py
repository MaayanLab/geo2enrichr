

# app.py
def dlgeo():
	args = Request(flask.request.json)
	# The SoftFile class handles "to dict"-ing itself.
	sf   = SoftFile(args.accession)
	return sf.data


# files.py
class SoftFile(object):

	def __init__(self, name, data=None):
		if data is not None:
			self.name = name
			self.data = data
			return

		# Check if file exists on hard disk
		import os.path
		if not os.path.isfile(name):
			raw_data = geodownloader.download(name)
			self.name = name
		self.data = softparser(raw_data)

