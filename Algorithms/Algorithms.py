from collections import deque
from queue import PriorityQueue
import copy

class BFS():
    def __init__(self, maze):
        self.maze = maze
        self.frontier = []
        self.visited = []

        self.start, self.end = Get_Destination(self.maze)
        #Keep track of previous node, (Current Node) : Previous Node
        self.keep_track = dict()
        self.solution = []

    def Solve(self):
        self.frontier = deque([self.start])
        
        while True:
            cur_pos = self.frontier[0]

            next_move = Check_Valid_Move(self.maze, cur_pos, self.visited)
            self.visited.append(self.frontier.popleft())

            for move in next_move:
                self.frontier.append(move)

                self.keep_track[tuple(move)] = cur_pos

            if self.end in self.frontier:
                return

class DFS():
    def __init__(self, maze):
        self.maze = maze
        self.frontier = []
        self.visited = []

        self.start, self.end = Get_Destination(self.maze)
        self.keep_track = dict()
        self.solution = []

    def Solve(self):
        self.frontier = deque([self.start])
        while True:
            cur_pos = self.frontier[-1]
            next_move = Check_Valid_Move(self.maze, cur_pos, self.visited)
            self.visited.append(self.frontier.pop())

            for move in next_move:
                self.frontier.append(move)

                self.keep_track[tuple(move)] = cur_pos

            if self.end in self.frontier:
                return

class Dijkstra():
    def __init__(self, maze):
        pass

class AStar():
    def __init__(self, maze):
        self.maze = maze
        self.frontier = []
        self.visited = []

        self.start, self.end = Get_Destination(self.maze)
        self.keep_track = dict()
        self.solution = []

    def Solve(self):
        cost_map = Heuristic_Mapping(self.maze, self.end)

        step = 0

        #Each node in the frontier contains:
        #   - The heuristic value of the node
        #   - The position of the node
        #   - The amount of steps it takes to go from the start to the current position
        self.frontier = PriorityQueue()
        self.frontier.put((cost_map[self.start[0]][self.start[1]] + step, self.start, step))

        while self.frontier:
            #Get the current (heuristic_value, coordinates, old_step) and remove node from the frontier
            cur_vps = self.frontier.get()

            if self.end == cur_vps[1]:
                return
            
            next_move = Check_Valid_Move(self.maze, cur_vps[1], self.visited)
            self.visited.append(cur_vps[1])

            step = cur_vps[2] + 1

            for move in next_move:
                self.frontier.put((cost_map[move[0]][move[1]] + step, move, step))

                self.keep_track[tuple(move)] = cur_vps[1]

class GreedyBestFirst():
    def __init__(self, maze):
        self.maze = maze
        self.frontier = []
        self.visited = []

        self.start, self.end = Get_Destination(self.maze)
        self.keep_track = dict()
        self.solution = []

    def Solve(self):
        cost_map = Heuristic_Mapping(self.maze, self.end)

        #Each node in the frontier contains:
        #   - The heuristic value of the node
        #   - The position of the node
        self.frontier = PriorityQueue()
        self.frontier.put((cost_map[self.start[0]][self.start[1]], self.start))

        while True:
            #Get the current (heuristic value, coordinate) and remove node from the frontier
            cur_vp = self.frontier.get()
            
            if self.end == cur_vp[1]:
                return
            
            next_move = Check_Valid_Move(self.maze, cur_vp[1], self.visited)
            self.visited.append(cur_vp[1])

            for move in next_move:
                self.frontier.put((cost_map[move[0]][move[1]], move))

                self.keep_track[tuple(move)] = cur_vp[1]

def Get_Destination(maze: list[list[str]]) -> list[int]:
    '''
    - Input: A Text Maze
    - Output: [Start, End] Position of the maze
    '''
    row, col = len(maze), len(maze[0])

    destination = ['0', '0']

    for i in range(row):
        for j in range(col):
            if maze[i][j] == 'E':
                destination[0] = [i,j]
            elif maze[i][j] == 'S':
                destination[1] = [i,j]

    return destination

def Check_Valid_Move(maze: list[list[str]], cur_pos: list[int], visited: list[list[int]]):
    '''
    - Input:
        - A Maze
        - Current Position on the maze
        - The list of visited cells
    - Output:
        - All possible adjacent cells that hasn't been visited and not walls
    '''
    res = []

    moves_list = [[cur_pos[0] - 1, cur_pos[1]], [cur_pos[0] + 1, cur_pos[1]], [cur_pos[0], cur_pos[1] - 1], [cur_pos[0], cur_pos[1] + 1]]
    
    for move in moves_list:
        if move[0] < 0 or move[1] < 0:
            continue

        try:
            next_stage = maze[move[0]][move[1]]
        except IndexError:
            continue
        else:
            if ((next_stage == ' ') or (next_stage == 'S')) and ([move[0], move[1]] not in visited):
                res.append(move)

    return res

def Heuristic_Mapping(maze: list[list[str]], end: list[int]):
        '''
        Return a new maze that contains the heuristic value of each cells in the maze

        - The heuristic value of each cell is the Manhattan distance from its position to the end position
        '''
        cost_map = copy.deepcopy(maze)

        for i in range(len(cost_map)):
            for j in range(len(cost_map[0])):
                if cost_map[i][j] != '#':
                    cost_map[i][j] = abs(i - end[0]) + abs(j - end[1])

        return cost_map

def Get_Solution(solution, keep_track_array, start_position: list[int], end_position: list[int]):
    '''
    - Input:
        - A list named "solution" to write the solution to
        - An array which get a cell and returns the previous cell
        - The start, end positions of the maze
    - Output:
        - None
        (The result will be written into the "solution" list instead of returning anything)
    '''
    current_position = keep_track_array[tuple(end_position)]

    while current_position != start_position:
        solution.append(current_position)

        current_position = keep_track_array[tuple(current_position)]

    solution = solution[::-1]