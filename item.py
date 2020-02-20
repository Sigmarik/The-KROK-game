import pygame
from GameCell import *
class Item: # Класс артефакта. Хранит свою анимацию и может возвращать кадр в зависимости от времени.
    par_cell = TGameCell(pygame.Surface([10, 10]), [0, 0])
    slides = []
    delta_frame = 0
    def __init__(self, par_cell, slides, delta_frame = 1): # Создаёт артефакт.
        self.par_cell = par_cell
        self.slides = slides.copy()
        self.delta_frame = delta_frame
    def get_anim_tick(self, tm): # Возвращает текущий кадр анимации
        index = (tm // self.delta_frame) % len(self.slides)
        return self.slides[int(index)]
