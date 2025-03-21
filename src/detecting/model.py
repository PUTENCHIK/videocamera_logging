import time

from numpy import ndarray
from typing import Union
from pathlib import Path
from ultralytics import YOLO

from src import Config
from src import DetectingResults


class DetectingModel:
    def __init__(
            self,
            model: str = Config.model_name
        ):
        self.__model = YOLO(Config.model_storage / model)
    
    def predict(
            self,
            source: Union[str, Path, ndarray],
            conf: float = Config.model_confidence
        ) -> DetectingResults:
        start = time.time()
        results = self.__model.predict(source=source, conf=conf)
        detecting_time = time.time() - start

        return DetectingResults(results, detecting_time)
