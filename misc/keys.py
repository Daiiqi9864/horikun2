import pygame


# 因为冲刺键是左shift，测试时一定切输入法！
class KeyManager:
    def __init__(self):
        self.key_left = pygame.K_a
        self.key_right = pygame.K_d
        self.key_down = pygame.K_s
        self.key_up = pygame.K_w
        self.key_jump = pygame.K_SPACE
        self.key_attack = pygame.K_z
        self.key_interact = pygame.K_RETURN
        self.key_dash = pygame.K_LSHIFT
        self.key_exit = pygame.K_ESCAPE
