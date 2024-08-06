import time
from collections import deque

from pi.PID import PID
from pin_control import PinControl

# A high-level wrapper class for a port control sub with pre-made methods

class UserSub:
    def __init__(self, port_control_sub: PinControl, Fp, Fi, Fd, max_speed, average_accuracy):
        self.port_sub: PinControl = port_control_sub
        self.forward_speed = 0
        self.Fp = Fp
        self.Fi = Fi
        self.Fd = Fd
        self.max_speed = max_speed
        self.average_accuracy = average_accuracy
        self.update_sensors()

    def update_sensors(self):
        self.port_sub.update_data()
        self.forward_speed = self.port_sub.imu.get_forward_speed()

    def update_motors(self):
        self.port_sub.update_motors()

    def depth(self):
        return self.port_sub.sub.depth

    def heading(self):
        return self.port_sub.sub.heading

    def speed(self):
        return self.forward_speed

    def set_wanted_speed(self, speed):
        self.port_sub.sub.set_wanted_speed(speed)

    def set_wanted_heading(self, heading):
        self.port_sub.sub.set_heading(heading)

    def set_wanted_depth(self, depth):
        self.port_sub.sub.set_wanted_depth(depth)

    def stop_motion(self, timeout: float = 10, interval=0.01):
        """
        Stop forward motion using a pid defined using `Kp`, `Ki`, and `Kd`; blocks until average speed over
        `average_length` intervals is less than or equal to max_speed. If it is not stopped after
        `timeout` seconds, it will stop and return False, otherwise True.
        Updates motors every `interval` seconds, default 0.01 (= 10 ms)
        """
        speed_pid = PID(self.Fp, self.Fi, self.Fd, 0)

        start = time.time()
        previous = deque()

        while timeout > time.time() - start:
            if len(previous) >= self.average_accuracy:
                average = sum(previous) / self.average_accuracy
                if self.max_speed >= average:
                    return True
            previous.appendleft(self.speed())
            previous.pop()

            self.update_sensors()
            self.set_wanted_speed(speed_pid.signal(self.speed()))
            self.update_motors()

            time.sleep(interval)

        return False


    def move_time(self, speed, seconds):
        """Move at `speed` for `seconds` seconds before stopping"""
        self.set_wanted_speed(speed)
        time.sleep(seconds)
        self.stop_motion()