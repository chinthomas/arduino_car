from score_test import Scoreboard #score.py
from score_student import Scoreboard_stu
import BluetoothSerial   #藍牙檔案
import time
import sys
import argparse

class interface:
    def __init__(self, port) -> None:
        self.ser = BluetoothSerial.bluetooth()
        while not self.ser.do_connect(port): pass
        print("BT Connected!")     

    def score(self):
        if self.ser.waiting():
            UID = self.ser.SerialreadString()
            UID = UID.replace('\n','')
            while len(UID) < 8:
                UID = '0' + UID
            self.upload_UID(UID)
            # print(hex(int(UID,16)))
            # print(f'Board~ we have {self.board.getCurrentScore()} point')

    def send_action(self, action):
        self.ser.Serialwrite(action)

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
        time.sleep(0.5)

    def upload_UID(self, UID):
        self.board.add_UID(UID)
        print("upload:", UID, "length:", len(UID),'\n')
        self.point = self.board.getCurrentScore()
    
    def end_interface(self):
        self.ser.Serialwrite("exit")
        self.ser.disconnect()

if __name__ == "__main__":
    def get_parser():
        parser = argparse.ArgumentParser(description="Arduino-Car Server")
        parser.add_argument('-p', '--port', default="COM8", help="the port of BT")
        return parser
    parser = get_parser()
    args = parser.parse_args()
    interf = interface(args.port)
    action = input("Please Give the Action To Car:")
    interf.connect_server(True)
    interf.send_action(action)
    t_start = time.time()
    while (time.time() - t_start) < 30:
        interf.score() 
    interf.end_interface()
