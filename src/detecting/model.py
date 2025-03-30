import time

from numpy import ndarray
from typing import Union, List
from pathlib import Path
from ultralytics import YOLO

from src import Config
from src.detecting.results import DetectingResults


class DetectingModel:
    def __init__(self,
                 model: str = Config.model.default):
        model_path = Config.pathes.models / model
        self.__model = YOLO(model_path) if model_path.exists() else None
    
    def predict(self,
                source: Union[str, Path, ndarray, list],
                ids: List[int],
                conf: float = Config.model.confidence) -> DetectingResults:
        start = time.perf_counter()
        results = self.__model.predict(source=source,
                                       conf=conf,
                                       verbose=False)
        detecting_time = time.perf_counter() - start

        return DetectingResults(results, ids, detecting_time)


detecting_model = DetectingModel()
