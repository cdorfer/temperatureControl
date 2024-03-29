import visa
from time import sleep

#WARNING
#it's a bit fucked up ch1=right, ch2=left - British device..
#here it's programmed the only logical way (their ch2 = our ch1) and (their ch1 = our ch2)
#Gott strafe England!

class LowVoltage(object):
	def __init__(self, mx_vol):
		self.rm = None
		self.lv = None
		self.max_voltage = mx_vol
		self.open()
		self.initialize()
		self.enabled = False

	def open(self):
		try:
			self.rm = visa.ResourceManager('@py')
			self.lv = self.rm.open_resource('TCPIP::192.168.1.117::9221::SOCKET') 
			self.lv.Timeout = 5000
			self.lv.read_termination = '\r'
			print('Connected to: ', self.lv.query('*idn?'))
			self.lv.write('*rst')  #default the instrument
		except Exception as e:
			print("Failed to connect to LV supply.\nError: {}".format(e))

	def initialize(self):
		try:
			self.lv.write('OP2 0') #turn channel 1 off
			cmd = 'V2 {}'.format(self.max_voltage)
			self.lv.write(cmd)
			self.lv.write('I2 0.002') #sets current limit
			self.lv.write('OCP2 2') #current protection trip point

			self.lv.write('OP1 0') #turn channel 2 off
			cmd = 'V1 {}'.format(self.max_voltage)
			self.lv.write(cmd)
			self.lv.write('I1 0.002') #sets current limit
			self.lv.write('OCP1 2') #current protection trip point
		except Exception as e:
			print("Failed to initialize LV supply.\nError: {}".format(e))		

	def close(self):
		self.lv.write('OP2 0') #turn channel 1 off
		self.lv.write('OP1 0') #turn channel 2 off
		self.lv.close()
		self.rm = None
		self.lv = None
		print('Connection to low voltage supply closed.')

	def turnChannelOn(self):
		self.lv.write('OP2 1') #turn channel 1 on
		self.lv.write('OP1 1') #turn channel 2 on

	def setCurrent(self, curr1, curr2):
		try:
			self.turnChannelOn()
			cmd = 'I2 {}'.format(curr1)
			self.lv.write(cmd) #changes the current limit
			sleep(0.010)
			cmd = 'I1 {}'.format(curr2)
			self.lv.write(cmd) #changes the current limit
		except Exception as e:
			print("Failed to set current on LV supply.\nError: {}".format(e))

	def getCurrent(self):
		curr1 = self.lv.query('I2O?')
		print(curr1)
		sleep(0.4)
		curr2 = self.lv.query('I1O?')
		print(curr2)


		'''
		curr1 = -1
		curr2 = -1
		try:
			curr1 = self.lv.query('I2O?')
			curr1 = float(curr1.replace('A', ''))
			sleep(0.040)
		except:
			pass
		
		try:
			curr2 = self.lv.query('I1O?')
			curr2 = float(curr2.replace('A', ''))
		except:
			pass

		return [curr1, curr2]
		'''


if __name__ == '__main__':
	lv = LowVoltage(1)
	lv.turnChannelOn()
	lv.setCurrent(0.2, 0.3)
	for i in range(20):
		lv.getCurrent()
		sleep(0.5)
	lv.close()