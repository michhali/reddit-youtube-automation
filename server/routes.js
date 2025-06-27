const express = require('express');
const router = express.Router();

const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

const pythonDir = path.join(__dirname, 'python');

router.post('/essay-to-video', async (req, res) => {
  const { text } = req.body;
  if (!text) return res.status(400).json({ error: 'No text provided' });

  const textLinesPath = path.join(pythonDir, 'text_lines.json');
  const captionsPath = path.join(pythonDir, 'captions.json');

  // Step 1: Save the text lines
  const lines = text.split('\n').filter(line => line.trim() !== '');
  fs.writeFileSync(textLinesPath, JSON.stringify(lines, null, 2));
  console.log(`✅ Saved ${lines.length} lines to text_lines.json`);

  // Step 2: Generate captions
  try {
    execSync(`python generate_captions_json.py`, { cwd: pythonDir });
    console.log("✅ captions.json generated");
  } catch (err) {
    console.error("generate_captions_json.py failed:", err.message);
    return res.status(500).json({ error: 'Caption generation failed' });
  }

  // Step 3: Generate video
  try {
    execSync(`python make_video.py`, { cwd: pythonDir });
    console.log("✅ Video generated");
  } catch (err) {
    console.error("make_video.py failed:", err.message);
    return res.status(500).json({ error: 'Video generation failed' });
  }

  // Step 4: Respond with video path
  res.json({ video: 'final_video.mp4' });
});

module.exports = router;
