from standart import *
import pygame
from person import *
class enemy(person): # Класс врага. Может "догонять" другого персонажа и реализует собственное бессмертие.
    def TStep(self, target, fld, fld_arr, scr, static = False): # Определяет направление шага и вызывает step на себя же.
        #print(target.cell_pos)
        for _ in range(1 if not static else 0):
            delta = [target.cell_pos[0] - self.cell_pos[0], target.cell_pos[1] - self.cell_pos[1]]
            if delta != [0, 0]:
                R = randint(0, 1)
                #print(delta)
                self.health = 200
                if abs(delta[0]) > abs(delta[1]) or (delta[0] == delta[1] and R == 0):
                    self.step([sign(delta[0]) * 60, 0], fld, fld_arr, scr)
                else:#elif abs(delta[0]) < abs(delta[1]) or (delta[0] == delta[1] and R == 1):
                    self.step([0, sign(delta[1]) * 60], fld, fld_arr, scr)
        delta = [target.cell_pos[0] - self.cell_pos[0], target.cell_pos[1] - self.cell_pos[1]]
        if delta == [0, 0]:
            target.death(scr, fld_arr)
