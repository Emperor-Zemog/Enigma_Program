# This Class Takes in the encrypted file and return it in clear text/ vis versa
import os
from contextlib import suppress
class Lampboard:
    fName = ""
    bFileName = "P47.txt"
    mFileName = "D13.txt"
    mPasList = []
    pSalt = b''
    pIV = b''

    def bWrite_pFile(self,pFileName,salt,inVec,cid_Data):
        pFile = open(pFileName, "wb")
        pFile.write(inVec) #16 bytes
        print(inVec)
        pFile.write(salt) #32 bytes
        print(salt)
        pFile.write(cid_Data)
        print(cid_Data)
        pFile.close()
        print("write to " + pFileName + " was successful")
    def bLoad_pFile(self,pFileName):
        cid_Data = b''
        if os.stat(pFileName).st_size > 0:
            pFile = open(pFileName, "rb")
            self.pIV = pFile.read(16)
            self.pSalt = pFile.read(32)
            cid_Data = pFile.read()
            pFile.close()
            print(pFileName+" Loaded")
        else:
            print(pFileName+ " is empty")
        return cid_Data
    def get_pIV(self):
        return self.pIV
    def get_pSalt(self):
        return self.pSalt
    def bClear_pFile(self, pFileName):
        if os.stat(pFileName).st_size > 0:
            pFile = open(pFileName, "wb").close()
            print(pFileName+" is clear")
        else:
            print (pFileName+" is already clear")