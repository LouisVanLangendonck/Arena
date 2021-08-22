import pygame

def determineSide(rect1, rect2):
    if rect1.midtop[1] < rect2.midtop[1]:
        return 'top'
    elif rect1.midleft[0] < rect2.midleft[0]:
        return "left"
    elif rect1.midright[0] > rect2.midright[0]:
        return "right"
    else:
        return 'bottom'

def draw_bar(surf, pos, size, borderC, backC, healthC, progress):
    pygame.draw.rect(surf, backC, (*pos, *size))
    pygame.draw.rect(surf, borderC, (*pos, *size), 1)
    innerPos  = (pos[0]+1, pos[1]+1)
    innerSize = ((size[0]-2) * progress, size[1]-2)
    rect = (round(innerPos[0]), round(innerPos[1]), round(innerSize[0]), round(innerSize[1]))
    pygame.draw.rect(surf, healthC, rect)  