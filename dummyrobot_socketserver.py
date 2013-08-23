import socket
from struct import pack, unpack

# socket parameters
HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50000              # Arbitrary non-privileged port

# create host socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # reuse socket in case already in use
s.bind((HOST, PORT))
s.listen(1) # only allow 1 connection in queue

# wait for client to connect
print 'waiting for client to connect'
conn, addr = s.accept()
print 'Connected by', addr

done = False

q0 = 0
q1 = 0
q2 = 0
dq0 = 0
dq1 = 0
dq2 = 0


while not done:
	# print 'waiting to receive data...'
	gc_torques = conn.recv(1024)
	# print 'received', len(gc_torques)
	# print 'sending',  q0,q1,q2,dq0,dq1,dq2
	conn.sendall(pack('dddddd', q0,q1,q2,dq0,dq1,dq2))
	# print 'sent',  q0,q1,q2,dq0,dq1,dq2

conn.close()
s.close()
