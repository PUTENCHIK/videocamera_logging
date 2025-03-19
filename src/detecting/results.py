import ultralytics
import ultralytics.engine
import ultralytics.engine.results

from src import Config


class DetectingResults:
    def __init__(
            self,
            results: ultralytics.engine.results.Results,
            detecting_time: float
        ):
        self.time = detecting_time
        self.classes = [int(cls_) for cls_ in results[0].boxes.cls]
        self.boxes = [list(map(int, [*xyxy])) for xyxy in results[0].boxes.xyxy]
        self.probs = [round(float(data[4]), 2) for data in results[0].boxes.data]
    
    def __str__(self) -> str:
        return f"({round(self.time, 3)} s): {[pair for pair in zip(self.classes_names, self.probs)]}"
    
    def to_json(self) -> dict:
        return {
            "time": self.time,
            "objects": [{
                "index": i,
                "class_index": cls_,
                "class_name": Config.detecting_classes_names[cls_],
                "box": self.boxes[i],
                "prob": self.probs[i]
            } for i, cls_ in enumerate(self.classes)]
        }

    @property
    def classes_names(self) -> list:
        return [Config.detecting_classes_names[i] for i, _ in enumerate(self.classes)]
