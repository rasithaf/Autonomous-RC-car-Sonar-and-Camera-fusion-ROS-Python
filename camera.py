#!/usr/bin/env python
# Rasitha Fernando
# 12/05/2019

import rospy
from std_msgs.msg import String
import os
import cv2
import numpy as np


def talker():
  video_capture = cv2.VideoCapture(0)
  video_capture.set(3,160)
  video_capture.set(4,120)

  while not rospy.is_shutdown():
    val = "0"
    rospy.init_node('camera', anonymous=True)

    # Capture frame-by-frame
    ret, frame = video_capture.read()
    _, img = video_capture.read()

    if ret:
      hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
      blur = cv2.GaussianBlur(hsv,(5,5),0)
    
    # color Threshold
      ret,thresh = cv2.threshold(hsv,60,120,cv2.THRESH_BINARY_INV)    

    # defining the range of yellow
      yellow_lower = np.array([22,60,200],np.uint8)
      yellow_upper = np.array([60,255,255],np.uint8)
    
      yellow = cv2.inRange(hsv, yellow_lower, yellow_upper)
      
      kernal = np.ones((5, 5), "uint8")
      yellow = cv2.dilate(yellow, kernal)
    
      res_yellow = cv2.bitwise_and(frame, frame, mask = yellow)	
 

    # Frame contours
      contours,hierarchy = cv2.findContours(yellow,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
     
      for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
        cv2.drawContours(img, [approx], 0, (0), 5)
        x = approx.ravel()[0]
        y = approx.ravel()[1]
        
    # Detecting contours
      if len(contours) > 0:

        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)

        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])

        cv2.line(frame,(cx,0),(cx,720),(255,0,0),1)
        cv2.line(frame,(0,cy),(1280,cy),(255,0,0),1)
        cv2.drawContours(frame, contours, -1, (255,128,213), 1)

        val = String

        if cx >= 130 and cx < 160:
          val = "145"

        elif cx < 130 and cx >= 86:
          val = "120"

        elif cx < 86 and cx >= 76:
          dec  =  100 + 4*(cx -81)
          val = str(int(dec))

        elif cx < 76 and cx >= 30:
          val = "79"

        elif cx < 30 and cx > 0:
          val = "55"

	else:
          val = "0"
          print ("Nothing found...") 

        # Display the resulting frame
        cv2.imshow('frame',frame)
        cv2.imshow('yellow',yellow) 
        cv2.imshow('res_yellow',res_yellow)
    else: 
        val = "0"
        print ("Nothing found...")   

    if cv2.waitKey(1) & 0xFF == ord('q'):
	video_capture.release()
   	cv2.destroyAllWindows()        
	break

    pub = rospy.Publisher('cam_talk', String, queue_size=1)
    pub.publish(val)
    rospy.loginfo(val)

if __name__ == '__main__':
  try:
    talker()
  except rospy.ROSInterruptException:
    pass

