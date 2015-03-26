import urllib
import gzip, zlib
from scrapy import Spider, Item, Field

url = "https://kickass.to/movies/"

#make a request to the url
handle = urllib.urlopen(url)

#Hex output of request to kickass
byteOutput =  handle.read()

#Decompress gzip content
htmltxt = zlib.decompress(byteOutput, 15+32)

outputFilename = "kickass.txt"

f = open(outputFilename, "w")

f.write(htmltxt)
f.close()