from dataclasses import dataclass

import numpy as np
from fastapi.testclient import TestClient

from nc_service.app import get_app


@dataclass
class Model:

    def predict(self, *args, **kwargs) -> np.ndarray:
        return np.array([[0]])


def test_predict(mocker):
    mocker.patch('joblib.load', return_value=Model())

    app = get_app()

    client = TestClient(app)

    data = {"data": [[1]]}

    assert client.post('/predict', json=data).json().get('result') == np.array([[0]])


