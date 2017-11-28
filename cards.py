import random
class Card(object):
	def __init__(self,n):
		self.n=n
		self.v=self.value(n)
		self.s=self.suit(n)
	def value(self,n):
		return n%13
	def suit(self,n):
		return n/13
	def disp(self):
		if self.s==0:
			suit='c'
		elif self.s==1:
			suit='h'
		elif self.s==2:
			suit='d'
		elif self.s==3:
			suit='s'
		else:
			suit='error'
		if self.v==0:
			value='K'
		elif self.v==1:
			value='A'
		elif self.v==10:
			value='T'
		elif self.v==11:
			value='J'
		elif self.v==12:
			value='Q'
		else:
			value=self.v
		print value,suit
class Deck(object):
	def __init__(self):
		self.deck=[]
		for i in range(52):
			self.add(i)
	def shuffle(self):
		tmp=[]
		for i in range(51,-1,-1):
			t=random.randint(0,i)
			tmp.append(self.deck[t])
			self.deck.pop(t)
		self.deck=tmp
	def add(self,i):
		card=Card(i)
		self.deck.append(card)
	def printAll(self):
		for c in self.deck:
			c.disp()
