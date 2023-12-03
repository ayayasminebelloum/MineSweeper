from tkinter import *
import random

# hn is hidden nothing
# n is unhidden nothing
# hb is hidden bomb
# b is unhidden bomb
# f is flagged cell
# fb is flagged bomb

moves_stack = []

def push_move(action, i, j):
    moves_stack.append((action, i, j))


def pop_move():
    if moves_stack:
        return moves_stack.pop()
    return None

def calculate_move_score(cell):
    i, j = cell
    score = 0

    # Check the 3x3 neighborhood around the cell
    for x in range(max(0, i - 1), min(30, i + 2)):
        for y in range(max(0, j - 1), min(16, j + 2)):
            if field[x][y] == 'n':
                score += 1
            elif field[x][y] == 'fb':
                score -= 1
            elif field[x][y] == 'f':
                score -= 1  

    return score

def choose_greedy_move():
    best_move = None
    best_score = -1

    for i in range(30):
        for j in range(16):
            if field[i][j] == 'hn':
                score = calculate_move_score((i, j))

                if score > best_score:
                    best_score = score
                    best_move = (i, j)

    if best_move is not None:
        return best_move
    else:
        # If no safe cells found, choose a random hidden cell
        return random_hidden_cell()

def reveal_cell(cell):
    i, j = cell
    count = countMines(i, j)

    if count > 0:
        field[i][j] = 'n'
    elif count == 0:
        floodFill(i, j)

def cpu_greedy_play():
    while True:
        cell_to_click = choose_greedy_move()

        if field[cell_to_click[0]][cell_to_click[1]] == 'hb':
            print("CPU lost! Player 2 won.")
            break

        reveal_cell(cell_to_click)

        if game_won():
            print("CPU won! Game over.")
            break

def bomb_placement():
    existing_bombs = []
    while len(existing_bombs) != 60:
        x, y = random.randint(0, 29), random.randint(0, 15)
        if [x, y] not in existing_bombs:
            field[x][y] = 'hb'
            existing_bombs.append([x, y])

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
            if field[i][j] == 'b':
                canvas.create_rectangle(i * 20, j * 20, i * 20 + 20, j * 20 + 20, fill='white')
                canvas.create_oval(i * 20, j * 20, i * 20 + 20, j * 20 + 20, fill='red')
            if field[i][j] == 'f' or field[i][j] == 'fb':
                canvas.create_rectangle(i * 20, j * 20, i * 20 + 20, j * 20 + 20, fill='yellow')
                canvas.create_text(i * 20 + 10, j * 20 + 10, text='F', fill='black')

def countMines(i, j):
    mines = 0
    for x in range(max(0, i - 1), min(30, i + 2)):
        for y in range(max(0, j - 1), min(16, j + 2)):
            if field[x][y] == 'hb' or field[x][y] == 'fb':
                mines += 1
    return mines

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

def random_hidden_cell():
    empty_cells = [(i, j) for i in range(30) for j in range(16) if field[i][j] == 'hn']
    if empty_cells:
        return random.choice(empty_cells)
    return None

def game_won():
    return all(cell != 'hn' for row in field for cell in row)

window = Tk()
window.title('Minesweeper')
w = 600
h = 320

canvas = Canvas(window, bg='white', height=h, width=w)
canvas.pack()
field = [['hn' for _ in range(16)] for _ in range(30)]
moves_stack = []

bomb_placement()
draw()

points = 0
flags = 60

def GameOver():
    # Function to handle game over logic
    global canvas
    canvas.delete(ALL)
    for i in range(30):
        for j in range(16):
            if field[i][j] == 'hb' or field[i][j] == 'b':
                canvas.create_rectangle(i * 20, j * 20, i * 20 + 20, j * 20 + 20, fill='white')
                canvas.create_oval(i * 20, j * 20, i * 20 + 20, j * 20 + 20, fill='red')
            elif field[i][j] == 'fb':
                canvas.create_rectangle(i * 20, j * 20, i * 20 + 20, j * 20 + 20, fill='white')
                canvas.create_oval(i * 20, j * 20, i * 20 + 20, j * 20 + 20, fill='yellow')
            else:
                canvas.create_rectangle(i * 20, j * 20, i * 20 + 20, j * 20 + 20, fill='white')


def onClick(event):
    global points, flags

    i = event.x // 20
    j = event.y // 20

    if event.num == 1:  # Left-click
        if field[i][j] == 'hn':
            count = countMines(i, j)
            if count > 0: 
                field[i][j] = 'n'
            elif count == 0:
                floodFill(i, j)
        elif field[i][j] == 'hb':
            field[i][j] = 'b'
            GameOver()
            print('You lost')
            print('You touched a Bomb.')
            return
        draw()
        push_move('left-click', i, j)
    elif event.num == 2:  
        # Right-click
        if field[i][j] == 'hn':
            flags -= 1
            field[i][j] = 'f'
        elif field[i][j] == 'hb' and field[i][j] != 'fb':
            flags -= 1
            points += 1
            field[i][j] = 'fb'
        elif field[i][j] == 'f':
            flags += 1
            field[i][j] = 'hn'
        elif field[i][j] == 'fb':
            flags += 1
            field[i][j] = 'hb'

        draw()
        push_move('right-click', i, j)

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

def undo_bomb():
    move = pop_move()
    if move:
        action, i, j = move
        if action == 'left-click':
            field[i][j] = 'hn'
        elif action == 'right-click':
            field[i][j] = 'hn'
        draw()


window.bind('<Button-1>', onClick)
window.bind('<Button-2>', onClick)

undo_button = Button(window, text="Undo", command=pop_move)
undo_button.pack()

# Uncomment the line below if you want the CPU to play automatically
#cpu_greedy_play()

window.mainloop()
