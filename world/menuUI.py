from world.sprite import *
from misc.events import EventHandler
from misc.font import *
from invent.item import *
from invent.saveload import *


class MenuUI:
    def __init__(self, param):
        self.screen = param['screen']
        self.player = param['player']
        self.item_texture = param['item_texture']
        self.log = param['log']

        self.save_manager = param['save_manager']   # 从当前缓存的存档中读取一些数据
        self.global_variables = self.save_manager.global_variables
        self.items = self.save_manager.items
        self.player_state = self.save_manager.player_state

        self.zero_template = read_image('menuUI_0_template.png')
        self.zero_button_active = read_image('menuUI_0_button_active.png')
        self.zero_button_passive = read_image('menuUI_0_button_passive.png')
        self.A_template_active = read_image('menuUI_A_template_active.png')
        self.A_template_passive = read_image('menuUI_A_template_passive.png')
        self.B_button_active = read_image('menuUI_B_button_active.png')
        self.B_button_passive = read_image('menuUI_B_button_passive.png')
        self.C_template_active = read_image('menuUI_C_template_active.png')
        self.C_template_passive = read_image('menuUI_C_template_passive.png')

        self.layer_active = 0
        self.item_active = [0, 0, 0]  # 用来显示
        self.text_list_0 = ['状态', '背包', '队伍', '系统']
        self.text_list_B = ['使用道具', '材料收集', '重要物品']
        self.text_list_C = ['选择调换位置的角色', '选择将角色替换至的位置']
        self.text_list_D = ['存档', '读档', '设置', '退出']
        self.item_max = 4
        self.menu_stat = 'menu_template'  # 用来区分

        self.itemAll_list = [[],[],[]]  # 这里的item不表示项，表示物品栏内容。
        self.item_window_len = 0
        self.item_window_bias = 0

    def esc(self):
        # 当esc从scene管理器传到这里
        if self.layer_active > 0:
            self.layer_active -= 1
            if '0_' in self.menu_stat:
                self.menu_stat = 'menu_template'
                self.item_max = 4
            elif 'B_' in self.menu_stat:
                self.menu_stat = 'B0_'
                self.item_max = 3
            elif 'C_' in self.menu_stat:
                self.menu_stat = 'C0_'
                self.item_max = 4
            return False
        else:
            self.menu_stat = 'menu_template'
            return True

    def update(self):
        if_UI_close = False
        # respond to key action, only in menu
        if EventHandler.keydown(pygame.K_RETURN):
            if self.layer_active == 0:
                # self.menu_stat == 'menu_template'
                temp_list = ['A0_', 'B0_', 'C0_', 'D0_']
                temp_max = [4, 3, 4, 4]
                self.menu_stat = temp_list[self.item_active[0]]
                self.item_max = temp_max[self.item_active[0]]

                self.layer_active += 1
                self.item_active[self.layer_active] = 0
            elif self.layer_active == 1:
                if self.menu_stat == 'A0_':
                    self.item_max = 1
                    self.log.log("你现在查询了某个角色的个人信息")
                elif self.menu_stat == 'B0_':

                    # 进入具体物品菜单的时候更新该类菜单包含的物品列表
                    self.itemAll_list[self.item_active[1]].clear()
                    self.item_window_bias = 0
                    for key in self.items:
                        if_key = (self.item_active[1] == 0 and isinstance(self.items[key], ItemUse)) or \
                                 (self.item_active[1] == 1 and isinstance(self.items[key], ItemMat)) or \
                                 (self.item_active[1] == 2 and isinstance(self.items[key], ItemKey))
                        if if_key and self.items[key].quantity >= 1:
                            self.itemAll_list[self.item_active[1]].append(key)
                    self.item_window_len = min(6, len(self.itemAll_list[self.item_active[1]]))

                    if self.item_window_len > 0:    # 仅当有道具的时候能进入具体道具栏
                        temp_list = ['B_1', 'B_2', 'B_3']
                        self.menu_stat = temp_list[self.item_active[1]]

                        self.layer_active += 1
                        self.item_active[self.layer_active] = 0

                        self.item_max = self.item_window_len

                elif self.menu_stat == 'C0_':
                    temp_list = ['C_1', 'C_2', 'C_3', 'C_4']
                    self.menu_stat = temp_list[self.item_active[1]]
                    self.item_max = 4

                    self.layer_active += 1
                    self.item_active[self.layer_active] = 0
                elif self.menu_stat == 'D0_':
                    if self.item_active[1] == 0:
                        self.log.log("你执行了存档")
                        self.save_manager.save()
                        self.layer_active = 0
                        self.menu_stat = 'menu_template'
                        if_UI_close = True
                    elif self.item_active[1] == 1:
                        self.log.log("你执行了读档")
                        self.save_manager.load()
                        self.layer_active = 0
                        self.menu_stat = 'menu_template'
                        if_UI_close = True
                    elif self.item_active[1] == 2:
                        self.log.log("你试图唤出设置画面")
                    else:
                        self.log.log("拜拜")
                        exit()
            elif self.layer_active == 2:
                if self.menu_stat == 'B_1':
                    self.log.log(f'你试图使用第{self.item_active[2] + self.item_window_bias + 1}项可消耗品')
                elif self.menu_stat == 'B_2':
                    self.log.log(f'你试图调查第{self.item_active[2] + self.item_window_bias + 1}项合成材料')
                elif self.menu_stat == 'B_3':
                    self.log.log(f'你试图使用第{self.item_active[2] + self.item_window_bias + 1}项关键道具')
                elif self.menu_stat in ['C_1', 'C_2', 'C_3', 'C_4']:
                    self.log.log(f'你试图将{self.item_active[1]+1}号角色替换到{self.item_active[2]+1}号位上')

        elif EventHandler.keydown(pygame.K_a) or EventHandler.keydown(pygame.K_w):
            if 'B_' in self.menu_stat:
                # 物品栏需要能滚动
                if self.item_active[self.layer_active] > 0:
                    self.item_active[self.layer_active] -= 1
                elif self.item_window_bias > 0:
                    self.item_window_bias -= 1
                else:
                    self.item_window_bias = max(0, len(self.itemAll_list[self.item_active[1]]) - 6)
                    self.item_active[self.layer_active] = self.item_window_len - 1
            else:
                if self.item_active[self.layer_active] > 0:
                    self.item_active[self.layer_active] -= 1
                else:
                    self.item_active[self.layer_active] = self.item_max - 1

        elif EventHandler.keydown(pygame.K_d) or EventHandler.keydown(pygame.K_s):
            if 'B_' in self.menu_stat:
                # 物品栏需要能滚动
                if self.item_active[self.layer_active] < self.item_max - 1:
                    self.item_active[self.layer_active] += 1
                elif self.item_window_bias < max(0, len(self.itemAll_list[self.item_active[1]]) - 6):
                    self.item_window_bias += 1
                else:
                    self.item_window_bias = 0
                    self.item_active[self.layer_active] = 0
            else:
                if self.item_active[self.layer_active] < self.item_max - 1:
                    self.item_active[self.layer_active] += 1
                else:
                    self.item_active[self.layer_active] = 0
        return if_UI_close

    def draw(self):
        # 具体画哪个菜单，触发哪个绘图事件，在这里面管理

        # 画最底层的面板和面板上的几个按钮
        self.screen.blit(self.zero_template, [35, 30])
        for i in range(4):
            if i == self.item_active[0]:
                self.screen.blit(self.zero_button_active, [90 + i * 105, 77])
                blit_text(self.screen, self.text_list_0[i], [120 + i * 105, 85], COLORS['menu_highlight'])
            else:
                self.screen.blit(self.zero_button_passive, [100 + i * 105, 80])
                blit_text(self.screen, self.text_list_0[i], [120 + i * 105, 85], COLORS['menu_normal'])
        # 二级菜单界面
        if self.layer_active >= 1:
            if 'A' in self.menu_stat:
                for i in range(4):
                    if i == self.item_active[1]:
                        self.screen.blit(self.A_template_active, [100 + i * 105, 140])
                    else:
                        self.screen.blit(self.A_template_passive, [100 + i * 105, 140])
            elif 'B' in self.menu_stat:
                for i in range(3):
                    if i == self.item_active[1]:
                        self.screen.blit(self.B_button_active, [105 + i * 80, 140])
                        blit_text(self.screen, self.text_list_B[i], [105 + i * 80, 140], COLORS['menu_highlight'])
                    else:
                        self.screen.blit(self.B_button_passive, [105 + i * 80, 140])
                        blit_text(self.screen, self.text_list_B[i], [105 + i * 80, 140], COLORS['menu_normal'])
            elif 'C' in self.menu_stat:
                blit_text(self.screen, self.text_list_C[0], (0, 0), COLORS['menu_normal'])
                for i in range(4):
                    if i == self.item_active[1]:
                        self.screen.blit(self.C_template_active, [170, 140 + i * 60])
                    else:
                        self.screen.blit(self.C_template_passive, [170, 140 + i * 60])
            elif 'D' in self.menu_stat:
                for i in range(4):
                    if i == self.item_active[1]:
                        self.screen.blit(self.B_button_active, [160, 160 + i * 50])
                        blit_text(self.screen, self.text_list_D[i], [160, 160 + i * 50], COLORS['menu_highlight'])
                    else:
                        self.screen.blit(self.B_button_passive, [160, 160 + i * 50])
                        blit_text(self.screen, self.text_list_D[i], [160, 160 + i * 50], COLORS['menu_normal'])

        # 三级菜单界面
        if self.layer_active == 2:
            if 'B_' in self.menu_stat:

                x, y, w, h = 355, 145, 150, 240
                pygame.draw.rect(self.screen, [222, 200, 142], [x, y, w, h])
                pygame.draw.lines(self.screen, [0, 0, 0], True,
                                  [[x, y], [x, y + h],
                                   [x + w, y + h], [x + w, y]])

                key = self.itemAll_list[self.item_active[1]][self.item_active[2] + self.item_window_bias]
                self.screen.blit(self.item_texture[key], (x+50, y+50))
                blit_text(self.screen, self.items[key].introduce, (60, 400), COLORS['menu_item'])

                for i in range(self.item_window_len):
                    x, y, w, h = 105, 180 + i * 35, 230, 30
                    if i == self.item_active[2]:
                        pygame.draw.rect(self.screen, [249, 248, 232], [x, y, w, h])
                    else:
                        pygame.draw.rect(self.screen, [222, 200, 142], [x, y, w, h])
                    pygame.draw.lines(self.screen, [0, 0, 0], True,
                                      [[x, y], [x, y + h],
                                       [x + w, y + h], [x + w, y]])

                    key = self.itemAll_list[self.item_active[1]][i + self.item_window_bias]
                    self.screen.blit(self.item_texture[key], (x+10, y+5))
                    blit_text(self.screen, self.items[key].name, (x+50, y+5), COLORS['menu_item'])

            elif 'C_' in self.menu_stat:
                blit_text(self.screen, self.text_list_C[1], (0, 0), COLORS['menu_normal'])
                for i in range(4):
                    if i == self.item_active[2]:
                        self.screen.blit(self.C_template_active, [190, 160 + i * 60])
                    else:
                        self.screen.blit(self.C_template_passive, [190, 160 + i * 60])


class HomeUI:
    # 在篝火的特别菜单。
    def __init__(self, param):
        self.screen = param['screen']
        self.player = param['player']

    def draw(self):
        pass