# ytdl

What I usually do when I hear a song that I decide I like, is, I note it down in my phone. Previously, on, say, a weekend, I would sit in front of my computer and download all this songs that I have noted down (in Google Keep). But when the list becomes too large, I find that I cannot bring myself to sit down and download all the songs in them. I guess I just like the patience and tolerance to do such arduous grunt (but essential) work. Hence the requirement for this Python script.

What this Python script does, is, for each song in a text file, it searches for that song on Youtube and downloads only the audio as an mp3 file. It uses the tool [youtube-dl](https://rg3.github.io/youtube-dl/) to do this.

## Usage

```bash
python /path/to/ytdl.py /path/to/songs.txt
```

(The files will be downloaded in the the directory from which the above command is executed. The files `ytdl.py` and `songs.txt` can be present anywhere.)

## Setting Things Up

I use the [Youtube Data API](https://developers.google.com/youtube/v3/) to search for songs on Youtube. Hence, you will need a Google API key to be able to use `ytdl`. After getting this API key, create a new file called `config.json` (in the directory that contains `ytdl.py`). Add a json entry called `API_KEY` and mention your API key here. If you are behind a proxy, also add an entry with the key `HTTP_PROXY` to this json file.

## Miscellaneous Info

1. This tool is intended to simply *clone and run*. No additional configuration should be required apart from setting the API key and the proxy. And yes, you can run it on both Linux and Windows.

2. The file that contains the list of songs (I simply refer to it as `songs.txt`) should separate different songs by at least a newline. Also make sure to have one song on a single line.

3. `youtube-dl` requires some additional binaries to be able to convert files to mp3. They are present in the `utils/` directory.

4. Songs will be deleted from your `songs.txt` after downloading them. This makes it possible to simply run the script on any computer without the fear of downloading songs multiple times between computers.

5. ([TODO](https://github.com/chiragvartak/ytdl/issues/8): Press `Ctrl-C` anytime while downloading is ongoing. It won't break anything or create any inconsistencies.)

6. The script is intended to run with Python 3, not Python 2.

7. You need to always have the [latest youtube-dl executable](https://github.com/rg3/youtube-dl/releases/latest). Because [Google frequently changes the way to access Youtube](https://askubuntu.com/questions/598200/youdtube-dl-failed-to-extract-signature).