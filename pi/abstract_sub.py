import numpy as np
from PID import PID
from differential_PID import DifferentialPID

# An abstract model of a sub which contains all of the needed PIDs and other low-level details
# to control the sub. 

class AUV:
    def __init__(self, wanted_depth, wanted_angle, motor_min, Dp, Di, Dd, Rp, Ri, Rd):
        '''
        Dp, Di, and Dd are Kp Ki and Kd for the depth PID, and Rp Ri and Rd are the 
        equivalents for the rotation PID
        '''

        self.depth = 0
        self.wanted_speed = 0
        self.rotation = np.array([0, 0, 0])
        # roll (left/right into water) / pitch (forward/backward) / yaw (left/right turning)
        # check out the picture on https://en.wikipedia.org/wiki/Ship_motions
        # in degrees!

        self.forward_velocity = 0
        # the current forward velocity. potential future issue: only keeping track of forward
        # velocity could mean left/right movement would be unchecked. this could be fixed by
        # keeping track of forward/up/side, but it might not be an issue because the angle is
        # fixed by the rotation_pid


        self.depth_pid = PID(Dp, Di, Dd, wanted_depth)
        self.rotation_pid = DifferentialPID(PID(Rp, Ri, Rd, wanted_angle), motor_min)
        
    
    def set_depth(self, depth):
        '''Sets the current depth of the sub.'''
        self.depth = depth
        

    def set_forward_velocity(self, velocity):
        '''Sets the velocity of the sub'''
        self.forward_velocity = velocity
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

    def set_wanted_speed(self, speed):
        self.wanted_speed = speed


    def get_motors(self):
        '''
        Gets the calculated speed each of the motors should travel at, in the form \n
        (VFL, VFR, VBL, VBR, HFL, HFR, HBL, HBR) \n
        (eg. HBR = horizontal-back-right, VFL = vertical-front-left)
        '''

        vertical_motors = np.tile(self.depth_pid.predict(self.depth), 4)
        horizontal_motors = np.zeros(4)
        
        rotational_motors = self.rotation_pid.predict(self.depth) # get rotational pid speed (x, y)

        for i in range(4):
            horizontal_motors[i] += rotational_motors[i%2]
            # add to diagonals
        
        horizontal_motors += np.tile(self.forward_speed, 4)

        return np.concatenate(vertical_motors, horizontal_motors)