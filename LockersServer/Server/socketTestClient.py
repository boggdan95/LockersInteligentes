#!/usr/bin/python
import SocketServer

class EchoRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        return

if __name__ == '__main__':
    import socket
    import threading
    import socket

    print "Content-Type: text/html"
    print ""

    ip = '127.0.0.1'
    port = 30000

    # Connect to the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))

    # Send the data
    len_sent = s.send("Hello world")

    # Receive a response
    response = s.recv(len_sent)
    print response

    # Clean up
    s.close()
