import tkinter as tk
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk
import threading

class VideoProcessorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Video Processor")
        
        self.canvas1 = tk.Canvas(master, width=400, height=300)
        self.canvas1.grid(row=0, column=0, padx=10, pady=10)
        
        self.canvas2 = tk.Canvas(master, width=400, height=300)
        self.canvas2.grid(row=0, column=1, padx=10, pady=10)
        
        self.canvas3 = tk.Canvas(master, width=400, height=300)
        self.canvas3.grid(row=0, column=2, padx=10, pady=10)
        
        self.upload_button = tk.Button(master, text="Upload Video", command=self.upload_video)
        self.upload_button.grid(row=1, column=0, padx=10, pady=10)
        
        self.delete_button = tk.Button(master, text="Delete Video", command=self.delete_video)
        self.delete_button.grid(row=1, column=3, padx=10, pady=10)
        
        self.bgr2gray_button = tk.Button(master, text="Convert to Grayscale", command=self.convert_to_grayscale)
        self.bgr2gray_button.grid(row=1, column=1, padx=10, pady=10)
        
        self.canny_button = tk.Button(master, text="Apply Canny Edge", command=self.apply_canny_edge)
        self.canny_button.grid(row=1, column=2, padx=10, pady=10)
        
        self.replay_button = tk.Button(master, text="Replay", command=self.replay_videos)
        self.replay_button.grid(row=1, column=4, padx=10, pady=10)
        
        self.video = None
        self.stop_threads = False
        self.process_gray = False
        self.process_edges = False
        self.video_lock = threading.Lock()  # Create a lock for video access
        
    def upload_video(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.avi")])
        if file_path:
            if self.video is not None:
                self.video.release()  # Release the previous video capture object
                self.video = None  # Reset the video object
            self.video = cv2.VideoCapture(file_path)
            self.show_frame()
            
    def show_frame(self):
        _, frame = self.video.read()
        if frame is not None:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_pil = Image.fromarray(frame_rgb)
            frame_tk = ImageTk.PhotoImage(frame_pil)
            self.canvas1.create_image(0, 0, anchor=tk.NW, image=frame_tk)
            self.canvas1.image = frame_tk
            
            if self.process_gray:
                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                gray_frame_pil = Image.fromarray(gray_frame)
                gray_frame_tk = ImageTk.PhotoImage(gray_frame_pil)
                self.canvas2.create_image(0, 0, anchor=tk.NW, image=gray_frame_tk)
                self.canvas2.image = gray_frame_tk
                
            if self.process_edges:
                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                edges_frame = cv2.Canny(gray_frame, 100, 200)
                edges_frame_pil = Image.fromarray(edges_frame)
                edges_frame_tk = ImageTk.PhotoImage(edges_frame_pil)
                self.canvas3.create_image(0, 0, anchor=tk.NW, image=edges_frame_tk)
                self.canvas3.image = edges_frame_tk
                
            if not self.stop_threads:
                self.master.after(10, self.show_frame)
            
    def delete_video(self):
        self.stop_threads = True
        if self.video is not None:
            self.video.release()
            self.video = None  # Reset the video object
        self.canvas1.delete("all")
        self.canvas2.delete("all")
        self.canvas3.delete("all")
        
    def convert_to_grayscale(self):
        self.process_gray = True
        self.stop_threads = False
        threading.Thread(target=self._convert_to_grayscale_thread).start()

    def _convert_to_grayscale_thread(self):
        while not self.stop_threads:
            with self.video_lock:  # Acquire the lock before accessing self.video
                ret, frame = self.video.read()
            if not ret:
                break
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray_frame_pil = Image.fromarray(gray_frame)
            gray_frame_tk = ImageTk.PhotoImage(gray_frame_pil)
            self.canvas2.create_image(0, 0, anchor=tk.NW, image=gray_frame_tk)
            self.canvas2.image = gray_frame_tk
            self.master.update()  # Update the window to display the new frame

    def apply_canny_edge(self):
        self.process_edges = True
        self.stop_threads = False
        threading.Thread(target=self._apply_canny_edge_thread).start()

    def _apply_canny_edge_thread(self):
        while not self.stop_threads:
            with self.video_lock:  # Acquire the lock before accessing self.video
                ret, frame = self.video.read()
            if not ret:
                break
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            edges_frame = cv2.Canny(gray_frame, 100, 200)
            edges_frame_pil = Image.fromarray(edges_frame)
            edges_frame_tk = ImageTk.PhotoImage(edges_frame_pil)
            self.canvas3.create_image(0, 0, anchor=tk.NW, image=edges_frame_tk)
            self.canvas3.image = edges_frame_tk
            self.master.update()
            
    def replay_videos(self):
        # Reset flags and reinitialize video capture object
        self.stop_threads = False
        self.process_gray = True
        self.process_edges = True
        if self.video is not None:
            self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Reset video to the beginning
        self.show_frame()

def main():
    root = tk.Tk()
    app = VideoProcessorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
