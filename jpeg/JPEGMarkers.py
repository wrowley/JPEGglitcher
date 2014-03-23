##The JFIF is full of these markers, which each follow a "0xff" byte in the file.
##After the "0xff" byte are these markers which say what comes next in the file
markers = {}

##Start of frame markers
markers['SOF'] = []
#Goes c0 to c3...
for i in range(0,4):
	markers['SOF'].append('0xffc'+hex(i)[2])
#Define huffman table section
markers['DHT'] = '0xffc4'
#...and c5 to cb...
for i in range(5,12):
	markers['SOF'].append('0xffc'+hex(i)[2])
#Define arithmetic coding conditioning
markers['DAC'] = '0xffcc'
#...and cd to cf...
for i in range(13,16):
	markers['SOF'].append('0xffc'+hex(i)[2])


##Start of image
markers['SOI'] = '0xffd8'
##End of image
markers['EOI'] = '0xffd9'

##Start of scan
markers['SOS'] = '0xffda'
##Define quantization table(s)
markers['DQT'] = '0xffdb'
##Define number of lines
markers['DNL'] = '0xffdc'
##Define restart interval
markers['DRI'] = '0xffdd'
##Define hierarchical progression
markers['DHP'] = '0xffde'
##Expand reference component(s)
markers['EXP'] = '0xffdf'

##Application markers
markers['APP'] = []
#Goes from e0 to e16
for i in range(0,16):
	markers['APP'].append('0xffe'+hex(i)[2])
##JPEG Extensions
markers['JPG'] = []
#Goes from f0 to f14
for i in range(0,14):
	markers['JPG'].append('0xfff'+hex(i)[2])

##Comment
markers['COM'] = '0xfffe'

##Temporary private use in arithmetic coding
markers['TEM*'] = '0xff01'

##Reserved markers
markers['RES'] = []
tmp = 2
#for 0:b
for i in range(0,12):
	for j in range(tmp,16):
		markers['RES'].append('0xff'+hex(i)[2]+hex(j)[2])
	tmp = 0


