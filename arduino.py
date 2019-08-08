#author: dorfer@phys.ethz.ch
import serial
import time
import collections
import numpy as np


class Arduino(object):

    def __init__(self, serial_port='/dev/ttyACM0', baud_rate=9600, read_timeout=5):
        self.conn = serial.Serial(serial_port, baud_rate)
        self.conn.timeout = read_timeout # Timeout for readline()
        time.sleep(0.2)
        print('Connection to Arduino opened.')

    def getTemperature(self):
        try:
            temperatures = []
            for ch in ['A', 'B']:
                cmd = ch + '\r\n'
                self.conn.write(str.encode(cmd))
                temp = self.conn.readline()
                temp = temp.decode()
                temp = float(temp)
                temperatures.append(temp)
            return temperatures
        except:
            return [999, 999] #so we don't overheat our sensor in case something goes wrong
            pass


    def close(self):
        self.a.close()
        print('Connection to Arduino closed.')


if __name__ == '__main__':
    ard = Arduino()
    print(ard.getTemperature())