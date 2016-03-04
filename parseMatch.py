from cassiopeia import riotapi

def getWinner(match):
	#Return winner of the match
	if match.blue_team.data.winner:
		return 0
	else:
		return 1

def getRoles(match):
	'''Return a dict with the following setup:
	{'teamPosition': idNum}
	'''
	roleMap = {}

	#Take care of the duo lanes where sup can't be auto determined
	#Base this on CS value
	blueDuo = []
	for p in match.blue_team.participants:
		if p.timeline.role.name == 'duo':
			blueDuo.append(p)
	redDuo = []
	for p in match.red_team.participants:
		if p.timeline.role.name == 'duo':
			redDuo.append(p)
	if blueDuo:
		if blueDuo[0].stats.data.minionsKilled > blueDuo[1].stats.data.minionsKilled:
			roleMap['blueADC'] = blueDuo[0].id
			roleMap['blueSup'] = blueDuo[1].id
		else:
			roleMap['blueADC'] = blueDuo[1].id
			roleMap['blueSup'] = blueDuo[0].id
	if redDuo:
		if redDuo[0].stats.data.minionsKilled > redDuo[1].stats.data.minionsKilled:
			roleMap['redADC'] = redDuo[0].id
			roleMap['redSup'] = redDuo[1].id
		else:
			roleMap['redADC'] = redDuo[1].id
			roleMap['redSup'] = redDuo[0].id

	#Full dictionary creation step
	for p in match.blue_team.participants:
		if p.timeline.role.name == 'none':
			curRole = p.timeline.lane.name
		else:
			curRole = p.timeline.role.name
			curLane = p.timeline.lane.name
		if curRole == 'jungle':
			roleMap['blueJung'] = p.id
		elif curRole == 'support':
			roleMap['blueSup'] = p.id
		elif curRole == 'duo':
			continue
		elif curRole == 'carry':
			roleMap['blueADC'] = p.id
		else:
			if curLane == 'top_lane':
				roleMap['blueTop'] = p.id
			else:
				roleMap['blueMid'] = p.id
	for p in match.red_team.participants:
		if p.timeline.role.name == 'none':
			curRole = p.timeline.lane.name
		else:
			curRole = p.timeline.role.name
			curLane = p.timeline.lane.name
		if curRole == 'jungle':
			roleMap['redJung'] = p.id
		elif curRole == 'support':
			roleMap['redSup'] = p.id
		elif curRole == 'duo':
			continue			
		elif curRole == 'carry':
			roleMap['redADC'] = p.id
		else:
			if curLane == 'top_lane':
				roleMap['redTop'] = p.id
			else:
				roleMap['redMid'] = p.id
	return roleMap

def getTeamStats(team):
	'''
	Returns a list of the below stats with bool values at
	indexes 2-7 (Should not normalize these same way)
	'''
	return [team.data.baronKills,
			team.data.dragonKills,
			1 if team.data.firstBaron else 0,
			1 if team.data.firstBlood else 0,
			1 if team.data.firstDragon else 0,
			1 if team.data.firstInhibitor else 0,
			1 if team.data.firstRiftHerald else 0,
			1 if team.data.firstTower else 0,
			team.data.inhibitorKills,
			team.data.riftHeraldKills,
			team.data.towerKills,
			]

def checkforZeroes(delta):
	'''
	Pad values for the delta statistics if game ends early
	'''
	tenToTwenty = delta.tenToTwenty
	twentyToThirty = delta.twentyToThirty
	thirtyToEnd = delta.thirtyToEnd
	if twentyToThirty == 0:
		twentyToThirty = tenToTwenty
		thirtyToEnd = tenToTwenty
	elif thirtyToEnd == 0:
		thirtyToEnd = twentyToThirty
	return twentyToThirty, thirtyToEnd

def getPStats(p, matchLen):
	'''
	Anything multiplied by coeff is changed to be 'cs per min'
	Possible None types with the deltas, currently throw these matches out
	If games end early, deltas are padded based on prev delta value
	Indexes 3-8 are bools for future normalization
	'''
	zZ = p.timeline.data
	coeff = 1/matchLen
	csPer20, csPer30 = checkforZeroes(zZ.creepsPerMinDeltas)
	csDiff20, csDiff30 = checkforZeroes(zZ.csDiffPerMinDeltas)
	dmgTakeDiff20, dmgTakeDiff30 = checkforZeroes(zZ.damageTakenDiffPerMinDeltas)
	dmgTakePer20, dmgTakePer30 = checkforZeroes(zZ.damageTakenPerMinDeltas)
	gold20, gold30 = checkforZeroes(zZ.goldPerMinDeltas)
	xpDiff20, xpDiff30 = checkforZeroes(zZ.xpDiffPerMinDeltas)
	xpPer20, xpPer30 = checkforZeroes(zZ.xpPerMinDeltas)

	return	[p.stats.data.assists*coeff,
			p.stats.data.deaths*coeff,
			p.stats.data.doubleKills,
			1 if p.stats.data.firstBloodAssist else 0,
			1 if p.stats.data.firstBloodKill else 0,
			1 if p.stats.data.firstInhibitorAssist else 0,
			1 if p.stats.data.firstInhibitorKill else 0,
			1 if p.stats.data.firstTowerAssist else 0,
			1 if p.stats.data.firstTowerKill else 0,
			p.stats.data.goldEarned*coeff,
			p.stats.data.goldSpent*coeff,
			p.stats.data.killingSprees,
			p.stats.data.kills*coeff,
			p.stats.data.largestKillingSpree,
			p.stats.data.largestMultiKill,
			p.stats.data.magicDamageTaken*coeff,
			p.stats.data.minionsKilled*coeff,
			p.stats.data.neutralMinionsKilled*coeff,
			p.stats.data.neutralMinionsKilledEnemyJungle*coeff,
			p.stats.data.neutralMinionsKilledTeamJungle*coeff,
			p.stats.data.pentaKills,
			p.stats.data.physicalDamageTaken*coeff,
			p.stats.data.quadraKills,
			p.stats.data.sightWardsBoughtInGame*coeff,
			p.stats.data.totalDamageDealt*coeff,
			p.stats.data.totalDamageDealtToChampions*coeff,
			p.stats.data.totalDamageTaken*coeff,
			p.stats.data.totalHeal*coeff,
			p.stats.data.totalTimeCrowdControlDealt*coeff,
			p.stats.data.totalUnitsHealed*coeff,
			p.stats.data.towerKills*coeff,
			p.stats.data.visionWardsBoughtInGame*coeff,
			p.stats.data.wardsKilled*coeff,
			p.stats.data.wardsPlaced*coeff,
			zZ.creepsPerMinDeltas.zeroToTen,
			zZ.creepsPerMinDeltas.tenToTwenty,
			csPer20,
			csPer30,
			zZ.csDiffPerMinDeltas.zeroToTen,
			zZ.csDiffPerMinDeltas.tenToTwenty,
			csDiff20,
			csDiff30,
			zZ.damageTakenDiffPerMinDeltas.zeroToTen,
			zZ.damageTakenDiffPerMinDeltas.tenToTwenty,
			dmgTakeDiff20,
			dmgTakeDiff30,
			zZ.damageTakenPerMinDeltas.zeroToTen,
			zZ.damageTakenPerMinDeltas.tenToTwenty,
			dmgTakePer20,
			dmgTakePer30,
			zZ.goldPerMinDeltas.zeroToTen,
			zZ.goldPerMinDeltas.tenToTwenty,
			gold20,
			gold30,
			zZ.xpDiffPerMinDeltas.zeroToTen,
			zZ.xpDiffPerMinDeltas.tenToTwenty,
			xpDiff20,
			xpDiff30,
			zZ.xpPerMinDeltas.zeroToTen,
			zZ.xpPerMinDeltas.tenToTwenty,
			xpPer20,
			xpPer30
			]

def processMatch(match):
	'''
	Returns a list with attributes arranged as following:
	[class, blue_team, red_team, blue_players(Top, Mid, Jungle, ADC, Sup), red_players(Top, Mid, Jungle, ADC, Sup)]
	'''
	winClass = getWinner(match)
	roleMap = getRoles(match)
	blueStats = getTeamStats(match.blue_team)
	redStats = getTeamStats(match.red_team)
	statMap = {}
	matchLen = match.duration.total_seconds()/60
	for p in match.participants:
		curId = p.id
		curList = getPStats(p, matchLen)
		statMap[curId] = curList
	final = 	([winClass]+blueStats+redStats+statMap[roleMap['blueTop']]+
				statMap[roleMap['blueMid']]+statMap[roleMap['blueJung']]+
				statMap[roleMap['blueSup']]+statMap[roleMap['blueADC']]+
				statMap[roleMap['redTop']]+statMap[roleMap['redMid']]+
				statMap[roleMap['redJung']]+statMap[roleMap['redSup']]+
				statMap[roleMap['redADC']])
	return final