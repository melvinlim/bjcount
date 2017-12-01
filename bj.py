from table import *
from player import *
def initPlayers(bankroll,humanPlayer=False):
	nPlayers=1
	players=[]
	i=0
	for i in range(nPlayers):
		p=Player(i,bankroll)
		players.append(p)
	i+=1
	p=Stands(i,bankroll)
	players.append(p)
	i+=1
	p=BasicNoDouble(i,bankroll)
	players.append(p)
	i+=1
	p=BasicDouble(i,bankroll)
	players.append(p)
	if humanPlayer==True:
		i+=1
		p=Human(i,bankroll)
		players.append(p)
	return players
print 'update interval?\n[1000]',
x=raw_input()
try:
	updateInterval=int(x)
except:
	updateInterval=1000
print 'human player?\n[n]',
x=raw_input()
try:
	if x=='y':
		humanPlayer=True
	else:
		humanPlayer=False
except:
	humanPlayer=False
bankroll=100000
players=initPlayers(bankroll,humanPlayer)
t=Table(players=players,nDecks=4,bankroll=bankroll,minBet=10,maxBet=20,bjmultiplier=1.5)
#t=Table(nPlayers=4,nDecks=2,bankroll=100,minBet=10,bjmultiplier=1.5)
handsPlayed=0
while True:
	print 'hands played: '+str(handsPlayed)
	if handsPlayed%updateInterval==0:
		print 'continue? (y/n)\t',
		state=raw_input()
		if state=='':
			pass
		elif state=='n':
			break
	t.round()
	t.status()
	handsPlayed+=1
