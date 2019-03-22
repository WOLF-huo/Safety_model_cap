# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 10:38:14 2018

@author: sgs4176
"""

import numpy as np
import cv2

def contrast_brightness_demo(image, c, b):  #其中c为对比度，b为每个像素加上的值（调节亮度）
    blank = np.zeros(image.shape, image.dtype)   #创建一张与原图像大小及通道数都相同的黑色图像
    dst = cv2.addWeighted(image, c, blank, 1-c, b) #c为加权值，b为每个像素所加的像素值
    ret, dst = cv2.threshold(dst, 25, 255, cv2.THRESH_BINARY)
    return dst

def drawfire(image,fireimage):
    _,contours, hierarchy = cv2.findContours(fireimage,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)     
    c_max = []
    max_area = 0
    max_cnt = 0
    for i in range(len(contours)):
        cnt = contours[i]
        area = cv2.contourArea(cnt)
        
        if (area>max_area):
            if(max_area!=0):        
                c_min = []
                c_min.append(cnt)
            max_area = area
            max_cnt = cnt
        else:
            c_min = []
            c_min.append(cnt)

    c_max.append(max_cnt)
#    x,y,w,h = cv2.boundingRect(max_cnt)
#    cv2.rectangle(image, (x,y), (x+w, y+h), (0, 255, 0), 1)
#    rect = cv2.minAreaRect(max_cnt)
#    box = cv2.boxPoints(rect)
#    box = np.int0(box)
    if(max_area!=0):   
#        cv2.drawContours(image,[box],-1,(0,0,255),1)
        cv2.drawContours(image,c_max,-1,(0,0,255),1)
    cv2.imshow("img", image) 
    

if __name__ == '__main__':
#    capture = cv2.VideoCapture(r"C:\Users\sgs4176\Videos\test_fire_3.mp4")
    capture = cv2.VideoCapture(r"rtsp://admin:QACXNT@10.0.1.47:554/h264/ch1/main/av_stream")
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    redThre = 105
    saturationTh = 45
    while(True):
        ret, frame = capture.read()
        if(ret==False):
            break
#        cv2.imshow("frame", frame)
        B = frame[:, :, 0]
        G = frame[:, :, 1]
        R = frame[:, :, 2]
        minValue = np.array(np.where(R <= G, np.where(G <= B, R, 
                                                      np.where(R <= B, R, B)), np.where(G <= B, G, B)))
        S = 1 - 3.0 * minValue / (R + G + B)
        fireImg = np.array(np.where(R > redThre, 
                                    np.where(R >= G, 
                                             np.where(G >= B, 
                                                      np.where(S >= 0.2, 
                                                               np.where(S >= (255 - R)*saturationTh/redThre, 255, 0), 0), 0), 0), 0))
        gray_fireImg = np.zeros([fireImg.shape[0], fireImg.shape[1], 1], np.uint8)
        gray_fireImg[:, :, 0] = fireImg
        gray_fireImg = cv2.GaussianBlur(gray_fireImg, (7, 7), 0)
        gray_fireImg = contrast_brightness_demo(gray_fireImg, 5.0, 25)
#        _,contours, hierarchy = cv2.findContours(gray_fireImg,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) 
        drawfire(frame, gray_fireImg)
#        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
#        gray_fireImg = cv2.morphologyEx(gray_fireImg, cv2.MORPH_CLOSE, kernel)
#        dst = cv2.bitwise_and(frame, frame, mask=gray_fireImg)
#        cv2.imshow("fire", dst)
#        cv2.imshow("gray_fireImg", gray_fireImg)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()