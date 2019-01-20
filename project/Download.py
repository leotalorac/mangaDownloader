from bs4 import BeautifulSoup as bs
from urllib.request import (
    urlopen, urlparse, urlunparse, urlretrieve,Request,HTTPError)
import os
import binascii
import struct
import sys
import shutil
import time

# headers fro the request
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
   'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
   'Accept-Encoding': 'none',
   'Accept-Language': 'en-US,en;q=0.8',
   'Connection': 'keep-alive'}
hdr2 = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11','Accept': 'bytes','Connection': 'keep-alive'}

def main():
	url = input("write the url \n")
	nimg = int(input("put the number of images \n"))+1
	name = input("Put the name of the anime\n")
	ch = input("Put the number of the anime chapter\n")
	newpath = "../Images/"+name.replace(" ","_") 
	if not os.path.exists(newpath):
		os.makedirs(newpath)
	folder = newpath+"/"+name.replace(" ","_")+"_chapter"+str(ch)
	if not os.path.exists(folder):
		os.makedirs(folder)
	for i in range(1,nimg):
		urls = url + str(i)
		print(urls)
		img = downloadimage(urls,nimg,i,folder)
		print(str(i)+".jpg")		
		if(i%10 == 0):
			print("wait")
			time.sleep(30)
	file = newpath+"/chapter"+str(ch)
	shutil.make_archive(newpath+"/chapter"+str(ch), 'zip', folder)
	print("make zip")
	thisFile = file + ".zip" 
	base = os.path.splitext(thisFile)[0]
	print(base)
	os.rename(thisFile, base + ".cbr")
def downloadimage(url,n,i,folder):
	req = Request(url, headers=hdr)
	try:
		page = urlopen(req)
		soup = bs(page,"lxml")
		parsed = list(urlparse(url))
		img = soup.findAll("img")
		nameimg = iroute(i) + ".jpg"
		image = img[0]
		outpath = os.path.join(folder, nameimg)
		parsed[2] = image["src"]
		if image["src"].lower().startswith("http://"):
			urlretrieve(image["src"], outpath)
		else:
			reqimg = Request(image["src"], headers=hdr2)
			imgreq = urlopen(reqimg)
			# Download the data.
			with imgreq as in_file:
				hex_data = in_file.read()
			with open(outpath, 'wb') as out_file:
				out_file.write(hex_data)
	except Exception as ex :
		print("error " + str(type(ex)) + str(ex))

def iroute(i):
	stringi = str(i);
	ze = 3-len(stringi)
	stringi = ("0"*ze)+stringi
	return stringi
if __name__ == "__main__":
	main()