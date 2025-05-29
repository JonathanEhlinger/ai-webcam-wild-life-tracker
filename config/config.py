import json
import os

DEFAULT_CONFIG = {
    "confidence_threshold": 0.5,
    "target_species": ["squirrel", "bird", "dog", "human", "snake"],
    "enable_speech": False,
    "data_dir": "data",
    "log_format": "json",
    "camera_index": 1  # Try 1 for NexiGO, change to 2 or 3 if needed
}

def load_config(path="config.json"):
    if os.path.exists(path):
        with open(path, "r") as f:
            try:
                user_config = json.load(f)
            except json.JSONDecodeError:
                print(f"Error: {path} is not a valid JSON file. Using default configuration.")
                user_config = {}
        config = {**DEFAULT_CONFIG, **user_config}
    else:
        config = DEFAULT_CONFIG
    os.makedirs(config["data_dir"], exist_ok=True)
    return config
