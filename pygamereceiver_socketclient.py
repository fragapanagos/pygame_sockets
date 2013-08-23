import socket
from struct import unpack

# socket parameters
HOST = 'localhost'        # We'll be on the same computer
PORT = 50001              # Arbitrary non-privileged port

# create client socket
try:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, msg:
	print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
	sys.exit();

# connect client socket to server socket
s.connect((HOST, PORT))

done = False

while not done:
	# look for data in the socket
	# s.sendall('hello')

	data = s.recv(1024)

	# run until we stop receiving data
	if not data:
		done = True
	else:
		print 'Received', repr(unpack('ddd', data))
		# print 'Received', data

# close socket
s.close()
