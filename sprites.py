import pygame
from sys import exit
from pygame.locals import *
import pygame.constants
from settings import *
import random as rd
from pygame.math import Vector2 as vec
from images import *
from helper_functions import *
from music import *

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
        self.bh_poss = True
        self.direc = 'r'

        self.frame = 0
        self.punch_frame = 0
        self.stun_frame = 0
        self.jump_count = 0
        self.bh_regen_count = 0
        self.regen_time = FPS*10
        
        self.image = idle_frames_r[0]
        self.rect = self.image.get_rect()
        self.size = self.image.get_size()

        self.platform_list = pygame.sprite.Group()     

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

        #REGENERATION OF BLACK HOLE
        if not self.bh_poss:
            self.bh_regen_count += 1
            if self.bh_regen_count == self.regen_time:
                self.bh_poss = True
                self.bh_regen_count = 0


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
                    self.agility = 0.25
                elif self.vel.x < 0:
                    self.direc == 'l'
                    self.image = block_frame_l  
                    self.agility = 0.25  
                
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
            draw_bar(surf, health_rect.topleft, health_rect.size, 
                (0, 0, 0), (255, 0, 0), (0, 255, 0), self.health/max_health)
    
    def draw_bh_powerup(self, surf):
        if self.bh_poss:
            bh_rect = pygame.Rect(0, 0, 200, 30)
            if self.player_one:
                bh_rect.topleft = (30, 30)
            else:
                bh_rect.topright = (WIDTH-30, 30)
            draw_bar(surf, bh_rect.topleft, bh_rect.size, 
                (0, 0, 0), (0, 0, 0), (131, 29, 163), 1)
        else:
            bh_rect = pygame.Rect(0, 0, 200, 30)
            if self.player_one:
                bh_rect.topleft = (30, 30)
            else:
                bh_rect.topright = (WIDTH-30, 30)
            draw_bar(surf, bh_rect.topleft, bh_rect.size, 
               (0, 0, 0), (0, 0, 0), (131, 29, 163), self.bh_regen_count/self.regen_time)

class Platform(pygame.sprite.Sprite):
    def __init__(self,x,y,w,h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w,h))
        self.image.fill('White')
        #self.image = pygame.transform.scale(platform_test, (w,h))
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
        self.x = x
        self.y = y
        self.direction = direction
        self.vel = 8
        self.gravity = -20
        self.image = blackhole_air_frame_r[0] 
        self.rect = self.image.get_rect()
        self.rect.midbottom = (self.x,self.y)
        self.living_time = FPS*3

        self.proj_frame = 0
        self.ground_frame = 0
        self.spin_frame = 0

    def update(self):
        if self.x > WIDTH:
            self.x = 0
        elif self.x < 0:
            self.x = WIDTH
        self.rect.midbottom = (self.x,self.y)
        shot_anim_speed = 4
        if self.in_air:
            if self.direction == 'r':
                self.x += self.vel
            else:
                self.x -= self.vel
            self.y += self.gravity
            self.gravity += 1
            self.proj_frame += 1
            self.image = blackhole_air_frame_r[self.proj_frame // ((ANIMATION_VEL+shot_anim_speed)+1)]
            if self.proj_frame == ((len(blackhole_air_frame_r)) * (ANIMATION_VEL+shot_anim_speed)):
                    self.proj_frame = 0
        # if self.rect.topleft[0] > WIDTH:
            # self.active = False
        else:
            spinning_speed = 5
            self.spin_frame += 1
            self.ground_frame += 1
            self.image = blackhole_ground_frame[self.spin_frame // ((spinning_speed)+1)]
            if self.spin_frame == ((len(blackhole_ground_frame)) * (spinning_speed)):
                    self.spin_frame = 0
            self.rect = self.image.get_rect()
            self.rect.midbottom = (self.x,self.y)
            if self.ground_frame == self.living_time:
                self.active = False
        
    def suck(self, target):
        target.acc = vec(0,0)
        target.vel.y = 0
        x_diff = target.pos.x - self.x
        if x_diff > 0:
            target.pos.x -= (x_diff/(self.living_time/2))
        else:
            target.pos.x -= (x_diff/(self.living_time/2))
        target.vel.y = 0

class Non_interacting_item(pygame.sprite.Sprite):
    def __init__(self,x,y,vel,image):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.vel = vel
        self.image = image
        self.rect = image.get_rect()
        self.rect.topright = (self.x, self.y)        

    def update(self):
        self.x += self.vel
        self.rect.topright = (self.x, self.y)

class Sun(Non_interacting_item):
    def __init__(self,vel,image):
        self.x = 0
        self.y = 30
        super().__init__(self.x,self.y,vel,image)

    def update(self):
        self.x += self.vel
        self.rect.topright = (self.x, self.y)
        if self.rect.left > WIDTH:
            self.x = 0
            

class Cloud(Non_interacting_item):
    def __init__(self, x):
        self.vel = rd.random()
        self.seed = rd.randint(0,len(clouds)-1)
        self.y = rd.randint(-50, 350)
        self.image = clouds[self.seed]
        super().__init__(x,self.y,self.vel, self.image)

    def update(self):
        self.x += self.vel
        self.rect.topright = (self.x, self.y)
        if self.rect.left > WIDTH:
            self.vel = rd.random()
            self.seed = rd.randint(0,len(clouds)-1)
            self.image = clouds[self.seed]
            self.x = 0
            self.y = rd.randint(-50, 350)




 


