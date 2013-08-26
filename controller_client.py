import numpy as np
import socket
from pygame_interface import PyGameController

# socket parameters
HOST = 'localhost'	# Symbolic name meaning all available interfaces
PORT = 50001						# Arbitrary non-privileged port

# create socket 
try:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, msg:
	print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
	sys.exit();

# connect socket to server 
s.connect((HOST, PORT))

# create pygame user interface
controller = PyGameController()

# run controller
controller.run(s)
