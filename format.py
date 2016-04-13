def prepareReturn(roleMap, statMap, prediction, match):
	'''Want to return a dictionary / JSON object with the form:
	(Winner, Win%, {blueTop: (SumName, Champ, Rank, AvgPerformance)}...)
	StatIndexes: Kills, Deaths, Assists, CS, Gold, WardsPlaced
	'''
	assistIndex = 1
	deathIndex = 2
	goldIndex = 10
	killIndex = 13
	csIndex = 17
	wardIndex = 34
	player = 0
	if prediction[0] > prediction[1]:
		winner = 'Blue'
	else:
		winner = 'Red'
	percent = np.max(prediction)
	for p in match.participants:
		role = roleMap[p]
		side = p.side.name
		rank = 'bronze'
		summoner = p.summoner_name
		champion = p.champion.name
		stats = statMap[side+role]
		assists = stats[player*63+assistIndex]
		death = stats[player*63+deathIndex]
		gold = stats[player*63+goldIndex]
		kills = stats[player*63+killIndex]
		cs = stats[player*63+csIndex]
		wards = stats[player*63+wardIndex]

	return (
			{"matchData": {
							"winner": %s,
							"winPercent": %d,
							"playerData": [
								{
									"redTop": {
										"rank": %s
										"kills": %f,
										"deaths": %f,
										"assists": %f,
										"gold": %f,
										"cs": %f,
										"wards": %f
									}
								},
								{
									"redMid": {
										"rank": %s
										"kills": %f,
										"deaths": %f,
										"assists": %f,
										"gold": %f,
										"cs": %f,
										"wards": %f
									}
								},
								{
									"redJung": {
										"rank": %s
										"kills": %f,
										"deaths": %f,
										"assists": %f,
										"gold": %f,
										"cs": %f,
										"wards": %f
									}
								},
								{
									"redADC": {
										"rank": %s
										"kills": %f,
										"deaths": %f,
										"assists": %f,
										"gold": %f,
										"cs": %f,
										"wards": %f
									}
								},
								{
									"redSup": {
										"rank": %s
										"kills": %f,
										"deaths": %f,
										"assists": %f,
										"gold": %f,
										"cs": %f,
										"wards": %f
									}
								},
								{
									"blueTop": {
										"rank": %s
										"kills": %f,
										"deaths": %f,
										"assists": %f,
										"gold": %f,
										"cs": %f,
										"wards": %f
									}
								},
								{
									"blueMid": {
										"rank": %s
										"kills": %f,
										"deaths": %f,
										"assists": %f,
										"gold": %f,
										"cs": %f,
										"wards": %f
									}
								},
								{
									"blueJung": {
										"rank": %s
										"kills": %f,
										"deaths": %f,
										"assists": %f,
										"gold": %f,
										"cs": %f,
										"wards": %f
									}
								},
								{
									"blueADC": {
										"rank": %s
										"kills": %f,
										"deaths": %f,
										"assists": %f,
										"gold": %f,
										"cs": %f,
										"wards": %f
									}
								},
								{
									"blueSup": {
										"rank": %s
										"kills": %f,
										"deaths": %f,
										"assists": %f,
										"gold": %f,
										"cs": %f,
										"wards": %f
									}
								}
							]
						}
			) % (winner, percent, )