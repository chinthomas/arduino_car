import copy
class ShortestPath:
    """
        infromation of node
    """
    def __init__(self, start:str, end:str, point: int, bfspath:list,length:int, action:str) -> None:
        time_list = {'s':1.6, 't':1.47, 'r':1.27, 'l':1.27} # 直走轉彎的時間資訊
        self.start= start       # 起點
        self.end = end          # 終點
        self.point = point      # 分數
        self.path = bfspath     # 路徑節點順序
        self.length = length    # 路徑長度
        self.action = action    # path action，路徑的前後左右迴轉
        self.usetime = 0.0      # 記錄總共使用的時間
        for act in self.action:
            self.usetime += time_list[act]

    def __str__(self) -> str:
        returnstring = 'path  :' 
        returnstring += self.path[0]
        for i in self.path[1:]:
            returnstring+='->'
            returnstring+=i
        returnstring +='\n'
        returnstring +=f'action:{self.action}'
        returnstring +='\n'
        returnstring +=f'point :{self.point}'
        returnstring +='\n'
        returnstring +=f'length:{self.length}'
        returnstring +='\n'
        returnstring +=f'time  :{self.usetime}'
        returnstring +='\n'

        return  returnstring
    
    def __add__(self ,other):
        bfspath_s = copy.deepcopy(self.path)
        bfspath_o = copy.deepcopy(other.path)
        if len(self.action) == 0 and len(self.path)==0:
            action = other.action
            bfspath_s = bfspath_o
        else:
            for i in bfspath_o[1:]:
                bfspath_s.append(i)
            action = self.action+'t'+other.action[1:]
        return ShortestPath(self.start, other.end, self.point+other.point, bfspath_s, self.length+ other.length, action)

if __name__ == "__main__":

    path_a = ShortestPath('1','3',10,['1','2','3'],3,'srr')
    path_b = ShortestPath('3','8',10,['3','5','8'],3,'sll')
    path_c =path_a+path_b
    print(path_a)
    print(path_b)
    print(path_c)