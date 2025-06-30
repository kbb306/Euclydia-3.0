import ggwave
import simpleaudio as sa
import time

def play_waveform(waveform):
    # Normalize the waveform to 16-bit PCM and play it using simpleaudio
    import numpy as np
    samples = np.frombuffer(waveform, dtype=np.float32)
    scaled = (samples * 32767).astype(np.int16)
    sa.play_buffer(scaled.tobytes(), 1, 2, 48000)
    time.sleep(5.5)  # delay to avoid overlap

protocols = []

print("Testing available protocols...\n")

for pid in range(32):  # Try more, as many as might exist
    try:
        phrase = f"Testing protocol {pid}"
        waveform = ggwave.encode(phrase, protocolId=pid)
        protocols.append(pid)
        print(f"✅ Protocol {pid}: Playing → {phrase}")
        play_waveform(waveform)
    except Exception as e:
        print(f"❌ Protocol {pid} failed: {e}")
        continue

print("\n✅ Available protocol IDs:", protocols)
