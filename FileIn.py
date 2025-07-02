import ggwave
import pyaudio
import ffmpeg
import subprocess
# FRAME_SIZE=4  # 32-bit samples @ 1 channel
FRAME_SIZE = 4
BUFFER_SIZE = 1024*FRAME_SIZE

parameters = ggwave.getDefaultParameters()
parameters["payloadLength"] = 16
instance = ggwave.init(parameters)

def read_audio(filename):
    print(f"[DEBUG] Reading audio from: {filename}")
    process = (
        ffmpeg
        .input(filename)
        .output('-', format='f32le', acodec='pcm_f32le', ar=48000, ac=1)
        .global_args('-map_metadata', '-1', '-vn')
        .overwrite_output()
        .run_async(pipe_stdout=True, pipe_stderr=subprocess.PIPE)
    )

    while True:
        packet = process.stdout.read(4096)
        if not packet:
            break
        yield packet

    stderr_output = process.stderr.read().decode(errors="ignore")
    yield ("[STDERR]", stderr_output)  # mark this specially

def ggwave_from_file(filename):
    audio = read_audio(filename)

    decoded_phrases = []
    stderr_output = ""

    for chunk in audio:
        if isinstance(chunk, tuple) and chunk[0] == "[STDERR]":
            stderr_output = chunk[1]
            break

        res = ggwave.decode(instance, chunk)
        if res:
            decoded_phrases.append(res)

    return decoded_phrases, stderr_output
