from djitellopy import Tello
import cv2
import numpy as np
from markers import Marker
from time import sleep


tello = Tello()
tello.connect()

tello.streamon()
frame_read = tello.get_frame_read()

# TODO uncomment this and land() when need to fly
#tello.takeoff()

arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_100)

size = 150
focal_length = 912 # 820mm dist, 167 pxl img, 150mm tag size = 912 focal length (not in mm, ratio between pxl and mm)
mm_to_pxl_ratio = 225/340.25 # 225mm to 340.25pxl
# sensor_width = 2.77 # from https://tellopilots.com/threads/tello-camera-sensor-detailed-specs-sensor-width-in-mm-for-photogrametry.3427/
# fov = 82.6 # from https://www.ryzerobotics.com/tello/specs
# total_length = 2592 # from https://www.ryzerobotics.com/tello/specs

while True:

    img = frame_read.frame
    cv2.imshow('tello camera', img)

    corners, ids, rejects = cv2.aruco.detectMarkers(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), arucoDict)
    detection = cv2.aruco.drawDetectedMarkers(img, corners, borderColor=(255,0,0))

    if len(corners) == 0:
        print('no marker')
        continue

    marker = Marker(id, corners)
    side_len = marker.get_avg_side_length()
    center = marker.get_center()
    dist = marker.get_dist_to_marker(size, focal_length)
    orientation = marker.get_orientation()

    #print('side len: ', side_len)
    #print('center: ', center)
    print('distance: ', dist)
    #print('orientation: ', orientation)
    sleep(0.33)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cv2.destroyAllWindows()
#tello.land()