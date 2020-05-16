#!/usr/bin/python
# -*- coding: utf-8 -*-
""" MPU6050 data acquisition and transmission."""
import math
from MPU6050 import *

from MPU_processing import mpu_sensor
from MPU_processing import multiplex

from socket import *
from threading import Thread
from queue import Queue
import time
from pyquaternion import Quaternion

serverPort = 8866

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))

# Muc constants
i2c_bus = 1
mux_address = 0x70

# Queue to manage data
queue_mpu = Queue(maxsize=1)
queue_addr = Queue(maxsize=1)
queue_mpu.put(0)
queue_addr.put(0)


def read_data(q_mpu, q_addr):
    """Read commands from pc."""
    while(True):
        tag = 0
        message, clientAddress = serverSocket.recvfrom(2048)
        message = message.decode()
        print(message)
        q_addr.get()
        q_addr.put(clientAddress)
        tag = message[0:5]
        if(tag == "#MUX#"):
            msg = message.strip("#MUX#")
            print(msg)

            if(msg == "INIT"):
                mux = multiplex(i2c_bus)
                print("MUX INITIALIZE")
                messagge = ("#MUX#INIT")
                serverSocket.sendto(messagge.encode(), clientAddress)

            elif(msg[0:6] == "SWITCH"):
                msg = msg.strip("SWITCH")
                channel = int(msg)
                mux.channel(mux_address, channel)
                print("SWITCHED ON CHANNEL:\t" + str(channel))
                messagge = ("#MUX#SWITCH" + str(channel))
                serverSocket.sendto(messagge.encode(), clientAddress)
        elif(tag == "#MPU#"):
            name = message.strip("#MPU#")
            mpu = mpu_sensor(str(name), "Calibration/" + str(name) + "_cal.txt")
            coef = wait(mpu)
            q_mpu.get()
            q_mpu.put(mpu)

            messagge = ("#MPU#INIT#" + str(coef))
            serverSocket.sendto(messagge.encode(), clientAddress)

        '''
        elif(tag=="#BUZZ#"):
            msg = message.strip("#BUZZ#")
            freq = int(msg)
            buzzer.play(freq)
            #buzzer.stop()
        else:
            buzzer.stop()
        '''


def rpy(a_quat, a_grav_vect):
        # roll: (tilt left/right, about X axis)
    roll = math.atan(a_grav_vect.y /
                     math.sqrt(a_grav_vect.x * a_grav_vect.x +
                               a_grav_vect.z * a_grav_vect.z))
    # pitch: (nose up/down, about Y axis)
    pitch = math.atan(a_grav_vect.x /
                      math.sqrt(a_grav_vect.y * a_grav_vect.y +
                                a_grav_vect.z * a_grav_vect.z))
    # yaw: (about Z axis)
    yaw = math.atan2(2 * a_quat.x * a_quat.y - 2 * a_quat.w * a_quat.z,
                     2 * a_quat.w * a_quat.w + 2 * a_quat.x * a_quat.x - 1)
    return [roll, pitch, yaw]


def wait(mpu):
    time0 = time.time()
    time1 = time.time()
    quat_tmp = [0, 0, 0, 0]
    gravity_tmp = [0, 0, 0]
    tmp_yaw = 0

    while True:
        try:
            rotate_vect, gravity_vect = mpu.get_value(quat_tmp, gravity_tmp)
            rot_quat = Quaternion(rotate_vect)

            grav_quat = Quaternion(scalar=None, vector=gravity_vect)

            yaw = rpy(rot_quat, grav_quat)[2]
            break
        except TypeError as e:
            print(e)
            continue
    old_yaw = yaw

    while(time1 - time0 < 40):
        time1 = time.time()
        try:
            rotate_vect, gravity_vect = mpu.get_value(quat_tmp, gravity_tmp)
            rot_quat = Quaternion(rotate_vect)
            grav_quat = Quaternion(scalar=None, vector=gravity_vect)

            new_yaw = rpy(rot_quat, grav_quat)[2]
            tmp_yaw += new_yaw - old_yaw
            old_yaw = new_yaw

        except TypeError:
            continue

    cof = (tmp_yaw / (time1 - time0))
    print(cof)
    print(type(cof))
    return cof


def write_data(q_mpu, q_addr):
    """Write acquire data on wifi network."""
    quat_tmp = [0, 0, 0, 0]
    gravity_tmp = [0, 0, 0]

    mpu = q_mpu.get()
    q_mpu.put(mpu)
    while(mpu == 0):

        try:
            mpu = q_mpu.get()
            q_mpu.put(mpu)
            rotate_vect, gravity_quat = mpu.get_value(quat_tmp, gravity_tmp)
        except Exception as e:
            continue

    time0 = time.time()
    time1 = time.time()

    while(time1 - time0 < 30):
        time1 = time.time()
        try:
            rotate_vect, gravity_quat = mpu.get_value(quat_tmp, gravity_tmp)
        except TypeError:
            continue
    print("STABILIZED")
    message = ("#MPU#DATA#Q" + str(rotate_vect) + "/G" + str(gravity_quat))
    clientAddress = q_addr.get()
    q_addr.put(clientAddress)
    serverSocket.sendto(message.encode(), clientAddress)

    while(True):
        mpu = q_mpu.get()
        q_mpu.put(mpu)
        if mpu != 0:
            try:
                rotate_vect, gravity_quat = mpu.get_value(quat_tmp, gravity_tmp)
                message = ("#MPU#DATA#Q" + str(rotate_vect) + "/G" + str(gravity_quat))

                clientAddress = q_addr.get()
                q_addr.put(clientAddress)
                serverSocket.sendto(message.encode(), clientAddress)

            except TypeError as t:
                continue
            except OSError as o:
                continue


if __name__ == "__main__":

    readThread = Thread(name="readThread", target=read_data, args=[queue_mpu, queue_addr])
    readThread.start()
    writeThread = Thread(name="writeThread", target=write_data, args=[queue_mpu, queue_addr])
    writeThread.start()
