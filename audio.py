import cv2, pyautogui, time, keyboard, wave
from moviepy import VideoFileClip, AudioFileClip
import soundcard as sc
import numpy as np
from collections import deque

# Parameters
FPS = 30  # Frames per second
RECORD_SECONDS = 30  # Duration of the recording to keep (in seconds)
WIDTH, HEIGHT = pyautogui.size()  # Screen dimensions
BUFFER_SIZE = FPS * RECORD_SECONDS  # Number of frames to keep in memory

# Rolling buffer for frames (store the last 30 seconds of frames)
frame_buffer = deque(maxlen=BUFFER_SIZE)

# Audio recording setup using SoundCard
audio_buffer = []

# Get the default output device (system audio)
input_device = sc.default_speaker()  
samplerate = 44100  
channels = 1 
dtype = np.int16