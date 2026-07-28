import os
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

class CryptoEngine():

    def __init__(self, key, nonce_size):
        self.__KEY = base64.b64decode(key)
        self.__NonceSize = nonce_size           #Nonce size
        self.__aesgcm = AESGCM(self.__KEY)

    @staticmethod
    def generate_key(byteSize: int) -> str:
        return base64.b64encode(os.urandom(byteSize)).decode()

    def encrypt(self, plainText: str) -> str:
        nonce = os.urandom(self.__NonceSize)
        ciperText = self.__aesgcm.encrypt(nonce, plainText.encode(), associated_data=None)
        return base64.b64encode( nonce+ciperText ).decode()

    def decrypt(self, EnMsg :str) -> str | None:
        raw = base64.b64decode(EnMsg)
        nonce, ciper = raw[:self.__NonceSize], raw[self.__NonceSize:]
        return self.__aesgcm.decrypt(nonce, ciper, associated_data=None).decode()

