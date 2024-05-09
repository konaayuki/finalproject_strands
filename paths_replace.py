

import random
import numpy as np 
import os 
#GENERATE PATHS IN A GRID
rows, cols = 5,5

#DEFINE BOARD
board = [[ '_' for i in range(rows)] for j in range(cols)]
#test_list = ['CHOCOLATE', 'MARSHMELLOW', 'GRAHAM', 'FIREPIT', 'SMORE', 'ROAST', 'CRISP'] #FOR 8x6
test_list = ['BUNNY', 'MARSHMALLOW', 'GRAHAM', 'THE']

import random

def is_valid_move(x, y, rows, cols, visited):
    return 0 <= x < rows and 0 <= y < cols and (x, y) not in visited

def find_paths(x, y, rows, cols, path, visited, paths):
    path.append((x, y)) #appends the current position to the path
    visited.add((x, y)) #adds the current position to the visited list

    if len(path) == rows * cols: #checks if the length of the path is equal to all the spaces in the grid
        paths.append(path.copy()) #appends the current path to the path list as it is a valid path
        #return #once a valid path is found, RETURN AND STOP HERE
        
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1),(-1,-1),(1,1),(1,-1),(-1,1)]: #looks over the 4 possible directions (up/down/left/right)
        nx, ny = x + dx, y + dy #calculates next direction
        if is_valid_move(nx, ny, rows, cols, visited): #checks if it is a valid move
            find_paths(nx, ny, rows, cols, path, visited, paths)
    
    visited.remove((x, y))
    path.pop()

def fill_board(board, test_list,all_paths):

    split_list = []
    for word in test_list:
        for letter in word:
            split_list.append(letter)

    for i in range (0, len(all_paths[0])): 
        x,y = all_paths[0][i]
        #print (split_list[i])

        board[x][y] = split_list[i]

    return board

def save_paths(filename,paths):
    np.save(filename,paths)
    return 

def generate_hamiltonian_paths(rows, cols):
    paths = []
    start_x, start_y = random.randint(0, rows-1), random.randint(0, cols-1) #randomly generate starting position for the path
    find_paths(start_x, start_y, rows, cols, [], set(), paths)
    return paths, (start_x, start_y)

# filename= f'{rows}{cols}.npy'
# if os.path.exists(filename):
#     all_paths = np.load(filename)
# else:

all_paths, start_point = generate_hamiltonian_paths(rows, cols)
#     save_paths(filename,all_paths)

fill_board(board, test_list,all_paths)

print (all_paths[0])