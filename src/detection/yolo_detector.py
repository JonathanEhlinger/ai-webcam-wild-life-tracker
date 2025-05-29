class YOLODetector:
    def __init__(self, model_path: str, target_species: list, confidence_threshold: float = 0.5):
        self.model_path = model_path
        self.target_species = target_species
        self.confidence_threshold = confidence_threshold
        self.model = self.load_model()

    def load_model(self):
        import cv2
        from ultralytics import YOLO
        
        model = YOLO(self.model_path)
        return model

    def detect_objects(self, frame):
        results = self.model(frame)
        detections = []
        
        for result in results:
            for box in result.boxes:
                if box.conf > self.confidence_threshold:
                    species = box.cls
                    if species in self.target_species:
                        detections.append({
                            'species': species,
                            'confidence': box.conf,
                            'bbox': box.xyxy
                        })
        return detections

    def get_detections(self, video_source):
        import cv2
        
        cap = cv2.VideoCapture(video_source)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            detections = self.detect_objects(frame)
            yield frame, detections
        
        cap.release()