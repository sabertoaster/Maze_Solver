import random, sys, os
import pygame
from random import choice
from random import shuffle
from random import randint


sys.setrecursionlimit(15000)
class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = {'top': True, 'bottom': True, 'right': True, 'left': True}
        
            
class DepthFirstSearchGeneration:
    def __init__(self, size_maze : tuple ):
        self.size = size_maze
        self.maze = [[Cell(i,j) for i in range(size_maze[1])] for j in range(size_maze[0])]
        self.visited = [[False for i in range(size_maze[1])] for j in range(size_maze[0])]
    
    def run(self, current_cell: tuple):
        self.visited[current_cell[0]][current_cell[1]] = True
        # đánh dấu ô này đã đi qua
        
        distance = [(0, -1), (-1, 0), (0, 1), (1, 0)]
        current_wall = ['left', 'top', 'right', 'bottom']
        next_wall = ['right', 'bottom', 'left', 'top']
        x, y = current_cell
        list_neighbors = [(x + dx, y + dy) for dx, dy in distance 
                          if x + dx >= 0 and x + dx < self.size[0] and y + dy >= 0 and y + dy < self.size[1] ]
        # danh sách các ô kề với ô hiện tại
        shuffle(list_neighbors)
        # trộn danh sách lên  => khỏi phải random 1 ô :))
        
        for next_neighbor in list_neighbors:
            if self.visited[next_neighbor[0]][next_neighbor[1]] == False:
                # Nếu ô này chưa được đi qua 
                iter = distance.index((next_neighbor[0] - current_cell[0], next_neighbor[1] - current_cell[1]))
                # xác định mối qua hệ thông qua distance (lên, xuống , phải, trái)
                self.maze[current_cell[0]][current_cell[1]].walls[current_wall[iter]] = False
                self.maze[next_neighbor[0]][next_neighbor[1]].walls[next_wall[iter]] = False
                #xóa bỏ phần tường giữa hai ô
                self.run(next_neighbor)
                # tiếp tục đi qua ô tiếp theo
        

class KruskalAlgorithmGeneration:
    def __init__(self, size_maze : tuple ):
        self.size = size_maze
        self.maze = [[Cell(i,j) for i in range(size_maze[1])] for j in range(size_maze[0])]
        self.parent = [ (i * self.size[1] + j) for i in range(self.size[0]) for j in range(self.size[1])]
        self.sz = [1] * (self.size[0] * self.size[1])
    
    def find(self, vertex: int):
        # tìm đỉnh cha của đỉnh hiện tại
        if vertex == self.parent[vertex]:
            return vertex
        self.parent[vertex] = self.find(self.parent[vertex])
        return self.parent[vertex]
    
    def join(self, vertex1: int, vertex2: int):
        # gộp 2 đỉnh thành 1
        vertex1, vertex2 = self.find(vertex1), self.find(vertex2)
        if vertex1 == vertex2:
            return 
        # tối ưu thông qua mảng sz
        if self.sz[vertex1] < self.sz[vertex2]:
            vertex1, vertex2 = vertex2, vertex1
        self.parent[vertex2] = vertex1
        self.sz[vertex1] += self.sz[vertex2]
    
    def run(self):
        visited_cell = [(i, j) for i in range(self.size[0]) for j in range(self.size[1])]        
        # danh sách vị trí các đỉnh , mỗi đỉnh là một ô
        while len(visited_cell) != 0:
            current_cell = choice(visited_cell) if visited_cell else False
            
            # chọn ngẫu nhiên ra một ô
            
            distance = [(0, -1), (-1, 0), (0, 1), (1, 0)]
            current_wall = ['left', 'top', 'right', 'bottom']
            next_wall = ['right', 'bottom', 'left', 'top']
            
            x, y = current_cell
            list_neighbors = [(x + dx, y + dy) for dx, dy in distance 
                              if x + dx >= 0 and x + dx < self.size[0] and y + dy >= 0 and y + dy < self.size[1] 
                              and self.find( (x * self.size[1] + y)) != self.find( ((x + dx) * self.size[1] + y + dy)) ]
            
            # danh sách kề với ô vừa sinh ngẫu nhiên
            
            if len(list_neighbors) == 0:
                visited_cell.remove(current_cell)
                # nếu như cả bốn ô xung quanh đều cùng đỉnh cha với đỉnh hiện tại thì ko cần nối đỉnh nữa
                continue
            next_neighbor = choice(list_neighbors)
            # chọn một đỉnh xung qua đỉnh vừa sinh ngẫu nhiên, lúc này ta có 2 đỉnh ngẫu nhiên kề nhau
            iter = distance.index((next_neighbor[0] - current_cell[0], next_neighbor[1] - current_cell[1]))
            # xác định xem (lên , xuống, phải, trái)
            self.maze[current_cell[0]][current_cell[1]].walls[current_wall[iter]] = False
            self.maze[next_neighbor[0]][next_neighbor[1]].walls[next_wall[iter]] = False            
            # xóa tường giữa hai ô
            self.join((current_cell[0] * self.size[1] + current_cell[1]),(next_neighbor[0] * self.size[1] + next_neighbor[1]))
            #gộp hai đỉnh thành một
            
class WilsonAlgorithmGeneration:
    def __init__(self, size_maze):
        self.size = size_maze
        self.maze = [[Cell(j,i) for j in range(size_maze[1])] for i in range(size_maze[0])]

    def run(self):
        visited_cell = [(i, j) for i in range(self.size[0]) for j in range(self.size[1])] 
        start = choice(visited_cell)
        # chọn một ô ngẫu nhiên
        visited_cell.remove(start)
        # cho ô đó là ô đã visited
        
        distance = [(0, -1), (-1, 0), (0, 1), (1, 0)]
        current_wall = ['left', 'top', 'right', 'bottom']
        next_wall = ['right', 'bottom', 'left', 'top']
        
        while len(visited_cell) != 0 :
            # còn ô chưa có đường thăm qua
            path = [choice(visited_cell)]
            # chọn ngẫu nhiên một ô
            while path[-1] in visited_cell:
                
                x, y = path[-1]
                neighbors = [(x+dx, y+dy) for dx, dy in distance
                         if 0 <= x+dx < self.size[0] and 0 <= y+dy < self.size[1]]
                #danh sách kề với ô sinh ngẫu nhiên
                path.append(choice(neighbors))
                # them ô này vào đường đi
                if path.count(path[-1]) > 1:
                    # nếu ô này lập lại thành chu trình thì bỏ chu trình bố ra khỏi path
                    path = path[:path.index(path[-1])+1]


            for i in range(len(path) - 1):
                # tiến hành đánh dấu ô đã visited
                # xóa các tường ở những ô trong đường đi
                current_cell = path[i]
                next_neighbor = path[i + 1]
                iter = distance.index((next_neighbor[0] - current_cell[0], next_neighbor[1] - current_cell[1]))
                self.maze[current_cell[0]][current_cell[1]].walls[current_wall[iter]] = False
                self.maze[next_neighbor[0]][next_neighbor[1]].walls[next_wall[iter]] = False
                visited_cell.remove(current_cell)


def random_start_end(size):
    start = randint(0, size[0]), randint(0, size[1])
    end = randint(0, size[0]), randint(0, size[1])
    return start, end
class Maze:
    """_summary_
    
    return self.size    -> tuple() : dòng trước, cột sau
    
    return mảng 2 chiều với mỗi phần tữ trong mảng là một class cell
    ví dụ 
    self.maze[i][j] -> ô tại dòng i cột j
    self.maze[i][j].x    -> tọa độ x tại ô dòng i cột j
    self.maze[i][j].y    -> tọa độ y tại ô dòng i cột j
    Lưu ý i, j là tọa độ của mảng 2 chiều, còn x, y là tọa độ trên màn hình để vẽ 
    self.maze[i][j].walls = {'top': False, 'bottom': True, 'right': True, 'left': True}
    nếu self.maze[i][j].walls['top'] == False => bên trên ô đó không có bức tường  |__|
                                                                             __        
    nếu self.maze[i][j].walls['top'] == True => bên trên ô đó có bức tường  |__|
    """
    def __init__(self, type_generating_maze : str, size_maze : tuple):
        self.start, self.end = random_start_end(size_maze)
        if type_generating_maze == 'DFS':
            tmp = DepthFirstSearchGeneration(size_maze)
            tmp.run(self.start)
            self.maze = tmp.maze
            self.size = size_maze
            
        elif type_generating_maze == 'Kruskal':
            tmp = KruskalAlgorithmGeneration(size_maze)
            tmp.run()
            self.maze = tmp.maze
            self.size = size_maze
        elif type_generating_maze == 'Wilson':
            tmp = WilsonAlgorithmGeneration(size_maze)
            tmp.run()
            self.maze = tmp.maze
            self.size = size_maze
