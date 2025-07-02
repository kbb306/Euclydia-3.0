import ggwave
import pyaudio
from smaz import compress, decompress
import wave
import numpy as np
from GGwavefilein import *
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

    