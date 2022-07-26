
from periphery import GPIO
from time import sleep
import signal
import sys
from datetime import datetime

#__________EMAIL 
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
#_________________________________

flag = True
#______________PIN INIT      _____________________
#REMOTE PIN
R_A = GPIO(2, "in") #23
R_B = GPIO(4, "in") #19
R_C = GPIO(1, "in") #27
R_D = GPIO(3, "in") #21
#LED
Alarm_LED = GPIO(101, "out")    #16
Status_LED = GPIO(121, "out") #18
#flame
flame = GPIO(5, "in") #24
#sound
sound = GPIO(122, "in") #29
#motion
motion = GPIO(56, "in") #7
#relay
relay = GPIO(123, "out") #31
#GAS
gas = GPIO(124, "in") #33
#buzzer
buz = GPIO(125, "out") #35
#_____________________________________________________
def handler(signal, frame): #for exit event
  global flag
  print('goodbye')
  R_A.close()
  R_B.close()
  gas.close()
  motion.close()
  Alarm_LED.close()
  Status_LED.close()
  flag = False

#___CONFIG 
Time4WaitAfterDetect = 3 # sec wait befor ALARM
Time4BUZAfterDetect = 4 # second turn on buzzer AND alarm_LED
Time4BUZAFterDetectGAS = 10
Time4BUZAFterDetectNOISE = 5
Time4BUZAFterDetectFLAME = 15

now2 = datetime.now()
TimeToTurnOnLight =  now2.replace(hour=21 , minute=0)
TimeToTurnOffLight = now2.replace(hour=22 , minute=30)

#_______________________________
def SendMain(ImgFileName , alert) :
	#if(ImgFileName==null) return #
	img_data = open(ImgFileName, 'rb').read()
	msg = MIMEMultipart()
	msg['Subject'] = 'Alert Notification: ' + alert + ' Detected! ' # Subject of message
	msg['From'] = '####@blackrainbow.pro' # from who
	msg['To'] = 'Reciver@example.com' # to who 

	text = MIMEText("A suspicious motion/flame detected! Alert from your Home Security System!") # text of message
	msg.attach(text)
	image = MIMEImage(img_data, name=os.path.basename(ImgFileName))
	msg.attach(image)

	s = smtplib.SMTP('#mailServer.blackrainbow.pro', #PORT ) # email server info , name and port ( 587)
	s.ehlo()
	s.starttls()
	s.ehlo()
	s.login('####@blackrainbow.pro', '#PASWORD#') # login information
	s.sendmail(msg['From'], msg['To'], msg.as_string())
	s.quit()
#_______________________________

signal.signal(signal.SIGINT, handler) 
#_____________________________________________________
relay.write(True) # relays turned off by +5V 
while flag:
	
	#read remote signals
	V_A = R_A.read()
	V_B = R_B.read()
	V_C = R_C.read()
	V_D = R_D.read()
	
	motion_flag = True
	gas_flag    = False
	noise_flag  = False
	flame_flag  = False
	
	#____AAAAA
	if(V_A) :
		if(not V_A) :
			now2 = datetime.now()
			print("LOG : TURN OF ALARM IN : " + now2.strftime("%H:%M"))
		Alarm_LED.write(False)
		print("A turn")
		Alarm_LED.write(True)
		Status_LED.write(True)
		buz.write(True)
		sleep(2)
		Alarm_LED.write(False)
		#Status_LED.write(False)
		buz.write(False)
		print("burglar alarm activated\n")
		while(not V_D) :
			V_A=False
			V_D = R_D.read() # turn of alarms with B button
			motion_flag = motion.read()
			if(motion_flag):
				print("motion detected")
				#take picture
				SendMain("motion.jpg", "motion")
				#call to owner
				
				#__LOW BUZ
				buz.write(True)
				Alarm_LED.write(True)
				sleep(0.4)
				buz.write(False)
				sleep(1)
				buz.write(True)
				sleep(1.5)
				buz.write(False)
				Alarm_LED.write(False)
				V_B = R_B.read() # turn off alarms with B button
				sleep(0.5)
				#_________
				
				sleep(Time4WaitAfterDetect)
				Alarm_LED.write(True)
				Status_LED.write(False)
				buz.write(True)
				sleep(Time4BUZAfterDetect)
				buz.write(False)
				Alarm_LED.write(False)
				Status_LED.write(True)
				sleep(1)
				print("motion detected -> END of action")
			#_END OF MOTION DETECTOR
			gas_flag    = gas.read()
			if(not gas_flag):
				print("GAS detected")
				#take picture
				#email picture
				#call to owner
				SendMain("gas.jpg", "gas")
				#__LOW BUZ
				buz.write(True)
				Alarm_LED.write(True)
				sleep(0.4)
				buz.write(False)
				sleep(1)
				buz.write(True)
				sleep(1.5)
				buz.write(False)
				Alarm_LED.write(False)
				V_B = R_B.read() # turn off alarms with B button
				sleep(0.5)
				#_________
				
				sleep(1)#one second wait and turn on alarm
				Alarm_LED.write(True)
				Status_LED.write(False)
				buz.write(True)
				sleep(Time4BUZAFterDetectGAS)
				buz.write(False)
				Alarm_LED.write(False)
				Status_LED.write(True)
				sleep(1)
				print("GAS detected -> END of action")
			#_END OF GAS DETECTOR
			noise_flag  = sound.read()
			if(not noise_flag):
				print("NOISE detected")
				#take picture
				#email pictire
				#call to owner
				
				#__LOW BUZ
				buz.write(True)
				Alarm_LED.write(True)
				sleep(0.1)
				buz.write(False)
				sleep(2)
				buz.write(True)
				sleep(2)
				buz.write(False)
				Alarm_LED.write(False)
				V_B = R_B.read() # turn off alarms with B button
				sleep(0.5)
				#_________
				
				sleep(2)#second wait and turn on alarm
				Alarm_LED.write(True)
				Status_LED.write(False)
				buz.write(True)
				sleep(Time4BUZAFterDetectNOISE)
				buz.write(False)
				Alarm_LED.write(False)
				Status_LED.write(True)
				sleep(1)
				print("NOISE detected -> END of action")
			#_END OF NOISE DETECTOR
			flame_flag  = flame.read()
			if(not flame_flag):
				print("FLAME detected")
				#take picture
				#email pictire
				#call to owner
				SendMain("motion.jpg", "flame")
				#__LOW BUZ
				buz.write(True)
				Alarm_LED.write(True)
				sleep(0.1)
				buz.write(False)
				sleep(0.5)
				buz.write(True)
				sleep(4)
				buz.write(False)
				Alarm_LED.write(False)
				V_B = R_B.read() # turn off alarms with B button
				sleep(0.5)
				#_________
				
				sleep(0.01)# second wait and turn on alarm
				Alarm_LED.write(True)
				Status_LED.write(False)
				buz.write(True)
				sleep(Time4BUZAFterDetectFLAME)
				buz.write(False)
				Alarm_LED.write(False)
				Status_LED.write(True)
				sleep(1)
				print("FLAME detected -> END of action")
			#_END OF FLAME DETECTOR
			
			# time to turn on relay ( lamp )
			now = datetime.now()
			current_time = now.strftime("%H:%M") 
			if(now > TimeToTurnOnLight and now < TimeToTurnOffLight) : 
				relay.write(False)
				#print("turn on relay : " + current_time)
			else:
				#print("turn OFF relay : " + current_time)
				relay.write(True)  # TURN OFF RELAY NOW
			
		V_B = R_B.read() # turn of alarms with B button	
		#END WHILE 
		
	#____AAAAA
	
	#____BBBBBB
	if(V_B) :
		#flame and gas sensor is on 
		print("B turn")
		V_B=False
		V_C=False
		buz.write(True)
		sleep(0.5)
		buz.write(False)
		V_D = False
		Status_LED.write(True)
		while(not V_D ) :
			V_D = R_D.read() # read D key for stop and change status
			sleep(0.01)
			gas_flag = gas.read()
			if(not gas_flag):
				print("GAS detected")
				#take picture
				#email pictire
				#call to owner
				SendMain("gas.jpg", "gas_B_MODE_")
				#__LOW BUZ
				buz.write(True)
				Alarm_LED.write(True)
				sleep(0.4)
				buz.write(False)
				sleep(1)
				buz.write(True)
				sleep(1.5)
				buz.write(False)
				Alarm_LED.write(False)
				V_B = R_B.read() # turn off alarms with B button
				sleep(0.5)
				#_________
				sleep(1)#one second wait and turn on alarm
				Alarm_LED.write(True)
				Status_LED.write(False)
				buz.write(True)
				sleep(Time4BUZAFterDetectGAS)
				buz.write(False)
				Alarm_LED.write(False)
				Status_LED.write(True)
				sleep(1)
				print("GAS detected -> END of action")
			#_END OF GAS DETECTOR
			
			flame_flag  = flame.read()
			if(not flame_flag):
				print("B FLAME detected")
				#take picture
				#email pictire
				#call to owner
				
				#__LOW BUZ
				buz.write(True)
				Alarm_LED.write(True)
				sleep(0.1)
				buz.write(False)
				sleep(0.5)
				buz.write(True)
				sleep(4)
				buz.write(False)
				Alarm_LED.write(False)
				V_B = R_B.read() # turn off alarms with B button
				sleep(0.5)
				#_________
				
				sleep(0.01)# second wait and turn on alarm
				Alarm_LED.write(True)
				Status_LED.write(False)
				buz.write(True)
				sleep(Time4BUZAFterDetectFLAME)
				buz.write(False)
				Alarm_LED.write(False)
				Status_LED.write(True)
				sleep(1)
				print("B FLAME detected -> END of action")
			#_END OF FLAME DETECTOR
			
			motion_flag = motion.read() # turn on lights when wome thing move
			if(motion_flag):
				relay.write(False)
				sleep(20)
				relay.write(True)
			
		#end of B while
			
	#____BBBBBB	
	
	if(V_C) :
		print("C turn")
		V_C=False
		buz.write(True)
		sleep(0.5)
		buz.write(False)
		Status_LED.write(True)
		sleep(2)
		Status_LED.write(False)
		relay.write(False)
		sleep(7)
		relay.write(True)
		# take picture
		# send mail
		# call to owner
		
	if(V_D) : # TURN OFF SYSTEM
		print("D turn")
		buz.write(True)
		sleep(0.5)
		buz.write(False)
		D_flag = True
		while(D_flag) :
			V_A = R_A.read()
			V_B = R_B.read()
			V_C = R_C.read()
			sleep(0.1)
			if(V_A):
				D_flag = False
				print("D_A")
			if(V_B):
				D_flag = False
				print("D_B")
			if(V_C):
				D_flag = False
				print("D_C")
			Status_LED.write(True)
			sleep(0.15)
			Status_LED.write(False)
			
	#end of while

#_functions


