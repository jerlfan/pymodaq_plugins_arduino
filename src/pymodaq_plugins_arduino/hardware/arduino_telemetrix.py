from pyvisa import ResourceManager
from telemetrix import telemetrix


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
        for pin in self.pin_values_output:
            self.analog_write(pin, int(value))

    def analog_write_and_memorize(self, pin, value):
        value = self.round_value(value)
        self.analog_write(pin, value)
        self.pin_values_output[pin] = value

    def get_output_pin_value(self, pin: int):
        return self.pin_values_output.get(pin, 0)

    def ini_i2c(self, port: int = 0):
        self.set_pin_mode_i2c(port)

    def writeto(self, addr, bytes_to_write: bytes):
        """ to use the interface proposed by the lcd_i2c package made for micropython originally"""
        self.i2c_write(addr, [int.from_bytes(bytes_to_write)])