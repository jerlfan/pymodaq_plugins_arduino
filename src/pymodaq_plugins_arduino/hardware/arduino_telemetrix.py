import numbers
from threading import Lock


from pyvisa import ResourceManager
from telemetrix import telemetrix

lock = Lock()

VISA_rm = ResourceManager()
COM_PORTS = []
for name, rinfo in VISA_rm.list_resources_info().items():
    if rinfo.alias is not None:
        COM_PORTS.append(rinfo.alias)
    else:
        COM_PORTS.append(name)


class Arduino(telemetrix.Telemetrix):
    COM_PORTS = COM_PORTS

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pin_values_output = {}

    @staticmethod
    def round_value(value):
        return max(0, min(255, int(value)))

    def set_pins_output_to(self, value: int):
        lock.acquire()
        for pin in self.pin_values_output:
            self.analog_write(pin, int(value))
        lock.release()

    def analog_write_and_memorize(self, pin, value):
        lock.acquire()
        value = self.round_value(value)
        self.analog_write(pin, value)
        self.pin_values_output[pin] = value
        lock.release()

    def get_output_pin_value(self, pin: int) -> numbers.Number:
        value = self.pin_values_output.get(pin, 0)
        return value

    def ini_i2c(self, port: int = 0):
        lock.acquire()
        self.set_pin_mode_i2c(port)
        lock.release()

    def writeto(self, addr, bytes_to_write: bytes):
        """ to use the interface proposed by the lcd_i2c package made for micropython originally"""
        lock.acquire()
        self.i2c_write(addr, [int.from_bytes(bytes_to_write, byteorder='big')])
        lock.release()

    def servo_move_degree(self, pin: int, value: float):
        """ Move a servo motor to the value in degree between 0 and 180 degree"""
        lock.acquire()
        self.servo_write(pin, int(value * 255 / 180))
        self.pin_values_output[pin] = value
        lock.release()


if __name__ == '__main__':
    import time
    tele = Arduino('COM23')
    tele.set_pin_mode_servo(5, 100, 3000)
    time.sleep(.2)

    tele.servo_write(5, 90)

    time.sleep(1)

    tele.servo_write(5, 00)

    tele.shutdown()