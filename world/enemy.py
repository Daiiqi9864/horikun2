from world.bullet import *


class Mob(pygame.sprite.Sprite):
    def __init__(self, groups, pos: pygame.math.Vector2, param: dict):
        super().__init__(*groups)

        # parameters
        self.name = param['name']
        self.group_list = param['group_list']
        self.block_group = self.group_list['block_group']
        self.enemy_group = self.group_list['enemy_group']

        self.player = self.player = param['player']

        self.animator = param['animator']
        self.image = self.animator.image(run=False)
        self.rect = self.image.get_rect(topleft=pos)

        self.data_sheet = param['information']

        # health parameters
        self.health_max = self.data_sheet['health']
        self.health = self.data_sheet['health']

        # movement
        self.velocity = pygame.math.Vector2()
        self.speed = self.data_sheet['speed']
        self.speed_walk = self.speed['speed_walk']
        self.speed_jump = self.speed['speed_jump']

        # states
        self.active = self.data_sheet['active']
        self.status = 'idle'
        self.direction = 'R'

        self.attack = False
        self.attack_in_cd = False
        self.grounded = False

        # attack
        self.attack_pattern = self.data_sheet['atk_pattern']
        self.attack_damage = self.data_sheet['atk_damage']

        # cooldown
        self.attack_cooldown = 60
        self.counter = self.attack_cooldown

    def move(self):

        self.velocity.y += GRAVITY
        # terminal velocity check
        if self.velocity.y > SPD_LIM:
            self.velocity.y = SPD_LIM

        dx = self.player.rect.x - self.rect.x
        dy = self.player.rect.y - self.rect.y
        if abs(dx) < TILE_SIZE * 3 and abs(dy) < TILE_SIZE * 3:
            # within range
            if dx >= 0:
                self.direction = 'R'
                if dx <= TILE_SIZE/2 and self.grounded and not self.attack_in_cd:
                    self.attack = True
                    self.velocity.x = 0
                    self.status = 'attack_ground'
                elif not self.attack_in_cd:
                    self.velocity.x = self.speed_walk
                    self.status = 'walk'
            else:
                self.direction = 'L'
                if dx >= -TILE_SIZE/2 and self.grounded and not self.attack_in_cd:
                    self.attack = True
                    self.velocity.x = 0
                    self.status = 'attack_ground'
                elif not self.attack_in_cd:
                    self.velocity.x = -self.speed_walk
                    self.status = 'walk'
        else:
            self.attack = False
            self.velocity.x = 0
            self.status = 'idle'

        fact_velocity = pygame.Vector2(round(self.velocity.x), math.ceil(self.velocity.y))

        self.rect.x += fact_velocity.x
        self.check_collisions('horizontal')
        self.rect.y += fact_velocity.y
        self.check_collisions('vertical')

        if self.grounded and not self.attack and abs(self.velocity.x) < 0.1:
            self.velocity.y = -self.speed_jump
            self.grounded = False

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
                self.grounded = True
            else:
                self.grounded = False

    def check_player_collision(self):
        if self.status == 'attack_ground' and not self.attack_in_cd:
            if self.rect.colliderect(self.player.rect):
                self.player.health -= self.attack_damage['attack_ground']
                self.attack_in_cd = True
                self.counter = self.attack_cooldown

                # knockback player(在写好玩家横向变速之前还没用)
                if self.player.rect.centerx > self.rect.centerx:
                    self.player.velocity.x = 2
                elif self.player.rect.centerx < self.rect.centerx:
                    self.player.velocity.x = -2
                self.player.velocity.y += -2

    def update(self):
        self.move()
        self.check_player_collision()
        self.image = self.animator.image(run=True, current_stat=self.status)

        if self.attack_in_cd:
            self.counter -= 1
            if self.counter < 0:
                self.counter = self.attack_cooldown
                self.attack_in_cd = False
