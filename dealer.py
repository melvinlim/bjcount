from player import *	
class Dealer(Player):
	def __init__(self,pid,bankroll,table):
		super(Dealer,self).__init__(pid,bankroll)
		self.table=table
		self.table.deck.shuffle()
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
			p.betDecision(self.table.minBet,self.table.maxBet)
		for p in players:
			if p.betBox>=self.table.minBet and p.betBox<=self.table.maxBet:
				activePlayers.append(p)
			else:
				p.bankroll+=p.betBox
				p.betBox=0
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
			if w.blackjack==True:
				w.win(w.betBox*self.table.bjmultiplier)
			else:
				w.win(w.betBox)
			s+=str(w.pid)+' '
		print s
		for p in activePlayers:
			if p.split:
				p.splitHands=len(p.hands)
				p.bankroll-=p.betBox*(p.splitHands-1)
				p.bankroll+=p.betBox*p.splitTies
				p.bankroll+=2*p.betBox*p.splitWins
				print 'Player '+str(p.pid)+': w/t/h:'+str(p.splitWins)+'/'+str(p.splitTies)+'/'+str(p.splitHands)
				p.split=False
		if ties:
			print 'tied: ',
			for p in ties:
				p.win(0)
				print p.pid,
			print
		for p in activePlayers:
			p.discard()
		self.discard()
	def decide(self,first,hand):
		return self.type1()
	def dealCard(self,hand):
		card=self.table.deck.pop()
		if card==None:
			print 'out of cards.  reshuffling.'
			self.table.deck.refill()
			self.table.deck.shuffle()
			card=self.table.deck.pop()
		hand.add(card)
		return card
	def evalHand(self,hand):
		aces=hand.hasAce
		if hand.isSoft():
			v=hand.handValue+10
		else:
			v=hand.handValue
		if v==21 and len(hand.cards)==2:
			return 9999
		return v
	def evalAll(self,players):
		winners=[]
		ties=[]
		dt=self.evalHand(self.hand)
		if dt>21 and dt!=9999:
			dt=0
		for p in players:
			if p.split:
				p.splitWins=0
				p.splitTies=0
				for h in p.hands:
					t=self.evalHand(h)
					if t>dt and t<=21:
						p.splitWins+=1
					elif t==dt:
						p.splitTies+=1
			else:
				p.blackjack=False
				t=self.evalHand(p.hand)
				if t>dt:
					if t==9999:
						p.blackjack=True
						winners.append(p)
					elif t<=21:
						winners.append(p)
				elif t==dt:
					ties.append(p)
		return winners,ties
	def handleDecisions(self,p):
		d=''
		first=True
		while d!='double' and d!='surrender' and self.evalHand(p.hand)<21:
			d=p.decide(first,p.hand)
			if d=='stand':
				return None
			elif d=='hit' or d=='double':
				card=self.dealCard(p.hand)
				p.disp()
			elif first==True and d=='surrender':
				p.payout(0.5*p.betBox)
				p.discard()
				return p
			elif d=='split':
				p.split=True
				h1=Hand()
				h2=Hand()
				h1.add(p.hand.cards[0])
				h2.add(p.hand.cards[1])
				self.dealCard(h1)
				self.dealCard(h2)
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
			d=p.decide(first,h)
			if d=='stand':
				return None
			elif d=='hit':
				card=self.dealCard(h)
				print 'split hand:\t',
				print h.textString
			elif d=='split':
				h1=Hand()
				h2=Hand()
				h1.add(h.cards[0])
				h2.add(h.cards[1])
				self.dealCard(h1)
				self.dealCard(h2)
				p.hands.append(h1)
				p.hands.append(h2)
				return h
