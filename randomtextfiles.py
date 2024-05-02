#creating a randomized word list from a theme textfile
import random

#basic function to calculate the total letter count
def calculate_letter_count(word):
    return sum(1 for char in word if char.isalpha())

#total letters in crossword = 48
need_count = 48

def find_word_bycount(file_path, need_count):
    #file_path would be the randomly selected theme textfile, currently not coded
    #open textfile
    with open(file_path, 'r') as file:
        #read the words in file
        words = file.read().split()

    #empty list to store words
    selected_words = []

    for word in words:
        #use precreated basic function to calculate letter count through each word in file
        letter_count = calculate_letter_count(word)
        if letter_count == need_count:
            selected_words.append(word)
            
    return selected_words