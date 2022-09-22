import sys
import time
import RPi.GPIO as GPIO

mode=GPIO.getmode()

GPIO.cleanup()

baseSpeed = 100

DIR1=21; //FLB
DIR2=20; //FLF
DIR3=16; //FRB
DIR4=26; //FRF
DIR5=6; //config
DIR6=5; //config
DIR7=7; //config
DIR8=8; //config
PWM1=13; //M1
PWM2=19; //M2
PWM3=12; //M3
PWM4=18; //M4

GPIO.setmode(GPIO.BOARD)

GPIO.setup(DIR1,GPIO.OUT)
GPIO.setup(DIR2,GPIO.OUT)
GPIO.setup(DIR3,GPIO.OUT)
GPIO.setup(DIR4,GPIO.OUT)
GPIO.setup(DIR5,GPIO.OUT)
GPIO.setup(DIR6,GPIO.OUT)
GPIO.setup(DIR7,GPIO.OUT)
GPIO.setup(DIR8,GPIO.OUT)
GPIO.setup(PWM1,GPIO.OUT)
GPIO.setup(PWM3,GPIO.OUT)
GPIO.setup(PWM2,GPIO.OUT)
GPIO.setup(PWM4,GPIO.OUT)

sleep(1)

pwm1 = GPIO.PWM(PWM1,1000)
pwm2 = GPIO.PWM(PWM2,1000)
pwm3 = GPIO.PWM(PWM3,1000)
pwm4 = GPIO.PWM(PWM4,1000)

def turn_right(baseSpeed):
    
    GPIO.output(DIR1,GPIO.HIGH)
    GPIO.output(DIR2,GPIO.LOW)
    GPIO.output(DIR3,GPIO.LOW)
    GPIO.output(DIR4,GPIO.HIGH)
    GPIO.output(DIR5,GPIO.LOW)
    GPIO.output(DIR6,GPIO.HIGH)
    GPIO.output(DIR7,GPIO.HIGH)
    GPIO.output(DIR8,GPIO.LOW)
    
    pwm1.start(baseSpeed)
    pwm2.start(baseSpeed)
    pwm3.start(baseSpeed)
    pwm4.start(baseSpeed)

    initialAngle = getAngle()

    while notTurned90(initialAngle):
        sleep(0.01)

def turn_left(baseSpeed):
  
    GPIO.output(DIR1,GPIO.LOW)
    GPIO.output(DIR2,GPIO.HIGH)
    GPIO.output(DIR3,GPIO.HIGH)
    GPIO.output(DIR4,GPIO.LOW)
    GPIO.output(DIR5,GPIO.HIGH)
    GPIO.output(DIR6,GPIO.LOW)
    GPIO.output(DIR7,GPIO.LOW)
    GPIO.output(DIR8,GPIO.HIGH)
    
    pwm1.start(baseSpeed)
    pwm2.start(baseSpeed)
    pwm3.start(baseSpeed)
    pwm4.start(baseSpeed)

    initialAngle = getAngle()

    while notTurned90(initialAngle):
        sleep(0.01)

def go_forward(baseSpeed, duration):

    GPIO.output(DIR1,GPIO.LOW)
    GPIO.output(DIR2,GPIO.HIGH)
    GPIO.output(DIR3,GPIO.LOW)
    GPIO.output(DIR4,GPIO.HIGH)
    GPIO.output(DIR5,GPIO.LOW)
    GPIO.output(DIR6,GPIO.HIGH)
    GPIO.output(DIR7,GPIO.LOW)
    GPIO.output(DIR8,GPIO.HIGH)
    
    pwm1.start(baseSpeed)
    pwm2.start(baseSpeed)
    pwm3.start(baseSpeed)
    pwm4.start(baseSpeed)

    sleep(duration)

def go_backward(baseSpeed, duration):

    GPIO.output(DIR1,GPIO.HIGH)
    GPIO.output(DIR2,GPIO.LOW)
    GPIO.output(DIR3,GPIO.HIGH)
    GPIO.output(DIR4,GPIO.LOW)
    GPIO.output(DIR5,GPIO.HIGH)
    GPIO.output(DIR6,GPIO.LOW)
    GPIO.output(DIR7,GPIO.HIGH)
    GPIO.output(DIR8,GPIO.LOW)

    pwm1.start(baseSpeed)
    pwm2.start(baseSpeed)
    pwm3.start(baseSpeed)
    pwm4.start(baseSpeed)

    sleep(duration)

def holt(baseSpeed, duration):

    GPIO.output(DIR1,GPIO.LOW)
    GPIO.output(DIR2,GPIO.LOW)
    GPIO.output(DIR3,GPIO.LOW)
    GPIO.output(DIR4,GPIO.LOW)
    GPIO.output(DIR5,GPIO.LOW)
    GPIO.output(DIR6,GPIO.LOW)
    GPIO.output(DIR7,GPIO.LOW)
    GPIO.output(DIR8,GPIO.LOW)

    pwm1.start(baseSpeed)
    pwm2.start(baseSpeed)
    pwm3.start(baseSpeed)
    pwm4.start(baseSpeed)

    sleep(duration)

while (1):

go_forward(baseSpeed,5)
holt(baseSpeed,5)

GPIO.cleanup()