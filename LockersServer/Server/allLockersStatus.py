#!/usr/bin/python
from pymongo import MongoClient
import random
import datetime
from datetime import datetime
from datetime import timedelta
import cgi
import cgitb
cgitb.enable()

client = MongoClient('localhost',27017)

db = client.lockers

print "Content-Type: text/html"
print ""
print "{u'lockers':["
for locker in db.lockerStatus.find():
	print locker
	print ","
print "]}"