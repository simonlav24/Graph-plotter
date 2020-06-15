from math import fabs, sqrt, cos, sin, pi, floor, ceil, e
from random import uniform, randint, choice
import pygame
from vector import *
#from pygame import gfxdraw
pygame.init()
fpsClock = pygame.time.Clock()
#pygame.font.init()
#myfont = pygame.font.SysFont('Arial', 12)

winWidth = 800
winHeight = 500
win = pygame.display.set_mode((winWidth,winHeight))
pygame.display.set_caption('Simon\'s desmos')

scaleFactor = 5
################################################################################ transformations

cam = Vector(0,0)

def param(pos):
	return (int(pos[0] * scaleFactor + winWidth/2 - cam[0]), int(-pos[1] * scaleFactor + winHeight/2 - cam[1]))

def parami(pos):
	return ((pos[0] - winWidth/2 + cam[0]) / scaleFactor ,- (pos[1] - winHeight/2 + cam[1]) / scaleFactor)

def drawPoint(pos):
	pygame.draw.circle(win, (255,0,0) , param((pos[0],pos[1])) ,2)

grid_amount = 50
def drawGrid():
	for x in range(-grid_amount,grid_amount,5):
		if x == 0:
			continue
		pygame.draw.line(win, (200,200,200), param((x,grid_amount)), param((x,-grid_amount)))
	for y in range(-grid_amount,grid_amount,5):
		if y == 0:
			continue
		pygame.draw.line(win, (200,200,200), param((grid_amount,y)), param((-grid_amount,y)))
	pygame.draw.line(win, (100,100,100), param((0,grid_amount)), param((0,-grid_amount)))
	pygame.draw.line(win, (100,100,100), param((grid_amount,0)), param((-grid_amount,0)))

def drawGraph(rStart, rStop, dx, graph, color = (100,0,0)):
	lines = []
	x = rStart
	while x < rStop:
		lines.append(param((x, graph(x))))
		x += dx
	pygame.draw.lines(win, color, False, lines, 2)

################################################################################ Classes

def f(x):
	return sin(x) + 5 * e**(-(x * 0.5)**2)
	return 
	if x <= 1:
		return 1
	return f(floor(x/2)) + f(ceil(x/2)) + 1

################################################################################ Setup



################################################################################ Main Loop
mousePressed = False
run = True
while run:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			point = Vector(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) / scaleFactor
			mousePressed = True
			camPrev = vectorCopy(cam)
		# mouse control
		if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
			mousePressed = False
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
			origin = param((0,0))
			mouse = pygame.mouse.get_pos()
			adjust = Vector(mouse[0] - origin[0], mouse[1] - origin[1])
			cam += adjust * 0.2
			scaleFactor += 0.2 * scaleFactor
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
			origin = param((0,0))
			mouse = pygame.mouse.get_pos()
			adjust = Vector(mouse[0] - origin[0], mouse[1] - origin[1])
			cam -= adjust * 0.2
			scaleFactor -= 0.2 * scaleFactor
		# keys pressed once
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_h:
				cam *= 0
	keys = pygame.key.get_pressed()
	if keys[pygame.K_ESCAPE]:
		run = False
	
	if mousePressed:
		current = Vector(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) / scaleFactor
		cam = camPrev + (point - current) * scaleFactor
	
	# draw:
	win.fill((255,255,255))
	drawGrid()
	
	drawGraph(-20,20,0.1,f)
	
	pygame.display.update()
	fpsClock.tick(120)
pygame.quit()














