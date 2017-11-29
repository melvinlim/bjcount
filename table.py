from deck import *
import random,time
class Player(object):
	def __init__(self,pid):
		self.hand=[]
		self.pid=pid
	def receive(self,card):
		assert card!=None
		self.hand.append(card)
	def discard(self):
		self.hand=[]
	def disp(self):
		print 'Player '+str(self.pid)+':\t',
		s=''
		for c in self.hand:
			s+=c.cardString+' '
		print s
	def decide(self):
		return random.randint(0,1)
class Dealer(Player):
	def __init__(self,pid):
		super(Dealer,self).__init__(pid)
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
	def __init__(self,pid):
		super(Human,self).__init__(pid)
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
			t=self.eval(p.hand)
			if t>hs:
				if t<=21:
					winners=[]
					hs=t
					winners.append(p.pid)
			elif t==hs:
				winners.append(p.pid)
		return winners
class Table(object):
	def __init__(self,p,nDecks):
		random.seed(time.time)
		self.deck=Deck(nDecks)
		self.judge=Judge()
		self.players=[]
		for i in range(p):
			p=Player(i)
			self.players.append(p)
		p=Human(i+1)
		self.players.append(p)
		p=Dealer(i+2)
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
		for i in range(2):
			for p in self.players:
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
			print 'winner: '+str(winners[0])
		else:
			s=''
			for w in winners:
				s+=str(w)+' '
			print 'winners: '+s
		self.clear()
	def status(self):
		for p in self.players:
			p.disp()
#			v=self.judge.eval(p.hand)
#			print v
#		self.deck.printAll()
