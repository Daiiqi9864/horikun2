import pygame
import sys
from misc.globals import *
from misc.events import EventHandler
from world.scene import Scene
from world.sceneMain import *


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(CAPTION)  # 标题
        icon_my = pygame.image.load('res/holy.ico')
        pygame.display.set_icon(icon_my)
        self.screen = pygame.display.set_mode([SCREENWIDTH, SCREENHEIGHT])  # 主屏幕大小
        self.clock = pygame.time.Clock()

        self.running = True
        self.gameStateManager = GameStateManager('title')   # 它的设置决定了开始游戏时所处的画面
        self.scene = Scene(self,'01', self.gameStateManager)
        self.titleScene = TitleScene(self, self.gameStateManager)
        self.endScenes = EndScenes(self, self.gameStateManager)
        self.scene_states = {'title': self.titleScene,      # 游戏中各个场景。以后如果有大世界/秘境切换，也放在这里。
                             'scene': self.scene,
                             'end': self.endScenes
                             }

    def run(self):
        while self.running:
            self.update()
            self.draw()
        self.close()

    def update(self):
        EventHandler.poll_events()
        for event in EventHandler.events:
            if event.type == pygame.QUIT:
                self.running = False

        self.scene_states[self.gameStateManager.get_state()].update()

        pygame.display.update()
        self.clock.tick(FPS)

    def draw(self):
        self.scene_states[self.gameStateManager.get_state()].draw()

    def close(self):
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()