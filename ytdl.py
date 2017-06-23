import sys
import json
import string
import urllib.request
import urllib.parse
import json
import subprocess
import os
import fileinput
import collections

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
    """Return as an OrderedDict the songs listed in a text file, the key is the
    "searchable_string" and the value is the original line in the file; each
    song should be on a single line and different songs should be separated by
    at least one newline. Given, filename which has the list of songs."""
    file = open(filename, 'r')
    songs_list = collections.OrderedDict()
    for line in file:
        if line == '\n' or line.strip()[0] == '#':
            continue
        songs_list[get_searchable_string(line)] = line.strip()
    file.close()
    return songs_list

if __name__ == '__main__':
    config_filename = 'config.json'
    songs_filename = ''
    HTTP_PROXY = ''
    API_KEY = ''

    if len(sys.argv) != 3:
        print('Usage: ytdl.py <songs.txt> <download-folder>')
        sys.exit(0)

    songs_filename = sys.argv[1]
    download_folder = sys.argv[2]

    config_data = {}
    with open(config_filename, 'r') as f:
        config_data = json.load(f)
    if 'HTTP_PROXY' in config_data:
        HTTP_PROXY = config_data['HTTP_PROXY']
    API_KEY = config_data['API_KEY']
    print('Your API_KEY:', API_KEY)
    print('Your HTTP_PROXY:', HTTP_PROXY)
    print('^ Hope that they are both correct.')

    # TODO
    # check_network()
    
    songs_list = get_songs_list(songs_filename)
    for song in songs_list:
        queries = {
            "key": API_KEY,
            "part": "snippet",
            "maxResults": "1",
            "q": song,
            "type": "video"
        }
        query_string = urllib.parse.urlencode(queries)
        url = "https://www.googleapis.com/youtube/v3/search?" + query_string
        response = urllib.request.urlopen(url)
        if response.getcode() != 200:
            print('GET ', response.geturl(), 'returned a', response.getcode())
            sys.exit(1)
        response_dict = json.loads(response.read().decode('utf-8'))
        res = response_dict

        # Check if the search string gives no results
        if res['pageInfo']['totalResults'] == 0:
            print('No results for string:', song, flush=True)
            print('')
            continue

        video_title = res['items'][0]['snippet']['title']
        video_id = res['items'][0]['id']['videoId']
        url = "https://www.youtube.com/watch?v=" + video_id
        try:
            print('Title:', video_title, flush=True)
        except UnicodeEncodeError:
            print("<UnicodeEncodeError>", flush=True)
        except UnicodeDecodeError:
            print("<UnicodeDecodeError>", flush=True)
        print('Url:', url, flush=True)
        print("Line in file:", songs_list[song], flush=True)
        print("Searchable string:", song, flush=True)

        ffmpeg_path = ""
        if sys.platform == "win32":
            ffmpeg_path = r"libav\win64\usr\bin"
        else:
            ffmpeg_path = "libav/win64/usr/bin"

        subprocess.call([
            "ytdl",
            "--proxy", HTTP_PROXY,
            "--abort-on-error",
            "--socket-timeout", "30",
            "--extract-audio",
            "--audio-format", "mp3",
            "--audio-quality", "0",
            "--max-filesize", "20m",
            "--retries", "3",
            "--ffmpeg-location", ffmpeg_path,
            "--output", os.path.join(download_folder, "%(title)s-%(id)s.%(ext)s"),
            "--restrict-filenames",
            url
            ],
            shell=False)

        # Check and comment a song if mp3 downloaded successfully
        # downloaded = False # Unnecessary
        for fname in os.listdir(download_folder):
            if video_id in fname:
                # downloaded = True
                with fileinput.FileInput(songs_filename, inplace=True) as file:
                    for line in file:
                        print(line.replace(songs_list[song], '# ' +
                            songs_list[song] + ' --> ' + fname), end='')
                break

        print("", flush=True)
        

# https://www.youtube.com/watch?v=R0Avu3v9a8w

# ytdl --proxy <HTTP_PROXY> --abort-on-error --socket-timeout "30" -x --audio-format "mp3" --max-filesize "20m" --retries "3" --ffmpeg-location "libav\win64\usr\bin" <url>
# --audio-quality

# part=snippet
# maxResults
# q
# type=video

# %load_ext autoreload
# %autoreload 2

# res = response.read().decode('utf-8')

# Video URL part
# ['items'][0]['id']['videoId']

# Video Title
# ['items'][0]['snippet']['title']

# Name of song that is replaced in different - fixed
# Non-unicode characters handling - fixed
# Load output in a file by default
# Output searchable_string too - done
# change location of song downloads
# Skip when no results - done