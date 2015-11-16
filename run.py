from bs4 import BeautifulSoup
import urllib2
import operator

url = "http://www.sports-reference.com/cfb/years/2015-schedule.html"  # change to whatever your url is

page = urllib2.urlopen(url).read()
soup = BeautifulSoup(page)

recordDic = {}
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



for keys in recordDic.keys():
	recordDic[keys]['numWins'] = len(recordDic[keys]['wins'])
for keys in recordDic.keys():
	recordDic[keys]['numLosses'] = len(recordDic[keys]['losses'])

#TWINS rank
#currentl FCS teams only have record on games vs FBS
ranking1 = {}
for keys in recordDic.keys():
	totalWins = 0
	for teamsBeat in recordDic[keys]['wins']:
		totalWins+= len(recordDic[teamsBeat]['wins'])
	ranking1[keys] = totalWins


sorted_x = sorted(ranking1.items(), key=operator.itemgetter(1), reverse=True)
ranking = 1
for (a,b) in sorted_x:
	print str(ranking) +'. '+a
	ranking+=1


