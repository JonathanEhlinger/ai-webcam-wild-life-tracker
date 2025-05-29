from flask import Flask, render_template, Response
from src.detection.yolo_detector import YOLODetector
from src.logging.event_logger import EventLogger

def create_app():
    app = Flask(__name__)

    # Initialize the YOLO detector and event logger
    detector = YOLODetector()
    logger = EventLogger()

    @app.route('/')
    def index():
        return render_template('index.html')

    def generate_frames():
        while True:
            frame, detections = detector.detect_objects()
            if frame is not None:
                # Log the detections
                for detection in detections:
                    logger.log_event(detection)
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    @app.route('/video_feed')
    def video_feed():
        return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

    return app