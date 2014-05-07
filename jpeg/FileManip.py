import logging
import array as arr

class ByteArray(object):
	def __init__(self):
		"""A ByteArray, Java-style, except that I like using it."""
		self._size = 0
		self._buf = arr.array('B')
		self._cursor = 0

	def get_size(self):
		return self._size
	def get_buf(self):
		return self._buf
	def get_cursor(self):
		return self._cursor

	def absorbFile(self,filePath):
		"""Read the contents of a file into the ByteArray

		Args:
			filePath - path to the file in the filesystem

		"""
		self._cursor = 0
		in_file = open(filePath, "rb")
		self._buf = arr.array('B',in_file.read())
		in_file.close()
		self._size = len(self._buf)

	def getBytesAt(self, offset, num_bytes):
		"""Get the bytes at the specified offset
		"""
		return self._buf[offset:offset+num_bytes]

	def byteAt(self, offset):
		"""Grab a 'byte' i.e. 8-bit uint from the array at the specified offset
		"""
		bts = self.getBytesAt(offset, 1)
		return bts[0]

	def shortAt(self, offset):
		"""Grab a 'short' i.e. 16-bit uint from the array at the specified offset
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
		if (self._cursor <= self._size):
			byte = self._buf[self._cursor]
			self._cursor = self._cursor + 1
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
		self._buf[self._cursor] = byte
		self._cursor += 1

	def moveCursor(self, N):
		"""Moves cursor forward by N

		Args:
			N - integer to move the cursor forward by (may be negative to move cursor backwards)

		"""
#		logging.info("Cursor was at " + str(self._cursor))
		self._cursor += N
#		logging.info("Cursor now at " + str(self._cursor))


