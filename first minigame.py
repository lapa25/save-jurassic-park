import pygame   # импорт библиотек
import os
import sys
from board import Board


def load_image(name, colorkey=None):  # функция для загрузки изображений
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print('Файл с изображением не найден.')
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Electro(pygame.sprite.Sprite):     # класс для спрайта электрощитка
    image_down = load_image('electricity_down.png')
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


class Straight(pygame.sprite.Sprite):    # класс для спрайта прямого провода
    g_image = load_image('straight_gorizont.png')
    v_image = load_image('straight_vertical.png')

    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = Straight.v_image
        self.rect = self.image.get_rect()
        if level == 1:
            self.rect.x = x + ((133 - self.rect.width) // 2)
        elif level == 2:
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
                if level == 1:
                    self.rect.x = self.x + ((133 - self.rect.width) // 2)
                elif level == 2:
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


class T(pygame.sprite.Sprite):   # класс для спрайта разветвляющегося провода
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


class Lamp(pygame.sprite.Sprite):   # класс для спрайта лампочки
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
        elif rotate == 'right':
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

    def update(self, *args):
        if level == 1:
            if self.now == 'right':
                if e.is_now() == 'left' and s1.is_now() == 'gorizont' and (t.is_now() == 'up' or t.is_now() == 'down'):
                    self.image = self.image_right_on
                    self.on = True
                else:
                    self.image = self.image_right_off
                    self.on = False
            if self.now == 'left':
                if e.is_now() == 'left' and s1.is_now() == 'gorizont' and t.is_now() == 'up' and c.is_now() == 'right' \
                        and s2.is_now() == 'gorizont' and s3.is_now() == 'gorizont':
                    self.image = self.image_left_on
                    self.on = True
                else:
                    self.image = self.image_left_off
                    self.on = False
        if level == 2:
            if self.now == 'right':
                if e.is_now() == 'up' and c1.is_now() == 'down' and t1.is_now() == 'down' and s.is_now() == 'vertical' \
                        and (t2.is_now() == 'up' or t2.is_now() == 'left'):
                    self.image = self.image_right_on
                    self.on = True
                else:
                    self.image = self.image_right_off
                    self.on = False
            elif self.now == 'left':
                if e.is_now() == 'up' and c1.is_now() == 'down' and t1.is_now() == 'down' and s.is_now() == 'vertical' \
                        and (t2.is_now() == 'up' or t2.is_now() == 'right'):
                    self.image = self.image_left_on
                    self.on = True
                else:
                    self.image = self.image_left_off
                    self.on = False
            if self.now == 'up':
                if e.is_now() == 'up' and c1.is_now() == 'down' and (t1.is_now() == 'up' or t1.is_now() == 'down') \
                        and c2.is_now() == 'right':
                    self.image = self.image_up_on
                    self.on = True
                else:
                    self.image = self.image_up_off
                    self.on = False
        if level == 3:
            if self.now == 'up1':
                if e.is_now() == 'up' and (t2.is_now() == 'down' or t2.is_now() == 'right') and \
                        (t1.is_now() == 'left' or t1.is_now() == 'down'):
                    self.image = self.image_up_on
                    self.on = True
                else:
                    self.image = self.image_up_off
                    self.on = False
            elif self.now == 'up2':
                if e.is_now() == 'up' and (t2.is_now() == 'down' or t2.is_now() == 'left') and \
                        (t3.is_now() == 'right' or t3.is_now() == 'down'):
                    self.image = self.image_up_on
                    self.on = True
                else:
                    self.image = self.image_up_off
                    self.on = False
            elif self.now == 'down':
                if e.is_now() == 'up' and (t2.is_now() == 'down' or t2.is_now() == 'right') and \
                        (t1.is_now() == 'left' or t1.is_now() == 'up'):
                    self.image = self.image_down_on
                    self.on = True
                else:
                    self.image = self.image_down_off
                    self.on = False
            elif self.now == 'left':
                if e.is_now() == 'up' and (t2.is_now() == 'down' or t2.is_now() == 'left') and \
                            (t3.is_now() == 'right' or t3.is_now() == 'up') and c.is_now() == 'right':
                    self.image = self.image_left_on
                    self.on = True
                else:
                    self.image = self.image_left_off
                    self.on = False

    def is_on(self):
        return self.on


if __name__ == '__main__':   # инициализация игры
    pygame.init()
    size = width, height = 850, 480
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Провода')
    all_sprites = pygame.sprite.Group()
    start = pygame.sprite.Sprite(all_sprites)
    start.image = load_image('electricity room.jpg')  # стартовый экран
    start.rect = start.image.get_rect()
    start.rect.x = 0
    start.rect.y = -150

    screen.fill((202, 196, 176))
    running4 = True

    level = 1

    board = Board(5, 3)
    board.set_view(10, 10, 133)
    while running4:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    all_sprites = pygame.sprite.Group()
                    screen.fill((202, 196, 176))
                    running4 = False
                    running = True
            all_sprites.draw(screen)
            board.render(screen)
            pygame.display.flip()
    if level == 1:
        e = Electro(409, 143, all_sprites)
        s1 = Straight(276, 143, all_sprites)  # создание спрайтов конкретно для первого уровня
        s2 = Straight(276, 10, all_sprites)
        s3 = Straight(409, 10, all_sprites)
        c = Corner(143, 10, all_sprites)
        t = T(143, 143, all_sprites)
        l1 = Lamp(542, 10, 'left', all_sprites)
        l2 = Lamp(10, 143, 'right', all_sprites)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    all_sprites.update(event)
                    if l1.is_on() and l2.is_on():
                        all_sprites = pygame.sprite.Group()
                        nextlvl = pygame.sprite.Sprite(all_sprites)
                        nextlvl.image = load_image('next level.png')
                        nextlvl.rect = nextlvl.image.get_rect()
                        nextlvl.rect.x = (850 - nextlvl.rect.width) // 2
                        nextlvl.rect.y = (480 - nextlvl.rect.height) // 2
                        if (event.pos[0] >= 266 and event.pos[0] < 584) and (
                                event.pos[1] >= 212 and event.pos[1] < 306):
                            level = 2
                            running = False
            all_sprites.draw(screen)
            board.render(screen)
            pygame.display.flip()
    if level == 2:
        all_sprites = pygame.sprite.Group()
        screen.fill((202, 196, 176))
        e = Electro(409, 143, all_sprites)
        c1 = Corner(409, 10, all_sprites)
        c2 = Corner(143, 10, all_sprites)  # создание спрайтов для второго уровня
        t1 = T(276, 10, all_sprites)
        t2 = T(276, 276, all_sprites)
        s = Straight(276, 143, all_sprites)
        l1 = Lamp(143, 276, 'right', all_sprites)
        l2 = Lamp(409, 276, 'left', all_sprites)
        l3 = Lamp(143, 143, 'up', all_sprites)
        running2 = True
        while running2:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running2 = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    all_sprites.update(event)
                    if l1.is_on() and l2.is_on() and l3.is_on():
                        all_sprites = pygame.sprite.Group()
                        nextlvl = pygame.sprite.Sprite(all_sprites)
                        nextlvl.image = load_image('next level.png')
                        nextlvl.rect = nextlvl.image.get_rect()
                        nextlvl.rect.x = (850 - nextlvl.rect.width) // 2
                        nextlvl.rect.y = (480 - nextlvl.rect.height) // 2
                        if (event.pos[0] >= 266 and event.pos[0] < 584) and (
                                event.pos[1] >= 212 and event.pos[1] < 306):
                            level = 3
                            running2 = False
            all_sprites.draw(screen)
            board.render(screen)
            pygame.display.flip()
    if level == 3:
        all_sprites = pygame.sprite.Group()
        screen.fill((202, 196, 176))
        e = Electro(276, 276, all_sprites)
        l1 = Lamp(409, 276, 'up1', all_sprites)
        l2 = Lamp(409, 10, 'down', all_sprites)
        l3 = Lamp(276, 10, 'left', all_sprites)
        l4 = Lamp(143, 276, 'up2', all_sprites)
        c = Corner(143, 10, all_sprites)
        t1 = T(409, 143, all_sprites)
        t2 = T(276, 143, all_sprites)
        t3 = T(143, 143, all_sprites)
        running3 = True
        while running3:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running3 = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    all_sprites.update(event)
            all_sprites.draw(screen)
            board.render(screen)
            pygame.display.flip()
    pygame.quit()