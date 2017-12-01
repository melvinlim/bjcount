class Hand(object):
	def __init__(self):
		self.cards=[]
		self.hasAce=False
		self.wager=0
		self.handValue=0
		self.textString=''
	def add(self,card):
		if card.bjv==0:
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
			return True
		return False
