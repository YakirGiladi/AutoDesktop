import time
import os
import logging
import win32api
import winsound
import ctypes
from pyautogui import *
from pywinauto import application
import numpy as np
import cv2
import pyscreenshot as ImageGrab

enable_log = True

# from pywinauto import *
# from pywinauto.application import Application
# from pywinauto.application import ProcessNotFoundError

# # create new logger file
# logging.basicConfig(filemode='w')

# create and configure logger
logger = logging.getLogger('AutoDesktop')
logger.setLevel(logging.INFO)

# create formatters
file_formatter = logging.Formatter('[%(asctime)-15s][%(levelname)-5s] - %(message)s')
# file_formatter = logging.Formatter('[%(asctime)-15s] - %(message)s')
# file_formatter = logging.Formatter('%(levelname)-8s - %(message)s')
# console_formatter = logging.Formatter('%(message)s')

# create file handler
file_handler = logging.FileHandler('AutoDesktop_Logs.txt',mode='w') # 'w' overwrite (write mode))
file_handler.setLevel(logging.INFO)

# create console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

file_handler.setFormatter(file_formatter)
# console_handler.setFormatter(console_formatter)

# add handlers to logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

APP_PATH = 'c:/windows/system32/'



#### OS ####
class OS():

    def do_sleep(sec = 1):
        time.sleep(sec)
        log("Sleeing {} sec".format(sec))

    def make_noise(freq, duration, sleep):
        winsound.Beep(freq, duration)
        time.sleep(sleep)

    def log_enable(enable = True):
        global enable_log
        enable_log = enable 

    def log(text='',log_type="Info"):
        if enable_log:
            if log_type == "Info":
                logger.info(text)
            elif log_type == "Error":
                logger.error(text)


class UIElem():
    """
    Represents UI element (button, link)
    """

    def __init__(self, elem, attempts = 3, sleep_time = 1):
        # image of needed ui element
        self.screen = elem
        # center coordinat
        self.x = None
        self.y = None
        # pause between events
        self.timeout = sleep_time # was 0.7
        # max attempts to try fo click or find ui element
        self.max_attempts = attempts
        self.mouse_speed = 0.5

    def get_coordinates(screen):

        x = None
        y = None
        scns = "screenshot.png"

        screenshot = ImageGrab.grab()
        screenshot.save(scns)

        img_rgb = cv2.imread(scns)
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        os.remove(scns) # remove the screenshot

        template = cv2.imread(screen,0)
        w, h = template.shape[::-1]

        res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
        
        threshold = 0.8
        loc = np.where( res >= threshold)
       
        if loc[1]:
            x = loc[1][0] + w/2
            y = loc[0][0] + h/2

        return x, y

    def coordinates(self):

        attempts = 0

        while attempts < self.max_attempts:
            try:
                
                self.x, self.y = UIElem.get_coordinates(self.screen)

                if (self.x and self.y) != None:

                    return self.x, self.y

                attempts += 1
                logger.info('Cannot found {}. attempts={}'.format(self.screen, attempts))
                
                if self.timeout > 0:
                    time.sleep(self.timeout)

            except Exception as err:
                logger.info('{}. Warning: {}. attempts={}'.format(self.screen, err, attempts+1))
                # time.sleep(self.sleep)
                attempts += 1
                continue
                
        return self.x, self.y


    def click(self, click_type='Single', coordinates=True):
        """
        click types: simple, double, right
        """
        attempts = 0
        clicked = False
        
        while attempts < self.max_attempts:
            try:
                
                self.x, self.y = UIElem.get_coordinates(self.screen)

                if (self.x and self.y) != None:

                    found = True

                    moveTo(self.x, self.y, self.mouse_speed)
                    if click_type == 'Single':
                        click(self.x, self.y)
                    elif click_type == 'Double':
                        doubleClick(self.x, self.y)
                    elif click_type == 'Right':
                        click(self.x, self.y, button='right')
                    clicked = True
                    time.sleep(self.timeout)


                    if coordinates:
                        logger.info('Found {} coordinates: {}, {}'.format(self.screen, self.x, self.y))
                    else:
                        logger.info('Found {}'.format(self.screen)) 

                    break # break the loop

                attempts += 1
                logger.info('Cannot found {}. attempts={}'.format(self.screen, attempts))
                
                if self.timeout > 0:
                    time.sleep(self.timeout)
            except TypeError as err:
                logger.info('{}. Warning: {}. attempts={}'.format(self.screen, err, attempts+1))
                # time.sleep(self.sleep)
                attempts += 1
                continue

        return clicked


        # while attempts < self.max_attempts:
        #     try:
        #         self.x, self.y = locateCenterOnScreen(self.screen)

        #         if coordinates:
        #             logger.info('{} click on {} coordinates: {}, {}'.format(click_type ,self.screen, self.x, self.y))
        #         else:
        #             logger.info('{} click on {}'.format(click_type, self.screen))

        #         moveTo(self.x, self.y, self.mouse_speed)
        #         if click_type == 'Single':
        #             click(self.x, self.y)
        #         elif click_type == 'Double':
        #             doubleClick(self.x, self.y)
        #         elif click_type == 'Right':
        #             click(self.x, self.y, button='right')
        #         clicked = True
        #         # time.sleep(self.timeout)               
        #         break

        #     except TypeError as err:
        #         logger.info('{}. Warning: {}. attempts={}'.format(self.screen, err, attempts+1))
        #         # time.sleep(self.sleep)
        #         attempts += 1
        #         continue

        # return clicked

    def find(self, coordinates=True):
        """
        find neede image on the screen
        """
        scns = "screenshot.png"
        attempts = 0
        found = False

        while attempts < self.max_attempts:
            try:
                screenshot = ImageGrab.grab()
                screenshot.save(scns)

                img_rgb = cv2.imread(scns)
                img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
                os.remove(scns) # remove the screenshot

                template = cv2.imread(self.screen,0)
                w, h = template.shape[::-1]

                res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
                
                threshold = 0.8
                loc = np.where( res >= threshold)
               
                if loc[1]:
                    self.x = loc[1][0] + w/2
                    self.y = loc[0][0] + h/2

                    counter = 0
                    found = True

                    if coordinates:
                        logger.info('Found {} coordinates: {}, {}'.format(self.screen, self.x, self.y))
                    else:
                        logger.info('Found {}'.format(self.screen))
                    break

                attempts += 1
                logger.info('Cannot found {}. attempts={}'.format(self.screen, attempts))
                
                if self.timeout > 0:
                    time.sleep(self.timeout)

            except Exception as err:
                logger.info('{}. Warning: {}. attempts={}'.format(self.screen, err, attempts+1))
                # time.sleep(self.sleep)
                attempts += 1
                continue

        return found
        
class Keyboard():

    def set_keyboard(id=67699721):

        win32api.LoadKeyboardLayout('00000409',1) # to switch to english

        user32 = ctypes.WinDLL('user32', use_last_error=True)
        curr_window = user32.GetForegroundWindow()
        thread_id = user32.GetWindowThreadProcessId(curr_window, 0)
        klid = user32.GetKeyboardLayout(thread_id)

        while(1):
            if klid != 67699721:
                hotkey('alt', 'shift')
                user32 = ctypes.WinDLL('user32', use_last_error=True)
                curr_window = user32.GetForegroundWindow()
                thread_id = user32.GetWindowThreadProcessId(curr_window, 0)
                klid = user32.GetKeyboardLayout(thread_id)
            else:
                logger.info('Language set')
                break
    def keyboard_press(key):
        press(key)
        logger.info('Pressed {}'.format(key))

    def keyboard_type(type_write, speed=0):
        typewrite(type_write,speed)
        logger.info("typed \'{}\'' in speed {}".format(type_write,speed))

    def keyboard_multiPress(multi):
        multi_list = multi.split(" ")
        logger.info('Multi pressed on {}'.format(multi_list))
        for i in range(len(multi_list)):
            keyDown(multi_list[i])
        for i in reversed(range(len(multi_list))):
            keyUp(multi_list[i])

class Mouse():

    def move_mouse(x=0, y=0, speed=0):

        moveTo(x,y,speed)
        logger.info('Mouse moved to {},{} in speed {}'.format(x,y,speed))

    def mouse_click_coordinates(x,y,click_type='Single',clicks=1,  speed=0):

        if click_type == 'Single':
            click(x, y, clicks=clicks, interval=speed)
        elif click_type == 'Double':
            doubleClick(x, y, interval=speed)
        elif click_type == 'Right':
            click(x, y, button='right', clicks=clicks, interval=speed)
        logger.info('Mouse did {} click on {},{} {} times by speed {}'.format(click_type, x,y,clicks,speed))
        

    def mouse_click(click_type='Single', clicks=1, speed=0):

        print(click_type, clicks, speed)
        x,y = mouse_coordinates()
        mouse_click_coordinates(x,y, click_type=click_type, clicks=clicks, speed=speed)
        logger.info('Mouse clicked {} times by speed {}'.format(clicks,speed))
        
    def mouse_coordinates():

        return position()


# if __name__ == '__main__':
#     wifi = UIElem('nf.png')
#     x,y = wifi.coordinates()
#     print(x,y)

# Mouse.move_mouse(100,100,1)

# keyboard_multiPress('ctrl alt delete')
# def open(app='Notepad.exe'):
#     Application().start(app)

############### SHOW #################
# set_keyboard(67699721)
# press('winleft')
# typewrite('run')
# press('enter')
# time.sleep(1)
# typewrite('ncpa.cpl')
# press('enter')

# wifi_exists = wifi.find()
# if wifi_exists:
#     wifi.click('Double')
# else:
#     print('Not Found')
######################################


# My keyboard is set to the English - United States keyboard

# For debugging Windows error codes in the current thread


# nwa.SetFocus()
# nwa.Network_Connections.Shell_Folder_View('ItemsView->Ethernet')
# Application().Start("CabinetWClass")
# press('win')
# typewrite('ncpa.cpl')
# press('enter')

# app.Window_(title='Title', class_name='#32770')

# app = application.Application()
# app.Start("Notepad.exe")