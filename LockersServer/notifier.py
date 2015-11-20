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

for reservation in db.reservations.find():
	now = datetime.now()
	expirationDate = reservation['expirationDate']
	expirationDate = datetime.strptime(expirationDate, '%Y-%m-%d')
	notificationDate = expirationDate - timedelta(1)
	if(notificationDate<now):
		#NOTIFY!!!!!!!