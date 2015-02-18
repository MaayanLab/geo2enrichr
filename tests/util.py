import json


def toJSON(respOrFile):
	if type(respOrFile) is str:
		return json.load(file('tests/data/' + respOrFile, 'r'))
	else:
		return json.loads(respOrFile.data)
