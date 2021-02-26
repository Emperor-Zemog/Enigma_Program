# this is the main file, it class all the other files, it might be deleted if it proves unneeded
from Lampboard import Lampboard


class Machine:
    fName = ""
    pIV = b''
    pSalt = b''
    pCy_data = b''
    def set_pIV(self, iv):
        self.pIV = iv
    def get_pIV(self):
        return self.pIV
    def set_pCy_data(self,cData):
        self.pCy_data = cData
    def get_pCy_data(self):
        return self.pCy_data
    def set_pSalt(self,salt):
        self.pSalt = salt
    def get_pSalt(self):
        return self.pSalt
    def set_fName(self,name):
        print(name)
        self.fName = name
    def get_fName(self):
        print(self.fName)
        return self.fName


