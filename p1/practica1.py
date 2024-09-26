# ---------------- LIBRERIAS ---------------- #
from tkinter import *
import tkinter as tk
from tkinter import ttk
import os
import numpy as np
import math

# ------------ GENERACION DE LA VENTANA ------------ #
ventana = tk.Tk()
ventana.geometry("600x450")
ventana.title("Practica #1 - Cifrado Afin")


# ------------ VARIABLES GLOBALES ------------ #
valorN = tk.IntVar()
valorA = tk.IntVar()
valorB = tk.IntVar()

# ------------ CONFIGURACION GRID VENTANA ------------ #
ventana.rowconfigure(0, weight=1)
ventana.rowconfigure(1, weight=1)
ventana.rowconfigure(2, weight=1)
ventana.rowconfigure(3, weight=1)
ventana.rowconfigure(4, weight=1)
ventana.rowconfigure(5, weight=1)
ventana.rowconfigure(6, weight=1)
ventana.rowconfigure(7, weight=1)
ventana.rowconfigure(8, weight=1)
ventana.columnconfigure(0, weight=1)
ventana.columnconfigure(1, weight=1)
ventana.columnconfigure(2, weight=1)
ventana.columnconfigure(3, weight=1)
ventana.columnconfigure(4, weight=1)
ventana.columnconfigure(5, weight=1)


# ------------ ALGORITMO EXTENDIDO DE EUCLIDES ------------ #
def algoritmoExtendidoEuclides(a, b):
    if (a == 0):
        return 0, 1
    else:
        x, y = algoritmoExtendidoEuclides(b % a, a)
        return y-(b//a)*x, x


# ------------ ALGORITMO DE EUCLIDES ------------ #
def algoritmoEuclides():
    textoCarita = tk.Label(ventana, text="")
    textoCarita.grid(row=3, column=0, sticky="NSWE", columnspan=6)
    if (valorN.get() == 0 and valorA.get() == 0):
        textoCarita.config(text="ESPERANDO CAPTURA DE VALORES", fg="grey", font="Helvetica 14 italic")
        textoFuncionCifrado = tk.Label(ventana, text="")
        funcionCifrado = tk.Label(ventana, text="")
        textoFuncionDesifrado = tk.Label(ventana, text="")
        funcionDesifrado1 = tk.Label(ventana, text="")
        funcionDesifrado2 = tk.Label(ventana, text="")
        textoFuncionCifrado.grid(row=4, column=0, sticky="NSWE", columnspan=6)
        funcionCifrado.grid(row=5, column=0, sticky="NSWE", columnspan=6)
        textoFuncionDesifrado.grid(row=6, column=0, sticky="NSWE", columnspan=6)
        funcionDesifrado1.grid(row=7, column=0, sticky="NSWE", columnspan=6)
        funcionDesifrado2.grid(row=8, column=0, sticky="NSWE", columnspan=6)
    elif (math.gcd(valorN.get(), valorA.get()) == 1):
        textoCarita.config(text="VALOR EXISTENTE  ヽ(•‿•)ノ", fg="green", font="Helvetica 14 italic")
        x, y = algoritmoExtendidoEuclides(valorA.get(), valorN.get())
        print(f'x = {x}, y = {y}')
        textoFuncionCifrado = tk.Label(ventana, text="- Funcion de Cifrado -", fg="black", font="Helvetica 12 bold")
        cadenaCifrado = "C = " + str(valorA.get()) + "p + " + str(valorB.get()) + " mod " + str(valorN.get()) 
        funcionCifrado = tk.Label(ventana, text=cadenaCifrado, fg="black", font="Helvetica 10")
        textoFuncionDesifrado = tk.Label(ventana, text="- Funcion de Desifrado -", fg="black", font="Helvetica 12 bold")
        cadenaDescifrado1 = "P = " + str(x) + " (C + " + str(valorN.get()-valorB.get()) + ") mod " + str(valorN.get()) 
        funcionDesifrado1 = tk.Label(ventana, text=cadenaDescifrado1, fg="black", font="Helvetica 10")
        cadenaDescifrado2 = "P = " + str(x) + "C + " + str((x*(valorN.get()-valorB.get()))%valorN.get()) + " mod " + str(valorN.get()) 
        funcionDesifrado2 = tk.Label(ventana, text=cadenaDescifrado2, fg="black", font="Helvetica 10")
        textoFuncionCifrado.grid(row=4, column=0, sticky="NSWE", columnspan=6)
        textoFuncionDesifrado.grid(row=6, column=0, sticky="NSWE", columnspan=6)
        funcionCifrado.grid(row=5, column=0, sticky="NSWE", columnspan=6)
        funcionDesifrado1.grid(row=7, column=0, sticky="NSWE", columnspan=6)
        funcionDesifrado2.grid(row=8, column=0, sticky="NSWE", columnspan=6)
    else:
        textoCarita.config(text="VALOR NO EXISTENTE ( ╥_╥ ) , INTENTE CON OTRO", fg="red", font="Helvetica 14 italic")
        textoFuncionCifrado = tk.Label(ventana, text="")
        funcionCifrado = tk.Label(ventana, text="")
        textoFuncionDesifrado = tk.Label(ventana, text="")
        funcionDesifrado1 = tk.Label(ventana, text="")
        funcionDesifrado2 = tk.Label(ventana, text="")
        textoFuncionCifrado.grid(row=4, column=0, sticky="NSWE", columnspan=6)
        funcionCifrado.grid(row=5, column=0, sticky="NSWE", columnspan=6)
        textoFuncionDesifrado.grid(row=6, column=0, sticky="NSWE", columnspan=6)
        funcionDesifrado1.grid(row=7, column=0, sticky="NSWE", columnspan=6)
        funcionDesifrado2.grid(row=8, column=0, sticky="NSWE", columnspan=6)


# ------------ FUNCION PRINCIPAL ------------ #
def main():
    # Texto para los campos
    textoCampos = tk.Label(ventana, text="Capture los valores de los parametros n, alpha y beta:", fg="blue", font="Helvetica 15 bold")
    textoCampos.grid(row=0, column=0, sticky="NSWE", columnspan=6)

    # Campo para el valor de N
    textoN = tk.Label(ventana, text="n : ", fg="black", font="Helvetica 12 bold")
    textoN.grid(row=1, column=0, sticky="NSWE")
    entradaN = tk.Entry(ventana, textvariable=valorN,
                        width=20, justify=tk.CENTER, state=NORMAL)
    entradaN.grid(row=1, column=1)

    # Campo para el valor de A (alpha)
    textoA = tk.Label(ventana, text="α : ", fg="black", font="Helvetica 12 bold")
    textoA.grid(row=1, column=2, sticky="NSWE")
    entradaA = tk.Entry(ventana, textvariable=valorA,
                        width=20, justify=tk.CENTER, state=NORMAL)
    entradaA.grid(row=1, column=3)

    # Campo para el valor de B (beta)
    textoB = tk.Label(ventana, text="β : ", fg="black", font="Helvetica 12 bold")
    textoB.grid(row=1, column=4, sticky="NSWE")
    entradaB = tk.Entry(ventana, textvariable=valorB,
                        width=20, justify=tk.CENTER, state=NORMAL)
    entradaB.grid(row=1, column=5)

    # Boton para verificar por el AE
    botonVerificar = tk.Button(ventana, text="V E R I F I C A R", fg="white", bg="black", font="Helvetica 12 bold", command=algoritmoEuclides)
    botonVerificar.grid(row=2, column=2, sticky="NSWE",padx=10, pady=10, columnspan=2)

    # Ejecucion en bucle de la interfaz
    ventana.mainloop()


# ------------ INICIO DEL PROGRAMA ------------ #
main()
