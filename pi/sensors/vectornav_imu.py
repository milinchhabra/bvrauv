import time

from pi.port_controller import PortController
import vnpy


# wrapper class to get data out of the imu
class VectorNavIMU:
    def __init__(self, port: str, baud: int):
        self.imu = vnpy.VnSensor()
        self.imu.connect(port, baud)

    def get_heading(self) -> float:
        return self.imu.read_yaw_pitch_roll().x

    def angle_to(self, target: float) -> float:
        yaw = self.get_heading()
        diff = point_to - yaw

        if abs(point_to - yaw) >= 180:
            sign = yaw / abs(yaw)
            abs_diff_yaw = 180 - abs(yaw)
            abs_diff_target = 180 - abs(point_to)
            diff = sign * (abs_diff_yaw + abs_diff_target)
        return diff

    def get_forward_speed(self) -> float:
        # this doesnt work bc no odometry
        # # TODO read speed with self.port.read()!
        # # REMEMBER TO SANITIZE FIRST
        # self.port.read()
        # return 1.0
        raise NotImplementedError()


# vn = VectorNavIMU('COM3', 921600)
#
# print(vn.imu.read_model_number())
# point_to = 170