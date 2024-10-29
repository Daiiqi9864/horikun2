import pygame
from misc.globals import *
import math


def read_image(name: str):
    image = pygame.image.load('res/' + name).convert()
    image.set_colorkey(TRANSPARENT_COLORKEY)
    return image


class SpriteSheet:
    def __init__(self, sheet_tile_data):
        self.sheet = read_image(sheet_tile_data['file_name'])
        self.size_pix = sheet_tile_data['size_pix']
        if 'size_unit' in sheet_tile_data:
            self.size_unit = sheet_tile_data['size_unit']
        else:
            (m,n) = self.sheet.get_size()
            self.size_unit = (int(m/self.size_pix), int(n/self.size_pix))
        self.textures = {}
        for i in range(self.size_unit[0]):
            for j in range(self.size_unit[1]):
                self.textures[i * 0x10 + j * 0x01] = pygame.Surface.subsurface(
                    self.sheet, pygame.Rect(i * self.size_pix, j * self.size_pix, self.size_pix, self.size_pix))


class Animator:
    # Taking over the sprite sheet, animation and collider rect of a sprite(player etc.)
    # Reminding status machine is complemented in sprite class, this animator only plays corresponding animation.
    def __init__(self, param):
        self.sheet = read_image(param['file_name'])
        self.size_pix = param['size_pix']
        if 'size_unit' in param:
            self.size_unit = param['size_unit']
        else:
            (m,n) = self.sheet.get_size()
            self.size_unit = (int(m/self.size_pix), int(n/self.size_pix))

        if 'size_colli' in param:
            self.size_colli = param['size_colli']
        else:
            self.size_colli = [self.size_pix,self.size_pix]
        if 'type_colli' in param:
            self.type_colli = param['type_colli']
        else:
            self.type_colli = 'bottom'

        self.status = param['status']

        self.last_stat = 'idle'
        self.current_stat = 'idle'
        self.frame_index = 0    # 当前正在播放的关键帧序号
        self.frame_count = 0    # 当前正在播放的帧序号

        self.textures = {}
        for key in self.status:
            self.textures[key] = []
            for i in range(self.status[key][1], self.status[key][1] + self.status[key][2]):
                self.textures[key].append(
                    pygame.Surface.subsurface(
                        self.sheet, pygame.Rect(i * self.size_pix, self.status[key][0] * self.size_pix,
                                                self.size_pix, self.size_pix))
                )

        if self.type_colli == 'bottom':
            self.bias_colli = [int((self.size_pix - self.size_colli[0]) / 2), self.size_pix - self.size_colli[1]]
        elif self.type_colli == 'center':
            self.bias_colli = [int((self.size_pix - self.size_colli[0]) / 2),
                               int((self.size_pix - self.size_colli[1]) / 2)]
        else:
            self.bias_colli = [0, 0]

    def rect(self, pos):
        # return the actual collider of this sprite
        return pygame.Rect(pos[0] + self.bias_colli[0],
                           pos[1] + self.bias_colli[1],
                           self.size_colli[0],
                           self.size_colli[1])

    def image(self, run=True, current_stat='idle', dir='R'):
        # decide
        self.last_stat = self.current_stat
        self.current_stat = current_stat

        if self.current_stat != self.last_stat:
            self.frame_index = 0
            self.frame_count = 0

        # tick
        if run:
            self.frame_count += 1
            if self.frame_count >= ANIME_FRAME:
                self.frame_count = 0
                self.frame_index += 1
                if self.frame_index >= self.status[current_stat][2]:
                    self.frame_index = 0

        image_temp = self.textures[self.current_stat][self.frame_index]
        if dir == 'R':
            return image_temp
        else:
            return pygame.transform.flip(image_temp, True, False)

    def check_end(self):
        return (self.frame_count >= ANIME_FRAME-1) and (self.frame_index >= self.status[self.current_stat][2]-1)


class Entity(pygame.sprite.Sprite):
    def __init__(self, groups, image=pygame.Surface((TILE_SIZE, TILE_SIZE)),
                 position=(0, 0), name: str = "default"):
        super().__init__(*groups)
        self.name = name  # identifier
        self.in_groups = groups
        self.image = image
        self.rect = self.image.get_rect(topleft=position)

    def update(self):
        pass


