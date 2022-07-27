from djitellopy import Tello
import cv2
import numpy as np
from markers import Marker
from matplotlib import pyplot as plt


tello = Tello()
tello.connect()

tello.streamon()
frame_read = tello.get_frame_read()

tello.takeoff()

arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_100)

size = 150
focal_length = 25
# sensor_width = 2.77 # from https://tellopilots.com/threads/tello-camera-sensor-detailed-specs-sensor-width-in-mm-for-photogrametry.3427/
# fov = 82.6 # from https://www.ryzerobotics.com/tello/specs
# total_length = 2592 # from https://www.ryzerobotics.com/tello/specs

while True:

    img = frame_read.frame
    cv2.imshow('tello camera', img)

    corners, ids, rejects = cv2.aruco.detectMarkers(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), arucoDict)
    detection = cv2.aruco.drawDetectedMarkers(img, corners, borderColor=(255,0,0))

    marker = Marker(id, corners)
    side_len = marker.get_avg_side_length()
    center = marker.get_center()
    orientation = marker.get_pos_to_marker()
    dist = marker.get_dist_to_marker(size, focal_length)

    print('side len: ', side_len)
    print('center: ', center)
    print('orientation: ', orientation)
    print('distance: ', dist)

    key = cv2.waitKey(1) & 0xff
    if key == ord('q'):
        break

print('corners', corners)
print('printable')
cv2.destroyAllWindows()
tello.land()