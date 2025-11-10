import sounddevice as sd
import numpy as np
import tkinter as tk
from tkinter import ttk

# === INITIAL CONFIG ===
SAMPLE_RATE = 44100
BLOCK_SIZE = 1024
GAIN = 1.0
WET_DRY = 0.3
DECAY = 0.5
DELAY_SIZE = 22050  # 0.5 sec default

# Buffers
waveform_data = np.zeros(BLOCK_SIZE)
reverb_buffer = np.zeros(DELAY_SIZE)
reverb_index = 0
stream = None  # initialized later

# === AUDIO EFFECT ===
def tal_reverb(indata):
    global waveform_data, reverb_buffer, reverb_index
    dry = indata[:, 0]
    output = np.zeros_like(dry)

    # Vectorized circular buffer
    idx = (reverb_index + np.arange(len(dry))) % len(reverb_buffer)
    output[:] = dry * (1 - WET_DRY) + reverb_buffer[idx] * WET_DRY
    reverb_buffer[idx] = dry + reverb_buffer[idx] * DECAY
    reverb_index = (reverb_index + len(dry)) % len(reverb_buffer)

    # Apply gain and clip
    output *= GAIN
    output = np.clip(output, -1.0, 1.0)

    waveform_data[:] = output
    return output.reshape(-1, 1)

# === AUDIO CALLBACK ===
def audio_callback(indata, outdata, frames, time, status):
    if status:
        print("Audio status:", status)
    outdata[:] = tal_reverb(indata)

# === STREAM MANAGEMENT ===
def start_stream():
    global stream
    if stream:
        try:
            stream.stop()
            stream.close()
        except Exception:
            pass
    stream = sd.Stream(channels=1,
                       samplerate=SAMPLE_RATE,
                       blocksize=BLOCK_SIZE,
                       dtype='float32',
                       callback=audio_callback)
    stream.start()

def restart_stream():
    start_stream()

# === GUI CALLBACKS ===
def update_gain(val):
    global GAIN
    GAIN = float(val)

def update_wet(val):
    global WET_DRY
    WET_DRY = float(val)

def update_decay(val):
    global DECAY
    DECAY = float(val)

def update_delay(val):
    global DELAY_SIZE, reverb_buffer, reverb_index
    DELAY_SIZE = int(float(val))
    reverb_buffer = np.zeros(DELAY_SIZE)
    reverb_index = 0

# === VISUALIZER ===
def update_visualizer():
    canvas.delete("wave")
    canvas.delete("grid")

    h = canvas.winfo_height()
    w = canvas.winfo_width()

    # === Modern Grid ===
    grid_color = "#2A2A2A"
    # Vertical lines (every 50 px)
    for x in range(0, w, 50):
        canvas.create_line(x, 0, x, h, fill=grid_color, width=1, tags="grid")
    # Horizontal lines (every 25 px)
    for y in range(0, h, 25):
        canvas.create_line(0, y, w, y, fill=grid_color, width=1, tags="grid")
    # Center line (0 axis)
    canvas.create_line(0, h/2, w, h/2, fill="#444", width=1, tags="grid")

    # === Waveform ===
    if waveform_data is not None and len(waveform_data) > 0:
        step = max(1, len(waveform_data) // w)
        for i in range(0, len(waveform_data) - step, step):
            x0 = i / len(waveform_data) * w
            y0 = h / 2 - waveform_data[i] * h / 2
            x1 = (i + step) / len(waveform_data) * w
            y1 = h / 2 - waveform_data[i + step] * h / 2
            canvas.create_line(x0, y0, x1, y1, fill="cyan", width=1, tags="wave")

    root.after(30, update_visualizer)


# === GUI ===
root = tk.Tk()
root.title("Live Mic (Reverb)")
root.configure(bg="#F0F0F0")
root.resizable(False, False)

canvas = tk.Canvas(root, bg="#1E1E1E", height=150)
canvas.pack(fill="x", padx=20, pady=15)

frame = ttk.Frame(root, padding=20)
frame.pack()

# Gain
ttk.Label(frame, text="Gain").grid(row=0, column=0, padx=10)
gain_slider = ttk.Scale(frame, from_=5.0, to=0.1, orient="vertical", command=update_gain, length=150)
gain_slider.set(GAIN)
gain_slider.grid(row=1, column=0, padx=10)

# Wet/Dry
ttk.Label(frame, text="Wet/Dry").grid(row=0, column=1, padx=10)
wet_slider = ttk.Scale(frame, from_=1.0, to=0.0, orient="vertical", command=update_wet, length=150)
wet_slider.set(WET_DRY)
wet_slider.grid(row=1, column=1, padx=10)

# Decay
ttk.Label(frame, text="Decay").grid(row=0, column=2, padx=10)
decay_slider = ttk.Scale(frame, from_=0.95, to=0.0, orient="vertical", command=update_decay, length=150)
decay_slider.set(DECAY)
decay_slider.grid(row=1, column=2, padx=10)

# Delay Size
ttk.Label(frame, text="Delay Size").grid(row=0, column=3, padx=10)
delay_slider = ttk.Scale(frame, from_=44100, to=515, orient="vertical", command=update_delay, length=150)
delay_slider.set(DELAY_SIZE)
delay_slider.grid(row=1, column=3, padx=10)

# Stop
stop_button = ttk.Button(frame, text="Stop Stream", command=lambda: (stream.stop(), root.destroy()))
stop_button.grid(row=2, column=0, columnspan=4, pady=20)

# === START ===
start_stream()
update_visualizer()
root.mainloop()

if stream:
    stream.stop()
    stream.close()
