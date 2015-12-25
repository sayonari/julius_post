#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Julius web client (with CherryPy:http://www.cherrypy.org/)
# written by Ryota NISHIMURA  2015/Dec./16

import requests
import time
import sys
import codecs

sys.stdout = codecs.getwriter('shift_jis')(sys.stdout)

url = "http://nishimura-asr.local:8000/asr_julius"
files = {
	'myFile': open('test_16000.wav', 'rb')
}
files4 = {
	'myFile': open('test_16000.wav', 'rb')
}
files2 = {
	'myFile': open('yokohama_16000.wav', 'rb')
}
files3 = {
	'myFile': open('long_16000.wav', 'rb')
}

start_time = time.time()
s = requests.Session()
end_time = time.time()
delta_time = end_time - start_time
print "#############################"
print "### -> Time (requests.Session()) : " +  str(delta_time)  + "sec"
print "#############################"

start_time = time.time()
r = s.post(url, files=files)
end_time = time.time()
print r.text
delta_time = end_time - start_time
print "### -> Time (1st connect, 3.30sec) : " +  str(delta_time)   + "sec"
print "#############################" + "\n"

start_time = time.time()
r2 = s.post(url, files=files2)
end_time = time.time()
print r2.text
delta_time = end_time - start_time
print "### -> Time (2nd connect, 2.89sec) : " + str(delta_time)  + "sec"
print "#############################" + "\n"

start_time = time.time()
r = s.post(url, files=files4)
end_time = time.time()
print r.text
delta_time = end_time - start_time
print "### -> Time (re recog, 3.30sec) : " +  str(delta_time)   + "sec"
print "#############################" + "\n"

start_time = time.time()
r3 = s.post(url, files=files3)
end_time = time.time()
print r3.text
delta_time = end_time - start_time
print "### -> Time (other data, 5.37sec) : " + str(delta_time)  + "sec"
print "#############################" + "\n"