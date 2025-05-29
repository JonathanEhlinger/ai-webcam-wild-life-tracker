import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import cv2
from PIL import Image, ImageTk
import threading
import time
import os
import json
import platform
import subprocess

try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False

CONFIG_PATH = "config.json"
LOG_PATH = "data/events.json"

class CameraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Wildlife Detection System")
        self.running = False
        self.frame = None
        self.detected = []
        self.camera_index = self.load_camera_index()
        self.cap = None
        self.ai_enabled = tk.BooleanVar(value=True)
        self.model = YOLO("yolov8n.pt") if YOLO_AVAILABLE else None

        # UI Layout
        self.video_label = tk.Label(root)
        self.video_label.pack()

        btn_frame = tk.Frame(root)
        btn_frame.pack(fill=tk.X, pady=5)
        self.start_btn = tk.Button(btn_frame, text="Start Camera", command=self.start_camera)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        self.stop_btn = tk.Button(btn_frame, text="Stop Camera", command=self.stop_camera, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        self.save_btn = tk.Button(btn_frame, text="Save Frame", command=self.save_frame, state=tk.DISABLED)
        self.save_btn.pack(side=tk.LEFT, padx=5)
        self.options_btn = tk.Button(btn_frame, text="Options", command=self.show_options)
        self.options_btn.pack(side=tk.LEFT, padx=5)
        self.logs_btn = tk.Button(btn_frame, text="View Logs", command=self.show_logs)
        self.logs_btn.pack(side=tk.LEFT, padx=5)
        self.ai_check = tk.Checkbutton(btn_frame, text="Enable AI Detection", variable=self.ai_enabled)
        self.ai_check.pack(side=tk.LEFT, padx=5)
        self.live_log_btn = tk.Button(btn_frame, text="Live Log", command=self.show_live_log)
        self.live_log_btn.pack(side=tk.LEFT, padx=5)
        self.recording = False
        self.video_writer = None
        self.record_btn = tk.Button(btn_frame, text="Start Recording", command=self.toggle_recording)
        self.record_btn.pack(side=tk.LEFT, padx=5)
        self.record_label = tk.Label(btn_frame, text="")
        self.record_label.pack(side=tk.LEFT, padx=5)

        self.live_log_window = None
        self.live_log_text = None
        self.simple_log = tk.BooleanVar(value=True)
        self.update_job = None

    def load_camera_index(self):
        # Try to auto-select NexiGo if present
        cam_list, cam_map = self.enumerate_cameras_with_names()
        for display in cam_list:
            if "nexigo" in display.lower():
                return cam_map[display]
        # Fallback to config or first available
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, "r") as f:
                config = json.load(f)
            return config.get("camera_index", 0)
        if cam_list:
            return cam_map[cam_list[0]]
        return 0

    def start_camera(self):
        self.cap = self.open_camera_with_fallback(self.camera_index)
        if not self.cap or not self.cap.isOpened():
            messagebox.showerror("Error", f"Could not open camera index {self.camera_index}")
            return
        self.running = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.save_btn.config(state=tk.NORMAL)
        self.update_frame_gui()  # Use after() instead of thread

    def open_camera_with_fallback(self, index):
        # Try DSHOW, MSMF, and default backends
        for backend in [cv2.CAP_DSHOW, cv2.CAP_MSMF, None]:
            if backend is not None:
                cap = cv2.VideoCapture(index, backend)
            else:
                cap = cv2.VideoCapture(index)
            if cap.isOpened():
                return cap
            cap.release()
        return None

    def stop_camera(self):
        self.running = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.save_btn.config(state=tk.DISABLED)
        if self.cap:
            self.cap.release()
            self.cap = None
        if self.update_job:
            self.root.after_cancel(self.update_job)
            self.update_job = None
        if self.recording:
            self.toggle_recording()

    def toggle_recording(self):
        if not self.recording:
            save_dir = "data"
            os.makedirs(save_dir, exist_ok=True)
            filename = time.strftime("%Y%m%d_%H%M%S.avi")
            self.record_path = os.path.join(save_dir, filename)
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            self.video_writer = cv2.VideoWriter(self.record_path, fourcc, 20.0, (640, 480))
            self.recording = True
            self.record_btn.config(text="Stop Recording")
            self.record_label.config(text=f"Recording: {filename}")
        else:
            self.recording = False
            if self.video_writer:
                self.video_writer.release()
                self.video_writer = None
            self.record_btn.config(text="Start Recording")
            self.record_label.config(text="Saved: " + os.path.basename(self.record_path))

    def update_frame_gui(self):
        if self.running and self.cap:
            ret, frame = self.cap.read()
            if ret:
                self.frame = frame
                display_frame = frame.copy()
                detections = []
                if self.ai_enabled.get() and YOLO_AVAILABLE and self.model:
                    results = self.model.predict(display_frame, imgsz=640, conf=0.4, verbose=False)
                    for r in results:
                        for box in r.boxes:
                            x1, y1, x2, y2 = map(int, box.xyxy[0])
                            cls = int(box.cls[0])
                            conf = float(box.conf[0])
                            label = self.model.names[cls] if hasattr(self.model, "names") else str(cls)
                            detections.append({"label": label, "conf": conf, "box": [x1, y1, x2, y2]})
                            cv2.rectangle(display_frame, (x1, y1), (x2, y2), (0,255,0), 2)
                            cv2.putText(display_frame, f"{label} {conf:.2f}", (x1, y1-10),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
                self.detected = [(d["box"][0], d["box"][1], d["box"][2], d["box"][3], d["label"], d["conf"]) for d in detections]
                self.update_live_log(detections)
                rgb = cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(rgb)
                imgtk = ImageTk.PhotoImage(image=img.resize((640, 480)))
                self.video_label.imgtk = imgtk
                self.video_label.config(image=imgtk)
                # Save frame to video if recording
                if self.recording and self.video_writer:
                    self.video_writer.write(cv2.resize(display_frame, (640, 480)))
            self.update_job = self.root.after(30, self.update_frame_gui)  # ~33 FPS

    def save_frame(self):
        if self.frame is not None:
            save_dir = "data"
            os.makedirs(save_dir, exist_ok=True)
            filename = time.strftime("%Y%m%d_%H%M%S.jpg")
            path = os.path.join(save_dir, filename)
            cv2.imwrite(path, self.frame)
            self.log_event(filename)
            messagebox.showinfo("Saved", f"Frame saved to {path}")

    def log_event(self, image_filename):
        os.makedirs("data", exist_ok=True)
        event = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "camera_index": self.camera_index,
            "detections": [
                {"label": label, "conf": conf, "box": [x1, y1, x2, y2]}
                for (x1, y1, x2, y2, label, conf) in self.detected
            ],
            "image": image_filename
        }
        with open(LOG_PATH, "a") as f:
            f.write(json.dumps(event) + "\n")

    def show_options(self):
        opt = tk.Toplevel(self.root)
        opt.title("Options")
        tk.Label(opt, text="Camera Index:").pack(side=tk.LEFT, padx=5)
        idx_var = tk.IntVar(value=self.camera_index)
        idx_entry = tk.Entry(opt, textvariable=idx_var, width=5)
        idx_entry.pack(side=tk.LEFT, padx=5)
        def save_idx():
            self.camera_index = idx_var.get()
            with open(CONFIG_PATH, "w") as f:
                json.dump({"camera_index": self.camera_index}, f)
            messagebox.showinfo("Saved", "Camera index updated. Restart camera to apply.")
            opt.destroy()
        tk.Button(opt, text="Save", command=save_idx).pack(side=tk.LEFT, padx=5)

        # Improved camera selection dropdown with device names
        tk.Label(opt, text=" | Quick Select: ").pack(side=tk.LEFT)
        cam_list, cam_map = self.enumerate_cameras_with_names()
        cam_var = tk.StringVar(value=cam_list[0] if cam_list else "")
        cam_menu = ttk.Combobox(opt, textvariable=cam_var, values=cam_list, width=40)
        cam_menu.pack(side=tk.LEFT)
        def select_cam():
            idx_var.set(cam_map.get(cam_var.get(), 0))
        cam_menu.bind("<<ComboboxSelected>>", lambda e: select_cam())

        # Add a Test Cameras button
        def test_cameras():
            test_win = tk.Toplevel(opt)
            test_win.title("Test Cameras")
            label = tk.Label(test_win)
            label.pack()
            idxs = [cam_map[c] for c in cam_list]
            current = [0]  # mutable for closure

            def show_frame():
                idx = idxs[current[0]]
                cap = self.open_camera_with_fallback(idx)
                if cap and cap.isOpened():
                    ret, frame = cap.read()
                    if ret:
                        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        from PIL import Image, ImageTk
                        img = Image.fromarray(rgb)
                        imgtk = ImageTk.PhotoImage(image=img.resize((320, 240)))
                        label.imgtk = imgtk
                        label.config(image=imgtk)
                        label.after(100, show_frame)
                    cap.release()
            def next_cam():
                current[0] = (current[0] + 1) % len(idxs)
                show_frame()
            def prev_cam():
                current[0] = (current[0] - 1) % len(idxs)
                show_frame()
            btn_prev = tk.Button(test_win, text="<< Prev", command=prev_cam)
            btn_prev.pack(side=tk.LEFT)
            btn_next = tk.Button(test_win, text="Next >>", command=next_cam)
            btn_next.pack(side=tk.LEFT)
            show_frame()
        tk.Button(opt, text="Test Cameras", command=test_cameras).pack(side=tk.LEFT, padx=5)

    def enumerate_cameras_with_names(self, max_test=10):
        """
        Returns (list of display names, dict of display name -> index)
        Shows Windows-reported camera names and device instance paths.
        """
        available = []
        cam_map = {}
        cam_names = []
        cam_paths = []
        if platform.system() == "Windows":
            try:
                # Get camera names
                result = subprocess.run(
                    [
                        "powershell",
                        "-Command",
                        "Get-CimInstance Win32_PnPEntity | Where-Object {$_.Service -eq 'usbvideo'} | Select-Object Name,DeviceID"
                    ],
                    capture_output=True, text=True, timeout=5
                )
                # Parse output for Name and DeviceID
                lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
                for line in lines:
                    if "DeviceID" in line:
                        cam_paths.append(line.split(":",1)[-1].strip())
                    elif "Name" in line:
                        cam_names.append(line.split(":",1)[-1].strip())
            except Exception:
                pass
        name_idx = 0
        path_idx = 0
        for i in range(max_test):
            cap = self.open_camera_with_fallback(i)
            if cap and cap.isOpened():
                # Try to assign a name and path from Windows list in order
                display = f"{i}: "
                if name_idx < len(cam_names):
                    display += cam_names[name_idx]
                    name_idx += 1
                else:
                    display += "Camera"
                if path_idx < len(cam_paths):
                    display += f" [{cam_paths[path_idx]}]"
                    path_idx += 1
                available.append(display)
                cam_map[display] = i
                cap.release()
        return available, cam_map

    def show_logs(self):
        log_win = tk.Toplevel(self.root)
        log_win.title("Event Logs")
        text = tk.Text(log_win, width=100, height=25)
        text.pack()
        if os.path.exists(LOG_PATH):
            with open(LOG_PATH, "r") as f:
                for line in f:
                    text.insert(tk.END, line)
        else:
            text.insert(tk.END, "No logs found.")

    def show_live_log(self):
        if self.live_log_window and tk.Toplevel.winfo_exists(self.live_log_window):
            self.live_log_window.lift()
            return
        self.live_log_window = tk.Toplevel(self.root)
        self.live_log_window.title("Live AI Log")
        self.live_log_text = tk.Text(self.live_log_window, width=80, height=20)
        self.live_log_text.pack()
        simple_check = tk.Checkbutton(self.live_log_window, text="Simple Log", variable=self.simple_log)
        simple_check.pack()
        self.live_log_window.after(500, self.refresh_live_log)

    def update_live_log(self, detections):
        # Store the latest detections for the log window
        self.latest_detections = detections

    def refresh_live_log(self):
        if self.live_log_window and self.live_log_text:
            self.live_log_text.delete(1.0, tk.END)
            if hasattr(self, "latest_detections") and self.latest_detections:
                if self.simple_log.get():
                    # Show a summary: just the object names and counts
                    summary = {}
                    for d in self.latest_detections:
                        summary[d["label"]] = summary.get(d["label"], 0) + 1
                    lines = [f"{label}: {count}" for label, count in summary.items()]
                    self.live_log_text.insert(tk.END, "Detected objects:\n" + "\n".join(lines))
                else:
                    # Show detailed info
                    for d in self.latest_detections:
                        self.live_log_text.insert(
                            tk.END,
                            f"{d['label']} ({d['conf']:.2f}) at {d['box']}\n"
                        )
            else:
                self.live_log_text.insert(tk.END, "No detections.")
            self.live_log_window.after(500, self.refresh_live_log)

    def on_close(self):
        self.stop_camera()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = CameraApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
