# DTI Motors API Wiki
## Introduction
For the motion control of DTI motors in Closed-Loop mode, an additional
daughter board is mounted on the driver PCB. Feedback from an external optical
encoder is fed to the daughter board and used to close the loop.  The position
and speed of the motor can them be controlled through a set of serial commands
that access pre-programmed motion control algorithms.

The algorithms are optimized on the specific dynamic characteristics of the
motor.  The algorithms also analyze encoder feedback and preform real-time
noise filtration.

The DTI Motor API provides access to these commands using the following
functions.

### Motor Class Definition
#### PiezoMotor()
The motor first need to be instantiated as python class.  The PiezoMotor class
take one of two options; "Linear" or "Rotary"

        #DTI Linear motor
        motor1 = PiezoMotor("Linear")

        #DTI Rotary motor1
        motor2 = PiezoMotor("Rotary")

### Driver board connection
Once the instance is created the motor driver board need to be located and
connected using serial.tools.list_ports which is available form https://pyserial.readthedocs.io/en/latest/pyserial.html
#### MotorSearch()
This function searches for active serial port connection.

        motor1.MotorSearch()
        motor2.MotorSearch()

#### ConnectToBoard()
This function opens the serial communication.

        a = Motor1.ConnectToBoard(1)
        b = Motor2.ConnectToBoard(2)

### Motor commands
**SetVelocity(velocity)**
<br>Set Velocity - This command is used to set the motor velocity.  The velocity
is entered as RPM and has a range of 0.01 - 100 RPMs.  The velocity over the
entire range is controlled internally by the driver board and uses four separate
algorithms to optimize and stabilize the required velocity.

        #Set speed to 60 RPMs
        motor1.SetVelocity(60)
        motor2.SetVelocity(60)

**Destination(direction, position)**
<br>Set Destination - This command moves and positions the motor to a specific
location.  Movement is entered as specific pulses from the encoder; where the
resolution of the encoder is equal to 40.5 arc.sec.  
Movement direction is
specified using the keywords:  Right or Clockwise rotation 'R', Left of Counter
Clockwise rotation 'L'.

        #Move 1000 pulses to the left
        Motor1.Destination('L',1000)

        #Rotate 1000 pulses Clockwise
        Motor2.Destination('R',1000)

**BrakingDistance(pulses)**
<br>Breaking Distance - This command is used to program the breaking
distance before reaching the target coordinate. Normally, it is placed before
the “Destination” operator. The users need to enter the breaking distance
(in pulses).  
This operator improves accuracy of positioning, when approaching target
coordinate. It provides the flexibility of changing the braking distance,
depending on the load. This function helps to eliminate unwanted effects, like
target “overshooting” and “hunting” mode, which are typical for servo systems
based on electromagnetic motors.

        #Set breaking distance to help eliminate overshooting
        Motor1.BrakingDistance(500)
        Motor2.BrakingDistance(500)

**MoveTime(direction, milliseconds)**
<br>Move Time - This operator is used for programming a specified time of
movement with speed defined by Set Velocity operator placed before this
operator. The user needs to specify the direction of movement and enter the
movement time in milliseconds. The  direction is specified using the
keywords:  Right or Clockwise rotation 'R', Left or Counter Clockwise
rotation 'L'.

        #Moves the motor for 100 milliseconds
        Motor1.MoveTime('R', 100)
        Motor2.MoveTime('L', 100)

**Home(direction)**
<br>Home - This operator is for the Linear motor series only!
This operation is used to move the linear motor to the extreme edge of the
travel range.  The direction is specified using the keywords:  Right 'R' or
Left 'L'.

        #Moves the motor from it current position to the far left position
        Motor1.Home('L')
