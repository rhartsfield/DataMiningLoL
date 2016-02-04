from cassiopeia import riotapi

riotapi.set_region("NA")
riotapi.set_api_key("bf735671-a14a-4c52-8e02-ed476b7f8434")
riotapi.set_rate_limits((10, 10), (500, 600))
global QUEUES
QUEUES = ["RANKED_TEAM_5x5", "RANKED_SOLO_5x5", "RANKED_PREMADE_5x5"]

def writeMatches(outfile, summoner, num=100, queues=QUEUES, seasons="SEASON2015"):
	matchList = riotapi.get_match_list(summoner, num_matches=num, ranked_queues=queues, seasons=season)
	for i in range(len(matchList)):
		current = riotapi.get_match(matchList[i])
		print "Writing data for %d" % (current.id)
		outfile.write(current.to_json())

summoner = riotapi.get_summoner_by_name("Applecrispy")
matchList = riotapi.get_match_list(summoner, ranked_queues=QUEUES, seasons="SEASON2015")

outFile = open('matches.txt', 'a')
writeMatches(outFile, summoner)
gold = 0
gold_part = []
for i in range(len(matchList)):
	current = riotapi.get_match(matchList[i])
	# for player in current.participants:
	# 	try:
	# 		if (player.previous_season_tier.name == "gold"):
	# 			gold_part.append(player)
	# 			gold += 1
	# 			print "##### Gold found ######"
	# 	except ValueError:
	# 		print "unranked"
	# if gold > 10:
	# 	break

# for player in gold_part:
# 	outFile.write(player.summoner.to_json())
# 	outFile.write('\n')
outFile.close()