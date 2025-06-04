import os
import json
import moviepy.config as mpyconf
mpyconf.IMAGEMAGICK_BINARY = "C:\\Program Files\\ImageMagick-7.1.1-Q16\\magick.exe"

import random
from pathlib import Path
from moviepy.editor import (
    VideoFileClip, concatenate_videoclips, TextClip, CompositeVideoClip, AudioFileClip
)
from pydub import AudioSegment

# Load captions
with open("captions.json", "r") as f:
    captions = json.load(f)

# Combine all voice clips into one
audio_dir = Path("..") / "audio"
final_audio = AudioSegment.empty()
for i in range(len(captions)):
    clip_path = audio_dir / f"voice_{i}.mp3"
    segment = AudioSegment.from_file(clip_path)
    final_audio += segment

audio_output_path = "combined_voice.mp3"
final_audio.export(audio_output_path, format="mp3")
audio_duration = len(final_audio) / 1000.0  # in seconds

# Load a random Minecraft background video
bg_folder = Path("C:/Users/micha/OneDrive/Computer/background")
bg_videos = list(bg_folder.glob("*.mp4"))
bg_video_path = random.choice(bg_videos)

# Load and loop background video to match audio
bg_clip = VideoFileClip(str(bg_video_path)).without_audio()
loops = int(audio_duration // bg_clip.duration) + 1
looped_clip = concatenate_videoclips([bg_clip] * loops).subclip(0, audio_duration)

# Overlay captions
text_clips = []
from moviepy.editor import TextClip

text_clips = []

print("📝 Starting caption rendering...")

for i, caption in enumerate(captions):
    try:
        print(f"▶️ Caption {i+1}/{len(captions)}: '{caption['text']}' (from {caption['start']}s to {caption['end']}s)")

        txt = TextClip(
            caption["text"],
            fontsize=40,
            color='white',  # You can change this to 'yellow' or 'black' if background is light
            font='Arial-Bold',
            size=(int(looped_clip.w * 0.8), None),
            method='caption'
        )

        txt = txt.set_position(('center', 'bottom')).set_start(caption["start"]).set_end(caption["end"])
        text_clips.append(txt)

    except Exception as e:
        print(f"❌ Failed to render caption {i+1}: {e}")


# Final composition with audio
audio = AudioFileClip(audio_output_path)
video = CompositeVideoClip([looped_clip] + text_clips).set_audio(audio)
video.write_videofile("final_video.mp4", fps=30)

print("✅ Rendered final_video.mp4")
video.write_videofile("final_video.mp4", fps=30, verbose=True, progress_bar=True)
