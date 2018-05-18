#!/usr/bin/python3
# -*- coding: utf-8 -*-

import AutoDesktop
import Dictionary
import helpFrame
import tkinter
import os
import string
from tkinter import *
from tkinter import ttk
from tkinter import filedialog, messagebox
import os
from tkinter.ttk import Frame, Label, Style
import threading
import time
import math
import subprocess as sp

do_action = False
disable_unsupported = True
file = ""
script_name = ""
rf_filename = ""
text_actions_list = None
listKeyFile = "listkey.txt"
programName = "subl.exe"
selfCodingFile = "self_coding"
selfCodingDir = "Self Coding Scripts"
signScriptsFile = "All Scenarios.txt"


class Sas():

    master = None
    listbox = None
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
        
        print("callback")
        Sas.sas_highlight_searched()
        Sas.sas_update_listbox()

    def sas_highlight_searched():

        global sv, scenarios

        search = sv.get()
        for i,item in enumerate(scenarios):

            if search.lower() in item.lower():
                listbox.selection_set(i)
            else:
                listbox.selection_clear(i)
        if search == '':
            listbox.selection_clear(0, END)

    def sas_update_listbox():

        global sv, scenarios

        search_term = sv.get()
        listbox.delete(0, END)

        for key in scenarios:
            if search_term.lower() in key.lower():
                listbox.insert(END, key)

    def sas_cancel():

        master.quit()
        master.destroy()

    def sas_delete():
        
        global listbox

        selection = listbox.curselection()
        if selection:
            to_delete = listbox.get(selection[0]).strip()
            listbox.delete(selection[0])
            os.remove(to_delete)

        # with open(signScriptsFile, 'r+w') as asf:
        #     for line in asf.readlines():
        #         if line == to_delete:
        #             f.write("")

    def sas_open():

        global script_name, file

        selection = listbox.curselection()
        if selection:
            file = listbox.get(selection[0]).strip()
            app.openfile(show = True)
            Sas.sas_cancel()
        else:
            Application.raise_an_error_msg("Not exists scenario","You must to choose a scenario !")

    def SAS_application():

        global master, listbox, sv, scenarios

        signScriptsFile = "All Scenarios.txt"

        master = Tk()
        master.title("Show All Scenarios")
        master.geometry("430x370")
        master.iconbitmap(default='icon.ico')

        sv = StringVar()
        sv.trace("w", lambda name, index, mode, sv=sv: Sas.callback())
        search = Entry(master, textvariable=sv)

        Label(master, text="Search:").grid(row=1, column=1, columnspan=2, padx=2)
        search.grid(row=1, column=3, columnspan=3, sticky=W, pady=5)

        options_frame = LabelFrame(master, labelanchor=N+W, text="All Scenarios", font="Arial 15 bold italic")
        options_frame.grid(row=2, column=0, columnspan=6, sticky=N, ipady=3, ipadx=5, pady=15, padx=20)

        ttk.Button(master, text="Cancel", command=Sas.sas_cancel).grid(row=3, column=2,  sticky=W, padx=2)
        ttk.Button(master, text="Delete", command=Sas.sas_delete).grid(row=3, column=3,  sticky=W, padx=2)
        ttk.Button(master, text="Open", command=Sas.sas_open).grid(row=3, column=4,  sticky=W, padx=2)

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

        master.protocol('WM_DELETE_WINDOW', Sas.sas_cancel)

        master.mainloop()


class Application(Frame):

    def quit(self):
        root.quit()
        # if messagebox.askokcancel("Quit", "Do you want to quit?"):
        #     root.quit()

    def sign_scripts_names(filename):

        if not ".txt" in filename:
            filename = filename + ".txt"
            
        with open(signScriptsFile, "a") as ssf:
            print("ssf:{}".format(filename))
            ssf.write(filename + "\n")

    def save(self):

        print("save")

        global file, text_actions_list
        actions_save = text_actions_list.get("1.0",END) #store the contents of the text widget in a str
        
        try:
            if not file:
                Application.save_as(self)
            else:
                with open(file, 'w') as outputFile:  #see if the str containing the output
                    outputFile.write(actions_save)         #file (self.f) exists, and we can write to it,
        except AttributeError:                     #and if it doesn't,
            Application.save_as()


    def save_as(self):

        global file, text_actions_list

        print("save_as")

        actions_save = text_actions_list.get("1.0",END).strip()
        try:
            file = filedialog.asksaveasfilename( defaultextension=".txt", filetypes = (("text file", "*.txt"), ("text", "*.txt")))
            
            if file:
                with open(file, 'w') as outputFile:
                    outputFile.write(actions_save)
                Application.sign_scripts_names(file)
            else:
                Application.raise_an_info_msg("Attention !","You didn\'t choose path\nThe file not saved !")
        except Exception as e:
            print(e)
            Application.raise_an_error_msg("Error",e)

    def help_frame(self):

        helpFrame.run_help()

    def raise_an_error_msg(title_text,text):

        messagebox.showerror(title_text, text)

    def raise_an_info_msg(title_text,text):

        messagebox.showinfo(title_text, text)

    def __init__(self, master=None):

        global text_actions_list

        master.event_generate("<<NotebookTabChanged>>")
        self.insert_filename_fm = None
        self.countdown_fm = None

        self.master = master
        self.line_start_save = 0
        self.line_start = 0
        self.line_end = 0
        self.object_cb_list = []
        self.typekey_list = []

        self.search_func=IntVar(master) # find, click, coordinate
        self.rlb=IntVar(master) # right, left, double Search Obj
        self.rbv=IntVar(master) # L/R Click
        self.exists_clicked=IntVar(master)
        self.lb_condition_var = StringVar(master)
        self.rb_log_type = StringVar(master)

        self.btn_if_pressed = False
        self.btn_else_pressed = False

        self.run_script = None
        self.if_finished_td = None
        self.countdown_fm_thread = None
        self.countdown_thread = None

        self.lb_coutdown = None

        s = tkinter.ttk.Style()
        # print(s.theme_names())
        s.theme_use("xpnative")

        def set_exists_scenario():

            global script_name, file

            combo = set()
            contentfile = ""
            script_name = ""
            self.object_cb_list = []

            with open(file, 'r') as readfile:
                for line in readfile:
                    if "search" in line:
                        contentfile += line
                        line = next(readfile)
                        combo.add(line)

                    contentfile += line

                else:
                    set_condition(line[:line.index(":")])

            for val in combo:
                self.object_cb_list.append(val)

            self.cb_obj['values'] = self.object_cb_list
            clear_actions_list(openfile = True)
            insert_to_actions_list(contentfile.strip(), openfile = True)

        def condition():

            return int(self.lb_condition_var.get())

        def set_condition(num):

            self.lb_condition_var.set(str(num))

            if int(num) > 0:
                btn_finish_condition.config(state=NORMAL)
            else:
                btn_finish_condition.config(state=DISABLED)

        def create_menu_bar(master):
            # create a toplevel menu
            menubar = Menu(master)

            # create a pulldown menu, and add it to the menu bar
            filemenu = Menu(menubar, tearoff=0)
            filemenu.add_command(label="New Scenario", command=new_scenario_com, accelerator="Ctrl+N")
            filemenu.add_command(label="Open", command=openfile, accelerator="Ctrl+O")
            filemenu.add_command(label="Save", command=self.save, accelerator="Ctrl+S")
            filemenu.add_command(label="Save As", command=self.save_as, accelerator="Ctrl+Shift+S")
            filemenu.add_separator()
            filemenu.add_cascade(label="Help", command=self.help_frame, accelerator="F1")
            filemenu.add_command(label="Exit", command=self.quit, accelerator="Ctrl+Q")
            menubar.add_cascade(label="File", menu=filemenu)

            # create more pulldown menus
            # editmenu = Menu(menubar, tearoff=0)
            # editmenu.add_command(label="Cut", command=hello)
            # editmenu.add_command(label="Copy", command=hello)
            # editmenu.add_command(label="Paste", command=hello)
            # menubar.add_cascade(label="Edit", menu=editmenu)

            helpmenu = Menu(menubar, tearoff=0)
            helpmenu.add_command(label="About", command=hello)
            menubar.add_cascade(label="Help", menu=helpmenu)

            
            # display the menu
            root.config(menu=menubar)

        def thread_run_script():

            global file, script_name

            print(file,script_name)
            self.if_finished_td.start()
            self.countdown_fm_thread.start()

            Dictionary.convert_code(file, script_name)
            Dictionary.run_scenario(script_name)

        def thread_isFinished_script():

            while(True):

                if not self.run_script.isAlive():
                    # self.run_script._stop_event.set()
                    Application.raise_an_info_msg("AutoDesktop Info Message","Finished Scenario !")
                    break

        # def save():

        #     global file
        #     actions_save = text_actions_list.get("1.0",END) #store the contents of the text widget in a str
            
        #     try:
        #         if not file:
        #             save_as()
        #         else:
        #             with open(file, 'w') as outputFile:  #see if the str containing the output
        #                 outputFile.write(actions_save)         #file (self.f) exists, and we can write to it,
        #     except AttributeError:                     #and if it doesn't,
        #         save_as()  

        # def save_as():

        #     global file

        #     actions_save = text_actions_list.get("1.0",END).strip()
        #     try:
        #         file = filedialog.asksaveasfilename( defaultextension=".txt", filetypes = (("text file", "*.txt"), ("text", "*.txt")))
        #         sign_scripts_names(file)
        #         if os.path.isfile(file):
        #             with open(file, 'w') as outputFile:
        #                 outputFile.write(actions_save)
        #         else:
        #             raise_an_info_msg("Attention !","You didn\'t choose path\nThe file not saved !")
        #     except Exception as e:
        #         print(e)
        #         raise_an_error_msg("Error",e)

        def openfile(show = False):

            global file, script_name

            self.object_cb_list = []
            if not show:
                file = filedialog.askopenfilename( defaultextension=".txt", filetypes = (("text file", "*.txt"), ("text", "*.txt")))
            if os.path.isfile(file):
                set_exists_scenario()

        def new_scenario_com():

            global file, script_name

            line_number = get_number_of_lines()
            if line_number > 1:
                if len(file) == 0:
                    Application.raise_an_info_msg("Need to save","Before you created a new scenario\nYou need to save the exists")
                    save_as()
                    clear_actions_list(openfile = False)

            file = ""
            script_name = ""

        def get_number_of_lines():

            global text_actions_list

            return int(text_actions_list.index('end').split('.')[0]) - 1

        def valid_input_digit(input_str):

            return input_str.isdigit()

        def sleep():

            sleep_str = self.tf_sleep_var.get()

            if valid_input_digit(sleep_str):
                time_sleep = int(float(sleep_str))

                if time_sleep == 0:
                    Application.raise_an_error_msg("Input Error","Time sleep must be more then 0 !")
                else:
                    insert_to_actions_list("sleep({})".format(time_sleep))
                    if do_action:
                        AutoDesktop.do_sleep(time_sleep)
            else:
                Application.raise_an_error_msg("Input Error","Time sleep must be a number !")

        def get_path():
            path = filedialog.askopenfilename( filetypes = (("PNG file", "*.png"), ("PNG", "*.png")))
            if path:
                self.tf_search_object_var.set(path)
            else:
                Application.raise_an_error_msg("Input Error","Path field is empty !")

        def set_typekey_list(keylist):

            self.typekey_list = keylist

        def move_mouse_com():
            x = self.tf_move_mouse_x_var.get()
            y = self.tf_move_mouse_y_var.get()
            speed_var = self.tf_move_mouse_speed_var.get()

            if valid_input_digit(x) and valid_input_digit(y) and valid_input_digit(speed_var):

                if x[0] == '0':
                    x = "1"
                if y[0] == '0':
                    y = "1"

                insert_to_actions_list("move_mouse({},{},{})".format(x.strip(), y.strip(), speed_var.strip()))
                if do_action:
                    AutoDesktop.move_mouse(int(float(x)) ,int(float(y)), int(float(speed)))
            else:
                Application.raise_an_error_msg("Input Error","Mouse vars must be numbers !")

        def get_search_object_name(path = ""):

            name = ""
            names_dir = path.split("/")
            for name_dir in names_dir:
                if ".png" in name_dir or ".PNG" in name_dir:
                    name = name_dir[:name_dir.index(".")]

            return name

        def add_cb_obj(text):

            self.object_cb_list.append(text)
            self.cb_obj['values'] = self.object_cb_list 

        def search_object_com():
            path = self.tf_search_object_var.get().strip()

            if not path:
                Application.raise_an_error_msg("Input Error","Path field is empty !")
            else:
                attempts = self.tf_search_attempts_var.get().strip()
                sleep_var = self.tf_search_sleep_var.get().strip()

                if valid_input_digit(sleep_var) and valid_input_digit(attempts):

                    if attempts == "0":
                        attempts = "1"
                        self.tf_search_attempts_var.set("1")

                    obj_name = get_search_object_name(path)
                    add_cb_obj(obj_name)

                    search_func = self.search_func.get()

                    if search_func == 0:
                        search_func = 'find()'
                        # obj_name += "_exists"
                    if search_func == 1:

                        click_type = self.rlb.get()

                        if click_type == 0:
                            click_type = 'Single'
                        elif click_type == 1:
                            click_type = 'Right'
                        elif click_type == 2:
                            click_type = 'Double'
                        search_func = 'click(\"{}\")'.format(click_type)

                    if search_func == 2: 
                        search_func = 'coordinate()'


                    insert_to_actions_list("search_object(\"{}\",{},{})\n{}\n{}".format(path, attempts, sleep_var, obj_name, search_func), search_object = True)
                    self.tf_search_object_var.set("")
                    if do_action:
                        object_searched = AutoDesktop.UIElem(str(path))
                        ######################### Need to be in Thread #########################
                        exist = object_searched.find() 
                        if not exist:
                            print("Cannot Find the " + path)
                        else:
                            print("Found the " + path)
                            AutoDesktop.move_mouse(object_searched.x, object_searched.y , 1) 
                        ######################### Need to be in Thread #########################
                else:
                    Application.raise_an_error_msg("Input Error","Time sleep & Attempts must be numbers !")


        def click():

            clicktype = self.rbv.get()
            clicks = self.tf_click_time_var.get()
            sleep_var = self.tf_click_speed_var.get()

            if valid_input_digit(sleep_var) and valid_input_digit(clicks):

                if clicks == "0":
                    clicks = "1"
                    self.tf_click_time_var.set("1")
                if clicktype == 0: ## Right
                    clicktype = 'Right'
                if clicktype == 1: ## Left
                    clicktype = 'Single'

                insert_to_actions_list("click(\"{}\",{},{})".format(clicktype, clicks, sleep_var))
                if do_action:
                    AutoDesktop.mouse_click(click_type=clicktype, clicks=clicks, speed=sleep_var)
            else:
                Application.raise_an_error_msg("Input Error","Time speed & Clicks must be numbers !")

        def typetext():

            text = self.tf_typetext_text_var.get().strip()
            if text:
                speed = int(self.tf_typetext_speed_var.get())
                self.tf_typetext_text_var.set("")

                insert_to_actions_list("typetext(\"{}\",{})".format(text, speed))
                if do_action:
                    AutoDesktop.keyboard_type(type_write=text, speed=speed)
            else:
                Application.raise_an_error_msg("Input Error","Text field is empty !")

        def get_from_file_keys():

            listkey = []
            os.system("python listKeyApp.py")

            if os.path.isfile(listKeyFile):
                with open(listKeyFile, "r") as lkf:
                    line = lkf.read()
                os.remove(listKeyFile)
                listkey = line.split(" ")

            return listkey

        def press_keyboard():

            key = self.tf_keypress_var.get().strip()
            if not key:
                Application.raise_an_error_msg("Input Error","key field is empty !")
            else:
                self.tf_keypress_var.set("")
                insert_to_actions_list("press_keyboard(\"{}\")".format(key))

        def choose_from_list():
        
            listkey = get_from_file_keys()

            if listkey:
                del listkey[-1]

                for key in listkey:
                    insert_to_actions_list("press_keyboard(\"{}\")".format(key))
            

        def multipress_typekey():

            listkey = get_from_file_keys()

            if listkey:
                del listkey[-1]
                # build string
                press = ""
                for key in listkey:
                    press += "{} ".format(key)
                press = press[:-2]

                insert_to_actions_list("keyboard_multiPress(\"{}\")".format(press))

        def add_to_lineindex(lineindex, to_add):

            return str(round(float(lineindex), 1) + to_add)

        def get_float_string_int(line_start):

            return int(float(floor_line_string(line_start))) 


        def insert_to_actions_list(text="", openfile = False, cond = True, search_object = False):

            global text_actions_list

            text_actions_list.config(state=NORMAL)
            if self.line_start == 0:
                print("(INSERT)")
                self.line_start = INSERT
                text_actions_list.tag_remove("highlight", 1.0, "end")
                text_actions_list.tag_add("highlight", "{}.0".format(get_number_of_lines()), "end")
            
            if openfile:
                text_actions_list.insert(INSERT, '{}'.format(text))
                text_actions_list.tag_remove("highlight", 1.0, "end")
                text_actions_list.tag_add("highlight", "{}.0".format(get_number_of_lines()), "end")

            elif self.line_end == END: # End of list
                print("(=END)")
                # text_actions_list.insert(INSERT, '{}\n{}:'.format(text,condition()))
                text_actions_list.insert(self.line_start, '{}\n{}:'.format(text,condition()))
                text_actions_list.tag_remove("highlight", 1.0, "end")
                # text_actions_list.tag_add("highlight", "{}.0".format(get_number_of_lines()), "end")
                text_actions_list.tag_add("highlight", "{}.0".format(get_number_of_lines()), "end")
                if self.line_start != INSERT:
                    self.line_start = add_to_lineindex(self.line_start, 1)

            elif self.line_start != INSERT and get_float_string_int(self.line_start) > get_number_of_lines() and get_number_of_lines() > 2 :
                # print("(==)")
                # print("lineN:{}".format(get_number_of_lines()))
                # print(get_float_string_int(self.line_start))
                if get_float_string_int(self.line_start) == get_number_of_lines() + 1:
                    # print("lineS:{}".format(get_float_string_int(self.line_start)))
                    text_actions_list.insert(self.line_start, "\n{}".format(text))
                    # print("lineS:{}".format(get_float_string_int(self.line_start)))
                else:
                    # print("lineS:{}".format(get_float_string_int(self.line_start)))
                    text_actions_list.insert(self.line_start, '{}\n{}:'.format(text,condition()))
                    text_actions_list.tag_remove("highlight", 1.0, "end")
                    text_actions_list.tag_add("highlight", "{}.0".format(get_number_of_lines()), "end")
                    self.line_start = add_to_lineindex(self.line_start, 1)

            elif self.line_start == INSERT:

                if cond:
                    print("(1 insert)")
                    text_actions_list.insert(self.line_start, '{}\n{}:'.format(text,condition()))
                    text_actions_list.tag_remove("highlight", 1.0, "end")
                    text_actions_list.tag_add("highlight", "{}.0".format(get_number_of_lines()), "end")

            else:

                if not cond:
                    print("(2 not)")
                    text_actions_list.insert(self.line_start, '{}\n{}:'.format(text,condition()))
                    text_actions_list.tag_remove("highlight", 1.0, "end")
                else:
                    print("(2 yes)")
                    condition_inline, line = get_condition_string()
                    size_condition = len(condition_inline)

                    if ":" in text:
                        text_actions_list.tag_remove("highlight", 1.0, "end")
                        
                        if search_object and len(line) > 1:
                            print("with \\n")
                            # self.line_start = str(round(float(self.line_start), 1) + 1)
                            # self.line_end = str(round(float(self.line_end), 1) + 1)
                            self.line_start = add_to_lineindex(self.line_start, 1)
                            self.line_end = add_to_lineindex(self.line_start, 1)

                            text = str(condition()) + ":" + text + "\n"
                            starter = self.line_start
                            
                            # self.line_start = str(round(float(self.line_start), 1) + 2)
                            # self.line_end = str(round(float(self.line_end), 1) + 2)
                            self.line_start = add_to_lineindex(self.line_start, 2)
                            self.line_end = add_to_lineindex(self.line_end, 2)

                            text_actions_list.insert(starter, text)
                            text_actions_list.tag_add("highlight", starter, self.line_end)
                        else:

                            print("(:1:)" + self.line_start)
                            # print("text:" + text)
                            text_actions_list.insert(self.line_start, text)

                            text_actions_list.tag_add("highlight", self.line_start, self.line_end)
                    
                    elif len(line) > 1 or get_float_string_int(self.line_start) == get_number_of_lines():
                        
                        print("len(line):{}".format(len(line)))

                        print("(<1:)" + self.line_start)
                        # self.line_start = str(round(float(self.line_start), 1) + 1)
                        # self.line_end = str(round(float(self.line_end), 1) + 1)
                        # print("!!!:{},{}".format(get_float_string_int(floor_line_string(self.line_start)),get_number_of_lines()))
                        if get_float_string_int(floor_line_string(self.line_start)) + 1 == get_number_of_lines():
                            print("111")
                            text_actions_list.insert(self.line_start, '{}:{}\n'.format(condition(), text))
                            self.line_start = add_to_lineindex(self.line_start, 1)
                            self.line_end = add_to_lineindex(self.line_end, 1)
                        else:
                            print("222")
                            self.line_start = add_to_lineindex(self.line_start, round(0.2,1))
                            self.line_end = add_to_lineindex(self.line_end, 1)
                            self.line_start = add_to_lineindex(self.line_start, round(0.8,1))

                            # text_actions_list.delete(self.line_start, self.line_end)
                            text_actions_list.insert(self.line_start, str(condition()) + ":" + text + "\n" )
                            # self.line_end = add_to_lineindex(self.line_end, 1)

                        text_actions_list.tag_remove("highlight", 1.0, "end")
                        text_actions_list.tag_add("highlight", floor_line_string(self.line_start), self.line_end)

                        # print(self.line_start,self.line_end)

                    else:
                        print("(!1:)" + self.line_start)
                        text_actions_list.insert(self.line_start, '{}'.format(text))
                        self.line_start = floor_line_string(self.line_start)
                    # print("E:" + self.line_start)
                    print()

            text_actions_list.config(state=DISABLED)
            text_actions_list.see("end")

        def clear_actions_list(openfile = False):

            global text_actions_list

            text_actions_list.config(state=NORMAL)
            text_actions_list.delete('1.0', END)
            if not openfile:
                set_condition(0)
                text_actions_list.insert(INSERT, "0:")
                self.line_start = INSERT
                self.line_end = END
            text_actions_list.config(state=DISABLED)

        def hello():
            print ("hello!")

        def get_condition_string(only_condition = False):

            global text_actions_list

            print(self.line_start, self.line_end)

            if only_condition:
                # print("only_condition")
                starter = self.line_start
                line = text_actions_list.get(floor_line_string(starter), self.line_end)
                return line.split(":")[0]

            else:
                line = text_actions_list.get(self.line_start, self.line_end)
                return line.split(":")[0] , line


        def select(event):

            global text_actions_list

            self.line_start = text_actions_list.index("@%s,%s linestart" % (event.x, event.y))
            self.line_end = text_actions_list.index("%s lineend +1c" % self.line_start ) # +1c (newline)
            # print(self.line_start)

            text_actions_list.tag_remove("highlight", 1.0, "end")

            condition_inline, line = get_condition_string()
            if "search_object" in line:
                # self.line_end = str(round(float(self.line_end), 1) + 2)
                self.line_end = add_to_lineindex(self.line_end, 2)

            text_actions_list.tag_add("highlight", self.line_start, self.line_end)

            if self.line_start != self.line_start_save:
                self.line_start_save = self.line_start
            else:
                text_actions_list.tag_remove("highlight", 1.0, "end")
                self.line_start_save = 0

            # text_actions_list.tag_configure("highlight", background="bisque")
            # print(self.line_start)

            if int(float(floor_line_string(self.line_start))) == get_number_of_lines():
                print("jump_end")
                jump_end(start = False)

            if valid_input_digit(condition_inline):
                self.lb_condition_var.set(condition_inline)

        def remove_action():

            global text_actions_list

            start = self.line_start
            size_condition = 0
            text_actions_list.config(state=NORMAL)
            size_condition , line = get_condition_string()
            starter = round(0.1, 1)

            if ":" in line:
                # print("remove:" + start)
                if len(line) > 1:
                    for i in range(int(size_condition)):
                        starter = round(round(starter,1) + round(0.1, 1),1)
                    else:
                        self.line_start = str(math.floor(float(self.line_start)) + round(0.2, 1))

                print(self.line_start, self.line_end)
                text_actions_list.delete(self.line_start, self.line_end)
                text_actions_list.insert(self.line_start,"\n")
                text_actions_list.config(state=DISABLED)

                if "search_object" in line:
                    print(get_float_string_int(self.line_start))

                    # self.line_end = str(round(get_float_string_int(self.line_start), 1) + 1) + ".0"
                    self.line_end = add_to_lineindex(get_float_string_int(self.line_start), 1)
                    print(self.line_end)

                text_actions_list.tag_add("highlight", start, self.line_end)

                


        def search_func_disable_rld():

            rb_click_obj_R.config(state=DISABLED)
            rb_click_obj_L.config(state=DISABLED)
            rb_click_obj_D.config(state=DISABLED)

        def search_func_enable_rld():

            rb_click_obj_R.config(state=NORMAL)
            rb_click_obj_L.config(state=NORMAL)
            rb_click_obj_D.config(state=NORMAL)

        def OK():

            global file, script_name, rf_filename

            self.run_script = threading.Thread(target=thread_run_script)
            self.if_finished_td = threading.Thread(target=thread_isFinished_script)
            self.countdown_fm_thread = threading.Thread(target=countdown_frame)
            self.run_script.daemon = True
            self.if_finished_td.daemon = True
            self.countdown_fm_thread.daemon = True

            # countdown_frame()
            if not script_name:
                script_name = (rf_filename.get("1.0",END)).strip() ## not working for the 2nd time
            # sign_scripts_names(script_name)

            if os.path.getsize(file) > 0:
                ##### put on thread #####

                if not self.run_script.is_alive():
                    self.run_script.start()
                    # self.insert_filename_fm.destroy() # not working
                else:
                    print("{} is still Alive".format(run_script))

            else: # is empty
                Application.raise_an_error_msg("Running Error", "Can\'t run empty scenario")

            self.insert_filename_fm.destroy()

        def check_legal_object(obj_name):

            # obj_name += '\n'
            if obj_name in self.object_cb_list:
                return True
            else:
                return False

        def floor_line_string(line_string):

            if line_string == 'insert':
                return line_string
            else:
                return str(int(float(line_string))) + ".0"

        def get_object_condition_name():

            obj_name = self.cb_obj.get().strip()

            # print(obj_name)

            if check_legal_object(obj_name):

                if self.exists_clicked.get() == 0:
                    obj_name = obj_name + "_exists"
                if self.exists_clicked.get() == 1:
                    obj_name = obj_name + "_clicked"
                
                self.cb_obj.set("")

                return obj_name

            else:
                return False
            

        def if_command():


            obj_name = get_object_condition_name()

            print("o:{}".format(obj_name))

            if obj_name:

                btn_else.config(state=NORMAL)
                btn_if.config(state=DISABLED)
                btn_if_not.config(state=DISABLED)

                cond = condition() + 1
                self.lb_condition_var.set(cond)
                
                insert_to_actions_list("if({})".format(obj_name))
                btn_finish_condition.config(state=NORMAL)

            else:
                Application.raise_an_error_msg("Running Error", "Object Name Doen\'t exists")

        def if_not_command():

            obj_name = get_object_condition_name()

            if obj_name:

                btn_else.config(state=NORMAL)
                btn_if.config(state=DISABLED)
                btn_if_not.config(state=DISABLED)

                cond = condition() + 1
                self.lb_condition_var.set(cond)
            
                insert_to_actions_list("if_not({})".format(obj_name))
                btn_finish_condition.config(state=NORMAL)

            else:
                Application.raise_an_error_msg("Running Error", "Object Name Doen\'t exists")        

        def else_command():

            obj_name = get_object_condition_name()

            if obj_name:

                btn_if.config(state=NORMAL)
                btn_if_not.config(state=NORMAL)
                btn_else.config(state=DISABLED)

                cond = condition() - 1
                self.lb_condition_var.set(cond)
                edit_line(last_lineindex())
                self.lb_condition_var.set(cond + 1)

                insert_to_actions_list("{}".format("else({})".format(obj_name)))

            else:
                Application.raise_an_error_msg("Running Error", "Object Name Doen\'t exists")
            
        def cond_plus():

            global text_actions_list

            if get_number_of_lines() != 1:

                self.line_start = floor_line_string(self.line_start)
                start = self.line_start
                
                if self.line_end != END and self.line_end != 0:
                    print("Con Here")
                    condition_inline, line = get_condition_string()
                    size_condition = len(condition_inline)
                    set_condition(int(condition_inline.strip()) + 1)
                    if get_float_string_int(self.line_start) == get_number_of_lines() + 1:
                        self.line_start = add_to_lineindex(self.line_start, 1)
                    print(self.line_start, get_number_of_lines())
                    edit_line(self.line_start, str(condition()) + ":" + line[size_condition + 1:], condition = True)
                    text_actions_list.tag_add("highlight", start, self.line_end)
                
                else:
                    print("Else Here")
                    cond = condition() + 1
                    self.lb_condition_var.set(cond)

                    edit_line(last_lineindex())

        def cond_minus():

            global text_actions_list

            if get_number_of_lines() != 1:

                cond = get_condition_string(only_condition = True)
                if cond != "0" and cond != "": 

                    start = self.line_start

                    if self.line_end != END:

                        condition_inline, line = get_condition_string()
                        print("line:len:{}".format(len(line)))
                        if len(line) > 1:

                            if int(condition_inline) > 0:
                                print("line > 1")
                                set_condition(int(condition_inline) - 1)
                                size_condition = len(condition_inline)
                                edit_line(self.line_start, str(condition()) + ":" + line[size_condition + 1:], condition = True)

                        else:
                            print("line < 1")
                            set_condition(condition() - 1)
                            size_condition = len(condition_inline)
                            self.line_start = floor_line_string(self.line_start)
                            edit_line(self.line_start, str(condition()) + ":\n", condition = True)

                        
                        text_actions_list.tag_add("highlight", start, self.line_end)
                         
                    else:

                        cond = condition() - 1
                        self.lb_condition_var.set(cond)

                        edit_line(last_lineindex())
                print()

        def last_lineindex():

            global text_actions_list

            return text_actions_list.index("end-1c linestart")

        def edit_line(lineindex, text="", condition = False):

            global text_actions_list
            
            if self.line_end == 0:
                self.line_end = END

            # print(self.line_start, self.line_end)
            text_actions_list.config(state=NORMAL)
            text_actions_list.delete(lineindex, self.line_end)
            insert_to_actions_list(text , cond = condition)
            text_actions_list.config(state=DISABLED)

        def finish_condition():

            cond = condition() - 1
            
            if cond >= 0:
                self.lb_condition_var.set(cond)

            btn_if.config(state=NORMAL)
            btn_if_not.config(state=NORMAL)
            btn_else.config(state=DISABLED)

            edit_line(last_lineindex())

            if condition() == 0:
                btn_finish_condition.config(state=DISABLED)

        def jump_end(start = True):

            global text_actions_list

            if get_number_of_lines() > 1:

                text_actions_list.tag_remove("highlight", 1.0, "end")
                text_actions_list.tag_add("highlight", "{}.0".format(get_number_of_lines()), "end")
                # print("jump_end:{}".format(get_number_of_lines()))
                if start:
                    print("START")
                    print(get_number_of_lines() + 1)
                    self.line_start = "{}.0".format(get_number_of_lines() + 1)
                    # self.line_start = INSERT
                    # self.line_end = "{}.0".format(get_number_of_lines() + 1)
                    self.line_end = END
                else:
                    self.line_start = INSERT
                    self.line_end = END
                print(self.line_start, self.line_end)

        def generator_newFileName(filename):
            
            if not os.path.isfile("{}.py".format(filename)):
                return "{}.py".format(filename)
            else:
                i = 1
                while os.path.exists("{} ({}).py".format(filename, i)):
                    i += 1

                return "{} ({}).py".format(filename, i)

        def show_all_scenarios():

            Sas.SAS_application()

        def self_coding():

            global selfCodingFile, selfCodingDir

            if not os.path.exists(selfCodingDir):
                os.makedirs(selfCodingDir)

            src_name = selfCodingFile         
            selfCodingFile = generator_newFileName("{}/{}".format(selfCodingDir,selfCodingFile))
            print(selfCodingFile)
            instructions = "\t# Start to write your code here..\n" + \
                           "\t# Scenario script location: \'{}\'\n".format(selfCodingFile) + \
                           "\t# Change it if you want to.. \n"

            with open(selfCodingFile, "a") as self_coding_file:
                
                self_coding_file.write(Dictionary.get_starter_code() + instructions)
            
            os.system("\"{}\"".format(selfCodingFile))

            selfCodingFile = src_name

        def add_log():

            type_log = self.rb_log_type.get()

            log = self.tf_log_var.get().strip()

            if not log:
                Application.raise_an_error_msg("Input Error","Log field is empty !")
            else:
                self.tf_log_var.set("")
                insert_to_actions_list("log(\"{}\",\"{}\")".format(log, self.rb_log_type.get()))

        def insert_filename_frame():

            global script_name, rf_filename

            self.insert_filename_fm = Tk()
            self.insert_filename_fm.geometry("300x100")
            self.insert_filename_fm.title("Script Name")

            v = StringVar()
            v.set("Scenario Script Name:")
            lb_fm = Label(self.insert_filename_fm, textvariable=v)
            lb_fm.pack(side="top", fill='both', expand=True, padx=4, pady=4)

            rf_filename = Text(self.insert_filename_fm, width=20,height=1)
            rf_filename.pack(side="top", fill='both', expand=True, padx=4, pady=4)
            Button(self.insert_filename_fm, text='Cancel', command=self.insert_filename_fm.destroy).pack(side="right", fill='both', expand=True, padx=4, pady=4)
            Button(self.insert_filename_fm, text='OK', command=OK).pack(side="left", fill='both', expand=True, padx=4, pady=4)
            

        def countdown_td():

            for i in range(2,-1,-1):
                v = str(i)
                time.sleep(1)

                if i == 0:
                    v = "Start !"
                self.lb_coutdown.config(text=v)

            self.countdown_fm.destroy()
                
        def countdown_frame():

            self.countdown_fm = Tk()
            # self.countdown_fm.overrideredirect(True)  

            self.countdown_fm.geometry("300x100")
            self.countdown_fm.title("Countdown to Running:")

            Label(self.countdown_fm, text="Countdown to Running:", font=("Helvetica", 15)).pack(side="top", expand=True)
            self.lb_coutdown = Label(self.countdown_fm, text="3", font=("Helvetica", 25))
            self.lb_coutdown.pack(side="top",  expand=True)

            # self.countdown_fm.tkraise()
            # self.countdown_fm.mainloop()

            self.countdown_thread = threading.Thread(target=countdown_td)
            self.countdown_thread.start()

            self.countdown_fm.mainloop()


        def run():
            global file, script_name

            if len(file) == 0:
                save_as()

            Application.save(self)
            print("len(script_name):{}".format(len(script_name)))
            if len(script_name) == 0:
                if script_name == "":
                    insert_filename_frame()
            else:
                OK()
                
                

        fm2 = Frame(master)
        create_menu_bar(master)


        ############ AutoDesktop ############
        autodesktop_frame = LabelFrame(fm2, labelanchor=N, text="AutoDesktop", font="Arial 25 bold italic")
        autodesktop_frame.grid(row=0, column=0, columnspan=2, sticky=E+W, ipady=5, pady=5, ipadx=10)

        ############ Actions List ############
        scenarios_list = LabelFrame(fm2, text="Scenarios List", font="Arial 20 bold italic")
        scenarios_list.grid(row=1, column=1, sticky=N+W, ipady=5, ipadx=10)

        ############ Scenarios Actions ############
        scenarios_actions = LabelFrame(fm2, text="Scenarios Actions", font="Arial 20 bold italic")
        scenarios_actions.grid(row=1, column=0, sticky=N+W,ipady=5, ipadx=10)


        ############ OS Actions ############
        os_actions = LabelFrame(scenarios_actions, text="OS", font="Arial 15 bold italic")
        os_actions.grid(row=0, column=0, sticky=N+W,pady=2, ipady=5, padx=9, ipadx=10)

        ############ Search Object Actions ############
        search_object_frame = LabelFrame(scenarios_actions, text="Search Object", font="Arial 15 bold italic")
        search_object_frame.grid(row=1, column=0,columnspan=10, sticky=N+W, pady=2, ipady=5, padx=9, ipadx=10)

        ############ Condition ############
        condition_actions = LabelFrame(scenarios_actions, text="Condition", font="Arial 15 bold italic")
        condition_actions.grid(row=2, column=0, sticky=N+W,pady=2, ipady=5, padx=9, ipadx=10)

        ############ UI Actions ############
        ui_actions = LabelFrame(scenarios_actions, text="UI", font="Arial 15 bold italic")
        ui_actions.grid(row=3, column=0,columnspan=10, sticky=N+W, pady=2, ipady=5, padx=9, ipadx=10)

        ############ Keyboard Actions ############
        keyboard_actions = LabelFrame(scenarios_actions, text="Keyboard", font="Arial 15 bold italic")
        keyboard_actions.grid(row=4, column=0,columnspan=10, sticky=N+W,  ipady=1, padx=9, ipadx=10)


        ## Top title btns
        save_photo = PhotoImage(file="GUI_img/save_btn_1.png")
        save_btn = ttk.Button(autodesktop_frame, image=save_photo, command=self.save) 
        save_btn.grid(row=0, column=0, padx=10, pady=2)
        save_btn.image = save_photo

        btn_new_scenario = ttk.Button(autodesktop_frame, width=15, text='New Scenario', command=new_scenario_com)
        btn_new_scenario.grid(row=0, column=1, padx=0, pady=2)

        btn_open_scenario = ttk.Button(autodesktop_frame, width=15, text='Open Scenario', command=openfile)
        btn_open_scenario.grid(row=0, column=2, padx=10, pady=2)

        btn_show_all_scenarios = ttk.Button(autodesktop_frame, width=17, text='Show All Scenarios', command=show_all_scenarios)
        btn_show_all_scenarios.grid(row=0, column=3, padx=0, pady=2)

        btn_write_end = ttk.Button(autodesktop_frame, width=15, text='Add 2 The End', command=jump_end)
        btn_write_end.grid(row=0, column=4, padx=10, pady=2)

        btn_self_coding = ttk.Button(autodesktop_frame, width=15, text='Self Coding', command=self_coding)
        btn_self_coding.grid(row=0, column=5, padx=0, pady=2)

        ####### Sleep #######
        btn_sleep = ttk.Button(os_actions, width=15, text='Sleep', command=sleep)
        btn_sleep.grid(row=0, column=0,columnspan=2, padx=5, pady=2,sticky=W)
        Label(os_actions, text="Time:").grid(row=0, column=2, sticky=W, padx=2)
        self.tf_sleep_var = StringVar()
        tf_sleep = Entry(os_actions,  width=7, textvariable=self.tf_sleep_var)
        tf_sleep.grid(row=0, column=3, sticky=W)
        tf_sleep.insert(INSERT, "1")

        ####### Log #######
        btn_log = ttk.Button(os_actions, width=15, text='Log', command=add_log)
        btn_log.grid(row=1, column=0,columnspan=2, padx=5, pady=2,sticky=W)
        Label(os_actions, text="Text:").grid(row=1, column=2, sticky=W, padx=2)
        self.tf_log_var = StringVar()
        tf_log = Entry(os_actions, width=14, textvariable=self.tf_log_var)
        tf_log.grid(row=1, column=3, sticky=W)
        
        self.rb_log_type.set("Info") 
        rb_log_info = Radiobutton(os_actions, width = 6, text="Info", variable=self.rb_log_type, value="Info")
        rb_log_err = Radiobutton(os_actions, width = 6, text="Error", variable=self.rb_log_type, value="Error")
        rb_log_info.grid(sticky=W, row=1, column=4)
        rb_log_err.grid(sticky=W ,row=1, column=5)

        ####### IF/ELSE #######
        btn_if = ttk.Button(condition_actions, width=6, text='If', command=if_command)
        btn_if.grid(row=0, column=0, pady=2, padx=5)
        btn_if_not = ttk.Button(condition_actions, width=6, text='If Not', command=if_not_command)
        btn_if_not.grid(row=0, column=1, pady=2)
        btn_else = ttk.Button(condition_actions, width=6, text='Else', command=else_command)
        btn_else.grid(row=1, column=0, pady=2)
        btn_else.config(state=DISABLED)

        btn_finish_condition = ttk.Button(condition_actions, width=6, text='Finish', command=finish_condition)
        btn_finish_condition.grid(row=1, column=1, sticky=W)
        btn_finish_condition.config(state=DISABLED)
        
        Label(condition_actions, text="Object:").grid(row=0, column=3, sticky=W,padx=8)
        # self.box_value = StringVar()
        self.cb_obj = ttk.Combobox(condition_actions, width=15)
        # self.box.current(0)
        self.cb_obj.grid(row=0, column=4, columnspan=2 , sticky=W)

        Label(condition_actions, text="Condition:").grid(row=0, column=6, sticky=W, padx=2)
        self.lb_condition_var.set("0")
        lb_condition = Label(condition_actions, font = "Helvetica 15 bold", textvariable = self.lb_condition_var).grid(row=0, column=7, sticky=W, padx=2)


        rb_exists = Radiobutton(condition_actions, width = 6, text="Exists", variable=self.exists_clicked, value=0)
        rb_clicked = Radiobutton(condition_actions, width = 6, text="Clicked", variable=self.exists_clicked, value=1)
        rb_exists.grid(sticky=W, row=1, column=3)
        rb_clicked.grid(sticky=W ,row=1, column=4)

        ####### Search Object #######
        btn_search_object = ttk.Button(search_object_frame, width=15, text='Search Object', command=search_object_com)
        btn_search_object.grid(row=0, column=0, padx=5, pady=2, columnspan=2, sticky=W)

        # Path
        Label(search_object_frame, text="Path:").grid(row=1, column=0, sticky=W,padx=5)
        self.tf_search_object_var = StringVar()
        tf_search_object = Entry(search_object_frame, width=8, textvariable=self.tf_search_object_var)
        tf_search_object.grid(row=1, column=1, sticky=W)

        # Browse
        btn_browse = ttk.Button(search_object_frame,width=3, text="...", command=get_path)  
        btn_browse.grid(row=1, column=2,columnspan=2, padx=5,sticky=W)

        rb_click_obj_R = Radiobutton(search_object_frame, width = 3, text="Left", variable=self.rlb, value=0)
        rb_click_obj_L = Radiobutton(search_object_frame, width = 5, text="Right", variable=self.rlb, value=1)
        rb_click_obj_D = Radiobutton(search_object_frame, width = 6, text="Double", variable=self.rlb, value=2)
        rb_click_obj_R.grid(sticky=W, row=1, column=3)
        rb_click_obj_L.grid(sticky=W ,row=1, column=4)
        rb_click_obj_D.grid(sticky=W ,row=1, column=5)
        search_func_disable_rld()

        # search attempts
        self.tf_search_attempts_var = StringVar()
        Label(search_object_frame,text="Attempts:").grid(row=2, column=0, sticky=W,padx=5)
        tf_search_attempts = Entry(search_object_frame, textvariable=self.tf_search_attempts_var, width=8)
        tf_search_attempts.grid(row=2, column=1, sticky=W)
        tf_search_attempts.insert(INSERT, "3")

        # search sleep
        self.tf_search_sleep_var = StringVar()
        Label(search_object_frame, text="Sleep:").grid(row=2, column=2, sticky=W,padx=5)
        tf_search_sleep = Entry(search_object_frame, textvariable=self.tf_search_sleep_var, width=8)
        tf_search_sleep.grid(row=2, column=3,columnspan=3, sticky=W)
        tf_search_sleep.insert(INSERT, "1")

        
        rb_click_find = Radiobutton(search_object_frame, text="Find", variable=self.search_func, value=0,command=search_func_disable_rld)
        rb_click_click = Radiobutton(search_object_frame, text="Click", variable=self.search_func, value=1,command=search_func_enable_rld)
        rb_click_getcoordinate = Radiobutton(search_object_frame, text="Coordinate", variable=self.search_func, value=2)
        rb_click_find.grid(sticky=W, row=0, column=2)
        rb_click_click.grid(sticky=W ,row=0, column=3)
        rb_click_getcoordinate.grid(sticky=W ,row=0, column=4, columnspan=2)

        ####### Move Mouse #######
        btn_move_mouse = ttk.Button(ui_actions, width = 15, text='Move Mouse', command=move_mouse_com)
        btn_move_mouse.grid(row=3, column=0, pady=2, padx=5)

        # Mouse X
        Label(ui_actions,text="X:").grid(row=3, column=1, sticky=W)
        self.tf_move_mouse_x_var = StringVar()
        tf_move_mouse_x = Entry(ui_actions, width=7, textvariable=self.tf_move_mouse_x_var)
        tf_move_mouse_x.grid(row=3, column=2, sticky=W)
        tf_move_mouse_x.insert(INSERT, "1")

        # Mouse Y
        Label(ui_actions, text="Y:").grid(row=3, column=3, sticky=W, padx=5)
        self.tf_move_mouse_y_var = StringVar()
        tf_move_mouse_y = Entry(ui_actions, width=7, textvariable=self.tf_move_mouse_y_var)
        tf_move_mouse_y.grid(row=3, column=4, sticky=W)
        tf_move_mouse_y.insert(INSERT, "1")

        # Mouse Speed
        Label(ui_actions, text="Speed:").grid(row=3, column=5, sticky=W, padx=5)
        self.tf_move_mouse_speed_var = StringVar()
        tf_move_mouse_speed = Entry(ui_actions, width=7, textvariable=self.tf_move_mouse_speed_var)
        tf_move_mouse_speed.grid(row=3, column=6, sticky=W)
        tf_move_mouse_speed.insert(INSERT, "0")

        ####### Click #######
        btn_click = ttk.Button(ui_actions, width = 15, text='Click', command = click)
        btn_click.grid(row=4, column=0, pady=2)

        # Click Times
        self.tf_click_time_var = StringVar()
        Label(ui_actions, text="Times:").grid(row=4, column=1, ipadx=5)
        tf_click_time = Entry(ui_actions, textvariable=self.tf_click_time_var ,width=7)
        tf_click_time.insert(INSERT, "1")
        tf_click_time.grid(row=4, column=2, sticky=W)

        # Click Speed
        self.tf_click_speed_var = StringVar()
        Label(ui_actions, text="Speed:").grid(row=4, column=3, sticky=W, padx=5)
        tf_click_speed = Entry(ui_actions,textvariable=self.tf_click_speed_var , width=7)
        tf_click_speed.insert(INSERT, "0")
        tf_click_speed.grid(row=4, column=4, sticky=W)

        rb_click_R = Radiobutton(ui_actions, width = 5, text="Left", variable=self.rbv, value=1)
        rb_click_L = Radiobutton(ui_actions, width = 5, text="Right", variable=self.rbv, value=0)
        rb_click_R.grid(sticky=E, row=4, column=5)
        rb_click_L.grid(sticky=W ,row=4, column=6)

        ####### Keyboard Actions Widgets ########
        ### Type Text ###
        btn_typetext = ttk.Button(keyboard_actions, width = 15, text='Type Text', command = typetext)
        btn_typetext.grid(row=0, column=0, pady=2, padx=5)

        # Type Text Times
        self.tf_typetext_text_var = StringVar()
        Label(keyboard_actions, text="Text:").grid(row=0, column=1)
        tf_typetext_text = Entry(keyboard_actions, textvariable=self.tf_typetext_text_var, width=7)
        tf_typetext_text.grid(row=0, column=2, sticky=W)

        # Type Text Speed
        Label(keyboard_actions, text="Speed:").grid(row=0, column=3, sticky=W, padx=5)
        self.tf_typetext_speed_var = StringVar()
        tf_typetext_speed = Entry(keyboard_actions, textvariable=self.tf_typetext_speed_var, width=7)
        tf_typetext_speed.insert(INSERT, "0")
        tf_typetext_speed.grid(row=0, column=4, sticky=W)

        ### Keyboard press ###
        btn_keypress = ttk.Button(keyboard_actions, width = 15, text='Keyboard Press', command = press_keyboard)
        btn_keypress.grid(row=1, column=0, pady=2)
        Label(keyboard_actions, text="Key:").grid(row=1, column=1)
        self.tf_keypress_var = StringVar()
        tf_keypress = Entry(keyboard_actions,textvariable=self.tf_keypress_var, width=7)
        tf_keypress.grid(row=1, column=2, sticky=W)
        btn_multipress = ttk.Button(keyboard_actions, width = 15, text='MultiPress', command = multipress_typekey)
        btn_multipress.grid(row=2, column=0, pady=2)

        from_list = ttk.Button(keyboard_actions, text="Choose From List", command=choose_from_list)
        from_list.grid(row=1, column=3, columnspan=3, pady=2, padx=5)


        
        ############ Action List ############        
        # text field
        text_actions_list = Text(master=scenarios_list, height=27, width=35)
        text_actions_list.grid(row=2, column=1,columnspan=20, pady=2 , padx=10)
        text_actions_list.insert(INSERT, "0:")
        text_actions_list.tag_configure("highlight", background="#5DADE2")
        text_actions_list.tag_add("highlight", "0.0", "end")


        scr_v = Scrollbar(scenarios_list, orient=VERTICAL, command=text_actions_list.yview)
        scr_v.grid(row=2, column=11, columnspan=15, sticky=N+S)

        # scr_h = Scrollbar(scenarios_list, orient=HORIZONTAL, command=text_actions_list.xview)
        # scr_h.grid(row=3, column=1, columnspan=15, sticky=W+E)
        
        text_actions_list.config(yscrollcommand=scr_v.set, font=('Arial', 10))
        # text_actions_list.config(xscrollcommand=scr_h.set, font=('Arial', 10))
        text_actions_list.config(font=('Arial', 10))
        text_actions_list.config(state=DISABLED)
        text_actions_list.bind("<Button 1>",select)

        btn_write_end = ttk.Button(scenarios_list, width=36, text='Write To The End', command=jump_end)
        btn_write_end.grid(row=3, column=1, columnspan=15, padx=15)

        # remove Action
        btn_remove_action = ttk.Button(scenarios_list, width = 16, text='Remove Action', command=remove_action)
        btn_remove_action.grid(row=4, column=1, padx=15, pady=5, sticky=W)

        # Clear Actions
        btn_clear_actions_list = ttk.Button(scenarios_list, width = 17, text='Clear Actions', command=clear_actions_list)
        btn_clear_actions_list.grid(row=4, column=2, columnspan=2)

        # Increase Condition Actions
        Label(scenarios_list, text="Condition Generator :").grid(row=5, column=1 , padx=10)
        condition_pluse = ttk.Button(scenarios_list, width = 3, text='+', command=cond_plus)
        condition_pluse.grid(row=5, column=2)
        condition_minus = ttk.Button(scenarios_list, width = 3, text='-', command=cond_minus)
        condition_minus.grid(row=5, column=3)

        ####### EXIT #######
        ttk.Button(fm2, width = 15, text='EXIT', command=self.quit).grid(row=4, column=0, pady=5)

        ####### RUN #######
        ttk.Button(fm2, width = 15, text='RUN', command=run).grid(row=4, column=1, pady=5)

        fm2.pack(anchor=CENTER, padx=10)
        root.protocol('WM_DELETE_WINDOW', self.quit)


        self.openfile = openfile
        # self.save = save

        ####### Shortkeys #######
        root.bind_all("<Control-q>", func=quit)
        root.bind_all("<Control-s>", func=Application.save)
        root.bind_all("<Control-Shift-S>", func=Application.save_as)
        root.bind_all("<F1>", func=Application.help_frame)


        if disable_unsupported:
            rb_click_getcoordinate.config(state=DISABLED)

list_TF = []

root = Tk()
root.geometry("1100x850")
root.title("AutoDesktop")
root.iconbitmap(default='icon.ico')
app = Application(root)
root.mainloop()
root.destroy()