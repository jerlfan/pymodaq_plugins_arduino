
from typing import Union, List, Dict
from pymodaq.control_modules.move_utility_classes import (DAQ_Move_base, comon_parameters_fun,
                                                          main, DataActuatorType, DataActuator)

from pymodaq_utils.utils import ThreadCommand  # object used to send info back to the main thread
from pymodaq_gui.parameter import Parameter

from pymodaq_plugins_arduino.hardware.arduino_telemetrix import Arduino # ACS controller wrapper


class DAQ_Move_StepperMotor(DAQ_Move_base):
    """ Minimalistic plugin to control ACS motion stages with PyMoDAQ.
    
    This object inherits all functionalities to communicate with PyMoDAQ’s DAQ_Move module through inheritance via
    DAQ_Move_base. It makes a bridge between the DAQ_Move module and the Python wrapper of a particular instrument.

    Use the ACSpy package wrapper to communicate with the ACS motion stages. 
    It may works with up to 8 axes depending the configuration.
    It does not consider the daisy chain option: only one controller.
    Only ETHERNET communication is implemented (see ACS manual for configuration).
    (It has been tested with USB to ethernet adapter).
    Tested with ACS SPiiPlusEC controller and one drive UDMnt(2 axes).
    The stages were alio's translation stages  AI-CM-6000-XY.
    PyMoDAQ version during the test was PyMoDAQ==5.0.5.
    The operating system used was Windows 11.
    Installation instructions: ACS drivers must be installed from the manufacturer's.
    They usually come with the controller and with a "buffer" file for coniguration.
    
  
    Attributes:
    -----------
    controller: object
        The particular object that allow the communication with the hardware, in general a python wrapper around the
         hardware library.
         
    # TODO add your particular attributes here if any

    """
    is_multiaxes = True
     # Configured for only two stepper motors with arduino Uno board.
    _axis_names: Union[List[str], Dict[str, int]] = {'Motor0':0, 'Motor1':1}
    # TODO changing the name using the config file is not implemented yet.
    _controller_units: Union[str, List[str]] = ''
    _epsilon: Union[float, List[float]] = 1 
    data_actuator_type = DataActuatorType.DataActuator  
    
    
    params = [ {'title': 'Ports:', 'name': 'com_port', 'type': 'list',
                  'value': config('com_port'), 'limits': Arduino.COM_PORTS}, 
                ] + comon_parameters_fun(is_multiaxes, axis_names=_axis_names, epsilon=_epsilon)
    # _epsilon is the initial default value for the epsilon parameter allowing pymodaq to know if the controller reached
    # the target value. It is the developer responsibility to put here a meaningful value

    def ini_attributes(self):
        self.controller: Optional[Arduino] = None

    def get_actuator_value(self):
        """Get the current value from the hardware with scaling conversion.

        Returns
        -------
        float: The position obtained after scaling conversion.
        """
        
        pos = DataActuator(
                    data=self.controller.axes[self.axis_value].rpos,
                    unit=self.axis_unit)  
        pos = self.get_position_with_scaling(pos)
        return pos

    def move_done_callback(self, val: int):
        """Will be triggered for each end of move; abs, rel or homing"""
        self._move_done = True
        self.stop_motion()
        logger.debug('Callback called')

    def user_condition_to_reach_target(self) -> bool:
        """ Will be triggered for each end of move; abs, rel or homing"""
        return self._move_done

    def close(self):
        """Terminate the communication protocol"""
        self.controller.disable_all()
        self.controller.disconnect()

    def commit_settings(self, param: Parameter):
        """Apply the consequences of a change of value in the detector settings

        Parameters
        ----------
        param: Parameter
            A given parameter (within detector_settings) whose value has been changed by the user
        """
        ## TODO for your custom plugin
        if param.name() == 'axis':
            self.get_actuator_value()  # to update the current position of the axis
            #self.axis_unit = 'mm'
            # do this only if you can and if the units are not known beforehand, for instance
            # if the motors connected to the controller are of different type (mm, µm, nm, , etc...)
            # see BrushlessDCMotor from the thorlabs plugin for an exemple

        elif param.name() == "a_parameter_you've_added_in_self.params":
           self.controller.your_method_to_apply_this_param_change()
        else:
            pass

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
        
        self.ini_stage_init(slave_controller=controller)  # will be useful when controller is slave

        if self.is_master:  # is needed when controller is master
            self.controller = Controller(contype="ethernet", n_axes=2) 
            self.controller.connect()  # any object that will control the stages
            self.controller.enable_all()  # enable all axes
            self.settings['serial_num']=self.controller.serial_number()
            self.controller.load_buffer(self.settings['buff_num'])  # load the buffer file (it is needed to configure the controller)
            
          
        info = "Controller connected and axis enabled"
        initialized = True#self.controller.a_method_or_atttribute_to_check_if_init()  # todo
        return info, initialized

    def move_abs(self, value: DataActuator):
        """ Move the actuator to the absolute target defined by value

        Parameters
        ----------
        value: (float) value of the absolute target positioning
        """

        value = self.check_bound(value)  #if user checked bounds, the defined bounds are applied here
        self.target_value = value
        value = self.set_position_with_scaling(value)  # apply scaling if the user specified one
        self.controller.axes[self.axis_value].ptp(value.value())  # when writing your own plugin replace this line
        self.emit_status(ThreadCommand('Update_Status', ['Some info you want to log']))

    def move_rel(self, value: DataActuator):
        """ Move the actuator to the relative target actuator value defined by value

        Parameters
        ----------
        value: (float) value of the relative target positioning
        """
        value = self.check_bound(self.current_position + value) - self.current_position
        self.target_value = value + self.current_position
        value = self.set_position_relative_with_scaling(value)

        
        self.controller.axes[self.axis_value].ptpr(value.value())
        self.emit_status(ThreadCommand('Update_Status', ['Some info you want to log']))

    def move_home(self):
        """Call the reference method of the controller"""
        self.move_abs(DataActuator(data=0, unit=self.axis_unit))
    

    def stop_motion(self):
      """Stop the actuator and emits move_done signal"""

      ## TODO for your custom plugin
      raise NotImplemented  # when writing your own plugin remove this line
      self.controller.your_method_to_stop_positioning()  # when writing your own plugin replace this line
      self.emit_status(ThreadCommand('Update_Status', ['Some info you want to log']))


if __name__ == '__main__':
    main(__file__)