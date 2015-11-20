import RPi.GPIO as GPIO
#import requests

GPIO.setmode(GPIO.BCM)

pin = [0,0,0,0]


number1 = 14
number2 = 15
number3 = 18
number4 = 23
lockerSelector = 24
disparador1 = 27
disparador2 = 22
carrera1 = 10
carrera2 = 9

GPIO.setup(number1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(number2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(number3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(number4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(carrera1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(carrera2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.setup(lockerSelector, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(disparador1, GPIO.OUT)
GPIO.setup(disparador2, GPIO.OUT)

global actualPinPosition
actualPinPosition = 0
global actualLocker
actualLocker = 1


GPIO.output(disparador1, GPIO.HIGH)
GPIO.output(disparador2, GPIO.HIGH)


#puertos del display
d=[2,3,4,7]

#Establece todas las salidas del display
for p in d:
    GPIO.setup(p, GPIO.OUT)

#Muestra en el display el numero seleccionado
def Display(num):
    #Recorre los puertos
    for p in d:
        #asigna HIGH o LOW segun el ultimo termino
        if (num % 2)==1:
            GPIO.output(p, GPIO.HIGH)
        else:
            GPIO.output(p, GPIO.LOW)
        #Corrimiento para proximo valor
        num = num // 2
    return

def number1Pressed(channel):
	global actualPinPosition
	pin[actualPinPosition] = 1
	if(actualPinPosition==3):
		validate()
		actualPinPosition = 0
	else:
		actualPinPosition = actualPinPosition + 1

def number2Pressed(channel):
	global actualPinPosition
	pin[actualPinPosition] = 2
	if(actualPinPosition==3):
		validate()
		actualPinPosition = 0
	else:
		actualPinPosition = actualPinPosition + 1

def number3Pressed(channel):
	global actualPinPosition
	pin[actualPinPosition] = 3
	if(actualPinPosition==3):
		validate()
		actualPinPosition = 0
	else:
		actualPinPosition = actualPinPosition + 1

def number4Pressed(channel):
	global actualPinPosition
	pin[actualPinPosition] = 4
	if(actualPinPosition==3):
		validate()
		actualPinPosition = 0
	else:
		actualPinPosition = actualPinPosition + 1

def lockerSelectorPressed(channel):
	global actualLocker
	if(actualLocker==1):
		actualLocker=2
	else:
		actualLocker=1
	Display(actualLocker)
	actualPinPosition=0

def carrera1Pressed(channel):
	GPIO.output(disparador1, GPIO.HIGH)

def carrera2Pressed(channel):
	GPIO.output(disparador2, GPIO.HIGH)		


def validate():
	#VALIDAR PIN EN EL SERVIDOR
	global pin 
	global actualLocker

	code=0
	for dato in pin:
		code=code*10
		code+=dato
	payload ={
		"pin" : code,
		"lockerCode" : actualLocker,
	}
	r= requests.post("http://159.203.103.193/validatePin.py",data=payload)	
	print code
	if (1 == Int(r.text)):
		if (actualLocker == 1):
			GPIO.output(disparador1, GPIO.LOW)
		else:
			GPIO.output(disparador2, GPIO.LOW)

GPIO.add_event_detect(number1, GPIO.RISING, callback=number1Pressed, bouncetime=300)
GPIO.add_event_detect(number2, GPIO.RISING, callback=number2Pressed, bouncetime=300)
GPIO.add_event_detect(number3, GPIO.RISING, callback=number3Pressed, bouncetime=300)
GPIO.add_event_detect(number4, GPIO.RISING, callback=number4Pressed, bouncetime=300)
GPIO.add_event_detect(lockerSelector, GPIO.RISING, callback=lockerSelectorPressed, bouncetime=300)
GPIO.add_event_detect(carrera1, GPIO.RISING, callback=carrera1Pressed, bouncetime=500)
GPIO.add_event_detect(carrera2, GPIO.RISING, callback=carrera2Pressed, bouncetime=500)

Display(actualLocker)

while(True):
	continue