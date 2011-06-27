#!/usr/bin/env python2

import pygame, os, platform, random
from pygame.locals import *

class Wall(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x
         
class Player(pygame.sprite.Sprite):

        dir_y = 0
        length = 60

        def __init__(self, y):
                pygame.sprite.Sprite.__init__(self)
                self.image = pygame.Surface([10, self.length])
                self.image.fill((0, 255, 0))
                self.image = self.image
                self.rect = self.image.get_rect()
                self.rect.top = y
                self.rect.left = 50

        def change(self, y):
                self.dir_y += y

        def update(self):
                old_y = self.rect.top
                old_y2 = self.rect.bottom
                new_y = self.rect.centery + self.dir_y
                self.rect.centery = new_y
                if self.rect.top < 10:
                        self.rect.top = old_y
                if self.rect.bottom > (screen.get_height() - 10):
                        self.rect.bottom = old_y2

class CPU(pygame.sprite.Sprite):

        dir_y = 0

        def __init__(self, y):
                pygame.sprite.Sprite.__init__(self)
                self.image = pygame.Surface([10, 60])
                self.image.fill((255, 0, 0))
                self.rect = self.image.get_rect()
                self.rect.top = y
                self.rect.left = (screen.get_width() - 50)

        def change(self, y):
                if ball.rect.left > (screen.get_width()/2) and ball.dir_x > 0:
                        slope = float(ball.dir_y)/float(ball.dir_x)
                        intercept = ball.rect.centery - (float(slope) * float(ball.rect.centerx))
                        new_y = (float(slope) * float(self.rect.centerx)) + float(intercept)
##                        alternate method
##                        new_y = ball.rect.centery 
                        if (new_y - 25) < self.rect.centery < (new_y + 25):
                            self.dir_y = 0
                        elif self.rect.centery > (new_y + 25):
                            self.dir_y = -y
                        elif self.rect.centery < (new_y - 25):
                            self.dir_y = y
                        else:
                            self.dir_y = 0
                else:
                        self.dir_y = 0
                        
                        
        def update(self):
                old_y = self.rect.top
                old_y2 = self.rect.bottom
                new_y = self.rect.centery + self.dir_y
                self.rect.centery = new_y
                if self.rect.top < 10:
                        self.rect.top = old_y
                if self.rect.bottom > (screen.get_height() - 10):
                        self.rect.bottom = old_y2

class ball(pygame.sprite.Sprite):

        def __init__(self, x, y, (speedx, speedy)):
                self.dir_x = speedx
                self.dir_y = speedy
                pygame.sprite.Sprite.__init__(self)
                self.image = pygame.Surface([15,15])
                self.image.fill((0, 250, 0))
                self.rect = self.image.get_rect()
                self.rect.top = y
                self.rect.left = x

        def update(self, paddle, walls):
                old_x = self.rect.left
                self.rect.left += self.dir_x

                collide = pygame.sprite.spritecollide(self, paddle, False)
                if collide:
                        self.rect.left = old_x
                        self.dir_x = -self.dir_x
                        if player.dir_y or CPU.dir_y:
                                self.dir_y += player.dir_y/2
                                self.dir_y += CPU.dir_y/2
                                
                collide = pygame.sprite.spritecollide(self, walls, False)
                if collide:
                        self.rect.left = old_x
                        self.dir_x = -self.dir_x

                old_y = self.rect.top
                self.rect.top += self.dir_y

                collide = pygame.sprite.spritecollide(self, paddle, False)
                if collide:
                        self.rect.top = old_y
                        self.dir_y = -self.dir_y
                if self.dir_x > 10:
                        self.dir_x = 10
                if self.dir_y > 10:
                        self.dir_y = 10

                collide = pygame.sprite.spritecollide(self, walls, False)
                if collide:
                        self.rect.top = old_y
                        self.dir_y = -self.dir_y
                if self.dir_x > 10:
                        self.dir_x = 10
                if self.dir_y > 10:
                        self.dir_y = 10

def num():
    i = random.randrange(0, 15)
    speeds = [(5, 5), (-5, 5), (5, -5), (-5, -5), (3, 4),
              (4, 5), (-4, 3), (-2, -5), (-2, -4), (4, 1),
              (5, 2), (-4, 1), (-3, -2), (3, 5), (-3, 1)]
    return speeds[i]
    
if 'Windows' in platform.platform():
        os.environ['SDL_VIDEODRIVER'] = 'windib'
pygame.init()
pygame.display.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption('Dans PaddleBall')
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((0, 0, 0))
screen.blit(background, (0, 0))
wall_list = pygame.sprite.RenderPlain()
wall = Wall(0, 0, 10, screen.get_height())
wall_list.add(wall)
wall = Wall((screen.get_width() - 10), 0, 10, screen.get_height())
wall_list.add(wall)
wall = Wall(0, 0, screen.get_width(), 10)
wall_list.add(wall)
wall = Wall(0, (screen.get_height() - 10), screen.get_width(), 10)
wall_list.add(wall)
player = Player(100)
player2 = CPU(100)
paddles = pygame.sprite.RenderPlain(player)
paddles.add(player2)
ball = ball(screen.get_rect().centerx, screen.get_rect().centery, num())
ball2 = pygame.sprite.RenderPlain(ball)
on = True

while on:
        for event in pygame.event.get():
                if event.type == QUIT:
                        on = False
                if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                                on = False
                        if event.key == K_UP:
                                player.change(-6)
                        if event.key == K_DOWN:
                                player.change(6)
                if event.type == KEYUP:
                        if event.key == K_UP:
                                player.change(6)
                        if event.key == K_DOWN:
                                player.change(-6)
                                
        player2.change(5)
        paddles.update()
        ball.update(paddles, wall_list)
        screen.fill((0, 0, 0))
        wall_list.draw(screen)
        paddles.draw(screen)
        ball2.draw(screen)
        pygame.display.flip()
        
        if ball.rect.left > (screen.get_width() - 40):
                on = False
                print "YOU WIN!"
        if ball.rect.left < 20:
                on = False
                print "Loser."
pygame.quit()
        
