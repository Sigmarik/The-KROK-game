import pygame
from GameCell import *
class TFireCell(TGameCell): # Клетка огня. В дополнение от родителя проигрывает анимацию.
    TYPE = 'fire'
    def magic_old(self, scr): # Старая версия анимации. Если всё же хотите её увидеть, то можете назвать её "magic" (без кавычек) и переназвать оригинальную функцию.
        for stage in range(9):
            pygame.event.get()
            for i in range(self.damage * 90):
                R = randint(100, 255)
                scr.set_at([self.pos[0] + randint(1, self.img.get_width() - 1), self.pos[1] + randint(1, self.img.get_height() - 1)], [R + randint(0, 255 - R), R, 0])
            pygame.display.update()
            pygame.time.delay(100)
    def magic(self, scr): # Активирует собственную магию.
        for stage in range(9):
            pygame.event.get()
            N = self.damage * 3
            for i in range(N):
                R = randint(100, 255)
                start = [self.pos[0] + 30 + randint(-10, 10), self.pos[1] + 60 - 2]
                finish = [start[0] + randint(-5, 5), start[1] - randint(5, 15) * self.damage]
                pygame.draw.line(scr, [R + randint(0, 255 - R), R, 0], start, finish, 5)
                #pygame.draw.line(scr, [R + randint(0, 255 - R), R, 0], [self.pos[0] + randint(0, 60), self.pos[1] + 60 - i * 60 / N], [self.pos[0] + randint(0, 60), self.pos[1] + 60 - i * 60 / N - randint(0, 60 // N)])
            pygame.display.update()
            if self.FullAnim:
                pygame.time.delay(100)
