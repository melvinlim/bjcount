import random
class Player(object):
	def __init__(self,pid,bankroll):
		self.hand=[]
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
	def receive(self,card):
		assert card!=None
		self.hand.append(card)
	def discard(self):
		self.hand=[]
		self.betBox=0
		self.gamesPlayed+=1
	def win(self,amount):
		self.bankroll+=amount+self.betBox
		self.gamesWon+=1
	def disp(self):
		print 'Player '+str(self.pid)+' ('+str(self.bankroll)+'):\t',
		s=''
		for c in self.hand:
			s+=c.cardString+' '
		print s
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
	def decide(self):
		d=random.randint(0,1)
		if d==0:
			return 'stand'
		else:
			return 'hit'
class Stands(Player):
	def __init__(self,pid,bankroll):
		super(Stands,self).__init__(pid,bankroll)
	def decide(self):
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
	def decide(self):
		print 'Player '+str(self.pid)+':\t',
		print '(h)it/(s)tand?\t',
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
		return d
