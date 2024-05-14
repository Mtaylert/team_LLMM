from fastapi import FastAPI
import uvicorn
from app.schemas import LLMInput
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="team-llmm")

# Initialize OpenAI client with API key from environment variable
client = OpenAI(api_key='key')


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
    openai_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": input_request.input_question},
        ]
    )
    response = openai_response.choices[0].message.content

    return response




if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=3928)