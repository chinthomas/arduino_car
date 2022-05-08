import maze
import time
import interface
import argparse
import threading
import sys

# 這裡可以改預設參數 #
# default 後面 #
def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Arduino-Car Server")
    parser.add_argument('-p', '--port', default="COM8", help="the port of BT")
    parser.add_argument('-f', '--file', default="./data/maze_8x6_1.csv", help="the file of maze")
    parser.add_argument('--start', default="1", help="the start node")
    parser.add_argument('--end', default="0", help="the end node")
    parser.add_argument('--dir', default="N", help="the car direction")

    parser.add_argument('--mode', default="1", help="mode for get_action(diff. treasure order)")

    parser.add_argument('-t', '--test', help="test without connect to server", action="store_true")
    parser.add_argument('--bfs', help="only test the bfs", action="store_true")
    return parser

def get_action(fname, start:str, end:str, dir:str, mode:str='1')-> list:
    carmaze = maze.bfs_maze(fname)
    print(f"--- Analyze of Maze use mode{mode} ---")
    if mode == '0':
        entire_path, length = carmaze.bfs(start, end)
    elif mode == '1':
        entire_path, length = carmaze.bfs_allmaze(start)
    elif mode == '2':
        entire_path, length = carmaze.bfs_allmaze_length(start)
    elif mode == '3':
        solution = carmaze.strategy1(start,dir,3) # modify width of the maze
        return solution.action
    elif mode == '4':
        entire_path, length = carmaze.strategy2(start,6) # modify width of the maze
    elif mode == '5':
        entire_path = carmaze.strategy4('6',6) # modify width of the maze
        length = '?'

    path, action = carmaze.get_dir(dir)
    print("Entire Path:", entire_path)
    print("Length:", length)
    print("Action:", action)
    print("")
    return action

def main(parser: argparse.ArgumentParser):
    args = parser.parse_args()
    action = get_action(args.file, mode=args.mode, start=args.start, end=args.end, dir=args.dir)
    if args.bfs:
        return 0

    ### setup the interface for data transformation ###
    interf = interface.interface(args.port)

    ans = input('ready to go?[y/n]')
    if ans in ['n', 'N']:print('cancel plan')
    
    ### start
    else:
        interf.connect_server(args.test,'RFeasy') # 隊名這裡改
        t_start = time.time()
        interf.send_action(action)                # 傳車子的動作指令
        while (time.time()-t_start) < 95:         # 程式執行時間，結束後車子仍會跑，但python收不到UID
            interf.score()                        # 讀UID並print分數

    ### gmae end ###
    print("Interface Deconnect\n")
    interf.end_interface()

if __name__ =="__main__":
    parser = get_parser()
    main(parser)