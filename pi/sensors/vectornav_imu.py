from pi.port_controller import PortController


# wrapper class to get data out of the imu
class VectorNavIMU:
    def __init__(self, port: str):
        self.port: PortController = PortController(port)

    def get_angle(self) -> float:
        # TODO read angle with self.port.read()!
        # REMEMBER TO SANITIZE FIRST
        self.port.read()
        return 1.0

    def get_forward_speed(self) -> float:
        # TODO read speed with self.port.read()!
        # REMEMBER TO SANITIZE FIRST
        self.port.read()
        return 1.0
