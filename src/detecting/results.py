from typing import List
from ultralytics.engine.results import Results

from src import Config


class DetectingResults:
    def __init__(
            self,
            results: Results,
            ids: List[int],
            detecting_time: float
        ):
        self.ids = ids
        self.time = detecting_time
        self.classes = []
        self.boxes = []
        self.probs = []
        for i, result in enumerate(results):
            if result.boxes:
                self.classes += [[int(cls_) for cls_ in result.boxes.cls]]
                self.boxes += [[list(map(int, [*xyxy])) for xyxy in result.boxes.xyxy]]
                self.probs += [[round(float(data[4]), 2) for data in result.boxes.data]]
            else:
                self.classes += [[]]
                self.boxes += [[]]
                self.probs += [[]]
    
    def __str__(self) -> str:
        return(f"Time: {round(self.time, 3)}\n"
               f"Cameras id: {self.ids}\n"
               f"Classes: {self.classes}\n"
               f"Classes names: {self.classes_names}\n"
               f"Boxes: {self.boxes}\n"
               f"Probs: {self.probs}\n")
    
    def to_json(self) -> dict:
        results = {}
        for camera_id, f_classes, f_classes_names, f_boxes, f_probs in zip(self.ids, self.classes, self.classes_names, self.boxes, self.probs):
            objects = []
            for cls_, cls_name, box, prob in zip(f_classes, f_classes_names, f_boxes, f_probs):
                objects += [{
                    "class_index": cls_,
                    "class_name": cls_name,
                    "box": box,
                    "prob": prob,
                }]
            results[camera_id] = objects
        return {
            "time": self.time,
            "results": results
        }

    @property
    def classes_names(self) -> list:
        return [[Config.detecting_classes_names[cls_] for cls_ in class_] for class_ in self.classes]
    
    @property
    def any_objects(self) -> bool:
        return any([len(cls_) for cls_ in self.classes])
