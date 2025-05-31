import os
import sys
from gtts import gTTS

text = sys.argv[1]

# Absolute path based on this script's location
base_dir = os.path.dirname(os.path.abspath(__file__))
audio_dir = os.path.join(base_dir, "..", "audio")
os.makedirs(audio_dir, exist_ok=True)

output_path = os.path.join(audio_dir, "voice.mp3")

tts = gTTS(text=text)
tts.save(output_path)
print("Text received:", text)

print(f"Saved to: {output_path}")

