import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from generate import get_hint


class HintModel(BaseModel):
    message: str


app = FastAPI()


@app.get(
    path="/hint",
    response_model=HintModel,
)
async def root():
    return {"message": get_hint()}


uvicorn.run(app, port=8080)
