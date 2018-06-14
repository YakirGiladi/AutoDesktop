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
	print("3")
	# create element of the enthernet_3 object
	OS.log("Opened the network connection window")
	enthernet_3 = UIElem("C:/AutoDesktop/Test_imgs/enthernet_3.png",2 ,1)
	enthernet_3_clicked = enthernet_3.click()

	if not enthernet_3_clicked:
		OS.log("Try to click the enthernet_3 that was choosen (blue)")
		enthernet_3_blue = UIElem("C:/AutoDesktop/Test_imgs/enthernet_3_blue.png",2 ,1)
		enthernet_3_blue_clicked = enthernet_3_blue.click()
		
		if not enthernet_3_blue_clicked:
			OS.log("The enthernet_3 object wasn't click", "Error")
			OS.END()
	

	OS.log("Clicked enthernet_3 object ")
