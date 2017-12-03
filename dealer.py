from player import *	
class Dealer(Player):
	def __init__(self,pid,bankroll,table):
		super(Dealer,self).__init__(pid,bankroll)
		self.table=table
		self.table.shoe.shuffle()
	def disp(self):
		print 'Dealer:\t\t',
		print self.hand.textString
	def type1(self):
		aces=self.hand.hasAce
		soft=self.hand.isSoft()
		if soft:
			v=self.hand.handValue+10
		else:
			v=self.hand.handValue
		if v<17:
			return 'hit'
		elif v==17 and aces==True and soft==True:
			return 'hit'
		else:
			return 'stand'
	def step(self,players):
		activePlayers=[]
		for p in players:
			if p.hand.wager>=self.table.minBet and p.hand.wager<=self.table.maxBet:
				activePlayers.append(p)
			else:
				p.bankroll+=p.hand.wager
				p.hand.wager=0
		if len(activePlayers)==0:
			print 'no players'
			return
		for i in range(2):
			for p in activePlayers:
				self.dealCard(p.hand)
		self.dealCard(self.hand)
		self.table.disp()
		tbr=[]
		for p in activePlayers:
			x=self.handleDecisions(p)
			tbr.append(x)
		for p in tbr:
			if p!=None:
				activePlayers.remove(p)
		self.dealCard(self.hand)
		self.disp()
		self.handleDecisions(self)
		winners,ties=self.evalAll(activePlayers)
		if winners==[]:
			print 'no winners',
		elif len(winners)==1:
			print 'winner: ',
		else:
			print 'winners: ',
		s=''
		for w in winners:
			s+=str(w.pid)+' '
		print s
		if ties:
			print 'tied: ',
			for p in ties:
				print p.pid,
			print
		for p in activePlayers:
			p.discard()
		self.discard()
	def decide(self,table,first,hand):
		return self.type1()
	def dealCard(self,hand):
		card=self.table.shoe.pop()
		if card==None:
			print 'out of cards.  reshuffling.'
			self.table.shoe.refill()
			self.table.shoe.shuffle()
			card=self.table.shoe.pop()
		hand.add(card)
		return card
	def evalHand(self,hand):
		if hand.isSoft():
			v=hand.handValue+10
		else:
			v=hand.handValue
		if v==21 and len(hand.cards)==2:
			hand.isBlackjack=True
		if v>21:
			hand.isBusted=True
		return v
	def evalAll(self,players):
		wins=[]
		ties=[]
		htbe=[]
		for p in players:
			if p.split:
				for h in p.hands:
					htbe.append(h)
			else:
				htbe.append(p.hand)
		dt=self.evalHand(self.hand)
		if self.hand.isBlackjack:
			for h in htbe:
				self.evalHand(h)
				if h.isBlackjack:
					ties.append(h.owner)
					h.owner.payout(h.wager)
				else:
					h.outcome='losingOutcome'
		elif self.hand.isBusted:
			for h in htbe:
				self.evalHand(h)
				if h.isBusted:
					h.outcome='losingOutcome'
				else:
					wins.append(h.owner)
					h.owner.win(h.wager)
		else:
			for h in htbe:
				t=self.evalHand(h)
				if h.isBlackjack:
					wins.append(h.owner)
					h.owner.win(h.wager*self.table.bjmultiplier)
				elif h.isBusted:
					h.outcome='losingOutcome'
				elif t>dt:
					wins.append(h.owner)
					h.owner.win(h.wager)
				elif t==dt:
					ties.append(h.owner)
					h.owner.payout(h.wager)
				else:
					h.outcome='losingOutcome'
		return wins,ties
	def handleDecisions(self,p):
		d=''
		first=True
		while self.evalHand(p.hand)<21:
			d=p.decide(self.table,first,p.hand)
			if d=='stand':
				return None
			elif d=='double':
				p.makeBet(p.hand.wager)
				card=self.dealCard(p.hand)
				p.disp()
				return None
			elif d=='hit':
				card=self.dealCard(p.hand)
				p.disp()
			elif d=='surrender':
				if first==True:
					p.payout(0.5*p.hand.wager)
					p.discard()
					return p
				else:
					card=self.dealCard(p.hand)
					p.disp()
			elif d=='split':
				p.gamesPlayed+=1
				p.split=True
				h1=Hand(p)
				h2=Hand(p)
				h1.add(p.hand.cards[0])
				h2.add(p.hand.cards[1])
				self.dealCard(h1)
				self.dealCard(h2)
				h1.wager+=p.hand.wager
				h2.wager+=p.hand.wager
				p.bankroll-=p.hand.wager
				p.hand=Hand(p)
				p.hands=[h1,h2]
				self.handleSplit(p)
				return None
			first=False
		return None
	def handleSplit(self,p):
		tbr=[]
		for h in p.hands:
			x=self.handleSplitHand(p,h)
			if x!=None:
				tbr.append(x)
		for h in tbr:
			p.hands.remove(h)
	def handleSplitHand(self,p,h):
		print 'split hand:\t',
		print h.textString
		first=False
		d=''
		while self.evalHand(h)<21:
			d=p.decide(self.table,first,h)
			if d=='stand':
				return None
			elif d=='hit':
				self.dealCard(h)
				print 'split hand:\t',
				print h.textString
			elif d=='double':
				self.dealCard(h)
				p.bankroll-=h.wager
				h.wager+=h.wager
				print 'split hand:\t',
				print h.textString
				return None
			elif d=='split':
				p.gamesPlayed+=1
				h1=Hand(p)
				h2=Hand(p)
				h1.add(h.cards[0])
				h2.add(h.cards[1])
				self.dealCard(h1)
				self.dealCard(h2)
				h1.wager+=h.wager
				h2.wager+=h.wager
				p.bankroll-=h.wager
				p.hands.append(h1)
				p.hands.append(h2)
				return h
			else:
				print 'cannot surrender split hand'
				return None
