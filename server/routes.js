const express = require('express');
const router = express.Router();
const Video = require('./models/Video');


// POST - Save a new video
router.post('/api/videos', async (req, res) => {
  try {
    const newVideo = new Video(req.body);
    const savedVideo = await newVideo.save();
    res.status(201).json(savedVideo);
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});
console.log(typeof Video); // should be 'function'

// GET - Fetch all videos
router.get('/api/videos', async (req, res) => {
  try {
    const videos = await Video.find();
    res.json(videos);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

module.exports = router;
