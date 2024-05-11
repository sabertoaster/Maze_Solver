import pygame
from MazeGeneration import *
# from Algorithms import depth_first_search
# from Algorithms import breadth_first_search
# from Algorithms import dijkstra
# from Algorithms import astar
from Algorithms import *

WIDTH, HEIGHT = 602, 602
TILE = 60
rows, cols = HEIGHT // TILE, WIDTH // TILE
pygame.init()
sc = pygame.display.set_mode((HEIGHT, WIDTH))
pygame.display.set_caption('Generating Maze')


def print_cell(self : Cell):
    x, y = self.x * TILE, self.y * TILE
    pygame.draw.rect(sc, pygame.Color('white'), (x, y, TILE, TILE))
    #pygame.draw.rect(sc, pygame.Color('gray'), (x, y, TILE, TILE))
    
    if self.walls['top']:
        pygame.draw.line(sc, pygame.Color('black'),(x, y), (x + TILE, y), 2)
    if self.walls['right']:
        pygame.draw.line(sc, pygame.Color('black'), (x + TILE, y), (x + TILE, y + TILE), 2)
    if self.walls['left']:
        pygame.draw.line(sc, pygame.Color('black'), (x, y), (x, y + TILE), 2)
    if self.walls['bottom']:
        pygame.draw.line(sc, pygame.Color('black'), (x, y + TILE), (x + TILE, y + TILE), 2)

def print_path(path: list[tuple], test: Maze, Color: str):
    for (i, j) in path:
        # print(i,j)
        x, y = test.maze[i][j].x * TILE, test.maze[i][j].y * TILE
        pygame.draw.rect(sc, pygame.Color(Color), (x , y , TILE , TILE ))
        if test.maze[i][j].walls['top']:
            pygame.draw.line(sc, pygame.Color('black'),(x, y), (x + TILE, y), 2)
        if test.maze[i][j].walls['right']:
            pygame.draw.line(sc, pygame.Color('black'), (x + TILE, y), (x + TILE, y + TILE), 2)
        if test.maze[i][j].walls['left']:
            pygame.draw.line(sc, pygame.Color('black'), (x, y), (x, y + TILE), 2)
        if test.maze[i][j].walls['bottom']:
            pygame.draw.line(sc, pygame.Color('black'), (x, y + TILE), (x + TILE, y + TILE), 2)

def draw_maze():
    cell_size = 15
    
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            ceil_rect = pygame.Rect(j * cell_size, i * cell_size, cell_size, cell_size)

            if maze[i][j] == ' ':
                pygame.draw.rect(sc, (255,255,255), ceil_rect)
            elif maze[i][j] == '#':
                pygame.draw.rect(sc, (0,0,0), ceil_rect)
            elif maze[i][j] == 'E':
                pygame.draw.rect(sc, (255,255,0), ceil_rect)
            elif maze[i][j] == 'S':
                pygame.draw.rect(sc, (255,0,0), ceil_rect)


fps_clock = pygame.time.Clock()
running = True
test = Maze('DFS', (10, 10))
#path1 = depth_first_search(test, (0,0), (49, 49))
Real_Maze = test

maze = convert(Real_Maze.maze, Real_Maze)

for x in range(2 * test.size[0] - 1):
    for y in range(2 * test.size[1] - 1):
        print(maze[x][y], end='')
    print()

for x in range(2 * test.size[0] - 1):
    for y in range(2 * test.size[1] - 1):
        if maze[x][y] == 'E':
            start = (x, y)
        if maze[x][y] =='S':
            end = (x, y)

Al = TotalAlgorithms(maze) 
print(start, end)
path, visited = Al.dijkstra(start, end)
print('path', path)

draw_maze()

finding_index = 0
cell_size = 15

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    # for i in range(test.size[0]):
    #     for j in range(test.size[1]):
    #         print_cell(test.maze[i][j])
            #print(test.maze[i][j].walls)
    #print_path(path1,test, 'red')
    #print_path(path2,test, 'yellow')
    
    if finding_index < len(path):
        position = path[finding_index]
        
        cell_rect = pygame.Rect(position[1] * cell_size, position[0] * cell_size, cell_size, cell_size)

        pygame.draw.rect(sc, (0,255,0), cell_rect)

        finding_index += 1
        
    pygame.display.update()
    fps_clock.tick(10)