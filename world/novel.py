import pygame

from invent.item import *
from world.noveldata import *
from world.mapUI import *
from misc.events import EventHandler


class Novel:
    def __init__(self, param):
        self.screen = param['screen']
        self.player = param['player']
        self.mapUI = param['mapUI']
        self.log = param['log']
        self.group_list = param['group_list']

        self.save_manager = param['save_manager']   # 从当前缓存的存档中读取一些数据
        self.global_variables = self.save_manager.global_variables
        self.items = self.save_manager.items
        self.player_state = self.save_manager.player_state

        self.enemy_group = self.group_list['enemy_group']
        self.event_group = self.group_list['event_group']
        self.event_content = []
        self.now_content = {}
        self.now_index = 0
        self.max_index = 0

        # 在执行move操作时的特定参数
        self.target_cha = None
        self.target_pos = None
        self.frame_move = pygame.Vector2(0, 0)
        self.frame_count = 0

        # 与显示相关的参数
        self.curr_dialog = ''
        self.curr_stand = [None, None]
        self.curr_name = [None, None]
        self.curr_select_index = []  # 目前展示出的每个选项会跳跃到的paragraph序号
        self.curr_select_text = []
        self.sel_item = 0
        self.sel_item_max = 0
        self.trigger = True  # should update contents on this frame. avoid duplicate scanning.

        # 显示内容
        self.img_dialog = read_image('novel_dialog.png')
        self.img_name = read_image('novel_name.png')
        self.img_select_active = read_image('novel_select_active.png')
        self.img_select_passive = read_image('novel_select_passive.png')

    def set_script(self, name):
        # 这里获取的 name 是npc的名字
        for event in self.event_group:
            if event.name == name:
                self.event_content = novel_data[event.event_name]
                self.now_index = 0
                self.max_index = len(self.event_content)
                return
        print('寻找事件内容失败')

    def update(self):
        # 帧事件
        if self.now_index >= self.max_index:
            # list out of range
            return True
        else:
            self.now_content = self.event_content[self.now_index]
        if 'paragraph_start' in self.now_content:
            temp_condition = False
            if 'condition' in self.now_content and self.now_content['condition'] != 0:  # 需要条件才能开启这段
                # 处理开启段所需条件
                # 统计条件数
                if 'and' in self.now_content and self.now_content['and']:
                    condition_num = 0
                    for index in range(self.now_index, self.max_index):
                        condition_num += 1
                        self.now_content = self.event_content[index]
                        if not self.now_content['and']:
                            break
                else:
                    condition_num = 1
                # 对所有条件进行判断
                for i in range(condition_num):
                    self.now_content = self.event_content[self.now_index]

                    if self.now_content['condition'] == 'item':
                        if self.now_content['direction'] == 'equal':
                            temp_condition &= self.items[self.now_content['id']] == self.now_content['quantity']
                        elif self.now_content['direction'] == 'not_equal':
                            temp_condition &= self.items[self.now_content['id']] != self.now_content['quantity']
                        elif self.now_content['direction'] == 'less':
                            temp_condition &= self.items[self.now_content['id']] < self.now_content['quantity']
                        else:
                            temp_condition &= self.items[self.now_content['id']] >= self.now_content['quantity']
                    elif self.now_content['condition'] == 'variable':
                        if self.now_content['condition'] == 'item':
                            if self.now_content['direction'] == 'equal':
                                temp_condition &= self.global_variables[self.now_content['name']] == self.now_content[
                                    'value']
                            elif self.now_content['direction'] == 'not_equal':
                                temp_condition &= self.global_variables[self.now_content['name']] != self.now_content[
                                    'value']
                            elif self.now_content['direction'] == 'less':
                                temp_condition &= self.global_variables[self.now_content['name']] < self.now_content['value']
                            else:
                                temp_condition &= self.global_variables[self.now_content['name']] >= self.now_content[
                                    'value']
                    elif self.now_content['condition'] == 'player':
                        if self.now_content['direction'] == 'equal':
                            temp_condition &= self.player.name == self.now_content['name']
                        elif self.now_content['direction'] == 'not_equal':
                            temp_condition &= self.player.name != self.now_content['name']
                    elif self.now_content['condition'] == 'health':
                        if self.now_content['direction'] == 'more':
                            temp_condition &= self.player.health == self.now_content['quantity']
                        elif self.now_content['direction'] == 'less':
                            temp_condition &= self.player.health != self.now_content['quantity']
                    elif self.now_content['condition'] == 'select':
                        temp_condition = False  # 如果这个paragraph是专为某个选项准备的结果，那么不能自然进入
            else:
                temp_condition = True

            if temp_condition:
                # 满足自然进入该段的条件，则进入该段，下一帧开始执行内容
                self.now_index += 1
            else:
                # 无法进入该段，则跳到该段的end条目，下一帧处理end
                next_index = self.now_index
                for index in range(self.now_index, self.max_index):
                    if 'paragraph_end' in self.event_content[index]:
                        break
                    next_index += 1
                self.now_index = next_index
        elif 'paragraph_end' in self.now_content:
            if self.now_index == self.max_index:
                # 执行到了最后一条，清除当前缓存事件内容，回到游戏中
                self.event_content = []
                self.now_content = {}
                self.now_index = 0
                self.max_index = 0
                return True  # 表示novel的部分结束，可以回到游戏
            else:
                self.now_index += 1
        elif self.now_content['type'] == 'talk':
            if self.trigger:
                self.trigger = False
                self.curr_dialog = self.now_content['content']
                if 'stand' in self.now_content:
                    if 'stand_pos' in self.now_content and self.now_content['stand_pos'] == 'left':
                        self.curr_stand[0] = read_image(self.now_content['stand'])
                    else:
                        self.curr_stand[1] = read_image(self.now_content['stand'])
                if 'name' in self.now_content:
                    if 'name_pos' in self.now_content and self.now_content['name_pos'] == 'left':
                        self.curr_name[0] = self.now_content['name']
                    else:
                        self.curr_name[1] = self.now_content['name']
            elif EventHandler.keydown(pygame.K_SPACE) or EventHandler.keydown(pygame.K_RETURN):
                self.now_index += 1
                self.trigger = True
                self.curr_dialog = ''
                self.curr_stand = [None, None]
                self.curr_name = [None, None]
        elif self.now_content['type'] == 'item':
            temp_quantity = self.items[self.now_content['id']].quantity + self.now_content['quantity']
            if self.now_content['quantity'] >= 0:
                if temp_quantity <= 99:
                    self.items[self.now_content['id']].quantity = temp_quantity
                else:
                    self.items[self.now_content['id']].quantity = 0
                self.log.log(f"得到 {self.items[self.now_content['id']].name} × {self.now_content['quantity']}")
            else:
                if 0 <= temp_quantity:
                    self.items[self.now_content['id']].quantity = temp_quantity
                else:
                    self.items[self.now_content['id']].quantity = 0
                self.log.log(f"失去 {self.now_content['name']} × {-self.now_content['quantity']}")
            self.now_index += 1
        elif self.now_content['type'] == 'variable':
            if 'quantity' in self.now_content:
                self.global_variables[self.now_content['name']] += self.now_content['quantity']
            elif 'value' in self.now_content:
                self.global_variables[self.now_content['name']] = self.now_content['value']
            else:
                # 若不对变量做任何操作，则默认为读取并显示变量
                self.log.log(str(self.global_variables[self.now_content['name']]))
            self.now_index += 1
        elif self.now_content['type'] == 'log':
            self.log.log(self.now_content['content'])
            self.now_index += 1
        elif self.now_content['type'] == 'move':
            if self.target_cha is None:
                if self.now_content['group'] == 'enemy_group':
                    for enemy in self.enemy_group:
                        if enemy.name == self.now_content['name']:
                            self.target_cha = enemy
                            break
                elif self.now_content['group'] == 'event_group':
                    for event in self.event_group:
                        if event.name == self.now_content['name']:
                            self.target_cha = event
                            break
                else:
                    # 若不规定来源组，默认是让玩家角色平移
                    self.target_cha = self.player

                self.frame_count = self.now_content['frame']

                if 'pos' in self.now_content:
                    self.frame_move[0] = (self.now_content['pos'][0] - self.target_cha.rect[0]) / self.frame_count
                    self.frame_move[1] = (self.now_content['pos'][1] - self.target_cha.rect[1]) / self.frame_count
                elif 'dir' in self.now_content:
                    if 'speed' in self.now_content:
                        temp_speed = self.now_content['speed']
                    else:
                        temp_speed = self.target_cha.speed_walk
                    if self.now_content['dir'] == 'L':
                        self.frame_move[0] = -temp_speed
                        self.frame_move[1] = 0
                    elif self.now_content['dir'] == 'R':
                        self.frame_move[0] = temp_speed
                        self.frame_move[1] = 0
                    elif self.now_content['dir'] == 'U':
                        self.frame_move[0] = 0
                        self.frame_move[1] = -temp_speed
                    else:
                        self.frame_move[0] = 0
                        self.frame_move[1] = temp_speed
                else:
                    self.frame_move[0] = self.frame_move[1] = 0
            elif self.frame_count > 0:
                self.target_cha.rect[0] += self.frame_move[0]
                self.target_cha.rect[1] += self.frame_move[1]
                self.frame_count -= 1
            else:
                self.target_cha = None
                self.target_pos = None
                self.now_index += 1
        elif self.now_content['type'] == 'active':
            if self.now_content['group'] == 'enemy_group':
                for enemy in self.enemy_group:
                    if enemy.name == self.now_content['name']:
                        self.target_cha = enemy
                        break
            elif self.now_content['group'] == 'event_group':
                for event in self.event_group:
                    if event.name == self.now_content['name']:
                        self.target_cha = event
                        break

            if self.target_cha:
                if self.now_content['dir'] == 'on':
                    self.target_cha.active = True
                elif self.now_content['dir'] == 'off':
                    self.target_cha.active = False
                else:
                    self.target_cha.active = not self.target_cha.active

            self.target_cha = None
            self.now_index += 1
        elif self.now_content['type'] == 'select':
            if self.trigger:
                self.trigger = False
                self.curr_select_index = []
                self.curr_select_text = []
                for key in self.now_content['selects']:
                    self.curr_select_index.append(key)
                    self.curr_select_text.append(self.now_content['selects'][key])
                self.sel_item_max = len(self.curr_select_index)
                self.sel_item = 0
            elif EventHandler.keydown(pygame.K_w) or EventHandler.keydown(pygame.K_a):
                if self.sel_item <= 0:
                    self.sel_item = self.sel_item_max - 1
                else:
                    self.sel_item -= 1
            elif EventHandler.keydown(pygame.K_s) or EventHandler.keydown(pygame.K_d):
                self.sel_item += 1
                if self.sel_item >= self.sel_item_max:
                    self.sel_item = 0
            elif EventHandler.keydown(pygame.K_SPACE) or EventHandler.keydown(pygame.K_RETURN):
                key = self.curr_select_index[self.sel_item]

                target_index = 0
                for i in range(self.max_index):
                    if 'paragraph_start' in self.event_content[i] and \
                            'condition' in self.event_content[i] and \
                            self.event_content[i]['condition'] == 'select' and \
                            self.event_content[i]['value'] == key:
                        target_index = i
                        break

                self.curr_select_index = []
                self.curr_select_text = []
                self.now_index = target_index + 1  # jump to the second line of corresponding paragraph
                self.sel_item_max = 0
                self.trigger = True

        return False  # 表示novel还没结束，需要继续卡在这里

    def draw(self):
        if self.curr_stand[0]:
            # left stand
            image = self.curr_stand[0]
            rect = image.get_rect()
            self.screen.blit(image, (100 - rect[2] / 2, SCREENHEIGHT - rect[3]))
        if self.curr_stand[1]:
            # right stand
            image = self.curr_stand[1]
            rect = image.get_rect()
            self.screen.blit(image, (540 - rect[2] / 2, SCREENHEIGHT - rect[3]))
        if self.curr_name[0]:
            # left name
            image = self.img_dialog
            rect = image.get_rect()
            self.screen.blit(image, (200 - rect[2] / 2, 300 - rect[3]))
            blit_text(self.screen, self.curr_name[0], (200, 300))
        if self.curr_name[1]:
            # right name
            image = self.img_dialog
            rect = image.get_rect()
            self.screen.blit(image, (440 - rect[2] / 2, 300 - rect[3]))
            blit_text(self.screen, self.curr_name[1], (440, 300))
        if self.curr_dialog:
            # in dialog
            self.screen.blit(self.img_dialog, (0, 340))
            blit_text(self.screen, self.curr_dialog, (40, 360))

        if self.sel_item_max:
            for i in range(self.sel_item_max):
                rect = self.img_select_active.get_rect()
                if i == self.sel_item:
                    self.screen.blit(self.img_select_active, ((SCREENWIDTH-rect[2])/2, 50 + i * 100))
                else:
                    self.screen.blit(self.img_select_passive, ((SCREENWIDTH-rect[2])/2, 50 + i * 100))
                blit_text(self.screen, self.curr_select_text[i], (SCREENWIDTH/2, 60 + i * 100), mode='middle')
