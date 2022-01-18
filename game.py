import pygame  # импорт библиотек
from random import randint
import sys
import os
from random import randrange


def load_image(name, colorkey=None):  # функция для загрузки изображений
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f'Файл с изображением {name} не найден.')
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class BoardFirstGame:
    def __init__(self, width, height):  # икласс клетчатого поля для первой мини игры
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30
        self.coords = []

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        left = self.left
        top = self.top
        for i in range(self.height):
            for k in range(self.width):
                if (left, top) not in self.coords:
                    self.coords.append((left, top))
                left += self.cell_size
            top += self.cell_size
            left = self.left
        top = self.top

    def get_cell(self, mouse_pos):  # получение координаты клетки
        for i in self.coords:
            if (0 <= mouse_pos[0] - i[0] <= self.cell_size) and (0 <= mouse_pos[1] - i[1] <= self.cell_size):
                return i


class BoardSecondGame:  # класс клетчатого поля для второй мини игры
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


class BoardFourthGame:  # класс клетчатого поля для четвертой мини игры
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


class Electro(pygame.sprite.Sprite):  # далее идут классы для спрайтов первой мини игры
    image_down = load_image('electricity_down.png')  # класс для спрайта электрощитка
    image_left = load_image('electricity_left.png')
    image_up = load_image('electricity_up.png')
    image_right = load_image('electricity_right.png')

    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = Electro.image_down
        self.rect = self.image.get_rect()
        self.rect.x = x + ((133 // 2) - (self.rect.width // 2))
        self.rect.y = y + (133 - self.rect.height)
        self.x = x
        self.y = y
        self.now = 'down'

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            screen.fill((202, 196, 176))
            if self.now == 'down':
                self.image = self.image_left
                self.rect = self.image.get_rect()
                self.rect.x = self.x
                self.rect.y = self.y + ((133 - self.rect.height) // 2)
                self.now = 'left'
            elif self.now == 'left':
                self.image = self.image_up
                self.rect = self.image.get_rect()
                if level == 3:
                    self.rect.x = self.x + ((133 // 2) - (self.rect.width // 2)) + 1
                else:
                    self.rect.x = self.x + ((133 // 2) - (self.rect.width // 2))
                self.rect.y = self.y
                self.now = 'up'
            elif self.now == 'up':
                self.image = self.image_right
                self.rect = self.image.get_rect()
                self.rect.x = self.x + (133 - self.rect.width)
                self.rect.y = self.y + ((133 - self.rect.height) // 2)
                self.now = 'right'
            elif self.now == 'right':
                self.image = self.image_down
                self.rect = self.image.get_rect()
                self.rect.x = self.x + ((133 // 2) - (self.rect.width // 2))
                self.rect.y = self.y + (133 - self.rect.height)
                self.now = 'down'

    def is_now(self):
        return self.now


class Straight(pygame.sprite.Sprite):  # класс для спрайта прямого провода
    g_image = load_image('straight_gorizont.png')
    v_image = load_image('straight_vertical.png')

    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = Straight.v_image
        self.rect = self.image.get_rect()
        self.rect.x = x + ((133 - self.rect.width) // 2) + 1
        self.rect.y = y
        self.x = x
        self.y = y
        self.now = 'vertical'

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            screen.fill((202, 196, 176))
            if self.now == 'vertical':
                self.image = self.g_image
                self.rect = self.image.get_rect()
                self.rect.x = self.x
                self.rect.y = self.y + ((133 - self.rect.height) // 2)
                self.now = 'gorizont'
            elif self.now == 'gorizont':
                self.image = self.v_image
                self.rect = self.image.get_rect()
                self.rect.x = self.x + ((133 - self.rect.width) // 2) + 1
                self.rect.y = self.y
                self.now = 'vertical'

    def is_now(self):
        return self.now


class Corner(pygame.sprite.Sprite):  # класс для спрайта углового провода
    image_down = load_image('corner_down.png')
    image_left = load_image('corner_left.png')
    image_up = load_image('corner_up.png')
    image_right = load_image('corner_right.png')

    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = Corner.image_down
        self.rect = self.image.get_rect()
        if level == 1:
            self.rect.x = x
            self.rect.y = y + (133 - self.rect.height)
        elif level == 2:
            self.rect.x = x - 1
            self.rect.y = y + (133 - self.rect.height) + 1
        elif level == 3:
            self.rect.x = x
            self.rect.y = y + (133 - self.rect.height)
        self.x = x
        self.y = y
        self.now = 'down'

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            screen.fill((202, 196, 176))
            if self.now == 'down':
                self.image = self.image_left
                self.rect = self.image.get_rect()
                self.rect.x = self.x
                if level == 1:
                    self.rect.y = self.y
                elif level == 2:
                    self.rect.y = self.y - 1
                elif level == 3:
                    self.rect.y = self.y
                self.now = 'left'
            elif self.now == 'left':
                self.image = self.image_up
                self.rect = self.image.get_rect()
                self.rect.x = self.x + (133 - self.rect.width)
                self.rect.y = self.y - 1
                self.now = 'up'
            elif self.now == 'up':
                self.image = self.image_right
                self.rect = self.image.get_rect()
                if level == 1:
                    self.rect.x = self.x + (133 - self.rect.width) + 2
                elif level == 2:
                    self.rect.x = self.x + (133 - self.rect.width) + 1
                elif level == 3:
                    self.rect.x = self.x + (133 - self.rect.width) + 2
                self.rect.y = self.y + (133 - self.rect.height) + 1
                self.now = 'right'
            elif self.now == 'right':
                self.image = self.image_down
                self.rect = self.image.get_rect()
                if level == 1:
                    self.rect.x = self.x
                    self.rect.y = self.y + (133 - self.rect.height)
                elif level == 2:
                    self.rect.x = self.x - 1
                    self.rect.y = self.y + (133 - self.rect.height) + 1
                elif level == 3:
                    self.rect.x = self.x
                    self.rect.y = self.y + (133 - self.rect.height)
                self.now = 'down'

    def is_now(self):
        return self.now


class T(pygame.sprite.Sprite):  # класс для спрайта разветвляющегося провода
    image_down = load_image('t_down.png')
    image_left = load_image('t_left.png')
    image_up = load_image('t_up.png')
    image_right = load_image('t_right.png')

    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = T.image_down
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y + (133 - self.rect.height) + 1
        self.x = x
        self.y = y
        self.now = 'down'

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            screen.fill((202, 196, 176))
            if self.now == 'down':
                self.image = self.image_left
                self.rect = self.image.get_rect()
                self.rect.x = self.x
                self.rect.y = self.y - 1
                self.now = 'left'
            elif self.now == 'left':
                self.image = self.image_up
                self.rect = self.image.get_rect()
                self.rect.x = self.x
                self.rect.y = self.y - 1
                self.now = 'up'
            elif self.now == 'up':
                self.image = self.image_right
                self.rect = self.image.get_rect()
                self.rect.x = self.x + (133 - self.rect.width) + 2
                self.rect.y = self.y - 1
                self.now = 'right'
            elif self.now == 'right':
                self.image = load_image('t_down.png')
                self.rect = self.image.get_rect()
                self.rect.x = self.x
                self.rect.y = self.y + (133 - self.rect.height) + 1
                self.now = 'down'

    def is_now(self):
        return self.now


class Lamp(pygame.sprite.Sprite):  # класс для спрайта лампочки
    image_left_off = load_image('lamp_off_left.png')
    image_right_off = load_image('lamp_off_right.png')
    image_left_on = load_image('lamp_on_left.png')
    image_right_on = load_image('lamp_on_right.png')
    image_up_off = load_image('lamp_off_up.png')
    image_down_off = load_image('lamp_off_down.png')
    image_up_on = load_image('lamp_on_up.png')
    image_down_on = load_image('lamp_on_down.png')

    def __init__(self, x, y, rotate, *group):
        super().__init__(*group)
        if rotate == 'left':
            self.image = self.image_left_off
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y + ((133 - self.rect.height) // 2) - 1
        elif rotate == 'right' or rotate == 'right2':
            self.image = self.image_right_off
            self.rect = self.image.get_rect()
            self.rect.x = x + (133 - self.rect.width)
            self.rect.y = y + ((133 - self.rect.height) // 2) - 1
        elif rotate == 'up' or rotate == 'up1' or rotate == 'up2':
            self.image = self.image_up_off
            self.rect = self.image.get_rect()
            if level == 3:
                self.rect.x = x + ((133 - self.rect.width) // 2) + 1
            else:
                self.rect.x = x + ((133 - self.rect.width) // 2)
            self.rect.y = y
        elif rotate == 'down':
            self.image = self.image_down_off
            self.rect = self.image.get_rect()
            if level == 3:
                self.rect.x = x + ((133 - self.rect.width) // 2) + 1
            else:
                self.rect.x = x + ((133 - self.rect.width) // 2)
            self.rect.y = y + (133 - self.rect.height)
        self.x = x
        self.y = y
        self.now = rotate
        self.on = False

    def update(self, *args):  # здесь определена логика для загорания лампочек на каждом уровне
        if level == 1:
            if self.now == 'right':
                if e1.is_now() == 'left' and s1.is_now() == 'gorizont' \
                        and (t1.is_now() == 'up' or t1.is_now() == 'down'):
                    self.image = self.image_right_on
                    self.on = True
                else:
                    self.image = self.image_right_off
                    self.on = False
            if self.now == 'left':
                if e1.is_now() == 'left' and s1.is_now() == 'gorizont' and t1.is_now() == 'up' and c1.is_now() == 'right' \
                        and s2.is_now() == 'gorizont' and s3.is_now() == 'gorizont':
                    self.image = self.image_left_on
                    self.on = True
                else:
                    self.image = self.image_left_off
                    self.on = False
        if level == 2:
            if self.now == 'right':
                if e2.is_now() == 'up' and c2.is_now() == 'down' and t2.is_now() == 'down' and s4.is_now() == 'vertical' \
                        and (t3.is_now() == 'up' or t3.is_now() == 'left'):
                    self.image = self.image_right_on
                    self.on = True
                else:
                    self.image = self.image_right_off
                    self.on = False
            elif self.now == 'left':
                if e2.is_now() == 'up' and c2.is_now() == 'down' and t2.is_now() == 'down' and s4.is_now() == 'vertical' \
                        and (t3.is_now() == 'up' or t3.is_now() == 'right'):
                    self.image = self.image_left_on
                    self.on = True
                else:
                    self.image = self.image_left_off
                    self.on = False
            if self.now == 'up':
                if e2.is_now() == 'up' and c2.is_now() == 'down' and (t2.is_now() == 'up' or t2.is_now() == 'down') \
                        and c3.is_now() == 'right':
                    self.image = self.image_up_on
                    self.on = True
                else:
                    self.image = self.image_up_off
                    self.on = False
        if level == 3:
            if self.now == 'right':
                if e_1.is_now() == 'left' and (t_2.is_now() == 'down' or t_2.is_now() == 'up') \
                        and (t_1.is_now() == 'up' or t_1.is_now() == 'down'):
                    self.image = self.image_right_on
                    self.on = True
                else:
                    self.image = self.image_right_off
                    self.on = False
            if self.now == 'left':
                if e_1.is_now() == 'left' and (
                        t_2.is_now() == 'down' or t_2.is_now() == 'up') and t_1.is_now() == 'up' and \
                        (
                                t_3.is_now() == 'down' or t_3.is_now() == 'right') and s_2.is_now() == 'gorizont' and s_3.is_now() == 'gorizont':
                    self.image = self.image_left_on
                    self.on = True
                else:
                    self.image = self.image_left_off
                    self.on = False
            if self.now == 'up':
                if e_1.is_now() == 'left' and t_2.is_now() == 'down':
                    self.image = self.image_up_on
                    self.on = True
                else:
                    self.image = self.image_up_off
                    self.on = False
            if self.now == 'right2':
                if e_1.is_now() == 'left' and (t_1.is_now() == 'up' or t_1.is_now() == 'right') \
                        and (t_3.is_now() == 'down' or t_3.is_now() == 'left'):
                    self.image = self.image_right_on
                    self.on = True
                else:
                    self.image = self.image_right_off
                    self.on = False

    def is_on(self):  # метод возвращает: горит лампочка или нет
        return self.on


class Game4(BoardFourthGame):  # класс 4 мини игры, унаследованный от класса поля
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


class Game2(BoardSecondGame):  # класс 2 мини игры, унаследованный от класса поля
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
        for i in range(10):
            i, j = randint(0, self.height - 1), randint(0, self.width - 1)
            while [i, j] in list_walls or (i == 0 and j == 0) or (i == self.height - 1 and j == self.width - 1):
                i, j = randint(0, self.height - 1), randint(0, self.width - 1)
            list_walls.append([i, j])
            self.board[j][i] = 10
        while not self.has_path(0, 0, 9, 9):
            for elem in list_walls:
                self.board[elem[1]][elem[0]] = 0
            list_walls = []
            for i in range(10):
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
        if not was:  # как я поняла, эта часть кода отвечает за победу? по идее, если да, то именно тут будет
            global startgame2  # изменяться значение переменной, которая включает эту игру
            startgame2 = 'end'
            font = pygame.font.Font(None, 50)
            text = font.render('Победа!', True, pygame.Color('yellow'))
            screen.blit(text, (300, 15))
        all_sprites2.draw(screen)


class Egg(pygame.sprite.Sprite):  # класс спрайта яйца для 3 мини игры
    image = load_image('egg.png')

    def __init__(self):
        super().__init__(eggs)
        self.image = Egg.image
        self.rect = self.image.get_rect()
        self.rect.x = randrange(0, width - self.rect.width)
        self.rect.y = 50
        self.y = 50
        self.v = 100
        self.clock = pygame.time.Clock()

    def update(self):
        global mistakes
        self.y = self.y + self.v * self.clock.tick() / 1000
        self.rect.y = self.y
        if self.rect.y > height:
            missed_eggs.add(self)
            mistakes = len(missed_eggs)


def draw_final(screen, time):  # для 1 миниигры, отрисовка финала
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 50)
    txt = f'Электричество восстановлено! Ваше время: {str(time)[0:2]}'
    text = font.render(txt, True, (100, 255, 100))
    text2 = font.render("Нажмите пробел", True, (100, 255, 100))
    text2_x = width // 2 - text2.get_width() // 2
    text2_y = height // 2 - text2.get_height() // 2 + 100
    text_x = width // 2 - text.get_width() // 2
    text_y = height // 2 - text.get_height() // 2
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    screen.blit(text2, (text2_x, text2_y))
    pygame.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10, text_w + 20, text_h + 20), 1)


def draw(screen, mistakes):  # для 3 миниигры, отрисовка полоски вверху
    life = 3
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, width, 50))
    font = pygame.font.Font(None, 50)
    text = font.render(str(life - mistakes), True, (255, 255, 255))
    text_x = 50
    text_y = 10
    screen.blit(text, (text_x, text_y))


def draw_game_over(screen):  # для 3 миниигры, отрисовка проигрыша
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 50)
    text = font.render("Game Over", True, (100, 255, 100))
    text_x = width // 2 - text.get_width() // 2
    text_y = height // 2 - text.get_height() // 2
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    pygame.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10, text_w + 20, text_h + 20), 1)


def draw_win(screen):  # для 3 миниигры, отрисовка победы
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 50)
    text = font.render("Победа! Вы справились.", True, (100, 255, 100))
    text2 = font.render("Нажмите пробел", True, (100, 255, 100))
    text2_x = width // 2 - text2.get_width() // 2
    text2_y = height // 2 - text2.get_height() // 2 + 100
    text_x = width // 2 - text.get_width() // 2
    text_y = height // 2 - text.get_height() // 2
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    screen.blit(text2, (text2_x, text2_y))
    pygame.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10, text_w + 20, text_h + 20), 1)


startgame1 = False  # переменные для стартов всех игр
startgame2 = False
startgame3 = False
startgame4 = False
end = False

if __name__ == '__main__':  # инициализация игры
    pygame.init()
    size = width, height = 980, 590
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Save Jurassic Park')
    all_sprites = pygame.sprite.Group()

    jurassic_park = pygame.sprite.Sprite(all_sprites)
    jurassic_park.image = load_image('1.JPEG')  # стартовая картинка
    jurassic_park.rect = jurassic_park.image.get_rect()
    jurassic_park.rect.x = 0
    jurassic_park.rect.y = 0
    picture = 1

    all_game_running = True

    while all_game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: # чтоб по пробелу сменялись картинки-предистории к игре
                    if picture == 1:
                        jurassic_park.image = load_image('2.JPEG')
                        jurassic_park.rect = jurassic_park.image.get_rect()
                        jurassic_park.rect.x = 0
                        jurassic_park.rect.y = 0
                        picture = 2
                    elif picture == 2:
                        jurassic_park.image = load_image('3.JPEG')
                        jurassic_park.rect = jurassic_park.image.get_rect()
                        jurassic_park.rect.x = 0
                        jurassic_park.rect.y = 0
                        picture = 3
                    elif picture == 3:
                        jurassic_park.image = load_image('4.JPEG')
                        jurassic_park.rect = jurassic_park.image.get_rect()
                        jurassic_park.rect.x = 0
                        jurassic_park.rect.y = 0
                        picture = 4
                    elif picture == 4:
                        starting = True
                        all_sprites.remove(jurassic_park)
                        all_game_running = False
                        startgame1 = True

        all_sprites.draw(screen)
        pygame.display.flip()

    pygame.quit()

if startgame1:  # первая мини игра
    pygame.init()
    size = width, height = 850, 480
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Провода')
    first_level = pygame.sprite.Group()
    second_level = pygame.sprite.Group()
    third_level = pygame.sprite.Group()
    start_group = pygame.sprite.Group()
    nxtlvl_group = pygame.sprite.Group()

    start = pygame.sprite.Sprite(start_group)
    start.image = load_image('electricity room.jpg')  # стартовый экран
    start.rect = start.image.get_rect()
    start.rect.x = 0
    start.rect.y = -150

    nextlvl = pygame.sprite.Sprite(nxtlvl_group)
    nextlvl.image = load_image('next level.png')  # спрайт перехода на след. уровень
    nextlvl.rect = nextlvl.image.get_rect()
    nextlvl.rect.x = (width - nextlvl.rect.width) // 2
    nextlvl.rect.y = (height - nextlvl.rect.height) // 2

    screen.fill((202, 196, 176))
    running = True
    level = 1

    board = BoardFirstGame(5, 3)
    board.set_view(10, 10, 133)
    game_start = False

    make1 = True
    make2 = True
    make3 = True
    get_time = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game_start is False:
                        game_start = True
                        start_group.remove(start)
                        start_time = pygame.time.get_ticks()
                        screen.fill((202, 196, 176))
                    if level == 'end':
                        running = False
                        startgame1 = False
                        startgame2 = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if level == 1 and game_start:
                    first_level.update(event)
                    if l1.is_on() and l2.is_on():
                        if (event.pos[0] >= 266 and event.pos[0] < 584) and \
                                (event.pos[1] >= 212 and event.pos[1] < 306):
                            level = 2
                            screen.fill((202, 196, 176))
                elif level == 2 and game_start:
                    second_level.update(event)
                    if l3.is_on() and l4.is_on() and l5.is_on():
                        if (event.pos[0] >= 266 and event.pos[0] < 584) and \
                                (event.pos[1] >= 212 and event.pos[1] < 306):
                            level = 3
                            screen.fill((202, 196, 176))
                elif level == 3 and game_start:
                    third_level.update(event)
        if game_start is False:
            start_group.draw(screen)
            pygame.display.flip()
        elif game_start:
            if level == 1:
                if make1:
                    e1 = Electro(409, 143, first_level)
                    s1 = Straight(276, 143, first_level)  # создание спрайтов конкретно для первого уровня
                    s2 = Straight(276, 10, first_level)
                    s3 = Straight(409, 10, first_level)
                    c1 = Corner(143, 10, first_level)
                    t1 = T(143, 143, first_level)
                    l1 = Lamp(542, 10, 'left', first_level)
                    l2 = Lamp(10, 143, 'right', first_level)
                    make1 = False

                first_level.draw(screen)
                pygame.display.flip()
                if l1.is_on() and l2.is_on():
                    first_level.empty()
                    nxtlvl_group.draw(screen)
                    pygame.display.flip()
            if level == 2:
                if make2:
                    e2 = Electro(409, 143, second_level)
                    c2 = Corner(409, 10, second_level)
                    c3 = Corner(143, 10, second_level)  # создание спрайтов для второго уровня
                    t2 = T(276, 10, second_level)
                    t3 = T(276, 276, second_level)
                    s4 = Straight(276, 143, second_level)
                    l3 = Lamp(143, 276, 'right', second_level)
                    l4 = Lamp(409, 276, 'left', second_level)
                    l5 = Lamp(143, 143, 'up', second_level)
                    make2 = False
                second_level.draw(screen)
                pygame.display.flip()
                if l3.is_on() and l4.is_on() and l5.is_on():
                    second_level.empty()
                    nxtlvl_group.draw(screen)
            if level == 3:
                if make3:
                    e_1 = Electro(409, 143, third_level)
                    t_2 = T(276, 143, third_level)  # создание спрайтов конкретно для первого уровня
                    s_2 = Straight(276, 10, third_level)
                    s_3 = Straight(409, 10, third_level)
                    t_3 = T(143, 10, third_level)
                    t_1 = T(143, 143, third_level)
                    l_1 = Lamp(542, 10, 'left', third_level)
                    l_2 = Lamp(10, 143, 'right', third_level)
                    l_3 = Lamp(276, 276, 'up', third_level)
                    l_4 = Lamp(10, 10, 'right2', third_level)
                    make3 = False
                third_level.draw(screen)
                pygame.display.flip()
                if l_1.is_on() and l_2.is_on() and l_3.is_on() and l_4.is_on():
                    third_level.empty()
                    end_time = pygame.time.get_ticks()
                    level = 'end'

                if level == 'end':
                    final_time = (end_time - start_time) / 1000
                    draw_final(screen, final_time)

            board.render(screen)
            pygame.display.flip()

    pygame.quit()

if startgame2:  # вторая мини игра
    def do():
        global startgame2, startgame3
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
        board = Game2(10, 10)
        while running:  # игровой цикл
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:  # переход к игре при нажатии пробела
                    if event.key == pygame.K_SPACE and begin:
                        begin = False
                        make_bombs_keys = True
                    elif event.key == pygame.K_SPACE:
                        if startgame2 == 'end':
                            running = False
                            startgame3 = True
                            startgame2 = False
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
                    board = Game2(10, 10)
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

if startgame3:  # третья мини игра
    pygame.init()
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Инкубатор')
    eggs = pygame.sprite.Group()
    basket_group = pygame.sprite.Group()
    missed_eggs = pygame.sprite.Group()
    catched_eggs = pygame.sprite.Group()
    heart_group = pygame.sprite.Group()
    start_group = pygame.sprite.Group()
    CREATEEGG = pygame.USEREVENT + 1
    MISTAKE = pygame.USEREVENT + 2
    screen.fill((202, 196, 176))

    running = True
    time_spawn = 2500
    mistakes = 0

    eggs_count = 0
    right = False
    left = False
    levelup = False
    basket = pygame.sprite.Sprite(basket_group)  # спрайт корзины
    basket.image = load_image('basket.png')
    basket.rect = basket.image.get_rect()
    basket.rect.x = (width - basket.rect.width) // 2
    basket.rect.y = height - basket.rect.height

    heart = pygame.sprite.Sprite(heart_group)
    heart.image = load_image('heart.png')  # спрайт жизней
    heart.rect = heart.image.get_rect()
    heart.rect.x = 0
    heart.rect.y = 0

    start = pygame.sprite.Sprite(start_group)
    start.image = load_image('incubator.jpeg')  # начальный экран
    start.rect = start.image.get_rect()
    start.rect.x = 0
    start.rect.y = -120

    start_game = False
    start_create = False
    nextgame = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start_game = True
                    start_group.remove(start)
                    start_create = True
                    if nextgame:
                        running = False
                        startgame4 = True
                        startgame3 = False
            if event.type == CREATEEGG:
                Egg()
                eggs_count += 1
                if eggs_count == 5 or eggs_count == 15 or eggs_count == 25:
                    levelup = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    right = True
                if event.key == pygame.K_LEFT:
                    left = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    right = False
                if event.key == pygame.K_LEFT:
                    left = False
        if left and basket.rect.x > 0:
            basket.rect.x -= 1
        if right and basket.rect.x < width - basket.rect.width:
            basket.rect.x += 1
        if mistakes == 3:
            start_game = False
            draw_game_over(screen)
        egg = pygame.sprite.spritecollideany(basket, eggs)
        if egg != None:
            if egg.rect.y + egg.rect.height - 30 <= basket.rect.y:
                pygame.sprite.spritecollide(basket, eggs, True)
                catched_eggs.add(egg)
        if eggs_count == 5 or eggs_count == 15 or eggs_count == 25:
            if levelup:
                time_spawn -= 500
                pygame.time.set_timer(CREATEEGG, time_spawn)
                levelup = False
        if eggs_count == 30:
            time_spawn = 0
            pygame.time.set_timer(CREATEEGG, time_spawn)
            if len(catched_eggs) == (30 - mistakes):
                start_game = False
                draw_win(screen)
                nextgame = True
        start_group.draw(screen)
        if start_game:
            if start_create:
                start_create = False
                pygame.time.set_timer(CREATEEGG, time_spawn)
            screen.fill((202, 196, 176))
            draw(screen, mistakes)
            heart_group.draw(screen)
            basket_group.draw(screen)
            eggs.draw(screen)
            eggs.update()
        pygame.display.flip()
    pygame.quit()

if startgame4:  # 4 мини игра
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
        count = 4
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
            else:  # рисование поля
                board = Game4(5, 5, level)
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
                list_light = []
                take_signals = True
                remember = False
                board = Game4(5, 5, level)
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
        end = True
        startgame4 = False

if end:
    pygame.init()
    size1 = width1, height1 = 980, 590
    screen1 = pygame.display.set_mode(size1)
    pygame.display.set_caption('Финал')
    all_sprites1 = pygame.sprite.Group()
    sprite1 = pygame.sprite.Sprite()
    sprite1.image = load_image('jurassic park end.jpg')
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
