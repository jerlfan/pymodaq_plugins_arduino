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

    def analog_write_and_memorize(self, pin, value):
        self.analog_write(pin, value)
        self.pin_values_output[pin] = value

    def get_output_pin_value(self, pin: int):
        return self.pin_values_output[pin]

