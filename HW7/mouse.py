import numpy as np

maze = np.array([
    [1, 1, 1, 1, 1, 1],
    [1, 2, 0, 0, 1, 1],
    [1, 1, 1, 0, 0, 1],
    [1, 0, 0, 0, 1, 1],
    [1, 0, 1, 3, 1, 1],
    [1, 1, 1, 1, 1, 1]
])

ROWS, COLS = maze.shape
path = []

def dfs(x, y):
    print(f"Checking cell ({x}, {y})...", end=" ")
  
    if x < 0 or y < 0 or x >= COLS or y >= ROWS:
        print("Out of bounds.")
        return False

    if maze[y, x] == 1:
        print("Hit a Wall (1).")
        return False
    if maze[y, x] == 4:
        print("Already visited (4).")
        return False

    if maze[y, x] == 3:
        print("Found the GOAL (3)! Stopping.")
        path.append((x, y))
        return True

    print("Valid path. Moving forward.")
    

    maze[y, x] = 4
    path.append((x, y))

    
    if dfs(x + 1, y): return True
    
    if dfs(x, y + 1): return True
 
    if dfs(x - 1, y): return True
  
    if dfs(x, y - 1): return True

    print(f"Dead end at ({x}, {y}). Backtracking...")
    path.pop()
    return False

start_pos = np.where(maze == 2)
start_y, start_x = start_pos[0][0], start_pos[1][0]

print(f"--- STARTING DEBUG RUN FROM ({start_x}, {start_y}) ---")
found = dfs(start_x, start_y)

print("-" * 30)
if found:
    print("FINAL RESULT: Success! The mouse can escape.")
    print("Path taken:", path)
else:
    print("FINAL RESULT: The mouse is trapped.")
