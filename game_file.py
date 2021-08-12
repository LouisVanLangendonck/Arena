import pygame
from sys import exit
from pygame.locals import *
import pygame.constants

pygame.init()

screen = pygame.display.set_mode((1440,900))
pygame.display.set_caption('Arena')
clock = pygame.time.Clock()

FRICTION = -0.1

background = pygame.image.load('graphics/backgrounds/basic.png').convert_alpha()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        idle_unscaled = [pygame.image.load('graphics/players/Louis/idle/1.png'), pygame.image.load('graphics/players/Louis/idle/2.png')]
        self.images = [pygame.transform.scale(images, (22*4,32*4)) for images in idle_unscaled]
        self.image = self.images[0]
        self.rect = self.image.get_rect(midbottom = (200, 600)) 
        self.vel_x = 0
        self.vel_y = 0

        self.direction = 'R'
        walk_frames_R_unscaled = [pygame.image.load('graphics/players/Louis/walk/1.png')]
        self.walk_frames_R = [pygame.transform.scale(images, (22*4,32*4)) for images in walk_frames_R_unscaled]


player1 = pygame.sprite.GroupSingle()
player1.add(Player())

screen.blit(background, (0,0))
    
    



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    player1.draw(screen)

    pygame.display.update()
    clock.tick(60)
    