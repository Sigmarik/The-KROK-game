import pygame
from item import *
class hammer(Item): # Класс молота. Может "ударить" игрока на половину здоровья.
    def activate(self, player, enemyes, FSize): # Активирует эффект
        player.health = int(player.health * 0.5)
