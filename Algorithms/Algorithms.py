from collections import deque
from queue import PriorityQueue
import copy
import heapq
from MazeGeneration import *
import sys

sys.setrecursionlimit(15000)


def trace_path(trace: dict, goal: tuple) -> list[tuple]:
    """
    Returns:
        đường đi trong mê cung
        list[tuple]: [(1,2), (2,2), (3,2), (3,3)] mỗi tuple là (i, j) tọa độ trong mảng Maze 2 chiều 
    """
    path = []
    while goal != None:
        path.append(goal)
        goal = trace[goal]
    return path[::-1]


def check_connect(maze: Maze, current_cell: tuple, next_neighbor: tuple) -> bool:
    distance = [(0, -1), (-1, 0), (0, 1), (1, 0)]
    current_wall = ['left', 'top', 'right', 'bottom']
    next_wall = ['right', 'bottom', 'left', 'top']
    iter = distance.index((next_neighbor[0] - current_cell[0], next_neighbor[1] - current_cell[1]))
    if(maze.maze[current_cell[0]][current_cell[1]].walls[current_wall[iter]] == False and maze.maze[next_neighbor[0]][next_neighbor[1]].walls[next_wall[iter]] == False):
        return True
    return False


def breadth_first_search(maze: Maze, start: tuple, goal: tuple) -> list[tuple]:
    """_summary_
    Returns:
        đường đi trong mê cung
        list[tuple]: vs [(1,2), (2,2), (3,2), (3,3)] mỗi tuple là (i, j) tọa độ trong mảng Maze 2 chiều
    """
    trace = {start: None}
    queue = deque()
    queue.append(start)
    
    while len(queue) != 0:
        current_cell = queue.popleft()
        x, y = current_cell
        list_neighbors = [(x+dx, y+dy) for dx, dy in [(0, -1), (-1, 0), (0, 1), (1, 0)]
                          if x+dx >= 0 and x+dx < maze.size[0] 
                          and y+dy >= 0 and y+dy < maze.size[1]]
        
        for next_neighbor in list_neighbors:
            if check_connect(maze, current_cell, next_neighbor) and next_neighbor not in trace:
                trace[next_neighbor] = current_cell
                queue.append(next_neighbor)
    
    return trace_path(trace, goal)

    

def depth_first_search(maze: Maze, start: tuple, goal: tuple) -> list[tuple]:
    """_summary_
    Returns:
        đường đi trong mê cung
        list[tuple]: vs [(1,2), (2,2), (3,2), (3,3)] mỗi tuple là (i, j) tọa độ trong mảng Maze 2 chiều
    """
    trace = {start: None}
    
    
    def dfs(maze: Maze, current_cell: tuple):

        if goal in trace:
            return
        
        x, y = current_cell
        list_neighbors = [(x+dx, y+dy) for dx, dy in [(0, -1), (-1, 0), (0, 1), (1, 0)]
                          if x+dx >= 0 and x+dx < maze.size[0] 
                          and y+dy >= 0 and y+dy < maze.size[1]]
        for next_neighbor in list_neighbors:
            if (check_connect(maze, current_cell, next_neighbor) and next_neighbor not in trace):
                trace[next_neighbor] = current_cell
                dfs(maze, next_neighbor)

    dfs(maze, start)
    return trace_path(trace, goal)


def astar(maze: Maze, start: tuple, goal: tuple) -> list[tuple]:
        priority = []
        heapq.heappush(priority, (0, start))
        distance = {start : 0}
        trace = {start: None} 
        while len(priority) != 0:
        
            current_cost, current_cell = heapq.heappop(priority)
            
            if current_cell == goal:
                break
            
            x, y = current_cell
            list_neighbors = [(x + dx, y + dy) for dx, dy in [(0, -1), (-1, 0), (0, 1), (1, 0)]
                                if x + dx >= 0 and x + dx < maze.size[0] 
                                and y + dy >= 0 and y + dy < maze.size[1]]
            
            heuristic = lambda begin_point, end_point : (abs(begin_point[0] - end_point[0]) + abs(begin_point[1] - end_point[1]))
            
            for next_neighbor in list_neighbors:
                
                if (check_connect(maze, current_cell, next_neighbor) 
                    and (next_neighbor not in distance 
                         or distance[next_neighbor] > distance[current_cell] + 1)):
                    
                    distance[next_neighbor] = distance[current_cell] + 1
                    trace[next_neighbor] = current_cell            
                    heapq.heappush(priority,(distance[current_cell] + 1 + heuristic(next_neighbor, goal), (next_neighbor)))

        return trace_path(trace, goal)

def dijkstra(maze: Maze, start: tuple, goal: tuple) -> list[tuple]:
    
    priority = PriorityQueue()
    priority.put((0, start))
    distance = {start : 0}
    trace = {start: None}
    
    while not priority.empty():
        current_cost, current_cell = priority.get()
        
        if current_cost != distance[current_cell]:
            continue
        
        if current_cell == goal:
            break
        
        x, y = current_cell
        list_neighbors = [(x+dx, y+dy) for dx, dy in [(0, -1), (-1, 0), (0, 1), (1, 0)]
                          if x+dx >= 0 and x+dx < maze.size[0] 
                          and y+dy >=0 and y+dy < maze.size[1]]

        for next_neighbor in list_neighbors:
            if (check_connect(maze, current_cell, next_neighbor)
                and (next_neighbor not in distance 
                     or distance[next_neighbor] > distance[current_cell] + 1)):
                
                distance[next_neighbor] = distance[current_cell] + 1
                trace[next_neighbor] = current_cell
                priority.put((distance[next_neighbor], next_neighbor))
    
    return trace_path(trace, goal)
    

def greedy_best_first():
    pass 
    
