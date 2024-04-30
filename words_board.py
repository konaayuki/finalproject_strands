
#DEFINE GRAPH
import numpy as np
graph_board = np.zeros((8,6))

#DEFINE BOARD
board = [8,6]
board = [[ '_' for i in range(6)] for j in range(8)]

#TESTING LIST
world_piece = ["MARSH", "MOUNTAIN", "SWAMP", "TERRAIN", "PLAIN", "FOREST", "TUNDRA", "DESERT"]

import random

def words_board (world_piece, graph_board, board):
    start_row = random.randint(0, 7) 
    start_col = random.randint(0,5)
    start_placement=[start_row,start_col]
    print(start_placement)

    for i in range (0, len(world_piece)):
        word = world_piece[i]

        for letter in word:
            if graph_board[start_placement[0]][start_placement[1]] == 0: #if the starting position is empty
                possible_list = look_neighbours(graph_board, start_row, start_col)
                board,select_position = select_options(graph_board, board,letter, possible_list)
                if select_position != start_placement:
                    start_row = select_position[0]
                    start_col=select_position[1]

def select_options( graph_board, board,letter, possible_list): #out of the empty spots found in look_neighbours, randomly select one spot
    if possible_list:
        print ('here')
        select_position = random.choice(possible_list)
        x,y = select_position
        graph_board[x][y] = 1
        board[x][y] = letter

    return board, select_position

def look_neighbours(graph_board, start_row, start_col): #function to check spots around
    possible_list = [] #create a list of possible options to go next

    if (start_row + 1) < 8 and graph_board[start_row + 1][start_col] == 0: #checks option in the row above but the same column
        possible_list.append([start_row + 1, start_col])

    if (start_row - 1) >= 0 and graph_board[start_row - 1][start_col] == 0: #check option in the row below but the same column
        possible_list.append([start_row - 1, start_col])

    if (start_col + 1) < 6 and graph_board[start_row][start_col + 1] == 0: #check option in the same row but the column to the right
        possible_list.append([start_row, start_col + 1])
    
    if (start_col - 1) >= 0 and graph_board[start_row][start_col - 1] == 0: #check option in the same row but the column to the left
        possible_list.append([start_row, start_col - 1])
    
    if (start_row + 1) < 8 and (start_col + 1) < 6 and graph_board[start_row + 1][start_col + 1] == 0: #top right (one row up, column to the right)
        possible_list.append([start_row + 1, start_col + 1])
    
    if (start_row + 1) < 8 and (start_col - 1) >= 0 and graph_board[start_row + 1][start_col - 1] == 0: #top left 
        possible_list.append([start_row + 1, start_col - 1])
    
    if (start_row - 1) >= 0 and (start_col + 1) < 6 and graph_board[start_row - 1][start_col + 1] == 0: #bottom right
        possible_list.append([start_row - 1, start_col + 1])
    
    if (start_row - 1) >= 0 and (start_col - 1) >= 0 and graph_board[start_row - 1][start_col - 1] == 0: #bottom left
        possible_list.append([start_row - 1, start_col - 1])
    
    print(possible_list)
    
    return possible_list

words_board (world_piece, graph_board, board)
print(graph_board)
print (board)

                



