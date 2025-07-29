// ✅ Streamlined React App: User pastes essay, hits submit, and gets back the final rendered video with TTS and captions
import { useState } from 'react';
import './App.css';

function App() {
  const [essay, setEssay] = useState("");
  const [videoReady, setVideoReady] = useState(false);
  const [loading, setLoading] = useState(false);
  const [videoPath, setVideoPath] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setVideoReady(false);

    try {
      const res = await fetch('http://localhost:5000/api/essay-to-video', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: essay })
      });

      if (!res.ok) throw new Error("Video generation failed");

      const result = await res.json();
     setVideoPath(`http://localhost:5000/static/${result.video || 'final_video.mp4'}`);

      setVideoReady(true);
    } catch (err) {
      console.error('Error:', err);
      alert('An error occurred while generating the video.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '2rem' }}>
     <h1>
  <span className="youtube-box">Reddit ➜ YouTube</span> Video Generator
</h1>


      <h2>Paste Essay or Long Text</h2>
      <form onSubmit={handleSubmit}>
        <textarea
          placeholder="Paste your essay here..."
          value={essay}
          onChange={(e) => setEssay(e.target.value)}
          rows={6}
          style={{ width: '100%' }}
          required
        />
        <br />
        <button type="submit" disabled={loading} style={{ marginTop: '1rem' }}>
          {loading ? "Generating..." : "Generate Video"}
        </button>
      </form>

  {videoReady && (
  <div style={{ marginTop: '2rem' }}>
    <h2>Your video is ready:</h2>
    <video src={videoPath} controls width="100%" />
    <br />
    <a
      href={videoPath}
      download="reddit_story.mp4"
      className="download-button"
    >
      Download Video
    </a>
  </div>
)}

    </div>
  );
}

export default App;
