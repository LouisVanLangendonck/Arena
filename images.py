import pygame
#from sprites import Spritesheet
from settings import *

pygame.init()
pygame.display.set_mode((WIDTH,HEIGHT))

#my_spritesheet = Spritesheet('graphics/spritesheet_test.png')


walk_frames_r = [pygame.image.load('graphics/players/louis/walk/walk01.png').convert_alpha(), pygame.image.load('graphics/players/louis/walk/walk02.png').convert_alpha(), pygame.image.load('graphics/players/louis/walk/walk03.png').convert_alpha(), pygame.image.load('graphics/players/louis/walk/walk04.png').convert_alpha(), pygame.image.load('graphics/players/louis/walk/walk05.png').convert_alpha(), pygame.image.load('graphics/players/louis/walk/walk06.png').convert_alpha(), pygame.image.load('graphics/players/louis/walk/walk07.png').convert_alpha(), pygame.image.load('graphics/players/louis/walk/walk08.png').convert_alpha(), pygame.image.load('graphics/players/louis/walk/walk09.png').convert_alpha(), pygame.image.load('graphics/players/louis/walk/walk10.png').convert_alpha()]
walk_frames_l = [pygame.transform.flip(images, True, False) for images in walk_frames_r]

idle_frames_r = [pygame.image.load('graphics/players/Rokus/demo.png')]
#idle_frames_r = [pygame.image.load('graphics/players/Louis/idle/idle01.png')]
idle_frames_l = [pygame.transform.flip(images, True, False) for images in idle_frames_r]

punch_frames_r = [pygame.image.load('graphics/players/louis/punch/punch01.png').convert_alpha(), pygame.image.load('graphics/players/louis/punch/punch02.png').convert_alpha(), pygame.image.load('graphics/players/louis/punch/punch03.png').convert_alpha(), pygame.image.load('graphics/players/louis/punch/punch04.png').convert_alpha(), pygame.image.load('graphics/players/louis/punch/punch05.png').convert_alpha(), pygame.image.load('graphics/players/louis/punch/punch06.png').convert_alpha(), pygame.image.load('graphics/players/louis/punch/punch07.png').convert_alpha()]
punch_frames_l = [pygame.transform.flip(images, True, False) for images in punch_frames_r]

block_frame_r = pygame.image.load('graphics/players/louis/block.png').convert_alpha()
block_frame_l = pygame.transform.flip(block_frame_r, True, False)

blackhole_air_frame_r = [pygame.image.load('graphics/players/louis/black_hole/bhproj01.png').convert_alpha(), pygame.image.load('graphics/players/louis/black_hole/bhproj02.png').convert_alpha(), pygame.image.load('graphics/players/louis/black_hole/bhproj03.png').convert_alpha(), pygame.image.load('graphics/players/louis/black_hole/bhproj04.png').convert_alpha()]
blackhole_air_frame_l = [pygame.transform.flip(images, True, False) for images in blackhole_air_frame_r]
blackhole_ground_frame = [pygame.image.load('graphics/players/louis/black_hole/bh01.png').convert_alpha(), pygame.image.load('graphics/players/louis/black_hole/bh02.png').convert_alpha(), pygame.image.load('graphics/players/louis/black_hole/bh03.png').convert_alpha(), pygame.image.load('graphics/players/louis/black_hole/bh04.png').convert_alpha()]

stun_frame_r = pygame.image.load('graphics/players/louis/stunned.png').convert_alpha()
stun_frame_l = pygame.transform.flip(stun_frame_r, True, False)

duck_frame_r = pygame.image.load('graphics/players/louis/duck.png').convert_alpha()
duck_frame_l = pygame.transform.flip(duck_frame_r, True, False)

platform_test = pygame.image.load('graphics/platform/test.png').convert_alpha()

sun = pygame.image.load('graphics/backgrounds/NII/sun.png').convert_alpha()

clouds = [pygame.image.load('graphics/backgrounds/NII/cloud1.png').convert_alpha(),
    pygame.image.load('graphics/backgrounds/NII/cloud2.png').convert_alpha(),
    pygame.image.load('graphics/backgrounds/NII/cloud3.png').convert_alpha(),
    pygame.image.load('graphics/backgrounds/NII/cloud4.png').convert_alpha(),
    pygame.image.load('graphics/backgrounds/NII/cloud5.png').convert_alpha(),
    pygame.image.load('graphics/backgrounds/NII/cloud6.png').convert_alpha(),
    pygame.image.load('graphics/backgrounds/NII/cloud7.png').convert_alpha(),
    pygame.image.load('graphics/backgrounds/NII/cloud8.png').convert_alpha(),
    pygame.image.load('graphics/backgrounds/NII/cloud9.png').convert_alpha(),
    pygame.image.load('graphics/backgrounds/NII/cloud10.png').convert_alpha(),
    pygame.image.load('graphics/backgrounds/NII/cloud11.png').convert_alpha(),
    pygame.image.load('graphics/backgrounds/NII/cloud12.png').convert_alpha(),
    pygame.image.load('graphics/backgrounds/NII/cloud13.png').convert_alpha(),
    pygame.image.load('graphics/backgrounds/NII/cloud14.png').convert_alpha(),
    pygame.image.load('graphics/backgrounds/NII/cloud15.png').convert_alpha(),
    pygame.image.load('graphics/backgrounds/NII/cloud16.png').convert_alpha(),
    pygame.image.load('graphics/backgrounds/NII/cloud17.png').convert_alpha()]

background = pygame.image.load('graphics/backgrounds/saint_cath_dag.png').convert_alpha()
