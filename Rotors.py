from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
class Rotors:
    pSWord = ""
    salt = b''
    mKey = b''
    mIV = b''
    badPass = False
    def set_Password(self, pWord):
        self.pSWord = pWord
        print("password set")
    def make_salt(self):
        self.salt = get_random_bytes(32)
    def set_salt(self,iSalt):
        self.salt = iSalt
    def make_key(self):
        if self.pSWord == "":
            print("password wasn't set")
        else:
            if self.salt == b'':
                self.make_salt()
            self.mKey = PBKDF2(self.pSWord, self.salt, dkLen=32)

    def encrypt_data(self, data):
        cipher = AES.new(self.mKey, AES.MODE_CBC)  # Create a AES cipher object with the key using the mode CBC
        ciphered_data = cipher.encrypt(pad(data, AES.block_size))  # Pad the input data and then encrypt
        self.mIV = cipher.iv
        return ciphered_data
    def get_iv(self):
        return self.mIV
    def get_salt(self):
        return self.salt
    def get_badPass(self):
        return self.badPass
    def decrypt_data(self, ciphered_data,iV):
        cipher = AES.new(self.mKey, AES.MODE_CBC, iv=iV)  # Setup cipher
        original_data = unpad(cipher.decrypt(ciphered_data), AES.block_size)  # Decrypt and then up-pad the result
        self.badPass = False
        return original_data



