#!/usr/bin/python
import SocketServer

class EchoRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        return

if __name__ == '__main__':
    import socket
    import threading    
    from pymongo import MongoClient
    import random
    import socket
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
    reservation = db.reservations.find_one({"ID":ID})
    lockerCode = reservation['lockerCode']

    print "Content-Type: text/html"
    print ""

    ip = '127.0.0.1' #ACTUALIZAR CON IP DE RASPBERRY
    port = 30000

    # Connect to the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))

    # Send the data
    len_sent = s.send(lockerCode)

    # Receive a response
    response = s.recv(len_sent)
    #print 'Locker "%s" has been unlocked.' % response
    print '{"text":"Unlocked."}'

    # Clean up
    s.close()