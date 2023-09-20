#!/usr/bin/env python
# -*- coding: utf-8 -*-

#to import modules
import paho.mqtt.client as mqtt
import RPi.GPIO as gpio

in1 = 24
in2 = 23
en = 25
temp1=1

def gpioSetup():
	gpio.setmode(gpio.BCM)
	gpio.setup(21, gpio.OUT)
	


    

def connectionStatus(client, userdata, flags, rc):
	mqttClient.subscribe("rpi/gpio")

def messageDecoder(client, userdata, msg):
	message = msg.payload.decode(encoding='UTF-8')
	
	if message == "on":
		open_door()
		#gpio.output(in1,gpio.HIGH)
		#gpio.output(in2,gpio.LOW)
		#temp1=1
		#x='z'
		print("Door OPEN!")
		
	elif message == "off":
		gpio.output(21, gpio.LOW)
		print("LED is OFF!")
	else:
		print("Unknown message!")
        



#set up RPI gpio pins
gpioSetup()

def open_door():
    ''' function to open Mail box door '''
    #new part
    gpio.output(21, gpio.OUT)
    gpio.output(in1,gpio.LOW)
    gpio.output(in2,gpio.HIGH)
    

    temp1=0
    x='z'
        #end of new part
    #motor_on(pin)
    #time.sleep(4.8)
    #motor_off(pin)
   
    #print('Hey! Open Sesame!!')
    
    
def close_door():
    ''' function to close Mail box door '''
    #TODO: Fugure out revere motor control
    #new part
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)

    temp1=1
    x='z'
        #end of new part
    #motor_on(pin)
    #time.sleep(4.8)
    #motor_off(pin)
   
    #print('Hey! Close Sesame!!')

#set client name
clientName = "RPI"

#MQTT server ip
serverAddress = "192.168.6.170"

#Ecplise as mqttClient
mqttClient = mqtt.Client(clientName)

#set calling func to mqtt client 
mqttClient.on_connect = connectionStatus
mqttClient.on_message = messageDecoder


#connect to client server
mqttClient.connect(serverAddress)

#Monitor Client activity forever
mqttClient.loop_forever()




