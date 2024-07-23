import abstract_sub
import time

def get_forward_velocity():
    # read from the imu
    # TODO finish this!
    return 1

def get_depth():
    # read from the depth sensor
    # TODO finish this!
    return 1

def get_angle():
    # read from the imu (i think thats what has angle)
    # TODO finish this!
    return 1


def set_motor(speed, index):
    '''
    Send to the Arduino a command to turn motor at index `index` at speed `speed`
    '''
    # TODO finish this!
    pass

def set_motors(motors):
    '''
    Sends commands to all motors, in the format\n
    (VFL, VFR, VBL, VBR, HFL, HFR, HBL, HBR)
    '''
    # TODO finish this!
    pass


if __name__ == '__main__':

    wanted_depth = 10
    # depending on the pid format...

    wanted_angle = 0
    # also depending on the pid format...

    motor_min = 5
    # check the motors

    sub = abstract_sub.AUV(wanted_depth, wanted_angle, motor_min, 0.6, 0.0, 0.1, 0.6, 0.0, 0.1)
    # final values are for two pid controllers; these DEFINITELY need to be retuned!


    delay = 0.001
    # how often to run the loop (in seconds)

    while True:
        sub.set_depth(get_depth())
        sub.set_forward_velocity(get_forward_velocity())
        sub.set_rotation(get_angle())

        set_motors(sub.get_motors())

        time.sleep(delay)
