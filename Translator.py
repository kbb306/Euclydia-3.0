import ggwave
import pyaudio
from smaz import compress, decompress
import wave
import numpy as np
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
        self.p = pyaudio.PyAudio()
        self.main()
        
    def say(self,phrase,voice):
        waveform = ggwave.encode(compress(phrase), self.voice_map[voice] , volume = 20)

        stream = self.p.open(format=pyaudio.paFloat32, channels=1, rate=48000, output=True, frames_per_buffer=4096)
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

    def filein(self, file):
        # Open the .wav file
        wf = wave.open(file, 'rb')

        # Ensure it's mono, 48000 Hz, 16-bit PCM
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != 48000:
            print("Unsupported audio format: must be 48000 Hz, 16-bit mono.")
            return

        # Initialize GGWave decoder
        instance = ggwave.init()

        try:
            while True:
                frames = wf.readframes(1024)
                if not frames:
                    break

                decoded = ggwave.decode(instance, frames)

                if decoded:
                    try:
                        message = decompress(decoded).decode("utf-8")
                        print("Received message:", message)
                    except Exception as e:
                        print(f"[Decompression error] {e}")
        finally:
            ggwave.free(instance)
            wf.close()

    

    def fileout(self, phrase, voice, filename):
        # Encode the phrase with GGWave
        waveform = ggwave.encode(phrase, self.voice_map[voice], volume=20)

        # Convert from float32 (used by ggwave) to int16 PCM
        samples = np.frombuffer(waveform, dtype=np.float32)
        pcm_data = np.int16(samples * 32767)

        # Write to WAV file
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(1)              # mono
            wf.setsampwidth(2)              # 2 bytes per sample (16-bit)
            wf.setframerate(48000)          # standard GGWave rate
            wf.writeframes(pcm_data.tobytes())

        print(f"[Saved] {phrase} → {filename}")

        
    def main(self):
        choice = 0
        while True:
            choice = int(input("""Say, listen, or use file?
                        1. Say
                        2. Listen
                        3. Input file
                        4. Output file
                        
                        Choice: """))
            
            if choice == 1:
                phrase = input("Enter a short phrase (<100 characters): ")
                print(self.voice_map.keys())
                voice = input("Select a voice: ")
                self.say(phrase, voice)

            elif choice == 2:
                self.listen()
            
            elif choice == 3:
                path = input("Enter file path: ")
                self.filein(path)

            elif choice == 4:
                path = input("Enter a filepath: ")
                print(self.voice_map.keys())
                voice = input("Enter a voice: ")
                phrase = input("Enter a short phrase (<100 characters): ")
                self.fileout(phrase,self.voice_map[voice],path)
            
            elif choice == 5:
                print("Goodbye!")
                break


Alex = translator()       
                    
