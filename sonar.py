#!/usr/bin/env python3
# Rasitha Fernando
# 12/05/2019

import Jetson.GPIO as GPIO
import time
from std_msgs.msg import Int16
from std_msgs.msg import Float64MultiArray
from std_msgs.msg import String
import rospy
GPIO.cleanup()


def call_sonar(TRIG, ECHO):
 GPIO.setmode(GPIO.BOARD)
 
 GPIO.setup(TRIG,GPIO.OUT)
 GPIO.setup(ECHO,GPIO.IN)

 GPIO.output(TRIG, GPIO.LOW)

 GPIO.output(TRIG,GPIO.HIGH)
 time.sleep(0.00001)
 GPIO.output(TRIG, GPIO.LOW)
 pulse_start = time.time()
 pulse_end = time.time()
 count = 0
 flag = 0

 while GPIO.input(ECHO)==0:   
  pulse_start = time.time()
  count = count + 1

  if count >= 5:
    print ("I break")
    flag = 1
    break 

 	   
 while GPIO.input(ECHO)==1: 
  pulse_end = time.time()
	  
 pulse_duration = pulse_end - pulse_start
 distance = pulse_duration * 17150
 distance = round(distance,2)
 if flag == 1 or distance < 0:
   distance = 0
 return distance


def talker():
 
 distance =Float64MultiArray()
 distance.data = [0, 0, 0] # Right, middle, Left

 while not rospy.is_shutdown():
  rospy.init_node('sonar', anonymous=True)
 
  # First TRIG and then ECHO {Right-(40,38),Mid-(23,13), Left-(22,21)}
  distance_R = call_sonar(22,21) 
  distance_M = call_sonar(40,38)
  distance_L = call_sonar(37,33)
  distance.data = [distance_R, distance_M, distance_L]

  limit = 57
  xl = distance_L 
  xr = distance_R 

  if distance_R >= limit and distance_L >= limit:
    dec = 100 

  elif distance_R> distance_L and distance_L < limit :
    X = xl - xr
    dec = (100 - (45/limit) * (xl - limit) ) + 20

  elif distance_L> distance_R and distance_R < limit:
    X = xr - xl
    dec = 100 + 45/limit *(xr - limit) - 20

  if dec > 145:
    dec = 145
  if dec < 55:
    dec = 55

  if distance_M <=40 or distance_L <=10 or distance_R <=10:
    dec = 0
  dec = int(dec)
  y = str(dec)
  pub = rospy.Publisher('sonar_talk', String, queue_size=1)
    
  pub.publish(y)
  rospy.loginfo(y)
  GPIO.cleanup()


if __name__ == '__main__':
 try:
  talker()
 except rospy.ROSInterruptException:
  pass
