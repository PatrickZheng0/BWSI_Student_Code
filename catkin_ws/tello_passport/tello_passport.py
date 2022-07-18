from djitellopy import Tello
import time

tello = Tello()
tello.connect()

tello.takeoff

tello.curve_xyz_speed(25, -25, 0, 25, -75, 0, 20)

tello.land