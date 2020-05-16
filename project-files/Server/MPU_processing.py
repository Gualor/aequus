#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Contains the classes and methods to read and process the sensor's data."""

from MPU6050 import *
import smbus

i2c_bus = 1
mux_address = 0x70
dev_address = 0x68

# File path for calibration
mpu0_path = "Calibration/mpu0_cal.txt"
mpu1_path = "Calibration/mpu1_cal.txt"
mpu2_path = "Calibration/mpu2_cal.txt"
mpu3_path = "Calibration/mpu3_cal.txt"
mpu4_path = "Calibration/mpu4_cal.txt"
mpu5_path = "Calibration/mpu5_cal.txt"


class mpu_sensor(MPU6050):
    """Class for MPU6050 sensor with setup and reading functions."""

    def __init__(self, name, path_txt):
        """Sensor initialization."""
        self.cal_values = self.read_calibration(path_txt)
        self.i2c_bus = 1
        self.dev_address = 0x68
        self.x_accel_offset = self.cal_values["x_accel_offset"]
        self.y_accel_offset = self.cal_values["y_accel_offset"]
        self.z_accel_offset = self.cal_values["z_accel_offset"]
        self.x_gyro_offset = self.cal_values["x_gyro_offset"]
        self.y_gyro_offset = self.cal_values["y_gyro_offset"]
        self.z_gyro_offset = self.cal_values["z_gyro_offset"]
        super(mpu_sensor, self).__init__(self.i2c_bus, self.dev_address, self.x_accel_offset, self.y_accel_offset, self.z_accel_offset, self.x_gyro_offset, self.y_gyro_offset, self.z_gyro_offset, a_debug=False)
        self.dmp_initialize()
        self.set_DMP_enabled(True)
        self.name = name
        self.int_status = self.get_int_status()
        self.packet_size = self.DMP_get_FIFO_packet_size()
        self.FIFO_count = self.get_FIFO_count()
        self.FIFO_buffer = [0] * 64
        print("######\tSETUP SENSOR: " + self.name + " COMPLETED\t######")
        # print(hex(self.int_status))
        # print(self.packet_size)
        # print(self.FIFO_count)

    def read_calibration(self, path):
        """Return a dictionary with coefficient's name and associated value."""
        dict = {}
        with open(path, "r") as fp:
            for line in fp:
                tmp = line.split()
                header = tmp[0]
                value = round(float(tmp[2]))
                dict[header] = value
        return dict

    def get_value(self, tmp_quat, tmp_gravity):
        """Read value from sensor."""
        self.FIFO_count = self.get_FIFO_count()
        self.int_status = self.get_int_status()
        # If overflow is detected by status or fifo count we want to reset
        if (self.FIFO_count == 1024) or (self.int_status & 0x10):
            self.reset_FIFO()
        elif (self.FIFO_count % self.packet_size != 0):
            self.reset_FIFO()
        # Check if fifo data is ready
        elif (self.int_status & 0x02):
            # Wait until packet_size number of bytes are ready for reading, default
            # is 42 bytes
            while self.FIFO_count < self.packet_size:
                self.FIFO_count = self.get_FIFO_count()
            self.FIFO_buffer = self.get_FIFO_bytes(self.packet_size)
            self.quat = self.DMP_get_quaternion_int16(self.FIFO_buffer)
            tmp_quat = [self.quat.w, self.quat.x, self.quat.y, self.quat.z]
            tmp_gravity = self.DMP_get_gravity(self.quat)
            return tmp_quat, tmp_gravity


class multiplex(object):
    """Class for I2C expander mux."""

    def __init__(self, bus=1):
        """Mux init."""
        self.bus = smbus.SMBus(bus)

    def channel(self, address=0x70, channel=0):
        """Channels selector I2C."""
        action = 1 << channel
        # 0x04 is the register for switching channels
        self.bus.write_byte_data(address, 0x04, action)


if __name__ == "__main__":

    # Mux definition
    mux = multiplex(i2c_bus)
    # Sensors definition
    mux.channel(mux_address, 0)
    mpu0 = mpu_sensor("mpu0", mpu0_path)
    mux.channel(mux_address, 1)
    mpu1 = mpu_sensor("mpu1", mpu1_path)
    mux.channel(mux_address, 2)
    mpu2 = mpu_sensor("mpu2", mpu2_path)
    mux.channel(mux_address, 3)
    mpu3 = mpu_sensor("mpu3", mpu3_path)
    mux.channel(mux_address, 4)
    mpu4 = mpu_sensor("mpu4", mpu4_path)
    mux.channel(mux_address, 5)
    mpu5 = mpu_sensor("mpu5", mpu5_path)

    while(True):

        # Sensors reading
        mux.channel(mux_address, 0)
        mpu0.get_value()
        mux.channel(mux_address, 1)
        mpu1.get_value()
        mux.channel(mux_address, 2)
        mpu2.get_value()
        mux.channel(mux_address, 3)
        mpu3.get_value()
        mux.channel(mux_address, 4)
        mpu4.get_value()
        mux.channel(mux_address, 5)
        mpu5.get_value()
