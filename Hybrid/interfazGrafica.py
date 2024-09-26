import os
from tkinter import Button, Entry, Frame, Label, filedialog as tk
from Hash import Hashtext
from RSACifrado import RSACifrado
from AES_CFB import CFB_Cifrado


class InterfazGrafica:
     
    def __init__(self, master):
        self.master = master
        master.title("Cifrado Hibrido")

        # Crear un contenedor Frame
        self.frame = Frame(master)
        self.frame.pack(padx=30, pady=30)

        self.label = Label(self.frame, text="Seleccione un archivo")
        self.label.pack()

        self.boton_seleccionar = Button(self.frame, text="Seleccionar...", command=self.abrir_archivo)
        self.boton_seleccionar.pack(pady=10)

        #Este regularmente es la publica para quien envia, privada para quien recibe
        self.label1 = Label(self.frame, text="Seleccione una llave para cifrar o decifrar")
        self.label1.pack()

        self.boton_seleccionar_pub = Button(self.frame, text="Seleccionar...", command=self.abrir_pem_publica)
        self.boton_seleccionar_pub.pack(pady=10)

        self.label2 = Label(self.frame, text="Seleccione una llave para firmar o verificar")
        self.label2.pack()
        #Este regularmente es la publica para quien envia, privada para quien recibe
        self.boton_seleccionar_priv = Button(self.frame, text="Seleccionar llave privada", command=self.abrir_pem_privada)
        self.boton_seleccionar_priv.pack(pady=10)

        self.boton_cifrar = Button(self.frame, text="Cifrar y firmar", command=self.cifrar_firmar)
        self.boton_cifrar.pack(pady=10)

        self.boton_descifrar = Button(self.frame, text="Descifrar y Verificar", command=self.descifrar_verificar)
        self.boton_descifrar.pack(pady=10)

    def abrir_archivo(self):
        self.ruta_archivo = tk.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
        self.label.configure(text=f"Archivo seleccionado: {self.ruta_archivo}")
        
    def abrir_pem_publica(self):
        self.ruta_publica = tk.askopenfilename(filetypes=[("Archivos PEM", "*.pem")])
        self.label1.configure(text=f"Llave pública seleccionada: {self.ruta_publica}")
        
    def abrir_pem_privada(self):
        self.ruta_privada = tk.askopenfilename(filetypes=[("Archivos PEM", "*.pem")])
        self.label2.configure(text=f"Llave privada seleccionada: {self.ruta_privada}")

    def cifrar_firmar(self):
        try:
            c_hash = Hashtext(self.ruta_archivo)
            texto_plano =  c_hash.getContenido()
            hash_texto = c_hash.hashContenido(texto_plano)
            llave = str(97846) #se generan aleatoriamente
            vector = str(9278346)
            aes = CFB_Cifrado(texto_plano, llave, vector)
            texto_cifrado = aes.cifrar_texto()

            cifrador = RSACifrado(self.ruta_privada, self.ruta_publica)
            # cifrador.generar_llaves()
            # cifrador.guardar_llave_privada("llave_privada_Alicia.pem")
            # cifrador.guardar_llave_publica("llave_publica_Alicia.pem")
            
            firma = cifrador.firmar_hash(texto_plano)
            
            ruta = c_hash.obtenerNuevaRuta(self.ruta_archivo)
            agregar_todo(ruta, texto_cifrado, firma, cifrador.cifrar(aes.get_iv()), cifrador.cifrar(aes.get_llave()) )
            
            self.label.configure(text="Cifrado y firma digital realizados con éxito.")
        except Exception as e:
            self.label.configure(text=f"Error durante el cifrado y firma: {str(e)}")
    
    
    def descifrar_verificar(self):
        try:
            texto_cifrado = obtener_texto(self.ruta_archivo)
            lista_objetos = separar_archivo(texto_cifrado)
            cifrador = RSACifrado(self.ruta_publica, self.ruta_privada)
            
            texto_c = lista_objetos[0]
            firma_c = lista_objetos[1]
            llave_c = lista_objetos[2]
            iv_c = lista_objetos[3]

            llave_d = cifrador.descifrar(llave_c.split(":")[1])
            iv_d = cifrador.descifrar(iv_c.split(":")[1])
            aes = CFB_Cifrado(" ", llave_d, iv_d)

            tetxo_d = aes.decifrar_texto(texto_c, llave_d, iv_d)
            guarda_decifrado(self.ruta_archivo,tetxo_d)

            if cifrador.verificar_firma(tetxo_d, firma_c.split(":")[1]):
                self.label = Label(self.master, text="El archivo no ha sido modificado, salvado con exito")
                self.label.pack()
                
            else:
                self.label = Label(self.master, text="Error de coincidencia de firma : El archivo ha sido modificado")
                self.label.pack()
        except Exception as e:
            self.label.configure(text=f"Error durante el descifrado y verificación, posible modificacion del archivo")
        
def guarda_decifrado(ruta_archivo, texto):
    directorio = os.path.dirname(ruta_archivo)
    nombre_archivo = os.path.basename(ruta_archivo)
    nombre_sin_extension = os.path.splitext(nombre_archivo)[0]
    nueva_ruta = os.path.join(directorio, nombre_sin_extension + "_d.txt")
    
    with open(nueva_ruta, 'w') as archivo_nuevo:
            # Escribe el contenido original en el nuevo archivo
            archivo_nuevo.write(texto)
            #print(self.getContenido())
    
    



def agregar_todo(ruta_archivo, texto, firma, vector, llave):
    try:
        with open(ruta_archivo, "w") as archivo:
            archivo.write(texto)
            print("Se agregó correctamente el texto.")
            
            archivo.write('\nFirma:' + firma)
            print("Archivo firmado.")

            archivo.write('\nLlave:' + llave)
            print("Se agregó correctamente la llave.")

            archivo.write('\nVector:' + vector)
            print("Se agregó correctamente el vector.")
    except Exception as e:
        print(f"Error al agregar contenido al archivo: {str(e)}")

def obtener_texto(ruta_archivo):
    try:
        with open(ruta_archivo, "r") as archivo:
            return archivo.read()
    except Exception as e:
        print(f"Error al obtener el contenido del archivo: {str(e)}")
        return ""

def separar_archivo(texto):
    return texto.split("\n")

#Creamos todas las llaves para usarlas
# cifrador1 = RSACifrado()
# cifrador1.generar_llaves()
# cifrador1.guardar_llave_privada("llave_privada_Alicia.pem")
# cifrador1.guardar_llave_publica("llave_publica_Alicia.pem")

# cifrador2 = RSACifrado()
# cifrador2.generar_llaves()
# cifrador2.guardar_llave_privada("llave_privada_Betito.pem")
# cifrador2.guardar_llave_publica("llave_publica_Betito.pem")

# cifrador3 = RSACifrado()
# cifrador3.generar_llaves()
# cifrador3.guardar_llave_privada("llave_privada_Candy.pem")
# cifrador3.guardar_llave_publica("llave_publica_Candy.pem")

root = tk.Tk()
mi_interfaz = InterfazGrafica(root)
root.mainloop()
