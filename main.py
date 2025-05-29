from config.config import load_config
from detection.detector import Detector
from eventlog.event_logger import EventLogger  # <-- updated import
from web.dashboard import run_dashboard

def main():
    config = load_config()
    logger = EventLogger(config)
    detector = Detector(config, logger)
    # Start detection in a separate thread if needed
    detector.start()
    # Start web dashboard (blocks main thread)
    run_dashboard(config, logger, detector)

if __name__ == "__main__":
    main()

# No changes to this file are needed.
# Please ensure the directory structure, __init__.py files,
# and dependencies (requirements.txt) are correctly set up
# as described in the instructions.
# This file appears correct, assuming sub-modules are correctly structured
# and __init__.py files are present in 'config', 'detection', 'eventlog', and 'web' directories.
