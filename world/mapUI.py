from world.sprite import *
from misc.font import *


class MapUI:
    def __init__(self, param):
        self.screen = param['screen']
        self.sprite_group = param['sprite_group']
        self.player = param['player']
        self.group_list = param['group_list']
        self.enemy_group = self.group_list['enemy_group']
        self.event_group = self.group_list['event_group']

        self.topleft = read_image('mapUI_topleft.png')

    def change_player(self, player):
        # 把左上显示基于的当前活跃角色换掉
        self.player = player

    def draw_topleft(self):
        # 左上包含信息：当前队伍中角色，活跃角色的生命值
        self.screen.blit(self.topleft, [0, 0])

        # 绘制玩家角色血条
        hp_prop = self.player.health / self.player.health_max
        pygame.draw.rect(self.screen, COLOR_HP_BG,
                         [PLAYER_HP_X, PLAYER_HP_Y, PLAYER_HP_W * hp_prop, PLAYER_HP_H])
        pygame.draw.lines(self.screen, COLOR_HP_FRAME, True,
                          [[PLAYER_HP_X, PLAYER_HP_Y], [PLAYER_HP_X, PLAYER_HP_Y + PLAYER_HP_H],
                           [PLAYER_HP_X + PLAYER_HP_W, PLAYER_HP_Y + PLAYER_HP_H],
                           [PLAYER_HP_X + PLAYER_HP_W, PLAYER_HP_Y]])
        blit_text(self.screen, f'{self.player.health}/{self.player.health_max}',
                  (PLAYER_HP_X + PLAYER_HP_W / 2, PLAYER_HP_Y), (255, 255, 255), 'middle')

    # 绘制可攻击对象血条、可交互对象提示
    def draw_enemy_health(self):
            for enemy in self.enemy_group:
                x = enemy.rect[0] + enemy.rect[2]/2 + self.sprite_group.offset[0] - 20
                y = enemy.rect[1] + self.sprite_group.offset[1] - 7
                pygame.draw.rect(self.screen, COLOR_HP_BG,
                                 [x, y, 40 * enemy.health / enemy.health_max, 5])
                pygame.draw.lines(self.screen, COLOR_HP_FRAME, True,
                                  [[x, y],
                                   [x, y + 5],
                                   [x + 40, y + 5],
                                   [x + 40, y]])

    def draw_field_command(self):
            for event in self.event_group:
                if not event.auto_trigger:
                    x = event.rect[0] + event.rect[2]/2 + self.sprite_group.offset[0] - 5
                    y = event.rect[1] + self.sprite_group.offset[1] - 12
                    pygame.draw.rect(self.screen, (0, 0, 0),
                                     [x, y, 10, 10])

    def draw(self):
        self.draw_field_command()
        self.draw_enemy_health()
        self.draw_topleft()


class Log:
    def __init__(self, param):
        self.screen = param['screen']
        
        self.bottomright = read_image('mapUI_bottomright.png')

        self.log_content = []
        self.log_frame = 0

    def log(self, texts):
        # 在右下log窗最下方添加一条文本，把历史文本往上推，推过头的文本删除掉
        if isinstance(texts, str):
            if len(self.log_content) >= 5:
                del self.log_content[0]
            self.log_content.append(texts)
        else:
            for text in texts:
                if len(self.log_content) >= 5:
                    del self.log_content[0]
                self.log_content.append(text)
        self.log_frame = 120

    def draw(self):
        # 右下包含信息：最多5行的log
        if self.log_frame > 0:
            alpha = min(10*self.log_frame, 255)
            self.bottomright.set_alpha(alpha)
            self.screen.blit(self.bottomright, [SCREENWIDTH - self.bottomright.get_width(),
                                                SCREENHEIGHT - self.bottomright.get_height()])
            # re-write blit_text adding transparency
            for i in range(len(self.log_content)):
                text_item = f_yahei_20_norm.render(self.log_content[i], True, (0,0,0), None)
                text_item.set_alpha(alpha)
                text_rect = text_item.get_rect()
                text_rect.topleft = (SCREENWIDTH - self.bottomright.get_width() + 15,
                                     SCREENHEIGHT - self.bottomright.get_height() + 15 + i * 18)
                self.screen.blit(text_item, text_rect)

            self.log_frame -= 1
