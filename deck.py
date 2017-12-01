import random,time
class Card(object):
	def __init__(self,n):
		self.n=n
		self.tmpval=n%13
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
			assert False
		if self.tmpval==0:
			self.bjv=10
			value='K'
		elif self.tmpval==1:
			self.bjv=0
			value='A'
		elif self.tmpval==10:
			self.bjv=10
			value='T'
		elif self.tmpval==11:
			self.bjv=10
			value='J'
		elif self.tmpval==12:
			self.bjv=10
			value='Q'
		else:
			self.bjv=self.tmpval
			value=str(self.tmpval)
		self.suit=suit
		self.value=value
		self.textString=self.value+self.suit
	def disp(self):
		print self.textString
		#print self.value,self.suit,self.n
class Deck(object):
	def __init__(self,nDecks):
		self.nDecks=nDecks
		self.nCards=nDecks*52
		self.refill()
		random.seed(time.time())
	def refill(self):
		self.deck=[]
		for i in range(self.nDecks):
			for j in range(52):
				self.add(j)
	def shuffle(self):
		tmp=[]
		for i in range(self.nCards-1,-1,-1):
			t=random.randint(0,i)
			tmp.append(self.deck[t])
			self.deck.pop(t)
		self.deck=tmp
	def add(self,i):
		card=Card(i)
		self.deck.append(card)
	def printAll(self):
		for card in self.deck:
			card.disp()
	def pop(self):
		try:
			card=self.deck.pop()
		except:
			card=None
		return card
