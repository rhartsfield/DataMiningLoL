from sklearn import tree
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
import numpy as np
import random
from sklearn.externals.six import StringIO  
import pydot
import pickle

inFile = open('goldMatches.csv', 'r')

tiers = ['bronze', 'silver', 'gold', 'platinum','diamond']
# for tier in tiers:
# 	tierFile = tier+'Matches.csv'
# 	inFile = open(tierFile, 'r')
labels = [item for item in open('DataMininingHeaderFin.csv').read().strip().split(',')]
rawData = []
print len(labels)
'''
Numbers No Longer Accurate

Index 0 = Class
--------------------------
Index 1-11 = Blue Team	
Index 12-22 = Red Team
--------------------------
Index 23-84 = Blue Top
Index 85-146 = Blue Mid
Index 147-208 = Blue Jung
Index 209-270 = Blue Sup
Index 271-332 = Blue ADC
--------------------------
Index 333-394 = Red Top
Index 395-456 = Red Mid
Index 457-518 = Red Jung
Index 519-580 = Red Sup
Index 581-642 = Red ADC
'''

''' TODO:
Import the cluster data for each tier, find average outlier percent based on role
Fill each stat vector with the average
Can then extract from match history in prediction phase
Not enough variation to matter in model, need to be done in processing
'''

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
print "Training..."
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
		returnModel = model
	print score

pickle.dump(returnModel, open('model', 'w'))
# pickle.dump(avg, open('avg', 'w'))
dot_data = StringIO() 
tree.export_graphviz(model, out_file=dot_data, feature_names=labels) #class_names = list_of_names
graph = pydot.graph_from_dot_data(dot_data.getvalue()) 
graph.write_pdf("tree.pdf") 