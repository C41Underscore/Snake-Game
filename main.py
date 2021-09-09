import pygame as pg
from queue import Queue

BOARD_SIZE = 600
UNIT = 20


class GameBoard:

    def __init__(self, surface):
        self.surface = surface
        if BOARD_SIZE % UNIT > 0:
            print("UNIT does not evenly divide into BOARD_SIZE, unable to load game!")
            exit(0)
        self.board = []
        for i in range(0, int(BOARD_SIZE/UNIT)):
            self.board.append([])
            for j in range(0, int(BOARD_SIZE/UNIT)):
                self.board[i].append(pg.Rect(i*UNIT, j*UNIT, UNIT, UNIT))

    def place_snake(self, x, y):
        pg.draw.rect(self.surface, (0, 0, 0), self.board[y][x])

    def remove_snake(self, x, y):
        pg.draw.rect(self.surface, (255, 255, 255), self.board[y][x])


class Snake:

    def __init__(self, board):
        self.board = board
        self.head_x = int((BOARD_SIZE/UNIT)/2)
        self.head_y = self.head_x
        self.board.place_snake(self.head_x, self.head_y)
        self.length = 1
        self.body = []
        self.__moving_north = True
        self.__moving_east = None

    def move(self):
        self.body.insert(0, (int(self.head_x), int(self.head_y)))
        if self.__moving_north is not None:
            if self.__moving_north:
                self.head_y -= 1
            else:
                self.head_y += 1
        else:
            if self.__moving_east:
                self.head_x += 1
            else:
                self.head_x -= 1
        while len(self.body) > self.length - 1:
            loc = self.body.pop()
            self.board.remove_snake(loc[0], loc[1])
            if BOARD_SIZE % UNIT < self.head_x or self.head_x < 0:
                exit(0)
            if BOARD_SIZE % UNIT < self.head_y or self.head_y < 0:
                exit(0)
        self.board.place_snake(self.head_x, self.head_y)

    def move_up(self):
        self.__moving_north = True
        self.__moving_east = None

    def move_down(self):
        self.__moving_north = False
        self.__moving_east = None

    def move_left(self):
        self.__moving_north = None
        self.__moving_east = False

    def move_right(self):
        self.__moving_north = None
        self.__moving_east = True


def run_game(snake):
    game_running = True
    while game_running:
        keys_pressed = pg.key.get_pressed()
        if keys_pressed[pg.K_UP]:
            snake.move_up()
        if keys_pressed[pg.K_DOWN]:
            snake.move_down()
        if keys_pressed[pg.K_LEFT]:
            snake.move_left()
        if keys_pressed[pg.K_RIGHT]:
            snake.move_right()
        snake.move()


def main():
    pg.display.init()
    display_window = pg.display.set_mode((BOARD_SIZE, BOARD_SIZE))
    surface = pg.display.get_surface()
    run_game(Snake(GameBoard(surface)))


if __name__ == "__main__":
    main()
