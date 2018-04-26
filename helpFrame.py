from tkinter import *
from tkinter import ttk
import re
import os

help_content = "This is the help_content\nThis is the help_content\nThis is the help_content"
title = "AutoDekstop Help"
master_h = None

class Help():

    def quit(self):
        global master_h
        master_h.quit()
        master_h.destroy()

    def __init__(self, master_h=None):

        self.master_h = master_h

        ############ AutoDekstop Help ############
        adt_help_frame = LabelFrame(master_h, labelanchor=N, text=title, font="Arial 25 bold italic")
        adt_help_frame.pack()
        adt_help_frame.pack_propagate(0) 

        help_label = Label(adt_help_frame, text=help_content, font="Arial 10")
        help_label.grid(row=0, column=0, padx=2, pady=15)

        master_h.protocol('WM_DELETE_WINDOW', self.quit)

        mainloop()



def run_help():

    global master_h

    master_h = Tk()
    master_h.title(title)
    master_h.geometry("400x300")
    master_h.iconbitmap(default='icon.ico')
    app_help = Help(master_h)
    master_h.mainloop()

