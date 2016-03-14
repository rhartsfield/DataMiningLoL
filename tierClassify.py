from sklearn.linear_model import Perceptron
from sklearn import tree
import numpy as np
import random
from sklearn.externals.six import StringIO  
import pydot 

inFile = open('goldMatches.csv', 'r')

tiers = ['bronze', 'silver', 'gold', 'platinum','diamond']
# for tier in tiers:
# 	tierFile = tier+'Matches.csv'
# 	inFile = open(tierFile, 'r')

rawData = []

'''
Index 0 = Class
--------------------------
Index 1-11 = Blue Team			CUT THESE
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
for line in inFile:
	l = line.strip().split(',')
	l = map(float, l)
	rawData.append(l)

for i in range(10):
	random.shuffle(rawData)
	trainClass = []
	trainData = []
	testClass = []
	testData = []
	for i in range(len(rawData)):
		if i%10 == 0:
			testClass.append(rawData[i][0])
			testData.append(rawData[i][23:)
		else:
			trainClass.append(rawData[i][0])
			trainData.append(rawData[i][23:)

	trainClass = np.array(trainClass)
	trainData = np.array(trainData)
	testClass = np.array(testClass)
	testData = np.array(testData)

	model1 = tree.DecisionTreeClassifier(max_depth=4)
	model1.fit(trainData, trainClass)
	print model1.score(testData, testClass)


dot_data = StringIO() 
tree.export_graphviz(model, out_file=dot_data) 
graph = pydot.graph_from_dot_data(dot_data.getvalue()) 
graph.write_pdf("tree.pdf") 