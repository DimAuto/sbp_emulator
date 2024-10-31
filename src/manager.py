# from keyboard import Keyboard
from threading import Thread, Lock
import time
import os
from queue import Queue

class Transmitter(object):
    def __init__(self, serial,messager) -> None:
        super(Transmitter, self).__init__(messager)
        self.message ={"stx": 0, "protocol_rev": [], "token": 0, "senderID":[], "cmd":0,
                        "data":[], "checksum":[], "etx":0 }
        self.TOKEN = 0
        self.cmd = 0
        self.data = []
        # self.data_tmp = []
        self.checksum = [0x00,0x00,0x00,0x00]
        self.serial = serial
        self.senderID = 0x32
        self.data_dict = {"86": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], "128":[48,48,48,48,48,48], "112": [0,0],
                     "114": [0,0], "116":[0], "81":[0], "51":1}

    def set_tx_cmd(self, cmd):
        self.cmd = int(cmd)
    
    def construct_message(self):
        self.data = self.data_dict.get(str(self.cmd))
        self.message["stx"] = 2
        self.message["protocol_rev"] = [254, 1]
        self.message["token"] = self.TOKEN
        self.message["senderID"] = [7, self.senderID]
        self.message["cmd"] = self.cmd
        self.message["data"] = self.data_dict.get(str(self.cmd))
        self.message["checksum"] = self.checksum
        self.message["etx"] = 3

    def calc_checksum_tx(self):
        if self.TOKEN >= 255:
            self.TOKEN = 0
        else:
            self.TOKEN += 1
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

    def send_message(self):
        message = []
        for i in self.message:
            if type(self.message[i]) is list:
                for j in self.message[i]:
                    if j in [2,3,27]:
                        message.append(27)
                    message.append(j)
            else:
                if self.message[i] in [2,3,27] and i not in ["stx", "etx"]:
                    message.append(27)
                message.append(self.message[i])
        self.messager.signal.emit(f"Trasmitted message : {message}")
        message = bytes(message)
        self.serial.write_serial(message)
    
class Receiver(object):

    def __init__(self,messager) -> None:
        super(Receiver, self).__init__()
        self.message_rx ={"stx": 0, "protocol_rev": [], "token": 0, "senderID":[], "cmd":0,
                       "data":[], "checksum":[], "etx":0 }
        self.checksum_rx = [0x00,0x00,0x00,0x00]
        self.bsl_flag = False
        self.TOKEN_RX = 0
        self.messager = messager

        
    def parse(self, message):
        self.message_rx["stx"] = message[0]
        self.message_rx["protocol_rev"] = message[1:3]
        self.message_rx["token"] = message[3]
        self.message_rx["senderID"] = message[4:6]
        self.message_rx["cmd"] = message[6]
        self.message_rx["data"] = message[7:-5]
        self.message_rx["checksum"] = message[-5:-1]
        self.message_rx["etx"] = message[-1]
        self.TOKEN_RX = int(self.message.get("token"))

    def calc_checksum(self):
        checksum = 0
        checksum ^= self.message_rx.get("protocol_rev")[0]
        checksum ^= self.message_rx.get("protocol_rev")[1]
        checksum ^= self.message_rx.get("token")
        checksum ^= self.message_rx.get("senderID")[0]
        checksum ^= self.message_rx.get("senderID")[1]
        checksum ^= self.message_rx.get("cmd")
        data = self.message_rx.get("data")
        for i in range(0,len(data)):
            checksum ^= data[i]
        self.checksum_rx[3] = checksum
        # print(f"Calculated CHECKSUM = {self.checksum} - received = {self.message.get('checksum')}")
        if self.checksum_rx== self.message_rx.get("checksum"):
            return True
        else:
            return False
        
    def send_ACK(self):
        mess = bytes([6,self.TOKEN_RX])
        # print(mess)
        self.serial.write_serial(mess)

    def send_NACK(self):
        mess = bytes([15,self.TOKEN_RX])
        # print(mess)
        self.serial.write_serial(mess)


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
        self.messager = messager  #messager class
        self.messager.killsignal.connect(self.set_killflag)
        self.messager.data_tx.connect(self.set_transmitter_data)
        self.messager.reply_scan.connect(self.set_scan_enable)
        self.messager.send_hb.connect(self.set_hb_enable)
        self.messager.reply_voltage.connect(self.set_voltage_enable)
        self.messager.reply_GPS_location.connect(self.set_gps_coor_enable)
        self.messager.reply_GPS_clock.connect(self.set_gps_clock_enable)
        self.messager.master_enable.connect(self.set_master_enable)
        self.killflag = 0
        self.tx_enabled = False
        self.hb_timeout = 0
        self.tx_th_lock = False
        self.master_enable = True
        # DATA FIELD ENABLE FLAGS  
        self.scan_enabled = False
        self.hb_enabled = False
        self.voltage_req_cmd = [112, 114, 116]
        self.gps_loc_req_cmd = [86]
        self.gps_clock_req_cmd = [128]
        self.enabled_cmds = []
        #QUEUE
        self.queue = Queue(maxsize=14)
        self.ack_queue = Queue(maxsize=3)
        #THREADING
        self.mutex = Lock()
        self.read_thread = Thread(target=self.read_serial,args=[])
        self.read_thread.start()
        self.write_thread = Thread(target=self.transmit, args=[])
        self.write_thread.start()
        self.hb_thread = Thread(target=self.hb_transmit, args=[])
        self.hb_thread.start()

    def set_master_enable(self, val:bool):
        self.master_enable = val
    
    def set_scan_enable(self, val:bool):
        self.scan_enabled = val

    def set_hb_enable(self, val:bool):
        self.hb_enabled = val

    def set_voltage_enable(self, val:bool):
        if val == True:
            self.enabled_cmds += self.voltage_req_cmd
            self.messager.signal.emit("Voltage transmit enabled")
        else:
            self.enabled_cmds = [x for x in self.enabled_cmds if x not in self.voltage_req_cmd]
            self.messager.signal.emit("Voltage transmit disabled")

    def set_gps_coor_enable(self, val:bool):
        if val == True:
            self.enabled_cmds += self.gps_loc_req_cmd
            self.messager.signal.emit("GPS coors enabled")
        else:
            self.enabled_cmds = [x for x in self.enabled_cmds if x not in self.gps_loc_req_cmd]
            self.messager.signal.emit("GPS coors disabled")

    def set_gps_clock_enable(self, val:bool):
        if val == True:
            self.enabled_cmds += self.gps_clock_req_cmd
            self.messager.signal.emit("GPS clock enabled")
        else:
            self.enabled_cmds = [x for x in self.enabled_cmds if x not in self.gps_clock_req_cmd]  
            self.messager.signal.emit("GPS clock disabled")      

    def thread_watch(self):
        while 1:
            if (self.read_thread.is_alive() == False):
                self.read_thread.start()

    def set_max_repeats(self, max_repeats):
        self.max_repeats = max_repeats

    def set_killflag(self, val):
        self.killflag = val

    def set_transmitter_data(self,val:dict):
        self.data_dict = val

    def proccess_packet(self):
        if self.packet[0] in ["06", "15"]:
                if self.packet[1] != "1b":
                    try:
                        self.ack_queue.put([self.packet[1], self.packet[0]], block=False)
                    except Queue.Full:
                        self.ack_queue.empty()
                        self.ack_queue.put([self.packet[1], self.packet[0]], block=False)

                    self.packet = self.packet[2:]
                else:
                    try:
                        self.ack_queue.put([self.packet[2], self.packet[0]], block=False)
                    except Queue.Full:
                        self.ack_queue.empty()
                        self.ack_queue.put([self.packet[2], self.packet[0]], block=False)
                    self.packet = self.packet[3:] 
        if self.packet[0] != '02':
            try:
                index = self.packet.index('02')
                self.packet = self.packet[index::]   
            except:
                self.packet = []
                return
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
                # self.messager.signal.emit(f"Received Message = {self.message_rx}")
                if self.calc_checksum() == True and self.master_enable == True:
                    self.mutex.acquire()
                    self.send_ACK()
                    self.mutex.release()
                    self.queue.put(self.message_rx.get("cmd"))
                elif self.calc_checksum() == False and self.master_enable == True:
                    self.mutex.acquire()
                    self.send_NACK()
                    self.mutex.release()
                    self.messager.signal.emit(f"Invalid checksum")
            except Exception as e:
                self.messager.signal.emit(f"Failed to parse message: {str(e)} - {self.payload}")
            finally:
                self.packet = []
  
    def read_serial(self):
        while (self.killflag == 0):
            if self.serial.in_waiting() > 1:
                r =  bytes.hex(self.serial.read_serial(), " ")
                r = r.split(" ")
                # print(r)
                if (r[-1] == "03" and r[-2] != "1b"):
                    self.packet += r
                    self.proccess_packet()
                else:
                    # if r[0] in ["06", "15"]:
                    #     if len(r) < 3:
                    #         try:
                    #             self.ack_queue.put([r[1], r[0]], block=False)
                    #         except Queue.Full:
                    #             self.ack_queue.empty()
                    #             self.ack_queue.put([r[1], r[0]], block=False)
                    #     else:
                    #         try:
                    #             self.ack_queue.put([r[2], r[0]], block=False) 
                    #         except Queue.Full:
                    #             self.ack_queue.empty()
                    #             self.ack_queue.put([r[2], r[0]], block=False)
                    # else:
                        # if "03" in r[-4::]:
                        #     index = r.index("03")
                        #     if r[index-1] == "1b":
                        #         self.packet = r[0:index+1]
                        #         self.proccess_packet()
                    self.packet += r
                self.repeats+=1  
            self.payload = []

            
    def transmit(self):
        while (self.killflag == 0):
            if self.queue.qsize != 0:
                cmd = self.queue.get() 
                if cmd == 80:
                    self.tx_enabled = True
                    self.messager.signal.emit("Received SCAN")
                else:
                    # if self.tx_enabled == True:
                    if cmd in self.enabled_cmds:
                        try:
                            self.set_tx_cmd(cmd)
                            self.construct_message()
                            self.calc_checksum_tx()
                            self.mutex.acquire()
                            self.send_message()

                            self.mutex.release()

                            if self.ack_queue.qsize() > 0:
                                ack_resp = []
                                ack_resp = self.ack_queue.get()
                            # print(ack_resp)
                        except Exception as e:
                            print(f"Exception: {str(e)}")


    def hb_transmit(self):
        # curr_token = 0
        while(self.killflag == 0):
            if self.hb_enabled == True and self.master_enable == True:
                self.set_tx_cmd(81)
                try:
                    self.construct_message()
                    curr_token = self.TOKEN
                    self.calc_checksum_tx()
                    self.mutex.acquire()
                    self.send_message()
                    self.mutex.release()
                except Exception as e:
                    print(str(e))

                timeout = time.time()
                ack_resp = []
                # while(1):
                if self.ack_queue.qsize() > 0:
                    ack_resp = self.ack_queue.get()
                    # print(ack_resp)
                #         if ack_resp[0] == curr_token:
                #             if ack_resp[1] == "06":
                #                 self.hb_timeout = 0
                #                 break
                #             else:
                #                 self.hb_timeout += 1
                #                 break
                #     if time.time() - timeout > 0.50:
                #         self.hb_timeout += 1
                #         break
                # if self.hb_timeout > 3:
                #     self.tx_enabled = False
                #     self.messager.signal.emit(f"Disconnected from master")
                time.sleep(self.data_dict.get("51"))


