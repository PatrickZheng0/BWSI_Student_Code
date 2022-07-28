import numpy as np
import math

class Marker:

    def __init__(self, id, corner):
        self.id = id
        self.tl = corner[0][0][0] # top left
        self.tr = corner[0][0][1]
        self.br = corner[0][0][2] # bottom right
        self.bl = corner[0][0][3]

        self.bottom_dist = self.calc_distance(self.br, self.bl)
        self.top_dist = self.calc_distance(self.tr, self.tl)
        self.right_dist = self.calc_distance(self.tr, self.br)
        self.left_dist = self.calc_distance(self.tl, self.bl)

        self.avg_side_length = None
        self.center = None

        self.lr = None # left right orientation
        self.tb = None # top down orientation

        self.dist = None # dist to drone
        self.patrick_dist = None # my test idea

        self.marker_roll = None # how much marker has turned clockwise

    
    def calc_distance(self, arr1, arr2):
        dist = np.sqrt(np.sum(np.square(arr1-arr2)))
        return dist


    def get_avg_side_length(self):
        length = (self.top_dist + self.bottom_dist)/2
        width = (self.right_dist + self.left_dist)/2
        self.avg_side_length = (length + width)/2
        return self.avg_side_length


    def get_center(self):
        center_diagonal_1 = (self.tr + self.bl)/2
        center_diagonal_2 = (self.tl + self.br)/2
        self.center = (center_diagonal_1 + center_diagonal_2)/2
        return self.center


    def get_dist_to_marker(self, size, focal_length):
        self.dist = focal_length*size/self.avg_side_length
        return self.dist


    def get_orientation(self):
        diagonal_len = self.calc_distance(self.tr, self.center)
        x = np.abs((self.tr[0] - self.center[0])/diagonal_len)
        y = np.abs((self.tr[1] - self.center[1])/diagonal_len)
        if (self.tr[0] > self.center[0]) and (self.tr[1] < self.center[1]): # quadrant 1
            angle = math.atan(x/y)
            if angle < math.pi/4:
                angle = -math.pi*3/2 - angle
            else: 
                angle = math.pi/2 - angle
        if (self.tr[0] > self.center[0]) and (self.tr[1] > self.center[1]): # quadrant 4
            angle = -math.atan(y/x)
        if (self.tr[0] < self.center[0]) and (self.tr[1] > self.center[1]): # quadrant 3
            angle = -math.atan(x/y) - math.pi/2
        if (self.tr[0] < self.center[0]) and (self.tr[1] < self.center[1]): # quadrant 2
            angle = -math.atan(y/x) - math.pi

        angle *= 180/math.pi # convert radians to degrees

        self.marker_roll = 45 - angle
        return self.marker_roll


    def get_drone_turn(self, mm_to_pxl_ratio):
        dist_from_center = self.center - np.array([416, 416])
        dist_from_center *= mm_to_pxl_ratio
        dist_from_center[1] = -dist_from_center[1]
        diagonal = np.sqrt(np.sum(np.square(dist_from_center)))
        straight_dist_to_aruco_plane = np.sqrt(np.square(diagonal) + np.square(self.dist))

        horizontal_angle = math.atan(dist_from_center[0]/straight_dist_to_aruco_plane)
        vertical_angle = math.atan(dist_from_center[1]/straight_dist_to_aruco_plane)
        angles = np.array([horizontal_angle, vertical_angle])

        return angles


    def patrick_idea_get_distance_to_img(self, total_img_length, fov, rl_img_size):
        img_length = (self.top_dist + self.bottom_dist)/2
        total_length = total_img_length

        fraction = img_length/total_length
        angle = fraction*fov

        dist = img_length/2 * 1/math.tan(angle/2)
        dist *= rl_img_size/img_length # converts from pixel length to real life mm
        
        self.patrick_dist = dist
        
        return self.patrick_dist