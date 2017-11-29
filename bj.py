from table import *
t=Table(p=4,nDecks=2,bankroll=100,minBet=10,bjmultiplier=1.5)
t.newGame()
while True:
	t.round()
	print 'continue? (y/n)\t',
	state=raw_input()
	if state=='':
		pass
	elif state=='n':
		break
#t.status()
