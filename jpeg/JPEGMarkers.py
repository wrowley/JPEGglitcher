##The JFIF is full of these markers, which each follow a "0xff" byte in the file.
##After the "0xff" byte are these markers which say what comes next in the file
markers = {}

##Start of image
markers['SOI'] = '0xd8'
##End of image
markers['EOI'] = '0xd9'

##Start of scan
markers['SOS'] = '0xda'
##Define quantization table(s)
markers['DQT'] = '0xdb'
##Define number of lines
markers['DNL'] = '0xdc'
##Define restart interval
markers['DRI'] = '0xdd'
##Define hierarchical progression
markers['DHP'] = '0xde'
##Expand reference component(s)
markers['EXP'] = '0xdf'
##Comment
markers['COM'] = '0xfe'

##Application markers
markers['APP'] = []
#Goes from e0 to e16
for i in range(0,16):
	markers['APP'].append('0xe'+hex(i)[2])

##JPEG Extensions
markers['JPG'] = []
#Goes from f0 to f14
for i in range(0,14):
	markers['JPG'].append('0xf'+hex(i)[2])

##Start of frame markers
markers['SOF'] = []
#Goes c0 to cf
for i in range(0,16):
	markers['SOF'].append('0xc'+hex(i)[2])