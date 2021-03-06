import random,time
from card import *
class Shoe(object):
	def __init__(self,nDecks):
		random.seed(time.time())
		self.nDecks=nDecks
		self.nCards=nDecks*52
		self.fill()
		self.r7startingCount=(-2)*self.nDecks
		self.resetCounts()
	def getDealtRatio(self):
		return self.cardsDealt*1.0/self.nCards
	def updateCounts(self,card):
		if card==None:
			return
		elif card.textString=='7d' or card.textString=='7h':
			self.r7count+=1
		elif card.bjv<7:
			self.r7count+=1
		elif card.bjv>9:
			self.r7count-=1
	def fill(self):
		self.decks=[]
		for i in range(self.nDecks):
			for j in range(52):
				self.add(j)
	def resetCounts(self):
		self.r7count=self.r7startingCount
	def shuffle(self):
		self.fill()
		self.resetCounts()
		self.cardsDealt=0
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
	def pop(self,target=None):
		self.cardsDealt+=1
		if target!=None:
			i=0
			for c in self.decks:
				if (c.n%13)==target:
					targetIndex=i
				i+=1
		try:
			if target==None:
				card=self.decks.pop()
			else:
				card=self.decks.pop(targetIndex)
		except:
			card=None
		self.updateCounts(card)
		return card
