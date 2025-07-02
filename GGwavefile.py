# file: GGwavefile.py

import ggwave
import ffmpeg
import subprocess
import numpy as np
import wave

class ggwavin():
    """Credit to franga2000 on github: https://github.com/franga2000"""
    def __init__(self):
        self.FRAME_SIZE = 4
        self.BUFFER_SIZE = 1024 * self.FRAME_SIZE

        parameters = ggwave.getDefaultParameters()
        parameters["payloadLength"] = 16
        self.instance = ggwave.init(parameters)

    def read_audio(self, filename):
        print(f"[DEBUG] Reading audio from: {filename}")
        process = (
            ffmpeg
            .input(filename)
            .output('-', format='f32le', acodec='pcm_f32le', ar=48000, ac=1)
            .global_args('-map_metadata', '-1', '-vn')
            .overwrite_output()
            .run_async(pipe_stdout=True, pipe_stderr=subprocess.DEVNULL)
        )

        while process.poll() is None:
            packet = process.stdout.read(self.BUFFER_SIZE)
            print(f"[DEBUG] Read audio packet of size: {len(packet)}")
            yield packet

        process.wait()

    def ggwave_decode(self, audio):
        for chunk in audio:
            print(f"[DEBUG] Decoding audio chunk of size: {len(chunk)}")
            res = ggwave.decode(self.instance, chunk)
            if res:
                text = res.decode("latin1")
                print(f"[DEBUG] Decoded text: {repr(text)}")
                yield text

    def ggwave_from_file(self, filename):
        print(f"[DEBUG] Starting ggwave_from_file with: {filename}")
        audio = self.read_audio(filename)
        decoder = self.ggwave_decode(audio)
        for msg in decoder:
            print("[DEBUG] Yielding:", repr(msg))
            yield msg


class ggwavout():
    def __init__(self, filename):
        self.volume_ = 20
        self.sample_rate_ = 48000
        self.filename = filename

    def out(self, phrase, voice):
        waveform = ggwave.encode(phrase, voice, volume=self.volume_)
        waveform_float32 = np.frombuffer(waveform, dtype=np.float32)
        waveform_int16 = np.int16(waveform_float32 * 32767)

        with wave.open(self.filename, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(self.sample_rate_)
            wf.writeframes(waveform_int16.tobytes())
