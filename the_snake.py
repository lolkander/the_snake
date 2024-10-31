import pygame
from random import choice

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, position=(0, 0)):
        """
        Инициализирует базовые атрибуты объекта.

        :param position: Позиция объекта на игровом поле.
        """
        self.position = position
        self.body_color = None

    def draw(self):
        """
        Абстрактный метод для отрисовки объекта на экране.
        Предназначен для переопределения в дочерних классах.
        """
        pass


class Apple(GameObject):
    """Класс для яблока."""

    def __init__(self):
        """Инициализирует яблоко."""
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайное положение яблока на игровом поле."""
        x_positions = [i * GRID_SIZE for i in range(GRID_WIDTH)]
        y_positions = [i * GRID_SIZE for i in range(GRID_HEIGHT)]
        self.position = (choice(x_positions), choice(y_positions))

    def draw(self):
        """Отрисовывает яблоко на игровой поверхности."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс для змейки."""

    def __init__(self):
        """Инициализирует начальное состояние змейки."""
        super().__init__((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.length = 2
        self.positions = [self.position]
        self.direction = 'RIGHT'
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет позицию змейки."""
        head_x, head_y = self.positions[0]

        if self.direction == 'UP':
            head_y -= GRID_SIZE
        elif self.direction == 'DOWN':
            head_y += GRID_SIZE
        elif self.direction == 'LEFT':
            head_x -= GRID_SIZE
        elif self.direction == 'RIGHT':
            head_x += GRID_SIZE

        # Проверка на прохождение сквозь стены
        if head_x < 0:
            head_x = SCREEN_WIDTH - GRID_SIZE
        elif head_x >= SCREEN_WIDTH:
            head_x = 0
        if head_y < 0:
            head_y = SCREEN_HEIGHT - GRID_SIZE
        elif head_y >= SCREEN_HEIGHT:
            head_y = 0

        self.positions = [(head_x, head_y)] + self.positions[:self.length - 1]
        if len(self.positions) > self.length:
            self.last = self.positions[-1]
        else:
            self.last = None

    def draw(self):
        """Отрисовывает змейку на экране."""
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 2
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = 'RIGHT'
        self.next_direction = None
        self.last = None


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise SystemExit
            elif (event.key == pygame.K_UP
                  and game_object.direction != 'DOWN'):
                game_object.next_direction = 'UP'
            elif (event.key == pygame.K_DOWN
                  and game_object.direction != 'UP'):
                game_object.next_direction = 'DOWN'
            elif (event.key == pygame.K_LEFT
                  and game_object.direction != 'RIGHT'):
                game_object.next_direction = 'LEFT'
            elif (event.key == pygame.K_RIGHT
                  and game_object.direction != 'LEFT'):
                game_object.next_direction = 'RIGHT'


def main():
    """
    Основная функция игры, которая инициализирует PyGame,
    создает объекты змейки и яблока,
    и запускает основной игровой цикл.
    """
    # Инициализация PyGame:
    pygame.init()
    global snake, apple
    snake = Snake()
    apple = Apple()

    while True:
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pygame.display.update()

        clock.tick(SPEED)


if __name__ == '__main__':
    main()
