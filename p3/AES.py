# ---------------- LIBRERIAS ---------------- #
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from PIL import Image, ImageFilter
from Crypto.Cipher import AES
import os


# ---------------- CLASE PARA LA APLICACION GENERADA ---------------- #
class Application(Frame):

    # ------------ INICIAMOS LA APLICACION ------------ #
    def __init__(self, master=None):
        super().__init__(master)

        # ------- CONFIGURACION GRID VENTANA ------- #
        self.rowconfigure(0, minsize=1)
        self.rowconfigure(1, minsize=1)
        self.rowconfigure(2, minsize=1)
        self.rowconfigure(3, minsize=1)
        self.rowconfigure(4, minsize=1)
        self.rowconfigure(5, minsize=1)
        self.rowconfigure(6, minsize=1)
        self.rowconfigure(7, minsize=1)
        self.rowconfigure(8, minsize=1)
        self.rowconfigure(9, minsize=1)
        self.rowconfigure(10, minsize=1)
        self.rowconfigure(11, minsize=1)
        self.rowconfigure(12, minsize=1)
        self.rowconfigure(13, minsize=1)
        self.rowconfigure(14, minsize=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)

        # ------- CONFIGURACION DE LA VENTANA ------- #
        self.master = master
        self.master.title("PRACTICA #4 CIFRADO/DESCIFRADO AES (BMP)")
        self.master.geometry('550x390')
        self.pack(fill=BOTH, expand=True)

        # Espacio en blanco.
        self.espacio = Label(self, text="").grid(row=0, column=0, sticky="NSWE", columnspan=4)

        # Titulo de la practica.
        self.key_label = Label(self, text="PRACTICA #4\nCIFRADOR/DESCIFRADOR AES EN IMAGENES BMP", foreground="blue", font=("Comic Sans MS bold", 16))
        self.key_label.grid(row=1, column=0, sticky="NSWE", columnspan=4)

        # Espacio en blanco.
        self.espacio = Label(self, text="").grid(row=2, column=0, sticky="NSWE", columnspan=4)

        # Campo para la captura de la llave.
        self.key_label = Label(self, text="Capture la llave : ", foreground="black", font=("Comic Sans MS bold", 12))
        self.key_label.grid(row=3, column=1, sticky="W")
        self.key_entry = Entry(self, width=15, justify="center", foreground="black", font=("Comic Sans MS", 12))
        self.key_entry.grid(row=3, column=2, sticky="NSWE")

        # Espacio en blanco.
        self.espacio = Label(self, text="").grid(row=4, column=0, sticky="NSWE", columnspan=4)

        # Campo para la captura del vector inicial.
        self.iv_label = Label(self, text="Capture el C0 : ", foreground="black", font=("Comic Sans MS bold", 12))
        self.iv_label.grid(row=5, column=1, sticky="W")
        self.iv_entry = Entry(self, width=15, justify="center", foreground="black", font=("Comic Sans MS", 12))
        self.iv_entry.grid(row=5, column=2, sticky="NSWE")

        # Espacio en blanco.
        self.espacio = Label(self, text="").grid(row=6, column=0, sticky="NSWE", columnspan=4)

        # Campo para seleccionar la accion a realizar (CIFRAR, DESCIFRAR).
        self.encrypt_label = Label(self, text="Seleccione la acción : ", foreground="black", font=("Comic Sans MS bold", 12))
        self.encrypt_label.grid(row=7, column=1, sticky="W")
        self.encrypt_combobox = ttk.Combobox(self, width=15, state="readonly", values=["CIRFRAR", "DESCIFRAR"], justify="center", foreground="black", font=("Comic Sans MS", 12))
        self.encrypt_combobox.current(0)
        self.encrypt_combobox.grid(row=7, column=2, sticky="WE")

        # Espacio en blanco.
        self.espacio = Label(self, text="").grid(row=8, column=0, sticky="NSWE", columnspan=4)

        # Campo para seleccionar el modo a utilizar (ECB, CBC, CFB, OFB).
        self.mode_label = Label(self, text="Seleccione el modo : ",foreground="black", font=("Comic Sans MS bold", 12))
        self.mode_label.grid(row=9, column=1, sticky="W")
        self.mode_combobox = ttk.Combobox(self, width=15, state="readonly", values=["ECB", "CBC", "CFB", "OFB"], justify="center", foreground="black", font=("Comic Sans MS", 12))
        self.mode_combobox.current(0)
        self.mode_combobox.grid(row=9, column=2, sticky="WE")
        
        # Espacio en blanco.
        self.espacio = Label(self, text="").grid(row=10, column=0, sticky="NSWE", columnspan=4)

        # Boton para seleecionar la imagen con la que se va a trabajar.
        self.file_choose_button = tk.Button(self, text="SELECCIONAR IMAGEN", command=self.seleccionarImagen, fg="white", bg="black", font="Helvetica 10 bold")
        self.file_choose_button.grid(row=11, column=1, sticky="NS", columnspan=2, ipadx=10)

        # Espacio en blanco.
        self.espacio = Label(self, text="").grid(row=12, column=0, sticky="NSWE", columnspan=4)

        # Boton para iniciar la ejecucion del programa, cifrando o descifrando la imagen.
        self.start_button = tk.Button(self, text="LISTO", command=self.ejecutar, fg="white", bg="black", font="Helvetica 10 bold")
        self.start_button.grid(row=13, column=1, sticky="NS", columnspan=2, ipadx=10)

        # Espacio en blanco.
        self.espacio = Label(self, text="").grid(row=14, column=0, sticky="NSWE", columnspan=4)


    # ------- FUNCION PARA SELECCIONAR LA IMAGEN POR MEDIO DE UNA VENTANA ------- #
    def seleccionarImagen(self):
        # Ventana auxiliar del gestor de archivos.
        self.filename = askopenfilename(filetypes=(("Bitmap File", "*.bmp"), ("All Files", "*.*")), title="Elige una imagen BMP")

    
    # ------- FUNCION PARA SELECCIONAR EJECUTAR LA ACCION SELECCIONADA ------- #
    def ejecutar(self):
        # Variables auxiliares.
        key = self.key_entry.get()  # Llave.
        iv = self.iv_entry.get()    # Vector inicial.
        function = self.encrypt_combobox.get()  # Accion a realizar.
        mode = self.mode_combobox.get()     # Modo a utilizar.

        # Obtenemos la llave.
        try:
            int_k = int(key)
        except:
            messagebox.showinfo("Error", "La llave debe ser un valor numerico entero")
            return

        # El vector inicial no se utiliza en el modo ECB.
        if mode != 'ECB' and not iv.strip():
            messagebox.showinfo("Error", "El vector inicial no es valido")
            return

        # Para cada accion enviamos el modo, la llave y el vector inicial.
        if function == 'CIRFRAR':
            self.encrypt_file(mode, key, iv)
        else:
            self.decrypt_file(mode, key, iv)


    # ------- FUNCION PARA CIFRAR ------- #
    def encrypt_file(self, mode, key, iv):
        # Convertimos la imagen, por medio del RGB.
        try:
            image = Image.open(self.filename).convert('RGB')
        except AttributeError:
            messagebox.showinfo("Error", "Seleccione una imagen.")
            return

        # Variables auxiliares.
        image_array = bytes(image.tobytes())    # Arreglo de bytes de la imagen.
        filename_w_ext = os.path.basename(self.filename)    # Extension de la imagen.
        filename, file_extension = os.path.splitext(filename_w_ext) # Nombre de la imagen.

        # Creacion de la  nueva imagen CIFRADA.
        image_array = self.aesCipher(key, image_array, mode, 'CIRFRAR', iv)
        Image.frombytes("RGB", image.size, image_array, "raw", "RGB").save("EK"+"_"+filename+"_"+mode+".bmp", format='BMP')

        # Mensaje para confirmar que se cifro correctamente.
        messagebox.showinfo("Completado", "La imagen ha sido cifrada con exito.")


    # ------- FUNCION PARA DESCIFRAR ------- #
    def decrypt_file(self, mode, key, iv):
        # Convertimos la imagen, por medio del RGB.
        try:
            image = Image.open(self.filename).convert('RGB')
        except AttributeError:
            messagebox.showinfo("Error", "Seleccione una imagen.")
            return

        # Variables auxiliares.
        image_array = bytes(image.tobytes())
        filename_w_ext = os.path.basename(self.filename)
        filename, file_extension = os.path.splitext(filename_w_ext)
        slash = filename.split("_")
        x = ""

        # Analizamos la cadena
        if (len(slash) > 1):
            x = slash[1]
        else:
            x = slash[0]

        # Creacion de la nueva imagen DESCIFRADA.
        image_array = self.aesCipher(key, image_array, mode, 'DESCIFRAR', iv)
        Image.frombytes("RGB", image.size, image_array, "raw", "RGB").save("DK"+"_"+filename+"_"+mode+".bmp", format='BMP')

        # Mensjae para confirmar que se descifro correcta,ente.
        messagebox.showinfo("Completado", "La imagen ha sido descifrada con exito.")


    # ------- FUNCION AUXILIAR PARA EL CIFRADOR AES ------- #
    def aesCipher(self, key, data, mode, function, iv):
        # Asignamos el modo que nos ofrece la libreria AES
        if (mode == 'ECB'):
            tempCipher = AES.new(self.toUtf8(self.padKeyAes(key)), AES.MODE_ECB)
        elif (mode == 'CBC'):
            tempCipher = AES.new(self.toUtf8(self.padKeyAes(key)), AES.MODE_CBC, self.toUtf8(self.padIV(iv, 'AES')))
        elif (mode == 'OFB'):
            tempCipher = AES.new(self.toUtf8(self.padKeyAes(key)), AES.MODE_OFB, self.toUtf8(self.padIV(iv, 'AES')))
        elif (mode == 'CFB'):
            tempCipher = AES.new(self.toUtf8(self.padKeyAes(key)), AES.MODE_CFB, self.toUtf8(self.padIV(iv, 'AES')))

        return tempCipher.encrypt(self.pad(data, 'AES')) if (function == 'CIRFRAR') else tempCipher.decrypt(self.pad(data, 'AES'))


    # ------- FUNCION PARA DEFINIR EL FORMATO A UTILIZAR ------- #
    def toUtf8(self, data):
        return data.encode('UTF-8')


    # ------- FUNCION PARA EL RELLENO DEPENDIENDO DE LA LLAVE ------- #
    def padKeyAes(self, key):
        # Variables auxiliares.
        paddedKey = self.pad(key.encode(), 'AES').decode()

        # Comprobamos que la llave sea de longitud 16.
        if (len(paddedKey) != 16):
            messagebox.showinfo("PROBLEMA", "La llave debe de tener una longitud de 16 caracteres numericos")
            if (len(paddedKey) > 16):
                return paddedKey[:16]

        return self.pad(key.encode(), 'AES').decode()


    # ------- FUNCION PARA EL RELLENO DEPENDIENDO DEL VECTOR INICIAL ------- #
    def padIV(self, iv, mode):
        # Variables auxiliares.
        padded_IV = self.pad(iv.encode(), mode).decode()

        # Comprobamos que el vector sea de longitud permitida.
        if (mode == 'AES' and len(padded_IV) > AES.block_size):
            return padded_IV[:AES.block_size]
        
        return padded_IV

    
    # ------- FUNCION PARA EL RELLENO ------- #
    def pad(self, data, mode):
        # Variables auxiliares.
        length = (AES.block_size - len(data)) % AES.block_size

        return data + bytes([length])*length


# ------- GENERACION DE LA VENTANA ------- #
root = Tk()
app = Application(master=root)
app.mainloop()