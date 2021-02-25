import logging
from asyncio import sleep

from fastapi import FastAPI, APIRouter

from model import get_model, model
from schemas import PredictRequest, PredictResponse
from storage import storage

logger = logging.getLogger(__name__)


class ModelPredictView:

    async def predict(self, data: PredictRequest) -> PredictResponse:
        return await model.predict_async(data)

    async def predict_delayed(self, data: PredictRequest) -> PredictResponse:
        storage_row = storage.add_request(data)
        while True:
            if storage_row.response is None:
                await sleep(0.2)
            else:
                return storage_row.response

    def setup_app(self, app: FastAPI):
        router = APIRouter()

        router.add_api_route('/predict', self.predict, response_model=PredictResponse, methods=['POST'])
        router.add_api_route('/predict_delayed', self.predict_delayed, response_model=PredictResponse, methods=['POST'])

        app.include_router(router)
