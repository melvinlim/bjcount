from table import *
print 'update interval?\n[1000]',
x=raw_input()
try:
	updateInterval=int(x)
except:
	updateInterval=1000
t=Table(nPlayers=1,nDecks=2,bankroll=10000,minBet=10,maxBet=20,bjmultiplier=1.5)
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
