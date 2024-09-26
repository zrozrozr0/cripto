import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

BLOCK_SIZE = 16  # Bytes


class CFB_Cifrado:
    def __init__(self, texto, llave, vector):
        self.texto = texto
        
        # self.key = get_random_bytes(BLOCK_SIZE)
        # self.iv = get_random_bytes(BLOCK_SIZE)

        self.key = pad(bytes(llave, "UTF-8"), BLOCK_SIZE)  # El Aes es de 128 bytes
        #self.key = bytes(llave, "UTF-8")  # El Aes es de 128 bytes
        self.iv = pad(bytes(vector, "UTF-8"), BLOCK_SIZE)
        
    def get_llave(self):
        return self.key

    def get_iv(self):
        return self.iv

    def cifrar_texto(self):
        if self.key is not None:
            print("Se está cifrando...")
            cipher = AES.new(self.key, AES.MODE_CFB, self.iv)

            ct_bytes = cipher.encrypt(pad(bytes(self.texto, "UTF-8"), BLOCK_SIZE))
            ct_texto = ct_bytes.hex()
            
            print("Proceso terminado")
            return ct_texto
        else:
            print("Llave no válida")

    def decifrar_texto(self, texto_cifrado, llave, vector):
        print("Se está descifrando...")
        llave_b = bytes(llave, "UTF-8")
        vector_b = bytes(vector, "UTF-8")
        decipher = AES.new(llave_b, AES.MODE_CFB, vector_b)
        ct_bytes = bytes.fromhex(texto_cifrado)
        
        pt_bytes = unpad(decipher.decrypt(ct_bytes), BLOCK_SIZE)
        texto_descifrado = pt_bytes.decode("UTF-8")
        
        print("Descifrado terminado")
        return texto_descifrado

