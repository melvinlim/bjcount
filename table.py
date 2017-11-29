from deck import *
from player import *
import random,time
class Table(object):
	def __init__(self,nPlayers,nDecks,bankroll,minBet,bjmultiplier):
		random.seed(time.time)
		self.bjmultiplier=bjmultiplier
		self.nPlayers=nPlayers+1
		self.deck=Deck(nDecks)
		self.players=[]
		self.bankroll=bankroll
		self.minBet=minBet
		for i in range(nPlayers):
			p=Player(i,bankroll)
			self.players.append(p)
		p=Human(i+1,bankroll)
		self.players.append(p)
		self.dealer=Dealer(i+2,bankroll,self)
	def clear(self):
		for p in self.players:
			p.discard()
		self.dealer.discard()
	def newGame(self):
		self.deck.shuffle()
	def deal(self,p):
		card=self.deck.pop()
		if card==None:
			print 'out of cards.  reshuffling.'
			self.deck.refill()
			self.deck.shuffle()
			card=self.deck.pop()
		p.receive(card)
		return card
	def round(self):
		#assert len(self.players)==self.nPlayers+1
		print len(self.players)
		out=[]
		if len(self.players)==0:
			print 'no players remaining'
			return
		for p in self.players:
			if p.bankroll>=self.minBet:
				p.bet(self.minBet)
			else:
				out.append(p)
		for p in out:
			self.players.remove(p)
		for i in range(2):
			for p in self.players:
				if p.betAmount>0:
					self.deal(p)
			self.deal(self.dealer)
		self.disp()
		for p in self.players:
			d=-1
			while d!=0 and self.dealer.eval(p.hand)<21:
				d=p.decide()
				if d==0:
					pass
				elif d==1:
					card=self.deal(p)
					p.disp()
		p=self.dealer
		d=-1
		while d!=0 and self.dealer.eval(p.hand)<21:
			d=p.decide()
			if d==0:
				pass
			elif d==1:
				card=self.deal(p)
				p.disp()
#					print 'dealt '+card.cardString+' to '+str(p.pid)+':'
#		self.disp()
		self.dealer.judge(self.players)
		self.clear()
	def disp(self):
		for p in self.players:
			p.disp()
#			v=self.dealer.eval(p.hand)
#			print v
#		self.deck.printAll()
		self.dealer.disp()
	def status(self):
		for p in self.players:
			p.status()
