from pymodaq_plugins_arduino.hardware.arduino_telemetrix import Arduino
from pymodaq_plugins_arduino.hardware.lcd_i2c.lcd_i2c import LCD

from pymodaq_plugins_arduino.utils import Config
config = Config()


class ArduinoLCD(Arduino):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ini_i2c()
        self.lcd = LCD(config('LCD', 'address'),
                       cols=config('LCD', 'cols'),
                       rows=config('LCD', 'rows'),
                       i2c=self)

        self._is_init: bool = False

    def ini_lcd(self):
        self.lcd.begin()
        self.lcd.display()
        self.lcd.backlight()
        self._is_init = True

    def shutdown(self):
        if self._is_init:
            self.lcd.no_backlight()
            self.lcd.clear()
        super().shutdown()
