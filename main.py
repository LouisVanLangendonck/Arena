import pygame
from sys import exit
from pygame.locals import *
import pygame.constants
from settings import *
from sprites import *
from images import *
from pygame.math import Vector2 as vec

class Game:
    def __init__(self):    
        # initialization
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption('Arena')
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        print('test')

    def new(self):
        # start new game
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.black_holes = pygame.sprite.Group()
        self.player1 = Player(1,1,20)
        self.player2 = Player(2,1,20)
        p1 = Platform(0,(HEIGHT-150), WIDTH, 200)
        p2 = Platform(100, 150, 300, 40)
        self.all_sprites.add(p1)
        self.all_sprites.add(p2)
        self.platforms.add(p1)
        self.platforms.add(p2)
        self.all_sprites.add(self.player1)
        self.all_sprites.add(self.player2)
        self.run()
        
    def run(self):
        # game loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        #game loop - update
        self.all_sprites.update()
        #Player-Platform Collision
        plat_hit0 = pygame.sprite.spritecollide(self.player1, self.platforms, False)
        plat_hit1 = pygame.sprite.spritecollide(self.player2, self.platforms, False)        
        if plat_hit0:
            self.player1.pos.y = plat_hit0[0].rect.top + 1
            self.player1.vel.y = 0
            self.player1.in_air = False
        if plat_hit1:
            self.player2.pos.y = plat_hit1[0].rect.top + 1
            self.player2.vel.y = 0
            self.player2.in_air = False
        #Player-Player collision
        if pygame.sprite.collide_rect(self.player1, self.player2):
            if self.player1.image == punch_frames_l[3] or self.player1.image == punch_frames_r[3]:
                if self.player1.pos.x > self.player2.pos.x and self.player1.direc == 'l':
                    if self.player2.blocking == True:
                        if self.player2.direc == 'r':
                            self.player1.stunned = True
                        else:
                            self.player2.get_hit()
                            if self.player2.health <= 0:
                                self.all_sprites.remove(self.player2)

                    else:
                        self.player2.get_hit()
                        if self.player2.health <= 0:
                            self.all_sprites.remove(self.player2)
                        
                elif self.player1.pos.x < self.player2.pos.x and self.player1.direc == 'r':
                    if self.player2.blocking == True:
                        if self.player2.direc == 'l':
                            self.player1.stunned = True
                        else:
                            self.player2.get_hit()
                            if self.player2.health <= 0:
                                self.all_sprites.remove(self.player2)

                    else:
                        self.player2.get_hit()
                        if self.player2.health <= 0:
                            self.all_sprites.remove(self.player2)
            
            if self.player2.image == punch_frames_l[3] or self.player2.image == punch_frames_r[3]:
                if self.player2.pos.x > self.player1.pos.x and self.player2.direc == 'l':
                    if self.player1.blocking == True:
                        if self.player1.direc == 'r':
                            self.player2.stunned = True
                        else:
                            self.player1.get_hit()
                            if self.player1.health <= 0:
                                self.all_sprites.remove(self.player1)

                    else:
                        self.player1.get_hit()
                        if self.player1.health <= 0:
                            self.all_sprites.remove(self.player1)
                        
                elif self.player2.pos.x < self.player1.pos.x and self.player2.direc == 'r':
                    if self.player1.blocking == True:
                        if self.player1.direc == 'l':
                            self.player2.stunned = True
                        else:
                            self.player1.get_hit()
                            if self.player1.health <= 0:
                                self.all_sprites.remove(self.player1)

                    else:
                        self.player1.get_hit()
                        if self.player1.health <= 0:
                            self.all_sprites.remove(self.player1)
        #Blackhole-Platform collision
        if len(self.black_holes) > 0:
            for holes in self.black_holes:
                collision = pygame.sprite.spritecollide(holes, self.platforms, False)
                if collision:
                    holes.rect.bottom = collision[0].rect.top - 80
                    holes.gravity = 0
                    holes.in_air = False
                if holes.in_air == False:
                    if holes.player_one:
                        collision2 = pygame.sprite.collide_rect(holes, self.player2)
                        if collision2:
                            self.player2.stunned = True
                            holes.suck(self.player2)
                    if not holes.player_one:
                        collision1 = pygame.sprite.collide_rect(holes, self.player1)
                        if collision1:
                            self.player1.stunned = True
                            holes.suck(self.player1)
                if not holes.active:
                    self.black_holes.remove(holes)
                    self.all_sprites.remove(holes)
                
        #Blackhole-player collision
        



    def events(self):
        #game loop - events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if self.player1.in_air:
                        pass
                    else:
                        self.player1.jump()
                if event.key == pygame.K_z:
                    if self.player2.in_air:
                        pass
                    else:
                        self.player2.jump()
                if event.key == pygame.K_KP0:
                    if not self.player1.blocking:
                        if self.player1.punching:
                            pass
                        else:
                            self.player1.punching = True
                if event.key == pygame.K_f:
                    if not self.player2.blocking:
                        if self.player2.punching:
                            pass
                        else:
                            self.player2.punching = True
                if event.key == pygame.K_KP1:
                    if not self.player1.punching:
                        self.player1.blocking = True
                if event.key == pygame.K_g:
                    if not self.player2.punching:
                        self.player2.blocking = True
                if event.key == pygame.K_h:
                    if (not self.player2.punching and not self.player2.blocking and not self.player2.stunned):
                        black_hole = Black_hole(2,self.player2.rect.center[0], self.player2.rect.center[1]-20,'r')
                        black_hole.in_air = True
                        self.black_holes.add(black_hole)
                        self.all_sprites.add(black_hole)
                if event.key == pygame.K_s:
                    self.player2.ducked = True
                if event.key == pygame.K_DOWN:
                    self.player1.ducked = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_KP1:
                    self.player1.blocking = False
                if event.key == pygame.K_g:
                    self.player2.blocking = False
                if event.key == pygame.K_s:
                    self.player2.ducked = False
                    self.player2.agility = self.player2.agility_original
                if event.key == pygame.K_DOWN:
                    self.player1.ducked = False
                    self.player1.agility = self.player1.agility_original
                
    def draw(self):
        #game loop - draw  
        self.screen.blit(background, (0,0))
        self.player1.draw_health(self.screen)
        self.player2.draw_health(self.screen)
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def show_start_screen(self):
        pass
    def show_game_over_screen(self):
        pass

g = Game()
g.show_start_screen()
while g.running:
    g.new()    