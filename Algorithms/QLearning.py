import numpy as np
import pygame
from MazeGeneration import *
import matplotlib.pyplot as plt

list_cnt = []
class QLearning:
    def __init__(self, maze : Maze):
        self.maze = maze
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
    
    
    
        
    def run_episode(self, start: tuple, end:tuple):
        self.maze.start = start
        self.maze.end = end
        state = self.maze.start
        total_reward = 0
        cnt = 0
        while state != self.maze.end:
            action = self.select_action(state)
            next_state = (state[0] + self.actions[action][0], state[1] + self.actions[action][1])
            reward = -1
            cnt += 1
            if self.maze.maze[next_state[0]][next_state[1]] == False:
                reward = -5
                next_state = state
            elif next_state == self.maze.end:
                reward = 100
                
            self.update_value(state, action, reward, next_state)
            total_reward += reward
            state = next_state
        list_cnt.append(cnt)
        return total_reward

    def train(self, num_train, start: tuple, end: tuple):
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
# print(len(path))

# for i in range(10):
#     for j in range(10):
#         print('({}, {}) {:.2f} {:.2f} {:.2f} {:.2f}'.format(i, j, Q.QTable[i, j, 0], Q.QTable[i, j, 1], Q.QTable[i, j, 2], Q.QTable[i, j, 3]))


# policy = np.argmax(Q.QTable, axis=2)
# print("Policy:")
# print(policy)
# print(list_cnt)
# plt.plot(list_cnt)
# plt.xlabel('train')
# plt.ylabel('cnt')
# plt.show()



running = True
test = Q.maze

