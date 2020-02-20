import pygame
from GameCell import *
class TGroundCell(TGameCell): # Клетка земли. В дополнение от родителя проигрывает анимацию.
    TYPE = 'ground'
    def magic(self, scr): # Активирует собственную магию.
        starts = [[self.pos[0] + 30, self.pos[1] + 58]] * self.damage * 2
        for stage in range(3 * self.damage):
            pygame.event.get()
            N = self.damage * 3
            for i, start in enumerate(starts):
                finish = [start[0] + randint(-5, 5), start[1] - 6]
                pygame.draw.line(scr, [randint(0, 75), 120, randint(0, 75)], start, finish, 5)
                starts[i] = finish
            pygame.display.update()
            if self.FullAnim:
                pygame.time.delay(300 // self.damage)
