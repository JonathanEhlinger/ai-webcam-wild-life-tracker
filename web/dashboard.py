from flask import Flask, render_template, Response
import time
import cv2

def run_dashboard(config, logger, detector):
    app = Flask(__name__)

    @app.route("/")
    def index():
        # Simple HTML page with video stream
        return """
        <html>
        <head><title>Wildlife Detection Dashboard</title></head>
        <body>
            <h1>Live Camera Feed</h1>
            <img src="/video_feed" width="640" height="480"/>
        </body>
        </html>
        """

    def gen_frames():
        print("Starting video stream generator...")
        frame_sent = 0
        while True:
            frame = detector.get_latest_frame()
            if frame is not None:
                ret, buffer = cv2.imencode('.jpg', frame)
                if not ret:
                    print("Warning: Failed to encode frame.")
                    time.sleep(0.03)
                    continue
                frame_bytes = buffer.tobytes()
                frame_sent += 1
                if frame_sent % 30 == 0:
                    print(f"Streamed {frame_sent} frames to client.")
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            else:
                print("Warning: No frame available to stream.")
                time.sleep(0.03)

    @app.route("/video_feed")
    def video_feed():
        print("Client connected to /video_feed")
        return Response(gen_frames(),
                        mimetype="multipart/x-mixed-replace; boundary=frame")

    @app.route("/events")
    def events():
        # TODO: Return event logs (JSON)
        return {"events": logger.get_events()}

    app.run(host="0.0.0.0", port=5000, debug=True)

# This Flask stub is a good starting point.
# You'll need to create HTML templates in a 'templates' subdirectory within 'web/'.
# Video streaming will require opencv to capture frames from the detector
# and format them for an HTTP multipart response.
# The /events route will fetch data from the EventLogger.
