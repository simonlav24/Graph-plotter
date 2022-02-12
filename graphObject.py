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
# pygame.init()
pygame.font.init()


############################################################################### transformations
	
class Graph:
	def __init__(self, pos, size, font, aafont=True):
		self.pos = vectorCopy(pos)
		self.size = vectorCopy(size)
		self.scaleFactor = 5
		self.gridView = 20
		self.cam = Vector()
		self.surf = pygame.Surface((self.size[0], self.size[1]))
		self.surf.fill((255,255,255))

		self.font = font
		self.aafont = aafont

		self.point = None
		self.mousePressed = False
	def step(self, mousePosition=None):
		if self.mousePressed:
			mousePos = tup2vec(pygame.mouse.get_pos()) - Vector(self.pos[0], self.pos[1])
			if mousePosition:
				mousePos = mousePosition
			current = Vector(mousePos[0] / self.scaleFactor, mousePos[1] / self.scaleFactor)
			self.cam = self.camPrev + (self.point - current) * self.scaleFactor
	def draw(self):
		self.surf.fill((255,255,255))
		self.drawGrid()
	def drawGraph2(self, time, values, color):
		points = []
		for i in range(len(time)):
			points.append(self.param((time[i], values[i])))
		pygame.draw.lines(self.surf, color, False, points, 2)
	def param(self, pos):
		return Vector(int(pos[0] * self.scaleFactor + self.size[0]/2 - self.cam[0]), int(-pos[1] * self.scaleFactor + self.size[1]/2 - self.cam[1]))
	def parami(self, pos):
		return Vector((pos[0] - self.size[0]/2 + self.cam[0]) / self.scaleFactor ,- (pos[1] - self.size[1]/2 + self.cam[1]) / self.scaleFactor)
	def upLeft(self):
		return self.parami((0,0))
	def downRight(self):
		return self.parami((self.size[0], self.size[1]))
	def handleGraphEvent(self, event, mousePosition=None):
		mousePos = pygame.mouse.get_pos()
		if mousePosition:
			mousePos = mousePosition
		if not (mousePos[0] > self.pos[0] and mousePos[0] < self.pos[0] + self.size[0] and mousePos[1] > self.pos[1] and mousePos[1] < self.pos[1] + self.size[1]):
			return
		mousePos = tup2vec(mousePos) - Vector(self.pos[0], self.pos[1])
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			# if mouse is in the graph rectangle
				self.point = Vector(mousePos[0] / self.scaleFactor, mousePos[1] / self.scaleFactor) 
				self.mousePressed = True
				self.camPrev = Vector(self.cam[0], self.cam[1])
		# mouse control
		if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
			self.mousePressed = False
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
			origin = self.param((0,0))
			mouse = mousePos
			adjust = Vector(mouse[0] - origin[0], mouse[1] - origin[1])
			self.cam = self.cam + adjust * 0.2
			self.scaleFactor += 0.2 * self.scaleFactor

			self.gridView = int((self.downRight()[0] - self.upLeft()[0])/10) + 1
			self.gridView = max(5 * int(self.gridView/5), 5)
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
			origin = self.param((0,0))
			mouse = mousePos
			adjust = Vector(mouse[0] - origin[0], mouse[1] - origin[1])
			self.cam = self.cam - adjust * 0.2
			self.scaleFactor -= 0.2 * self.scaleFactor

			self.gridView = int((self.downRight()[0] - self.upLeft()[0])/10) + 1
			self.gridView = max(5 * int(self.gridView/5), 5)
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_h:
				self.cam = (0,0)
				self.scaleFactor = 5
	def drawGrid(self):
		x = self.closestFive(self.upLeft()[0] - self.gridView)
		while x < self.downRight()[0]:
			pygame.draw.line(self.surf, (230,230,230), self.param((x,self.upLeft()[1])), self.param((x,self.downRight()[1])))
			x += self.gridView/5
		y = self.closestFive(self.upLeft()[1] + self.gridView)
		while y > self.downRight()[1]:
			pygame.draw.line(self.surf, (230,230,230), self.param((self.upLeft()[0],y)), self.param((self.downRight()[0],y)))
			y -= self.gridView/5
		x = self.closestFive(self.upLeft()[0])
		while x < self.downRight()[0]:
			pygame.draw.line(self.surf, (180,180,180), self.param((x,self.upLeft()[1])), self.param((x,self.downRight()[1])))
			x += self.gridView
		y = self.closestFive(self.upLeft()[1])
		while y > self.downRight()[1]:
			pygame.draw.line(self.surf, (180,180,180), self.param((self.upLeft()[0],y)), self.param((self.downRight()[0],y)))
			y -= self.gridView
		pygame.draw.line(self.surf, (100,100,100), self.param((0,self.upLeft()[1])), self.param((0,self.downRight()[1])))
		pygame.draw.line(self.surf, (100,100,100), self.param((self.upLeft()[0],0)), self.param((self.downRight()[0],0)))
		
		x = self.closestFive(self.upLeft()[0])
		y = self.closestFive(self.upLeft()[1])
		# draw grid numbers
		while x < self.downRight()[0]:
			text = self.font.render(str(x), self.aafont, (0, 0, 0))
			self.surf.blit(text, self.param((x, clamp(0, self.upLeft()[1] - 4, self.downRight()[1]))) + Vector(2, -18))
			x += self.gridView
		while y > self.downRight()[1]:
			text = self.font.render(str(y), self.aafont, (0, 0, 0))
			self.surf.blit(text, self.param((clamp(0, self.downRight()[0] - 4, self.upLeft()[0]) , y)) + Vector(2, -18))
			y -= self.gridView
	def closestFive(self, x):
		if self.gridView == 0:
			print("z")
		return self.gridView * round(x / self.gridView)
	def blitToScreen(self, screen):
		screen.blit(self.surf, self.pos)

def clamp(x, up, down):
	if x > up:
		x = up
	if x < down:
		x = down
	return x

if __name__ == "__main__":
	pygame.init()
	screen = pygame.display.set_mode((800, 600))

	graph = Graph(Vector(100,100), Vector(400,300), pygame.font.Font("pixelFont.ttf", 12))

	run = True
	while run:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			graph.handleGraphEvent(event)
		
		if pygame.key.get_pressed()[pygame.K_ESCAPE]:
			run = False

		graph.step()
		graph.draw()

		screen.fill((255,255,255))
		graph.blitToScreen(screen)
		pygame.display.flip()

