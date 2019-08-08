import sys
import serial
import time
from simple_pid import PID
import threading
#import matplotlib
#matplotlib.use("TkAgg")
#import matplotlib.pyplot as plt




class TemperatureControl(object):
    def __init__(self, ard, lv, logger):
        self.ard = ard
        self.lv = lv
        
        #PID controllers
        self.pid1 = PID()
        self.pid1.sample_time = 0.5 #update every 1s
        self.pid1.output_limits = (0, 1.5) #Amps on output

        self.pid2 = PID()
        self.pid2.sample_time = 0.5 #update every 1s
        self.pid2.output_limits = (0, 1.5) #Amps on output
        
        #thread the temp control process
        self.pill2kill = threading.Event()
        self.controlThread = threading.Thread(target=self.controlCurrent, args=(self.pill2kill, 'test'))


        self.running = False

        self.logger = logger

        
    def setTemperature(self, temp1, temp2):
        self.pid1.setpoint = temp1
        self.pid2.setpoint = temp2


    def controlCurrent(self, killme, arg):
        self.running = True
        while True:
            [temp1, temp2] = self.ard.getTemperature()
            #calculate needed current
            set_curr1 = self.pid1(temp1)
            set_curr2 = self.pid2(temp2)
            #set it to lv supply and read actual value back
            self.lv.setCurrent(set_curr1, set_curr2)
            [out_curr1, out_curr2] = self.lv.getCurrent()

            self.logger.info('{} {} {} {}'.format(temp1, out_curr1, temp2, out_curr2))
            if killme.wait(0.005):
                return

    def stopControl(self):
        print('Executing stop control.')
        self.running = False
        self.pill2kill.set()
        self.controlThread.join(2)
        self.lv.setCurrent(0, 0)
        self.pill2kill = threading.Event()
        self.controlThread = threading.Thread(target=self.controlCurrent, args=(self.pill2kill, 'test'))