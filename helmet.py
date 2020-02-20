import pygame
from item import *
class helmet(Item): # Класс шлема. Может перенести игрока в случайную клетку (не занятую скелетом).
    def activate(self, player, enemyes, FSize):# Активирует эффект
        player.health = int(player.health * 1.5)
        player.pos = [randint(0, FSize - 1) * 60, randint(0, FSize - 1) * 60]
        while player.pos in [en.pos for en in enemyes]:
            player.pos = [randint(0, FSize - 1) * 60, randint(0, FSize - 1) * 60]
        player.cell_pos_upd()
