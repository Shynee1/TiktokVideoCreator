# TikTok Video Creator

A Python application that automates the end-to-end creation of Reddit storytime videos for TikTok.  
Handles everything from scraping Reddit posts to synthesizing voiceovers and assembling the final video.

<p align="center">
  <img src="https://github.com/Shynee1/TiktokVideoCreator/assets/87081214/adbf322e-a54f-4d04-9879-c862d72119ad" alt="animated" />
</p>

---

## Features

- Scrapes the top daily post from the popular subreddit **r/AmItheAsshole (AITA)**
- Uses TikTok’s native Text-to-Speech (TTS) API to generate narrations
- Transcribes speech to timestamped subtitles using **OpenAI’s Whisper**
- Automatically overlays audio, subtitles, and gameplay background footage with **MoviePy**
- Supports customizable video backgrounds (e.g., Minecraft parkour, Subway Surfers)

All content is generated and compiled autonomously, making it easy to batch-create TikTok-ready videos.

---

## How It Works

1. **Reddit Scraping** – Utilizes `PRAW` to fetch top posts from r/AITA  
2. **Text-to-Speech** – Sends post text to TikTok's TTS API, saving audio for narration  
3. **Transcription** – Runs OpenAI Whisper locally to generate aligned subtitles  
4. **Video Composition** – Combines narration, subtitles, and gameplay footage into one cohesive video using MoviePy  

---

## Setup & Installation

### Requirements

- Python **3.11+**: [Download here](https://www.python.org/downloads/release/python-3117/)
- `ffmpeg` must be installed and available in your system PATH

### Steps

1. **Clone the repository**

```bash
git clone https://github.com/Shynee1/TiktokVideoCreator
cd TiktokVideoCreator
```

2. **Install Dependencies**

```bash
pip install -r requirements.txt
```

3. **Download required assets**
- [Background Gameplay Files (Google Drive)](https://drive.google.com/drive/folders/1TWEpfcW3aq6tcTMpgAP9RhPVDR6HpWza?usp=sharing)
- Extract the folder and place the videos into the `assets/background_videos` directory

4. **Set up Reddit API credentials**
- [Create a Reddit Developer Application](https://old.reddit.com/prefs/apps/)
- Add your Reddit API credentials to a file named `praw.ini` in the project root:

```ini
[DEFAULT]
client_id=YOUR_CLIENT_ID
client_secret=YOUR_CLIENT_SECRET
user_agent=YOUR_APP_NAME
```

## Notes
- Output videos are saved to the output/ directory by default
- Whisper will automatically generate .srt subtitle files
- Background clips are randomly selected unless otherwise specified

This project was built for automation, experimentation, and educational purposes. Feel free to fork, modify, or expand on it!
