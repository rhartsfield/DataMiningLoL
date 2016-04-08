from cassiopeia import riotapi
import parseMatch
import pickle
import numpy as np


riotapi.set_region("NA")
riotapi.set_api_key("bf735671-a14a-4c52-8e02-ed476b7f8434")
riotapi.set_rate_limits((10, 10), (500, 600))

# testFile = pickle.load(open('testMatches.txt'))

global QUEUES, BACKUP
QUEUES = ["RANKED_TEAM_5x5", "RANKED_SOLO_5x5", "RANKED_PREMADE_5x5", 'TEAM_BUILDER_DRAFT_RANKED_5x5']
# BACKUP = ['NORMAL_5x5_BLIND', 'NORMAL_5x5_DRAFT']

'''
TODO: Retool so that the functions are able to work with both a participant and
currentGame participant object: For use with currentMatchObject
Will need to set up a role prediction method:
Build a dict of {champ:[role1, role2]} and  if (len(dict[champ]) > 1):
disambiguate with sumomner spells
'''
roleCorr = {'Sup':'support', 'Top':'solo', 'Mid':'solo', 'Jung':'none', 'ADC':'carry'}
laneCorr = {'Sup':'bot_lane', 'Top':'top_lane', 'Mid':'mid_lane', 'Jung':'jungle', 'ADC':'bot_lane'}

def averageMatches(participant, matchList):
	length = 5
	statVector = np.zeros(63)
	pulled = 0
	for matchRef in matchList:
		try:
			match = matchRef.match(include_timeline=True)
		except:
			print 'Match pull from reference failed.'
		hold = statVector
		try:
			for p in match.participants:
				if p.summoner.id == participant.summoner.id:
					statVector = np.add(statVector, np.array(parseMatch.getPStats(p, match)))
					pulled += 1
					break
		except AttributeError:
			print 'Match parse failed.'
			statVector = hold
		if pulled > length-1:
			break
	return np.divide(statVector, pulled)

def getAvgPerformance(participant, guessedRole=""):
	champ = participant.champion
	if guessedRole != "":
		role = roleCorr[guessedRole]
		lane = laneCorr[guessedRole]
	else:
		role = participant.timeline.role.name
		lane = participant.timeline.lane.name
	matchList = riotapi.get_match_list(participant.summoner, num_matches=10, ranked_queues=QUEUES, champions=champ, seasons=["SEASON2015", 'SEASON2016'])
	if len(matchList) < 5:
		print 'Not enough matches found as %s for %s.' % (champ, participant.summoner_name)
		print 'Searching for other games as %s %s' % (role, lane)
		modList = []
		count = 0
		matchList = riotapi.get_match_list(participant.summoner, num_matches=100, ranked_queues=QUEUES, seasons=["SEASON2015", 'SEASON2016'])
		for match in matchList:
			if (match.role.name == role) and match.lane.name == lane:
				count += 1
				modList.append(match)
			if count > 20:
				break
		matchList = modList
	if len(matchList) == 0:
		print 'No ranked data found for %s' % (participant.summoner_name)
		print 'Looking at all games...'
		matchList = riotapi.get_match_list(participant.summoner, num_matches=100, ranked_queues=QUEUES, seasons=["SEASON2015", 'SEASON2016'])
		print len(matchList)
	if len(matchList) == 0:
		print len(matchList)
		return None
	return averageMatches(participant, matchList)

# print getAvgPerformance(testFile[0].participants[1])