import csv
import copy
from shortestpath import ShortestPath
def bfs(adj_dict:dict, a:str, b:str, path_length = 1) -> tuple:
    """
    adj_dict = {
        index : [connect node,...],
        index : [...]...
    }
    """
    pivot = 0 # point to the node in the node_list
    visited = [a] # list the node we have visited
    dis_list = [0] # list the dis. of the node
    pre =[None] # list the previous node
    
    while(pivot < len(visited) and b not in set(visited)):
        node = visited[pivot]
        for item in adj_dict[node]:
            if item not in set(visited):
                # entend the node_list
                # get the info. we need
                visited.append(item)
                dis_list.append(dis_list[pivot] + path_length)
                pre.append(visited[pivot])
        pivot += 1 # move to next node in node_list
        
        # step by step check
        # print(visited,dis_list,pre,sep = '\n')
        # print('\n')
        
    # a, b is not connected
    if b not in set(visited):
        return ["no path"],0

    pivot = visited.index(b)
    bfspath = [b]
    dis = dis_list[pivot]
    while(pivot != 0):
        bfspath.append(pre[pivot])
        pivot = visited.index(pre[pivot])
    return bfspath[::-1], dis

class bfs_maze:
    def __init__(self, fname) -> None:
        """ 
            auto import csv table to self.maze
            and get header
            #start = ['node', 'direction']
            maze = [
                {'index' : 'node','North' : 'node','Sorth' : 'node', ...},
                {'index' : 'node','North' : 'node','Sorth' : 'node', ...},
                {'index' : 'node','North' : 'node','Sorth' : 'node', ...},...
            ] 
            
            header = 
            ['index', 'North', 'South', 'West', 'East', 'ND', 'SD', 'WD', 'ED']

            end_point = 
            ['node', 'node', ...]

            bfs_->
            path = 
            ['start', 'node', ..., 'end']


        """
        self.path = list()
        self.maze = list()
        self.endpoint = list()
        with open(fname, 'r', encoding='utf-8') as csvfile:
            rows = csv.DictReader(csvfile)
            self.header = rows.fieldnames
            for row in rows:
                i = 0
                for key in self.header[1:5]:
                    if row[key] > '0':
                        i += 1
                if i <= 1:
                    self.endpoint.append(row['index'])
                self.maze.append(row)
        self.start = self.endpoint[0]        

    def __str__(self) -> str:
        string = str()
        for item in self.header:
            if len(item) < 5:
                string += ' '*(5-len(item))
            string += item +','
        string += '\n'     
        for item in self.maze:
            for index in self.header:
                if len(item[index]) < 5:
                    string += ' '*(5-len(item[index]))
                string += item[index] +','
            string += '\n'
        return string

    def drawmaze(self) -> str:    
        pass


    ### get adjacent list only ###
    def find_adj(self) -> None:
        self.adj = dict()
        for row in self.maze:               # row = {'index' : 'node','North' : 'node','Sorth' : 'node', ...}
            self.adj[row['index']] = list()
            for dir in self.header[1:5]:    # dir : direction
                if (row[dir] != ''):        # find which direction is connected
                    self.adj[row['index']].append(row[dir])

    def find_adj_dis(self) -> None:
        # add node between a and b according to the distance
        def extend_path(a:str, b:str , dis:str) -> list:
            switch = False # a,b switch or not
            # let a < b
            if a > b :
                a,b = b,a
                switch = True
            path = [a]
            
            for l in range(1,int(dis)):
                path.append(a+b+str(l))
            path.append(b)
            
            if switch:
                return path[::-1]
            return path

        self.adj = dict()
        for row in self.maze:                                           # row = {'index' : 'node','North' : 'node','Sorth' : 'node', ...}
            self.adj[row['index']] = list()                             # 'node' : [...]
            for dir, dis in zip(self.header[1:5], self.header[5::]):    # dir : direction, dis : distance
                #do below four time : 
                if(row[dir] != ''):                                     # if direction is connected
                    path = extend_path(row['index'], row[dir], row[dis])# add node according to the distance
                    self.adj[row['index']].append(path[1])              # new node connect with index
                    for node in range(1,len(path)-1):                   # new node add into adjacent list
                        self.adj[path[node]] =  [path[node-1], path[node+1]]

    def find_point(self, start, w):
        """
            self.point = {
                'node':int(point),...
            }
        """
        treasure = copy.deepcopy(self.endpoint)
        treasure.remove(start)
        x0 = (int(start)-1)//w
        y0 = (int(start)-1)%w
        self.point = dict()
        self.point['0'] = 0 ### stategy2
        for i in treasure:
            x = (int(i)-1)//w
            y = (int(i)-1)%w
            self.point[i] = abs(x-x0)+abs(y-y0)
# -----------------------------------------------------------------------------------------------------
# 寶藏順序規劃
# -----------------------------------------------------------------------------------------------------

    def find_order(self, start_node)->list:
        """ 只有起點正確, endpoint=[result] """
        i_start = self.endpoint.index(start_node)
        self.endpoint = self.endpoint[i_start:]+self.endpoint[:i_start]
        return self.endpoint

    def find_order_exhuasive(self, start_node)->list:
        """ 
            窮舉出所有的寶藏順序, 
            endpoint=[
                [result1],
                [result2],...
            ]
        """
        def search(now:str, endpoint:list, path:list):
            ### 加上現在的node
            new_path=copy.deepcopy(path)
            new_path.append(now)
            ### 將寶藏點扣除
            copy_endpoint = copy.deepcopy(endpoint)
            copy_endpoint.remove(now)
            
            ### 迴圈終點
            if len(copy_endpoint)==0:
                # print(new_path)
                solution.append(new_path)
            ### 下一個node
            else:
                for i in copy_endpoint:
                    search(i, copy_endpoint, new_path)
        solution =[]
        endpoint = copy.deepcopy(self.endpoint)
        search(start_node, endpoint, [])
        self.endpoint = solution
        return solution

# -----------------------------------------------------------------------------------------------------
#  add path with different method
# -----------------------------------------------------------------------------------------------------
    ### 給任意兩點，回傳bfs最短路徑 ###
    def bfs(self, a, b) -> tuple:    # (path:list, length:int)
        self.find_adj()
        self.path, length = bfs(self.adj, a, b)
        return self.path, length
    
    ### 給任意兩點，回傳bfs最短路徑，加入距離為條件 ###
    def bfs_short(self, a, b) -> tuple:
        self.find_adj_dis()
        rowpath, length = bfs(self.adj, a, b)
        self.path = []
        for i in rowpath:
            if int(i) < 100:
                self.path.append(i)
        return self.path, length
    
    ### 給任意起點，隨機回傳走完地圖的路徑 ###
    def bfs_allmaze(self, start_node):
        self.find_order(start_node)     # 排好寶藏順序
        endpoint = self.endpoint[::-1]  # 使用pop所以list要顛倒
        start = endpoint.pop()
        entire_path = [start]           # 紀錄經過的node
        entire_length = 0               # 紀錄路徑長度
        while len(endpoint) > 0:        # 提出下一個節點，進行BFS
            end = endpoint.pop()
            path, length = self.bfs_short(start, end)
            # print(f'start:{start}, end:{end}, path: {path}')
            ### add node in entire_path
            entire_length += length     # 將結果累積紀錄
            for node in path[1:len(path)]:
                entire_path.append(node)
            start = end                 # 下一次

        self.path = entire_path
        return entire_path, entire_length
    
    ### 給任意起點，回傳走完地圖最短的路徑 ###
    def bfs_allmaze_length(self, start_node:str):
        self.find_order_exhuasive(start_node)
        solution_path = []
        solution_len = 0
        for treasure in self.endpoint:
            treasure = treasure[::-1]
            start = treasure.pop()
            entire_path = [start]
            entire_length = 0
            while len(treasure) > 0:
                end = treasure.pop()                
                path, length = self.bfs_short(start, end)
                entire_length += length
                for node in path[1:len(path)]:
                    entire_path.append(node)
                start = end
            if solution_len == 0:# compare length 
                solution_len = entire_length
                solution_path = entire_path
            elif solution_len > entire_length:
                solution_len = entire_length
                solution_path = entire_path
        self.path = solution_path
        return(solution_path, solution_len)

# ------------------------------------------------------------------------------------------------------------
# direction
# ------------------------------------------------------------------------------------------------------------
    ### 找出由a到b的方向 ###
    def node_dir(self, a:str, b:str) -> str:
        for row in self.maze:
            if row['index'] == a:                               # find index a
                for dir, d in zip(self.header[1:5], ['N', 'S', 'W', 'E']): # dir :keyword of maze's dict
                    if row[dir] == b:                                   #  d  :['N', 'S', 'W', 'E']
                            return d
        print(f'{a}, {b} not connected')
        return 'None'

    def get_dir(self, pos ='N') -> str:
        direction = {
            'N' : {'N': 's', 'S': 't', 'W': 'l', 'E': 'r'}, 
            'S' : {'N': 't', 'S': 's', 'W': 'r', 'E': 'l'}, 
            'W' : {'N': 'r', 'S': 'l', 'W': 's', 'E': 't'}, 
            'E' : {'N': 'l', 'S': 'r', 'W': 't', 'E': 's'}
        }
        path_turn = str()
        path_ns = str()
        path =self.path[::-1]
        node_a = path.pop()
        while len(path) > 0:
            node_b = path.pop()
            if int(node_b) < 100: # node_b < '111'???
                next_pos = self.node_dir(node_a, node_b)
                path_ns += next_pos
                path_turn += direction[pos][next_pos]
                pos = next_pos
                node_a = node_b
        return path_ns, path_turn

# ------------------------------------------------------------------------------------------------------------
# solution
# ------------------------------------------------------------------------------------------------------------

    def find_all_path(self, start_node) -> dict:
        """
            all_path = {
                a, b, node_list, length, action, time
            }
        """
        endpoint = copy.deepcopy(self.endpoint)
        all_path = list()
        while len(endpoint) > 1:
            start = endpoint.pop()
            path_infro = dict()
            for end in endpoint:
                self.path , length =self.bfs_short(start, end)
                path_infro['a']=min(start,end)
                path_infro['b']=max(start,end)
                path_infro['path']=self.path
                path_infro['length']=length
                all_path.append(path_infro)
                print(path_infro)

    def strategy1(self, start_node, pos, width):
        def search(now:ShortestPath, now_node:str, treasure_left:list,pos):
            treasure = copy.deepcopy(treasure_left)
            treasure.remove(now_node)
            if len(treasure) == 0 or now.usetime > 60:
                # print(now)
                if solution[0].point<now.point:
                    solution[0] = now
                if solution[0].point==now.point and solution[0].usetime > now.usetime:
                    solution[0] = now
            else:
                for next_node in treasure:
                    next_path , length = self.bfs_short(now_node, next_node)
                    dir, action = self.get_dir(pos)
                    next = now + ShortestPath(now_node, next_node, self.point[next_node], next_path, length, action)
                    search(next, next_node, treasure,pos)

        self.find_point(start_node, width)
        print(self.point)
        treasure = copy.deepcopy(self.endpoint)
        now = ShortestPath(start='0',end=start_node, point=0, bfspath=[], length=0, action='')
        solution = [now]
        search(now, start_node, treasure,pos)
        print(solution[0])
        return solution[0]
    
# ------------------------------------------------------------------------------------------------------------
    def strategy2(self, start_node, width):
        def analyze_stem(stem:list, treasure)->list:
            stem_point = dict()
            stem_connect = dict()
            for stemNode in stem:
                stem_point[stemNode]=0
                stem_connect[stemNode]=[]
            for endpoint in treasure:
                heff = 0
                hi = '0'
                for stemNode, stem_len in zip(stem, range(len(stem))):
                    n,l=self.bfs_short(stemNode,endpoint)
                    eff = self.point[endpoint] / (l+stem_len)
                    if eff > heff:
                        heff = eff
                        hi = stemNode
                    # print(endpoint, stemNode, eff)
                n,l=self.bfs_short(start_node,endpoint)
                stem_point[hi] += self.point[endpoint]/l # version2
                stem_connect[hi].append(endpoint)
            return stem_point, stem_connect

        def search(start_node, treasure):
            if len(treasure) == 1:
                return treasure
            elif len(treasure) == 0:
                return []
            
            highestNode = '0' # node of highest_node
            for i in treasure:# find highest point
                if self.point[i] > self.point[highestNode]:
                    highestNode = i
            treasure.remove(highestNode)
            
            stem , stem_length = self.bfs_short(start_node, highestNode)
            stem_point = dict() # [point/length,...]
            stem_connect = dict() # [[connected_treasure],...]
            stem_point ,stem_connect = analyze_stem(stem, treasure)
            stem_point[highestNode] = self.point[highestNode]/stem_length
            treasure_high = [] 
            treasure_low = []
            for node in stem:
                if stem_point[node] >= stem_point[highestNode]:
                    treasure_high += stem_connect[node]
                else:
                    treasure_low += stem_connect[node]
            # print(start_node, highestNode)
            # print(stem)
            # print(stem_point)
            # print(stem_connect)
            # print('')
            return search(start_node, treasure_high) + [highestNode] + search(highestNode, treasure_low)
        treasure = copy.deepcopy(self.endpoint)
        self.find_point(start_node, width)
        treasure.remove(start_node)
        print(treasure)
        treasure_order = search(start_node, treasure)
        print(f'treasure order:{treasure_order}')
        self.endpoint=[start_node] + treasure_order

        return self.bfs_allmaze(start_node)
if __name__ == "__main__":
    import time
    # test web : http://192.168.50.165:3000
    # maze = bfs_maze("./E_maze.csv")
    # maze = bfs_maze("./E_maze_random.csv")
    # maze = bfs_maze("medium_maze.csv")
    # maze = bfs_maze("maze.csv")

    def timer(func):
        def wrapped(*args, **kwargs):
            t_start = time.time()
            func(*args, **kwargs)
            print(f'timer : using {(time.time()-t_start):.6f}s\n')
        return wrapped

    @timer
    def test1(fname,a ,b ,pos='N'):
        print(f"--- BFS shortest path from node{a} to node{b} ---")
        
        maze = bfs_maze('./data/'+fname)
        maze_path, length = maze.bfs_short(a, b)
        print("Path list:",maze_path,)
        print("Length:", length)
        dir, action = maze.get_dir(pos)
        print("Car Action:" , action)

    @timer
    def test2(fname, start, pos='N'):    
        print(f"--- Show path to run {fname} from node{start}---")
        
        maze = bfs_maze('./data/'+fname)
        maze_path, length = maze.bfs_allmaze(start)
        print("Entire Path:", maze_path)
        print("Length:", length)
        dir, action = maze.get_dir(pos)
        print("entire action:" ,action)
    
    @timer
    def test3(fname, start, pos='N'):
        print(f"--- Show shortest paths in {fname} ---")
        maze = bfs_maze('./data/'+fname)
        maze_path, length = maze.bfs_allmaze_length(start)
        print("Entire Path:", maze_path)
        print("Length:", length)
        dir, action = maze.get_dir(pos)
        print("entire action:" ,action)
    @timer
    def test4(fname, start, pos='N'):
        print(f'--- Show all paths in {fname} ---')
        maze = bfs_maze('./data/'+fname)
        print(maze.endpoint)
        maze.strategy1(start,pos,6)
    
    def test5(fname, start, width, pos='N'):
        print(f'--- Use s2  solve {fname} ---')
        maze = bfs_maze('./data/'+fname)
        maze_path, length = maze.strategy2(start, width)
        print("Entire Path:", maze_path)
        print("Length:", length)
        dir, action = maze.get_dir(pos)
        print("entire action:" ,action)

    # test5("medium_maze.csv",'1', 3)
    # test5("maze.csv",'2', 5)
    test5("maze_8x6_1.csv",'6', 6)

    # test3("medium_maze.csv",'1')    
    # test4("maze.csv",'2','N')
    # test4("maze_8x6_1.csv",'6', 'W')
    # test3("maze_8x6_1.csv",'6', 'W')