import pygame   # импорт библиотек
import os
import sys
from random import randrange


def draw(screen, mistakes):
    life = 3
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, width, 50))
    font = pygame.font.Font(None, 50)
    text = font.render(str(life - mistakes), True, (255, 255, 255))
    text_x = 50
    text_y = 10
    screen.blit(text, (text_x, text_y))


def draw_game_over(screen):
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 50)
    text = font.render("Game Over", True, (100, 255, 100))
    text_x = width // 2 - text.get_width() // 2
    text_y = height // 2 - text.get_height() // 2
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    pygame.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10,
                                           text_w + 20, text_h + 20), 1)


def draw_win(screen):
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 50)
    text = font.render("Победа! Вы справились.", True, (100, 255, 100))
    text_x = width // 2 - text.get_width() // 2
    text_y = height // 2 - text.get_height() // 2
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    pygame.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10,
                                           text_w + 20, text_h + 20), 1)


def load_image(name, colorkey=None):  # функция для загрузки изображений
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print('Файл с изображением не найден.')
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Egg(pygame.sprite.Sprite):
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


if __name__ == '__main__':   # инициализация игры
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
    basket = pygame.sprite.Sprite(basket_group)
    basket.image = load_image('basket.png')
    basket.rect = basket.image.get_rect()
    basket.rect.x = (width - basket.rect.width) // 2
    basket.rect.y = height - basket.rect.height

    heart = pygame.sprite.Sprite(heart_group)
    heart.image = load_image('heart.png')
    heart.rect = heart.image.get_rect()
    heart.rect.x = 0
    heart.rect.y = 0

    start = pygame.sprite.Sprite(start_group)
    start.image = load_image('incubator.jpeg')
    start.rect = start.image.get_rect()
    start.rect.x = 0
    start.rect.y = -120

    start_game = False
    start_create = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start_game = True
                    start_group.remove(start)
                    start_create = True
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
            if len(catched_eggs) > 27:
                start_game = False
                draw_win(screen)
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