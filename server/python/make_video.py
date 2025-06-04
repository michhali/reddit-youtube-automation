import os
import json
import random
from pathlib import Path
from gtts import gTTS
from pydub import AudioSegment
from moviepy.editor import (
    VideoFileClip, concatenate_videoclips,
    TextClip, CompositeVideoClip, AudioFileClip
)
import moviepy.config as mpyconf

# Optional: force path to ImageMagick
mpyconf.IMAGEMAGICK_BINARY = "C:\\Program Files\\ImageMagick-7.1.1-Q16\\magick.exe"

# ========== CONFIG ==========
reddit_parts = [
    "This is the title of the Reddit post.",
    "Here is the body of the post with more explanation."
]
audio_dir = Path("..") / "audio"
audio_dir.mkdir(parents=True, exist_ok=True)
bg_folder = Path("C:/Users/micha/OneDrive/Computer/background")
output_json_path = Path("captions.json")
output_video_path = "final_video.mp4"

# ========== STEP 1: Generate Voice Clips ==========
print("🎤 Generating TTS voice clips...")

for i, text in enumerate(reddit_parts):
    audio_path = audio_dir / f"voice_{i}.mp3"
    if not audio_path.exists():
        print(f"🗣️  Generating voice_{i}.mp3...")
        tts = gTTS(text)
        tts.save(audio_path)
    else:
        print(f"✅ voice_{i}.mp3 already exists")

# ========== STEP 2: Generate captions.json ==========
print("📝 Generating captions.json...")

output_json = []
current_time = 0.0

for i, text in enumerate(reddit_parts):
    audio_path = audio_dir / f"voice_{i}.mp3"
    if not audio_path.exists():
        print(f"⚠️ Missing audio: {audio_path}")
        continue

    duration = AudioSegment.from_file(audio_path).duration_seconds
    caption = {
        "start": round(current_time, 2),
        "end": round(current_time + duration, 2),
        "text": text
    }
    output_json.append(caption)
    current_time += duration

with open(output_json_path, "w") as f:
    json.dump(output_json, f, indent=2)

print("✅ captions.json generated.")

# ========== STEP 3: Combine audio ==========
print("🔊 Combining voice clips...")
final_audio = AudioSegment.empty()

for i in range(len(output_json)):
    audio_path = audio_dir / f"voice_{i}.mp3"
    segment = AudioSegment.from_file(audio_path)
    final_audio += segment

combined_audio_path = "combined_voice.mp3"
final_audio.export(combined_audio_path, format="mp3")
audio_duration = len(final_audio) / 1000.0
print("✅ Audio combined.")

# ========== STEP 4: Load background ==========
print("🎥 Loading background...")
bg_videos = list(bg_folder.glob("*.mp4"))
bg_video_path = random.choice(bg_videos)

bg_clip = VideoFileClip(str(bg_video_path)).without_audio()
loops = int(audio_duration // bg_clip.duration) + 1
looped_clip = concatenate_videoclips([bg_clip] * loops).subclip(0, audio_duration)

# ========== STEP 5: Load captions ==========
print("📝 Rendering captions...")
with open(output_json_path, "r") as f:
    captions = json.load(f)

text_clips = []
for i, caption in enumerate(captions):
    try:
        print(f"  ▶️ Caption {i+1}: '{caption['text']}' ({caption['start']}s → {caption['end']}s)")
        txt = TextClip(
            caption["text"],
            fontsize=40,
            color='white',
            font='Arial-Bold',
            size=(int(looped_clip.w * 0.8), None),
            method='caption'
        )
        txt = txt.set_position(('center', 'bottom')).set_start(caption["start"]).set_end(caption["end"])
        text_clips.append(txt)
    except Exception as e:
        print(f"  ❌ Failed to render caption {i+1}: {e}")

# ========== STEP 6: Final render ==========
print("🎬 Rendering final video...")

# Load the generated TTS audio
audio = AudioFileClip(combined_audio_path)

# Combine background video with captions and set audio
try:
    final_video = CompositeVideoClip([looped_clip, *text_clips]).set_audio(audio)
    final_video.write_videofile(output_video_path, fps=30, codec="libx264", audio_codec="aac")
    print("✅ final_video.mp4 created successfully.")
except Exception as e:
    print(f"❌ Failed to render video: {e}")

print("✅ Done! Your video is ready:")

