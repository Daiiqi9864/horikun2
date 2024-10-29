import pygame

from misc.globals import *
from misc.events import *
from misc.font import *
from misc.keys import *

class TitleScene:
    def __init__(self, app, gameStateManager):
        self.app = app
        self.gameStateManager = gameStateManager    # 加入这条，在这个画面内就可以主动更改state key存储器的内容了。
        self.window_stat = 'in_title_main'
        self.select_item = 1
        self.SELECT_ITEM_MAX = 4
        self.text_list = ['开始新游戏', '读档继续', '附加内容', '退出游戏']

    def update(self):
        # 帧更新
        if EventHandler.keydown(pygame.K_ESCAPE):
            self.select_item = 3
        elif EventHandler.keydown(pygame.K_a) or EventHandler.keydown(pygame.K_w):
            self.select_item -= 1
            self.select_item %= self.SELECT_ITEM_MAX
        elif EventHandler.keydown(pygame.K_d) or EventHandler.keydown(pygame.K_s):
            self.select_item += 1
            self.select_item %= self.SELECT_ITEM_MAX
        elif EventHandler.keydown(pygame.K_RETURN):
            if self.select_item == 0:
                self.gameStateManager.set_state('scene')
            elif self.select_item == 1:
                self.gameStateManager.set_state('scene')
            elif self.select_item == 2:
                pass
            elif self.select_item == 3:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    def draw(self):
        self.app.screen.fill('gray23')
        blit_text(self.app.screen, "游戏标题", (SCREENWIDTH/2, 80), COLORS['title'], mode='midtop')
        for i in range (0,self.SELECT_ITEM_MAX):
            if i == self.select_item:
                blit_text(self.app.screen, self.text_list[i], (SCREENWIDTH/2, 250+50*i), COLORS['title_highlight'],mode='midtop')
            else:
                blit_text(self.app.screen, self.text_list[i], (SCREENWIDTH/2, 250+50*i), COLORS['title_normal'], mode='midtop')


class EndScenes:
    # 标题画面在这里只会有1个，end画面总会有很多个。
    def __init__(self, app, gameStateManager):
        self.gameStateManager = gameStateManager
        self.select_item = 0
        self.SELECT_ITEM_MAX = 2
        self.text_list = ['回到标题画面', '退出游戏']

    def update(self):
        # 帧更新
        if EventHandler.keydown(pygame.K_a) or EventHandler.keydown(pygame.K_w):
            self.select_item -= 1
            self.select_item %= self.SELECT_ITEM_MAX
        elif EventHandler.keydown(pygame.K_d) or EventHandler.keydown(pygame.K_s):
            self.select_item += 1
            self.select_item %= self.SELECT_ITEM_MAX
        elif EventHandler.keydown(pygame.K_RETURN):
            if self.select_item == 0:
                self.gameStateManager.set_state('title')
            elif self.select_item == 1:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    def draw(self):
        pass


class GameStateManager:
    # 它用于存储{标题画面,end画面,地图A画面,地图B画面,...}state dict中，当前所在的key。
    def __init__(self, currentState):
        self.currentState = currentState

    def get_state(self):
        return self.currentState

    def set_state(self, state=str):
        self.currentState = state
