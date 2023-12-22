from moviepy.editor import *
from post_grabber import PostGrabber
from tiktok_tts import TikTokTTS
from video_creator import VideoCreator
import os

subreddit = "amitheasshole"
category = "top"
background_video_path = "assets/background_videos/"
background_audio_path = "assets/background_audios/"
output_video_path = "outputs/videos/"
output_audio_path = "outputs/audios/"
iterations = 1

# Check if output directories are missing
if not os.path.exists(output_video_path) or not os.path.exists(output_audio_path):
    os.makedirs(output_video_path)
    os.makedirs(output_audio_path)

# Check if background clips are missing
if not os.path.exists(background_video_path) or not os.path.exists(background_audio_path):
    print(f"ERROR: Missing directory '{background_video_path}' or '{background_audio_path}'")
    
post_grabber = PostGrabber(subreddit, category)
tts = TikTokTTS("en_us_006")

for i in range(iterations):
    # Scrape subreddit and obtain post text
    post = post_grabber.next_post()
    text = post_grabber.get_post_text(post)
    print(text)

    file_index = len(os.listdir(output_video_path))
    audio_destination = output_audio_path + "audio" + str(file_index) + ".mp3"
    video_desination = output_video_path + "final" + str(file_index) + ".mp4"

    # Generate TTS using TikTok's text-to-speech
    tts.create_tts(text, audio_destination)

    # Generate and save video 
    creator = VideoCreator(text, "Impact", 65, 2)
    comp = creator.create_composition(background_video_path, background_audio_path, audio_destination)
    print(f"Writing file to {video_desination}...")
    comp.write_videofile(video_desination, threads = 4, logger = None, fps = 60)
    print(f"File successfully written")

    creator.free_memory()

    print(f'Iteration {i} completed')

