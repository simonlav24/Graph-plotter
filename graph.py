from math import fabs, sqrt, cos, sin, pi, floor, ceil, e
from random import uniform, randint, choice
import pygame
pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Arial', 16)

fpsClock = pygame.time.Clock()

winWidth = 800
winHeight = 500
win = pygame.display.set_mode((winWidth,winHeight))
pygame.display.set_caption('Simon\'s graph')

scaleFactor = 5
gridView = 20
################################################################################ transformations

cam = (0,0)

def vecAdd(v1, v2):
	return (v1[0] + v2[0], v1[1] + v2[1])
def vecSub(v1, v2):
	return (v1[0] - v2[0], v1[1] - v2[1])
def vecMult(v, s):
	return (v[0] * s, v[1] * s)

def param(pos):
	return (int(pos[0] * scaleFactor + winWidth/2 - cam[0]), int(-pos[1] * scaleFactor + winHeight/2 - cam[1]))

def parami(pos):
	return ((pos[0] - winWidth/2 + cam[0]) / scaleFactor ,- (pos[1] - winHeight/2 + cam[1]) / scaleFactor)

def drawPoint(pos):
	pygame.draw.circle(win, (255,0,0) , param((pos[0],pos[1])) ,2)

def upLeft():
	return parami((0,0))
		
def downRight():
	return parami((winWidth,winHeight))

def closestFive(x):
	if gridView == 0:
		print("z")
	return gridView * round(x / gridView)

def clamp(x, up, down):
	if x > up:
		x = up
	if x < down:
		x = down
	return x

def drawGrid():
	x = closestFive(upLeft()[0])
	while x < downRight()[0]:
		pygame.draw.line(win, (230,230,230), param((x,upLeft()[1])), param((x,downRight()[1])))
		x += gridView/5
	y = closestFive(upLeft()[1])
	while y > downRight()[1]:
		pygame.draw.line(win, (230,230,230), param((upLeft()[0],y)), param((downRight()[0],y)))
		y -= gridView/5

	x = closestFive(upLeft()[0])
	while x < downRight()[0]:
		pygame.draw.line(win, (180,180,180), param((x,upLeft()[1])), param((x,downRight()[1])))
		x += gridView
	y = closestFive(upLeft()[1])
	while y > downRight()[1]:
		pygame.draw.line(win, (180,180,180), param((upLeft()[0],y)), param((downRight()[0],y)))
		y -= gridView
	pygame.draw.line(win, (100,100,100), param((0,upLeft()[1])), param((0,downRight()[1])))
	pygame.draw.line(win, (100,100,100), param((upLeft()[0],0)), param((downRight()[0],0)))
	
	x = closestFive(upLeft()[0] + gridView)
	y = closestFive(upLeft()[1] + gridView)
	while x < downRight()[0]:
		text = myfont.render(str(x), True, (0, 0, 0))
		win.blit(text, vecAdd(param((x, clamp(0, upLeft()[1], downRight()[1]))), (2, -18)))
		x += gridView
	while y > downRight()[1]:
		text = myfont.render(str(y), True, (0, 0, 0))
		win.blit(text, vecAdd(param((clamp(0, downRight()[0], upLeft()[0]) , y)), (2, -18)))
		y -= gridView

def drawGraph(rStart, rStop, dx, graph, color = (100,0,0)):
	lines = []
	x = rStart
	while x < rStop:
		lines.append(param((x, graph(x))))
		x += dx
	pygame.draw.lines(win, color, False, lines, 2)
	
def drawGraph2(time, values, color):
	points = []
	for i in range(len(time)):
		points.append(param((time[i], values[i])))
	pygame.draw.lines(win, color, False, points, 2)

def setCam(pos):
	global cam
	cam = (pos[0] * scaleFactor, -pos[1] * scaleFactor)
	
def setZoom(zoom):
	global scaleFactor, gridView
	scaleFactor = zoom
	gridView = int((downRight()[0] - upLeft()[0])/10) + 1
	gridView = max(5 * int(gridView/5), 5)

################################################################################ function example

def f(x):
	return sin(x) + 5 * e**(-(x * 0.5)**2)
	return 
	if x <= 1:
		return 1
	return f(floor(x/2)) + f(ceil(x/2)) + 1

################################################################################ Main Loop
def mainLoop(step, draw):
	global scaleFactor, cam, gridView
	mousePressed = False
	run = True
	while run:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				point = (pygame.mouse.get_pos()[0] / scaleFactor, pygame.mouse.get_pos()[1] / scaleFactor) 
				mousePressed = True
				camPrev = (cam[0], cam[1])
			# mouse control
			if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
				mousePressed = False
			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
				origin = param((0,0))
				mouse = pygame.mouse.get_pos()
				adjust = (mouse[0] - origin[0], mouse[1] - origin[1])
				cam = vecAdd(cam, vecMult(adjust, 0.2))
				scaleFactor += 0.2 * scaleFactor
				
				gridView = int((downRight()[0] - upLeft()[0])/10) + 1
				gridView = max(5 * int(gridView/5), 5)
			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
				origin = param((0,0))
				mouse = pygame.mouse.get_pos()
				adjust = (mouse[0] - origin[0], mouse[1] - origin[1])
				cam = vecSub(cam, vecMult(adjust, 0.2))
				scaleFactor -= 0.2 * scaleFactor
				
				gridView = int((downRight()[0] - upLeft()[0])/10) + 1
				gridView = max(5 * int(gridView/5), 5)
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_h:
					cam = (0,0)
					scaleFactor = 5

		keys = pygame.key.get_pressed()
		if keys[pygame.K_ESCAPE]:
			run = False
		
		if mousePressed:
			current = (pygame.mouse.get_pos()[0] / scaleFactor, pygame.mouse.get_pos()[1] / scaleFactor)
			cam = vecAdd(camPrev, vecMult(vecSub(point, current), scaleFactor))
		
		
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
	# graph.drawPoint((0,14))
# graph.mainLoop(step, draw)






