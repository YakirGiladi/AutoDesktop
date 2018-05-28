from tkinter import *
from tkinter import ttk
import re
import os

help_content = "This is the help_content\nThis is the help_content\nThis is the help_content"
title = "About AutoDekstop"
master_h = None

class Help():

    global title, help_content

    def quit(self):

        global master_h
        
        master_h.quit()
        master_h.destroy()

    # def __init__(self, master_h=None):
    def __init__(self):

        global master_h

        # self.master = master_h

        ############ AutoDekstop Help ############
        adt_help_frame = LabelFrame(master_h, labelanchor=N, text=title, font="Arial 25 bold italic")
        adt_help_frame.pack()
        adt_help_frame.pack_propagate(0) 

        help_label = Label(adt_help_frame, text=help_content, font="Arial 10")
        help_label.grid(row=0, column=0, padx=2, pady=15, sticky=E)

        master_h.protocol('WM_DELETE_WINDOW', self.quit)

        mainloop()



def run_help(kind):

    global master_h, title, help_content
    
    master_h = Tk()

    if kind == "About":
        title = "About AutoDekstop"

        with open ("About.txt", 'r') as abf:
            help_content = abf.read()

        master_h.geometry("500x650")

    elif kind == "Instructions":
        title = "AutoDekstop Instructions"

        with open ("Instructions.txt", 'r') as abf:
            help_content = abf.read()

        master_h.geometry("600x550")

    
    master_h.title(title)
    
    master_h.iconbitmap(default='AutoDekstop_logo.ico')
    # app_help = Help(master_h)
    app_help = Help()
    master_h.mainloop()