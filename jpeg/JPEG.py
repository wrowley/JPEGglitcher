import logging
import sys
import copy

import FileManip as fm
from JPEGMarkers import *

class SegmentFactory(object):
	@staticmethod
	def getSegment(hexKey,byteArray):
		if (hexKey == markers['SOI']):
			return SOIMarker(byteArray)
		elif (markers['APP'].count(hexKey) == 1):
			return ApplicationSegment(byteArray,int(hexKey[5]))
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
			return EOIMarker(byteArray)
		else:
			logging.error("Unrecognised segment: " + hexKey)
			return None

class Segment(object):
	def __init__(self):
		pass

	def toString(self):
		return str(self.__class__)

class MarkerOnly(Segment):
	def __init__(self):
		super(MarkerOnly,self).__init__()

class SOIMarker(MarkerOnly):
	def __init__(self, byteArray):
		super(SOIMarker,self).__init__()
		self.bytes = byteArray.nextBytes(2)

class EOIMarker(MarkerOnly):
	def __init__(self, byteArray):
		super(EOIMarker,self).__init__()
		self.bytes = byteArray.nextBytes(2)

class MarkerSegment(Segment):
	def __init__(self, byte_array):
		super(MarkerSegment,self).__init__()
		self.ba     = byte_array
		self.offset = byte_array.cursor
		# Length is always 2 bytes from the marker
		self.length = byte_array.shortAt(self.offset + 2)
		# And the total size is length + sizeof(marker)
		self.bytes  = byte_array.nextBytes(self.length + 2)

	def get_offset(self):
		return self.offset

	def get_length(self):
		return self.length

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

class JPEG(object):
	def __init__(self, filePath):
		self._filePath   = filePath
		self._byte_array = fm.ByteArray()
		self.segments    = []

		self._init_segments()

	def _init_segments(self):
		#Absorb the file into a ByteArray
		self._byte_array.absorbFile(self._filePath)

		#it's the start of the file, so we can be pretty sure about this!
		FFD8 = self._byte_array.nextHexShort()
		self._byte_array.moveCursor(-2)

		if (FFD8 != '0xffd8'):
			#but if it turns out it wasn't the start of the file :(
			logging.info('Start of file has ' + FFD8 + ' not 0xffd8')
			#probably quit
			sys.exit(-2)

		segment = SegmentFactory.getSegment(FFD8, self._byte_array)

		while(True):
			#Add the segment to the JPEG
			self.addSegment(segment)

			#Break loop once we get to the Huffman coding
			if (segment.__class__ == SOSSegment):
				logging.info("BREAKING LOOP AT START OF STREAM")
				break

			#grab the next
			hex_short = self._byte_array.nextHexShort()
			self._byte_array.moveCursor(-2)

			#if we find '0xff' we have successfully found a new segment
			segment = SegmentFactory.getSegment(hex_short, self._byte_array)

			if not segment:
				#otherwise i guess quit the loop and report something
				logging.info("After: " + segment.toString()+"")
				logging.info("Found: " + byte + "; Expecting 0xff")
				logging.info("CURSOR AT " + hex(self._byte_array.cursor) +"")
				break

	def get_byte_array_clone(self):
		return copy.deepcopy(self._byte_array)

	def addSegment(self, segment):
		self.segments.append(segment)

	def getSegments(self):
		return self.segments

