import serial
from serial.tools import list_ports
import sys
import glob
import time

class SerialComm(object):
    def __init__(self, ftdi_serial = None, baud = None, stop_char = chr(3)) -> None:
        self.ftdi_serial = ftdi_serial
        self.baud = baud
        self.device = None
        self.error = None
        self.ser = None
        self.stop_char = stop_char.encode('utf-8')
        # self.search_dev()
        # self.serial_connect()
        if self.error:
            print(self.error)

    def __del__(self):
        self.serial_disconnect()

    def set_error(self, error):
        self.error = error

    def search_dev(self):
        device = list(list_ports.comports())
        for dev in device:
            if dev.serial_number == self.ftdi_serial:
                #print(f"Serial found: {dev.serial_number} = Serial Expected: {self.ftdi_serial}")
                self.device = dev.device
                break
            else:
                #print(f"Serial found: {dev.serial_number} - Serial Expected: {self.ftdi_serial}")
                self.device = None
        print(self.device)

    def is_open(self):
        if self.ser is not None:
            return self.ser.is_open

    def serial_connect(self):
        if self.device == None:
            self.ser = None
            return
        try:
            self.ser = serial.Serial(self.device, self.baud, bytesize=serial.EIGHTBITS,
                                     parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, xonxoff=False,
                                     rtscts=False, write_timeout=3, dsrdtr=False, inter_byte_timeout=None, exclusive=None, timeout=3)
            print(f"Connected to {self.device}!")
            if not self.is_open():
                self.ser = None
        except Exception as e:
            self.set_error(str(e))
            self.ser = None

    def serial_disconnect(self):
        try:
            self.ser.close()
            print("Disconnected")
        except Exception as e:
            self.set_error(str(e))

    def read_serial(self):
        mes = self.ser.read_until(self.stop_char)
        mes = mes.split(self.stop_char)[0]
        return mes
    
    def read_size(self, size):
        mes = self.ser.read(size)
        return mes
    
    def read_all(self):
        mes = self.ser.read_all()
        return mes

    def write_serial(self, data):
        return self.ser.write(data)

    def empty_input_buffer(self):
        return self.ser.reset_input_buffer()

    def empty_output_buffer(self):
        return self.ser.reset_output_buffer()

    def in_waiting(self):
        return self.ser.in_waiting

    def serial_ports():
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux'):
            ports = glob.glob('/dev/tty[A-Za-z]*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(s)
            except (OSError, serial.SerialException):
                pass
        return result

    def list_ports(self):
        device = list(list_ports.comports())
        return device

# s = SerialComm("A106RGATA", 9600, "\r")
# time.sleep(1)
# if (s.is_open()):
#     print(s.write_serial("#CMD:ADC:R_D:0\r".encode('utf-8')))
#     print("YES")
#     s.serial_disconnect()
# else:
#     print("NO")
