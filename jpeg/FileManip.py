import logging
import array as arr

class ByteArray(object):
	def __init__(self):
		"""A ByteArray, Java-style, except that I like using it."""
		self.size = 0
		self.buf = arr.array('B')
		self.cursor = 0

	def absorbFile(self,filePath):
		"""Read the contents of a file into the ByteArray

		Args:
			filePath - path to the file in the filesystem

		"""
		self.cursor = 0
		in_file = open(filePath, "rb")
		self.buf = arr.array('B',in_file.read())
		in_file.close()
		self.size = len(self.buf)

	def getBytesAt(self, offset, num_bytes):
		"""Get the bytes at the specified offset
		"""
		return self.buf[offset:offset+num_bytes]

	def shortAt(self, offset):
		"""Grab a 'short' i.e. 16-bit uint from the array at the speified offset
		"""
		bts = self.getBytesAt(offset, 2)
		return ((bts[0] << 8) + bts[1])

	def nextShort(self):
		"""Grab a 'short' i.e. 16-bit uint from the file.
		Moves cursor forward by 2.
		"""
		return ((self.nextByte() << 8) + self.nextByte())

	def nextByte(self):
		"""Grab the next byte from the file.
		Moves cursor forward by 1.
		"""
		if (self.cursor <= self.size):
			byte = self.buf[self.cursor]
			self.cursor = self.cursor + 1
		else:
			byte = 0
		return byte

	def nextHexByte(self):
		"""Grab the next byte from the file as a (lower case) hex string
		Moves cursor forward by 1.
		"""
		return hex(self.nextByte())

	def nextHexShort(self):
		"""Grab the next byte from the file as a (lower case) hex string
		Moves cursor forward by 1.
		"""
		return hex(self.nextShort())

	def nextBytes(self,N):
		"""Grab the next N bytes from the file and returns a list containing them in order.
		Moves cursor forward by N.

		Args:
			N - number of bytes to take from stream

		"""
		bytes = []
		for i in range(0,N):
			bytes.append(self.nextByte())
		return bytes


	def writeNextByte(self,byte):
		"""Write a byte into the stream Array at the current cursor.
		Moves cursor forward by 1.

		Args:
			byte - byte to insert into the stream

		"""
		self.buf[self.cursor] = byte
		self.cursor += 1

	def moveCursor(self, N):
		"""Moves cursor forward by N

		Args:
			N - integer to move the cursor forward by (may be negative to move cursor backwards)

		"""
#		logging.info("Cursor was at " + str(self.cursor))
		self.cursor += N
#		logging.info("Cursor now at " + str(self.cursor))


