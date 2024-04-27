import random

# Maze dimensions
ROWS = 50
COLS = 50

# Directions (N, E, S, W)
directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]

# Function to generate maze using Recursive Backtracking algorithm
def generate_maze(rows, cols):
    maze = [["#" for _ in range(cols)] for _ in range(rows)]
    stack = [(random.randint(0, cols - 1), random.randint(0, rows - 1))]

    while stack:
        x, y = stack[-1]
        maze[y][x] = " "
        neighbors = []

        for dx, dy in directions:
            nx, ny = x + dx * 2, y + dy * 2
            if 0 <= nx < cols and 0 <= ny < rows and maze[ny][nx] == "#":
                neighbors.append((nx, ny))

        if neighbors:
            nx, ny = random.choice(neighbors)
            maze[(y + ny) // 2][(x + nx) // 2] = " "
            stack.append((nx, ny))
        else:
            stack.pop()

    return maze

# Function to save maze to a text file
def save_maze_to_file(maze, filename):
    with open(filename, "w") as file:
        for row in maze:
            file.write("".join(row) + "\n")

# Generate maze
maze = generate_maze(ROWS, COLS)

# Save maze to a text file
save_maze_to_file(maze, "maze2.txt")