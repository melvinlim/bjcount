from deck import *
class Player(object):
	def __init__(self):
		hand=[]
class Table(object):
	def __init__(self,p):
		self.deck=Deck()
		self.players=[]
		for i in range(p):
			p=Player()
			self.players.append(p)
		self.deck.printAll()
