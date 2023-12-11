import tkinter as tk
from tkinter import *
from tkinter import messagebox
import random
import time

ANCHO, ALTO, CANTIDAD_BOMBAS = 6, 6, 6
COLORES = {
    0: "light green", 
    1: "light green",        
    2: "light green",
    3: "light green",
    4: "light green"}

root = Tk()
frame = Frame(root)
frame.pack()
root.title("Buscaminas")
root.iconbitmap("../img/bomba.ico")
root.resizable(False, False)
frame.config(width=400, height=400)

# Contador de tiempo
tiempo_inicio = 0
tiempo_label = None
tiempo_activo= True

def iniciar_tiempo():
    global tiempo_inicio
    tiempo_inicio = time.time()
    actualizar_tiempo()

def actualizar_tiempo():
    global tiempo_activo
    if tiempo_activo:
        tiempo_transcurrido = round(time.time() - tiempo_inicio)
        tiempo_label.config(text=f"Tiempo: {tiempo_transcurrido}s")
        root.after(1000, actualizar_tiempo)

def crear_menu():
    menu_bar = Menu(frame)
    root.config(menu=menu_bar)

    menu_dificultad = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Dificultad", menu=menu_dificultad)
    menu_dificultad.add_command(label="Fácil", command=lambda: establecer_dificultad(6, 6, 6))
    menu_dificultad.add_command(label="Intermedio", command=lambda: establecer_dificultad(8, 8, 8))
    menu_dificultad.add_command(label="Difícil", command=lambda: establecer_dificultad(10, 10, 10))

def establecer_dificultad(ancho, alto, cantidad_bombas):
    global ANCHO, ALTO, CANTIDAD_BOMBAS
    ANCHO, ALTO, CANTIDAD_BOMBAS = ancho, alto, cantidad_bombas
    limpiar_tablero()
    crear_tablero()

def limpiar_tablero():
    global botones, tiempo_label
    for i in range(len(botones)):
        for j in range(len(botones[i])):
            if botones[i][j] is not None:
                botones[i][j].unbind("<Button-1>")
                botones[i][j].unbind("<Button-3>")
                botones[i][j].destroy()
                botones[i][j] = None
    if tiempo_label is not None:
        tiempo_label.destroy()

def crear_tablero():
    global tablero, botones, banderas, tiempo_label, tiempo_activo
    tablero = [[0] * ANCHO for _ in range(ALTO)]
    banderas = [[False] * ANCHO for _ in range(ALTO)]
    place_bombs()
    calculate_numbers()

    botones = [[None] * ANCHO for _ in range(ALTO)]

    for i in range(ALTO):
        for j in range(ANCHO):
            botones[i][j] = Button(frame, text="", width=6, height=3, font=("Arial 12 bold"))
            botones[i][j].bind("<Button-1>", lambda event, i=i, j=j: on_left_click(i, j))
            botones[i][j].bind("<Button-3>", lambda event, i=i, j=j: on_right_click(i, j))
            botones[i][j].grid(row=i, column=j)

    tiempo_label = Label(frame, text="Tiempo: 0s", font=("Arial 12 bold"))
    tiempo_label.grid(row=ALTO, columnspan=ANCHO)
    iniciar_tiempo()

def place_bombs():
    bombs_placed = 0
    while bombs_placed < CANTIDAD_BOMBAS:
        x, y = random.randint(0, ANCHO - 1), random.randint(0, ALTO - 1)
        if tablero[y][x] != -1:
            tablero[y][x] = -1
            bombs_placed += 1

def calculate_numbers():
    for i in range(ALTO):
        for j in range(ANCHO):
            if tablero[i][j] == -1:
                continue
            for x in range(-1, 2):
                for y in range(-1, 2):
                    if 0 <= i + y < ALTO and 0 <= j + x < ANCHO and tablero[i + y][j + x] == -1:
                        tablero[i][j] += 1

def on_left_click(i, j):
    if tablero[i][j] == -1:
        game_over()
    elif tablero[i][j] == 0:
        visited = set()
        reveal_empty_cells(i, j, visited)
    else:
        botones[i][j].config(text=str(tablero[i][j]), bg=COLORES.get(tablero[i][j], "light green"))
        botones[i][j].config(state=tk.DISABLED)

banderaImgSlot = PhotoImage(file="../img/banderaSlot.png")
imagenTransparente = PhotoImage(file="../img/imagenTransparente.png")

def on_right_click(i, j):
    if botones[i][j]["state"] == tk.NORMAL:
        if not banderas[i][j]:
            botones[i][j].config(image=banderaImgSlot, width=64, height=65)
            banderas[i][j] = True
        else:
            botones[i][j].config(image=imagenTransparente, text="")
            banderas[i][j] = False

def reveal_empty_cells(i, j, visited):
    if (0 <= i < ALTO and 0 <= j < ANCHO and
            botones[i][j]["state"] == tk.NORMAL and
            (i, j) not in visited):
        visited.add((i, j))
        if tablero[i][j] == 0:
            botones[i][j].config(state=tk.DISABLED, text="", bg=COLORES[0])
            for x in range(-1, 2):
                for y in range(-1, 2):
                    reveal_empty_cells(i + y, j + x, visited)
        elif 0 < tablero[i][j] < 9:
            botones[i][j].config(state=tk.DISABLED, text=str(tablero[i][j]), bg=COLORES[tablero[i][j]])

def verificar_victoria():
    celdas_sin_bomba = [botones[i][j]["state"] == tk.DISABLED for i in range(ALTO) for j in range(ANCHO)]
    if all(celdas_sin_bomba):
        messagebox.showinfo("¡Felicidades!", f"¡Has ganado en {tiempo_label.cget('text').split()[1]}!")
        root.destroy()

imagenBomba = PhotoImage(file="../img/bomba3.png")

def game_over():
    global tiempo_activo
    tiempo_activo = False
    
    for i in range(ALTO):
        for j in range(ANCHO):
            if tablero[i][j] == -1:
                botones[i][j].config(image=imagenBomba, width=64, height=65, bg="#f17070", state=tk.DISABLED)
            else:
                botones[i][j].config(state=tk.DISABLED)
    respuesta = messagebox.askyesno("Fin del Juego", f"¡Has perdido!\n¿Quieres volver a jugar?")
    if respuesta == True:
        reiniciar_juego()
    else:
        root.destroy()

def reiniciar_juego():
    limpiar_tablero()
    crear_tablero()

if __name__ == "__main__":
    crear_menu()
    crear_tablero()
    root.mainloop()
