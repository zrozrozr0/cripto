from hashlib import md5
from base64 import b64decode
from base64 import b64encode
from Crypto.Cipher import AES, PKCS1_OAEP
import random
import string
from typing import KeysView
from Crypto import PublicKey
import Crypto
from Crypto.PublicKey import RSA
from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme
from Crypto.Hash import SHA256
import binascii
from Crypto.Random import get_random_bytes
from Crypto import Random
import ast
import base64
from os import remove
# Padding for the input string --not
# related to encryption itself.
BLOCK_SIZE = 16  # Bytes
def pad(s): return s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * \
    chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)


def unpad(s): return s[:-ord(s[len(s) - 1:])]


# Este cacho es del AES


class AESCipher:

    def __init__(self, key):
        self.key = md5(key.encode('utf8')).hexdigest()

    def encrypt(self, raw):
        raw = pad(raw)
        cipher = AES.new(self.key.encode("utf8"), AES.MODE_ECB)
        return b64encode(cipher.encrypt(raw.encode('utf8')))

    def decrypt(self, enc):
        enc = b64decode(enc)
        cipher = AES.new(self.key.encode("utf8"), AES.MODE_ECB)
        return unpad(cipher.decrypt(enc)).decode('utf8')


def random_char(y):
    return ''.join(random.choice(string.ascii_letters) for x in range(y))
# cifra el texto con el aes


def cifrarTexto(Mensaje):
    mensaje = openFile(Mensaje)
    pwd = random_char(16)
    c = AESCipher(pwd).encrypt(mensaje)
    out = open('cifrado.txt', 'wb')
    out.write(c)
    out.write(b'\n--------------------------------------\n')
    out.close()
    return pwd
# descifra el texto completo, incluyendo la llave


def descifrarTexto(msgfile,pwd):
    archivo = open(msgfile, "r", encoding="ISO-8859-1")
    msg_sign = str(archivo.read())
    msgaux = msg_sign.split('\n--------------------------------------\n')
    mensaje = str(msgaux[0])
    p = AESCipher(pwd).decrypt(mensaje)
    out = open('descifrado.txt', 'w')
    out.write(p)
    out.write('\n--------------------------------------\n')
    out.write(pwd)
    out.write('\n--------------------------------------\n')
    out.close()


def cifrarcontra(pwd,pub_key):
    contra = pwd
    data = contra
    data = str.encode(data)
    out = open('cifrado.txt', 'a', encoding="ISO-8859-1")
    rsa_public_key = RSA.import_key(
        open(pub_key).read())
    rsa_public_key = PKCS1_OAEP.new(rsa_public_key)
    encrypted_text = rsa_public_key.encrypt(data)
    aux = encrypted_text
    out.write(encrypted_text.decode("ISO-8859-1"))
    out.write('\n--------------------------------------\n')
    out.close()


def sacarLlave(msgfile):
    archivo = open(msgfile, "r", encoding="ISO-8859-1")
    msg_sign = str(archivo.read())
    msgaux = msg_sign.split('\n--------------------------------------\n')
    aux = str(msgaux[1])
    archivo.close()
    out = open('cifradocontra.txt', 'w', encoding="ISO-8859-1")
    out.write(aux)
    out.close()


def descifrarcontra(msgfile,priv_key):
    sacarLlave(msgfile)
    file_in = open("cifradocontra.txt", "r", encoding="ISO-8859-1")
    encrypted_text = file_in.read().encode("ISO-8859-1")
    rsa_private_key = RSA.import_key(
        open(priv_key).read())
    rsa_private_key = PKCS1_OAEP.new(rsa_private_key)
    try:
        decrypted_text = rsa_private_key.decrypt(encrypted_text)
        return decrypted_text.decode("utf-8")
    except:
        return "mamadas"


def openFile(filename):
    f = open(filename, "r", encoding="ISO-8859-1")
    mensaje = f.read()
    f.close
    return mensaje


def signature(msgfile, priv_key):
    msg = str(openFile(msgfile))
    hash = SHA256.new(msg.encode())
    try:
        keyPair = RSA.importKey(openFile(priv_key))
        signer = PKCS115_SigScheme(keyPair)
        signature = signer.sign(hash)
        signature_hex = signature.hex()
        divider_message_sign = "_/_/"
        f = open("message_signed.txt", "w", encoding="ISO-8859-1")
        f.write(msg+divider_message_sign+signature_hex)
        f.close()
        print("File signed successfully")
    except:
        print("Something went wrong")


def validate(msg_sign_file, pub_key):
    msg_sign = str(openFile(msg_sign_file))
    index_divider = msg_sign.find('_/_/')
    msg = msg_sign[0:index_divider].encode()
    hash = SHA256.new(msg)
    pubKey = RSA.importKey(openFile(pub_key))
    verifier = PKCS115_SigScheme(pubKey)
    try:
        signature = msg_sign[index_divider+4:]
        verifier.verify(hash, bytearray.fromhex(signature))
        print("Signature is valid.")
    except:
        print("Signature is invalid.")


def auxcifrar(Mensaje,priv_key,pub_key):
    contra = cifrarTexto(Mensaje)
    cifrarcontra(contra,pub_key)
    contra = descifrarcontra("cifrado.txt",priv_key)
    #print("contra: ",contra)
    if(contra == "mamadas"):
        auxcifrar()

def C_S(msgfile, priv_key,pubkfile):
    try:
        auxcifrar(msgfile,priv_key,pubkfile)
        signature("cifrado.txt", priv_key)
        remove("cifradocontra.txt")
        remove("cifrado.txt")
        return "Everything's fine"
    except:
        return "Something went wrong"

def D_V(msgfile, priv_key,pubkfile):
    try:
        contra = descifrarcontra(msgfile,priv_key)
        descifrarTexto(msgfile,contra)
        print("Archivo descifrado correctamente")
        remove("cifradocontra.txt")
        validate(msgfile,pubkfile)
        return "Valid sign, decipher txt generated"
    except:
        return "Something went wrong"
