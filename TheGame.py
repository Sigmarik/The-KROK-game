import pygame
#from random import randint
import time

pygame.init()

FullAnim = True

INF = 1000000001

seed = int(input('Enter game seed --> ')) % INF

def randint(a, b): # Функция рандома. Нужна для возможности использования сидов (подробнее - "https://www.youtube.com/watch?v=FwUsIr5OHFE").
    global seed
    if a >= b:
        return a
    val = sum([int(x) % 7 for x in str(seed)])
    if val != 0:
        seed = ((seed // val) * (val + 13)) % INF
    else:
        seed = INF - 1
    #print(seed)
    return seed % (b - a + 1) + a

def sign(x): # Мат. функция сигнума.
    if x == 0:
        return 0
    return x // abs(x)

def dist(a, b = [0, 0]): # Высчитывает линейное расстояние между точками.
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5

def ImLoad(imname, pix = [0, 0]): # Загружает и возвращает изображение (при этом фон делается прозрачным).
    img = pygame.image.load(imname)
    img.set_colorkey(img.get_at(pix))
    return img

class TGameCell: # Класс стандартной игрофой клетки. Хранит свою картинку, силу и может отрисовывать себя же.
    pos = [0, 0]
    img = pygame.Surface([10, 10])
    damage = 0
    def __init__(self, img, pos, damage = 0): # Создаёт игровую клетку
        self.img = img
        self.pos = pos
        self.damage = damage
    def draw(self, scr): # Рисует клетку в заданных координатах
        scr.blit(self.img, self.pos)

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
            if FullAnim:
                pygame.time.delay(100)

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
            if FullAnim:
                pygame.time.delay(300 // self.damage)

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
            if FullAnim:
                pygame.time.delay(300 // self.damage)

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

class helmet(Item): # Класс шлема. Может перенести игрока в случайную клетку (не занятую скелетом).
    def activate(self, player, enemyes, FSize):# Активирует эффект
        player.health = int(player.health * 1.5)
        player.pos = [randint(0, FSize - 1) * 60, randint(0, FSize - 1) * 60]
        while player.pos in [en.pos for en in enemyes]:
            player.pos = [randint(0, FSize - 1) * 60, randint(0, FSize - 1) * 60]
        player.cell_pos_upd()
class hammer(Item): # Класс молота. Может "ударить" игрока на половину здоровья.
    def activate(self, player, enemyes, FSize): # Активирует эффект
        player.health = int(player.health * 0.5)
class finish(Item): # Класс финиша. Использует некоторые механики артефактов. Завершает игру.
    def activate(self, player, enemyes, FSize): # Активирует эффект (завершает игру)
        pygame.quit()
        print('You win!\n' * 30)
        input('Press [Enter] to quit...')
        exit()
        
class person: # Класс персонажа. Хранит здоровье, картинку и может двигаться.
    pos = []
    cell_pos = [0, 0]
    image = 0
    health = 60
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
        if FullAnim:
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
        
class TGameMech: # Класс игры. Хранит все игровые переменные, константы и т.д. Может запустить игру.:
    field = []
    FSize = 12
    im_lib = [[pygame.image.load('assets/fire1.bmp'), pygame.image.load('assets/fire2.bmp'), pygame.image.load('assets/fire3.bmp')],
              [pygame.image.load('assets/ground1.bmp'), pygame.image.load('assets/ground2.bmp'), pygame.image.load('assets/ground3.bmp')],
              [pygame.image.load('assets/water1.bmp'), pygame.image.load('assets/water2.bmp'), pygame.image.load('assets/water3.bmp')]]
    cells = [TFireCell(im_lib[0], [0, 0], damage = 3)]
    player = person([0, randint(0, FSize - 1) * 60], ImLoad('assets/player.bmp'))
    items = []
    enemyes = []
    board = 0
    collected = []
    max_items = 0
    WIN = False
    def __init__(self): # Создаёт новую игру (при этом не удаляя старую). Генерирует поле, начальные позиции персонажей и т.д.
        self.board = pygame.Surface([self.FSize * 60] * 2)
        for i in range(self.FSize):
            self.field.append([])
            for j in range(self.FSize):
                dmg = randint(1, 3)
                CType = randint(0, 2)
                if CType == 0:
                    cl = TFireCell(self.im_lib[CType][dmg - 1], [i * 60, j * 60], damage = dmg)
                elif CType == 1:
                    cl = TGroundCell(self.im_lib[CType][dmg - 1], [i * 60, j * 60], damage = dmg)
                elif CType == 2:
                    cl = TWaterCell(self.im_lib[CType][dmg - 1], [i * 60, j * 60], damage = dmg)
                self.field[-1].append(cl)
                self.board.blit(cl.img, [i * 60, j * 60])
        EImg = ImLoad('assets/enemy.bmp')
        for i in range(randint(2, 5)):#3):
            self.enemyes.append(enemy([randint(0, self.FSize - 1) * 60, randint(0, self.FSize - 1) * 60], EImg))
        slides = [[ImLoad('assets/TheGreatHelmet1.bmp'), ImLoad('assets/TheGreatHelmet2.bmp'), ImLoad('assets/TheGreatHelmet3.bmp'), ImLoad('assets/TheGreatHelmet2.bmp')],
                  [ImLoad('assets/TheGreatHammer1.bmp'), ImLoad('assets/TheGreatHammer2.bmp'), ImLoad('assets/TheGreatHammer3.bmp'), ImLoad('assets/TheGreatHammer2.bmp')],
                  [ImLoad('assets/finish.bmp')]]
        self.items = [helmet(self.field[randint(0, self.FSize - 1)][randint(1, self.FSize - 1)], slides[0], 0.15),
                      hammer(self.field[randint(0, self.FSize - 1)][randint(1, self.FSize - 1)], slides[1], 0.1),
                      finish(self.field[randint(0, self.FSize - 1)][randint(1, self.FSize - 1)], slides[2], 0.1)]
        self.max_items = len(self.items)
    def start(self): # Начинает созданную игру и ведёт её до конца.
        global FullAnim
        step_count = 0
        KG = True
        scr = pygame.display.set_mode([self.FSize * 60 + 200, self.FSize * 60])
        font = pygame.font.Font('arial.otf', 24)
        while KG:
            step = [0, 0]
            scr.fill([0, 0, 0])
            scr.blit(self.board, [0, 0])
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    KG = False
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_w, pygame.K_UP]:
                        step = [0, -1]
                    if event.key in [pygame.K_s, pygame.K_DOWN]:
                        step = [0, 1]
                    if event.key in [pygame.K_a, pygame.K_LEFT]:
                        step = [-1, 0]
                    if event.key in [pygame.K_d, pygame.K_RIGHT]:
                        step = [1, 0]
                    if event.key in [pygame.K_SPACE]:
                        step = 0
                    if event.key in [pygame.K_f]:
                        FullAnim = not FullAnim
                        print(FullAnim)
            for i, x in enumerate(self.collected):
                scr.blit(x.get_anim_tick(pygame.time.get_ticks() / 1000), [self.FSize * 60 + (i % 2) * 80, 50 + (i // 2) * 60])
            scr.blit(self.board, [0, 0])
            scr.blit(font.render('Health: ' + str(self.player.health), 0, [255, 255, 255]), [self.FSize * 60, 0])
            for it in self.items[::-1]:
                img = it.get_anim_tick(pygame.time.get_ticks() / 1000)
                scr.blit(img, it.par_cell.pos)
                if dist(it.par_cell.pos, self.player.pos) <= 10:
                    self.items.remove(it)
                    self.collected.append(it)
                    it.activate(self.player, self.enemyes, self.FSize)
            scr.blit(self.player.image, self.player.pos)
            for en in self.enemyes:
                scr.blit(en.image, en.pos)
            #for item in items:
            if len(self.collected) == self.max_items and False:
                scr.blit(font.render('You WIN!!!', 0, [255, 0, 0]), [self.FSize * 60, 20])
                self.WIN = True
                for en in self.enemyes:
                    en.image = ImLoad('assets/win.bmp')
            if step == 0 or (step != [0, 0] and (-1 <= self.player.pos[0] + step[0] * 60 <= (self.FSize) * 60 and -1 <= self.player.pos[1] + step[1] * 60 <= (self.FSize) * 60)):
                if step == 0:
                    step = [0, 0]
                step_count += 1
                PPos = self.player.cell_pos
                cl = self.field[PPos[0]][PPos[1]]
                scr.blit(cl.img, cl.pos)
                for it in self.items:
                    img = it.get_anim_tick(pygame.time.get_ticks() / 1000)
                    scr.blit(img, it.par_cell.pos)
                self.player.step([step[0] * 60, step[1] * 60], scr.copy(), self.field, scr)
                if (step_count % 2 == 0 and not self.WIN) or True:
                    for i, enem in enumerate(self.enemyes):
                        OK = True
                        for it in self.items:
                            img = it.get_anim_tick(pygame.time.get_ticks() / 1000)
                            scr.blit(img, it.par_cell.pos)
                        for j, en in enumerate(self.enemyes):
                            if i != j and en.cell_pos == enem.cell_pos:
                                OK = False
                        PPos = enem.cell_pos
                        cl = self.field[PPos[0]][PPos[1]]
                        scr.blit(cl.img, cl.pos)
                        if not OK:
                            scr.blit(enem.image, enem.pos)
                        enem.TStep(self.player, scr.copy(), self.field, scr, static = (step_count % 2 == 0 and not self.WIN))
            pygame.display.update()
        pygame.quit()

game = TGameMech()
game.start()
