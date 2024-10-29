"""
world/item.py
"""


class Item:
    def __init__(self, name="name", graph_index=(0, 0), quantity=0, introduce=None) -> None:
        self.name = name
        self.graph_index = graph_index
        self.quantity = quantity
        self.introduce = introduce

    def use(self, *args, **kwargs):
        pass

    def __str__(self):
        return f'Name: {self.name}, Quantity: {self.quantity}'


class ItemUse(Item):  # special item type
    def __init__(self, name, graph_index, quantity=0, introduce=None, param=None) -> None:
        super().__init__(name, graph_index, quantity, introduce)
        if param is None:
            pass
        else:
            if 'hp' in param:
                self.hp = param('hp')  # 回复量
            if 'sp' in param:
                self.hp = param('sp')  # SP在这个游戏中是各种攻击连招消耗的体力值。也许在野外打开菜单也会消耗一定的SP。
            if 'mhp' in param:
                self.hp = param('mhp')  # 最大HP   *以下都是暂时增加
            if 'msp' in param: self.hp = param('msp')  # 最大SP
            if 'atk' in param: self.hp = param('atk')  # 攻击力。指增伤系数。
            if 'def' in param: self.hp = param('def')  # 防御力。指减伤系数。
            if 'spd' in param: self.hp = param('spd')  # 移动速度。因为是动作游戏，所以“速度”概念很重要，拆了。
            if 'agi' in param: self.hp = param('agi')  # 敏捷，这里指攻击速度
            if 'eva' in param: self.hp = param('eva')  # 回避率。
            if 'cri' in param: self.hp = param('cri')  # 暴击率。指增伤系数翻倍几率
            if 'duration' in param: self.hp = param('duration')  # 持续时间。

    def use(self, player):
        if self.quantity > 0:
            self.quantity -= 1
            pass  # 对场上角色起效


class ItemMat(Item):  # special item type
    def __init__(self, name, graph_index, quantity, introduce):
        super().__init__(name, graph_index, quantity, introduce)


class ItemKey(Item):  # special item type
    def __init__(self, name, graph_index, quantity, introduce):
        super().__init__(name, graph_index, quantity, introduce)

