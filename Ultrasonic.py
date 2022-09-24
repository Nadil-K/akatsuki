import sys
import RPi.GPIO as GPIO
import time

faceWallThreshold = 30
sideWallThreshold = 50

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

# Configure Pins
PIN_TRIGGER1 = 11
PIN_ECHO1 = 33
PIN_TRIGGER2 = 7
PIN_ECHO2 = 32
PIN_TRIGGER3 = 16
PIN_ECHO3 = 22
PIN_TRIGGER4 = 15
PIN_ECHO4 = 35


GPIO.setup(PIN_TRIGGER1, GPIO.OUT)
GPIO.setup(PIN_ECHO1, GPIO.IN)
GPIO.setup(PIN_TRIGGER2, GPIO.OUT)
GPIO.setup(PIN_ECHO2, GPIO.IN)
GPIO.setup(PIN_TRIGGER3, GPIO.OUT)
GPIO.setup(PIN_ECHO3, GPIO.IN)
GPIO.setup(PIN_TRIGGER4, GPIO.OUT)
GPIO.setup(PIN_ECHO4, GPIO.IN)

    #   GPIO.output(PIN_TRIGGER, GPIO.LOW)

    #   print "Waiting for sensor to settle"

    #   time.sleep(2)

    #   print "Calculating distance"
    
def checkFaceWall(distance):

    if (distance < faceWallThreshold):
        return True
    return False
        
def checkSideWall(distance):

    if (distance < sideWallThreshold):
        return True
    return False

def getDistance1():

    # Set trigger high
    GPIO.output(PIN_TRIGGER1, GPIO.HIGH)
    time.sleep(0.00001)
    # Set trigger low
    GPIO.output(PIN_TRIGGER1, GPIO.LOW)
    time.sleep(0.00001)
    
    # Measure time
    while GPIO.input(PIN_ECHO1)==0:
        pulse1_start_time = time.time()
    while GPIO.input(PIN_ECHO1)==1:
        pulse1_end_time = time.time()
        

    # Calculate Distance
    return round((pulse1_end_time - pulse1_start_time) * 17150, 2)        
    
def getDistance2():
    
    # Set trigger high
    GPIO.output(PIN_TRIGGER2, GPIO.HIGH)
    time.sleep(0.00001)
    # Set trigger low
    GPIO.output(PIN_TRIGGER2, GPIO.LOW)
    time.sleep(0.00001)
    
    # Measure time
    while GPIO.input(PIN_ECHO2)==0:
        pulse2_start_time = time.time()
    while GPIO.input(PIN_ECHO2)==1:
        pulse2_end_time = time.time()
        

    # Calculate Distance
    return round((pulse2_end_time - pulse2_start_time) * 17150, 2)

def getDistance3():
    
    # Set trigger high
    GPIO.output(PIN_TRIGGER3, GPIO.HIGH)
    time.sleep(0.00001)
    # Set trigger low
    GPIO.output(PIN_TRIGGER3, GPIO.LOW)
    time.sleep(0.00001)
    
    # Measure time
    while GPIO.input(PIN_ECHO3)==0:
        pulse3_start_time = time.time()
    while GPIO.input(PIN_ECHO3)==1:
        pulse3_end_time = time.time()
        

    # Calculate Distance
    return round((pulse3_end_time - pulse3_start_time) * 17150, 2)
    
def getDistance4():
    
    # Set trigger high
    GPIO.output(PIN_TRIGGER4, GPIO.HIGH)
    time.sleep(0.00001)
    # Set trigger low
    GPIO.output(PIN_TRIGGER4, GPIO.LOW)
    time.sleep(0.00001)
    
    # Measure time
    while GPIO.input(PIN_ECHO4)==0:
        pulse4_start_time = time.time()
    while GPIO.input(PIN_ECHO4)==1:
        pulse4_end_time = time.time()
        

    # Calculate Distance
    return round((pulse4_end_time - pulse4_start_time) * 17150, 2)

while (True):
    distance1 = getDistance1()
    distance2 = getDistance2()
    distance3 = getDistance3()
    distance4 = getDistance4()

    print("Top:",distance1,"cm", checkFaceWall(distance1))
    print("Left:",distance2,"cm", checkSideWall(distance2))
    print("Right:",distance3,"cm", checkSideWall(distance3))
    print("Back:",distance4,"cm", checkFaceWall(distance4))
    time.sleep(0.1)    

GPIO.cleanup()
