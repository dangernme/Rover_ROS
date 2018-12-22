#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Range
import RPi.GPIO as GPIO

LEFT_TRIGGER = 24
LEFT_ECHO = 22
RIGHT_TRIGGER = 5
RIGHT_ECHO = 23

def talker(): 
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LEFT_TRIGGER, GPIO.OUT)
    GPIO.setup(LEFT_ECHO, GPIO.IN) 
    GPIO.output(LEFT_TRIGGER, True)
    GPIO.setup(RIGHT_TRIGGER, GPIO.OUT)
    GPIO.setup(RIGHT_ECHO, GPIO.IN) 
    GPIO.output(RIGHT_TRIGGER, True)
 
    pub = rospy.Publisher('distance', Range, queue_size=10)
    rospy.init_node('front_distance_sensors', anonymous=True)
    
    rate = rospy.Rate(10) # 10hz
    
    range_left = Range()
    range_right = Range()

    range_left.radiation_type = range_left.ULTRASOUND
    range_right.radiation_type = range_left.ULTRASOUND

    range_left.min_range = 0.03
    range_right.min_range = 0.03

    range_left.max_range = 3.0
    range_right.max_range = 3.0

    range_left.field_of_view = 60
    range_right.field_of_view = 60

    while not rospy.is_shutdown():
        range_left.range = get_distance_left()
        range_right.range = get_distance_right()

        rospy.loginfo(range_left)
        rospy.loginfo(range_right)
        pub.publish(range_left)
        pub.publish(range_right)
        rate.sleep()

    GPIO.cleanup()

def get_distance_left():
    GPIO.output(LEFT_TRIGGER, False)
        
    while GPIO.input(LEFT_ECHO) == 0:
        pass
        
    nosig = rospy.get_time()
        
    while GPIO.input(LEFT_ECHO) == 1:
        pass

    sig = rospy.get_time()
        
    tl = sig - nosig
    distance = (tl * 343) /2 
    GPIO.output(LEFT_TRIGGER, True)
    return distance

def get_distance_right():
    GPIO.output(RIGHT_TRIGGER, False)
    
    while GPIO.input(RIGHT_ECHO) == 0:
        pass
        
    nosig = rospy.get_time()
    
    while GPIO.input(RIGHT_ECHO) == 1:
        pass
        
    sig = rospy.get_time()
    
    tl = sig - nosig
    distance = (tl * 343) / 2 
    GPIO.output(RIGHT_TRIGGER, True)
    return distance

if __name__ == '__main__':
    try: 
        talker()
    except rospy.ROSInterruptException:
        pass
