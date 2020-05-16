#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Contains the commands to be given to the raspberry to control data acquisition."""

from socket import *
import ast
import math
import time
from pyquaternion import Quaternion


# Screen costants
W_SIZE = 480
H_SIZE = 320

# Socket costants
serverName = "192.168.4.1"
serverPort = 8866
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.setsockopt(SOL_SOCKET, SO_RCVBUF, 1)


class MultiplexCommands(object):
    """Class with methods for controlling the I2C mux from raspberry."""

    def __init__(self):
        """MultiplexCommands initialization."""
        self.__addr__ = 0x70
        self.__bus__ = 1
        self.channel = 0
        msg = "#MUX#INIT"
        clientSocket.sendto(msg.encode(), (serverName, serverPort))
        raw_msg, serverAddress = clientSocket.recvfrom(2048)
        print(raw_msg)
        if self.parser(raw_msg):
            print("Mux Initialized")

    def switch_channel(self, channel=0):
        """Methods for sending to the raspberry the mux channel."""
        msg = "#MUX#SWITCH" + str(channel)
        clientSocket.sendto(msg.encode(), (serverName, serverPort))
        raw_msg, serverAddress = clientSocket.recvfrom(2048)
        if self.parser(raw_msg):
            print("Switched channel on mpu" + str(self.channel))

    def parser(self, raw_msg):
        """Method that parse raw messages."""
        tmp = raw_msg.decode("utf-8")
        tmp = tmp.strip("#MUX#")
        if tmp[0:5] == "INIT":
            return True
        elif tmp[0:5] == "SWITCH":
            tmp = tmp.strip("SWITCH")
            self.channel = int(tmp)
            return True


class MPUCommands(object):
    """Class with methods to control setup and data acquisition of MPU6050 sensors from raspberry."""

    def __init__(self, name):
        """ MPU commands class initialization."""
        self.__name__ = name
        self.__addr__ = 0x68
        msg = "#MPU#" + str(name)
        clientSocket.sendto(msg.encode(), (serverName, serverPort))
        raw_msg, serverAddress = clientSocket.recvfrom(2048)
        if self.parser(raw_msg):
            print("MPU" + str(self.__name__) + ": INITIALIZED")

    def read_value(self, queue):
        """Read value from the sensors."""
        while(True):
            raw_msg, serverAddress = clientSocket.recvfrom(2048)
            quat, grav = self.parser(raw_msg)
            queue.get()
            queue.put(quat)

    def read_gravity(self):
        """Read gravity data."""
        raw_msg, serverAddress = clientSocket.recvfrom(2048)
        quat, grav = self.parser(raw_msg)
        self.quaternion = quat
        self.gravity = grav
        return grav

    def parser(self, raw_msg):
        """Method that parse raw messages."""
        tmp = raw_msg.decode("utf-8")
        tmp = tmp.strip("#MPU#")
        if tmp[0:5] == "DATA#":
            tmp = tmp.strip("DATA#")
            tmp = tmp.split("/")
            tmp[0] = tmp[0].strip("Q")
            q = ast.literal_eval(tmp[0])
            tmp[1] = tmp[1].strip("G")
            g = ast.literal_eval(tmp[1])
            # print(q)
            return q, g
        elif tmp[0:5] == "INIT#":
            tmp = tmp.strip("INIT#")
            self.drift = float(tmp)
            return True


def enable_buzzer(freq):
    """Activates the buzzer on the backstrap."""
    msg = "#BUZZ#" + str(freq)
    clientSocket.sendto(msg.encode(), (serverName, serverPort))


def stabilize_quat(mpu, t, dist):
    """Function that returns a stabilized quaternion."""
    q0 = Quaternion((0, 0, 0, 0))
    t0 = time.time()
    tmp_dist = 10000
    while((time.time() - t0 < t) or tmp_dist > dist):
        try:
            mpu.read_value()
            rotate_vect = mpu.quaternion
            q1 = Quaternion(rotate_vect)
            tmp_dist = Quaternion.absolute_distance(q1, q0)
            q0 = q1
        except Exception:
            continue
    g = mpu.read_gravity()
    return q1, g


def orientate_quat(quat, grav):
    """Function that returns a quaternion oriented accordinf to vect."""

    grav_rot = Quaternion(scalar=None, vector=grav).normalised
    quat_rot = grav_rot * quat.normalised
    return quat_rot


def filter_outlier(pos0, pos1):
    """Filetr outlier in the positions."""
    delta = 200
    if abs(pos0 - pos1) > delta:
        print("FOUND OUTLIER")
        return pos0
    else:
        return pos1


def yaw_drift(yaw, coeff, dt):
    """Function that compensate drift yaw."""
    yaw = yaw - coeff * dt
    return yaw


def quat_projection(ang, drift, dt):
    """Porject quate on the rotation plane."""
    z = [0, 0, -1]
    ang = yaw_drift(ang, drift, dt)
    q_z = Quaternion(axis=z, degrees=ang)
    return q_z


def quat_to_euler(w, x, y, z):
    """Obtain eulerian system from a quaternion."""
    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + y * y)
    X = math.degrees(math.atan2(t0, t1))

    t2 = +2.0 * (w * y - z * x)
    t2 = +1.0 if t2 > +1.0 else t2
    t2 = -1.0 if t2 < -1.0 else t2
    Y = math.degrees(math.asin(t2))

    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (y * y + z * z)
    Z = math.degrees(math.atan2(t3, t4))

    return X, Y, Z


def fix_drifting(quat, drift, dt):
    """Compensated the quaternion drifting on the gyroscope."""
    w = quat.w
    x = quat.x
    y = quat.y
    z = quat.z
    X, Y, Z = quat_to_euler(w, x, y, z)
    quat_proj = quat_projection(Z, drift, dt)
    return quat_proj


def follow_position(r_pos, glider, scale):
    """Function that moves the hang glider of discrete units following the position of the MPU."""
    step = 10 * scale
    sens = step
    dist = abs(r_pos - glider.pos[0])
    if dist > sens:
        if glider.pos[0] < r_pos:
            tmp = glider.pos[0] + step
            if tmp + glider.base / 2 <= W_SIZE * scale:
                glider.pos[0] = tmp
        elif glider.pos[0] > r_pos:
            tmp = glider.pos[0] - step
            if tmp - glider.base / 2 >= 0 * scale:
                glider.pos[0] = tmp


def convert_pos(x, scale):
    """Convert the coordinates."""
    x_new = x * W_SIZE * scale + W_SIZE / 2 * scale
    return x_new


if __name__ == "__main__":

    # Mux initialization
    mux = MultiplexCommands()

    # MPU6050 initialization
    mux.switch_channel(4)
    mpu4 = MPUCommands("mpu4")

    rel_quat, gravity = stabilize_quat(mpu=mpu4, t=10, dist=10)
    abs_quat = orientate_quat(rel_quat, gravity, vector)
    ref_pos = Quaternion(scalar=None, vector=abs_quat.axis)

    while(True):

        # Mpu sensor reading
        try:
            mpu4.read_value()
            rel_quat = Quaternion(mpu4.quaternion)
            abs_quat = orientate_quat(rel_quat, gravity, vector)
            new_quat = abs_quat.rotate(ref_pos)
        except Exception as e:
            print(e)
            continue

        real_pos = convert_pos(new_quat.x)
        follow_position(real_pos, glider, Screen_scale)
        old_pos = real_pos
