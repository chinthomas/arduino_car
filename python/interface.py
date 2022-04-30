from charset_normalizer import from_bytes
from score import Scoreboard #score.py
from score_student import Scoreboard_stu
import BluetoothSerial   #藍牙檔案
import time
import sys
import argparse

class interface:
    def __init__(self) -> None:
        self.ser = BluetoothSerial.bluetooth()

    def connect_BT(self, port) -> None:
        while not self.ser.do_connect(port): pass
        print("BT Connected!")

    def score(self):
        if self.ser.waiting():
            UID = self.ser.SerialreadString()
            UID = UID.replace('\n','')
            while len(UID) < 8:
                UID = '0' + UID
            self.upload_UID(UID)
            print(hex(int(UID,16)))
            print(f'Board~ we have {self.board.getCurrentScore()} point')

    def send_action(self, map):
        self.ser.Serialwrite(map)

    def BT_write(self)->None:
        while True:
            Msg = input()
            if Msg == "exit": sys.exit()
            self.ser.Serialwrite(Msg)

    def BT_read(self) -> None:
        while True:
            if self.ser.waiting(): 
                Msg = self.ser.SerialreadString()
                print(Msg)

    def connect_server(self, test, team_name='Team One'):
        if test:
            self.board = Scoreboard_stu('./data/UID.csv',team_name)
        else:
            self.board = Scoreboard('filepath',team_name)
        time.sleep(3)

    def upload_UID(self, UID):
        self.board.add_UID(UID)
        print("upload:", UID, "length:", len(UID))
        self.point = self.board.getCurrentScore()
    
    def end_interface(self):
        self.ser.Serialwrite("exit")
        self.ser.disconnect()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="interface test")
    parser.add_argument('-t', '--test', help="test without connect with server", action="store_true")
    args = parser.parse_args()

    car_interf = interface()
    car_interf.connect_BT("COM4")
    map = input("Please Give the Action To Car:")
    car_interf.connect_server(args.test)
    t_start = time.time()
    car_interf.send_action(map)
    UID = b'84EAB017'
    car_interf.upload_UID(hex(int.from_bytes(UID, byteorder='big', signed=False)))
    time.sleep(10)
    UID = b'0596E4D0'
    car_interf.upload_UID(UID)
    while (time.time() - t_start) < 95:
        if car_interf.ser.waiting():
            # UID = car_interf.ser.SerialReadByte()
            # car_interf.upload_UID(UID)
            car_interf.score()        
    car_interf.end_interface()
    # readThread = threading.Thread(target=car_interf.BT_write)
    # readThread.daemon = True
    # readThread.start()

    # car_interf.BT_read()