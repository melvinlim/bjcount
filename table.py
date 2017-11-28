from deck import *
import random,time
class Player(object):
	def __init__(self,pid):
		self.hand=[]
		self.pid=pid
	def receive(self,card):
		self.hand.append(card)
	def disp(self):
		print 'Player '+str(self.pid)+':'
		for c in self.hand:
			c.disp()
	def decide(self):
		return random.randint(0,1)
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
		winner=-1
		for p in table.players:
			t=self.eval(p.hand)
			if t>hs:
				if t<=21:
					hs=t
					winner=p.pid
		return winner
class Table(object):
	def __init__(self,p):
		random.seed(time.time)
		self.deck=Deck()
		self.judge=Judge()
		self.players=[]
		for i in range(p):
			p=Player(i)
			self.players.append(p)
	def newGame(self):
		self.deck.shuffle()
		for i in range(2):
			for p in self.players:
				card=self.deck.pop()
				p.receive(card)
		self.status()
		for p in self.players:
			d=p.decide()
			if d==0:
				pass
			elif d==1:
				card=self.deck.pop()
				p.receive(card)
		self.status()
		winner=self.judge.winner(self)
		print 'winner: '+str(winner)
	def status(self):
		for p in self.players:
			p.disp()
			v=self.judge.eval(p.hand)
			print v
#		self.deck.printAll()
