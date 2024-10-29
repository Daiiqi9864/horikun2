import pygame
from misc.globals import *

pygame.init()

f_yahei_50_norm = pygame.font.Font('C:/Windows/Fonts/msyhl.ttc', 50)
f_yahei_50_bold = pygame.font.Font('C:/Windows/Fonts/msyh.ttc', 50)
f_yahei_40_norm = pygame.font.Font('C:/Windows/Fonts/msyhl.ttc', 40)
f_yahei_40_bold = pygame.font.Font('C:/Windows/Fonts/msyh.ttc', 40)
f_yahei_30_norm = pygame.font.Font('C:/Windows/Fonts/msyhl.ttc', 30)
f_yahei_30_bold = pygame.font.Font('C:/Windows/Fonts/msyh.ttc', 30)
f_yahei_20_norm = pygame.font.Font('C:/Windows/Fonts/msyhl.ttc', 20)
f_yahei_20_bold = pygame.font.Font('C:/Windows/Fonts/msyh.ttc', 20)


def blit_text(screen, text=None, pos=(0,0), color=(0,0,0), mode='topleft', gap=35, font=f_yahei_20_norm):
    if isinstance(text, list):
        for i in range(len(text)):
            text_item = font.render(text[i], True, color, None)
            text_rect = text_item.get_rect()
            if mode == 'topleft':
                text_rect.topleft = (pos[0],pos[1]+i*gap)
            else:
                text_rect.midtop = (pos[0],pos[1]+i*gap)
            screen.blit(text_item, text_rect)
    else:
        text_item = font.render(text, True, color, None)
        text_rect = text_item.get_rect()
        if mode == 'topleft':
            text_rect.topleft = (pos[0], pos[1])
        else:
            text_rect.midtop = (pos[0], pos[1])
        screen.blit(text_item, text_rect)
