"""
.. module:: vcnl4200

**************
VCNL4200 Module
**************

.. _datasheet: https://www.vishay.com/docs/84430/vcnl4200.pdf

This module contains the Zerynth driver for Vishay VCNL4200.
The unit integrates a high sensitivity long distance proximity sensor (PS),
ambient light sensor (ALS), and 940 nm IRED into one small package.

Communication with this unit is done using I2C.

"""

import i2c

DEFAULT_I2C_ADDR = 0x51
REG_ALS_DATA = 0x09
REG_PS_DATA = 0x08

REG_ALS_CONF = 0x00
REG_PS_CONF_1_2 = 0x03
REG_PS_CONF_3 = 0x04

DEFAULT_ALS_CONF = 0b00000000
DEFAULT_PS_CONF1 = 0b11001010
DEFAULT_PS_CONF2 = 0b00001000
DEFAULT_PS_CONF3 = 0b00000000

class VCNL4200():
    '''
    
==============
VCNL4200 class
==============

.. class:: VCNL4200(drvsel, ps=True, als=True, address=DEFAULT_I2C_ADDR, clk=400000)

    Initialize an object representing the VCNL4200 board.
    The I2C communication is started, and enabled sensors are configured
    with a stanrdard configuration.

    Note: Default settings enable proximity sensor high definition and
    faster duty time, this results in more accuracy at the cost of more
    power usage.
    Refer to sensor datasheet and use configure_proximity_sensor(),
    configure_ambient_light_sensor() methods for more advanced settings.

    :param drvsel: The I2C port to be used. (e.g. I2C0)
    :param ps: Boolean for enabling the proximity sensor on board (Default: True)
    :param als: Boolean for enabling the ambient light sensor on board (Default: True)
    :param address: Byte for selecting the I2C address to be used. (Default: sensor default)
    :param clk: I2C clock speed to be used (100000 or 400000). (Default: 400000)
    '''
    def __init__(self, drvsel, ps=True, als=True, address=DEFAULT_I2C_ADDR, clk=100000):
        self.port = i2c.I2C(drvsel, address, clk)
        self.port.start()
        if ps:
            self.configure_proximity_sensor(DEFAULT_PS_CONF1, DEFAULT_PS_CONF2, DEFAULT_PS_CONF3)
        if als:
            self.configure_ambient_light_sensor(DEFAULT_ALS_CONF)

    def get_distance(self):
        '''
.. method:: get_distance()

    Returns an integer representing the proximity read from the sensor.
        '''
        return self._read_register(REG_PS_DATA)

    def get_ambient_light(self):
        '''
.. method:: get_ambient_light()

    Returns an integer in range 0-65535 representing the ambient light
    level read from the sensor.
        '''
        return self._read_register(REG_ALS_DATA)

    def configure_proximity_sensor(self, conf1, conf2, conf3):
        '''
.. method:: configure_proximity_sensor(conf1, conf2, conf3)

    Write settings for proximity sensor in registers PS_CONF1, PS_CONF2,
    and PS_CONF3. Refer to datasheet for all the available settings.

    :param conf1: Byte to be written in PS_CONF1 register.
    :param conf2: Byte to be written in PS_CONF2 register.
    :param conf3: Byte to be written in PS_CONF3 register.
        '''
        self._write_register(REG_PS_CONF_1_2, conf1, conf2)
        self._write_register(REG_PS_CONF_3, conf3)

    def configure_ambient_light_sensor(self, conf):
        '''
.. method:: configure_ambient_light_sensor(conf)

    Write settings for ambient light sensor in register ALS_CONF.
    Refer to datasheet for all the available settings.

    :param conf: Byte to be written in ALS_CONF register.
        '''
        self._write_register(REG_ALS_CONF, conf)

    def _read_register(self, address):
        data = self.port.write_read(address, 2)
        return data[0] + data[1] * 256

    def _write_register(self, address, low_byte, high_byte=0x00):
        return self.port.write([address, low_byte, high_byte])
