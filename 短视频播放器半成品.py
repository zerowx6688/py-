import os
import tkinter as tk
from tkinter import filedialog
import vlc

class ShortVideoPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("短视频播放器")
        self.root.geometry("450x700")  # 设置窗口尺寸为428x700

        self.video_folder = ""
        self.video_files = []
        self.current_video_index = 0

        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()

        self.create_menu()  # 创建菜单栏

        self.video_frame = tk.Frame(root)
        self.video_frame.pack()

        self.title_label = tk.Label(root, text="", padx=10, pady=10)
        self.title_label.pack()

        self.prev_button = tk.Button(root, text="上一个", command=self.play_previous_video)
        self.prev_button.pack(side="left", padx=10, pady=10)

        self.next_button = tk.Button(root, text="下一个", command=self.play_next_video)
        self.next_button.pack(side="right", padx=10, pady=10)

        self.progress_bar = tk.Scale(root, from_=0, to=100, orient="horizontal", length=600, command=self.update_progress)
        self.progress_bar.pack()

        self.video_canvas = tk.Canvas(self.video_frame, width=800, height=600)
        self.video_canvas.pack()

        self.root.bind("<Left>", self.play_previous_video)
        self.root.bind("<Right>", self.play_next_video)
        self.root.bind("<Up>", self.adjust_volume_up)
        self.root.bind("<Down>", self.adjust_volume_down)
        self.root.bind("<Left>", self.seek_backward)
        self.root.bind("<Right>", self.seek_forward)

    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="选项", menu=file_menu)
        file_menu.add_command(label="选择视频文件夹", command=self.load_video_folder)
        file_menu.add_command(label="显示视频列表", command=self.show_video_list)

    def load_video_folder(self):
        self.video_folder = filedialog.askdirectory()
        video_extensions = (".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm", ".m4v")
        self.video_files = [f for f in os.listdir(self.video_folder) if f.lower().endswith(video_extensions)]
        if self.video_files:
            self.play_video()

    def play_video(self):
        media = self.instance.media_new(os.path.join(self.video_folder, self.video_files[self.current_video_index]))
        self.player.set_media(media)
        self.player.set_hwnd(self.video_canvas.winfo_id())
        self.player.play()
        self.progress_bar.set(0)  # 重置进度条位置
        self.update_title_label()  # 更新标题标签

    def play_previous_video(self, event=None):
        if self.current_video_index > 0:
            self.current_video_index -= 1
            self.play_video()

    def play_next_video(self, event=None):
        if self.current_video_index < len(self.video_files) - 1:
            self.current_video_index += 1
            self.play_video()

    def update_progress(self, value):
        # 将进度条的值映射到视频的时间位置并设置播放位置
        if self.player.get_length():
            position = int((float(value) / 100) * self.player.get_length())
            self.player.set_time(position)

    def show_video_list(self):
        if self.video_files:
            video_list_window = tk.Toplevel(self.root)
            video_list_window.title("视频列表")

            video_list = tk.Listbox(video_list_window)
            for video_file in self.video_files:
                video_list.insert(tk.END, video_file)
            video_list.pack()

            video_list.bind("<Double-Button-1>", self.on_video_list_double_click)

    def on_video_list_double_click(self, event):
        selected_index = event.widget.curselection()
        if selected_index:
            self.current_video_index = selected_index[0]
            self.play_video()

    def update_title_label(self):
        if self.video_files:
            current_title = self.video_files[self.current_video_index]
            self.title_label.config(text="当前播放：" + current_title)

    def adjust_volume_up(self, event=None):
        current_volume = self.player.audio_get_volume()
        if current_volume < 100:
            self.player.audio_set_volume(current_volume + 10)

    def adjust_volume_down(self, event=None):
        current_volume = self.player.audio_get_volume()
        if current_volume > 0:
            self.player.audio_set_volume(current_volume - 10)

    def seek_forward(self, event=None):
        current_time = self.player.get_time()
        new_time = current_time + 15000  # 增加15秒
        if new_time <= self.player.get_length():
            self.player.set_time(new_time)

    def seek_backward(self, event=None):
        current_time = self.player.get_time()
        new_time = current_time - 15000  # 减少15秒
        if new_time >= 0:
            self.player.set_time(new_time)

    def on_closing(self):
        self.video_files = []
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ShortVideoPlayer(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
