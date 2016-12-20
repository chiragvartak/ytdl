import sys
import json
import string

config_file = 'config.json'
songs_file = ''
HTTP_PROXY = ''
API_KEY = ''

if len(sys.argv) != 2:
    print('Usage: ytdl.py <songs.txt>')

songs_file = sys.argv[1]

config_data = {}
with open(config_file, 'r') as f:
    config_data = json.load(f)
if 'HTTP_PROXY' in config_data:
    HTTP_PROXY = config_data['HTTP_PROXY']
API_KEY = config_data['API_KEY']

# TODO: check_network()

def get_searchable_string(s):
    offensive_chars = string.punctuation
    offensive_words = ['song']
    for ch in offensive_chars:
        s = s.replace(ch, ' ')
    for word in offensive_words:
        s = s.replace(word, ' ')
    s = s.strip()
    return s

if __name__ == '__main__':
    with open(songs_file, 'r') as f:
        songs = f.read().split('\n')
    
    for song in songs:
        if song == '':
            continue
        searchable_string = get_searchable_string(song)
