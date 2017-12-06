import random
from hand import *
class Player(object):
	def __init__(self,pid,bankroll):
		self.maxBankroll=bankroll
		self.maxlft=0
		self.isSittingOut=False
		self.hasSurrendered=False
		self.insuranceBet=0
		self.hands=[Hand(self)]
		self.pid=pid
		self.bankroll=bankroll
		self.startingBankroll=bankroll
		self.handsPlayed=0
		self.handsWon=0
	def updateStats(self):
		if self.bankroll>self.maxBankroll:
			self.maxBankroll=self.bankroll
		lft=self.maxBankroll-self.bankroll
		if lft>self.maxlft:
			self.maxlft=lft
	def decideOnInsurance(self,table):
		return
	def makeOpeningBet(self,amount):
		assert amount<=self.bankroll
		self.bankroll-=amount
		self.openingWager=amount
	def betDecision(self,minB,maxB,table):
		if self.bankroll>=minB:
			self.makeOpeningBet(minB)
			return True
		else:
			return False
	def discardHand(self):
		self.hands=[Hand(self)]
		self.handsPlayed+=1
	def receiveChips(self,amount):
		self.bankroll+=amount
	def disp(self):
		print 'Player '+str(self.pid)+' ('+str(self.bankroll)+'):\t',
		print self.hands[0].textString
	def status(self):
		if self.handsPlayed==0:
			winPct=0
			profitPerHand=0
		else:
			winPct=self.handsWon*100.0/self.handsPlayed
			profitPerHand=(self.bankroll-self.startingBankroll)*1.0/self.handsPlayed
		print 'Player '+str(self.pid)+' ('+str(self.bankroll)+'):',
#		print '\twinPct: %.2f'%(winPct),
		print '\tprofit/hand: %.2f'%(profitPerHand),
		print '\thands: %d'%(self.handsPlayed),
		print '\tmaxlft: %d'%(self.maxlft)
	def decide(self,table,first,hand):
		if hand.isSoft()==False:
			if hand.highValue>=17:
				return 'stand'
		d=random.randint(0,1)
		if d==0:
			return 'stand'
		else:
			return 'hit'
class Stands(Player):
	def __init__(self,pid,bankroll):
		super(Stands,self).__init__(pid,bankroll)
	def decide(self,table,first,hand):
		return 'stand'
class Human(Player):
	def __init__(self,pid,bankroll):
		super(Human,self).__init__(pid,bankroll)
	def decideOnInsurance(self,table):
		print 'Player '+str(self.pid)+':\t',
		print 'insurance amount?\n',
		print '[0]',
		c=raw_input()
		try:
			n=int(c)
			if n<=self.hands[0].wager/2:
				self.bankroll-=n
				self.insuranceBet=n
				return True
			else:
				return False
		except:
			return False
	def betDecision(self,minB,maxB,table):
		print 'Player '+str(self.pid)+':\t',
		print 'bet amount?\n',
		print '['+str(minB)+']',
		c=raw_input()
		try:
			n=int(c)
			if self.bankroll>=n:
				self.makeOpeningBet(n)
				return True
			else:
				return False
		except:
			if self.bankroll>=minB:
				self.makeOpeningBet(minB)
				return True
			else:
				return False
	def decide(self,table,first,hand):
		print 'Player '+str(self.pid)+':\t',
		options=''
		if first==True:
			options+='(h)it/(s)tand/(d)ouble/s(u)rrender'
		else:
			options+='(h)it/(s)tand/(d)ouble'
		if hand.canSplit():
			options+='/s(p)lit'
		options+='?\t'
		print options,
		c=raw_input()
		if c=='':
			d='stand'
		elif c=='h':
			d='hit'
		elif c=='s':
			d='stand'
		elif c=='d':
			d='double'
		elif first==True and c=='u':
			d='surrender'
		elif hand.canSplit() and c=='p':
			d='split'
		return d
class BasicDouble(Player):
	def __init__(self,pid,bankroll,settings):
		super(BasicDouble,self).__init__(pid,bankroll)
		self.settings=settings
	def decide(self,table,first,hand):
		dealerCard=table.dealer.hand.cards[0].bjv
		if dealerCard==0:
			dealerCard=11
		if hand.canSplit():
			if hand.hasAce:
				return 'split'
			elif hand.lowValue==20:
				return 'stand'
			elif hand.lowValue==18:
				if dealerCard<7:
					return 'split'
				elif dealerCard>9:
					return 'stand'
				elif dealerCard>7:
					return 'split'
				else:
					return 'stand'
			elif hand.lowValue==16:
				return 'split'
			elif hand.lowValue==14:
				if dealerCard<8:
					return 'split'
				else:
					return 'hit'
			elif hand.lowValue==12:
				if dealerCard<7:
					return 'split'
				else:
					return 'hit'
			elif hand.lowValue==10:
				if dealerCard<10:
					if not self.settings.allowDouble:
						return 'hit'
					return 'double'
				else:
					if self.settings.modifiedStrategy:
						if dealerCard==10:
							if table.shoe.r7count>=2:
								if not self.settings.allowDouble:
									return 'hit'
								return 'double'
					return 'hit'
			elif hand.lowValue==8:
				if dealerCard>6 or dealerCard<5:
					return 'hit'
				else:
					return 'split'
			else:
				if dealerCard<8:
					return 'split'
				else:
					return 'hit'
		elif hand.isSoft():
			if hand.lowValue>9:
				return 'stand'
			elif hand.lowValue==9:
				if dealerCard==6:
					if not self.settings.allowDouble:
						return 'stand'
					return 'double'
				else:
					return 'stand'
			elif hand.lowValue==8:
				if dealerCard>8:
					return 'hit'
				elif dealerCard>6:
					return 'stand'
				else:
					if not self.settings.allowDouble:
						return 'stand'
					return 'double'
			elif hand.lowValue==7:
				if dealerCard>6:
					return 'hit'
				elif dealerCard<3:
					return 'hit'
				else:
					if not self.settings.allowDouble:
						return 'hit'
					return 'double'
			elif hand.lowValue>4:
				if dealerCard>6:
					return 'hit'
				elif dealerCard<4:
					return 'hit'
				else:
					if not self.settings.allowDouble:
						return 'hit'
					return 'double'
			else:
				if dealerCard>6:
					return 'hit'
				elif dealerCard<5:
					return 'hit'
				else:
					if not self.settings.allowDouble:
						return 'hit'
					return 'double'
		else:
			if hand.lowValue<9:
				return 'hit'
			elif hand.lowValue==9:
				if dealerCard>6 or dealerCard<3:
					if self.settings.simplifiedStrategy:
						if dealerCard==2:
							if not self.settings.allowDouble:
								return 'hit'
							return 'double'
					return 'hit'
				else:
					if not self.settings.allowDouble:
						return 'hit'
					return 'double'
			elif hand.lowValue==10:
				if dealerCard<10:
					if not self.settings.allowDouble:
						return 'hit'
					return 'double'
				else:
					if self.settings.modifiedStrategy:
						if dealerCard==10:
							if table.shoe.r7count>=2:
								if not self.settings.allowDouble:
									return 'hit'
								return 'double'
					return 'hit'
			elif hand.lowValue==11:
				if not self.settings.allowDouble:
					return 'hit'
				return 'double'
			elif hand.lowValue==12:
				if dealerCard>6:
					return 'hit'
				elif dealerCard<4:
					if self.settings.modifiedStrategy:
						return 'stand'
					else:
						return 'hit'
				else:
					return 'stand'
			elif hand.lowValue==13 or hand.lowValue==14:
				if dealerCard>6:
					return 'hit'
				else:
					return 'stand'
			elif hand.lowValue==15:
				if dealerCard==10:
					if self.settings.allowSurrender:
						return 'surrender'
					else:
						return 'hit'
				elif dealerCard>6:
					return 'hit'
				else:
					return 'stand'
			elif hand.lowValue==16:
				if dealerCard>8:
					if self.settings.allowSurrender:
						return 'surrender'
					else:
						return 'hit'
				elif dealerCard>6:
					return 'hit'
				else:
					return 'stand'
			else:
				return 'stand'
		return 'stand'
class BasicDoubleR7Count(BasicDouble):
	def __init__(self,pid,bankroll,settings):
		super(BasicDoubleR7Count,self).__init__(pid,bankroll,settings)
	def decideOnInsurance(self,table):
		if self.settings.alwaysTakeInsurance and table.shoe.r7count>=2:
			self.bankroll-=self.hands[0].wager/2
			self.insuranceBet=self.hands[0].wager/2
		else:
			return
	def betDecision(self,minB,maxB,table):
		count=table.shoe.r7count
		if self.settings.canSitOut:
			if count<(table.shoe.r7startingCount):
				self.isSittingOut=True
				bet=0
				self.makeOpeningBet(0)
				return False
		if self.bankroll>=minB:
			if count>5:
				bet=maxB
			elif count>0:
				bet=minB+(maxB-minB)*0.5
			else:
				bet=minB
			self.makeOpeningBet(bet)
			return True
		else:
			self.makeOpeningBet(0)
			return False
