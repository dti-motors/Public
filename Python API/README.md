# DTI Motors API Wiki
## Introduction
For the motion control of DTI motors in Closed-Loop mode, and additional
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
