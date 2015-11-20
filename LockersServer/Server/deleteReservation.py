#!/usr/bin/python
from pymongo import MongoClient
import random
import datetime
from datetime import datetime
from datetime import timedelta
import cgi
import cgitb
cgitb.enable()

# Create instance of FieldStorage 
form = cgi.FieldStorage() 

# Get data from fields
ID = form.getvalue('ID')

client = MongoClient('localhost',27017)

db = client.lockers
collection = db.reservations

print "Content-Type: text/html"
print ""

reservation = db.reservations.find_one({"ID":ID})
db.lockerStatus.update(
	{ "lockerCode": reservation['lockerCode'] },
	{ '$set': { "lockerStatus": "false" } }
)
#REFRESH LEDS ON LOCKERS!!!!!!!

db.reservations.remove({"ID":ID})

print '{"text":"Reservation removed."}'