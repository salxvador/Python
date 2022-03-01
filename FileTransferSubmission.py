
##Allow the user to browse and choose a specific folder that will contain
##  the files to be checked daily.

##Allow the user to browse and choose a specific folder that will receive
##  the copied files.

##Allow the user to manually initiate the 'file check' process that is
##  performed by the script.


import shutil
import os
import datetime
import tkinter as tk
from tkinter import *
from tkinter import filedialog as fd

####  TKINTER GUI  ####

win = tk.Tk()
win.title("File Shuttle")

#buttons
btnBrowse1 = tk.Button(win, text="Browse...", command= lambda: browse(entSource))
btnBrowse1.grid(row=1, column=0, padx=7, pady=5)

btnBrowse2 = tk.Button(win, text="Browse...", command= lambda: browse(entDest))
btnBrowse2.grid(row=3, column=0, padx=7, pady=5)

btnMove = tk.Button(win,text="Move Files", command= lambda: moveFiles())
btnMove.grid(row=4, column=0, columnspan=2, padx=7, pady=5, sticky=E+W)

#labels
lblSource = tk.Label(win, text="Source Directory:")
lblSource.grid(row=0, column=1, padx=7, sticky=W)

lblDestination = tk.Label(win, text="Destination Directory:")
lblDestination.grid(row=2, column=1, padx=7, sticky=W)

#entry fields
entSource = tk.Entry(win, width=40)
entSource.grid(row=1, column=1, padx=7, pady=5)

entDest = tk.Entry(win, width=40)
entDest.grid(row=3, column=1, padx=7, pady=5)

####  BROWSE FN  ####

#allows user to select dierctory, then inserts path into appropriate entry field
def browse(field):
    path = fd.askdirectory() + '/'
    #if user runs process multiple times, need to clear this field, then insert new selection
    field.delete(0,END) 
    field.insert(0,path)

####  SHUTIL FN  ####
    
# This fn will move files that were created or modified in in the last 24 hrs from the
#   source directory to the destination directory

def moveFiles():
    #get paths for source and dest, make a list of files in the source
    source = entSource.get()
    destination = entDest.get()
    files = os.listdir(source)
    # 'i' contains the file name, so adding it to the paths allows us to move them.
    for i in files:
        fpath = source + i
        #epoch is the time in seconds since the "epoch" began
        epoch = os.path.getmtime(fpath)
        #modTime is a human-readable format
        modTime = datetime.datetime.fromtimestamp(epoch)
        #will use this time delta to see if modDate files are older than 24 hrs
        # activeTime gives us 24 hrs before current time
        td = datetime.timedelta(hours=24)
        activeTime = datetime.datetime.now() - td
        if activeTime > modTime: #files older than 24 hours will NOT be moved
            print(i + " will not be moved.")
        else: #files modified in last 24 hours are moved.
            shutil.move(source+i, destination)
            print(i + " has been moved to Destination Directory.")


if __name__ == "__main__":
    win.mainloop()
