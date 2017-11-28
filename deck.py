import random
class Card(object):
	def __init__(self,n):
		self.n=n
		self.v=n%13
		self.s=n/13
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
			self.bjv=10
			value='K'
		elif self.v==1:
			self.bjv=0
			value='A'
		elif self.v==10:
			self.bjv=10
			value='T'
		elif self.v==11:
			self.bjv=10
			value='J'
		elif self.v==12:
			self.bjv=10
			value='Q'
		else:
			self.bjv=self.v
			value=str(self.v)
		self.suit=suit
		self.value=value
		self.cardString=self.value+self.suit
	def disp(self):
		print self.cardString
		#print self.value,self.suit,self.n
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
	def pop(self):
		c=self.deck.pop()
		return c
