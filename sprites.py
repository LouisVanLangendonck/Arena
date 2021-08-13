import pygame
from sys import exit
from pygame.locals import *
import pygame.constants
from settings import *
from pygame.math import Vector2 as vec

class Player(pygame.sprite.Sprite):
    def __init__(self, agility, jumping_power):
        super().__init__()
        
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)

        self.agility = agility
        self.jumping_power = jumping_power

        self.frame = 0
        self.direc = 'r'
        walk_frames_unscaled = [pygame.image.load('graphics/players/Louis/walk/1.png'), pygame.image.load('graphics/players/Louis/walk/2.png'), pygame.image.load('graphics/players/Louis/walk/3.png'), pygame.image.load('graphics/players/Louis/walk/4.png'),pygame.image.load('graphics/players/Louis/walk/5.png'),pygame.image.load('graphics/players/Louis/walk/6.png'), pygame.image.load('graphics/players/Louis/walk/7.png')]
        self.walk_frames_r = [pygame.transform.scale(images, (22*4,32*4)) for images in walk_frames_unscaled]
        self.walk_frames_l = [pygame.transform.flip(images, True, False) for images in self.walk_frames_r]
        idle_frames_unscaled = [pygame.image.load('graphics/players/Louis/idle/1.png'), pygame.image.load('graphics/players/Louis/idle/2.png')]
        self.idle_frames_r = [pygame.transform.scale(images, (22*4,32*4)) for images in idle_frames_unscaled]
        self.idle_frames_l = [pygame.transform.flip(images, True, False) for images in self.idle_frames_r]
        
        self.image = self.idle_frames_r[0]
        self.rect = self.image.get_rect()

        self.size = self.image.get_size()      


    def update(self):
        #GRAVITY
        self.acc = vec(0,0.5)
        
        #MOVE LEFT AND RIGHT
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acc.x = -self.agility
        if keys[pygame.K_RIGHT]:
            self.acc.x = +self.agility
        if self.pos.x > WIDTH:
            self.pos.x = 0-self.size[0]
        if self.pos.x < 0-self.size[0]:
            self.pos.x = WIDTH

        #EQUATIONS OF MOTION
        self.acc.x += self.vel.x*FRICTION
        self.vel += self.acc
        self.pos += self.vel + 0.5*self.acc
        self.rect.bottomleft = self.pos
    


        # self.frame += 1
        # if self.vel_x == 0:
        #     if self.direc == 'r':
        #         if self.frame > ((len(self.idle_frames_r)-1) * (5*ANIMATION_VEL)):
        #             self.frame = 0
        #         self.image = self.idle_frames_r[self.frame // (5*ANIMATION_VEL)]
        #     if self.direc == 'l':
        #         if self.frame > ((len(self.idle_frames_l)-1) * ANIMATION_VEL):
        #             self.frame = 0
        #         self.image = self.idle_frames_l[self.frame // ANIMATION_VEL]  

        # if self.vel_x > 0:
        #     self.direc == 'r'
        #     if self.frame > ((len(self.walk_frames_r)-1) * ANIMATION_VEL):
        #         self.frame = 0
        #     self.image = self.walk_frames_r[self.frame // ANIMATION_VEL]
        # if self.vel_x < 0:
        #     self.direc == 'l'
        #     if self.frame > (len(self.walk_frames_l)-1) * ANIMATION_VEL:
        #         self.frame = 0
        #     self.image = self.walk_frames_l[self.frame // ANIMATION_VEL]