import numpy as np
import pygame
from MazeGeneration import *
import matplotlib.pyplot as plt


list_cnt = []

WIDTH, HEIGHT = 602, 602
TILE = 60
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

class QLearning:
    def __init__(self):
        self.maze = Maze('Kruskal', (10, 10))
        self.actions = [(1, 0), (-1, 0), (0, -1), (0, 1)]
        self.epsilon = 0.1 # exploration rate
        self.alpha = 0.5 # learning rate
        self.gamma = 0.9 # discount factor
        self.QTable = np.zeros((self.maze.size[0], self.maze.size[1], len(self.actions)))
        
    def select_action(self, state):
        if np.random.rand() < self.epsilon:
            return np.random.choice(len(self.actions))
        else:
            return np.argmax(self.QTable[state[0], state[1]])
    
    def update_value(self, state, action, reward, next_state):
        self.QTable[state[0], state[1], action] += self.alpha * (reward + self.gamma * np.max(self.QTable[next_state[0], next_state[1]]) - self.QTable[state[0], state[1], action])
    
    
    def check_connect(self, state: tuple, next_state: tuple) -> bool:
        distance = [(0, -1), (-1, 0), (0, 1), (1, 0)]
        current_wall = ['left', 'top', 'right', 'bottom']
        next_wall = ['right', 'bottom', 'left', 'top']
        iter = distance.index((next_state[0] - state[0], next_state[1] - state[1]))
        if(self.maze.maze[state[0]][state[1]].walls[current_wall[iter]] == False and self.maze.maze[next_state[0]][next_state[1]].walls[next_wall[iter]] == False):
            return True
        return False
        
    def run_episode(self):
        self.maze.start = (0, 0)
        self.maze.end = (9, 9)
        state = self.maze.start
        total_reward = 0
        cnt = 0
        while state != self.maze.end:
            action = self.select_action(state)
            next_state = (state[0] + self.actions[action][0], state[1] + self.actions[action][1])
            reward = -1
            cnt += 1
            if self.check_connect(state, next_state) == False:
                reward = -5
                next_state = state
            elif next_state == self.maze.end:
                reward = 100
                
            self.update_value(state, action, reward, next_state)
            total_reward += reward
            state = next_state
        list_cnt.append(cnt)
        return total_reward

    def train(self, num_train):
        for episode in range(num_train):
            total_reward = self.run_episode()
            if (episode + 1) % 100 == 0:
                print("Episode:" , episode + 1, "Total_reward:", total_reward)
                
    def find_path(self):
        self.maze.start = (0, 0)
        self.maze.end = (9, 9)
        path = []
        policy = np.argmax(Q.QTable, axis=2)
        state = self.maze.start
        while state != self.maze.end:
            action = policy[state[0]][state[1]]
            path.append(state)
            state = state[0] + self.actions[action][0], state[1] + self.actions[action][1]
        path.append(state)
        return path
    
Q = QLearning()
Q.train(100)

#Display policy
path = Q.find_path()
print(len(path))

for i in range(10):
    for j in range(10):
        print('({}, {}) {:.2f} {:.2f} {:.2f} {:.2f}'.format(i, j, Q.QTable[i, j, 0], Q.QTable[i, j, 1], Q.QTable[i, j, 2], Q.QTable[i, j, 3]))


policy = np.argmax(Q.QTable, axis=2)
print("Policy:")
print(policy)
print(list_cnt)
plt.plot(list_cnt)
plt.xlabel('train')
plt.ylabel('cnt')
plt.show()



running = True
test = Q.maze


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    for i in range(test.size[0]):
        for j in range(test.size[1]):
            print_cell(test.maze[i][j])
            #print(test.maze[i][j].walls)
    print_path(path,test, 'red')
    
        
    pygame.display.update()
    fps_clock.tick(10)