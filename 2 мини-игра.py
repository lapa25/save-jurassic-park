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
                    pygame.draw.rect(screen, pygame.Color('red'),
                                     (x + 2, y + 2, self.cell_size - 4, self.cell_size - 4))
                x += self.cell_size
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
    def __init__(self, width, height):
        super().__init__(width, height)

    def bombs_keys(self, count1, count2):
        sp = []
        for i in range(count1 + count2):
            i, j = randint(0, self.height - 1), randint(0, self.width - 1)
            while [i, j] in sp:
                i, j = randint(0, self.height - 1), randint(0, self.width - 1)
            sp.append([i, j])
        return sp[:count1], sp[count1:]

    def has_path(self, x1, y1, x2, y2):
        sp = [[x1, y1, x1, y1]]
        was1 = False
        was = [[x1, y1, x1, y1]]
        x, y = sp[0][2], sp[0][3]
        while x != x2 or y != y2:
            if x + 1 < self.width and self.board[y][x + 1] == 0 and [x, y, x + 1, y] not in was:
                sp.append([x, y, x + 1, y])
                was.append([x, y, x + 1, y])
                if x + 1 == x2 and y == y2:
                    break
            if x - 1 >= 0 and self.board[y][x - 1] == 0 and [x, y, x - 1, y] not in was:
                sp.append([x, y, x - 1, y])
                was.append([x, y, x - 1, y])
                if x - 1 == x2 and y == y2:
                    break
            if y + 1 < self.height and self.board[y + 1][x] == 0 and [x, y, x, y + 1] not in was:
                sp.append([x, y, x, y + 1])
                was.append([x, y, x, y + 1])
                if x == x2 and y + 1 == y2:
                    break
            if y - 1 >= 0 and self.board[y - 1][x] == 0 and [x, y, x, y - 1] not in was:
                sp.append([x, y, x, y - 1])
                was.append([x, y, x, y - 1])
                if x == x2 and y + 1 == y2:
                    break
            sp = sp[1:]
            if len(sp) == 0:
                was1 = True
                break
            x, y = sp[0][2], sp[0][3]
        if was1:
            return False
        was = was[::-1]
        way = [[x2, y2]]
        for elem in was:
            if way[-1][0] == elem[2] and way[-1][1] == elem[3]:
                if [elem[0], elem[1]] not in way:
                    way.append([elem[0], elem[1]])
        return True

    def make_maze(self):
        list_walls = []
        for i in range(30):
            i, j = randint(0, self.height - 1), randint(0, self.width - 1)
            while [i, j] in list_walls or (i == 0 and j == 0) or (i == self.height - 1 and j == self.width - 1):
                i, j = randint(0, self.height - 1), randint(0, self.width - 1)
            list_walls.append([i, j])
            self.board[j][i] = 1
        while not self.has_path(0, 0, 9, 9):
            for elem in list_walls:
                self.board[elem[1]][elem[0]] = 0
            list_walls = []
            for i in range(30):
                i, j = randint(0, self.height - 1), randint(0, self.width - 1)
                while [i, j] in list_walls or (i == 0 and j == 0) or (i == self.height - 1 and j == self.width - 1):
                    i, j = randint(0, self.height - 1), randint(0, self.width - 1)
                list_walls.append([i, j])
                self.board[j][i] = 1


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


def do():
    pygame.init()  # инициализация экрана
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Лабиринт')
    all_sprites = pygame.sprite.Group()
    sprite = pygame.sprite.Sprite()
    sprite.image = load_image('лабиринт.png')  # подгрузка начального экрана
    sprite.rect = sprite.image.get_rect()
    sprite.rect.y = 0  # настройка параметров
    sprite.rect.x = 0
    all_sprites.add(sprite)
    list_bombs = list()
    list_keys = list()
    running = True
    begin = True
    make_bombs_keys = False
    while running:  # игровой цикл
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:  # переход к игре при нажатии пробела
                if event.key == pygame.K_SPACE and begin:
                    begin = False
                    make_bombs_keys = True
        if begin:
            all_sprites.draw(screen)
        else:
            if make_bombs_keys:
                board = Game(10, 10)
                board.set_view(50, 50, 40)
                board.make_maze()
                sprite1 = pygame.sprite.Sprite()
                sprite1.image = load_image('стрелка.png')  # подгрузка начального экрана
                sprite1.rect = sprite1.image.get_rect()
                sprite1.rect.y = 0  # настройка параметров
                sprite1.rect.x = 0
                all_sprites.add(sprite1)
                all_sprites.draw(screen)
            board.render(screen)
            make_bombs_keys = False
        pygame.display.flip()


do()
