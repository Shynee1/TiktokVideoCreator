# Tiktok Video Creator
Python application to automate the creation of Reddit storytime posts. \
Manages everything from scraping the Reddit post to composing the final video. 

<p align="center">
  <img src="https://github.com/Shynee1/TiktokVideoCreator/assets/87081214/adbf322e-a54f-4d04-9879-c862d72119ad" alt="animated" />
</p>

## **Features**
- Scrapes the top post from popular subreddit 'AITA'
- Reads the post using Tiktok's text-to-speech API
- Converts TTS to timestamped subtitles using OpenAI's 'Whisper'
- Adds background audio/video and composes final result with MoviePy
  
## **Documentation**
- Install Python [3.11](https://www.python.org/downloads/release/python-3117/)
- Download the [latest release](https://github.com/Shynee1/TiktokVideoCreator/releases)
- Download required [background gameplay files](https://drive.google.com/drive/folders/1TWEpfcW3aq6tcTMpgAP9RhPVDR6HpWza?usp=sharing)
- Add `background_videos` to project's `assets` folder
- Create [Reddit Developer Application](https://old.reddit.com/prefs/apps/)
- Add Reddit credentials to `praw.ini`
- Install packages using ```pip install -r requirements.txt```
- Run `main.py`
