import cv2, pyautogui, time, os
import numpy as np
from threading import Lock


# Parameters
FPS = 30  
RECORD_SECONDS = 30  
WIDTH, HEIGHT = pyautogui.size() 
BUFFER_SIZE = FPS * RECORD_SECONDS

save_directory_file = "save_directory.txt"

def get_save_directory():
    if os.path.exists(save_directory_file):
        with open(save_directory_file, "r") as f:
            return f.read().strip()
    else:
        return os.path.join(os.path.dirname(__file__), "recordings")

SAVE_DIRECTORY = get_save_directory()

if not os.path.exists(SAVE_DIRECTORY):
    os.makedirs(SAVE_DIRECTORY)
    print(f"Created directory: {SAVE_DIRECTORY}")
else:
    print(f"Directory already exists: {SAVE_DIRECTORY}")

# buffer
frame_buffer = [None] * BUFFER_SIZE  # Initialize buffer with fixed size
buffer_lock = Lock()  # Create a lock for the buffer
recording = False  # Start with no recording

# Video
def create_video_writer(output_filename, fps, width, height):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    return cv2.VideoWriter(output_filename, fourcc, fps, (width, height))

# Save the video from the buffer
def save_video_from_buffer():
    timestamp = time.strftime("%d-%m-%Y_%H-%M-%S")
    filename = f"recording_{timestamp}.mp4"
    output_filepath = os.path.join(SAVE_DIRECTORY, filename)
    print(f"Saving to: {output_filepath}")  # Debug print
    out = create_video_writer(output_filepath, FPS, WIDTH, HEIGHT)
    
    with buffer_lock:  # Lock the buffer during iteration
        buffer_copy = frame_buffer.copy()  # Create a copy of the buffer
    for frame in buffer_copy:
        out.write(frame)
    
    out.release()
    print(f"Recording saved as {filename}")

# Start recording
def start_recording():
    global recording
    recording = True
    print("Recording started...")

# Stop recording
def stop_recording():
    global recording
    recording = False
    print("Recording stopped.")

# Save the last 30 seconds
def save_last_30_seconds():
    print("Saving the last 30 seconds...")
    save_video_from_buffer()

# Screen recording loop
def record_screen():
    global recording
    buffer_index = 0  # Initialize buffer index
    while True:
        if recording:
            # screenshot
            img = pyautogui.screenshot()
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # buffer
            with buffer_lock:  # Lock the buffer during modification
                frame_buffer[buffer_index] = frame
                buffer_index = (buffer_index + 1) % BUFFER_SIZE  # Circular buffer logic

        time.sleep(1 / FPS)

# Run the recording function
if __name__ == "__main__":
    record_screen()

