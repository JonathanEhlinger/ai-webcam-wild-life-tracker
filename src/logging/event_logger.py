class EventLogger:
    def __init__(self, json_file='data/logs/events.json', csv_file='data/logs/events.csv'):
        self.json_file = json_file
        self.csv_file = csv_file
        self.events = []

    def log_event(self, timestamp, species, confidence):
        event = {
            'timestamp': timestamp,
            'species': species,
            'confidence': confidence
        }
        self.events.append(event)
        self.save_to_json(event)
        self.save_to_csv(event)

    def save_to_json(self, event):
        import json
        try:
            with open(self.json_file, 'a') as json_file:
                json.dump(event, json_file)
                json_file.write('\n')  # Write each event on a new line
        except Exception as e:
            print(f"Error saving to JSON: {e}")

    def save_to_csv(self, event):
        import csv
        try:
            with open(self.csv_file, 'a', newline='') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=event.keys())
                if csv_file.tell() == 0:  # Check if file is empty to write header
                    writer.writeheader()
                writer.writerow(event)
        except Exception as e:
            print(f"Error saving to CSV: {e}")