import pygame as pg
import numpy as np
import sys

pg.init()

WIDTH, HEIGHT = 1000, 800
DISPLAY = pg.display.set_mode((WIDTH, HEIGHT))
side = 7  # coefficient to adjust size of board - bigger "side" = smaller board

board = np.zeros((6, 7))

turn = 1  # player 1 turn

t = 100  # fall speed of piece in seconds

fps = 60
clock = pg.time.Clock()


class Button:
    def __init__(self, text, x, y, width, height, colour, font, thick, curve):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour
        self.font = font
        self.thick = thick
        self.curve = curve

    def draw(self, win):
        pg.draw.rect(win, self.colour, (self.x, self.y, self.width, self.height), self.thick, self.curve)
        f, fs = self.font
        font = pg.font.SysFont(f, fs)
        text = font.render(self.text, True, (255, 255, 255))
        win.blit(text, (self.x + round(self.width / 2) - round(text.get_width() / 2),
                        (self.y + round(self.height / 2) - round(text.get_height() / 2))))

    def click(self, mousePos):
        x1 = mousePos[0]
        y1 = mousePos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False


def switch_turn():
    """Switches the turn"""
    global turn
    if turn == 1:
        turn = 2
    else:
        turn = 1


def max_y(c):
    """Determines the lowest position that the piece can go"""
    for y in range(len(board)):
        if board[y][c] != 0:
            return y
    return len(board)


def drop(c, y, maxY):
    """Recursive function that makes the piece drop"""
    global place_buttons
    if y < maxY:
        if y > 0:
            board[y - 1][c] = 0
        board[y][c] = turn
        display()
        pg.time.wait(t)
        return drop(c, y + 1, maxY)
    else:
        place_buttons = True
        display()
        switch_turn()
        return y - 1


def check_win(x, y):
    """After every turn, checks if the player has won"""
    switch_turn()

    # horizontal check
    s, i, j = 1, x, y
    while i > 0 and board[j][i - 1] == turn:
        i -= 1
        s += 1
    i, j = x, y
    while i < len(board[0]) - 1 and board[j][i + 1] == turn:
        i += 1
        s += 1
    if s >= 4:
        return True

    # vertical check
    s, i, j = 1, x, y
    while j > 0 and board[j - 1][i] == turn:
        j -= 1
        s += 1
    i, j = x, y
    while j < len(board) - 1 and board[j + 1][i] == turn:
        j += 1
        s += 1
    if s >= 4:
        return True

    # diagonal check 1
    s, i, j = 1, x, y
    while i > 0 and j > 0 and board[j - 1][i - 1] == turn:
        i -= 1
        j -= 1
        s += 1
    i, j = x, y
    while i < len(board[0]) - 1 and j < len(board) - 1 and board[j + 1][i + 1] == turn:
        i += 1
        j += 1
        s += 1
    if s >= 4:
        return True

    # diagonal check 2
    s, i, j = 1, x, y
    while i > 0 and j < len(board) - 1 and board[j + 1][i - 1] == turn:
        i -= 1
        j += 1
        s += 1
    i, j = x, y
    while i < len(board[0]) - 1 and j > 0 and board[j - 1][i + 1] == turn:
        i += 1
        j -= 1
        s += 1
    if s >= 4:
        return True
    switch_turn()
    return False


def play(c):
    """Called when someone pressed a button"""
    global turn, place_buttons
    if board[0][c] == 0:
        place_buttons = False
        pg.display.update()

        y = drop(c, 0, max_y(c))

        if check_win(c, y):
            print(f"Player {turn} wins!")
            pg.quit()
            sys.exit()


def display():
    """Displays the board"""
    pg.draw.rect(DISPLAY, (0, 0, 255), (100, 145, WIDTH - 200, HEIGHT - 170))

    for y in range(len(board)):
        for x in range(len(board[y])):
            if board[y][x] == 0:
                pg.draw.circle(DISPLAY, (255, 255, 255),
                               ((WIDTH - 300) / side * x + 205, (WIDTH - 300) / side * y + 205), 40)
            elif board[y][x] == 1:
                pg.draw.circle(DISPLAY, (100, 50, 150),
                               ((WIDTH - 300) / side * x + 205, (WIDTH - 300) / side * y + 205), 40)
            elif board[y][x] == 2:
                pg.draw.circle(DISPLAY, (255, 223, 0),
                               ((WIDTH - 300) / side * x + 205, (WIDTH - 300) / side * y + 205), 40)

    if place_buttons:
        for btn in column_buttons:
            btn.draw(DISPLAY)
    clearboard.draw(DISPLAY)

    pg.display.update()


def clear_board():
    """Resets the game"""
    global board, turn, place_buttons
    board = np.zeros((6, 7))
    turn = 1
    place_buttons = True
    display()


column_buttons = [Button(f"{i+1}", 168 + i * 100, 100, 75, 35, (180, 180, 180), ("lucidaconsole", 15), 0, 30)
                  for i in range(7)]

clearboard = Button("Clear", 455, 20, 100, 50, (150, 150, 150), ("lucidaconsole", 15), 0, 20)

place_buttons = True

# Main Game loop
while True:
    clock.tick(fps)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

        if event.type == pg.MOUSEBUTTONDOWN:
            pos = pg.mouse.get_pos()
            for i in range(len(column_buttons)):
                if column_buttons[i].click(pos):
                    play(i)
            if clearboard.click(pos):
                clear_board()

    display()