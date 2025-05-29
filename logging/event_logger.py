import os
import json
from datetime import datetime

class EventLogger:
    def __init__(self, config):
        self.config = config
        self.log_path = os.path.join(config["data_dir"], f"events.{config['log_format']}")
        self.events = []

    def log_event(self, species, confidence, image_path, video_path=None):
        event = {
            "timestamp": datetime.now().isoformat(),
            "species": species,
            "confidence": confidence,
            "image": image_path,
            "video": video_path
        }
        self.events.append(event)
        self._save_event(event)

    def _save_event(self, event):
        if self.config["log_format"] == "json":
            with open(self.log_path, "a") as f:
                f.write(json.dumps(event) + "\n")
        # TODO: Add CSV support if needed

    def get_events(self, filters=None):
        # TODO: Implement filtering by date, species, etc.
        return self.events
