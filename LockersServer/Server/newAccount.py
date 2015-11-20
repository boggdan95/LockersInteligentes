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
user = form.getvalue('user')
email = form.getvalue('email')
password = form.getvalue('password')

client = MongoClient('localhost',27017)

db = client.lockers
collection = db.users

creationDate = datetime.date.today()

#TODO ID
ID = db.users.find().count()+1

newAccount = {
        "user" : user,
        "ID": str(ID),
        "email" : email,
        "password" : password,
        "creationDate" : str(creationDate),
}

db.users.insert_one(newAccount)

print "Content-Type: text/html"
print ""
print '{"text":"Account created."}'