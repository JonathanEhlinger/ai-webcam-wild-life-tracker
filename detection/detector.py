import threading
import cv2
import time
import numpy as np

class Detector:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.running = False
        self.cap = None
        self.latest_frame = None
        self.lock = threading.Lock()
        self.camera_index = config.get("camera_index", 0)  # Default to 0 if not set

    def start(self):
        self.running = True
        thread = threading.Thread(target=self.run, daemon=True)
        thread.start()

    def run(self):
        print(f"Attempting to open webcam with DirectShow backend at index {self.camera_index}...")
        self.cap = cv2.VideoCapture(self.camera_index, cv2.CAP_DSHOW)
        if not self.cap.isOpened():
            print(f"Error: Could not open webcam at index {self.camera_index} with DirectShow backend.")
            self.running = False
            return
        print("Webcam opened successfully.")
        print(f"Frame width: {self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)}")
        print(f"Frame height: {self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)}")
        print(f"FPS: {self.cap.get(cv2.CAP_PROP_FPS)}")
        frame_count = 0
        while self.running:
            ret, frame = self.cap.read()
            if not ret or frame is None:
                print(f"Warning: Failed to grab frame from webcam at index {self.camera_index}.")
                time.sleep(0.5)
                continue
            print(f"Frame {frame_count} captured from camera index {self.camera_index}.")
            frame = cv2.resize(frame, (640, 480))
            with self.lock:
                self.latest_frame = frame.copy()
            frame_count += 1
            if frame_count % 30 == 0:
                print(f"Captured {frame_count} frames from camera index {self.camera_index}.")
            time.sleep(0.03)  # ~30 FPS, reduces CPU usage
        if self.cap is not None:
            self.cap.release()
            print("Webcam released.")

    def get_latest_frame(self):
        with self.lock:
            if self.latest_frame is not None:
                return self.latest_frame.copy()
            else:
                return None
