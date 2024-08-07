import serial


class PortController:
    def __init__(self, port: str, *, baud: int = 9600, parity: str = serial.PARITY_NONE, stopbits: int = serial.STOPBITS_ONE, bytesize: int = serial.EIGHTBITS, timeout: float = 1):
        # Replace port with the correct port and '9600' with the correct baud rate
        self.ser = serial.Serial(
            port=port,
            baudrate=baud,
            parity=parity,
            stopbits=stopbits,
            bytesize=bytesize,
            timeout=timeout
        )

    def write(self, data, encoding: str = 'utf-8') -> None:
        """Write `data` to port using `encoding`"""
        self.ser.write(data.encode(encoding))

    def read(self, size: int = 1) -> bytes:
        """Reads `size` bytes. Sanitize data before use."""
        return self.ser.read(size)
