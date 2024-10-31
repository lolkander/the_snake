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
    def __init__(self):
        super().__init__()
        self.title("Snake Game")
        self.resizable(False, False)
        self.score = 0
        self.high_score = 0
        self.direction = 'down'
        self.snake = None
        self.food = None

        self.label = tk.Label(self, text="Score:{}".format(self.score), font=('consolas', 20))
        self.label.pack()

        self.canvas = tk.Canvas(self, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
        self.canvas.pack()

        self.center_window()

        self.bind('<Left>', lambda event: self.change_direction('left'))
        self.bind('<Right>', lambda event: self.change_direction('right'))
        self.bind('<Up>', lambda event: self.change_direction('up'))
        self.bind('<Down>', lambda event: self.change_direction('down'))

        self.show_title_screen()

    def center_window(self):
        self.update()
        window_width = self.winfo_width()
        window_height = self.winfo_height()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))

        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def start_game(self):
        self.canvas.delete("all")
        self.score = 0
        self.direction = 'down'
        self.label.config(text="Score:{}".format(self.score))
        self.snake = Snake(self.canvas)
        self.food = Food(self.canvas, self.snake)
        self.next_turn()

    def next_turn(self):
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
        opposite_directions = {'left': 'right', 'right': 'left', 'up': 'down', 'down': 'up'}
        if self.direction != opposite_directions.get(new_direction):
            self.direction = new_direction

    def game_over(self):
        if self.score > self.high_score:
            self.high_score = self.score
        self.canvas.delete(tk.ALL)
        self.canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2 - 40,
                                font=('consolas', 70), text="GAME OVER", fill="red", tag="gameover")
        self.canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2 + 10,
                                font=('consolas', 20), text="Score: {}".format(self.score), fill="white")
        self.canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2 + 40,
                                font=('consolas', 20), text="High Score: {}".format(self.high_score), fill="white")
        self.canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2 + 70,
                                font=('consolas', 20), text="Press Enter to Restart", fill="white", tag="restart")
        self.bind('<Return>', self.restart_game)

    def restart_game(self, event):
        self.unbind('<Return>')
        self.start_game()

    def show_title_screen(self):
        self.canvas.delete("all")
        self.canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2 - 40,
                                font=('consolas', 50), text="Snake Game", fill="white", tag="title")
        self.canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2 + 40,
                                font=('consolas', 20), text="Press Enter to Start", fill="white", tag="start_prompt")
        self.bind('<Return>', self.start_game_from_title)

    def start_game_from_title(self, event):
        self.unbind('<Return>')
        self.start_game()


class Snake:
    def __init__(self, canvas):
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
            square = self.canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

    def move(self, direction):
        x, y = self.coordinates[0]

        if direction == "up":
            y -= SPACE_SIZE
        elif direction == "down":
            y += SPACE_SIZE
        elif direction == "left":
            x -= SPACE_SIZE
        elif direction == "right":
            x += SPACE_SIZE

        self.coordinates.insert(0, [x, y])

        square = self.canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
        self.squares.insert(0, square)

        del self.coordinates[-1]
        self.canvas.delete(self.squares[-1])
        del self.squares[-1]

    def eat_food(self, food):
        if self.coordinates[0] == food.coordinates:
            self.coordinates.append(self.coordinates[-1])  # Add new segment at the snake's tail
            square = self.canvas.create_rectangle(self.coordinates[-1][0], self.coordinates[-1][1],
                                                  self.coordinates[-1][0] + SPACE_SIZE,
                                                  self.coordinates[-1][1] + SPACE_SIZE,
                                                  fill=SNAKE_COLOR)
            self.squares.append(square)
            return True
        return False

    def check_collisions(self):
        x, y = self.coordinates[0]

        if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
            return True

        for body_part in self.coordinates[1:]:
            if x == body_part[0] and y == body_part[1]:
                return True

        return False


class Food:
    def __init__(self, canvas, snake):
        self.canvas = canvas
        while True:
            x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
            y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
            self.coordinates = [x, y]
            if self.coordinates not in snake.coordinates:
                break

        self.canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")


if __name__ == "__main__":
    game = SnakeGame()
    game.mainloop()
