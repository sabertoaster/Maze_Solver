import random, sys, os
import pygame

ROW, COL = 20, 20
CELL_SIZE = 15

class Cell:
    '''
    An element of the maze, whose attributes:
    - [x,y]: The coordinate of the cell in the maze
    - Walls: Between 2 adjacent cells, Has 4 sides: Top, Bottom, Left, Right. Default is all True
    '''
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = {'top': True, 'bottom': True, 'left': True, 'right': True}

class Generate_Maze:
    '''
    - Init the maze whose elements is Cell
    - Init the visited list
    '''
    def __init__(self):
        self.maze = [[Cell(x,y) for y in range(COL)] for x in range(ROW)]
        self.visited = []

    #Return the coordinates of the valid neighbor cells
    def Valid_Moves(self, current_cell: Cell):
        moves = [[current_cell.x - 1, current_cell.y], [current_cell.x + 1, current_cell.y], [current_cell.x, current_cell.y - 1], [current_cell.x, current_cell.y + 1]]        

        res = []

        for move in moves:
            if move in self.visited:
                continue
            if move[0] < 0 or move[1] < 0 or move[0] > ROW - 1 or move[1] > COL - 1:
                continue

            res.append(move)

        return res
    
    #Return a randomly chosen coordinate from the valid neighbor cells
    def Choose_Move(self, current_cell: Cell):
        valid_moves = self.Valid_Moves(current_cell)

        if valid_moves:
            return random.choice(valid_moves)
        return False
    
    def Remove_Walls(self, current_cell: Cell, next_cell: Cell):
        dx = next_cell.x - current_cell.x
        dy = next_cell.y - current_cell.y

        if dx == 1:
            next_cell.walls['left'] = False
            current_cell.walls['right'] = False
        elif dx == -1:
            next_cell.walls['right'] = False
            current_cell.walls['left'] = False

        if dy == 1:
            next_cell.walls['top'] = False
            current_cell.walls['bottom'] = False
        elif dy == -1:
            next_cell.walls['bottom'] = False
            current_cell.walls['top'] = False

    def Generate(self):
        cur_cell = self.maze[0][0]
        
        #Store the previous node that has a non-visited neighbor
        keep_track = [self.maze[0][0]]

        #Initialize for the first move (Go below to get the full workflow)
        next_x, next_y = self.Choose_Move(cur_cell)

        next_cell = self.maze[next_x][next_y]
    
        self.Remove_Walls(cur_cell, next_cell)

        self.visited.append([0,0])
        self.visited.append([next_x, next_y])

        keep_track.append(next_cell)

        cur_cell = next_cell

        #From the second moves:
        while cur_cell != self.maze[0][0]:
            #Check if the current cell has any valid neighbor (Not visited)

            #If it has any valid neighbor, return a randomly chosen coordinate from valid neighbors
            if self.Choose_Move(cur_cell):
                #Get the current second move coordinate
                next_x, next_y = self.Choose_Move(cur_cell)
                #Then get its cell
                next_cell = self.maze[next_x][next_y]
            
                #Remove the walls between the current cell and the next cell
                self.Remove_Walls(cur_cell, next_cell)

                #Append the next cell into the visited list so that we only visit it once
                self.visited.append([next_x, next_y])

                #Keep track of the previous cell which has neighbor
                keep_track.append(cur_cell)

                #Go to the next cell
                cur_cell = next_cell

            #If it doesn't have any valid neighbor, we will go to the previous cell which has at least one neighbor
            else:
                cur_cell = keep_track.pop()
        #Eliminate the loop when the current cell return back to the start

    def Generate_Destination(self, maze):
        row, col = len(maze), len(maze[0])

        strategy = random.choice([0,1])

        if strategy == 0:
            x_start = random.randint(0, row - 1)
            y_start = 0

            x_end = random.randint(0, row - 1)
            y_end = col - 1

        elif strategy == 1:
            x_start = 0
            y_start = random.randint(0, col - 1)

            x_end = row - 1
            y_end = random.randint(0, col - 1)

        maze[x_start][y_start] = 'E'
        maze[x_end][y_end] = 'S'

        return maze

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

pygame.init()
screen = pygame.display.set_mode((COL * CELL_SIZE + 4, ROW * CELL_SIZE + 4))

Real_Maze = Generate_Maze()

Real_Maze.Generate()

Write_File('../LEGACY', 'maze6.txt', Real_Maze.maze, Real_Maze)


#Visualize

# Real_Maze.Draw_Maze()

# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()

#     pygame.display.update()