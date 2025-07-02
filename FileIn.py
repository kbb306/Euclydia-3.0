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
	process = (ffmpeg
		.input(filename)
		.output('-', format='f32le', acodec='pcm_f32le', ar=48000, ac=1)
		.global_args('-map_metadata', '-1', '-vn')
		.overwrite_output()
		.run_async(pipe_stdout=True, pipe_stderr=subprocess.DEVNULL)
	)

	while process.poll() is None:
		packet = process.stdout.read(BUFFER_SIZE)
		yield packet
	process.wait()


def ggwave_decode(audio):
	for chunk in audio:
		res = ggwave.decode(instance, chunk)
		if res:
			text = res.decode("latin1")
			yield text


def ggwave_from_file(filename):
	audio = read_audio(filename)
	decoder = ggwave_decode(audio)

	for msg in decoder:
		yield msg
	