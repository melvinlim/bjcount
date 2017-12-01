import random
from hand import *
class Player(object):
	def __init__(self,pid,bankroll):
		self.split=False
		self.hand=Hand()
		self.pid=pid
		self.bankroll=bankroll
		self.startingBankroll=bankroll
		self.gamesPlayed=0
		self.gamesWon=0
		self.betBox=0
	def makeBet(self,amount):
		assert amount<=self.bankroll
		self.bankroll-=amount
		self.betBox+=amount
	def betDecision(self,minB,maxB):
		if self.bankroll>=minB:
			self.makeBet(minB)
			return True
		else:
			return False
	def discard(self):
		self.hand=Hand()
		self.betBox=0
		self.gamesPlayed+=1
	def win(self,amount):
		self.bankroll+=amount+self.betBox
		self.gamesWon+=1
	def payout(self,amount):
		self.bankroll+=amount
	def disp(self):
		print 'Player '+str(self.pid)+' ('+str(self.bankroll)+'):\t',
		print self.hand.textString
	def status(self):
		if self.gamesPlayed==0:
			winsOverGames=0
			earningsPerGame=0
		else:
			winsOverGames=self.gamesWon*1.0/self.gamesPlayed
			earningsPerGame=(self.bankroll-self.startingBankroll)*1.0/self.gamesPlayed
		print 'Player '+str(self.pid)+':',
		print '\twins/games: '+str(winsOverGames),
		print '\tearnings/game: '+str(earningsPerGame)
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
	def betDecision(self,minB,maxB):
		print 'Player '+str(self.pid)+':\t',
		print 'bet amount?\n',
		print '['+str(minB)+']',
		c=raw_input()
		try:
			n=int(c)
			if self.bankroll>=n:
				self.makeBet(n)
				return True
			else:
				return False
		except:
			if self.bankroll>=minB:
				self.makeBet(minB)
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
			self.makeBet(self.betBox)
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
		elif self.hand.isSoft():
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
