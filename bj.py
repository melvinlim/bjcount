from table import *
from player import *
def initPlayers(bankroll,humanPlayer=False):
	players=[]
	players.append(Player(len(players),bankroll))
	players.append(Stands(len(players),bankroll))
	players.append(BasicNoDouble(len(players),bankroll))
	players.append(BasicDouble(len(players),bankroll))
#	players.append(BasicDoubleR7Count(len(players),bankroll))
#	players.append(BasicDoubleR7CountSitOut(len(players),bankroll))
#	players.append(BasicDoubleR7CountSitOutModified(len(players),bankroll))
#	players.append(BasicDoubleR7CountSitOutModified2(len(players),bankroll))
	players.append(BasicDoubleR7CountSitOutModified3(len(players),bankroll))
	if humanPlayer==True:
		players.append(Human(len(players),bankroll))
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
t=Table(players=players,nDecks=4,bankroll=bankroll,minBet=10,maxBet=30,bjmultiplier=1.5)
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
