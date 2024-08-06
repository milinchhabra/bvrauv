from pi.port_controller import PortController
from motor_packet import MotorPacket

# A wrapper class to communicate with the arduino motor controller

# TODO consider output of arduino; events maybe?


class MotorControl:
    def __init__(self, port: str):

        self.port: str = port
        self.serial: PortController = PortController(port)

    def send(self, packet: MotorPacket) -> None:
        """Send a packet of commands over this port"""
        self.serial.write(packet.toString())


