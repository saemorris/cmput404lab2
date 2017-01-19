#!/usr/bin/env python 

import socket

# AF_INET means we wnat an IPv4 socket
# SOCK_STREAM means we want a TCP packet
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# (client, port)
# need the double brackets
clientSocket.connect(("www.google.com", 80))

# GET - method
# / - path on the server
# HTTP/1.0 - protocal number
# \r\n\r\n - two blank lines, indicates the end of the headers
request = "GET / HTTP/1.0\r\n\r\n"

clientSocket.sendall(request)

response = bytearray()
while True: 
	part = clientSocket.recv(1024)
	if (part):
		response.extend(part)
	else: 
		break

print(response)
