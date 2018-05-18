from AutoDesktop import *

if __name__ == '__main__':

	Keyboard.set_keyboard()
	OS.log_filename("passed_test.txt")
	OS.log("Start Scenario","Info")
	Mouse.move_mouse(100,100,1)
	windows = UIElem("C:/AutoDesktop/windows.PNG",3,1)
	windows_clicked = windows.click("Single")
	if(windows_clicked):
		Mouse.move_mouse(100,100,1)
		OS.log("Passed Test","Info")
	else:
		OS.log("Failed Test","Error")
