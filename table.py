from shoe import *
#from player import *
from dealer import *
class Table(object):
	def __init__(self,players,nDecks,bankroll,minBet,maxBet,bjmultiplier,dealtRatio):
		self.dealtRatio=dealtRatio
		self.bjmultiplier=bjmultiplier
		self.shoe=Shoe(nDecks)
		self.players=players
		self.bankroll=bankroll
		self.minBet=minBet
		self.maxBet=maxBet
		self.dealer=Dealer(-1,bankroll,self)
	def round(self):
		self.tableState='takingBets'
		for p in self.players:
			p.betDecision(self.minBet,self.maxBet,self)
		self.tableState='allowingDecisions'
		self.dealer.step(self.players)
	def disp(self):
		for p in self.players:
			p.disp()
#		self.deck.printAll()
		self.dealer.disp()
	def setUp(self,p1,p2,d1):
		p=Player(1,1000)
		d=Dealer(-1,1000,self)
		p.hands=[Hand(p)]
		d.hands=[Hand(p)]
		d.hand=d.hands[0]
		c1=Card(p1)
		c2=Card(p2)
		c3=Card(d1)
		p.hands[0].add(c1)
		p.hands[0].add(c2)
		d.hands[0].add(c3)
		return p,d
	def mcSim(self,p1,p2,d1):
		quiet=True
		handsPerStep=1000
		hands=0
		value={}
		for d in ['stand','hit']:
			value[d]=0
		while True:
			for i in range(handsPerStep):
				p,d=self.setUp(p1,p2,d1)
				d.dealCard(d.hands[0])
				decision=d.handleDecisions(p,quiet)
				if not quiet:
					print decision
				d.handleDecisions(d,quiet)
				if not quiet:
					p.disp()
					d.disp()
				winningHands,tiedHands=d.evalAll([p])
				if not quiet:
					print winningHands,tiedHands
				if winningHands!=[]:
					value[decision]+=1
				elif tiedHands!=[]:
					value[decision]+=0
				else:
					value[decision]-=1
				hands+=1
			for d in value:
				print d+':\t'+str(value[d]*1.0/hands)
			print 'simulated %d hands'%hands
			raw_input()
	def status(self):
		for p in self.players:
			p.status()
