from Crypto.PublicKey import RSA

Alicia = RSA.generate(1024)
f = open("PrivateKeyAlicia.pem","wb")
f.write(Alicia.exportKey("PEM"))
f.close
f = open("PublicKeyAlicia.pem","wb")
f.write(Alicia.publickey().exportKey("PEM"))
f.close


Betito = RSA.generate(1024)
f = open("PrivateKeyBetito.pem","wb")
f.write(Betito.exportKey("PEM"))
f.close
f = open("PublicKeyBetito.pem","wb")
f.write(Betito.publickey().exportKey("PEM"))
f.close


Eva = RSA.generate(1024)
f = open("PrivateKeyEva.pem","wb")
f.write(Eva.exportKey("PEM"))
f.close
f = open("PublicKeyEva.pem","wb")
f.write(Eva.publickey().exportKey("PEM"))
f.close