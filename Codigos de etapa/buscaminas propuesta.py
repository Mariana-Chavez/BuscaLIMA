import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random

class BuscaminasGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Buscaminas")
        self.nivel = None
        self.filas = 0
        self.columnas = 0
        self.bombas = {}
        self.tablero = []
        self.botones = []
        self.imagen_bomba = Image.open("img/bomba3.png")  
        self.imagen_bandera = Image.open("img/bandera.png")  
        
        self.menu_nivel()
        self.frame_tablero = tk.Frame(self.master)  
        self.frame_tablero.pack()

    def menu_nivel(self):
        self.nivel = tk.StringVar()

        label = tk.Label(self.master, text="Selecciona un nivel:")
        label.pack()

        facil = tk.Radiobutton(self.master, text="Fácil", variable=self.nivel, value="facil", command=self.iniciar_juego)
        facil.pack()
        intermedio = tk.Radiobutton(self.master, text="Intermedio", variable=self.nivel, value="intermedio", command=self.iniciar_juego)
        intermedio.pack()
        dificil = tk.Radiobutton(self.master, text="Difícil", variable=self.nivel, value="dificil", command=self.iniciar_juego)
        dificil.pack()

    def iniciar_juego(self):
        self.filas, self.columnas = self.obtener_tamanio_tablero()
        self.generar_tablero()
        self.colocar_bombas()
        self.mostrar_tablero()

    def obtener_tamanio_tablero(self):
        if self.nivel.get() == "facil":
            return 8, 8
        elif self.nivel.get() == "intermedio":
            return 12, 12
        elif self.nivel.get() == "dificil":
            return 16, 16
        else:
            return 0, 0

    def generar_tablero(self):
        self.tablero = [[' ' for _ in range(self.columnas)] for _ in range(self.filas)]

    def colocar_bombas(self):
        num_bombas = self.filas * self.columnas // 6
        bombas = random.sample(range(self.filas * self.columnas), num_bombas)

        for posicion in bombas:
            fila = posicion // self.columnas
            columna = posicion % self.columnas
            self.bombas[(fila, columna)] = True

    def mostrar_tablero(self):
        for boton in self.botones:
            boton.destroy()
        self.botones.clear
        for fila in range(self.filas):
            for columna in range(self.columnas):
                boton = tk.Button(self.frame_tablero, width=3, height=1, command=lambda f=fila, c=columna: self.revelar_casilla(f, c))
                boton.grid(row=fila, column=columna)
                self.botones.append(boton)
           

    def mostrar_bombas(self):
        for (fila, columna) in self.bombas:
            label = tk.Label(self.frame_tablero)
            imagen = ImageTk.PhotoImage(self.imagen_bomba)
            label.image = imagen
            label.configure(image=imagen)
            label.grid(row=fila, column=columna)
            
    def encontrar_boton(self, fila, columna):
        return self.botones[fila*sel.columnas + columna]

    def revelar_casilla(self, fila, columna):
        if (fila, columna) in self.bombas:
            self.mostrar_bombas()
            messagebox.showinfo("¡Perdiste!", "¡Has perdido! 😞")
            self.reiniciar_juego()
        else:
            bombas_adyacentes = self.contar_bombas_adyacentes(fila, columna)
            boton = self.encontrar_boton(fila, columna)
            if bombas_adyacentes > 0:
                boton.config(text=str(bombas_adyacentes))
            else:
                self.revelar_casillas_adyacentes_vacias(fila, columna)

    def contar_bombas_adyacentes(self, fila, columna):
        bombas_adyacentes = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                nueva_fila = fila + i
                nueva_columna = columna + j
                if 0 <= nueva_fila < self.filas and 0 <= nueva_columna < self.columnas:
                    if (nueva_fila, nueva_columna)  in self.bombas:
                        bombas_adyacentes +=1
        return bombas_adyacentes
        
    def revelar_casillas_adyacentes_vacias(self, fila, columna):
        for i in range(-1, 2):
            for j in range(-1, 2):
                nueva_fila = fila + i
                nueva_columna = columna + j
                if 0 <= nueva_fila < self.filas and 0 <= nueva_columna < self.columnas:
                    boton = self.encontrar_boton(nueva_fila, nueva_columna)
                    if boton and boton.cget('text')==' ':
                        self.revelar_casilla(nueva_fila, nueva_columna)
             
    def reiniciar_juego(self):
        for boton in self.botones:
            boton.destroy()
        self.botones.clear()
        self.menu_nivel()

def main():
    root = tk.Tk()
    buscaminas = BuscaminasGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
