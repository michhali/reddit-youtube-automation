const express = require('express');
const router = express.Router();
const { exec } = require('child_process');
const path = require('path');

router.get('/ping', (req, res) => {
  res.json({ message: "Ping route is alive" });
});

router.post('/tts', (req, res) => {
  const { text } = req.body;

  if (!text) {
    return res.status(400).json({ error: 'Missing text input' });
  }

  const pythonScript = path.join(__dirname, 'python', 'gtts_generate.py');
  const command = `python "${pythonScript}" "${text.replace(/"/g, '\\"')}"`;

  exec(command, (error, stdout, stderr) => {
    if (error || stderr) {
      return res.status(500).json({ error: stderr || error.message });
    }

    console.log(stdout);
    console.log("Running:", command);
    res.status(200).json({ message: 'Audio generated', file: '/audio/voice.mp3' });
  });
});

module.exports = router;
