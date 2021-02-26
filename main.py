# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from Lampboard import Lampboard
from Rotors import Rotors
pList = ["a", "b", "c"]
cList =[]
tWord = "hello there"
tCWord = ""
tUCWord = ""

tKey="athena"
oList = []
bList = []
lBoard = Lampboard()
rot = Rotors()
print(tWord)
tCWord = rot.encrypt(tKey, tWord)
print(tCWord)
tUCWord = rot.decrypt(tKey, tCWord)
print (tUCWord)
## lBoard.write_to_mFile(pList)
## oList = lBoard.read_mFile()
## bList = lBoard.read_bFile()


# Press the green button in the gutter to run the script.


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
