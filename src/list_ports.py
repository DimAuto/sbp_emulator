import serial
from serial.tools import list_ports

device = list(list_ports.comports())
for dev in device:
    try:
        print(f"{dev.device} | hwid:{dev.hwid} | Serial:{dev.serial_number} | desc:{dev.description}")
    except Exception as e:
        print(f"Error: {str(e)}")
        