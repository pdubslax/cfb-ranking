from bs4 import BeautifulSoup
import urllib2
import operator

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

url = "http://www.sports-reference.com/cfb/years/2015-schedule.html"  # change to whatever your url is
url2 = "http://espn.go.com/college-football/statistics/teamratings"

page = urllib2.urlopen(url).read()
soup = BeautifulSoup(page)

page2 = urllib2.urlopen(url2).read()
soup2 = BeautifulSoup(page2)


		


recordDic = {}
pageRankFormat = []
wins = []
losses = []

for tr in soup.find_all('tr')[2:]:
	tds = tr.find_all('td')
	if len(tds)>0 and tds[6].text != '':
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

		if team1Score > team2Score:
			if team1 not in recordDic:
				recordDic[team1] = {}
				recordDic[team1]['wins'] = []
				recordDic[team1]['losses'] = []
			if team2 not in recordDic:
				recordDic[team2] = {}
				recordDic[team2]['wins'] = []
				recordDic[team2]['losses'] = []

			recordDic[team1]['wins'].append(team2)
			recordDic[team2]['losses'].append(team1)
			pageRankFormat.append((team2,team1))
			
		else:
			if team1 not in recordDic:
				recordDic[team1] = {}
				recordDic[team1]['wins'] = []
				recordDic[team1]['losses'] = []
			if team2 not in recordDic:
				recordDic[team2] = {}
				recordDic[team2]['wins'] = []
				recordDic[team2]['losses'] = []

			recordDic[team1]['losses'].append(team2)
			recordDic[team2]['wins'].append(team1)
			pageRankFormat.append((team1,team2))
			

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


for keys in recordDic.keys():
	recordDic[keys]['numWins'] = len(recordDic[keys]['wins'])
for keys in recordDic.keys():
	recordDic[keys]['numLosses'] = len(recordDic[keys]['losses'])


print 'FPI Ranking'
sorted_x = sorted(fbiRankings.items(), key=operator.itemgetter(1), reverse=True)
ranking = 1
for (a,b) in sorted_x:
	print str(ranking) +'. '+a
	ranking+=1
	if ranking==5:
		break

fbiRankAccuracy = rankingAccuracy(pageRankFormat,fbiRankings)
print 'Accuracy: ' + str(fbiRankAccuracy)

print
#TWINS rank
#currentl FCS teams only have record on games vs FBS
ranking1 = {}
for keys in recordDic.keys():
	totalWins = 0.0
	for teamsBeat in recordDic[keys]['wins']:
		totalWins+= len(recordDic[teamsBeat]['wins'])


		
	numGames = len(recordDic[keys]['wins']) + len(recordDic[keys]['losses'])
	ranking1[keys] = totalWins/numGames

print 'Twins Ranking'
sorted_x = sorted(ranking1.items(), key=operator.itemgetter(1), reverse=True)
ranking = 1
for (a,b) in sorted_x:
	print str(ranking) +'. '+a
	ranking+=1
	if ranking==5:
		break

twinsRankAccuracy = rankingAccuracy(pageRankFormat,ranking1)
print 'Accuracy: ' + str(twinsRankAccuracy)

print
print 'PageRank Ranking'
ranking2,numIter = pagerank(pageRankFormat)
sorted_x = sorted(ranking2.items(), key=operator.itemgetter(1), reverse=True)
ranking = 1
for (a,b) in sorted_x:
	print str(ranking) +'. '+a
	ranking+=1
	if ranking==5:
		break

pageRankAccuracy = rankingAccuracy(pageRankFormat,ranking2)


print 'Accuracy: ' + str(pageRankAccuracy)


