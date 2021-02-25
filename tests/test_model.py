import asyncio
import numpy as np
from dataclasses import dataclass
from typing import List, Union, Callable

import pytest

from nc_service.model import MLModel, ModelPredictError
from nc_service.schemas import PredictRequest, PredictResponse


def predict(data: List[List[Union[int, str]]]) -> np.ndarray:
    res = []

    for row in data:
        res.append(list(map(lambda x: x ** 2, row)))

    return np.array(res)


def predict_error(*args, **kwargs):
    raise ValueError


@dataclass
class Model:
    predict_func: Callable

    def predict(self, data: List[List[Union[int, str]]]) -> List[List[Union[int, str]]]:
        return self.predict_func(data)


def test_predict():
    test_data = [
        [1, 2, 3],
        [4, 5, 6]
    ]

    c_data = predict(test_data).tolist()

    ml_model = MLModel(model=Model(predict_func=predict))

    res = asyncio.run(ml_model.predict_async(PredictRequest(data=test_data)))

    assert res == PredictResponse(result=c_data)


def test_predict_with_error():
    ml_model = MLModel(model=Model(predict_func=predict_error))

    with pytest.raises(ModelPredictError):
        asyncio.run(ml_model.predict_async(PredictRequest(data=[])))
