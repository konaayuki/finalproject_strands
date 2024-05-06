#import os
pip install requests
import random
import requests
#import urllib3
#urllib3.disable_warnings(urllib3.exceptions.NotOpenSSLWarning)

#accessing datamuse api
#searches for:
#words that have related meaning to query word/phrase
#max 50 words per query
#limited to words of 4 to 12 letters
def datamuse_api_get(query):
    url = 'https://api.datamuse.com/words'
    parameters = {'ml': query, 'max': 50, 'sp': '???? - ????????????'}
    response = requests.get(url, params= parameters)
    return response.json() #ask about this
    
#getting related words from a theme
def get_related_words():
    #chooses a random theme from a created list
    themes = ['music', 'literature', 'weather', 'school', 'technology', 'city', 'farm', 'shopping', 'biomes', 'magazine names', 'beach', 'puzzle games', 'party goods', 'sports']
    random_theme = random.choice(themes)
    print(random_theme)
    
    #uses the api to find related words and writes to a new textfile
    related_words = datamuse_api_get(random_theme)
    if related_words:
        file_path = f'{random_theme}.txt'
        #file_path = os.path.join(f'{random_theme}.txt')
        with open(file_path, 'w') as file:
            for word in related_words:
                file.write(word + '\n')



