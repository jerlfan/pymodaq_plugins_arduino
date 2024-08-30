pymodaq_plugins_arduino
#######################

.. the following must be adapted to your developed package, links to pypi, github  description...

.. image:: https://img.shields.io/pypi/v/pymodaq_plugins_arduino.svg
   :target: https://pypi.org/project/pymodaq_plugins_arduino/
   :alt: Latest Version

.. image:: https://readthedocs.org/projects/pymodaq/badge/?version=latest
   :target: https://pymodaq.readthedocs.io/en/stable/?badge=latest
   :alt: Documentation Status

.. image:: https://github.com/PyMoDAQ/pymodaq_plugins_arduino/workflows/Upload%20Python%20Package/badge.svg
   :target: https://github.com/PyMoDAQ/pymodaq_plugins_arduino
   :alt: Publication Status

.. image:: https://github.com/PyMoDAQ/pymodaq_plugins_arduino/actions/workflows/Test.yml/badge.svg
    :target: https://github.com/PyMoDAQ/pymodaq_plugins_arduino/actions/workflows/Test.yml


This package regroups a list of instrument created around an arduino board. Some instruments use the
Telemetrix library to use python together with the arduino board.


Authors
=======

* Sebastien J. Weber  (sebastien.weber@cemes.fr)


.. if needed use this field

    Contributors
    ============

    * First Contributor
    * Other Contributors

.. if needed use this field

  Depending on the plugin type, delete/complete the fields below


Instruments
===========

Below is the list of instruments included in this plugin

Actuators
+++++++++

* **LED**: control of a multicolor LED using three PWM digital outputs. Allows the control of the three color channel
  independently

.. if needed use this field

    Viewer0D
    ++++++++

    * **yyy**: control of yyy 0D detector
    * **xxx**: control of xxx 0D detector

    Viewer1D
    ++++++++

    * **yyy**: control of yyy 1D detector
    * **xxx**: control of xxx 1D detector


    Viewer2D
    ++++++++

    * **yyy**: control of yyy 2D detector
    * **xxx**: control of xxx 2D detector


    PID Models
    ==========

    Extensions
    ==========


Installation instructions
=========================

* PyMoDAQ version > 4.1.0


LED actuator
++++++++++++

The LED actuator uses the telemetrix library. The correponding sketch should therefore be uploaded
on the arduino board
