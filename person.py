from standart import *
import pygame
class person: # Класс персонажа. Хранит здоровье, картинку и может двигаться.
    pos = []
    cell_pos = [0, 0]
    image = 0
    health = 60
    FullAnim = True
    def __init__(self, pos, img): # Создаёт персонажа и задаёт начальные параметры
        self.pos = pos
        self.image = img
        self.cell_pos = [self.pos[0] // 60, self.pos[1] // 60]
    def cell_pos_upd(self): # Обновляет клеточную позицию игрока.
        self.cell_pos = [self.pos[0] // 60, self.pos[1] // 60]
    def death(self, scr, fld_arr): # Проигрывает смерть персонажа и конец игры.
        global FullAnim
        FullAnim = False
        self.image = ImLoad('assets/Graveyard.bmp')
        scr.blit(self.image, [int(x) for x in self.pos])
        for i in range(len(fld_arr)):
            for j in range(len(fld_arr[i])):
                fld_arr[i][j].magic(scr)
        KG = True
        while KG:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    KG = False
        pygame.quit()
        exit()
    def step(self, stp, fld, fld_arr, scr): # Ведёт персонажа в заданном направлении
        if self.FullAnim:
            N = 100
        else:
            N = 1
        self.cell_pos[0] += stp[0] // 60
        self.cell_pos[1] += stp[1] // 60
        #print(self.cell_pos)
        for i in range(N):
            pygame.event.get()
            scr.blit(fld, [0, 0])
            self.pos[0] += stp[0] / N
            self.pos[1] += stp[1] / N
            scr.blit(self.image, [int(x) for x in self.pos])
            pygame.display.update()
            pygame.time.delay(10)
        cell = fld_arr[self.cell_pos[0]][self.cell_pos[1]]
        cell.magic(scr)
        if cell.TYPE == 'fire':
            self.health += cell.damage * 5
        else:
            self.health -= cell.damage * 5
        if self.health <= 0:
            self.death(scr, fld_arr)
