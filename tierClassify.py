from sklearn import tree
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
import numpy as np
import random
from sklearn.externals.six import StringIO  
import pydot
import pickle

tiers = ['bronze', 'silver', 'gold', 'platinum','diamond']

labels = [item for item in open('DataMininingHeaderFin.csv').read().strip().split(',')]
modelDict = {}
avgDict = {}
for tier in tiers:
	tierFile = tier+'Matches.csv'
	inFile = open(tierFile, 'r')
	rawData = []
	for line in inFile:
		l = line.strip().split(',')
		l = map(float, l)
		rawData.append(l)

	maxes = np.zeros(len(rawData[0]))
	avg = np.zeros(len(rawData[0])-23)
	print "Normalizing data..."
	for match in rawData:
		for i in range(len(match)):
			if match[i] > maxes[i]:
				maxes[i] = match[i]
	for match in rawData:
		avg += np.array(match[23:])
		for i in range(len(match)):
			if maxes[i] != 0:
				match[i] = match[i] / maxes[i]
	avg = np.divide(avg,len(rawData))

	print "Training for %s..." % (tier)
	maxval = 0
	for i in range(10):
		random.shuffle(rawData)
		trainClass = []
		trainData = []
		testClass = []
		testData = []
		for i in range(len(rawData)):
			if i%10 == 0:
				testClass.append(rawData[i][0])
				testData.append(rawData[i][23:])
			else:
				trainClass.append(rawData[i][0])
				trainData.append(rawData[i][23:])
		trainClass = np.array(trainClass)
		trainData = np.array(trainData)
		testClass = np.array(testClass)
		testData = np.array(testData)

		# model = SVC(probability=False)
		# model.fit(trainData, trainClass)
		model = tree.DecisionTreeClassifier()
		model.fit(trainData, trainClass)
		# model = GaussianNB()
		# model.fit(trainData, trainClass)
		score = model.score(testData, testClass)
		# res = model.predict_proba(testData[0])
		if score > maxval:
			modelDict[tier] = model
			maxval = score
		print score
	print "Max score for %s: %f" % (tier, maxval)
	if tier == 'bronze':
		pickle.dump(avg, open('avg', 'w'))

pickle.dump(modelDict, open('model', 'w'))

# for tier in tiers:
# 	dot_data = StringIO() 
# 	tree.export_graphviz(modelDict[tier], out_file=dot_data, feature_names=labels) #class_names = list_of_names
# 	graph = pydot.graph_from_dot_data(dot_data.getvalue()) 
# 	graph.write_pdf(tier+"tree_w_names.pdf") 

# 	dot_data = StringIO() 
# 	tree.export_graphviz(modelDict[tier], out_file=dot_data) #class_names = list_of_names
# 	graph = pydot.graph_from_dot_data(dot_data.getvalue()) 
# 	graph.write_pdf(tier+"tree_no_names.pdf") 