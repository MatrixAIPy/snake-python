import os
import random
import msvcrt
import time
from typing import List, Tuple


class Game:
    def __init__(self, start_x: int, start_y: int, board_size: int = 10):
        self.board_size = board_size
        self.snake: List[Tuple[int, int]] = [(start_x, start_y)]
        self.food_x: int = 0
        self.food_y: int = 0
        self.last_move: str = "d"
        self.spawn_food()

    def change_position(self, dx: int, dy: int) -> None:
        head_x, head_y = self.snake[0]
        self.snake.insert(0, (head_x + dx, head_y + dy))

    def remove_tail(self) -> None:
        if self.snake:
            self.snake.pop()

    def is_over(self) -> bool:
        head = self.snake[0]
        return head in self.snake[1:]

    def handle_wall_collision(self) -> None:
        x, y = self.snake[0]
        if x < 0:
            self.snake[0] = (self.board_size - 1, y)
        elif x >= self.board_size:
            self.snake[0] = (0, y)
        elif y < 0:
            self.snake[0] = (x, self.board_size - 1)
        elif y >= self.board_size:
            self.snake[0] = (x, 0)

    def spawn_food(self) -> None:
        all_coords = [(x, y) for x in range(self.board_size) for y in range(self.board_size)]
        free_coords = [coord for coord in all_coords if coord not in self.snake]
        if free_coords:
            self.food_x, self.food_y = random.choice(free_coords)


class Console:
    def __init__(self, board_size: int = 10):
        self.board_size = board_size
        self.directions = {
            "w": (0, -1),
            "s": (0, 1),
            "a": (-1, 0),
            "d": (1, 0)
        }

    def print_board(self, game: Game) -> None:
        output = []
        for y in range(self.board_size):
            row = []
            for x in range(self.board_size):
                if (x, y) in game.snake:
                    row.append("■")
                elif x == game.food_x and y == game.food_y:
                    row.append("x")
                else:
                    row.append(".")
            output.append(" ".join(row))
        print("\n".join(output))

    def get_move(self, game: Game, timeout: float = 0.1) -> Tuple[int, int]:
        start_time = time.time()
        move = None

        while time.time() - start_time <= timeout:
            if msvcrt.kbhit():
                char = msvcrt.getch().decode().lower()
                if char in self.directions:
                    move = char
            time.sleep(0.01)

        if move is None:
            move = game.last_move
        else:
            game.last_move = move

        return self.directions[move]


def main() -> None:
    board_size = 10
    game = Game(start_x=2, start_y=2, board_size=board_size)
    console = Console(board_size=board_size)

    while not game.is_over():
        os.system("cls" if os.name == "nt" else "clear")
        console.print_board(game)

        dx, dy = console.get_move(game)
        game.change_position(dx, dy)

        if game.food_x == game.snake[0][0] and game.food_y == game.snake[0][1]:
            game.spawn_food()
        else:
            game.remove_tail()

        game.handle_wall_collision()

    print("GAME OVER")


if __name__ == "__main__":
    main()