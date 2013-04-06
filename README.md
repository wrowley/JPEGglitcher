JPEGglitcher
============

A python script and associated tools to mess around with the Huffman coding in a JPEG/JPG (JFIF).

Written in an afternoon, so don't expect super-completeness (works on most JPEGs/JPGs I have tested, but may stumble on some files with weird elements in their file format...)! That is to say, this is not a complete JFIF parser by any stretch of the imagination.

Note that currently this script will ~probably~ totally break the Huffman coding sequence, since it will possibly insert bytes into the stream which contain non-existant Huffman codes. Every time you run it on a JPEGs/JPG it will produce a totally new output.
