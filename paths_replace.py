

import random

#DEFINE BOARD
board = [6,5]
board = [[ '_' for i in range(6)] for j in range(5)]
test_list = ['CHIP', 'LEFT', 'DREAM', 'POP','CHOCOLATE','SPIKE']

import random

def is_valid_move(x, y, rows, cols, visited):
    return 0 <= x < rows and 0 <= y < cols and (x, y) not in visited


def find_paths(x, y, rows, cols, path, visited, paths):
    path.append((x, y)) #appends the current position to the path
    visited.add((x, y)) #adds the current position to the visited list

    if len(path) == rows * cols: #checks if the length of the path is equal to all the spaces in the grid
        paths.append(path.copy()) #appends the current path to the path list as it is a valid path
        return #once a valid path is found, RETURN AND STOP HERE
        
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
    
    if len(split_list) == len(all_paths[0]):
        print('HERE')

    for i in range (0, len(all_paths[0])):
       x,y = all_paths[0][i]
       board[x][y] = split_list[i]
       #print ( all_paths[0][i] )
       #all_paths[0][i] = split_list[i]
       #print (all_paths[0][i])

       #board[all_paths[0][i][0]],board[all_paths[0][i][1]]=split_list[i]
    
   #print (split_list)

    # for i in range (0, len(all_paths[0])): #30 spots
    #     board[all_paths[0][i][0]][all_paths[0][i][1]]=split_list[i]
    return board

def generate_hamiltonian_paths(rows, cols):
    #n = rows * cols #number of spaces
    #print(n)
    paths = []
    start_x, start_y = random.randint(0, rows-1), random.randint(0, cols-1) #randomly generate starting position for the path
    #print(start_x,start_y)
    find_paths(start_x, start_y, rows, cols, [], set(), paths)
    return paths, (start_x, start_y)

#GENERATE PATHS IN A GRID
rows, cols = 6,5
all_paths, start_point = generate_hamiltonian_paths(rows, cols)
fill_board(board, test_list,all_paths)

#print(all_paths)

# print (all_paths[0])
# print (all_paths[0][0][0])
# print (all_paths[0][0][1])
# print (all_paths[0][1][0])
# print (all_paths[0][1][1])

print (board)