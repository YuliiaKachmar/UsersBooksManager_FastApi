from fastapi import FastAPI
import uvicorn

from Models import user_model
from db import engine
import routes


app = FastAPI()
app.include_router(routes.router)


def create_app():
    user_model.Base.metadata.create_all(bind=engine)
    return app


if __name__ == "__main__":
    app = create_app()
    uvicorn.run("app:app", port=9000, reload=True)
