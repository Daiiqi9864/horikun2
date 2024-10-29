from world.sprite import *


class Npc(pygame.sprite.Sprite):
    def __init__(self, groups, pos: pygame.math.Vector2, param: dict):
        super().__init__(*groups)

        # parameters
        self.name = param['name']
        self.group_list = param['group_list']
        self.block_group = self.group_list['block_group']

        self.player = self.player = param['player']

        self.animator = param['animator']
        self.image = self.animator.image(run=False)
        self.rect = self.image.get_rect(topleft=pos)

        self.data_sheet = param['information']

        # movement
        self.velocity = pygame.math.Vector2()
        self.speed = self.data_sheet['speed']
        self.speed_walk = self.speed['speed_walk']
        self.speed_jump = self.speed['speed_jump']

        # states
        self.auto_trigger = self.data_sheet['auto_trigger']
        self.active = self.data_sheet['active']
        self.event_name = self.data_sheet['event_name']

        self.status = 'idle'
        self.direction = 'R'

        self.grounded = False

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
            else:
                self.direction = 'L'

        fact_velocity = pygame.Vector2(0, math.ceil(self.velocity.y))

        self.rect.y += fact_velocity.y
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
                self.grounded = True
            else:
                self.grounded = False

    def update(self):
        if not self.active:
            self.kill()
        self.move()
        self.image = self.animator.image(run=True, current_stat=self.status)
