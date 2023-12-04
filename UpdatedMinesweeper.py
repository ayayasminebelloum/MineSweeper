from tkinter import *
import random
import time

# hn is hidden nothing
# n is unhidden nothing
# hb is hidden bomb
# b is unhidden bomb
# f is flagged cell
# fb is flagged bomb

# Moves stack
moves_stack = []

def push_move(action, i, j):
    moves_stack.append((action, i, j))

def pop_move():
    if moves_stack:
        return moves_stack.pop()
    return None

def undo_bomb():
    move = pop_move()
    if move:
        action, i, j = move
        if action == 'left-click':
            field[i][j] = 'hn'
        elif action == 'right-click':
            field[i][j] = 'hn'
        draw()

def onClick(event):
    global points, flags

    i = event.x // 20
    j = event.y // 20

    if event.num == 2:
        right_click(i, j)
    elif event.num == 1:  # Left-click
        left_click(i, j)

    print("Flags:", flags)
    print()

    if points == 30 * 16 - 60:
        print('You win!')
        print('You dismantled every bomb.')
        return
    if flags == 0 and points != 30 * 16 - 60:
        print('You lost')
        print("You didn't dismantle every bomb.")
        GameOver()
        return

def left_click(i, j):
    global points
    if field[i][j] == 'hn':
        count = countMines(i, j)
        if count > 0:
            field[i][j] = 'n'
        elif count == 0:
            floodFill(i, j)
        draw()
        push_move('left-click', i, j)
    elif field[i][j] == 'hb':
        field[i][j] = 'b'
        print('You lost')
        print('You touched a Bomb.')
        GameOver()
        return

def right_click(i, j):
    global points, flags
    if field[i][j] == 'hn':
        flags -= 1
        field[i][j] = 'fn'
    elif field[i][j] == 'hb':
        flags -= 1
        points += 1
        field[i][j] = 'fb'
    elif field[i][j] == 'fn':
        flags += 1
        field[i][j] = 'hn'
    elif field[i][j] == 'fb':
        flags += 1
        points -= 1
        field[i][j] = 'hb'
    push_move('right-click', i, j)
    draw()

def floodFill(i, j):
    if i < 0 or j < 0 or i >= 30 or j >= 16:
        return

    if field[i][j] == 'hn':
        count = countMines(i, j)
        if count > 0:
            field[i][j] = 'n'
            canvas.create_rectangle(i * 20, j * 20, i * 20 + 20, j * 20 + 20, fill='grey90')
            canvas.create_text(i * 20 + 10, j * 20 + 10, text=str(count), fill='black')
        elif count == 0:
            field[i][j] = 'n'
            for x in range(max(0, i - 1), min(30, i + 2)):
                for y in range(max(0, j - 1), min(16, j + 2)):
                    if field[x][y] == 'hn':
                        floodFill(x, y)

def GameOver():
    canvas.delete(ALL)
    for i in range(30):
        for j in range(16):
            if field[i][j] == 'hb' or field[i][j] == 'b':
                canvas.create_rectangle(i * 20, j * 20, i * 20 + 20, j * 20 + 20, fill='white')
                canvas.create_oval(i * 20, j * 20, i * 20 + 20, j * 20 + 20, fill='red')
            elif field[i][j] == 'fb':
                canvas.create_rectangle(i * 20, j * 20, i * 20 + 20, j * 20 + 20, fill='white')
                canvas.create_oval(i * 20, j * 20, i * 20 + 20, j * 20 + 20, fill='yellow')
            elif field[i][j] == 'fn':
                canvas.create_rectangle(i * 20, j * 20, i * 20 + 20, j * 20 + 20, fill='white')
                canvas.create_oval(i * 20, j * 20, i * 20 + 20, j * 20 + 20, fill='yellow')
            else:
                canvas.create_rectangle(i * 20, j * 20, i * 20 + 20, j * 20 + 20, fill='white')
    time.sleep(2)
    window.destroy()

def undo_cpu():
    move = pop_move()
    if move:
        action, i, j = move
        if action == 'left-click':
            field[i][j] = 'hn'
        elif action == 'right-click':
            field[i][j] = 'hn'
        draw()

def cpu_player():
    for i in range(30):
        for j in range(16):
            if field[i][j] == 'hn':
                left_click(i, j)
                return

def bomb_placement():
    existing_bombs = []
    while len(existing_bombs) != 60:
        x, y = random.randint(0, 29), random.randint(0, 15)
        if [x, y] not in existing_bombs:
            field[x][y] = 'hb'
            existing_bombs.append([x, y])
    return existing_bombs

def countMines(i, j):
    mines = 0
    for x in range(max(0, i - 1), min(30, i + 2)):
        for y in range(max(0, j - 1), min(16, j + 2)):
            if field[x][y] == 'hb' or field[x][y] == 'fb':
                mines += 1
    return mines

def draw():
    canvas.delete(ALL)
    for i in range(30):
        for j in range(16):
            if field[i][j] == 'hn' or field[i][j] == 'hb':
                canvas.create_rectangle(i * 20, j * 20, i * 20 + 20, j * 20 + 20, fill='lightblue')
            elif field[i][j] == 'n':
                count = countMines(i, j)
                if count > 0:
                    canvas.create_rectangle(i * 20, j * 20, i * 20 + 20, j * 20 + 20, fill='grey90')
                    canvas.create_text(i * 20 + 10, j * 20 + 10, text=str(count), fill='black')
                else:
                    floodFill(i, j)
                    canvas.create_rectangle(i * 20, j * 20, i * 20 + 20, j * 20 + 20, fill='white')
            elif field[i][j] == 'fb' or field[i][j] == 'fn':
                canvas.create_rectangle(i * 20, j * 20, i * 20 + 20, j * 20 + 20, fill='yellow')
                canvas.create_text(i * 20 + 10, j * 20 + 10, text='F', fill='black')

# GUI Setup
window = Tk()
window.title('Minesweeper')
w = 600
h = 320

canvas = Canvas(window, bg='white', height=h, width=w)
canvas.pack()

field = [['hn' for _ in range(16)] for _ in range(30)]

bomb_placement()
draw()

points = 0
flags = 60

window.bind('<Button-1>', onClick)
window.bind('<Button-2>', onClick)

undo_button = Button(window, text="Undo", command=undo_bomb)
undo_button.pack()

quit_button = Button(window, text="Quit", command=window.destroy)
quit_button.pack()

cpu_button = Button(window, text="CPU Player", command=cpu_player)
cpu_button.pack()

window.mainloop()