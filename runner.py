from collections import deque
import pygame, sys, time

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
                maze[line_index] = [*maze[line_index].strip()]

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
        self.start, self.end = self.get_start_position()
        self.frontier = deque([self.start])
        self.visited = [self.start]
        self.solution = [1]

    def get_start_position(self):
        start_pos = ['0', '0']

        for i in range(self.row):
            for j in range(self.col):
                if self.maze[i][j] == 'E':
                    start_pos[0] = [i,j]
                elif self.maze[i][j] == 'S':
                    start_pos[1] = [i,j]

        return start_pos
    
    def check_valid_move(self, cur_pos: list[int]):
        res = []

        moves_list = [[cur_pos[0] - 1, cur_pos[1]], [cur_pos[0] + 1, cur_pos[1]], [cur_pos[0], cur_pos[1] - 1], [cur_pos[0], cur_pos[1] + 1]]
        
        for move in moves_list:
            next_stage = self.maze[move[0]][move[1]]

            if (next_stage == ' ' or (next_stage == 'S')) and [move[0], move[1]] not in self.visited:
                res.append(move)

        return res
    
    def move(self):
        while bool(self.frontier):
            number_of_moves = 0 #Count the number of possible next moves

            cur_pos = self.frontier[-1]
            next_move = self.check_valid_move(cur_pos)
            self.visited.append(self.frontier.pop())

            for move in next_move:
                self.frontier.append(move)
                number_of_moves += 1

            self.solution.append(number_of_moves)

            if self.end in self.frontier:
                return
            
    def find_path(self):
        for i in range(len(self.solution)):
            if self.solution[i] == 0:
                cur_index = i
                prev_index = i - 1
                while prev_index >= 0 and self.solution[prev_index] <= 1:
                    if (abs(self.visited[cur_index][1] - self.visited[prev_index][1]) == 1) ^ (abs(self.visited[cur_index][0] - self.visited[prev_index][0]) == 1):
                        self.solution[prev_index] = 0
                        cur_index = prev_index
                    prev_index -= 1
                else:
                    self.solution[prev_index] -= 1
            
    def draw_solution(self):
        cell_size = 15

        for position in self.visited:
            cell_rect = pygame.Rect(position[1] * cell_size, position[0] * cell_size, cell_size, cell_size)

            pygame.draw.rect(screen, (0,255,0), cell_rect)

    def draw_final_solution(self):
        cell_size = 15

        for i in range(len(self.solution)):
            if self.solution[i] != 0:
                cell_rect = pygame.Rect(self.visited[i][1] * cell_size, self.visited[i][0] * cell_size, cell_size, cell_size)
                
                pygame.draw.rect(screen, (0,255,255), cell_rect)
            
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
sol.move()

screen.fill((0,0,0))

io.draw_maze()
sol.find_path()
# sol.draw_solution()

finding_index = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if finding_index < len(sol.visited):
        position = sol.visited[finding_index]

        cell_rect = pygame.Rect(position[1] * cell_size, position[0] * cell_size, cell_size, cell_size)

        pygame.draw.rect(screen, (0,255,0), cell_rect)

        finding_index += 1

    # pygame.time.wait(20)

    pygame.display.update()
    clock.tick(100)