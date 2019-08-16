import serial
from time import sleep


#WARNING
#it's a bit fucked up ch1=right, ch2=left - British device..
#here it's programmed the only logical way (their ch2 = our ch1) and (their ch1 = our ch2)
#Gott strafe England!

class LowVoltage(object):
	def __init__(self, mx_vol):
		self.lv = None
		self.max_voltage = mx_vol
		self.open()
		self.initialize()
		self.enabled = False

	def open(self):
		self.lv = serial.Serial("/dev/lvsupply", 9600)
		if self.lv.isOpen() == True:
			sleep(0.2)
			self.lv.write(b'*RST\r\n')
			self.lv.write(b'*IDN?\r\n') 
			val = self.lv.readline().decode()
			print(' Connected to:\n',val)
		else:
			print("Failed to open connection.")

	def initialize(self):
		self.lv.write(b'OP2 0\r\n') #turn channel 1 off
		cmd = 'V2 {}\r\n'.format(self.max_voltage)
		self.lv.write(str.encode(cmd))
		self.lv.write(b'I2 0.002\r\n') #sets current limit
		self.lv.write(b'OCP2 2\r\n') #current protection trip point

		self.lv.write(b'OP1 0\r\n') #turn channel 2 off
		cmd = 'V1 {}\r\n'.format(self.max_voltage)
		self.lv.write(str.encode(cmd))
		self.lv.write(b'I1 0.002\r\n') #sets current limit
		self.lv.write(b'OCP1 2\r\n') #current protection trip point


	def turnChannelOn(self):
		self.lv.write(b'OP2 1\r\n') #turn channel 1 on
		self.lv.write(b'OP1 1\r\n') #turn channel 2 on

	def setCurrent(self, curr1, curr2):
		self.turnChannelOn()
		cmd = 'I2 {}\r\n'.format(curr1)
		self.lv.write(str.encode(cmd)) #changes the current limit
		sleep(0.010)
		cmd = 'I1 {}\r\n'.format(curr2)
		self.lv.write(str.encode(cmd)) #changes the current limit


	def getCurrent(self):
		self.lv.write(b'I2O?\r\n') 
		curr1 = self.lv.readline().decode()
		curr1 = curr1.replace('A', '').rstrip("\n\r")
		sleep(0.010)
		self.lv.write(b'I1O?\r\n') 
		curr2 = self.lv.readline().decode()
		curr2 = curr2.replace('A', '').rstrip("\n\r")
		return [curr1, curr2]

	
	def close(self):
		self.lv.write(b'OP2 0\r\n') #turn channel 1 off
		self.lv.write(b'OP1 0\r\n') #turn channel 2 off
		self.lv.close()
		print('Connection to low voltage supply closed')



if __name__ == '__main__':
	lv = LowVoltage(1)
	lv.close()
	#lv.turnChannelOn()
	#lv.setCurrent(0.2)
