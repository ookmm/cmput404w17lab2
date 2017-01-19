#!/usr/bin/env python

import socket, os, sys, errno, select

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Want to listen on all available addresses and bind to this port
serverSocket.bind(("0.0.0.0", 8002))

# Tell OS to start listening
# 5 Connections at the time
serverSocket.listen(5)

while True:
	# Wait for connections to come in
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
	
	# If in the parent process
	if (os.fork() != 0):
		continue
		
	
	clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# AF_INET means we want an IPv4 socket
	# SOCK_STREAM means we want a TCP socket
	
	# Make an outgoing connection to google
	clientSocket.connect(("www.google.com", 80))
	
	# Means that lines where part variables are won't get stuck
	incomingSocket.setblocking(0)
	clientSocket.setblocking(0)
	
	while True:
		request = bytearray()
		while True:
			# If there is nothing else to read, quit the loop
			try:
				part = incomingSocket.recv(1024)
			except IOError, e:
				if e.errno == socket.errno.EAGAIN:
					break
				else:
					raise
					
			if (part):
				request.extend(part)
				clientSocket.sendall(part)
			else:
				sys.exit(0) # quit the program
		if len(request) > 0:
			print(request)
	
		# Third part	
		
		response = bytearray()
		while True:
			try:
				part = clientSocket.recv(1024)
			except IOError, e:
				if e.errno == socket.errno.EAGAIN:
					break
				else:
					raise
					
			if (part):
				response.extend(part)
				# Sending to the browser
				incomingSocket.sendall(part)
			else:
				sys.exit(0) # quit the program
		if len(response) > 0:
			print(response)
			
		select.select(
			[incomingSocket, clientSocket], # read
			[], 									  # write
			[incomingSocket, clientSocket], # exceptions
			0.1									  # times out
		)


