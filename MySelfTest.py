from AutoDesktop import *

if __name__ == '__main__':

	Keyboard.set_keyboard()
	# Start to write your code here..
	# Scenario script location: 'Self Coding Scripts/self_coding (3).py'
	# Change it if you want to..

	# open the network connection
	OS.log_filename("MySelfTest")
	OS.log("Scenario Start !")

	OS.log("open the network connection")
	Keyboard.keyboard_multiPress("winleft r")
	Keyboard.keyboard_type("ncpa.cpl",0.2)
	Keyboard.keyboard_press("enter")

	# create element of the network connection title object
	# to verify if the window opened
	OS.log("verify if the window opened")
	OS.do_sleep(2)
	net_con = UIElem("C:/AutoDesktop/Test_imgs/network_connection.png",3 ,1)
	print(net_con)
	net_con_exisit = net_con.find()

	print("0")
	if not net_con_exisit:
		print("1")
		OS.log("Try to find the 'network_connection_unfocused'")
		net_con_unfocused = UIElem("C:/AutoDesktop/Test_imgs/network_connection_unfocused.png",2 ,1)
		net_con_unfocused_exisit = net_con_unfocused.find()
		
		if not net_con_unfocused_exisit:
			print("2")
			OS.log("The network connection window wasn't open", "Error")
			OS.END()

	# create element of the enthernet_3 object
	OS.log("Opened the network connection window")
	enthernet = UIElem("C:/AutoDesktop/Test_imgs/enthernet.png",2 ,1)
	enthernet_clicked = enthernet.click()

	if not enthernet_clicked:
		OS.log("Try to click the enthernet that was choosen (blue)")
		enthernet = UIElem("C:/AutoDesktop/Test_imgs/enthernet_3_blue.png",2 ,1)
		enthernet_clicked = enthernet.click()
		
		if not enthernet_clicked:
			OS.log("The enthernet object wasn't click", "Error")
			OS.END()

	OS.log("Clicked enthernet object ")
	OS.log("Try to right click on enthernet object ")
	enthernet_clicked = enthernet.click(click_type="Right")
	
	if not enthernet_clicked:
		OS.log("Cannot do right click on enthernet", "Error")
		OS.END()

	OS.log("Do right click on enthernet")
	Keyboard.keyboard_press("down")
	Keyboard.keyboard_press("enter")
	
	OS.log("Disable enthernet")
	OS.log("Moving mouse to coordinate: 100,100")
	Mouse.move_mouse(100,100,0.5)

	OS.log("Do sleep 3 sec")
	OS.do_sleep(3)
	
	OS.log("Try to right click on disabled_ethernet object ")
	disabled_ethernet = UIElem("C:/AutoDesktop/Test_imgs/disabled_ethernet.png",3 ,1)
	disabled_ethernet_clicked = disabled_ethernet.click(click_type="Right")
	if not disabled_ethernet_clicked:
		OS.log("Cannot do right click on disabled_ethernet", "Error")
		OS.END()

	OS.log("Enable the disabled_ethernet")
	Keyboard.keyboard_press("down")
	Keyboard.keyboard_press("enter")

	OS.log("Do sleep 3 sec")
	OS.do_sleep(3)

	OS.log("Verify if the ethernet is up")
	ethernet_frame = UIElem("C:/AutoDesktop/Test_imgs/ethernet_frame.png",3 ,1)
	ethernet_frame_exsist = ethernet_frame.find()

	if not ethernet_frame_exsist:
		OS.log("The test failure", "Error")
		OS.END()
	
	OS.log("Ethernet is up")
	OS.log("The test Passed")






	