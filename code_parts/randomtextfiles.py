#creating a randomized word list from a theme textfile
import random

#basic function to calculate the total letter count
def calculate_letter_count(word):
    return sum(1 for char in word if char.isalpha())

#total letters in crossword = 48
need_count = 25

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

selected_words = find_word_bycount(file_path, need_count)

"""
example:
file_path = 'file.txt'

"""



"""
#basic function to calculate the total letter count
def calculate_letter_count(word):
    return sum(1 for char in word if char.isalpha())

#randomly generating words that total to needed count
def find_word_by_totcount(file_path, need_count, current_words = [], current_count=0, start_index=0):
    #file_path would be the randomly selected theme textfile, currently not coded
    #open textfile
    all_combinations = []

    with open(file_path, 'r') as file:
        #read the words in file
        words = file.read().split()

    print("Words in file:", words)
    print("Start index:", start_index)
    print("Current words:", current_words)
    print("Current count:", current_count)
        
    if current_count == need_count:
        print("Current count equals need count. Current words:", current_words)
        all_combinations.append(current_words)
    elif current_count > need_count or start_index == len(words):
        print("Terminating condition reached.")
    else:
        print("Entering recursive loop.")
        for ii in range(start_index, len(words)):
            term = words[ii]
            letter_count = calculate_letter_count(term)
            print("Processing word:", term, "Letter count:", letter_count)
            if current_count + letter_count <= need_count:
                new_count = current_count + letter_count
                new_words = current_words + [term]
                print("New words:", new_words)
                all_combinations.extend(find_word_by_totcount(file_path, need_count, new_words, new_count, start_index+1))
    
    return all_combinations
    
def select_random_combination(file_path, need_count):
    combinations = find_word_by_totcount(file_path, need_count)
    if combinations:
        random_combination = random.choice(combinations)
        return random_combination
    else:
        return None
    
theme, related_words = get_related_words()
file_path = creating_word_list_file(theme, related_words)
need_count = 25
random_combination = select_random_combination(file_path, need_count)
print(random_combination)
    
"""


"""
    for word in words:
        #use precreated basic function to calculate letter count through each word in file
        letter_count = calculate_letter_count(word)
        if letter_count == need_count:
            selected_words.append(word)
            
    print(selected_words)
    
find_word_bycount(file_path, need_count)
    
"""