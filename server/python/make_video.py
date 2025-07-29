# Fully patched make_video.py with clean encoding, no emojis, and debug overlay
import os
import json
import random
from pathlib import Path
from pydub import AudioSegment
from moviepy.editor import (
    VideoFileClip, concatenate_videoclips,
    TextClip, CompositeVideoClip, AudioFileClip
)
import moviepy.config as mpyconf

# Set working directory to this script's folder
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# ImageMagick path (confirmed working)
mpyconf.IMAGEMAGICK_BINARY = "C:\\Program Files\\ImageMagick-7.1.2-Q16\\magick.exe"

# ========== CONFIG ==========
audio_dir = Path("..") / "audio"
audio_dir.mkdir(parents=True, exist_ok=True)
bg_folder = Path("C:/Users/micha/OneDrive/Computer/background")
output_json_path = Path("captions.json")
output_video_path = "final_video.mp4"

# ========== STEP 1: Load voice clips ==========
print("Scanning for voice clips...")
voice_files = sorted(audio_dir.glob("voice_*.mp3"))

if not voice_files:
    print("No voice_*.mp3 files found. Did you run the TTS step?")
    exit(1)

# Load caption lines with proper encoding
with open("text_lines.json", "r", encoding="utf-8") as f:
    caption_lines = json.load(f)

# ========== STEP 2: Generate captions ==========
print("Generating captions.json...")
output_json = []
current_time = 0.0
final_audio = AudioSegment.empty()

for i, clip_path in enumerate(voice_files):
    segment = AudioSegment.from_file(clip_path)
    final_audio += segment
    duration = segment.duration_seconds

    text = caption_lines[i] if i < len(caption_lines) else f"[Caption {i+1}]"

    caption = {
        "start": round(current_time, 2),
        "end": round(current_time + duration, 2),
        "text": text
    }
    output_json.append(caption)
    current_time += duration

# Save captions with UTF-8 encoding and readable characters
with open(output_json_path, "w", encoding="utf-8") as f:
    json.dump(output_json, f, indent=2, ensure_ascii=False)
print("captions.json generated.")

# ========== STEP 3: Export combined audio ==========
combined_audio_path = "combined_voice.mp3"
final_audio.export(combined_audio_path, format="mp3")
audio_duration = len(final_audio) / 1000.0
print("Audio combined.")

# ========== STEP 4: Load background video ==========
print("Loading background...")
bg_videos = list(bg_folder.glob("*.mp4"))
bg_video_path = random.choice(bg_videos)
bg_clip = VideoFileClip(str(bg_video_path)).without_audio()
loops = int(audio_duration // bg_clip.duration) + 1
looped_clip = concatenate_videoclips([bg_clip] * loops).subclip(0, audio_duration)

# ========== STEP 5: Render captions ==========
print("Rendering captions...")
with open(output_json_path, "r", encoding="utf-8") as f:
    captions = json.load(f)

text_clips = []
for i, caption in enumerate(captions):
    try:
        print(f"Caption {i+1}: '{caption['text']}' ({caption['start']}s -> {caption['end']}s)")
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
        print(f"[ERROR] Failed to render caption {i+1}: {e}")

print(f"Total text clips rendered: {len(text_clips)}")

# Optional: test debug caption
try:
    debug_clip = TextClip(
        "DEBUG TEST CAPTION",
        fontsize=40,
        color='yellow',
        font='Arial-Bold',
        size=(int(looped_clip.w * 0.8), None),
        method='caption'
    ).set_position(('center', 'top')).set_duration(3)
    text_clips.insert(0, debug_clip)
except Exception as e:
    print(f"[ERROR] Failed to render debug caption: {e}")

# ========== STEP 6: Final video ==========
print("Rendering final video...")
audio = AudioFileClip(combined_audio_path)
final_video = CompositeVideoClip([looped_clip, *text_clips]).set_audio(audio)
final_video.write_videofile(output_video_path, fps=30, codec="libx264", audio_codec="aac", verbose=True)
print("final_video.mp4 created successfully.")
