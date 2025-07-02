import ggwave
import pyaudio
import ffmpeg
import subprocess
class ggwav():
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
                text = res.decode("utf-8")
                yield text


    def ggwave_from_file(self,filename):
        audio = self.read_audio(filename)
        decoder = self.ggwave_decode(audio)

        return list(decoder)
        
translator = ggwav()
msg = translator.ggwave_from_file(input("Enter a file path: "))
print(msg)