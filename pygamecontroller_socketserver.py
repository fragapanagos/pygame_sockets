import pygame
import numpy as np
import socket
from struct import pack, unpack

def clip(a, minimum, maximum):
	return max(minimum, min(a, maximum))

# set limits
scale = 3. # maximum absolute value of command
null_scale = .2 # distance from center required before changing x or y

# width and height of pygame window
width = 800
height = 800

# Initialize pygame engine
pygame.init()

# Define some colors
BLACK	= (  0,   0,   0)
WHITE	= (255, 255, 255)
BLUE	= (  0,   0, 255)
GREEN	= (  0, 255,   0)
RED		= (255,   0,   0)

# configure screen
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Neuroarm Controller')
screen.fill(WHITE)
pygame.display.flip()

# socket parameters
HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50001              # Arbitrary non-privileged port

# create host socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # reuse socket in case already in use
s.bind((HOST, PORT))
s.listen(1) # only allow 1 connection in queue

# wait for client to connect
print 'waiting for client to connect'
conn, addr = s.accept()
print 'Connected by', addr

# Loop until the user clicks the close button
done = False

# create clock for limiting while loop cycle time
clock = pygame.time.Clock()
max_loops_per_sec = 10

# commands to send
x = 0
y = 0
z = 0

while not done:

	# Limit while loop speed
	clock.tick(max_loops_per_sec)

	for event in pygame.event.get():	# User did something
		if event.type == pygame.QUIT:	# If user clicked close
			done=True					# Flag that we are done so exit loop


	screen.fill(WHITE)

	# draw zone where cursor position doesn't affect x or y
	null_box = pygame.Rect(0, 0, null_scale * width, null_scale * height)
	null_box.center = (width/2, height/2) # set center of box at center
	pygame.draw.rect(screen, BLACK, null_box)

	# get the mouse cursor position
	xpos,ypos = pygame.mouse.get_pos()
	# get the mouse button states
	b1, b2, b3 = pygame.mouse.get_pressed()	# b1,b2,b3 = left,middle,right buttons

	# draw a circle at the cursor position
	pygame.draw.circle(screen, (255, 0, 0), (xpos, ypos), 10)

	# send 0 commands if middle button not pressed
	if b2==0:
		x = 0
		y = 0
		z = 0
	else:
		# convert mouse position into changes in x and y
		dx = xpos-width/2
		dy = -(ypos-height/2)

		if abs(dx) > null_scale / 2 * width:
			x = clip(x + scale * dx / (float(width)/2.) / max_loops_per_sec, 
			         -scale, scale)
		if abs(dy) > null_scale / 2 * height:
			y = clip(y + scale * dy / (float(height)/2.) / max_loops_per_sec, 
			         -scale, scale)	

		# convert button presses into changes in z 
		# left,right - increase,decrease z command
		if b1==1 and b3==0:
			z = min(scale, z + scale / max_loops_per_sec)
		elif b1==0 and b3==1:
			z = max(-scale, z - scale / max_loops_per_sec)

	# Display x, y, z on screen
	font = pygame.font.Font(None, 36)
	text = font.render("(x,y,z) = " + str(x) + "," + str(y) + "," + str(z), 1, BLACK)
	textpos = text.get_rect()
	textpos.centerx = screen.get_rect().centerx
	screen.blit(text, textpos)

	# Update screen after all drawing commands
	pygame.display.flip()

	# Send data to client
	# print 'waiting to receive data...'
	ack = conn.recv(1024)
	# print 'received', len(ack)
	# print 'sending', x,y,z
	conn.sendall(pack('ddd', x, y, z))
	# conn.sendall(str(x) + ',' + str(y) + ',' + str(z))
	# print 'sent', x,y,z

conn.close()
pygame.quit()
