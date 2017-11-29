import random,time
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
		self.betAmount=amount
		self.gamesPlayed+=1
	def receive(self,card):
		assert card!=None
		self.hand.append(card)
	def discard(self):
		self.hand=[]
		self.betAmount=0
	def win(self,amount):
		self.bankroll+=amount+self.betAmount
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
class Dealer(Player):
	def __init__(self,pid,bankroll,table):
		super(Dealer,self).__init__(pid,bankroll)
		self.table=table
	def disp(self):
		print 'Dealer:\t\t',
		s=''
		for c in self.hand:
			s+=c.cardString+' '
		print s
	def type1(self):
		v=0
		aces=False
		for c in self.hand:
			if c.bjv==0:
				aces=True
				v+=1
			else:
				v+=c.bjv
		if aces==True:
			if (v+10)<=21:
				v+=10
		if v<17:
			return 1
		elif v==17 and aces==True:
			return 1
		else:
			return 0
	def judge(self,players):
		winners,ties=self.winner(players)
		if winners==[]:
			print 'no winners',
		elif len(winners)==1:
			print 'winner: ',
		else:
			print 'winners: ',
		s=''
		for w in winners:
			if w.blackjack==True:
				w.win(w.betAmount*self.table.bjmultiplier)
			else:
				w.win(w.betAmount)
			s+=str(w.pid)+' '
		print s
		if ties:
			print 'tied: ',
			for p in ties:
				p.win(0)
				print p.pid,
			print
	def decide(self):
		return self.type1()
	def eval(self,hand):
		v=0
		aces=False
		for c in hand:
			if c.bjv==0:
				aces=True
				v+=1
			else:
				v+=c.bjv
		if aces==True:
			if (v+10)<=21:
				v+=10
		return v
	def winner(self,players):
		winners=[]
		ties=[]
		dt=self.eval(self.hand)
		if dt>21:
			dt=0
		for p in players:
			p.blackjack=False
			t=self.eval(p.hand)
			if t>dt:
				if t<=21:
					winners.append(p)
					if t==21 and len(p.hand)==2:
						p.blackjack=True
			elif t==dt:
				ties.append(p)
		return winners,ties
class Human(Player):
	def __init__(self,pid,bankroll):
		super(Human,self).__init__(pid,bankroll)
	def decide(self):
		print 'Player '+str(self.pid)+':\t',
#		self.disp()
		print '(h)it/(s)tand?\t',
		c=raw_input()
		if c=='':
			d=0
		elif c=='h':
			d=1
		elif c=='s':
			d=0
		return d
