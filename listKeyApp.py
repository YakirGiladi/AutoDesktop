from tkinter import *
from tkinter import ttk
import re

master = None
listbox = None
list_insert = None
sv = None

keys = ['\\t', '\\n', '\\r', '!', '"', '#', '$', '%', '&', "'", '(',
')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7',
'8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`',
'a', 'b', 'c', 'd', 'e','f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~',
'accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace',
'browserback', 'browserfavorites', 'browserforward', 'browserhome',
'browserrefresh', 'browsersearch', 'browserstop', 'capslock', 'clear',
'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 'delete',
'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10',
'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20',
'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9',
'final', 'fn', 'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert', 'junja',
'kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail',
'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack',
'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6',
'num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause', 'pgdn',
'pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn',
'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select', 'separator',
'shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop', 'subtract', 'tab',
'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen',
'command', 'option', 'optionleft', 'optionright']


# Return index of desired element to seek for
def callback():

    global sv
    highlight_searched()
    update_listbox()

def highlight_searched():

    global sv

    search = sv.get()
    for i,item in enumerate(keys):

        if search.lower() in item.lower():
            listbox.selection_set(i)
        else:
            listbox.selection_clear(i)
    if search == '':
        listbox.selection_clear(0, END)

def update_listbox():
    search_term = sv.get()
    listbox.delete(0, END)
    for key in keys:
        if search_term.lower() in key.lower():
            listbox.insert(END, key)

def insert():

    global listbox, list_insert
    
    select = listbox.get(ACTIVE)
    list_insert.insert(END, select)

def cancel():

    master.quit()
    master.destroy()

def delete():
    
    global list_insert

    selection = list_insert.curselection()
    if selection:
        list_insert.delete(selection[0])

def export():

    global master, list_insert, keylist

    keylist = []
    a = list_insert.get (0, last=list_insert.size()-1 )
    for i in a:
        keylist.append(i)
    else:
        with open("listkey.txt","w") as lkf:
            for key in keylist:
                lkf.write(re.escape(key) + " ")
        master.quit()
        master.destroy()




def list_application():

    global master, listbox, list_insert, sv

    master = Tk()
    master.title("Search from a list")
    master.geometry("450x300")
    master.iconbitmap(default='AutoDekstop_logo.ico')



    sv = StringVar()
    sv.trace("w", lambda name, index, mode, sv=sv: callback())
    search = Entry(master, textvariable=sv)

    Label(master, text="Search:").grid(row=1, column=0, sticky=E, padx=2)
    search.grid(row=1, column=1, sticky=N, ipadx=5, pady=5, padx=15)
    ttk.Button(master, text="Add Key", command=insert).grid(row=1, column=2, sticky=W, padx=2)
    ttk.Button(master, text="Export List", command=export).grid(row=1, column=3, sticky=W, padx=2)

    options_frame = LabelFrame(master, labelanchor=N, text="Key Options", font="Arial 15 bold italic")
    options_frame.grid(row=2, column=0, columnspan=2, sticky=E, ipady=3, ipadx=5, pady=15, padx=15)

    insert_frame = LabelFrame(master, labelanchor=N, text="Insert List", font="Arial 15 bold italic")
    insert_frame.grid(row=2, column=2, columnspan=3, sticky=W, ipady=3, ipadx=5, pady=15, padx=15)



    ttk.Button(master, text="Cancel", command=cancel).grid(row=3, column=1,  sticky=W, padx=2)
    ttk.Button(master, text="Delete", command=delete).grid(row=3, column=3,  sticky=W, padx=2)

    scrollbar_opt = Scrollbar(options_frame)
    scrollbar_opt.pack(side=RIGHT, fill=Y)

    scrollbar_ins = Scrollbar(insert_frame)
    scrollbar_ins.pack(side=RIGHT, fill=Y)

    listbox = Listbox(options_frame, width=20)
    listbox.pack(padx=15)

    list_insert = Listbox(insert_frame, width=20)
    list_insert.pack(padx=15)

    listbox.config(yscrollcommand=scrollbar_opt.set)
    scrollbar_opt.config(command=listbox.yview)

    listbox.config(yscrollcommand=scrollbar_opt.set)
    scrollbar_opt.config(command=listbox.yview)

    for item in keys:
        listbox.insert(END, item)

    mainloop()

list_application()

