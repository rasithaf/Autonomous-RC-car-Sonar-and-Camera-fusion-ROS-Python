#!/usr/bin/env python3
# Rasitha Fernando
# 12/05/2019

import rospy
from std_msgs.msg import Int16MultiArray
from std_msgs.msg import String
import signal
from adafruit_servokit import ServoKit
import board
import busio

global x
x = Int16MultiArray
x = [1000,1000]


def callback1(data):
  x[0] = int(data.data)
  fusion()
  return(x)  


def callback2(data):
  x[1] = int(data.data)



def fusion():     
  if x[1] == 100:
    dec = str(x[0])
  else:  
    dec = str(x[1])

  pub = rospy.Publisher('fusion_talk', String, queue_size=1)
  pub.publish(dec)
  rospy.loginfo(dec)



def listener():
  rospy.init_node('fusion', anonymous=True)
  rospy.Subscriber('sonar_talk', String, callback2, queue_size=1) 
  rospy.Subscriber('cam_talk', String, callback1, queue_size=1)  
  rospy.spin()


if __name__ == '__main__':
  try:   
    global dec 
    dec = String   
    listener()

  except rospy.ROSInterruptException:
    pass
 

