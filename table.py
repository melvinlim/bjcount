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
#		p=Human(i+1,bankroll)
		p=Stands(i+1,bankroll)
		self.players.append(p)
		self.dealer=Dealer(i+2,bankroll,self)
	def newGame(self):
		self.deck.shuffle()
	def dealCard(self,p):
		card=self.deck.pop()
		if card==None:
			print 'out of cards.  reshuffling.'
			self.deck.refill()
			self.deck.shuffle()
			card=self.deck.pop()
		p.receive(card)
		return card
	def round(self):
		self.dealer.step(self.players)
	def disp(self):
		for p in self.players:
			p.disp()
#		self.deck.printAll()
		self.dealer.disp()
	def status(self):
		for p in self.players:
			p.status()
