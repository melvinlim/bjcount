from deck import *
import random,time
class Player(object):
	def __init__(self):
		self.hand=[]
	def receive(self,card):
		self.hand.append(card)
	def disp(self):
		for c in self.hand:
			c.disp()
class Table(object):
	def __init__(self,p):
		random.seed(time.time)
		self.deck=Deck()
		self.players=[]
		for i in range(p):
			p=Player()
			self.players.append(p)
	def newGame(self):
		self.deck.shuffle()
		for i in range(2):
			for p in self.players:
				p.receive(self.deck.pop())
	def status(self):
		for p in self.players:
			p.disp()
#		self.deck.printAll()
