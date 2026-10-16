/**
 * PURANA RADIO (पुराना रेडियो)
 * 1980s-1990s Retro Indian Bus & Barber Shop Player Engine
 */

document.addEventListener('DOMContentLoaded', () => {
  // --- Audio Tracks Database ---
  const PLAYLISTS = {
    bus: [
      {
        id: 'bus-1',
        title: 'सुहाना सफर (Highway Express)',
        titleEn: 'Suhana Safar (Highway Express)',
        artist: 'किशोर कुमार & आर.डी. बर्मन',
        artistEn: 'Kishore Kumar & R.D. Burman',
        src: 'audio/bus/song1.wav',
        freq: '98.4 MHz',
        needlePos: '45%'
      },
      {
        id: 'bus-2',
        title: 'धीरे धीरे से (खिड़की वाली सीट)',
        titleEn: 'Dheere Dheere Se (Khidki Wali Seat)',
        artist: 'कुमार सानू & अलका याज्ञिक',
        artistEn: 'Kumar Sanu & Alka Yagnik',
        src: 'audio/bus/song2.wav',
        freq: '99.2 MHz',
        needlePos: '48%'
      },
      {
        id: 'bus-3',
        title: 'यादों की बारात (Night Highway)',
        titleEn: 'Yaadon Ki Baraat (Night Highway)',
        artist: 'मोहम्मद रफ़ी & पंचम दा',
        artistEn: 'Mohammed Rafi & Pancham Da',
        src: 'audio/bus/song3.wav',
        freq: '100.8 MHz',
        needlePos: '53%'
      },
      {
        id: 'bus-4',
        title: 'चला जाता हूँ (Horn OK Please)',
        titleEn: 'Chala Jaata Hoon (Horn OK Please)',
        artist: 'किशोर कुमार & कल्याणजी-आनंदजी',
        artistEn: 'Kishore Kumar & Kalyanji-Anandji',
        src: 'audio/bus/song4.wav',
        freq: '101.5 MHz',
        needlePos: '56%'
      }
    ],
    barber: [
      {
        id: 'barber-1',
        title: 'चाय और ट्रांजिस्टर (Morning Raga)',
        titleEn: 'Chai Aur Transistor (Morning Raga)',
        artist: 'उस्ताद बिस्मिल्लाह ख़ान & पं. रविशंकर',
        artistEn: 'Ustad Bismillah Khan & Pt. Ravi Shankar',
        src: 'audio/barber/song1.wav',
        freq: '104.2 MHz',
        needlePos: '74%'
      },
      {
        id: 'barber-2',
        title: 'उस्ताद जी का सुर (उस्तादी बैठक)',
        titleEn: 'Ustad Ji Ka Sur (Ustadi Baithak)',
        artist: 'उस्ताद विलायत ख़ान (सितार वादन)',
        artistEn: 'Ustad Vilayat Khan (Sitar Baithak)',
        src: 'audio/barber/song2.wav',
        freq: '105.0 MHz',
        needlePos: '77%'
      },
      {
        id: 'barber-3',
        title: 'शाम-ए-ग़ज़ल (पुरानी हवेली)',
        titleEn: 'Sham-E-Ghazal (Purani Haveli)',
        artist: 'जगजीत सिंह & गुलाम अली',
        artistEn: 'Jagjit Singh & Ghulam Ali',
        src: 'audio/barber/song3.wav',
        freq: '106.2 MHz',
        needlePos: '82%'
      },
      {
        id: 'barber-4',
        title: 'रेडियो सीलोन (आकाशवाणी 1982)',
        titleEn: 'Radio Ceylon Nostalgia (Aakashvani 1982)',
        artist: 'विविध भारती & अमीन सायानी',
        artistEn: 'Vividh Bharati & Ameen Sayani',
        src: 'audio/barber/song4.wav',
        freq: '107.5 MHz',
        needlePos: '88%'
      }
    ]
  };

  // --- State ---
  let currentCategory = 'bus';
  let currentTrackIndex = 0;
  let isPlaying = false;
  let tapeCounterVal = 0;
  let tapeCounterTimer = null;
  let vuMeterTimer = null;

  // --- DOM Elements ---
  const audio = document.getElementById('main-audio');
  const sfxClick = document.getElementById('sfx-click');
  const sfxTuning = document.getElementById('sfx-tuning');

  // Category buttons
  const catBusBtn = document.getElementById('cat-bus');
  const catBarberBtn = document.getElementById('cat-barber');

  // Transport Controls
  const btnPrev = document.getElementById('btn-prev');
  const btnPlay = document.getElementById('btn-play');
  const btnNext = document.getElementById('btn-next');
  const playIcon = document.getElementById('play-icon');
  const playLabelEn = document.getElementById('play-label-en');
  const playLabelHi = document.getElementById('play-label-hi');

  // Progress and Times
  const timeElapsed = document.getElementById('time-elapsed');
  const timeTotal = document.getElementById('time-total');
  const seekBarContainer = document.getElementById('seek-bar-container');
  const seekFill = document.getElementById('seek-fill');
  const seekThumb = document.getElementById('seek-thumb');

  // Display Elements
  const lcdTitle = document.getElementById('lcd-title');
  const lcdStatus = document.getElementById('lcd-status');
  const lcdTrackNum = document.getElementById('lcd-track-num');
  const lcdChannel = document.getElementById('lcd-channel');
  const tapeCounter = document.getElementById('tape-counter');

  // Cassette Elements
  const cassetteTape = document.getElementById('cassette-tape');
  const cassetteTitle = document.getElementById('cassette-title');
  const cassetteArtist = document.getElementById('cassette-artist');
  const cassetteSide = document.getElementById('cassette-side');
  const cassetteCatTag = document.getElementById('cassette-cat-tag');

  // Tuner & Hardware
  const tuningNeedle = document.getElementById('tuning-needle');
  const stereoLed = document.getElementById('stereo-led');
  const tuningLed = document.getElementById('tuning-led');
  const vuNeedle = document.getElementById('vu-needle');
  const vuBars = document.querySelectorAll('#vu-bars .bar');

  // Autoplay and Alerts
  const autoplayPrompt = document.getElementById('autoplay-prompt');
  const tapToPlayBtn = document.getElementById('tap-to-play-btn');
  const audioErrorBanner = document.getElementById('audio-error-banner');
  const audioErrorText = document.getElementById('audio-error-text');
  const retryBtn = document.getElementById('retry-btn');

  // Helper: Play mechanical SFX
  function playClickSfx() {
    if (sfxClick) {
      sfxClick.currentTime = 0;
      sfxClick.volume = 0.45;
      sfxClick.play().catch(() => {});
    }
  }

  function playTuningSfx() {
    if (sfxTuning) {
      sfxTuning.currentTime = 0;
      sfxTuning.volume = 0.35;
      sfxTuning.play().catch(() => {});
    }
  }

  // Format seconds as MM:SS
  function formatTime(seconds) {
    if (isNaN(seconds) || seconds < 0) return '00:00';
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
  }

  // Get current active song object
  function getCurrentSong() {
    const list = PLAYLISTS[currentCategory];
    return list[currentTrackIndex] || list[0];
  }

  // Load a song into the player
  function loadSong(song, shouldPlay = true) {
    // Hide any previous audio error banner
    hideAudioError();

    audio.src = song.src;
    audio.load();

    // Update Cassette Tape info
    cassetteTitle.textContent = song.title;
    cassetteArtist.textContent = song.artist;
    cassetteCatTag.textContent = currentCategory === 'bus' ? 'बस वाले गाने' : 'नाई की दुकान रेडियो';
    cassetteSide.textContent = currentTrackIndex < 2 ? 'SIDE A' : 'SIDE B';

    // Update Analog Needle Position
    tuningNeedle.style.left = song.needlePos;

    // Update LCD Screen
    const totalTracks = PLAYLISTS[currentCategory].length;
    lcdTrackNum.textContent = `TRACK [0${currentTrackIndex + 1}/0${totalTracks}]`;
    lcdChannel.textContent = currentCategory === 'bus' ? 'CH-1: BUS SPECIAL (98.4 FM)' : 'CH-2: SALOON TRANSISTOR (104.2 FM)';
    lcdTitle.textContent = `${song.titleEn.toUpperCase()} — ${song.artistEn.toUpperCase()}`;

    // Reset Progress
    seekFill.style.width = '0%';
    seekThumb.style.left = '0%';
    timeElapsed.textContent = '00:00';
    timeTotal.textContent = '00:00';

    if (shouldPlay) {
      playAudio();
    } else {
      pauseAudio();
    }
  }

  // Play audio safely
  function playAudio() {
    const playPromise = audio.play();
    if (playPromise !== undefined) {
      playPromise
        .then(() => {
          isPlaying = true;
          updatePlaybackUI(true);
          autoplayPrompt.classList.add('hidden');
        })
        .catch((err) => {
          console.warn('Playback prevented by browser policy:', err);
          isPlaying = false;
          updatePlaybackUI(false);
          // Show the clear one-tap autoplay unlock prompt
          autoplayPrompt.classList.remove('hidden');
        });
    }
  }

  // Pause audio safely
  function pauseAudio() {
    audio.pause();
    isPlaying = false;
    updatePlaybackUI(false);
  }

  // Toggle Play / Pause
  function togglePlayPause() {
    playClickSfx();
    if (isPlaying) {
      pauseAudio();
    } else {
      playAudio();
    }
  }

  // Update UI Elements based on Play/Pause status
  function updatePlaybackUI(playing) {
    if (playing) {
      playIcon.textContent = '⏸';
      playLabelEn.textContent = 'PAUSE';
      playLabelHi.textContent = 'रोको';
      btnPlay.classList.add('is-playing');
      lcdStatus.textContent = 'PLAYING ▶';
      cassetteTape.classList.add('spinning');
      stereoLed.classList.add('active');
      startTapeCounter();
      startVUMeter();
    } else {
      playIcon.textContent = '⏵';
      playLabelEn.textContent = 'PLAY';
      playLabelHi.textContent = 'बजाओ';
      btnPlay.classList.remove('is-playing');
      lcdStatus.textContent = 'PAUSED ⏸';
      cassetteTape.classList.remove('spinning');
      stereoLed.classList.remove('active');
      stopTapeCounter();
      stopVUMeter();
    }
  }

  // Previous Track
  function playPreviousTrack() {
    playClickSfx();
    const list = PLAYLISTS[currentCategory];
    currentTrackIndex = (currentTrackIndex - 1 + list.length) % list.length;
    loadSong(list[currentTrackIndex], true);
  }

  // Next Track
  function playNextTrack() {
    playClickSfx();
    const list = PLAYLISTS[currentCategory];
    currentTrackIndex = (currentTrackIndex + 1) % list.length;
    loadSong(list[currentTrackIndex], true);
  }

  // Switch Category (Bus Wale Gaane vs Barber Shop Radio)
  function switchCategory(category) {
    if (currentCategory === category) return;

    playTuningSfx();
    playClickSfx();

    // Flash tuning indicator LED
    tuningLed.classList.add('active');
    setTimeout(() => {
      tuningLed.classList.remove('active');
    }, 600);

    currentCategory = category;
    currentTrackIndex = 0;

    // Update tab button states
    if (category === 'bus') {
      catBusBtn.classList.add('active');
      catBusBtn.setAttribute('aria-selected', 'true');
      catBarberBtn.classList.remove('active');
      catBarberBtn.setAttribute('aria-selected', 'false');
    } else {
      catBarberBtn.classList.add('active');
      catBarberBtn.setAttribute('aria-selected', 'true');
      catBusBtn.classList.remove('active');
      catBusBtn.setAttribute('aria-selected', 'false');
    }

    loadSong(PLAYLISTS[currentCategory][0], true);
  }

  // Seeker Click / Drag
  function handleSeek(e) {
    const rect = seekBarContainer.getBoundingClientRect();
    const clickX = e.clientX - rect.left;
    const width = rect.width;
    const percent = Math.max(0, Math.min(1, clickX / width));

    if (audio.duration && !isNaN(audio.duration)) {
      audio.currentTime = percent * audio.duration;
      seekFill.style.width = `${percent * 100}%`;
      seekThumb.style.left = `${percent * 100}%`;
      timeElapsed.textContent = formatTime(audio.currentTime);
    }
  }

  // Tape Counter Mechanism
  function startTapeCounter() {
    if (tapeCounterTimer) clearInterval(tapeCounterTimer);
    tapeCounterTimer = setInterval(() => {
      tapeCounterVal = (tapeCounterVal + 1) % 1000;
      tapeCounter.textContent = String(tapeCounterVal).padStart(3, '0');
    }, 1200);
  }

  function stopTapeCounter() {
    if (tapeCounterTimer) {
      clearInterval(tapeCounterTimer);
      tapeCounterTimer = null;
    }
  }

  // Analog VU Meter & LED Column Physics
  function startVUMeter() {
    if (vuMeterTimer) clearInterval(vuMeterTimer);
    vuMeterTimer = setInterval(() => {
      if (!isPlaying) return;
      // Realistic rhythmic needle deflection between -25deg and +15deg
      const angle = -20 + Math.random() * 32 + (Math.sin(Date.now() / 150) * 8);
      vuNeedle.style.transform = `rotate(${angle}deg)`;

      // Dynamic LED pulse bars
      const activeCount = Math.floor(Math.random() * 5) + 1;
      vuBars.forEach((bar, idx) => {
        if (idx <= activeCount) {
          bar.classList.add('active');
        } else {
          bar.classList.remove('active');
        }
      });
    }, 120);
  }

  function stopVUMeter() {
    if (vuMeterTimer) {
      clearInterval(vuMeterTimer);
      vuMeterTimer = null;
    }
    vuNeedle.style.transform = 'rotate(-30deg)';
    vuBars.forEach(bar => bar.classList.remove('active'));
  }

  // Error handling: Show friendly message instead of pretending
  function showAudioError(message) {
    pauseAudio();
    audioErrorText.textContent = message || 'सिग्नल कमज़ोर है / Audio unavailable. Please retry.';
    audioErrorBanner.classList.remove('hidden');
    lcdStatus.textContent = 'SIGNAL LOSS ⚠️';
  }

  function hideAudioError() {
    audioErrorBanner.classList.add('hidden');
  }

  // --- HTML5 Audio Event Listeners ---
  audio.addEventListener('loadedmetadata', () => {
    timeTotal.textContent = formatTime(audio.duration);
  });

  audio.addEventListener('timeupdate', () => {
    if (!audio.duration || isNaN(audio.duration)) return;
    const current = audio.currentTime;
    const total = audio.duration;
    const percent = (current / total) * 100;

    seekFill.style.width = `${percent}%`;
    seekThumb.style.left = `${percent}%`;
    timeElapsed.textContent = formatTime(current);
    timeTotal.textContent = formatTime(total);
  });

  // Automatically play next song when current track ends
  audio.addEventListener('ended', () => {
    playNextTrack();
  });

  // Error event: If audio file fails to load
  audio.addEventListener('error', (e) => {
    console.error('Audio error:', e);
    const song = getCurrentSong();
    showAudioError(`⚠️ ट्रैक "${song.title}" उपलब्ध नहीं है / Signal unavailable. Retrying next song...`);
    // Automatically attempt next song after 2 seconds
    setTimeout(() => {
      playNextTrack();
    }, 2500);
  });

  // --- UI Event Handlers ---
  btnPlay.addEventListener('click', togglePlayPause);
  btnPrev.addEventListener('click', playPreviousTrack);
  btnNext.addEventListener('click', playNextTrack);

  catBusBtn.addEventListener('click', () => switchCategory('bus'));
  catBarberBtn.addEventListener('click', () => switchCategory('barber'));

  seekBarContainer.addEventListener('click', handleSeek);

  // Autoplay fallback unlock button
  tapToPlayBtn.addEventListener('click', () => {
    playClickSfx();
    autoplayPrompt.classList.add('hidden');
    playAudio();
  });

  // Retry button on error banner
  retryBtn.addEventListener('click', () => {
    hideAudioError();
    loadSong(getCurrentSong(), true);
  });

  // Keyboard navigation shortcuts
  document.addEventListener('keydown', (e) => {
    if (e.code === 'Space') {
      e.preventDefault();
      togglePlayPause();
    } else if (e.code === 'ArrowRight') {
      e.preventDefault();
      playNextTrack();
    } else if (e.code === 'ArrowLeft') {
      e.preventDefault();
      playPreviousTrack();
    }
  });

  // --- Initial Startup ---
  // Load the first song from BUS WALE GAANE
  loadSong(PLAYLISTS.bus[0], false);

  // Attempt autoplay when browser permits it
  const initialAutoplay = audio.play();
  if (initialAutoplay !== undefined) {
    initialAutoplay
      .then(() => {
        isPlaying = true;
        updatePlaybackUI(true);
        autoplayPrompt.classList.add('hidden');
      })
      .catch((err) => {
        // Autoplay blocked by browser policy -> display friendly one-tap unlock modal
        console.log('Autoplay policy blocked initial playback, showing unlock modal:', err);
        autoplayPrompt.classList.remove('hidden');
        updatePlaybackUI(false);
      });
  }
});
