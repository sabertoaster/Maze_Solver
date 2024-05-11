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
        
        
class DepthFirstSearch:
    def __init__(self, size_maze : tuple ):
        self.size = size_maze
        self.maze = [[Cell(i,j) for i in range(size_maze[1])] for j in range(size_maze[0])]
        self.visited = [[False for i in range(size_maze[1] + 5)] for j in range(size_maze[0] + 5)]
    
    def run(self, current_cell: tuple):
        self.visited[current_cell[0]][current_cell[1]] = True
        # đánh dấu ô này đã đi qua
        
        distance = [(0, -1), (-1, 0), (0, 1), (1, 0)]
        current_wall = ['left', 'top', 'right', 'bottom']
        next_wall = ['right', 'bottom', 'left', 'top']
        x, y = current_cell
        list_neighbors = [(x + dx, y + dy) for dx, dy in distance 
                          if x + dx >= 0 and x + dx < self.size[0] 
                          and y + dy >= 0 and y + dy < self.size[1]]
        # danh sách các ô kề với ô hiện tại
        
        if len(list_neighbors) == 0:
            return
        
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
        

class KruskalAlgorithm:
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
            
class WilsonAlgorithm:
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

class PrimAlgorithm:
    def __init__(self, size_maze):
        self.size = size_maze
        self.maze = [[Cell(j,i) for j in range(size_maze[1])] for i in range(size_maze[0])]

    def run(self):
        distance = [(0, -1), (-1, 0), (0, 1), (1, 0)]
        current_wall = ['left', 'top', 'right', 'bottom']
        next_wall = ['right', 'bottom', 'left', 'top']
        start = randint(0, self.size[0]), randint(0, self.size[1])
        visited = [[False for j in range(self.size[1] + 5)] for i in range(self.size[0] + 5)]
        x, y = start
        list_random_cell = [(x+dx, y+dy) for dx, dy in [(0, -1), (-1, 0), (0, 1), (1, 0)]
                              if x+dx >= 0 and x+dx < self.size[0]
                              and y+dy >= 0 and y+dy < self.size[1]
                              and visited[x+dx][y+dy] == False]
        visited[x][y] = True
                
        while len(list_random_cell) != 0:
            current_cell = choice(list_random_cell)
            list_random_cell.remove(current_cell)
            x, y = current_cell
            visited[x][y] = True
            list_neighbors = [(x+dx, y+dy) for dx, dy in [(0, -1), (-1, 0), (0, 1), (1, 0)]
                              if x+dx >= 0 and x+dx < self.size[0]
                              and y+dy >= 0 and y+dy < self.size[1]
                              and visited[x+dx][y+dy] == True]
            
            if len(list_neighbors) == 0:
                continue
            next_neighbor = choice(list_neighbors)
            iter = distance.index((next_neighbor[0] - current_cell[0], next_neighbor[1] - current_cell[1]))
            self.maze[current_cell[0]][current_cell[1]].walls[current_wall[iter]] = False
            self.maze[next_neighbor[0]][next_neighbor[1]].walls[next_wall[iter]] = False
            list_neighbors = [(x+dx, y+dy) for dx, dy in [(0, -1), (-1, 0), (0, 1), (1, 0)]
                              if x+dx >= 0 and x+dx < self.size[0]
                              and y+dy >= 0 and y+dy < self.size[1]
                              and visited[x+dx][y+dy] == False]
            
            for next_neighbor in list_neighbors:
                if next_neighbor not in list_random_cell:
                    list_random_cell.append(next_neighbor)            
                    
                    
class BinaryTreeAlgorithm:
    def __init__(self, size_maze):
        self.size = size_maze
        self.maze = [[Cell(j,i) for j in range(size_maze[1] + 5)] for i in range(size_maze[0] + 5)]                  
    
    def run(self):
        # East/ South
        for row in range(self.size[0]):
            for col in range(self.size[1]):
                if row == self.size[0] - 1 and col == self.size[1] - 1:
                    continue
                if row == self.size[0] - 1:
                    self.maze[row][col].walls['right'] = False
                    self.maze[row][col + 1].walls['left'] = False
                if col == self.size[1] - 1:
                    self.maze[row][col].walls['bottom'] = False
                    self.maze[row + 1][col].walls['top'] = False
                else:
                    wall = choice(['right', 'bottom'])
                    if wall == 'right':
                        self.maze[row][col].walls[wall] = False
                        self.maze[row][col + 1].walls['left'] = False
                    else:
                        self.maze[row][col].walls[wall] = False
                        self.maze[row + 1][col].walls['top'] = False
                #print(row, col, self.maze[row][col].walls)

def random_start_end(size):
    start = randint(0, size[0]), randint(0, size[1])
    end = randint(0, size[0]), randint(0, size[1])
    return start, end
class Maze:
    """
    type_generating_maze chọn một trong các ['DFS', 'Kruskal', 'Prim', 'Wilson']
    nếu ghi sai thì Maze sẽ random tự chọn kiểu
    
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
        Algorithm = ['DFS', 'Kruskal', 'Wilson', 'Prim','BinaryTree']
        if type_generating_maze not in Algorithm:
            type_generating_maze = choice(Algorithm)
        if type_generating_maze == 'DFS':
            tmp = DepthFirstSearch(size_maze)
            tmp.run((0,0))
            self.maze = tmp.maze
            self.size = size_maze          
        elif type_generating_maze == 'Kruskal':
            tmp = KruskalAlgorithm(size_maze)
            tmp.run()
            self.maze = tmp.maze
            self.size = size_maze
        elif type_generating_maze == 'Wilson':
            tmp = WilsonAlgorithm(size_maze)
            tmp.run()
            self.maze = tmp.maze
            self.size = size_maze
        elif type_generating_maze == 'Prim':
            tmp = PrimAlgorithm(size_maze)
            tmp.run()
            self.maze = tmp.maze
            self.size = size_maze
        elif type_generating_maze == 'BinaryTree':
            tmp = BinaryTreeAlgorithm(size_maze)
            tmp.run()
            self.maze = tmp.maze
            self.size = size_maze

ROW, COL = 20, 20
CELL_SIZE = 15

def Draw_Maze(self):
    for x in range(ROW):
        for y in range(COL):
            cell_rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)

            pygame.draw.rect(screen, (0,0,0), cell_rect)

            if self.maze[x][y].walls['top']:
                pygame.draw.line(screen, (255, 255, 255), [x * CELL_SIZE, y * CELL_SIZE], [(x + 1) * CELL_SIZE + 2, y * CELL_SIZE], width = 4)
            if self.maze[x][y].walls['bottom']:
                pygame.draw.line(screen, (255, 255, 255), [x * CELL_SIZE, (y + 1) * CELL_SIZE], [(x + 1) * CELL_SIZE + 2, (y + 1)* CELL_SIZE], width = 4)
            if self.maze[x][y].walls['left']:
                pygame.draw.line(screen, (255, 255, 255), [x * CELL_SIZE, y * CELL_SIZE], [x * CELL_SIZE, (y + 1) * CELL_SIZE], width = 4)
            if self.maze[x][y].walls['right']:
                pygame.draw.line(screen, (255, 255, 255), [(x + 1) * CELL_SIZE, y * CELL_SIZE], [(x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE], width = 4)

def Write_File(savepath, filename, maze: list[list[Cell]], maze_instance: Generate_Maze):
    maze_output = [[' ' for i in range(2 * COL - 1)] for j in range(2 * ROW - 1)]

    for x in range(ROW):
        for y in range(COL):
            if maze[x][y].walls['top'] and 2 * y - 1 >= 0:
                maze_output[2 * y - 1][2 * x] = '#'
            if maze[x][y].walls['bottom'] and 2 * y + 1 < 2 * ROW - 1:
                maze_output[2 * y + 1][2 * x] = '#'
            if maze[x][y].walls['left'] and 2 * x - 1 >= 0:
                maze_output[2 * y][2 * x - 1] = '#'
            if maze[x][y].walls['right'] and 2 * x + 1 < 2 * COL - 1:
                maze_output[2 * y][2 * x + 1] = '#'

            if 2 * x + 1 < 2 * ROW - 1 and 2 * y + 1 < 2 * COL - 1:
                maze_output[2 * y + 1][2 * x + 1] = '#'

    maze_output = maze_instance.Generate_Destination(maze_output)

    for x in range(2 * ROW - 2):
        maze_output[x] = ''.join(maze_output[x]) + '\n'
    maze_output[2 * ROW - 2] = ''.join(maze_output[2 * ROW - 2])

    completeName = os.path.join(savepath, filename)
    with open(completeName, mode = 'w') as file_output:
        file_output.write(''.join(maze_output))

    file_output.close()

# pygame.init()
# screen = pygame.display.set_mode((COL * CELL_SIZE + 4, ROW * CELL_SIZE + 4))

# Real_Maze = Generate_Maze()

# Real_Maze.Generate()

# Write_File('../LEGACY', 'maze6.txt', Real_Maze.maze, Real_Maze)


#Visualize

# Real_Maze.Draw_Maze()

# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()

#     pygame.display.update()
