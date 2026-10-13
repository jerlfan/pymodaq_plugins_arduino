from typing import Union, List, Dict, Optional
from pymodaq.control_modules.move_utility_classes import (
    DAQ_Move_base, comon_parameters_fun, main, DataActuatorType, DataActuator
)
from pymodaq_gui.parameter import Parameter
from pymodaq_plugins_arduino.hardware.arduino_telemetrix import Arduino
from pymodaq_plugins_arduino.utils import Config

config = Config()


class DAQ_Move_StepperMotor(DAQ_Move_base):
    """Plugin to control stepper motor using Arduino controller and PyMoDAQ.

    This object inherits all functionalities to communicate with PyMoDAQ’s DAQ_Move module through inheritance via
    DAQ_Move_base. It makes a bridge between the DAQ_Move module and the Python wrapper of a particular instrument.

    Use the arduino_telemetrix wrapper to communicate with the Arduino Board.
    Telemetrix supports up to 4 stepper motors, but this plugin currently drives a single axis.
    It does not consider the daisy chain option: only one controller.
    Moves are non-blocking and can be stopped with the Stop button.
    There is no encoder: the position is the step counter of the Arduino, reset to 0 at initialization.
    Tested with Arduino Uno and one motor NEMA17 (1 axis).
    PyMoDAQ version during the test was PyMoDAQ==5.3.2.
    The operating system used was Windows 11.
    Telemetrix4Arduino has to be uploaded on the Arduino board.

    Attributes
    ----------
    controller: object
        The particular object that allows communication with the hardware, in general, a Python wrapper around the
        hardware library.
    """
    _axis_names: Union[List[str], Dict[str, int]] = {'Stepper': config('stepper', 'name')}
    _controller_units: Union[str, Dict[str, str]] = {'Stepper': 'count'}
    _epsilons: Union[float, Dict[str, float]] = {'Stepper': 1}
    data_actuator_type = DataActuatorType.DataActuator

    params = [
        {
            'title': 'Ports:',
            'name': 'com_port',
            'type': 'list',
            'value': config('com_port'),
            'limits': Arduino.COM_PORTS,
        }
    ] + comon_parameters_fun(axis_names=_axis_names)

    def ini_attributes(self):
        self.controller: Optional[Arduino] = None

    def get_actuator_value(self) -> DataActuator:
        """Get the current position of the motor, in steps, with scaling conversion."""
        pos = DataActuator(data=self.controller.get_stepper_position(),
                           units=self.axis_unit)
        pos = self.get_position_with_scaling(pos)
        return pos

    def close(self):
        """Terminate the communication with the Arduino."""
        if self.controller is not None:
            self.controller.shutdown()

    def commit_settings(self, param: Parameter):
        """Apply the consequences of a change of value in the detector settings.

        Parameters
        ----------
        param: Parameter
            A given parameter (within detector_settings) whose value has been changed by the user.
        """
        pass

    def ini_stage(self, controller=None):
        """Actuator communication initialization.

        Parameters
        ----------
        controller: object
            Custom object of a PyMoDAQ plugin (Slave case). None if only one actuator by controller (Master case).

        Returns
        -------
        info: str
        initialized: bool
            False if initialization failed otherwise True.
        """
        if self.is_master:
            self.controller = Arduino(com_port=self.settings['com_port'])
            self.controller.initialize_stepper_motor(
                config('stepper', 'pins', 'pul_pin'),
                config('stepper', 'pins', 'dir_pin'),
                config('stepper', 'pins', 'ena_pin'),
            )  # Pulse, direction, enable pins
        else:
            self.controller = controller

        info = "Stepper motor connected with config file"
        initialized = self.controller.stepper_motor is not None
        return info, initialized

    def move_abs(self, value: DataActuator):
        """Move the motor to the absolute target defined by value."""
        value = self.check_bound(value)
        self.target_value = value
        value = self.set_position_with_scaling(value)
        self.controller.move_stepper_to_position(value.value(self.axis_unit))

    def move_rel(self, value: DataActuator):
        """Move the motor by the relative amount defined by value."""
        self.move_abs(self.current_value + value)

    def move_home(self):
        """Move the motor back to its reference position (step 0)."""
        home = DataActuator(data=0, units=self.axis_unit)
        self.target_value = self.get_position_with_scaling(home)
        self.controller.move_stepper_to_position(0)

    def stop_motion(self):
        """Stop the motor immediately, then emit the move_done signal"""
        self.controller.stop_stepper()
        self.move_done()


if __name__ == '__main__':
    main(__file__)