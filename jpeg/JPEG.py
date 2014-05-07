import logging
import sys
import copy

import FileManip as fm
from JPEGMarkers import *

class SegmentFactory(object):
	@staticmethod
	def getSegment(marker, byte_array):
		if (marker == markers['SOI']):
			return SOIMarker(byte_array)
		elif (markers['APP'].count(marker) == 1):
			return ApplicationSegment(byte_array)
		elif (marker == markers['DQT'] ):
			return DQTSegment(byte_array)
		elif (markers['SOF'].count(marker) == 1):
			return SOFSegment(byte_array)
		elif (marker == markers['SOS']):
			return SOSSegment(byte_array)
		elif (marker == markers['DHT']):
			return DHTSegment(byte_array)
		elif (marker == markers['DAC']):
			return MarkerSegment(byte_array) #must do this better
		elif (marker == markers['COM']):
			return MarkerSegment(byte_array) #must do this better
		elif (marker == markers['EOI']):
			return EOIMarker(byte_array)
		else:
			logging.error("Unrecognised segment: " + marker)
			return None

class Segment(object):
	def __init__(self):
		pass

	def __str__(self):
		return str(self.__class__)

class MarkerOnly(Segment):
	def __init__(self):
		super(MarkerOnly,self).__init__()

class SOIMarker(MarkerOnly):
	def __init__(self, byte_array):
		super(SOIMarker,self).__init__()
		self.bytes = byte_array.nextBytes(2)

class EOIMarker(MarkerOnly):
	def __init__(self, byte_array):
		super(EOIMarker,self).__init__()
		self.bytes = byte_array.nextBytes(2)

class MarkerSegment(Segment):
	def __init__(self, byte_array):
		super(MarkerSegment,self).__init__()
		self.ba     = byte_array
		self.offset = byte_array.get_cursor()
		# Length is always 2 bytes from the marker
		self.length = byte_array.shortAt(self.offset + 2)
		# And the total size is length + sizeof(marker)
		self.bytes  = byte_array.nextBytes(self.length + 2)

	def get_offset(self):
		return self.offset

	def get_length(self):
		return self.length

	def __str__(self):
		return Segment.__str__(self) + ", offset -> " + hex(self.offset) + ', length -> ' + str(self.length)

class DQTSegment(MarkerSegment):
	def __init__(self,byte_array):
		super(DQTSegment,self).__init__(byte_array)

class SOFSegment(MarkerSegment):
	def __init__(self,byte_array):
		super(SOFSegment,self).__init__(byte_array)

class DHTSegment(MarkerSegment):
	def __init__(self,byte_array):
		super(DHTSegment,self).__init__(byte_array)

class SOSSegment(MarkerSegment):
	def __init__(self,byte_array):
		super(SOSSegment,self).__init__(byte_array)
		#number of bytes corresponding to the header length has already been read..??
		#but 'length' has slightly ambiguous meaning here.. see p37, ISO/IEC 10918-1 : 1993(E)
#		self.bytes.append(self.ba.nextBytes(1)) #compensate for Ns
#		self.bytes.append(self.ba.nextBytes(1)) #compensate for Ss
#		self.bytes.append(self.ba.nextBytes(1)) #compensate for Se
#		self.bytes.append(self.ba.nextBytes(1)) #compensate for Ah & Al (nybble each)

class ApplicationSegment(MarkerSegment):
	def __init__(self, byte_array):
		super(ApplicationSegment,self).__init__(byte_array)
		self.N = byte_array.byteAt(self.offset + 1) & 0xf

	def __str__(self):
		return MarkerSegment.__str__(self) + ' type -> ' + str(self.N)

class JPEG(object):
	def __init__(self, filePath):
		self._filePath   = filePath
		self._byte_array = fm.ByteArray()
		self._segments    = []

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
			self.add_segment(segment)

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
				logging.info("After: " + segment.__str__()+"")
				logging.info("Found: " + byte + "; Expecting 0xff")
				logging.info("CURSOR AT " + hex(self._byte_array.get_cursor()) +"")
				break

	def get_byte_array_clone(self):
		return copy.deepcopy(self._byte_array)

	def add_segment(self, segment):
		self._segments.append(segment)

	def get_segments(self):
		return self._segments

