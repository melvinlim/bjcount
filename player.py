import random
from hand import *
class Player(object):
	def __init__(self,pid,bankroll):
		self.hasSurrendered=False
		self.insuranceBet=0
		self.hands=[Hand(self)]
		self.pid=pid
		self.bankroll=bankroll
		self.startingBankroll=bankroll
		self.gamesPlayed=0
		self.gamesWon=0
	def decideOnInsurance(self):
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
	def discard(self):
		self.hands=[Hand(self)]
		self.gamesPlayed+=1
	def win(self,amount):
		self.bankroll+=amount+self.hands[0].wager
		self.gamesWon+=1
	def payout(self,amount):
		self.bankroll+=amount
	def disp(self):
		print 'Player '+str(self.pid)+' ('+str(self.bankroll)+'):\t',
		print self.hands[0].textString
	def status(self):
		if self.gamesPlayed==0:
			winPercent=0
			profitPerGame=0
		else:
			winPercent=self.gamesWon*100.0/self.gamesPlayed
			profitPerGame=(self.bankroll-self.startingBankroll)*1.0/self.gamesPlayed
		print 'Player '+str(self.pid)+' ('+str(self.bankroll)+'):\t',
		print 'win%: '+str(winPercent),
		print '\tprofit/game: '+str(profitPerGame)
	def decide(self,table,first,hand):
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
	def decideOnInsurance(self):
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
class BasicNoDouble(Player):
	def __init__(self,pid,bankroll):
		super(BasicNoDouble,self).__init__(pid,bankroll)
	def decide(self,table,first,hand):
		dealerCard=table.dealer.hand.cards[0].bjv
		if dealerCard==0:
			dealerCard=11
		if hand.canSplit():
			if hand.hasAce:
				return 'split'
			elif hand.handValue==20:
				return 'stand'
			elif hand.handValue==18:
				if dealerCard<7:
					return 'split'
				elif dealerCard>9:
					return 'stand'
				elif dealerCard>7:
					return 'split'
				else:
					return 'stand'
			elif hand.handValue==16:
				return 'split'
			elif hand.handValue==14:
				if dealerCard<8:
					return 'split'
				else:
					return 'hit'
			elif hand.handValue==12:
				if dealerCard<7:
					return 'split'
				else:
					return 'hit'
			elif hand.handValue==10:
				return 'hit'
			elif hand.handValue==8:
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
			if hand.handValue>8:
				return 'stand'
			elif hand.handValue==8:
				if dealerCard<9:
					return 'stand'
				else:
					return 'hit'
			else:
				return 'hit'
		else:
			if hand.handValue<12:
				return 'hit'
			elif hand.handValue==12:
				if dealerCard>6:
					return 'hit'
				elif dealerCard<4:
					return 'hit'
				else:
					return 'stand'
			elif hand.handValue==13 or hand.handValue==14:
				if dealerCard>6:
					return 'hit'
				else:
					return 'stand'
			elif hand.handValue==15:
				if dealerCard==10:
					return 'surrender'
				elif dealerCard>6:
					return 'hit'
				else:
					return 'stand'
			elif hand.handValue==16:
				if dealerCard>8:
					return 'surrender'
				elif dealerCard>6:
					return 'hit'
				else:
					return 'stand'
			else:
				return 'stand'
		return 'stand'
class BasicDouble(Player):
	def __init__(self,pid,bankroll):
		super(BasicDouble,self).__init__(pid,bankroll)
	def decide(self,table,first,hand):
		dealerCard=table.dealer.hand.cards[0].bjv
		if dealerCard==0:
			dealerCard=11
		if hand.canSplit():
			if hand.hasAce:
				return 'split'
			elif hand.handValue==20:
				return 'stand'
			elif hand.handValue==18:
				if dealerCard<7:
					return 'split'
				elif dealerCard>9:
					return 'stand'
				elif dealerCard>7:
					return 'split'
				else:
					return 'stand'
			elif hand.handValue==16:
				return 'split'
			elif hand.handValue==14:
				if dealerCard<8:
					return 'split'
				else:
					return 'hit'
			elif hand.handValue==12:
				if dealerCard<7:
					return 'split'
				else:
					return 'hit'
			elif hand.handValue==10:
				if dealerCard<10:
					return 'double'
				else:
					return 'hit'
			elif hand.handValue==8:
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
			if hand.handValue>9:
				return 'stand'
			elif hand.handValue==9:
				if dealerCard==6:
					return 'double'
				else:
					return 'stand'
			elif hand.handValue==8:
				if dealerCard>8:
					return 'hit'
				elif dealerCard>6:
					return 'stand'
				else:
					return 'double'
			elif hand.handValue==7:
				if dealerCard>6:
					return 'hit'
				elif dealerCard<3:
					return 'hit'
				else:
					return 'double'
			elif hand.handValue>4:
				if dealerCard>6:
					return 'hit'
				elif dealerCard<4:
					return 'hit'
				else:
					return 'double'
			else:
				if dealerCard>6:
					return 'hit'
				elif dealerCard<5:
					return 'hit'
				else:
					return 'double'
		else:
			if hand.handValue<9:
				return 'hit'
			elif hand.handValue==9:
				if dealerCard>6 or dealerCard<3:
					return 'hit'
				else:
					return 'double'
			elif hand.handValue==10:
				if dealerCard<10:
					return 'double'
				else:
					return 'hit'
			elif hand.handValue==11:
				return 'double'
			elif hand.handValue==12:
				if dealerCard>6:
					return 'hit'
				elif dealerCard<4:
					return 'hit'
				else:
					return 'stand'
			elif hand.handValue==13 or hand.handValue==14:
				if dealerCard>6:
					return 'hit'
				else:
					return 'stand'
			elif hand.handValue==15:
				if dealerCard==10:
					return 'surrender'
				elif dealerCard>6:
					return 'hit'
				else:
					return 'stand'
			elif hand.handValue==16:
				if dealerCard>8:
					return 'surrender'
				elif dealerCard>6:
					return 'hit'
				else:
					return 'stand'
			else:
				return 'stand'
		return 'stand'
class BasicDoubleR7Count(BasicDouble):
	def __init__(self,pid,bankroll):
		super(BasicDoubleR7Count,self).__init__(pid,bankroll)
	def betDecision(self,minB,maxB,table):
		count=table.shoe.r7count
		if self.bankroll>=minB:
			if count>10:
				bet=maxB
			elif count>5:
				bet=minB+(maxB-minB)*0.5
			else:
				bet=minB
			self.makeOpeningBet(bet)
			return True
		else:
			return False
class BasicDoubleR7CountSitOut(BasicDouble):
	def __init__(self,pid,bankroll):
		super(BasicDoubleR7CountSitOut,self).__init__(pid,bankroll)
	def betDecision(self,minB,maxB,table):
		count=table.shoe.r7count
		if count<10:
			bet=0
			self.makeOpeningBet(0)
			return False
		if self.bankroll>=minB:
			if count>20:
				bet=maxB
			elif count>15:
				bet=minB+(maxB-minB)*0.5
			else:
				bet=minB
			self.makeOpeningBet(bet)
			return True
		else:
			self.makeOpeningBet(0)
			return False
class BasicDoubleR7CountSitOutModified(BasicDouble):
	def __init__(self,pid,bankroll):
		super(BasicDoubleR7CountSitOutModified,self).__init__(pid,bankroll)
	def betDecision(self,minB,maxB,table):
		count=table.shoe.r7count
		if count<10:
			bet=0
			self.makeOpeningBet(0)
			return False
		if self.bankroll>=minB:
			if count>20:
				bet=maxB
			elif count>15:
				bet=minB+(maxB-minB)*0.5
			else:
				bet=minB
			self.makeOpeningBet(bet)
			return True
		else:
			self.makeOpeningBet(0)
			return False
	def decideOnInsurance(self):
		self.bankroll-=self.hands[0].wager/2
		self.insuranceBet=self.hands[0].wager/2
	def decide(self,table,first,hand):
		dealerCard=table.dealer.hand.cards[0].bjv
		if dealerCard==0:
			dealerCard=11
		if hand.canSplit():
			if hand.hasAce:
				return 'split'
			elif hand.handValue==20:
				return 'stand'
			elif hand.handValue==18:
				if dealerCard<7:
					return 'split'
				elif dealerCard>9:
					return 'stand'
				elif dealerCard>7:
					return 'split'
				else:
					return 'stand'
			elif hand.handValue==16:
				return 'split'
			elif hand.handValue==14:
				if dealerCard<8:
					return 'split'
				else:
					return 'hit'
			elif hand.handValue==12:
				if dealerCard<7:
					return 'split'
				else:
					return 'hit'
			elif hand.handValue==10:
				if dealerCard<10:
					return 'double'
				else:
					return 'hit'
			elif hand.handValue==8:
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
			if hand.handValue>9:
				return 'stand'
			elif hand.handValue==9:
				if dealerCard==6:
					return 'double'
				else:
					return 'stand'
			elif hand.handValue==8:
				if dealerCard>8:
					return 'hit'
				elif dealerCard>6:
					return 'stand'
				else:
					return 'double'
			elif hand.handValue==7:
				if dealerCard>6:
					return 'hit'
				elif dealerCard<3:
					return 'hit'
				else:
					return 'double'
			elif hand.handValue>4:
				if dealerCard>6:
					return 'hit'
				elif dealerCard<4:
					return 'hit'
				else:
					return 'double'
			else:
				if dealerCard>6:
					return 'hit'
				elif dealerCard<5:
					return 'hit'
				else:
					return 'double'
		else:
			if hand.handValue<9:
				return 'hit'
			elif hand.handValue==9:
				if dealerCard>6 or dealerCard<3:
					return 'hit'
				else:
					return 'double'
			elif hand.handValue==10:
				if dealerCard<11:
					return 'double'
				else:
					return 'hit'
			elif hand.handValue==11:
				return 'double'
			elif hand.handValue==12:
				if dealerCard>6:
					return 'hit'
				else:
					return 'stand'
			elif hand.handValue==13 or hand.handValue==14:
				if dealerCard>6:
					return 'hit'
				else:
					return 'stand'
			elif hand.handValue==15:
				if dealerCard==10:
					return 'surrender'
				elif dealerCard>6:
					return 'hit'
				else:
					return 'stand'
			elif hand.handValue==16:
				if dealerCard>8:
					return 'surrender'
				elif dealerCard>6:
					return 'hit'
				else:
					return 'stand'
			else:
				return 'stand'
		return 'stand'
