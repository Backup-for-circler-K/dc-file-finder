#-*- coding:utf-8 -*-
from time import *
from bs4 import BeautifulSoup

import urllib.request
import sys
import requests
import os
import hashlib

CHECKSUM = "801b0ee9d41fbe7c58f6547f6a3006e9"
MURL = "http://gall.dcinside.com/mgallery/board/view/?id="
RURL = "http://gall.dcinside.com/board/view/?id="
MGALL = "gohome"
RGALL = "game_classic1"
START = 200000
END = 1600000
split_num = 39
page_item = 50

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

print("[+] Start Crawler")

for i in range(START, END + 1):
	try:
		req = urllib.request.Request(RURL + RGALL + "&no=" + str(i))
		data = urllib.request.urlopen(req).read()
		bs = BeautifulSoup(data, 'html.parser')

		filebox = bs.find('ul', {'class' : 'appending_file'})
		if filebox != None:
			print("[+] Image Found in NO[" + str(i) + "]")
			filebox_image = filebox.find("a")

			url = str(filebox_image).split('"')
			real_url = url[1][split_num:]

			a = str(real_url)
			filename = url[2][1:-4]
			b = a.split("&")
			c = b[0]
			d = b[1][4:]
			e = c + "&" + d
			rp_to = "http://image.dcinside.com/viewimage.php?" + e
			paths = os.getcwd() + "/"
			r = requests.get(rp_to)

			if r.status_code == 200:
				with open(paths + filename, 'wb') as f:
					f.write(r.content)

			vars = md5(filename)
			if CHECKSUM == vars:
				print("[!] WOWWWOWO FOUND IT!! in NO[" + str(i) + "]")
				break
			else:
				print("[!] NOT FOUND in NO[" + str(i) + "]")
				os.popen("rm -rf " + filename)
				sleep(1)
		elif filebox == None:
			print("[+] Image Not Found in NO[" + str(i) + "]")
			sleep(1)
			continue
	except:
		print("[+] Image Not Found in NO[" + str(i) + "]")
		continue