"""Practicing pygames

a pretty basic brickbreaker game 

my method for placing bricks is pretty bad. 

Ill probably work on improving it at a later time
"""

import pygame, os, random, platform, math
from pygame.locals import *

class Wall(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x
        
class Brick(pygame.sprite.Sprite):
	
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((60, 30))
		self.image.fill((160, 0, 0))
		self.rect = self.image.get_rect()
		self.rect.centerx = x
		self.rect.centery = y
		
class Player(pygame.sprite.Sprite):
	
	dir_x = 0
	length = 90
	lives = 3
	
	def __init__(self, x):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((self.length, 5))
		self.image.fill((202, 202, 202))
		self.rect = self.image.get_rect()
		self.rect.centerx = x
		self.rect.top = (screen.get_height() - 50)
		
	def move(self, x):
		self.dir_x += x
		
	def update(self, walls):
		old_x = self.rect.left
		self.rect.left += self.dir_x
		collide = pygame.sprite.spritecollide(self, walls, False)
		if collide:
			self.rect.left = old_x
			
class Ball(pygame.sprite.Sprite):
	
	def __init__(self, x, y, speedx, speedy):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((15, 15))
		self.image.fill((0, 0, 255))
		self.rect = self.image.get_rect()
		self.rect.centerx = x
		self.rect.centery = y
		self.dir_x = speedx
		self.dir_y = speedy
		self.collide = False
		self.collide2 = False
		
	def update(self, walls, paddle, bricks):
		old_y = self.rect.top
		self.rect.top += self.dir_y
		
		collide = pygame.sprite.spritecollide(self, bricks, True)
		if collide:
			self.rect.top = old_y
			self.dir_y = -self.dir_y 
			
		collide = pygame.sprite.spritecollide(self, paddle, False)
		if collide:
			self.rect.top = old_y
			self.dir_y = -self.dir_y
			if player.dir_x:
				self.dir_x += player.dir_x/2
				
		collide = pygame.sprite.spritecollide(self, walls, False)
		if collide:
			self.rect.top = old_y
			self.dir_y = -self.dir_y 
				
		old_x = self.rect.left
		self.rect.left += self.dir_x
		
		collide = pygame.sprite.spritecollide(self, bricks, True)
		if collide:
			self.rect.left = old_x
			self.dir_x = -self.dir_x
			
		collide = pygame.sprite.spritecollide(self, paddle, False)
		if collide:
			self.rect.left = old_x
			self.dir_x = -self.dir_x
			if player.dir_x:
				self.dir_x += player.dir_x/2
				
		collide = pygame.sprite.spritecollide(self, walls, False)
		if collide:
			self.rect.left = old_x
			self.dir_x = -self.dir_x
			
		if self.dir_x > 10:
			self.dir_x = 10
		if self.dir_y > 10:
			self.dir_y = 10
			
def BrickGen(number):
	bricklist = []
	for i in range(1, (number + 1)):
		x = 140 + (70 * i)
		y = screen.get_height()/4
		while x > (screen.get_width() - 160):
			x -= screen.get_width()/1.2
			y += 40
		brick = Brick(x, y)
		bricklist.append(brick)
	return bricklist
			
	
if 'Windows' in platform.platform():
	os.environ['SDL_VIDEODRIVER'] = 'windib'
pygame.init()
pygame.display.init()
pygame.font.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((0, 0, 0))
screen.blit(background, (0, 0))
player = Player((screen.get_width()/2))
wall = Wall(0, 0, screen.get_width(), 10)
walls = pygame.sprite.RenderPlain(wall)
wall = Wall(0, 0, 10, screen.get_height())
walls.add(wall)
wall = Wall((screen.get_width() - 10), 0, 10, screen.get_height())
walls.add(wall)
wall = Wall(0, (screen.get_height() - 10), screen.get_width(), 10)
walls.add(wall)
bricks = pygame.sprite.RenderPlain()
bricks.add(BrickGen(80))
paddle = pygame.sprite.RenderPlain(player)
ball = Ball((screen.get_width()/2), (screen.get_height()/2), 0 ,5)
ball2 = pygame.sprite.RenderPlain(ball)
allsprites = pygame.sprite.Group(walls, bricks, paddle, ball2)
on = True
playing = True
while on:
	while playing:
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					on = False
					playing = False
				if event.key == K_LEFT:
					player.move(-6)
				if event.key == K_RIGHT:
					player.move(6)
			if event.type == KEYUP:
				if event.key == K_LEFT:
					player.move(6)
				if event.key == K_RIGHT:
					player.move(-6)
		bricks.update()
		ball2.update(walls, paddle, bricks)
		paddle.update(walls)
		screen.fill((0, 0, 0))
		allsprites.draw(screen)
		pygame.display.flip()
		if not len(bricks.sprites()):
			playing = False
			
	text = pygame.font.Font(None, 80)
	text = text.render('You WIN!!!!', True, (255, 255, 255))
	textpos = text.get_rect(centerx=background.get_width()/2, centery=background.get_height()/2)
	screen.blit(text, textpos)
	pygame.display.flip()
	for event in pygame.event.get():
		if event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				on = False

pygame.quit()
			
