import random
import requests
#import urllib3
#urllib3.disable_warnings(urllib3.exceptions.NotOpenSSLWarning)

#accessing datamuse api
#searches for:
#words that have related meaning to query word/phrase
#max 20 words per query
#limited to words > 3 letters
def datamuse_api_get(query):
    url = 'https://api.datamuse.com'
    response = requests.get(f'{url}/words?ml={query}&sp>???&max=50')
    return response.json()
    
#getting related words from a theme
def get_related_words():
    #chooses a random theme from a created list
    themes = ['music', 'literature', 'weather', 'school', 'technology', 'city', 'farm', 'shopping', 'biomes', 'beach', 'puzzle+games', 'party+goods', 'sports']
    random_theme = random.choice(themes)
        #debug: print(random_theme)
    
    #uses the api to find related words and writes to a new textfile
    retrieved = datamuse_api_get(random_theme)
        #debug: print(retrieved)
    #prints out retrieved - a list of dictionaries
    
    #extract values of the 'word' key in each dictionary
    #put them into list of strings
    related_words_prot = [dic['word'] for dic in retrieved]
    #print(related_words_prot)

    #limit word length and omit non alphabetic symbols
    related_words_fin = [term for term in related_words_prot if len(term) <= 10 and term.isalpha()]
        #debug: print(related_words_fin)
    return random_theme, related_words_fin

#creating text file for retrieved words
def creating_word_list_file(theme, related_words):
    #creating the textfile
    file_path = f'{theme}.txt'
    with open(file_path, 'w') as file:
        for string in related_words:
            file.write(string + '\n')
    #print("Text file created successfully:", file_path)  # Print the path of the created file
    return file_path

#reloading the text file
def load_file(file_path):
    with open(file_path, 'r') as file:
        return file.read().splitlines()
    
#system to randomly find word combinations that add up to total of 25 letters
def generate_random_combination(list, target_length):
    #initiate 
    combination = []
    current_length = 0

    while current_length < target_length and list:
        term = random.choice(list)
        #add term if word doesn't pass limit
        if current_length + len(term) <= target_length:
            combination.append(term)
            current_length += len(term)
            list.remove(term) #remove once used terms to prevent repeats
        else:
            remaining_length = target_length - current_length
            shorter_word = [w for w in list if len(w) <= remaining_length]
            if shorter_word:
                term = random.choice(shorter_word)
                combination.append(term)
                current_length += len(term)
                list.remove(term)
            else:
                break
    return combination

#running the combination system
def find_words_by_count():
    file_path = creating_word_list_file(*get_related_words())
    list = load_file(file_path)
    combination = generate_random_combination(list, 25)
    print(combination)

find_words_by_count()

