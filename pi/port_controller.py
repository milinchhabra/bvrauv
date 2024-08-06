import serial
import time


# TODO label with typing
class PortController:
    def __init__(self, port, *, baud=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1):

        # Replace port with the correct port and '9600' with the correct baud rate
        self.ser = serial.Serial(
            port=port,
            baudrate=baud,
            parity=parity,
            stopbits=stopbits,
            bytesize=bytesize,
            timeout=timeout
        )

    def write(self, data, encoding='utf-8'):
        self.ser.write(data.encode(encoding))

    def read(self, size=1):
        # size = number of bytes. Sanitize data before use!
        self.ser.read(size)