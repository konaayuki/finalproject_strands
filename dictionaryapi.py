import random
import requests
#import urllib3
#urllib3.disable_warnings(urllib3.exceptions.NotOpenSSLWarning)


def datamuse_api_get(query):
    url = 'https://api.datamuse.com/words'
    parameters = {'ml': query, 'max': 50, 'sp': '????? - ????????????'}
    response = requests.get(url, params= parameters)
    return response.json()
    

def get_related_words():
    themes = ['music', 'literature', 'weather', 'school', 'technology', 'city', 'farm', 'shopping', 'biomes', 'magazine names', 'beach', 'puzzle games', 'party goods', 'sports']
    random_theme = random.choice(themes)
    
    related_words = datamuse_api_get(random_theme)
    if related_words:
        file_path = f'{random_theme}.txt'
        with open(file_path, 'w') as file:
            for word in related_words:
                file.write(word + '\n')



