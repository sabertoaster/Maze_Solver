from collections import deque
from queue import PriorityQueue
import pygame, sys, time
import copy
from Minimap import Minimap

class IO_Basics:
    #Open and get the maze from file
    def get_maze(self, filename):
        with open(file = filename, mode = 'r') as file_input:
            #Return a list that stores all the maze
            global maze
            maze = file_input.readlines()
            
            #Remove all the newline character from the data 
            #And transform each cell from string into list elements
            for line_index in range(len(maze)):
                maze[line_index] = [*maze[line_index].strip('\n')]

            file_input.close()

    #Write the solution into a new file
    def write_maze(self):
        pass

    def draw_maze(self):
        cell_size = 15
        
        for i in range(len(maze)):
            for j in range(len(maze[0])):
                ceil_rect = pygame.Rect(j * cell_size, i * cell_size, cell_size, cell_size)

                if maze[i][j] == ' ':
                    pygame.draw.rect(screen, (255,255,255), ceil_rect)
                elif maze[i][j] == '#':
                    pygame.draw.rect(screen, (0,0,0), ceil_rect)
                elif maze[i][j] == 'E':
                    pygame.draw.rect(screen, (255,255,0), ceil_rect)
                elif maze[i][j] == 'S':
                    pygame.draw.rect(screen, (255,0,0), ceil_rect)

class Solution:
    def __init__(self, maze):
        self.maze = maze
        self.row = len(maze)
        self.col = len(maze[0])
        self.start, self.end = self.get_destination()
        self.frontier = []
        self.visited = []
        self.solution = dict()

    def get_destination(self):
        destination = ['0', '0']

        for i in range(self.row):
            for j in range(self.col):
                if self.maze[i][j] == 'E':
                    destination[0] = [i,j]
                elif self.maze[i][j] == 'S':
                    destination[1] = [i,j]

        return destination
    
    def check_valid_move(self, cur_pos: list[int]):
        res = []

        moves_list = [[cur_pos[0] - 1, cur_pos[1]], [cur_pos[0] + 1, cur_pos[1]], [cur_pos[0], cur_pos[1] - 1], [cur_pos[0], cur_pos[1] + 1]]
        
        for move in moves_list:
            if move[0] < 0 or move[1] < 0:
                continue

            try:
                next_stage = self.maze[move[0]][move[1]]
            except IndexError:
                continue
            else:
                if (next_stage == ' ' or (next_stage == 'S')) and [move[0], move[1]] not in self.visited:
                    res.append(move)

        return res
    
    def move_dfs(self):
        self.frontier = deque([self.start])
        while True:
            cur_pos = self.frontier[-1]
            next_move = self.check_valid_move(cur_pos)
            self.visited.append(self.frontier.pop())

            for move in next_move:
                self.frontier.append(move)

                self.solution[tuple(move)] = cur_pos

            if self.end in self.frontier:
                return
            
    def move_bfs(self):
        self.frontier = deque([self.start])
        
        while True:
            cur_pos = self.frontier[0]

            next_move = self.check_valid_move(cur_pos)
            self.visited.append(self.frontier.popleft())

            for move in next_move:
                self.frontier.append(move)

                self.solution[tuple(move)] = cur_pos

            if self.end in self.frontier:
                return
            
    def heuristic_function(self):
        cost_map = copy.deepcopy(maze)

        for i in range(len(cost_map)):
            for j in range(len(cost_map[0])):
                if cost_map[i][j] != '#':
                    cost_map[i][j] = abs(i - self.end[0]) + abs(j - self.end[1])

        return cost_map

    def move_Greedy(self):
        cost_map = self.heuristic_function()

        self.frontier = PriorityQueue()
        self.frontier.put((cost_map[self.start[0]][self.start[1]], self.start))

        while True:
            #Get the current (heuristic value, coordinate) and remove node from the frontier
            cur_vp = self.frontier.get()
            
            if self.end == cur_vp[1]:
                return
            
            next_move = self.check_valid_move(cur_vp[1])
            self.visited.append(cur_vp[1])

            for move in next_move:
                self.frontier.put((cost_map[move[0]][move[1]], move))

    def move_A_star(self):
        cost_map = self.heuristic_function()
        step = 0

        self.frontier = PriorityQueue()
        self.frontier.put((cost_map[self.start[0]][self.start[1]] + step, self.start, step))

        while self.frontier:
            #Get the current (heuristic_value, coordinates, old_step) and remove node from the frontier
            cur_vps = self.frontier.get()

            if self.end == cur_vps[1]:
                return
            
            next_move = self.check_valid_move(cur_vps[1])
            self.visited.append(cur_vps[1])

            step = cur_vps[2] + 1

            for move in next_move:
                self.frontier.put((cost_map[move[0]][move[1]] + step, move, step))

                self.solution[tuple(move)] = cur_vps[1]
            
    def draw_solution(self):
        cell_size = 15

        current_position = self.solution[tuple(self.end)]
        while current_position != self.start:
            cell_rect = pygame.Rect(current_position[1] * cell_size, current_position[0] * cell_size, cell_size, cell_size)

            pygame.draw.rect(screen, (52, 229, 235), cell_rect)
            
            current_position = self.solution[tuple(current_position)]


#Initialize all the essences     
io = IO_Basics()
io.get_maze('maze2.txt')

cell_size = 15
row, col = len(maze), len(maze[0])

pygame.init()
screen = pygame.display.set_mode((col * cell_size, row * cell_size))
clock = pygame.time.Clock()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 200)


#Maze Solver

sol = Solution(maze)
sol.move_A_star()

screen.fill((0,0,0))

io.draw_maze()
# sol.draw_solution()

def play_with_AI():
    finding_index = 1
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if finding_index < len(sol.visited):
            position = sol.visited[finding_index]

            # cell_rect = pygame.Rect(position[1] * cell_size, position[0] * cell_size, cell_size, cell_size)

            # pygame.draw.rect(screen, (0,255,0), cell_rect)

            pygame.draw.circle(screen, (30, 50, 163), [int((position[1] + 0.5) * cell_size), int((position[0] + 0.5) * cell_size)], cell_size // 2 - 1)

            finding_index += 1
        else:
            sol.draw_solution()

        # pygame.time.wait(20)

        pygame.display.update()
        clock.tick(100)

class Player:
    def __init__(self, pos):
        self.pos = pos

    def move(self, key_down):
        if key_down == 'w':
            self.pos[0] -= 1
        if key_down == 'a':
            self.pos[1] -= 1
        if key_down == 's':
            self.pos[0] += 1
        if key_down == 'd':
            self.pos[1] += 1
        
    def draw_player(self):
        ceil_rect = pygame.Rect(self.pos[1] * cell_size, self.pos[0] * cell_size, cell_size, cell_size)

        pygame.draw.rect(screen, (255, 51, 255), ceil_rect)
    
    def remove_previous(self):
        ceil_rect = pygame.Rect(self.pos[1] * cell_size, self.pos[0] * cell_size, cell_size, cell_size)

        pygame.draw.rect(screen, (255, 255, 255), ceil_rect)

player = Player([30, 30])

resolution = (row * cell_size, col * cell_size)
minimap = Minimap(screen, maze, player, resolution)

def play_with_player():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                player.remove_previous()

                # if event.key == pygame.K_m:
                #     minimap.zoom()
                if event.key == pygame.K_w:
                    player.move('w')
                elif event.key == pygame.K_a:
                    player.move('a')
                elif event.key == pygame.K_s:
                    player.move('s')
                elif event.key == pygame.K_d:
                    player.move('d')
                
                player.draw_player()

                minimap.update()

        pygame.display.update()
        clock.tick(100)

play_with_player()