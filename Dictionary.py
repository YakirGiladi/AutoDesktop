#!/usr/bin/python3
# -*- coding: utf-8 -*-
import AutoDesktop
import os
import winsound
import time
import win32gui
import win32con

run_script = True
sleep_time = True

num_indentation = 0
indentation = ""
frequency = 1000  # Set Frequency To 2500 Hertz
duration = 100  # Set Duration To 1000 ms == 1 second

# content_code = "from AutoDesktop import *\n\nif __name__ == '__main__':\n\n"
content_code = "from AutoDesktop import *\n\nif __name__ == '__main__':\n\n\tKeyboard.set_keyboard()\n"


action_dictionary = {"log":"OS.log"
                    ,"sleep":"OS.do_sleep"
                    ,"move_mouse":"Mouse.move_mouse"
                    ,"click":"Mouse.mouse_click"
                    ,"search_object":"UIElem"
                    ,"press_keyboard":"Keyboard.keyboard_press"
                    ,"typetext":"Keyboard.keyboard_type"
                    ,"keyboard_multiPress":"Keyboard.keyboard_multiPress"
                    ,"if":"if"
                    ,"if_not":"if not"
                    ,"else":"else:\n"}



def get_dictionary():

    return action_dictionary

def get_starter_code():

    return content_code

def handle_search_object_action(obj_name, scen_action, obj_func, code_file):
    
    search_type = ""
    obj_name = obj_name.strip()
    obj_func = obj_func.strip()

    cmd_write = indentation + obj_name + " = " + scen_action
    code_file.write(cmd_write)
    # print(cmd_write)

    if obj_func == "find()":
        search_type = "_exists = "
    elif "click(" in obj_func :
        search_type = "_clicked = "

    cmd_write = indentation + obj_name + search_type + obj_name + "." + obj_func + "\n"
    code_file.write(cmd_write)
    # print(cmd_write)

def indentation_creator(num_indentation):

    global indentation
    indentation = ""

    for i in range(num_indentation):
        indentation += "\t" 

def condition_handler(action):

    global num_indentation

    if len(action) > 1:
        num_indentation = int(action.split(":")[0]) + 1
        indentation_creator(num_indentation)

def convert_code(filename = "C:/AutoDesktop/Test_imgs/AutoTest.txt", code_file = "code_file"):

    global indentation, num_indentation, content_code

    scenario_filename = filename
    code_filename = code_file

    content_code = content_code + "\tOS.log_filename(\"{}.txt\")\n".format(code_filename)

    if not ".py" in code_filename:
        code_filename += ".py"
    with open(code_filename,"w") as code_file:
        code_file.write(content_code)

        with open(scenario_filename,"r") as scenario_file:
            for action in scenario_file:
                
                condition_handler(action)
                # print(num_indentation)
                if "(" in action:

                    index2 = action.index("(")
                    index1 = action.index(":") + 1
                    
                    if "search_object" in action:

                        scen_action = action_dictionary[action[index1:index2]] + action[index2:]
                        obj_name = next(scenario_file)
                        obj_func = next(scenario_file)
                        handle_search_object_action(obj_name,scen_action,obj_func,code_file)
                        
                    else:
                        if "if" in action:
                            action = action_dictionary[action[index1:index2]] + action[index2:].strip() + ":\n"
                        elif "else" in action:
                            # print(action[index1:index2])
                            action = action_dictionary[action[index1:index2]]
                        else:
                            action = action_dictionary[action[index1:index2]] + action[index2:]
                        code_file.write("{}{}".format(indentation,action))
                        # print(action)



def run_scenario(code_filename = "code_file"):

    if run_script:
        if sleep_time:
            for i in range(3):
                winsound.Beep(frequency, duration)
                time.sleep(0.9)

        for i in range(2):
            Minimize = win32gui.GetForegroundWindow()
            win32gui.ShowWindow(Minimize, win32con.SW_MINIMIZE)

        if not ".py" in code_filename:
            code_filename += ".py"
        AutoDesktop.Keyboard.keyboard_multiPress("winleft d")
        os.system("python {}".format(code_filename))

# run_scenario("6")

# convert_code()
# run_scenario()
# keyboard_multiPress
# keyboard_type
# keyboard_press
# mouse_coordinates
# mouse_click
# mouse_click_coordinates
# move_mouse
# set_keyboard
# UIElem