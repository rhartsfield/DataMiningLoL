from cassiopeia import riotapi

def getWinner(match):
	if match.blue_team.data.winner:
		return match.blue_team.data.teamId
	else:
		return match.red_team.data.teamId

def getRoles(match):
	'''Return a dict with the following setup:
	{'teamPosition': idNum}
	'''
	roleMap = {}

	#Take care of the duo lanes where sup can't be auto determined
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

def getPStats(p, matchLen):
	'''
	Anything multiplied by coeff is changed to be 'cs per min'
	Possible None types with the deltas, currently throw these matches out
	Indexes 3-8 are bools for future normalization
	'''
	coeff = 1/matchLen
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
			p.timeline.data.creepsPerMinDeltas.zeroToTen,
			p.timeline.data.creepsPerMinDeltas.tenToTwenty,
			p.timeline.data.creepsPerMinDeltas.twentyToThirty,
			p.timeline.data.creepsPerMinDeltas.thirtyToEnd,
			p.timeline.data.csDiffPerMinDeltas.zeroToTen,
			p.timeline.data.csDiffPerMinDeltas.tenToTwenty,
			p.timeline.data.csDiffPerMinDeltas.twentyToThirty,
			p.timeline.data.csDiffPerMinDeltas.thirtyToEnd,
			p.timeline.data.damageTakenDiffPerMinDeltas.zeroToTen,
			p.timeline.data.damageTakenDiffPerMinDeltas.tenToTwenty,
			p.timeline.data.damageTakenDiffPerMinDeltas.twentyToThirty,
			p.timeline.data.damageTakenDiffPerMinDeltas.thirtyToEnd,
			p.timeline.data.damageTakenPerMinDeltas.zeroToTen,
			p.timeline.data.damageTakenPerMinDeltas.tenToTwenty,
			p.timeline.data.damageTakenPerMinDeltas.twentyToThirty,
			p.timeline.data.damageTakenPerMinDeltas.thirtyToEnd,
			p.timeline.data.goldPerMinDeltas.zeroToTen,
			p.timeline.data.goldPerMinDeltas.tenToTwenty,
			p.timeline.data.goldPerMinDeltas.twentyToThirty,
			p.timeline.data.goldPerMinDeltas.thirtyToEnd,
			p.timeline.data.xpDiffPerMinDeltas.zeroToTen,
			p.timeline.data.xpDiffPerMinDeltas.tenToTwenty,
			p.timeline.data.xpDiffPerMinDeltas.twentyToThirty,
			p.timeline.data.xpDiffPerMinDeltas.thirtyToEnd,
			p.timeline.data.xpPerMinDeltas.zeroToTen,
			p.timeline.data.xpPerMinDeltas.tenToTwenty,
			p.timeline.data.xpPerMinDeltas.twentyToThirty,
			p.timeline.data.xpPerMinDeltas.thirtyToEnd
			]

def processMatch(match):
	'''
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
	winClass = 0 if winClass == 100 else 1
	final = 	([winClass]+blueStats+redStats+statMap[roleMap['blueTop']]+
				statMap[roleMap['blueMid']]+statMap[roleMap['blueJung']]+
				statMap[roleMap['blueSup']]+statMap[roleMap['blueADC']]+
				statMap[roleMap['redTop']]+statMap[roleMap['redMid']]+
				statMap[roleMap['redJung']]+statMap[roleMap['redSup']]+
				statMap[roleMap['redADC']])
	return final