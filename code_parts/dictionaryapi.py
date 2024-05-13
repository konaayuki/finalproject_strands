import os
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
    #parameters = {'ml': query, 'max': 50, 'sp': '???? - ????????????', 'partOfSpeech':'n'}
    response = requests.get(f'{url}/words?ml={query}&sp>???&max=20')
    return response.json() #ask about this
    
#getting related words from a theme
def get_related_words():
    #chooses a random theme from a created list
    themes = ['music', 'literature', 'weather', 'school', 'technology', 'city', 'farm', 'shopping', 'biomes', 'beach', 'puzzle+games', 'party+goods', 'sports']
    random_theme = random.choice(themes)
    print(random_theme)
    
    #uses the api to find related words and writes to a new textfile
    retrieved = datamuse_api_get(random_theme)
    print(retrieved)
    #prints out retrieved - a list of dictionaries
    
    #extract values of the 'word' key in each dictionary
    #put them into list of strings
    related_words_prot = [dic['word'] for dic in retrieved]
    print(related_words_prot)

    #limit word length and omit non alphabetic symbols
    related_words_fin = [term for term in related_words_prot if len(term) <= 8 and term.isalpha()]
    print(related_words_fin)

    #creating the textfile
    file_path = f'{random_theme}.txt'
    #file_path = os.path.join('finalproject_strands', f'{random_theme}.txt')
    with open(file_path, 'w') as file:
        for string in related_words_fin:
            file.write(string + '\n')
    print("Text file created successfully:", file_path)  # Print the path of the created file

get_related_words()





