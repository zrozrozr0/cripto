from typing import KeysView
from Crypto import PublicKey
import Crypto
from Crypto.PublicKey import RSA
from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme
from Crypto.Hash import SHA256
import binascii

def openFile(filename):
    f=open(filename,"r")
    mensaje=f.read()
    f.close
    return mensaje

def signature(msgfile, priv_key):
    msg=str(openFile(msgfile))
    hash = SHA256.new(msg.encode())
    try:
        keyPair = RSA.importKey(openFile(priv_key))
        signer = PKCS115_SigScheme(keyPair)
        signature = signer.sign(hash)
        signature_hex = signature.hex()
        divider_message_sign = "_/_/"
        f = open("message_signed.txt","w")
        f.write(msg+divider_message_sign+signature_hex)
        f.close
        return "File signed successfully"
    except:
        return "Something went wrong"

def validate(msg_sign_file, pub_key):
    msg_sign = str(openFile(msg_sign_file))
    index_divider = msg_sign.find('_/_/')
    msg=msg_sign[0:index_divider].encode()
    hash = SHA256.new(msg)
    pubKey = RSA.importKey(openFile(pub_key))
    verifier = PKCS115_SigScheme(pubKey)
    try:
        signature = msg_sign[index_divider+4:]
        verifier.verify(hash, bytearray.fromhex(signature))
        return "Signature is valid."
    except:
        return "Signature is invalid." 