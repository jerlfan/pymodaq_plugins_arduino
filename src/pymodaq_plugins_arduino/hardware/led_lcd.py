import time

from pymodaq_plugins_arduino.hardware.arduino_telemetrix_lcd import ArduinoLCD

from pymodaq_plugins_arduino.utils import Config

from threading import Lock

config = Config()

lcd_header = 'RED  GREEN  BLUE'

lock = Lock()


def lcd_string(red: int, green: int, blue: int):
    return f'{red:03.0f}   {green:03.0f}    {blue:03.0f}'


class LED_LCD(ArduinoLCD):

    def ini_lcd(self):
        super().ini_lcd()
        self.lcd.clear()
        self.lcd.print(lcd_header)

    def analog_write_and_memorize(self, pin, value):
        lock.acquire()
        super().analog_write_and_memorize(pin, value)
        self.lcd.set_cursor(0, 1)
        string = lcd_string(self.pin_values_output.get(config('LED', 'pins', 'red_pin'), 0),
                            self.pin_values_output.get(config('LED', 'pins', 'green_pin'), 0),
                            self.pin_values_output.get(config('LED', 'pins', 'blue_pin'), 0),
                            )
        self.lcd.print(string)
        time.sleep(0.003)
        lock.release()
