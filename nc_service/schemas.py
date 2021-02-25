from typing import List, Union

from pydantic import BaseModel


class PredictRequest(BaseModel):
    data: List[List[Union[int, str]]]


class PredictResponse(BaseModel):
    result: List[List[Union[int, str]]]


class ErrorResponse(BaseModel):
    message: str
