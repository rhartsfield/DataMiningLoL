import avgPerformance, parseMatch
import numpy as np
from cassiopeia import riotapi
import pickle

def getAvg(role):
	avg = pickle.load(open('avg'))
	if role == "blueTop":
		return avg[0:63]
	if role == "blueMid":
		return avg[63:126]
	if role == "blueJung":
		return avg[126:189]
	if role == "blueSup":
		return avg[189:252]
	if role == "blueADC":
		return avg[252:315]
	if role == "redTop":
		return avg[315:378]
	if role == "redMid":
		return avg[378:441]
	if role == "redJung":
		return avg[441:504]
	if role == "redSup":
		return avg[504:567]
	if role == "redADC":
		return avg[567:630]


riotapi.set_region("NA")
riotapi.set_api_key("bf735671-a14a-4c52-8e02-ed476b7f8434")
riotapi.set_rate_limits((10, 10), (500, 600))
global QUEUES
QUEUES = ["RANKED_TEAM_5x5", "RANKED_SOLO_5x5", "RANKED_PREMADE_5x5"]

summonerNames = ["Blazed Aldrin", "Tahola", "Smoakee", "NSCrafting", "ZSlayer93", "Shintopher"]
matchList = []
for name in summonerNames:
	summoner = riotapi.get_summoner_by_name(name)
	matchList += riotapi.get_match_list(summoner, ranked_queues=QUEUES)[:25]
correct = 0.0
total = 0.0
blueGuess = 0.0
redGuess = 0.0
model = pickle.load(open('model'))['gold']

for i in range(len(matchList)):
	try:
		testMatch = matchList[i].match(include_timeline=True)
	except:
		continue
	matchClass = parseMatch.getWinner(testMatch)
	roleMap = parseMatch.getRoles(testMatch)
	inv_map = {v: k for k, v in roleMap.items()}
	statMap = {}
	for p in testMatch:
		try:
			stats, webStats, rank = avgPerformance.getAvgPerformance(p)
		except:
			stats = getAvg(inv_map[p.id])
			print len(stats)
		statMap[p.id] = list(stats)
		print p.summoner_name
	try:
		statVector = (statMap[roleMap['blueTop']]+statMap[roleMap['blueMid']]+statMap[roleMap['blueJung']]+
					statMap[roleMap['blueSup']]+statMap[roleMap['blueADC']]+statMap[roleMap['redTop']]+
					statMap[roleMap['redMid']]+statMap[roleMap['redJung']]+statMap[roleMap['redSup']]+
					statMap[roleMap['redADC']])
	except KeyError as c:
		print c
		continue
	results = model.predict(statVector)
	guessClass = results	#for SVM
	# if results[0][0] > results[0][1]:
	# 	guessClass = 0
	# else:
	# 	guessClass = 1
	if guessClass == 0:
		blueGuess += 1
	else:
		redGuess += 1
	if matchClass == guessClass:
		correct += 1
	total += 1
	print "Real winner is %d" % (matchClass)
	print "Guessed winner is %d" % (guessClass)
	perCor = correct/total
	print "Current Accuracy after %d matches: %%%.2f" % (total, perCor*100)
	print "Has guessed blue %%%.2f of the time." % (blueGuess/total * 100)
	print "Has guessed red %%%.2f of the time." % (redGuess/total * 100)

perCor = correct/total
print "=================================="
print "Final Prediction Accuracy: %%%.2f" % (perCor*100)