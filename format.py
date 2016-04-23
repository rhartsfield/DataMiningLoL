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
		rank.title()
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
							"winner": winner,
							"winPercent": percent,
							"playerData": {
									"redTop": {
										"summoner": assignDict["redTop"][0],
										"champion": assignDict["redTop"][1],
										"rank": assignDict["redTop"][2],
										"kills": assignDict["redTop"][3],
										"deaths": assignDict["redTop"][4],
										"assists": assignDict["redTop"][5],
										"gold": assignDict["redTop"][6],
										"cs": assignDict["redTop"][7],
										"wards": assignDict["redTop"][8]
									},
									"redMid": {
										"summoner": assignDict["redMid"][0],
										"champion": assignDict["redMid"][1],
										"rank": assignDict["redMid"][2],
										"kills": assignDict["redMid"][3],
										"deaths": assignDict["redMid"][4],
										"assists": assignDict["redMid"][5],
										"gold": assignDict["redMid"][6],
										"cs": assignDict["redMid"][7],
										"wards": assignDict["redMid"][8]
									},
									"redJung": {
										"summoner": assignDict["redJung"][0],
										"champion": assignDict["redJung"][1],
										"rank": assignDict["redJung"][2],
										"kills": assignDict["redJung"][3],
										"deaths": assignDict["redJung"][4],
										"assists": assignDict["redJung"][5],
										"gold": assignDict["redJung"][6],
										"cs": assignDict["redJung"][7],
										"wards": assignDict["redJung"][8]
									},
									"redADC": {
										"summoner": assignDict["redADC"][0],
										"champion": assignDict["redADC"][1],
										"rank": assignDict["redADC"][2],
										"kills": assignDict["redADC"][3],
										"deaths": assignDict["redADC"][4],
										"assists": assignDict["redADC"][5],
										"gold": assignDict["redADC"][6],
										"cs": assignDict["redADC"][7],
										"wards": assignDict["redADC"][8]
									},
									"redSup": {
										"summoner": assignDict["redSup"][0],
										"champion": assignDict["redSup"][1],
										"rank": assignDict["redSup"][2],
										"kills": assignDict["redSup"][3],
										"deaths": assignDict["redSup"][4],
										"assists": assignDict["redSup"][5],
										"gold": assignDict["redSup"][6],
										"cs": assignDict["redSup"][7],
										"wards": assignDict["redSup"][8]
									},
									"blueTop": {
										"summoner": assignDict["blueTop"][0],
										"champion": assignDict["blueTop"][1],
										"rank": assignDict["blueTop"][2],
										"kills": assignDict["blueTop"][3],
										"deaths": assignDict["blueTop"][4],
										"assists": assignDict["blueTop"][5],
										"gold": assignDict["blueTop"][6],
										"cs": assignDict["blueTop"][7],
										"wards": assignDict["blueTop"][8]
									},
									"blueMid": {
										"summoner": assignDict["blueMid"][0],
										"champion": assignDict["blueMid"][1],
										"rank": assignDict["blueMid"][2],
										"kills": assignDict["blueMid"][3],
										"deaths": assignDict["blueMid"][4],
										"assists": assignDict["blueMid"][5],
										"gold": assignDict["blueMid"][6],
										"cs": assignDict["blueMid"][7],
										"wards": assignDict["blueMid"][8]
									},
									"blueJung": {
										"summoner": assignDict["blueJung"][0],
										"champion": assignDict["blueJung"][1],
										"rank": assignDict["blueJung"][2],
										"kills": assignDict["blueJung"][3],
										"deaths": assignDict["blueJung"][4],
										"assists": assignDict["blueJung"][5],
										"gold": assignDict["blueJung"][6],
										"cs": assignDict["blueJung"][7],
										"wards": assignDict["blueJung"][8]
									},
									"blueADC": {
										"summoner": assignDict["blueADC"][0],
										"champion": assignDict["blueADC"][1],
										"rank": assignDict["blueADC"][2],
										"kills": assignDict["blueADC"][3],
										"deaths": assignDict["blueADC"][4],
										"assists": assignDict["blueADC"][5],
										"gold": assignDict["blueADC"][6],
										"cs": assignDict["blueADC"][7],
										"wards": assignDict["blueADC"][8]
									},
									"blueSup": {
										"summoner": assignDict["blueSup"][0],
										"champion": assignDict["blueSup"][1],
										"rank": assignDict["blueSup"][2],
										"kills": assignDict["blueSup"][3],
										"deaths": assignDict["blueSup"][4],
										"assists": assignDict["blueSup"][5],
										"gold": assignDict["blueSup"][6],
										"cs": assignDict["blueSup"][7],
										"wards": assignDict["blueSup"][8]
									}
								}
							}
						}