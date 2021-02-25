import uvicorn as uvicorn
from fastapi import FastAPI

from views import ModelPredictView
from worker import Worker


def init_app(app: FastAPI):
    Worker().start_worker()
    ModelPredictView().setup_app(app)


def get_app() -> FastAPI:
    app = FastAPI()
    init_app(app)

    return app


def start_app():
    uvicorn.run(get_app(), host="127.0.0.1", port=8000)


if __name__ == "__main__":
    start_app()
