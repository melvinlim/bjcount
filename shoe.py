import random,time
from card import *
class Shoe(object):
	def __init__(self,nDecks):
		self.nDecks=nDecks
		self.nCards=nDecks*52
		self.refill()
		random.seed(time.time())
	def refill(self):
		self.decks=[]
		for i in range(self.nDecks):
			for j in range(52):
				self.add(j)
	def shuffle(self):
		tmp=[]
		for i in range(self.nCards-1,-1,-1):
			t=random.randint(0,i)
			tmp.append(self.decks[t])
			self.decks.pop(t)
		self.decks=tmp
	def add(self,i):
		card=Card(i)
		self.decks.append(card)
	def printAll(self):
		for card in self.decks:
			card.disp()
	def pop(self):
		try:
			card=self.decks.pop()
		except:
			card=None
		return card
