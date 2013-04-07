import sys
import copy
import random
import os

import jpeg.JPEG as JPEG
import utils.FileManip as fm
import utils.Logging as Logging




if __name__ == "__main__":
	
	#Set up debug logging...
	debug = Logging.Logger(True)
	
	debug.log('\n--Interpreting arguments--')
	#Check someone provided a jpeg and only a jpg
	if (len(sys.argv) != 2):
		print 'Hey! Provide the path to a jpeg/jpg as the first argument!\n'
		sys.exit(-1)

	
	#Get the path to the file
	jpegfile = sys.argv[1]
	debug.log('Input file: ' + jpegfile)
	jpegfileoutbits = os.path.splitext(jpegfile)
	jpegfileout = jpegfileoutbits[0] + '-out' + jpegfileoutbits[1]
	debug.log('Output file: ' + jpegfileout)
	
	debug.log('\n--Attempting to analyse the jpeg--')
	theJPEG = JPEG.JPEG()
	
	#Absorb the file into a ByteArray
	ba = fm.ByteArray()
	ba.absorbFile(jpegfile)
	ba_out = copy.deepcopy(ba)
	
	#it's the start of the file, so we can be pretty sure about this!
	FF = ba.nextByte()
	
	if (hex(FF) != '0xff'):
		#but if it turns out it wasn't the start of the file :(
		debug.log('Start of file has' + hex(FF) + ' not 0xff')
		#probably quit
		sys.exit(-2)
	else:
		#otherwise
		debug.log('Found the right marker at start of file')
		#grab a segment yaaay (however this segment is only 2-bytes long including the 0xff)
		segment = JPEG.SegmentFactory.getSegment(ba.nextHexByte(),ba)
	
		
	while(True):
		#Add the segment to the JPEG
		theJPEG.addSegment(segment)
	
		#this is a pretty crappy and possibly confusing break condition,
		#basically break if we've found the start of the Huffman stream!
		if (segment.__class__ == JPEG.SOSSegment):
			#(the JPEG.SOSSegment describes but is not the stream, so it is okay that we have absorbed it)
			debug.log('SOS Segment done and now we can wreck things')
			break
	
		#grab the next
		byte = ba.nextHexByte()
		
		if (byte == '0xff'):
			#if we find '0xff' we have successfully found a new segment
			segment = JPEG.SegmentFactory.getSegment(ba.nextHexByte(),ba)
		else:
			#otherwise i guess quit the loop
			break
		
		#let's describe the segment we found
		#debug.log(segment.toString())
		
	#Retrieve the segments from the jpeg
	theSegments = theJPEG.getSegments()
	
	#Tell everyone what the jpeg looks like
	debug.log('\n--The jpeg looks like this inside!--')
	for segment in theSegments:
		debug.log(segment.toString())
	
	##The following is a fairly ad-hoc and actually pretty troublesome way of ruining the Huffman stream
	##It is troublesome because it will (probably) result in the stream containing codes from the Huffman table
	##which do not exist.
	#The higher this number, the more the roll-off of the writing of bytes as we write them
	#(this limits how totally garbage the imnage gets in the raster-sense
	num = 512
	#How many bytes have we written to the stream?
	timesWritten = 0
	#Point the cursor to the start of the stream
	debug.log('\n--Destroying the Huffman coding sequence--')
	debug.log('Updating output cursor so we can start writing bytes')
	ba_out.cursor = ba.cursor
	for i in range(ba.cursor,ba.size):
		if (random.randrange(0,(timesWritten+1)*num-(num-1)) == 0):
			debug.log('Writing random byte at location ' + str(ba_out.cursor))
			ba_out.writeNextByte(random.randrange(0,255))
			timesWritten+=1
		else:
			ba_out.moveCursor(1)
	
	
	#Write the file out somewhere sensible
	debug.log('\n--Attempting to write the file out--')
	out_file = open(jpegfileout, "wb")
	out_file.write(ba_out.buf)
	debug.log('Written successfully to ' + jpegfileout + '\n')
	out_file.close()
	
	