# Autonomous-RC-car-Sonar-and-Camera-fusion-ROS-Python

This project was built on Jetson Nano developer kit, RC Car, Logitech USB Cam and HC-SR04 Sonar.

I tested the project on the following environment: (If you are not using ROS environment, remove the ros commands in the code) 

Ubuntu 18.04,
Python,
ROS Melodic,
Numpy,
OpenCV

Camera:

Used logitech usb cam

It follows a yellow line

RC car has steering angle range between 55 and 145

wheel position: 55 -> left most, 100 -> straight, 145 -> right most

frame has been segmented to 5 main positions

Sonar:

Used three of HC-SR04 ultrasonic sonars (has 30 degree range)

Those three were mounted with 40 degree diference from sensor center(as shown in figure)

![Sonar](https://github.com/rasithaf/Autonomous-RC-car-Sonar-and-Camera-fusion-ROS-Python/blob/master/Sonar_Mount.png)

Pins: TRIG and ECHO respectivly

{Right-(40,38),Mid-(23,13), Left-(22,21)}

Servo:

Needs "adafruit_servokit" module

Fusion:

Will make the decision and prioritize the actions

Output video: See Sonar+Camera fusion in https://rasithaf.wixsite.com/mysite/videos
