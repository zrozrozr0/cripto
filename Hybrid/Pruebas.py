from Hash import Hashtext
from AES_CFB import CFB_Cifrado
from RSACifrado import RSACifrado

def agregar_todo(ruta_archivo, texto, firma, vector, llave):
    with open(ruta_archivo, "w") as archivo:
        #archivo.write(texto)
        archivo.write(texto)
        print("Se agrego correctamente el texto.")
        
        archivo.write('\nFirma:' + firma)
        print("Archivo firmado.")

        archivo.write('\nLlave:' + llave)
        print("Se agrego correctamente ela llave.")

        archivo.write('\nVector:' + vector)
        print("Se agrego correctamente el vector.")

        

def unir_firma_texto (ruta_archivo, firma):
        with open(ruta_archivo, "a") as archivo:
            #archivo.write(texto)
            archivo.write('\nFirma:' + firma)
            print("Archivo firmado.")

def unir_vector_cifrado (ruta_archivo, vector):
    with open(ruta_archivo, "a") as archivo:
        #archivo.write(texto)
        archivo.write('\nVector:' + vector)
        print("Se agrego correctamente el vector.")
        
def unir_llave_cifrado (ruta_archivo, llave):
    with open(ruta_archivo, "a") as archivo:
        #archivo.write(texto)
        archivo.write('\nLlave:' + llave)
        print("Se agrego correctamente ela llave.")

def obtener_texto(ruta_archivo):
     with open(ruta_archivo, "r") as archivo:
        #archivo.write(texto)
        return archivo.read()
     
def separar_archivo(texto):
    return texto.split("\n")


c_hash = Hashtext("elvis.txt")
texto_plano =  c_hash.getContenido()
hash_texto = c_hash.hashContenido(texto_plano)
print("Este es el hash del texto: ", hash_texto)

llave = str(97846) #se generan aleatoriamnete
vector = str(9278346)
aes = CFB_Cifrado(texto_plano, llave, vector)
texto_cifrado = aes.cifrar_texto()
#print("Texto cifrado: ",  texto_cifrado)

cifrador = RSACifrado()
cifrador.generar_llaves()
cifrador.guardar_llave_privada("llave_privada_Alicia.pem")
cifrador.guardar_llave_publica("llave_publica_Alicia.pem")
# Firmar un hash usando la llave privada
firma = cifrador.firmar_hash(texto_plano)
#print("Firma, el hash cifrado: ", firma)

ruta = "elvis_RSA_c.txt"
agregar_todo(ruta, texto_cifrado, firma, cifrador.cifrar(aes.get_iv()), cifrador.cifrar(aes.get_llave()) )
# unir_firma_texto(ruta,firma)
# unir_llave_cifrado(ruta,cifrador.cifrar(aes.get_llave()))
# unir_vector_cifrado(ruta,cifrador.cifrar(aes.get_iv()))


texto_cifrado = obtener_texto(ruta)
lista_obejetos = separar_archivo(texto_cifrado)
#el 0: texto, 1:firma , 2 y 3 llave y vector
texto_c = lista_obejetos[0]
firma_c = lista_obejetos[1]
llave_c = lista_obejetos[2]
iv_c = lista_obejetos[3]

# print(llave_c)
llave_d = cifrador.descifrar(llave_c.split(":")[1])
# print(llave_d)
iv_d = cifrador.descifrar(iv_c.split(":")[1])


tetxo_d = aes.decifrar_texto(texto_c, llave_d, iv_d)
#print(tetxo_d) si funciono
#firma_d = cifrador.descifrar(firma_c.split(":")[1]) No se necesetia por la funcion

if ( cifrador.verificar_firma(tetxo_d, firma_c.split(":")[1]) ):
    print(f'NO se ha modificado el archivo')
else:
    print("Error archivo modificado")
# texto_original = "Hola, este es un texto de prueba."
# texto_cifrado = cifrador.cifrar_texto(texto_original)
# print("Texto cifrado:", texto_cifrado)

# # Descifrar texto usando la llave privada
# texto_descifrado = cifrador.descifrar_texto(texto_cifrado)
# print("Texto descifrado:", texto_descifrado)

