import pygame
from MazeGeneration import *
from Algorithms import depth_first_search
from Algorithms import breadth_first_search
from Algorithms import dijkstra
from Algorithms import astar


WIDTH, HEIGHT = 602, 602
TILE = 12
rows, cols = HEIGHT // TILE, WIDTH // TILE
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
fps_clock = pygame.time.Clock()
running = True
test = Maze('BinaryTree', (50, 50))
#path1 = depth_first_search(test, (0,0), (49, 49))
path2 = astar(test, (0,0), (0, 49))


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    for i in range(test.size[0]):
        for j in range(test.size[1]):
            print_cell(test.maze[i][j])
            print(test.maze[i][j].walls)
    #print_path(path1,test, 'red')
    print_path(path2,test, 'yellow')
    
        
    pygame.display.update()
    fps_clock.tick(10)