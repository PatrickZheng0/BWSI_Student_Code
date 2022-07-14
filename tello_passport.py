from djitellopy import Tello
import time

tello = Tello()
tello.connect()

tello.takeoff

for i in range(8):
    tello.move_left(70)
    tello.rotate_clockwise(45)

tello.land