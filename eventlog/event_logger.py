import json
from datetime import datetime

class EventLogger:
    def __init__(self, log_file='events.json'):
        self.log_file = log_file

    def log_event(self, event_type, details):
        event = {
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            'details': details
        }
        self._save_event(event)

    def _save_event(self, event):
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(event) + '\n')

    # This is a good basic logger.
    # For _save_event, if multiple processes/threads might write,
    # consider file locking or a more robust logging mechanism for production.
    # The get_events() method will need implementation for actual filtering.