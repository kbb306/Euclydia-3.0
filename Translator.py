import ggwave
import pyaudio
from smaz import compress, decompress
import wave
class translator():
    def __init__(self):
        self.p = pyaudio.PyAudio()
    def say(self,phrase):
        waveform = ggwave.encode(compress(phrase), protocolId = 1, volume = 20)

        stream = p.open(format=pyaudio.paFloat32, channels=1, rate=48000, output=True, frames_per_buffer=4096)
        stream.write(waveform, len(waveform)//4)
        stream.stop_stream()
        stream.close()

        self.p.terminate()
    
    def listen(self):
        stream = self.p.open(format=pyaudio.paFloat32, channels=1, rate=48000, input=True, frames_per_buffer=1024)

        print('Listening ... Press Ctrl+C to stop')
        instance = ggwave.init()

        try:
            while True:
                data = stream.read(1024, exception_on_overflow=False)
                res = decompress(ggwave.decode(instance, data))
                if (not res is None):
                    try:
                        print('Received text: ' + res.decode("utf-8"))
                    except:
                        pass
        except KeyboardInterrupt:
            pass

        ggwave.free(instance)

        stream.stop_stream()
        stream.close()

        self.p.terminate()

    def file(self,file):
        pass
        
