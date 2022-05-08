# main.py 使用方法 #
*通常可以直接在終端機操作程式，
*也可以進到main.py的檔案中直接更改參數的預設數值在執行。
*參數更改從get_parser()中更改，
*目前每一個參數都有預設，
*要注意的是藍牙的序列埠，很可能不一樣，用 -p 改。
*還有起使得方向，預設是朝北方，可以通過 --dir 更改(記得要大寫)
*程式操作時間我先調成95秒，測試時可以再更改。

# 功能說明 # 
***1. 連接正式的伺服器***
*用助教給的score.py連到http://140.112.175.15:3000 計時行動
*python main.py

***2. 連接local的伺服器***

*python main.py -t

***3. 測試BFS的運算成果(車車不會動)***
*python main.py --bfs

***4. 不同BFS的模式***
>* python main.py --mode MODE
>* mode 0 : 輸入起點、終點，和指定地圖，以最短路徑行走到終點
>* mode 1 : (預設模式)輸入起點，和指定地圖，隨機路線走完全部的寶藏點
>* mode 2 : 窮舉最短路徑
>* mode 3 : 遞迴求時間內最高分
>* mode 4 : 用stem-branch根據單位路徑的效率高低前進

***5. 其他參數***
>*   -h, --help            show this help message and exit
>*   -p PORT, --port PORT  the port of BT
>*   -f FILE, --file FILE  the file of maze
>*   --start START         the start node
>*   --end END             the end node(acquired when use mode 0)
>*   --dir DIR             the car direction( NSWE )
>*   --mode MODE           mode for get_action(diff. treasure order)
>*   -t, --test            test without connect to server
>*   --bfs                 only test the bfs


# 其他檔案 #
***maze.py*** 
* 分析地圖的演算法
* 裡面有比較多的註解
* (英文差敬請見諒)

***BluetoothSerial.py***
可以測試藍牙

***interface.py***
* Arduino、server和python間資料傳輸的設定

***score.py***
* 連接伺服器
***score_student.py***
* 連接local

***data(dir)***
* 存放地圖資料
* 存放local伺服器的UID分數(可加入新的UID)
