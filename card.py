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
			face='K'
		elif self.tmpVal==1:
			self.bjv=0
			face='A'
		elif self.tmpVal==10:
			self.bjv=10
			face='T'
		elif self.tmpVal==11:
			self.bjv=10
			face='J'
		elif self.tmpVal==12:
			self.bjv=10
			face='Q'
		else:
			self.bjv=self.tmpVal
			face=str(self.tmpVal)
		self.suit=suit
		self.face=face
		self.textString=self.face+self.suit
	def disp(self):
		print self.textString
		#print self.face,self.suit,self.n
