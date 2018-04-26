import numpy as np
import cv2
import pyscreenshot as ImageGrab
from pyautogui import *
import os
import math
from matplotlib import pyplot as plt

if __name__ == '__main__':

    # screenshot = ImageGrab.grab()
    # screenshot.save('screenshot.png')
# attribute:3.7416573867739413
# attribute:3.7416573867739413
# avg:26.72612419124244
# avg:26.72612419124244

    scns1 = "view.png"
    # scns2 = "delete_70per.png"
    # scns2 = "delete_60per.png"
    # scns2 = "delete_50per.png"
    # scns2 = "delete_25per.png"
    # scns2 = "delete_24per.png"
    scns2 = "view.jpg"
    scns2 = "view.bmp"
    img1 = cv2.imread(scns1,0)
    img2 = cv2.imread(scns2,0)

    # create a mask
    # mask = np.zeros(img.shape[:2], np.uint8)
    # mask[100:400, 100:400] = 255
    # masked_img = cv2.bitwise_and(img,img,mask = mask)
    # Calculate histogram with mask and without mask
    # Check third argument for mask
    jim1 = cv2.calcHist([img1],[0],None,[255],[0,255])
    jim2_hlaf = cv2.calcHist([img2],[0],None,[255],[0,255])
    # print(jim1)
    sum_jim1 = sum(jim1)[0]
    sum_jim2_hlaf = sum(jim2_hlaf)[0]
    # print("hist_full:{}%".format(np.mean(hist_full)))
    print("sum1:{}".format(sum_jim1))
    print("sum2:{}".format(sum_jim2_hlaf))

    summ = sum_jim2_hlaf / sum_jim1 

    avg = summ * 100
    print("avg:{}".format(avg))
    # print("list_hista_avg:{}%".format(np.mean(list_hista_avg)))

    # # print(hist_mask)
    # plt.subplot(221), plt.imshow(img1)
    # plt.subplot(222), plt.imshow(mask)
    # plt.subplot(223), plt.imshow(img1)
    # plt.subplot(224), plt.plot(img1), plt.plot(img2)
    # plt.xlim([0,256])
    # plt.show()








    # screenshot = ImageGrab.grab()
    # screenshot.save('screenshot.png')

    # scns = "screenshot.png"
    # img_rgb = cv2.imread(scns)
    # img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    # template = cv2.imread('esc.png',0)
    # w, h = template.shape[::-1]

    # res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
    # os.remove(scns)
    
    # threshold = 0.8
    # loc = np.where( res >= threshold)
   
    # if loc[1]:
    #     x = loc[1][0] + w/2
    #     y = loc[0][0] + h/2

    #     counter = 0
    #     print(x,y)
    #     moveTo(x,y,0.2)

    # read('C_driver.png',0)
# cv2.imshow('image',img)
# k = cv2.waitKey(0)
# if k == 27:         # wait for ESC key to exit
#     cv2.destroyAllWindows()
# elif k == ord('s'): # wait for 's' key t
