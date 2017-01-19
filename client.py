#!/usr/bin/env python

import socket

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# AF_INET means we want an IPv4 socket
# SOCK_STREAM means we want a TCP socket

clientSocket.connect(("www.google.com", 80))

request = "GET / HTTP/1.0\r\n\r\n"
# Blank line signifies the end of the header

clientSocket.sendall(request)

# Read from the socket
response = bytearray()
while True:
	part = clientSocket.recv(1024)
	if (part):
		response.extend(part)
	else:
		break

print response
