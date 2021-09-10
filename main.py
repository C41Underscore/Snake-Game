import pygame as pg
from queue import Queue
from time import sleep
from random import randint

BOARD_SIZE = 400
UNIT = 20


class GameBoard:

    def __init__(self, surface):
        self.current_marker = (None, None)
        self.surface = surface
        if BOARD_SIZE % UNIT > 0:
            print("UNIT does not evenly divide into BOARD_SIZE, unable to load game!")
            exit(0)
        self.board = []
        for i in range(0, int(BOARD_SIZE/UNIT)):
            self.board.append([])
            for j in range(0, int(BOARD_SIZE/UNIT)):
                self.board[i].append(pg.Rect(i*UNIT, j*UNIT, UNIT, UNIT))
        self.place_marker()

    def place_snake(self, x, y):
        if x < 0 or y < 0 or x > int(BOARD_SIZE/UNIT) or y > int(BOARD_SIZE/UNIT):
            print("Snake went out of bounds!")
            exit(0)
        pg.draw.rect(self.surface, (255, 255, 255), self.board[y][x])
        if self.current_marker == (x, y):
            self.place_marker()
            pg.display.update(self.board[y][x])
            return True
        pg.display.update(self.board[y][x])
        return False

    def remove_snake(self, x, y):
        pg.draw.rect(self.surface, (0, 0, 0), self.board[y][x])
        pg.display.update(self.board[y][x])

    def place_marker(self):
        r_x = randint(1, int((BOARD_SIZE/UNIT) - 1))
        r_y = randint(1, int((BOARD_SIZE/UNIT) - 1))
        pg.draw.rect(self.surface, (255, 0, 0), self.board[r_y][r_x])
        pg.display.update(self.board[r_y][r_x])
        self.current_marker = (r_x, r_y)
        print(self.current_marker)


class Snake:

    def __init__(self, board):
        self.board = board
        self.head_x = int((BOARD_SIZE/UNIT)/2)
        self.head_y = self.head_x
        self.board.place_snake(self.head_x, self.head_y)
        self.length = 1
        self.body = []
        self.__direction = randint(0, 3)

    def move(self, up, down, left, right):
        self.body.append((int(self.head_x), int(self.head_y)))
        if up:
            self.head_x -= 1
            self.__direction = 0
        if down:
            self.head_x += 1
            self.__direction = 1
        if left:
            self.head_y -= 1
            self.__direction = 2
        if right:
            self.head_y += 1
            self.__direction = 3
        if up == down == left == right == 0:
            if self.__direction == 0:
                self.head_x -= 1
            elif self.__direction == 1:
                self.head_x += 1
            elif self.__direction == 2:
                self.head_y -= 1
            elif self.__direction == 3:
                self.head_y += 1
        if (self.head_x, self.head_y) in self.body:
            print("You went over yourself!")
            exit(0)
        if self.board.place_snake(self.head_x, self.head_y):
            self.length += 1
        while len(self.body) > self.length - 1:
            loc = self.body.pop(0)
            self.board.remove_snake(loc[0], loc[1])


def run_game(snake):
    game_running = True
    while game_running:
        pg.event.pump()
        keys_pressed = pg.key.get_pressed()
        snake.move(keys_pressed[pg.K_UP], keys_pressed[pg.K_DOWN], keys_pressed[pg.K_LEFT], keys_pressed[pg.K_RIGHT])
        sleep(0.1)


def main():
    pg.display.init()
    display_window = pg.display.set_mode((BOARD_SIZE, BOARD_SIZE))
    surface = pg.display.get_surface()
    run_game(Snake(GameBoard(surface)))


if __name__ == "__main__":
    main()
