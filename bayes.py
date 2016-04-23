from sklearn.naive_bayes import GaussianNB
import numpy as np
import random
import pickle

def editRaws(rawData):
	'''Slice out the attributes we don't want to look at'''
	newRaw = []
	for match in rawData:
		newRaw.append(match[23:])
	return newRaw

inFile = open('goldMatches.csv', 'r')
rawData = []

for line in inFile:
	l = line.strip().split(',')
	l = map(float, l)
	rawData.append(l)

rawData = editRaws(rawData)
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


	model = GaussianNB()
	model.fit(trainData, trainClass)
	score = model.score(testData, testClass)
	if score > maxval:
		returnModel = model
	print score
	print np.max(model.predict_proba(testData[0]))

pickle.dump(returnModel, open('model', 'w'))
# pickle.dump(avg, open('avg', 'w'))