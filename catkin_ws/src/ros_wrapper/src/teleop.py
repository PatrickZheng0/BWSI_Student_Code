#!/usr/bin/env python3

import rospy
from std_msgs.msg import Empty
from geometry_msgs.msg import Twist
from ros_wrapper.msg import Flip

from pynput.keyboard import Listener



class Teleop():

    def __init__(self):
        
        rospy.init_node("teleop", anonymous=True)
        
        self.flip_pub = rospy.Publisher('/tello/flip', Flip, queue_size=10)
        self.vel_pub = rospy.Publisher('/tello/cmd_vel', Twist, queue_size=10)
        self.takeoff_pub = rospy.Publisher('/tello/takeoff', Empty, queue_size=10)
        self.land_pub = rospy.Publisher('/tello/land', Empty, queue_size=10)

        self.vel_data = Twist()
        self.flip_data = Flip()
        self.rate = rospy.Rate(5)

        self.x_speed = 30
        self.y_speed = 30
        self.x_rotate = 50

    
    def on_press(self, key):

        if key.char == "w":
            self.vel_data.linear.y = self.y_speed
            self.vel_pub.publish(self.vel_data)
        elif key.char == "s":
            self.vel_data.linear.y = -self.y_speed
            self.vel_pub.publish(self.vel_data)
        elif key.char == "a":
            self.vel_data.linear.x = -self.x_speed
            self.vel_pub.publish(self.vel_data)
        elif key.char == "d":
            self.vel_data.linear.x = self.x_speed
            self.vel_pub.publish(self.vel_data)
        elif key.char == "c":
            self.vel_data.angular.x = -self.x_rotate
            self.vel_pub.publish(self.vel_data)
        elif key.char == "v":
            self.vel_data.angular.x = self.x_rotate
            self.vel_pub.publish(self.vel_data)


    def on_release(self, key):
        
        if key.char == "u":
            print("key: ", key)
            self.flip_data.direction = "f"
            self.flip_pub.publish(self.flip_data)
        elif key.char == "j":
            print("key: ", key)
            self.flip_data.direction = "b"
            self.flip_pub.publish(self.flip_data)
        elif key.char == "h":
            print("key: ", key)
            self.flip_data.direction = "l"
            self.flip_pub.publish(self.flip_data)
        elif key.char == "k":
            print("key: ", key)
            self.flip_data.direction = "r"
            self.flip_pub.publish(self.flip_data)
        elif key.char == "t":
            print("key: ", key)
            self.takeoff_pub.publish()
        elif key.char == "l":
            print("key: ", key)
            self.land_pub.publish()

        elif (key.char == "w") or (key.char == "a") or (key.char == "s") or (key.char == "d") or (key.char == "c") or (key.char == "v"):
            print("key: ", key)
            self.vel_data.linear.x = 0
            self.vel_data.linear.y = 0
            self.vel_data.angular.x = 0
            self.vel_pub.publish(self.vel_data)
        


if __name__ == "__main__":
    
    try:
        teleop = Teleop()
        listener = Listener(on_press=lambda event: teleop.on_press(event),
                            on_release=lambda event: teleop.on_release(event))
        listener.start()

        while listener.running and not rospy.is_shutdown():
            teleop.rate.sleep()

    except rospy.ROSInterruptException:
        pass