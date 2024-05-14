from fastapi import FastAPI
import uvicorn

from app.schemas import LLMInput
def create_app() -> FastAPI:
    _app = FastAPI(title="team-llmm")
    return _app


app = create_app()


@app.on_event("startup")
async def startup():
    print("app started")


@app.on_event("shutdown")
async def shutdown():
    print("SHUTDOWN")


@app.get("/")
async def hello():
    return "Hello team llmm"


@app.post("/question-answering")
async def question_answering(input_request: LLMInput):
    print(input_request)

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=3928)