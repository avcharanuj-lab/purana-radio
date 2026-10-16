import math
import struct
import wave
import os

SAMPLE_RATE = 22050

def write_wav(filename, samples):
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        # Clamp to 16-bit signed integer
        clamped = [max(-32767, min(32767, int(s * 32767))) for s in samples]
        wf.writeframes(struct.pack(f'<{len(clamped)}h', *clamped))
    print(f"Generated: {filename} ({len(samples)/SAMPLE_RATE:.1f}s, {os.path.getsize(filename):,} bytes)")

def gen_sfx():
    # 1. Mechanical cassette button click
    click_dur = 0.25
    n_click = int(SAMPLE_RATE * click_dur)
    click_samples = []
    for i in range(n_click):
        t = i / SAMPLE_RATE
        # Clunk + snap
        snap = math.sin(2 * math.pi * 1200 * t) * math.exp(-40 * t) if t < 0.05 else 0
        clunk = math.sin(2 * math.pi * 140 * t) * math.exp(-25 * t)
        spring = 0.3 * math.sin(2 * math.pi * 600 * t) * math.exp(-15 * t)
        noise = (math.sin(t * 104857) % 0.2) * math.exp(-30 * t)
        click_samples.append((snap * 0.5 + clunk * 0.6 + spring * 0.3 + noise) * 0.8)
    write_wav("audio/sfx/click.wav", click_samples)

    # 2. Transistor tuning static & whistle
    tune_dur = 0.6
    n_tune = int(SAMPLE_RATE * tune_dur)
    tune_samples = []
    for i in range(n_tune):
        t = i / SAMPLE_RATE
        # Heterodyne whistle changing pitch
        f_whistle = 800 + 1200 * math.sin(math.pi * t / tune_dur)
        whistle = 0.25 * math.sin(2 * math.pi * f_whistle * t)
        # FM radio static noise
        noise = ((math.sin(t * 88392) * 43758.5453) % 1.0 - 0.5) * 0.18
        # Crackle burst
        crackle = 0.3 if (i % 730 < 40 and t < 0.4) else 0.0
        fade = math.sin(math.pi * (t / tune_dur))
        tune_samples.append((whistle + noise + crackle) * fade * 0.7)
    write_wav("audio/sfx/tuning.wav", tune_samples)

# Musical helper functions
def note_freq(semitones_from_a4):
    return 440.0 * (2.0 ** (semitones_from_a4 / 12.0))

# Standard notes
# C4 = -9, D4 = -7, E4 = -5, F4 = -4, G4 = -2, A4 = 0, B4 = 2, C5 = 3
N = {
    'C3': -21, 'D3': -19, 'E3': -17, 'F3': -16, 'G3': -14, 'A3': -12, 'B3': -10,
    'C4': -9,  'Db4': -8, 'D4': -7,  'Eb4': -6, 'E4': -5,  'F4': -4,  'Gb4': -3,
    'G4': -2,  'Ab4': -1, 'A4': 0,   'Bb4': 1,  'B4': 2,
    'C5': 3,   'Db5': 4,  'D5': 5,   'Eb5': 6,  'E5': 7,   'F5': 8,   'Gb5': 9,
    'G5': 10,  'Ab5': 11, 'A5': 12,  'Bb5': 13, 'B5': 14,
    'C6': 15,  'D6': 17
}

# --- SONG 1: Suhana Safar (Highway Express) ---
def gen_bus_song1():
    bpm = 108
    beat_dur = 60.0 / bpm
    total_beats = 64
    dur = total_beats * beat_dur
    num_samples = int(SAMPLE_RATE * dur)

    # Melody in C Major / Bilawal: C D E G A C
    # Upbeat Kishore / Pancham style highway road trip
    melody_notes = [
        ('G4', 1.0), ('A4', 0.5), ('G4', 0.5), ('E4', 1.0), ('C4', 1.0),
        ('D4', 0.5), ('E4', 0.5), ('D4', 1.0), ('C4', 2.0),
        ('E4', 1.0), ('G4', 1.0), ('A4', 1.0), ('C5', 1.0),
        ('D5', 0.5), ('C5', 0.5), ('A4', 1.0), ('G4', 2.0),
        # Phrase 2
        ('C5', 1.0), ('D5', 0.5), ('C5', 0.5), ('A4', 1.0), ('G4', 1.0),
        ('A4', 0.5), ('G4', 0.5), ('E4', 1.0), ('D4', 2.0),
        ('C4', 1.0), ('E4', 1.0), ('G4', 1.0), ('A4', 1.0),
        ('G4', 1.0), ('E4', 0.5), ('D4', 0.5), ('C4', 2.0),
        # Repeat phrase with variations
        ('G4', 1.0), ('A4', 0.5), ('G4', 0.5), ('E4', 1.0), ('C4', 1.0),
        ('D4', 0.5), ('E4', 0.5), ('D4', 1.0), ('C4', 2.0),
        ('E4', 1.0), ('G4', 1.0), ('A4', 1.0), ('C5', 1.0),
        ('D5', 0.5), ('C5', 0.5), ('A4', 1.0), ('G4', 2.0),
        ('C5', 1.0), ('D5', 1.0), ('E5', 1.5), ('D5', 0.5),
        ('C5', 1.0), ('A4', 1.0), ('G4', 2.0),
        ('E4', 1.0), ('G4', 1.0), ('D4', 1.0), ('C4', 3.0)
    ]

    melody_events = []
    t_acc = 0.0
    for note, b in melody_notes:
        freq = note_freq(N[note])
        melody_events.append((t_acc, b * beat_dur, freq))
        t_acc += b * beat_dur

    samples = []
    for i in range(num_samples):
        t = i / SAMPLE_RATE

        # 1. Lead Whistle / Flute melody
        lead = 0.0
        for start_t, note_dur, freq in melody_events:
            if start_t <= t < start_t + note_dur + 0.1:
                dt = t - start_t
                env = math.sin(math.pi * min(1.0, dt / (note_dur + 0.05)))
                vibrato = math.sin(2 * math.pi * 5.5 * dt) * 4.0 if dt > 0.2 else 0.0
                f = freq + vibrato
                # Flute / Whistle tone: Sine + warm 2nd harmonic
                tone = math.sin(2 * math.pi * f * dt) + 0.3 * math.sin(2 * math.pi * f * 2 * dt)
                lead += tone * env * 0.4

        # 2. Acoustic Guitar Chords strumming (C, Am, F, G)
        bar_idx = int(t / (4 * beat_dur)) % 4
        chord_roots = [N['C3'], N['A3'], N['F3'], N['G3']]
        chord_root = chord_roots[bar_idx]
        beat_in_bar = (t % (4 * beat_dur)) / beat_dur
        strum_t = (beat_in_bar % 0.5) * beat_dur
        guitar = 0.0
        if strum_t < 0.3:
            env_g = math.exp(-12.0 * strum_t)
            for interval in [0, 4, 7, 12]:
                f_strum = note_freq(chord_root + 12 + interval)
                guitar += math.sin(2 * math.pi * f_strum * strum_t) * env_g * 0.08

        # 3. Dholak / Tabla Bus Rhythm: Keharwa (Dha Ge Na Tin, Na Ke Dhin Na)
        b_time = (t % beat_dur)
        beat_num = int(t / beat_dur) % 4
        perc = 0.0
        if b_time < 0.15:
            # Bayan bass thump on beat 0 and 2
            if beat_num in [0, 2]:
                bass_f = 95.0 * math.exp(-18.0 * b_time) + 55.0
                perc += 0.35 * math.sin(2 * math.pi * bass_f * b_time) * math.exp(-12.0 * b_time)
            # Dayan rim tap on all beats and offbeats
            perc += 0.18 * math.sin(2 * math.pi * 580 * b_time) * math.exp(-25.0 * b_time)

        # Offbeat dholak slap
        offbeat_time = ((t + beat_dur * 0.5) % beat_dur)
        if offbeat_time < 0.1:
            perc += 0.12 * math.sin(2 * math.pi * 880 * offbeat_time) * math.exp(-35.0 * offbeat_time)

        # 4. Bassline
        bass_freq = note_freq(chord_root)
        bass = 0.18 * math.sin(2 * math.pi * bass_freq * t) * (0.8 + 0.2 * math.sin(2 * math.pi * (1/beat_dur) * t))

        # Cassette warmth
        tape = 0.005 * math.sin(2 * math.pi * 50 * t)

        mix = lead + guitar + perc + bass + tape
        samples.append(mix * 0.85)

    write_wav("audio/bus/song1.wav", samples)

# --- SONG 2: Dheere Dheere Se (Khidki Wali Seat) ---
def gen_bus_song2():
    bpm = 86
    beat_dur = 60.0 / bpm
    total_beats = 48
    dur = total_beats * beat_dur
    num_samples = int(SAMPLE_RATE * dur)

    # Romantic 90s Melody in D Major: D E F# G A B C# D
    melody_notes = [
        ('A4', 1.0), ('F#4', 1.0), ('G4', 1.0), ('E4', 1.0),
        ('D4', 2.0), ('E4', 1.0), ('F#4', 1.0),
        ('G4', 1.5), ('A4', 0.5), ('B4', 1.0), ('A4', 1.0),
        ('F#4', 2.0), ('D4', 2.0),
        # Verse 2
        ('D5', 1.5), ('C#5', 0.5), ('B4', 1.0), ('A4', 1.0),
        ('B4', 1.0), ('A4', 1.0), ('G4', 1.0), ('F#4', 1.0),
        ('E4', 2.0), ('F#4', 1.0), ('G4', 1.0),
        ('A4', 1.5), ('G4', 0.5), ('F#4', 1.0), ('E4', 1.0),
        ('D4', 3.0), ('D4', 1.0),
        # Outro phrase
        ('F#4', 1.0), ('A4', 1.0), ('D5', 2.0),
        ('C#5', 1.0), ('B4', 1.0), ('A4', 2.0),
        ('G4', 1.0), ('F#4', 1.0), ('E4', 1.0), ('D4', 3.0)
    ]

    melody_events = []
    t_acc = 0.0
    for note, b in melody_notes:
        semis = N.get(note)
        if semis is None:
            # Handle accidental
            if note == 'F#4': semis = N['Gb4']
            elif note == 'C#5': semis = N['Db5']
        freq = note_freq(semis)
        melody_events.append((t_acc, b * beat_dur, freq))
        t_acc += b * beat_dur

    samples = []
    for i in range(num_samples):
        t = i / SAMPLE_RATE

        # 1. Indian Bansuri (Flute) with expressive breathy vibrato
        lead = 0.0
        for start_t, note_dur, freq in melody_events:
            if start_t <= t < start_t + note_dur + 0.15:
                dt = t - start_t
                env = math.sin(math.pi * min(1.0, dt / (note_dur + 0.08)))
                vib = math.sin(2 * math.pi * 5.0 * dt) * 3.5 if dt > 0.15 else 0.0
                f = freq + vib
                # Bansuri harmonic spectrum: Sine + soft 2nd + 3rd harmonic
                tone = math.sin(2 * math.pi * f * dt) + 0.25 * math.sin(2 * math.pi * f * 2 * dt) + 0.1 * math.sin(2 * math.pi * f * 3 * dt)
                lead += tone * env * 0.45

        # 2. Harmonium reed pad chords
        chord_time = int(t / (4 * beat_dur)) % 3
        # D Major, G Major, A Major
        pad_roots = [N['D3'], N['G3'], N['A3']]
        root = pad_roots[chord_time]
        pad = 0.0
        for interval in [0, 4, 7]:
            pf = note_freq(root + interval + 12)
            pad += (math.sin(2 * math.pi * pf * t) + 0.4 * math.sin(2 * math.pi * pf * 2 * t) + 0.2 * math.sin(2 * math.pi * pf * 3 * t)) * 0.05

        # 3. Soft 90s Keharwa rhythm
        b_time = (t % beat_dur)
        beat_num = int(t / beat_dur) % 4
        perc = 0.0
        if b_time < 0.2:
            if beat_num in [0, 2]:
                bf = 80.0 * math.exp(-10.0 * b_time) + 45.0
                perc += 0.3 * math.sin(2 * math.pi * bf * b_time) * math.exp(-8.0 * b_time)
            perc += 0.14 * math.sin(2 * math.pi * 440 * b_time) * math.exp(-20.0 * b_time)

        # 4. Melodic bass
        bass = 0.15 * math.sin(2 * math.pi * note_freq(root) * t)

        samples.append((lead + pad + perc + bass) * 0.85)

    write_wav("audio/bus/song2.wav", samples)

# --- SONG 3: Yaadon Ki Baraat (Night Highway) ---
def gen_bus_song3():
    bpm = 98
    beat_dur = 60.0 / bpm
    total_beats = 48
    dur = total_beats * beat_dur
    num_samples = int(SAMPLE_RATE * dur)

    # Groovy 80s Sitar + Synth Riff in E Minor
    riff = [
        ('E4', 0.5), ('G4', 0.5), ('A4', 0.5), ('B4', 0.5),
        ('D5', 0.5), ('B4', 0.5), ('A4', 0.5), ('G4', 0.5),
        ('E4', 1.0), ('B4', 1.0), ('A4', 1.0), ('G4', 1.0),
        ('E4', 2.0), ('D4', 1.0), ('E4', 1.0),
        # Phrase 2
        ('B4', 0.5), ('D5', 0.5), ('E5', 1.0), ('D5', 0.5), ('B4', 0.5),
        ('A4', 1.0), ('G4', 0.5), ('A4', 0.5), ('B4', 2.0),
        ('G4', 0.5), ('A4', 0.5), ('B4', 0.5), ('A4', 0.5),
        ('G4', 0.5), ('E4', 0.5), ('D4', 0.5), ('E4', 2.5)
    ]
    # Loop twice
    full_riff = riff + riff

    events = []
    t_acc = 0.0
    for note, b in full_riff:
        events.append((t_acc, b * beat_dur, note_freq(N[note])))
        t_acc += b * beat_dur

    samples = []
    for i in range(num_samples):
        t = i / SAMPLE_RATE

        # 1. Sitar lead with metallic harmonics and fast decay
        lead = 0.0
        for st, nd, freq in events:
            if st <= t < st + nd + 0.15:
                dt = t - st
                decay = math.exp(-3.5 * dt)
                sitar = (
                    math.sin(2 * math.pi * freq * dt) +
                    0.6 * math.sin(2 * math.pi * freq * 2 * dt) +
                    0.35 * math.sin(2 * math.pi * freq * 3 * dt) +
                    0.2 * math.sin(2 * math.pi * freq * 4 * dt)
                ) * decay
                lead += sitar * 0.45

        # 2. Disco-Bollywood Bass Groove (Octave bouncing in E)
        sub_beat = (t % (beat_dur * 0.5)) / (beat_dur * 0.5)
        step = int(t / (beat_dur * 0.5)) % 4
        f_bass = note_freq(N['E3']) if step in [0, 2] else note_freq(N['E3'] + 12)
        bass = 0.22 * math.sin(2 * math.pi * f_bass * t) * math.exp(-4.0 * sub_beat)

        # 3. Driving 80s Highway Drum Beat
        b_time = t % beat_dur
        perc = 0.0
        # Kick drum
        if int(t / beat_dur) % 2 == 0 and b_time < 0.15:
            perc += 0.35 * math.sin(2 * math.pi * (100 * math.exp(-20 * b_time) + 45) * b_time) * math.exp(-12 * b_time)
        # Snare slap
        if int(t / beat_dur) % 2 == 1 and b_time < 0.12:
            perc += 0.25 * math.sin(2 * math.pi * 320 * b_time) * math.exp(-22 * b_time)
        # Hi-hat 16ths
        hat_time = t % (beat_dur * 0.25)
        if hat_time < 0.04:
            perc += 0.1 * math.sin(2 * math.pi * 3000 * hat_time) * math.exp(-50 * hat_time)

        samples.append((lead + bass + perc) * 0.8)

    write_wav("audio/bus/song3.wav", samples)

# --- SONG 4: Chala Jaata Hoon (Horn OK Please) ---
def gen_bus_song4():
    bpm = 114
    beat_dur = 60.0 / bpm
    total_beats = 48
    dur = total_beats * beat_dur
    num_samples = int(SAMPLE_RATE * dur)

    # Cheerful Kishore Kumar style bouncy melody in G Major
    melody = [
        ('G4', 0.5), ('B4', 0.5), ('D5', 0.5), ('B4', 0.5),
        ('G4', 1.0), ('E4', 1.0),
        ('A4', 0.5), ('B4', 0.5), ('A4', 0.5), ('G4', 0.5),
        ('D4', 2.0),
        ('E4', 0.5), ('G4', 0.5), ('A4', 0.5), ('B4', 0.5),
        ('C5', 1.0), ('E5', 1.0),
        ('D5', 1.0), ('B4', 1.0), ('G4', 2.0),
        # Phrase 2
        ('D5', 0.5), ('D5', 0.5), ('E5', 0.5), ('D5', 0.5),
        ('B4', 1.0), ('G4', 1.0),
        ('C5', 0.5), ('C5', 0.5), ('D5', 0.5), ('C5', 0.5),
        ('A4', 2.0),
        ('G4', 0.5), ('A4', 0.5), ('B4', 0.5), ('C5', 0.5),
        ('D5', 1.0), ('B4', 1.0), ('G4', 2.0)
    ]
    full_melody = melody + melody

    events = []
    t_acc = 0.0
    for note, b in full_melody:
        events.append((t_acc, b * beat_dur, note_freq(N[note])))
        t_acc += b * beat_dur

    samples = []
    for i in range(num_samples):
        t = i / SAMPLE_RATE

        # 1. Accordion / Harmonium melody
        lead = 0.0
        for st, nd, freq in events:
            if st <= t < st + nd + 0.08:
                dt = t - st
                env = math.sin(math.pi * min(1.0, dt / (nd + 0.04)))
                # Accordion reed dual oscillation
                acc = (math.sin(2 * math.pi * freq * dt) + 0.5 * math.sin(2 * math.pi * (freq * 1.003) * dt) + 0.3 * math.sin(2 * math.pi * freq * 2 * dt)) * env
                lead += acc * 0.4

        # 2. Bus horn flourish at start of loop
        horn = 0.0
        if 0.1 < t < 0.6:
            th = t - 0.1
            f1, f2 = 330.0, 440.0
            horn = (0.25 * math.sin(2 * math.pi * f1 * th) + 0.25 * math.sin(2 * math.pi * f2 * th)) * math.sin(math.pi * (th / 0.5))

        # 3. Oom-pah bouncy rhythm (Bass on 1 & 3, Strum on 2 & 4)
        b_time = t % beat_dur
        beat_idx = int(t / beat_dur) % 4
        rhythm = 0.0
        if beat_idx in [0, 2] and b_time < 0.18:
            rhythm += 0.3 * math.sin(2 * math.pi * note_freq(N['G3']) * b_time) * math.exp(-10 * b_time)
        elif beat_idx in [1, 3] and b_time < 0.15:
            # Accordion chord chop
            for f_ch in [note_freq(N['B4']), note_freq(N['D5']), note_freq(N['G5'])]:
                rhythm += 0.08 * math.sin(2 * math.pi * f_ch * b_time) * math.exp(-15 * b_time)

        samples.append((lead + horn + rhythm) * 0.8)

    write_wav("audio/bus/song4.wav", samples)

# --- BARBER SHOP RADIO SONGS ---

# Song 1: Chai Aur Transistor (Morning Raga Bhairav)
def gen_barber_song1():
    bpm = 72
    beat_dur = 60.0 / bpm
    total_beats = 48
    dur = total_beats * beat_dur
    num_samples = int(SAMPLE_RATE * dur)

    # Raag Bhairav: Komal Re (r), Shuddha Ga (G), Shuddha Ma (M), Pa (P), Komal Dha (d), Shuddha Ni (N)
    # Authentic Indian Morning Transistor Raga
    # C scale: C, Db, E, F, G, Ab, B, C
    scale_bhairav = [
        ('C4', 2.0), ('Db4', 2.0), ('E4', 2.0), ('F4', 1.5), ('E4', 0.5),
        ('Db4', 2.0), ('C4', 2.0),
        ('E4', 1.0), ('F4', 1.0), ('G4', 2.0), ('Ab4', 2.0),
        ('G4', 1.5), ('F4', 0.5), ('E4', 2.0),
        ('Ab4', 1.0), ('B4', 1.0), ('C5', 2.5), ('B4', 0.5),
        ('Ab4', 1.0), ('G4', 2.0), ('F4', 1.0), ('E4', 1.0),
        ('Db4', 2.0), ('C4', 3.0)
    ]

    events = []
    t_acc = 0.5
    for note, b in scale_bhairav:
        events.append((t_acc, b * beat_dur, note_freq(N[note])))
        t_acc += b * beat_dur

    samples = []
    for i in range(num_samples):
        t = i / SAMPLE_RATE

        # 1. Hypnotic Tanpura Drone (Sa - Pa - Sa - Sa)
        # Continuous shimmering background
        tanpura = (
            0.14 * math.sin(2 * math.pi * note_freq(N['G3']) * t) +
            0.18 * math.sin(2 * math.pi * note_freq(N['C4']) * t) +
            0.10 * math.sin(2 * math.pi * note_freq(N['C5']) * t) +
            0.06 * math.sin(2 * math.pi * note_freq(N['C5'] * 1.5) * t) * (0.8 + 0.2 * math.sin(2 * math.pi * 0.3 * t))
        )

        # 2. Sitar Plucks with rich meend and sympathetic resonating strings
        lead = 0.0
        for st, nd, freq in events:
            if st <= t < st + nd + 0.2:
                dt = t - st
                decay = math.exp(-2.2 * dt)
                sitar = (
                    math.sin(2 * math.pi * freq * dt) +
                    0.65 * math.sin(2 * math.pi * freq * 2 * dt) +
                    0.4 * math.sin(2 * math.pi * freq * 3 * dt) +
                    0.25 * math.sin(2 * math.pi * freq * 4 * dt) +
                    0.15 * math.sin(2 * math.pi * freq * 5 * dt)
                ) * decay
                lead += sitar * 0.4

        # 3. Gentle Tabla Teental (Dha Dhin Dhin Dha)
        b_time = t % beat_dur
        beat_idx = int(t / beat_dur) % 4
        tabla = 0.0
        if b_time < 0.22:
            # Bayan (bass) resonance
            bf = 110.0 * math.exp(-12.0 * b_time) + 65.0
            tabla += 0.3 * math.sin(2 * math.pi * bf * b_time) * math.exp(-8.0 * b_time)
            # Dayan sweet tone
            tabla += 0.16 * math.sin(2 * math.pi * note_freq(N['C5']) * b_time) * math.exp(-15.0 * b_time)

        samples.append((tanpura + lead + tabla) * 0.85)

    write_wav("audio/barber/song1.wav", samples)

# Song 2: Ustad Ji Ka Sur (Ustadi Baithak)
def gen_barber_song2():
    bpm = 84
    beat_dur = 60.0 / bpm
    total_beats = 48
    dur = total_beats * beat_dur
    num_samples = int(SAMPLE_RATE * dur)

    # Fast melodic Sitar & Sarod jugalbandi in Raag Yaman
    yaman = [
        ('B3', 0.5), ('D4', 0.5), ('E4', 0.5), ('Gb4', 0.5),
        ('A4', 0.5), ('B4', 0.5), ('C5', 0.5), ('B4', 0.5),
        ('A4', 1.0), ('Gb4', 1.0), ('E4', 1.0), ('D4', 1.0),
        ('E4', 0.5), ('Gb4', 0.5), ('E4', 0.5), ('D4', 0.5),
        ('B3', 2.0),
        # Second cycle
        ('D4', 0.5), ('E4', 0.5), ('Gb4', 1.0), ('A4', 0.5), ('B4', 0.5),
        ('D5', 1.0), ('C5', 0.5), ('B4', 0.5), ('A4', 1.0),
        ('Gb4', 1.0), ('E4', 1.0), ('D4', 2.0)
    ]
    full_yaman = yaman + yaman

    events = []
    t_acc = 0.5
    for note, b in full_yaman:
        events.append((t_acc, b * beat_dur, note_freq(N[note])))
        t_acc += b * beat_dur

    samples = []
    for i in range(num_samples):
        t = i / SAMPLE_RATE

        # 1. Tanpura
        tanpura = 0.15 * math.sin(2 * math.pi * note_freq(N['D4']) * t) + 0.1 * math.sin(2 * math.pi * note_freq(N['A3']) * t)

        # 2. Fast Jhala Plucks
        lead = 0.0
        for st, nd, freq in events:
            if st <= t < st + nd + 0.1:
                dt = t - st
                pluck = (math.sin(2 * math.pi * freq * dt) + 0.7 * math.sin(2 * math.pi * freq * 2 * dt) + 0.4 * math.sin(2 * math.pi * freq * 3 * dt)) * math.exp(-3.8 * dt)
                lead += pluck * 0.45

        # 3. Fast Tabla Rupak Taal rhythm (Tin Tin Na Dhin Na Dhin Na)
        b_time = t % (beat_dur * 0.5)
        tabla = 0.0
        if b_time < 0.12:
            step = int(t / (beat_dur * 0.5)) % 7
            if step in [3, 5]:
                # Bayan bass
                tabla += 0.28 * math.sin(2 * math.pi * (100 * math.exp(-15 * b_time) + 60) * b_time) * math.exp(-10 * b_time)
            tabla += 0.15 * math.sin(2 * math.pi * note_freq(N['D5']) * b_time) * math.exp(-22 * b_time)

        samples.append((tanpura + lead + tabla) * 0.85)

    write_wav("audio/barber/song2.wav", samples)

# Song 3: Sham-E-Ghazal (Purani Haveli)
def gen_barber_song3():
    bpm = 66
    beat_dur = 60.0 / bpm
    total_beats = 40
    dur = total_beats * beat_dur
    num_samples = int(SAMPLE_RATE * dur)

    # Slow, deeply soulful evening Ghazal in Raag Kafi
    ghazal = [
        ('D4', 2.0), ('F4', 1.5), ('G4', 0.5), ('A4', 2.0),
        ('Bb4', 1.5), ('A4', 0.5), ('G4', 2.0),
        ('A4', 1.0), ('G4', 1.0), ('F4', 1.0), ('E4', 1.0),
        ('D4', 3.0), ('D4', 1.0),
        # She'r phrase
        ('D5', 2.0), ('C5', 1.0), ('Bb4', 1.0),
        ('A4', 1.5), ('Bb4', 0.5), ('A4', 2.0),
        ('G4', 1.5), ('F4', 0.5), ('E4', 1.0), ('F4', 1.0),
        ('D4', 4.0)
    ]

    events = []
    t_acc = 0.5
    for note, b in ghazal:
        events.append((t_acc, b * beat_dur, note_freq(N[note])))
        t_acc += b * beat_dur

    samples = []
    for i in range(num_samples):
        t = i / SAMPLE_RATE

        # 1. Sarangi / Violin bowed lead with smooth portamento & vibrato
        lead = 0.0
        for st, nd, freq in events:
            if st <= t < st + nd + 0.2:
                dt = t - st
                env = math.sin(math.pi * min(1.0, dt / (nd + 0.1)))
                vib = math.sin(2 * math.pi * 4.5 * dt) * 3.0 if dt > 0.2 else 0.0
                tone = math.sin(2 * math.pi * (freq + vib) * dt) + 0.35 * math.sin(2 * math.pi * (freq*2 + vib*2) * dt) + 0.2 * math.sin(2 * math.pi * (freq*3 + vib*3) * dt)
                lead += tone * env * 0.45

        # 2. Harmonium background drone chords
        h_chord = (math.sin(2 * math.pi * note_freq(N['D3']) * t) + 0.4 * math.sin(2 * math.pi * note_freq(N['A3']) * t)) * 0.12

        # 3. Delicate Ghazal Keharwa Tabla (soft Dayan tintinnabulation)
        b_time = t % beat_dur
        tabla = 0.0
        if b_time < 0.2:
            beat_idx = int(t / beat_dur) % 4
            if beat_idx == 0:
                tabla += 0.25 * math.sin(2 * math.pi * 85 * b_time) * math.exp(-8 * b_time)
            tabla += 0.12 * math.sin(2 * math.pi * note_freq(N['D5']) * b_time) * math.exp(-18 * b_time)

        samples.append((lead + h_chord + tabla) * 0.85)

    write_wav("audio/barber/song3.wav", samples)

# Song 4: Radio Ceylon Nostalgia (Aakashvani 1982)
def gen_barber_song4():
    bpm = 80
    beat_dur = 60.0 / bpm
    total_beats = 44
    dur = total_beats * beat_dur
    num_samples = int(SAMPLE_RATE * dur)

    # Classic Radio Ceylon / All India Radio signature chimes followed by retro tune
    chimes = [
        # AIR Signature interval chime (Famous Walter Kaufmann melody motif)
        ('C4', 1.0), ('G4', 1.0), ('C5', 1.5), ('G4', 0.5),
        ('E4', 1.5), ('F4', 0.5), ('D4', 2.0),
        # Radio Melody
        ('G4', 1.0), ('C5', 1.0), ('D5', 1.0), ('E5', 1.5), ('D5', 0.5),
        ('C5', 1.0), ('A4', 1.0), ('G4', 2.0),
        ('F4', 1.0), ('A4', 1.0), ('C5', 1.0), ('B4', 1.0),
        ('G4', 1.0), ('E4', 1.0), ('C4', 3.0),
        # Reprise
        ('E4', 1.0), ('G4', 1.0), ('C5', 2.0),
        ('D5', 1.0), ('B4', 1.0), ('C5', 3.0)
    ]

    events = []
    t_acc = 0.0
    for note, b in chimes:
        events.append((t_acc, b * beat_dur, note_freq(N[note])))
        t_acc += b * beat_dur

    samples = []
    for i in range(num_samples):
        t = i / SAMPLE_RATE

        # 1. Analog Transistor Chime / Synth Tone
        lead = 0.0
        for st, nd, freq in events:
            if st <= t < st + nd + 0.15:
                dt = t - st
                env = math.sin(math.pi * min(1.0, dt / (nd + 0.08)))
                tone = math.sin(2 * math.pi * freq * dt) + 0.45 * math.sin(2 * math.pi * freq * 2 * dt) + 0.2 * math.sin(2 * math.pi * freq * 3 * dt)
                lead += tone * env * 0.45

        # 2. Transistor radio mid-range filter / subtle tape flutter
        flutter = 1.0 + 0.004 * math.sin(2 * math.pi * 3.5 * t)

        # 3. Vintage Tabla / Bongo beat starting after initial chime (after 4 bars)
        perc = 0.0
        if t > 4 * beat_dur:
            b_time = t % beat_dur
            if b_time < 0.18:
                perc += 0.25 * math.sin(2 * math.pi * 90 * b_time) * math.exp(-10 * b_time)
                perc += 0.14 * math.sin(2 * math.pi * 520 * b_time) * math.exp(-22 * b_time)

        mix = (lead + perc) * flutter * 0.85
        samples.append(mix)

    write_wav("audio/barber/song4.wav", samples)

if __name__ == '__main__':
    print("Generating SFX...")
    gen_sfx()
    print("\nGenerating BUS WALE GAANE...")
    gen_bus_song1()
    gen_bus_song2()
    gen_bus_song3()
    gen_bus_song4()
    print("\nGenerating BARBER SHOP RADIO...")
    gen_barber_song1()
    gen_barber_song2()
    gen_barber_song3()
    gen_barber_song4()
    print("\nAll audio tracks successfully created!")
