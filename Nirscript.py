from AutoDesktop import *

if __name__ == '__main__':

	Keyboard.set_keyboard()
	OS.log_filename("Nirscript.txt")
	Keyboard.keyboard_press("winleft")
	Keyboard.keyboard_type("pc",0)
	Keyboard.keyboard_press("enter")
	OS.do_sleep(1)
	C_driver = UIElem("C:/AutoDesktop/Test_imgs/C_driver.png",3,1)
	C_driver_clicked = C_driver.click("Double")
	if not(C_driver_clicked):
		OS.log("Cannot clicked on C_driver")
	else:
		full_size = UIElem("C:/AutoDesktop/Test_imgs/full_size.png",3,1)
		full_size_clicked = full_size.click('Single')
		new_folder = UIElem("C:/AutoDesktop/Test_imgs/new_folder.png",3,1)
		new_folder_clicked = new_folder.click('Single')
		if not(new_folder_clicked):
			OS.log("Cannot clicked on new_folder")
		else:
			Keyboard.keyboard_type("test_folder",0.1)
			Keyboard.keyboard_press("enter")
			Keyboard.keyboard_press("up")
			Keyboard.keyboard_press("up")
			Keyboard.keyboard_press("up")
			Keyboard.keyboard_press("up")
			Keyboard.keyboard_press("up")
			test_folder = UIElem("C:/AutoDesktop/Test_imgs/test_folder.png",3,1)
			test_folder_clicked = test_folder.click("Right")
			if not(test_folder_clicked):
				OS.log("Cannot found test_folder")
				Keyboard.keyboard_press("down")
				Keyboard.keyboard_press("down")
				Keyboard.keyboard_press("down")
				Keyboard.keyboard_press("down")
				Keyboard.keyboard_press("down")
				Keyboard.keyboard_press("delete")
			if(test_folder_clicked):
				Keyboard.keyboard_press("up")
				Keyboard.keyboard_press("up")
				Keyboard.keyboard_press("up")
				Keyboard.keyboard_press("enter")
				Keyboard.keyboard_press("enter")
			test_folder = UIElem("C:/AutoDesktop/Test_imgs/test_folder.png",1,1)
			test_folder_exists = test_folder.find()
			if(test_folder_exists):
				OS.log("Cannot Delete \'test folder\'")
			else:
				OS.log("'Delete \'test folder\''")
				OS.log("test PASSED")
