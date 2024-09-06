from pymodaq.control_modules.move_utility_classes import main

from pymodaq_plugins_arduino.daq_move_plugins.daq_move_LED import DAQ_Move_LED
from pymodaq_plugins_arduino.hardware.led_lcd import LED_LCD
from pymodaq_plugins_arduino.utils import Config

config = Config()


class DAQ_Move_LEDwithLCD(DAQ_Move_LED):
    """ Instrument plugin class for an actuator.
    
    This object inherits all functionalities to communicate with PyMoDAQ’s DAQ_Move module through inheritance via
    DAQ_Move_base. It makes a bridge between the DAQ_Move module and the Python wrapper of a particular instrument.

    Attributes:
    -----------
    controller: object
        The particular object that allow the communication with the hardware, in general a python wrapper around the
         hardware library.
         
    """

    def ini_stage(self, controller=None):
        """Actuator communication initialization

        Parameters
        ----------
        controller: (object)
            custom object of a PyMoDAQ plugin (Slave case). None if only one actuator by controller (Master case)

        Returns
        -------
        info: str
        initialized: bool
            False if initialization failed otherwise True
        """

        self.controller = self.ini_stage_init(
            old_controller=controller,
            new_controller=None)
        if self.is_master:
            self.controller = LED_LCD(
                com_port=self.settings['com_port']
                                              )
            self.controller.ini_lcd()
            self.set_pins()

        info = "Whatever info you want to log"
        initialized = True
        return info, initialized


if __name__ == '__main__':
    main(__file__)
