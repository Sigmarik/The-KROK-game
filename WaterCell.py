import pygame
from GameCell import *
class TWaterCell(TGameCell): # Клетка воды (льда). В дополнение от родителя проигрывает анимацию.
    TYPE = 'water'
    def magic(self, scr): # Активирует собственную магию.
        for stage in range(3 * self.damage):
            pygame.event.get()
            N = self.damage * 3
            start = [self.pos[0] + 30 + randint(-10, 10), self.pos[1] + randint(0, 58)]
            for i in range(N):
                R = randint(0, 255)
                finish = [start[0] + randint(-3, 3) * self.damage, start[1] + randint(-3, 3) * self.damage]
                pygame.draw.line(scr, [R, R, 255], start, finish, 5)
            pygame.display.update()
            if self.FullAnim:
                pygame.time.delay(300 // self.damage)
