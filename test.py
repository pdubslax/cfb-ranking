from bs4 import BeautifulSoup
import urllib2
import operator
from random import randint
import copy

from difflib import SequenceMatcher

def similar(a, b):
	return SequenceMatcher(None, a, b).ratio()

def is_abbrev(abbrev, text):
	abbrev=abbrev.lower()
	text=text.lower()
	words=text.split()
	if not abbrev:
		return True
	if abbrev and not text:
		return False
	if abbrev[0]!=text[0]:
		return False
	else:
		return (is_abbrev(abbrev[1:],' '.join(words[1:])) or any(is_abbrev(abbrev[1:],text[i+1:]) for i in range(len(words[0]))))


def rankingAccuracy(actual,ranking):
	correct = 0.0
	total = 0.0
	for tail_node, head_node in actual:
		if tail_node not in ranking or head_node not in ranking:
			correct += 1
		elif (ranking[tail_node]<ranking[head_node]):
			correct += 1
		total += 1
	return correct/total

def seasonRankingAccuracy(actual,ranking,n,reverseParam):
	sorted_x = sorted(ranking.items(), key=operator.itemgetter(1), reverse=reverseParam)
	sortedList = []
	for (a,b) in sorted_x:
		sortedList.append(a)
	correct = 0.0
	total = 0.0
	for tail_node, head_node in actual:
		if tail_node in ranking and head_node in ranking and (sortedList.index(tail_node) < n or sortedList.index(head_node) < n):
			if tail_node not in ranking or head_node not in ranking:
				correct += 1
			elif (ranking[tail_node]<ranking[head_node]):
				correct += 1
			total += 1
	return correct,total

def adjustedRankingAccuracy(actual,ranking,n,reverseParam):
	sorted_x = sorted(ranking.items(), key=operator.itemgetter(1), reverse=reverseParam)
	sortedList = []
	for (a,b) in sorted_x:
		sortedList.append(a)
	correct = 0.0
	total = 0.0
	for tail_node, head_node in actual:
		if tail_node in ranking and head_node in ranking and (sortedList.index(tail_node) < n or sortedList.index(head_node) < n):
			if tail_node not in ranking or head_node not in ranking:
				correct += 1
			elif (ranking[tail_node]<ranking[head_node]):
				correct += 1
			total += 1
	return correct/total

def populateDicsForWeek(week):
	url = "http://www.sports-reference.com/cfb/years/2015-schedule.html"  # change to whatever your url is
	url2 = "http://espn.go.com/college-football/statistics/teamratings/_/year/2015/key/"
	weekArray = ['20150907040000','20150914040000','20150921040000','20150928040000','20151005040000','20151012040000','20151019040000','20151026040000','20151102040000','20151109040000','20151116040000','20151123040000','20151130040000','20151207040000','20151213040000']
	if week < len(weekArray):
		url2 = url2 + weekArray[week-1]
	else:
		url2 = url2 + weekArray[len(weekArray)-1]

	page = urllib2.urlopen(url).read()
	soup = BeautifulSoup(page)

	page2 = urllib2.urlopen(url2).read()
	soup2 = BeautifulSoup(page2)

	recordDic = {}
	nextWeekGames = []
	pageRankFormat = []
	wins = []
	losses = []

	fbiList = []
	for tr in soup2.find_all('tr')[2:]:
		tds = tr.find_all('td')
		name = tds[1].text
		rest = name.split(',', 1)[0]
		rest = rest.replace(" ", "")
		rest= rest.replace('(', '').replace(')', '')
		if rest != 'TEAM':
			if rest not in recordDic:
				currentMax = 0.0
				foundAbrev = False
				likelyMatch = ''
				for teams in recordDic.keys():
					if is_abbrev(rest,teams) and not likelyMatch:
						foundAbrev = True 
						likelyMatch = teams
					elif is_abbrev(rest,teams):
						# print rest, teams
						likelyMatch = ''

					if (similar(rest,teams)>currentMax):
						currentMax = similar(rest,teams)
						bestMatch = teams
				if (likelyMatch != '' and foundAbrev):
					rest = likelyMatch
				if (rest == 'UCF'):
					rest = 'CentralFlorida'
				elif (rest == 'UTEP'):
					rest = 'Texas-ElPaso'
				elif (rest == 'ULMonroe'):
					rest = 'Louisiana-Monroe'
				elif (rest == 'SMU'):
					rest = 'SouthernMethodist'
				elif (rest == 'UMass'):
					rest = 'Massachusetts'
				elif (rest == 'UNLV'):
					rest = 'Nevada-LasVegas'
				elif (rest == 'UConn'):
					rest = 'Connecticut'
				elif (rest == 'ECU'):
					rest = 'EastCarolina'
				elif (rest == 'UVA'):
					rest = 'Virginia'
				elif (rest == 'USF'):
					rest = 'SouthFlorida'
				elif (rest == 'MissSt'):
					rest = 'MississippiState'
				elif (rest == 'UNC'):
					rest = 'NorthCarolina'
				elif (rest == 'LSU'):
					rest = 'LouisianaState'
				elif (rest == 'USC'):
					rest = 'SouthernCalifornia'
				elif (rest == 'FSU'):
					rest = 'FloridaState'
				elif (rest == 'FAU'):
					rest = 'FloridaAtlantic'
				elif (rest == 'FIU'):
					rest = 'FloridaInternational'
				elif (rest == 'TCU'):
					rest = 'TexasChristian'
				elif (rest == 'OleMiss'):
					rest = 'Mississippi'
				elif (rest == 'OSU'):
					rest = 'OhioState'
				# print rest, bestMatch
			fbiList.append(rest)

	fbiRankings = {}
	startingNum = 200
	for values in fbiList:
		fbiRankings[values] = startingNum
		startingNum -= 1



	weekCount = 1
	specialTimer = False
	for tr in soup.find_all('tr')[2:]:
		tds = tr.find_all('td')
		if len(tds) < 6:
			weekCount += 1
		
		if len(tds)<6 and specialTimer and weekCount>week+1:
			return recordDic,nextWeekGames,pageRankFormat,fbiRankings
			
		if len(tds)>0 and tds[6].text != '' and not specialTimer:
			string = tds[5].text
			result = ''.join([i for i in string if not i.isdigit()])
			result = result.replace('(','')
			result = result.replace(')','')
			result = result.replace(' ','')
			team1 = str(result.lstrip())

			team1Score = int(tds[6].text)
			

			string = tds[8].text
			result = ''.join([i for i in string if not i.isdigit()])
			result = result.replace('(','')
			result = result.replace(')','')
			result = result.replace(' ','')
			team2 = str(result.lstrip())

			team2Score = int(tds[9].text)
			# print team2Score
			if team1Score > team2Score:
				if team1 not in recordDic:
					recordDic[team1] = {}
					recordDic[team1]['wins'] = []
					recordDic[team1]['losses'] = []
				if team2 not in recordDic:
					recordDic[team2] = {}
					recordDic[team2]['wins'] = []
					recordDic[team2]['losses'] = []

				pageRankFormat.append((team2,team1))
				recordDic[team1]['wins'].append(team2)
				recordDic[team2]['losses'].append(team1)
				
			else:
				if team1 not in recordDic:
					recordDic[team1] = {}
					recordDic[team1]['wins'] = []
					recordDic[team1]['losses'] = []
				if team2 not in recordDic:
					recordDic[team2] = {}
					recordDic[team2]['wins'] = []
					recordDic[team2]['losses'] = []

				pageRankFormat.append((team1,team2))
				recordDic[team1]['losses'].append(team2)
				recordDic[team2]['wins'].append(team1)
		if len(tds)>0 and tds[6].text != '' and specialTimer:
			string = tds[5].text
			result = ''.join([i for i in string if not i.isdigit()])
			result = result.replace('(','')
			result = result.replace(')','')
			result = result.replace(' ','')
			team1 = str(result.lstrip())

			team1Score = int(tds[6].text)
			

			string = tds[8].text
			result = ''.join([i for i in string if not i.isdigit()])
			result = result.replace('(','')
			result = result.replace(')','')
			result = result.replace(' ','')
			team2 = str(result.lstrip())

			team2Score = int(tds[9].text)

			resultObject = {}
			resultObject['team1']=team1
			resultObject['team2']=team2


			if team1Score > team2Score:
				resultObject['winner']=team1
				
			else:
				resultObject['winner']=team2
			nextWeekGames.append(resultObject)


		if weekCount > week:
			specialTimer = True


def TWINSRanking(recordDic):
	ranking1 = {}
	for keys in recordDic.keys():
		totalWins = 0.0
		for teamsBeat in recordDic[keys]['wins']:
			totalWins+= len(recordDic[teamsBeat]['wins'])


			
		numGames = len(recordDic[keys]['wins']) + len(recordDic[keys]['losses'])
		ranking1[keys] = totalWins/numGames
	return ranking1

def correctWeekListBuild(nextWeeksGames):
	games = []
	for dic in nextWeeksGames:
		if dic['winner'] != dic['team1']:
			games.append((dic['team1'],dic['winner']))
		else:
			games.append((dic['team2'],dic['winner']))
	return games

def printTop(ranking,n,reverseParam,d1):
	sorted_x = sorted(ranking.items(), key=operator.itemgetter(1), reverse=reverseParam)
	ranking = 1
	for (a,b) in sorted_x:
		if a in d1:
			print str(ranking) +'. '+a
			ranking+=1
			if ranking==n+1:
				break

def pagerank(graph, damping=0.85, epsilon=1.0e-8):
    inlink_map = {}
    outlink_counts = {}
    
    def new_node(node):
        if node not in inlink_map: inlink_map[node] = set()
        if node not in outlink_counts: outlink_counts[node] = 0
    
    for tail_node, head_node in graph:
        new_node(tail_node)
        new_node(head_node)
        if tail_node == head_node: continue
        
        if tail_node not in inlink_map[head_node]:
            inlink_map[head_node].add(tail_node)
            outlink_counts[tail_node] += 1
    
    all_nodes = set(inlink_map.keys())
    for node, outlink_count in outlink_counts.items():
        if outlink_count == 0:
            outlink_counts[node] = len(all_nodes)
            for l_node in all_nodes: inlink_map[l_node].add(node)
    
    initial_value = 1 / len(all_nodes)
    ranks = {}
    for node in inlink_map.keys(): ranks[node] = initial_value
    
    new_ranks = {}
    delta = 1.0
    n_iterations = 0
    while delta > epsilon:
        new_ranks = {}
        for node, inlinks in inlink_map.items():
            new_ranks[node] = ((1 - damping) / len(all_nodes)) + (damping * sum(ranks[inlink] / outlink_counts[inlink] for inlink in inlinks))
        delta = sum(abs(new_ranks[node] - ranks[node]) for node in new_ranks.keys())
        ranks, new_ranks = new_ranks, ranks
        n_iterations += 1
    
    return ranks, n_iterations

def masterRanking(startingPointRanking,pageRankFormat):
	teamList = []
	for team in startingPointRanking.keys():
		teamList.append(team)

	curMax = rankingAccuracy(pageRankFormat,startingPointRanking)
	for i in range(10000):
		rankingTest = copy.deepcopy(startingPointRanking)
		team1 = teamList[randint(0,len(teamList)-1)]
		team2 = teamList[randint(0,len(teamList)-1)]
		temp = rankingTest[team1]
		rankingTest[team1] = rankingTest[team2]
		rankingTest[team2] = temp
		twinsRankAccuracy = rankingAccuracy(pageRankFormat,rankingTest)
		if twinsRankAccuracy > curMax:
			curMax = twinsRankAccuracy
			startingPointRanking = rankingTest
			# print curMax
			# print curMax

	return startingPointRanking
			

def main():
	# my code here
	totalPlayed = 0.0
	totalCorrect = 0.0
	for index in range(5,14):
		recordDic, nextWeeksGames, results, fpiRankings = populateDicsForWeek(index)
		twinsRank = TWINSRanking(recordDic)
		pageRank, iters = pagerank(results)
		bestRank = masterRanking(twinsRank,results)
		# print pageRank
		printTop(bestRank,10,True,fpiRankings)
		if (index == 14):
			gameEvalList = results
		gameEvalList = correctWeekListBuild(nextWeeksGames)

		# twinsRankAccuracy = rankingAccuracy(gameEvalList,twinsRank)
		# pageRankAccuracy = rankingAccuracy(gameEvalList,pageRank)
		# fpiAccuracy = rankingAccuracy(gameEvalList,fpiRankings)
		# bestAccuracy = rankingAccuracy(gameEvalList,bestRank)

		twinsRankAccuracy = adjustedRankingAccuracy(gameEvalList,twinsRank,50,True)
		pageRankAccuracy = adjustedRankingAccuracy(gameEvalList,pageRank,50,True)
		fpiAccuracy = adjustedRankingAccuracy(gameEvalList,fpiRankings,50,True)
		bestAccuracy = adjustedRankingAccuracy(gameEvalList,bestRank,50,True)

		twinsRankAccuracy2 = rankingAccuracy(results,twinsRank)
		pageRankAccuracy2 = rankingAccuracy(results,pageRank)
		fpiAccuracy2 = rankingAccuracy(results,fpiRankings)
		bestAccuracy2 = rankingAccuracy(results,bestRank)
		cor,tot = seasonRankingAccuracy(gameEvalList,bestRank,50,True)
		totalPlayed += tot
		totalCorrect += cor


		print 'Week ' + str(index) + ' TWINs Accuracy: '+ str(twinsRankAccuracy) + ' from ' + str(twinsRankAccuracy2)
		print 'Week ' + str(index) + ' PageRank Accuracy: '+ str(pageRankAccuracy) + ' from ' + str(pageRankAccuracy2)		
		print 'Week ' + str(index) + ' My Best Accuracy: '+ str(bestAccuracy) + ' from ' + str(bestAccuracy2)
		print 'Week ' + str(index) + ' FPI Accuracy: '+ str(fpiAccuracy) + ' from ' + str(fpiAccuracy2)
	print totalPlayed,totalCorrect
	print totalCorrect/totalPlayed


if __name__ == "__main__":
	main()