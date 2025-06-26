
// ✅ Updated routes.js to support array of text inputs via "parts"
const express = require('express');
const router = express.Router();
const { exec } = require('child_process');
const path = require('path');

router.get('/ping', (req, res) => {
  res.json({ message: "Ping route is alive" });
});

router.post('/tts', (req, res) => {
  const { parts } = req.body;

  if (!parts || !Array.isArray(parts) || parts.length === 0) {
    return res.status(400).json({ error: 'Missing or invalid "parts" array' });
  }

  const scriptPath = path.join(__dirname, 'python', 'gtts_generate.py');

  const jobs = parts.map((text, i) => {
    const escapedText = text.replace(/"/g, '\\"');
    const command = `python "${scriptPath}" "${escapedText}" ${i}`;

    return new Promise((resolve, reject) => {
      exec(command, (err, stdout, stderr) => {
        if (err) {
          console.error(stderr || err.message);
          return reject(stderr || err.message);
        }
        console.log(stdout);
        resolve();
      });
    });
  });

  Promise.all(jobs)
    .then(() => res.status(200).json({ message: 'All audio clips generated successfully' }))
    .catch(error => res.status(500).json({ error }));
});

module.exports = router;