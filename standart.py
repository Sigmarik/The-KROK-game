import pygame
import random
seed = random.randint(0, 100)
INF = 9876546789
def __init__(seed):
    self.seed = seed
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
