import numpy as np
import math

class Marker:

    def __init__(self, id, corner):
        self.id = id
        self.bl = corner[0][0][0] # bottom left
        self.br = corner[0][0][1]
        self.tr = corner[0][0][2] # top right
        self.tl = corner[0][0][3]

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

    def get_pos_to_marker(self):

        if self.left_dist > self.right_dist:
            self.lr = 'angled right'
        else:
            self.lr = 'angled left'

        if self.top_dist > self.bottom_dist:
            self.tb  = 'angled down'
        else:
            self.tb = 'angled up'

        return [self.lr, self.tb]

    def get_dist_to_marker(self, size, focal_length):
        #focal_length = sensor_width/2 * 1/math.tan(fov/2)
        self.dist = focal_length*size/self.avg_side_length
        return self.dist


    def patrick_idea_get_distance_to_img(self, total_img_length, fov, rl_img_size):
        img_length = (self.top_dist + self.bottom_dist)/2
        total_length = total_img_length

        fraction = img_length/total_length
        angle = fraction*fov

        dist = img_length/2 * 1/math.tan(angle/2)
        dist *= rl_img_size/img_length # converts from pixel length to real life mm
        
        self.patrick_dist = dist
        
        return self.patrick_dist