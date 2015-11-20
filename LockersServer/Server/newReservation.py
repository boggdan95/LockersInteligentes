#!/usr/bin/python
from pymongo import MongoClient
import random
import datetime
from datetime import timedelta
import cgi
import cgitb
#cgitb.enable()

# Create instance of FieldStorage 
form = cgi.FieldStorage() 

# Get data from fields
ID = form.getvalue('ID')
lockerCode = form.getvalue('lockerCode')
days = int(form.getvalue('days'))

client = MongoClient('localhost',27017)

db = client.lockers
collection = db.reservations

reservationDate = datetime.date.today()
expirationDate = timedelta(days)
expirationDate = expirationDate + reservationDate

lockerRequested = db.lockerStatus.find_one({"lockerCode" : lockerCode})
lockerReservated = lockerRequested['lockerStatus']
lockerCode = lockerRequested['lockerCode']

pin = random.randint(1000,9999)

newReservation = {
        "ID" : ID,
        "reservationDate" : str(reservationDate),
        "expirationDate" : str(expirationDate),
        "lockerCode" : lockerCode,
        "pin" : pin
}

db.reservations.insert_one(newReservation)
db.lockerStatus.update(
    { "lockerCode": lockerCode },
    { '$set': { "lockerStatus": "true" } }
)
#REFRESH LEDS ON LOCKERS!!!!!!

print "Content-Type: text/html"
print ""
print newReservation