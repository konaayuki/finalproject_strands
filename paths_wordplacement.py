

import random

#DEFINE BOARD
#board = [8,6]
#board = [[ '_' for i in range(6)] for j in range(8)]

import random

def is_valid_move(x, y, rows, cols, visited):
    return 0 <= x < rows and 0 <= y < cols and (x, y) not in visited

def find_paths(x, y, rows, cols, path, visited, paths):
    path.append((x, y)) #appends the current position to the path
    #print (path)
    #print ('here')
    visited.add((x, y)) #adds the current position to the visited list

    if len(path) == rows * cols: #checks if the length of the path is equal to all the spaces in the grid
        paths.append(path.copy()) #appends the current path to the path list as it is a valid path
    else:
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1),(-1,-1),(1,1),(1,-1),(-1,1)]: #looks over the 4 possible directions (up/down/left/right)
            nx, ny = x + dx, y + dy #calculates next direction
            if is_valid_move(nx, ny, rows, cols, visited): #checks if it is a valid move
                find_paths(nx, ny, rows, cols, path, visited, paths)
        visited.remove((x, y))
    
    path.pop()

def generate_hamiltonian_paths(rows, cols):
    n = rows * cols #number of spaces
    print(n)
    paths = []
    start_x, start_y = random.randint(0, rows-1), random.randint(0, cols-1) #randomly generate starting position for the path
    print(start_x,start_y)
    find_paths(start_x, start_y, rows, cols, [], set(), paths)
    return paths, (start_x, start_y)

#GENERATE PATHS IN AN 8X6 GRID
rows, cols = 2, 2
all_paths, start_point = generate_hamiltonian_paths(rows, cols)
print(all_paths)