import pygame
from standart import *
class TGameCell: # Класс стандартной игрофой клетки. Хранит свою картинку, силу и может отрисовывать себя же.
    pos = [0, 0]
    img = pygame.Surface([10, 10])
    damage = 0
    FullAnim = True
    def __init__(self, img, pos, damage = 0): # Создаёт игровую клетку
        self.img = img
        self.pos = pos
        self.damage = damage
    def draw(self, scr): # Рисует клетку в заданных координатах
        scr.blit(self.img, self.pos)
