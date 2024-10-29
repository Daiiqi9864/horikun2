from world.sprite import *


class Bullet(pygame.sprite.Sprite):
    def __init__(self, groups, pos: pygame.math.Vector2, param: dict,
                 direction='R', to_player=False, to_enemy=False, homing=False, mass=0,
                 tough=0, damage=0, weak=False, short=True, life=0):
        super().__init__(*groups)

        self.group_list = param['group_list']
        self.to_player = to_player  # 子弹会击中谁
        self.to_enemy = to_enemy
        self.homing = homing    # 追踪。优先追踪敌人
        self.mass = mass    # 受重力影响的程度
        self.direction = direction

        self.tough = tough      # 削韧
        self.damage = damage
        self.weak = weak    # 一次碰撞后即销毁
        self.short = short  # 一次性动画播放完毕后即销毁
        self.life = life    # 生命周期帧数。当short激活的时候，该属性没用
        self.active = False     # 当前帧是否是子弹作为伤害作用的帧

        self.animator = param['animator']
        self.image = self.animator.image(run=False)
        self.frames = param['frames']   # 生效帧号
        self.frame_count = 0
        self.velocity = param['velocity']

        self.parent = param['parent']
        self.bond = param['bond']
        self.pos = pos
        if self.bond:
            if self.direction == 'R':
                self.rect = self.image.get_rect(
                    topleft=(self.parent.rect.x + self.pos.x, self.parent.rect.y + self.pos.y))
            else:
                self.rect = self.image.get_rect(
                    topleft=(self.parent.rect.x - self.pos.x, self.parent.rect.y + self.pos.y))

        else:
            self.rect = self.image.get_rect(topleft=pos)

    def on_collide(self):
        # 当子弹撞到了某个目标角色时，角色会调用子弹的该事件。
        if self.weak:
            self.kill()

    def update(self):
        if self.mass:
            self.velocity.y += GRAVITY * self.mass
            if self.velocity.y > SPD_LIM:
                self.velocity.y = SPD_LIM
        fact_velocity = pygame.Vector2(round(self.velocity.x), math.ceil(self.velocity.y))
        if self.bond:
            if self.direction == 'R':
                self.rect = self.image.get_rect(
                    topleft=(self.parent.rect.x + self.pos.x, self.parent.rect.y + self.pos.y))
            else:
                self.rect = self.image.get_rect(
                    topleft=(self.parent.rect.x - self.pos.x, self.parent.rect.y + self.pos.y))
        else:
            self.rect.x += fact_velocity.x
            self.rect.y += fact_velocity.y

        self.image = self.animator.image(run=True, dir=self.direction)

        self.frame_count += 1
        if self.frame_count in self.frames:
            self.active = True
        else:
            self.active = False
        if self.short:
            if self.animator.check_end():
                self.kill()
        else:
            if self.frame_count >= self.life:
                self.kill()
