from tempcontrol import TemperatureControl
from arduino import Arduino
from lowvoltage import LowVoltage
from time import sleep
from datetime import datetime
from pytz import timezone
import logging
import os
import subprocess

temp1 = 60
temp2 = 60
max_voltage = 3

#generate timezone-aware timestamp
localtz = timezone('Europe/Zurich')
now = datetime.now()
now_tz_aware = localtz.localize(now)
ts_str = now_tz_aware.strftime("%Y-%m-%d_%H-%M-%S")
log_fn = ts_str + '_tempcontrol.log'

#set up logging module
logger = logging.getLogger('TempControl')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(log_fn)
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(message)s', datefmt='%Y.%m.%d %H:%M:%S')
fh.setFormatter(formatter)
ch.setFormatter(logging.Formatter('%(message)s'))
logger.addHandler(fh)
logger.addHandler(ch)


def main():
	ard = Arduino()
	
	lowv = LowVoltage(max_voltage)
	lowv.turnChannelOn()
	lowv.setCurrent(0.1, 0.1)

	temp = TemperatureControl(ard, lowv, logger)
	temp.setTemperature(temp1, temp2)
	temp.controlThread.start()

	sleep(2)
	os.environ["GNUPLOT_FILE"] = log_fn
	subprocess.call(["gnuplot","plot.gnu"]) 
	sleep(10)
	temp.stopControl()



if __name__ == '__main__':
	main()