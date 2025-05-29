# Wildlife Detection System (Desktop GUI)

## Features
- Live camera feed with camera selection
- YOLOv8 AI detection (bounding boxes and labels)
- Save frames and log detections
- View logs in-app

## Setup

1. Install Python 3.10+.
2. Create and activate a virtual environment (optional but recommended).
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the GUI:
   ```
   python main_gui.py
   ```

## Usage

- Use **Options** to select your camera index.
- Click **Start Camera** to view the feed.
- Toggle **Enable AI Detection** for bounding boxes.
- Click **Save Frame** to save and log detections.
- Click **View Logs** to see detection history.

## How to Post This Project to GitHub

1. **Initialize a git repository (if you haven't already):**
   ```
   git init
   ```

2. **Add all files:**
   ```
   git add .
   ```

3. **Commit your changes:**
   ```
   git commit -m "Initial commit of wildlife detection system"
   ```

4. **Add your GitHub remote:**
   ```
   git remote add origin https://github.com/joanthanehlinger/ai-webcam-wild-life-tracker.git
   ```

5. **Push your code to GitHub:**
   ```
   git branch -M main
   git push -u origin main
   ```

6. **Your code is now posted to GitHub!**