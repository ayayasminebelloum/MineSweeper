from tkinter import *
import random

# hn is hidden nothing
# n is unhidden nothing
# hb is hidden bomb
# b is unhidden bomb
# f is flagged cell


def onClick(event): #this is the clicking function, its wired to the left/right click, it runs everytime you click on canvas
    global points, flags

    i = event.x // 20
    j = event.y // 20

    if event.num == 1:  # Left-click
        if field[i][j] == 'hn': #if you click on a hidden nothing it reveals nothing, checks if there bombs around
            count = countMines(i, j)
            if count > 0: 
                field[i][j] = 'n'
            elif count == 0:
                floodFill(i, j)
        elif field[i][j] == 'hb': #if you click on a hidden bomb it reveals the bomb
            field[i][j] = 'b'
            GameOver()
            print('You lost')
            print('You touched a Bomb.')
            return
        draw()
    elif event.num == 2:  # right-click
        if field[i][j] == 'hn': #if you flag nothing, it becomes a flag
            flags-=1
            field[i][j] = 'f'
        elif field[i][j] == 'hb':#if you flag a hidden bomb, it becomes a flagged bomb
            flags-=1
            points+=1
            field[i][j] = 'fb'
        elif field[i][j] == 'f':#if you reflag a flag it becomes nothing
            flags+=1
            field[i][j] = 'hn'
        elif field[i][j] == 'fb':#if you reflag a flagged bomb it becomes a hidden bomb
            flags+=1
            field[i][j] = 'hb'
        draw()

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

def floodFill(i, j):
    if i < 0 or j < 0 or i >= 30 or j >= 16:
        return

    if field[i][j] == 'hn':
        count = countMines(i, j)
        if count > 0:
            field[i][j] = 'n'

            # draws the number
            canvas.create_rectangle(i * 20, j * 20, i * 20 + 20, j * 20 + 20, fill='grey90')
            canvas.create_text(i * 20 + 10, j * 20 + 10, text=str(count), fill='black')
            
        elif count == 0:
            field[i][j] = 'n'

            # does the floodfill
            for x in range(max(0, i - 1), min(30, i + 2)):
                for y in range(max(0, j - 1), min(16, j + 2)):
                    if field[x][y] == 'hn':
                        floodFill(x, y)


def draw(): # this is the drawing function, it redraws the canvas everytime you click in case there are changes
    canvas.delete(ALL)
    for i in range(30):
        for j in range(16):
            if field[i][j] == 'hn' or field[i][j] == 'hb':  # this draws lightblue blocks, wether its hidden nothing or hidden bomb
                canvas.create_rectangle(i * 20, j * 20, i * 20 + 20, j * 20 + 20, fill='lightblue')
            elif field[i][j] == 'n': # this is for when its nothing
                count = countMines(i, j)
                if count > 0: # if there are mines nearby it writes the number of mines
                    canvas.create_rectangle(i * 20, j * 20, i * 20 + 20, j * 20 + 20, fill='grey90')
                    canvas.create_text(i * 20 + 10, j * 20 + 10, text=str(count), fill='black')
                else: # if no mines, drawsa white block and calls the flood fill function
                    floodFill(i, j)
                    canvas.create_rectangle(i * 20, j * 20, i * 20 + 20, j * 20 + 20, fill='white')
            if field[i][j] == 'b': # if bomb it draws a bomb
                canvas.create_rectangle(i * 20, j * 20, i * 20 + 20, j * 20 + 20, fill='white')
                canvas.create_oval(i * 20, j * 20, i * 20 + 20, j * 20 + 20, fill='red')
            if field[i][j] == 'f' or field[i][j] == 'fb': #if its a flag or flagged bomb, it draws the flag
                canvas.create_rectangle(i * 20, j * 20, i * 20 + 20, j * 20 + 20, fill='yellow')
                canvas.create_text(i * 20 + 10, j * 20 + 10, text='F', fill='black')

            #the 2 lines below are just so i can see the bombs, delete them for the normal game
#             if field[i][j] == 'hb':
#                 canvas.create_oval(i * 20, j * 20, i * 20 + 20, j * 20 + 20, fill='red')

def countMines(i, j): # function that counts nearby mines
    mines = 0
    for x in range(max(0, i - 1), min(30, i + 2)):
        for y in range(max(0, j - 1), min(16, j + 2)):
            if field[x][y] == 'hb' or field[x][y] == 'fb':
                mines += 1
    return mines

window = Tk()
window.title('Minesweeper')
w = 600
h = 320

canvas = Canvas(window, bg='white', height=h, width=w)
canvas.pack()
field = [['hn' for _ in range(16)] for _ in range(30)]

def bomb_placement(): # randomly places 60 bombs on canvas
    existing_bombs = []
    while len(existing_bombs) != 60:
        x, y = random.randint(0, 29), random.randint(0, 15)
        if [x, y] not in existing_bombs:
            field[x][y] = 'hb'
            existing_bombs.append([x, y])
    return existing_bombs

def GameOver(): #function Gameover, runs upon defeat, it reveals every hidden bomb
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

bomb_placement()
draw()

points = 0
flags = 60

window.bind('<Button-1>', onClick)
window.bind('<Button-2>', onClick)
window.mainloop()
