# Live Mic Audio Visualizer (Reverb)
<br>

This project captures live microphone input and applies a TAL-inspired reverb effect in real-time.
It includes:

  - Real-time microphone input with sounddevice
  - Adjustable Gain, Wet/Dry Mix, Decay, and Delay Size
  - Modern waveform visualizer with grid
  - Simple Tkinter GUI with vertical sliders and a stop button
  - Smooth and responsive reverb audio output

<br>

## Setup Instructions

### Clone and Prepare
```bash
git clone https://github.com/Rottie420/live-mic-reverb.git
cd live-mic-reverb

```

### Install the required Python packages from requirements.txt:

<br>

```bash
pip install -r requirements.txt

```

<br>

### GUI Details

<br>

**Canvas:** Displays real-time waveform with modern grid background

**Sliders:**
  - Gain — Controls overall signal amplification
  - Wet/Dry — Mix between clean and reverb signal
  - Decay — Controls how long the reverb tail lasts
  - Delay Size — Adjusts buffer size (reverb depth and delay time)
  - Stop Stream — Stops the audio stream and closes the app

<br>

### Audio Stream Configuration

<br>

  - Sample Rate: 44100 Hz (default)
  - Block Size: 1024 samples (default)
  - Gain: 1.0 (default)
  - Wet/Dry: 0.3 (default)
  - Decay: 0.5 (default)
  - Delay Size: 22050 (default)
  - Channels: 1 (mono input)
  - Data Type: float32

<br>

### Usage

<br>

Run the application:

```bash
python app.py

```

Adjust sliders to modify audio in real-time
Watch the waveform update dynamically on the canvas
Click Stop Stream to exit the application

<br>

### Notes

<br>

  - The waveform updates every 30 ms for smooth visualization.
  - Gain, wet/dry, decay, and delay sliders provide creative control
  - Ensure your microphone is connected and accessible
  - Recommended for experimenting with live mic audio effects
  
<br> <br> <br>