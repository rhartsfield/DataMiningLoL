from cassiopeia import riotapi
import csv
import argparse
import parseMatch

'''
Please set your own API key below this comment before using.
This should be run from the command line with the proper arguments outline below.
Two files will be created, one for summoner objects, the other for match objects.
This should be able to handle very large thresholds, just remember that you will
end up with (hopefully) threshold*10 matches with occasional failed pulls.
'''

riotapi.set_region("NA")
riotapi.set_api_key("bf735671-a14a-4c52-8e02-ed476b7f8434")
riotapi.set_rate_limits((10, 10), (500, 600))
global QUEUES
QUEUES = ["RANKED_TEAM_5x5", "RANKED_SOLO_5x5", "RANKED_PREMADE_5x5"]

def amassSummoners(targetLeague, seedSummoner, returnDict, threshold=10):
	'''Will take a target league and a starting seed and use the seed to do a branching
	   search for summoners that have reached the target league.
	   If threshold not met, runs recursively on a random summoner already found.
	   Returns a dict of summoner objects {Summoner name : Summoner object}
	'''
	if (type(seedSummoner) == str):
		print "Searching for summoners related to %s..." % (seedSummoner)
		seed = riotapi.get_summoner_by_name(seedSummoner)
	else:
		print "Searching for summoners related to %s..." % (seedSummoner.name)
		seed = seedSummoner
	matchList = riotapi.get_match_list(seed, ranked_queues=QUEUES, seasons="SEASON2015")
	counter = 0
	summonerDict = returnDict
	for i in range(len(matchList)):	
		try:	#Had issues with get_match request failing so wrapped in a try block
			currentMatch = riotapi.get_match(matchList[i])
			for participant in currentMatch.participants:
				try:
					if (participant.previous_season_tier.name == targetLeague) & (participant.summoner_name not in summonerDict):
						summonerDict[participant.summoner_name] = participant.summoner
						counter += 1
						print "##### Target found ######"
				except ValueError:
					continue
			if counter >= 5: break  	#Break after 10 summoners grabbed to increase spread
		except:
			print "Summoner pull failed."
	if len(summonerDict.keys()) < threshold:
		print "Current no. of summoners in %s: %d" % (targetLeague, len(summonerDict.keys()))
		summonList = summonerDict.values()
		summonerDict = amassSummoners(targetLeague, summonList[counter/2], summonerDict)
	return summonerDict

def collectMatches(targetLeague, summonerList):
	'''Given a list of summoner objects and a target league, will search through the match
	   history of each summoner for games where the majority of participants are in the 
	   target league. If found, adds to the matchDict. Will only pull 10 games per summoner
	   Returns a dict of Match objects { MatchID : Match Object}
	'''
	matchDict = {}
	for i in range(len(summonerList)):
		print "--------------------------------"
		counter = 0
		searched = 100
		try:
			matchList = riotapi.get_match_list(summonerList[i], num_matches=100, ranked_queues=QUEUES, seasons="SEASON2015")
		except:
			continue
		print "Looking at %s's match history..." % (summonerList[i].name)
		for i in range(len(matchList)):
			try:
				currentMatch = riotapi.get_match(matchList[i])
				majorityDict = {'unranked':0, 'bronze':0, 'silver':0, 'gold':0, 'platinum':0, 'diamond':0, 'master':0, 'challenger':0}
				for participant in currentMatch.participants:
					try:
						majorityDict[participant.previous_season_tier.name] += 1
					except ValueError:
						majorityDict['bronze'] += 1
				if (majorityDict[targetLeague] > 3) & (currentMatch.id not in matchDict):
					matchDict[currentMatch.id] = parseMatch.processMatch(currentMatch)
					counter += 1
				if counter == 10:		#Break after 10 games retrieved
					searched = i+1
					break
			except:
				print "Match pull failed."
		print "%d found out of %d searched" % (counter, searched)
		print "Current no. of %s matches: %d" % (targetLeague, len(matchDict.values()))
	return matchDict




if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='LoL API Data Gathering')
	parser.add_argument('-l', type=str, help="Target league {bronze, silver, gold, platinum, diamond", required=True)
	parser.add_argument('-s', type=str, help="Initial summoner name for seed", required=False)
	args = parser.parse_args()

	if ( args.l and args.s ):
		targetLeague = args.l.lower()
		seedSummoner = args.s
	elif ( args.l ):
		sessionLeague = args.l
		seedSummoner = "Applecrispy"
	else:
		print "Provide input in following form:\n -l <leaguename> -s <seedsummoner>"
	
	matchFileName = "%sMatches.csv" % (targetLeague)
	
	#Build up a list of summoners
	targetSummoners = amassSummoners(targetLeague, seedSummoner, {})
	summonerList = targetSummoners.values()
	print "Number of summoners mined: %d" % (len(summonerList))

	#Use that list to collect matches
	print "Looking up matches..."
	targetMatches = collectMatches(targetLeague, summonerList)
	matchList = targetMatches.values()
	print "Number of matches mined: %d" % (len(matchList))

	#for Python3, delete the b and add newline="" I think?
	with open(matchFileName, 'wb') as f:
		writer = csv.writer(f)
		writer.writerows(matchList)
