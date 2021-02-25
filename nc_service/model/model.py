import asyncio
import logging
import time
from concurrent.futures.thread import ThreadPoolExecutor
from dataclasses import dataclass
from typing import Any, List, Union

from schemas import PredictResponse, PredictRequest
from .exeptions import ModelPredictError

logger = logging.getLogger(__name__)


@dataclass
class MLModel:
    model: Any
    max_workers: int = 10

    def __post_init__(self):
        self._executor = ThreadPoolExecutor(self.max_workers)

    def predict(self, data: List[List[Union[int, str]]]) -> List[List[Union[int, str]]]:
        try:
            return self.model.predict(data).tolist()
        except Exception as e:
            raise ModelPredictError(e)

    async def predict_async(self, pr_req: PredictRequest) -> PredictResponse:
        return await asyncio.get_running_loop().run_in_executor(self._executor, self._predict_async, pr_req)

    def _predict_async(self, pr_req: PredictRequest) -> PredictResponse:
        logger.info(f'The model starts processing input data')
        start_time = time.time()

        try:
            prediction = PredictResponse(result=self.model.predict(pr_req.data).tolist())
        except Exception as e:
            logger.error(f'error predicting data')
            raise ModelPredictError(e)

        logger.info(f'The model finished processing input data'
                    f'Time: {start_time - time.time():.2f}')

        return prediction
