from moviepy.editor import *
from post_grabber import PostGrabber
from tiktok_tts import TikTokTTS
from video_creator import VideoCreator

subreddit = "amitheasshole"
category = "top"
background_video_path = "assets/background_videos/"
background_audio_path = "assets/background_audios/"
output_video_path = "outputs/videos/"
output_audio_path = "outputs/audios/"

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
    creator = VideoCreator(text, "Impact", 60, 2)
    comp = creator.create_composition(background_video_path, background_audio_path, audio_destination)
    comp.write_videofile(video_desination, threads = 4, fps = 60)

    print(f'Iteration {iterations} completed')
    iterations += 1
