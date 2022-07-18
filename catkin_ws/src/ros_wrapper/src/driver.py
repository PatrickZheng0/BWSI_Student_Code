#!/usr/bin/env python3

import rospy
from djitellopy import Tello
from sensor_msgs.msg import Image
from std_msgs.msg import Empty
from geometry_msgs.msg import Twist
from ros_wrapper.msg import Flip
from ros_wrapper.msg import State

class Driver():

    def __init__(self):

        rospy.init_node("driver", anonymous=True)

        self.tello = Tello()
        self.tello.connect()

        self.camera_pub = rospy.Publisher('/tello/cam_forward', Image, queue_size=10)
        self.state_pub = rospy.Publisher('/tello/state', State, queue_size=10)
        
        self.flip_sub = rospy.Subscriber('/tello/flip', Flip, self.flip_callback)
        self.vel_sub = rospy.Subscriber('/tello/cmd_vel', Twist, self.vel_callback)
        self.takeoff_sub = rospy.Subscriber('/tello/takeoff', Empty, self.takeoff_callback)
        self.land_sub = rospy.Subscriber('/tello/land', Empty, self.land_callback)

        self.state = State()

        #camera_pub.publish(tello.get_frame_read)
        self.state.battery = self.tello.get_battery()
        self.state.height = self.tello.get_height()
        self.state.temperature = self.tello.get_temperature()
        self.state_pub.publish(self.state)
        rospy.spin()

    def flip_callback(self, data):
        self.flip_data = data
        self.tello.flip(self.flip_data.direction)

        print("Doing flip: ", data.direction)

    def vel_callback(self, data):
        self.vel_data = data
        self.tello.send_rc_control(int(self.vel_data.linear.x), int(self.vel_data.linear.y), 0, int(self.vel_data.angular.x))

        print("Set Speed")

    def takeoff_callback(self, data):
        self.tello.takeoff()

        print("Doing: Takeoff")

    def land_callback(self, data):
        self.tello.land()

        print("Doing: Land")
    

if __name__ == "__main__":
    try:
        driver = Driver()
    except rospy.ROSInterruptException:
        pass