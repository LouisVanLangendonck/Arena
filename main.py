import pygame
from sys import exit
from pygame.locals import *
import pygame.constants
from settings import *
from sprites import *
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
        self.player1 = pygame.sprite.GroupSingle()
        self.player = Player(1,0.5)
        self.player1.add(self.player)
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
        self.player1.update()
        pygame.display.update()
        
    def events(self):
        #game loop - events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
                
    def draw(self):
        #game loop - draw  
        self.background = pygame.image.load('graphics/backgrounds/basic.png').convert_alpha()
        self.screen.blit(self.background, (0,0))
        self.player1.draw(self.screen)

    def show_start_screen(self):
        pass
    def show_game_over_screen(self):
        pass

g = Game()
g.show_start_screen()
while g.running:
    g.new()    