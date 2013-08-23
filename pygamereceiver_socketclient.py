import socket
from struct import unpack

# socket parameters
HOST = 'localhost'        # We'll be on the same computer
PORT = 50001              # Arbitrary non-privileged port

# create client socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

done = False

while not done:
	# look for data in the socket
	s.sendall('')
	data = s.recv(1024)

	# run until we stop receiving data
	if not data:
		done = True
	else:
		print 'Received', repr(unpack('ddd', data))
		# print 'Received', data

# close socket
s.close()
