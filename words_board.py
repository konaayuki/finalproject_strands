
#GENERATE 6 BY 8 EMPTY GAMEBOARD
#rows = 6
#cols = 8
#grid = []

#for i in range(rows):
#    row = []
#    for i in range(cols):
#     row.append(0)  # Fill the grid with 0s
#    grid.append(row)

#for row in grid:
#    print(row) #print grid
#Steps:
#Initialize the game board as a list with the dimensions 6x8 (6 columns, 8 rows)
#Begin by placing the spanagram which must touch 2 opposite sides of the board
#Loop through each theme word and attempt to place it on the board
#Check that each theme word can be placed horizontally or vertically without overlapping any existing words
#If a word can be placed without overlap, add it to the board
#Repeat this until all of the theme words are placed
#If the function can not place each word without overlap, create a backtrack function that will try other positions/directions


#TEST CASES
#thats_fortunate = ["HORSESHOE", "LUCKYCHARMS", "WISHBONE", "LADYBUG", "PENNY", "SHAMROCK"]
#whats_the_issue = ["TIME", "HIGHLIGHTS", "VOGUE", "MAGAZINES", "WIRED", "SEVENTEEN", "PEOPLE"]
#world_piece = ["MARSH", "MOUNTAIN", "SWAMP", "TERRAIN", "PLAIN", "FOREST", "TUNDRA", "DESERT"]


#DEFINE BOARD
# boardsize = [8,6] 
# gameboard = [[' ' for i in range(boardsize[1])] for i in range (boardsize[0])]

# import random
# world_piece = ["MARSH", "MOUNTAIN", "SWAMP", "TERRAIN", "PLAIN", "FOREST", "TUNDRA", "DESERT"]
# def words_board (world_piece, gameboard, boardsize):
    # placed_word = False
    # while not placed_word:
    #     #randomly place the words on the board
    #      start_row = random.randint(0, boardsize[0] - 1) 
    #      start_col = random.randint(0, boardsize[1] - 1)
    #      direction = random.choice(['vertical', 'horizontal'])

    #      for i in range (0, len(world_piece)):
    #         if direction == 'vertical':
    #             if start_row + len(world_piece[i]) <= boardsize[0]:
    #                 placed_valid = True
                

#      for i in range (0, len(world_piece)): #run for the number of words there are
#     #randomly place the words on the board
#         start_row = random.randint(0, boardsize[0] - 1) 
#         start_col = random.randint(0, boardsize[1] - 1)
#         direction = random.choice(['vertical', 'horizontal'])
        
#         for letter in world_piece[i]:
#             if start_row < 0 or start_row >= boardsize[0] or start_col < 0 or start_col >=boardsize[1] or (gameboard[start_row][start_col] != ' ' and gameboard[start_row][start_col] != letter):
#                 break
#             gameboard[start_row][start_col] = letter #place letters on the board
#             if direction =='vertical':
#                 start_row+=1
#             else:
#                 start_col+=1

# words_board(world_piece, gameboard, boardsize)
# print (gameboard)


#DEFINE GRAPH
import numpy as np
graph_board = np.zeros((8,6))

#DEFINE BOARD
board = [8,6]
print (len(board))
board = [[' ' for i in range(board[1])] for i in range (board[0])]

#TESTING LIST
world_piece = ["MARSH", "MOUNTAIN", "SWAMP", "TERRAIN", "PLAIN", "FOREST", "TUNDRA", "DESERT"]

import random

def words_board (world_piece, graph_board, board):
    for word in world_piece: #run for the number of words in the list
        
        #randomly choose starting position
        start_row = random.randint(0, board[0] - 1) 
        start_col = random.randint(0,board[1]-1)
        start_placement = (start_row,start_col)
        
        if graph_board[start_placement[0]][start_placement[1]] == 0: #if the starting position is empty
            n = look_neighbours(board, start_row, start_col)

# def select_options(start_placement, graph_board, board): #out of the empty spots found in look_neighbours, randomly select one spot
 #    n = look_neighbours(start_placement, graph_board)
     #for index in n:
      #   if graph_board(index) == 0:
       #      options.append()

def look_neighbours(board, start_row, start_col): #function to check spots around
    #x,y = index
    possible_list = [] #create a list of possible options to go next

    if (start_row +1) < 8 and board[start_row +1][start_col] == 0: #checks option in the row above but the same column
        possible_list.append([start_row+1, start_col])

    if (start_row -1) >= 0 and board[start_row -1][start_col] == 0: #check option in the row below but the same column
        possible_list.append([start_row-1, start_col])

    if (start_col +1) < 6 and board[start_row][start_col+1] == 0: #check option in the same row but the column to the right
        possible_list.append([start_row, start_col+1])
    
    if (start_col - 1) >=0 and board[start_row, start_col-1] == 0: #check option in the same row but the column to the left
        possible_list.append([start_row, start_col-1])
    
    if (start_row+1) <8 and (start_col+1) <6 and board[start_row+1][start_col+1] == 0: #top right (one row up, column to the right)
        possible_list.append([start_row+1, start_col+1])
    
    if (start_row+1) < 8 and (start_col-1) >=0 and board[start_row+1][start_col-1] == 0: #top left 
        possible_list.append([start_row+1, start_col-1])


    # if board(x+1, y) ==0: #if the spot is empty
    #     possible_list.append([x+1,y]) 
    # if board(x-1,y) ==0:
    #     possible_list.append([x+1,y]) 
    

                


