# import tkinter as Tk
from tkinter import *

master = Tk()

listbox = Listbox(master)
listbox.pack()

# Insert few elements in listbox:
for item in ["zero", "one", "two", "three", "four", "five", "six", "seven"]:
    listbox.insert(END, item)
# Return index of desired element to seek for
def check_index(element):
   try:
       index = listbox.get(0, "end").index(element)
       return index
   except ValueError:
       print('Item can not be found in the list!')
       index = -1 # Or whatever value you want to assign to it by default
       return index

def callback(sv):
    print (sv.get())

sv = StringVar()
sv.trace("w", lambda name, index, mode, sv=sv: callback(sv))
search = Entry(master, textvariable=sv)
search.pack()

print (check_index('three'))    # Will print 3

print (check_index(100)) # This will print:
                     # Item can not be found in the list!
                     # -1

mainloop()
