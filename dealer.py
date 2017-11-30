from player import *	
class Dealer(Player):
	def __init__(self,pid,bankroll,table):
		super(Dealer,self).__init__(pid,bankroll)
		self.table=table
		self.table.deck.shuffle()
	def disp(self):
		print 'Dealer:\t\t',
		s=''
		for c in self.hand:
			s+=c.cardString+' '
		print s
	def type1(self):
		v=0
		aces=False
		for c in self.hand:
			if c.bjv==0:
				aces=True
				v+=1
			else:
				v+=c.bjv
		if aces==True:
			if (v+10)<=21:
				v+=10
		if v<17:
			return 'hit'
		elif v==17 and aces==True:
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
				self.dealCard(p)
		self.dealCard(self)
		self.table.disp()
		for p in activePlayers:
			self.handleDecisions(p)
		self.dealCard(self)
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
		if ties:
			print 'tied: ',
			for p in ties:
				p.win(0)
				print p.pid,
			print
		for p in activePlayers:
			p.discard()
		self.discard()
	def decide(self):
		return self.type1()
	def dealCard(self,p):
		card=self.table.deck.pop()
		if card==None:
			print 'out of cards.  reshuffling.'
			self.table.deck.refill()
			self.table.deck.shuffle()
			card=self.table.deck.pop()
		p.receive(card)
		return card
	def evalHand(self,hand):
		v=0
		aces=False
		for c in hand:
			if c.bjv==0:
				aces=True
				v+=1
			else:
				v+=c.bjv
		if aces==True:
			if (v+10)<=21:
				v+=10
		if v==21 and len(hand)==2:
			return 9999
		return v
	def evalAll(self,players):
		winners=[]
		ties=[]
		dt=self.evalHand(self.hand)
		if dt>21 and dt!=9999:
			dt=0
		for p in players:
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
		while d!='stand' and d!='double' and self.evalHand(p.hand)<21:
			d=p.decide()
			if d=='stand':
				pass
			elif d=='hit' or d=='double':
				card=self.dealCard(p)
				p.disp()
