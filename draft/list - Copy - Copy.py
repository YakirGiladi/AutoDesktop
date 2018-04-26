from tkinter import *


def __init__(self, master):

  def cb(self, event):
    print ("variable is", self.var.get())

  self.var = IntVar()
  c = Checkbutton(master, text="Enable Tab",variable=self.var,command=self.cb) 
  c.pack(side=TOP)


  


master = Tk()

# c = Checkbutton(master, text="Expand", variable=var)
# c.pack()

mainloop()