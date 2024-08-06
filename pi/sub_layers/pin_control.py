from pi.motor_control.motor_serial import MotorControl
from pi.motor_control.motor_packet import all_motors_packet
from pi.sensors.vectornav_imu import VectorNavIMU
from pi.sensors.depth_sensor import DepthSensor
from abstract_sub import AUV

# A wrapper class for an abstract sub to control all ports (sensors and arduino)


class PinControl:
    def __init__(self, abstract_sub, motor_port, depth_bus, imu_port):
        self.sub: AUV = abstract_sub
        self.arduino = MotorControl(motor_port)
        self.depth_sensor = DepthSensor(depth_bus)
        self.imu = VectorNavIMU(imu_port)

    def update_data(self):
        self.sub.set_depth(self.depth_sensor.get_depth())
        self.sub.set_heading(self.imu.get_angle())

    def update_motors(self):
        self.arduino.send(all_motors_packet(self.sub.get_motors()))
