from math import fabs, sqrt, cos, sin, pi, floor, ceil, e
from random import uniform, randint, choice
import os
if not os.path.exists("vector.py"):
	print("fetching vector")
	import urllib.request
	with urllib.request.urlopen('https://raw.githubusercontent.com/simonlav24/wormsGame/master/vector.py') as f:
		text = f.read().decode('utf-8')
		with open("vector.py", "w+") as vectorpy:
			vectorpy.write(text)
from vector import *
import pygame
pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Arial', 16)

fpsClock = pygame.time.Clock()

############################################################################### transformations

class globalVars:
	def __init__(self):
		self.scaleFactor = 5
		self.gridView = 20
		self.cam = Vector()
		
		self.mousePressed = False
		self.run = True
		
		self.winWidth = 800
		self.winHeight = 500

globalvars = globalVars()

win = pygame.display.set_mode((globalvars.winWidth, globalvars.winHeight))
pygame.display.set_caption('Simon\'s graph')

def param(pos):
	return Vector(int(pos[0] * globalvars.scaleFactor + globalvars.winWidth/2 - globalvars.cam[0]), int(-pos[1] * globalvars.scaleFactor + globalvars.winHeight/2 - globalvars.cam[1]))

def parami(pos):
	return Vector((pos[0] - globalvars.winWidth/2 + globalvars.cam[0]) / globalvars.scaleFactor ,- (pos[1] - globalvars.winHeight/2 + globalvars.cam[1]) / globalvars.scaleFactor)

def drawPoint(pos):
	pygame.draw.circle(win, (255,0,0) , param((pos[0],pos[1])) ,2)

def upLeft():
	return parami((0,0))
		
def downRight():
	return parami((globalvars.winWidth, globalvars.winHeight))

def closestFive(x):
	if globalvars.gridView == 0:
		print("z")
	return globalvars.gridView * round(x / globalvars.gridView)

def clamp(x, up, down):
	if x > up:
		x = up
	if x < down:
		x = down
	return x

def drawGrid():
	x = closestFive(upLeft()[0] - globalvars.gridView)
	while x < downRight()[0]:
		pygame.draw.line(win, (230,230,230), param((x,upLeft()[1])), param((x,downRight()[1])))
		x += globalvars.gridView/5
	y = closestFive(upLeft()[1] + globalvars.gridView)
	while y > downRight()[1]:
		pygame.draw.line(win, (230,230,230), param((upLeft()[0],y)), param((downRight()[0],y)))
		y -= globalvars.gridView/5
	x = closestFive(upLeft()[0])
	while x < downRight()[0]:
		pygame.draw.line(win, (180,180,180), param((x,upLeft()[1])), param((x,downRight()[1])))
		x += globalvars.gridView
	y = closestFive(upLeft()[1])
	while y > downRight()[1]:
		pygame.draw.line(win, (180,180,180), param((upLeft()[0],y)), param((downRight()[0],y)))
		y -= globalvars.gridView
	pygame.draw.line(win, (100,100,100), param((0,upLeft()[1])), param((0,downRight()[1])))
	pygame.draw.line(win, (100,100,100), param((upLeft()[0],0)), param((downRight()[0],0)))
	
	x = closestFive(upLeft()[0] + globalvars.gridView)
	y = closestFive(upLeft()[1] + globalvars.gridView)
	while x < downRight()[0]:
		text = myfont.render(str(x), True, (0, 0, 0))
		win.blit(text, param((x, clamp(0, upLeft()[1], downRight()[1]))) + Vector(2, -18))
		x += globalvars.gridView
	while y > downRight()[1]:
		text = myfont.render(str(y), True, (0, 0, 0))
		win.blit(text, param((clamp(0, downRight()[0], upLeft()[0]) , y)) + Vector(2, -18))
		y -= globalvars.gridView

def drawGraph(rStart, rStop, dx, graph, color = (100,0,0)):
	lines = []
	x = rStart
	while x < rStop:
		lines.append(param((x, graph(x))))
		x += dx
		if x >= rStop:
			lines.append(param((rStop, graph(rStop))))
	pygame.draw.lines(win, color, False, lines, 2)
	
def drawGraph2(time, values, color):
	points = []
	for i in range(len(time)):
		points.append(param((time[i], values[i])))
	pygame.draw.lines(win, color, False, points, 2)

def setWinSize(size):
	global win
	globalvars.winWidth = size[0]
	globalvars.winHeight = size[1]
	win = pygame.display.set_mode((globalvars.winWidth, globalvars.winHeight))

def setCam(pos):
	globalvars.cam = Vector(pos[0] * globalvars.scaleFactor, -pos[1] * globalvars.scaleFactor)
	
def setZoom(zoom):
	globalvars.scaleFactor = zoom
	globalvars.gridView = int((downRight()[0] - upLeft()[0])/10) + 1
	globalvars.gridView = max(5 * int(globalvars.gridView/5), 5)

################################################################################ functions

def eventHandle(events):
	for event in events:
		if event.type == pygame.QUIT:
			globalvars.run = False
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			globalvars.point = Vector(pygame.mouse.get_pos()[0] / globalvars.scaleFactor, pygame.mouse.get_pos()[1] / globalvars.scaleFactor) 
			globalvars.mousePressed = True
			globalvars.camPrev = Vector(globalvars.cam[0], globalvars.cam[1])
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
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_h:
				globalvars.cam = (0,0)
				globalvars.scaleFactor = 5

	keys = pygame.key.get_pressed()
	if keys[pygame.K_ESCAPE]:
		globalvars.run = False
		
	if globalvars.mousePressed:
		current = Vector(pygame.mouse.get_pos()[0] / globalvars.scaleFactor, pygame.mouse.get_pos()[1] / globalvars.scaleFactor)
		globalvars.cam = globalvars.camPrev + (globalvars.point - current) * globalvars.scaleFactor

################################################################################ function example

def f(x):
	return sin(x) + 5 * e**(-(x * 0.5)**2)
	return 
	if x <= 1:
		return 1
	return f(floor(x/2)) + f(ceil(x/2)) + 1

################################################################################ Main Loop

def mainLoop(step, draw, eventHandler=eventHandle):
	while globalvars.run:
		eventHandler(pygame.event.get())
		
		# step:
		step()
		
		# draw:
		win.fill((255,255,255))
		drawGrid()
		draw()
		
		pygame.display.update()
		fpsClock.tick(60)
	pygame.quit()


################################################################################ project example:
# import graph
# def step():
	# pass
# def draw():
	# drawPoint((0,14))
# mainLoop(step, draw)






