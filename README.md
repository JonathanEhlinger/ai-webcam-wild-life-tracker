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

6. **Your code is now posted to GitHub at:**
   ```
   https://github.com/joanthanehlinger/ai-webcam-wild-life-tracker
   ```

## Troubleshooting "Repository not found" on git push

If you see:
```
remote: Repository not found.
fatal: repository 'https://github.com/joanthanehlinger/ai-webcam-wild-life-tracker.git/' not found
```
**This means the repository does not exist on GitHub or you do not have permission.**

### How to fix:

1. **Go to [https://github.com/new](https://github.com/new) and create a new repository**  
   - Name it: `ai-webcam-wild-life-tracker`
   - Make sure it is under your account: `jonathanehlinger`

2. **Do NOT initialize with a README, .gitignore, or license** (your local repo already has these).

3. **After creating the repo, run these commands again in your terminal:**
   ```
   git remote remove origin
   git remote add origin https://github.com/jonathanehlinger/ai-webcam-wild-life-tracker.git
   git push -u origin main
   ```

If prompted, log in with your GitHub credentials or use a personal access token.

## Pushing to your GitHub repository

1. **If you haven't already, create the repository at:**  
   https://github.com/JonathanEhlinger/ai-webcam-wild-life-tracker

2. **Update your remote and push:**
   ```
   git remote remove origin
   git remote add origin https://github.com/JonathanEhlinger/ai-webcam-wild-life-tracker.git
   git push -u origin main
   ```

3. **If prompted, log in with your GitHub credentials or use a personal access token.**

4. **Your code will now be live at:**  
   https://github.com/JonathanEhlinger/ai-webcam-wild-life-tracker

## Fixing "Malformed input to a URL function" when pushing to GitHub

You have a typo or extra character in your remote URL.  
**To fix:**

1. Remove the incorrect remote:
   ```
   git remote remove origin
   ```

2. Add the correct remote (no extra characters, no trailing `?` or `/`):
   ```
   git remote add origin https://github.com/JonathanEhlinger/ai-webcam-wild-life-tracker.git
   ```

3. Push your code:
   ```
   git push -u origin main
   ```

If prompted, log in with your GitHub credentials or use a personal access token.

## Fixing "Updates were rejected because the remote contains work that you do not have locally"

This means your GitHub repository already has some commits (like a README or .gitignore created on GitHub).

**To fix:**

1. **Pull the remote changes and merge:**
   ```
   git pull origin main --allow-unrelated-histories
   ```

2. **Resolve any merge conflicts if prompted.**

3. **Add and commit any resolved files:**
   ```
   git add .
   git commit -m "Merge remote-tracking branch 'origin/main'"
   ```

4. **Push your code:**
   ```
   git push -u origin main
   ```