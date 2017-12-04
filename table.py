from shoe import *
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
		value=self.initValue()
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
					if p.hands[0].isBlackjack:
						value[decision]+=1.5
					else:
						value[decision]+=1
				elif tiedHands!=[]:
					value[decision]+=0
				else:
					value[decision]-=1
				hands+=1
			for d in value:
				print d+':\t'+str(value[d]*1.0/hands)
			print p1,p2,d1
			print 'simulated %d hands'%hands
			print 'continue? (c to change problem)\t[y]',
			x=raw_input()
			if x=='c':
				print 'p1:\t',
				p1=self.assignInput(p1)
				print 'p2:\t',
				p2=self.assignInput(p2)
				print 'd1:\t',
				d1=self.assignInput(d1)
				print 'new problem: [%d,%d,%d]'%(p1,p2,d1)
				hands=0
				value=self.initValue()
			elif x=='n':
				break
	def initValue(self):
		value={}
		for d in ['stand','hit']:
			value[d]=0
		return value
	def assignInput(self,original):
		x=raw_input()
		try:
			tmp=int(x)
		except:
			tmp=original
		return tmp
	def status(self):
		for p in self.players:
			p.status()
