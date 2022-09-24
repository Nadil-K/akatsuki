previousError, cumError = 0, 0
base_speed = 25
max_change = 25

p = -0.6 #-0.6
i = 0.01 #0.001
d = -0.35 #-0.35
# Works when the robot is initially centered

def pid_controller(error):
    global previousError, cumError
    # error is left distance - right distance

    cumError += error
    rateError = (error - previousError)
    previousError = error
    print("Error : %.2f  Cum Error : %.2f  Rate Error : %.2f" %
          (error, cumError, rateError))

    change = p * error + i * cumError + d * rateError
    if change > max_change:
        change = max_change
    elif change < -1 * max_change:
        change = -1 * max_change

    leftSpeed = base_speed + (5*change)
    if (leftSpeed > 100):
        leftSpeed = 100
    elif (leftSpeed < 0):
        leftSpeed = 0
    rightSpeed = base_speed - (5*change)
    if (rightSpeed > 100):
        rightSpeed = 100
    elif (rightSpeed < 0):
        rightSpeed = 0
        
    print(leftSpeed, rightSpeed)
    return leftSpeed, rightSpeed
