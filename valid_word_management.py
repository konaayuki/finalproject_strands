
from collections import Counter #a dictionary subclass for counting occurences
import nltk #natural lanaguage toolkit
nltk.download('words')
from nltk.corpus import words

test_list = ['SMORE', 'ROAST', 'CRISP', 'BED', 'CARCASS']

def split_words(test_list):

    #make a list of all the letters that were used in the list
    seen = set()
    individual_letter = [letter.lower() for word in test_list for letter in word if letter not in seen and not seen.add(letter)]
    return individual_letter


def valid_words(individual_letter):

    all_words=words.words() #initializes all_words with a list of English words
    
    letters_count= Counter(individual_letter) #counts the number of times a letter appears in a word
    
    possible_words = [] #defines an empty list for the possible words

    for word in all_words: #iterates over each word in all_words list
       
        word_count = Counter(word) 

        if all(word_count[letter] <= letters_count[letter] for letter in word_count):
            #^checks if all of the letters in the current word can be formed using the letters in individual_letter list

            possible_words.append(word)
            #^if yes, add it to the list

    return list(set(possible_words))

individual_letter=split_words(test_list)
#print (individual_letter)
possible_words = valid_words(individual_letter)
#print (possible_words)


possible_words = [word.upper() for word in possible_words] #convert to uppercase
for i in range (len(test_list)):
    if test_list[i] in possible_words:
        print (test_list[i])