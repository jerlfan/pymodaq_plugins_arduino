import numpy as np
from pymodaq.utils.daq_utils import ThreadCommand
from pymodaq.utils.data import DataFromPlugins, DataToExport
from pymodaq.control_modules.viewer_utility_classes import DAQ_Viewer_base, comon_parameters, main
from pymodaq.utils.parameter import Parameter

from typing import Optional

from pymodaq_plugins_arduino.hardware.arduino_telemetrix import Arduino
from pymodaq_plugins_arduino.utils import Config

config=Config()
class DAQ_0DViewer_Analog(DAQ_Viewer_base):
    """ Instrument plugin class for a OD viewer.

    This object inherits all functionalities to communicate with PyMoDAQ’s DAQ_Viewer module through inheritance via
    DAQ_Viewer_base. It makes a bridge between the DAQ_Viewer module and the Python wrapper of a particular instrument.

    This plugins is intended to work with Arduino UNO type board. It should be working for others but haven't been
    tested yet (10/2024). This plugin use the Telemetrix implementation developed here:
    (https://mryslab.github.io/telemetrix/).
    It has been tested with an Arduino Uno with PyMoDAQ Version was 4.4.2 on Windows 10 Pro (Ver 22h2)

    This plugin needs to upload Telemetrix4Arduino to your Arduino-Core board (see Telemetrix installation)

    Attributes:
    -----------
    controller: object
        The particular object that allow the communication with the hardware, in general a python wrapper around the
         hardware library.

    # TODO add your particular attributes here if any

    """
    _controller_units=''
    params = comon_parameters + [{'title': 'Ports:', 'name': 'com_port', 'type': 'list',
                  'value': config('com_port'), 'limits': Arduino.COM_PORTS},
        {'title': 'AI:', 'name': 'ai_channel', 'type': 'list','limits':['0','1','2','3','4','5'],
         'value':'2'}
    ]

    def ini_attributes(self):
        #  TODO declare the type of the wrapper (and assign it to self.controller) you're going to use for easy
        #  autocompletion
        self.controller: Optional[Arduino] = None

        # TODO declare here attributes you want/need to init with a default value
        pass

    def commit_settings(self, param: Parameter):
        """Apply the consequences of a change of value in the detector settings

        Parameters
        ----------
        param: Parameter
            A given parameter (within detector_settings) whose value has been changed by the user
        """
        ## TODO for your custom plugin
        if param.name() == "ai_channel":
            self.controller.set_analog_input(param.value())  # when writing your own plugin replace this line

    #        elif ...
    ##

    def ini_detector(self, controller=None):
        """Detector communication initialization

        Parameters
        ----------
        controller: (object)
            custom object of a PyMoDAQ plugin (Slave case). None if only one actuator/detector by controller
            (Master case)

        Returns
        -------
        info: str
        initialized: bool
            False if initialization failed otherwise True
        """

        self.ini_detector_init(slave_controller=controller)

        if self.is_master:
            self.controller = Arduino(com_port=self.settings['com_port'])  # instantiate you driver with whatever arguments are needed
            #self.controller.open_communication()  # call eventual methods

        # TODO for your custom plugin (optional) initialize viewers panel with the future type of data
        #self.dte_signal_temp.emit(DataToExport(name='AnalogInput',
        #                                       data=[DataFromPlugins(name='Mock1',
        #                                                             data=[np.array([0]), np.array([0])],
        #                                                             dim='Data0D',
         #                                                            labels=['Mock1', 'label2'])]))
        #self.controller.analog_pin_values_input
        info = "Analog ready"
        initialized = True
        return info, initialized

    def close(self):
        """Terminate the communication protocol"""
        if self.is_master:
            self.controller.shutdown()

    def grab_data(self, Naverage=1, **kwargs):
        """Start a grab from the detector

        Parameters
        ----------
        Naverage: int
            Number of hardware averaging (if hardware averaging is possible, self.hardware_averaging should be set to
            True in class preamble and you should code this implementation)
        kwargs: dict
            others optionals arguments
        """
        self.controller.set_analog_input(2)
        data_tot = self.controller.analog_pin_values_input[2]
        self.dte_signal.emit(DataToExport(name='Analog Input',
                                          data=[DataFromPlugins(name='AI', data=data_tot,
                                                                dim='Data0D', labels=['dat0', 'data1'])]))


    def callback(self):
        """optional asynchrone method called when the detector has finished its acquisition of data"""
        data_tot = self.controller.your_method_to_get_data_from_buffer()
        self.dte_signal.emit(DataToExport(name='myplugin',
                                          data=[DataFromPlugins(name='Mock1', data=data_tot,
                                                                dim='Data0D', labels=['dat0', 'data1'])]))

    def stop(self):
        """Stop the current grab hardware wise if necessary"""
        self.controller.disable_all_reporting()


if __name__ == '__main__':
    main(__file__)