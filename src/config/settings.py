# Configuration settings for the wildlife detection system

# Detection parameters
DETECTION_CONFIDENCE_THRESHOLD = 0.5  # Minimum confidence threshold for detections
TARGET_SPECIES = ['squirrel', 'bird', 'dog', 'human', 'snake']  # List of species to detect

# Logging settings
LOGGING_ENABLED = True  # Enable or disable event logging
LOG_FORMAT = 'json'  # Format for logging events ('json' or 'csv')

# Web dashboard settings
DASHBOARD_PORT = 5000  # Port for the Flask web application
DEBUG_MODE = True  # Enable or disable debug mode for the web application

# Speech interaction settings
SPEECH_INTERACTION_ENABLED = False  # Enable or disable speech interaction
WHISPER_MODEL_PATH = 'path/to/whisper/model'  # Path to the Whisper model for speech recognition

# Other settings
IMAGE_SAVE_PATH = 'data/samples/images/'  # Directory to save detected images
VIDEO_SAVE_PATH = 'data/samples/videos/'  # Directory to save detected video clips
EVENT_LOG_PATH_JSON = 'data/logs/events.json'  # Path for JSON log file
EVENT_LOG_PATH_CSV = 'data/logs/events.csv'  # Path for CSV log file