# ---------------- LIBRERIAS ---------------- #
from tkinter import *
import tkinter as tk
from tkinter import ttk
import os
import numpy as np
import math
from tkinter import filedialog, messagebox
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

# ------------ GENERACION DE LA VENTANA ------------ #
ventana = tk.Tk()
ventana.geometry("550x220")
ventana.title("Practica #2 - Cifrado/Descifrado RSA")


# ------------ VARIABLES GLOBALES ------------ #
valorNombre = tk.StringVar()
valorRuta = tk.StringVar()
nombreArchivo = tk.StringVar()


# ------------ CONFIGURACION GRID VENTANA ------------ #
ventana.rowconfigure(0, minsize=1)
ventana.rowconfigure(1, minsize=1)
ventana.rowconfigure(2, minsize=1)
ventana.rowconfigure(3, minsize=1)
ventana.rowconfigure(4, minsize=1)
ventana.rowconfigure(5, minsize=1)
ventana.rowconfigure(6, minsize=1)
ventana.rowconfigure(7, minsize=1)
ventana.rowconfigure(8, minsize=1)
ventana.columnconfigure(0, weight=1)
ventana.columnconfigure(1, weight=1)
ventana.columnconfigure(2, weight=1)
ventana.columnconfigure(3, weight=1)
ventana.columnconfigure(4, weight=1)

# ------------ FUNCION PARA PROCESAR EL ARCHIVO SELECCIONADO ------------ #
def procesar_archivo(operacion):
    # Declaracion del mensaje
    textoMensaje = tk.Label(ventana, text="", fg="grey", font="Helvetica 15 italic")
    textoMensaje.grid(row=7, column=0, sticky="NSWE", columnspan=5)

    # Obtener la ruta del archivo seleccionado
    archivo = filedialog.askopenfilename()

    # Pedir al usuario que seleccione el archivo de la clave correspondiente
    if operacion == 'cifrar':
        titulo = 'SELECCIONE LA CLAVE PUBLICA'
    else:
        titulo = 'SELECCIONE LA CLAVE PRIVADA'
    archivo_clave = filedialog.askopenfilename(title=titulo)

    # Leer el contenido del archivo de la clave
    with open(archivo_clave, 'rb') as f:
        clave_bytes = f.read()
    
    # Deserializar la clave
    if operacion == 'cifrar':
        clave = serialization.load_pem_public_key(clave_bytes)
    else:
        clave = serialization.load_pem_private_key(clave_bytes, password=None)
    
    # Leer el contenido del archivo seleccionado
    with open(archivo, 'rb') as f:
        texto = f.read()
    
    # Realizar la operación de cifrado o descifrado
    if operacion == 'cifrar':
        resultado = clave.encrypt(texto, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
        archivo_salida = 'texto_cifrado.txt'
        # Mostrar un mensaje de éxito
        textoMensaje.config(text="EL ARCHIVO SE CIFRO CON EXITO", fg="green", font="Helvetica 15 italic")
    else:
        resultado = clave.decrypt(texto, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
        archivo_salida = 'texto_descifrado.bin'
        # Mostrar un mensaje de éxito
        textoMensaje.config(text="EL ARCHIVO SE DESCIFRO CON EXITO", fg="green", font="Helvetica 15 italic")
    
    # Guardar el resultado en un archivo
    with open(archivo_salida, 'wb') as f:
        f.write(resultado)


# ------------ FUNCION PARA GENERAR LA CLAVE PUBLICA Y PRIVADA ------------ #
def generar_claves():
        # Declaracion del mensaje
        textoMensaje = tk.Label(ventana, text="", fg="grey", font="Helvetica 15 italic")
        textoMensaje.grid(row=7, column=0, sticky="NSWE", columnspan=5)
        
        # Se debe de capturar el campo de nombre para poder generar el nombre de la clave
        if(valorNombre.get()!=""):
            # Generar un par de claves RSA
            clave_privada = rsa.generate_private_key(public_exponent=65537, key_size=2048)
            clave_publica = clave_privada.public_key()

            # Guardar la clave privada en un archivo
            nombreArchivo = valorNombre.get() + "_clave_privada.pem"
            with open(nombreArchivo, "wb") as f:
                f.write(clave_privada.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.PKCS8, encryption_algorithm=serialization.NoEncryption()))

            # Guardar la clave pública en un archivo
            nombreArchivo = valorNombre.get() + "_clave_publica.pem"
            with open(nombreArchivo, "wb") as f:
                f.write(clave_publica.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo))
            
            # Mostrar un mensaje de éxito
            textoMensaje.config(text="CLAVES GENERADAS CON EXITO", fg="green", font="Helvetica 15 italic")

        # Si no se capturo ningun nombre no se realiza ninguna funcion de creacion de clave.
        else:
            textoMensaje.config(text="FALTA NOMRE DE USUARIO", fg="red", font="Helvetica 15 italic")
            pass
        


# ------------ FUNCION PRINCIPAL ------------ #
def main():
    # Campo en blanco.
    espacio = tk.Label(ventana)
    espacio.grid(row=0, column=0, sticky="NSWE", columnspan=5)

    # Texto para los campos
    textoTitulo = tk.Label(ventana, text="PRACTICA #2 - CIFRADO/DESCIFRADO RSA", fg="blue", font="Helvetica 15 bold")
    textoTitulo.grid(row=1, column=0, sticky="NSWE", columnspan=5)

    # Campo en blanco.
    espacio = tk.Label(ventana)
    espacio.grid(row=2, column=0, sticky="NSWE", columnspan=5)

    # Campo para capturar el nombre de usuario y generar las llaves de usuario.
    textoNombre = tk.Label(ventana, text="Nombre Usuario:", fg="black", font="Helvetica 10 bold")
    textoNombre.grid(row=3, column=1, sticky="NSW")
    entradaNombre = tk.Entry(ventana, textvariable=valorNombre, width=20, justify=tk.CENTER, state="normal")
    entradaNombre.grid(row=3, column=2,sticky="NSWE")
    botonGenerarLlave = tk.Button(ventana, text="GENERAR CLAVES", fg="white", bg="cyan4", font="Helvetica 8 bold",command=generar_claves)
    botonGenerarLlave.grid(row=3, column=3, sticky="NS")

    # Campo en blanco.
    espacio = tk.Label(ventana)
    espacio.grid(row=4, column=0, sticky="NSWE", columnspan=5)
    
    # Campo para botones de Cifrado y Descifrado
    botonCifrar = tk.Button(ventana, text="CIFRAR", fg="black", bg="lime green", font="Helvetica 10 bold", command=lambda: procesar_archivo('cifrar'))
    botonCifrar.grid(row=5, column=1, sticky="NSE",ipadx=10)
    botonDescifrar = tk.Button(ventana, text="DESCIFRAR", fg="black", bg="lime green", font="Helvetica 10 bold", command=lambda: procesar_archivo('descifrar'))
    botonDescifrar.grid(row=5, column=3, sticky="NSW",ipadx=10)

    # Campo en blanco.
    espacio = tk.Label(ventana)
    espacio.grid(row=6, column=0, sticky="NSWE", columnspan=5)

    # Campo para el mensaje.
    textoMensaje = tk.Label(ventana, text="", fg="grey", font="Helvetica 15 italic")
    textoMensaje.grid(row=7, column=0, sticky="NSWE", columnspan=5)

    # Campo en blanco.
    espacio = tk.Label(ventana)
    espacio.grid(row=8, column=0, sticky="NSWE", columnspan=5)

    # Ejecucion en bucle de la interfaz
    ventana.mainloop()


# ------------ INICIO DEL PROGRAMA ------------ #
main()
