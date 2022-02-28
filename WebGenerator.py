
import webbrowser as wb #needed to open content in web browser
from tkinter import *
import tkinter as tk

#main gui frame:
win = tk.Tk()

## buttons and entry field:
btnSave = tk.Button(win,text="Save", width=15, command=lambda: setContent())
btnSave.grid(row=1,column=0, padx=10, pady=10, sticky=W)

btnPublish = tk.Button(win,text="Publish", width=15, command=lambda: openTab())
btnPublish.grid(row=1,column=0, padx=10, pady=10, sticky=E)

formtxt = tk.Entry(win,width=50)
formtxt.grid(row=0,column=0, padx=10, pady=10)

#When user clicks 'Save' in GUI:
def setContent():
    content = formtxt.get() #gets whatever they typed into the entry field.
    # open the HTML File, replace witht he new content, then close it.
    f = open('webGen.html',"w")
    f.write("<html>\n\t<body>\n\t\t<h1>\n\t"+ content +"\n\
            </h1>\n\t</body>\n</html>")
    f.close()

#when the user clicks 'Publish' this will open the page in their browser:
def openTab():
    wb.open_new_tab('webGen.html')



if __name__ == "__main__":
    win.mainloop()
