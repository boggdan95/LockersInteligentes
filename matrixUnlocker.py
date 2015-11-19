import RPi.GPIO as GPIO
import requests
import time #necesario para los delays

GPIO.setmode(GPIO.BCM)

pin = [0,0,0,0]


number1 = 14
number2 = 15
number3 = 18
number4 = 23
lockerSelector = 24

carrera1 = 10
carrera2 = 9

GPIO.setup(number1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(number2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(number3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(number4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(carrera1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(carrera2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.setup(lockerSelector, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

global estado1
estado1="abierto"
global estado2
estado2="abierto"

global actualPinPosition
actualPinPosition = 0
global actualLocker
actualLocker = 1

#==================
# SERVOS
#==================

servo1=22
GPIO.setup(servo1,GPIO.OUT)
s1 = GPIO.PWM(servo1, 50)

servo2=27
GPIO.setup(servo2,GPIO.OUT)
s2 = GPIO.PWM(servo2, 50)

abierto = 1
cerrado = 2

ms = 1000/50

def dutyCicle(pos):
    return pos *100/ms

s1.start(abierto)
time.sleep(0.5)
s1.stop()
s2.start(abierto)
time.sleep(0.5)
s2.stop()

def cerrar(n):
    
    global estado1
    global estado2
    
    servo1=22
    GPIO.setup(servo1,GPIO.OUT)
    s1 = GPIO.PWM(servo1, 50)

    servo2=27
    GPIO.setup(servo2,GPIO.OUT)
    s2 = GPIO.PWM(servo2, 50)
    
    duty = dutyCicle (cerrado)
    if (n==1):
        print "cerrar 1"
        s1.start(duty)
        s1.ChangeDutyCycle(duty)
        time.sleep(0.5)
        s1.stop()
        estado1="cerrado"
        
    if (n==2):
        print "cerrar 2"
        s2.start(duty)
        s2.ChangeDutyCycle(duty)
        time.sleep(0.5)
        s2.stop()
        estado2="cerrado"

    global actualPinPosition
    actualPinPosition = 0
    
    return

def abrir(n):

    global estado1
    global estado2
    
    servo1=22
    GPIO.setup(servo1,GPIO.OUT)
    s1 = GPIO.PWM(servo1, 50)

    servo2=27
    GPIO.setup(servo2,GPIO.OUT)
    s2 = GPIO.PWM(servo2, 50)
    
    duty = dutyCicle (abierto)
    if (n==1):
        print "abrir 1"
        s1.start(duty)
        s1.ChangeDutyCycle(duty)
        time.sleep(0.5)
        s1.stop()
        estado1="abierto"
        
    if (n==2):
        print "abrir 2"
        s2.start(duty)
        s2.ChangeDutyCycle(duty)
        time.sleep(0.5)
        s2.stop()
        estado2="abierto"

    global actualPinPosition
    actualPinPosition = 0
    
    return


#==================
# DISPLAY
#==================

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

global ejecucion
ejecucion=False

def carrera1Pressed(channel):
        global estado1
        global ejecucion
        if (estado1=="abierto" and ejecucion == False):
            ejecucion=True
            time.sleep(0.5)
            cerrar(1)
            print "carrera1 presionado"
            ejecucion=False
                       

def carrera2Pressed(channel):
        global estado2
        global ejecucion
	if (estado2=="abierto" and ejecucion == False):
            ejecucion=True
            time.sleep(0.5)
            cerrar(2)		
            print "carrera2 presionado"
            ejecucion=False		


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
			abrir(1)
		else:
			abrir(2)

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
