
from jpeg.JPEGMarkers import *
	
class SegmentFactory(object):
	@staticmethod
	def getSegment(hexKey,byteArray):
		if (hexKey == markers['SOI']):
			return Segment()
		elif (markers['APP'].count(hexKey) == 1):
			return ApplicationSegment(byteArray,int(hexKey[3]))
		elif (hexKey == markers['DQT'] ):
			return DQTSegment(byteArray)
		elif (markers['SOF'].count(hexKey) == 1):
			return SOFSegment(byteArray)
		elif (hexKey == markers['SOS']):
			return SOSSegment(byteArray)
		elif (hexKey == markers['COM']):
			return MarkerSegment(byteArray)
		elif (hexKey == markers['EOI']):
			return Segment()
		else:
			print hexKey


class Segment(object):
	def __init__(self):
		pass
				
	def toString(self):
		return str(self.__class__)
			
class MarkerSegment(Segment):
	def __init__(self, byteArray):
		super(MarkerSegment,self).__init__()
		self.ba = byteArray
		self.length = self.ba.nextShort()
		self.bytes = self.ba.nextBytes(self.length - 2)
		
	def toString(self):
		return Segment.toString(self)
		
class DQTSegment(MarkerSegment):
	def __init__(self,byteArray):
		super(DQTSegment,self).__init__(byteArray)
		
	def toString(self):
		return MarkerSegment.toString(self) + ' length -> ' + str(self.length)
		
class SOFSegment(MarkerSegment):
	def __init__(self,byteArray):
		super(SOFSegment,self).__init__(byteArray)
		
	def toString(self):
		return MarkerSegment.toString(self) + ' length -> ' + str(self.length)
		
class SOSSegment(MarkerSegment):
	def __init__(self,byteArray):
		super(SOSSegment,self).__init__(byteArray)
		
	def toString(self):
		return MarkerSegment.toString(self) + ' length -> ' + str(self.length)

		
class ApplicationSegment(MarkerSegment):
	def __init__(self, byteArray, N):
		super(ApplicationSegment,self).__init__(byteArray)
		self.N = N
	
	def toString(self):
		return Segment.toString(self) + ': type -> ' + str(self.N ) + ' length -> ' + str(self.length)

	