import pygame
import numpy as np
from PIL import Image
import os

NUMBER = 0

SIZE = (1200,900)
CELL = (255,255,0)
COUNT = ()

def fill_cell(mask, pos):
    pos_stack = [pos]
    x_list = []
    y_list = []
    shape = mask.shape
    counted = np.zeros(shape[:2])
    while len(pos_stack) > 0:
        x, y = pos_stack.pop()
        while (mask[x,y] == CELL).all() and x>=0:
            x -= 1
        x += 1
        above, below = False, False
        while x < shape[0] and (mask[x,y]==CELL).all() and not counted[x,y]:
            x_list.append(x)
            y_list.append(y)
            if (not above) and (y>0) and (mask[x,y-1]==CELL).all() and not counted[x,y]:
                pos_stack.append([x,y-1])
                above = True
            elif (above) and (y>0) and (mask[x,y-1]!=CELL).any():
                above = False
            elif (not below) and (y<shape[1]-1) and (mask[x,y+1]==CELL).all():
                pos_stack.append([x,y+1])
                below = True
            elif (below) and (y<shape[1]-1) and (mask[x,y+1]!=CELL).any():
                below = False
            x += 1
    return x_list, y_list
    


imgdir = 'marked_data/img/' + str(NUMBER) + '.jpg'
maskdir = 'marked_data/mask/' + str(NUMBER) + '.png'
clipimg_dir = 'clipped/' + str(NUMBER) + '/img'
clipmask_dir = 'clipped' + str(NUMBER) + '/mask'
os.makedirs(clipimg_dir, exist_ok=True)
os.makedirs(clipmask_dir,exist_ok=True)

img = Image.open(imgdir).resize(SIZE)
mask = Image.open(maskdir).resize(SIZE)

img = np.asarray(img).swapaxes(0,1)
mask = np.asarray(mask).swapaxes(0,1)

mainloop = True
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(SIZE)
background = pygame.Surface(SIZE)
second_mask = pygame.Surface(SIZE)
second_mask.set_colorkey((0,0,0))
pygame.surfarray.blit_array(background, mask)
background.blit(second_mask, (0,0))
screen.blit(background,(0,0))
while mainloop:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainloop = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print(len(fill_cell(mask, pygame.mouse.get_pos())[0]))
    pygame.display.flip()