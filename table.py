from deck import *
#from player import *
from dealer import *
class Table(object):
	def __init__(self,players,nDecks,bankroll,minBet,maxBet,bjmultiplier):
		self.bjmultiplier=bjmultiplier
		self.deck=Deck(nDecks)
		self.players=players
		self.bankroll=bankroll
		self.minBet=minBet
		self.maxBet=maxBet
		self.dealer=Dealer(-1,bankroll,self)
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
