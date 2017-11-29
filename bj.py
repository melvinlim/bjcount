from table import *
fullyAutomated=True
updateInterval=1000
t=Table(nPlayers=4,nDecks=2,bankroll=100000,minBet=10,bjmultiplier=1.5)
#t=Table(nPlayers=4,nDecks=2,bankroll=100,minBet=10,bjmultiplier=1.5)
t.newGame()
round=0
while True:
	t.round()
	t.status()
	if fullyAutomated:
		if round%updateInterval==0:
			print 'continue? (y/n)\t',
			state=raw_input()
			if state=='':
				pass
			elif state=='n':
				break
	else:
		print 'continue? (y/n)\t',
		state=raw_input()
		if state=='':
			pass
		elif state=='n':
			break
	round+=1
