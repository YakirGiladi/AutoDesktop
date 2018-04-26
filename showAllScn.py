from tkinter import *
from tkinter import ttk
import re
import os



class Sas():

    sas_master = None
    listbox = None
    list_insert = None
    sv = None
    
    scenarios = set()

    def get_scenarios_from_file(filename):

        scenarios = set()
        with open(filename, 'r') as asf:
            for line in asf.readlines():
                scenarios.add(line)

        return scenarios

    # Return index of desired element to seek for
    def callback():

        global sv
        print("123")
        Sas.highlight_searched()
        Sas.update_listbox()

    def highlight_searched():

        global sv

        search = sv.get()
        for i,item in enumerate(scenarios):

            if search.lower() in item.lower():
                listbox.selection_set(i)
            else:
                listbox.selection_clear(i)
        if search == '':
            listbox.selection_clear(0, END)

    def update_listbox():
        search_term = sv.get()
        listbox.delete(0, END)

        for key in scenarios:
            if search_term.lower() in key.lower():
                listbox.insert(END, key)

    def cancel():

        sas_master.quit()
        sas_master.destroy()

    def delete():
        
        global listbox

        selection = listbox.curselection()
        if selection:
            to_delete = listbox.get(selection[0]).strip()
            listbox.delete(selection[0])
            os.remove(to_delete)

    def SAS_application():

        global sas_master, listbox, sv, scenarios

        signScriptsFile = "All Scenarios.txt"

        sas_master = Tk()
        sas_master.title("Show All Scenarios")
        sas_master.geometry("350x300")
        sas_master.iconbitmap(default='icon.ico')


        sv = StringVar()
        sv.trace("w", lambda name, index, mode, sv=sv: Sas.callback())
        search = Entry(sas_master, textvariable=sv)

        Label(sas_master, text="Search:").grid(row=1, column=1, columnspan=2, padx=2)
        search.grid(row=1, column=3, columnspan=3, sticky=W, pady=5)

        options_frame = LabelFrame(sas_master, labelanchor=N+W, text="All Scenarios", font="Arial 15 bold italic")
        options_frame.grid(row=2, column=0, columnspan=6, sticky=N, ipady=3, ipadx=5, pady=15, padx=20)

        ttk.Button(sas_master, text="Cancel", command=Sas.cancel).grid(row=3, column=2,  sticky=W, padx=2)
        ttk.Button(sas_master, text="Delete", command=Sas.delete).grid(row=3, column=3,  sticky=W, padx=2)
        ttk.Button(sas_master, text="Open", command=Sas.delete).grid(row=3, column=4,  sticky=W, padx=2)

        scrollbar_opt = Scrollbar(options_frame)
        scrollbar_opt.pack(side=RIGHT, fill=Y)

        listbox = Listbox(options_frame, width=40)
        listbox.pack(padx=15)

        listbox.config(yscrollcommand=scrollbar_opt.set)
        scrollbar_opt.config(command=listbox.yview)


        scenarios = Sas.get_scenarios_from_file(signScriptsFile)
        scenarios = sorted(scenarios)
        for scn in scenarios:
            listbox.insert(END, scn)

        sas_master.mainloop()

Sas.SAS_application()

