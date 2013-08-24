import socket
from struct import unpack
import sys

# socket parameters
host= 'localhost'        # We'll be on the same computer
PORT = 50001              # Arbitrary non-privileged port

# create client socket
try:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, msg:
	print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
	sys.exit();

# get the ip address of the remote host
try: 
	host_ip = socket.gethostbyname(host)
except socket.gaierror:
	print 'Hostname could not be resolved. Exiting'
	sys.exit()

# connect client socket to server socket
try:
	s.connect((host_ip, PORT))
except socket.error, msg:
	print 'Failed to connect socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
	sys.exit();

done = False
while not done:
	# # send data to controller
	# print 'sending hello'
	# try:
	# 	s.sendall('hello')
	# except socket.error:
	# 	print 'Send failed'
	# 	sys.exit()
	# print 'sent hello'

	# look for data from controller
	data = s.recv(1024)
	# run until we stop receiving data
	if not data:
		print 'controller closed, terminating receiver'
		done = True
	else:
		print 'Received', repr(unpack('ddd', data))

# close socket
s.close()
