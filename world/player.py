import pygame

from misc.events import EventHandler
from world.bullet import *
import math


class Player(pygame.sprite.Sprite):
    def __init__(self, groups, pos: pygame.math.Vector2, param: dict) -> None:
        super().__init__(*groups)

        # parameters
        self.name = param['name']
        self.group_list = param['group_list']
        self.block_group = self.group_list['block_group']
        self.enemy_group = self.group_list['enemy_group']
        self.bullet_group = self.group_list['bullet_group']
        self.event_group = self.group_list['event_group']
        self.key_manager = param['key_manager']

        self.animator = param['animator']
        self.image = self.animator.image(run=False)
        self.rect = self.image.get_rect(topleft=pos)

        self.data_sheet = param['information']

        # health parameters
        self.health_max = self.data_sheet['health']
        self.health = self.data_sheet['health']
        self.v_attack = 10
        self.v_defence = 12
        self.tough = self.v_defence  # 韧性值，上限与防御相等

        # movement
        self.velocity = pygame.math.Vector2()
        self.speed = self.data_sheet['speed']
        self.speed_walk = self.speed['speed_walk']
        self.speed_run = self.speed['speed_run']
        self.speed_dash = self.speed['speed_dash']
        self.speed_jump = self.speed['speed_jump']

        # status
        self.status = 'idle'
        self.direction = 'R'
        self.speed_x = 0
        self.attack_sequence = self.data_sheet['attack_sequence']

        # self.animator.frame_index = 0  # 当前正在播放的关键帧序号
        # self.animator.frame_count = 0  # 当前正在播放的帧序号
        self.action_count = 0  # 当前一次性动作播放的帧序号。尽量不用它，可以的话把它删掉。
        self.if_ground = False  # 是否在着地
        self.if_crouch = False  # 是否在下蹲
        self.if_dash = False  # 是否在冲刺
        self.if_attack = False  # 是否在攻击
        self.if_wind = False  # 是否在风场中
        self.crouch_counter = 0  # 蹲下的程度，用来做站-蹲之间的过渡，最大15
        self.CROUCH_COUNTER_MAX = 15
        self.stage_attack = 0  # 当前攻击段数
        self.stage_jump = 0  # 当前跳跃段数
        self.STAGE_JUMP_MAX = 114                                                               # 测试用，一般为2
        self.stage_dash = 0  # 当前冲刺段数
        self.pre_attack = False  # 是否有保存的攻击输入
        self.pre_attack_hard = 0  # 有保存的重击输入的帧数
        self.PRE_ATTACK_HARD_MAX = 20
        self.if_controllable = True  # 是否可通过判断状态或输入按键更改状态，包括可取消后摇的情况。与硬直倒地一定矛盾。
        self.iv_frames = 0  # 当前还剩的无敌帧数

    def input(self, event_name):
        # 只要player角色存在，每帧都先进行这个判定。在这个判定之后，主程序选择进入事件、背包，或正常更新动作。
        if not event_name:
            # interact
            for event in self.event_group:
                if event.active and event.rect.colliderect(self.animator.rect(self.rect)):
                    if EventHandler.keydown(self.key_manager.key_interact) or event.auto_trigger:
                        return event.name

        return None

    def move(self):
        # 不在强制事件中时，角色的活动。
        keys_press = pygame.key.get_pressed()
        if_decided = False  # 本帧动作已最终决定，后续判定都不采用

        # 0. y方向自然加速
        self.velocity.y += GRAVITY
        # terminal velocity check
        if self.velocity.y > SPD_LIM:
            self.velocity.y = SPD_LIM
        # velocity(float) need to be added as int on rect, for rect collision(mainly on grounding check per frame).
        fact_velocity = pygame.Vector2(0, math.ceil(self.velocity.y))

        # 1.暂存攻击与重击
        if self.if_controllable or self.if_attack:
            if EventHandler.keydown(self.key_manager.key_attack):
                self.pre_attack = True
            elif keys_press[self.key_manager.key_attack]:
                self.pre_attack_hard = min(self.pre_attack_hard + 1, self.PRE_ATTACK_HARD_MAX)
            else:
                self.pre_attack_hard = max(self.pre_attack_hard - 1, 0)

        # 2.受击相关
        temp_bullet = None
        temp_bullet_list = []
        if not self.iv_frames:
            for bullet in self.bullet_group:
                if bullet.active and bullet.to_player and bullet.rect.colliderect(self.animator.rect(self.rect)):
                    temp_bullet_list.append(bullet)
                    if not temp_bullet or bullet.damage > temp_bullet.damage:
                        temp_bullet = bullet
        if temp_bullet:
            if_decided = True
            # 受伤计算
            pass
            if temp_bullet.tough > 0:
                # 击退计算
                pass
                # 削韧硬直
                if self.if_ground:
                    self.tough -= temp_bullet.tough
                    if self.tough <= 0:
                        self.tough = 0
                        self.status = 'faint'
                        self.iv_frames = 4  # 获得无敌时间
                    else:
                        if self.if_crouch:
                            self.status = 'freeze_down'
                        else:
                            self.status = 'freeze_normal'
                        self.iv_frames = 4  # 获得无敌时间
                else:
                    self.status = 'down'
                    self.iv_frames = 4  # 获得无敌时间
                # 由于陷入硬直，所有动作被打断
                self.if_dash = False
                self.if_attack = False
                self.stage_attack = 0
                self.stage_jump = 0
                self.pre_attack = False
                self.pre_attack_hard = 0
                self.if_controllable = False
            for index in range(len(temp_bullet_list)-1,0,-1):
                temp_bullet_list[index].on_collide()
        elif self.if_controllable:
            # 3.键位操作进入攻击、跳跃、冲刺 +互动
            if self.pre_attack:

                temp_switch = False   # 触发了战斗动作

                if (not self.if_ground) and (self.stage_attack <= 2) and keys_press[self.key_manager.key_down]:
                    self.status = 'attack_drop'
                    temp_switch = True
                elif self.stage_attack == 0:
                    if not self.if_ground:
                        self.status = 'attack_air_1'
                        temp_switch = True
                    elif self.if_crouch:
                        self.status = 'attack_crouch_1'
                        temp_switch = True
                    elif keys_press[self.key_manager.key_up]:
                        self.status = 'attack_up_1'
                        temp_switch = True
                    elif keys_press[self.key_manager.key_down]:
                        self.status = 'attack_down_1'
                        temp_switch = True
                    else:
                        self.status = 'attack_front_1'
                        temp_switch = True
                elif self.stage_attack == 1:
                    if not self.if_ground:
                        self.status = 'attack_air_2'
                        temp_switch = True
                    elif self.if_crouch:
                        self.status = 'attack_crouch_2'
                        temp_switch = True
                    elif keys_press[self.key_manager.key_up]:
                        self.status = 'attack_up_2'
                        temp_switch = True
                    elif keys_press[self.key_manager.key_down]:
                        self.status = 'attack_down_2'
                        temp_switch = True
                    else:
                        self.status = 'attack_front_2'
                        temp_switch = True
                elif self.stage_attack == 2:
                    if not self.if_ground:
                        self.status = 'attack_air_3'
                        temp_switch = True
                    elif keys_press[self.key_manager.key_up]:
                        self.status = 'attack_up_3'
                        temp_switch = True
                    elif keys_press[self.key_manager.key_down]:
                        self.status = 'attack_down_3'
                        temp_switch = True
                    else:
                        self.status = 'attack_front_3'
                        temp_switch = True

                if temp_switch:
                    if_decided = True
                    self.if_attack = True
                    self.pre_attack = False
                    self.if_controllable = False
                    self.action_count = 0  # 开始为强制动作计时

                    dx = self.attack_sequence[self.status]['vel'][0]
                    dy = self.attack_sequence[self.status]['vel'][1]
                    if dx:
                        self.speed_x = dx
                    if dy:
                        self.velocity.y = dy
                        fact_velocity.y = math.ceil(self.velocity.y)

                    self.stage_attack += 1

            elif self.pre_attack_hard and self.stage_attack >= 1:
                temp_switch = False     # 触发的战斗动作已经是最后一段

                if self.pre_attack_hard >= self.PRE_ATTACK_HARD_MAX:
                    if self.if_ground:
                        if not self.if_crouch:
                            self.status = 'attack_front_h'
                            temp_switch = True
                    else:
                        self.status = 'attack_air_h'
                        temp_switch = True

                if temp_switch:
                    if_decided = True
                    self.if_attack = True
                    self.pre_attack = False
                    self.if_controllable = False
                    self.action_count = 0  # 开始为强制动作计时
                    self.stage_attack = 0
                    self.pre_attack_hard = 0

                    dx = self.attack_sequence[self.status]['vel'][0]
                    dy = self.attack_sequence[self.status]['vel'][1]
                    if dx:
                        self.speed_x = dx
                    if dy:
                        self.velocity.y = dy
                        fact_velocity.y = math.ceil(self.velocity.y)

                    self.stage_attack += 1

            elif EventHandler.keydown(self.key_manager.key_jump) and self.stage_jump < self.STAGE_JUMP_MAX:
                self.stage_jump += 1
                self.status = 'rise_jump'

                # 跳起的速度处理
                self.velocity.y = self.speed_jump
                fact_velocity.y = math.ceil(self.velocity.y)
                self.if_ground = False

            elif EventHandler.keydown(self.key_manager.key_dash) and not self.if_ground and self.stage_dash < 2:
                self.if_dash = True
                self.stage_dash += 1
                self.status = 'dash'
                # 空中冲刺的速度处理
                self.speed_x = self.speed_run
                self.velocity.y = -2
                fact_velocity.y = math.ceil(self.velocity.y)

        if EventHandler.keydown(pygame.K_r):
            print(str(self.velocity))  # 测试用功能

        # 5&7.攻击、受击、跳跃、冲刺的一次性动作当中，向前数一帧。到达最大帧数时，进入下一个动作，并设置按键可控。
        if not if_decided:
            if self.status == 'attack_drop':
                # 下落攻击在落地时结束，同时创建子弹
                if_decided = True

                if self.action_count < self.attack_sequence[self.status]['total']:
                    if self.action_count == self.attack_sequence[self.status]['bullet']:
                        Bullet(groups=(self.group_list['sprite_group'], self.group_list['bullet_group']),
                               pos=pygame.Vector2(self.attack_sequence[self.status]['pos'][0],
                                                  self.attack_sequence[self.status]['pos'][1]),
                               param={'group_list': self.group_list,
                                      'animator': Animator(
                                          {'file_name': 'player_00_bullet.png',
                                           'size_pix': 40,
                                           'size_unit': (4, 4),
                                           'status': {'idle': self.attack_sequence[self.status]['anim']}}
                                      ),
                                      'frames': (),
                                      'velocity': pygame.Vector2(0, 0),
                                      'parent': self,
                                      'bond': True
                                      },
                               direction=self.direction,
                               to_enemy=True,
                               damage=self.v_attack*self.attack_sequence[self.status]['atk'])
                    self.action_count += 1
                else:
                    self.action_count = 0

                # 结束动作
                if self.if_ground:
                    if self.direction == 'R':
                        dx = self.rect.x + self.attack_sequence[self.status]['pos'][0]
                    else:
                        dx = self.rect.x - self.attack_sequence[self.status]['pos'][0]
                    Bullet(groups=(self.group_list['sprite_group'], self.group_list['bullet_group']),
                           pos=pygame.Vector2(dx,
                                              self.rect.y + self.attack_sequence[self.status]['pos'][1]),
                           param={'group_list': self.group_list,
                                  'animator': Animator(
                                      {'file_name': 'player_00_bullet.png',
                                       'size_pix': 40,
                                       'size_unit': (4, 4),
                                       'status': {'idle': (6, 0, 4)}}
                                  ),
                                  'frames': (0,),
                                  'velocity': pygame.Vector2(0, 0),
                                  'parent': self,
                                  'bond': False
                                  },
                           direction=self.direction,
                           to_enemy=True,
                           damage=self.v_attack*self.attack_sequence[self.status]['atk'])

                    self.if_attack = False
                    self.pre_attack = False
                    self.if_controllable = True
                    self.stage_attack = 0
                    self.pre_attack_hard = 0

                    self.crouch_counter = self.CROUCH_COUNTER_MAX
                    self.status = 'stand'
                    if_decided = False

            elif 'attack' in self.status:
                if_decided = True

                # 6.攻击中，读表设置可控，生成子弹
                if self.action_count <= self.attack_sequence[self.status]['total']:
                    if self.action_count == self.attack_sequence[self.status]['bullet']:
                        Bullet(groups=(self.group_list['sprite_group'], self.group_list['bullet_group']),
                               pos=pygame.Vector2(self.attack_sequence[self.status]['pos'][0],
                                                  self.attack_sequence[self.status]['pos'][1]),
                               param={'group_list': self.group_list,
                                      'animator': Animator(
                                          {'file_name': 'player_00_bullet.png',
                                           'size_pix': 40,
                                           'size_unit': (4, 4),
                                           'status': {'idle': self.attack_sequence[self.status]['anim']}}
                                      ),
                                      'frames': (18,),
                                      'velocity': pygame.Vector2(0, 0),
                                      'parent': self,
                                      'bond': True
                                      },
                               direction=self.direction,
                               to_enemy=True,
                               damage=self.v_attack*self.attack_sequence[self.status]['atk'])
                    self.action_count += 1

                # 允许在限定帧范围内取消后摇
                if 'cancel' in self.attack_sequence[self.status] and \
                        self.attack_sequence[self.status]['cancel'][0] <= self.action_count <= \
                        self.attack_sequence[self.status]['cancel'][1]:
                    self.if_controllable = True
                else:
                    self.if_controllable = False

                # 结束动作
                if self.animator.check_end():

                    self.if_attack = False
                    self.pre_attack = False
                    self.if_controllable = True
                    self.action_count = 0  # 开始为强制动作计时
                    self.stage_attack = 0
                    self.pre_attack_hard = 0

                    self.status = 'fall_free'
                    if_decided = False
            elif 'freeze' in self.status or 'faint' in self.status:
                pass
            elif 'down' in self.status:
                # 'down'后接'down_end'，直至结束，更新无敌帧数，不可被打断
                pass
            elif 'dash' in self.status:
                # 'dash'后接'dash_end'，可以被打断
                if_decided = True
                if self.animator.check_end():
                    if self.status == 'dash':
                        self.status = 'dash_end'
                        self.speed_x = self.speed_walk
                    elif self.status == 'dash_end':
                        self.status = 'fall_free'
                        if_decided = False

        # 4. 根据一些变量决定状态。
        if self.if_controllable and not if_decided:
            if self.if_ground:
                # 先处理下蹲输入
                if keys_press[self.key_manager.key_down]:
                    self.crouch_counter = min(self.crouch_counter + 1, self.CROUCH_COUNTER_MAX)
                else:
                    self.crouch_counter = max(self.crouch_counter - 1, 0)

                self.if_crouch = self.crouch_counter == self.CROUCH_COUNTER_MAX

                if self.crouch_counter:
                    if self.if_crouch:
                        if self.velocity.x:
                            self.status = 'crawl'
                        else:
                            self.status = 'crouch'
                    elif keys_press[self.key_manager.key_down]:
                        self.status = 'inv_stand'
                    else:
                        self.status = 'stand'
                else:
                    if keys_press[self.key_manager.key_dash] and self.if_ground and not self.if_crouch:
                        self.status = 'run'
                        self.speed_x = self.speed_run
                    elif self.velocity.x:
                        self.status = 'walk'
                    else:
                        self.status = 'idle'

            else:
                if 'jump' in self.status:
                    # 'rise_jump'后接'fall_jump'后接'fall_free'，可以被打断
                    if self.animator.check_end():
                        if self.status == 'rise_jump':
                            self.status = 'fall_jump'
                        elif self.status == 'fall_jump':
                            self.status = 'fall_free'
                elif fact_velocity.y <= 0 or self.if_wind:
                    self.status = 'rise_free'
                else:
                    self.status = 'fall_free'

            # 根据朝向方向和摩擦力编辑速度。还不管惯性。
            if keys_press[self.key_manager.key_left]:
                self.direction = 'L'
                if not self.status == 'run':
                    self.speed_x = self.speed_walk
            elif keys_press[self.key_manager.key_right]:
                self.direction = 'R'
                if not self.status == 'run':
                    self.speed_x = self.speed_walk
            elif self.if_ground:
                self.speed_x = 0

        elif self.if_ground:
            if self.speed_x <= 0.3:
                self.speed_x = 0
            else:
                self.speed_x *= 0.95

        if self.direction == 'L':
            self.velocity.x = -self.speed_x
        if self.direction == 'R':
            self.velocity.x = +self.speed_x
        fact_velocity.x = round(self.velocity.x)

        # 状态的帧更新
        if self.iv_frames > 0:
            self.iv_frames -= 1
        if self.tough < self.v_defence:
            self.tough += 1
        if self.if_ground:
            self.stage_jump = 0
            self.stage_dash = 0

        self.rect.x += fact_velocity.x  # applying horizontal velocity
        self.check_collisions('horizontal')
        self.rect.y += fact_velocity.y  # applying vertical velocity
        self.check_collisions('vertical')

    def check_collisions(self, direction):
        # 这里如果要考虑被推开的情况，以及图像尺寸与碰撞尺寸不一，那么我原有的那个更好一些。
        if direction == 'horizontal':
            for block in self.block_group:
                if block.rect.colliderect(self.animator.rect(self.rect)):
                    if self.velocity.x > 0:  # moving right
                        self.rect.x = block.rect.left - self.animator.bias_colli[0] - self.animator.size_colli[0]
                    elif self.velocity.x < 0:  # moving left
                        self.rect.x = block.rect.right - self.animator.bias_colli[0]
                    self.velocity.x = 0
        if direction == 'vertical':
            collisions = 0
            for block in self.block_group:
                if block.rect.colliderect(self.animator.rect(self.rect)):
                    if self.velocity.y >= 0:  # moving down
                        self.rect.y = block.rect.top - self.rect[3]
                        collisions += 1
                        self.velocity.y = 0
                    else:  # moving up
                        self.rect.y = block.rect.bottom - self.animator.bias_colli[1]
            if collisions > 0:
                self.if_ground = True
            else:
                self.if_ground = False

    def update(self):
        self.move()
        self.image = self.animator.image(run=True, current_stat=self.status, dir=self.direction)

        if self.health <= 0:
            self.kill()


