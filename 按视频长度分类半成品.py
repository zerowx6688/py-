from moviepy.editor import VideoFileClip
import os
import shutil
import tkinter as tk
from tkinter import filedialog

def categorize_videos(input_folder, short_output_folder, long_output_folder, threshold=1200):
    # Create output folders if they don't exist
    if not os.path.exists(short_output_folder):
        os.makedirs(short_output_folder)
    if not os.path.exists(long_output_folder):
        os.makedirs(long_output_folder)

    # Get a list of video files in the input folder
    supported_video_formats = ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.mpeg', '.3gp', '.m4v', '.ogv', '.rm', '.vob', '.ts', '.asf', '.divx']
    video_files = [f for f in os.listdir(input_folder) if any(f.lower().endswith(ext) for ext in supported_video_formats)]

    # Create lists to temporarily hold videos for moving
    videos_to_move_short = []
    videos_to_move_long = []

    for video_file in video_files:
        video_path = os.path.join(input_folder, video_file)
        try:
            video_duration = VideoFileClip(video_path).duration
        except Exception as e:
            print(f"Error processing '{video_file}': {e}")
            continue

        if video_duration >= threshold:
            videos_to_move_long.append(video_file)
        else:
            videos_to_move_short.append(video_file)

    # Move videos to the appropriate folders
    for video_file in videos_to_move_long:
        src_path = os.path.join(input_folder, video_file)
        dest_path = os.path.join(long_output_folder, video_file)
        shutil.move(src_path, dest_path)
        print(f"Moved '{video_file}' to '{long_output_folder}'")

    for video_file in videos_to_move_short:
        src_path = os.path.join(input_folder, video_file)
        dest_path = os.path.join(short_output_folder, video_file)
        shutil.move(src_path, dest_path)
        print(f"Moved '{video_file}' to '{short_output_folder}'")

def select_input_folder():
    folder = filedialog.askdirectory()
    input_folder_var.set(folder)

def select_short_output_folder():
    folder = filedialog.askdirectory()
    short_output_folder_var.set(folder)

def select_long_output_folder():
    folder = filedialog.askdirectory()
    long_output_folder_var.set(folder)

def run_categorization():
    input_folder = input_folder_var.get()
    short_output_folder = short_output_folder_var.get()
    long_output_folder = long_output_folder_var.get()
    categorize_videos(input_folder, short_output_folder, long_output_folder, threshold=1200)  # Using 1200 seconds (20 minutes)

# Create the main GUI window
root = tk.Tk()
root.title("视频分类工具")

# Set the window size
window_width = 250
window_height = 300
root.geometry(f"{window_width}x{window_height}")

# Create and place labels and entry fields for input, short output, and long output folders
tk.Label(root, text="原视频文件夹：").pack()
input_folder_var = tk.StringVar()
input_folder_entry = tk.Entry(root, textvariable=input_folder_var)
input_folder_entry.pack()
tk.Button(root, text="选择文件夹", command=select_input_folder).pack()

tk.Label(root, text="短视频输出文件夹：").pack()
short_output_folder_var = tk.StringVar()
short_output_folder_entry = tk.Entry(root, textvariable=short_output_folder_var)
short_output_folder_entry.pack()
tk.Button(root, text="选择文件夹", command=select_short_output_folder).pack()

tk.Label(root, text="长视频输出文件夹：").pack()
long_output_folder_var = tk.StringVar()
long_output_folder_entry = tk.Entry(root, textvariable=long_output_folder_var)
long_output_folder_entry.pack()
tk.Button(root, text="选择文件夹", command=select_long_output_folder).pack()

# Create and place the "Run" button
run_button = tk.Button(root, text="开始分类", command=run_categorization)
run_button.pack(pady=10)  # Adding vertical padding

# Run the GUI event loop
root.mainloop()
