import ggwave
import pyaudio
import wave
import numpy as np
from GGwavefilein import *
from smaz_encode import *
class translator():
    def __init__(self):
        self.voice_map = {
            "FC": 2,
            "FA": 1,
            "MC": 8,
            "MA": 7,
            "SC": 0,
            "EU": 6,
        }
        self.middleman = smaz_wrapper()
        
        self.main()
    def say(self):
        p = pyaudio.PyAudio()

        phrase = input("Enter text <100 characters: ")
        codephrase = self.middleman.encode(phrase)
        print(self.voice_map.keys())
        voice = input("Select a voice: ")
        waveform = ggwave.encode(codephrase, self.voice_map[voice], volume = 20)

        
        stream = p.open(format=pyaudio.paFloat32, channels=1, rate=48000, output=True, frames_per_buffer=4096)
        stream.write(waveform, len(waveform)//4)
        stream.stop_stream()
        stream.close()

        p.terminate()

    def listen(self):
        p = pyaudio.PyAudio()

        stream = p.open(format=pyaudio.paFloat32, channels=1, rate=48000, input=True, frames_per_buffer=1024)

        print('Listening ... Press Ctrl+C to stop')
        instance = ggwave.init()

        try:
            while True:
                data = stream.read(1024, exception_on_overflow=False)
                res = ggwave.decode(instance, data)
                if (not res is None):
                    try:
                        phrase = self.middleman.decode(res.decode('latin1'))
                        print("Recieved text:"+ phrase)
                    except:
                        pass
        except KeyboardInterrupt:
            pass

        ggwave.free(instance)

        stream.stop_stream()
        stream.close()

        p.terminate()

    def filein(self,file):
        readaloud = ggwav()
        compressed_list = readaloud.ggwave_from_file(file)
        out = []
        for each in compressed_list:
            unzip = self.middleman.decode(each)
            out.append(unzip)
        for each in out:
            print(each)


