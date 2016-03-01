from cassiopeia import riotapi
import pickle
from matplotlib import pyplot as plt
import numpy as np
import random
from sklearn import cluster

inFile = open('goldMatches.txt', 'r')
matchList = pickle.load(inFile)
kills = []
topkills = []
midkills = []
jungkills = []
botkills = []

for match in matchList:
	top = [participant.id for participant in match.participants if participant.timeline.lane.name == "top_lane"]
	mid = [participant.id for participant in match.participants if participant.timeline.lane.name == "mid_lane"]
	bot = [participant.id for participant in match.participants if participant.timeline.lane.name == "bot_lane"]
	jung = [participant.id for participant in match.participants if participant.timeline.lane.name == "jungle"]
	#Find two mins in cs and assume sup match.participants.stats
	sup = []
	frameSet = match.frames
	for participant in match.participants:
		kills = participant.stats['kills']

	# for x,y in frameSet[1].__dict__.items():
	# 	print x
	# 	print y
	eventSet = [event for eventList in [frame.events for frame in frameSet] for event in eventList]
	for event in eventSet:
		posList = ['kill', 'elite_monster_kill', 'building_kill'] #Have pos attributes
		if event.type.name == 'kill':
			dead = event.victim.id
			if dead in top:
				topkills.append(event)
			if dead in mid:
				midkills.append(event)
			if dead in jung:
				jungkills.append(event)
			if dead in bot:
				botkills.append(event)
# dbscan = cluster.DBSCAN()

#66k kills in gold matches
# target = random.sample(kills, 20000)
# topkills = random.sample(topkills, 5000)
# midkills = random.sample(midkills, 5000)
# jungkills = random.sample(jungkills, 5000)
# botkills = random.sample(botkills, 5000)

# top_xvals = []
# top_yvals = []
# mid_xvals = []
# mid_yvals = []
# jung_xvals = []
# jung_yvals = []
# bot_xvals = []
# bot_yvals = []
# for event in topkills:
# 	top_xvals.append(event.position.x)
# 	top_yvals.append(event.position.y)
# for event in midkills:
# 	mid_xvals.append(event.position.x)
# 	mid_yvals.append(event.position.y)
# for event in jungkills:
# 	jung_xvals.append(event.position.x)
# 	jung_yvals.append(event.position.y)
# for event in botkills:
# 	bot_xvals.append(event.position.x)
# 	bot_yvals.append(event.position.y)

# test = [[x, y] for (x,y) in zip(xvals,yvals)]
# dbscan.fit(test)
# labels = dbscan.labels_
# for i in range(-1, len(dbscan.components_)):
# 	ds = test[np.where(labels==i)]
# 	# plot the data observations
# 	pyplot.plot(ds[:,0],ds[:,1],'o')


# plt.scatter(top_xvals,top_yvals, s=1, alpha= 0.1, color='red')
# plt.scatter(mid_xvals,mid_yvals, s=1, alpha= 0.1, color='orange')
# plt.scatter(jung_xvals,jung_yvals, s=1, alpha= 0.1, color='blue')
# plt.scatter(bot_xvals,bot_yvals, s=1, alpha= 0.1, color='green')
# plt.show()