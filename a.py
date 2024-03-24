from cryptography.fernet import Fernet

def keygener():
    key = Fernet.generate_key()
    return key

def keysave(key,id):
    with open(f'.\\keys\\{id}.key',"wb") as keyfile:
        keyfile.write(key)

def keyload(id):
    with open(f'.\\keys\\{id}.key','rb') as keyfile:
        lk = keyfile.read()
    return lk

def encrypt(txt,key,nickname):
    suite = Fernet(key)
    keysave(key,nickname)
    return suite.encrypt(txt)

def decrypt(txt,nickname):
    key = keyload(nickname)
    suite = Fernet(key)
    return suite.decrypt(txt)
