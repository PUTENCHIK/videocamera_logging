from typing import List
from ultralytics.engine.results import Results

from src import Config


class DetectingResults:
    def __init__(self,
                 results: Results,
                 ids: List[int],
                 detecting_time: float):
        self.ids = ids
        self.time = detecting_time
        self.labels = []
        self.boxes = []
        self.probs = []
        for result in results:
            if result.boxes:
                self.labels += [[int(cls_.item()) for cls_ in result.boxes.cls]]
                self.boxes += [[xyxyn.tolist() for xyxyn in result.boxes.xyxyn]]
                self.probs += [[round(float(data[4]), 2) for data in result.boxes.data]]
            else:
                self.labels += [[]]
                self.boxes += [[]]
                self.probs += [[]]
    
    def __str__(self) -> str:
        return(f"Time: {round(self.time, 3)}\n"
               f"Cameras id: {self.ids}\n"
               f"Labels: {self.labels}\n"
               f"Boxes: {self.boxes}\n"
               f"Probs: {self.probs}\n")
    
    def to_json(self) -> dict:
        results = {}
        for camera_id, f_labels, f_boxes, f_probs in zip(self.ids, self.labels, self.boxes, self.probs):
            objects = []
            for label, box, prob in zip(f_labels, f_boxes, f_probs):
                objects += [{
                    "label": label,
                    "box": box,
                    "prob": prob,
                }]
            results[camera_id] = objects
        return {
            "time": self.time,
            "results": results
        }
    
    @property
    def any_objects(self) -> bool:
        return any([len(cls_) for cls_ in self.labels])
