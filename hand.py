class Hand(object):
	def __init__(self,owner):
		self.cards=[]
		self.hasAce=False
		self.wager=0
		self.handValue=0
		self.textString=''
		self.handWon=False
		self.handTied=False
		self.isBlackjack=False
		self.isBusted=False
		self.outcome=''
		self.owner=owner
	def add(self,card):
		if card.face=='A':
			self.hasAce=True
			self.handValue+=1
		else:
			self.handValue+=card.bjv
		self.cards.append(card)
		self.textString+=card.textString+' '
	def isSoft(self):
		if self.hasAce:
			if (self.handValue+10)<=21:
				return True
		return False
	def canSplit(self):
		if self.cards[0].bjv==self.cards[1].bjv:
			if len(self.cards)==2:
				return True
		return False
	def updateValue(self):
		if self.isSoft():
			v=self.handValue+10
		else:
			v=self.handValue
		if v>21:
			self.isBusted=True
		elif v==21 and len(self.cards)==2:
			self.isBlackjack=True
		self.trueValue=v
