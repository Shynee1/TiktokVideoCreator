from moviepy.editor import *
import whisper_timestamped
import random
import os

class VideoCreator:
    def __init__(self, text: str, font: str, fontsize: int, stroke_width: int):
        self.text = text
        self.whisper = whisper_timestamped.load_model("base")
        self.font = font
        self.fontsize = fontsize
        self.stroke_width = stroke_width
        self.memory_pool = []

    # Grab a random background video and select a random starting point
    def get_backgroud_video(self, path: str, audio_duration: float) -> VideoFileClip:
        files = os.listdir(path)
        index = random.randint(0, len(files) - 1)
        video = VideoFileClip(path + files[index])
        start = random.randint(0, int(video.duration - audio_duration))
        video = video.subclip(start, start + audio_duration).set_position("center")
        self.memory_pool.append(video)
        return video
    
    # Grab random background audio and select a random starting point
    def get_background_audio(self, path: str, duration: float) -> AudioFileClip:
        files = os.listdir(path)
        index = random.randint(0, len(files) - 1)
        audio = AudioFileClip(path + files[index])
        start = random.randint(0, int(audio.duration - duration))
        audio = audio.subclip(start, start + duration).volumex(0.05)
        self.memory_pool.append(audio)
        return audio

    # Create subtitles using OpenAI Whisper
    def create_subtitles(self, audio_path: str) -> list[TextClip]:
        result = whisper_timestamped.transcribe(self.whisper, audio_path, compression_ratio_threshold=1.8)
        print("Successfully transcribed video")
        clips = []
        segments = result["segments"]
        for i in range(len(segments)):
            words = segments[i]["words"]
            for j in range(len(words)):
                word = words[j]["text"].upper()
                start = words[j]["start"]
                end = words[j]["end"]
                clips.append(self.create_clip(word, start, end))
                start = end

        print("Successfully created subtitles")
        return clips
    
    # Create a textclip with the given duration
    def create_clip(self, word: str, start: float, end: float) -> TextClip:
        textclip = (TextClip(
                word,      
                color = 'white', 
                stroke_color = 'black', 
                fontsize = self.fontsize, 
                font = self.font, 
                stroke_width = self.stroke_width
                )
            .set_duration(end - start)
            .set_start(start)
            .set_position("center")
        )
        self.memory_pool.append(textclip)
        return textclip
    
    # Compose everything into a final 9:16 video
    def create_composition(self, video_background_folder: str, audio_background_folder: str, audio_output_path: str) -> CompositeVideoClip:
        tts = AudioFileClip(audio_output_path)
        bacgkround_audio = self.get_background_audio(audio_background_folder, tts.duration)
        audio_comp = CompositeAudioClip([tts, bacgkround_audio])

        background_video = self.get_backgroud_video(video_background_folder, tts.duration)
        subtitles = self.create_subtitles(audio_output_path)
        clips = [background_video] + subtitles

        comp = CompositeVideoClip(clips, size = (608, 1080))
        comp = comp.set_audio(audio_comp)
        comp = comp.set_duration(tts.duration) 
        self.memory_pool.append(comp) 

        print("Successfully created composition")
        return comp
    
    def free_memory(self):
        memory_pool_length = len(self.memory_pool)
        for clip in self.memory_pool:
            clip.close()

        print(f"Successfully freed {memory_pool_length} objects")