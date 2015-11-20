#!/usr/bin/python
from pymongo import MongoClient
client = MongoClient('localhost',27017)

db = client.lockers

for i in range(100):

	newLocker = {
	        "lockerCode" : str(i),
	        "lockerStatus": "false",
	}

	db.lockerStatus.insert_one(newLocker)