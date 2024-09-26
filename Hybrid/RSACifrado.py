from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256


class RSACifrado:
    def __init__(self, llave_privada_path=None, llave_publica_path=None):
        if llave_privada_path:
            with open(llave_privada_path, "rb") as f:
                self.llave_privada = RSA.import_key(f.read())
        else:
            self.llave_privada = None
        
        if llave_publica_path:
            with open(llave_publica_path, "rb") as f:
                self.llave_publica = RSA.import_key(f.read())
        else:
            self.llave_publica = None

    def generar_llaves(self, tamano=2048):
        self.llave_privada = RSA.generate(tamano)
        self.llave_publica = self.llave_privada.publickey()

    def guardar_llave_privada(self, path):
        if self.llave_privada:
            with open(path, "wb") as f:
                f.write(self.llave_privada.export_key())

    def guardar_llave_publica(self, path):
        if self.llave_publica:
            with open(path, "wb") as f:
                f.write(self.llave_publica.export_key())

    def cifrar(self, datos):
        if self.llave_publica:
            cifrador = PKCS1_OAEP.new(self.llave_publica)
            datos_cifrados = cifrador.encrypt(datos)
            return datos_cifrados.hex()
        else:
            print("No se ha especificado una llave pública.")

    #Revisar bien los datos que se envian y recibe, en caso de que no funcione al decifrar, revisar primero aqui
    def descifrar(self, texto_cifrado):
        if self.llave_privada:
            descifrador = PKCS1_OAEP.new(self.llave_privada)
            texto_bytes = bytes.fromhex(texto_cifrado)
            texto_descifrado = descifrador.decrypt(texto_bytes)
            return texto_descifrado.decode("UTF-8")
        else:
            print("No se ha especificado una llave privada.")

    def firmar_hash(self, hash_data):
        if self.llave_privada:
            hash_obj = SHA256.new(hash_data.encode("UTF-8")) 
            firma = pkcs1_15.new(self.llave_privada).sign(hash_obj)
            return firma.hex()
        else:
            print("No se ha especificado una llave privada.")
            
    def verificar_firma(self, hash_data, firma_hex):
        if self.llave_publica:
            hash_obj = SHA256.new(hash_data.encode("UTF-8"))
            firma = bytes.fromhex(firma_hex)
            try:
                pkcs1_15.new(self.llave_publica).verify(hash_obj, firma)
                return True  # La firma es válida
            except (ValueError, TypeError):
                return False  # La firma es inválida
        else:
            print("No se ha especificado una llave pública.")
            return False

