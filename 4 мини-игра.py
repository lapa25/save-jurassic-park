import pygame  # импорт библиотек
from random import randint
import sys
import os


class Board:  # класс клетчатого поля
    def __init__(self, width, height):  # инициализация с размерами
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def set_view(self, left, top, cell_size):  # метод установки размеров
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):  # рисование поля
        x, y = self.left, self.top
        screen.fill((0, 0, 0))
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(screen, pygame.Color('white'), (x, y, self.cell_size, self.cell_size), 1)
                if self.board[i][j] == 1:
                    pygame.draw.rect(screen, pygame.Color('green'), (x + 2, y + 2,
                                                                     self.cell_size - 4, self.cell_size - 4))
                if self.board[i][j] == 2:
                    pygame.draw.rect(screen, pygame.Color('red'), (x + 2, y + 2,
                                                                   self.cell_size - 4, self.cell_size - 4))
                x += self.cell_size

            font = pygame.font.Font(None, 40)  # надпись с номером уровня
            text = font.render(f"{self.level} уровень", False, (100, 255, 100))
            text_x = 185
            text_y = 25
            text_w = text.get_width()
            text_h = text.get_height()
            screen.blit(text, (text_x, text_y))
            pygame.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10,
                                                   text_w + 20, text_h + 20), 1)
            x = self.left
            y += self.cell_size

    def get_cell(self, mouse_pos):  # определение номера клети по координатам
        x1 = (self.width * self.cell_size) + self.left
        y1 = (self.height * self.cell_size) + self.top
        if self.left > mouse_pos[0] or mouse_pos[0] > x1 or self.top > mouse_pos[1] or mouse_pos[1] > y1:
            return
        else:
            return (mouse_pos[0] - self.left) // self.cell_size, \
                   (mouse_pos[1] - self.top) // self.cell_size


class Game(Board):  # класс игры, унаследованный от класса поля
    def __init__(self, width, height, level):
        super().__init__(width, height)
        self.level = level

    def signals(self, count_signals):  # метод, генерирующий сигналы
        sp = []
        for i in range(count_signals):
            i, j = randint(0, self.height - 1), randint(0, self.width - 1)
            while [i, j] in sp:
                i, j = randint(0, self.height - 1), randint(0, self.width - 1)
            sp.append([i, j])
        return sp


def load_image(name, colorkey=None):  # метод для загрузки изображений
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def do():  # функция, создающая уровень
    pygame.init()  # инициализация экрана
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Сигнал о помощи')
    all_sprites = pygame.sprite.Group()
    sprite = pygame.sprite.Sprite()
    sprite.image = load_image('комната связи 1.png')  # подгрузка начального экрана
    sprite.rect = sprite.image.get_rect()
    sprite.rect.y = - 300  # настройка параметров
    sprite.rect.x = 0
    left, top = 125, 125
    count = 5
    count1 = 0
    index = 0
    level = 1
    list_signals = list()
    list_light = list()
    all_sprites.add(sprite)
    running = True
    begin = True
    take_signals = False
    remember = False
    clock = pygame.time.Clock()
    while running:  # игровой цикл
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return 'exit'
            if event.type == pygame.KEYDOWN:  # переход к игре при нажатии пробела
                if event.key == pygame.K_SPACE:
                    begin = False
                    take_signals = True
            if event.type == pygame.MOUSEBUTTONDOWN and remember:  # запоминание позиций нажатых клеток
                if board.get_cell(event.pos) != None:
                    x, y = board.get_cell(event.pos)
                    if list_signals[count1][0] == y and list_signals[count1][1] == x:
                        if len(list_light) != 0:
                            list_light = list_light[1:]
                        list_light.append([(y, x), 1])
                    else:
                        if len(list_light) != 0:
                            list_light = list_light[1:]
                        list_light.append([(y, x), 2])
                    count1 += 1
        if sprite.rect.y < -1:  # выезд пролога к игре
            sprite.rect.y += clock.tick() / 1000
            screen.fill(pygame.Color("black"))
        else:
            sprite.rect.y = 0
        if begin:
            all_sprites.draw(screen)
        else:  # рисоввание поля
            board = Game(count, count, level)
            board.set_view(left, top, 50)
            board.render(screen)
            if take_signals:
                list_signals = board.signals(count)
            take_signals = False
        if len(list_signals) != 0 and index < len(list_signals):  # рисование рандомных сигналов
            board.board[list_signals[index][0]][list_signals[index][1]] = 1
            board.render(screen)
            clock.tick(1)
            board.board[list_signals[index][0]][list_signals[index][1]] = 0
            index += 1
        elif index == len(list_signals) and index != 0:
            clock.tick(1)
            index += 1
            remember = True
        if len(list_light) != 0:  # показ правильности нажатых клеток
            board.board[list_light[0][0][0]][list_light[0][0][1]] = list_light[0][1]
            board.render(screen)
            board.board[list_light[0][0][0]][list_light[0][0][1]] = 0
            if list_light[0][1] == 2:  # окончание при ошибки
                return 'mistake'
        if count1 == len(list_signals) and count1 != 0:  # настройки следующего уровня
            list_signals = []
            count += 1
            count1 = 0
            level += 1
            index = 0
            left, top = left - 25, top - 25
            list_light = []
            take_signals = True
            remember = False
            board = Game(count, count, level)
            board.set_view(left, top, 50)
            board.render(screen)
            if take_signals:
                clock.tick(1)
                list_signals = board.signals(count)
            if level == 4:  # окончание
                return
        pygame.display.flip()


mistake = 0
make = do()
while make == 'mistake':  # счет ошибок и различные исходы в соответствии с этим
    mistake += 1
    pygame.init()
    size1 = width1, height1 = 500, 500
    screen1 = pygame.display.set_mode(size1)
    pygame.display.set_caption('Сигнал о помощи')
    all_sprites1 = pygame.sprite.Group()
    sprite1 = pygame.sprite.Sprite()
    sprite1.image = load_image('end3.png')
    sprite1.rect = sprite1.image.get_rect()
    sprite1.rect.y = 0
    sprite1.rect.x = 0
    all_sprites1.add(sprite1)
    clock1 = pygame.time.Clock()
    running1 = True
    while running1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running1 = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running1 = False
        all_sprites1.draw(screen1)
        pygame.display.flip()
    if mistake == 3:
        pygame.init()
        size1 = width1, height1 = 500, 500
        screen1 = pygame.display.set_mode(size1)
        pygame.display.set_caption('Сигнал о помощи')
        all_sprites1 = pygame.sprite.Group()
        sprite1 = pygame.sprite.Sprite()
        sprite1.image = load_image('end2.png')
        sprite1.rect = sprite1.image.get_rect()
        sprite1.rect.y = 0
        sprite1.rect.x = 0
        all_sprites1.add(sprite1)
        clock1 = pygame.time.Clock()
        running1 = True
        while running1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running1 = False
            all_sprites1.draw(screen1)
            pygame.display.flip()
        break
    make = do()
if make == None:
    pygame.init()
    size1 = width1, height1 = 500, 500
    screen1 = pygame.display.set_mode(size1)
    pygame.display.set_caption('Сигнал о помощи')
    all_sprites1 = pygame.sprite.Group()
    sprite1 = pygame.sprite.Sprite()
    sprite1.image = load_image('end1.png')
    sprite1.rect = sprite1.image.get_rect()
    sprite1.rect.y = 0
    sprite1.rect.x = 0
    all_sprites1.add(sprite1)
    clock1 = pygame.time.Clock()
    running1 = True
    while running1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running1 = False
        all_sprites1.draw(screen1)
        pygame.display.flip()
