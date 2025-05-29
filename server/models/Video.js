const mongoose = require('mongoose');

const videoSchema = new mongoose.Schema({
  redditThread: {
    type: String,
    required: true
  },
  title: {
    type: String,
    required: true
  },
  videoLink: {
    type: String,
    required: true
  },
  status: {
    type: String,
    default: "completed"
  },
  createdAt: {
    type: Date,
    default: Date.now
  }
});

module.exports = mongoose.model('Video', videoSchema);

