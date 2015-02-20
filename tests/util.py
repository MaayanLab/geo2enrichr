import json


def toJSON(respOrFile):
	if type(respOrFile) is str:
		j = json.load(file('tests/data/' + respOrFile, 'r'))
		if type(j) is not str:
			return json.dumps(j)
	else:
		return json.loads(respOrFile.data)
