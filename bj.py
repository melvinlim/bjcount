from table import *
from player import *
from settings import *
def initPlayers(bankroll,humanPlayer=False):
	players=[]
	players.append(Player(len(players),bankroll))
	players.append(Stands(len(players),bankroll))
	players.append(BasicDouble(len(players),bankroll,Settings(allowDouble=False)))
	players.append(BasicDouble(len(players),bankroll,Settings()))
	players.append(BasicDoubleR7Count(len(players),bankroll,Settings()))
#	players.append(BasicDoubleR7Count(len(players),bankroll,Settings(canSitOut=True)))
	players.append(BasicDoubleR7Count(len(players),bankroll,Settings(canSitOut=True,alwaysTakeInsurance=True)))
	players.append(BasicDoubleR7Count(len(players),bankroll,Settings(canSitOut=True,alwaysTakeInsurance=True,modifiedStrategy=True)))
	players.append(BasicDoubleR7Count(len(players),bankroll,Settings(canSitOut=True,alwaysTakeInsurance=True,modifiedStrategy=True,simplifiedStrategy=True)))
	if humanPlayer==True:
		players=[]
		players.append(Player(len(players),bankroll))
		players.append(Human(len(players),bankroll))
	return players
humanPlayer=False
updateInterval=1
NDECKS=8
print 'mcSim?\t[n]',
x=raw_input()
if x=='y':
	NDECKS=8
	doMC=True
else:
	doMC=False
	print 'human player?\n[n]',
	x=raw_input()
	try:
		if x=='y':
			humanPlayer=True
		else:
			humanPlayer=False
	except:
		humanPlayer=False
	if not humanPlayer:
		print 'update interval?\n[1000]',
		x=raw_input()
		try:
			updateInterval=int(x)
		except:
			updateInterval=1000
bankroll=100000
players=initPlayers(bankroll,humanPlayer)
t=Table(players=players,nDecks=NDECKS,bankroll=bankroll,minBet=10,maxBet=20,bjmultiplier=1.5,dealtRatio=0.4)
handsPlayed=0
if doMC:
#	t.mcSim(8,7,1)	#test player 8,7 versus dealer A
	t.mcSim(8,7,7)
else:
	while True:
		print 'rounds dealt: '+str(handsPlayed)
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
