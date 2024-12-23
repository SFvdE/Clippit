import tkinter as tk
from tkinter import filedialog

def choose_save_directory():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    selected_directory = filedialog.askdirectory(title="Select Save Directory")
    if selected_directory:
        print(f"Selected directory: {selected_directory}")
        return selected_directory
    else:
        print("No directory selected.")
        return None

if __name__ == "__main__":
    save_directory = choose_save_directory()
    if save_directory:
        # Save the selected directory to a file or use it directly in your application
        with open("save_directory.txt", "w") as f:
            f.write(save_directory)
