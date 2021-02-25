from dataclasses import dataclass, field
from queue import Queue, Empty
from typing import Iterable

from schemas import PredictRequest, PredictResponse


@dataclass
class StorageRow:
    request: PredictRequest
    response: PredictResponse = field(init=False, default=None)


class Storage:
    def __init__(self):
        self._queue: Queue[StorageRow] = Queue()

    def add_request(self, req: PredictRequest):
        row = StorageRow(req)
        self._queue.put(row)

        return row

    def get_requests(self) -> Iterable[StorageRow]:
        while True:
            try:
                yield self._queue.get_nowait()
            except Empty:
                break


storage = Storage()
