from math import fabs, sqrt, cos, sin, pi, floor, ceil, e
from random import uniform, randint, choice
import pygame
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
from menu import *
myfont = pygame.font.SysFont('Tahoma', 22)

##################################################################################### 

fps = 60

def parseArgs():
	parser = argparse.ArgumentParser()
	parser.add_argument('-g', '--graph', type=str, help="graph mathematical definition, for example: ([1,2,3],[(1,2),(1,0)])")
	return parser.parse_args()

colorScheme = [(35, 110, 150), (21, 178, 211), (255, 215, 0), (243, 135, 47), (255, 89, 143)]

DEFAULT_VERTEX_COLOR = colorScheme[1]
DEFAULT_VERTEX_SELECTED_COLOR = colorScheme[2]
VERTEX_ROOT = (255,0,0)
DEFAULT_EDGE_COLOR = colorScheme[2]
TEXT_COLOR = (0,0,0)
VERTEX_RADIUS = 15
EDGE_WIDTH = 5
TRIANGLE = [Vector(0, VERTEX_RADIUS/2), Vector(-VERTEX_RADIUS,0), Vector(0,-VERTEX_RADIUS/2)]

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
	_selected = None
	def __init__(self, value, pos=Vector(0,0)):
		Vertex._reg.append(self)
		self.pos = pos
		self.value = value
		self.vSurf = myfont.render(str(self.value), True, TEXT_COLOR)
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
		self.directed = directed
	def draw(self):
		if self.directed:
			trianglePos = self.v2.pos - normalize(self.v2.pos - self.v1.pos) * 2*VERTEX_RADIUS / globalvars.scaleFactor
		else:
			trianglePos = self.v2.pos
		pygame.draw.line(win, self.color, param(self.v1.pos), param(trianglePos), EDGE_WIDTH)
		if not self.directed:
			return
		angle = getAngleByTwoVectors(self.v2.pos, self.v1.pos)
		triangle = [vectorCopy(v / globalvars.scaleFactor).rotate(angle) + trianglePos for v in TRIANGLE]
		pygame.draw.polygon(win, self.color, [param(v) for v in triangle])

#####################################################################################

def neighbors(v):
	for edge in Edge._reg:
		if edge.directed:
			if edge.v1 == v:
				yield edge.v2
		else:
			if edge.v1 == v or edge.v2 == v:
				yield edge.v1
				yield edge.v2

def makeRoot(v):
	if Algo._root:
		Algo._root.color = DEFAULT_VERTEX_COLOR
	Algo._root = v
	v.color = VERTEX_ROOT

class Algo:
	_current = None
	_root = None
	def step(self):
		pass

class algoBFS(Algo):
	def __init__(self):
		Algo._current = self
		self.root = None
		self.visited = []
		self.queue = []
		self.colors = {"unvisited": (255,255,0), "visited": (0,0,255), "queue": (0,255,0), "root": (255,0,0)}
		self.time = 0
	def initAlgo(self):
		if Algo._root:
			self.root = Algo._root
		else:
			self.root = Vertex._reg[0]
		self.queue = [self.root]
		for v in Vertex._reg:
			if v == self.root:
				continue
			v.color = self.colors["unvisited"]

	def step(self):
		self.time += 1
		if self.time % (fps//2) != 0:
			return
		if len(self.queue) == 0:
			Algo._current = None
			return
		currentNode = self.queue.pop(0)
		currentNode.color = self.colors["visited"]
		if currentNode == self.root:
			self.root.color = self.colors["root"]
		self.visited.append(currentNode)
		for neighbor in neighbors(currentNode):
			if not neighbor in self.visited and not neighbor in self.queue:
				self.queue.append(neighbor)
				neighbor.color = self.colors["queue"]

def createGridGraph():
	i = 0
	gridSize = 10
	for y in range(-gridSize//2, gridSize//2):
		for x in range(-gridSize//2, gridSize//2):
			Vertex(i, Vector(x * 10, y * 10))
			i += 1

	for v in Vertex._reg:
		vIndex = Vertex._reg.index(v)
		if vIndex >= len(Vertex._reg) - 1:
			continue
		if (vIndex + 1) % gridSize == 0:
			continue
		Edge(v, Vertex._reg[vIndex + 1], directed=False)
		if vIndex + gridSize >= len(Vertex._reg):
			continue
		Edge(v, Vertex._reg[vIndex + gridSize], directed=False)

##################################################################################### menu

def initializeRightClickMenu():
	menuRightClick = findMenu("rightClick")
	if menuRightClick:
		Menu._reg.remove(menuRightClick)

	menuRightClick = Menu(name="rightClick" ,pos=pygame.mouse.get_pos(), size=Vector(100,100), register=True)
	menuRightClick.insert(MENU_BUTTON, text="Add Vertex", key="addVertex")

def initializeRightClickVertex():
	menuRightClick = Menu(name="rightClickVertex" ,pos=pygame.mouse.get_pos(), size=Vector(100,80), register=True)
	Menu.parameters = [Vertex._selected]
	menuRightClick.insert(MENU_BUTTON, text="make root", key="makeRoot")

def initializeAlgoMenu():
	menuAlgo = Menu(name="algo" ,pos=Vector(10,10), size=Vector(100,600), register=True)
	menuAlgo.insert(MENU_BUTTON, text="Run BFS", key="runBfs")
	menuAlgo.insert(MENU_BUTTON, text="test2", key="test2")
	menuAlgo.insert(MENU_BUTTON, text="test3", key="test3")

def menuEvents(event):
	if event.key == "addVertex":
		Vertex(str(len(Vertex._reg)), pos=parami(closestMargin(event.getSuperMenu().pos)))
	
	if event.key == "makeRoot":
		print(Vertex._selected)
		makeRoot(event.getSuperMenu().parameters[0])

	if event.key == "runBfs":
		algoBFS().initAlgo()

	if event.getSuperMenu().name == "rightClick":
		Menu._reg.remove(event.getSuperMenu())
	if event.getSuperMenu().name == "rightClickVertex":
		Menu._reg.remove(event.getSuperMenu())

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

# createGridGraph()
# example graph
# for i in range(10):
# 	Vertex(i, giveSpot())
# for i in range(10):
# 	Edge(choice(Vertex._reg), choice(Vertex._reg))

setZoom(5)
setFps(fps)
setWinSize((1280, 720))
Menu._font = myfont
Menu._win = win

initializeAlgoMenu()
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
		menuHandleEvents(event, menuEvents)
		if event.type == pygame.QUIT:
			globalvars.run = False
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: #mouse press main
			globalvars.point = Vector(pygame.mouse.get_pos()[0] / globalvars.scaleFactor, pygame.mouse.get_pos()[1] / globalvars.scaleFactor) 
			globalvars.mousePressed = True
			globalvars.camPrev = Vector(globalvars.cam[0], globalvars.cam[1])
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
			pass
		
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3: #right click
			if Vertex._selected:
				initializeRightClickVertex()
			else:
				initializeRightClickMenu()

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
		Vertex._selected = None
		for vertex in Vertex._reg:
			if vertex.pos[0] - VERTEX_RADIUS/globalvars.scaleFactor < mousePos[0] and mousePos[0] < vertex.pos[0] + VERTEX_RADIUS/globalvars.scaleFactor and \
					vertex.pos[1] - VERTEX_RADIUS/globalvars.scaleFactor < mousePos[1] and  mousePos[1] < vertex.pos[1] + VERTEX_RADIUS/globalvars.scaleFactor:
				vertex.selected = True
				Vertex._selected = vertex
				oneSelected = vertex
				if lcontrol:
					mouseMode = MOUSE_EDGE
				else:
					mouseMode = MOUSE_MOVE
				break
		if not oneSelected:
			mouseMode = MOUSE_HAND

def step():
	menuStep()
	if Algo._current:
		Algo._current.step()

def draw():
	for edge in Edge._reg:
		edge.draw()
	for vertex in Vertex._reg:
		vertex.draw()
		vertex.selected = False
		
	if globalvars.mousePressed and mouseMode == MOUSE_EDGE:
		pygame.draw.line(win, DEFAULT_EDGE_COLOR, pygame.mouse.get_pos(), param(oneSelected.pos) , 10)
	menuDraw()

mainLoop(step, draw, nodeEventHandler)