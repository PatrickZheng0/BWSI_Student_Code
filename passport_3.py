from djitellopy import Tello
import cv2
import numpy as np
import time
from time import sleep

from markers import Marker
from pid import PID

tello = Tello()
tello.connect()

tello.takeoff()

tello.streamon()
frame_read = tello.get_frame_read()

arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_100)

size = 150
focal_length = 912 # 820mm dist, 167 pxl img, 150mm tag size = 912 focal length (not in mm, ratio between pxl and mm)

# challenge 3

turn_pid = PID(0.25, 0, 0.001)
turn_pid.set_sample_time(0.1)
turn_pid.SetPoint = 416 # frame size ~ 832x832 pxls

shift_pid = PID(0.05, 0, 0)
shift_pid.set_sample_time(0.1)
shift_pid.SetPoint = 416 # frame size ~ 832x832 pxls

img = frame_read.frame
corners, ids, rejects = cv2.aruco.detectMarkers(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), arucoDict)

move_pid = PID(0.1, 0.025, 0.02)
move_pid.set_sample_time(0.1)
move_pid.SetPoint = 700 # drone stays 400mm from wall

check_turn = False
move_up = False

prev_time = time.time()

while True:
    img = frame_read.frame
    corners, ids, rejects = cv2.aruco.detectMarkers(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), arucoDict)

    if len(corners) == 0:
        tello.send_rc_control(0, 0, 0, 45)
        while len(corners) == 0:
            img = frame_read.frame
            corners, ids, rejects = cv2.aruco.detectMarkers(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), arucoDict)

            current_time = time.time()

            if (current_time - prev_time > 12) and (move_up == False):
                tello.send_rc_control(0, 0, 20, 0)
                sleep(1)
                tello.send_rc_control(0, 0, 0, 0)
                move_up = True
        
        tello.send_rc_control(0, 0, 0, 0)

    marker = Marker(id, corners)

    # if check_turn == False:
    #     for i in range(25):
    #         img = frame_read.frame
    #         corners, ids, rejects = cv2.aruco.detectMarkers(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), arucoDict)

    #         feedback = marker.get_center()[0]
    #         turn_pid.update(feedback)
    #         turn_output = int(turn_pid.output)
    #         tello.send_rc_control(0, 0, 0, -turn_output)
    #         sleep(0.05)
    #         tello.send_rc_control(0, 0, 0, 0)
        
    #     check_turn = True

    # side_len = marker.get_avg_side_length()
    # if (marker.get_dist_to_marker(size, focal_length) > move_pid.get_set_point() + 25) or (marker.get_dist_to_marker(size, focal_length) < move_pid.get_set_point - 25):
    #     img = frame_read.frame
    #     corners, ids, rejects = cv2.aruco.detectMarkers(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), arucoDict)
    #     marker = Marker(id, corners)

    #     side_len = marker.get_avg_side_length()
    #     dist = marker.get_dist_to_marker(size, focal_length)
    #     if dist < move_pid.get_set_point():
    #         tello.send_rc_control(0, -20, 0, 0)
    #     else: tello.send_rc_control(0, 20, 0, 0)

    #     while (marker.get_dist_to_marker(size, focal_length) > move_pid.get_set_point() + 25) or (marker.get_dist_to_marker(size, focal_length) < move_pid.get_set_point - 25):
    #         img = frame_read.frame
    #         corners, ids, rejects = cv2.aruco.detectMarkers(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), arucoDict)
    #         marker = Marker(id, corners)
    #         side_len = marker.get_avg_side_length()
    #         print('dist: ', marker.get_dist_to_marker(size, focal_length))

    #     tello.send_rc_control(0, 0, 0, 0)

    tello.send_rc_control(0, 0, 0, 0)

    #for i in range(50):
    # img = frame_read.frame
    # corners, ids, rejects = cv2.aruco.detectMarkers(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), arucoDict)
    # marker = Marker(id, corners)

    side_len = marker.get_avg_side_length()
    move_feedback = marker.get_dist_to_marker(size, focal_length)
    move_pid.update(move_feedback)
    move_output = int(move_pid.output)

    shiftx_feedback = marker.get_center()[0]
    shift_pid.update(shiftx_feedback)
    shiftx_output = int(shift_pid.output)

    shifty_feedback = marker.get_center()[1]
    shift_pid.update(shifty_feedback)
    shifty_output = int(shift_pid.output)

    tello.send_rc_control(-shiftx_output, -move_output, -shifty_output, 0)
    sleep(0.075)
    tello.send_rc_control(0, 0, 0, 0)
    print(marker.get_dist_to_marker(size, focal_length))
    print('shiftx: ', 416 - marker.get_center()[0])
    print('shifty: ', 416 - marker.get_center()[1])

    if (marker.get_dist_to_marker(size, focal_length) < 300):
        tello.send_rc_control(0, 0, 0, 0)
        tello.land()
        break

#     #TODO move this statement
#     #TODO fix get dist method
#     tello.send_rc_control(0, 0, 0, 0)
#     print('done')
#     break

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break


# challenge 2

# pid = PID(0.25, 0, 0.001)
# pid.set_sample_time(0.1)
# pid.SetPoint = 416 # frame size ~ 832x832 pxls

# current_time = time.time()
# time_now = time.time()

# while time_now - current_time < 60:
#     time_now = time.time()

#     img = frame_read.frame
#     #cv2.imshow('tello camera', img)

#     corners, ids, rejects = cv2.aruco.detectMarkers(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), arucoDict)
#     #detection = cv2.aruco.drawDetectedMarkers(img, corners, borderColor=(255,0,0))

#     marker = Marker(id, corners)

#     feedback = marker.get_center()[0]
#     pid.update(feedback)
#     output = int(pid.output)
#     tello.send_rc_control(0, 0, 0, -output)
#     sleep(0.05)
#     tello.send_rc_control(0, 0, 0, 0)


#     key = cv2.waitKey(1) & 0xFF
#     if key == ord('q'):
#         break

# challenge 1

# tello.curve_xyz_speed(50, 50, 0, 100, 0, 0, 20)
# tello.curve_xyz_speed(-50, -50, 0, -100, 0, 0, 20)

# tello.land()

cv2.destroyAllWindows()
tello.land()