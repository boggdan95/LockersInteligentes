#!/usr/bin/python
from pymongo import MongoClient
import cgi
import cgitb
cgitb.enable()

# Create instance of FieldStorage 
form = cgi.FieldStorage() 

# Get data from fields
pin = form.getvalue('pin')
lockerCode = form.getvalue('lockerCode')

client = MongoClient('localhost',27017)

db = client.lockers
collection = db.users

print "Content-Type: text/html"
print ""

#TODO ID
locker = db.reservations.find_one({'lockerCode':lockerCode})
print locker
if(int(locker['pin'])==int(pin)):
	print 1
else:
	print 0