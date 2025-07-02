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
        
        self.main()

    def say(self,phrase,voice):
        codephrase = compress(phrase)
        print(codephrase)
        p = pyaudio.PyAudio()
        waveform = ggwave.encode(codephrase, self.voice_map[voice] , volume = 20)

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
                decoded = ggwave.decode(instance, data)

                if decoded:
                    try:
                        message = decompress(decoded)
                        print("Received message:", message)
                    except Exception as e:
                        print(f"[Decompression error] {e}")

        except KeyboardInterrupt:
            pass

        ggwave.free(instance)

        stream.stop_stream()
        stream.close()

        p.terminate()


    def filein(filepath):
        # Open the WAV file—must be 48 kHz mono 32‑bit float RAW
        wf = wave.open(filepath, 'rb')
        assert wf.getframerate() == 48000, "WAV must be 48 kHz"
        assert wf.getnchannels() == 1, "WAV must be mono"
        
        # Initialize ggwave decoder
        params = ggwave.getDefaultParameters()
        instance = ggwave.init(params)
        
        # Read chunks
        chunk_size = 1024 * wf.getsampwidth()
        while True:
            data = wf.readframes(chunk_size)
            if not data:
                break
            res = ggwave.decode(instance, data)
            if res:
                text = res.decode('utf-8', errors='ignore')
                print("Decoded:", text)

        wf.close()
        ggwave.free(instance)

    def fileout(self, phrase, voice, filename):
        #Compress the phrase
        codephrase = compress(phrase)
        # Encode the phrase with GGWave
        waveform = ggwave.encode(codephrase,voice, volume=20)

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
                        5. Exit
                        
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
                    
