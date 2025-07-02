import ggwave
import pyaudio
import wave
import numpy as np
from GGwavefile import *
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

    def main(self):
        while True:
            choice = int(input("""Select an action:
                                1. Play a phrase in Euclydian
                                2. Listen for a phrase in Euclydian
                                3. Decode a recording.
                                4. Create a recording
                                5. Quit
                                
                               Selection: """))
            if choice == 1:
                self.say()
            elif choice == 2:
                self.listen()
            elif choice == 3:
                file = input("Enter a file path: ")
                self.filein(file)
            elif choice == 4:
                file = input("Enter a file path: ")
                self.fileout(file)
            elif choice == 5:
                print("Goodbye.")
                break

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
        readaloud = ggwavin()
        compressed = readaloud.ggwave_from_file(file)
        phrase = self.middleman.decode(compressed)
        print(phrase)

    def fileout(self,file):
        talksay = ggwavout(file)
        phrase = input("Enter a phrase: ")
        print(self.voice_map.keys())
        voice = input("Enter a voice: ")
        codephrase = self.middleman.encode(phrase)
        talksay.out(codephrase,self.voice_map[voice])

Alex = translator()

