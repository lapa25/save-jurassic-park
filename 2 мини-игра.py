import pygame  # импорт библиотек
from random import randint
import os


class Board:  # класс клетчатого поля
    def __init__(self, width, height):  # инициализация с размерами
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.board_1 = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30
        self.lose = False
        self.x = 0

    def set_view(self, left, top, cell_size):  # метод установки размеров
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):  # рисование поля
        x, y = self.left, self.top
        screen.fill((0, 0, 0))
        pygame.draw.polygon(screen, pygame.Color('yellow'), ((50, 10), (80, 10), (80, 30), (65, 45), (50, 30)))
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(screen, pygame.Color('white'), (x, y, self.cell_size, self.cell_size), 1)
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
        for i in range(15):
            i, j = randint(0, self.height - 1), randint(0, self.width - 1)
            while [i, j] in list_walls or (i == 0 and j == 0) or (i == self.height - 1 and j == self.width - 1):
                i, j = randint(0, self.height - 1), randint(0, self.width - 1)
            list_walls.append([i, j])
            self.board[j][i] = 10
        while not self.has_path(0, 0, 9, 9):
            for elem in list_walls:
                self.board[elem[1]][elem[0]] = 0
            list_walls = []
            for i in range(15):
                i, j = randint(0, self.height - 1), randint(0, self.width - 1)
                while [i, j] in list_walls or (i == 0 and j == 0) or (i == self.height - 1 and j == self.width - 1):
                    i, j = randint(0, self.height - 1), randint(0, self.width - 1)
                list_walls.append([i, j])
                self.board[j][i] = 10
        for k in range(3):
            i, j = randint(0, self.height - 1), randint(0, self.width - 1)
            while [i, j] in list_walls:
                i, j = randint(0, self.height - 1), randint(0, self.width - 1)
            self.board_1[j][i] = 12

    def open_cell(self, screen, pos, button):
        x, y = self.get_cell(pos)
        all_sprites2 = pygame.sprite.Group()
        if button == 1:
            if self.board[y][x] != 10:
                sp = [[y, x]]
                was = [[y, x]]
                while len(sp) != 0:
                    y, x = sp[0]
                    count = 0
                    if self.height > y - 1 >= 0 and self.width > x - 1 >= 0 and self.board[y - 1][x - 1] == 10:
                        count += 1
                    if self.height > y - 1 >= 0 and self.width > x >= 0 and self.board[y - 1][x] == 10:
                        count += 1
                    if self.height > y - 1 >= 0 and self.width > x + 1 >= 0 and self.board[y - 1][x + 1] == 10:
                        count += 1
                    if self.height > y >= 0 and self.width > x - 1 >= 0 and self.board[y][x - 1] == 10:
                        count += 1
                    if self.height > y >= 0 and self.width > x + 1 >= 0 and self.board[y][x + 1] == 10:
                        count += 1
                    if self.height > y + 1 >= 0 and self.width > x - 1 >= 0 and self.board[y + 1][x - 1] == 10:
                        count += 1
                    if self.height > y + 1 >= 0 and self.width > x >= 0 and self.board[y + 1][x] == 10:
                        count += 1
                    if self.height > y + 1 >= 0 and self.width > x + 1 >= 0 and self.board[y + 1][x + 1] == 10:
                        count += 1
                    self.board[y][x] = count
                    if self.board_1[y][x] != 12:
                        self.board_1[y][x] = 2
                    if self.board_1[y][x] != 1:
                        font = pygame.font.Font(None, 50)
                        text = font.render(str(count), True, pygame.Color('green'))
                        screen.blit(text, ((x * self.cell_size + self.left + self.cell_size // 4),
                                           (y * self.cell_size + self.top)))
                    if self.board_1[y][x] == 12:
                        sprite2 = pygame.sprite.Sprite()
                        sprite2.image = load_image('ключ.png')
                        sprite2.rect = sprite2.image.get_rect()
                        sprite2.rect.y = 10
                        if self.x == 0:
                            sprite2.rect.x = 100
                            self.x = 100
                        else:
                            self.x += 50
                            sprite2.rect.x = self.x
                        all_sprites2.add(sprite2)
                    if count == 0:
                        if self.height > y - 1 >= 0 and self.width > x - 1 >= 0 and [y - 1, x - 1] not in was:
                            sp.append([y - 1, x - 1])
                            was.append([y - 1, x - 1])
                        if self.height > y - 1 >= 0 and self.width > x >= 0 and [y - 1, x] not in was:
                            sp.append([y - 1, x])
                            was.append([y - 1, x])
                        if self.height > y - 1 >= 0 and self.width > x + 1 >= 0 and [y - 1, x + 1] not in was:
                            sp.append([y - 1, x + 1])
                            was.append([y - 1, x + 1])
                        if self.height > y >= 0 and self.width > x - 1 >= 0 and [y, x - 1] not in was:
                            sp.append([y, x - 1])
                            was.append([y, x - 1])
                        if self.height > y >= 0 and self.width > x + 1 >= 0 and [y, x + 1] not in was:
                            sp.append([y, x + 1])
                            was.append([y, x + 1])
                        if self.height > y + 1 >= 0 and self.width > x - 1 >= 0 and [y + 1, x - 1] not in was:
                            sp.append([y + 1, x - 1])
                            was.append([y + 1, x - 1])
                        if self.height > y + 1 >= 0 and self.width > x >= 0 and [y + 1, x] not in was:
                            sp.append([y + 1, x])
                            was.append([y + 1, x])
                        if self.height > y + 1 >= 0 and self.width > x + 1 >= 0 and [y + 1, x + 1] not in was:
                            sp.append([y + 1, x + 1])
                            was.append([y + 1, x + 1])
                    sp = sp[1:]
            else:
                return 'lose'
        elif button == 3:
            if self.board_1[y][x] == 0:
                self.board_1[y][x] = 1
                pygame.draw.rect(screen, pygame.Color('blue'),
                                 (x * self.cell_size + self.top + 2, y * self.cell_size + self.left + 2,
                                  self.cell_size - 4, self.cell_size - 4))
            else:
                self.board_1[y][x] = 0
                pygame.draw.rect(screen, pygame.Color('black'),
                                 (x * self.cell_size + self.top + 2, y * self.cell_size + self.left + 2,
                                  self.cell_size - 4, self.cell_size - 4))
        was = False
        for a in range(len(self.board_1)):
            for b in range(len(self.board_1[a])):
                if self.board_1[a][b] == 0:
                    was = True
                    break
        if not was:
            font = pygame.font.Font(None, 50)
            text = font.render('Победа!', True, pygame.Color('yellow'))
            screen.blit(text, (300, 15))
        all_sprites2.draw(screen)


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
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
    sprite.image = load_image('begin_лабиринт.png')  # подгрузка начального экрана
    sprite.rect = sprite.image.get_rect()
    sprite.rect.y = 0  # настройка параметров
    sprite.rect.x = 0
    all_sprites.add(sprite)
    running = True
    begin = True
    make_bombs_keys = False
    numbers = False
    while running:  # игровой цикл
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:  # переход к игре при нажатии пробела
                if event.key == pygame.K_SPACE and begin:
                    begin = False
                    make_bombs_keys = True
            if event.type == pygame.MOUSEBUTTONDOWN and not make_bombs_keys:
                if board.get_cell(event.pos) is not None:
                    res = board.open_cell(screen, event.pos, event.button)
                    if res == 'lose':
                        return 'lose'
                    numbers = True
        if begin:
            all_sprites.draw(screen)
        else:
            if make_bombs_keys:
                board = Game(10, 10)
                board.set_view(50, 50, 40)
                board.make_maze()
            if not numbers:
                board.render(screen)
            make_bombs_keys = False
        pygame.display.flip()


result = do()
if result == 'lose':
    pygame.init()
    size1 = width1, height1 = 500, 500
    screen1 = pygame.display.set_mode(size1)
    pygame.display.set_caption('Лабиринт')
    all_sprites1 = pygame.sprite.Group()
    sprite1 = pygame.sprite.Sprite()
    sprite1.image = load_image('end_лабиринт.png')
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
