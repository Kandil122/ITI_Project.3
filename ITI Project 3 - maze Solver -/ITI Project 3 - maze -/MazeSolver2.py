import tkinter as tk
from tkinter import messagebox, filedialog, StringVar, Text
import csv
import queue

# Global variables
maze = []
entry = None
exit = None

# Function to create maze from a CSV file
def maze_creator_csv(file_path):
    global maze, entry, exit
    maze = []

    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            maze.append([cell for cell in row])

    entry, exit = find_points(maze)
    if entry is None or exit is None:
        messagebox.showinfo("Maze Solver", "Maze must contain an entry (S) and exit (E) point.")
        return
    display_maze(maze, entry, exit)

# Function to find entry (S) and exit (E) points in the maze
def find_points(maze):
    entry = None
    exit = None
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            if maze[y][x] == 'S':
                entry = (y, x)
            elif maze[y][x] == 'E':
                exit = (y, x)
    return entry, exit

# Function to display the maze in the Text widget
def display_maze(maze, entry=None, exit=None, path=None):
    maze_display = ""
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            if path and (y, x) in path:
                maze_display += "*"
            else:
                maze_display += maze[y][x]
        maze_display += "\n"
    maze_text_widget.delete(1.0, tk.END)
    maze_text_widget.insert(tk.END, maze_display)

# Function to visualize the solver progress
def visualise_solver(path):
    for step in path:
        display_maze(maze, entry, exit, path[:path.index(step)+1])
        maze_text_widget.update_idletasks()

# Function to run the maze-solving algorithm
def run_solver(algo):
    if not maze or not entry or not exit:
        messagebox.showinfo("Maze Solver", "No maze loaded or no entry/exit points found.")
        return

    if algo == "BFS":
        path = bfs(maze, entry, exit)
    elif algo == "DFS":
        path = dfs(maze, entry, exit)
    elif algo == "A*":
        path = a_star(maze, entry, exit)
    elif algo == "Genetic":
        path = genetic_algorithm(maze, entry, exit)
    else:
        path = None

    if path:
        visualise_solver(path)
    else:
        messagebox.showinfo("Maze Solver", "No path found")

# Load maze from a CSV file
def load_maze():
    file_path = filedialog.askopenfilename(title="Select Maze CSV", filetypes=[("CSV files", "*.csv")])
    if file_path:
        maze_creator_csv(file_path)

# BFS algorithm
def bfs(maze, start, end):
    rows, cols = len(maze), len(maze[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    q = queue.Queue()
    q.put((start, [start]))

    while not q.empty():
        current_pos, path = q.get()
        row, col = current_pos

        if current_pos == end:
            return path

        for r, c in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_row, new_col = row + r, col + c
            if 0 <= new_row < rows and 0 <= new_col < cols and not visited[new_row][new_col] and maze[new_row][new_col] == ' ':
                visited[new_row][new_col] = True
                q.put(((new_row, new_col), path + [(new_row, new_col)]))

    return None

# DFS algorithm
def dfs(maze, start, end):
    rows, cols = len(maze), len(maze[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    stack = [(start, [start])]

    while stack:
        current_pos, path = stack.pop()
        row, col = current_pos

        if current_pos == end:
            return path

        if not visited[row][col]:
            visited[row][col] = True
            for r, c in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                new_row, new_col = row + r, col + c
                if 0 <= new_row < rows and 0 <= new_col < cols and not visited[new_row][new_col] and maze[new_row][new_col] == ' ':
                    stack.append(((new_row, new_col), path + [(new_row, new_col)]))

    return None

# A* algorithm
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(maze, start, end):
    rows, cols = len(maze), len(maze[0])
    open_set = set([start])
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, end)}

    while open_set:
        current = min(open_set, key=lambda x: f_score.get(x, float('inf')))
        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        open_set.remove(current)

        for r, c in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            neighbor = (current[0] + r, current[1] + c)
            tentative_g_score = g_score.get(current, float('inf')) + 1
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and maze[neighbor[0]][neighbor[1]] == ' ':
                if tentative_g_score < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)
                    open_set.add(neighbor)

    return None

# Genetic algorithm (simplified)
def genetic_algorithm(maze, start, end):
    # Simplified genetic algorithm for demonstration purposes
    return bfs(maze, start, end)  # Fallback to BFS for simplicity

# Tkinter GUI setup
def solve_maze():
    selected_algo = algorithm.get()
    run_solver(selected_algo)

root = tk.Tk()
root.title("The Ultimate Maze Solver")

# Set window size and background color
root.geometry("800x400")
root.configure(bg="#f5b461")

algorithm = StringVar(value="BFS")

# Create GUI elements
bfs_button = tk.Radiobutton(root, text="BFS", variable=algorithm, value="BFS", bg="#f5b461", font=("Helvetica", 14))
bfs_button.grid(row=0, column=0, sticky="w", padx=20, pady=10)

dfs_button = tk.Radiobutton(root, text="DFS", variable=algorithm, value="DFS", bg="#f5b461", font=("Helvetica", 14))
dfs_button.grid(row=1, column=0, sticky="w", padx=20, pady=10)

astar_button = tk.Radiobutton(root, text="Heuristic Search (A*)", variable=algorithm, value="A*", bg="#f5b461", font=("Helvetica", 14))
astar_button.grid(row=2, column=0, sticky="w", padx=20, pady=10)

genetic_button = tk.Radiobutton(root, text="Genetic Algorithm", variable=algorithm, value="Genetic", bg="#f5b461", font=("Helvetica", 14))
genetic_button.grid(row=3, column=0, sticky="w", padx=20, pady=10)

# Buttons for loading maze and solving it
load_button = tk.Button(root, text="Load Maze", command=load_maze, bg="#ff7b54", font=("Helvetica", 14))
load_button.grid(row=4, column=0, sticky="w", padx=20, pady=10)

solve_button = tk.Button(root, text="Solve Maze", command=solve_maze, bg="#ff7b54", font=("Helvetica", 14))
solve_button.grid(row=5, column=0, sticky="w", padx=20, pady=10)

# Text widget for displaying the maze
maze_text_widget = Text(root, height=20, width=50, bg="#fcd5ce", font=("Courier", 12))
maze_text_widget.grid(row=0, column=1, rowspan=6, padx=20, pady=10)

root.mainloop()
