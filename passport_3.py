from time import sleep
from djitellopy import Tello

tello = Tello()
tello.connect()

# challenge 1
tello.takeoff()

tello.send_rc_control(-30, 0, 0, -10)
sleep(5)
tello.send_rc_control(0, 0, 0, 0)

tello.land()