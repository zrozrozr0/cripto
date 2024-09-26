import hashlib
import os

class Hashtext:
    def __init__(self, ruta):
        self.ruta = ruta
        self.contenido =  open(self.ruta, 'r')
        self.texto = self.contenido.read()


    def getContenido(self):
        return self.texto

    def hashContenido(self,texto):
        
         # Aplica la función hash SHA256 al contenido
        hash_obj = hashlib.sha256(texto.encode())

        # Obtiene el hash en formato hexadecimal
        hash_resultado = hash_obj.hexdigest()
        return hash_resultado

    def obtenerNuevaRuta(self, ruta_archivo):
        directorio = os.path.dirname(ruta_archivo)
        nombre_archivo = os.path.basename(ruta_archivo)
        nombre_sin_extension = os.path.splitext(nombre_archivo)[0]
        nueva_ruta = os.path.join(directorio, nombre_sin_extension + "_h.txt")
        return nueva_ruta
    
    
    def unirHashOriginal(self, ruta_archivo):
        with open(self.obtenerNuevaRuta(ruta_archivo), 'w') as archivo_nuevo:
            # Escribe el contenido original en el nuevo archivo
            archivo_nuevo.write(self.getContenido())
            #print(self.getContenido())
            contenido_hash = self.hashContenido(self.texto)
            # Escribe el hash en una nueva línea
            archivo_nuevo.write('$$$$' + contenido_hash)
            print("Nuevo archivo creado con éxito.")

    def obtenerHash(self, ruta):
        archivo = open(ruta, "r")
        cadena = archivo.read()
        return cadena.split("$$$$")[1]
    
    def obtenerContenHash(self, ruta):
        archivo = open(ruta, "r")
        cadena = archivo.read()
        cadena = cadena.split("$$$$")[0]
        return cadena
    
    def compararHashes(self, textoRecibido, hash):
        hashcomparacion = self.hashContenido(textoRecibido)
        if (hash == hashcomparacion):
            return True
        else: 
            return False

''' 
iniciar = Hashtext("elvis.txt")
iniciar.unirHashOriginal()
rutah = "elvis_h.txt"
iniciar.obtenerHash(rutah)
print(iniciar.compararHashes(iniciar.obtenerContenHash(rutah),iniciar.obtenerHash(rutah)))
'''
