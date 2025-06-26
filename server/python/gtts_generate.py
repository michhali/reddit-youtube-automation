
import os
import sys
from gtts import gTTS

text = sys.argv[1]
index = sys.argv[2] if len(sys.argv) > 2 else "0"

# Absolute path based on this script's location
base_dir = os.path.dirname(os.path.abspath(__file__))
audio_dir = os.path.join(base_dir, "..", "audio")
os.makedirs(audio_dir, exist_ok=True)

output_path = os.path.join(audio_dir, f"voice_{index}.mp3")

tts = gTTS(text=text)
tts.save(output_path)

# Print safely without using emoji that cp1252 can't encode
print("Saved voice_{} with text: {}".format(index, text))
