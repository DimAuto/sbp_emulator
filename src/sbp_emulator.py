from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication
from manager import Handler
import time
import numpy as np


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
        self.voltage_sources = {"Battery": 0, "External": 1}

        self.messager.signal.connect(self.set_message)
        self.connected_flag = False
        self.stop_tx_flag = False
        
        self.scan_enabled = False
        self.hb_enabled = False
        self.hb_interval = "1000"
        self.max_retransmit = 3
        self.voltage_reply_enabled = False
        self.voltage_source = [0]
        self.gps_coor_enabled = False
        self.gps_clock_enabled = False
        self.lat = "0"
        self.long = "0"
        self.alt = "0"
        self.hacc = "0"
        self.gps_h = "00"
        self.gps_m = "00"
        self.gps_s = "00"
        self.battery_V_mv = [0, 0]
        self.external_V_mv = [0, 0]
        self.master_enable = False
        self.tx_data = []
        self.gps_data = []
        self.gps_clock = []
        self.FW_version = ['t','e','s','t','1','2','3']

        self.data_dict = {"86": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], "128":[48,48,48,48,48,48], "112": [0,0],
                     "114": [0,0], "116":[0], "81":[0], "101": self.FW_version, "51":1.0}

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1400, 1080)
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
        self.horizontalLayout.addWidget(self.comboBox_7)
        self.pushButton_2 = QtWidgets.QPushButton(self.verticalWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.pressed.connect(self.connect_toPort)
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.checkBox_6 = QtWidgets.QCheckBox(self.verticalWidget)
        self.checkBox_6.setMaximumSize(QtCore.QSize(300, 16777215))
        self.checkBox_6.setObjectName("checkBox_6")
        self.checkBox_6.stateChanged.connect(self.set_master_enabled)
        self.horizontalLayout.addWidget(self.checkBox_6)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.line = QtWidgets.QFrame(self.verticalWidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_17 = QtWidgets.QLabel(self.verticalWidget)
        self.label_17.setObjectName("label_17")
        self.gridLayout.addWidget(self.label_17, 0, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.verticalWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.checkBox_2 = QtWidgets.QCheckBox(self.verticalWidget)
        self.checkBox_2.setObjectName("checkBox_2")
        self.checkBox_2.stateChanged.connect(self.set_hb_enabled)
        self.gridLayout.addWidget(self.checkBox_2, 1, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.verticalWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lineEdit_8 = QtWidgets.QLineEdit(self.verticalWidget)
        self.lineEdit_8.setMaximumSize(QtCore.QSize(300, 16777215))
        self.lineEdit_8.setObjectName("lineEdit_8")
        self.lineEdit_8.textChanged.connect(self.set_ack_timeout_ms)
        self.gridLayout.addWidget(self.lineEdit_8, 1, 2, 1, 1)
        self.checkBox = QtWidgets.QCheckBox(self.verticalWidget)
        self.checkBox.setObjectName("checkBox")
        self.checkBox.stateChanged.connect(self.set_scan_enabled)
        self.gridLayout.addWidget(self.checkBox, 1, 0, 1, 1)
        self.label_18 = QtWidgets.QLabel(self.verticalWidget)
        self.label_18.setObjectName("label_18")
        self.gridLayout.addWidget(self.label_18, 0, 3, 1, 1)
        self.spinBox = QtWidgets.QSpinBox(self.verticalWidget)
        self.spinBox.setMaximumSize(QtCore.QSize(300, 16777215))
        self.spinBox.setObjectName("spinBox")
        self.spinBox.textChanged.connect(self.set_max_retransmit)
        self.gridLayout.addWidget(self.spinBox, 1, 3, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.line_2 = QtWidgets.QFrame(self.verticalWidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.comboBox = QtWidgets.QComboBox(self.verticalWidget)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.currentTextChanged.connect(self.set_voltage_source)
        self.gridLayout_2.addWidget(self.comboBox, 0, 2, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.verticalWidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 1, 1, 1, 1)
        self.horizontalSlider = QtWidgets.QSlider(self.verticalWidget)
        # self.horizontalSlider.setMaximumSize(QtCore.QSize(700, 16777215))
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalSlider.setMinimum(0)
        self.horizontalSlider.setMaximum(25000)
        self.horizontalSlider.valueChanged.connect(self.set_external_V)
        self.gridLayout_2.addWidget(self.horizontalSlider, 2, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.verticalWidget)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 1, 2, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.verticalWidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 0, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.verticalWidget)
        self.label_8.setObjectName("label_8")
        self.gridLayout_2.addWidget(self.label_8, 2, 2, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.verticalWidget)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 2, 1, 1, 1)
        self.checkBox_3 = QtWidgets.QCheckBox(self.verticalWidget)
        self.checkBox_3.setObjectName("checkBox_3")
        self.checkBox_3.stateChanged.connect(self.set_voltage_enabled)
        self.gridLayout_2.addWidget(self.checkBox_3, 0, 0, 1, 1)
        self.horizontalSlider_2 = QtWidgets.QSlider(self.verticalWidget)
        # self.horizontalSlider_2.setMaximumSize(QtCore.QSize(700, 16777215))
        self.horizontalSlider_2.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_2.setObjectName("horizontalSlider_2")
        self.horizontalSlider_2.setMinimum(0)
        self.horizontalSlider_2.setMaximum(25000)
        self.horizontalSlider_2.valueChanged.connect(self.set_battery_V)
        self.gridLayout_2.addWidget(self.horizontalSlider_2, 1, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)
        self.line_3 = QtWidgets.QFrame(self.verticalWidget)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout.addWidget(self.line_3)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_13 = QtWidgets.QLabel(self.verticalWidget)
        self.label_13.setObjectName("label_13")
        self.gridLayout_3.addWidget(self.label_13, 2, 4, 1, 1)
        self.label_14 = QtWidgets.QLabel(self.verticalWidget)
        self.label_14.setObjectName("label_14")
        self.gridLayout_3.addWidget(self.label_14, 2, 5, 1, 1)
        self.checkBox_5 = QtWidgets.QCheckBox(self.verticalWidget)
        self.checkBox_5.setObjectName("checkBox_5")
        self.checkBox_5.stateChanged.connect(self.set_gps_clock_enabled)
        self.gridLayout_3.addWidget(self.checkBox_5, 1, 4, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.verticalWidget)
        self.label_12.setObjectName("label_12")
        self.gridLayout_3.addWidget(self.label_12, 2, 3, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.verticalWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout_3.addWidget(self.label_3, 0, 0, 1, 1)
        self.checkBox_4 = QtWidgets.QCheckBox(self.verticalWidget)
        self.checkBox_4.setObjectName("checkBox_4")
        self.checkBox_4.stateChanged.connect(self.set_gps_coor_enabled)
        self.gridLayout_3.addWidget(self.checkBox_4, 1, 0, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.verticalWidget)
        self.label_10.setObjectName("label_10")
        self.gridLayout_3.addWidget(self.label_10, 2, 1, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.verticalWidget)
        self.label_11.setObjectName("label_11")
        self.gridLayout_3.addWidget(self.label_11, 2, 2, 1, 1)
        self.label_15 = QtWidgets.QLabel(self.verticalWidget)
        self.label_15.setObjectName("label_15")
        self.gridLayout_3.addWidget(self.label_15, 2, 6, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.verticalWidget)
        self.label_9.setObjectName("label_9")
        self.gridLayout_3.addWidget(self.label_9, 2, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.verticalWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout_3.addWidget(self.lineEdit, 3, 0, 1, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.verticalWidget)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout_3.addWidget(self.lineEdit_2, 3, 1, 1, 1)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.verticalWidget)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.gridLayout_3.addWidget(self.lineEdit_3, 3, 2, 1, 1)
        self.lineEdit_4 = QtWidgets.QLineEdit(self.verticalWidget)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.gridLayout_3.addWidget(self.lineEdit_4, 3, 3, 1, 1)
        self.lineEdit_5 = QtWidgets.QLineEdit(self.verticalWidget)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.gridLayout_3.addWidget(self.lineEdit_5, 3, 4, 1, 1)
        self.lineEdit_6 = QtWidgets.QLineEdit(self.verticalWidget)
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.gridLayout_3.addWidget(self.lineEdit_6, 3, 5, 1, 1)
        self.lineEdit_7 = QtWidgets.QLineEdit(self.verticalWidget)
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.gridLayout_3.addWidget(self.lineEdit_7, 3, 6, 1, 1)
        self.label_16 = QtWidgets.QLabel(self.verticalWidget)
        self.label_16.setObjectName("label_16")
        self.gridLayout_3.addWidget(self.label_16, 0, 4, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_3)
        self.line_4 = QtWidgets.QFrame(self.verticalWidget)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.verticalLayout.addWidget(self.line_4)
        self.console = QtWidgets.QListWidget(self.verticalWidget)
        self.console.setStyleSheet("background-color: rgb(72, 72, 72);")
        self.console.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.console)
        self.gridLayout_6.addWidget(self.verticalWidget, 0, 0, 1, 1)

        self.lineEdit.textChanged.connect(self.set_lat)
        self.lineEdit_2.textChanged.connect(self.set_long)
        self.lineEdit_3.textChanged.connect(self.set_alt)
        self.lineEdit_4.textChanged.connect(self.set_hacc)
        self.lineEdit_5.textChanged.connect(self.set_GPS_clock_H)
        self.lineEdit_6.textChanged.connect(self.set_GPS_clock_M)
        self.lineEdit_7.textChanged.connect(self.set_GPS_clock_S)

        self.retranslateUi(Form)
        self.configUI()
        self.disable_all_cb()
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "SBP-S Emulator"))
        self.pushButton.setText(_translate("Form", "Scan Ports"))
        self.pushButton_2.setText(_translate("Form", "Connect"))
        self.checkBox_6.setText(_translate("Form", "SBP Enable"))
        self.label_17.setText(_translate("Form", "Heartbeat Interval"))
        self.label_2.setText(_translate("Form", "Send Heartbeat"))
        self.checkBox_2.setText(_translate("Form", "Enabled"))
        self.label.setText(_translate("Form", "Reply to scan messages"))
        self.checkBox.setText(_translate("Form", "Enabled"))
        self.label_18.setText(_translate("Form", "Max retransmit #"))
        self.label_4.setText(_translate("Form", "Battery"))
        self.label_7.setText(_translate("Form", "0"))
        self.label_5.setText(_translate("Form", "Voltage Source"))
        self.label_8.setText(_translate("Form", "0"))
        self.label_6.setText(_translate("Form", "External"))
        self.checkBox_3.setText(_translate("Form", "Reply to voltage requests"))
        self.label_13.setText(_translate("Form", "Hours"))
        self.label_14.setText(_translate("Form", "Minutes"))
        self.checkBox_5.setText(_translate("Form", "Reply to GPS clock requests"))
        self.label_12.setText(_translate("Form", "Circ. Error"))
        self.label_3.setText(_translate("Form", "GPS Location"))
        self.checkBox_4.setText(_translate("Form", "Reply to GPS coor requests"))
        self.label_10.setText(_translate("Form", "Longtitude"))
        self.label_11.setText(_translate("Form", "Altitude"))
        self.label_15.setText(_translate("Form", "Seconds"))
        self.label_9.setText(_translate("Form", "Latitude"))
        self.label_16.setText(_translate("Form", "GPS Clock"))

    def configUI(self):
        self.comboBox_7.addItems(self.baud_list)
        self.scan_ports()
        self.comboBox.addItems(self.voltage_sources)
        self.lineEdit.setText(self.lat)
        self.lineEdit_2.setText(self.long)
        self.lineEdit_3.setText(self.alt)
        self.lineEdit_4.setText(self.hacc)
        self.lineEdit_5.setText(self.gps_h)
        self.lineEdit_6.setText(self.gps_m)
        self.lineEdit_7.setText(self.gps_s)
        self.lineEdit_8.setText(self.hb_interval)
        self.checkBox_6.setChecked(True)

    def enable_all_cb(self):
        self.checkBox.setEnabled(True)
        self.checkBox_2.setEnabled(True)
        self.checkBox_3.setEnabled(True)
        self.checkBox_4.setEnabled(True)
        self.checkBox_5.setEnabled(True)
        self.checkBox_6.setEnabled(True)

    def disable_all_cb(self):
        self.checkBox.setEnabled(False)
        self.checkBox_2.setEnabled(False)
        self.checkBox_3.setEnabled(False)
        self.checkBox_4.setEnabled(False)
        self.checkBox_5.setEnabled(False)
        self.checkBox_6.setEnabled(False)
        self.checkBox.setCheckState(False)
        self.checkBox_2.setCheckState(False)
        self.checkBox_3.setCheckState(False)
        self.checkBox_4.setCheckState(False)
        self.checkBox_5.setCheckState(False)
        # self.checkBox_6.setCheckState(False)


    def log(self, txt, color="yellow"):
        i = QtWidgets.QListWidgetItem(txt)
        i.setForeground(QColor(color))
        if self.console.count() > 100:
            self.console.clear
        self.console.addItem(i)
        self.console.scrollToBottom()
        
        QApplication.processEvents()

    def clear_console(self):
        self.console.clear()

    def set_ports(self):
        self.ports = []
        for d in self.serial.list_ports():
            try:
                self.ports.append(" | ".join([d.device, d.serial_number]))
            except:
                pass

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
                # self.pushButton_2.setStyleSheet("background-color: red")
                self.disable_all_cb()
                self.connected_flag = False

            else:
                # self.pushButton_2.setStyleSheet("background-color: green")
                self.manager = Handler(self.serial, self.messager)
                self.log("Connected to Port", "green")
                self.pushButton_2.setText("Disconnect")
                self.enable_all_cb()
                self.connected_flag = True

        else:
            self.log("Disconnecting from Port", "red")
            self.messager.killsignal.emit(1)
            del self.manager
            self.serial.serial_disconnect()
            self.connected_flag = False
            # self.pushButton_2.setStyleSheet("background-color: red")
            self.pushButton_2.setText("Connect")
            self.disable_all_cb()

#------------ SETTERS GETTERS--------------#
    def set_message(self, message):
        self.log(str(message), "white")

    def set_baud(self):
        self.serial_baud = int(self.comboBox_7.currentText())

    def set_lat(self):
        self.lat = self.lineEdit.text()
        self.set_GPS_data()

    def get_lat(self):
        temp = 0
        try:
            temp = float(self.lat) * 200000
            temp = np.uint32(temp)
        except:
            pass
        return [(temp & 0xFF000000) >>24, (temp & 0x00FF0000) >> 16,
                (temp & 0x0000FF00) >>8, (temp & 0x000000FF)]

    def set_long(self):
        self.long = self.lineEdit_2.text()
        self.set_GPS_data()

    def get_long(self):
        temp = 0
        try:
            temp = float(self.long) * 200000
            temp = np.uint32(temp)
        except:
            pass
        return [(temp & 0xFF000000) >>24, (temp & 0x00FF0000) >> 16,
                (temp & 0x0000FF00) >>8, (temp & 0x000000FF)]
        
    def set_alt(self):
        self.alt = self.lineEdit_3.text()
        self.set_GPS_data()

    def get_alt(self):
        temp = 0
        try:
            temp = float(self.alt) * 200000
            temp = np.uint32(temp)
        except:
            pass
        return [(temp & 0xFF000000) >>24, (temp & 0x00FF0000) >> 16,
                (temp & 0x0000FF00) >>8, (temp & 0x000000FF)]
    
    def set_hacc(self):
        self.hacc = self.lineEdit_4.text()
        self.set_GPS_data()

    def get_hacc(self):
        temp = 0
        try:
            temp = float(self.hacc) * 200000
            temp = np.uint32(temp)
        except:
            pass
        return [(temp & 0xFF000000) >>24, (temp & 0x00FF0000) >> 16,
                (temp & 0x0000FF00) >>8, (temp & 0x000000FF)]

    def set_GPS_clock_H(self):
        self.gps_h = self.lineEdit_5.text()
        self.set_GPS_clock()
        
    def get_GPS_clock_H(self):
        return [ord(i) for i in self.gps_h]

    def set_GPS_clock_M(self):
        self.gps_m = self.lineEdit_6.text()
        self.set_GPS_clock()

    def get_GPS_clock_M(self):
        return [ord(i) for i in self.gps_m]

    def set_GPS_clock_S(self):
        self.gps_s = self.lineEdit_7.text()
        self.set_GPS_clock()

    def get_GPS_clock_S(self):
        return [ord(i) for i in self.gps_s]

    def set_GPS_data(self): 
        self.gps_data = self.get_lat() + self.get_long() + self.get_alt() + self.get_hacc()
        self.data_dict["86"] = self.gps_data
        self.messager.data_tx.emit(self.data_dict)

    def set_GPS_clock(self):
        self.gps_clock = self.get_GPS_clock_H() + self.get_GPS_clock_M()+ self.get_GPS_clock_S()
        self.data_dict["128"] = self.gps_clock
        self.messager.data_tx.emit(self.data_dict)

    def set_voltage_source(self):
        self.voltage_source[0] = (self.voltage_sources.get(self.comboBox.currentText()))
        self.data_dict["116"] = self.voltage_source
        self.messager.data_tx.emit(self.data_dict)

    def get_voltage_source(self):
        return self.voltage_source
    
    def set_battery_V(self):
        temp = self.horizontalSlider_2.value()
        self.label_7.setText(str(temp))
        temp = np.uint16(temp * 4.095)
        self.battery_V_mv[0] = temp >> 8
        self.battery_V_mv[1] = temp & 0xFF
        self.data_dict["112"] = self.battery_V_mv
        self.messager.data_tx.emit(self.data_dict)

    def get_battery_V(self) ->list:
        pass

    def set_external_V(self):
        temp = self.horizontalSlider.value()
        self.label_8.setText(str(temp))
        temp = np.uint16(temp * 4.095)
        self.external_V_mv[0] = temp >> 8
        self.external_V_mv[1] = temp & 0xFF
        self.data_dict["114"] = self.battery_V_mv
        self.messager.data_tx.emit(self.data_dict)

    def get_external_V(self):
        pass

    def set_ack_timeout_ms(self):
        self.hb_interval = self.lineEdit_8.text()
        try:
            temp = int(self.hb_interval)
            if temp in range(500, 10001):
                self.data_dict["51"] = temp / 1000
                self.messager.data_tx.emit(self.data_dict)
                self.lineEdit_8.setStyleSheet("background-color: white")
            else:
                self.lineEdit_8.setStyleSheet("background-color: red")
        except:
            self.lineEdit_8.setStyleSheet("background-color: red")

    def get_ack_timeout_ms(self):
        return int(self.hb_interval) / 1000
    
    def set_max_retransmit(self):
        self.max_retransmit = int(self.spinBox.text())

    def get_max_retransmit(self):
        return self.max_retransmit

    def set_scan_enabled(self):
        self.scan_enabled = self.checkBox.isChecked()
        self.messager.reply_scan.emit(self.scan_enabled) #Send message to handler

    def get_scan_enabled(self):
        return self.scan_enabled

    def set_hb_enabled(self):
        self.hb_enabled = self.checkBox_2.isChecked()
        self.messager.send_hb.emit(self.hb_enabled) #Send message to handler

    def get_hb_enabled(self):
        return self.hb_enabled

    def set_voltage_enabled(self):
        self.voltage_reply_enabled = self.checkBox_3.isChecked()
        self.messager.reply_voltage.emit(self.voltage_reply_enabled) #Send message to handler

    def get_voltage_enabled(self):
        return self.voltage_reply_enabled

    def set_gps_coor_enabled(self):
        self.gps_coor_enabled = self.checkBox_4.isChecked()
        self.set_GPS_data()
        self.messager.reply_GPS_location.emit(self.gps_coor_enabled) #Send message to handler

    def get_gps_coor_enabled(self):
        return self.gps_coor_enabled

    def set_gps_clock_enabled(self):
        self.gps_clock_enabled = self.checkBox_5.isChecked()
        self.set_GPS_clock()
        self.messager.reply_GPS_clock.emit(self.gps_clock_enabled) #Send message to handler

    def get_gps_clock_enabled(self):
        return self.gps_coor_enabled

    def set_master_enabled(self):
        self.master_enable = self.checkBox_6.isChecked()
        self.messager.master_enable.emit(self.master_enable)

    def get_master_enabled(self):
        return self.master_enable
    

class Messager(QtCore.QObject):
    signal = QtCore.pyqtSignal(str)
    killsignal = QtCore.pyqtSignal(int)
    data_tx = QtCore.pyqtSignal(dict)
    reply_scan = QtCore.pyqtSignal(bool)
    send_hb = QtCore.pyqtSignal(bool)
    reply_voltage = QtCore.pyqtSignal(bool)
    reply_GPS_location = QtCore.pyqtSignal(bool)
    reply_GPS_clock = QtCore.pyqtSignal(bool)
    master_enable = QtCore.pyqtSignal(bool)
    