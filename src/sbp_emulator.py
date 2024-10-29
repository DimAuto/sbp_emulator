
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication
from manager import Handler
import time


class Ui_Form(object):

    def __init__(self, ser, messager) -> None:
        self.manager = None
        self.messager = messager
        self.repeats = 1
        self.interval = 1
        self.cmd = 0
        self.data = []
        self.serial = ser
        self.ports = []
        self.serial_baud = 115200
        self.baud_list = ["9600", "19200", "115200", "921600"]

        self.commands = {"Heartbeat": 0x50, "GNSS_Coors": 0x56, "GNSS_Clock": 0x80, 
                        "Battery_V": 0x70, "External_V": 0x72, "Selected_PLine": 0x74,
                        "GetFW_Ver": 0x65, "Flip_Flag": 0x82}

        self.command_list = ["0x50", "0x56", "0x57", "0x58", "0x70", "0x65", "0x62", "0x72", 
                             "0x74", "0x78", "0x80", "0x81", "0x82", "0x84", "0x90", "0xA0","0xA1",
                             "0xC0", "0xC1", "0xC2", "0xC3", "0xB0", "0xB1", "0xB2", "0xD1", "0xD2"]
        self.messager.signal.connect(self.set_message)
        self.connected_flag = False
        self.stop_tx_flag = False

        self.blocks = {}

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1114, 870)
        self.gridLayout_6 = QtWidgets.QGridLayout(Form)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.verticalWidget = QtWidgets.QWidget(Form)
        self.verticalWidget.setObjectName("verticalWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtWidgets.QPushButton(self.verticalWidget)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.pressed.connect(self.scan_ports)
        self.horizontalLayout.addWidget(self.pushButton)
        self.comboBox_2 = QtWidgets.QComboBox(self.verticalWidget)
        self.comboBox_2.setObjectName("comboBox_2")
        self.horizontalLayout.addWidget(self.comboBox_2)
        self.comboBox_7 = QtWidgets.QComboBox(self.verticalWidget)
        self.comboBox_7.setObjectName("comboBox_7")
        self.comboBox_7.currentIndexChanged.connect(self.set_baud)
        self.horizontalLayout.addWidget(self.comboBox_7)
        self.pushButton_2 = QtWidgets.QPushButton(self.verticalWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.pressed.connect(self.connect_toPort)
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.checkBox_6 = QtWidgets.QCheckBox(self.verticalWidget)
        self.checkBox_6.setMaximumSize(QtCore.QSize(300, 16777215))
        self.checkBox_6.setObjectName("checkBox_6")
        self.horizontalLayout.addWidget(self.checkBox_6)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_4 = QtWidgets.QLabel(self.verticalWidget)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 0, 0, 1, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.verticalWidget)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout_2.addWidget(self.lineEdit_2, 1, 1, 1, 1)
        self.checkBox_2 = QtWidgets.QCheckBox(self.verticalWidget)
        self.checkBox_2.setObjectName("checkBox_2")
        self.gridLayout_2.addWidget(self.checkBox_2, 3, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.verticalWidget)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 1, 0, 1, 1)
        self.label_16 = QtWidgets.QLabel(self.verticalWidget)
        self.label_16.setAlignment(QtCore.Qt.AlignCenter)
        self.label_16.setObjectName("label_16")
        self.gridLayout_2.addWidget(self.label_16, 2, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.verticalWidget)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 3, 1, 1, 1)
        self.comboBox = QtWidgets.QComboBox(self.verticalWidget)
        self.comboBox.setObjectName("comboBox")
        self.gridLayout_2.addWidget(self.comboBox, 0, 1, 1, 1)
        self.lineEdit_6 = QtWidgets.QLineEdit(self.verticalWidget)
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.gridLayout_2.addWidget(self.lineEdit_6, 2, 1, 1, 1)
        self.horizontalLayout_2.addLayout(self.gridLayout_2)
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.comboBox_3 = QtWidgets.QComboBox(self.verticalWidget)
        self.comboBox_3.setObjectName("comboBox_3")
        self.gridLayout_4.addWidget(self.comboBox_3, 0, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.verticalWidget)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.gridLayout_4.addWidget(self.label_5, 4, 1, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.verticalWidget)
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.gridLayout_4.addWidget(self.label_10, 0, 0, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.verticalWidget)
        self.label_12.setAlignment(QtCore.Qt.AlignCenter)
        self.label_12.setObjectName("label_12")
        self.gridLayout_4.addWidget(self.label_12, 1, 0, 1, 1)
        self.checkBox_4 = QtWidgets.QCheckBox(self.verticalWidget)
        self.checkBox_4.setObjectName("checkBox_4")
        self.gridLayout_4.addWidget(self.checkBox_4, 4, 0, 1, 1)
        self.lineEdit_4 = QtWidgets.QLineEdit(self.verticalWidget)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.gridLayout_4.addWidget(self.lineEdit_4, 1, 1, 1, 1)
        self.label_17 = QtWidgets.QLabel(self.verticalWidget)
        self.label_17.setAlignment(QtCore.Qt.AlignCenter)
        self.label_17.setObjectName("label_17")
        self.gridLayout_4.addWidget(self.label_17, 2, 0, 1, 1)
        self.lineEdit_7 = QtWidgets.QLineEdit(self.verticalWidget)
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.gridLayout_4.addWidget(self.lineEdit_7, 2, 1, 1, 1)
        self.horizontalLayout_2.addLayout(self.gridLayout_4)
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.label_13 = QtWidgets.QLabel(self.verticalWidget)
        self.label_13.setAlignment(QtCore.Qt.AlignCenter)
        self.label_13.setObjectName("label_13")
        self.gridLayout_5.addWidget(self.label_13, 0, 0, 1, 1)
        self.lineEdit_5 = QtWidgets.QLineEdit(self.verticalWidget)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.gridLayout_5.addWidget(self.lineEdit_5, 1, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.verticalWidget)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.gridLayout_5.addWidget(self.label_8, 4, 1, 1, 1)
        self.comboBox_4 = QtWidgets.QComboBox(self.verticalWidget)
        self.comboBox_4.setObjectName("comboBox_4")
        self.gridLayout_5.addWidget(self.comboBox_4, 0, 1, 1, 1)
        self.checkBox_5 = QtWidgets.QCheckBox(self.verticalWidget)
        self.checkBox_5.setObjectName("checkBox_5")
        self.gridLayout_5.addWidget(self.checkBox_5, 4, 0, 1, 1)
        self.label_15 = QtWidgets.QLabel(self.verticalWidget)
        self.label_15.setAlignment(QtCore.Qt.AlignCenter)
        self.label_15.setObjectName("label_15")
        self.gridLayout_5.addWidget(self.label_15, 1, 0, 1, 1)
        self.label_18 = QtWidgets.QLabel(self.verticalWidget)
        self.label_18.setAlignment(QtCore.Qt.AlignCenter)
        self.label_18.setObjectName("label_18")
        self.gridLayout_5.addWidget(self.label_18, 2, 0, 1, 1)
        self.lineEdit_8 = QtWidgets.QLineEdit(self.verticalWidget)
        self.lineEdit_8.setObjectName("lineEdit_8")
        self.gridLayout_5.addWidget(self.lineEdit_8, 2, 1, 1, 1)
        self.horizontalLayout_2.addLayout(self.gridLayout_5)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.comboBox_5 = QtWidgets.QComboBox(self.verticalWidget)
        self.comboBox_5.setObjectName("comboBox_5")
        self.gridLayout.addWidget(self.comboBox_5, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.verticalWidget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.verticalWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 1, 1, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.verticalWidget)
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName("label_11")
        self.gridLayout.addWidget(self.label_11, 3, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.verticalWidget)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.checkBox = QtWidgets.QCheckBox(self.verticalWidget)
        self.checkBox.setObjectName("checkBox")
        self.gridLayout.addWidget(self.checkBox, 3, 0, 1, 1)
        self.label_19 = QtWidgets.QLabel(self.verticalWidget)
        self.label_19.setAlignment(QtCore.Qt.AlignCenter)
        self.label_19.setObjectName("label_19")
        self.gridLayout.addWidget(self.label_19, 2, 0, 1, 1)
        self.lineEdit_9 = QtWidgets.QLineEdit(self.verticalWidget)
        self.lineEdit_9.setObjectName("lineEdit_9")
        self.gridLayout.addWidget(self.lineEdit_9, 2, 1, 1, 1)
        self.horizontalLayout_2.addLayout(self.gridLayout)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_14 = QtWidgets.QLabel(self.verticalWidget)
        self.label_14.setAlignment(QtCore.Qt.AlignCenter)
        self.label_14.setObjectName("label_14")
        self.gridLayout_3.addWidget(self.label_14, 4, 1, 1, 1)
        self.checkBox_3 = QtWidgets.QCheckBox(self.verticalWidget)
        self.checkBox_3.setObjectName("checkBox_3")
        self.gridLayout_3.addWidget(self.checkBox_3, 4, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.verticalWidget)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.gridLayout_3.addWidget(self.label_7, 0, 0, 1, 1)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.verticalWidget)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.gridLayout_3.addWidget(self.lineEdit_3, 1, 1, 1, 1)
        self.comboBox_6 = QtWidgets.QComboBox(self.verticalWidget)
        self.comboBox_6.setObjectName("comboBox_6")
        self.gridLayout_3.addWidget(self.comboBox_6, 0, 1, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.verticalWidget)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.gridLayout_3.addWidget(self.label_9, 1, 0, 1, 1)
        self.label_20 = QtWidgets.QLabel(self.verticalWidget)
        self.label_20.setAlignment(QtCore.Qt.AlignCenter)
        self.label_20.setObjectName("label_20")
        self.gridLayout_3.addWidget(self.label_20, 2, 0, 1, 1)
        self.lineEdit_10 = QtWidgets.QLineEdit(self.verticalWidget)
        self.lineEdit_10.setObjectName("lineEdit_10")
        self.gridLayout_3.addWidget(self.lineEdit_10, 2, 1, 1, 1)
        self.horizontalLayout_2.addLayout(self.gridLayout_3)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem1)
        self.listWidget = QtWidgets.QListWidget(self.verticalWidget)
        self.listWidget.setStyleSheet("background-color: rgb(72, 72, 72);")
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)
        self.gridLayout_6.addWidget(self.verticalWidget, 0, 0, 1, 1)

        self.retranslateUi(Form)
        self.set_blocks()
        self.configUI()
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "SBP-S Emulator"))
        self.pushButton.setText(_translate("Form", "Scan Ports"))
        self.pushButton_2.setText(_translate("Form", "CONNECT"))
        self.checkBox_6.setText(_translate("Form", "SBP Enable"))
        self.label_4.setText(_translate("Form", "CMD"))
        self.checkBox_2.setText(_translate("Form", "Enable"))
        self.label_6.setText(_translate("Form", "Interval"))
        self.label_16.setText(_translate("Form", "Data"))
        self.label_2.setText(_translate("Form", "ERROR"))
        self.label_5.setText(_translate("Form", "ERROR"))
        self.label_10.setText(_translate("Form", "CMD"))
        self.label_12.setText(_translate("Form", "Interval"))
        self.checkBox_4.setText(_translate("Form", "Enable"))
        self.label_17.setText(_translate("Form", "Data"))
        self.label_13.setText(_translate("Form", "CMD"))
        self.label_8.setText(_translate("Form", "ERROR"))
        self.checkBox_5.setText(_translate("Form", "Enable"))
        self.label_15.setText(_translate("Form", "Interval"))
        self.label_18.setText(_translate("Form", "Data"))
        self.label.setText(_translate("Form", "CMD"))
        self.label_11.setText(_translate("Form", "ERROR"))
        self.label_3.setText(_translate("Form", "Interval"))
        self.checkBox.setText(_translate("Form", "Enable"))
        self.label_19.setText(_translate("Form", "Data"))
        self.label_14.setText(_translate("Form", "ERROR"))
        self.checkBox_3.setText(_translate("Form", "Enable"))
        self.label_7.setText(_translate("Form", "CMD"))
        self.label_9.setText(_translate("Form", "Interval"))
        self.label_20.setText(_translate("Form", "Data"))


    def set_blocks(self):
        self.blocks = {
            "1" :{"Cmd": self.comboBox, "Interval": self.lineEdit_2, "Data": self.lineEdit_6, "Enable": self.checkBox_2, "Error": self.label_2},
            "2" :{"Cmd": self.comboBox_3, "Interval": self.lineEdit_4, "Data": self.lineEdit_7, "Enable": self.checkBox_4, "Error": self.label_5},
            "3" :{"Cmd": self.comboBox_4, "Interval": self.lineEdit_5, "Data": self.lineEdit_8, "Enable": self.checkBox_5, "Error": self.label_8},
            "4" :{"Cmd": self.comboBox_5, "Interval": self.lineEdit, "Data": self.lineEdit_9, "Enable": self.checkBox, "Error": self.label_11},
            "5" :{"Cmd": self.comboBox_6, "Interval": self.lineEdit_3, "Data": self.lineEdit_10, "Enable": self.checkBox_3, "Error": self.label_14}
        }
    

    def configUI(self):
        self.comboBox_7.addItems(self.baud_list)
        self.scan_ports()
        self.comboBox.addItems(self.commands)
        self.comboBox_3.addItems(self.commands)
        self.comboBox_4.addItems(self.commands)
        self.comboBox_5.addItems(self.commands)
        self.comboBox_6.addItems(self.commands)

        self.set_interval("1", "1000")
        self.set_interval("2", "1000")
        self.set_interval("3", "1000")
        self.set_interval("4", "1000")
        self.set_interval("5", "1000")

        self.set_data("1", "0")
        self.set_data("2", "0")
        self.set_data("3", "0")
        self.set_data("4", "0")
        self.set_data("5", "0")


    def set_cmd(self, block:str, number:str):
        obj = self.blocks[block].get("Cmd")
        obj.setText(number)

    def set_interval(self, block:str, number:str):
        obj = self.blocks[block].get("Interval")
        obj.setText(number)
    
    def get_interval(self, block):
        obj =  self.blocks[block].get("Interval")
        return obj.text()
    
    def set_data(self, block:str, data:str):
        obj = self.blocks[block].get("Data")
        obj.setText(data)
    
    def get_data(self, block):
        obj =  self.blocks[block].get("Data")
        return obj.text()
    
    def set_enable(self, block:str, enable:bool):
        obj = self.blocks[block].get("Enable")
        obj.setChecked(enable)
    
    def get_enable(self, block):
        obj =  self.blocks[block].get("Enable")
        return obj.isChecked()


    
    def log(self, txt, color="yellow"):
        if "Received Message" in txt:
            if not self.checkBox_2.isChecked():
                return
        i = QtWidgets.QListWidgetItem(txt)
        i.setForeground(QColor(color))
        self.console.addItem(i)
        self.console.scrollToBottom()
        # if self.console.count() > 80:
        #     self.console.clear
        QApplication.processEvents()

    def set_message(self, message):
        self.log(str(message), "white")

    def clear_console(self):
        self.console.clear()

    def set_ports(self):
        self.ports = []
        for d in self.serial.list_ports():
            try:
                self.ports.append(" | ".join([d.device, d.serial_number]))
            except:
                pass

    def set_baud(self):
        self.serial_baud = int(self.comboBox_7.currentText())
        
    
    # def set_data(self):
    #     tmp = self.lineEdit.text()
    #     tmp = tmp.split(" ")
    #     if tmp[0] == "@":
    #         lat = float(tmp[1]) * 200000
    #         long = float(tmp[2]) * 200000
    #         alt = float(tmp[3]) * 200000
    #         hacc = float(tmp[4]) * 200000
    #         lat = f"{int(lat):x}"
    #         long = f"{int(long):x}"
    #         alt = f"{int(alt):x}"
    #         hacc = f"{int(hacc):x}"
    #         while(len(lat)<8):
    #             lat = "0"+ lat
    #         while(len(long)<8):
    #             long = "0" + long
    #         while(len(alt)<8):
    #             alt = "0" + alt
    #         while(len(hacc)<8):
    #             hacc = "0" + hacc
    #         lat = [lat[i:i+2] for i in range(0,len(lat),2)]
    #         long = [long[i:i+2] for i in range(0,len(long),2)]
    #         alt = [alt[i:i+2] for i in range(0,len(alt),2)]
    #         hacc = [hacc[i:i+2] for i in range(0,len(hacc),2)]
    #         suma = lat+long+alt+hacc
    #         self.data = [int(suma[i],16) for i in range(0,len(suma))]
    #         print(self.data)
    #     else:   
    #          self.data = [int(tmp[i],16) for i in range(0,len(tmp))]
    #          print("Data: ",self.data)

    def transmit_message(self):
        if self.manager == None:
            self.log("First Connect to a Device", "red")
        self.set_data()
        self.manager.set_tx_data(self.data)
        self.manager.set_tx_cmd(self.cmd)
        self.manager.transmit_message()
    
    def stop_repeated_tx(self):
        self.manager.stop_tx_flag = True
    
    def start_repeated_tx(self):
        if self.manager == None:
            self.log("First Connect to a Device", "red")
        self.manager.set_max_repeats(self.repeats)
        self.manager.set_repeat_interval(self.interval)
        self.set_data()
        self.manager.set_tx_data(self.data)
        self.manager.set_tx_cmd(self.cmd)
        self.manager.repeated_tx_start()

    def repeated_tx(self):
        
        for i in range(0, self.repeats):
            if self.stop_tx_flag == True:
                break
            self.transmit_message()
            time.sleep(self.interval)
            QApplication.processEvents()

    def scan_ports(self):
        self.set_ports()
        self.comboBox_2.clear()
        self.comboBox_2.addItems(self.ports)

    def connect_toPort(self):
        if self.connected_flag == False:
            port = self.comboBox_2.currentText().split("|")[0][0:-1]
            self.serial.device = port
            self.serial.baud = self.serial_baud
            self.serial.error = None
            self.serial.serial_connect()
            if self.serial.error is not None:
                self.log(self.serial.error, "red")
                self.pushButton_2.setStyleSheet("background-color: red")
                self.connected_flag = False

            else:
                self.pushButton_2.setStyleSheet("background-color: green")
                self.manager = Handler(self.serial, self.messager)
                self.log("Connected to Port", "green")
                self.connected_flag = True

        else:
            self.log("Disconnecting from Port", "red")
            self.messager.killsignal.emit(1)
            del self.manager
            self.serial.serial_disconnect()
            self.connected_flag = False
            self.pushButton_2.setStyleSheet("background-color: red")




class Messager(QtCore.QObject):
    signal = QtCore.pyqtSignal(str)
    killsignal = QtCore.pyqtSignal(int)


# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     Form = QtWidgets.QWidget()
#     ui = Ui_Form()
#     ui.setupUi(Form)
#     Form.show()
#     sys.exit(app.exec_())
