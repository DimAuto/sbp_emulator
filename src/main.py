from serial_comm import SerialComm
import os
from PyQt5 import QtWidgets
from sbp_emulator import Messager
from sbp_emulator import Ui_Form as UI
import sys



if __name__ == "__main__": 
    ser = SerialComm() 
    messager = Messager()
    try:
        app = QtWidgets.QApplication(sys.argv)
        Form = QtWidgets.QWidget()
        ui = UI(ser, messager)
        ui.setupUi(Form)
        Form.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(str(e))
        os._exit(-1)
    finally:
        os._exit(-1)
         