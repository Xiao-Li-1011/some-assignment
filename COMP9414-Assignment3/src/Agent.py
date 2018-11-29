import sys
import socket

def print_view(view):
	print('+-----+')
	for y in range(2, -3, -1):
		line = '|'
		for x in range(-2, 3):
			if not (x == 0 and y ==0):
				line += view[(x, y)]
			else:
				line += '^'
		line += '|'
		print(line)
	print('+-----+')

class Compass:
	def __init__(self, start = 'n'):
		self.directions = ['n', 'e', 's', 'w']
		if start in self.directions:
			self.index = self.directions.index(start)
		else:
			self.index = 0
	def left(self):
		self.index = (self.index - 1) % len(self.directions)
	def right(self):
		self.index = (self.index + 1) % len(self.directions)
	def current(self):
		return self.directions[self.index]

class Agent:
	def __init__(self):
		self.env = {}

		self.border_n = 0
		self.border_e = 0
		self.border_s = 0
		self.border_w = 0

		self.compass = Compass()

		self.axe = set()
		self.key = set()
		self.dynamite = set()
		self.treasure = None

		self.trees = set()
		self.walls = set()
		self.doors = set()
		self.water = set()
		
		self.have_axe = False
		self.have_key = False
		self.have_raft = False
		self.have_treasure = False 
		self.have_dynamite = False

		self.plan_ahead = False

		self.path = []
		self.moves = []

		self.x = 0
		self.y = 0

	def set_path(self, path):
		self.path = path
		self.moves = self.get_moves(path)

	def clear_path(self):
		self.path = []
		self.moves = []

	def show(self):
		line = '+'
		for x in range(self.border_w, self.border_e + 1):
			line += '-'
		line += '+'
		print(line)
		direction = self.compass.current()
		for y in range(self.border_n, self.border_s - 1, -1):
			line = '|'
			for x in range(self.border_w, self.border_e + 1):
				if x == self.x and y == self.y:
					if direction == 'n':
						line += '^'
					elif direction == 'e':
						line += '>'
					elif direction == 's':
						line += 'v'
					elif direction == 'w':
						line += '<'
				elif x == 0 and y == 0:
					line += 'X'
				elif (x, y) in self.env:
					line += self.env[(x, y)]
				else:
					line += '/'
			line += '|'
			print(line)
		line = '+'
		for x in range(self.border_w, self.border_e + 1):
			line += '-'
		line += '+'
		print(line)
		print('Trees: ' + str(self.trees))
		print('Walls: ' + str(self.walls))
		print('Doors: ' + str(self.doors))	
		print('Water: ' + str(self.water))

		print('Axe: ' + str(self.axe))
		print('Key: ' + str(self.key))
		print('Dynamite: ' + str(self.dynamite))	
		print('Treasure: ' + str(self.treasure))

		print('have_axe: ' + str(self.have_axe))
		print('have_key: ' + str(self.have_key))
		print('have_raft: ' + str(self.have_raft))
		print('have_treasure: ' + str(self.have_treasure))
		print('have_dynamite: ' + str(self.have_dynamite))	


	def check(self, pos):
		if self.env[pos] == '':
			pass		
	# def get_action(self):
	# 	if self.have_treasure:
	# 		if not set.moves:
	# 			path = self.pathfind((0, 0))
	# 			self.set_path(path)

	# 		else:
	# 			for m in self.path:
	# 				if not self.valid(m):
	# 					path = self.pathfind((0, 0))
	# 					self.set_path(path)
	# 					break
	# 		return self.moves.pop(0)

	# 	if self.treasure:
	# 		self.check_treasure()

	# 	if not self.moves








if len(sys.argv) < 3:
	print('Usage : {} -p <port>'.format(sys.argv[0]))
	sys.exit()

sd = socket.create_connection(('localhost', sys.argv[2]))
in_stream = sd.makefile('r')
out_stream = sd.makefile('w')

action = ''
agent = Agent()

while True:
	view = {}
	for y in range(2, -3, -1):
		for x in range(-2, 3):
			if not (x == 0 and y == 0):
				ch = in_stream.read(1)
				if ch == -1:
					exit()
				view[(x, y)] = ch

	agent.update(view, action)

	action = agent.get_action()
	out_stream.write(action)
	out_stream.flush()

			
