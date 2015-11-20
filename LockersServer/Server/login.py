#!/usr/bin/python
from pymongo import MongoClient
import random
import datetime
from datetime import timedelta
import cgi
import cgitb
cgitb.enable()

# Create instance of FieldStorage 
form = cgi.FieldStorage() 

# Get data from fields
email = form.getvalue('email')
password = form.getvalue('password')

client = MongoClient('localhost',27017)

db = client.lockers

if(db.users.find({"email":email}).count()!=0):
	if(db.users.find_one({"email":email})['password']==password):
		credenciales = "true"
	else:
		credenciales = "false"
else:
	credenciales = "false"

if(credenciales=="true"):
	ID = db.users.find_one({"email":email})['ID']
	if(db.reservations.find({"ID":ID}).count()!=0):
		reservation = db.reservations.find_one({"ID":ID})

		data = {
	        "reservationDate" : reservation['reservationDate'],
	        "expirationDate" : reservation['expirationDate'],
	        "lockerCode" : reservation['lockerCode'],
	        "pin" : reservation['pin']
		}

		info = {
		"credenciales" : credenciales,
		"reservacion" : "true",
		"data": data,
		"ID" : ID,
		}
	else:
		info = {
			"credenciales" : credenciales,
			"reservacion" : "false",
			"ID" : ID,
		}	
else:
	info = {
		"credenciales" : credenciales
	}

print "Content-Type: text/html"
print ""
print info