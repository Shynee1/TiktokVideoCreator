from moviepy.editor import *
from post_grabber import PostGrabber
from tiktok_tts import TikTokTTS
from video_creator import VideoCreator
import os

subreddit = "amitheasshole"
category = "top"
system_path = "C:/Program Files/TikTok Video Creator"
background_video_path = "assets/background_videos/"
background_audio_path = "assets/background_audios/"
output_video_path = "outputs/videos/"
output_audio_path = "outputs/audios/"

# Check if output directories are missing
if not os.path.exists(output_video_path) or not os.path.exists(output_audio_path):
    os.makedirs(output_video_path)
    os.makedirs(output_audio_path)

# Check if background clips are missing
if not os.path.exists(background_video_path) or not os.path.exists(background_audio_path):
    print(f"ERROR: Missing directory '{background_video_path}' or '{background_audio_path}'")
    
iterations = 0
post_grabber = PostGrabber(subreddit, category)
tts = TikTokTTS("en_us_006")

while iterations <= 2:
    # Scrape subreddit and obtain post text
    post = post_grabber.next_post()
    text = post_grabber.get_post_text(post)
    
    audio_destination = output_audio_path + "audio" + str(iterations) + ".mp3"
    video_desination = output_video_path + "final" + str(iterations) + ".mp4"

    # Generate TTS using TikTok's text-to-speech
    tts.create_tts(text, audio_destination)

    # Generate and save video 
    creator = VideoCreator(text, "Impact", 65, 2)
    comp = creator.create_composition(background_video_path, background_audio_path, audio_destination)
    comp.write_videofile(video_desination, threads = 4, logger = None, fps = 60)
    print(f"File written to {video_desination}")

    creator.free_memory()

    print(f'Iteration {iterations} completed')
    iterations += 1

