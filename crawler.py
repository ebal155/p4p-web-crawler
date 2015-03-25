import urllib.request
import gzip, zlib

url = "https://kickass.to/"

#make a request to the url
handle = urllib.request.urlopen(url)

byteOutput =  handle.read()

#Decompress gzip content
htmltxt = zlib.decompress(byteOutput, 15+32)

#Decode bytes into string
htmltxt = str(htmltxt.decode("utf-8"))

#Save to a txt file
outputfilename = "kickass.txt"
f = open(outputfilename, "w")

f.write(htmltxt)
f.close()