import pygame   # импорт библиотеки


class Board:
    def __init__(self, width, height):   #инициализация класса
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
                if (left, top) not in self.coords:   # отрисовка клеток закомментирована, чтобы в конечном результате
                    self.coords.append((left, top))  # их не было видно
                # pygame.draw.rect(screen, pygame.Color('white'),
                #                  (left, top, self.cell_size, self.cell_size), width=1)
                left += self.cell_size
            top += self.cell_size
            left = self.left
        top = self.top

    def get_cell(self, mouse_pos):   # получение координаты клетки
        for i in self.coords:
            if (0 <= mouse_pos[0] - i[0] <= self.cell_size) and (0 <= mouse_pos[1] - i[1] <= self.cell_size):
                return i


    def on_click(self, cell_coords):
        print(cell_coords)

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)


if __name__ == '__main__':
    pygame.init()
    size = width, height = 850, 480
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('board')
    board = Board(5, 3)
    board.set_view(10, 10, 133)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event.pos)
        screen.fill((0, 0, 0))
        board.render(screen)
        pygame.display.flip()
    pygame.quit()