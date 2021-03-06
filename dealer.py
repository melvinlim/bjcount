from player import *
class Dealer(Player):
	def __init__(self,pid,bankroll,table):
		super(Dealer,self).__init__(pid,bankroll)
		self.table=table
		self.table.shoe.shuffle()
		self.hand=self.hands[0]
	def discardHand(self):
		self.hands=[Hand(self)]
		self.hand=self.hands[0]
	def disp(self):
		print 'Dealer:\t\t',
		print self.hand.textString
	def type1(self):
		soft=self.hand.isSoft()
		v=self.hand.highValue
		if v<17:
			return 'hit'
		elif v==17 and soft:
			return 'hit'
		else:
			return 'stand'
	def step(self,players):
		if self.table.shoe.getDealtRatio()>self.table.dealtRatio:
			self.table.shoe.shuffle()
			for p in players:
				p.isSittingOut=False
		activePlayers=[]
		for p in players:
			if p.isSittingOut==False and p.openingWager>=self.table.minBet and p.openingWager<=self.table.maxBet:
				p.hands=[Hand(p)]
				p.hands[0].wager=p.openingWager
				p.openingWager=0
				activePlayers.append(p)
			else:
				p.bankroll+=p.openingWager
				p.openingWager=0
		if len(activePlayers)==0:
			print 'no players'
			return
		for i in range(2):
			for p in activePlayers:
				self.dealCard(p.hands[0])
		visibleCard=self.dealCard(self.hand)
		self.table.disp()
		if visibleCard.face=='A':
			for p in activePlayers:
				p.decideOnInsurance(self.table)
				if p.insuranceBet>p.hands[0].wager:
					p.bankroll+=p.insuranceBet
					p.insuranceBet=0
		for p in activePlayers:
			self.handleDecisions(p)
		self.dealCard(self.hand)
		self.disp()
		self.handleDecisions(self)
		winningHands,tiedHands=self.evalAll(activePlayers)
		if self.hand.isBlackjack:
			for p in activePlayers:
				if p.insuranceBet>0:
					p.bankroll+=p.insuranceBet*2
					p.insuranceBet=0
		self.printResults(winningHands,tiedHands)
		for p in activePlayers:
			p.updateStats()
			p.insuranceBet=0
			p.discardHand()
		self.discardHand()
	def printResults(self,winningHands,tiedHands):
		if winningHands==[]:
			print 'no winning hands',
		elif len(winningHands)==1:
			print 'winning hand: ',
		else:
			print 'winning hands: ',
		for p in winningHands:
			print p.pid,
		print
		if tiedHands:
			print 'tied hands: ',
			for p in tiedHands:
				print p.pid,
			print
	def decide(self,table,firstDecision,hand):
		return self.type1()
	def dealCard(self,hand):
		card=self.table.shoe.pop()
		if card==None:
			print 'out of cards.  reshuffling.'
			self.table.shoe.shuffle()
			for p in self.table.players:
				p.isSittingOut=False
			card=self.table.shoe.pop()
		hand.add(card)
		return card
	def makePayout(self,p,amount):
		p.handsWon+=1
		p.receiveChips(amount)
	def returnChips(self,p,amount):
		p.receiveChips(amount)
	def evalAll(self,players):
		wins=[]
		ties=[]
		dt=self.hand.highValue
		for p in players:
			if p.hasSurrendered:
				self.returnChips(p,0.5*p.hands[0].wager)
				p.hasSurrendered=False
			else:
				for h in p.hands:
					t=h.highValue
					if self.hand.isBlackjack:
							if h.isBlackjack:
								ties.append(p)
								self.returnChips(p,h.wager)
							else:
								h.outcome='losingOutcome'
					elif self.hand.isBusted:
							if h.isBusted:
								h.outcome='losingOutcome'
							else:
								wins.append(p)
								self.makePayout(p,h.wager*2)
					else:
						if h.isBlackjack:
							wins.append(p)
							self.makePayout(p,h.wager+(h.wager*self.table.bjmultiplier))
						elif h.isBusted:
							h.outcome='losingOutcome'
						elif t>dt:
							wins.append(p)
							self.makePayout(p,h.wager*2)
						elif t==dt:
							ties.append(p)
							self.returnChips(p,h.wager)
						else:
							h.outcome='losingOutcome'
		return wins,ties
	def handleDecisions(self,p,quiet=False):
		hasHit=False
		firstDecision=True
		phv=p.hands[0].highValue
		while phv<21:
			d=p.decide(self.table,firstDecision,p.hands[0])
			if d=='stand':
				if hasHit:
					return 'hit'
				else:
					return 'stand'
			elif d=='double':
				p.bankroll-=p.hands[0].wager
				p.hands[0].wager+=p.hands[0].wager
				card=self.dealCard(p.hands[0])
				if not quiet:
					p.disp()
				return None
			elif d=='hit':
				hasHit=True
				card=self.dealCard(p.hands[0])
				phv=p.hands[0].highValue
				if not quiet:
					p.disp()
			elif d=='surrender':
				if firstDecision==True:
					p.hasSurrendered=True
					return p
				else:
					card=self.dealCard(p.hands[0])
					phv=p.hands[0].highValue
					if not quiet:
						p.disp()
			elif d=='split':
				p.handsPlayed+=1
				h1=Hand(p)
				h2=Hand(p)
				h1.add(p.hands[0].cards[0])
				h2.add(p.hands[0].cards[1])
				self.dealCard(h1)
				self.dealCard(h2)
				h1.wager+=p.hands[0].wager
				h2.wager+=p.hands[0].wager
				p.bankroll-=p.hands[0].wager
				p.hands=[]
				p.hands+=self.handleSplitHand(h1,1)
				p.hands+=self.handleSplitHand(h2,1)
				return None
			firstDecision=False
		return 'hit'
	def handleSplitHand(self,h,depth):
		result=[h]
		p=h.owner
		print 'split hand:\t',
		print h.textString
		firstDecision=False
		phv=h.highValue
		while phv<21:
			d=p.decide(self.table,firstDecision,h)
			if d=='stand':
				return result
			elif d=='hit':
				self.dealCard(h)
				phv=h.highValue
				print 'split hand:\t',
				print h.textString
			elif d=='double':
				#import pdb
				#pdb.set_trace()
				self.dealCard(h)
				p.bankroll-=h.wager
				h.wager+=h.wager
				print 'split hand:\t',
				print h.textString
				return result
			elif d=='split':
				p.handsPlayed+=1
				h1=Hand(p)
				h2=Hand(p)
				h1.add(h.cards[0])
				h2.add(h.cards[1])
				self.dealCard(h1)
				self.dealCard(h2)
				h1.wager+=h.wager
				h2.wager+=h.wager
				p.bankroll-=h.wager
				result=[]
				result+=self.handleSplitHand(h1,depth+1)
				result+=self.handleSplitHand(h2,depth+1)
				return result
			else:
				print 'cannot surrender split hand'
				return result
		return result
