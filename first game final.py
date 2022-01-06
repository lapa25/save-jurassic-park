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


def draw_final(screen, time):
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 50)
    txt = f'Электричество восстановлено! Ваше время: {str(time)[0:2]}'
    text = font.render(txt, True, (100, 255, 100))
    text_x = width // 2 - text.get_width() // 2
    text_y = height // 2 - text.get_height() // 2
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    pygame.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10,
                                           text_w + 20, text_h + 20), 1)


def draw(screen):
    if level == 1:
        pygame.draw.circle(screen, (0, 0, 0), (width - 30, 30), 20, width=2)
        pygame.draw.circle(screen, (0, 0, 0), (width - 30, 80), 20, width=2)
        pygame.draw.circle(screen, (0, 0, 0), (width - 30, 130), 20, width=2)
    elif level == 2:
        pygame.draw.circle(screen, (0, 0, 0), (width - 30, 30), 20, width=2)
        pygame.draw.circle(screen, (100, 255, 100), (width - 30, 30), 18)
        pygame.draw.circle(screen, (0, 0, 0), (width - 30, 80), 20, width=2)
        pygame.draw.circle(screen, (0, 0, 0), (width - 30, 130), 20, width=2)
    elif level == 3:
        pygame.draw.circle(screen, (0, 0, 0), (width - 30, 30), 20, width=2)
        pygame.draw.circle(screen, (100, 255, 100), (width - 30, 30), 18)
        pygame.draw.circle(screen, (0, 0, 0), (width - 30, 80), 20, width=2)
        pygame.draw.circle(screen, (100, 255, 100), (width - 30, 80), 18)
        pygame.draw.circle(screen, (0, 0, 0), (width - 30, 130), 20, width=2)
    elif level == 'end':
        pygame.draw.circle(screen, (0, 0, 0), (width - 30, 30), 20, width=2)
        pygame.draw.circle(screen, (100, 255, 100), (width - 30, 30), 18)
        pygame.draw.circle(screen, (0, 0, 0), (width - 30, 80), 20, width=2)
        pygame.draw.circle(screen, (100, 255, 100), (width - 30, 80), 18)
        pygame.draw.circle(screen, (0, 0, 0), (width - 30, 130), 20, width=2)
        pygame.draw.circle(screen, (100, 255, 100), (width - 30, 130), 18)


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
        if level == 1 or level == 3:
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
                if level == 1 or level == 3:
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

    def update(self, *args):
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
                if e_1.is_now() == 'left' and (t_2.is_now() == 'down' or t_2.is_now() == 'up') and t_1.is_now() == 'up' and \
                        (t_3.is_now() == 'down' or t_3.is_now() == 'right') and s_2.is_now() == 'gorizont' and s_3.is_now() == 'gorizont':
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

    def is_on(self):
        return self.on


if __name__ == '__main__':   # инициализация игры
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
    nextlvl.image = load_image('next level.png')
    nextlvl.rect = nextlvl.image.get_rect()
    nextlvl.rect.x = (850 - nextlvl.rect.width) // 2
    nextlvl.rect.y = (480 - nextlvl.rect.height) // 2

    screen.fill((202, 196, 176))
    running = True
    level = 1

    board = Board(5, 3)
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
                    game_start = True
                    start_group.remove(start)
                    start_time = pygame.time.get_ticks()
                    screen.fill((202, 196, 176))
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
                draw(screen)
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
                draw(screen)
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
                draw(screen)
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