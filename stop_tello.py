from djitellopy import Tello

tello = Tello()
tello.connect()

tello.takeoff()
tello.send_rc_control(0, 0, 0, 0)
tello.land()
tello.end()