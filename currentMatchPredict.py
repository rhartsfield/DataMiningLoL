from cassiopeia import riotapi
from sklearn.linear_model import Perceptron
from sklearn import svm
import format
import pickle
import avgPerformance

champDict = {}
for line in open('dictionary.txt'):
	l = line.strip().split(',')
	champ = l[0]
	l.remove(champ)
	champDict[champ] = l

def getTeam(match, teamcolor):
	teamList = []
	for p in match.participants:
		if p.side.name == teamcolor:
			teamList.append(p)
	return teamList

def getAvg():
	return pickle.load(open('avg'))

def rolePredict(match):
	#return a list of tuples (p, role)
	roleList = []
	possibleBlueRoles = ['Top', 'Mid', 'Sup', 'Jung', 'ADC']
	possibleRedRoles = ['Top', 'Mid', 'Sup', 'Jung', 'ADC']
	assigned = []
	redTeam = getTeam(match, 'red')
	blueTeam = getTeam(match, 'blue')
	teamList = [blueTeam, redTeam]
	n=0
	while len(redTeam) > 0:
		for p in redTeam:
			champ = p.champion.name
			role = champDict[champ]
			# print champ, p.data.spell1Id, p.data.spell2Id
			for r in assigned:
				if r in role:
					role.remove(r)
			if len(role) == 1:
				roleList.append((p, role[0]))
				possibleRedRoles.remove(role[0])
				redTeam.remove(p)
				assigned.append(role[0])
			else:
				if len(possibleRedRoles) == 1:
					roleList.append((p, possibleRedRoles[0]))
					assigned.append(possibleRedRoles[0])
					possibleRedRoles = []
					redTeam.remove(p)
				elif (p.data.spell1Id == 11) or (p.data.spell2Id == 11):
					roleList.append((p, 'Jung'))
					possibleRedRoles.remove('Jung')
					redTeam.remove(p)
					assigned.append('Jung')
				elif (p.data.spell1Id == 7) or (p.data.spell2Id == 7):
					if 'ADC' in possibleRedRoles:
						roleList.append((p, 'ADC'))
						possibleRedRoles.remove('ADC')
						redTeam.remove(p)
						assigned.append('ADC')
		if n > 10:
			break
		n += 1
	n=0
	assigned = []
	while len(blueTeam) > 0:
		for p in blueTeam:
			champ = p.champion.name
			role = champDict[champ]
			# print champ, p.data.spell1Id, p.data.spell2Id
			for r in assigned:
				if r in role:
					role.remove(r)
			if len(role) == 1:
				roleList.append((p, role[0]))
				possibleBlueRoles.remove(role[0])
				blueTeam.remove(p)
				assigned.append(role[0])
			else: #spell inference
				if len(possibleBlueRoles) == 1:
					roleList.append((p, possibleBlueRoles[0]))
					assigned.append(possibleBlueRoles[0])
					possibleBlueRoles = []
					blueTeam.remove(p)
				elif (p.data.spell1Id == 11) or (p.data.spell2Id == 11):
					roleList.append((p, 'Jung'))
					possibleBlueRoles.remove('Jung')
					blueTeam.remove(p)
					assigned.append('Jung')
				elif (p.data.spell1Id == 7) or (p.data.spell2Id == 7):
					if 'ADC' in possibleBlueRoles:
						roleList.append((p, 'ADC'))
						possibleBlueRoles.remove('ADC')
						blueTeam.remove(p)
						assigned.append('ADC')
		if n > 10:
			break
		n += 1
	return roleList

def allRoles(match):
	roleDict = {}
	roles = rolePredict(match)
	for pair in roles:
		p = pair[0]
		roleDict[p] = pair[1]
	return roleDict

def fetchModel(match):
	return pickle.load(open('model'))

def getCurrentMatch(summonerName, region="NA"):
	riotapi.set_region(region)
	summoner = riotapi.get_summoner_by_name(summonerName)
	match = riotapi.get_current_game(summoner)
	if match is None:
		return None
	roleMap = allRoles(match)
	# for x in roleMap:
	# 	print x.champion.name, x.side.name, roleMap[x]
	if len(roleMap.keys()) < 10:
		print "Role confusion!"
		return None
	statMap = {}
	rankMap = {}
	nonNormMap = {}
	for p in match.participants:
		role = roleMap[p]
		stats, nonNorm, rank = avgPerformance.getAvgPerformance(p, role)
		if stats is None:
			#currently filling with avg gold?
			stats = getAvg()
			rank = "unranked"
		statMap[p.side.name+role] = list(stats)
		rankMap[p] = rank
		nonNormMap[p] = nonNorm
		print p.summoner_name, p.side.name+role
	statVector = (statMap['blueTop']+statMap['blueMid']+statMap['blueJung']+
				statMap['blueSup']+statMap['blueADC']+statMap['redTop']+
				statMap['redMid']+statMap['redJung']+statMap['redSup']+
				statMap['redADC'])
	model = fetchModel(match)
	results = model.predict_proba(statVector)
	return format.prepareReturn(roleMap, rankMap, nonNormMap, results, match)

print getCurrentMatch('Shintopher')