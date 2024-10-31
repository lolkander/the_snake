import tkinter as tk
import random

# Constants
GAME_WIDTH = 600
GAME_HEIGHT = 400
SPEED = 100
SPACE_SIZE = 20
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"


class SnakeGame(tk.Tk):
    """Класс, представляющий игру Змейка."""

    def __init__(self):
        """Инициализация игрового окна и начальных условий."""
        super().__init__()
        self.title("Snake Game")
        self.resizable(False, False)
        self.score = 0
        self.high_score = 0
        self.direction = 'down'
        self.snake = None
        self.food = None

        self.label = tk.Label(
            self, text="Score:{}".format(self.score), font=('consolas', 20)
        )
        self.label.pack()

        self.canvas = tk.Canvas(
            self, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH
        )
        self.canvas.pack()

        self.center_window()

        self.bind('<Left>', lambda event: self.change_direction('left'))
        self.bind('<Right>', lambda event: self.change_direction('right'))
        self.bind('<Up>', lambda event: self.change_direction('up'))
        self.bind('<Down>', lambda event: self.change_direction('down'))

        self.show_title_screen()

    def center_window(self):
        """Центрирует окно игры на экране."""
        self.update()
        window_width = self.winfo_width()
        window_height = self.winfo_height()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))

        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def start_game(self):
        """Запускает игру, инициализирует змейку и еду."""
        self.canvas.delete("all")
        self.score = 0
        self.direction = 'down'
        self.label.config(text="Score:{}".format(self.score))
        self.snake = Snake(self.canvas)
        self.food = Food(self.canvas, self.snake)
        self.next_turn()

    def next_turn(self):
        """Обновляет состояние игры, перемещает змейку и проверяет столкновения."""
        self.snake.move(self.direction)

        if self.snake.check_collisions():
            self.game_over()
        else:
            if self.snake.eat_food(self.food):
                self.score += 1
                self.label.config(text="Score:{}".format(self.score))
                self.canvas.delete("food")
                self.food = Food(self.canvas, self.snake)
            self.after(SPEED, self.next_turn)

    def change_direction(self, new_direction):
        """Изменяет направление движения змейки."""
        opposite_directions = {
            'left': 'right', 'right': 'left',
            'up': 'down', 'down': 'up'
        }
        if self.direction != opposite_directions.get(new_direction):
            self.direction = new_direction

    def game_over(self):
        """Обрабатывает окончание игры и отображает результаты."""
        if self.score > self.high_score:
            self.high_score = self.score
        self.canvas.delete(tk.ALL)
        self.canvas.create_text(
            GAME_WIDTH / 2, GAME_HEIGHT / 2 - 40,
            font=('consolas', 70), text="GAME OVER", fill="red", tag="gameover"
        )
        self.canvas.create_text(
            GAME_WIDTH / 2, GAME_HEIGHT / 2 + 10,
            font=('consolas', 20), text="Score: {}".format(self.score), fill="white"
        )
        self.canvas.create_text(
            GAME_WIDTH / 2, GAME_HEIGHT / 2 + 40,
            font=('consolas', 20),
            text="High Score: {}".format(self.high_score), fill="white"
        )
        self.canvas.create_text(
            GAME_WIDTH / 2, GAME_HEIGHT / 2 + 70,
            font=('consolas', 20),
            text="Press Enter to Restart", fill="white", tag="restart"
        )
        self.bind('<Return>', self.restart_game)

    def restart_game(self, event):
        """Перезапускает игру при нажатии клавиши Enter."""
        self.unbind('<Return>')
        self.start_game()

    def show_title_screen(self):
        """Отображает экран приветствия перед началом игры."""
        self.canvas.delete("all")
        self.canvas.create_text(
            GAME_WIDTH / 2, GAME_HEIGHT / 2 - 40,
            font=('consolas', 50), text="Snake Game", fill="white", tag="title"
        )
        self.canvas.create_text(
            GAME_WIDTH / 2, GAME_HEIGHT / 2 + 40,
            font=('consolas', 20),
            text="Press Enter to Start", fill="white", tag="start_prompt"
        )
        self.bind('<Return>', self.start_game_from_title)

    def start_game_from_title(self, event):
        """Начинает игру из экрана приветствия."""
        self.unbind('<Return>')
        self.start_game()


class Snake:
    """Класс, представляющий змейку в игре."""

    def __init__(self, canvas):
        """Инициализация змейки."""
        self.canvas = canvas
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        # Start the snake in the center of the screen
        start_x = GAME_WIDTH // 2
        start_y = GAME_HEIGHT // 2

        for i in range(0, BODY_PARTS):
            self.coordinates.append([start_x, start_y])
            start_x -= SPACE_SIZE  # Move the next part to the left of the previous part

        for x, y in self.coordinates:
            square = self.canvas.create_rectangle(
                x, y, x + SPACE_SIZE, y + SPACE_SIZE,
                fill=SNAKE_COLOR, tag="snake"
            )
            self.squares.append(square)

    def move(self, direction):
        """Перемещает змейку в заданном направлении."""
        x, y = self.coordinates[0]

        if direction == "up":
            y -= SPACE_SIZE
        elif direction == "down":
            y += SPACE_SIZE
        elif direction == "left":
            x -= SPACE_SIZE
        elif direction == "right":
            x += SPACE_SIZE

        # Проверка на пересечение границ
        x %= GAME_WIDTH
        y %= GAME_HEIGHT

        self.coordinates.insert(0, [x, y])

        square = self.canvas.create_rectangle(
            x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR
        )
        self.squares.insert(0, square)

        del self.coordinates[-1]
        self.canvas.delete(self.squares[-1])
        del self.squares[-1]

    def eat_food(self, food):
        """Проверяет, съела ли змейка еду."""
        if self.coordinates[0] == food.coordinates:
            self.coordinates.append(self.coordinates[-1])  # Add new segment at the snake's tail
            square = self.canvas.create_rectangle(
                self.coordinates[-1][0], self.coordinates[-1][1],
                self.coordinates[-1][0] + SPACE_SIZE,
                self.coordinates[-1][1] + SPACE_SIZE,
                fill=SNAKE_COLOR
            )
            self.squares.append(square)
            return True
        return False

    def check_collisions(self):
        """Проверяет на наличие столкновений со стенами или телом змейки."""
        x, y = self.coordinates[0]

        # Проверка на столкновения с телом
        for body_part in self.coordinates[1:]:
            if x == body_part[0] and y == body_part[1]:
                return True

        return False


class Food:
    """Класс, представляющий еду для змейки."""

    def __init__(self, canvas, snake):
        """Инициализация еды с случайным положением."""
        self.canvas = canvas
        while True:
            x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
            y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
            self.coordinates = [x, y]
            if self.coordinates not in snake.coordinates:
                break

        self.canvas.create_oval(
            x, y, x + SPACE_SIZE, y + SPACE_SIZE,
            fill=FOOD_COLOR, tag="food"
        )


if __name__ == "__main__":
    game = SnakeGame()
    game.mainloop()
