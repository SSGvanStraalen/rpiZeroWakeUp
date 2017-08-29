import json

class DataPersistor:

	def saveData(fileName, data):
		with open(fileName, 'w') as outfile:
	 		json.dump(data, outfile)
	def loadData(fileName):
		with open(fileName) as infile:
			return json.load(infile)
