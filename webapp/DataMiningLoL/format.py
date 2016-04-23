import numpy as np

def prepareReturn(roleMap, rankMap, nonNormMap, prediction, match):
	'''Want to return a dictionary / JSON object with the form:
	(Winner, Win%, {blueTop: (SumName, Champ, Rank, AvgPerformance)}...)
	StatIndexes: Kills, Deaths, Assists, CS, Gold, WardsPlaced
	'''
	player = 0
	if prediction[0][0] > prediction[0][1]:
		winner = 'Blue'
	else:
		winner = 'Red'
	percent = np.max(prediction)
	assignDict = {}
	for p in match.participants:
		role = roleMap[p]
		rank = rankMap[p]
		side = p.side.name
		summoner = p.summoner_name
		champion = p.champion.name
		stats = nonNormMap[p]
		assists = stats[0]
		deaths = stats[1]
		gold = stats[2]
		kills = stats[3]
		cs = stats[4]
		wards = stats[5]
		assignDict[side+role] = [summoner, champion, rank, kills, deaths, assists, gold, cs, wards]

	return {"matchData": {
							"winner": "winner",
							"winPercent": "51",
							"playerData": {
									"redTop": {
										"summoner": "summoner",
										"champion": "Ahri",
										"rank": "rank",
										"kills": "3",
										"deaths": "4",
										"assists": "5",
										"gold": "100",
										"cs": "8",
										"wards": "12"
									},
									"redMid": {
										"summoner": "summoner",
										"champion": "Ahri",
										"rank": "rank",
										"kills": "3",
										"deaths": "4",
										"assists": "5",
										"gold": "100",
										"cs": "8",
										"wards": "12"
									},
									"redJung": {
										"summoner": "summoner",
										"champion": "Ahri",
										"rank": "rank",
										"kills": "3",
										"deaths": "4",
										"assists": "5",
										"gold": "100",
										"cs": "8",
										"wards": "12"
									},
									"redADC": {
										"summoner": "summoner",
										"champion": "Ahri",
										"rank": "rank",
										"kills": "3",
										"deaths": "4",
										"assists": "5",
										"gold": "100",
										"cs": "8",
										"wards": "12"
									},
									"redSup": {
										"summoner": "summoner",
										"champion": "Ahri",
										"rank": "rank",
										"kills": "3",
										"deaths": "4",
										"assists": "5",
										"gold": "100",
										"cs": "8",
										"wards": "12"
									},
									"blueTop": {
										"summoner": "summoner",
										"champion": "Ahri",
										"rank": "rank",
										"kills": "3",
										"deaths": "4",
										"assists": "5",
										"gold": "100",
										"cs": "8",
										"wards": "12"
									},
									"blueMid": {
										"summoner": "summoner",
										"champion": "Ahri",
										"rank": "rank",
										"kills": "3",
										"deaths": "4",
										"assists": "5",
										"gold": "100",
										"cs": "8",
										"wards": "12"
									},
									"blueJung": {
										"summoner": "summoner",
										"champion": "Ahri",
										"rank": "rank",
										"kills": "3",
										"deaths": "4",
										"assists": "5",
										"gold": "100",
										"cs": "8",
										"wards": "12"
									},
									"blueADC": {
										"summoner": "summoner",
										"champion": "Ahri",
										"rank": "rank",
										"kills": "3",
										"deaths": "4",
										"assists": "5",
										"gold": "100",
										"cs": "8",
										"wards": "12"
									},
									"blueSup": {
										"summoner": "summoner",
										"champion": "Ahri",
										"rank": "rank",
										"kills": "3",
										"deaths": "4",
										"assists": "5",
										"gold": "100",
										"cs": "8",
										"wards": "12"
									}
								}
							}
						}