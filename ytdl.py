import sys
import json
import string
import urllib.request
import urllib.parse
import json

def get_searchable_string(s):
    """Returns a new string with all the punctuations and offensive words
    removed, so that the new string is friendly for a search operation."""
    offensive_chars = string.punctuation
    offensive_words = ['song']
    for ch in offensive_chars:
        s = s.replace(ch, ' ')
    for word in offensive_words:
        s = s.replace(word, ' ')
    s = ' '.join(s.split())
    return s

def test_get_searchable_string():
    s = "song: Calvin Harris - My Way (Official Video)"
    expected = "Calvin Harris My Way Official Video"
    actual = get_searchable_string(s)
    assert actual == expected

def get_songs_list(filename):
    """Return as a list the songs listed in a text file; each song should be on
    a single line and different songs should be separated by at least one
    newline. Given, filename which has the list of songs."""
    file = open(filename, 'r')
    songs_list = []
    for line in file:
        if line == '\n':
            continue
        songs_list.append(get_searchable_string(line))
    file.close()
    return songs_list

if __name__ == '__main__':
    config_filename = 'config.json'
    songs_filename = ''
    HTTP_PROXY = ''
    API_KEY = ''

    songs_filename = sys.argv[1]

    config_data = {}
    with open(config_filename, 'r') as f:
        config_data = json.load(f)
    if 'HTTP_PROXY' in config_data:
        HTTP_PROXY = config_data['HTTP_PROXY']
    API_KEY = config_data['API_KEY']

    if len(sys.argv) != 2:
        print('Usage: ytdl.py <songs.txt>')

    # TODO
    # check_network()geturl
    
    for song in get_songs_list(songs_filename):
        queries = {
            "key": API_KEY,
            "part": "snippet",
            "maxResults": "1",
            "q": song,
            "type": "video"
        }
        query_string = urllib.parse.urlencode(queries)
        url = "https://www.googleapis.com/youtube/v3/search?" + query_string
        # response = urllib.request.urlopen("https://www.google.com/")
        response = urllib.request.urlopen(url)
        if response.getcode() != 200:
            print('GET ', response.geturl(), 'returned a', response.getcode())
            sys.exit(1)
        # if response
        json.load(response.read())
        # ['items'][0]['snippet']['title']



# part=snippet
# maxResults
# q
# type=video

# %load_ext autoreload
# %autoreload 2