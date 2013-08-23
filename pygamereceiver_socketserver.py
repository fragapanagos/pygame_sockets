import socket
from struct import unpack

# socket parameters
HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50001              # Arbitrary non-privileged port

# create host socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # reuse socket in case already in use
s.bind((HOST, PORT))
s.listen(1) # only allow 1 connection in queue

# wait for client to connect
conn, addr = s.accept()
s.close()
print 'Connected by', addr

done = False

while not done:
	# look for data in the socket
	data = conn.recv(1024)

	# run until we stop receiving data
	if not data:
		done = True
	else:
		# print 'Received', repr(unpack('ddd', data))
		print 'Received', data

# close socket
conn.close()
