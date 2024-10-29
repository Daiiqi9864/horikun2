from misc.globals import *

sheet_texture_data = {
    'type': 'tile',
    'file_name': 'tile_00.png',
    'size_pix': TILE_SIZE,
    'size_unit': (3,3)
}

sheet_player_data = {
    'type': 'character',
    'file_name': 'player_00.png',
    'size_pix': 40,
    'size_unit': (15, 16),

    'size_colli': (16,24),
    'type_colli': 'bottom',
    'health': 100,
    'speed': {
        'speed_walk': 2,
        'speed_run': 5,
        'speed_dash': 3,
        'speed_jump': -7
    },

    # (动画所在行，起始列，从起始列开始共有的列数)
    'status': {
        # 站立静止(4)
        'idle': (0, 0, 4),
        # 跳跃上升(4), once
        'rise_jump': (0, 5, 4),
        # 受力上升(4)
        'rise_free': (0, 10, 4),

        # 站立晕眩(4)
        'faint': (1, 0, 4),
        # 跳跃下降(4), once, 也是所有强制动作结束后的默认过渡结果
        'fall_jump': (1, 5, 4),
        # 自由落体(4)
        'fall_free': (1, 10, 4),

        # 行走(6)
        'walk': (2, 0, 6),
        # 跑步(6)
        'run': (2, 7, 6),

        # 空中冲刺(4)
        'dash': (3, 0, 4),
        # 冲刺结束(4), once
        'dash_end': (3, 5, 4),
        # 下蹲静止(4)
        'crouch': (3, 10, 4),

        # 倒地(4)
        'down': (4, 0, 4),
        # 倒地起身(4), once
        'down_end_stand': (4, 5, 4),
        # 倒地起蹲(4), once
        'down_end_crouch': (4, 10, 4),

        # 前向攻击(4), once
        'attack_front_1': (5, 0, 6),
        'attack_front_2': (5, 7, 6),
        'attack_front_3': (6, 0, 6),
        # 前上攻击(4), once
        'attack_up_1': (6, 7, 6),
        'attack_up_2': (7, 0, 6),
        'attack_up_3': (7, 7, 6),
        # 前下攻击(4), once
        'attack_down_1': (8, 0, 6),
        'attack_down_2': (8, 7, 6),
        'attack_down_3': (9, 0, 6),
        # 空中攻击(4), once
        'attack_air_1': (9, 7, 6),
        'attack_air_2': (10, 0, 6),
        'attack_air_3': (10, 7, 6),
        # 下落攻击(4), once
        'attack_drop': (11, 0, 6),
        # 前向aa重(4), once
        'attack_front_h': (11, 7, 6),
        # 空中aa重(4), once
        'attack_air_h': (12, 0, 6),
        # 下蹲攻击(4), once
        'attack_crouch_1': (12, 7, 6),
        'attack_crouch_2': (13, 0, 6),
        'attack_crouch_3': (13, 7, 6),

        # 下蹲行走(6)
        'crawl': (14, 0, 6),
        # 蹲站切换(4), once
        'stand': (14, 7, 4),
        'inv_stand': (15, 7, 4),
        # 站立硬直(1)
        'freeze_normal': (14, 12, 1),
        # 下蹲硬直(1)
        'freeze_down': (14, 13, 1),

        # 预留(12)
        'special_skill': (15, 0, 6),
        'special_wait': (15, 7, 6)
    },

    # (攻击动作的总帧数，发射子弹的帧号，是否允许手动取消后摇，可以取消后摇的帧范围)
    # 子弹中心偏置，子弹覆盖半径这些，之后再加。
    'attack_sequence': {
        'attack_front_1':  {'anim': (0, 0, 4), 'pos': (15, 0), 'atk': 1.0, 'vel': (1, 0), 'total': 24, 'bullet': 4, 'cancel': (14, 20)},
        'attack_front_2':  {'anim': (0, 5, 4), 'pos': (15, 0), 'atk': 1.0, 'vel': (1, 0), 'total': 24, 'bullet': 4, 'cancel': (14, 20)},
        'attack_front_3':  {'anim': (0, 10,4), 'pos': (15, 0), 'atk': 1.0, 'vel': (1, 0), 'total': 24, 'bullet': 4, 'cancel': (24, 24)},
        'attack_up_1':     {'anim': (1, 0, 4), 'pos': (18, 0), 'atk': 1.0, 'vel': (0, 0), 'total': 24, 'bullet': 4, 'cancel': (14, 20)},
        'attack_up_2':     {'anim': (1, 5, 4), 'pos': (18, 0), 'atk': 1.0, 'vel': (0, 0), 'total': 24, 'bullet': 4, 'cancel': (14, 20)},
        'attack_up_3':     {'anim': (1, 10,4), 'pos': (18, 0), 'atk': 1.0, 'vel': (0, 0), 'total': 24, 'bullet': 4},
        'attack_down_1':   {'anim': (2, 0, 4), 'pos': (10, 5), 'atk': 1.0, 'vel': (0, 0), 'total': 24, 'bullet': 4, 'cancel': (14, 20)},
        'attack_down_2':   {'anim': (2, 5, 4), 'pos': (10, 5), 'atk': 1.0, 'vel': (0, 0), 'total': 24, 'bullet': 4, 'cancel': (14, 20)},
        'attack_down_3':   {'anim': (2, 10,4), 'pos': (10, 5), 'atk': 1.0, 'vel': (0, 0), 'total': 24, 'bullet': 4},
        'attack_air_1':    {'anim': (3, 0, 4), 'pos': ( 0, 0), 'atk': 1.0, 'vel': (None, -2), 'total': 24, 'bullet': 4, 'cancel': (14, 20)},
        'attack_air_2':    {'anim': (3, 5, 4), 'pos': ( 0, 0), 'atk': 1.0, 'vel': (None, -2), 'total': 24, 'bullet': 4, 'cancel': (14, 20)},
        'attack_air_3':    {'anim': (3, 10,4), 'pos': ( 0, 0), 'atk': 1.0, 'vel': (None, -2), 'total': 24, 'bullet': 4, 'cancel': (24, 24)},
        'attack_drop':     {'anim': (4, 0, 4), 'pos': (20, 0), 'atk': 1.0, 'vel': (0, 4), 'total': 24, 'bullet': 0},
        'attack_front_h':  {'anim': (4, 5, 4), 'pos': ( 0, 0), 'atk': 1.0, 'vel': (3, 0), 'total': 24, 'bullet': 4},
        'attack_air_h':    {'anim': (4, 10,4), 'pos': ( 0, 0), 'atk': 1.0, 'vel': (1, -3), 'total': 24, 'bullet': 4},
        'attack_crouch_1': {'anim': (5, 0, 4), 'pos': (10, 5), 'atk': 1.0, 'vel': (0, 0), 'total': 24, 'bullet': 4, 'cancel': (14, 20)},
        'attack_crouch_2': {'anim': (5, 5, 4), 'pos': (10, 5), 'atk': 1.0, 'vel': (0, 0), 'total': 24, 'bullet': 4, 'cancel': (14, 20)},
        'attack_crouch_3': {'anim': (5, 10,4), 'pos': (10, 5), 'atk': 1.0, 'vel': (0, 0), 'total': 24, 'bullet': 4},
    },
    # 各类攻击与段数的攻击力
    'atk_damage': {
        'attack_ground': 10,
        'attack_run': 20,
        'attack_reach': 8,
        'attack_drop': 14
    }
}

sheet_enemy_data = {
    'type': 'character',
    'file_name': 'sprite_00.png',
    'size_pix': 40,
    'size_unit': (4, 4),

    'size_colli': (24,28),
    'type_colli': 'bottom',
    'health': 60,
    'speed': {
        'speed_walk': 1,
        'speed_jump': -4
    },
    'active': True,

    # (动画所在行，起始列，从起始列开始共有的列数)
    'status': {
        'idle': (1, 0, 4),
        'walk': (0, 0, 4),
        'attack_ground': (3, 0, 4),
    },
    # (前摇占用帧数，（起效帧），后摇占用帧数)
    'atk_pattern': {
        'attack_ground': (16, 8),
    },
    # 各类攻击与段数的攻击力
    'atk_damage': {
        'attack_ground': 9,
    }
}

sheet_event_data = {
    'type': 'event',
    'file_name': 'sprite_00.png',
    'size_pix': 40,
    'size_unit': (4, 4),

    'size_colli': (24,28),
    'type_colli': 'bottom',
    'speed': {
        'speed_walk': 1,
        'speed_jump': -4
    },
    'auto_trigger': False,     # 碰撞不需调查即开始事件
    'active': True,     # 初始化时默认的是否存在。具体是否存在要看存档读取情况。

    # (动画所在行，起始列，从起始列开始共有的列数)
    'status': {
        'idle': (1, 0, 4)
    },
    'event_name': 'template'     # 调用的剧本
}