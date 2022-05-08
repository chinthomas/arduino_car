import threading
import time
import sys
import serial

class bluetooth:
    # def __init__(self, port: str, baudrate: int=9600):
    def __init__(self):

        """ Initialize an BT object, and auto-connect it. """
        # The port name is the name shown in control panel
        # And the baudrate is the communication setting, default value of HC-05 is 9600.
        # self.ser = serial.Serial(port, baudrate=baudrate)
        self.ser = serial.Serial()
        
    def is_open(self) -> bool:
        return self.ser.is_open

    def waiting(self) -> bool:
        return self.ser.in_waiting
    def disconnect(self):
        self.ser.close()

    def do_connect(self, port: str, baudrate: int=9600) -> bool:
        """ Connect to the specify port with particular baudrate """
        # Connection function. Disconnect the previous communication, specify a new one.
        self.ser.close()
        print("Connecting...")

        try:
            self.ser = serial.Serial(port, baudrate=9600, timeout=2)
            print("connect success\n")
            return True
        except serial.serialutil.SerialException:
            print("fail to connect\n")
            return False

    def Serialwrite(self, output: str) -> None:
        # Write the byte to the output buffer, encoded by utf-8.
        if output == "exit":sys.exit()
        send = output.encode("utf-8")
        self.ser.write(send)

    def SerialreadString(self) -> str:
        # Scan the input buffer until meet a '\n'. return none if doesn't exist.
        time.sleep(0.05)    # let msg fill the buffer
        if(self.waiting()):
            # receiveMsg = self.ser.readline().decode("utf-8")[:-1]            
            receiveMsg = self.ser.read(self.ser.inWaiting()).decode("utf-8")
            ### test the message we get ###
            # receiveMsg_b =self.ser.read(self.ser.inWaiting())
            # print('Row~', receiveMsg_b)
            # receiveMsg = receiveMsg_b.decode("utf-8")
            # print('Decode~', receiveMsg)
            # self.ser.flushInput()
            return receiveMsg


    def SerialReadByte(self):
        time.sleep(0.2)
        receiveMsg = self.ser.read(self.ser.inWaiting())
        if (receiveMsg):
            UID = hex(int.from_bytes(receiveMsg, byteorder='big', signed=False))
            print("Arduino~",receiveMsg)
            self.ser.flushInput() # refresh input buffer
            return UID
        else:
            return 0


if __name__ == "__main__":
    def read() -> None:
        while True:
            if bt.waiting():
                Msg = bt.SerialreadString()
                print(f'{Msg}')
                # TypeError: cannot convert 'str' object to bytes
                # print(hex(int.from_bytes(Msg, byteorder='big', signed=False)))

    def write() -> None:
        while True:
            msgWrite = input()
            if msgWrite == "exit": sys.exit()
            bt.Serialwrite(msgWrite)

    # Please modify the port name.
    port = "COM8"
    bt = bluetooth()
    # bt = bluetooth(port)
    while not bt.do_connect(port): pass
    print("BT Connected!")

    readThread = threading.Thread(target=read)
    readThread.daemon = True
    readThread.start()

    while True:
        msgWrite = input()
        if msgWrite == "exit": sys.exit()
        bt.Serialwrite(msgWrite)
