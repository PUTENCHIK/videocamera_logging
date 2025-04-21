from numpy import ndarray
from datetime import datetime
from ultralytics.engine.results import Results

from src import Config


class DetectingResults:
    def __init__(self,
                 results: Results,
                 frame: ndarray,
                 detecting_time: float,
                 predicted_at: datetime):
        self.time = detecting_time
        self.frame = frame
        self.predicted_at = predicted_at
        result = results[0]
        if result.boxes:
            self.labels = [int(cls_.item()) for cls_ in result.boxes.cls]
            self.boxes = [xyxyn.tolist() for xyxyn in result.boxes.xyxyn]
            self.probs = [round(float(data[4]), 2) for data in result.boxes.data]
        else:
            self.labels = []
            self.boxes = []
            self.probs = []
    
    def __str__(self) -> str:
        return(f"Time: {round(self.time, 3)}\n"
               f"Labels: {self.labels}\n"
               f"Boxes: {self.boxes}\n"
               f"Probs: {self.probs}")
    
    def to_json(self) -> dict:
        objects = []
        for label, box, prob in zip(self.labels, self.boxes, self.probs):
            objects += [{
                "label": label,
                "box": box,
                "prob": prob,
            }]
        return {
            "time": self.time,
            "objects": objects
        }
    
    @property
    def any_objects(self) -> bool:
        return bool(self.labels)
