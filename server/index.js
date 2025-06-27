const express = require('express');
const cors = require('cors');
require('dotenv').config();
const connectDB = require('./db');
const path = require('path'); // <== add this line if not already there

const app = express();
connectDB();

app.use(cors());
app.use(express.json());

// ✅ Serve audio files from /audio
app.use('/audio', express.static(path.join(__dirname, 'audio')));
app.use('/static', express.static(path.join(__dirname, 'python')));

// ✅ Mount routes (must come after middleware)
const routes = require('./routes');
app.use('/api', routes);
app.use('/static', express.static(path.join(__dirname, 'python')));

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`🚀 Server running on http://localhost:${PORT}`);
});
