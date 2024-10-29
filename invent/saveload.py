from invent.item import *
import pickle


class SaveManager:
    def __init__(self, param):
        # 现在仅支持处理当前所在地图的事件开关。以后增加地图之后记得把这项改成带地图索引字典的。
        self.event_list = param['event_list']
        self.player = param['player']

        self.global_variables = {
            'test_value': 114,
        }

        # groups: list[str] = ['sprites', 'item_group']
        self.items: dict[str, Item] = {
            0: ItemUse("QQ软糖", (0, 0), 0, "看起来像是刨冰味的。刨冰大概是软糖味的。"),  # 最多能放下22个全角字符。
            1: ItemUse("01", (0, 1), 0, "intro1"),
            2: ItemUse("02", (0, 2), 0, ["这这这这这这这这这这这这这这这这这这这这这这这这", "qwerty"]),
            3: ItemUse("03", (0, 3), 0, "xx"),
            4: ItemUse("04", (0, 4), 0, "1"),
            5: ItemUse("05", (0, 5), 0, ["1111", "22", "33"]),
            6: ItemUse("xxxx", (1, 0), 0, "x"),
            7: ItemUse("这个东西", [1, 1], 0, "  "),
            8: ItemUse("一二三四五六七", [1, 2], 0, "啊"),
            9: ItemUse("蚂蚁", (1, 3), 0, "刚从战场归来的,血淋淋的蚂蚁。"),
            10: ItemUse("鲸鱼", (1, 4), 0, "鲸鱼吃过的棒棒糖。它很乐于和人分享。"),
            11: ItemUse("小草", (1, 5), 0, "不知道从哪摘的野草。")
        }

        self.player_state = {
            'name': '',
            'position': (0, 0),
            'health': 1,
            'health_max': 1
        }

        self.map_key = ''

    def redirect_eventlist(self, content):
        # 替换指向对象
        self.event_list = content

    def redirect_player(self, player):
        self.player = player

    def update_player(self):
        # 更新主角相关存档内容
        self.player_state['name'] = self.player.name
        self.player_state['position'] = (self.player.rect.x, self.player.rect.y)
        self.player_state['health'] = self.player.health
        self.player_state['health_max'] = self.player.health_max

    def apply_player(self):
        # 从即时存档加载主角相关内容
        self.player.name = self.player_state['name']
        self.player.rect.x = self.player_state['position'][0]
        self.player.rect.y = self.player_state['position'][1]
        self.player.health = self.player_state['health']
        self.player.health_max = self.player_state['health_max']

    def save(self):
        group_active = dict()
        for chunk_pos in self.event_list:
            group_active[chunk_pos] = list()
            for i in range(len(self.event_list[chunk_pos])):
                group_active[chunk_pos].append(self.event_list[chunk_pos][i].active)

        item_count = dict()
        for key in self.items:
            item_count[key] = self.items[key].quantity

        self.update_player()

        with open('save_dir/savefile.pkl', 'wb') as f:
            savedata = {
                'event': group_active,
                'var': self.global_variables.copy(),
                'item': item_count,
                'stat': self.player_state.copy(),
                'map': self.map_key
            }
            pickle.dump(savedata, f)

    def load(self):
        with open('save_dir/savefile.pkl', 'rb') as f:
            savedata = pickle.load(f)

        group_active = savedata['event'].copy()
        for chunk_pos in self.event_list:
            for i in range(len(self.event_list[chunk_pos])):
                self.event_list[chunk_pos][i].active = group_active[chunk_pos][i]

        self.global_variables = savedata['var'].copy()

        item_count = savedata['item'].copy()
        for key in self.items:
            self.items[key].quantity = item_count[key]

        self.player_state = savedata['stat'].copy()
        self.player.name = self.player_state['name']
        self.player.rect.x = self.player_state['position'][0]
        self.player.rect.y = self.player_state['position'][1]
        self.player.health = self.player_state['health']
        self.player.health_max = self.player_state['health_max']

        self.map_key = savedata['map']
