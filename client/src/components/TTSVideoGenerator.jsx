import { useState } from 'react';

const TTSVideoGenerator = () => {
  const [lines, setLines] = useState(['']);
  const [videoUrl, setVideoUrl] = useState(null);

  const handleLineChange = (index, value) => {
    const updated = [...lines];
    updated[index] = value;
    setLines(updated);
  };

  const addLine = () => {
    setLines([...lines, '']);
  };

  const submitLines = async () => {
    try {
      const res = await fetch('http://localhost:5000/api/tts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ parts: lines }),
      });
      const data = await res.json();
      if (data.success) {
        setVideoUrl(data.videoPath || 'http://localhost:5000/final_video.mp4');
      }
    } catch (err) {
      console.error('TTS Error:', err);
    }
  };

  return (
    <div>
      <h2>Generate Video from Custom Text</h2>
      {lines.map((line, i) => (
        <div key={i}>
          <input
            type="text"
            value={line}
            onChange={(e) => handleLineChange(i, e.target.value)}
            placeholder={`Line ${i + 1}`}
          />
        </div>
      ))}
      <button onClick={addLine}>+ Add Line</button>
      <button onClick={submitLines}>Generate Video</button>

      {videoUrl && (
        <div style={{ marginTop: '1rem' }}>
          <h3>Generated Video</h3>
          <video src={videoUrl} controls width="600" />
        </div>
      )}
    </div>
  );
};

export default TTSVideoGenerator;
