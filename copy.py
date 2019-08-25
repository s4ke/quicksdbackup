from datetime import datetime
from threading import Thread

import PySimpleGUI as sg

from shutil import copytree, copy2

import os

FROM_DIR = "J:\\"
TO_DIR = "D:\\Bilder\\Automatisch\\"

# All the stuff inside your window. This is the PSG magic code compactor...
layout = [[sg.Text('Ursprung: ' + FROM_DIR)],
          [sg.Text('Ziel: ' + TO_DIR)],
          [sg.Button('SD Karte sichern')],
          [sg.Button('Schließen')]]

window = sg.Window('SD Karte Sicherung', layout)
# Event Loop to process "events"
while True:
    event, values = window.Read()
    if event == 'SD Karte sichern':
        now = datetime.now()

        # copy subdirectory example
        fromDirectory = FROM_DIR
        toDirectory = TO_DIR + now.strftime("%d-%m-%Y-%H-%M-%S")

        count = [0]
        cancelled = [False]
        total = 0

        for dirpath, dirs, files in os.walk(fromDirectory):    
            for filename in files:
                fname = os.path.join(dirpath,filename)
                total += 1
        
        print("found " + str(total) + " files.")

        sg.OneLineProgressMeter('Fortschritt', count[0], total, 'progress')

        def copy2_verbose(src, dst):
            if cancelled[0]:
                raise InterruptedError('stopped')
            copy2(src, dst)
            count[0] += 1

        def copy():
            try:
                copytree(fromDirectory, toDirectory, copy_function=copy2_verbose)
            except InterruptedError as e:
                print('caught InterruptedError!', e)

        process = Thread(target=copy)
        process.start()

        last_cnt = count[0]
        while count[0] <= total:
            if last_cnt != count[0]:
                print(str(count[0]) + '/' + str(total))
                last_cnt = count[0]
            if not sg.OneLineProgressMeter('Fortschritt', count[0], total, 'progress'):
                if count[0] != total:
                    cancelled[0] = True
                    print("cancelled!!!")
                break

        if not cancelled[0]:
            layout = [[sg.Text('Fertig!')],
                      [sg.Submit()]]

            popup = sg.Window('Ergebnis', layout)

            event = popup.Read()
            popup.Close()

    if event in (None, 'Schließen'):
        break

window.Close()



