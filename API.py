import sys
import RPi.GPIO as GPIO
import time
import PID
#import adafruit_mpu6050
#import board
# import GYRO
#from simple_pid import PID



GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
mode=GPIO.getmode()
#pid.sample_time=0.01
#pid.set_point(3.5)
#pid.output_limits=(0,1)

faceWallThreshold = 2
sideWallThreshold = 6

baseSpeed = 80 

PIN_TRIGGER1 = 11
PIN_ECHO1 = 33
PIN_TRIGGER2 = 7
PIN_ECHO2 = 32
PIN_TRIGGER3 = 16
PIN_ECHO3 = 22
PIN_TRIGGER4 = 15
PIN_ECHO4 = 35

start=21
shortestpath=23

GPIO.setup(PIN_TRIGGER1, GPIO.OUT)
GPIO.setup(PIN_ECHO1, GPIO.IN)
GPIO.setup(PIN_TRIGGER2, GPIO.OUT)
GPIO.setup(PIN_ECHO2, GPIO.IN)
GPIO.setup(PIN_TRIGGER3, GPIO.OUT)
GPIO.setup(PIN_ECHO3, GPIO.IN)
GPIO.setup(PIN_TRIGGER4, GPIO.OUT)
GPIO.setup(PIN_ECHO4, GPIO.IN)

GPIO.setup(start, GPIO.IN)
GPIO.setup(shortestpath, GPIO.IN)




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

#GPIO.setmode(GPIO.BOARD)

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

'''
i2c = board.I2C()  # uses board.SCL and board.SDA
mpu = adafruit_mpu6050.MPU6050(i2c)

def getAngle():
    return calc()

def notTurned90(a):    
    return (abs(a-getAngle()) <= 90)

def calc():
    a1,a2=0,0
    angle=initial
    time1 =time.time()
    time2 = time1

    a1=a2
    time1 = time2
    time2 = time.time()
    a2=mpu.gyro[2]
    if -0.1<a2<0.1:
        return 0
    angle+=(180*(time2-time1)*(a1+a2)/(2*3.14))
    #print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (mpu.acceleration))
    #print("Gyro X:%.2f, Y: %.2f, Z: %.2f rad/s" % (mpu.gyro))
    #print("Temperature: %.2f C" % mpu.temperature)
    print("Angle: %.2f degree " %angle)
    time.sleep(0.0001)
    return round(angle,2)
'''
def startUp():
    if (GPIO.input(start)==1):
        return True
    
def reset():
    if (GPIO.input(shortestpath)==1):
        return True

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
    initialtime=time.time()
    while GPIO.input(PIN_ECHO1)==0:
        #pass
        pulse1_start_time = time.time()
        if (pulse1_start_time - initialtime > 0.005):
            break
    while GPIO.input(PIN_ECHO1)==1:
        pulse1_end_time = time.time()
        
    # Calculate Distance
    try:
        return round((pulse1_end_time - pulse1_start_time) * 17150, 2)
    except:
        return False       
    
def getDistance2():
    
    # Set trigger high
    GPIO.output(PIN_TRIGGER2, GPIO.HIGH)
    time.sleep(0.00001)
    # Set trigger low
    GPIO.output(PIN_TRIGGER2, GPIO.LOW)
    time.sleep(0.00001)
    
    # Measure time
    initialtime=time.time()
    while GPIO.input(PIN_ECHO2)==0:
        #pass
        pulse2_start_time = time.time()
        if (pulse2_start_time - initialtime > 0.005):
            break
    while GPIO.input(PIN_ECHO2)==1:
        pulse2_end_time = time.time()
        
    # Calculate Distance
    try:
        return round((pulse2_end_time - pulse2_start_time) * 17150, 2)
    except:
        return False

def getDistance3():
    
    # Set trigger high
    GPIO.output(PIN_TRIGGER3, GPIO.HIGH)
    time.sleep(0.00001)
    # Set trigger low
    GPIO.output(PIN_TRIGGER3, GPIO.LOW)
    time.sleep(0.00001)
    
    # Measure time
    initialtime=time.time()
    while GPIO.input(PIN_ECHO3)==0:
        #pass
        pulse3_start_time = time.time()
        if (pulse3_start_time - initialtime > 0.005):
            break
    while GPIO.input(PIN_ECHO3)==1:
        pulse3_end_time = time.time()
        
    # Calculate Distance
    try:
        return round((pulse3_end_time - pulse3_start_time) * 17150, 2)
    except:
        return False
    
def getDistance4():
    
    # Set trigger high
    GPIO.output(PIN_TRIGGER4, GPIO.HIGH)
    time.sleep(0.00001)
    # Set trigger low
    GPIO.output(PIN_TRIGGER4, GPIO.LOW)
    time.sleep(0.00001)
    
    # Measure time
    initialtime=time.time()
    while GPIO.input(PIN_ECHO4)==0:
        #pass
        pulse4_start_time = time.time()
        if (pulse4_start_time - initialtime > 0.005):
            break
    while GPIO.input(PIN_ECHO4)==1:
        pulse4_end_time = time.time()
        
    # Calculate Distance
    try:
        return round((pulse4_end_time - pulse4_start_time) * 17150, 2)
    except:
        return False

def wallFront():
    dis=getDistance1()
    while(getDistance1()==False):
        dis=getDistance1()
    if (dis < faceWallThreshold):
        return True
    return False

def wallRight():
    dis=getDistance3()
    while(getDistance3()==False):
        dis=getDistance3()
    if (dis < sideWallThreshold):
        return True
    return False

def wallLeft():
    dis=getDistance2()
    while(getDistance2()==False):
        dis=getDistance2()
    if (dis < faceWallThreshold):
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

def pause1(initial):
    while(True):
        if((initial-getDistance1())>=15):
            break
    
def pause2():
    #prev=10
    while(True):
        if(getDistance1()<=2): #or prev<=1.5):
            break
        #prev=getDistance1()

def moveForward():
    log("moveforward");

    #correction=keepStraight()
    initialDistance=getDistance1()
    #error = getDistance2() - getDistance3()
    
    #Uncomment above if does not work
    dist2 = getDistance2()
    if dist2 > 7:
        dist2 = 7
    dist3 = getDistance3()
    if dist3 > 7:
        dist3 = 7
    
    error = dist2 - dist3
    #
    
    leftSpeed, rightSpeed = PID.pid_controller(error)
    
    GPIO.output(DIR1,GPIO.HIGH)
    GPIO.output(DIR2,GPIO.LOW)
    GPIO.output(DIR3,GPIO.HIGH)
    GPIO.output(DIR4,GPIO.LOW)
    GPIO.output(DIR5,GPIO.HIGH)
    GPIO.output(DIR6,GPIO.LOW)
    GPIO.output(DIR7,GPIO.HIGH)
    GPIO.output(DIR8,GPIO.LOW)

    if(getDistance1()>16):
        pwm1.start(leftSpeed)#baseSpeed+correction)
        pwm2.start(rightSpeed)#baseSpeed-correction)
        pwm3.start(leftSpeed)#baseSpeed+correction)
        pwm4.start(rightSpeed)#baseSpeed-correction)    
    else:
        
        pwm1.start(30)#baseSpeed+correction)
        pwm2.start(30)#baseSpeed-correction)
        pwm3.start(30)#baseSpeed+correction)
        pwm4.start(30)#baseSpeed-correction)  
        time.sleep(0.02)
        print("forward")
        
    if(getDistance1()>16):
        pause1(initialDistance)
    else:
        pause2()
    #pause(initialDistance)
    #time.sleep(0.5)
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

def turnRight(duration=0.23):
    
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
    
    #time.sleep(duration)
    #holt(1)
    '''
    initialAngle = getAngle()

    while notTurned90(initialAngle):
        time.sleep(0.01)'''
      
def turnLeft(duration=0.23): #0.25 #0.315
  
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
    '''
    initialAngle = gyrooooo.getAngle()

    while gyrooooo.notTurned90(initialAngle):
        time.sleep(0.01)
    '''

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
