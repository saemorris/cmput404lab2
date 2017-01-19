#!/usr/bin/env python

import socket, os, sys, errno

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#tell the os to let us reuse the address lots of times in a short period of time
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# bind socket to a specific address and port that our machine has
# a computer has multiple addresses -> localhost, wifi address, 
# ethernet address (0.0.0.0 <- listen to all addresses on the local system
# cannot use ports that are less than 1024 unless you are root
serverSocket.bind(("0.0.0.0", 8000))

# start listening for connections, allow for 5 connection at a times
serverSocket.listen(5)

while True:
	(incomingSocket, address) = serverSocket.accept()
	print "Got a connection from %s" % (repr(address))

	try:
		reaped = os.waitpid(0, os.WNOHANG)
	except OSError, e:
		if e.errno == errno.ECHILD:
			pass
		else:
			raise
	else:
		print "Reaped %s" % (repr(reaped))

	if (os.fork() != 0):
		continue

	clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	clientSocket.connect(("www.google.com", 80))

	incomingSocket.setblocking(0)
	clientSocket.setblocking(0)
	
	while True:
		# read the request
		request = bytearray()
		while True:
			try:
				part = incomingSocket.recv(1024)
			except IOError, e:
				if e.errno == socket.errno.EAGAIN:
					break
			if (part):
				request.extend(part)
				# forward the request to the client
				clientSocket.sendall(part)
			else:
				#quit the program
				sys.exit(0)

		if len(request) > 0:	
			print(request)
	
		response = bytearray()
		while True:
			try:
				part = clientSocket.recv(1024)
			except IOError, e:
				if e.errno == socket.errno.EAGAIN:
					break
			if (part):	
				response.extend(part)
				incomingSocket.sendall(part)
			else:
				sys.exit(0)

		if len(response) > 0:
			print(response)
