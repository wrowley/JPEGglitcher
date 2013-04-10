
from jpeg.JPEGMarkers import *


class JPEG(object):
	def __init__(self):
		self.segments = []
		pass
	
	def addSegment(self, segment):
		self.segments.append(segment)
		
	def getSegments(self):
		return self.segments

class SegmentFactory(object):
	@staticmethod
	def getSegment(hexKey,byteArray):
		if (hexKey == markers['SOI']):
			return SOIMarker()
		elif (markers['APP'].count(hexKey) == 1):
			return ApplicationSegment(byteArray,int(hexKey[3]))
		elif (hexKey == markers['DQT'] ):
			return DQTSegment(byteArray)
		elif (markers['SOF'].count(hexKey) == 1):
			return SOFSegment(byteArray)
		elif (hexKey == markers['SOS']):
			return SOSSegment(byteArray)
		elif (hexKey == markers['DHT']):
			return DHTSegment(byteArray)
		elif (hexKey == markers['DAC']):
			return MarkerSegment(byteArray) #must do this better
		elif (hexKey == markers['COM']):
			return MarkerSegment(byteArray) #must do this better
		elif (hexKey == markers['EOI']):
			return EOIMarker()
		else:
			print hexKey


class Segment(object):
	def __init__(self):
		pass
				
	def toString(self):
		return str(self.__class__)
		
class MarkerOnly(Segment):
	def __init__(self):
		super(MarkerOnly,self).__init__()

class SOIMarker(MarkerOnly):
	def __init__(self):
		super(SOIMarker,self).__init__()
		
class EOIMarker(MarkerOnly):
	def __init__(self):
		super(EOIMarker,self).__init__()

		
			
class MarkerSegment(Segment):
	def __init__(self, byteArray):
		super(MarkerSegment,self).__init__()
		self.offset = byteArray.cursor - 2
		self.ba = byteArray
		self.length = self.ba.nextShort()
		self.bytes = self.ba.nextBytes(self.length - 2)
		
	def toString(self):
		return Segment.toString(self) + ", offset -> " + hex(self.offset) + ', length -> ' + str(self.length)
		
class DQTSegment(MarkerSegment):
	def __init__(self,byteArray):
		super(DQTSegment,self).__init__(byteArray)
		
	def toString(self):
		return MarkerSegment.toString(self)
		
class SOFSegment(MarkerSegment):
	def __init__(self,byteArray):
		super(SOFSegment,self).__init__(byteArray)
		
	def toString(self):
		return MarkerSegment.toString(self)
		
class DHTSegment(MarkerSegment):
	def __init__(self,byteArray):
		super(DHTSegment,self).__init__(byteArray)
		
	def toString(self):
		return MarkerSegment.toString(self)
		
class SOSSegment(MarkerSegment):
	def __init__(self,byteArray):
		super(SOSSegment,self).__init__(byteArray)
		#number of bytes corresponding to the header length has already been read..??
		#but 'length' has slightly ambiguous meaning here.. see p37, ISO/IEC 10918-1 : 1993(E)
#		self.bytes.append(self.ba.nextBytes(1)) #compensate for Ns
#		self.bytes.append(self.ba.nextBytes(1)) #compensate for Ss
#		self.bytes.append(self.ba.nextBytes(1)) #compensate for Se
#		self.bytes.append(self.ba.nextBytes(1)) #compensate for Ah & Al (nybble each)
		
		
	def toString(self):
		return MarkerSegment.toString(self)

		
class ApplicationSegment(MarkerSegment):
	def __init__(self, byteArray, N):
		super(ApplicationSegment,self).__init__(byteArray)
		self.N = N
	
	def toString(self):
		return MarkerSegment.toString(self) + ' type -> ' + str(self.N)

	