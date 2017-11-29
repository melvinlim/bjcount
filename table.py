from deck import *
import random,time
class Player(object):
	def __init__(self,pid,bankroll):
		self.hand=[]
		self.pid=pid
		self.bankroll=bankroll
	def bet(self,amount):
		assert amount<=self.bankroll
		self.bankroll-=amount
		self.betAmount=amount
	def receive(self,card):
		assert card!=None
		self.hand.append(card)
	def discard(self):
		self.hand=[]
		self.betAmount=0
	def win(self,amount):
		self.bankroll+=amount+self.betAmount
	def disp(self):
		print 'Player '+str(self.pid)+' ('+str(self.bankroll)+'):\t',
		s=''
		for c in self.hand:
			s+=c.cardString+' '
		print s
	def decide(self):
		return random.randint(0,1)
class Dealer(Player):
	def __init__(self,pid,bankroll):
		super(Dealer,self).__init__(pid,bankroll)
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
			return 1
		elif v==17 and aces==True:
			return 1
		else:
			return 0
	def decide(self):
		return self.type1()
class Human(Player):
	def __init__(self,pid,bankroll):
		super(Human,self).__init__(pid,bankroll)
	def decide(self):
		print 'Player '+str(self.pid)+':\t',
#		self.disp()
		print '(h)it/(s)tand?\t',
		c=raw_input()
		if c=='':
			d=0
		elif c=='h':
			d=1
		elif c=='s':
			d=0
		return d
class Judge(object):
	def __init__(self):
		pass
	def eval(self,hand):
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
		return v
	def winner(self,table):
		hs=0
		winners=[]
		for p in table.players:
			p.blackjack=False
			t=self.eval(p.hand)
			if t>hs:
				if t<=21:
					winners=[]
					hs=t
					winners.append(p)
					if t==21 and len(p.hand)==2:
						p.blackjack=True
			elif t==hs:
				winners.append(p)
		return winners
class Table(object):
	def __init__(self,p,nDecks,bankroll,minBet,bjmultiplier):
		random.seed(time.time)
		self.bjmultiplier=bjmultiplier
		self.deck=Deck(nDecks)
		self.judge=Judge()
		self.players=[]
		self.bankroll=bankroll
		self.minBet=minBet
		for i in range(p):
			p=Player(i,bankroll)
			self.players.append(p)
		p=Human(i+1,bankroll)
		self.players.append(p)
		p=Dealer(i+2,bankroll)
		self.players.append(p)
	def clear(self):
		for p in self.players:
			p.discard()
	def newGame(self):
		self.deck.shuffle()
	def deal(self,p):
		card=self.deck.pop()
		if card==None:
			print 'out of cards.  reshuffling.'
			self.deck.refill()
			self.deck.shuffle()
			card=self.deck.pop()
		p.receive(card)
		return card
	def round(self):
		out=[]
		if len(self.players)==1:
			print 'no players remaining'
			return
		for p in self.players:
			if p.bankroll>=self.minBet:
				p.bet(self.minBet)
			else:
				out.append(p)
		for p in out:
			self.players.remove(p)
		for i in range(2):
			for p in self.players:
				if p.betAmount>0:
					self.deal(p)
		self.status()
		for p in self.players:
			d=-1
			while d!=0 and self.judge.eval(p.hand)<21:
				d=p.decide()
				if d==0:
					pass
				elif d==1:
					card=self.deal(p)
					p.disp()
#					print 'dealt '+card.cardString+' to '+str(p.pid)+':'
#		self.status()
		winners=self.judge.winner(self)
		if winners==[]:
			print 'winner: dealer'
		elif len(winners)==1:
			print 'winner: ',
		else:
			print 'winners: ',
		s=''
		for w in winners:
			if w.blackjack==True:
				w.win(w.betAmount*self.bjmultiplier)
			else:
				w.win(w.betAmount)
			s+=str(w.pid)+' '
		print s
		self.clear()
	def status(self):
		for p in self.players:
			p.disp()
#			v=self.judge.eval(p.hand)
#			print v
#		self.deck.printAll()
