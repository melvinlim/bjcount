from player import *
class Dealer(Player):
	def __init__(self,pid,bankroll,table):
		super(Dealer,self).__init__(pid,bankroll)
		self.table=table
		self.table.shoe.shuffle()
		self.hand=self.hands[0]
	def discard(self):
		self.hands=[Hand(self)]
		self.hand=self.hands[0]
	def disp(self):
		print 'Dealer:\t\t',
		print self.hand.textString
	def type1(self):
		soft=self.hand.isSoft()
		v=self.evalHand(self.hand)
		if v<17:
			return 'hit'
		elif v==17 and soft:
			return 'hit'
		else:
			return 'stand'
	def step(self,players):
		activePlayers=[]
		for p in players:
			if p.openingWager>=self.table.minBet and p.openingWager<=self.table.maxBet:
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
		if v>21:
			hand.isBusted=True
		elif v==21 and len(hand.cards)==2:
			hand.isBlackjack=True
		return v
	def evalAll(self,players):
		wins=[]
		ties=[]
		dt=self.evalHand(self.hand)
		for p in players:
			for h in p.hands:
				t=self.evalHand(h)
				if self.hand.isBlackjack:
						if h.isBlackjack:
							ties.append(p)
							p.payout(h.wager)
						else:
							h.outcome='losingOutcome'
				elif self.hand.isBusted:
						if h.isBusted:
							h.outcome='losingOutcome'
						else:
							wins.append(p)
							p.win(h.wager)
				else:
					if h.isBlackjack:
						wins.append(p)
						p.win(h.wager*self.table.bjmultiplier)
					elif h.isBusted:
						h.outcome='losingOutcome'
					elif t>dt:
						wins.append(p)
						p.win(h.wager)
					elif t==dt:
						ties.append(p)
						p.payout(h.wager)
					else:
						h.outcome='losingOutcome'
		return wins,ties
	def handleDecisions(self,p):
		d=''
		first=True
		while self.evalHand(p.hands[0])<21:
			d=p.decide(self.table,first,p.hands[0])
			if d=='stand':
				return None
			elif d=='double':
				p.bankroll-=p.hands[0].wager
				p.hands[0].wager+=p.hands[0].wager
				card=self.dealCard(p.hands[0])
				p.disp()
				return None
			elif d=='hit':
				card=self.dealCard(p.hands[0])
				p.disp()
			elif d=='surrender':
				if first==True:
					p.payout(0.5*p.hands[0].wager)
					p.discard()
					return p
				else:
					card=self.dealCard(p.hands[0])
					p.disp()
			elif d=='split':
				p.gamesPlayed+=1
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
			first=False
		return None
	def handleSplitHand(self,h,depth):
		result=[h]
		p=h.owner
		print 'split hand:\t',
		print h.textString
		first=False
		d=''
		while self.evalHand(h)<21:
			d=p.decide(self.table,first,h)
			if d=='stand':
				return result
			elif d=='hit':
				self.dealCard(h)
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
				result=[]
				result+=self.handleSplitHand(h1,depth+1)
				result+=self.handleSplitHand(h2,depth+1)
				print depth
				return result
			else:
				print 'cannot surrender split hand'
				return result
		return result
