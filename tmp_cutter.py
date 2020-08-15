import pygame
import numpy as np
from PIL import Image
import os

NUMBER = 5

SIZE = (800,600)
CELL = (255,255,0)
MARKED = (255,0,255)

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
            counted[x,y] = True
            if (not above) and (y>0) and (mask[x,y-1]==CELL).all() and not counted[x,y-1]:
                pos_stack.append([x,y-1])
                above = True
            elif (above) and (y>0) and ((mask[x,y-1]!=CELL).any() or counted[x,y-1]):
                above = False
            if (not below) and (y<shape[1]-1) and (mask[x,y+1]==CELL).all() and not counted[x,y+1]:
                pos_stack.append([x,y+1])
                below = True
            elif (below) and (y<shape[1]-1) and ((mask[x,y+1]!=CELL).any() or counted[x,y+1]):
                below = False
            x += 1
    return x_list, y_list
    


imgdir = 'marked_data/img/' + str(NUMBER) + '.jpg'
maskdir = 'marked_data/mask/' + str(NUMBER) + '.png'
clipimg_dir = 'clipped/' + str(NUMBER) + '/img'
clipmask_dir = 'clipped/' + str(NUMBER) + '/mask'
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

clipped_masks = []
clipped_imgs = []

while mainloop:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainloop = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            rr, cc = fill_cell(mask, pygame.mouse.get_pos())
            if len(rr) > 100:
                print(len(rr))
                sm_pxarray = pygame.PixelArray(second_mask)
                for r, c in zip(rr,cc):
                    sm_pxarray[r,c] = MARKED
                print('marked')
                sm_pxarray.close()
                background.blit(second_mask, (0,0))
                screen.blit(background, (0,0))
                r0, c0 = np.min(rr), np.min(cc)
                r1, c1 = np.max(rr), np.max(cc)
                x0, y0 = max(0,r0-20), max(0,c0-20)
                x1, y1 = min(SIZE[0]-1, r1+20), min(SIZE[1]-1, c1+20)
                new_mask = np.ones_like(mask) * 255
                new_mask[rr,cc] = CELL
                clipped_imgs.append(img[x0:x1,y0:y1])
                clipped_masks.append(new_mask[x0:x1,y0:y1])
    pygame.display.flip()

for i, mk, im in zip(range(len(clipped_imgs)),clipped_masks,clipped_imgs):
    mk_save = Image.fromarray(mk.swapaxes(0,1))
    im_save = Image.fromarray(im.swapaxes(0,1))
    mk_name = str(i) + '_mask.png'
    im_name = str(i) + '.png'
    mk_filename = os.path.join(clipmask_dir, mk_name)
    im_filename = os.path.join(clipimg_dir,im_name)
    mk_save.save(mk_filename)
    im_save.save(im_filename)