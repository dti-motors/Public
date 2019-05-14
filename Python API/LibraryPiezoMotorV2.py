import serial
import serial.tools.list_ports
import time

class PiezoMotor:

    def __init__(self, motor_type):
        self.id = None
        self.motor_type = motor_type
        self.ser = serial.Serial(
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
        )

    def motor_search(self):
        # TODO
        pass

    def set_id(self, target_id):
        self.id = target_id

    def connect(self):

        if self.ser.is_open:
            self.ser.close()

        self.ser.list_ports = list(serial.tools.list_ports.comports())
        for port in self.ser.list_ports:
            if 'CP210' in port.description:
                print('Found device: ')
                print(port.device)
                self.ser.port = port.device
                self.ser.open()
                #data = self.__send_and_receive(b'\x01')
                #print(data)
                #Data=int.from_bytes(data,byteorder='little')
                #print(Data)

    def set_velocity(self, velocity, timeout=0):
        if self.motor_type == "Linear":
            velocity = round(velocity * 100 / 1.4)
        else:
            velocity = round(velocity * 100)

        data = bytearray([5, 3, 3]) + velocity.to_bytes(2, byteorder="little")
        return self.__send_and_receive(data, timeout)

    def braking_distance(self, value, timeout=0):
        if self.motor_type == "Linear":
            value = round(value / 2.6)

        data = bytearray([5, 3, 9]) + value.to_bytes(2, byteorder="little")
        return self.__send_and_receive(data, timeout)

    def destination(self, direction, position, timeout=0):
        dir = 0
        if direction == 'R':
            dir = 1
        elif direction == 'L':
            dir = 0
        else:
            print('Wrong direction command')
            return -1

        if self.motor_type == 'Linear':
            position = round(position/2.6)

        data = bytearray([5, 5, 6, dir]) + int(position).to_bytes(3, byteorder="little")
        return self.__send_and_receive(data, timeout)

    def move_time(self, direction, time_val, timeout=0):
        dir = 0
        if direction == 'R':
            dir = 1
        elif direction == 'L':
            dir = 0
        else:
            print('Wrong direction command')
            return -1

        data = bytearray([5, 6, 1, dir]) + time_val.to_bytes(4, byteorder="little")
        return self.__send_and_receive(data, timeout)

    def pause(self, time):

        data = bytearray([5, 5, 2]) + time.to_bytes(4, byteorder="little")

        self.__send(data)
        return self.read()

    def __send(self, data_to_send):
        if not self.ser.is_open:
            print('Serial port is not open')
            return -1
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()
        try:
            self.ser.write(data_to_send)
        except:
            print('Send Error')
            return -1
        return 0

    def __send_and_receive(self, data_to_send, timeout):
        data = -1
        if not self.ser.is_open:
            print('Serial port is not open')
            return -1
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()
        try:
            self.ser.write(data_to_send)
        except:
            print('Send Error')
            return -1

        response = 0
        start_time = time.time()
        while response != b'\x07':

            response = self.read()

            if timeout > 0:
                if time.time() - start_time > timeout:
                    print('Timeout occured while waitind response from device')
                    return -1

        return 0

    def read(self):
        if not self.ser.is_open:
            print('Serial port is not open')
            return -1
        data = 0

        try:
            data = self.ser.read(1)
        except:
            print('Read Error')
            return -1
        return data

    def __del__(self):
        print('Closing the port')
        self.ser.close()
