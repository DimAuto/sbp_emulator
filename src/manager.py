# from keyboard import Keyboard
from threading import Thread
import time
import os

class Transmitter(object):
    def __init__(self, serial,messager) -> None:
        super(Transmitter, self).__init__(messager)
        self.message ={"stx": 0, "protocol_rev": [], "token": 0, "senderID":[], "cmd":0,
                        "data":[], "checksum":[], "etx":0 }
        self.TOKEN = 0
        self.cmd = 0
        self.data = []
        self.data_tmp = []
        self.checksum = [0x00,0x00,0x00,0x00]
        self.serial = serial
        self.senderID = 49

    def set_tx_data(self,data):
        self.data = data
        self.data_tmp = data

    def set_tx_cmd(self, cmd):
        self.cmd = cmd
    
    def construct_message(self):
        if self.TOKEN >= 255:
            self.TOKEN = 0
        self.message["stx"] = 2
        self.message["protocol_rev"] = [254, 1]
        self.message["token"] = self.TOKEN
        self.message["senderID"] = [7, self.senderID]
        self.message["cmd"] = self.cmd
        self.message["data"] = self.data_tmp
        self.message["checksum"] = self.checksum
        self.message["etx"] = 3

    def calc_checksum_tx(self):
        checksum = 0
        checksum ^= self.message.get("protocol_rev")[0]
        checksum ^= self.message.get("protocol_rev")[1]
        checksum ^= self.message.get("token")
        checksum ^= self.message.get("senderID")[0]
        checksum ^= self.message.get("senderID")[1]
        checksum ^= self.message.get("cmd")
        data = self.message.get("data")
        for i in range(0,len(data)):
            checksum ^= data[i]
        self.checksum[3] = checksum
        #print("CHECKSUM:", checksum)

    def data_add_esc(self):
        list = []
        for i in range (0,len(self.data)):
            if self.data[i] in [2,3,27]:
                list.append(27)
                list.append(self.data[i])
            else:
                list.append(self.data[i])
        self.data_tmp = list

    def send_message(self):
        message = []
        for i in self.message:
            if type(self.message[i]) is list:
                for j in self.message[i]:
                    message.append(j)
            else:
                if (i=="token"):
                    if (self.message[i] == 3) or (self.message[i] == 27) or (self.message[i] == 2):
                        message.append(27)
                message.append(self.message[i])
        self.TOKEN += 1
        print(f"Trasmitted message : {message}")
        message = bytes(message)
        
        self.serial.write_serial(message)
        # print(message)
    
class Receiver(object):

    def __init__(self,messager) -> None:
        super(Receiver, self).__init__()
        self.message ={"stx": 0, "protocol_rev": [], "token": 0, "senderID":[], "cmd":0,
                       "data":[], "checksum":[], "etx":0 }
        self.payload = []
        self.checksum = [0x00,0x00,0x00,0x00]
        self.bsl_flag = False
        self.messager = messager

        
    def parse(self, message):
        self.message["stx"] = message[0]
        self.message["protocol_rev"] = message[1:3]
        self.message["token"] = message[3]
        self.message["senderID"] = message[4:6]
        self.message["cmd"] = message[6]
        self.message["data"] = message[7:-5]
        self.message["checksum"] = message[-5:-1]
        self.message["etx"] = message[-1]

    def calc_checksum(self):
        checksum = 0
        checksum ^= self.message.get("protocol_rev")[0]
        checksum ^= self.message.get("protocol_rev")[1]
        checksum ^= self.message.get("token")
        checksum ^= self.message.get("senderID")[0]
        checksum ^= self.message.get("senderID")[1]
        checksum ^= self.message.get("cmd")
        data = self.message.get("data")
        for i in range(0,len(data)):
            checksum ^= data[i]
        self.checksum[3] = checksum
        # print(f"Calculated CHECKSUM = {checksum}")

    def get_message_rx(self):
        return self.message
    
    def parse_command(self):
        if self.message["cmd"] == 112:
            # battery voltage
            data = self.message.get("data")
            batt = (((data[0] << 8) | data[1]) / 4095)
            # print("\n--------------------------------------------")
            self.messager.signal.emit(f"Battery voltage = {batt}")
            # print("--------------------------------------------\n")
        elif self.message["cmd"] == 114:
            # external_v
            data = self.message.get("data")
            ext = (((data[0] << 8) | data[1]) / 4095)
           #print("\n--------------------------------------------")
            self.messager.signal.emit(f"External voltage = {ext}")
            #print("--------------------------------------------\n")
        elif self.message["cmd"] == 129:
            # nyx_consumption
            data = self.message.get("data")
            ext = (((data[0] << 8) | data[1]) / 4095)
           # print("\n--------------------------------------------")
            self.messager.signal.emit(f"NYX Consumption = {ext}")
           # print("--------------------------------------------\n")
        elif self.message["cmd"] == 116:
            # power line
            data = self.message.get("data")
            if data[0] == 0:
                device = "Battery"
            else:
                device = "External"
            #print("\n--------------------------------------------")
            self.messager.signal.emit(f"Power Line selected :{device}")
            #print("--------------------------------------------\n")

        elif self.message["cmd"] == 81:
            #print("\n--------------------------------------------")
            self.messager.signal.emit(f"HEARTBEAT")
            #print("--------------------------------------------\n")

        elif self.message["cmd"] == 130:
            data = self.message.get("data")
            if data[0] == 0:
                device = "NYX FLIPPED DOWN"
            else:
                device = "NYX FLIPPED UP"
           # print("\n--------------------------------------------")
            self.messager.signal.emit(f"Power Line selected :{device}")

        elif self.message["cmd"] == 86:
            # ublox
            data = self.message.get("data")
            # if all(i==0 for i in data):
            #     self.messager.signal.emit(f"GPS Coors: Lat = {0}, Long = {0}, alt = {0}")
            lat =  ((data[0] << 24) | (data[1] << 16) | (data[2] << 8) | (data[3])) / 200000
            long = ((data[4] << 24) | (data[5] << 16) | (data[6] << 8) | (data[7])) / 200000
            alt =  ((data[8] << 24) | (data[9] << 16) | (data[10] << 8) | (data[11])) / 200000
            hAcc = ((data[12] << 24) | (data[13] << 16) | (data[14] << 8) | (data[15])) / 200000
            #print("\n--------------------------------------------")
            self.messager.signal.emit(f"GPS Coors: Lat = {lat}, Long = {long}, alt = {alt}, hAcc = {hAcc}")
            #print("--------------------------------------------\n")

        elif self.message["cmd"] == 87:
            #magnetometer
            data = self.message.get("data")
            mgn_x = ((data[0] << 8) | data[1])
            mgn_y = ((data[2] << 8) | data[3])
            mgn_z = ((data[4] << 8) | data[5])
            #print("\n--------------------------------------------")
            self.messager.signal.emit(f"Magnetometer data: X: {mgn_x}, Y: {mgn_y}, Z: {mgn_z}")
            #print("--------------------------------------------\n")
        elif self.message["cmd"] == 88:
            #accel
            data = self.message.get("data")
            acc_x = ((data[0] << 8) | data[1])
            acc_y = ((data[2] << 8) | data[3])
            acc_z = ((data[4] << 8) | data[5])
            #print("\n--------------------------------------------")
            self.messager.signal.emit(f"Accelerometer data: X: {acc_x}, Y: {acc_y}, Z: {acc_z}")
            #print("--------------------------------------------\n")
        elif self.message["cmd"] == 101:
            #FW version
            data = self.message.get("data")
            #print("\n--------------------------------------------")
            data = [chr(i) for i in data]
            self.messager.signal.emit(f"FW_version: {"".join(data)}")
            #print("--------------------------------------------\n")

        elif self.message["cmd"] == 144:
            data = self.message.get("data")
            self.messager.signal.emit(f"Ublox Power Mode: {str(data)}")

        elif self.message["cmd"] == 128:
            data = self.message.get("data")
            self.messager.signal.emit(f"RTC: {[chr(d) for d in data]}")

        elif self.message["cmd"] == 132:
            data = self.message.get("data")
            self.messager.signal.emit(f"GNSS Quality: {str(data)}")

class Handler(Transmitter, Receiver):
    def __init__(self, serial, messager) -> None:
        super(Handler,self).__init__(serial, messager)
        self.serial = serial
        self.payload = []
        self.packet = []
        self.special_chars = ["02","03","1b"]
        self.received_flag = False
        self.repeats = 0
        self.max_repeats = 0
        self.repeat_interval = 0
        self.messager = messager
        self.messager.killsignal.connect(self.set_killflag)
        self.killflag = 0
        self.stop_tx_flag = False
        self.tx_th_lock = False
        self.read_thread = Thread(target=self.read_serial,args=[])
        self.read_thread.start()
        # self.thread_watch()
        
    def thread_watch(self):
        while 1:
            if (self.read_thread.is_alive() == False):
                self.read_thread.start()

    def set_max_repeats(self, max_repeats):
        self.max_repeats = max_repeats

    def set_repeat_interval(self, interval):
        self.repeat_interval = interval

    def set_killflag(self, val):
        self.killflag = val

   
    def read_serial(self):
        while (self.killflag == 0):
            if self.serial.in_waiting() > 1:
                time.sleep(0.005)
                r =  bytes.hex(self.serial.read_all(), " ")
                r = r.split(" ")
                # print(r)
                if r[0] == "5b" or r[1] == "5b":
                    buff = []
                    for t in r:
                        buff.append(chr(int(t,16)))
                        if (t == "0a"):
                            text = "".join(buff)
                            self.messager.signal.emit(f"|Debug|: {text}")
                            buff = []
                else:
                    if (r[-1] == "03" and r[-2] != "1b"):
                        self.packet = r
                        # print(f"Initial packet: {self.packet}")
                        if self.packet[0] in ["06", "15"]:
                            if self.packet[0] == "06":
                                self.messager.signal.emit("| ACK |")
                            elif self.packet[0] == "15":
                                self.messager.signal.emit("| NACK |")
                            if self.packet[1] == "1b":
                                self.packet = self.packet[3:]
                            else:
                                self.packet = self.packet[2:]
                        # print(f"Packet: {self.packet}")
                        try:
                            for i in range(0,len(self.packet)):
                                if self.packet[i] == "1b" and self.packet[i+1] in self.special_chars:
                                    pass
                                else:
                                    self.payload.append(ord(chr(int(self.packet[i], 16))))
                        except Exception as e:
                            print (str(e))                          
                        if self.payload != []:
                            try:
                                self.parse(self.payload)
                                self.messager.signal.emit(f"Received Message = {self.message}")
                                self.calc_checksum()
                                self.parse_command()
                            except Exception as e:
                                self.messager.signal.emit(f"Failed to parse message: {str(e)}")
                            finally:
                                # print("send")
                                mess = bytes([6,self.TOKEN])
                                self.serial.write_serial(mess)
                                self.packet = []
                    else:
                        self.packet = self.packet + r
                self.repeats+=1  
            self.payload = []

    def repeated_tx_start(self):
        if self.tx_th_lock ==True:
            return
        Thread(target=self.repeated_tx,args=[]).start()

    def transmit_message(self):
        self.construct_message()
        self.calc_checksum_tx()
        self.data_add_esc()
        self.construct_message()
        self.send_message() 

    def repeated_tx(self):
        print("Start repeated TX")
        for i in range(0,self.max_repeats):
            if self.stop_tx_flag == True:
                break
            self.transmit_message()
            time.sleep(self.repeat_interval)
        self.tx_th_lock = False
        self.stop_tx_flag = False
            
    # def transmit(self):
    #     kb = Keyboard()
    #     while (self.received_flag == False):
    #         self.construct_message()
    #         self.calc_checksum_tx()
    #         self.data_add_esc()
    #         self.construct_message()
    #         self.send_message()
    #         if self.repeats > self.max_repeats:
    #             break
    #         if kb.kbhit():
    #             c = kb.getch()
    #             if ord(c) == 27: # ESC
    #                 print(c)
    #                 break
    #         time.sleep(self.repeat_interval)
    #     os._exit(-1)

    # def listen(self):
    #     kb = Keyboard()
    #     while 1:
    #         if kb.kbhit():
    #             c = kb.getch()
    #             if ord(c) == 27: # ESC
    #                 print(c)
    #                 break
    #         time.sleep(0.5)

    


