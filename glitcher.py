import sys
import copy
import random
import os
import argparse
import logging

logging.basicConfig(format='%(message)s',level=logging.INFO)

import jpeg.JPEG as JPEG

def main(
	jpegfile,
	):

	# Get the path to the file
	logging.info('Input file: ' + jpegfile)

	# Get path to output file
	jpegfileoutbits = os.path.splitext(jpegfile)
	jpegfileout = jpegfileoutbits[0] + '-out' + jpegfileoutbits[1]
	logging.info('Output file: ' + jpegfileout)

	logging.info('--Attempting to analyse the jpeg--')
	theJPEG = JPEG.JPEG(jpegfile)

	# Retrieve the segments from the jpeg
	theSegments = theJPEG.getSegments()

	# Tell everyone what the jpeg looks like
	logging.info('--The jpeg looks like this inside!--')
	for segment in theSegments:
		logging.info(segment.toString())
		if isinstance(segment, JPEG.SOSSegment):
			huffman_segment = segment

	ba_out        = theJPEG.get_byte_array_clone()
	ba_out.cursor = huffman_segment.get_offset() + huffman_segment.get_length()

	## The following is a fairly ad-hoc and actually pretty troublesome way of ruining the Huffman stream
	## It is troublesome because it will (probably) result in the stream containing codes from the Huffman table
	## which do not exist.
	# The higher this number, the more the roll-off of the writing of bytes as we write them
	# (this limits how totally garbage the imnage gets in the raster-sense
	num = 512
	# How many bytes have we written to the stream?
	timesWritten = 0
	# Point the cursor to the start of the stream
	logging.info('--Destroying the Huffman coding sequence--')
	logging.info('Updating output cursor so we can start writing bytes')
	for i in range(ba_out.cursor,ba_out.size):
		if (random.randrange(0,(timesWritten+1)*num-(num-2)) == 0):
			logging.info('Writing random byte at location ' + hex(ba_out.cursor))
			ba_out.writeNextByte(random.randrange(0,255))
			timesWritten+=1
		else:
			ba_out.moveCursor(1)

	#Write the file out somewhere sensible
	logging.info('--Attempting to write the file out--')
	out_file = open(jpegfileout, "wb")
	out_file.write(ba_out.buf)
	logging.info('Written successfully to ' + jpegfileout + '\n')
	out_file.close()

if __name__ == "__main__":

	parser = argparse.ArgumentParser()

	parser.add_argument(
		"input_file",
		help="Path to the jpeg what requires breaking",
		)

	args = parser.parse_args(sys.argv[1:])

	main(args.input_file)
