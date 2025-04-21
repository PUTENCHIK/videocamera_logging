import time

from numpy import ndarray
from datetime import datetime
from ultralytics import YOLO

from src import Config
from src.detecting.results import DetectingResults


class DetectingModel:
    def __init__(self,
                 model: str = Config.detecting.model_name):
        self.model_path = Config.pathes.models / model
        self.__model = YOLO(self.model_path) if self.model_path.exists() else None
    
    def predict(self,
                frame: ndarray,
                predicted_at: datetime,
                conf: float = Config.detecting.confidence) -> DetectingResults:
        start = time.perf_counter()
        results = self.__model.predict(source=frame,
                                       conf=conf,
                                       verbose=False)
        detecting_time = time.perf_counter() - start

        return DetectingResults(results, frame, detecting_time, predicted_at)
    
    @property
    def model_specified(self) -> bool:
        return self.model_path.exists() and self.__model is not None


detecting_model = DetectingModel()
