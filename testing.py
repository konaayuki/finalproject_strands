import random
board_rows = 5
board_cols = 5
board = [[ '_' for i in range(board_rows)] for j in range(board_cols)]
combination = ['WATER', 'ROAST', 'SMORE', 'MARSH', 'SHOES']
def is_valid_move(x, y, board_rows, board_cols, visited):
    return 0 <= x < board_rows and 0 <= y < board_cols and (x, y) not in visited

def find_paths(x, y, board_rows, board_cols, path, visited, paths):
    path.append((x, y)) #appends the current position to the path
    visited.add((x, y)) #adds the current position to the visited list

    if len(path) == board_rows * board_cols: #checks if the length of the path is equal to all the spaces in the grid
        paths.append(path.copy()) #appends the current path to the path list as it is a valid path
        return #once a valid path is found, RETURN AND STOP HERE
        
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1),(-1,-1),(1,1),(1,-1),(-1,1)]: #looks over the 4 possible directions (up/down/left/right)
        nx, ny = x + dx, y + dy #calculates next direction
        if is_valid_move(nx, ny, board_rows, board_cols, visited): #checks if it is a valid move
            find_paths(nx, ny, board_rows, board_cols, path, visited, paths)
    
    visited.remove((x, y))
    path.pop()

def fill_board(board, combination,all_paths):

    split_list = []
    for word in combination:
        for letter in word:
            split_list.append(letter)

    for i in range (0, len(all_paths[0])): 
        x,y = all_paths[0][i]
        board[x][y] = split_list[i]

    return board, split_list

def generate_hamiltonian_paths(board_rows, board_cols,combination):
    paths = []
    start_x, start_y = random.randint(0, board_rows-1), random.randint(0, board_cols-1) #randomly generate starting position for the path
    find_paths(start_x, start_y, board_rows, board_cols, [], set(), paths)
    return paths, combination

#def generate_board(split_list, all_paths):



all_paths, combination = generate_hamiltonian_paths(board_rows, board_cols, combination)
board, split_list = fill_board(board, combination,all_paths)
#print (split_list)
#game_board = generate_board(split_list, all_paths)


# Print the first path
#print(all_paths[0])
print (board)
