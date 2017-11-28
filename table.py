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
				p.receive(self.deck.pop())
	def status(self):
		for p in self.players:
			p.disp()
			v=self.judge.eval(p.hand)
			print v
#		self.deck.printAll()
