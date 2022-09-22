import sys
import RPi.GPIO as GPIO
import time

faceWallThreshold = 30
sideWallThreshold = 50

GPIO.setmode(GPIO.BOARD)

# Configure Pins
PIN_TRIGGER1 = 7
PIN_ECHO1 = 11
PIN_TRIGGER2 = 7
PIN_ECHO2 = 11
PIN_TRIGGER3 = 7
PIN_ECHO3 = 11
PIN_TRIGGER4 = 7
PIN_ECHO4 = 11

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

def getDistance():

    # Set trigger high
    GPIO.output(PIN_TRIGGER1, GPIO.HIGH)
    GPIO.output(PIN_TRIGGER2, GPIO.HIGH)
    GPIO.output(PIN_TRIGGER3, GPIO.HIGH)
    GPIO.output(PIN_TRIGGER4, GPIO.HIGH)

    time.sleep(0.00001)

    # Set trigger low
    GPIO.output(PIN_TRIGGER1, GPIO.LOW)
    GPIO.output(PIN_TRIGGER2, GPIO.LOW)
    GPIO.output(PIN_TRIGGER3, GPIO.LOW)
    GPIO.output(PIN_TRIGGER4, GPIO.LOW)

    # Measure time
    while GPIO.input(PIN_ECHO1)==0:
        pulse1_start_time = time.time()
    while GPIO.input(PIN_ECHO1)==1:
        pulse1_end_time = time.time()

    while GPIO.input(PIN_ECHO2)==0:
        pulse2_start_time = time.time()
    while GPIO.input(PIN_ECHO2)==1:
        pulse2_end_time = time.time()

    while GPIO.input(PIN_ECHO3)==0:
        pulse3_start_time = time.time()
    while GPIO.input(PIN_ECHO3)==1:
        pulse3_end_time = time.time()

    while GPIO.input(PIN_ECHO4)==0:
        pulse4_start_time = time.time()
    while GPIO.input(PIN_ECHO4)==1:
        pulse4_end_time = time.time()


    # Calculate Distance
    distance1 = round((pulse1_end_time - pulse1_start_time) * 17150, 2)
    distance2 = round((pulse2_end_time - pulse2_start_time) * 17150, 2)
    distance3 = round((pulse3_end_time - pulse3_start_time) * 17150, 2)
    distance4 = round((pulse4_end_time - pulse4_start_time) * 17150, 2)

    print "Distance:",distance1,"cm", checkfaceWall(distance1)
    print "Distance:",distance2,"cm", checksideWall(distance2)
    print "Distance:",distance3,"cm", checksideWall(distance3)
    print "Distance:",distance4,"cm", checkfaceWall(distance4)

GPIO.cleanup()