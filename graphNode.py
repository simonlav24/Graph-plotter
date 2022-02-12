from math import fabs, sqrt, cos, sin, pi, floor, ceil, e
from random import uniform, randint, choice
import pygame
import sys
import ast
import argparse
from graph import *
if not os.path.exists("vector.py"):
	print("fetching vector")
	import urllib.request
	with urllib.request.urlopen('https://raw.githubusercontent.com/simonlav24/wormsGame/master/vector.py') as f:
		text = f.read().decode('utf-8')
		with open("vector.py", "w+") as vectorpy:
			vectorpy.write(text)
from vector import *
myfont = pygame.font.SysFont('Arial', 22)

##################################################################################### 

def parseArgs():
	parser = argparse.ArgumentParser()
	parser.add_argument('-g', '--graph', type=str, help="graph mathematical definition, for example: ([1,2,3],[(1,2),(1,0)])")
	return parser.parse_args()

colorScheme = [(35, 110, 150), (21, 178, 211), (255, 215, 0), (243, 135, 47), (255, 89, 143)]

DEFAULT_VERTEX_COLOR = colorScheme[1]
DEFAULT_VERTEX_SELECTED_COLOR = colorScheme[2]
DEFAULT_EDGE_COLOR = colorScheme[2]
TEXT_COLOR = (0,0,0)
VERTEX_RADIUS = 20
EDGE_WIDTH = 5
TRIANGLE = [Vector(0, VERTEX_RADIUS), Vector(-VERTEX_RADIUS,0), Vector(0,-VERTEX_RADIUS)]

spots = []
def giveSpot():
	taken = True
	while taken:
		x = randint(-3, 3) * 10
		y = randint(-3, 3) * 10
		if x % 20 == 0:
			y += 5
		if not (x,y) in spots:
			taken = False
	spots.append((x,y))
	return Vector(x,y)

def menuAddVertex(pos):
	Vertex(randint(0,100), tup2vec(closestMargin(parami(pos))))

def closestMargin(x, margin=5):
	if isinstance(x, tuple):
		return (margin * round(x[0]/ margin), margin * round(x[1]/ margin))
	else:
		return margin * round(x / margin)

class Vertex:
	_reg = []
	def __init__(self, value, pos=Vector(0,0)):
		Vertex._reg.append(self)
		self.pos = pos
		self.value = value
		self.vSurf = myfont.render(str(self.value), False, TEXT_COLOR)
		self.color = DEFAULT_VERTEX_COLOR
		self.selected = False
	def draw(self):
		vsurf = self.vSurf
		pygame.draw.circle(win, DEFAULT_VERTEX_SELECTED_COLOR if self.selected else self.color, param(self.pos), VERTEX_RADIUS)
		place = (self.pos[0] - (vsurf.get_width()/globalvars.scaleFactor/2), self.pos[1] + vsurf.get_height()/globalvars.scaleFactor/2)
		win.blit(vsurf, param(place))
		
class Edge:
	_reg = []
	def __init__(self, v1, v2, directed = False):
		Edge._reg.append(self)
		self.v1 = v1
		self.v2 = v2
		self.color = DEFAULT_EDGE_COLOR
	def draw(self):
		distance = dist(self.v1.pos, self.v2.pos)
		p1 = self.v1.pos + (self.v2.pos - self.v1.pos)
		pygame.draw.line(win, self.color, param(self.v1.pos), param(self.v2.pos), EDGE_WIDTH)
		angle = getAngleByTwoVectors(self.v2.pos, self.v1.pos)
		triangle = [vectorCopy(v / globalvars.scaleFactor).rotate(angle) + (self.v2.pos * 0.8 + self.v1.pos * 0.2) for v in TRIANGLE]
		pygame.draw.polygon(win, self.color, [param(v) for v in triangle])

class Menu:
	currentMenu = None
	BACK_COLOR = (100,100,100)
	TEXT_COLOR = (0,0,0)
	BACK_SELECTED_COLOR = (150,150,150)
	def __init__(self, winPos):
		self.winPos = tup2vec(winPos)
		self.elements = []
		self.buttons = []
		self.currentHeight = 5
		self.dims = [0,0]
		self.rect = [winPos, self.dims]
		Menu.currentMenu = self
	def addString(self, string):
		self.elements.append(MenuString(string, self.winPos + Vector(5, self.currentHeight)))
		self.currentHeight += self.elements[-1].height + 5
		self.dims[0] = max(self.dims[0], self.elements[-1].width + 15)
		self.dims[1] = self.currentHeight + 5
	def addButton(self, text, action = None, args = None):
		b = Button(text, self.winPos + Vector(5, self.currentHeight), action, args)
		self.elements.append(b)
		self.buttons.append(b)
		self.currentHeight += self.elements[-1].height + 5
		self.dims[0] = max(self.dims[0], self.elements[-1].width + 20)
		self.dims[1] = self.currentHeight
	def draw(self):
		pygame.draw.rect(win, Menu.BACK_COLOR, self.rect)
		for e in self.elements:
			e.draw()
	def destroy(self):
		for b in self.buttons:
			b.destroy()
		Menu.currentMenu = None
	
class MenuString:
	def __init__(self, string, winPos):
		self.winPos = winPos
		self.surf = myfont.render(string, False, Menu.TEXT_COLOR)
		self.width = self.surf.get_width()
		self.height = self.surf.get_height()
	def draw(self):
		win.blit(self.surf, self.winPos)
	
class Button:
	_reg = []
	def __init__(self, text ,winPos, action = None, args=None):
		Button._reg.append(self)
		self.text = text
		self.selected = False
		self.action = action
		self.args = args
		self.surf = myfont.render(text, False, Menu.TEXT_COLOR)
		self.width = self.surf.get_width()
		self.height = self.surf.get_height() + 10
		self.winPos = winPos
	def activate(self):
		if self.action:
			self.action(*self.args)
		else:
			print("epmty button activated")
	def step(self):
		pass
	def draw(self):
		pygame.draw.rect(win, Menu.BACK_COLOR if not self.selected else Menu.BACK_SELECTED_COLOR, (self.winPos, (self.width + 10, self.height)))
		win.blit(self.surf, self.winPos + Vector(5,5))
	def destroy(self):
		Button._reg.remove(self)

##################################################################################### setup

args = parseArgs()

if args.graph:
	counter = 0
	vertexInput, edgeInput = ast.literal_eval(args.graph)
	for v in vertexInput:
		Vertex(v, Vector(giveSpot()[0], counter))
		counter -= 10
	
	for e in edgeInput:
		Edge(Vertex._reg[e[0]], Vertex._reg[e[1]])

# example graph
# for i in range(10):
	# Vertex(i, giveSpot())
# for i in range(10):
	# Edge(choice(Vertex._reg), choice(Vertex._reg))

setZoom(5)

##################################################################################### Main funcs

MOUSE_HAND = 0
MOUSE_MOVE = 1
MOUSE_EDGE = 2

mouseMode = MOUSE_HAND
oneSelected = None

def nodeEventHandler(events):
	global mouseMode, oneSelected
	
	mousePos = parami(pygame.mouse.get_pos())
	
	for event in events:
		if event.type == pygame.QUIT:
			globalvars.run = False
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: #mouse press main
			globalvars.point = Vector(pygame.mouse.get_pos()[0] / globalvars.scaleFactor, pygame.mouse.get_pos()[1] / globalvars.scaleFactor) 
			globalvars.mousePressed = True
			globalvars.camPrev = Vector(globalvars.cam[0], globalvars.cam[1])
			if Menu.currentMenu:
				for button in Menu.currentMenu.buttons:
					if button.selected:
						button.activate()
			if Menu.currentMenu:
				Menu.currentMenu.destroy()
		if event.type == pygame.MOUSEBUTTONUP and event.button == 1: #mouse release main
			if mouseMode == MOUSE_EDGE:
				second = None
				for vertex in Vertex._reg:
					if vertex.pos[0] - VERTEX_RADIUS/globalvars.scaleFactor < mousePos[0] and mousePos[0] < vertex.pos[0] + VERTEX_RADIUS/globalvars.scaleFactor and \
							vertex.pos[1] - VERTEX_RADIUS/globalvars.scaleFactor < mousePos[1] and  mousePos[1] < vertex.pos[1] + VERTEX_RADIUS/globalvars.scaleFactor:
						second = vertex
						break
				if second:
					Edge(oneSelected, second)
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
			m = Menu(pygame.mouse.get_pos())
			m.addButton("add vertex", menuAddVertex, [m.winPos])
			
		# mouse control
		if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
			globalvars.mousePressed = False
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
			origin = param((0,0))
			mouse = pygame.mouse.get_pos()
			adjust = Vector(mouse[0] - origin[0], mouse[1] - origin[1])
			globalvars.cam = globalvars.cam + adjust * 0.2
			globalvars.scaleFactor += 0.2 * globalvars.scaleFactor
			
			globalvars.gridView = int((downRight()[0] - upLeft()[0])/10) + 1
			globalvars.gridView = max(5 * int(globalvars.gridView/5), 5)
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
			origin = param((0,0))
			mouse = pygame.mouse.get_pos()
			adjust = Vector(mouse[0] - origin[0], mouse[1] - origin[1])
			globalvars.cam = globalvars.cam - adjust * 0.2
			globalvars.scaleFactor -= 0.2 * globalvars.scaleFactor
			
			globalvars.gridView = int((downRight()[0] - upLeft()[0])/10) + 1
			globalvars.gridView = max(5 * int(globalvars.gridView/5), 5)
		# keys pressed once
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_h:
				globalvars.cam = (0,0)
				globalvars.scaleFactor = 5

	lcontrol = False
	keys = pygame.key.get_pressed()
	if keys[pygame.K_ESCAPE]:
		globalvars.run = False
	if keys[pygame.K_LCTRL]:
		lcontrol = True
	
	if globalvars.mousePressed:
		if mouseMode == MOUSE_HAND:
			current = Vector(pygame.mouse.get_pos()[0] / globalvars.scaleFactor, pygame.mouse.get_pos()[1] / globalvars.scaleFactor)
			globalvars.cam = globalvars.camPrev + (globalvars.point - current) * globalvars.scaleFactor
		elif mouseMode == MOUSE_MOVE:
			oneSelected.pos = Vector(closestMargin(mousePos[0]), closestMargin(mousePos[1]))
		elif mouseMode == MOUSE_EDGE:
			pass
	
	if not globalvars.mousePressed:
		oneSelected = None
		if Menu.currentMenu:
			for button in Menu.currentMenu.buttons:
				button.selected = False
				if pygame.mouse.get_pos()[0] > button.winPos[0] and pygame.mouse.get_pos()[0] < button.winPos[0] + button.width and\
						pygame.mouse.get_pos()[1] > button.winPos[1] and pygame.mouse.get_pos()[1] < button.winPos[1] + button.height:
					button.selected = True
		
		for vertex in Vertex._reg:
			if vertex.pos[0] - VERTEX_RADIUS/globalvars.scaleFactor < mousePos[0] and mousePos[0] < vertex.pos[0] + VERTEX_RADIUS/globalvars.scaleFactor and \
					vertex.pos[1] - VERTEX_RADIUS/globalvars.scaleFactor < mousePos[1] and  mousePos[1] < vertex.pos[1] + VERTEX_RADIUS/globalvars.scaleFactor:
				vertex.selected = True
				oneSelected = vertex
				if lcontrol:
					mouseMode = MOUSE_EDGE
				else:
					mouseMode = MOUSE_MOVE
				break
		if not oneSelected:
			mouseMode = MOUSE_HAND

def step():
	pass
def draw():
	for edge in Edge._reg:
		edge.draw()
	for vertex in Vertex._reg:
		vertex.draw()
		vertex.selected = False
		
	if globalvars.mousePressed and mouseMode == MOUSE_EDGE:
		pygame.draw.line(win, DEFAULT_EDGE_COLOR, pygame.mouse.get_pos(), param(oneSelected.pos) , 10)
		
	if Menu.currentMenu:
		Menu.currentMenu.draw()
	
mainLoop(step, draw, nodeEventHandler)