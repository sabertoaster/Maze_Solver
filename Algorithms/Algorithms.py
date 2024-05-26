from collections import deque
from queue import PriorityQueue
import copy

import heapq
# from Algorithms.MazeGeneration import *
import sys

class TotalAlgorithms:
    def __init__(self, maze: list[list[str]]):
        self.maze = maze

    def bfs(self, start: tuple[int], end: tuple[int]) -> tuple[list[tuple], list[tuple]]:
        if start == end:
            return None, None
        
        frontier = deque([start])
        visited = []
        trace = dict()
        
        while frontier:
            cur_pos = frontier[0]

            next_move = check_valid_move(self.maze, cur_pos, visited)
            visited.append(frontier.popleft())

            for move in next_move:
                frontier.append(move)

                trace[move] = cur_pos

            #When search ends, return the solution and visited list
            if end in frontier:
                return get_solution(trace, start, end), visited

    def dfs(self, start: tuple[int], end: tuple[int]) -> tuple[list[tuple], list[tuple]]:
        if start == end:
            return None, None
        
        frontier = deque([start])
        visited = []
        trace = dict()

        while frontier:
            cur_pos = frontier[-1]
            next_move = check_valid_move(self.maze, cur_pos, visited)
            visited.append(frontier.pop())

            for move in next_move:
                frontier.append(move)

                trace[move] = cur_pos

            if end in frontier:
                return get_solution(trace, start, end), visited
            
    #Greedy best first search
    def greedy(self, start: tuple[int], end: tuple[int]) -> tuple[list[tuple], list[tuple]]:
        if start == end:
            return None, None
        
        cost_map = heuristic_mapping(self.maze, end)
        visited = []
        trace = dict()

        #Each node in the frontier contains:
        #   - The heuristic value of the node
        #   - The position of the node
        frontier = PriorityQueue()
        frontier.put((cost_map[start[0]][start[1]], start))

        while frontier:
            #Get the current (heuristic value, coordinate) and remove node from the frontier
            cur_vp = frontier.get()
            
            if end == cur_vp[1]:
                return get_solution(trace, start, end), visited
            
            next_move = check_valid_move(self.maze, cur_vp[1], visited)
            visited.append(cur_vp[1])

            for move in next_move:
                frontier.put((cost_map[move[0]][move[1]], move))

                trace[move] = cur_vp[1]
            
    def a_star(self, start: tuple[int], end: tuple[int]) -> tuple[list[tuple], list[tuple]]:
        if start == end:
            return None, None
        
        cost_map = heuristic_mapping(self.maze, end)

        step = 0

        #Each node in the frontier contains:
        #   - The heuristic value of the node
        #   - The position of the node
        #   - The amount of steps it takes to go from the start to the current position
        frontier = PriorityQueue()
        frontier.put((cost_map[start[0]][start[1]] + step, start, step))

        visited = []

        trace = dict()

        while frontier:
            #Get the current (heuristic_value, coordinates, old_step) and remove node from the frontier
            cur_vps = frontier.get()

            if end == cur_vps[1]:
                return get_solution(trace, start, end), visited
            
            next_move = check_valid_move(self.maze, cur_vps[1], visited)
            visited.append(cur_vps[1])

            step = cur_vps[2] + 1

            for move in next_move:
                frontier.put((cost_map[move[0]][move[1]] + step, move, step))

                trace[move] = cur_vps[1]

    def dijkstra(self, start: tuple[int], end: tuple[int]) -> tuple[list[tuple], list[tuple]]:
        if start == end:
            return None, None
        
        priority = PriorityQueue()
        priority.put((0, start))
        distance = {start : 0}

        visited = []
        trace = dict()
        
        while not priority.empty():
            current_cost, current_cell = priority.get()

            visited.append(current_cell)
            
            if current_cost != distance[current_cell]:
                continue
            
            if current_cell == end:
                break
            
            next_move = check_valid_move(self.maze, current_cell, visited)

            for next_neighbor in next_move:
                if (next_neighbor not in distance or distance[next_neighbor] > distance[current_cell] + 1):
                    distance[next_neighbor] = distance[current_cell] + 1
                    trace[next_neighbor] = current_cell
                    priority.put((distance[next_neighbor], next_neighbor))
        
        return get_solution(trace, start, end), visited
    
    def path_energy(self, cur_energy, start: tuple[int], end: tuple[int]) -> tuple[list[tuple], list[tuple]]:
        if start == end:
            return None, None
        
        priority = PriorityQueue()
        priority.put((0, start, cur_energy))
        distance = {(start, cur_energy) : 0}

        visited = []
        trace = dict()
        
        while not priority.empty():
            current_cost, current_cell, current_energy = priority.get()

            visited.append(current_cell)
            
            if current_cost != distance[(current_cell, current_energy)]:
                continue
            
            if current_energy <= 0:
                continue
            if current_cell == end:
                break
            
            next_move = check_valid_move(self.maze, current_cell, visited)

            for next_neighbor in next_move:
                if self.maze[next_neighbor[0]][next_neighbor[1]] in ['1', '2', '3', '4', '5']:
                    tmp_energy = current_energy - 1 + int(self.maze[next_neighbor[0]][next_neighbor[1]])
                else:
                    tmp_energy = current_energy - 1
                if ((next_neighbor, tmp_energy) not in distance or distance[(next_neighbor, tmp_energy)] > distance[(current_cell, current_energy)] + 1):
                    distance[(next_neighbor, tmp_energy)] = distance[(current_cell, current_energy)] + 1
                    trace[next_neighbor] = current_cell
                    priority.put((distance[(next_neighbor, tmp_energy)], next_neighbor, tmp_energy ))
        
        if end not in visited:
            return None, None 
        return get_solution(trace, start, end), visited
    
def check_valid_move(maze: list[list[str]], cur_pos: tuple[int], visited: list[tuple[int]]):
    '''
    - Input:
        - A Maze
        - Current Position on the maze
        - The list of visited cells
    - Output:
        - All possible adjacent cells that hasn't been visited and not walls
    '''
    res = []

    moves_list = [(cur_pos[0] - 1, cur_pos[1]), (cur_pos[0] + 1, cur_pos[1]), (cur_pos[0], cur_pos[1] - 1), (cur_pos[0], cur_pos[1] + 1)]
    
    for move in moves_list:
        if move[0] < 0 or move[1] < 0:
            continue

        try:
            next_stage = maze[move[0]][move[1]]
        except IndexError:
            continue
        else:
            if (next_stage != '#') and ((move[0], move[1]) not in visited):
                res.append(move)

    return res

def heuristic_mapping(maze: list[list[str]], end: tuple[int]):
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

def get_solution(trace_path: dict, start: tuple[int], end: tuple[int]):
    '''
    - Input:
        - An array which get a cell and returns the previous cell
        - The start, end positions of the maze
    - Output:
        - None
        (The result will be written into the "solution" list instead of returning anything)
    '''
    current_position = trace_path[end]

    solution = []

    while current_position != start:
        solution.append(current_position)

        current_position = trace_path[current_position]

    return solution[::-1]
