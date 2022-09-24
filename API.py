import sys
import RPi.GPIO as GPIO
import time
import PID
#from simple_pid import PID

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
mode=GPIO.getmode()
#pid.sample_time=0.01
#pid.set_point(3.5)
#pid.output_limits=(0,1)

faceWallThreshold = 1.5
sideWallThreshold = 7

baseSpeed = 80

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


DIR1=38; #FLB
DIR2=40; #FLF
DIR3=36; #FRB
DIR4=37; #FRF
DIR5=31; #config
DIR6=29; #config
DIR7=26; #config
DIR8=24; #config
PWM1=13; #M1 Front Left
PWM2=19; #M2 Front Right
PWM3=12; #M3 Back Left
PWM4=18; #M4 Back Right

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

time.sleep(1)

pwm1 = GPIO.PWM(PWM1,1000)
pwm2 = GPIO.PWM(PWM2,1000)
pwm3 = GPIO.PWM(PWM3,1000)
pwm4 = GPIO.PWM(PWM4,1000)

'''
orients :
    0- North
    1- East
    2- South
    3- West
'''

errorDif=0
totalError=0
prevError=0
Kp=1
Ki=0.5
Kd=0.5

def keepStraight():
    global totalError
    global prevError
    leftValue=getDistance2()
    rightValue=getDistance3()
    error=rightValue-3.5
    totalError+=error
    errorDif=error-prevError
    prevError=error
    total=(Kp*error)+(Ki*totalError)+(Kd*errorDif)
    return total

def orientation(orient,turning):
    if (turning== 'L'):
        orient-=1
        if (orient==-1):
            orient=3
    elif(turning== 'R'):
        orient+=1
        if (orient==4):
            orient=0
    elif(turning== 'B'):
        if (orient==0):
            orient=2
        elif (orient==1):
            orient=3
        elif (orient==2):
            orient=0
        elif (orient==3):
            orient=1

    return(orient)

def updateCoordinates(x,y,orient):

    if (orient==0):
        y+=1
    if (orient==1):
        x+=1
    if (orient==2):
        y-=1
    if (orient==3):
        x-=1

    return(x,y)



class MouseCrashedError(Exception):
    pass

def command(args, return_type=None):
    line = " ".join([str(x) for x in args]) + "\n"
    sys.stdout.write(line)
    sys.stdout.flush()
    if return_type:
        response = sys.stdin.readline().strip()
        if return_type == bool:
            return response == "true"
        return return_type(response)

def mazeWidth():
    return command(args=["mazeWidth"], return_type=int)

def mazeHeight():
    return command(args=["mazeHeight"], return_type=int)

#def wallFront():
#    return command(args=["wallFront"], return_type=bool)

#def wallRight():
#    return command(args=["wallRight"], return_type=bool)

#def wallLeft():
#    return command(args=["wallLeft"], return_type=bool)

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

def wallFront():

    if (getDistance1() < faceWallThreshold):
        return True
    return False

def wallRight():

    if (getDistance3() < sideWallThreshold):
        return True
    return False

def wallLeft():

    if (getDistance2() < sideWallThreshold):
        return True
    return False

#def moveForward():
#    response = command(args=["moveForward"], return_type=str)

#    if response == "crash":
#        #log(str(cells[y][x]))
#        raise MouseCrashedError()

def holt(duration):
    
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

    time.sleep(duration)

'''def moveBackward():
    
    duration = 0.2
    
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

    time.sleep(duration)
    holt(1)'''

def pause(initial):
    while(True):
        if((initial-getDistance1())>=11):
            break

def moveForward():
    log("moveforward");

    duration = 0.299
    #correction=keepStraight()
    initialDistance=getDistance1()
    dist2 = getDistance2()
    if (dist2 > 7):
        dist = 3.5
    dist3 = getDistance3()
    if (dist3 > 7):
        dist = 3.5
    error = dist2 - dist3
    leftSpeed, rightSpeed = PID.pid_controller(error)
    
    GPIO.output(DIR1,GPIO.HIGH)
    GPIO.output(DIR2,GPIO.LOW)
    GPIO.output(DIR3,GPIO.HIGH)
    GPIO.output(DIR4,GPIO.LOW)
    GPIO.output(DIR5,GPIO.HIGH)
    GPIO.output(DIR6,GPIO.LOW)
    GPIO.output(DIR7,GPIO.HIGH)
    GPIO.output(DIR8,GPIO.LOW)

    pwm1.start(leftSpeed)#baseSpeed+correction)
    pwm2.start(rightSpeed)#baseSpeed-correction)
    pwm3.start(leftSpeed)#baseSpeed+correction)
    pwm4.start(rightSpeed)#baseSpeed-correction)

    #pause(initialDistance)
    time.sleep(0.5)
    holt(1)
    '''if((getDistance2()-getDistance3())>1):
        turnLeft(0.02)
    elif((getDistance2()-getDistance3())<-1):
        turnRight(0.02)
    elif((getDistance2()-getDistance3())>1.5):
        turnLeft(0.03)
    elif((getDistance2()-getDistance3())<-1.5):
        turnRight(0.03)
    elif((getDistance2()-getDistance3())>2):
        turnLeft(0.04)
    elif((getDistance2()-getDistance3())<-2):
        turnRight(0.04)'''

#def turnRight():
#    command(args=["turnRight"], return_type=str)

#def turnLeft():
#    command(args=["turnLeft"], return_type=str)

def turnRight(duration=0.25):
    
    GPIO.output(DIR1,GPIO.HIGH)
    GPIO.output(DIR2,GPIO.LOW)
    GPIO.output(DIR3,GPIO.LOW)
    GPIO.output(DIR4,GPIO.HIGH)
    GPIO.output(DIR5,GPIO.HIGH)
    GPIO.output(DIR6,GPIO.LOW)
    GPIO.output(DIR7,GPIO.LOW)
    GPIO.output(DIR8,GPIO.HIGH)
    
    pwm1.start(baseSpeed)
    pwm2.start(baseSpeed)
    pwm3.start(baseSpeed)
    pwm4.start(baseSpeed)
    
    time.sleep(duration)
    holt(1)
    #initialAngle = getAngle()

    #while notTurned90(initialAngle):
      #  time.sleep(0.01)
      
def turnLeft(duration=0.235): #0.25
  
    GPIO.output(DIR1,GPIO.LOW)
    GPIO.output(DIR2,GPIO.HIGH)
    GPIO.output(DIR3,GPIO.HIGH)
    GPIO.output(DIR4,GPIO.LOW)
    GPIO.output(DIR5,GPIO.LOW)
    GPIO.output(DIR6,GPIO.HIGH)
    GPIO.output(DIR7,GPIO.HIGH)
    GPIO.output(DIR8,GPIO.LOW)
    
    pwm1.start(baseSpeed)
    pwm2.start(baseSpeed)
    pwm3.start(baseSpeed)
    pwm4.start(baseSpeed)

    time.sleep(duration)
    holt(1)
    #initialAngle = getAngle()

    #while notTurned90(initialAngle):
     #   time.sleep(0.01)

def setWall(x, y, direction):
    command(args=["setWall", x, y, direction])

def clearWall(x, y, direction):
    command(args=["clearWall", x, y, direction])

def setColor(x, y, color):
    command(args=["setColor", x, y, color])

def clearColor(x, y):
    command(args=["clearColor", x, y])

def clearAllColor():
    command(args=["clearAllColor"])

def setText(x, y, text):
    command(args=["setText", x, y, text])

def clearText(x, y):
    command(args=["clearText", x, y])

def clearAllText():
    command(args=["clearAllText"])

def wasReset():
    return command(args=["wasReset"], return_type=bool)

def ackReset():
    command(args=["ackReset"], return_type=str)

def log(string):
    sys.stderr.write("{}\n".format(string))

