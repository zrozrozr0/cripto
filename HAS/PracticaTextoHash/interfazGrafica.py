from tkinter import Button, Label, filedialog as tk
from Practica5 import Hashtext

class interfazGrafica:
    def __init__(self, master) -> None:
        self.master = master
        master.title("Hash")
        self.label = Label(master, text="Eliga un archivo .txt para comenzar")
        self.label.pack(pady=20)

        self.boton_seleccionar = Button(master, text="--> Abrir <--", command=self.abrir_archivo)
        self.boton_seleccionar.pack(pady=10)

        self.boton_descifrar = Button(master, text="-> Hash <-", command=self.obtenerHash)
        self.boton_descifrar.pack(pady=10)

        self.boton_descifrar = Button(master, text="-> Verificacion <-", command=self.verificarHash)
        self.boton_descifrar.pack(pady=10)


    def abrir_archivo(self):
        self.ruta_archivo = tk.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
        self.label.configure(text=f"texto seleccionado: {self.ruta_archivo}")
        root.config(bg="gray") 

    def obtenerHash(self):
        iniciar = Hashtext(self.ruta_archivo)
        iniciar.unirHashOriginal(self.ruta_archivo)
        root.config(bg="green") 

    def verificarHash(self):
        ht = Hashtext(self.ruta_archivo)
        verifiacion  = ht.compararHashes(ht.obtenerContenHash(self.ruta_archivo),ht.obtenerHash(self.ruta_archivo))
        if verifiacion == True:
            self.label.configure(text=f"No se modifico el mensaje :)  = {verifiacion}")
            root.config(bg="green") 
        else:
            self.label.configure(text=f"Mensaje modificado ): = {verifiacion}")
            root.config(bg="red") 

root = tk.Tk()
root.geometry("800x300")  # Ajusta el tamaño de la ventana principal
root.config(bg="gray")  # Establece el color de fondo de la ventana principal
mi_interfaz = interfazGrafica(root)
root.mainloop()