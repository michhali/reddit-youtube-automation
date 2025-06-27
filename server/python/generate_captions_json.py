# generate_captions_json.py
import os
import json
from pydub.utils import mediainfo
from pathlib import Path

# Reddit post broken into parts (title, body, top comment)
import json

with open("text_lines.json", "r") as f:
    parts = json.load(f)

# Directory where voice clips are saved
audio_dir = Path("..") / "audio"

output_json = []

current_time = 0.0

for i, text in enumerate(parts):
    audio_path = audio_dir / f"voice_{i}.mp3"
    if not audio_path.exists():
        print(f"Missing audio: {audio_path}")
        continue

    # Use mediainfo to get duration in seconds
    info = mediainfo(str(audio_path))
    duration = float(info['duration'])

    caption = {
        "start": round(current_time, 2),
        "end": round(current_time + duration, 2),
        "text": text
    }
    output_json.append(caption)
    current_time += duration

# Save to JSON
with open("captions.json", "w") as f:
    json.dump(output_json, f, indent=2)

print(" captions.json generated.")
