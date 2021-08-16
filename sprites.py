import pygame
from sys import exit
from pygame.locals import *
import pygame.constants
from settings import *
from pygame.math import Vector2 as vec
from images import *

def draw_health_bar(surf, pos, size, borderC, backC, healthC, progress):
    pygame.draw.rect(surf, backC, (*pos, *size))
    pygame.draw.rect(surf, borderC, (*pos, *size), 1)
    innerPos  = (pos[0]+1, pos[1]+1)
    innerSize = ((size[0]-2) * progress, size[1]-2)
    rect = (round(innerPos[0]), round(innerPos[1]), round(innerSize[0]), round(innerSize[1]))
    pygame.draw.rect(surf, healthC, rect)  

class Player(pygame.sprite.Sprite):
    def __init__(self, type, agility, jumping_power):
        super().__init__()
        self.health = 100
        self.agility_original = agility

        if type == 1:
            self.player_one = True
        else:
            self.player_one = False
        
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)

        self.agility = agility
        self.jumping_power = jumping_power

        self.stunned = False
        self.blocking = False
        self.in_air = False
        self.punching = False
        self.ducked = False
        self.direc = 'r'

        self.frame = 0
        self.punch_frame = 0
        self.stun_frame = 0
        
        self.image = idle_frames_r[0]
        self.rect = self.image.get_rect()
        self.size = self.image.get_size()

                

    def jump(self):
        self.vel.y = -self.jumping_power
        self.in_air = True 

    def get_hit(self):
        self.health -= 5
        
    def update(self):
        #GRAVITY
        self.acc = vec(0,0.5)
        
        #MOVE LEFT AND RIGHT
        keys = pygame.key.get_pressed()
        if self.player_one:
            if not self.stunned:
                if keys[pygame.K_LEFT]:
                    self.acc.x = -self.agility
                if keys[pygame.K_RIGHT]:
                    self.acc.x = +self.agility
            if self.pos.x > WIDTH:
                self.pos.x = 0-self.size[0]
            if self.pos.x < 0-self.size[0]:
                self.pos.x = WIDTH
        else:
            if not self.stunned:
                if keys[pygame.K_q]:
                    self.acc.x = -self.agility
                if keys[pygame.K_d]:
                    self.acc.x = +self.agility
            if self.pos.x > WIDTH:
                self.pos.x = 0-self.size[0]
            if self.pos.x < 0-self.size[0]:
                self.pos.x = WIDTH
        
        #EQUATIONS OF MOTION
        self.acc.x += self.vel.x*FRICTION
        self.vel += self.acc
        self.pos += self.vel + 0.5*self.acc
        self.rect.midbottom = self.pos

        if not self.stunned:
            if self.ducked:
                if self.vel.x > 0:
                    self.direc == 'r'
                    self.image = duck_frame_r
                    self.rect.y += 58
                    self.agility = 0.25
                    
                elif self.vel.x < 0:
                    self.direc == 'l'
                    self.image = duck_frame_l
                    self.rect.y += 58
                    self.agility = 0.25

            elif self.blocking:
                if self.vel.x > 0:
                    self.direc == 'r'
                    self.image = block_frame_r
                elif self.vel.x < 0:
                    self.direc == 'l'
                    self.image = block_frame_l    
                
            elif self.punching == True:
                punching_speed = 3
                if self.direc == 'r':
                    self.punch_frame += 1
                    if self.punch_frame == ((len(punch_frames_r)) * (ANIMATION_VEL-punching_speed)):
                            self.punching = False
                            self.punch_frame = 0
                    self.image = punch_frames_r[self.punch_frame // ((ANIMATION_VEL-punching_speed)+1)]
                    
                    
                elif self.direc == 'l':
                    self.punch_frame += 1
                    if self.punch_frame == ((len(punch_frames_l)) * (ANIMATION_VEL-punching_speed)):
                            self.punching = False
                            self.punch_frame = 0
                    self.image = punch_frames_l[self.punch_frame // ((ANIMATION_VEL-punching_speed)+1)]
            elif self.in_air:
                if self.vel.x > 0:
                    self.direc = 'r'
                    if self.direc == 'r':
                        self.image = idle_frames_r[0]
                    elif self.direc == 'l':   
                        self.image = idle_frames_l[0]
                elif self.vel.x < 0:
                    self.direc = 'l'
                    if self.direc == 'r':
                        self.image = idle_frames_r[0]
                    elif self.direc == 'l':   
                        self.image = idle_frames_l[0]
            else:
                if -1 < self.vel.x < 1:
                    self.frame = 0
                    if self.direc == 'r':
                        self.image = idle_frames_r[0]
                    elif self.direc == 'l':   
                        self.image = idle_frames_l[0]
                elif self.vel.x > 1:
                    self.direc = 'r'
                    self.frame += 1
                    if self.frame >= ((len(walk_frames_r)) * ANIMATION_VEL):
                        self.frame = 0
                    self.image = walk_frames_r[self.frame // (ANIMATION_VEL+1)]
                elif self.vel.x < -1:
                    self.direc = 'l'
                    self.frame += 1
                    if self.frame > (len(walk_frames_l)-1) * ANIMATION_VEL:
                        self.frame = 0
                    self.image = walk_frames_l[self.frame // ANIMATION_VEL]

        elif self.stunned:
            self.stun_frame += 1
            stun_time = 60
            if self.stun_frame == stun_time:
                    self.stun_frame = 0
                    self.stunned = False
            elif self.direc == 'l':
                self.image = stun_frame_l
            elif self.direc == 'r':
                self.image = stun_frame_r
            

    def draw_health(self, surf):
        if self.health >=0:
            health_rect = pygame.Rect(0, 0, self.size[0], 7)
            health_rect.center = (self.pos.x, self.pos.y - (self.size[1] + 30))
            max_health = 100
            draw_health_bar(surf, health_rect.topleft, health_rect.size, 
                (0, 0, 0), (255, 0, 0), (0, 255, 0), self.health/max_health)
        
class Platform(pygame.sprite.Sprite):
    def __init__(self,x,y,w,h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w,h))
        self.image.fill('Brown')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Spritesheet:
    def __init__(self, filename):
        self.spritesheet = pygame.image.load(filename).convert()

    def get_image(self, x, y, w, h):
        image = pygame.Surface((w, h))
        image.blit(self.sprite_sheet,(0,0), (x,y,w,h))
        return image

class Black_hole(pygame.sprite.Sprite):
    def __init__(self,type, x,y,direction):
        pygame.sprite.Sprite.__init__(self)
        self.active = True
        self.in_air = False
        if type == 1:
            self.player_one = True
        else:
            self.player_one = False
        self.player_suck = False
        self.x = x
        self.y = y
        self.direction = direction
        self.vel = 8
        self.gravity = -20
        self.image = blackhole_air_frame_r[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

        self.proj_frame = 0
        self.ground_frame = 0
            

    def update(self):
        shot_anim_speed = 5
        if self.in_air:
            self.rect.x += self.vel
            self.rect.y += self.gravity
            self.gravity += 1
            self.proj_frame += 1
            self.image = blackhole_air_frame_r[self.proj_frame // ((ANIMATION_VEL+shot_anim_speed)+1)]
            if self.proj_frame == ((len(blackhole_air_frame_r)) * (ANIMATION_VEL+shot_anim_speed)):
                    self.proj_frame = 0
        # if self.rect.topleft[0] > WIDTH:
            # self.active = False
        else:
            self.ground_frame += 1
            self.image = blackhole_ground_frame
            if self.ground_frame == FPS*3:
                self.active = False
        
    def suck(self, player):
        print(player.pos.x, player.pos.y)
        print(self.rect.x, self.rect.y)

        

        



            





# class Healthbar(pygame.sprite.Sprite):
#     def __init__(self, type):
#         super().__init__()
#         self.health = 100
#         if type == 1:
#             self.player_one = True
#         else:
#             self.player_one = False
        
#         if self.player_one:
#             pygame.draw.rect()
 


