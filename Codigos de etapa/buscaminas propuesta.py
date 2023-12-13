import tkinter as tk
from tkinter import *
from tkinter import messagebox
import random
import time

#-----------------Dashboard Generator----------------

#Default level (easy)
WIDTH, HEIGHT, BOMB_COUNT = 6, 6, 6

root = Tk()
frame = Frame(root)
frame.pack()
root.title("Buscaminas")
root.iconbitmap("../img/bomba.ico")
root.resizable(False, False)
frame.config(width=400, height=400)


#-----------------Time counter----------------


#Variables
time_start = 0
time_label = None
time_active = True

def start_time():
    """ This function starts the time for the counter """
    global time_start
    time_start = time.time()
    update_time()

def update_time():
    """ This function updates the time every time you restart or change levels """
    global time_active
    if time_active:
        time_elapsed = round(time.time() - time_start)
        time_label.config(text=f"Tiempo: {time_elapsed}s")
        root.after(1000, update_time)


#--------------------Dropdown menu-------------------

def create_menu():
    """ This function creates the dropdown menu to choose between three levels """
    menu_bar = Menu(frame)
    root.config(menu=menu_bar)

    difficulty_menu = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Dificultad", menu=difficulty_menu)
    difficulty_menu.add_command(label="Facil", command=lambda: set_difficulty(6, 6, 6))
    difficulty_menu.add_command(label="Intermedio", command=lambda: set_difficulty(7, 7, 8))
    difficulty_menu.add_command(label="Dificil", command=lambda: set_difficulty(9, 9, 10))

def set_difficulty(width, height, bomb_count):
    """This feature changes the difficulty of the game"""
    global WIDTH, HEIGHT, BOMB_COUNT
    WIDTH, HEIGHT, BOMB_COUNT = width, height, bomb_count
    clear_board()
    create_board()

#---------------------Game board-----------------------

def clear_board():
    """This function is responsible for cleaning the board and resetting some variables"""
    global buttons, time_label
    for i in range(len(buttons)):
        for j in range(len(buttons[i])):
            if buttons[i][j] is not None:
                buttons[i][j].unbind("<Button-1>")
                buttons[i][j].unbind("<Button-3>")
                buttons[i][j].destroy()
                buttons[i][j] = None
    if time_label is not None:
        time_label.destroy()


def create_board():
    """This function is responsible for initializing and displaying the game board in the graphical interface"""
    global board, buttons, flags, time_label, time_active
    board = [[0] *  WIDTH for _ in range(HEIGHT)]
    flags = [[False] * WIDTH for _ in range(HEIGHT)]
    place_bombs()
    calculate_numbers()

    buttons = [[None] * WIDTH for _ in range(HEIGHT)]

    for i in range(HEIGHT):
        for j in range(WIDTH):
            buttons[i][j] = Button(frame, text="", width=6, height=3, font=("Arial 12 bold"))
            buttons[i][j].bind("<Button-1>", lambda event, i=i, j=j: on_left_click(i, j))
            buttons[i][j].bind("<Button-3>", lambda event, i=i, j=j: on_right_click(i, j))
            buttons[i][j].grid(row=i, column=j)

    time_label = Label(frame, text="Tiempo: 0s", font=("Arial 12 bold"))
    time_label.grid(row=HEIGHT, columnspan=WIDTH)
    start_time()

#----------------------------Mines------------------------

def place_bombs():
    """This function places the bombs on the board"""
    bombs_placed = 0
    while bombs_placed < BOMB_COUNT:
        x, y = random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1)
        if board[y][x] != -1:
            board[y][x] = -1
            bombs_placed += 1

def calculate_numbers():
    """this function counts how many mines there are in adjacent cells."""
    for i in range(HEIGHT):
        for j in range(WIDTH):
            if board[i][j] == -1:
                continue
            for x in range(-1, 2):
                for y in range(-1, 2):
                    if 0 <= i + y < HEIGHT and 0 <= j + x < WIDTH and board[i + y][j + x] == -1:
                        board[i][j] += 1

#--------------------------Game controls--------------------

def on_left_click(i, j):
    """This function creates one of the game controls, such that we create a function for left click and calls the game_over() function if the clicked cell contains a mine"""
    if board[i][j] == -1:
        game_over()
    elif board[i][j] == 0:
        visited = set()
        reveal_empty_cells(i, j, visited)
    else:
        buttons[i][j].config(text=str(board[i][j]))
        buttons[i][j].config(state=tk.NORMAL)

banderaImgSlot = PhotoImage(file="../img/banderaSlot.png") 
imagenTransparente = PhotoImage(file../img/imagenTransparente.png")


def on_right_click(i, j):
    """This function creates one of the game controls, such that places a flag in a cell or removes it"""
    if buttons[i][j]["state"] == tk.NORMAL:
        if not flags[i][j]:
            buttons[i][j].config(image=banderaImgSlot, width=64, height=65)
            flags[i][j] = True
        else:
            buttons[i][j].config(image=imagenTransparente, text="")
            flags[i][j] = False


#-------------------------------------Reveal empty cells-------------------------------------


def reveal_empty_cells(i, j, visited):
    """ Function that reveals the cells where there is a zero or better known as empty cells """
    if (0 <= i < HEIGHT and 0 <= j < WIDTH and
            buttons[i][j]["state"] == tk.NORMAL and
            (i, j) not in visited):
        visited.add((i, j))
        if board[i][j] == 0:
            buttons[i][j].config(state=tk.DISABLED, text="")
            for x in range(-1, 2):
                for y in range(-1, 2):
                    reveal_empty_cells(i + y, j + x, visited)
        elif 0 < board[i][j] < 9:
            buttons[i][j].config(state=tk.DISABLED, text=str(board[i][j]))


#-------------------------------------Win-------------------------------------

def check_win():
    """ Function that verifies if you have won """
    cells_without_bomb = [buttons[i][j]["state"] == tk.DISABLED for i in range(HEIGHT) for j in range(WIDTH)]
    if all(cells_without_bomb):
        messagebox.showinfo("¡Felicidades!", f"¡Has ganado!")
    response = messagebox.askyesno("Fin del Juego", f"¡Has perdido!\n¿Quieres volver a jugar?")
    if response:
        restart_game()
    else:
        root.destroy()


#-------------------------------------Game Over-------------------------------------

imagenBomba= PhotoImage(file="../img/bomba3.png") #Definimos la imagen de la bomba que deseemos que se muestra

def game_over():
    """ Function that indicates when you lose """"
    global time_active
    time_active = False

    for i in range(HEIGHT):
        for j in range(WIDTH):
            if board[i][j] == -1:
                buttons[i][j].config(image=imagenBomba, width=64, height=65, bg="#f17070")
            else:
                buttons[i][j].config(state=tk.DISABLED) 
    response = messagebox.askyesno("Fin del Juego", f"¡Has perdido!\n¿Quieres volver a jugar?") #Shows you a message to know if you want to play
    if response:
        restart_game()
    else:
        root.destroy()


#-----------------------------Reset game-------------------------

def restart_game():
    """ Function to restart the game """
    global time_active
    time_active = True  # Reactivate the timer
    clear_board()
    create_board()
    start_time()  # Start the timer again


#-----------Shows the graphical interface of the game-------

if __name__ == "__main__":
    create_menu()
    create_board()
    root.mainloop()

