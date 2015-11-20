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
user = form.getvalue('user')

client = MongoClient('localhost',27017)

db = client.lockers
collection = db.reservations

print "Content-Type: text/html"
print ""

reservation = db.reservations.find_one({"user":user})

now = datetime.now()
reservationDate = reservation['reservationDate']
expirationDate = reservation['expirationDate']
reservationDate = datetime.strptime(reservationDate, '%Y-%m-%d')
expirationDate = datetime.strptime(expirationDate, '%Y-%m-%d')

#remainingTime = expirationDate - reservationDate
remainingTime = expirationDate - now
print '{"remainingTime": "'+str(remainingTime)+'", "lockerCode": "'+reservation['lockerCode']+'"}"'