class Card(object):
	def __init__(self,n):
		self.n=n
		self.tmpVal=n%13
		self.s=n/13
		if self.s==0:
			suit='c'
		elif self.s==1:
			suit='h'
		elif self.s==2:
			suit='d'
		elif self.s==3:
			suit='s'
		else:
			assert False
		if self.tmpVal==0:
			self.bjv=10
			value='K'
		elif self.tmpVal==1:
			self.bjv=0
			value='A'
		elif self.tmpVal==10:
			self.bjv=10
			value='T'
		elif self.tmpVal==11:
			self.bjv=10
			value='J'
		elif self.tmpVal==12:
			self.bjv=10
			value='Q'
		else:
			self.bjv=self.tmpVal
			value=str(self.tmpVal)
		self.suit=suit
		self.value=value
		self.textString=self.value+self.suit
	def disp(self):
		print self.textString
		#print self.value,self.suit,self.n
