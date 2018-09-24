import serial


def get_weight():
    try:
        ser = serial.Serial('COM8', 9600, timeout=20, )
        s = ser.read(100)  # read up to one hundred bytes
        print(s)
    except:
        print("fail to open serial port")


read = input("Leer l, cerrar c")
while read.lower() != "c":
    get_weight()
    read = input("Leer l, cerrar c")
