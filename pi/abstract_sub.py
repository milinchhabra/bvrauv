import numpy as np
from PID import PID
from differential_PID import DifferentialPID

# An abstract model of a sub which contains all of the needed PIDs and other low-level details
# to control the sub. 

class AUV:
    def __init__(self, wanted_depth, wanted_angle, motor_min):
        self.depth = 0
        self.forward_speed = 0
        self.velocity = np.array([0, 0, 0])
        self.roation = np.array([0, 0, 0])
        # roll (left/right into water) / pitch (forward/backward) / yaw (left/right turning)
        # check out the picture on https://en.wikipedia.org/wiki/Ship_motions


        self.depth_pid = PID(0.6, 0.0, 0.1, wanted_depth)
        self.rotation_pid = DifferentialPID(PID(0.6, 0.0, 0.1, wanted_angle), motor_min)
        
    
    def set_depth(self, depth):
        self.depth = depth
        

    def set_velocity(self, velocity):
        '''Sets the velocity of the sub. Use a numpy array.'''
        self.velocity = velocity
        # use numpy!


    def set_rotation(self, rotation):
        '''Sets the rotation of the sub (roll/pitch/yaw). Use a numpy array.'''
        self.rotation = rotation
        # use numpy here too!


    def set_wanted_depth(self, depth):
        self.depth_pid = PID(self.depth_pid.Kp, self.depth_pid.Ki, self.depth_pid.Kd, depth)

    def set_wanted_rotation(self, rotation):
        rot = self.rotation_pid
        self.rotation_pid = DifferentialPID(PID(rot.Kp, rot.Ki, rot.Kd, rotation), rot.min)

    def set_forward_speed(self, speed):
        self.forward_speed = speed


    def get_motors(self):
        '''
        Gets the calculated speed each of the motors should travel at, in the form \n
        (VFL, VFR, VBL, VBR, HFL, HFR, HBL, HBR) \n
        (eg. HBR = horizontal-back-right, VFL = vertical-front-left)
        '''

        vertical_motors = np.tile(self.depth_pid.predict(self.depth), 4)
        horizontal_motors = np.zeros(4)
        
        rotational_motors = np.array([0]) # get rotational pid speed (x, y)

        for i in range(4):
            horizontal_motors[i] += rotational_motors[i%2]
            # add to diagonals
        
        horizontal_motors += np.tile(self.forward_speed, 4)

        return np.concatenate(vertical_motors, horizontal_motors)