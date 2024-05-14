from fastapi import FastAPI
import uvicorn
from app.schemas import LLMInput
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="team-llmm")

# Initialize OpenAI client with API key from environment variable
client = OpenAI(api_key='')


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


def scraper():
    pass


def dynamic_chunking():
    return ""


def semantic_chunking():
    return ""


def basic_chunking():
    return ""


@app.post("/question-answering")
async def question_answering(input_request: LLMInput):


    if input_request.chunking_type == 'dynamic_chunking':
        chunk = dynamic_chunking()
    elif input_request.chunking_type == 'semantic_chunking':
        chunk = semantic_chunking()
    elif input_request.chunking_type == 'basic_chunking':
        chunk = basic_chunking()

    prompt = f"""You are a helpful assistant. Use the content provided to answer the inquiries
    
    CONTENT:
    
    {chunk}
    """

    openai_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": input_request.input_question},
        ]
    )
    response = openai_response.choices[0].message.content

    return response




if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=3928)