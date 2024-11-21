 Real-Time Video Processing :

 GUI-based Video Processor Application using the tkinter library for the interface, cv2 from OpenCV for video processing, and Pillow for handling images.

Key Features :

Graphical User Interface (GUI):

--->Built using Tkinter to provide an intuitive interface for video processing tasks.
--->Includes multiple interactive buttons and canvases.

Video Uploading and Display:

--->Allows users to upload video files (.mp4, .avi) using a file dialog.
--->Displays video frames in real-time on the first canvas.

Real-Time Video Processing:

--->Converts video frames to grayscale and displays them on the second canvas.
--->Applies Canny edge detection and displays processed frames on the third canvas.

Multi-Threading for Smooth Performance:

--->Uses Python threading to perform real-time video processing without freezing the GUI.
--->Separate threads handle grayscale conversion and edge detection.

Playback Controls:

--->Replay functionality resets the video to the beginning for reprocessing or replay.
--->Delete functionality stops video processing and clears all canvases.
