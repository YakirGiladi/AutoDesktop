from tkinter import *
from tkinter import ttk
import re
import os

help_content = "This is the help_content\nThis is the help_content\nThis is the help_content"
title = "About AutoDekstop"
master_h = None

sizex = 0
sizey = 0

class Help():

    global title, help_content

    def quit(self):

        global master_h
        
        master_h.quit()
        master_h.destroy()

    # def __init__(self, master_h=None):
    def __init__(self, kind):

        global master_h, sizex, sizey

        # self.master = master_h

        ############ AutoDekstop Help/Instuctions ############

        # adt_help_frame = LabelFrame(master_h, labelanchor=N, text=title, font="Arial 25 bold italic")
        # adt_help_frame.pack()
        # adt_help_frame.pack_propagate(0) 

        def mouse_wheel(event):
            canvas.yview("scroll",event.delta,"units")
        

        def myfunction(event):
            canvas.configure(scrollregion=canvas.bbox("all"), width=sizex-25, height=sizey-25)


        myframe=Frame(master_h,relief=GROOVE, width=50, height=100,bd=1)
        myframe.place(x=10 , y=10)

        canvas=Canvas(myframe)
        frame=Frame(canvas)
        myscrollbar=Scrollbar(myframe,orient="vertical",command=canvas.yview)
        canvas.configure(yscrollcommand=myscrollbar.set)

        if kind == "Instructions":
            myscrollbar.pack(side="right",fill="y")
            # sizex = sizex-10
            sizex = sizex-20

        canvas.pack(anchor=CENTER)
        canvas.create_window((0,0),window=frame,anchor='nw')
        frame.bind("<Configure>",myfunction)
        Label(frame,text=title, justify=CENTER, font=("Courier", 15,'underline')).grid(row=0,column=0)
        Label(frame,text=help_content, justify=CENTER ).grid(row=1,column=0)

        master_h.protocol('WM_DELETE_WINDOW', self.quit)

        master_h.bind("<MouseWheel>", mouse_wheel)



        mainloop()


        # adt_help_frame = LabelFrame(master_h, labelanchor=N, text=title, font="Arial 25 bold italic")
        # adt_help_frame.pack()
        # adt_help_frame.pack_propagate(0) 


        # help_label = Label(adt_help_frame, text=help_content, font="Arial 10", justify=LEFT)
        # help_label.grid(row=0, column=0, padx=2, pady=15, sticky=E)

        # master_h.protocol('WM_DELETE_WINDOW', self.quit)

        # mainloop()



def run_help(kind):

    global master_h, title, help_content, sizex, sizey
    
    master_h = Tk()

    if kind == "About":
        title = "About AutoDekstop"

        with open ("About.txt", 'r') as abf:
            help_content = abf.read()

        # sizex = 345
        # sizey = 545

        sizex = 430
        sizey = 710

    elif kind == "Instructions":
        title = "AutoDekstop Instructions"

        with open ("Instructions.txt", 'r') as abf:
            help_content = abf.read()

        # sizex = 610
        # sizey = 545

        sizex = 750
        sizey = 710

    master_h.geometry("%dx%d+%d+%d" % (sizex, sizey, 100, 100))
    master_h.resizable(0,0)
    master_h.title(title)
    
    master_h.iconbitmap(default='AutoDekstop_logo.ico')
    # app_help = Help(master_h)
    app_help = Help(kind)
    master_h.mainloop()

# run_help("About")
# run_help("Instructions")