import random
class Player(object):
	def __init__(self,pid,bankroll):
		self.hand=[]
		self.pid=pid
		self.bankroll=bankroll
		self.startingBankroll=bankroll
		self.gamesPlayed=0
		self.gamesWon=0
	def bet(self,amount):
		assert amount<=self.bankroll
		self.bankroll-=amount
		self.betBox=amount
		self.gamesPlayed+=1
	def receive(self,card):
		assert card!=None
		self.hand.append(card)
	def discard(self):
		self.hand=[]
		self.betBox=0
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
		print 'Player '+str(self.pid)+':',
		print '\twins/games: '+str(self.gamesWon*1.0/self.gamesPlayed),
		print '\tearnings/game: '+str((self.bankroll-self.startingBankroll)*1.0/self.gamesPlayed)
	def decide(self):
		return random.randint(0,1)
class Stands(Player):
	def __init__(self,pid,bankroll):
		super(Stands,self).__init__(pid,bankroll)
	def decide(self):
		return 0
class Human(Player):
	def __init__(self,pid,bankroll):
		super(Human,self).__init__(pid,bankroll)
	def decide(self):
		print 'Player '+str(self.pid)+':\t',
		print '(h)it/(s)tand?\t',
		c=raw_input()
		if c=='':
			d=0
		elif c=='h':
			d=1
		elif c=='s':
			d=0
		return d
