import pi.ms5837 as ms5837


# wrapper class to get data out of the depth sensor
class DepthSensor:
    def __init__(self, bus=1):
        self.sensor = ms5837.MS5837_30BA(bus)
        # default I2C bus is 1 (pi 3)

        if not self.sensor.init():
            print("Sensor could not be initialized")
            exit(1)

        if not self.sensor.read():
            print("Sensor read failed!")
            exit(1)
        self.sensor.setFluidDensity(ms5837.DENSITY_FRESHWATER)

    def get_depth(self) -> float:
        if self.sensor.read():
            return self.sensor.depth()
        else:
            exit(1)