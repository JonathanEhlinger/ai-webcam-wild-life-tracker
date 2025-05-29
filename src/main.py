from detection.yolo_detector import YOLODetector
from logging.event_logger import EventLogger
from dashboard.app import create_app

def main():
    # Initialize the YOLO detector
    detector = YOLODetector()
    detector.load_model()

    # Initialize the event logger
    logger = EventLogger()

    # Create the Flask web application
    app = create_app(detector, logger)

    # Start the web application
    app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == "__main__":
    main()