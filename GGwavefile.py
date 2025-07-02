import ggwave
import pyaudio
import ffmpeg
import subprocess
import numpy as np
import wave
class ggwavin():
    """Credit to franga2000 on github: https://github.com/franga2000"""
    def __init__(self):
        # FRAME_SIZE=4  # 32-bit samples @ 1 channel
        self.FRAME_SIZE = 4
        self.BUFFER_SIZE = 1024*self.FRAME_SIZE

        parameters = ggwave.getDefaultParameters()
        parameters["payloadLength"] = 16
        self.instance = ggwave.init(parameters)

    def read_audio(self,filename):
        process = (ffmpeg
            .input(filename)
            .output('-', format='f32le', acodec='pcm_f32le', ar=48000, ac=1)
            .global_args('-map_metadata', '-1', '-vn')
            .overwrite_output()
            .run_async(pipe_stdout=True, pipe_stderr=subprocess.DEVNULL)
        )

        while process.poll() is None:
            packet = process.stdout.read(self.BUFFER_SIZE)
            yield packet
        process.wait()


    def ggwave_decode(self,audio):
        for chunk in audio:
            res = ggwave.decode(self.instance, chunk)
            if res:
                text = res.decode("latin1")
                yield text


    def ggwave_from_file(self,filename):
        audio = self.read_audio(filename)
        decoder = self.ggwave_decode(audio)
        for msg in decoder:
            yield msg
        
class ggwavout():
    def __init__(self,filename):
        # Parameters
        self.volume_ = 20
        self.sample_rate_ = 48000
        self.filename = filename

    def out(self,phrase,voice):
        # Generate audio waveform for string "hello python"
        waveform = ggwave.encode(phrase, voice, volume=self.volume_)

        # Convert byte data into float32
        waveform_float32 = np.frombuffer(waveform, dtype=np.float32)

        # Normalize the float32 data to the range of int16
        waveform_int16 = np.int16(waveform_float32 * 32767)

        # Save the waveform to a .wav file
        with wave.open(self.filename, "wb") as wf:
            wf.setnchannels(1)                  # mono audio
            wf.setsampwidth(2)                  # 2 bytes per sample (16-bit PCM)
            wf.setframerate(self.sample_rate_)       # sample rate
            wf.writeframes(waveform_int16.tobytes())  # write the waveform as bytes        
