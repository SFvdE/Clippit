import cv2, pyautogui, time, keyboard, wave, os
import soundcard as sc
import numpy as np
from collections import deque

# Parameters
FPS = 30  
RECORD_SECONDS = 30  
WIDTH, HEIGHT = pyautogui.size() 
BUFFER_SIZE = FPS * RECORD_SECONDS  

# Read the save directory from a file if it exists
save_directory_file = "save_directory.txt"
if os.path.exists(save_directory_file):
    with open(save_directory_file, "r") as f:
        SAVE_DIRECTORY = f.read().strip()
else:
    SAVE_DIRECTORY = os.path.join(os.path.dirname(__file__), "recordings")

# Ensure the save directory exists
if not os.path.exists(SAVE_DIRECTORY):
    os.makedirs(SAVE_DIRECTORY)
    print(f"Created directory: {SAVE_DIRECTORY}")
else:
    print(f"Directory already exists: {SAVE_DIRECTORY}")

# Rolling buffer for frames
frame_buffer = deque(maxlen=BUFFER_SIZE)

# Video writer setup
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
    
    for frame in frame_buffer:
        out.write(frame)
    
    out.release()
    print(f"Recording saved as {filename}")

# screen recording 
def record_screen():
    print("Recording... Press 'ctrl+a' to save the last 30 seconds. Press 'ESC' to stop.")

    while True:
        # screenshot
        img = pyautogui.screenshot()
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # buffer
        frame_buffer.append(frame)

        # Save
        if keyboard.is_pressed("ctrl+a"):
            print("Saving the last 30 seconds...")
            save_video_from_buffer()
            time.sleep(1)  # Prevent multiple triggers while holding the key

        # Quit
        if keyboard.is_pressed("esc"):
            print("Recording stopped.")
            break

    cv2.destroyAllWindows()

# Run the recording function
if __name__ == "__main__": 
    record_screen()
