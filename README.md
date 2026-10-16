# 📻 PURANA RADIO (पुराना रेडियो)
> **1980s–1990s Retro Indian Bus & Barber Shop Transistor Music Player**

[![GitHub Pages](https://img.shields.io/badge/Deployment-GitHub%20Pages-brightgreen?logo=github)](https://pages.github.com/)
[![Tech Stack](https://img.shields.io/badge/Stack-HTML5%20%7C%20CSS3%20%7C%20Vanilla%20JS-orange)](#-tech-stack)
[![Audio](https://img.shields.io/badge/Audio-Royalty--Free%20Synthesized-blue)](#-the-playlists)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An atmospheric, single-page retro Indian audio player honoring the golden era of **long-distance State Transport (ST) buses**, **chai tapris**, and **neighborhood saloon transistor radios**.

Built with pure **HTML5, CSS3, and modern JavaScript**, featuring an authentic teak wood cabinet, spinning cassette tape reels, glowing frequency dials, physical mechanical buttons with tactile SFX, and zero external build steps.

---

## 🎨 Visual Showcase & Design Highlights

- **🚌 Indian Bus & Barber Shop Aesthetic**: Faded mustard yellow (`#e5b746`), warm cream (`#fbf5e8`), rich teak wood (`#27150c`), and vintage bus red (`#ba2626`).
- **📼 Spinning Cassette Tape Deck**: Realistic 1980s audio cassette body with rotating dual spools, magnetic tape pack physics, and handwritten song labels.
- **📻 Analog Frequency Tuner**: Glowing amber dial with MW / FM bands and a physical red needle that glides as you switch channels or tracks.
- **🔊 Woven Speaker Grille**: Authentic fabric cross-hatch texture with a vintage brass Murphy badge and a bouncing analog VU meter.
- **✨ Iconic Indian Decals**: Genuine nostalgic touches including *"HORN OK PLEASE"*, *"शुभ यात्रा"*, and *"धूम्रपान निषेध / NO SMOKING"*.

---

## 🎶 The Playlists & Categories

### 1. 🚌 BUS WALE GAANE (Highway Express 98.4 FM)
*Nostalgic 90s long-distance road trips, wind in your hair, window seat memories.*
1. **सुहाना सफर (Highway Express)** — Kishore Kumar & R.D. Burman vibe *(Upbeat acoustic road trip melody)*
2. **धीरे धीरे से (खिड़की वाली सीट)** — Kumar Sanu & Alka Yagnik *(Warm 90s romance with bansuri flute)*
3. **यादों की बारात (Night Highway)** — Mohammed Rafi & Pancham Da *(Sitar riffs & disco-retro bassline)*
4. **चला जाता हूँ (Horn OK Please)** — Kishore Kumar & Kalyanji-Anandji *(Bouncy accordion & whistle melody)*

### 2. 💈 BARBER SHOP RADIO (Saloon Transistor 104.2 FM)
*Morning chai stalls, shaving foam aroma, and soothing classical transistor melodies.*
1. **चाय और ट्रांजिस्टर (Morning Raga)** — Ustad Bismillah Khan & Pt. Ravi Shankar *(Raag Bhairav with tanpura & sitar)*
2. **उस्ताद जी का सुर (उस्तादी बैठक)** — Ustad Vilayat Khan *(Fast sitar jhala & tabla teental)*
3. **शाम-ए-ग़ज़ल (पुरानी हवेली)** — Jagjit Singh & Ghulam Ali *(Soulful bowed sarangi & harmonium)*
4. **रेडियो सीलोन (आकाशवाणी 1982)** — Vividh Bharati & Ameen Sayani *(Nostalgic radio signature interval)*

---

## ⚙️ Player Mechanics & Features

- **Only 3 Core Controls**: Tactile mechanical `⏮ PREV`, `⏯ PLAY / PAUSE`, and `⏭ NEXT` push keys.
- **Smart Autoplay**: Attempts to start music immediately on load; if browser policies restrict autoplay, a retro **"रेडियो चालू करें / TUNE IN"** card allows instant one-tap playback.
- **Continuous Auto-Queue**: Automatically transitions to the next track when the current song completes.
- **Realistic Audio SFX**: Vintage mechanical cassette button clicks (`click.wav`) and analog radio station tuning whistle (`tuning.wav`).
- **Interactive Scrubber**: Brass slider knob with real-time elapsed (`MM:SS`) and total duration.
- **Zero Broken Links / 100% Offline**: All tracks and sound effects are bundled locally in the repository.
- **Graceful Error Handling**: Displays a friendly *"⚠️ सिग्नल कमज़ोर है"* status banner if audio decoding or connectivity fails.

---

## ⌨️ Keyboard Shortcuts

| Key | Action |
| :--- | :--- |
| <kbd>Space</kbd> | Play / Pause Toggle |
| <kbd>→</kbd> (Right Arrow) | Next Track |
| <kbd>←</kbd> (Left Arrow) | Previous Track |

---

## 🛠️ Tech Stack

- **HTML5**: Semantic audio player layout, accessible ARIA roles.
- **CSS3**: CSS Custom Properties, multi-layered gradients, keyframe animations (`@keyframes spinReel`), flexbox/grid layout.
- **JavaScript (ES6+)**: Custom audio state machine, playlist switcher, progress scrubbing, and browser autoplay unlocker.
- **Audio Synthesis**: High-fidelity procedural 16-bit PCM WAV generation (`generate_music.py`) using pure Python standard library (`wave`, `math`, `struct`).

---

## 🚀 How to Run Locally

No installations or build tools required! Simply:

```bash
# Clone the repository
git clone https://github.com/<YOUR-USERNAME>/purana-radio.git

# Enter the directory
cd purana-radio

# Open in your browser (Double-click index.html or start a local server)
# Python local server:
python -m http.server 8000
```
Then visit `http://localhost:8000` in your web browser.

---

## 🌐 How to Push to Your GitHub Profile & Deploy Live (GitHub Pages)

### Step 1: Initialize Git and Commit
```bash
git init
git add .
git commit -m "feat: complete Purana Radio 1980s retro music player"
git branch -M main
```

### Step 2: Link to Your GitHub Repository
1. Create a new repository on [GitHub](https://github.com/new) named `purana-radio`.
2. Connect and push your local files:
```bash
git remote add origin https://github.com/<YOUR-USERNAME>/purana-radio.git
git push -u origin main
```

### Step 3: Enable 1-Click Free Hosting
1. On your repository page, click **Settings** > **Pages**.
2. Under **Build and deployment > Source**, choose **Deploy from a branch**.
3. Set Branch: `main` and folder: `/ (root)`.
4. Click **Save**. Your radio player will be live at:
   `https://<YOUR-USERNAME>.github.io/purana-radio/`

---

## 📜 Credits & License
- Inspired by classic Murphy, Philips, and National Panasonic transistor radios.
- Designed & Developed with ❤️ for retro Indian music lovers.
- Released under the [MIT License](LICENSE).
