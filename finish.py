import pygame
from item import *
class finish(Item): # Класс финиша. Использует некоторые механики артефактов. Завершает игру.
    def activate(self, player, enemyes, FSize): # Активирует эффект (завершает игру)
        pygame.quit()
        print('You win!\n' * 30)
        input('Press [Enter] to quit...')
        exit()
