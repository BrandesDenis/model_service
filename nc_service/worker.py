import threading
from time import sleep
from dataclasses import dataclass
from typing import Tuple, List, Union

from model import model
from schemas import PredictResponse
from storage import storage, StorageRow


@dataclass
class Worker:
    delay: int = 5

    def start_worker(self):
        threading.Thread(target=self._consume_requests).start()

    def _consume_requests(self):
        while True:
            self._process_requests()
            self._delay()

    def _process_requests(self):
        storage_rows, merged_request_data = self._get_merged_request_data()
        if len(merged_request_data):
            predict_data = self._get_predict_data(merged_request_data)
            self._fill_responses_data(predict_data, storage_rows)

    def _get_merged_request_data(self) -> Tuple[List[Tuple[StorageRow, int]], List[List[Union[int, str]]]]:
        storage_rows = []
        merged_request_data = []
        for row in storage.get_requests():
            row_data = row.request.data
            merged_request_data += row_data
            storage_rows.append((row, len(row_data)))

        return storage_rows, merged_request_data

    def _get_predict_data(self, data: List[List[Union[int, str]]]) -> List[List[Union[int, str]]]:
        return model.predict(data)

    def _fill_responses_data(self,
                             data: List[List[Union[int, str]]],
                             storage_rows: List[Tuple[StorageRow, int]]):

        position = 0
        for storage_row_data in storage_rows:
            storage_row, len_ = storage_row_data
            end_position = position + len_
            storage_row.response = PredictResponse(result=data[position:end_position])

            position = end_position

    def _delay(self):
        sleep(self.delay)
