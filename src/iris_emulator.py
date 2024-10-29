from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication
from manager import Handler
import time


class Ui_MainWindow(object):

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
        self.command_list = ["0x50", "0x56", "0x57", "0x58", "0x70", "0x65", "0x62", "0x72", 
                             "0x74", "0x78", "0x80", "0x81", "0x82", "0x84", "0x90", "0xA0","0xA1",
                             "0xC0", "0xC1", "0xC2", "0xC3", "0xB0", "0xB1", "0xB2", "0xD1", "0xD2"]
        self.messager.signal.connect(self.set_message)
        self.connected_flag = False
        self.stop_tx_flag = False

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1020, 820)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(30, 120, 150, 25))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.currentIndexChanged.connect(self.set_cmd)
        self.comboBox_2 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_2.setGeometry(QtCore.QRect(140, 30, 260, 25))
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_3 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_3.setGeometry(QtCore.QRect(420, 30, 100, 25))
        self.comboBox_3.setObjectName("comboBox_3")
        self.comboBox_3.currentIndexChanged.connect(self.set_baud)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(30, 30, 100, 25))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.pressed.connect(self.scan_ports)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(540, 30, 100, 25))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.pressed.connect(self.connect_toPort)
        self.console = QtWidgets.QListWidget(self.centralwidget)
        self.console.setGeometry(QtCore.QRect(10, 240, 980, 550))
        self.console.setStyleSheet("background-color: rgb(59, 59, 59);\n"
"font: 7pt \"MS Shell Dlg 2\";\n"
"color: rgb(255, 0, 0);")
        self.console.setObjectName("listWidget")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(190, 120, 100, 25))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.pressed.connect(self.transmit_message)
        self.pushButton_3.setEnabled(False)
        self.pushButton_vout = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_vout.setGeometry(QtCore.QRect(840, 120, 140, 25))
        self.pushButton_vout.setObjectName("pushButton_vout")
        self.pushButton_vout.pressed.connect(self.enable_vidout)
        self.pushButton_vout.setEnabled(False)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(27, 155, 260, 75))
        self.groupBox.setObjectName("groupBox")
        self.pushButton_4 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_4.setGeometry(QtCore.QRect(150, 12, 100, 25))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.pressed.connect(self.start_repeated_tx)
        self.pushButton_4.setEnabled(False)
        self.pushButton_stop = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_stop.setGeometry(QtCore.QRect(150, 42, 100, 25))
        self.pushButton_stop.setObjectName("pushButton_stop")
        self.pushButton_stop.pressed.connect(self.stop_repeated_tx)
        self.pushButton_stop.setEnabled(False)
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.doubleSpinBox.setGeometry(QtCore.QRect(5, 22, 62, 30))
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.doubleSpinBox.valueChanged.connect(self.set_interval)
        self.spinBox = QtWidgets.QSpinBox(self.groupBox)
        self.spinBox.setGeometry(QtCore.QRect(75, 22, 51, 30))
        self.spinBox.setObjectName("spinBox")
        self.spinBox.valueChanged.connect(self.set_repeats)
        self.spinBox.setMaximum(10000)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 120, 121, 22))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(220, 10, 141, 20))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(530, 80, 140, 27))
        self.label_3.setObjectName("label_3")
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(305, 210, 80, 25))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.pressed.connect(self.clear_console)
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(400, 210, 250, 22))
        self.checkBox.setObjectName("checkBox")
        self.checkBox_2 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_2.setGeometry(QtCore.QRect(700, 210, 250, 22))
        self.checkBox_2.setObjectName("checkBox_2")
        self.checkBox_3 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_3.setGeometry(QtCore.QRect(550, 210, 250, 22))
        self.checkBox_3.setObjectName("checkBox_3")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(30, 80, 490, 27))
        self.lineEdit.setObjectName("lineEdit")
        # self.lineEdit.textChanged.connect(self.set_data)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 839, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.configUI()
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "IRIS-C Message Protocol Emulator"))
        self.pushButton.setText(_translate("MainWindow", "Scan Ports"))
        self.pushButton_2.setText(_translate("MainWindow", "CONNECT"))
        self.pushButton_3.setText(_translate("MainWindow", "Transmit"))
        self.pushButton_5.setText(_translate("MainWindow", "Clear"))
        self.pushButton_vout.setText(_translate("MainWindow", "Enable Video Out"))
        self.groupBox.setTitle(_translate("MainWindow", "Repeated Tx"))
        self.pushButton_4.setText(_translate("MainWindow", "Transmit x"))
        self.pushButton_stop.setText(_translate("MainWindow", "Stop_Tx"))
        self.label.setText(_translate("MainWindow", ""))
        self.label_2.setText(_translate("MainWindow", "Select Device"))
        self.label_3.setText(_translate("MainWindow", "Data to Transmit"))
        self.checkBox.setText(_translate("MainWindow", "Show Raw Data"))
        self.checkBox_2.setText(_translate("MainWindow", "Show Received Message Struct."))
        self.checkBox_3.setText(_translate("MainWindow", "Show Tx Data"))

    def configUI(self):
        self.comboBox_3.addItems(self.baud_list)
        self.scan_ports()
        self.comboBox.addItems(self.command_list)
        self.lineEdit.setText("00")
    
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


    def enable_vidout(self):
        self.serial.write_serial("$zvduo\r\n".encode("utf-8"))

    def set_baud(self):
        self.serial_baud = int(self.comboBox_3.currentText())
        
    def set_cmd(self):
        self.cmd = int(self.comboBox.currentText(), 16)

    def set_interval(self):
        self.interval = float(self.doubleSpinBox.text())
    
    def set_repeats(self):
        self.repeats = int(self.spinBox.text())

    def set_data(self):
        tmp = self.lineEdit.text()
        tmp = tmp.split(" ")
        if tmp[0] == "@":
            lat = float(tmp[1]) * 200000
            long = float(tmp[2]) * 200000
            alt = float(tmp[3]) * 200000
            hacc = float(tmp[4]) * 200000
            lat = f"{int(lat):x}"
            long = f"{int(long):x}"
            alt = f"{int(alt):x}"
            hacc = f"{int(hacc):x}"
            while(len(lat)<8):
                lat = "0"+ lat
            while(len(long)<8):
                long = "0" + long
            while(len(alt)<8):
                alt = "0" + alt
            while(len(hacc)<8):
                hacc = "0" + hacc
            lat = [lat[i:i+2] for i in range(0,len(lat),2)]
            long = [long[i:i+2] for i in range(0,len(long),2)]
            alt = [alt[i:i+2] for i in range(0,len(alt),2)]
            hacc = [hacc[i:i+2] for i in range(0,len(hacc),2)]
            suma = lat+long+alt+hacc
            self.data = [int(suma[i],16) for i in range(0,len(suma))]
            print(self.data)
        else:   
             self.data = [int(tmp[i],16) for i in range(0,len(tmp))]
             print("Data: ",self.data)

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
                self.pushButton_3.setEnabled(False)
                self.pushButton_4.setEnabled(False)
                self.pushButton_stop.setEnabled(False)
                self.pushButton_vout.setEnabled(False)
            else:
                self.pushButton_2.setStyleSheet("background-color: green")
                self.manager = Handler(self.serial, self.messager)
                self.log("Connected to Port", "green")
                self.connected_flag = True
                self.pushButton_3.setEnabled(True)
                self.pushButton_4.setEnabled(True)
                self.pushButton_stop.setEnabled(True)
                self.pushButton_vout.setEnabled(True)
        else:
            self.log("Disconnecting from Port", "red")
            self.messager.killsignal.emit(1)
            del self.manager
            self.serial.serial_disconnect()
            self.connected_flag = False
            self.pushButton_2.setStyleSheet("background-color: red")
            self.pushButton_3.setEnabled(False)
            self.pushButton_4.setEnabled(False)
            self.pushButton_vout.setEnabled(False)
        

# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     MainWindow = QtWidgets.QMainWindow()
#     ui = Ui_MainWindow()
#     ui.setupUi(MainWindow)
#     MainWindow.show()
#     sys.exit(app.exec_())


class Messager(QtCore.QObject):
    signal = QtCore.pyqtSignal(str)
    killsignal = QtCore.pyqtSignal(int)