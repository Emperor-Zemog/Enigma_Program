import PySimpleGUI as sg
import os.path
import time
from Lampboard import Lampboard
from Rotors import Rotors
from Machine import Machine
sg.theme('DarkPurple4')   # Add a touch of color
# All the stuff inside your window.
column_fileListing = [[sg.Text('Directory:'),sg.InputText(size=(25, 1), enable_events=True, key="-FOLDER-"),sg.FolderBrowse(),sg.Button('Refresh')],
                      [sg.Listbox(values=[], enable_events=True, size=(50, 20), key="-FILE LIST-")],
                      [sg.Text('File:     '),sg.InputText(size=(25, 1), enable_events=True, key="-FILE-"),sg.Button('Load'),sg.Button('Save')]
                      ]
column_Data = [[sg.Text('Password: '),sg.InputText(size=(25, 1), enable_events=True, key="-PASSWORD-"),sg.Button('Encrypt'),sg.Button('Decrypt')],
            [sg.Multiline(size=(100, 30), key='textbox')]]
row_Path = [[sg.Text('Path: '), sg.Text(enable_events=True,size=(60, 1) ,key= "-Path-")]]
row_Terminal = [[sg.Text('System Log')], [ sg.Listbox(values=[], enable_events=False, size=(70, 20), key="-LOG-")]]
column_Encrypted_Data=[[sg.Text('Encrypted Values')], [sg.Multiline( size=(70, 20), key="-Encrypted-")]] # might want to look into better output option
layout = [[sg.Column(row_Path)],
    [sg.HSeparator()],
    [sg.Column(column_fileListing),
        sg.VSeperator(),
     sg.Column(column_Data)],[sg.HSeparator()],
          [sg.Column(row_Terminal, justification='center'),sg.VSeperator(),
           sg.Column(column_Encrypted_Data, justification='center')]
]  # identify the multiline via key option

# Create the Window
window = sg.Window('Enigma MK-0-A2', layout).Finalize()
window.Maximize()

mach = Machine()
start_time = time.time()
sys_log=[]
rot = Rotors()
fileVal=""
lBoard = Lampboard()
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()

    if event in (None, 'Close Window'): # if user closes window or clicks cancel
        break
    print('You entered in the textbox:')
    print(values['textbox'])  # get the content of multiline via its unique key
    if event == "Refresh" or event == "-FOLDER-":
        folder = values["-FOLDER-"]
        filename = mach.get_fName()
        if filename == "":
            window["-Path-"].update(folder)
        else:
            window["-Path-"].update(filename)

        try:
        # Get list of files in folder
            file_list = os.listdir(folder)
        except:
            file_list = []

        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder, f))
            and f.lower().endswith((".txt", ".bin"))
        ]
        print(fnames)
        window["-FILE LIST-"].update(fnames)
    elif event == "-FILE LIST-":  # A file was chosen from the listbox
        try:
            filename = os.path.join(
                values["-FOLDER-"], values["-FILE LIST-"][0]
            )
            window["-FILE-"].update(values["-FILE LIST-"])
            window["-Path-"].update(filename)
            mach.set_fName(filename)
            fileVal = values["-FILE LIST-"][0]
        except:
            pass
    elif event == "-FILE-":
        try:
            filename = os.path.join(
                values["-FOLDER-"], values["-FILE-"]
            )
            window["-Path-"].update(filename)
            mach.set_fName(filename)
            fileVal = values["-FILE-"]
        except:
            pass
    elif event == "Load":

        filename = mach.get_fName()
        if filename == "" or fileVal == "":
            time_dif = time.time() - start_time
            e_Message = "%s: Can't Load -File Name field is empty" % round(time_dif, 2)
            print(e_Message)
            sys_log.append(e_Message)
            window["-LOG-"].update(sys_log)
        else:

            en_Data = lBoard.bLoad_pFile(filename)
            print(filename)
            mach.set_pIV(lBoard.get_pIV())
            mach.set_pCy_data(en_Data)
            mach.set_pSalt(lBoard.get_pSalt())
            ## window["textbox"].update(en_Data)
            window["-Encrypted-"].update(en_Data)
    elif event == "Save":
        filename = mach.get_fName()
        if filename == "" or fileVal == "":
            time_dif = time.time() - start_time

            e_Message = "%s: Can't Save -File Name field is empty" % round(time_dif, 2)
            print(e_Message)
            sys_log.append(e_Message)
            window["-LOG-"].update(sys_log)
        else:
            pSalt = mach.get_pSalt()
            pIV = mach.get_pIV()
            pCy_data = mach.get_pCy_data()
            lBoard.bWrite_pFile(filename,pSalt,pIV,pCy_data)
    elif event == "Encrypt":
        pPWord = values["-PASSWORD-"]
        if pPWord == "":
            time_dif = time.time() - start_time

            e_Message = "%s: Can't Encrypt -Password field is empty" % round(time_dif, 2)
            print(e_Message)
            sys_log.append(e_Message)
            window["-LOG-"].update(sys_log)
        else:
            rot.set_Password(pPWord)
            pSalt = mach.get_pSalt()

            if pSalt == b'':
                time_dif = time.time() - start_time
                print("%s: salt will be made in rot" % round(time_dif, 2))
            else:
                rot.set_salt(pSalt)
            rot.make_key()
            en_Data = values["textbox"]
            crp_Data = rot.encrypt_data(bytes(en_Data, 'utf-8'))
            mach.set_pCy_data(crp_Data)

            mach.set_pIV(rot.get_iv())
            mach.set_pSalt(rot.get_salt())
            ## window["textbox"].update(crp_Data)
            window["-Encrypted-"].update(crp_Data)
    elif event == "Decrypt":
        pPWord = values["-PASSWORD-"]
        if pPWord == "":
            time_dif = time.time() - start_time

            e_Message = "%s: Can't Decrypt -Password field is empty" % round(time_dif, 2)
            print(e_Message)
            sys_log.append(e_Message)
            window["-LOG-"].update(sys_log)
        else:
            rot.set_Password(pPWord)
            pSalt = mach.get_pSalt()

            if pSalt == b'':
                time_dif = time.time() - start_time
                print("%s: salt will be made in rot" % round(time_dif, 2))
            else:
                rot.set_salt(pSalt)
            rot.make_key()
            pIV = mach.get_pIV()
            eData = mach.get_pCy_data()
            print(eData)
            print(pIV)
            en_Data = rot.decrypt_data(eData,pIV)


            clear_Data = str(en_Data, 'UTF-8')
            window["textbox"].update(clear_Data)


window.close()