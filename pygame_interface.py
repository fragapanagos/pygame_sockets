"""Defines pygame controller class"""
import sys
import pygame
import socket
import numpy as np
from struct import pack, unpack

def clip(a, minimum, maximum):
	"""clips a value to within a range"""
	return max(minimum, min(a, maximum))

# Define some colors for controller window
BLACK	= (  0,   0,   0)
WHITE	= (255, 255, 255)
BLUE	= (  0,   0, 255)
GREEN	= (  0, 255,   0)
RED		= (255,   0,   0)

class PyGameController(object):
	"""Controller that uses a pygame window as a user interface"""

	def __init__(self, max_signal=3., deadzone_scale=.2, max_loop_speed=10):
		"""Create a controller.

		Args:
			max_signal (float): set the maximum absolute command value to send
			deadzone_scale (float): set the fraction of the window center to not affect the controller output
			max_loop_speed (float): set the maximum number of loops run by the controller per second
		"""
		# width and height of pygame window
		self.width = 800
		self.height = 800

		# set limits
		self.max_signal	= max_signal # maximum absolute value of command
		self.deadzone_scale = deadzone_scale # distance from center required before changing x or y
		self.max_loop_speed = max_loop_speed # max refresh speed of controller when running

		# Initialize pygame engine
		pygame.init()
		
		# create zone where cursor position doesn't affect x or y
		self.deadzone = pygame.Rect(0, 0, self.deadzone_scale * self.width, self.deadzone_scale * self.height)
		self.deadzone.center = (self.width/2, self.height/2) # set center of box at center

		# configure screen
		self.screen = pygame.display.set_mode((self.width, self.height))
		pygame.display.set_caption('Neuroarm Controller')
		self.screen.fill(WHITE)
		pygame.display.flip()

	def run(self, conn):
		"""Run the controller.

		Args:
			conn (socket): socket object to read/write data to
		"""
		# Run until the user clicks the close button
		done = False
		
		# create clock for limiting while loop cycle time
		clock = pygame.time.Clock()
		
		# commands to send
		x,y,z = 0,0,0
		
		while not done:
		
			# Limit while loop speed
			clock.tick(self.max_loop_speed)
		
			for event in pygame.event.get():	# User did something
				if event.type == pygame.QUIT:	# If user clicked close
					done=True					# Flag that we are done so exit loop
		
			self.screen.fill(WHITE)
		
			# draw deadzone where cursor position doesn't affect x or y
			pygame.draw.rect(self.screen, BLACK, self.deadzone)
		
			# get the mouse cursor position
			xpos,ypos = pygame.mouse.get_pos()
			# get the mouse button states
			b1, b2, b3 = pygame.mouse.get_pressed()	# b1,b2,b3 = left,middle,right buttons
		
			# draw a circle at the cursor position
			pygame.draw.circle(self.screen, (255, 0, 0), (xpos, ypos), 10)
		
			# send 0 commands if middle button not pressed
			if b2==0:
				x = 0
				y = 0
				z = 0
			else:
				# convert mouse position into changes in x and y
				dx = xpos-self.width/2
				dy = -(ypos-self.height/2)
		
				if abs(dx) > self.deadzone_scale / 2 * self.width:
					x = clip(x + self.max_signal * dx / (float(self.width)/2.) / self.max_loop_speed, 
					         -self.max_signal, self.max_signal)
				if abs(dy) > self.deadzone_scale / 2 * self.height:
					y = clip(y + self.max_signal * dy / (float(self.height)/2.) / self.max_loop_speed, 
					         -self.max_signal, self.max_signal)	
		
				# convert button presses into changes in z 
				# left,right - increase,decrease z command
				if b1==1 and b3==0:
					z = min(self.max_signal, z + self.max_signal / self.max_loop_speed)
				elif b1==0 and b3==1:
					z = max(-self.max_signal, z - self.max_signal / self.max_loop_speed)
		
			# Display x, y, z on screen
			font = pygame.font.Font(None, 36)
			text = font.render("(x,y,z) = " + str(x) + "," + str(y) + "," + str(z), 1, BLACK)
			textpos = text.get_rect()
			textpos.centerx = self.screen.get_rect().centerx
			self.screen.blit(text, textpos)
		
			# Update screen after all drawing commands
			pygame.display.flip()
		
			# receive data from receiver
			# print 'waiting to receive data...'
			# ack = conn.recv(1024)
			# print 'received', ack
		
			# Send data to receiver
			try:
				# print 'sending', x,y,z
				conn.sendall(pack('ddd', x, y, z))
			except socket.error:
				print 'Send failed'
				sys.exit()
			# print 'sent', x,y,z
		
		conn.close()
		pygame.quit()
