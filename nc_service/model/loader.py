from dataclasses import dataclass, field
from typing import List
import importlib

from .model import MLModel
from .exeptions import ModelLoadError

import joblib


@dataclass
class MLModelLoader:
    file_path: str
    model_dependencies: List = field(default_factory=list)

    def load(self) -> MLModel:
        self._load_imports()

        return self._load_model()

    def _load_imports(self):
        for import_name in self.model_dependencies:
            importlib.import_module(import_name)

    def _load_model(self) -> MLModel:
        try:
            print(self.file_path)
            model = joblib.load(self.file_path)

        except Exception as e:
            raise ModelLoadError(e)

        return MLModel(model)


def get_model(path: str, dependencies: List[str]) -> MLModel:
    return MLModelLoader(path, dependencies).load()


model = get_model('model2.joblib', ['sklearn'])
