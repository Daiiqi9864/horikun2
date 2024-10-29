import pygame
from world.player import Player

class Camera(pygame.sprite.Group):

    CAMERA_SPEED = 0.01
    CAMERA_PROPORTION = 0.5     # 它控制移动镜头的速度
    CAMERA_LIMIT = 800     # 超过这个距离的话，就用瞬移了
    offset = pygame.math.Vector2()

    def __init__(self):
        super().__init__()

    def draw(self, target: Player, display: pygame.Surface):
        offset_target = pygame.math.Vector2()
        offset_target.x = display.get_width() / 2 - target.rect.centerx
        offset_target.y = display.get_height() / 2 - target.rect.centery

        offset_delta_1 = offset_target - self.offset
        offset_delta_2 = pygame.math.Vector2()
        if offset_delta_1.x > self.CAMERA_LIMIT or offset_delta_1.y > self.CAMERA_LIMIT:
            offset_delta_2.x = offset_delta_1.x
            offset_delta_2.y = offset_delta_1.y
        else:
            offset_delta_2.x = self.CAMERA_PROPORTION * offset_delta_1.x * min(1.0, abs(offset_delta_1.x)*self.CAMERA_SPEED)
            offset_delta_2.y = self.CAMERA_PROPORTION * offset_delta_1.y * min(1.0, abs(offset_delta_1.y)*self.CAMERA_SPEED)
        self.offset += offset_delta_2

        for sprite in self.sprites():
            sprite_offset = pygame.math.Vector2()
            sprite_offset.x = self.offset.x + sprite.rect.x
            sprite_offset.y = self.offset.y + sprite.rect.y

            display.blit(sprite.image, sprite_offset)