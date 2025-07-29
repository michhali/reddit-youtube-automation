#  Reddit-to-YouTube Automation

**Reddit-to-YouTube Automation** is a full-stack app that transforms Reddit threads into storytelling-style YouTube videos.  
It uses AI-generated voiceovers, dynamic captions, and background visuals to automate the entire content creation pipeline.

---

##  Tech Stack

**Frontend:**  
- React  
- Tailwind CSS *(planned)*

**Backend:**  
- Node.js + Express

**Database:**  
- MongoDB Atlas

**Video Generation:**  
- Python + MoviePy

**APIs & Tools:**  
- gTTS (Google Text-to-Speech)  
- YouTube Data API *(planned)*  
- OpenAI API *(optional future feature)*

---

##  Hosting

- **Frontend:** Vercel *(planned)*  
- **Backend:** Render or Railway *(planned)*

---

## Core Features (Done)

- Submit Reddit post content via dashboard  
- Auto-generate voiceovers with gTTS  
- Parse lines and generate timed captions  
- Combine background video, captions, and audio into a final `.mp4`  
- Download completed video from frontend

---

## Usage (In Progress)

1. Paste a Reddit post into the input field  
2. The system:
   - Splits the text into sentences  
   - Generates voiceover for each line  
   - Creates synced captions  
   - Combines with background visuals  
3. Final video is downloadable from the dashboard

---

## Built with care by [Mihail Maravelias](https://github.com/michhali)
