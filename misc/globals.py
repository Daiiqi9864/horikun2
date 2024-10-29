# 系统
SCREENWIDTH, SCREENHEIGHT = 640, 480
CAPTION = 'horikun 2: return of kanesan'
FPS = 60

# 图像
TILE_SIZE = 32
ITEM_SIZE = 24
TRANSPARENT_COLORKEY = [0,0,255]
ANIME_FRAME = 6

# 角色动作
GRAVITY = 0.2  # 地面的重力加速度：像素/帧
SPD_LIM = 5  # 地面的降落限速：像素/帧

# 地图相关
MAP_LOAD = (1,1)    # 横向加载，纵向加载
MAP_KEY_INIT = 'map_d00'
PLY_POS_INIT = [1568, 192]

# 主菜单UI
WINDOW_STAT = {
    'main_menu': 0,
    'in_game': 1,
    'in_talk': 2,
    'in_select': 3,
    'in_forced': 4,
    'in_menu': 5
}

# 游戏内UI
COLOR_HP_BG, COLOR_HP_FRAME = [200, 0, 0], [50, 0, 0]
PLAYER_HP_X, PLAYER_HP_Y, PLAYER_HP_W, PLAYER_HP_H = 10, 47, 200, 15  # UI血条位置尺寸
COLORS = {
    'title': (170, 200, 100),   # 标题画面，标题
    'title_highlight': (250, 250, 250),     # 标题画面，选项
    'title_normal': (150, 150, 150),
    'menu_highlight': (50, 50, 50),     # 游戏内菜单
    'menu_normal': (100, 100, 100),
    'menu_item': (20, 20, 20),      # 物品栏内物品名与介绍
}


# 菜单UI
MENU_STAT = {
    'menu_template': 0,
    'A0_stat': 1,
    'B0_item': 2,
    'B_1_use_item': 3,
    'B_2_material': 4,
    'B_3_key_item': 5,
    'C0_form': 6,
    'C_1_reallocate': 7,
    'C_2_reallocate': 8,
    'C_3_reallocate': 9,
    'C_4_reallocate': 10,
    'D0_system': 11,
}

# 对话UI
