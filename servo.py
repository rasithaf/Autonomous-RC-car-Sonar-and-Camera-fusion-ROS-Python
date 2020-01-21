#!/usr/bin/env python3
# Rasitha Fernando
# 12/05/2019

import rospy
from std_msgs.msg import String
import time
import signal
from adafruit_servokit import ServoKit
import board
import busio
i2c_bus0=(busio.I2C(board.SCL_1,board.SDA_1))
kit = ServoKit(channels=16, i2c = i2c_bus0)

kit.continuous_servo[3].throttle = 0.0
time.sleep(1)
kit.continuous_servo[3].throttle = 0.1
time.sleep(1)
kit.continuous_servo[3].throttle = 0.15
time.sleep(1)
kit.continuous_servo[3].throttle = 0.2
time.sleep(1)
kit.continuous_servo[3].throttle = 0.0
#------------------------------------------------------

def callback(data):
      flag = 0
      dec = int(data.data)
      kit.servo[4].angle = dec
      
      if dec ==  100:
        kit.continuous_servo[3].throttle = 0.154

      elif dec > 0 and dec < 90 or dec > 108:
        kit.continuous_servo[3].throttle = 0.14

      if dec == 0:
        kit.continuous_servo[3].throttle = 0
        kit.servo[4].angle = 100
        flag = 0

      rospy.loginfo(dec)


def listener():
 rospy.init_node('servo', anonymous=True)
 rospy.Subscriber('fusion_talk', String, callback, queue_size=1)   
 rospy.spin()


if __name__ == '__main__':
  try:    
    listener()
  except rospy.ROSInterruptException:
    kit.continuous_servo[3].throttle = 0.0
    kit.servo[4].angle = 100 
    pass
 

