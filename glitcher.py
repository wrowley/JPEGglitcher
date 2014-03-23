import sys
import copy
import random
import os
import argparse
import logging

logging.basicConfig(format='%(message)s',level=logging.INFO)

import jpeg.JPEG as JPEG
import utils.FileManip as fm

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
	theJPEG = JPEG.JPEG()

	#Absorb the file into a ByteArray
	ba = fm.ByteArray()
	ba.absorbFile(jpegfile)
	ba_out = copy.deepcopy(ba)

	#it's the start of the file, so we can be pretty sure about this!
	FF = ba.nextByte()

	if (hex(FF) != '0xff'):
		#but if it turns out it wasn't the start of the file :(
		logging.info('Start of file has' + hex(FF) + ' not 0xff')
		#probably quit
		sys.exit(-2)
	else:
		#otherwise
		logging.info('Found the right marker at start of file')
		#grab a segment yaaay (however this segment is only 2-bytes long including the 0xff)
		segment = JPEG.SegmentFactory.getSegment(ba.nextHexByte(),ba)


	while(True):
		#Add the segment to the JPEG
		theJPEG.addSegment(segment)

		#Break loop once we get to the Huffman coding
		if (segment.__class__ == JPEG.SOSSegment):
			logging.info("BREAKING LOOP AT START OF STREAM")
			break

		#grab the next
		byte = ba.nextHexByte()

		if (byte == '0xff'):
			#if we find '0xff' we have successfully found a new segment
			segment = JPEG.SegmentFactory.getSegment(ba.nextHexByte(),ba)
		else:
			#otherwise i guess quit the loop and report something
			logging.info("After: " + segment.toString()+"")
			logging.info("Found: " + byte + "; Expecting 0xff")
			logging.info("CURSOR AT 0x" + hex(ba.cursor) +"")
			break

	#Retrieve the segments from the jpeg
	theSegments = theJPEG.getSegments()

	#Tell everyone what the jpeg looks like
	logging.info('--The jpeg looks like this inside!--')
	for segment in theSegments:
		logging.info(segment.toString())

	##The following is a fairly ad-hoc and actually pretty troublesome way of ruining the Huffman stream
	##It is troublesome because it will (probably) result in the stream containing codes from the Huffman table
	##which do not exist.
	#The higher this number, the more the roll-off of the writing of bytes as we write them
	#(this limits how totally garbage the imnage gets in the raster-sense
	num = 512
	#How many bytes have we written to the stream?
	timesWritten = 0
	#Point the cursor to the start of the stream
	logging.info('--Destroying the Huffman coding sequence--')
	logging.info('Updating output cursor so we can start writing bytes')
	ba_out.cursor = ba.cursor
	for i in range(ba.cursor,ba.size):
		if (random.randrange(0,(timesWritten+1)*num-(num-1)) == 0):
			logging.info('Writing random byte at location ' + str(ba_out.cursor))
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
