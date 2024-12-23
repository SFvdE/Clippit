import tkinter as tk
from Explorer import choose_save_directory 
import threading
import sys
import os

# Ensure the text module is in the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from text import start_recording, stop_recording, save_last_30_seconds, record_screen

def directory():
    save_directory = choose_save_directory()
    if save_directory:
        with open("save_directory.txt", "w") as f:
            f.write(save_directory)
        print(f"Save directory set to: {save_directory}")

# Create the main window
root = tk.Tk()
root.title("Recorder")
root.geometry("400x300")

# Set the background color to #252526
root.config(bg="#252526")

# Add a label with a contrasting color
label = tk.Label(root, text="", font=("Arial", 16), bg="#252526", fg="white")
label.pack(pady=20)

# Start recording
def start_recording_thread():
    threading.Thread(target=start_recording).start()

# Save the last 30 seconds
def save_last_30_seconds_thread():
    threading.Thread(target=save_last_30_seconds).start()

# Start the recording and buffering when the GUI starts
recording_thread = threading.Thread(target=record_screen, daemon=True)
recording_thread.start()

# Add buttons with the same color scheme
start_button = tk.Button(root, text="Start Recording", bg="#252526", fg="white", command=start_recording_thread, activebackground="#3c3f41", activeforeground="white")
start_button.pack(pady=10)

save_button = tk.Button(root, text="Save Last 30 Seconds", bg="#252526", fg="white", command=save_last_30_seconds_thread, activebackground="#3c3f41", activeforeground="white")
save_button.pack(pady=10)

stop_button = tk.Button(root, text="Stop Recording", bg="#252526", fg="white", command=stop_recording, activebackground="#3c3f41", activeforeground="white")
stop_button.pack(pady=10)

directory_button = tk.Button(root, text="Select directory", bg="#252526", fg="white", command=directory, activebackground="#3c3f41", activeforeground="white")
directory_button.pack(pady=10)

# Run the application
root.mainloop()
