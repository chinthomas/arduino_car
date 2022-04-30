import maze
import time
import interface
import argparse
import threading

# 這裡可以改預設參數 #
# default 後面 #
def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Arduino-Car Server")
    parser.add_argument('-p', '--port', default="COM4", help="the port of BT")
    parser.add_argument('-f', '--file', default="./data/E_maze.csv", help="the file of maze")
    parser.add_argument('--start', default="1", help="the start node")
    parser.add_argument('--end', default="0", help="the end node")
    parser.add_argument('--dir', default="N", help="the car direction")

    parser.add_argument('--mode', default="1", help="mode for get_action(diff. treasure order)")

    parser.add_argument('-t', '--test', help="test without connect to server", action="store_true")
    parser.add_argument('--bfs', help="only test the bfs", action="store_true")
    return parser

def get_action(carmaze:maze.bfs_maze, start:str, end:str, dir:str, mode:str='1')-> list:
    print(f"--- Analyze of Maze use mode{mode} ---")
    if mode == '0':
        entire_path, length = carmaze.bfs(start, end)
    elif mode == '1':
        entire_path, length = carmaze.bfs_all_maze(start)
    elif mode == '2':
        pass
    
    elif mode == '3':
        pass

    path, action = carmaze.get_dir(dir)
    print("Entire Path:", entire_path)
    print("Length:", length)
    print("Action:", action)
    print("")
    return action

def main(parser: argparse.ArgumentParser):
    args = parser.parse_args()
    
    ### analysis of maze ###
    carmaze = maze.bfs_maze(args.file)
    action = get_action(carmaze, mode=args.mode, start=args.start, end=args.end, dir=args.dir)
    # action = get_action(carmaze, '1', 'N', '0' ,'0', mode='1')
    if args.bfs:
        return False
    
    ### setup the interface for data transformation ###
    interf = interface.interface()
    interf.connect_BT(args.port)
    
    readThread = threading.Thread(target=interf.BT_write) # 還沒甚麼用
    readThread.daemon = True
    readThread.start()
    
    # time start
    interf.connect_server(args.test,'RFeasy') # 隊名這裡改

    # car start
    t_start = time.time()
    # action = ''                     # 直接指定用這行
    interf.send_action(action)        # 傳車子的動作指令

    while (time.time()-t_start) < 95: # 程式執行時間，結束後車子仍會跑，但python收不到UID
        interf.score()                # 讀UID並print分數

    ### gmae end ###
    print("interface end\n")
    interf.end_interface()
    

if __name__ =="__main__":
    parser = get_parser()
    main(parser)