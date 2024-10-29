# 事件是否存在于地图上，由自己的 active 属性决定
# paragraph_start, paragraph_end 项的取值没有意义，仅用来给剧本编写做参考。
# paragraph_end 项的设置没有意义，仅用来辅助剧本理解。
# paragraph_start 项后接 condition，用来表示实行条件，可以像以下这样写：
#
# 'condition': None		表示无需条件就进入，也可以不填。
# 'condition': 'item'
# 	'name': '物品名'
# 	'direction': 'equal', 'more', 'less', 'not_equal'	不填默认more，more含，less不含
# 	'quantity': 12
# 'condition': 'variable'
# 	'name': 'TILE_SIZE'		不填默认
# 	'direction': 'equal', 'more', 'less', 'not_equal'	不填默认equal
# 	'value': 32		不填默认True
# 'condition': 'player'
# 	'name': 'player_00'		不填默认player_00
# 	'direction': 'equal', 'not_equal'	不填默认equal
# 'condition': 'health'
# 	'direction': 'more', 'less'
# 	'quantity': 12
# 'condition': 'select'	接在选项后面，表示选择了对应选项后开启的段
# 	'value': 1		不填默认0
# 在表示复合条件时，可以添加 'and': True, 直到最后一条添加 'and': False， 表示所有条件and，该编写方法无视第一项的key，直至结束为止
#
# 选项必须处于一个 paragraph 的最后，而且前面必须紧跟一条 talk。


novel_data = {
    'template':
        [
            {'paragraph_start': 1},

            {'type': 'item', 'id': 2, 'quantity': +1},  # 记得显示log
            {'type': 'variable', 'name': 'test_value', 'value': +1},
            {'type': 'variable', 'name': 'test_value', 'quantity': +1},
            {'type': 'talk', 'content': '你好', 'stand': 'stand_02.png', 'stand_pos': 'L'},
            {'type': 'select', 'selects': {0: '选项1', 1: '选项2', 2: '选项3'}},
            {'paragraph_end': 1},

            {'paragraph_start': 2, 'condition': 'select', 'value': 0},
            {'type': 'log', 'content': 'log内容'},
            {'type': 'move', 'group': 'enemy_group', 'name': 'enemy00', 'dir': 'L', 'frame': 60},
            {'type': 'talk', 'content': '选项1对应对话'},
            {'paragraph_end': 2},

            {'paragraph_start': 2, 'condition': 'select', 'value': 1},
            {'type': 'talk', 'content': '选项2对应对话'},
            {'type': 'active', 'group': 'event_group', 'name': 'event00', 'dir': 'off'},
            {'paragraph_end': 2},

            {'paragraph_start': 2, 'condition': 'select', 'value': 2},
            {'type': 'talk', 'content': '选项3对应对话'},
            {'paragraph_end': 2},
        ]
}


