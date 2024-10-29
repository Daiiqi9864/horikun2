from mapdata.data_map import map_data
from world.texturedata import *
from world.player import Player
from world.enemy import *
from world.npc import *
from misc.camera import Camera
from world.menuUI import *
from world.mapUI import *
from world.novel import *
from misc.keys import *
from invent.saveload import *
from typing import Dict, Optional


class Map:
    def __init__(self, map_data=None, param=None):
        # enfolding parameters
        self.name = param['name']
        self.player = param['player']
        self.tile_sheet = SpriteSheet(param['textures'])
        self.enemy_animator = Animator(param['enemy'])
        self.event_animator = Animator(param['event'])
        self.key_manager = param['key_manager']
        self.item_texture = param['item_texture']
        self.group_list = param['group_list']
        self.save_manager = param['save_manager']

        # place tile according to map
        self.map_data = map_data
        self.tile_list = {}
        self.enemy_list = {}
        self.event_list = {}

        self.size_map_chunk_pix = (len(self.map_data[0][0][0]) * TILE_SIZE,
                                   len(self.map_data[0][0]) * TILE_SIZE)
        self.size_map_pix = (len(self.map_data[0]) * self.size_map_chunk_pix[0],
                             len(self.map_data) * self.size_map_chunk_pix[1])
        print("world map chunk pix size: " + str(self.size_map_chunk_pix))
        print("world map max pix size: " + str(self.size_map_pix))

        self.chunk_pos = tuple()
        self.active_chunk_refs = list()
        self.check_chunk()
        self.active_chunks: list[tuple[int, int]] = []

    def check_enemy(self):
        return self.enemy_list

    def check_event(self):
        return self.event_list

    def check_chunk(self):
        self.chunk_pos = (self.player.rect[0] // self.size_map_chunk_pix[0],
                          self.player.rect[1] // self.size_map_chunk_pix[1])  # 获取玩家当前所在的chunk坐标

        self.active_chunk_refs = [
            (self.chunk_pos[0] - 1, self.chunk_pos[1] - 1),
            (self.chunk_pos[0], self.chunk_pos[1] - 1),
            (self.chunk_pos[0] + 1, self.chunk_pos[1] - 1),

            (self.chunk_pos[0] - 1, self.chunk_pos[1]),
            (self.chunk_pos[0], self.chunk_pos[1]),
            (self.chunk_pos[0] + 1, self.chunk_pos[1]),

            (self.chunk_pos[0] - 1, self.chunk_pos[1] + 1),
            (self.chunk_pos[0], self.chunk_pos[1] + 1),
            (self.chunk_pos[0] + 1, self.chunk_pos[1] + 1),
        ]

    def update_chunk(self):
        # check if chunk changed. if changed, call the chunks to load or unload.
        self.check_chunk()

        for temp_chunk_pos in self.active_chunk_refs:
            # load or allocate
            if temp_chunk_pos not in self.active_chunks:
                if 0 <= temp_chunk_pos[0] < len(self.map_data[0]) and\
                        0 <= temp_chunk_pos[1] < len(self.map_data[1]):
                    self.load_chunk(temp_chunk_pos)
                    self.active_chunks.append(temp_chunk_pos)
        targets = []
        for temp_chunk_pos in self.active_chunks:
            if temp_chunk_pos not in self.active_chunk_refs:
                targets.append(temp_chunk_pos)
        for temp_chunk_pos in targets:
            # unload
            self.unload_chunk(temp_chunk_pos)
            self.active_chunks.remove(temp_chunk_pos)

    def load_chunk(self, chunk_pos):
        map_data = self.map_data[chunk_pos[1]][chunk_pos[0]]

        x_max = len(map_data[0])
        y_max = len(map_data)
        x_pix_start = chunk_pos[0] * self.size_map_chunk_pix[0]
        y_pix_start = chunk_pos[1] * self.size_map_chunk_pix[1]

        if not (chunk_pos in self.tile_list):
            self.tile_list[chunk_pos] = []
            self.enemy_list[chunk_pos] = []
            self.event_list[chunk_pos] = []

        for y in range(y_max):
            for x in range(x_max):
                tile_index = map_data[y][x]
                if tile_index == None:
                    continue
                else:
                    pos = (x_pix_start + x * self.tile_sheet.size_pix,
                           y_pix_start + y * self.tile_sheet.size_pix)

                    # first iteration: place map
                    if tile_index < 0x80:
                        # tile
                        tile_texture = self.tile_sheet.textures[tile_index]
                        if tile_index % 2:
                            group_tuple = (self.group_list['sprite_group'], self.group_list['block_group'])
                        else:
                            group_tuple = (self.group_list['sprite_group'],)
                        self.tile_list[chunk_pos].append(Entity(group_tuple, tile_texture, pos))

                    # second iteration: place enemy(0x80 ~ 0xB9)
                    elif tile_index == 0x80:
                        self.enemy_list[chunk_pos].append(
                            Mob(groups=(self.group_list['sprite_group'], self.group_list['enemy_group']),
                                pos=pygame.math.Vector2(pos),
                                param={'name': 'enemy00',
                                       'animator': self.enemy_animator,
                                       'group_list': self.group_list,
                                       'player': self.player,
                                       'information': sheet_enemy_data
                                       }))

                    # third iteration: place event(0xC0 ~ 0xFE)
                    elif tile_index == 0xC0:
                        self.event_list[chunk_pos].append(
                            Npc(groups=(self.group_list['sprite_group'], self.group_list['event_group']),
                                pos=pygame.math.Vector2(pos),
                                param={'name': 'event00',
                                       'animator': self.event_animator,
                                       'group_list': self.group_list,
                                       'player': self.player,
                                       'information': sheet_event_data
                                       }))

    def unload_chunk(self, chunk_pos):
        for sprite in self.tile_list[chunk_pos]:
            sprite.kill()
        self.tile_list.pop(chunk_pos)
        for sprite in self.enemy_list[chunk_pos]:
            sprite.kill()
        self.enemy_list.pop(chunk_pos)
        for sprite in self.event_list[chunk_pos]:
            sprite.kill()
        self.event_list.pop(chunk_pos)


class Scene:
    # game window manager
    def __init__(self, app, name, gameStateManager) -> None:
        self.app = app

        self.sprites = Camera()
        self.key_manager = KeyManager()
        self.blocks = pygame.sprite.Group()  # block表示地图上不可通过的块，chunk表示地图区块
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.events = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.group_list: dict[str, pygame.sprite.Group] = {
            'sprite_group': self.sprites,
            'block_group': self.blocks,
            'enemy_group': self.enemies,
            'bullet_group': self.bullets,
            'event_group': self.events,
            'item_group': self.items
        }

        self.save_manager = SaveManager(param={
            'event_list': None,
            'player': None
        })  # 在缓存里创建一个初始存档
        self.global_variables = self.save_manager.global_variables
        self.items = self.save_manager.items
        self.player_state = self.save_manager.player_state

        self.event_name = ''  # 触发事件，进入暂停

        item_tile = read_image('item.png')
        self.item_tiles = {}  # 因为不能在定义surface之前先调用subsurface，所以需要在这里单读一遍
        for key in self.items:
            self.item_tiles[key] = pygame.Surface.subsurface(item_tile,
                                                             [ITEM_SIZE * self.items[key].graph_index[1],
                                                              ITEM_SIZE * self.items[key].graph_index[0],
                                                              ITEM_SIZE, ITEM_SIZE])
        self.maps: dict[str, Map] = {}  # 定义一个空字典，用来存储当前map与缓存map
        # 加载初始map
        self.map_key = MAP_KEY_INIT  # 当前正位于前台的map
        self.map_key_old = self.map_key  # 用来判断帧更新的地图切换
        self.active_chunks = None
        self.player = None
        self.enemy_list = None
        self.event_list = None

        self.player_animator = Animator(sheet_player_data)
        self.player = self.gen_player(sheet_player_data)

        self.load_map(self.map_key)  # 创建 map_key 对应的 map 示例，并且填补上述内容
        
        self.mapUI = MapUI(param={'screen': self.app.screen,
                                  'sprite_group': self.sprites,
                                  'group_list': self.group_list,
                                  'player': self.player
                                  })
        self.log = Log(param={'screen': self.app.screen})
        self.menuUI = MenuUI(param={'screen': self.app.screen,
                                    'player': self.player,
                                    'log': self.log,
                                    'item_texture': self.item_tiles,
                                    'save_manager': self.save_manager
                                    })
        self.novel = Novel(param={'screen': self.app.screen,
                                  'player': sheet_player_data,
                                  'mapUI': self.mapUI,
                                  'log': self.log,
                                  'group_list': self.group_list,
                                  'save_manager': self.save_manager
                                  })

        self.window_stat = 'in_game'  # 先不与 WINDOW_STAT 同步。暂时觉得没必要。

    def gen_player(self, param):
        # place player(过去没有指定位置，在地图上定义了0xFF，并在迭代中查询地图完成。现在该定义无效，按照指定位置一次性生成。)

        player_pos = PLY_POS_INIT.copy()

        return Player(
            (self.group_list['sprite_group'],),
            pos=player_pos,
            param={'name': 'player00',
                   'animator': self.player_animator,
                   'group_list': self.group_list,
                   'key_manager': self.key_manager,
                   'information': param
                   })

    def update(self):
        if self.window_stat == 'in_game':

            if EventHandler.keydown(self.key_manager.key_exit):
                self.window_stat = 'in_menu'

            self.event_name = self.player.input(self.event_name)
            if self.event_name:
                self.novel.set_script(self.event_name)
                self.window_stat = 'in_talk'
            else:
                self.sprites.update()
                # 允许玩家在地图上变化位置。然后是改变位置之后的更新事件

                if self.map_key != self.map_key_old:
                    self.change_map()

                self.maps[self.map_key].update_chunk()  # 单个map内的chunk检测加载在map下完成。

        elif self.window_stat == 'in_menu':

            if EventHandler.keydown(self.key_manager.key_exit):
                if self.menuUI.esc():
                    self.window_stat = 'in_game'
            if_UI_close = self.menuUI.update()
            if if_UI_close:
                self.window_stat = 'in_game'

        elif self.window_stat == 'in_talk':

            result = self.novel.update()
            if result:
                self.window_stat = 'in_game'

    def load_map(self, map_key):
        self.maps[map_key] = Map(map_data[map_key],
                                 param={'name': map_key,
                                        'player': self.player,
                                        'textures': sheet_texture_data,
                                        'enemy': sheet_enemy_data,
                                        'event': sheet_event_data,
                                        'key_manager': self.key_manager,
                                        'item_texture': self.item_tiles,
                                        'group_list': self.group_list,
                                        'save_manager': self.save_manager})
        self.active_chunks = self.maps[map_key].active_chunks

        self.enemy_list = self.maps[map_key].check_enemy()
        self.event_list = self.maps[map_key].check_event()

        self.save_manager.redirect_eventlist(self.event_list)
        self.save_manager.redirect_player(self.player)
        self.save_manager.map_key = self.map_key

    def change_map(self):
        # 从旧地图切到当前正在的（本帧某些事件要求切换到的）地图
        self.save_manager.update_player()  # 记录当前主角信息
        self.load_map(self.map_key)  # 定义新地图
        self.save_manager.apply_player()  # 加载当前主角信息
        # 移除旧地图
        self.maps.pop(self.map_key_old)
        self.map_key_old = self.map_key  # 更新

    def draw(self):
        self.app.screen.fill('lightblue')
        self.sprites.draw(self.maps[self.map_key].player, self.app.screen)
        self.mapUI.draw()
        if self.window_stat == 'in_menu':
            self.menuUI.draw()
        elif self.window_stat == 'in_talk':
            self.novel.draw()
        self.log.draw()
